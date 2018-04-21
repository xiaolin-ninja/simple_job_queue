from flask import Flask, request, json

# ------------------------------------------------- #

app = Flask(__name__)

@app.route("/", methods=['POST'])
def status_timer():
	"""Takes in state changes data of a test run 
		and returns time spent on each state.
		>>> time_states('test-runs.json')
		{ "pending_seconds": 1,
		  "creating_seconds": 3,
		  "building_seconds": 10,
		  "running_seconds": 20
		}
	"""

	if request.headers['Content-Type'] != 'application/json':
		return 'Error, please pass webhooks data as json'

	# the parser returns a list of tuples where:
	# tuple[0] = status, tuple[1] = start time, tuple[2] = end time
	data = parse_webhooks(request.json)
	# I decided to make the dictionary separately instead of 
	# within the for loop to maintain the desired order
	state_times = {
				  'pending_seconds': 0,
				  'creating_seconds': 0,
				  'building_seconds': 0,
				  'running_seconds': 0
				  }

	# loop through each tuple
	for d in data:
		# d[0] is the status message
		status = d[0]
		# convert to integer to match formatting of sample answer
		time = int((convert_UTC(d[2]) - convert_UTC(d[1])).total_seconds())
		# aggregate time spent in each testing stage
		if status == 'pending':
			state_times['pending_seconds'] += time
		elif status == 'creating':
			state_times['creating_seconds'] += time
		elif status == 'building':
			state_times['building_seconds'] += time
		elif status == 'running':
			state_times['running_seconds'] += time
		else:
			return 'error, status not found'

	# I couldn't figure out how to get the output to pretty print as an ordered dictionary
	# According to Google, there's a Python bug that has trouble pretty printing ordered dictionaries
	# The docs says the following should do it, but a) it doesn't and b) it intuitively shouldn't... since json renders unordered.

	# return json.dumps(OrderedDict(state_times), indent=4)

	# the best I can do now is print in console
	print(json.dumps(state_times, indent=4))
	state_times = str(state_times)
	json_time = json.dumps(state_times)
	# returns json on one line, not pretty printed
	return json.loads(json_time)

	# After spending 1 hour on trying to pretty print, I decided 'done is better than perfect.'
	# I tried pprint, adding the indent option to json.dumps(), scoured the docs and couldn't figure it out
	# I tried jsonify, OrderedDict... it seems to be a pretty-printed and out of order, or pretty-printed and in order tradeoff
	# It seems like a simple syntax thing or a module I just haven't seen, so please teach me.


# ------------------------------------------------- #

app.run(port=8080)