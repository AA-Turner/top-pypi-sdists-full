import atexit
import datetime
import logging
import os
import sys
import time
import uuid

from python_agent import __legacy_mode__ as is_legacy_mode
from python_agent.common.agent_events.agent_events_manager import AgentEventsManager
from python_agent.common.constants import AGENT_TYPE_TEST_LISTENER
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.packages.six import add_metaclass
from python_agent.test_listener.integrations.pytest_xdist_helper import (
    override_xdist_exit_timeout,
)
from python_agent.test_listener.managers.events_manager import EventsManager
from python_agent.test_listener.managers.tia_manager import TIAManager
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import Singleton

log = logging.getLogger(__name__)

if is_legacy_mode:
    from python_agent.test_listener.managers.footprints_manager import FootprintsManager
else:
    from python_agent.test_listener.managers.footprints_manager_v6 import (
        FootprintsManager,
    )


@add_metaclass(Singleton)
class AgentManager(object):
    # Class-level variable to track exit code across instances
    _exit_code = 0

    def __init__(self, config_data=None, is_master=True):
        log.info("Initializing... Is Master? %s" % is_master)
        if not config_data:
            raise Exception("'config_data' must be provided")
        self.config_data = config_data
        self.config_data.agentType = AGENT_TYPE_TEST_LISTENER
        self.is_master = is_master
        self.pid = os.getpid()
        self.backend_proxy = BackendProxy(config_data)
        self.state_tracker = StateTracker(config_data)
        self.agents_events_manager = AgentEventsManager(config_data=config_data)
        self.agents_events_manager.send_agent_start(
            lab_id=config_data.labId, test_stage=config_data.testStage
        )
        self.footprints_manager = None
        if not config_data.skipFootprintsPipeline:
            self.footprints_manager = FootprintsManager(
                config_data, self.backend_proxy, self.agents_events_manager
            )
        self.events_manager = EventsManager(
            config_data, self.backend_proxy, self.agents_events_manager
        )
        self.tia_manager = TIAManager(config_data)
        if self.footprints_manager:
            self.footprints_manager.start()
        self.events_manager.start()

        # Install custom exit handler to track application exit codes
        self._install_exit_code_tracker()

        atexit.register(self.shutdown)
        self.agent_started()
        self.register_integrations()

    def _install_exit_code_tracker(self):
        """Override sys.exit to capture exit codes from monitored applications."""
        original_exit = sys.exit

        def custom_exit(code=0):
            """Capture exit code and delegate to original sys.exit."""
            AgentManager._exit_code = code if code is not None else 0
            original_exit(code)

        sys.exit = custom_exit

    def get_excluded_tests(self):
        return self.tia_manager.get_excluded_tests()

    def create_execution_id(self):
        if self.footprints_manager is None:
            return str(uuid.uuid4())
        return self.footprints_manager.get_current_execution_id()

    def start_execution(self, execution_id):
        """Register execution with backend and notify footprints manager."""
        from python_agent.test_listener.entities.start_execution_request import (
            StartExecutionRequest,
        )

        start_request = StartExecutionRequest(
            self.config_data.customerId,
            self.config_data.appName,
            self.config_data.branchName,
            self.config_data.buildName,
            self.config_data.labId,
            self.config_data.testStage,
            self.config_data.testGroupId,
            self.config_data.agentId,
        )
        start_request.executionId = execution_id
        self.backend_proxy.start_execution(self.config_data, start_request)
        if self.footprints_manager:
            self.footprints_manager.set_execution_active(execution_id)

    def end_execution(self, execution_id):
        """End execution with backend and clear footprints manager state.

        Drains the footprints pipeline (collect from coverage.py, wait for
        workers, send buffer) before clearing the execution, so the last ~1
        second of coverage is not lost. See SLDEV-26528.
        """
        if self.footprints_manager:
            self.footprints_manager.ensure_all_footprints_sent()
            self.footprints_manager.clear_execution()
        self.backend_proxy.end_execution(
            self.config_data,
            self.config_data.labId,
            self.config_data.testGroupId,
            execution_id,
        )

    def push_event(self, event):
        event["timestamp"] = int(round(time.time() * 1000))
        self.events_manager.push_event(event)

    def send_all(self):
        self.events_manager.send_all()
        if self.footprints_manager:
            self.footprints_manager.ensure_all_footprints_sent()

    def shutdown(self):
        """
        Shutdown the agent and display appropriate completion message.

        Displays 'FAILED' message if the monitored application exited with a non-zero code,
        otherwise displays 'SUCCEEDED' message.
        """
        if self.pid == os.getpid():
            log.info("Shutting down Sealights Agent...")
            self.events_manager.shutdown()
            if self.footprints_manager:
                self.footprints_manager.shutdown(self.is_master)
            self.agents_events_manager.send_agent_stop()
            log.info("Sealights Agent has been shut down.")

            command_name = self.config_data.command_name or "run"
            exit_code = AgentManager._exit_code

            # Display appropriate completion message based on exit code
            if exit_code != 0:
                ConsoleMessageTemplates.render_and_print(
                    "common.general.agent-ended-error",
                    command=command_name,
                    error=str(exit_code),
                    dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            else:
                ConsoleMessageTemplates.render_and_print(
                    "common.general.agent-ended-succeeded",
                    command=command_name,
                    dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

    def get_trace_function(self):
        if self.footprints_manager is None:
            return None
        return self.footprints_manager.get_trace_function()

    def agent_started(self):
        self.push_event({"type": "agentStarted"})

    def register_integrations(self):
        override_xdist_exit_timeout()

    def register_uwsgi_at_exit(self):
        if "uwsgi" in sys.modules:
            import uwsgi

            uwsgi_original_atexit_callback = getattr(uwsgi, "atexit", None)

            def uwsgi_atexit_callback():
                self.shutdown()
                if uwsgi_original_atexit_callback:
                    uwsgi_original_atexit_callback()

            uwsgi.atexit = uwsgi_atexit_callback
