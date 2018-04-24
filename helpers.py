import redis
from model import Site, db
import urllib
import requests

# ------------------------------------------------- #

def process_job():
    """processes url web scraping request
    If process has been done before, get result from database
    Otherwise, process and add data to database"""
    r = redis.StrictRedis()
    while True:
        curr_job = r.blpop('job_queue', 0)[1]
        r.hset('status', curr_job, 'processing')
        print('current job ID:', curr_job)
        # convert byte to string
        url = r.hget('urls', curr_job).decode("utf-8")
        print('Current URL:', url)

        # if this url has not been requested before/is not in the db
        if Site.query.filter_by(url=url).first():
            r.hset('status', curr_job, 'complete')
        else:
            # fetches url page source
            try:
                html = get_html(url).decode("utf-8")
                print('Successfully retrieved HTML')
            # add results to database
                db.session.add(Site(url=url, html=html))
                db.session.commit()
                print('Added to database')
                r.hset('status', curr_job, 'complete')
            except ValueError:
                r.hset('status', curr_job, 'abort')
            except TimeoutError:
                r.hset('status', curr_job, 'timeout')
        # update job status
        print('Job', curr_job, 'Completed')

def get_html(url):
    """Fetches html page source of url"""
    print('fetching', url)
    try:
        r = requests.get(url, timeout=30, stream=True)
        html = r.raw.read(10000000+1, decode_content=True)
        # limit file size to 10mb
        if len(html) > 10000000:
            raise ValueError('response too large')
        return html
    except:
        raise TimeoutError('request timed out')
    