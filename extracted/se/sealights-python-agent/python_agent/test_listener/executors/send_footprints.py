import atexit
import logging

from python_agent.test_listener.executors.anonymous_execution import AnonymousExecution
from python_agent.test_listener.managers.footprints_manager_v6 import FootprintsManager
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class SendFootprintsAnonymousExecution(AnonymousExecution):
    def __init__(self, config_data, labid):
        super(SendFootprintsAnonymousExecution, self).__init__(config_data, labid)
        self.footprints_manager = FootprintsManager(
            config_data, self.backend_proxy, None
        )
        atexit.register(self.footprints_manager.send_footprints_task)

    @disableable()
    def execute(self):
        self.footprints_manager.start()
        self.footprints_manager.send_footprints_task()
        self.footprints_manager.shutdown(True)
