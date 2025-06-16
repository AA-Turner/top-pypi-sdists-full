from aheadworks_core.model.http.api_request import ApiRequest as Api
from jira import JIRA
import json


class JiraApiManager:
    """api manager for jira"""

    def __init__(self, config):
        self.config = config
        self.request = Api(config=self.config)
        self.jira = JIRA(
            server=self.config.url,
            basic_auth=(self.config.user, self.config.token)
        )

    def get_jira_instance(self):
        return self.jira

    def get_issue_url(self, task_key):
        return '{}/browse/{}'.format(self.config.url, task_key)

    def get_release_report_all_issues_url(self, project_key, version_id):
        return '{}/projects/{}/versions/{}/tab/release-report-all-issues'.format(
            self.config.url,
            project_key,
            version_id
        )
