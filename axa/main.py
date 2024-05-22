
import os
from flask import Flask
from models.mymodels import ApiNotValid, ValidateMode, NotFoundModel, NoAccess
from services.ddbb import DDBB
import logging
from flask import request
from functools import wraps

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY #os.environ['FLASK_SECRET_KEY']
app.config.from_object(__name__)
app.logger.setLevel(logging.DEBUG)

# initialize database
ddbb = DDBB()


def login_is_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):        
        if ddbb.retrieve_user(kwargs["mode"], kwargs["admin_user"]).role != 'admin':  #authorization required
            return app.response_class(
                response=NoAccess().model_dump_json(),
                status=200,
                mimetype='application/json'
            )
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/user/<string:mode>/<string:user>')
def user(mode, user):
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
        resp = ddbb.retrieve_user(mode, user)
        
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


## ONLY FOR ADMIN USERS
@app.route('/userpolicies/<string:mode>/<string:admin_user>/<string:user>/')
@login_is_required
def userpolicies(mode, user, admin_user):
    app.logger.info(f'This endpoint will: \nGet the list of policies linked to a user name or user id -> Can be accessed by users with role "admin" ')
    modev = ValidateMode(mode=mode)
    if modev.valid == False:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
    try:
        resp = ddbb.retrieve_user_policies(mode, user, "table" if request.args.get("output") == "table" else "json")
    except KeyError:
        return app.response_class(
            response=NotFoundModel().model_dump_json(),
            status=201,
            mimetype='application/json'
        )

    response = app.response_class(
            response=resp[0],
            status=200,
            mimetype=resp[1]
        )

    return response


## ONLY FOR ADMIN USERS
@app.route('/policyuser/<string:policynumber>/<string:mode>/<string:admin_user>/')
@login_is_required
def policyuser(policynumber, mode, admin_user):
    app.logger.info(f'This endpoint will: \nGet the user linked to a policy number -> Can be accessed by users with role "admin"  ')
    modev = ValidateMode(mode=mode)
    if modev.valid == False:
        return app.response_class(
            response=ApiNotValid().model_dump_json(),
            status=200,
            mimetype='application/json'
        )
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


@app.route('/testadmin/<string:mode>/<string:admin_user>/') #'e519ddb1-cd20-4af4-ad40-e3051c03c075'
@login_is_required
def testadmin(mode, admin_user):
    app.logger.info(f'This endpoint will: \nGet the user a determine its role')
    return "User is admin"


if __name__ == '__main__':
    app.run(debug=False)