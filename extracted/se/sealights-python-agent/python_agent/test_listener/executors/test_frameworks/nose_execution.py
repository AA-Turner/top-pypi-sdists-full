import os
import sys
import logging
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class NoseAgentExecution(AgentExecution):
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
        super(NoseAgentExecution, self).__init__(
            config_data,
            labid,
            test_stage,
            cov_report=cov_report,
            per_test=per_test,
            interval=interval,
            test_group_id=test_group_id,
        )
        self.args = args

    def execute(self):
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="nose",
        )
        sys.path.insert(0, os.getcwd())
        try:
            import nose

            # first arg is ignored on parsing because it's the program name
            self.args.insert(0, "")
            addplugins = self.add_sealights_plugin() or []
            nose.main(addplugins=addplugins, argv=self.args)
        except ImportError as e:
            log.exception("Failed importing nose. Error: %s" % str(e))

    @disableable(fail_silently=True)
    def add_sealights_plugin(self):
        from python_agent.test_listener.integrations.nose_helper import (
            SealightsNosePlugin,
        )

        return [SealightsNosePlugin()]
