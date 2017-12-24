import os
import io
import json
import csv
import requests
from get_data import loop_download
from get_data import handle_simple_q

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
    with open('conf/conf.json') as f:
        conf = json.load(f)
        app.config['PORT'] = conf['PORT']
        app.config['DEBUG_LEVEL'] = conf['DEBUG_LEVEL']
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
    from pprint import pprint
    # simple or advanced query
    simple_q = str(request.form.get('main_query'))
    advanced_q = str(request.form.get('query-advanced'))
    
    if simple_q:
        main = request.form.get('main_query')
        query = str(main)
        size = int(request.form.get('size'))
        print(main)
        # filters
        tags= request.form.get('tags')
        domain = request.form.get('domain')
        source_publisher = request.form.get('source_publisher')
        lang = request.form.get('lang')
        date = request.form.get('lang')
        # if date:
        #     date_start = request.form.get('date_start')
        #     date_end = request.form.get('date_end')
        query_ready = handle_simple_q(main, size, tags, domain, source_publisher, lang, date)
        print('#### -> ', query_ready)
        print('#### -> ', type(query_ready))
        bucket_data = loop_download(query_ready)
        
    elif advanced_q: 
        # prepare query
        q = json.loads(advanced_q)
        query = str(q['query']['query_string']).replace(" ","_")
        # download query
        bucket_data = loop_download(advanced_q)
    
    # choose between CSV or JSON
    datatype = request.form.get('datatype')
    if datatype == 'json':
        return jsonify(bucket_data)

    elif datatype == 'csv':
        keys = list(bucket_data[0]['_source'])

        # parse data for csv
        bucket_data_csv = []
        for x in bucket_data:
            bucket_data_csv.append(x['_source'])
            # retrieve all keys existing and remove if duplicated (for csv)
            if x.keys() not in keys:
                keys.extend(x['_source'].keys())
                keys = set(keys)
                keys = list(keys)

        # write csv & data
        output = io.StringIO()
        writer = csv.DictWriter(output, keys)
        writer.writeheader()
        for x in bucket_data_csv:
            writer.writerow(x)
        csvdata = output.getvalue()
        return Response(
            csvdata,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename="+query+".csv"})
    
    else:
        return render_template('home.html')


##########################################################################
# Start
##########################################################################
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=app.config['DEBUG_LEVEL'], host='0.0.0.0', port=app.config['PORT'], threaded=True)
