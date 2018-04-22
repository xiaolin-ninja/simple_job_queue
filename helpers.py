import requests
from model import Sites, db
import redis

# ------------------------------------------------- #

def process_job():
	"""processes url web scraping request
	If process has been done before, get result from database
	Otherwise, process and add data to database"""
	r = redis.StrictRedis()

	curr_job = r.blpop('job_queue', 0)
	print(curr_job)
	url = r.hget('urls', curr_job)
	# add http header
	print(url)
	if url[:4] != 'http':
		url = 'http://' + url

	# if this url has not been requested before, the query is falsy
	if not Sites.query.filter_by(url=url).first():
		# fetches url page source
		html = get_html(url)
		# add to database
		db.session.add(Sites(url=url, html=html))
		db.session.commit()
	# complete job
	r.hset('status', curr_job, 'complete')
	return

def get_html(url):
	"""scrapes html page source of url"""
	# declaring this helper function isn't necessary for now, 
	# but if we want to further parse the page then it is useful
	return request.get(url).content