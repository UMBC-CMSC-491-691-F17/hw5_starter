#!/usr/bin/env python

""" A simple script to run one or more sparql queries on an endpoint and save the results as json and html. Examples

  python sparql.py http://dbpedia.org/sparql myquery.txt
  python sparql.py q*.txt  

First argument is endpoint if it looks like a URL, remaining args are names of files with SPARQL queries. Sends query in file F to the endpoint and writes results to files F.json and F.html

"""

# so this will run in python 3 and 2.x
from __future__ import print_function

import sys, urllib, json

usage = """USAGE: python sparql.py [endpoint] q1file q2file ... qnfile"""

default_endpoint = "http://live.dbpedia.org/sparql"
# default_endpoint = "http://dbpedia.org/sparql"

default_format = "application/json"

def ask_query(query, endpoint=default_endpoint, format=default_format):
    params={"query":query, "format":format, "default-graph":"",     
            "debug":"on", "timeout":"", "save":"display", "fname":"" }
    try:
        response = urllib.urlopen(endpoint, urllib.urlencode(params)).read()
        return json.loads(response)        
    except:
        return None

def number_results (json_obj):
    """ Returns the number of results in a json object returned by a
    sparql endpoint """
    if 'head' in json_obj:
        # the json is from a select sparql query
        return len(json_obj['results']['bindings'])
    else:
        # the json is from a construct sparql query
        return len(json_obj)
                  
def json2html(data):
    """ Constructs an HTML table string from a json object resulting from a sparql query"""
    html = ''
    if 'head' in data:
        # the json is from a select sparql query
        vars = data['head']['vars']
        html = '<thead><tr>' + ''.join(['<th> %s </th>' % v for v in vars]) + '</tr></thead><tbody>'
        html = html.encode('utf-8')
        for result in data['results']['bindings']:
            html += '<tr>' + ''.join(['<td>'+linkify(result.get(v,{}).get('value', ''))+'</td>' for v in vars]) + '</tr>'
        html += '</tbody>'
    else:
        # the json is from a construct sparql query
        for (s, po) in data.items():
            for (p, objs) in po.items():
                for o in objs:
                    html += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (linkify(s), linkify(p), linkify(o['value']))

    return '<table border="1">' + html + '</table>'

def linkify(string):
    """ if string looks like a URI, turn it into a link """
    result = '<a href="%s">%s</a>' % (string, string) if string.startswith('http://') else string
    return result.encode('utf-8')

        
def ask_and_write(file, endpoint):
    print('query {}'.format(file))
    data = ask_query(open(file).read(), endpoint)
    if data:
        with open(file+".html", 'w') as HOUT, open(file+".json", 'w') as JOUT:
            print('Query returned {} results'.format(number_results(data)))
            JOUT.write(json.dumps(data))
            HOUT.write("<html><body>"+json2html(data)+"</body></html>")
    else:
        print('Query {} failed'.format(file))

    print('')
        
def main():
    """If run as a script, invoke this"""
    if len(sys.argv) < 2:
        sys.exit(usage)
    elif sys.argv[1].lower().startswith('http'):
        endpoint = sys.argv[1]
        files = sys.argv[2:]
    else:
        endpoint = default_endpoint
        files = sys.argv[1:]
    for file in files:
        ask_and_write(file, endpoint)
        
if __name__ == "__main__":
    main()

