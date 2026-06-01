# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for internal team roster lookup.

This module exposes people lookup operations as MCP tools for AI agents.
These are thin wrappers around the core functions in internal_team_roster module.

## MCP reference

.. include:: ../../../docs/mcp-generated/people_lookup.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.internal_team_roster import fetch_roster, search_roster


class PersonRecord(BaseModel):
    """A person in the internal team roster."""

    slack_id: str | None = Field(default=None, description="Slack user ID")
    slack_display_name: str | None = Field(
        default=None, description="Slack display name"
    )
    slack_email: str | None = Field(
        default=None, description="Email address from Slack profile"
    )
    github_id: int | None = Field(default=None, description="GitHub numeric user ID")
    github_handle: str | None = Field(default=None, description="GitHub username")
    github_public_email: str | None = Field(
        default=None, description="Public email from GitHub profile"
    )


class PeopleLookupResponse(BaseModel):
    """Response from a people lookup query."""

    query: str = Field(description="The search query that was used")
    total_matches: int = Field(description="Number of matching records")
    matches: list[PersonRecord] = Field(description="Matching person records")


class RosterListResponse(BaseModel):
    """Response listing the full internal team roster."""

    total_members: int = Field(description="Total number of members in the roster")
    members: list[PersonRecord] = Field(description="All person records in the roster")


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_person(
    query: Annotated[
        str,
        Field(
            description=(
                "Search query to match against any field: email address, "
                "Slack display name, Slack user ID, GitHub handle, or GitHub user ID. "
                "Case-insensitive partial matching for strings, exact match for numeric IDs."
            )
        ),
    ],
) -> PeopleLookupResponse:
    """Look up a person in the Airbyte internal team roster.

    Searches the daily-generated roster artifact by any field value.
    The roster is built from Slack and GitHub org membership data,
    cross-referenced by email address.

    Use this to find someone's Slack ID for messaging, GitHub handle
    for code review, or to cross-reference identities across platforms.
    """
    roster = fetch_roster()
    matches = search_roster(roster, query)
    return PeopleLookupResponse(
        query=query,
        total_matches=len(matches),
        matches=[PersonRecord.model_validate(person) for person in matches],
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def list_team_roster() -> RosterListResponse:
    """List the full Airbyte internal team roster.

    Returns all members from the daily-generated roster artifact.
    The roster is sorted by Slack display name for easy scanning.
    Use lookup_person for targeted searches instead of scanning the full list.
    """
    roster = fetch_roster()
    return RosterListResponse(
        total_members=len(roster),
        members=[PersonRecord.model_validate(person) for person in roster],
    )


def register_people_lookup_tools(app: FastMCP) -> None:
    """Register people lookup tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
