import redis
from model import Site, db
import urllib

# ------------------------------------------------- #

def process_job():
	"""processes url web scraping request
	If process has been done before, get result from database
	Otherwise, process and add data to database"""
	r = redis.StrictRedis()

	curr_job = r.blpop('job_queue', 0)[1]
	print('current job ID:', curr_job)
	# convert byte to string
	url = r.hget('urls', curr_job).decode("utf-8")
	print('Current URL:', url)

	# if this url has not been requested before, the query is falsy
	if not Site.query.filter_by(url=url).first():
		# fetches url page source
		html = str(get_html(url))
		print('Successfully retrieved HTML')
		# add to database
		db.session.add(Site(url=url, html=html))
		db.session.commit()
		print('Added to database')
	# complete job
	r.hset('status', curr_job, 'complete')
	print('Job', curr_job, 'Completed')
	return

def get_html(url):
	"""scrapes html page source of url"""
	# declaring this helper function isn't necessary for now, 
	# but if we want to further parse the page then it is useful
	html = urllib.request.urlopen(url).read()
	return html