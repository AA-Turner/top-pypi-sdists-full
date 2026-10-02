"""Example: Agentic workflow that lists recent pull requests.

Given a repository name (e.g. ``"myrepo"``), the agent fetches
recent pull requests and summarises them.

Unlike ``github_issue_creator.py`` which calls connector tools directly
via ``ToolCallClient``, this example passes the connector to the
conversation API so the agent can use GitHub tools autonomously.

Run the worker::

    python -m mistralai.workflows.plugins.mistralai.connectors.examples.github_agent
"""

from __future__ import annotations

import asyncio

import pydantic
import structlog

import mistralai.workflows as workflows
from mistralai.workflows.plugins.mistralai import Agent, Runner
from mistralai.workflows.plugins.mistralai.connectors import (
    connector,
    uses_connectors,
)
from mistralai.workflows.plugins.mistralai.session.session import FinalOutputs

logger = structlog.get_logger(__name__)

github_connector = connector("github_app")


class GitHubAgentPrompt(pydantic.BaseModel):
    repo: str  # e.g. "myrepo"


@workflows.activity(name="extract-text-from-output")
async def extract_text(outputs: FinalOutputs) -> str:
    """Extract text content from agent outputs (runs outside the workflow sandbox)."""
    from mistralai.client import models as mistralai_models

    return "\n".join(chunk.text for chunk in outputs if isinstance(chunk, mistralai_models.TextChunk))


@workflows.workflow.define(name="github-agent", on_behalf_of=True)
@uses_connectors(github_connector)
class GitHubAgentWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, prompt: GitHubAgentPrompt) -> str:
        agent = Agent(
            name="github-pr-lister",
            model="mistral-medium-latest",
            instructions=(
                f"You have access to the GitHub repository {prompt.repo}. "
                "List the most recent pull requests I interacted with and give a short summary of each."
            ),
            connectors=[github_connector],
        )
        result = await Runner.run(
            agent=agent,
            inputs=f"List the recent pull requests on {prompt.repo}.",
        )
        return await extract_text(result)


if __name__ == "__main__":
    from mistralai.workflows.core.config.config import config
    from mistralai.workflows.core.logging import setup_logging

    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([GitHubAgentWorkflow]))
