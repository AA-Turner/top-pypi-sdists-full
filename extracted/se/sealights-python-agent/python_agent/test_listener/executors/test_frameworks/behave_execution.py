import logging
import os
import sys

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.coloring.playwright_helper import (
    PlaywrightBrowserAgent,
)
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.test_listener.sealights_api import SeaLightsAPI
from python_agent.utils import create_md5

log = logging.getLogger(__name__)
is_behave_installed = False

# Customer-facing default: the behave context attribute we look at to
# auto-detect a Playwright page. Exposed so the CLI (admin.py) and the
# executor stay in sync from a single source of truth.
BROWSER_PAGE_ATTR_DEFAULT = "page"

try:
    from behave.runner import ModelRunner
    from behave.__main__ import main as behave_main
    from behave.model import Scenario
    from behave.model_core import Status

    is_behave_installed = True
except ImportError:
    pass


class BehaveAgentExecution(AgentExecution):
    def __init__(
        self,
        config_data,
        labid,
        test_stage,
        cov_report,
        per_test,
        interval,
        test_group_id,
        args,
        browser_page_attr=BROWSER_PAGE_ATTR_DEFAULT,
    ):
        config_data.isInitialColor = False
        self.args = args
        self.excluded_set = {}
        self.is_sealights_agent_ready = False
        self.feature_file_content_cache = {}
        self.test_summary = {"passed": 0, "failed": 0, "skipped": 0, "total": 0}
        self.browser_page_attr = browser_page_attr
        self.playwright_agent = PlaywrightBrowserAgent()
        try:
            super(BehaveAgentExecution, self).__init__(
                config_data,
                labid,
                test_stage,
                cov_report=cov_report,
                per_test=per_test,
                interval=interval,
                test_group_id=test_group_id,
            )
            self.execution_id = SeaLightsAPI.create_execution_id()
            self.set_test_exclude_set()
            self.is_sealights_agent_ready = True
        except Exception as e:
            log.error("Failed initializing AgentExecution. Error: %s" % str(e))

    def execute(self):
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="behave",
        )
        if not is_behave_installed:
            log.error(
                "Behave is not installed. Please install it using: pip install behave"
            )
            return
        sys.path.insert(0, os.getcwd())
        if not self.is_sealights_agent_ready:
            log.warning("Sealights agent is disabled")
        else:
            self.add_sealights_hooks()
        if len(self.args) >= 1:
            behave_main(self.args)
        else:
            behave_main()

    def add_sealights_hooks(self):
        behave_run_hook = ModelRunner.run_hook
        this = self

        def run_hook(self, name, *args):
            context = self.context
            if name == "before_all":
                this.run_before_all()
                return behave_run_hook(self, name, *args)
            elif name == "after_all":
                result = behave_run_hook(self, name, *args)
                this.run_after_all(context)
                return result
            elif name == "before_scenario":
                scenario = getattr(context, "scenario", None)
                skipped = False
                if scenario is not None and isinstance(scenario, Scenario):
                    skipped = this.run_before_scenario(scenario)
                result = behave_run_hook(self, name, *args)
                if (
                    not skipped
                    and scenario is not None
                    and isinstance(scenario, Scenario)
                ):
                    this.run_browser_set_test(context, scenario)
                return result
            elif name == "after_scenario":
                scenario = getattr(context, "scenario", None)
                if scenario is not None and isinstance(scenario, Scenario):
                    this.run_browser_flush(context)
                result = behave_run_hook(self, name, *args)
                if scenario is not None and isinstance(scenario, Scenario):
                    this.run_after_scenario(scenario)
                return result
            else:
                return behave_run_hook(self, name, *args)

        ModelRunner.run_hook = run_hook

        if hasattr(ModelRunner, "run_hook_with_capture"):
            behave_run_hook_with_capture = ModelRunner.run_hook_with_capture
            sealights_hooks = frozenset(
                {"before_all", "after_all", "before_scenario", "after_scenario"}
            )

            def patched_run_hook_with_capture(self, hook_name, *args, **kwargs):
                if hook_name in sealights_hooks and not self.should_run_hook(hook_name):
                    return self.run_hook(hook_name, *args)
                return behave_run_hook_with_capture(self, hook_name, *args, **kwargs)

            ModelRunner.run_hook_with_capture = patched_run_hook_with_capture

        log.debug("Added SeaLights hooks to behave")

    def set_test_exclude_set(self):
        try:
            self.excluded_set = set(
                [t.get("name", "") for t in SeaLightsAPI.get_excluded_tests()]
            )
        except Exception as e:
            log.exception("failed getting excluded tests. error: %s" % str(e))

    def run_before_all(self):
        try:
            SeaLightsAPI.start_execution(self.execution_id)
            self.is_execution_ready = True
            log.debug("Sealights execution started")
        except Exception as e:
            log.exception("failed starting execution from behave. error: %s" % str(e))

    def run_after_all(self, context=None):
        try:
            if context is not None:
                # run_browser_flush -> PlaywrightBrowserAgent.send_all_footprints
                # already catches its own exceptions, so no extra guard needed
                # here -- a closed-browser flush degrades to a debug log inside
                # the helper.
                self.run_browser_flush(context)
            SeaLightsAPI.send_all()
            SeaLightsAPI.end_execution(self.execution_id)
            self.is_execution_ready = False
            log.debug("Sealights execution ended")
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
        except Exception as e:
            log.exception("failed ending execution from behave. error: %s" % str(e))

    def run_before_scenario(self, scenario):
        test_name = f"{scenario.feature.name}:{scenario.name}"
        test_checksum = self.get_test_checksum(scenario)
        SeaLightsAPI.notify_test_start(self.execution_id, test_name, test_checksum)
        log.debug("send test start for scenario: %s" % test_name)
        if test_name in self.excluded_set:
            SeaLightsAPI.notify_test_end(self.execution_id, test_name, 1, "skipped")
            log.debug("send test end for scenario: %s which is excluded" % test_name)
            scenario.skip()
            return True
        return False

    def run_after_scenario(self, scenario):
        test_status = getattr(scenario, "status", None)
        if test_status is None:
            log.error("scenario.status is not defined")
            return
        if test_status == Status.passed:
            test_status_str = "passed"
            self.test_summary["passed"] += 1
        elif test_status == Status.failed:
            test_status_str = "failed"
            self.test_summary["failed"] += 1
        elif test_status == Status.skipped:
            self.test_summary["skipped"] += 1
            test_status_str = "skipped"
        else:
            log.error("scenario.status is not valid")
            return
        self.test_summary["total"] += 1
        test_name = f"{scenario.feature.name}:{scenario.name}"
        test_checksum = self.get_test_checksum(scenario)
        test_duration = getattr(scenario, "duration", 1)
        if self.test_summary["total"] == 1:
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.first-test-reported", testName=test_name
            )
        SeaLightsAPI.notify_test_end(
            self.execution_id, test_name, test_duration, test_status_str, test_checksum
        )
        log.debug(
            "send test end for scenario: %s status: %s" % (test_name, test_status_str)
        )

    def _resolve_browser_page(self, context):
        """Return the Playwright-like page on the behave context, or None.

        Auto-detection: matches the JS cucumber-plugin pattern -- we treat any
        object on context.<browser_page_attr> with a callable .evaluate() as a
        Playwright page. No upfront flag, no playwright import dependency on
        our side, and no per-scenario polling.
        """
        if self.playwright_agent is None:
            return None
        page = getattr(context, self.browser_page_attr, None)
        if page is None:
            return None
        if not callable(getattr(page, "evaluate", None)):
            return None
        return page

    def run_browser_set_test(self, context, scenario):
        """Tell the browser which test is running. Never throws."""
        page = self._resolve_browser_page(context)
        if page is None:
            return
        test_name = f"{scenario.feature.name}:{scenario.name}"
        self.playwright_agent.set_test_identifier(page, self.execution_id, test_name)

    def run_browser_flush(self, context):
        """Tell the browser to flush coverage. Never throws."""
        page = self._resolve_browser_page(context)
        if page is None:
            return
        self.playwright_agent.send_all_footprints(page)

    def get_test_checksum(self, scenario):
        if scenario.filename not in self.feature_file_content_cache:
            try:
                with open(scenario.filename, "r") as file:
                    self.feature_file_content_cache[scenario.filename] = (
                        file.readlines()
                    )
            except FileNotFoundError:
                log.debug("feature file not found: %s" % scenario.filename)
                return ""
        try:
            line_content = self.feature_file_content_cache[scenario.filename][
                scenario.line - 1
            ]
            line_content = "".join(line_content.split())
        except IndexError:
            log.debug("line number not found: %s" % scenario.line)
            return ""
        checksum = create_md5()
        checksum.update(line_content.encode())
        return checksum.hexdigest()
