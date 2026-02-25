"""TestClient API for vanilla Python tests with BrowserStack integration.
This module provides user exposed functions for vanilla Python users (without pytest or other test frameworks)
to manually instrument their tests and send test lifecycle events to BrowserStack Test Observability.
The TestClient class allows users to:
- Set test metadata (name, hierarchy, file path)
- Mark test start/finish events
- Mark session name and status on BrowserStack Automate/App Automate
- Send test results (Pass/Fail) to Test Observability (currently working on this integration)
Example usage:
    ```python
    from browserstack_sdk.client import TestClient
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    test_client = TestClient() \
        .set_test_name("my_test") \
        .set_test_hierarchy(["tests", "MyTestSuite"]) \
        .set_file_path("tests/my_test.py")
    test_client.start()
    try:
        opts = Options()
        driver = webdriver.Remote(command_executor="hub_url", options=opts)
        driver.get('https://example.com')
        assert driver.title == "Example Domain"
        test_client.Pass()
    except Exception as e:
        test_client.Fail(e)
        raise
    finally:
        if driver:
            driver.quit()
    ```
"""
import threading
import logging
import os
import traceback
from bstack_utils.config import Config
from bstack_utils.helper import current_time, time_diff, Result
from bstack_utils.test_data import TestData
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.session_utils import browserstack_executor_helper
from bstack_utils.constants import HTTPS_HUB
logger = logging.getLogger(__name__)
class TestClient:
    """Public-facing API for vanilla Python test instrumentation.
    This class provides a builder pattern interface for configuring and running
    vanilla Python tests with BrowserStack integration. It handles:
    - Test lifecycle events (start, finish) for Test Observability
    - Session name marking on BrowserStack Automate
    - Session status marking (passed/failed)
    Attributes:
        _test_name (str): Name of the test
        _test_hierarchy (list): Hierarchical scope of the test (e.g., ["module", "class"])
        _file_path (str): File path where the test is located
        _test_data (TestData): Internal test data object for events
        _started_at (str): ISO timestamp when test started
        _driver (WebDriver): Reference to the Selenium WebDriver instance
    """
    def __init__(self):
        """Initialize a new TestClient instance."""
        self._test_name = None
        self._test_hierarchy = []
        self._file_path = None
        self._test_data = None
        self._started_at = None
        self._driver = None
        self._result_marked = False
        self._test_uuid = None
    def _get_driver(self):
        """Get the WebDriver instance from multiple possible locations.
        Current thread's bstackSessionDriver
        Returns:
            WebDriver: The driver instance, or None if not found
        """
        if self._driver:
            return self._driver
        logger.debug("TestClient: Starting driver search...")
        driver = getattr(threading.current_thread(), 'bstackSessionDriver', None)
        if driver:
            self._driver = driver
            logger.info("TestClient: Found driver on current thread")
            return driver
        logger.debug("TestClient: No driver on current thread")
        return None
    def set_test_name(self, name):
        """Set the name of the test.
        Args:
            name (str): The test name (e.g., "addProductToCart")
        Returns:
            TestClient: Self for method chaining
        """
        self._test_name = name
        return self
    def set_test_hierarchy(self, hierarchy):
        """Set the hierarchical scope of the test.
        Args:
            hierarchy (list): List of scope levels (e.g., ["tests", "BStackDemoTest"])
        Returns:
            TestClient: Self for method chaining
        """
        self._test_hierarchy = hierarchy if hierarchy else []
        return self
    def set_file_path(self, file_path):
        """Set the file path where the test is located.
        Args:
            file_path (str): Relative or absolute file path (e.g., "tests/vanilla_sample_test.py")
        Returns:
            TestClient: Self for method chaining
        """
        self._file_path = file_path
        return self
    def start(self):
        """Start the test and send TestRunStarted event to BrowserStack.
        This method:
        1. Creates a TestData object with configured metadata
        2. Sends TestRunStarted event to Test Observability (if enabled)
        3. Stores test UUID on current thread for driver integration
        4. Marks thread test status as 'pending'
        Must be called before creating the WebDriver instance.
        """
        if not self._test_name:
            logger.warning("TestClient.start() called without test_name. Use set_test_name() first.")
            return
        self._started_at = current_time()
        self._test_data = TestData(
            name=self._test_name,
            file_path=self._file_path or "unknown",
            started_at=self._started_at,
            framework='python-generic',  # Framework name for vanilla Python tests
            scope=self._test_hierarchy,
            tags=[],
            integrations={}
        )
        self._test_uuid = self._test_data.uuid
        threading.current_thread().current_test_uuid = self._test_data.uuid
        threading.current_thread().bstackTestMeta = {'status': 'pending'}
        try:
            TestHubHandler.send_run_event('TestRunStarted', self._test_data)
            logger.debug(f"TestClient: Sent TestRunStarted event for test '{self._test_name}'")
        except Exception as e:
            logger.error(f"TestClient: Failed to send TestRunStarted event: {e}")
    def _mark_session_name(self):
        """Mark the session name on BrowserStack Automate using test name.
        Session name will be set to the test_name configured via set_test_name().
        Respects skipSessionName setting from browserstack.yml testContextOptions.
        """
        global_config = Config.get_instance()
        if global_config.should_skip_session_name():
            logger.debug("TestClient: Skipping session name marking (skipSessionName is enabled)")
            return
        driver = self._get_driver()
        if not driver or not self._test_name:
            return
        try:
            executor_string = browserstack_executor_helper('setSessionName', self._test_name, '', '', '', '')
            driver.execute_script(executor_string)
            logger.debug(f"TestClient: Set session name to '{self._test_name}'")
        except Exception as e:
            logger.error(f"TestClient: Failed to set session name: {e}")
    def _mark_result(self, status, reason=''):
        """Mark the test result and send events.
        Args:
            status (str): 'passed' or 'failed'
            reason (str): Failure reason/exception (for failed tests)
        """
        if self._result_marked:
            logger.warning(f"TestClient: Result already marked for test '{self._test_name}'. Skipping.")
            return
        self._result_marked = True
        self._mark_session_name()
        if status == 'passed':
            result = Result.passed()
        else:
            result = Result.failed(exception=reason)
        finished_at = current_time()
        duration = time_diff(self._started_at, finished_at) if self._started_at else 0
        if self._test_data:
            self._test_data.stop(time=finished_at, duration=duration, result=result)
            try:
                TestHubHandler.send_run_event('TestRunFinished', self._test_data)
                logger.debug(f"TestClient: Sent TestRunFinished event for test '{self._test_name}' with result '{status}'")
            except Exception as e:
                logger.error(f"TestClient: Failed to send TestRunFinished event: {e}")
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            logger.debug("TestClient: Skipping session status marking (skipSessionStatus is enabled)")
        else:
            driver = self._get_driver()
            if driver:
                try:
                    executor_string = browserstack_executor_helper('setSessionStatus', '', status, reason, '', '')
                    driver.execute_script(executor_string)
                    logger.debug(f"TestClient: Successfully marked session status as '{status}'")
                except Exception as e:
                    logger.error(f"TestClient: Failed to mark session status: {e}")
            else:
                logger.debug("TestClient: No driver found, cannot mark session status")
        threading.current_thread().bstackTestMeta = {'status': status}
    def Pass(self):
        """Mark the test as passed.
        This method:
        1. Sets session name to test_name on BrowserStack Automate
        2. Sends TestRunFinished event with 'passed' status to Test Observability
        3. Marks session status as 'passed' on BrowserStack Automate
        Should be called after test assertions pass, before driver.quit().
        """
        self._mark_result('passed')
    def Fail(self, exception=None):
        """Mark the test as failed.
        Args:
            exception (Exception): The exception that caused the test to fail
        This method:
        1. Sets session name to test_name on BrowserStack Automate
        2. Sends TestRunFinished event with 'failed' status to Test Observability
        3. Marks session status as 'failed' on BrowserStack Automate
        4. Includes exception/traceback in failure reason
        Should be called in the except block when test fails, before driver.quit().
        """
        reason = ''
        if exception:
            if isinstance(exception, str):
                reason = exception
            else:
                try:
                    import sys
                    if sys.version_info >= (3, 10):
                        reason = ''.join(traceback.format_exception(exception))
                    else:
                        reason = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
                except:
                    reason = str(exception)
        self._mark_result('failed', reason)
