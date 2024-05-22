import requests
import time
import os
import json
import pandas as pd
import re
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, List
from flask import Flask
from models.mymodels import ResponseModel, Client, Policies, ApiNotValid, ValidateMode, NotFoundModel
from services.ddbb import DDBB
import logging
from flask import request

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY #os.environ['FLASK_SECRET_KEY']
app.config.from_object(__name__)
app.logger.setLevel(logging.DEBUG)

# initialize database
ddbb = DDBB()

"""
Clients: https://run.mocky.io/v3/532e77dc-2e2d-4a0c-91fd-5ea92ff5d615 

Policies: https://run.mocky.io/v3/289c72a0-8190-4a15-9a15-4118dc2fbde6 
"""

@app.route('/user/<string:mode>/<string:user_id>') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
def user(mode, user_id):
    app.logger.info(f'''This endpoint will: \nGet user data filtered by user id -> Can be accessed by users with role "users" and "admin" 
                    \nGet user data filtered by user name -> Can be accessed by users with role "users" and "admin" ''')
    modev = ValidateMode(mode=mode)
    if modev.valid == False:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    try:
        resp = ddbb.retrieve_user(mode, user_id)
        
    except KeyError:
        return app.response_class(
            response=NotFoundModel().model_dump_json(),
            status=201,
            mimetype='application/json'
        )
    
    response = app.response_class(
            response=resp.model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    
    return response

@app.route('/userpolicies/<string:mode>/<string:user_id>/') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
def userpolicies(mode, user_id):
    app.logger.info(f'This endpoint will: \nGet the list of policies linked to a user name or user id -> Can be accessed by users with role "admin" ')
    modev = ValidateMode(mode=mode)
    if modev.valid == False:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    try:
        resp = ddbb.retrieve_user_policies(mode, user_id, "table" if request.args.get("output") == "table" else "json")
    except KeyError:
        return app.response_class(
            response=NotFoundModel().model_dump_json(),
            status=201,
            mimetype='application/json'
        )
    app.logger.debug(resp[1])
    response = app.response_class(
            response=resp[0],
            status=200,
            mimetype=resp[1]
        )

    return response


@app.route('/policyuser/<string:policynumber>') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
def policyuser(policynumber):
    app.logger.info(f'This endpoint will: \nGet the user linked to a policy number -> Can be accessed by users with role "admin"  ')
    try:
        resp = ddbb.retrieve_policy(policynumber)
    except KeyError:
        return app.response_class(
            response=NotFoundModel().model_dump_json(),
            status=201,
            mimetype='application/json'
        )
    
    response = app.response_class(
        response=resp.model_dump_json(),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)