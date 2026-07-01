"""Example: GitHub connector workflow that creates an issue.

The workflow uses ``@uses_connectors`` to declare a dependency on the
``"github"`` connector.  At execution time the
:class:`ConnectorAuthInterceptor` checks whether the user already has
credentials for the connector:

* **Bearer / PAT token** — if a bearer credential (e.g. a GitHub Personal
  Access Token) is stored against the connector, the interceptor finds it
  and proceeds immediately.  No interactive OAuth flow is required.
* **OAuth2** — if no credentials exist but the connector has a preset
  OAuth2 app configuration, the interceptor emits an ``auth_url``
  task-event so the UI (or client helper) can trigger the OAuth flow.

The workflow itself only declares ``connector("github")`` — it does not
need to know which auth mechanism is used.  The right credential is
resolved automatically.

Run the worker::

    python -m mistralai.workflows.plugins.mistralai.connectors.examples.github_issue_creator
"""

from __future__ import annotations

import asyncio

import pydantic
import structlog

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import Depends, InteractiveWorkflow
from mistralai.workflows.core.logging import setup_logging
from mistralai.workflows.plugins.mistralai.connectors import (
    ToolCallClient,
    connector,
    uses_connectors,
)

logger = structlog.get_logger(__name__)

github_connector = connector("github_app")


class GitHubIssuePrompt(pydantic.BaseModel):
    owner: str
    repo: str
    title: str
    body: str


@workflows.activity(name="create-github-issue")
async def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    github: ToolCallClient = Depends(github_connector),
) -> None:
    """Create a GitHub issue using the connector's issue_write tool."""
    await github.call_tool(
        tool_name="issue_write",
        arguments={
            "method": "create",
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
        },
    )


@workflows.workflow.define(name="github-issue-creator", on_behalf_of=True)
@uses_connectors(github_connector)
class GitHubIssueCreatorWorkflow(InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, prompt: GitHubIssuePrompt) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        await create_github_issue(
            prompt.owner,
            prompt.repo,
            prompt.title,
            prompt.body,
        )
        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text="All done, thanks!")]
        )


if __name__ == "__main__":
    from mistralai.workflows.core.config.config import config

    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([GitHubIssueCreatorWorkflow]))
