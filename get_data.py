#!/usr/bin/env python
import requests
import json

def get_config():
    with open('conf/conf.json') as f:
            conf = json.load(f)
            VENDOR = conf['VENDOR']
            VENDOR_AUTH = conf['VENDOR_AUTH']

    headers = { 'X-vendor': VENDOR,
              'X-vendor-auth': VENDOR_AUTH }

    return VENDOR,VENDOR_AUTH, headers


def handle_data(page, response):
    file_name="data/" + MAIN_REQUEST + "%04d.json" % page
    print("Writing JSON data to: %s" % file_name)
    f=open( file_name, "w" );
    f.write( response.text )
    f.close()

def handle_simple_q(main, size, tags, domain, source_publisher, lang, date):
    q = {}
    q['query'] = { 'query_string': { 'query' : 'main:' + main }}
    q['size'] = size
    
    if tags or domain or source_publisher or lang:
        query_filters = []

        if tags:
            query_tags_str = '(' + tags + ')'
            query_filters.append(query_tags_str)
        if domain:
            query_domain_str = '(' + domain + ')'
            query_filters.append(query_domain_str)
        if source_publisher:
            query_source_publisher_str = '(source_publisher_type:' + source_publisher + ')'
            query_filters.append(query_source_publisher_str)
        if lang:
            query_lang_str = '(' + lang + ')'
            query_filters.append(query_lang_str)
                
        query = ' AND '.join(query_filters)
        q['filter'] = { 'query': { 'query_string' : { 'query' : str(query) } }}
    q = json.dumps(q)
    return q


def download(QUERY):    
    VENDOR,VENDOR_AUTH, headers = get_config()
    ###
    # Perform the first request.  The URL needs to be slightly different because
    # we have to specify the index name here.

    url='http://%s.elasticsearch.spinn3r.com/content*/_search?scroll=5m&pretty=true' % VENDOR
    print("Fetching from %s" % url)
    print("Running query: ")
    print(QUERY)

    ## we have to add our vendor code information to the request now.
    headers = { 'X-vendor': VENDOR,
    'X-vendor-auth': VENDOR_AUTH }
    
    try:
        response = requests.post( url, headers=headers, data=QUERY )
        print(response)
    except requests.exceptions.HTTPError as e:  # This is the correct syntax
        print(e)

    
#    response = requests.post( url, headers=headers, data=QUERY )
    data=json.loads(response.text)
    print("Query took: %sms" % data["took"])
    print("Total hits: %s" % data["hits"]["total"])

    return response


def loop_download(QUERY):
    VENDOR,VENDOR_AUTH, headers = get_config()
    NUMBER_OF_PAGES=json.loads(QUERY)['size']
    response = download(QUERY)

    # get scroll_id for next page
    data=json.loads(response.text)
    scroll_id = data["_scroll_id"]

    # prepare adding all data together and first response
    bucket_data = response.json()['hits']['hits']
    print('total len is : ', len(bucket_data))
    count = 0
    for page in range( 1, NUMBER_OF_PAGES):
        count += 1
        print(count)

        url='http://%s.elasticsearch.spinn3r.com/_search/scroll?scroll=5m&pretty=true' % VENDOR
        try:
            response = requests.post( url, headers=headers, data=scroll_id )
            print(response)
        except requests.exceptions.HTTPError as e:  # This is the correct syntax
            print(e)
#        response = requests.post( url, headers=headers, data=scroll_id )
        scroll_id = response.json()["_scroll_id"]
        
        if not response.json()['hits']:
            print('end of dataset')
            break
        else:
            bucket_data += response.json()['hits']['hits'] 
        print('--------------------------------------------')

    


    print('===============================================')
    print('total len AFTER is : ', len(bucket_data))
    
    return bucket_data


