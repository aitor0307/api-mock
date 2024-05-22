# use: pytest -rP
# show all prints: pytest -s

import pytest
import os
import json
from flask import Flask
from main import app
import requests
import time
import threading


@pytest.fixture(scope="session")
def flask_server():
    server_thread = threading.Thread(target=app.run, kwargs={"debug": False, "use_reloader": False})
    server_thread.daemon = True  # Ensure the server thread exits when the main thread exits
    server_thread.start()
    
    # Wait for the server to start up
    time.sleep(2)  # Adjust the time delay as needed
    
    yield "http://localhost:5000"

    #app.config['SERVER_SHUTDOWN'] = True


def test_adminrole(flask_server):
    #flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/testadmin/name/Manning")
    print(f"Response: > Admin role test: {res.text} <")
    assert res.status_code < 300

def test_userrole(flask_server):
    #flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/testadmin/name/Barnett")
    print(f"Response: > User role test: {res.text} <")
    assert res.status_code < 300

def test_user_id(flask_server):
    #flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/user/id/a3b8d425-2b60-4ad7-becc-bedf2ef860bd")
    print(f"Response: > Find by user id test: {res.text} <")
    assert res.status_code < 300

def test_user_name(flask_server):
    #flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/user/name/Ines")
    print(f"Response: > Find by user name test: {res.text} <")
    assert res.status_code < 300

def test_table_with_name():
    flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/userpolicies/name/Manning/Manning/?output=table")
    print(f"Response: > find user policies with user name Table: {res} <")
    assert res.status_code < 300


def test_json_with_name(flask_server):
    res = requests.get(flask_server + "/userpolicies/name/Manning/Manning/")
    print(f"Response: > find user policies with user name Json: {res} <")
    assert res.status_code < 300


def test_table_with_id():
    flask_server = "http://localhost:5000"
    res = requests.get(flask_server + "/userpolicies/name/Manning/Manning/?output=table")
    print(f"Response: > find user policies with user id Table: {res} <")
    assert res.status_code < 300


def test_json_with_id(flask_server):
    res = requests.get(flask_server + "/userpolicies/name/Manning/Manning/")
    print(f"Response: > find user policies with user id Json: {res} <")
    assert res.status_code < 300


def test_find_policy_user(flask_server):
    res = requests.get(flask_server + "/policyuser/d46f642a-cef5-4dd7-9924-d1867b268a97/name/Barnett/")
    print(f"Response: > find_policy being a user: {res} <")
    assert res.status_code < 300

def test_find_policy_admin(flask_server):
    res = requests.get(flask_server + "/policyuser/d46f642a-cef5-4dd7-9924-d1867b268a97/name/Manning/")
    print(f"Response: > find_policy being an admin: {res} <")
    assert res.status_code < 300