# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tool for Devin session naming.

This module exposes a Devin-specific session naming tool as an MCP endpoint.
It is a thin wrapper around the generic friendly-name generator in the
session_namer module, hard-wired to the silly-buddy scheme with Title Case
output and a contextual "aka Devin" suffix.

## MCP reference

.. include:: ../../../docs/mcp-generated/session_namer.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.session_namer import (
    NamingScheme,
    extract_session_id,
    generate_friendly_name,
)


class DevinSessionNameResponse(BaseModel):
    """Response from the Devin session naming tool."""

    session_id: str = Field(description="The input session ID")
    scheme_version: str = Field(description="The naming scheme version identifier")
    name: str = Field(
        description="The generated human-friendly session name in Title Case"
    )
    full_name: str = Field(
        description="The contextual full name including 'Devin' suffix (e.g. 'Silly Fred Devin')"
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def get_devin_session_name(
    session_id: Annotated[
        str,
        "The Devin session identifier or session URL. Accepts a raw session "
        "ID (e.g. 'b2a641e838214f91b50d0f88940ac119') or a full session URL "
        "(e.g. 'https://app.devin.ai/sessions/b2a641e8...'). The ID is "
        "extracted automatically from URLs. The same ID always produces "
        "the same name — this is a deterministic lookup, not a creation.",
    ],
) -> DevinSessionNameResponse:
    """Look up the deterministic friendly name for a Devin session.

    Uses the silly-buddy naming scheme to generate a Title Case two-word
    name (e.g. "Smelly Fred") from the session ID. The output is immutable
    and idempotent — the same session ID always yields the same name.

    If a full URL is provided instead of a bare ID, the session ID is
    extracted from the URL automatically.
    """
    resolved_id = extract_session_id(session_id)
    scheme = NamingScheme.SILLY_BUDDY
    name = generate_friendly_name(resolved_id, scheme)
    full_name = f"{name} Devin"
    return DevinSessionNameResponse(
        session_id=resolved_id,
        scheme_version="v1",
        name=name,
        full_name=full_name,
    )


def register_session_namer_tools(app: FastMCP) -> None:
    """Register session namer tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
