from typing import Optional, Any, List, Dict
from dataclasses import dataclass, field
from aiohttp import web
import hmac
import hashlib
from datamodel import BaseModel
from datamodel.libs.mapping import ClassDict
from datamodel.parsers.json import json_encoder, json_decoder
from ...conf import (
    JIRA_SECRET_TOKEN,
    JIRA_API_TOKEN,
    JIRA_USERNAME,
    JIRA_INSTANCE,
    JIRA_PROJECT,
)
from .http import HTTPHook


@dataclass
class AvatarUrls:
    _48x48: str = field(metadata={'alias': '48x48'})
    _24x24: str = field(metadata={'alias': '24x24'})
    _16x16: str = field(metadata={'alias': '16x16'})
    _32x32: str = field(metadata={'alias': '32x32'})

@dataclass
class User:
    self: str
    accountId: str
    avatarUrls: AvatarUrls
    displayName: str
    active: bool
    timeZone: str
    accountType: str

@dataclass
class StatusCategory:
    self: str
    id: int
    key: str
    colorName: str
    name: str

@dataclass
class Status:
    self: str
    description: str
    iconUrl: str
    name: str
    id: str
    statusCategory: StatusCategory

@dataclass
class Priority:
    self: str
    iconUrl: str
    name: str
    id: str

@dataclass
class Progress:
    progress: int
    total: int

@dataclass
class AggregateProgress:
    progress: int
    total: int

@dataclass
class Votes:
    self: str
    votes: int
    hasVoted: bool

@dataclass
class Watches:
    self: str
    watchCount: int
    isWatching: bool

@dataclass
class ProjectCategory:
    self: str
    id: str
    description: str
    name: str

@dataclass
class Project:
    self: str
    id: str
    key: str
    name: str
    projectTypeKey: str
    simplified: bool
    avatarUrls: AvatarUrls
    projectCategory: ProjectCategory

@dataclass
class IssueType:
    self: str
    id: str
    description: str
    iconUrl: str
    name: str
    subtask: bool
    avatarId: int
    hierarchyLevel: int

@dataclass
class TimeTracking:
    originalEstimate: Optional[str] = None
    remainingEstimate: Optional[str] = None
    timeSpent: Optional[str] = None

class JiraIssue(BaseModel):
    """JiraIssue.

    A BaseModel to represent a Jira Issue.
    """
    self: str
    id: str
    key: str
    event_type: str
    timestamp: int
    webhook_event: str
    issue_event_type_name: str
    issue_status: Optional[str]
    description: Optional[str]
    summary: str
    changelog: Optional[Dict]
    user: Optional[User]
    issue: dict
    fields: Optional[Dict]
    priority: Optional[Priority]
    status: Optional[Status]
    creator: Optional[User]
    reporter: Optional[User]
    aggregateprogress: AggregateProgress
    progress: Progress
    votes: Votes
    issuetype: IssueType
    project: Project
    watches: Watches
    timetracking: TimeTracking

    class Meta:
        strict: bool = False
        frozen: bool = False

class JiraTrigger(HTTPHook):
    """JiraTrigger.

    A Trigger that handles Jira webhooks for issue events.
    """

    def __init__(
        self,
        *args,
        secret_token: str = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.secret_token = secret_token or JIRA_SECRET_TOKEN
        self.username = kwargs.get('username', JIRA_USERNAME)
        self.instance = kwargs.get('instance', JIRA_INSTANCE)
        self.project = kwargs.get('project', JIRA_PROJECT)
        self.url = kwargs.get('url', '/api/v1/webhook/jira/')
        self.methods = ['POST']

    async def post(self, request: web.Request):
        try:
            # Verify the request
            if self.secret_token:
                signature = request.headers.get('X-Hub-Signature')
                if not signature:
                    return web.Response(status=401, text='Unauthorized')
                body = await request.read()
                computed_signature = 'sha256=' + hmac.new(
                    self.secret_token.encode('utf-8'),
                    body,
                    hashlib.sha256
                ).hexdigest()
                if not hmac.compare_digest(signature, computed_signature):
                    return web.Response(status=401, text='Unauthorized')
                payload = json_decoder(body)
            else:
                payload = await request.json()
            # Extract event details
            webhook_event = payload.get('webhookEvent')
            timestamp = payload.get('timestamp')
            user = payload.get('user', {})
            issue_type = payload.get('issue_event_type_name', 'issue_created')
            changelog = payload.get('changelog', {})
            issue = payload.get('issue', {})
            issue_key = issue.get('key')
            issue_fields = issue.get('fields', {})
            issue_status = issue_fields.get('status', {}).get('name')

            # Determine the event type
            event_type = None
            if webhook_event == 'jira:issue_created':
                event_type = 'created'
            elif webhook_event == 'jira:issue_updated':
                # Check if the issue was closed
                changelog = payload.get('changelog', {})
                items = changelog.get('items', [])
                for item in items:
                    if item.get('field') == 'status':
                        from_status = item.get('fromString')
                        to_status = item.get('toString')
                        if to_status.lower() == 'closed':
                            event_type = 'closed'
                        else:
                            event_type = 'updated'
                        break
                else:
                    event_type = 'updated'
            elif webhook_event == 'jira:issue_deleted':
                event_type = 'deleted'
            if event_type:
                # extracting information from issue:
                aggregateprogress = issue_fields.get('aggregateprogress', {})
                issuetype = issue_fields.get('issuetype', {})
                creator = issue_fields.get('creator', {})
                reporter = issue_fields.get('reporter', {})
                project = issue_fields.get('project', {})
                watches = issue_fields.get('watches', {})
                timetracking = issue_fields.get('timetracking', {})
                priority = issue_fields.get('priority', {})
                # Create the JiraIssue object
                jira_issue = JiraIssue(
                    event_type=event_type,
                    issue_status=issue_status,
                    timestamp=timestamp,
                    webhook_event=webhook_event,
                    issue_event_type_name=issue_type,
                    aggregateprogress=aggregateprogress,
                    issuetype=issuetype,
                    creator=creator,
                    reporter=reporter,
                    description=issue_fields.get('description'),
                    summary=issue_fields.get('summary'),
                    changelog=changelog,
                    user=user,
                    priority=priority,
                    project=project,
                    watches=watches,
                    timetracking=timetracking,
                    **issue
                )
                # Prepare data to pass to actions
                data = {
                    'webhook_event': webhook_event,
                    'event_type': event_type,
                    'issue_key': issue_key,
                    'issue_fields': issue_fields,
                    'issue': jira_issue
                }
                # Run actions
                result = await self.run_actions(**data)
                return self.response(
                    response=result,
                    status=self.default_status
                )
            else:
                return web.Response(
                    status=200,
                    text='Event ignored'
                )
        except Exception as e:
            self._logger.error(
                f"Error processing Jira webhook: {e}"
            )
            return web.Response(
                status=500,
                text='Jira: Internal Server Error'
            )
