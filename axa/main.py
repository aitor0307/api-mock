import requests
import time
import os
import json
import pandas as pd
import re
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, List
from flask import Flask
from models.mymodels import ResponseModel, Client, Policies, ApiNotValid
from services.ddbb import DDBB
import logging

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
    app.logger.info(f'Someone knocked the main door v2')
    if mode not in ["id", "name"]:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    resp = ddbb.retrieve_user(mode, user_id)
    response = app.response_class(
        response=resp.model_dump_json(),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/userpolicies/<string:mode>/<string:user_id>') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
def userpolicies(mode, user_id):
    app.logger.info(f'Someone knocked the main door v2')
    if mode not in ["id", "name"]:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    resp = ddbb.retrieve_user_policies(mode, user_id)
    response = app.response_class(
        response=resp.to_html(),
        status=200,
        mimetype='text/html'
    )
    return response


@app.route('/policyuser/<string:policynumber>') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
def policyuser(policynumber):
    app.logger.info(f'Someone knocked the main door v2')
    resp = ddbb.retrieve_policy_user(policynumber)
    response = app.response_class(
        response=resp.model_dump_json(),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)