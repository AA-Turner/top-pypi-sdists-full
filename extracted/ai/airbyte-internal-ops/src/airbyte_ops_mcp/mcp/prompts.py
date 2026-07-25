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

TEST_MY_TOOLS_GUIDANCE = """
Test all available tools in this MCP server to confirm they are working properly.

Guidelines:
- Iterate through each tool systematically
- Use read-only operations whenever possible
- For tools that modify data, use test/safe modes or skip if no safe testing method exists
- Avoid creating persistent side effects (e.g., don't create real resources, connections, or data)
- Document which tools were tested and their status
- Report any errors or issues encountered
- Provide a summary of the test results at the end

Focus on validating that tools:
1. Accept their required parameters correctly
2. Return expected output formats
3. Handle errors gracefully
4. Connect to required services (if applicable)

Test Environment:
- If declared, use the `AIRBYTE_CLOUD_TEST_WORKSPACE_ID` env var to identify the test workspace.
- If the env var is not declared (and if you have access), you may use the designated test
  workspace "19d7a891-8e0e-40ac-8a8c-5faf8d11e47c" for your tests.
- Always describe to your user exactly which workspace you are using for testing, and how you
  determined the workspace to use.

Testing git ops that require an airbyte repo checkout (e.g. "list connectors in repo"):
- Assume you have the airbyte repo checked out at `../airbyte`.

Testing Version Pinning:
- A persistent test connector is available in the test workspace for version override testing:
  - **Source ID:** `e465c30e-e1c1-4713-866c-fa503109c06c`
  - **Type:** source-faker
  - **Name:** "DO-NOT-DELETE mcp-testing source-faker for version override tests"
  - **URL:** https://cloud.airbyte.com/workspaces/19d7a891-8e0e-40ac-8a8c-5faf8d11e47c/source/e465c30e-e1c1-4713-866c-fa503109c06c
- Use this connector ID if it exists for faster testing. If it doesn't exist or you need a fresh
  connector, you can deploy a new one using the Airbyte (Coral) MCP server with source-faker
  and config `{"count":100,"seed":123,"parallelism":1}`.
- Between setting and unsetting version pinning, print the url of the deployed connector to the user
  so they can verify the version pinning took effect if they wish.

Be efficient and practical in your testing approach.
""".strip()


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
