# import requests
import pytest
import logging
from random import randint
from box import Box
from json import dumps


def get_id(response):
    # Make sure that  id=1 in the response

    assert response.json().get("id") == 1
    assert response.json().get("userId") == 1


def get_userid(response):
    # Make sure that  id=1 in the response

    assert response.json().get("userId") == 1


def generate_req1():

    req = {
    "i": "avocado",
    "q": "kale",
    "p": 1,
        }

    return Box(req)


def generate_response2():
    joke = [
  {
    "id": 50,
    "type": "general",
    "setup": "What do you call a factory that sells passable products?",
    "punchline": "A satisfactory"
  }
]

    return Box(joke)


def generate_req3():
    rint = str(randint(0,1000))
    req = {
        "first_name": "Max",
        "last_name": f'Smith{rint}',
        "gender": "male",
        "email": f'maxgsmith{rint}1982@sm.com',
        "status": "active"
    }
    # logging.info(f'\ngen json {dumps(req, indent=4)}')
    logging.info(f'\ngen Box {dumps(Box(req), indent=4)}')
    return Box(req)


def test_gen_func():
    generate_req3()

def log_response(response):
    # logging.info(f'\nJson response: {dumps(response.json(), indent=4)}')
    return





def save_data(response):
    return Box({"test_title": response.json()["results"][0]["title"]})

# @pytest.fixture(autouse=True)
# def response_after_test(pytestconfig, response):
#     # if pytestconfig.getoption('sr'):
#     logging.info(f"Got response: {dumps(response.json(), indent=4)}")