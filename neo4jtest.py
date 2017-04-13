#!/usr/bin/python2.7

import sys
sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')

from flask import Flask
from py2neo import Graph, Node, Relationship, Path
import N2nd3rdDegree 
from config import GRAPH_URL

graph = None

def sieve(n):
	sieve = [True] * (n + 1)
	sieve[0] = sieve[1] = False
	i=2
	while (i * i <= n):
		if (sieve[i]):
			k = i * i
			while (k <= n):
				sieve[k] = False
				k += i
		i += 1
	primes = []
	for c in xrange(n+1):
		if sieve[c]:
			primes.append(c)
	return primes


# Create random users
def createRandomUsers(qty):
	# People
	people = [ None ] * qty

	tx = graph.begin()
	# Create qty random users
	for c in range(0, qty):
		if c % 100000 == 0:
			tx.commit()
			tx = graph.begin()
		print "User: " + `c+1`
		people[c] = Node("Person", id=c+1)
		tx.create(people[c])
	tx.commit()

	primes = sieve(qty)

	tx = graph.begin()
	# Connect users with prime ID with users with previous ID and with its opposite in primes's list
	c = 0
	for p in primes:
		if c % 100000 == 0:
			tx.commit()
			tx = graph.begin()
		tx.create(Relationship(people[p-1], "CONNECTS_TO", people[p-2]))
		tx.create(Relationship(people[p-1], "CONNECTS_TO", people[primes[len(primes)-c-1]]))
		print "(" + `p` + " -> " + `primes[len(primes)-c-1]` + ")",
		c += 1
	tx.commit()

	print '\nConnecting odd IDs'
	tx = graph.begin()
	# Path between users with odd ID 
	c = 1
	while c < qty - 2:
		if c % 100001 == 0:
			tx.commit()
			tx = graph.begin()
		tx.create(Relationship(people[c-1], "CONNECTS_TO", people[c+1]))
		print "(" + `c` + " -> " + `c+2` + ")",
		c += 2
	tx.commit()

	print '\nConnecting even IDs'
	tx = graph.begin()
	# Path between users with even ID 
	c = 2
	while c < qty - 2:
		if c % 100000 == 0:
			tx.commit()
			tx = graph.begin()
		tx.create(Relationship(people[c-1], "CONNECTS_TO", people[c+1]))
		print "(" + `c` + " -> " + `c+2` + ")",
		c += 2
	tx.commit()

	cmd = "CREATE INDEX ON :Person(id)"
	graph.data(cmd)


# Create mini sample data using py2neo Node and Relationship
def createMSDpy2neo():
	# Init transactions
	tx = graph.begin()

	# People
	people = [ None ] * 11

	# Create persons
	for c in range(0, 10):
		people[c] = Node("Person", id=c+1)
		tx.create(people[c])

	# Create custom relationships
	tx.create(Relationship(people[9], "CONNECTS_TO", people[0]))
	tx.create(Relationship(people[0], "CONNECTS_TO", people[1]))
	tx.create(Relationship(people[0], "CONNECTS_TO", people[2]))
	tx.create(Relationship(people[0], "CONNECTS_TO", people[3]))
	tx.create(Relationship(people[1], "CONNECTS_TO", people[2]))
	tx.create(Relationship(people[1], "CONNECTS_TO", people[3]))
	tx.create(Relationship(people[1], "CONNECTS_TO", people[4]))
	tx.create(Relationship(people[3], "CONNECTS_TO", people[2]))
	tx.create(Relationship(people[3], "CONNECTS_TO", people[4]))
	tx.create(Relationship(people[3], "CONNECTS_TO", people[6]))
	tx.create(Relationship(people[4], "CONNECTS_TO", people[5]))
	tx.create(Relationship(people[5], "CONNECTS_TO", people[8]))
	tx.create(Relationship(people[6], "CONNECTS_TO", people[7]))
	tx.create(Relationship(people[7], "CONNECTS_TO", people[8]))

	# Commit transaction
	tx.commit()


def dropDB(max):
	c = 100000
	while c < max:
		cmd = "MATCH (n) WHERE n.id <= " + str(c) + " DETACH DELETE n"
		print cmd
		graph.data(cmd)
		c += 100000
	cmd = "MATCH (n) WHERE n.id <= " + str(max) + " DETACH DELETE n"
	print cmd
	graph.data(cmd)

	
def use():
	print "Use {} <COMMAND> <PARAMS>".format(sys.argv[0])
	print "List of Commands:"
	print "    MINIINIT: Create a know database for testing"
	print "    INIT: Create a random database of 2 millions random users"
	print "        Param: Amount of users to create"
	print "    DROP: Delete database"
	print "        Param: Amount of users to delete"
	print "    LIST: List of user ids of 2nd/3rd degree connections for USERID"
	print "        Param: USERID"
	print "    CHECK: Check if USERID1 and USERID2 are in 2nd/3rd degree connection"
	print "        Param: USERID1 USERID2"
	exit(0)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		use()
	try:
		graph = Graph(GRAPH_URL)
	except Exception as e:
		print `e`
		exit(0)

	cmd = sys.argv[1]
	if cmd == "LIST":
		if len(sys.argv) < 3:
			use()
		id1 = sys.argv[2]
		res = N2nd3rdDegree.search2nd3rdDegreeConnections(id1)
		print `res`
	elif cmd == "CHECK":
		if len(sys.argv) < 4:
			use()
		id1 = sys.argv[2]
		id2 = sys.argv[3]
		res = N2nd3rdDegree.check2nd3rdDegreeConnection(id1, id2)
		print `res`
	elif cmd == "DROP":
		if len(sys.argv) < 3:
			use()
		qty = sys.argv[2]
		dropDB(int(qty))
	elif cmd == "MINIINIT":
		createMSDpy2neo()
	elif cmd == "INIT":
		if len(sys.argv) < 3:
			use()
		qty = sys.argv[2]
		createRandomUsers(int(qty))
	else:
		use()
