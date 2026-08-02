import logging.config
import os
import time
from nose.plugins import Plugin
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.sealights_api import SeaLightsAPI

log = logging.getLogger(__name__)


# TODO: the nose and unittest plugins should have a common base class


class SealightsNosePlugin(Plugin):
    def __init__(self):
        super(SealightsNosePlugin, self).__init__()
        self.execution_id = SeaLightsAPI.create_execution_id()
        self.error_tests = {}
        self.skipped_tests = {}
        # the nose plugin needs these 3 attributes:
        self.name = self.__class__.__name__
        self.score = 0
        self.enableOpt = "enable_plugin_sealights"
        self.excluded_set = {}
        self.setTestExcludeSet()
        self.test_summary = {"passed": 0, "failed": 0, "skipped": 0, "total": 0}

    def setTestExcludeSet(self):
        try:
            self.excluded_set = set(
                [t.get("name", "") for t in SeaLightsAPI.get_excluded_tests()]
            )
        except Exception as e:
            log.exception("failed getting excluded tests. error: %s" % str(e))

    def options(self, parser, env=os.environ):
        """
        Add command line options here.
        :param parser:
        :param env:
        :return:
        """
        super(SealightsNosePlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        super(SealightsNosePlugin, self).configure(options, conf)
        self.enabled = True

    def begin(self):
        """
        Called before any tests are collected or run
        """
        try:
            SeaLightsAPI.start_execution(self.execution_id)
        except Exception as e:
            log.exception("failed starting execution from nose. error: %s" % str(e))

    def finalize(self, result):
        """
        Called after all report output, including output from all plugins, has been sent to the stream.
        :param result: test result object
        """
        try:
            if self.test_summary["total"] == 0:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.no-tests-captured"
                )
            else:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.captured-tests-summary",
                    testsExecuted=self.test_summary["total"],
                    testsPassed=self.test_summary["passed"],
                    testsFailed=self.test_summary["failed"],
                    testsSkipped=self.test_summary["skipped"],
                )
            SeaLightsAPI.send_all()
            SeaLightsAPI.end_execution(self.execution_id)
        except Exception as e:
            log.exception("failed ending execution from nose. error: %s" % str(e))

    def beforeTest(self, test):
        if test.id() in self.excluded_set:
            SeaLightsAPI.notify_test_start(self.execution_id, test.id())
            SeaLightsAPI.notify_test_end(self.execution_id, test.id(), 1, "skipped")
            self.test_summary["skipped"] += 1
            test.skipTest("test skipped by SeaLights TIA")
            self.detect_send_first_test_reported(test)

    def startTest(self, test):
        """
        Called before test run (after beforeTest)
            :param test:
            :type test: :class:`nose.case.Test`
            see: http://nose.readthedocs.io/en/latest/api/test_cases.html#nose.case.Test:
        """
        try:
            test.start_time = time.time()
            SeaLightsAPI.notify_test_start(self.execution_id, test.id())
        except Exception as e:
            log.exception(
                "failed sending test start event from nose. error: %s" % str(e)
            )

    def stopTest(self, test):
        """
        Called after test run - before afterTest
        :param test:
        :type :class:`nose.case.Test`
        """
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            if not self.error_tests.get(test.id()) and not self.skipped_tests.get(
                test.id()
            ):
                self.test_summary["passed"] += 1
                self.detect_send_first_test_reported(test)
                SeaLightsAPI.notify_test_end(
                    self.execution_id, test.id(), test.duration, "passed"
                )

        except Exception as e:
            log.exception("failed sending test end from nose. error: %s" % str(e))

    def addError(self, test, err):
        """
        Called when test raise uncaught exception
        Or when test is skipped.
        :param test:
        :param err:
        :return:
        """
        try:
            test.end_time = time.time()
            test.duration = test.end_time = test.start_time
            # The error tuple holds the the type in index 0 and the exception object in index 1
            # We use the type to discover if the test is skipped.
            if str(err[0]) == "<class 'unittest.case.SkipTest'>":
                self.skipped_tests[test.id()] = test.id()
                self.test_summary["skipped"] += 1
                SeaLightsAPI.notify_test_end(
                    self.execution_id, test.id(), test.duration, "skipped"
                )
            else:
                self.error_tests[test.id()] = test.id()
                self.test_summary["failed"] += 1

                SeaLightsAPI.notify_test_end(
                    self.execution_id, test.id(), test.duration, "failed"
                )
            self.detect_send_first_test_reported(test)
        except Exception as e:
            log.exception(
                "failed sending test end on from nose addError. error: %s" % str(e)
            )

    def addFailure(self, test, err):
        """
        Called when test fails (assert error)
        :param test:
        :param err:
        """
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.error_tests[test.id()] = test.id()
            self.test_summary["failed"] += 1
            self.detect_send_first_test_reported(test)
            SeaLightsAPI.notify_test_end(
                self.execution_id, test.id(), test.duration, "failed"
            )
        except Exception as e:
            log.exception(
                "failed sending test end from nose addFailure. error: %s" % str(e)
            )

    def detect_send_first_test_reported(self, test):
        self.test_summary["total"] += 1
        if self.test_summary["total"] == 1:
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.first-test-reported", testName=test.id()
            )
