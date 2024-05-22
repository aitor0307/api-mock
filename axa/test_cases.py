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
    server_thread = threading.Thread(target=app.run, kwargs={"debug": True, "use_reloader": False})
    server_thread.daemon = True  # Ensure the server thread exits when the main thread exits
    server_thread.start()
    
    # Wait for the server to start up
    time.sleep(4)  # Adjust the time delay as needed
    
    yield "http://localhost:5000"

    app.config['SERVER_SHUTDOWN'] = True


def test_example(flask_server):
    print("Making request to Flask server...")
    response = requests.get(flask_server + "/")
    print("Response:", response.text)
    assert response.status_code == 200


def test_table(flask_server):
    res = requests.get(flask_server + "/userpolicies/id/e8fd159b-57c4-4d36-9bd7-a59ca13057bb/?output=table")
    print(f"Response: > Table: {res.text} <")
    assert res.status_code < 300


def test_json(flask_server):
    res = requests.get(flask_server + "/userpolicies/id/e8fd159b-57c4-4d36-9bd7-a59ca13057bb/")
    print(f"Response: > Table: {res} <")
    assert res.status_code < 300

