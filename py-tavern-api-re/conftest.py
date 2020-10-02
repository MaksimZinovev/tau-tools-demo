# import logging.config
from logging import config
import os
import html
import yaml

import pytest
import logging
from random import randint
from box import Box
from json import dumps
from dotenv import load_dotenv

# =========== disable this section and obtain your own API keys to run tests on your machine ========
# =========== see comments in test_basics.tavern.yaml, test_http.tavern.yaml ================================
try:
    load_dotenv()
    API_KEY_DROPBOX = os.getenv('API_KEY_DROPBOX')
    API_KEY_GOREST = os.getenv('API_KEY_GOREST')
except Exception as e:
    logging.info(f'Disable try-except section at the top of conftest.py and obtain your own API keys to run tests '
                 f'on your machine: \n {e}')

# =====================================================================================================


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
    try:
        logging.info(f"================= RESPONSE ================== "
                     f"\n\nstatus code [{response.status_code}]\n{dumps(response.json(), indent=4)}\n\n")

    except ValueError as e:
        if "!DOCTYPE html" in response.text:
            logging.info(f"================= RESPONSE ================== "
                         f"\n\nstatus code [{response.status_code}]\n{html.unescape(response.text)}\n\n")
        else:
            logging.info(f"================= RESPONSE ================== "
                        f"\n\nstatus code [{response.status_code}]\n{response.text,}\n\n")
    return

