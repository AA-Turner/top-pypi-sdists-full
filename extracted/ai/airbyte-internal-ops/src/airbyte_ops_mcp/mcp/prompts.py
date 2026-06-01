# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP prompt definitions for the Airbyte Ops MCP server.

This module defines prompts that can be invoked by MCP clients to perform
common workflows.

## MCP reference

.. include:: ../../../docs/mcp-generated/prompts.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_prompt, register_mcp_prompts
from pydantic import Field

from airbyte_ops_mcp.mcp._guidance import TEST_MY_TOOLS_GUIDANCE


@mcp_prompt(
    name="test-my-tools",
    description="Test all available MCP tools to confirm they are working properly",
)
def test_my_tools_prompt(
    scope: Annotated[
        str | None,
        Field(
            description=(
                "Optional free-form text to focus or constrain testing. "
                "This can be a single word, a sentence, or a paragraph "
                "describing the desired scope or constraints."
            ),
        ),
    ] = None,
) -> list[dict[str, str]]:
    """Generate a prompt that instructs the agent to test all available tools.

    Returns:
        List containing a single message dict with the guidance text
    """
    content = TEST_MY_TOOLS_GUIDANCE

    if scope:
        content = f"{content}\n\n---\n\nAdditional scope or constraints:\n{scope}"

    return [
        {
            "role": "user",
            "content": content,
        }
    ]


def register_prompts(app: FastMCP) -> None:
    """Register all prompts with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_prompts(app, mcp_module=__name__)
