import inspect
from typing import Annotated, override

import fastmcp
import git
import pydantic

from bir_mcp.core import BaseMcp, build_readonly_tools, build_write_tools

RepoPathType = Annotated[
    str,
    pydantic.Field(
        description="The filesystem path to the local repo root or any file in the repo."
    ),
]


class Git(BaseMcp):
    @override
    def get_tag(self):
        return "git"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="MCP server with local Git tools",
            instructions=inspect.cleandoc("""
                Contains tools to work with local Git repository.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            get_local_repo_metadata,
        ]
        write_tools = [
            pull_branch,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        tools.extend(build_write_tools(write_tools, max_output_length=max_output_length, tags=tags))
        return tools


def get_local_repo_metadata(repo_path: RepoPathType = ".") -> dict:
    """
    Retrieves metadata about the Git repo in the local filesystem, such as branch names, remote urls,
    user emails from the Git config.
    """
    repo = git.Repo(repo_path, search_parent_directories=True)
    branch_names = [b.name for b in repo.branches]
    remotes = [{"name": r.name, "urls": list(r.urls)} for r in repo.remotes]
    config = repo.config_reader()
    user_emails = config.get_values(section="user", option="email")
    metadata = {
        "remotes": remotes,
        "branches": branch_names,
        "active_branch": repo.active_branch.name,
        "user_emails": user_emails,
    }
    return metadata


def pull_branch(
    branch: Annotated[str, pydantic.Field(description="The name of the branch to checkout.")],
    remote: Annotated[
        str, pydantic.Field(description="The name of the remote to fetch from.")
    ] = "origin",
    repo_path: RepoPathType = ".",
) -> dict:
    """Pull a branch from the remote to the local Git repo."""
    repo = git.Repo(repo_path, search_parent_directories=True)
    remote: git.Remote = repo.remote(remote)
    remote.fetch()
    repo.git.checkout(branch)
    remote.pull(branch)
    response = {"status": "success"}
    return response
