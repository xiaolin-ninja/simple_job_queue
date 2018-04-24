from flask import Flask, request, jsonify
import multiprocessing
from helpers import process_job 
import redis
from model import Site, connect_to_db, db 
import sys

# ------------------------------------------------- #

app = Flask(__name__)
# creates incrementer for job IDs
r = redis.StrictRedis()
r.set('curr_id', 0)


# based on the example, I'm going to assume the user must submit
# the url as 'www.site.com' without protocol headers, 
@app.route("/new/<site>", methods=['POST'])
def add_task(site):
    """add job to the queue, initiate web scraping process"""

    # I chose to use redis, so the queue could be accessed by helper functions,
    # since Flask is stateless across processes
    r = redis.StrictRedis()
    # increment job id counter
    job_id = r.incr('curr_id')
    # add http header, assume all jobs will be http:// for the sake of simplicity
    url = 'http://' + site
    # redis hash to keep track of jobs
    r.hset('urls', job_id, url)
    # redis hash to keep track of job statuses
    r.hset('status', job_id, 'pending')
    # redis list job queue
    r.rpush('job_queue', job_id)

    # returns job ID to user
    return jsonify({'job ID' : job_id})

@app.route("/status/<job_id>")
def check_job(job_id):
    """check job status, if done, return page source"""

    # convert from byte to unicode
    if r.hget('status', job_id).decode("utf-8") == 'timeout':
        return 'Request timed out'
    # for now we only abort because of large response
    if r.hget('status', job_id).decode("utf-8") == 'abort':
        return 'Response too large, limit 1MB'
    if r.hget('status', job_id).decode("utf-8") == 'complete':
        # if job status is done, retrieve url attached to job ID
        url = r.hget('urls', job_id).decode("utf-8")
        # query database of past successful scrapes
        return Site.query.filter_by(url=url).first().html
    
    # if job not complete, return processing message
    return 'Processing'
# ------------------------------------------------- #

if __name__ == "__main__":
    connect_to_db(app)
    if len(sys.argv) >1:
        db.create_all()
    for x in range(10):
        # start 10 workers in the background
        p = multiprocessing.Process(target=process_job)
        p.start()
    app.run(port=8080)