from jira import JIRA

from kacl.config import KACLConfig


class KACLJiraClient:
    def __init__(self, config: KACLConfig):
        self.config = config
        self.client = JIRA(
            server=config.issue_tracker_jira_host,
            basic_auth=(
                config.issue_tracker_jira_username,
                config.issue_tracker_jira_password,
            ),
        )

    def is_authenticated(self):
        try:
            # Attempt to fetch the current user as a way to check if authentication was successful
            self.client.current_user()
        except Exception:
            return False
        return True

    def add_comment(self, issue_key, comment):
        """
        Adds a comment to a JIRA issue.

        Args:
            issue_key (str): The key of the issue to add the comment to.
            comment (str): The text of the comment to add.

        Returns:
            None
        """
        self.client.add_comment(issue_key, comment)
