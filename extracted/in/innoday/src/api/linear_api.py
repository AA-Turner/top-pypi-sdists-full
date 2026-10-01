"""
Linear GraphQL API client.

Linear uses a single GraphQL endpoint. Auth uses the API key directly
(no Bearer prefix) in the Authorization header.
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)


class LinearAPIError(RuntimeError):
    """A Linear call failed, with Linear's own explanation attached.

    `http_status` is set when Linear answered with an HTTP error (auth, rate
    limit, outage, a query Linear could not validate), and is None when the
    request succeeded but GraphQL returned errors -- e.g. a feature the
    workspace's plan does not include.
    """

    def __init__(self, message: str, http_status: Optional[int] = None):
        super().__init__(message)
        self.http_status = http_status


_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def is_uuid(value: str) -> bool:
    """
    True if `value` looks like a UUID rather than a Linear team key ("UI").

    Linear team identifiers appear in two shapes depending on where they
    came from: the real team UUID (what GraphQL mutations require) or the
    short key shown in a team's URL (/team/<key>/...), which is NOT
    interchangeable with the UUID for mutations. Used both at board
    registration time and as a defensive re-check at adapter init time for
    boards registered before that resolution existed.
    """
    return bool(_UUID_RE.match(value))


_ISSUE_FIELDS = """
    id
    identifier
    title
    description
    state { name }
    priority
    url
    assignee { id name email }
    parent { id identifier }
    labels { nodes { name } }
    updatedAt
    completedAt
"""

_WORKFLOW_STATE_FIELDS = """
    id
    name
    type
    position
"""


class LinearAPI:
    """HTTP client for the Linear GraphQL API."""

    BASE_URL = "https://api.linear.app/graphql"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Linear API key is required")
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json",
        }

    async def _execute(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a GraphQL query and return the response dict.

        A GraphQL *validation* failure comes back as HTTP 400 with the reason
        in the body -- and `raise_for_status()` alone discards exactly that
        body, leaving "Client error '400 Bad Request' for url ..." as the only
        thing recorded on the failed `BoardSyncHistory` row. That message names
        no field and no type, so a schema change on Linear's side reads as a
        generic network fault. Carry the body through.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.BASE_URL,
                headers=self.headers,
                json={"query": query, "variables": variables},
                timeout=30.0,
            )
            if response.is_error:
                raise LinearAPIError(
                    f"Linear returned HTTP {response.status_code}: {response.text[:500]}",
                    http_status=response.status_code,
                )
            data = response.json()
            if "errors" in data:
                # `LinearAPIError`, not a bare `ValueError`. A GraphQL error is a
                # Linear failure, and it is the sibling of the HTTP branch above --
                # spelling one as a `ValueError` made it indistinguishable from a
                # programming mistake to every caller that tells those apart, and
                # `ValueError` is a class so broad (`json.JSONDecodeError`,
                # `pydantic.ValidationError`, `UnicodeDecodeError`) that no caller
                # can treat it as "an explanation meant for a person".
                raise LinearAPIError(f"GraphQL errors: {data['errors']}")
            return data

    async def get_team(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Fetch team info by ID."""
        query = """
        query GetTeam($teamId: String!) {
            team(id: $teamId) {
                id
                name
                key
                description
            }
        }
        """
        result = await self._execute(query, {"teamId": team_id})
        return result.get("data", {}).get("team")

    async def resolve_team_id_by_key(self, team_key: str) -> Optional[str]:
        """
        Resolve a Linear team key (e.g. "UI", "PF" -- the short code shown in
        a team's URL, /team/<key>/...) to its underlying team UUID.

        Linear's `team(id: ...)` query only accepts a real UUID, not the key,
        so a URL like linear.app/<workspace>/team/UI/all needs this lookup
        before the key can be used as a teamId in mutations (e.g. issueCreate).
        """
        query = """
        query ResolveTeamByKey($key: String!) {
            teams(filter: { key: { eq: $key } }) {
                nodes { id key name }
            }
        }
        """
        result = await self._execute(query, {"key": team_key})
        nodes = result.get("data", {}).get("teams", {}).get("nodes", [])
        return nodes[0]["id"] if nodes else None

    async def get_team_issues(
        self,
        team_id: str,
        updated_after: Optional[datetime] = None,
        cursor: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch all issues for a team, handling cursor-based pagination.

        Args:
            team_id: Linear team ID
            updated_after: If provided, only fetch issues updated after this datetime
            cursor: Pagination cursor (used internally for recursion)
        """
        filter_clause = ""
        variables: Dict[str, Any] = {"teamId": team_id, "cursor": cursor}

        if updated_after:
            filter_clause = ", filter: { updatedAt: { gte: $updatedAfter } }"
            variables["updatedAfter"] = updated_after.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # `IssueFilter.updatedAt` is a `DateTimeOrDuration`, NOT a
        # `DateComparator`. Declaring the wrong type fails GraphQL *validation*
        # -- HTTP 400, "used in position expecting type DateTimeOrDuration" --
        # so every call that passes `updated_after` failed while the unfiltered
        # full-board pull kept working. That asymmetry is what hid it: the only
        # caller that scopes by window is the summary engine's sync, which
        # treats a failure as "stale data is fine" and reports success anyway.
        updated_after_arg = (
            ", $updatedAfter: DateTimeOrDuration" if updated_after else ""
        )

        query = f"""
        query GetTeamIssues($teamId: String!, $cursor: String{updated_after_arg}) {{
            team(id: $teamId) {{
                issues(first: 100, after: $cursor{filter_clause}) {{
                    nodes {{
                        {_ISSUE_FIELDS}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
            }}
        }}
        """
        result = await self._execute(query, variables)
        team_data = result.get("data", {}).get("team", {})
        issues_data = team_data.get("issues", {})
        nodes = issues_data.get("nodes", [])
        page_info = issues_data.get("pageInfo", {})

        if page_info.get("hasNextPage") and page_info.get("endCursor"):
            next_page = await self.get_team_issues(
                team_id, updated_after=updated_after, cursor=page_info["endCursor"]
            )
            nodes.extend(next_page)

        return nodes

    async def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single issue by ID."""
        query = f"""
        query GetIssue($issueId: String!) {{
            issue(id: $issueId) {{
                {_ISSUE_FIELDS}
            }}
        }}
        """
        result = await self._execute(query, {"issueId": issue_id})
        return result.get("data", {}).get("issue")

    async def create_issue(
        self, team_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new issue in the team."""
        query = f"""
        mutation CreateIssue($input: IssueCreateInput!) {{
            issueCreate(input: $input) {{
                success
                issue {{
                    {_ISSUE_FIELDS}
                }}
            }}
        }}
        """
        issue_input: Dict[str, Any] = {
            "teamId": team_id,
            "title": data.get("title") or data.get("summary", ""),
            "description": data.get("description", ""),
        }
        if data.get("assignee_id"):
            issue_input["assigneeId"] = data["assignee_id"]
        if data.get("state_id"):
            issue_input["stateId"] = data["state_id"]

        result = await self._execute(query, {"input": issue_input})
        create_result = result.get("data", {}).get("issueCreate", {})
        if create_result.get("success"):
            return create_result.get("issue")
        return None

    async def update_issue(
        self, issue_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing issue."""
        query = f"""
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {{
            issueUpdate(id: $id, input: $input) {{
                success
                issue {{
                    {_ISSUE_FIELDS}
                }}
            }}
        }}
        """
        result = await self._execute(query, {"id": issue_id, "input": data})
        update_result = result.get("data", {}).get("issueUpdate", {})
        if update_result.get("success"):
            return update_result.get("issue")
        return None

    async def add_comment(self, issue_id: str, body: str) -> bool:
        """Add a comment to an issue."""
        query = """
        mutation AddComment($input: CommentCreateInput!) {
            commentCreate(input: $input) {
                success
            }
        }
        """
        result = await self._execute(
            query, {"input": {"issueId": issue_id, "body": body}}
        )
        return result.get("data", {}).get("commentCreate", {}).get("success", False)

    async def get_team_release_pipelines(self, team_id: str) -> List[Dict[str, Any]]:
        """The release pipelines linked to a team (Linear's Releases feature).

        Releases are a Business/Enterprise feature, so on other plans this can
        fail or come back empty -- callers treat either as "no release line".
        """
        query = """
        query GetTeamReleasePipelines($teamId: String!) {
            team(id: $teamId) {
                releasePipelines(first: 50) {
                    nodes {
                        id name type isProduction
                        stages { nodes { id type position } }
                        teams { nodes { id } }
                    }
                }
            }
        }
        """
        result = await self._execute(query, {"teamId": team_id})
        team = (result.get("data") or {}).get("team") or {}
        return (team.get("releasePipelines") or {}).get("nodes") or []

    async def get_pipeline_releases(
        self, pipeline_id: str, cursor: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Every release in a pipeline, each with its stage and all its issues.

        Paginates releases, and each release's issues, so a release holding
        more than one page of issues is never silently truncated -- a missing
        issue here would read as "not in this release".

        **Archived rows are included, both releases and issues.** Linear
        leaves them out by default and archives on its own (old completed
        releases, closed issues after a while), so leaving them out would read
        as "the board deleted this release" or "the ticket was removed".
        """
        query = """
        query GetPipelineReleases($pipelineId: String!, $cursor: String) {
            releasePipeline(id: $pipelineId) {
                releases(first: 50, after: $cursor, includeArchived: true) {
                    nodes {
                        id
                        name
                        version
                        archivedAt
                        stage { type }
                        issues(first: 50, includeArchived: true) {
                            nodes { identifier }
                            pageInfo { hasNextPage endCursor }
                        }
                    }
                    pageInfo { hasNextPage endCursor }
                }
            }
        }
        """
        result = await self._execute(
            query, {"pipelineId": pipeline_id, "cursor": cursor}
        )
        pipeline = (result.get("data") or {}).get("releasePipeline") or {}
        releases_data = pipeline.get("releases") or {}
        releases = releases_data.get("nodes") or []

        for release in releases:
            issues = release.get("issues") or {}
            page = issues.get("pageInfo") or {}
            if page.get("hasNextPage") and page.get("endCursor"):
                issues["nodes"] = (issues.get("nodes") or []) + (
                    await self._get_release_issues(release["id"], page["endCursor"])
                )

        page_info = releases_data.get("pageInfo") or {}
        if page_info.get("hasNextPage") and page_info.get("endCursor"):
            releases.extend(
                await self.get_pipeline_releases(
                    pipeline_id, cursor=page_info["endCursor"]
                )
            )
        return releases

    async def create_release(
        self,
        pipeline_id: str,
        version: str,
        stage_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a release in a pipeline; `name` and `version` are both the version."""
        query = """
        mutation CreateRelease($input: ReleaseCreateInput!) {
            releaseCreate(input: $input) {
                success
                release { id name version stage { type } }
            }
        }
        """
        release_input: Dict[str, Any] = {
            "pipelineId": pipeline_id,
            "name": version,
            "version": version,
        }
        if stage_id:
            release_input["stageId"] = stage_id
        result = await self._execute(query, {"input": release_input})
        payload = (result.get("data") or {}).get("releaseCreate") or {}
        if not payload.get("success") or not payload.get("release"):
            raise LinearAPIError(f"Linear did not create release {version}")
        return payload["release"]

    async def update_release(self, release_id: str, changes: Dict[str, Any]) -> None:
        """Rename a release or move its stage (`ReleaseUpdateInput` fields)."""
        query = """
        mutation UpdateRelease($id: String!, $input: ReleaseUpdateInput!) {
            releaseUpdate(id: $id, input: $input) { success }
        }
        """
        result = await self._execute(query, {"id": release_id, "input": changes})
        if not ((result.get("data") or {}).get("releaseUpdate") or {}).get("success"):
            raise LinearAPIError(f"Linear did not update release {release_id}")

    async def add_issue_to_release(self, issue_id: str, release_id: str) -> None:
        query = """
        mutation AddIssueToRelease($input: IssueToReleaseCreateInput!) {
            issueToReleaseCreate(input: $input) { success }
        }
        """
        result = await self._execute(
            query, {"input": {"issueId": issue_id, "releaseId": release_id}}
        )
        if not ((result.get("data") or {}).get("issueToReleaseCreate") or {}).get(
            "success"
        ):
            raise LinearAPIError(f"Linear did not attach {issue_id} to {release_id}")

    async def remove_issue_from_release(self, issue_id: str, release_id: str) -> None:
        query = """
        mutation RemoveIssueFromRelease($issueId: String!, $releaseId: String!) {
            issueToReleaseDeleteByIssueAndRelease(
                issueId: $issueId, releaseId: $releaseId
            ) { success }
        }
        """
        result = await self._execute(
            query, {"issueId": issue_id, "releaseId": release_id}
        )
        data = (result.get("data") or {}).get(
            "issueToReleaseDeleteByIssueAndRelease"
        ) or {}
        if not data.get("success"):
            raise LinearAPIError(f"Linear did not detach {issue_id} from {release_id}")

    async def _get_release_issues(
        self, release_id: str, cursor: Optional[str]
    ) -> List[Dict[str, Any]]:
        """The remaining pages of one release's issues, from `cursor` on."""
        query = """
        query GetReleaseIssues($releaseId: String!, $cursor: String) {
            release(id: $releaseId) {
                issues(first: 50, after: $cursor, includeArchived: true) {
                    nodes { identifier }
                    pageInfo { hasNextPage endCursor }
                }
            }
        }
        """
        result = await self._execute(query, {"releaseId": release_id, "cursor": cursor})
        issues = ((result.get("data") or {}).get("release") or {}).get("issues") or {}
        nodes = issues.get("nodes") or []
        page = issues.get("pageInfo") or {}
        if page.get("hasNextPage") and page.get("endCursor"):
            nodes.extend(await self._get_release_issues(release_id, page["endCursor"]))
        return nodes

    async def get_team_workflow_states(self, team_id: str) -> List[Dict[str, Any]]:
        """Fetch all workflow states for a team."""
        query = f"""
        query GetWorkflowStates($teamId: String!) {{
            team(id: $teamId) {{
                states {{
                    nodes {{
                        {_WORKFLOW_STATE_FIELDS}
                    }}
                }}
            }}
        }}
        """
        result = await self._execute(query, {"teamId": team_id})
        return result.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])

    async def get_team_members(self, team_id: str) -> List[Dict[str, Any]]:
        """Fetch all members of a team."""
        query = """
        query GetTeamMembers($teamId: String!) {
            team(id: $teamId) {
                members {
                    nodes {
                        id
                        name
                        displayName
                        email
                    }
                }
            }
        }
        """
        # `displayName` as well as `name`, because they are different things and
        # only one of them is a handle. `name` is the person's full name ("Alice
        # Anderson"); `displayName` is the unique `@`-nickname Linear shows and
        # that somebody would claim as their handle. Matching an outbound
        # assignee against `name` means anyone who claimed their actual handle
        # never matches -- the common case, not an edge one.
        result = await self._execute(query, {"teamId": team_id})
        return (
            result.get("data", {}).get("team", {}).get("members", {}).get("nodes", [])
        )
