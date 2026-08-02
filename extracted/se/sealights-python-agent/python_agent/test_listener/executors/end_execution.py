import logging

from python_agent.test_listener.executors.anonymous_execution import AnonymousExecution
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class EndAnonymousExecution(AnonymousExecution):
    def __init__(self, config_data, labid, testgroupid):
        super(EndAnonymousExecution, self).__init__(config_data, labid)
        self.testgroupid = testgroupid

    @disableable()
    def execute(self):
        # GET the active execution before the DELETE so the "closed by agent"
        # console message shows the real test stage (backend_proxy renders the
        # message from config_data.testStage). Falls back to the existing
        # config_data.testStage default if no execution is found.
        active_execution = self.backend_proxy.has_active_execution_v4(self.config_data)
        if isinstance(active_execution, dict) and active_execution.get("testStage"):
            self.config_data.testStage = active_execution["testStage"]
        self.backend_proxy.end_execution(self.config_data, self.labid, self.testgroupid)
        log.info(
            "Finished execution for labid: %s, testgroupid: %s"
            % (self.labid, self.testgroupid)
        )
