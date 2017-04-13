#!/usr/bin/python2.7

import sys
sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')

from flask import Flask, jsonify
app = Flask('neo4jTest')

from config import GRAPH_URL

from py2neo import Graph, Node, Relationship, Path

try:
	graph = Graph(GRAPH_URL)
except Exception as e:
	print `e`
	exit(0)


def search2ndDegree(id):
	# Also check it's not 1st degree connection
	cmd = "MATCH (p:Person)-[:CONNECTS_TO]-(st)-[:CONNECTS_TO]-(nd) WHERE p.id = " + str(id) + \
		" AND NOT (p)-[:CONNECTS_TO]-(nd) RETURN DISTINCT nd.id"
	res = graph.data(cmd)
	return [ x['nd.id'] for x in res ]


def search3rdDegree(id):
	# Also check it's not 1st degree connection
	cmd = "MATCH (p:Person)-[:CONNECTS_TO]-(st)-[:CONNECTS_TO]-(nd)-[:CONNECTS_TO]-(rd) WHERE p.id = " + \
		str(id) + " AND NOT (p)-[:CONNECTS_TO]-(nd) AND NOT (p)-[:CONNECTS_TO]-(rd) RETURN DISTINCT rd.id"
	res = graph.data(cmd)
	return [ x['rd.id'] for x in res ]


def search2nd3rdDegreeConnections(id):
	result2 = search2ndDegree(id)
	result3 = search3rdDegree(id)
	return list(set(result2 + result3))


def check2nd3rdDegreeConnection(id_1, id_2):
	cmd = "MATCH path=(p1:Person)-[r:CONNECTS_TO*2..3]-(p2:Person) WHERE p1.id=" + str(id_1) + " AND p2.id=" + str(id_2) + \
		" AND NOT (p1)-[:CONNECTS_TO]-(p2) RETURN count(path) AS p"
	res = graph.data(cmd)
	return (res[0]['p'] > 0)


@app.route('/2nd3rdDegree/<int:id>')
def search23d(id):
	return jsonify(search2nd3rdDegreeConnections(id))


@app.route('/2nd3rdDegree/<int:id_1>/<int:id_2>')
def check23d(id_1, id_2):
	return jsonify(check2nd3rdDegreeConnection(id_1, id_2))


if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = 3030)
