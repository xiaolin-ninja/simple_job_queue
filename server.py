from flask import Flask, request
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

# If there is work in the queue, do it (on app start)

# based on the example, I'm going to assume the user must submit
# the url as 'www.site.com' without the http:// header
@app.route("/add_job/<site>", methods=['POST'])
def add_task(site):
    """add job to the queue, initiate web scraping process"""
    # user passes URL to route
    print('user input:', site)
    # I chose to use redis, so the queue could be accessed by helper functions,
    # since Flask is stateless across processes
    r = redis.StrictRedis()
    # increment job id counter
    job_id = r.incr('curr_id')
    # add http header
    url = 'http://' + site
    r.hset('urls', job_id, url)
    # add new job to queue
    r.hset('status', job_id, 'processing')
    r.rpush('job_queue', job_id)

    p = multiprocessing.Process(target=process_job)
    p.start()

    return 'job ID:{}'.format(job_id)

@app.route("/status/<job_id>")
def check_job(job_id):
    """check job status, if done, return page source"""
    # if job is complete, return html
    print('job_id:', job_id)
    print('status:', r.hget('status', job_id))
    if r.hget('status', job_id).decode("utf-8") == 'complete':
        url = r.hget('urls', job_id).decode("utf-8")
        print('URL:', url)
        return Site.query.filter_by(url=url).first().html
    # else return processing message
    return 'Processing'
# ------------------------------------------------- #

if __name__ == "__main__":
    connect_to_db(app)
    if len(sys.argv) >1:
        db.create_all()
    app.run(port=8080)