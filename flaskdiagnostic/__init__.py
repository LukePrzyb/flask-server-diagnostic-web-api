# Flask Blueprint
# Used to separate concerns with flask routes
# Good for portability too.

from flask import Blueprint, render_template, abort, current_app, request, jsonify
from jinja2 import TemplateNotFound
import psutil, datetime, subprocess

# Credits: https://github.com/giampaolo/psutil/blob/master/scripts/meminfo.py
def bytes2human(n):
	# http://code.activestate.com/recipes/578019
	# >>> bytes2human(10000)
	# '9.8K'
	# >>> bytes2human(100001221)
	# '95.4M'
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n

# Setup routes in another library with blueprint
# Good for separation of concerns
callers = Blueprint('callers', __name__)

# psutil approach to diagnostic info
@callers.route('/diagnosticsTest', methods=['GET'])
def getSystemInfo():
	assert current_app.config['AUTH_TOKEN'], 'No Authentication Token provided'

	# To avoid malicious intent, check the token passed or else we return a default 404
	if current_app.config['AUTH_TOKEN'] != request.args.get('token'):
		abort(404)

	memory_information=psutil.virtual_memory()		# Actual Memory
	swap_information=psutil.swap_memory()			# Swap Memroy
	cpu_logical=psutil.cpu_count()					# CPU Logical Count
	cpu_real=psutil.cpu_count(logical=False)		# CPU Real Count
	server_users=psutil.users()						# Current Users logged in
	last_boot=datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")		# Last started

	memory_data={}

	# Convert to dictionary
	for entry in memory_information._fields:
		if entry != "percent":
			memory_data[entry]=bytes2human(getattr(memory_information,entry))
		else:
			memory_data[entry]=getattr(memory_information,entry)

	swap_data={}

	# Convert to dictionary
	for entry in swap_information._fields:
		if entry != "percent":
			swap_data[entry]=bytes2human(getattr(swap_information,entry))
		else:
			swap_data[entry]=getattr(swap_information,entry)

	for ind, user in enumerate(server_users):
		server_users[ind] = user.name

	output={
		'physical_memory':memory_data,
		'swap_memory':swap_data,
		'cpu_count':{
			'logical':cpu_logical,
			'real':cpu_real
		},
		'last_boot': last_boot,
		'login_users':server_users
	}

	return jsonify(output)

# Bash approach to diagnostic info
@callers.route('/diagnostics', methods=['GET'])
def get_tasks():
	assert current_app.config['AUTH_TOKEN'], 'No Authentication Token provided'

	# To avoid malicious intent, check the token passed or else we return a default 404
	if current_app.config['AUTH_TOKEN'] != request.args.get('token'):
		abort(404)

	# Call shell for diagnostic information available to bash
	proc = subprocess.Popen(['./diagnostics.sh'], stdout=subprocess.PIPE, shell=False)

	# get output
	(output,errors) = proc.communicate()

	if errors:
		print("Error:")
		print(errors)
		print("Default aborting.")
		abort(404)

	# Decode bytes and split by double newline for
	# individual sections based on bash script
	output=output.decode('utf-8')
	output=output.strip().split("\n\n")

	# Parse Memory information
	holder=output[0].strip().split('\n')

	final_output={}
	final_output[holder[0]]={}

	for j,y in enumerate(holder[1:]):
		hold2 = y.split(":")
		print(hold2)
		hold2[1] = hold2[1].split('|')

		tempDict={}

		for z in hold2[1]:
			z=z.split(",")
			tempDict[z[0]]=z[1]

		final_output[holder[0]][hold2[0]]=tempDict


	# Parse Filesystem information
	holder=output[1].strip().split('\n')

	final_output[holder[0]]=[]

	tmp = []

	for i,x in enumerate(holder[1:]):
		x=x.split("|")

		tempDict={}

		for z in x:
			z=z.split(",")

			tempDict[z[0]]=z[1]


		x=tempDict

		final_output[holder[0]].append(x)

	# Send
	return jsonify(final_output)