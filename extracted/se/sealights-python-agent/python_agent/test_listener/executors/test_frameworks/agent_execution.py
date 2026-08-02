import os

from python_agent.common import constants
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.managers.agent_manager import AgentManager
from python_agent.utils import disableable


class AgentExecution(object):
    """
    Handles execution configuration and initialization for test framework integrations.

    This class sets up the necessary configuration for the Sealights agent to monitor
    test executions and collect coverage data. It resolves lab IDs, configures test
    stages, and initializes the AgentManager when requested.
    """

    def __init__(
        self,
        config_data,
        labid,
        test_stage=None,
        cov_report=None,
        per_test=True,
        interval=constants.INTERVAL_IN_MILLISECONDS,
        init_agent=True,
        test_group_id=None,
    ):
        self.config_data = config_data
        if self.config_data.get_is_disabled():
            return
        self.labid = self.resolve_lab_id(labid)
        if cov_report:
            self.config_data.covReport = cov_report
        if test_stage:
            self.config_data.testStage = test_stage

        if test_group_id:
            self.config_data.testGroupId = test_group_id
        self.config_data.labId = self.labid
        self.config_data.workspacepath = self.config_data.additionalParams.get(
            "workspacepath", constants.DEFAULT_WORKSPACEPATH
        )
        self.config_data.include = self.config_data.additionalParams.get("include")
        self.config_data.exclude = self.config_data.additionalParams.get("exclude")
        # NOTE(SLDEV-26009): per_test / interval / intervalSeconds are now
        # applied inside ConfigurationManager._apply_cli_values so that remote
        # config can override them. DO NOT reintroduce writes to
        # ``self.config_data.perTest``, ``self.config_data.interval``, or
        # ``self.config_data.intervalSeconds`` here — they would run AFTER
        # remote config and re-invert precedence. The constructor still
        # accepts ``per_test`` and ``interval`` kwargs for signature
        # compatibility with the subclasses / tests, but it is a no-op.
        if init_agent:
            if test_stage:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.listener-essential-config-test-stage",
                    testStage=test_stage,
                )
            if not self.config_data.resolved_bsid_from_labid:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.listener-essential-config",
                    appName=self.config_data.appName,
                    branchName=self.config_data.branchName,
                    buildName=self.config_data.buildName,
                )
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.listener-essential-bsid",
                    buildSessionId=self.config_data.buildSessionId,
                )
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.listener-essential-labid",
                labId=self.config_data.labId,
            )
            self.init_agent()

    def resolve_lab_id(self, labid):
        if labid is not None:
            return labid
        labid_from_env = os.environ.get("SL_LABID") or os.environ.get("SL_LAB_ID")
        if labid_from_env is not None:
            return labid_from_env
        return (
            self.config_data.buildSessionId
            or self.config_data.appName
            or constants.DEFAULT_LAB_ID
        )

    @disableable(fail_silently=True)
    def init_agent(self):
        """
        Initialize the AgentManager which handles coverage collection and reporting.

        The AgentManager automatically tracks exit codes and displays appropriate
        messages on shutdown.
        """
        AgentManager(config_data=self.config_data)
