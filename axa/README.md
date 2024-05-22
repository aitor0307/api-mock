# Flask example to call webservices in the BE and provide an specific response

This is a simple example of a flask webservice calling a mock and ingesting some of its data. As it is meant to be handled via browser and without an authentication service behind, it will ask for the parameters in the url directly to be easily usable in a browser.

## How to run

If you wish to run flask directly you can do it by setting the environment variable FLASK_APP to "main.py" and then running ```flask run``` in the main directory.

If you have docker installed, you can run it easily with ```docker-compose up```. If not, you can also build the image yourself using the Dockerfile provided.

## Structure

First of all it will connect to the two endpoints provided to get a list of customers and policies. It will store them in an object which will act as a DDBB of two tables. This DDBB object will also be capable of handling the specific queries to search for the data the user wants.
This DDBB will act as the main source of data for user and its roles, as well as the policies.

It will contain 3 endpoints to perform different queries:
1. Will allow to retrieve a user via ID or name, by getting the parameter of how to search from the request itself, fulfilling the first 2 needs.
2. It will get the user that is related to a policy number. In the request we need to provide the user that is making the search, indistinct with id or name (this paremeter should also be provided)
3. It will retrieve all the policies of a user that is being searched. In the request we need to provide the user that is making the search, indistinct with id or name (this paremeter should also be provided). In the URL we can also state if we want to ouput the results in a table or as a json by adding ```?outcome=table```

*Note: points 2 and 3 have a decorator function over them that will check if the user that is making the query is admin or not, this way the decorator can be easily extender to other endpoints*

## Tests

You can run the default tests with ```pytest -s``` or you can start the server and test multiple things. Here you can find some examples:

Users who have user roles:  
- a3b8d425-2b60-4ad7-becc-bedf2ef860bd  Barnett  
- 44e44268-dce8-4902-b662-1b34d2c10b8e  Merrill  

Users who are admins:  
- a0ece5db-cd14-4f21-812f-966633e7be86  Britney  
- e8fd159b-57c4-4d36-9bd7-a59ca13057bb  Manning  

Policies (ids) you can check if they belong to a user:  
- 64cceef9-3a01-49ae-a23b-3761b604800b  
- 7b624ed3-00d5-4c1b-9ab8-c265067ef58b  
- 56b415d6-53ee-4481-994f-4bffa47b5239  
- 6f514ec4-1726-4628-974d-20afe4da130c  

## Nice to have

- Instead of requesting the user to provide the "authentication" via the url request, which should never be done in production, it should be handled with the session cookie or via a header.
- This authentication can be handled via a 3rd party service which will act as the authentication authority which could issue the bearer request, etc.
- The DDBB should definitely be set appart in its own service.