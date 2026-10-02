"""Example: mixed run_as connectors — read as the user, write as the deployment.

This workflow combines two connectors that run as *different* identities,
selected per-connector via ``run_as=``:

* **GitHub** with ``run_as="auto"`` — ``auto`` follows the workflow's
  ``on_behalf_of`` flag, so on this OBO workflow the recent pull requests are
  read **on behalf of the triggering user**, i.e. *that user's* PRs.
* **Notion** with ``run_as="deployment"`` — the summary page is written
  using the **deployment's own service identity** (whoever deployed the
  worker), regardless of who triggered the run.  The page therefore
  always lands in the deployer's Notion workspace, not the user's.

The net effect: "list my open PRs" runs as the user, but the resulting
Notion page is authored by the deployment's account.

Run the worker::

    python -m mistralai.workflows.plugins.mistralai.connectors.examples.github_prs_to_notion
"""

from __future__ import annotations

import asyncio
from typing import Any

import pydantic
import structlog

import mistralai.workflows as workflows
from mistralai.workflows import Depends
from mistralai.workflows.core.logging import setup_logging
from mistralai.workflows.plugins.mistralai.connectors import (
    ToolCallClient,
    connector,
    uses_connectors,
)

logger = structlog.get_logger(__name__)

github_connector = connector("github_app")
notion_connector = connector("Notion", run_as="deployment")


class PrsToNotionPrompt(pydantic.BaseModel):
    owner: str
    repo: str
    parent_page_id: str


@workflows.activity(name="list-user-pull-requests")
async def list_user_pull_requests(
    owner: str,
    repo: str,
    github: ToolCallClient = Depends(github_connector),
) -> Any:
    """List the triggering user's recent pull requests via the GitHub connector."""
    return await github.call_tool(
        tool_name="list_pull_requests",
        arguments={
            "owner": owner,
            "repo": repo,
            "state": "all",
            "sort": "updated",
            "direction": "desc",
            "perPage": 10,
        },
    )


@workflows.activity(name="write-prs-to-notion")
async def write_prs_to_notion(
    parent_page_id: str,
    title: str,
    content: str,
    notion: ToolCallClient = Depends(notion_connector),
) -> Any:
    """Write the PR summary to a Notion page using the deployment's identity."""
    return await notion.call_tool(
        tool_name="notion-create-pages",
        arguments={
            "parent": {"page_id": parent_page_id},
            "pages": [
                {
                    "properties": {"title": title},
                    "content": content,
                },
            ],
        },
    )


def _format_pull_requests(pull_requests: Any) -> str:
    items = pull_requests if isinstance(pull_requests, list) else [pull_requests]
    lines = [f"- {pr.get('title', pr)}" for pr in items]
    return "\n".join(lines) if lines else "No pull requests found."


@workflows.workflow.define(name="github-prs-to-notion", on_behalf_of=True)
@uses_connectors(github_connector, notion_connector)
class GitHubPrsToNotionWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, prompt: PrsToNotionPrompt) -> Any:
        pull_requests = await list_user_pull_requests(prompt.owner, prompt.repo)
        return await write_prs_to_notion(
            prompt.parent_page_id,
            title=f"Recent pull requests in {prompt.owner}/{prompt.repo}",
            content=_format_pull_requests(pull_requests),
        )


if __name__ == "__main__":
    from mistralai.workflows.core.config.config import config

    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([GitHubPrsToNotionWorkflow]))
