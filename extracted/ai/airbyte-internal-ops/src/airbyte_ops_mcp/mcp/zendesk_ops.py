# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for Zendesk Support operations.

This module exposes tools for pulling Zendesk tickets (and their comments) and
for posting internal (private, agent-only) notes to a ticket, so support
workflows can inspect and annotate ticket context through the hosted Ops MCP
server.

## MCP reference

.. include:: ../../../docs/mcp-generated/zendesk_ops.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred
# annotations are used. See: https://github.com/jlowin/fastmcp/issues/905

__all__: list[str] = []

from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.zendesk_api import (
    ZendeskAPIError,
    add_internal_note,
    add_ticket_tags,
    get_ticket,
    get_ticket_comments,
)


class ZendeskAttachment(BaseModel):
    """An attachment on a Zendesk ticket comment."""

    id: int | None = Field(default=None, description="Attachment ID.")
    file_name: str | None = Field(default=None, description="Original file name.")
    content_type: str | None = Field(default=None, description="MIME content type.")
    content_url: str | None = Field(
        default=None, description="URL to download the attachment content."
    )
    size: int | None = Field(default=None, description="File size in bytes.")


class ZendeskCustomField(BaseModel):
    """A single custom field value on a Zendesk ticket."""

    id: int | None = Field(default=None, description="Custom field ID.")
    value: str | int | float | bool | None = Field(
        default=None, description="Custom field value (may be null when unset)."
    )


class ZendeskComment(BaseModel):
    """A single comment on a Zendesk ticket."""

    id: int | None = Field(default=None, description="Comment ID.")
    author_id: int | None = Field(default=None, description="Author user ID.")
    public: bool | None = Field(
        default=None,
        description="`True` for public replies, `False` for internal notes.",
    )
    body: str = Field(default="", description="Plain-text comment body.")
    created_at: str | None = Field(
        default=None,
        description="ISO-8601 timestamp when the comment was created.",
    )
    attachments: list[ZendeskAttachment] = Field(
        default_factory=list,
        description="Files attached to the comment (metadata only).",
    )


class ZendeskTicketResponse(BaseModel):
    """Response from the `get_zendesk_ticket` tool."""

    success: bool = Field(description="Whether the ticket was retrieved.")
    message: str = Field(description="Human-readable status message.")
    ticket_id: int | None = Field(default=None, description="Zendesk ticket ID.")
    subject: str | None = Field(default=None, description="Ticket subject line.")
    status: str | None = Field(
        default=None,
        description="Ticket status (e.g. `open`, `pending`, `solved`, `closed`).",
    )
    description: str | None = Field(
        default=None,
        description="The ticket's first comment / description text.",
    )
    priority: str | None = Field(default=None, description="Ticket priority, if set.")
    tags: list[str] = Field(default_factory=list, description="Ticket tags.")
    requester_id: int | None = Field(
        default=None, description="User ID of the ticket requester."
    )
    organization_id: int | None = Field(
        default=None, description="Organization ID associated with the ticket."
    )
    created_at: str | None = Field(
        default=None, description="ISO-8601 ticket creation timestamp."
    )
    updated_at: str | None = Field(
        default=None, description="ISO-8601 ticket last-updated timestamp."
    )
    url: str | None = Field(
        default=None,
        description="Agent-facing Zendesk URL for the ticket.",
    )
    via_channel: str | None = Field(
        default=None,
        description="Channel the ticket came in through (e.g. `web`, `email`).",
    )
    via_source_rel: str | None = Field(
        default=None,
        description="Source relationship (e.g. `follow_up` for follow-up tickets).",
    )
    follow_up_source_ticket_id: int | None = Field(
        default=None,
        description=(
            "For follow-up tickets, the ID of the original (closed) ticket this "
            "one follows up on. `None` when the ticket is not a follow-up."
        ),
    )
    custom_fields: list[ZendeskCustomField] = Field(
        default_factory=list,
        description="Ticket custom fields (`id`/`value` pairs).",
    )
    comments: list[ZendeskComment] = Field(
        default_factory=list,
        description="Ticket comments, oldest first. Empty unless requested.",
    )


class ZendeskInternalNoteResponse(BaseModel):
    """Response from the `post_zendesk_internal_comment` tool."""

    success: bool = Field(description="Whether the internal note was posted.")
    message: str = Field(description="Human-readable status message.")
    ticket_id: int | None = Field(default=None, description="Zendesk ticket ID.")
    comment_id: int | None = Field(
        default=None,
        description="ID of the created comment, when Zendesk reports it.",
    )
    public: bool = Field(
        default=False,
        description="Always `False`: the note is a private, agent-only comment.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="The ticket's full tag list after the update.",
    )


class ZendeskTagsResponse(BaseModel):
    """Response from the `add_zendesk_ticket_tags` tool."""

    success: bool = Field(description="Whether the tags were added.")
    message: str = Field(description="Human-readable status message.")
    ticket_id: int | None = Field(default=None, description="Zendesk ticket ID.")
    tags: list[str] = Field(
        default_factory=list,
        description="The ticket's full tag list after the update.",
    )


def _agent_ticket_url(raw_url: str | None, ticket_id: int | None) -> str | None:
    """Derive the agent-facing ticket URL from the API `url` field."""
    if not raw_url or ticket_id is None:
        return None
    # API url looks like https://<subdomain>.zendesk.com/api/v2/tickets/123.json
    if "/api/v2/" not in raw_url:
        return None
    host = raw_url.split("/api/v2/", 1)[0]
    if not host:
        return None
    return f"{host}/agent/tickets/{ticket_id}"


def _map_attachments(raw_comment: dict[str, Any]) -> list[ZendeskAttachment]:
    """Map the `attachments` array of a raw comment into typed models."""
    raw_attachments = raw_comment.get("attachments")
    if not isinstance(raw_attachments, list):
        return []
    return [
        ZendeskAttachment(
            id=a.get("id"),
            file_name=a.get("file_name"),
            content_type=a.get("content_type"),
            content_url=a.get("content_url"),
            size=a.get("size"),
        )
        for a in raw_attachments
        if isinstance(a, dict)
    ]


def _map_custom_fields(ticket: dict[str, Any]) -> list[ZendeskCustomField]:
    """Map the ticket's `custom_fields` array into typed models."""
    raw_fields = ticket.get("custom_fields")
    if not isinstance(raw_fields, list):
        return []
    return [
        ZendeskCustomField(id=f.get("id"), value=f.get("value"))
        for f in raw_fields
        if isinstance(f, dict)
    ]


def _as_dict(value: Any) -> dict[str, Any]:
    """Return `value` when it is a dict, otherwise an empty dict."""
    return value if isinstance(value, dict) else {}


def _follow_up_source_ticket_id(via_source: dict[str, Any]) -> int | None:
    """Return the original ticket ID when the ticket is a follow-up."""
    if via_source.get("rel") != "follow_up":
        return None
    ticket_id = _as_dict(via_source.get("from")).get("ticket_id")
    return ticket_id if isinstance(ticket_id, int) else None


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_zendesk_ticket(
    ticket_id: Annotated[
        int,
        Field(description="The numeric Zendesk ticket ID to retrieve."),
    ],
    include_comments: Annotated[
        bool,
        Field(
            description=(
                "When `True`, also fetch the ticket's comments (oldest first), "
                "including any attachment metadata. Only the first page (up to "
                "100 comments) is returned. Defaults to `False` to keep "
                "responses small."
            )
        ),
    ] = False,
) -> ZendeskTicketResponse:
    """Retrieve a Zendesk Support ticket by its numeric ID.

    Returns the ticket's subject, status, description, tags, and requester/
    organization identifiers. Set `include_comments` to `True` to also pull the
    ticket's comment thread (public replies and internal notes), oldest first;
    only the first page (up to 100 comments) is returned.

    Credentials are read from the server environment (`ZENDESK_SUBDOMAIN`,
    `ZENDESK_EMAIL`, `ZENDESK_API_TOKEN`); this tool never accepts or logs them.
    """
    try:
        ticket: dict[str, Any] = get_ticket(ticket_id)
    except ZendeskAPIError as exc:
        return ZendeskTicketResponse(
            success=False,
            message=str(exc),
            ticket_id=ticket_id,
        )

    comments: list[ZendeskComment] = []
    comments_note = ""
    if include_comments:
        try:
            raw_comments = get_ticket_comments(ticket_id)
            comments = [
                ZendeskComment(
                    id=c.get("id"),
                    author_id=c.get("author_id"),
                    public=c.get("public"),
                    body=c.get("plain_body") or c.get("body") or "",
                    created_at=c.get("created_at"),
                    attachments=_map_attachments(c),
                )
                for c in raw_comments
                if isinstance(c, dict)
            ]
        except ZendeskAPIError as exc:
            comments_note = f" (comments could not be retrieved: {exc})"

    resolved_id = ticket.get("id", ticket_id)
    via = _as_dict(ticket.get("via"))
    via_source = _as_dict(via.get("source"))
    return ZendeskTicketResponse(
        success=True,
        message=f"Retrieved Zendesk ticket {resolved_id}.{comments_note}",
        ticket_id=resolved_id,
        subject=ticket.get("subject"),
        status=ticket.get("status"),
        description=ticket.get("description"),
        priority=ticket.get("priority"),
        tags=ticket.get("tags", []) or [],
        requester_id=ticket.get("requester_id"),
        organization_id=ticket.get("organization_id"),
        created_at=ticket.get("created_at"),
        updated_at=ticket.get("updated_at"),
        url=_agent_ticket_url(ticket.get("url"), resolved_id),
        via_channel=via.get("channel"),
        via_source_rel=via_source.get("rel"),
        follow_up_source_ticket_id=_follow_up_source_ticket_id(via_source),
        custom_fields=_map_custom_fields(ticket),
        comments=comments,
    )


def _created_comment_id(audit: dict[str, Any]) -> int | None:
    """Return the created comment's ID from a ticket-update `audit`, if present."""
    events = audit.get("events")
    if not isinstance(events, list):
        return None
    for event in events:
        if not isinstance(event, dict):
            continue
        if event.get("type") == "Comment" and isinstance(event.get("id"), int):
            return event["id"]
    return None


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def post_zendesk_internal_comment(
    ticket_id: Annotated[
        int,
        Field(description="The numeric Zendesk ticket ID to comment on."),
    ],
    body: Annotated[
        str,
        Field(
            description=(
                "The internal note text. Posted as a private (non-public) "
                "comment visible only to agents \u2014 NOT to the ticket "
                "requester/end user."
            )
        ),
    ],
    add_tags: Annotated[
        list[str] | None,
        Field(
            description=(
                "Optional tags to add to the ticket in the same call. Tags are "
                "appended (existing tags are preserved, never clobbered)."
            ),
        ),
    ] = None,
) -> ZendeskInternalNoteResponse:
    """Post an internal (private) note to a Zendesk ticket by its numeric ID.

    The comment is added with `public=False`, so it is an internal agent note
    and is **not** visible to the ticket requester/end user. Use it to record
    triage findings, cross-references, or context for other agents. Pass
    `add_tags` to also append tags to the ticket in the same call (existing
    tags are preserved).

    The numeric `ticket_id` must already be known; this tool does not search
    for tickets. Credentials are read from the server environment
    (`ZENDESK_SUBDOMAIN`, `ZENDESK_EMAIL`, `ZENDESK_API_TOKEN`); this tool
    never accepts or logs them.
    """
    try:
        result: dict[str, Any] = add_internal_note(ticket_id, body, add_tags=add_tags)
    except ZendeskAPIError as exc:
        return ZendeskInternalNoteResponse(
            success=False,
            message=str(exc),
            ticket_id=ticket_id,
        )

    updated_ticket = _as_dict(result.get("ticket"))
    resolved_id = updated_ticket.get("id", ticket_id)
    comment_id = _created_comment_id(_as_dict(result.get("audit")))
    tags = [tag for tag in updated_ticket.get("tags", []) or [] if isinstance(tag, str)]
    return ZendeskInternalNoteResponse(
        success=True,
        message=f"Posted internal note to Zendesk ticket {resolved_id}.",
        ticket_id=resolved_id,
        comment_id=comment_id,
        tags=tags,
    )


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def add_zendesk_ticket_tags(
    ticket_id: Annotated[
        int,
        Field(description="The numeric Zendesk ticket ID to tag."),
    ],
    tags: Annotated[
        list[str],
        Field(
            description=(
                "Tags to add to the ticket. Appended to the ticket's existing "
                "tags (never clobbered). At least one non-empty tag is required."
            )
        ),
    ],
) -> ZendeskTagsResponse:
    """Add tags to a Zendesk ticket by its numeric ID.

    Tags are Zendesk's label mechanism. This appends the supplied tags via the
    additive tags endpoint, so the ticket's existing tags are preserved and
    never overwritten. Adding a tag that is already present is a no-op.

    The numeric `ticket_id` must already be known; this tool does not search
    for tickets. Credentials are read from the server environment
    (`ZENDESK_SUBDOMAIN`, `ZENDESK_EMAIL`, `ZENDESK_API_TOKEN`); this tool
    never accepts or logs them.
    """
    try:
        result_tags = add_ticket_tags(ticket_id, tags)
    except ZendeskAPIError as exc:
        return ZendeskTagsResponse(
            success=False,
            message=str(exc),
            ticket_id=ticket_id,
        )

    return ZendeskTagsResponse(
        success=True,
        message=f"Added tags to Zendesk ticket {ticket_id}.",
        ticket_id=ticket_id,
        tags=result_tags,
    )


def register_zendesk_ops_tools(app: FastMCP) -> None:
    """Register zendesk_ops tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
