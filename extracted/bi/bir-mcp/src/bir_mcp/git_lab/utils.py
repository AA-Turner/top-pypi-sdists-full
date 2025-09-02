import re
import string

import gitlab as gl
import httpx
import pydantic

from bir_mcp.utils import filter_dict_by_keys, value_to_key


class GraphqlGlobalId(pydantic.BaseModel):
    """
    GitLab GraphQL often uses global ids for object identifiers,
    see https://docs.gitlab.com/api/graphql/#global-ids
    """

    global_id: str
    schema: str
    provider: str
    path: list[str]
    entity_id: int

    @staticmethod
    def from_global_id(global_id: str):
        schema, path = global_id.split("://")
        provider, *path, entity_id = path.split("/")
        global_id = GraphqlGlobalId(
            global_id=global_id,
            schema=schema,
            provider=provider,
            path=path,
            entity_id=int(entity_id),
        )
        return global_id


async def aget_project_id_from_path(graphql: gl.AsyncGraphQL, project: str) -> int:
    query = """
        query {
            project(fullPath: "$project") {
                id
            }
        }
    """
    result = await aexecute_parametrized_graphql_query(graphql, query, project=project)
    global_id = result["project"]["id"]
    global_id = GraphqlGlobalId.from_global_id(global_id)
    return global_id.entity_id


class MergeRequest(pydantic.BaseModel):
    project_path: str
    merge_request_iid: int


class GitLabUrl:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip("/")
        re_base_url = re.escape(self.base_url)
        project_path = rf"({re_base_url}/)?(?P<project_path>[\w\-/]+)"
        merge_request = rf"{project_path}/-/merge_requests/(?P<merge_request_iid>\d+)"
        self.project_path_pattern = re.compile(project_path)
        self.merge_request_pattern = re.compile(merge_request)

    def extract_project_path(self, project_path_or_url: str) -> str:
        match = self.project_path_pattern.match(project_path_or_url)
        if not match:
            raise ValueError(
                f"String '{project_path_or_url}' does not fit expected pattern for GitLab project:\n"
                f"{self.project_path_pattern.pattern}"
            )

        project_path = match.groupdict()["project_path"].strip("/")
        return project_path

    def extract_merge_request(self, merge_request_url: str) -> MergeRequest:
        match = self.merge_request_pattern.match(merge_request_url)
        if not match:
            raise ValueError(
                f"String '{merge_request_url}' does not fit expected pattern for GitLab merge request:\n"
                f"{self.merge_request_pattern.pattern}"
            )

        merge_request = MergeRequest(**match.groupdict())
        return merge_request

    def build_merge_request_comment_url(
        self, project_path_or_url: str, merge_request_iid: int, note_id: int
    ) -> str:
        project_path = self.extract_project_path(project_path_or_url)
        url = f"{self.base_url}/{project_path}/-/merge_requests/{merge_request_iid}#note_{note_id}"
        return url


def get_merge_request_diffs(gitlab: gl.Gitlab, project: str, merge_request_iid: int) -> dict:
    project = gitlab.projects.get(project)
    merge_request = project.mergerequests.get(merge_request_iid)
    # https://docs.gitlab.com/api/merge_requests/#get-single-merge-request-changes
    changes = merge_request.changes(access_raw_diffs=True, unidiff=True)
    changes = [
        filter_dict_by_keys(change, ["old_path", "new_path", "diff"])
        for change in changes["changes"]
    ]
    merge_request = filter_dict_by_keys(merge_request.asdict(), ["title", "description"])
    merge_request |= {"changes": changes}
    return merge_request


async def aget_merge_request_data(
    project: str,
    merge_request_iid: int,
    agraphql: gl.AsyncGraphQL,
    ahttpx_client: httpx.AsyncClient,
    access_raw_diffs: bool = True,
    unidiff: bool = True,
    api_version: int = 4,
) -> dict:
    """https://docs.gitlab.com/api/merge_requests/#get-single-merge-request-changes"""
    project_id = await aget_project_id_from_path(agraphql, project)
    changes_url = (
        f"api/v{api_version}/projects/{project_id}/merge_requests/{merge_request_iid}/changes"
    )
    response = await ahttpx_client.get(
        changes_url, params=dict(access_raw_diffs=access_raw_diffs, unidiff=unidiff)
    )
    merge_request = response.json()
    merge_request = filter_dict_by_keys(merge_request, ["title", "description", "changes"])
    merge_request["changes"] = [
        filter_dict_by_keys(change, ["old_path", "new_path", "diff"])
        for change in merge_request["changes"]
    ]
    return merge_request


async def aexecute_parametrized_graphql_query(
    graphql: gl.AsyncGraphQL, query: str, **parameters
) -> dict:
    query = string.Template(query).substitute(parameters)
    result = await graphql.execute(query)
    return result


async def aget_all_schema_types(graphql: gl.AsyncGraphQL) -> dict[str, str]:
    query = """
        query {
            __schema {
                types {
                    name
                    kind
                }
            }
        }
    """
    result = await graphql.execute(query)
    types = value_to_key(result["__schema"]["types"], "name")
    return types


async def aget_all_entity_type_fields(
    graphql: gl.AsyncGraphQL, entity_type: str, include_datatype_metadata: bool = False
) -> dict:
    """Note that entity_type is case-sensitive."""
    datatype_metadata = """
        type {
            name
            kind
            ofType {
                name
                kind
            }
        }
    """
    query = """
        query {
        __type(name: "$entity_type") {
            fields {
                name
                description
                $datatype_metadata
                args {
                    name
                    description
                    $datatype_metadata
                }
            }
        }
    }
    """
    result = await aexecute_parametrized_graphql_query(
        graphql,
        query,
        entity_type=entity_type,
        datatype_metadata=datatype_metadata if include_datatype_metadata else "",
    )
    fields = result["__type"]["fields"]
    for field in fields:
        field["args"] = value_to_key(field["args"], "name")

    fields = value_to_key(fields, "name")
    return fields


async def aget_merge_request_commits(
    graphql: gl.AsyncGraphQL, project: str, merge_request_iid: int, first: int = 1
) -> list:
    query = """
        query {
            project(fullPath: "$project") {
                mergeRequest(iid: "$merge_request_iid") {
                    commits(first: $first) {
                        nodes {
                            title
                            message
                            diffs {
                                oldPath
                                newPath
                                diff
                            }
                        }
                    }
                }
            }
        }
    """
    result = await aexecute_parametrized_graphql_query(
        graphql, query, project=project, merge_request_iid=merge_request_iid, first=first
    )
    commits = result["project"]["mergeRequest"]["commits"]["nodes"]
    return commits


def get_ansi_escape_pattern() -> str:
    return r"\x1b\[[;\d]*[A-Za-z]"


def get_gitlab_pat_scopes(gitlab: gl.Gitlab) -> list[str]:
    pat = gitlab.personal_access_tokens.get("self")
    scopes = sorted(pat.scopes)
    return scopes
