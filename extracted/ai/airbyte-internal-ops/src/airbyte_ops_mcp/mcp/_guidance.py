# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Guidance text for MCP prompts.

This module contains prompt text constants used by the MCP server's prompt templates.
"""

# =============================================================================
# Server Instructions
# =============================================================================
# This text is provided to AI agents via the MCP protocol's "instructions" field.
# It helps agents understand when to use this server's tools, especially when
# tool search is enabled. For more context, see:
# - FastMCP docs: https://gofastmcp.com/servers/overview
# - Claude tool search: https://www.anthropic.com/news/tool-use-improvements
# =============================================================================

MCP_SERVER_INSTRUCTIONS = """
Airbyte internal operations server for connector management, cloud administration,
and production database queries.

Use this server for:
- Publishing connector prereleases and managing version overrides/pins
- Running connector regression tests (single-version and comparison modes)
- Querying the Airbyte Cloud production database for workspace, connector, sync,
  and connection diagnostics
- Triggering and monitoring GitHub Actions CI workflows
- Looking up Cloud Logging errors for debugging connector issues
- Performing repository operations on the Airbyte monorepo (for example, listing
  connectors in the repo or inspecting connector definitions)

Requirements:
- GCP credentials for database queries and Cloud Logging access
- Airbyte Cloud credentials for cloud administration operations
- GitHub token for workflow dispatch and repository operations
- Local checkout of the Airbyte repository for repo tools (typically at `../airbyte`)

Note: This server is for Airbyte internal use only.
""".strip()

# =============================================================================
# Prompt Guidance Text
# =============================================================================

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
