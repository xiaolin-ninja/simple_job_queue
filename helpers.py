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
        if not Site.query.filter_by(url=url).first():
            # fetches url page source
            try:
                html = str(get_html(url)).decode("utf-8")
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
    return

def get_html(url):
    """Fetches html page source of url"""
    print('fetching', url)
    r = requests.get(url, timeout=1, stream=True)
    # limit file size to 1mb
    html = r.raw.read(1000000+1, decode_content=True)
    if len(html) > 1000000:
        raise ValueError('response too large')

    return html