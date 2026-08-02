import datetime
import logging

from python_agent.common.build_session.build_session_data import BuildSessionData
from python_agent.common.constants import BUILD_SESSION_ID_FILE
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.utils import disableable

log = logging.getLogger(__name__)


class PrConfig(object):
    def __init__(
        self,
        config_data,
        app_name,
        target_branch,
        latest_commit,
        pull_request_number,
        repo_url,
        build_session_id,
        workspacepath,
        include,
        exclude,
    ):
        self.config_data = config_data
        self.app_name = app_name
        self.target_branch = target_branch
        self.latest_commit = latest_commit
        self.pull_request_number = pull_request_number
        self.repo_url = repo_url
        self.build_session_id = build_session_id
        self.backend_proxy = BackendProxy(config_data)
        self.workspacepath = workspacepath
        self.include = include
        self.exclude = exclude

    @disableable()
    def execute(self):
        try:
            additional_params = {
                "workspacepath": self.workspacepath,
                "include": self.include,
                "exclude": self.exclude,
            }
            pull_request_params = {
                "latestCommit": self.latest_commit,
                "targetBranch": self.target_branch,
                "pullRequestNumber": self.pull_request_number,
                "repositoryUrl": self.repo_url,
            }
            build_session_data = BuildSessionData(
                self.app_name,
                None,
                None,
                self.build_session_id,
                additional_params=additional_params,
                pull_request_params=pull_request_params,
            )
            build_session_id = self.backend_proxy.create_pr_build_session_id(
                self.config_data,
                build_session_data,
            )
            log.info("Received Build Session Id: %s" % build_session_id)
            PrConfig.write_build_session_to_file(build_session_id)
        except Exception as e:
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-error",
                command="prconfig",
                error=str(e),
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

    @staticmethod
    def write_build_session_to_file(build_session_id):
        try:
            with open(BUILD_SESSION_ID_FILE, "w") as f:
                build_session_id = build_session_id.replace('"', "")
                f.write(build_session_id)
        except Exception as e:
            log.error(
                "Failed Saving Build Session Id File to: %s. Error: %s"
                % (BUILD_SESSION_ID_FILE, str(e))
            )
            raise
