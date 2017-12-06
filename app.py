import os
import io
import json
import csv
import requests
import get_data

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import Response
from flask import jsonify
from flask_bootstrap import Bootstrap

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

try:
	app = create_app()    
except BaseException as error:
	print('An exception occurred : {}'.format(error))

@app.route("/")
def hello():
	return render_template('home.html')

@app.route("/processing", methods=['POST', 'GET'])
def processing():
	# simple or advanced query
	simple = str(request.form.get('simple'))
	advanced = str(request.form.get('advanced'))
	print(simple)
	print(advanced)

	# filters
	# infinite = request.form.get('infinite')
	#size = int(request.form.get('size'))
	# date = request.form.get('date')
	
	# prepare query
	output_file = str(query.replace(" ","_"))
	bucket_data = []

	# package everything 
	#info = {
	#	"QUERY" : query,
	#	"SIZE" : size,
	#	"DATA" : bucket_data
	#}	

	# choose between CSV or JSON
	datatype = request.form.get('datatype')
	
	if datatype == 'json':
		buckets_data = loop_download(QUERY)


		return jsonify(buckets_data)

	elif datatype == 'csv':
		keys = bucket_data[0].keys()
		output = io.StringIO()

		dict_writer = csv.DictWriter(output, keys)
		dict_writer.writeheader()
		dict_writer.writerows(bucket_data)
		csvdata = output.getvalue()
		return Response(
			csvdata,
			mimetype="text/csv",
			headers={"Content-disposition":
					 "attachment; filename="+query+".csv"})
	
	else:
		return render_template('home.html')
	# request.form.get('date_end')


##########################################################################
# Start
##########################################################################
if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD']=True
	app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)

