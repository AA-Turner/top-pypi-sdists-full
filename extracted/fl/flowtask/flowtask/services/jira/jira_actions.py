from jira import JIRA, JIRAError
import requests

class JiraActions():
    def __init__(self, server: str, email: str, token: str):
        """
            Init class JiraActions.

            :param server: Server URL.
            :param email: User Email.
            :param token: API token of Jira.
        """
        try:
            self.server = server
            self.jira = JIRA(server=server, basic_auth=(email, token))
        except JIRAError as e:
            self.handle_jira_error(e, "Authenticating in Jira")

    def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = 'Bug'):
        """
            Creates a new Jira issue in the specified project.

            :param project_key: Key of the project in which the ticket is to be created.
            :param summary: Summary or title of the ticket.
            :param description: Description of the ticket.
            :param issue_type: Type of ticket (default 'Task').
            :return: Returns the ticket created.
        """
        try:
            issue_data = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type}
            }
            issue = self.jira.create_issue(fields=issue_data)
            return issue
        except JIRAError as e:
            self.handle_jira_error(e, "Creating an issue")

    def add_comment(self, issue_key: str, comment: str):
        """
            Adds a comment to a Jira issue.

            :param issue_key: Key of the issue to add the comment to.
            :param comment: The comment to be added.
            :return: Returns the added comment or raises an exception in case of error.
        """
        try:
            issue = self.jira.issue(issue_key)
            return self.jira.add_comment(issue, comment)
        except JIRAError as e:
            self.handle_jira_error(e, "Adding a comment")

    def transition_issue(self, issue_key: str, transition_name: str, comment: str = None):
        """
            Transitions a Jira issue to a new status based on the transition name.
            If the transition name is invalid, provides a list of valid transitions for the issue.

            :param issue_key: Key of the issue to transition.
            :param transition_name: Name of the transition to perform (e.g., 'Start Progress', 'Close Issue').
            :param comment: Optional comment to add during the transition.
            :return: Returns the issue after the transition or raises an exception in case of error.
        """
        try:
            # Get all possible transitions for the issue
            transitions = self.jira.transitions(issue_key)

            # Find the transition ID corresponding to the provided transition name
            valid_transitions = [t['name'] for t in transitions]
            transition_id = next((t['id'] for t in transitions if t['name'].lower() == transition_name.lower()), None)

            if not transition_id:
                valid_transitions_str = ', '.join(valid_transitions)
                raise ValueError(
                    f"Transition '{transition_name}' not found for issue {issue_key}. "
                    f"Valid transitions are: {valid_transitions_str}"
                )

            # Perform the transition
            self.jira.transition_issue(issue_key, transition_id, comment=comment)
            return self.jira.issue(issue_key)

        except JIRAError as e:
            self.handle_jira_error(e, "transitioning an issue")

    def assign_issue(self, issue_key: str, assignee: str):
        """
        Assigns a Jira issue to a specified user.

        :param issue_key: Key of the issue to be assigned (e.g., 'PROJ-123').
        :param assignee: Username or email of the user to whom the issue will be assigned.
        :return: The updated issue after the assignment.
        """
        try:
            # Assign the issue to the specified user
            issue = self.jira.issue(issue_key)
            self.jira.assign_issue(issue, assignee)
            return issue
        except JIRAError as e:
            self.handle_jira_error(e, f"assigning the issue {issue_key} to {assignee}")

    def add_worklog(self, issue_key: str, time_spent: str, comment: str = None, started: str = None):
        """
            Adds a worklog entry to a Jira issue.

            :param issue_key: Key of the issue to which the worklog will be added.
            :param time_spent: Time spent on the issue (e.g., '2h', '3d', '1w').
            :param comment: Optional comment to add with the worklog.
            :param started: Date and time the work started (optional, format: 'YYYY-MM-DDTHH:MM:SS.000+0000').
            :return: The worklog entry that was added, or raises an exception in case of error.
        """
        try:
            valid_units = ['h', 'd', 'w']
            if not any(time_spent.endswith(unit) for unit in valid_units):
                raise ValueError(f"Invalid time format: {time_spent}. Must end with one of {valid_units}.")
            # Add the worklog to the issue
            worklog = self.jira.add_worklog(
                issue=issue_key,
                timeSpent=time_spent,
                comment=comment,
                started=started
            )
            return worklog
        except JIRAError as e:
            self.handle_jira_error(e, "Adding a worklog")

    def list_issues(self):
        """
            Return a list of Jira issues.

            :return: The list of closed issues assigned to user.
        """
        try:
            qry = 'assignee = currentUser() and status != Closed and status != CANCELLED and status != Done order by created asc'  # noqa
            issues = self.jira.search_issues(qry)
            return issues
        except JIRAError as e:
            self.handle_jira_error(e, "listing the issues")

    def list_transitions(self, issue_key: str):
        """
            Return a list of a valid transitions of a issue.

            :param issue_key: Key of the issue to transition.
            :return: Returns the  list of a valid transitions of a issue.
        """
        try:
            transitions = self.jira.transitions(issue_key)
            valid_transitions = [t['name'] for t in transitions]
            return valid_transitions
        except JIRAError as e:
            self.handle_jira_error(e, "listing the transitions")

    @staticmethod
    def handle_jira_error(e: Exception, action: str):
        """
            Handles errors and exceptions that occur during interactions with Jira.

            This function captures exceptions thrown during Jira operations and raises appropriate
            errors with relevant messages based on the type of exception (e.g., JIRAError, connection issues).

            :param e: Exception object. This can be a JIRAError or other types of exceptions (e.g., connection errors).
            :param action: A string describing the action that was being attempted when the error occurred
                        (e.g., 'creating an issue', 'adding a comment').

            :raises ValueError: If there is a validation error (e.g., incorrect data in Jira fields).
            :raises PermissionError: If the user does not have sufficient permissions for the Jira operation.
            :raises ConnectionError: If there is a problem connecting to the Jira server or if the requested resource was not found.
            :raises TimeoutError: If the operation timed out while connecting to the Jira server.
            :raises Exception: For any other unexpected errors that occur during the Jira operation.
        """  # noqa
        if isinstance(e, JIRAError):
            if e.status_code == 400:
                raise ValueError(f"Validation error while {action}, please, check the provided values.")
            elif e.status_code == 403:
                raise PermissionError(f"Insufficient permissions while {action}.")
            elif e.status_code == 404:
                raise ConnectionError(f"Resource not found while {action}.")
            elif e.status_code in (500, 502):
                raise Exception(f"Server error while {action}. The Jira server might be down.")
            else:
                raise Exception(f"Jira error while {action}: {e.text}")
        elif isinstance(e, requests.ConnectionError):
            raise ConnectionError(
                f"Connection error: Unable to connect to the Jira server: {e}"
            )
        elif isinstance(e, requests.Timeout):
            raise TimeoutError("Request timed out.")
        else:
            raise Exception(f"An unexpected error occurred while {action}: {str(e)}")
