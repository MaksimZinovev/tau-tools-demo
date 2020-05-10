# import logging.config
from logging import config
import os

import pytest
import yaml

import requests
import pytest
import logging
from random import randint
from box import Box
from json import dumps


@pytest.fixture(scope="function", autouse=True)
def run_all():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "logging.yaml"), "r") as spec_file:
        settings = yaml.load(spec_file, Loader=yaml.SafeLoader)
        config.dictConfig(settings)


@pytest.fixture
def zipcode():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "zip_code.yaml"), "r") as file:
        zcode = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    logging.info(f'Code: {zcode["code"]}')
    return zcode["code"]



def pytest_tavern_beta_after_every_response(expected, response):
    # logging.info(f"================= GOT RESPONSE ================== \n\n{dumps(response.json(), indent=4)}")
    pass


def myfunc(response):
    response
    return