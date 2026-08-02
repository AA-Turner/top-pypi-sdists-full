import logging.config
import time
import unittest
import xmlrunner

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.sealights_api import SeaLightsAPI

__unittest = True
loader = unittest.loader.defaultTestLoader

log = logging.getLogger(__name__)
is_has_tests = True


class SealightsTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super(SealightsTestResult, self).__init__(stream, descriptions, verbosity)
        self.skipped_tests = {}
        self.error_tests = {}
        self.execution_id = SeaLightsAPI.create_execution_id()
        self.excluded_set = {}
        self.setTestExcludeSet()
        self.test_summary = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0,
        }

    def setTestExcludeSet(self):
        try:
            self.excluded_set = set(
                [t.get("name", "") for t in SeaLightsAPI.get_excluded_tests()]
            )
        except Exception as e:
            log.exception("failed getting excluded tests. error: %s" % str(e))

    def startTestRun(self):
        try:
            # startTestRun is called even when there are no tests found. We avoid it here.
            if is_has_tests:
                SeaLightsAPI.start_execution(self.execution_id)
        except Exception as e:
            log.exception("failed starting execution. error: %s" % str(e))
        super(SealightsTestResult, self).startTestRun()

    def stopTestRun(self):
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
            # stopTestRun is called even when there are no tests found. We avoid API call here.
            if is_has_tests:
                SeaLightsAPI.send_all()
                SeaLightsAPI.end_execution(self.execution_id)
        except Exception as e:
            log.exception("failed ending execution. error: %s" % str(e))
        super(SealightsTestResult, self).stopTestRun()

    def startTest(self, test):
        try:
            if test.id() in self.excluded_set:
                setattr(
                    test,
                    "setUp",
                    lambda: test.skipTest("test skipped by SeaLights TIA"),
                )
            test.start_time = time.time()
            SeaLightsAPI.notify_test_start(self.execution_id, test.id())
        except Exception as e:
            log.exception("failed sending test start. error: %s" % str(e))
        super(SealightsTestResult, self).startTest(test)

    def stopTest(self, test):
        try:
            if not self.skipped_tests.get(test.id()) and not self.error_tests.get(
                test.id()
            ):
                test.end_time = time.time()
                test.duration = test.end_time - test.start_time
                self.test_summary["passed"] += 1
                SeaLightsAPI.notify_test_end(
                    self.execution_id, test.id(), test.duration, "passed"
                )
                self.detect_send_first_test_reported(test.id())
        except Exception as e:
            log.exception("failed sending test end. error: %s" % str(e))
        super(SealightsTestResult, self).stopTest(test)

    def addError(self, test, err):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.error_tests[test.id()] = test.id()
            self.test_summary["failed"] += 1
            SeaLightsAPI.notify_test_end(
                self.execution_id, test.id(), test.duration, "failed"
            )
            self.detect_send_first_test_reported(test.id())
        except Exception as e:
            log.exception("failed sending test failed. error: %s" % str(e))
        super(SealightsTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.error_tests[test.id()] = test.id()
            self.test_summary["failed"] += 1
            SeaLightsAPI.notify_test_end(
                self.execution_id, test.id(), test.duration, "failed"
            )
            self.detect_send_first_test_reported(test.id())
        except Exception as e:
            log.exception("failed sending test failed. error: %s" % str(e))
        super(SealightsTestResult, self).addFailure(test, err)

    def addSkip(self, test, reason):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.skipped_tests[test.id()] = test.id()
            self.test_summary["skipped"] += 1
            SeaLightsAPI.notify_test_end(
                self.execution_id, test.id(), test.duration, "skipped"
            )
            self.detect_send_first_test_reported(test.id())
        except Exception as e:
            log.exception("failed sending test skipped. error: %s" % str(e))
        super(SealightsTestResult, self).addSkip(test, reason)

    def detect_send_first_test_reported(self, test_name):
        self.test_summary["total"] += 1
        if self.test_summary["total"] == 1:
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.first-test-reported", testName=test_name
            )


class SealightsTextTestRunner(unittest.TextTestRunner):
    resultclass = SealightsTestResult

    def run(self, test):
        if hasattr(test, "_tests") and not test._tests:
            global is_has_tests
            is_has_tests = False
        return super(SealightsTextTestRunner, self).run(test)


class SealightsJunitTestRunner(xmlrunner.XMLTestRunner):
    resultclass = SealightsTestResult

    def run(self, test):
        if hasattr(test, "_tests") and not test._tests:
            global is_has_tests
            is_has_tests = False
        return super(SealightsJunitTestRunner, self).run(test)


class SealightsTestProgram(unittest.TestProgram):
    def __init__(self, argv=None, testRunner=None, exit=True):
        super(SealightsTestProgram, self).__init__(
            module=None, argv=argv, testRunner=testRunner, exit=exit
        )


def main(args, is_junit=False, output="."):
    try:
        runner = SealightsTextTestRunner()
        if is_junit:
            runner = SealightsJunitTestRunner(output=output)
        SealightsTestProgram(testRunner=runner, argv=args, exit=False)
    except SystemExit as e:
        log.exception(
            "Failed Running Unittests With Args: %s. Error: %s" % (args, str(e))
        )
    except Exception as e:
        log.exception(
            "Failed Running Unittests With Args: %s. Error: %s" % (args, str(e))
        )
