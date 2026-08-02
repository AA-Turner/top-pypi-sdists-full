import datetime
import logging
import os

from python_agent.build_scanner import app as build_scanner
from python_agent.build_scanner.app import _resolve_file_filters
from python_agent.common.agent_events.agent_events_manager import AgentEventsManager
from python_agent.common.constants import AGENT_TYPE_BUILD_SCANNER
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class Build(object):
    def __init__(self, config_data):
        self.config_data = config_data
        self.config_data.agentType = AGENT_TYPE_BUILD_SCANNER
        self.workspacepath = self.config_data.additionalParams.get("workspacepath")
        self.include = self.config_data.additionalParams.get("include") or None
        self.exclude = self.config_data.additionalParams.get("exclude") or None
        self.agent_manager = AgentEventsManager(config_data=config_data)
        self.backend_proxy = BackendProxy(config_data)

    @disableable()
    def execute(self):
        log.info("Starting Build Scan")

        # Resolve file filters (handles .slignore precedence over CLI params)
        resolved_include, resolved_exclude = _resolve_file_filters(
            self.workspacepath, self.include, self.exclude
        )

        # Build agent config with the resolved include/exclude patterns
        agent_config = {
            "include": resolved_include,
            "exclude": resolved_exclude,
        }

        self.agent_manager.send_agent_start(
            lab_id="", test_stage="", agent_config=agent_config
        )
        try:
            # Pre-check: verify build session hasn't already been scanned
            submitted = self.backend_proxy.check_build_session_submitted(
                self.config_data, self.config_data.buildSessionId
            )

            # If submitted is True, the build session was already scanned - error out
            if submitted is True:
                ConsoleMessageTemplates.render_and_print(
                    "common.build-scanner.scanner-buildsessionid-already-scanned-error",
                    buildSessionId=self.config_data.buildSessionId,
                )
                raise Exception("Build session was already scanned")
            ConsoleMessageTemplates.render_and_print(
                "common.build-scanner.scanner-about-to-scan",
                appName=self.config_data.appName,
                branchName=self.config_data.branchName,
                buildName=self.config_data.buildName,
            )
            ConsoleMessageTemplates.render_and_print(
                "common.build-scanner.scanner-about-to-scan-scandir",
                scanDir=os.path.abspath(self.workspacepath),
            )
            build_scanner.main(
                config_data=self.config_data,
                workspacepath=self.workspacepath,
                include=self.include,
                exclude=self.exclude,
            )

        except Exception as e:
            ConsoleMessageTemplates.render_and_print(
                "common.build-scanner.scanner-buildmap-send-error",
            )
            log.exception("Build Scan Failed. Error: %s" % str(e))
            self.agent_manager.send_agent_build_scan_error(e)
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-error",
                command="scan",
                error=str(e),
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            self.agent_manager.send_agent_stop()
            raise

        self.agent_manager.send_agent_stop()
        log.info("Build Scan Finished")
