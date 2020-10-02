"""
Controller class and fixture that can be used to extend Pylenium
"""
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import logging


### HELPERS ###
# verify autocomplete feature
def wait_for_doc_ready_state(do, timeout: int = 10) -> None:
    logging.info(f'[STEP] wait_for_doc_ready_state() - Wait for doc ready state, timeout: ``{timeout}``')
    do.wait(timeout, use_py=True).until(lambda wd: wd.execute_script('return document.readyState;') == 'complete')

