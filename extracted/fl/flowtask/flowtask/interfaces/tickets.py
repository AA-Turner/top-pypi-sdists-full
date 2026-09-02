"""
Jira Interface for FlowTask.

Provides centralized Jira interactions including:
- Create tickets
- Assign tickets
- List tickets
- Get ticket details
- Update tickets
- Manage ticket transitions
"""
from typing import Optional, Dict, List, Any
from jira import JIRA
from jira.exceptions import JIRAError
from navconfig.logging import logging
from ..exceptions import ComponentError, ConfigError
from ..conf import (
    JIRA_API_TOKEN,
    JIRA_USERNAME,
    JIRA_INSTANCE,
    JIRA_PROJECT,
    JIRA_SECRET_TOKEN
)
from .credentials import CredentialsInterface


class JiraInterface(CredentialsInterface):
    """
    Jira Interface for FlowTask.

    Provides centralized access to Jira operations including ticket management,
    project interactions, and user assignments.

    Credentials can be provided via:
    - Environment variables (JIRA_API_TOKEN, JIRA_USERNAME, JIRA_INSTANCE)
    - Configuration file
    - Direct credential dictionary

    Supports both Basic Auth (username + API token) and OAuth authentication.
    """

    _credentials: dict = {
        "server": str,          # Jira instance URL
        "username": str,        # Username or email
        "password": str,        # API token (preferred) or password
        "token": str,           # API token (alternative key)
        "project": str,         # Default project key
        "oauth": dict,          # OAuth credentials if using OAuth
    }

    def __init__(self, *args, **kwargs):
        self.server: Optional[str] = kwargs.get('server', None)
        self.project: Optional[str] = kwargs.get('project', None)
        self.timeout: int = kwargs.get('timeout', 60)
        self.max_retries: int = kwargs.get('max_retries', 3)

        # Jira client instance
        self._jira: Optional[JIRA] = None
        self._connection_established: bool = False

        # Default field mappings
        self.default_issue_type: str = kwargs.get('default_issue_type', 'Task')
        self.default_priority: str = kwargs.get('default_priority', 'Medium')

        # Setup logging
        self._logger = logging.getLogger('Flowtask.JiraInterface')

        super().__init__(*args, **kwargs)

    def processing_credentials(self):
        """Process credentials using the inherited CredentialsInterface."""
        super().processing_credentials()

        # Use environment variables as fallbacks
        if not self.credentials:
            self.credentials = {}

        # Server/Instance URL
        if not self.credentials.get('server'):
            self.credentials['server'] = self.get_env_value(
                'JIRA_INSTANCE',
                default=JIRA_INSTANCE
            )

        # Username
        if not self.credentials.get('username'):
            self.credentials['username'] = self.get_env_value(
                'JIRA_USERNAME',
                default=JIRA_USERNAME
            )

        # API Token/Password
        if not self.credentials.get('password') and not self.credentials.get('token'):
            token = self.get_env_value('JIRA_API_TOKEN', default=JIRA_API_TOKEN)
            if token:
                self.credentials['password'] = token
            else:
                # Fallback to secret token
                secret = self.get_env_value('JIRA_SECRET_TOKEN', default=JIRA_SECRET_TOKEN)
                if secret:
                    self.credentials['password'] = secret

        # Use 'token' as alias for 'password'
        if self.credentials.get('token') and not self.credentials.get('password'):
            self.credentials['password'] = self.credentials['token']

        # Default project
        if not self.credentials.get('project'):
            self.credentials['project'] = self.get_env_value(
                'JIRA_PROJECT',
                default=JIRA_PROJECT
            )

        # Set instance variables
        self.server = self.credentials.get('server')
        self.project = self.credentials.get('project') or self.project

        # Validate required credentials
        if not self.server:
            raise ConfigError("Jira server URL is required")
        if not self.credentials.get('username'):
            raise ConfigError("Jira username is required")
        if not self.credentials.get('password'):
            raise ConfigError("Jira API token or password is required")

    async def connect(self) -> JIRA:
        """
        Establish connection to Jira instance.

        Returns:
            JIRA: Connected Jira client instance

        Raises:
            ComponentError: If connection fails
        """
        if self._jira and self._connection_established:
            return self._jira

        try:
            self.processing_credentials()

            # Prepare authentication options
            auth_options = {
                'server': self.server,
                'timeout': self.timeout,
                'max_retries': self.max_retries
            }

            # Check if OAuth is configured
            if self.credentials.get('oauth'):
                oauth_dict = self.credentials['oauth']
                auth_options.update({
                    'oauth': oauth_dict
                })
                self._logger.info("Using OAuth authentication for Jira")
            else:
                # Use basic authentication (username + API token)
                auth_options.update({
                    'basic_auth': (
                        self.credentials['username'],
                        self.credentials['password']
                    )
                })
                self._logger.info(f"Using basic auth for Jira: {self.credentials['username']}")

            # Create Jira connection
            self._jira = JIRA(**auth_options)

            # Test connection
            server_info = self._jira.server_info()
            self._logger.info(f"✅ Connected to Jira: {server_info['serverTitle']} v{server_info['version']}")

            self._connection_established = True
            return self._jira

        except JIRAError as e:
            error_msg = f"Jira connection failed: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error connecting to Jira: {str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def close(self):
        """Close Jira connection."""
        if self._jira:
            try:
                # Close any open sessions if available
                if hasattr(self._jira, 'close'):
                    self._jira.close()
                self._connection_established = False
                self._logger.info("Jira connection closed")
            except Exception as e:
                self._logger.warning(f"Error closing Jira connection: {e}")

    async def create_ticket(
        self,
        summary: str,
        description: str = "",
        issue_type: str = None,
        project: str = None,
        priority: str = None,
        assignee: str = None,
        labels: List[str] = None,
        components: List[str] = None,
        custom_fields: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new Jira ticket.

        Args:
            summary: Ticket summary/title
            description: Ticket description
            issue_type: Issue type (defaults to 'Task')
            project: Project key (defaults to configured project)
            priority: Priority level (defaults to 'Medium')
            assignee: Username to assign ticket to
            labels: List of labels to add
            components: List of component names
            custom_fields: Dictionary of custom field values
            **kwargs: Additional fields to include

        Returns:
            Dict containing created ticket information

        Raises:
            ComponentError: If ticket creation fails
        """
        try:
            await self.connect()

            # Use defaults if not provided
            project = project or self.project
            issue_type = issue_type or self.default_issue_type
            priority = priority or self.default_priority

            if not project:
                raise ComponentError("Project key is required for ticket creation")

            # Build issue dictionary
            issue_dict = {
                'project': {'key': project},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
                'priority': {'name': priority}
            }

            # Add optional fields
            if assignee:
                issue_dict['assignee'] = {'name': assignee}

            if labels:
                issue_dict['labels'] = labels

            if components:
                issue_dict['components'] = [{'name': comp} for comp in components]

            # Add custom fields
            if custom_fields:
                issue_dict.update(custom_fields)

            # Add any additional kwargs
            issue_dict.update(kwargs)

            # Create the issue
            new_issue = self._jira.create_issue(fields=issue_dict)

            result = {
                'key': new_issue.key,
                'id': new_issue.id,
                'url': f"{self.server}/browse/{new_issue.key}",
                'summary': summary,
                'status': new_issue.fields.status.name,
                'created': new_issue.fields.created
            }

            self._logger.info(f"✅ Created Jira ticket: {new_issue.key}")
            return result

        except JIRAError as e:
            error_msg = f"Failed to create Jira ticket: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def assign_ticket(
        self,
        ticket_key: str,
        assignee: str
    ) -> Dict[str, Any]:
        """
        Assign a ticket to a user.

        Args:
            ticket_key: Jira ticket key (e.g., 'PROJ-123')
            assignee: Username to assign ticket to

        Returns:
            Dict containing assignment result

        Raises:
            ComponentError: If assignment fails
        """
        try:
            await self.connect()

            issue = self._jira.issue(ticket_key)
            self._jira.assign_issue(issue, assignee)

            result = {
                'key': ticket_key,
                'assignee': assignee,
                'assigned_at': issue.fields.updated
            }

            self._logger.info(f"✅ Assigned ticket {ticket_key} to {assignee}")
            return result

        except JIRAError as e:
            error_msg = f"Failed to assign ticket {ticket_key}: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def list_tickets(
        self,
        project: str = None,
        jql: str = None,
        max_results: int = 100,
        fields: List[str] = None,
        assignee: str = None,
        status: str = None,
        issue_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        List tickets based on criteria.

        Args:
            project: Project key to filter by
            jql: Custom JQL query string
            max_results: Maximum number of results to return
            fields: List of fields to include in response
            assignee: Filter by assignee
            status: Filter by status
            issue_type: Filter by issue type

        Returns:
            List of ticket dictionaries

        Raises:
            ComponentError: If search fails
        """
        try:
            await self.connect()

            # Build JQL query if not provided
            if not jql:
                conditions = []

                if project:
                    conditions.append(f"project = {project}")
                elif self.project:
                    conditions.append(f"project = {self.project}")

                if assignee:
                    conditions.append(f"assignee = {assignee}")

                if status:
                    conditions.append(f"status = '{status}'")

                if issue_type:
                    conditions.append(f"issuetype = '{issue_type}'")

                jql = " AND ".join(conditions) if conditions else "ORDER BY created DESC"

            # Default fields if not specified
            if not fields:
                fields = [
                    'summary', 'status', 'assignee', 'priority',
                    'created', 'updated', 'issuetype', 'description'
                ]

            # Search for issues
            issues = self._jira.search_issues(
                jql_str=jql,
                maxResults=max_results,
                fields=fields
            )

            # Format results
            results = []
            for issue in issues:
                ticket_data = {
                    'key': issue.key,
                    'id': issue.id,
                    'url': f"{self.server}/browse/{issue.key}",
                    'summary': getattr(issue.fields, 'summary', ''),
                    'status': getattr(issue.fields.status, 'name', '') if hasattr(issue.fields, 'status') else '',
                    'assignee': getattr(issue.fields.assignee, 'displayName', '') if hasattr(issue.fields, 'assignee') and issue.fields.assignee else 'Unassigned',  # noqa
                    'priority': getattr(issue.fields.priority, 'name', '') if hasattr(issue.fields, 'priority') else '',
                    'issue_type': getattr(issue.fields.issuetype, 'name', '') if hasattr(issue.fields, 'issuetype') else '',  # noqa
                    'created': getattr(issue.fields, 'created', ''),
                    'updated': getattr(issue.fields, 'updated', ''),
                    'description': getattr(issue.fields, 'description', '')
                }
                results.append(ticket_data)

            self._logger.info(f"✅ Retrieved {len(results)} tickets")
            return results

        except JIRAError as e:
            error_msg = f"Failed to list tickets: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def get_ticket(
        self,
        ticket_key: str,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific ticket.

        Args:
            ticket_key: Jira ticket key (e.g., 'PROJ-123')
            fields: List of fields to include
            expand: Comma-separated list of parameters to expand

        Returns:
            Dict containing detailed ticket information

        Raises:
            ComponentError: If ticket retrieval fails
        """
        try:
            await self.connect()

            # Get the issue
            issue = self._jira.issue(ticket_key, fields=fields, expand=expand)

            # Extract comprehensive ticket data
            ticket_data = {
                'key': issue.key,
                'id': issue.id,
                'url': f"{self.server}/browse/{issue.key}",
                'summary': getattr(issue.fields, 'summary', ''),
                'description': getattr(issue.fields, 'description', ''),
                'status': getattr(issue.fields.status, 'name', '') if hasattr(issue.fields, 'status') else '',
                'assignee': getattr(issue.fields.assignee, 'displayName', '') if hasattr(issue.fields, 'assignee') and issue.fields.assignee else 'Unassigned',  # noqa
                'assignee_email': getattr(issue.fields.assignee, 'emailAddress', '') if hasattr(issue.fields, 'assignee') and issue.fields.assignee else '',  # noqa
                'reporter': getattr(issue.fields.reporter, 'displayName', '') if hasattr(issue.fields, 'reporter') else '',  # noqa
                'priority': getattr(issue.fields.priority, 'name', '') if hasattr(issue.fields, 'priority') else '',
                'issue_type': getattr(issue.fields.issuetype, 'name', '') if hasattr(issue.fields, 'issuetype') else '',
                'project': getattr(issue.fields.project, 'key', '') if hasattr(issue.fields, 'project') else '',
                'created': getattr(issue.fields, 'created', ''),
                'updated': getattr(issue.fields, 'updated', ''),
                'resolution': getattr(issue.fields.resolution, 'name', '') if hasattr(issue.fields, 'resolution') and issue.fields.resolution else '',  # noqa
                'labels': getattr(issue.fields, 'labels', []),
                'components': [comp.name for comp in getattr(issue.fields, 'components', [])],
                'fix_versions': [ver.name for ver in getattr(issue.fields, 'fixVersions', [])],
                'affects_versions': [ver.name for ver in getattr(issue.fields, 'versions', [])]
            }

            # Add comments if expanded
            if hasattr(issue.fields, 'comment') and issue.fields.comment:
                ticket_data['comments'] = [
                    {
                        'author': comment.author.displayName,
                        'body': comment.body,
                        'created': comment.created,
                        'updated': comment.updated
                    }
                    for comment in issue.fields.comment.comments
                ]

            self._logger.info(f"✅ Retrieved ticket details: {ticket_key}")
            return ticket_data

        except JIRAError as e:
            error_msg = f"Failed to get ticket {ticket_key}: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def update_ticket(
        self,
        ticket_key: str,
        fields: Dict[str, Any] = None,
        summary: str = None,
        description: str = None,
        priority: str = None,
        labels: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing ticket.

        Args:
            ticket_key: Jira ticket key (e.g., 'PROJ-123')
            fields: Dictionary of fields to update
            summary: New summary
            description: New description
            priority: New priority
            labels: New labels list
            **kwargs: Additional fields to update

        Returns:
            Dict containing update result

        Raises:
            ComponentError: If update fails
        """
        try:
            await self.connect()

            issue = self._jira.issue(ticket_key)

            # Build update dictionary
            update_fields = fields or {}

            if summary:
                update_fields['summary'] = summary
            if description:
                update_fields['description'] = description
            if priority:
                update_fields['priority'] = {'name': priority}
            if labels:
                update_fields['labels'] = labels

            # Add additional kwargs
            update_fields.update(kwargs)

            # Perform the update
            issue.update(fields=update_fields)

            result = {
                'key': ticket_key,
                'updated_fields': list(update_fields.keys()),
                'updated_at': issue.fields.updated
            }

            self._logger.info(f"✅ Updated ticket {ticket_key}")
            return result

        except JIRAError as e:
            error_msg = f"Failed to update ticket {ticket_key}: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def transition_ticket(
        self,
        ticket_key: str,
        transition: str,
        comment: str = None,
        fields: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Transition a ticket to a new status.

        Args:
            ticket_key: Jira ticket key (e.g., 'PROJ-123')
            transition: Transition name or ID
            comment: Optional comment to add
            fields: Additional fields to set during transition

        Returns:
            Dict containing transition result

        Raises:
            ComponentError: If transition fails
        """
        try:
            await self.connect()

            issue = self._jira.issue(ticket_key)

            # Get available transitions
            transitions = self._jira.transitions(issue)
            transition_id = None

            # Find transition by name or ID
            for t in transitions:
                if t['name'].lower() == transition.lower() or t['id'] == str(transition):
                    transition_id = t['id']
                    break

            if not transition_id:
                available = [t['name'] for t in transitions]
                raise ComponentError(
                    f"Transition '{transition}' not found. Available: {available}"
                )

            # Prepare transition data
            transition_data = {}
            if comment:
                transition_data['comment'] = [{'add': {'body': comment}}]
            if fields:
                transition_data['fields'] = fields

            # Perform transition
            self._jira.transition_issue(issue, transition_id, **transition_data)

            # Get updated issue to return new status
            updated_issue = self._jira.issue(ticket_key)

            result = {
                'key': ticket_key,
                'transition': transition,
                'new_status': updated_issue.fields.status.name,
                'transitioned_at': updated_issue.fields.updated
            }

            self._logger.info(f"✅ Transitioned ticket {ticket_key} to {updated_issue.fields.status.name}")
            return result

        except JIRAError as e:
            error_msg = f"Failed to transition ticket {ticket_key}: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def add_comment(
        self,
        ticket_key: str,
        comment: str,
        visibility: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Add a comment to a ticket.

        Args:
            ticket_key: Jira ticket key (e.g., 'PROJ-123')
            comment: Comment text
            visibility: Comment visibility restrictions

        Returns:
            Dict containing comment result

        Raises:
            ComponentError: If adding comment fails
        """
        try:
            await self.connect()

            issue = self._jira.issue(ticket_key)
            new_comment = self._jira.add_comment(
                issue,
                comment,
                visibility=visibility
            )

            result = {
                'key': ticket_key,
                'comment_id': new_comment.id,
                'comment': comment,
                'author': new_comment.author.displayName,
                'created': new_comment.created
            }

            self._logger.info(f"✅ Added comment to ticket {ticket_key}")
            return result

        except JIRAError as e:
            error_msg = f"Failed to add comment to ticket {ticket_key}: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    async def get_projects(self) -> List[Dict[str, Any]]:
        """
        Get list of available projects.

        Returns:
            List of project dictionaries

        Raises:
            ComponentError: If retrieval fails
        """
        try:
            await self.connect()

            projects = self._jira.projects()

            results = [
                {
                    'key': project.key,
                    'name': project.name,
                    'id': project.id,
                    'lead': getattr(project, 'lead', {}).get('displayName', '') if hasattr(project, 'lead') else '',
                    'project_type': getattr(project, 'projectTypeKey', ''),
                    'url': f"{self.server}/browse/{project.key}"
                }
                for project in projects
            ]

            self._logger.info(f"✅ Retrieved {len(results)} projects")
            return results

        except JIRAError as e:
            error_msg = f"Failed to get projects: {e.text if hasattr(e, 'text') else str(e)}"
            self._logger.error(error_msg)
            raise ComponentError(error_msg) from e

    # Context manager support
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
