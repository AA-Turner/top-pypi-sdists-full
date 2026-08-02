import logging
import os
import sys

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.test_listener.integrations.unittest_helper import (
    main as unittest_main,
)
from python_agent.test_listener.integrations.unittest_helper import unittest

log = logging.getLogger(__name__)


class UnittestAgentExecution(AgentExecution):
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
        super(UnittestAgentExecution, self).__init__(
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
        # we're appending the current working directory for customers running unittest using: "python -m unittest"
        # since running it like that adds current working directory to sys.path
        sys.path.insert(0, os.getcwd())
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="unittest",
        )
        if self.config_data.isDisabled:
            unittest.main(module=None, argv=list(self.args))
        else:
            unittest_main(["unittest"] + list(self.args))
