from flask import Flask, request
import multiprocessing
from helpers import process_job 
import redis
from model import connect_to_db, db 

# ------------------------------------------------- #

app = Flask(__name__)
# creates incrementer for job IDs
r = redis.StrictRedis()
r.set('curr_id', 0)

# If there is work in the queue, do it (on app start)
p = multiprocessing.Process(target=process_job)
p.start()

@app.route("/add_job", methods=['POST'])
def add_task():
    """add job to the queue, initiate web scraping process"""
    # user passes URL to route
    url = request.args.get('url')
    # I chose to use redis, so the queue could be accessed by helper functions,
    # since Flask is stateless across processes
    r = redis.StrictRedis()
    # increment job id counter
    job_id = r.incr('curr_id')
    # add new job to queue
    r.hset('urls', job_id, url)
    r.hset('status', job_id, 'processing')
    r.rpush('job_queue', job_id)

    return 'job ID:{}'.format(job_id)

@app.route("/check_id")
def check_job():
    """check job status, if done, return page source"""
    job_id = request.args.get('id')
    # if job is complete, return html
    if r.hget('status', job_id) == 'complete':
        return Sites.query.get(job_id).html
    # else return processing message
    return 'Processing'
# ------------------------------------------------- #

if __name__ == "__main__":
    connect_to_db(app)
    app.run(port=8080)