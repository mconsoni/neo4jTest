My first approach to Neo4j

Files:
	- README.md: this file.
	- config.py: Connection URL for Neo4j
	- N2nd3rdDegree.py: Webservice / Module with two routes / functions:
		Webservice base URL: http://127.0.0.1:3030/
		* Route: /2nd3rdDegree/<int:id> - Function: search2nd3rdDegreeConnections(id)
			Returns a list of user ids of 2nd/3rd degree connections for user with id=id.
		* Route: /2nd3rdDegree/<int:id_1>/<int:id_2> - Function: check2nd3rdDegreeConnection(id_1, id_2)
			Return true or false if two user ids are 2nd/3rd degree connections
	- neo4jtest.py: Script for creating nodes / connections, drop database and call functions from N2nd4rdDegree.py:
		Use ./neo4jtest.py <COMMAND> <PARAMS>
		List of Commands:
		    MINIINIT: Create a know database for testing
		    INIT: Create a random database of 2 millions random users
		        Param: Amount of users to create
		    DROP: Delete database
		        Param: Amount of users to delete
		    LIST: List of user ids of 2nd/3rd degree connections for USERID
		        Param: USERID
		    CHECK: Check if USERID1 and USERID2 are in 2nd/3rd degree connection
		        Param: USERID1 USERID2

