import inspect
from typing import Annotated, Iterable, override

import atlassian
import fastmcp
import httpx
import markdownify
import pydantic

from bir_mcp.atlassian.utils import (
    confluence_highlight_to_markdown_bold,
    generate_directed_linked_issues,
    infer_jira_field_representation,
    normalize_line_breaks,
)
from bir_mcp.core import AhttpxMixin, BaseMcp, build_readonly_tools, build_write_tools
from bir_mcp.utils import (
    araise_for_status,
    build_url,
    filter_dict_by_keys,
    format_datetime_for_ai,
    prepend_url_path_prefix_if_not_present,
    to_maybe_ssl_context,
)

IssueKeyType = Annotated[
    str,
    pydantic.Field(
        description="The Jira issue key in the format {jira_project_key}-{issue_sequntial_number}, for example ABC-123"
    ),
]


class Jira(BaseMcp, AhttpxMixin):
    def __init__(
        self,
        token: str,
        url: str = "https://jira-support.kapitalbank.az",
        api_version: int = 2,
        http_timeout_seconds: int = 10,
        backoff_and_retry: bool = True,
        retry_status_codes: Iterable[int] = (413, 429, 503, 504),
        max_backoff_seconds: int = 10,
        max_backoff_retries: int = 3,
        timezone: str = "UTC",
        ssl_verify: bool | str = True,
    ):
        super().__init__(timezone=timezone)
        self.jira = atlassian.Jira(
            url=url,
            token=token,
            api_version=api_version,
            verify_ssl=bool(ssl_verify),
            timeout=http_timeout_seconds,
            backoff_and_retry=backoff_and_retry,
            retry_status_codes=retry_status_codes,
            max_backoff_retries=max_backoff_retries,
            max_backoff_seconds=max_backoff_seconds,
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.ahttpx = httpx.AsyncClient(
            base_url=url,
            headers=headers,
            event_hooks={"response": [araise_for_status]},
            timeout=http_timeout_seconds,
            verify=to_maybe_ssl_context(ssl_verify),
        )
        self.api_version = api_version
        # anon_codec: AnonCodec
        # anon_codec.anonymize

    @override
    def get_tag(self):
        return "jira"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir Jira MCP server",
            instructions=inspect.cleandoc("""
                Jira related tools.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.get_raw_issue_fields,  # TODO: need to use anon_codec.anonymize on its output.
            self.get_allowed_issue_types_for_project,
            self.search_users,
            self.get_issue_overview,
        ]
        write_tools = [
            self.create_issue,
            self.http_request,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        tools.extend(build_write_tools(write_tools, max_output_length=max_output_length, tags=tags))
        return tools

    def build_issue_url(self, issue_key: str) -> str:
        return f"{self.jira.url}/browse/{issue_key}"

    def prepend_api(self, path: str) -> str:
        return prepend_url_path_prefix_if_not_present(f"rest/api/{self.api_version}", path)

    async def get_allowed_issue_types_for_project(self, project_key: str) -> dict:
        """
        Fetch all Jira issue types allowed in the project, grouped into tasks and subtasks,
        with optional descriptions.
        """
        project = await self.ahttpx_get(f"project/{project_key}")
        project = project.json()
        issue_types = project["issueTypes"]
        tasks = {}
        subtasks = {}
        for issue_type in issue_types:
            filtered_issue_type = {issue_type["name"]: issue_type["description"]}
            if issue_type["subtask"]:
                subtasks |= filtered_issue_type
            else:
                tasks |= filtered_issue_type

        return dict(tasks=tasks, subtasks=subtasks)

    async def get_raw_issue_fields(
        self,
        issue_key: IssueKeyType,
        issue_fields: Annotated[
            Iterable[str],
            pydantic.Field(description="The fields to fetch from the Jira issue"),
        ] = ("summary", "description"),
    ) -> dict:
        """Fetch raw issue fields for given Jira issue."""
        response = await self.ahttpx_get(f"issue/{issue_key}", fields=",".join(issue_fields))
        response = response.json()
        fields = response["fields"]
        return fields

    async def get_issue_overview(self, issue_key: IssueKeyType) -> dict:
        """
        Fetch a preformatted set of general Jira issue fields and attributes,
        such as summary, description, comments, issue type, parent, subtasks,
        issue links, priority.
        """
        fields = [
            "summary",
            "description",
            "comment",
            "issuetype",
            "parent",
            "subtasks",
            "issuelinks",
            "priority",
        ]
        response = await self.ahttpx_get(f"issue/{issue_key}", fields=",".join(fields))
        fields = response.json()["fields"]
        fields = {k: infer_jira_field_representation(v) for k, v in fields.items()}

        comments = fields.pop("comment")["comments"]
        comments = sorted(comments, key=lambda c: c["created"])
        comments = [f"{c['author']['displayName']}: {c['body']}" for c in comments]
        fields["comments"] = comments

        fields["issuelinks"] = [
            f"{directed_link}: {linked_issue['key']}"
            for directed_link, linked_issue in generate_directed_linked_issues(fields)
        ]

        fields = {
            key: normalize_line_breaks(value) if isinstance(value, str) else value
            for key, value in fields.items()
        }
        fields["jira_issue_url"] = build_url(self.jira.url, "browse", issue_key)
        return fields

    async def create_issue(
        self,
        project_key: Annotated[
            str, pydantic.Field(description="The key of a Jira project to create an issue in.")
        ],
        description: str,
        summary: str,
        issue_type: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc(f"""
                    The name of a Jira issue type to create, for example Development Task, Bug, Kanban Feature.
                    Note that each project has its own set of allowed issue types, for details refer to the 
                    "{get_allowed_issue_types_for_project.__name__}" tool.
                """),
            ),
        ],
        assignee: Annotated[
            str | None,
            pydantic.Field(description="The name of a Jira user to assign the issue to."),
        ] = None,
        additional_fields: Annotated[
            dict | None, pydantic.Field(description="Additional fields to set on the Jira issue.")
        ] = None,
    ) -> dict:
        """Create a new Jira issue and get its key."""
        fields = additional_fields or {}
        fields |= {
            "summary": summary,
            "description": description,
            "project": {"key": project_key},
            "issuetype": {"name": issue_type},
        }
        if assignee:
            fields["assignee"] = {"name": assignee}

        response = await self.ahttpx_post("issue", json={"fields": fields})
        issue = response.json()
        issue_key = issue["key"]
        created_issue = {
            "created_issue_key": issue_key,
            "url": self.build_issue_url(issue_key),
        }
        return created_issue

    async def search_users(
        self,
        query: Annotated[
            str,
            pydantic.Field(
                description="The query to search users by a non-case-sensitive match of username, name or email."
            ),
        ],
    ) -> dict:
        """Search for Jira users, primarily usefull to find an exact user name."""
        response = await self.ahttpx_get("user/search", username=query)
        users = response.json()
        users = [
            filter_dict_by_keys(user, ["name", "displayName", "emailAddress"]) for user in users
        ]
        users = dict(users=users)
        return users


class Confluence(BaseMcp, AhttpxMixin):
    def __init__(
        self,
        token: str,
        url: str = "https://confluence.kapitalbank.az",
        timezone: str = "UTC",
        http_timeout_seconds: int = 10,
        ssl_verify: bool | str = True,
    ):
        super().__init__(timezone=timezone)
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.ahttpx = httpx.AsyncClient(
            base_url=url,
            headers=headers,
            event_hooks={"response": [araise_for_status]},
            timeout=http_timeout_seconds,
            verify=to_maybe_ssl_context(ssl_verify),
        )

    @override
    def get_tag(self):
        return "confluence"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir Confluence MCP server",
            instructions=inspect.cleandoc("""
                Confluence related tools.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.list_all_spaces,
            self.search,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        return tools

    def prepend_api(self, path: str) -> str:
        """
        The legacy API, rest/api, has most of the core functionality,
        while the new rest/api/v2 is for new features.
        """
        return prepend_url_path_prefix_if_not_present("rest/api", path)

    def markdownify(self, html: str) -> str:
        """See docs https://pypi.org/project/markdownify/"""
        markdown = markdownify.markdownify(
            html,
            autolinks=False,
            strip=["a"],
            heading_style="ATX",
            bullets="-",
            escape_asterisks=False,
            escape_underscores=False,
        )
        return markdown

    async def search(
        self,
        cql_query: str,
        include_whole_page_content: Annotated[
            bool,
            pydantic.Field(
                description=inspect.cleandoc("""
                    Whether to include the whole body content for each search result.
                    Note that this can make the search results prohibitively long.
                """),
            ),
        ] = False,
        convert_html_to_markdown: Annotated[
            bool,
            pydantic.Field(
                description=inspect.cleandoc("""
                    Whether to convert the HTML content of the search results into
                    more concise and readable Markdown format.
                """),
            ),
        ] = True,
        limit_results: int = 10,
    ) -> dict:
        """
        Perform search in Confluence using Confluence Query Language (CQL).
        Note that to include only pages in the search results, the CQL should contain
        a "type=page" condition.
        """
        expand = "content.body.storage" if include_whole_page_content else None
        response = await self.ahttpx_get(
            "search",
            cql=cql_query,
            limit=limit_results,
            excerpt="highlight",
            expand=expand,
        )
        results = []
        for result in response.json()["results"]:
            result = filter_dict_by_keys(result, ["title", "lastModified", "content", "excerpt"])
            for field in ["excerpt", "title"]:
                result[field] = confluence_highlight_to_markdown_bold(result[field])

            result["lastModified"] = format_datetime_for_ai(
                result["lastModified"], timespec="hours"
            )
            result["content"] = filter_dict_by_keys(result["content"], ["id", "type", "body"])
            if expand:
                body = result
                for path in expand.split(","):
                    body = body.get(path)
                    if not body:
                        break
                else:
                    if convert_html_to_markdown:
                        body = self.markdownify(body)

                    result["content"]["body"] = body

            results.append(result)

        return {"results": results}

    async def list_all_spaces(self) -> dict:
        """List all global (non-personal) spaces in Confluence."""
        response = await self.ahttpx_get("space", type="global", limit=1000)
        spaces = response.json()["results"]
        spaces = [filter_dict_by_keys(space, ["key", "name"]) for space in spaces]
        return {"spaces": spaces}
