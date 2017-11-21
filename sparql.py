#!/usr/bin/env python

""" A simple script to run one or more sparql queries on an endpoint and save the results as json and html. Examples

  python sparql.py http://dbpedia.org/sparql myquery.txt
  python sparql.py q*.txt  

First argument is endpoint if it looks like a URL, remaining args are names of files with SPARQL queries. Sends query in file F to the endpoint and writes results to files F.json and F.html

"""

# so this will run in python 3 and 2.x
from __future__ import print_function

import sys, json
import urllib
# urllib has been reorganized in python3
if sys.version_info[0] < 3:
    from urllib import urlopen, urlencode
else:
    from urllib.request import urlopen
    from urllib.parse import urlencode

usage = """USAGE: python sparql.py [endpoint] q1file q2file ... qnfile"""

default_endpoint = "http://live.dbpedia.org/sparql"
# default_endpoint = "http://dbpedia.org/sparql"

default_format = "application/json"

def ask_query(query, endpoint=default_endpoint, format=default_format):
    params={"query":query, "format":format, "default-graph":"",     
            "debug":"on", "timeout":"", "save":"display", "fname":"" }
    try:
        response = urlopen(endpoint, urlencode(params).encode("utf-8")).read()
        return json.loads(response.decode("utf-8") )
    except:
        raise
        return None

def number_results (json_obj):
    """ Returns the number of results in a json object returned by a
    sparql endpoint """
    if not json_obj:
        return 0
    elif 'head' in json_obj:
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

        for result in data['results']['bindings']:
            result_values = [linkify(result.get(v,{}).get('value', '')) for v in vars]
            html += '<tr>' + ''.join(['<td>'+ rv + '</td>' for rv in result_values]) + '</tr>'
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
    #return result.encode('utf-8')
    return result

        
def ask_and_write(file, endpoint):
    print('query {0}'.format(file))
    data = ask_query(open(file).read(), endpoint)
    if data:
        print('Query returned {0} results'.format(number_results(data)))
        with open(file+".html", 'w') as HOUT:
            HOUT.write("<html><body>"+json2html(data)+"</body></html>")
        with open(file+".json", 'w') as JOUT:
            JOUT.write(json.dumps(data))
    else:
        print('Query {0} failed'.format(file))
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

