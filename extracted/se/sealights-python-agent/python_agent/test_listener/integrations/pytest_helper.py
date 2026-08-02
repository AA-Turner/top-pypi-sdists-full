"""
PYTEST_DONT_REWRITE
Do not delete!!!
This string was added so pytest won't try to apply its rewrite plugin
on the agent and warn the user that the agent was already imported
https://docs.pytest.org/en/latest/assert.html#advanced-assertion-introspection
"""

import functools
import json
import logging
import os
import pytest
from collections import defaultdict

import operator
from python_agent.common.config_data import ConfigData
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates

try:
    from _pytest.junitxml import mangle_test_address
except ImportError:
    from _pytest.junitxml import mangle_testnames as mangle_test_address

from python_agent.test_listener.managers.agent_manager import AgentManager
from python_agent.test_listener.sealights_api import SeaLightsAPI

log = logging.getLogger(__name__)


class SealightsPlugin(object):
    def __init__(self, is_dist=False):
        self.test_status = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))
        self.execution_id = None
        self.is_dist = is_dist
        self.test_summary = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0,
        }

    def pytest_collection_modifyitems(self, session, config, items):
        excluded_set = set(
            [t.get("name", "") for t in SeaLightsAPI.get_excluded_tests()]
        )
        if excluded_set:
            skip = pytest.mark.skip(reason="Skipping this because excluded by server")
            skipped_tests = []
            for item in items:
                test_name = get_test_name(item.nodeid)
                if test_name in excluded_set:
                    skipped_tests.append(item.name)
                    log.info(
                        "Set skip on test: %s known as %s" % (item.name, test_name)
                    )
                    item.add_marker(skip)
            if skipped_tests:
                log.info("skip %d tests" % (len(skipped_tests)))
                log.debug("skipped tests: %s" % skipped_tests)

    def pytest_sessionstart(self, session):
        try:
            self.try_initialize_agent_on_xdist_node(session)
            if self.is_dist and not self.is_slave(session):
                return
            self.execution_id = SeaLightsAPI.create_execution_id()
            SeaLightsAPI.start_execution(self.execution_id)
        except Exception as e:
            log.exception(
                "Failed Starting Execution. Execution Id: %s. Error: %s"
                % (self.execution_id, str(e))
            )

    def pytest_sessionfinish(self, session, exitstatus):
        try:
            if self.is_dist and not self.is_slave(session):
                return
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
            log.exception(
                "Failed Ending Execution. Execution Id: %s. Error: %s"
                % (self.execution_id, str(e))
            )
        if os.environ.get("SL_TEST"):
            AgentManager().shutdown()

    def pytest_runtest_logstart(self, nodeid, location):
        try:
            if self.is_dist and not self.is_slave(None):
                return
            SeaLightsAPI.notify_test_start(self.execution_id, get_test_name(nodeid))
        except Exception as e:
            log.exception(
                "Failed Notifying Test Start. Full Test Name: %s. Error: %s"
                % (nodeid, str(e))
            )

    def pytest_runtest_logreport(self, report):
        try:
            if self.is_dist and not self.is_slave(None):
                return
            self.test_status[report.nodeid]["passed"][report.when] = report.passed
            self.test_status[report.nodeid]["skipped"][report.when] = report.skipped
            self.test_status[report.nodeid]["failed"][report.when] = report.failed
            if report.when == "teardown":
                test = self.test_status[report.nodeid]
                passed = functools.reduce(operator.and_, list(test["passed"].values()))
                skipped = functools.reduce(operator.or_, list(test["skipped"].values()))
                failed = functools.reduce(operator.or_, list(test["failed"].values()))
                test_name = get_test_name(report.nodeid)
                if passed:
                    self.test_summary["passed"] += 1
                    SeaLightsAPI.notify_test_end(
                        self.execution_id,
                        test_name,
                        report.duration,
                        "passed",
                    )
                elif skipped:
                    self.test_summary["skipped"] += 1
                    SeaLightsAPI.notify_test_end(
                        self.execution_id,
                        test_name,
                        report.duration,
                        "skipped",
                    )
                elif failed:
                    self.test_summary["failed"] += 1
                    SeaLightsAPI.notify_test_end(
                        self.execution_id,
                        test_name,
                        report.duration,
                        "failed",
                    )
                self.detect_send_first_test_reported(test_name)
        except Exception as e:
            log.exception(
                "Failed Notifying Test End, Skip or Failed. Full Test Name: %s. Error: %s"
                % (report.nodeid, str(e))
            )

    def pytest_configure_node(self, node):
        """
        Mark this hook as optional in case xdist is not installed.
        """
        workerinput = self.get_xdist_workerinput(node)
        workerinput["sl_config_data"] = json.dumps(AgentManager().config_data.__dict__)

    def is_slave(self, session):
        if session:
            if not hasattr(session, "config"):
                return False
            # slaveinput/workerinput is a variable created in session config by the xdist plugin
            # https://github.com/pytest-dev/pytest-xdist/blob/fd2e8a67111542e03a1469dee6cfa6bff155b099/xdist/remote.py#L202
            return self.get_xdist_workerinput(session.config)
        else:
            if self.execution_id:
                return True
            return False

    def pytest_internalerror(excrepr, excinfo):
        log.exception(
            "Test Internal Error. Exception: %s. Excinfo: %s" % (excrepr, excinfo)
        )

    def pytest_exception_interact(node, call, report):
        log.exception(
            "Test Exception. Node: %s. Call: %s. Report: %s" % (node, call, report)
        )

    def try_initialize_agent_on_xdist_node(self, session):
        if self.is_slave(session):
            config_data = ConfigData()
            config_data.__dict__.update(self.get_config_data(session))
            AgentManager(config_data=config_data, is_master=False)

    def get_config_data(self, session):
        workerinput = self.get_xdist_workerinput(session.config)
        return json.loads(workerinput.get("sl_config_data", "{}"))

    def get_xdist_workerinput(self, config_or_node):
        return getattr(
            config_or_node, "slaveinput", getattr(config_or_node, "workerinput", {})
        )

    def detect_send_first_test_reported(self, test_name):
        self.test_summary["total"] += 1
        if self.test_summary["total"] == 1:
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.first-test-reported", testName=test_name
            )

    pytest_configure_node.optionalhook = True


def get_test_name(nodeid):
    # Parametrized tests can be very long.
    # We account it as a single test
    node_id = ".".join(mangle_test_address(nodeid))
    node_id = node_id.replace("::", ".")
    return node_id


def pytest_configure(config):
    is_dist = (
        config.getoption("numprocesses", default=False)
        or config.getoption("distload", False)
        or config.getoption("dist", "no") != "no"
    )
    plugin = SealightsPlugin(is_dist=is_dist)
    config.pluginmanager.register(plugin, "_sealights")
