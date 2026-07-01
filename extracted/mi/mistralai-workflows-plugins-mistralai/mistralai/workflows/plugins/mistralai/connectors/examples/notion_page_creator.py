"""Example: Notion connector workflow that creates pages.

The workflow uses ``@uses_connectors`` to declare a dependency on Notion.
At execution time the :class:`ConnectorAuthInterceptor` checks whether the
connector is already authenticated.  If not it pauses the workflow, emits
an ``auth_url`` task-event so the UI can show an OAuth button, and polls
the connector credentials API until the user completes the OAuth flow.

Run::

    python -m mistralai.workflows.plugins.mistralai.connectors.examples.notion_page_creator
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

notion_connector = connector("Notion")


class NotionPagePrompt(pydantic.BaseModel):
    parent_page_id: str
    title: str
    content: str


@workflows.activity(name="create-notion-page")
async def create_notion_page(
    parent_page_id: str,
    title: str,
    content: str,
    notion: ToolCallClient = Depends(notion_connector),
) -> dict[str, Any]:
    """Create a Notion page using the connector's notion-create-pages tool."""
    return await notion.call_tool(  # type: ignore[no-any-return]
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


@workflows.workflow.define(name="notion-page-creator", on_behalf_of=True)
@uses_connectors(notion_connector)
class NotionPageCreatorWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, prompt: NotionPagePrompt) -> dict[str, Any]:
        return await create_notion_page(
            prompt.parent_page_id,
            prompt.title,
            prompt.content,
        )


if __name__ == "__main__":
    from mistralai.workflows.core.config.config import config

    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([NotionPageCreatorWorkflow]))
