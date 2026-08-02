import importlib
import importlib.util
import inspect
import logging
import os
import sys

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class PytestAgentExecution(AgentExecution):
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
    ):
        config_data.isInitialColor = False
        super(PytestAgentExecution, self).__init__(
            config_data,
            labid,
            test_stage=test_stage,
            cov_report=cov_report,
            per_test=per_test,
            interval=interval,
            test_group_id=test_group_id,
        )
        self.args = args

    def execute(self):
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="pytest",
        )
        try:
            args = list(self.args)
            import pytest

            # we're appending the current working directory for customers running pytest using: "python -m pytest"
            # https://github.com/pytest-dev/pytest/blob/beacecf29ba0b99511a4e5ae9b96ff2b0c42c775/doc/en/usage.rst
            sys.path.append(os.getcwd())

            # we add the pytest_helper plugin here so it will be discovered after xdist, as this is a must
            # according to https://docs.pytest.org/en/latest/writing_plugins.html#plugin-discovery-order-at-tool-startup
            # plugins using -p are loaded after plugins that are registered using setuptools (xdist)
            self.set_original_argv(args, pytest.__name__)
            self.add_sealights_plugin(args)
            errno = pytest.main(args=args)
            raise SystemExit(errno)
        except ImportError as e:
            log.exception("Failed Importing pytest. Error: %s" % str(e))

    def set_original_argv(self, args, pytest_name):
        spec = importlib.util.find_spec(pytest_name)
        if spec is None:
            raise ImportError(f"No module named '{pytest_name}'")
        pytest_path = spec.origin
        sys.argv = [pytest_path] + args

    @disableable(fail_silently=True)
    def add_sealights_plugin(self, args):
        from python_agent.test_listener.integrations import pytest_helper

        args.extend(["-p", inspect.getmodule(pytest_helper).__name__])
