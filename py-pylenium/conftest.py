"""
`conftest.py` and `pylenium.json` files should stay at your Workspace Root.

conftest.py
    Although this file is editable, you should only change its contents if you know what you are doing.
    Instead, you can create your own conftest.py file in the folder where you store your tests.

pylenium.json
    You can change the values, but DO NOT touch the keys or you will break the schema.

py
    The only fixture you really need from this is `py`. This is the instance of Pylenium for each test.
    Just pass py into your test and you're ready to go!

Examples:
    def test_go_to_google(py):
        py.visit('https://google.com')
        assert 'Google' in py.title()
"""

import json
import logging
import os
import shutil
import sys
from time import sleep

import pytest
import requests
from faker import Faker
from pytest_reportportal import RPLogger, RPLogHandler

from pylenium import Pylenium
from pylenium.config import PyleniumConfig, TestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions as ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pylenium.element import Element, Elements

from typing import List, Tuple, Optional, Union

from utils.ut import Ut


class Controller(Pylenium):
    def __init__(self, config: PyleniumConfig):
        Pylenium.__init__(self, config)

    def clicknretry(self, css: str, timeout: int = None, maxretries: int = 3) -> None:
        """Make sure that click worked.
        Retry if the element is still visible (expected to be invisible after click).
        """

        attempt = 0
        by = By.CSS_SELECTOR
        self.log.info(f'[STEP] clicknretry : ``{css}``')
        while attempt < maxretries:
            if timeout == 0:
                element = self.webdriver.find_element(by, css)
            else:
                element = self.wait(timeout).until(
                    lambda x: x.find_element(by, css),
                    f'Could not find element with the CSS ``{css}``'
                )
            element.click()
            logging.info(f'clicked')

            try:
                self.wait(timeout).until(
                    ec.invisibility_of_element_located((by, css)))
            except ex.TimeoutException:
                attempt += 1
                logging.info(
                    f'TimeoutException upon waiting for invisibility of element {css}. Retrying n = {attempt}\n')
                continue
            break

    def click_with_retry(self, css: str, force=False, exp_condition=None, timeout: int = None,
                               max_retries: int = 3) -> None:
        """ Clicks the element. Has retry cycle based on expected condition.


        Args:
            css:  The selector to use.
            force: If True, a JavascriptExecutor command is sent instead of Selenium's native `.click()`.
            exp_condition: Condition used in retry cycle.
            timeout: The number of seconds to wait for this to succeed. Overrides the default wait_time.
            max_retries: max number of retries

        Returns: None.
        """
        by = By.CSS_SELECTOR
        attempt = 0
        use_send_keys = False
        if exp_condition is None:
            exp_condition = lambda _: True
        self.log.info(f'[STEP] .click_with_retry. Expected condition : ``{exp_condition}``, element: {css} ')
        while attempt < max_retries:
            element = self.webdriver.find_element(by, css)
            try:
                if force:
                    self.webdriver.execute_script('arguments[0].click()', element)
                else:
                    if use_send_keys:
                        element.send_keys(Keys.ENTER)
                        self.wait(timeout).until(exp_condition)
                    else:
                        element.click()
                        self.wait(timeout).until(exp_condition)

            except ex.TimeoutException:
                attempt += 1
                logging.info(
                    f'TimeoutException upon waiting for expected condition {exp_condition}. Retrying n = {attempt}\n')
                continue
            except ex.ElementClickInterceptedException:
                attempt += 1
                use_send_keys = True
                logging.info(
                    f'ElementClickInterceptedException upon clicking on element {css}. Retrying n = {attempt}\n')
                continue
            break

    def click_wait_for_elem_to_disappear(self, element: Element, force=False,
                                         element_to_disappear: Optional[Element] = None,
                                         timeout: int = None) -> bool:
        """ Clicks the element, then waits until that (or custom) elements disappears.
        An Expectation that an element is either invisible or not present on the DOM


        Args:
            element:  The element to click.
            force: If True, a JavascriptExecutor command is sent instead of Selenium's native `.click()`.
            element_to_disappear:  element to wait for to disappear.
            timeout: The number of seconds to wait for this to succeed. Overrides the default wait_time.


        Returns: Pylenium.
        """

        if element_to_disappear is None:
            element_before_click = element
        else:
            element_before_click = element_to_disappear

        self.log.info(f'[STEP] .click_wait_for_elem_to_disappear. '
                      f'Custom element to disappear is None: ``{True if element_to_disappear is None else False}`` ')

        if force:
            self.webdriver.execute_script('arguments[0].click()', element)
        else:
            element.click()
        try:
            value = self.wait(timeout).until(lambda _: element_before_click.should().disappear())
        except ex.TimeoutException:
            value = False
        if value:
            return value
        else:
            self.log.critical('.should().disappear()')
            raise AssertionError('Element was still visible or still in the DOM')

    def take(self, css: str, timeout: int = None, max_retries: int = 0, list_of_exceptions: list = None) -> Element:
        """ Get the DOM element that matches the `css` selector. Retry if any exception from list_of_exceptions
        is raised

        * If timeout=None (default), use the default wait_time.
        * If timeout > 0, override the default wait_time.
        * If timeout=0, poll the DOM immediately without any waiting.

        Args:
            css: The selector to use.
            timeout: The number of seconds to wait for this to succeed. Overrides the default wait_time.
            list_of_exceptions: list of handled exception in retry block. By default always use TimeoutException.
            max_retries: max number of retries

        Returns:
            The first element that is found, even if multiple elements match the query.

        """
        # by default always use TimeoutException
        if list_of_exceptions is None:
            list_of_exceptions = [ex.TimeoutException]
        else:
            list_of_exceptions.append(ex.TimeoutException)
        attempt = 0
        element = None
        by = By.CSS_SELECTOR
        self.log.info(f'[STEP] do.take() - Find the element with css: ``{css}``')

        while attempt <= max_retries:
            try:
                if timeout == 0:
                    element = self.webdriver.find_element(by, css)
                else:
                    element = self.wait(timeout).until(
                        lambda x: x.find_element(by, css),
                        f'Could not find element with the CSS ``{css}``'
                    )
            except list_of_exceptions as err:
                if max_retries == 0:
                    logging.info(f'{err} upon waiting for element {css}. NO retries\n')
                    raise err
                else:
                    attempt += 1
                    logging.info(f'{err} upon waiting for element {css}. Retrying n = {attempt}\n')
                    continue
            break

        return Element(self, element, locator=(by, css))

    def wait_for_doc_ready_state(self, timeout: int = 10) -> None:
        logging.info(f'[STEP] wait_for_doc_ready_state() - Wait for doc ready state, timeout: ``{timeout}``')
        WebDriverWait(self._webdriver, timeout).until(lambda wd: wd.execute_script('return document.readyState;') == 'complete')


def make_dir(filepath) -> bool:
    """ Make a directory.

    Returns:
        True if successful, False if not.
    """
    try:
        os.mkdir(filepath)
        return True
    except FileExistsError:
        return False


@pytest.fixture(scope='function')
def fake() -> Faker:
    """ A basic instance of Faker to make test data."""
    return Faker()


@pytest.fixture(scope='function')
def api():
    """ A basic instance of Requests to make HTTP API calls. """
    return requests


@pytest.fixture(scope="session")
def rp_logger(request):
    """ Report Portal Logger """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create handler for Report Portal if the service has been
    # configured and started.
    if hasattr(request.node.config, 'py_test_service'):
        # Import Report Portal logger and handler to the test module.
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
        # Add additional handlers if it is necessary
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        rp_handler = logging.StreamHandler(sys.stdout)
    # Set INFO level for Report Portal handler.
    rp_handler.setLevel(logging.INFO)
    return logger


@pytest.fixture(scope='session', autouse=True)
def project_root() -> str:
    """ The Project (or Workspace) root as a filepath.

    * This conftest.py file should be in the Project Root if not already.
    """
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session', autouse=True)
def test_run(project_root, request) -> str:
    """ Creates the `/test_results` directory to store the results of the Test Run.

    Returns:
        The `/test_results` directory as a filepath (str).
    """
    session = request.node
    test_results_dir = f'{project_root}/test_results'

    if os.path.exists(test_results_dir):
        # delete /test_results from previous Test Run
        shutil.rmtree(test_results_dir, ignore_errors=True)
    if not os.path.exists(test_results_dir):
        # create /test_results for this Test Run
        make_dir(test_results_dir)

    for test in session.items:
        # make the test_result directory for each test
        make_dir(f'{test_results_dir}/{test.name}')

    return test_results_dir


@pytest.fixture('session')
def py_config(project_root, request) -> PyleniumConfig:
    """ Initialize a PyleniumConfig for each test

    1. This starts by deserializing the user-created pylenium.json from the Project Root.
    2. If that file is not found, then proceed with Pylenium Defaults.
    3. Then any CLI arguments override their respective key/values.
    """
    try:
        # 1. Load pylenium.json in Project Root, if available
        with open(f'{project_root}/pylenium.json') as file:
            _json = json.load(file)
        config = PyleniumConfig(**_json)
    except FileNotFoundError:
        # 2. pylenium.json not found, proceed with defaults
        config = PyleniumConfig()

    # 3. Override with any CLI args/options
    # Driver Settings
    cli_remote_url = request.config.getoption('--remote_url')
    if cli_remote_url:
        config.driver.remote_url = cli_remote_url

    cli_browser_options = request.config.getoption('--options')
    if cli_browser_options:
        config.driver.options = [option.strip() for option in cli_browser_options.split(',')]

    cli_browser = request.config.getoption('--browser')
    if cli_browser:
        config.driver.browser = cli_browser

    cli_capabilities = request.config.getoption('--caps')
    if cli_capabilities:
        # --caps must be in '{"name": "value", "boolean": true}' format
        # with double quotes around each key. booleans are lowercase.
        config.driver.capabilities = json.loads(cli_capabilities)

    cli_page_wait_time = request.config.getoption('--page_load_wait_time')
    if cli_page_wait_time and cli_page_wait_time.isdigit():
        config.driver.page_load_wait_time = int(cli_page_wait_time)

    # Logging Settings
    cli_pylog_level = request.config.getoption('--pylog_level')
    if cli_pylog_level:
        config.logging.pylog_level = cli_pylog_level

    cli_screenshots_on = request.config.getoption('--screenshots_on')
    if cli_screenshots_on:
        shots_on = True if cli_screenshots_on.lower() == 'true' else False
        config.logging.screenshots_on = shots_on

    cli_extensions = request.config.getoption('--extensions')
    if cli_extensions:
        config.driver.extension_paths = [ext.strip() for ext in cli_extensions.split(',')]

    return config


@pytest.fixture(scope='function')
def test_case(test_run, py_config, request) -> TestCase:
    """ Manages data pertaining to the currently running Test Function or Case.

        * Creates the test-specific logger.

    Args:
        test_run: The Test Run (or Session) this test is connected to.

    Returns:
        An instance of TestCase.
    """
    test_name = request.node.name
    test_result_path = f'{test_run}/{test_name}'
    py_config.driver.capabilities.update({'name': test_name})
    return TestCase(name=test_name, file_path=test_result_path)


@pytest.fixture(scope='function')
def py(test_case, py_config, request, rp_logger):
    """ Initialize a Pylenium driver for each test.

    Pass in this `py` fixture into the test function.

    Examples:
        def test_go_to_google(py):
            py.visit('https://google.com')
            assert 'Google' in py.title()
    """
    py = Pylenium(py_config)
    yield py
    try:
        if request.node.report.failed:
            # if the test failed, execute code in this block
            if py_config.logging.screenshots_on:
                screenshot = py.screenshot(f'{test_case.file_path}/test_failed.png')
                with open(screenshot, "rb") as image_file:
                    rp_logger.info("Test Failed - Attaching Screenshot",
                                   attachment={"name": "test_failed.png",
                                               "data": image_file,
                                               "mime": "image/png"})
    except AttributeError:
        rp_logger.error('Unable to access request.node.report.failed, unable to take screenshot.')
    except TypeError:
        rp_logger.info('Report Portal is not connected to this test run.')
    py.quit()


@pytest.fixture(scope='function')
def do(test_case, py_config, request, rp_logger):
    """ Use "Controller" class to extend Pylenium methods
    Initialize a Pylenium driver for each test.

    Pass in this `py` fixture into the test function.

    Examples:
        def test_go_to_google(py):
            py.visit('https://google.com')
            assert 'Google' in py.title()
    """
    do = Controller(py_config)
    yield do
    try:
        if request.node.report.failed:
            # if the test failed, execute code in this block
            if py_config.logging.screenshots_on:
                screenshot = py.screenshot(f'{test_case.file_path}/test_failed.png')
                with open(screenshot, "rb") as image_file:
                    rp_logger.info("Test Failed - Attaching Screenshot",
                                   attachment={"name": "test_failed.png",
                                               "data": image_file,
                                               "mime": "image/png"})
    except AttributeError:
        rp_logger.error('Unable to access request.node.report.failed, unable to take screenshot.')
    except TypeError:
        rp_logger.info('Report Portal is not connected to this test run.')
    do.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Yield each test's outcome so we can handle it in other fixtures. """
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        setattr(item, "report", report)
    return report


def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', default='', help='The lowercase browser name: chrome | firefox'
    )
    parser.addoption(
        '--remote_url', action='store', default='', help='Grid URL to connect tests to.'
    )
    parser.addoption(
        '--screenshots_on', action='store', default='', help="Should screenshots be saved? true | false"
    )
    parser.addoption(
        '--pylog_level', action='store', default='', help="Set the pylog_level: 'off' | 'info' | 'debug'"
    )
    parser.addoption(
        '--options', action='store',
        default='', help='Comma-separated list of Browser Options. Ex. "headless, incognito"'
    )
    parser.addoption(
        '--caps', action='store',
        default='', help='List of key-value pairs. Ex. \'{"name": "value", "boolean": true}\''
    )
    parser.addoption(
        '--page_load_wait_time', action='store',
        default='', help='The amount of time to wait for a page load before raising an error. Default is 0.'
    )
    parser.addoption(
        '--extensions', action='store',
        default='', help='Comma-separated list of extension paths. Ex. "*.crx, *.crx"'
    )


@pytest.fixture(scope='function')
def ut():
    _ut = Ut()
    return _ut

