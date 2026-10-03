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

import re
from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.zendesk_api import (
    ZendeskAPIError,
    add_internal_note,
    add_ticket_tags,
    create_ticket,
    find_organizations_by_airbyte_org_id,
    find_ticket_form_id,
    get_current_user,
    get_ticket,
    get_ticket_comments,
    list_tickets_by_external_id,
    search,
    set_ticket_email_ccs,
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
    type: str | None = Field(default=None, description="Zendesk ticket type.")
    problem_id: int | None = Field(
        default=None, description="Associated problem ticket ID, if any."
    )
    assignee_id: int | None = Field(
        default=None, description="User ID of the ticket assignee."
    )
    submitter_id: int | None = Field(
        default=None, description="User ID of the ticket submitter."
    )
    ticket_form_id: int | None = Field(
        default=None, description="Ticket form ID used by the ticket."
    )
    email_cc_ids: list[int] | None = Field(
        default=None, description="Zendesk user IDs included as email CCs."
    )
    external_id: str | None = Field(
        default=None, description="External idempotency identifier for the ticket."
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
        description=(
            "Always `False`: this tool can only create a private, agent-only "
            "note, never a customer-visible reply."
        ),
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


class ZendeskTicketSummary(BaseModel):
    """A concise Zendesk ticket search result."""

    id: int = Field(description="Zendesk ticket ID.")
    subject: str | None = Field(default=None, description="Ticket subject.")
    status: str | None = Field(default=None, description="Ticket status.")
    type: str | None = Field(default=None, description="Ticket type.")
    requester_id: int | None = Field(default=None, description="Requester user ID.")
    assignee_id: int | None = Field(default=None, description="Assignee user ID.")
    organization_id: int | None = Field(
        default=None, description="Associated organization ID."
    )
    tags: list[str] = Field(default_factory=list, description="Ticket tags.")
    external_id: str | None = Field(default=None, description="External ticket ID.")
    created_at: str | None = Field(default=None, description="Ticket creation time.")
    updated_at: str | None = Field(default=None, description="Ticket update time.")
    url: str | None = Field(default=None, description="Agent-facing ticket URL.")


class ZendeskTicketSearchResponse(BaseModel):
    """Response from `search_zendesk_tickets`."""

    success: bool = Field(description="Whether the search succeeded.")
    message: str = Field(description="Human-readable status message.")
    count: int = Field(description="Number of tickets returned.")
    tickets: list[ZendeskTicketSummary] = Field(
        default_factory=list, description="Matching Zendesk tickets."
    )


class ZendeskOrganizationSummary(BaseModel):
    """A concise Zendesk organization search result."""

    id: int = Field(description="Zendesk organization ID.")
    name: str | None = Field(default=None, description="Organization name.")
    url: str | None = Field(default=None, description="Zendesk API organization URL.")


class ZendeskOrganizationSearchResponse(BaseModel):
    """Response from `find_zendesk_organization_by_airbyte_org_id`."""

    success: bool = Field(description="Whether the search succeeded.")
    message: str = Field(description="Human-readable status message.")
    organizations: list[ZendeskOrganizationSummary] = Field(
        default_factory=list, description="Matching Zendesk organizations."
    )


class OutreachContact(BaseModel):
    """A Zendesk outreach requester or CC contact."""

    email: str = Field(description="Contact email address.")
    name: str = Field(description="Contact name.")


class ZendeskOutreachTicketResponse(BaseModel):
    """Response from `create_zendesk_outreach_ticket`."""

    success: bool = Field(description="Whether the ticket was found or created.")
    message: str = Field(description="Human-readable status message.")
    created: bool = Field(description="Whether a new ticket was created.")
    ticket_id: int | None = Field(default=None, description="Zendesk ticket ID.")
    url: str | None = Field(default=None, description="Agent-facing ticket URL.")
    status: str | None = Field(default=None, description="Ticket status.")
    type: str | None = Field(default=None, description="Ticket type.")
    problem_id: int | None = Field(default=None, description="Problem ticket ID.")
    requester_id: int | None = Field(default=None, description="Requester user ID.")
    submitter_id: int | None = Field(default=None, description="Submitter user ID.")
    assignee_id: int | None = Field(default=None, description="Assignee user ID.")
    organization_id: int | None = Field(
        default=None, description="Associated organization ID."
    )
    ticket_form_id: int | None = Field(default=None, description="Ticket form ID.")
    email_cc_ids: list[int] | None = Field(
        default=None, description="Zendesk user IDs included as email CCs."
    )
    tags: list[str] = Field(default_factory=list, description="Ticket tags.")
    duplicate_ticket_ids: list[int] = Field(
        default_factory=list,
        description="Existing ticket IDs when an external ID has duplicates.",
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
        type=ticket.get("type"),
        problem_id=ticket.get("problem_id"),
        assignee_id=ticket.get("assignee_id"),
        submitter_id=ticket.get("submitter_id"),
        ticket_form_id=ticket.get("ticket_form_id"),
        email_cc_ids=ticket.get("email_cc_ids"),
        external_id=ticket.get("external_id"),
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


def _ticket_summary(ticket: dict[str, Any]) -> ZendeskTicketSummary:
    """Map a raw Zendesk ticket into a concise search result."""
    ticket_id = ticket.get("id")
    if not isinstance(ticket_id, int):
        raise ZendeskAPIError("Zendesk search result is missing a valid ticket ID.")
    return ZendeskTicketSummary(
        id=ticket_id,
        subject=ticket.get("subject"),
        status=ticket.get("status"),
        type=ticket.get("type"),
        requester_id=ticket.get("requester_id"),
        assignee_id=ticket.get("assignee_id"),
        organization_id=ticket.get("organization_id"),
        tags=ticket.get("tags", []) or [],
        external_id=ticket.get("external_id"),
        created_at=ticket.get("created_at"),
        updated_at=ticket.get("updated_at"),
        url=_agent_ticket_url(ticket.get("url"), ticket_id),
    )


def _outreach_ticket_response(
    ticket: dict[str, Any],
    *,
    created: bool,
    message: str,
    fallbacks: dict[str, Any] | None = None,
    success: bool = True,
    duplicate_ticket_ids: list[int] | None = None,
) -> ZendeskOutreachTicketResponse:
    """Map a raw Zendesk ticket into an outreach response."""
    fallbacks = fallbacks or {}
    ticket_id = ticket.get("id")
    return ZendeskOutreachTicketResponse(
        success=success,
        message=message,
        created=created,
        ticket_id=ticket_id,
        url=_agent_ticket_url(ticket.get("url"), ticket_id),
        status=ticket.get("status") or fallbacks.get("status"),
        type=ticket.get("type") or fallbacks.get("type"),
        problem_id=ticket.get("problem_id", fallbacks.get("problem_id")),
        requester_id=ticket.get("requester_id", fallbacks.get("requester_id")),
        submitter_id=ticket.get("submitter_id", fallbacks.get("submitter_id")),
        assignee_id=ticket.get("assignee_id"),
        organization_id=ticket.get("organization_id"),
        ticket_form_id=ticket.get("ticket_form_id", fallbacks.get("ticket_form_id")),
        email_cc_ids=ticket.get("email_cc_ids", fallbacks.get("email_cc_ids")),
        tags=ticket.get("tags", fallbacks.get("tags", [])) or [],
        duplicate_ticket_ids=duplicate_ticket_ids or [],
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def search_zendesk_tickets(
    query: Annotated[
        str,
        Field(
            description="Zendesk search query; ticket searches are scoped to tickets."
        ),
    ],
    sort_by: Annotated[
        Literal["created_at", "updated_at"] | None,
        Field(description="Optional ticket field to sort by."),
    ] = None,
    sort_order: Annotated[
        Literal["asc", "desc"],
        Field(description="Sort direction."),
    ] = "desc",
    limit: Annotated[
        int,
        Field(description="Maximum number of tickets to return.", ge=1, le=1000),
    ] = 100,
) -> ZendeskTicketSearchResponse:
    """Search Zendesk tickets, with results limited to 1,000.

    If `query` has no positive `type:ticket` filter, `type:ticket` is prepended.
    Negated type filters and queries that explicitly select another record type
    are rejected.
    """
    if re.search(r"(^|\s)-\s*type\s*:", query, flags=re.IGNORECASE):
        return ZendeskTicketSearchResponse(
            success=False,
            message="Zendesk ticket search does not accept negated type filters.",
            count=0,
        )
    type_filters = re.findall(r"\btype\s*:\s*([^\s]+)", query, flags=re.IGNORECASE)
    if type_filters and any(value.casefold() != "ticket" for value in type_filters):
        return ZendeskTicketSearchResponse(
            success=False,
            message="Zendesk ticket search only accepts `type:ticket` queries.",
            count=0,
        )
    search_query = query.strip()
    if not type_filters:
        search_query = f"type:ticket {search_query}".strip()

    try:
        results = search(
            search_query,
            sort_by=sort_by,
            sort_order=sort_order,
            max_results=limit,
        )
        tickets = [_ticket_summary(ticket) for ticket in results]
    except ZendeskAPIError as exc:
        return ZendeskTicketSearchResponse(
            success=False,
            message=str(exc),
            count=0,
        )

    return ZendeskTicketSearchResponse(
        success=True,
        message=f"Found {len(tickets)} Zendesk ticket(s).",
        count=len(tickets),
        tickets=tickets,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def find_zendesk_organization_by_airbyte_org_id(
    airbyte_org_id: Annotated[
        str,
        Field(
            description="Airbyte organization UUID stored on the Zendesk organization."
        ),
    ],
) -> ZendeskOrganizationSearchResponse:
    """Find Zendesk organizations by their `airbyte_org_id` custom field."""
    try:
        organizations = find_organizations_by_airbyte_org_id(airbyte_org_id)
    except ZendeskAPIError as exc:
        return ZendeskOrganizationSearchResponse(
            success=False,
            message=str(exc),
        )

    mapped = [
        ZendeskOrganizationSummary(
            id=organization["id"],
            name=organization.get("name"),
            url=organization.get("url"),
        )
        for organization in organizations
        if isinstance(organization.get("id"), int)
    ]
    return ZendeskOrganizationSearchResponse(
        success=True,
        message=f"Found {len(mapped)} Zendesk organization(s).",
        organizations=mapped,
    )


def _outreach_tags(tags: list[str]) -> list[str]:
    """Trim and deduplicate tags, ensuring the `outreach` tag is present."""
    cleaned: list[str] = []
    seen: set[str] = set()
    has_outreach = False
    for raw_tag in tags:
        tag = raw_tag.strip()
        if not tag:
            continue
        normalized = tag.casefold()
        if normalized in seen:
            continue
        seen.add(normalized)
        if normalized == "outreach":
            cleaned.append("outreach")
            has_outreach = True
        else:
            cleaned.append(tag)
    if not has_outreach:
        cleaned.append("outreach")
    return cleaned


def _outreach_cc_contacts(
    cc: list[OutreachContact],
    requester_email: str,
) -> list[dict[str, str]]:
    """Build deduped Zendesk email CC contacts, excluding the requester."""
    requester_email_normalized = requester_email.strip().casefold()
    contacts: list[dict[str, str]] = []
    seen_emails: set[str] = set()
    for contact in cc:
        email = contact.email.strip()
        if not email:
            raise ZendeskAPIError("CC contact email must not be empty.")
        normalized_email = email.casefold()
        if normalized_email == requester_email_normalized:
            continue
        if normalized_email in seen_emails:
            continue
        seen_emails.add(normalized_email)
        contacts.append(
            {
                "user_email": email,
                "user_name": contact.name.strip(),
                "action": "put",
            }
        )
    if len(contacts) > 48:
        raise ZendeskAPIError("At most 48 unique CC contacts are allowed.")
    return contacts


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def create_zendesk_outreach_ticket(
    external_id: Annotated[
        str,
        Field(description="Idempotency key beginning with `outreach:`."),
    ],
    ticket_type: Annotated[
        Literal["problem", "incident"],
        Field(description="Zendesk ticket type."),
    ],
    subject: Annotated[str, Field(description="Non-empty ticket subject.")],
    internal_note_html: Annotated[
        str,
        Field(description="Non-empty first comment, posted as a private HTML note."),
    ],
    problem_id: Annotated[
        int | None,
        Field(description="Required parent problem ticket ID for an incident."),
    ] = None,
    tags: Annotated[list[str], Field(description="Ticket tags.")] = [],  # noqa: B006
    ticket_form_name: Annotated[
        str,
        Field(description="Active ticket form name."),
    ] = "Support Outreach",
    requester: Annotated[
        OutreachContact | None,
        Field(
            description="Requester contact; required for incidents; not allowed for problems."
        ),
    ] = None,
    cc: Annotated[
        list[OutreachContact],
        Field(
            description="Requester contacts to CC; incidents only; Zendesk allows at most 48."
        ),
    ] = [],  # noqa: B006
    assignee_email: Annotated[
        str | None,
        Field(description="Optional assignee email address."),
    ] = None,
) -> ZendeskOutreachTicketResponse:
    """Create an idempotent ticket for the approved outreach workflow only.

    This tool cannot send anything public. The first comment is always private
    and visible only to Zendesk agents.
    CCs are applied in a separate update with no comment because Zendesk does
    not update email CCs when an internal note is added in the same update.
    Re-running on an existing ticket ensures the requested CCs without posting
    another comment.
    Callers must not run concurrent calls with the same `external_id`; duplicates
    are detected after creation but not prevented.
    """
    try:
        if (
            not external_id.startswith("outreach:")
            or not external_id[len("outreach:") :].strip()
        ):
            raise ZendeskAPIError("`external_id` must begin with `outreach:`.")

        existing = list_tickets_by_external_id(external_id)
        if len(existing) > 1:
            duplicate_ids = [
                ticket["id"] for ticket in existing if isinstance(ticket.get("id"), int)
            ]
            return ZendeskOutreachTicketResponse(
                success=False,
                message=(
                    "Multiple Zendesk tickets share this external ID: "
                    f"{', '.join(map(str, duplicate_ids))}."
                ),
                created=False,
                duplicate_ticket_ids=duplicate_ids,
            )
        if existing:
            ticket = existing[0]
            if ticket_type == "incident" and cc:
                if requester is None:
                    raise ZendeskAPIError("`requester` is required for an incident.")
                if not requester.email.strip():
                    raise ZendeskAPIError("Requester email must not be empty.")
                cc_contacts = _outreach_cc_contacts(cc, requester.email)
                if cc_contacts:
                    try:
                        ticket = set_ticket_email_ccs(ticket["id"], cc_contacts)
                    except ZendeskAPIError as exc:
                        return _outreach_ticket_response(
                            ticket,
                            created=False,
                            message=(
                                f"Failed to ensure CCs for existing Zendesk ticket "
                                f"{ticket.get('id')}: {exc}"
                            ),
                            success=False,
                        )
                return _outreach_ticket_response(
                    ticket,
                    created=False,
                    message=(
                        f"Found existing Zendesk ticket {ticket.get('id')}; "
                        f"ensured {len(cc_contacts)} CCs."
                    ),
                )
            return _outreach_ticket_response(
                ticket,
                created=False,
                message=f"Found existing Zendesk ticket {ticket.get('id')}; no ticket was created.",
            )

        if ticket_type == "incident" and problem_id is None:
            raise ZendeskAPIError("`problem_id` is required for an incident.")
        if ticket_type == "problem" and problem_id is not None:
            raise ZendeskAPIError("`problem_id` is not allowed for a problem ticket.")
        if ticket_type == "incident" and requester is None:
            raise ZendeskAPIError("`requester` is required for an incident.")
        if ticket_type == "problem" and requester is not None:
            raise ZendeskAPIError(
                "`requester` is not allowed for a problem ticket; MoonBot is the requester."
            )
        if ticket_type == "problem" and cc:
            raise ZendeskAPIError("`cc` is not allowed for a problem ticket.")
        if not subject.strip():
            raise ZendeskAPIError("Ticket subject must not be empty.")
        if not internal_note_html.strip():
            raise ZendeskAPIError("Internal note body must not be empty.")
        if requester is not None and not requester.email.strip():
            raise ZendeskAPIError("Requester email must not be empty.")
        if assignee_email is not None and not assignee_email.strip():
            raise ZendeskAPIError("Assignee email must not be empty.")

        current_user = get_current_user()
        current_user_id = current_user.get("id")
        if not isinstance(current_user_id, int):
            raise ZendeskAPIError(
                "Zendesk current-user response has an invalid user ID."
            )

        requester_email = (
            requester.email.strip()
            if requester is not None
            else str(current_user.get("email") or "").strip()
        )
        cc_contacts = _outreach_cc_contacts(cc, requester_email)

        ticket_form_id = find_ticket_form_id(ticket_form_name)
        ticket_payload: dict[str, Any] = {
            "subject": subject.strip(),
            "comment": {"html_body": internal_note_html.strip(), "public": False},
            "status": "new",
            "priority": "normal",
            "type": ticket_type,
            "tags": _outreach_tags(tags),
            "external_id": external_id,
            "ticket_form_id": ticket_form_id,
            "submitter_id": current_user_id,
        }
        if ticket_type == "incident":
            ticket_payload["problem_id"] = problem_id
        if requester is None:
            ticket_payload["requester_id"] = current_user_id
        else:
            ticket_payload["requester"] = {
                "name": requester.name.strip(),
                "email": requester.email.strip(),
            }
        if assignee_email is not None:
            ticket_payload["assignee_email"] = assignee_email.strip()

        ticket = create_ticket(ticket_payload)
        try:
            post_create_tickets = list_tickets_by_external_id(external_id)
        except ZendeskAPIError as exc:
            post_create_tickets = None
            duplicate_check_error = str(exc)
        else:
            duplicate_check_error = None
    except ZendeskAPIError as exc:
        return ZendeskOutreachTicketResponse(
            success=False,
            message=str(exc),
            created=False,
        )

    response_fallbacks: dict[str, Any] = {
        "status": "new",
        "type": ticket_type,
        "problem_id": problem_id,
        "submitter_id": current_user_id,
        "ticket_form_id": ticket_form_id,
        "email_cc_ids": [],
        "tags": ticket_payload["tags"],
    }
    if requester is None:
        response_fallbacks["requester_id"] = current_user_id
    if duplicate_check_error is not None:
        return _outreach_ticket_response(
            ticket,
            created=True,
            message=(
                f"Created ticket {ticket.get('id')} but could not check for "
                "duplicate tickets for this external ID: "
                f"{duplicate_check_error}."
            ),
            fallbacks=response_fallbacks,
            success=False,
        )
    if post_create_tickets is not None and len(post_create_tickets) > 1:
        duplicate_ids = [
            existing_ticket["id"]
            for existing_ticket in post_create_tickets
            if isinstance(existing_ticket.get("id"), int)
        ]
        return _outreach_ticket_response(
            ticket,
            created=True,
            message=(
                f"Created ticket {ticket.get('id')} but found duplicate tickets "
                f"for this external ID: {', '.join(map(str, duplicate_ids))}; "
                "resolve manually."
            ),
            fallbacks=response_fallbacks,
            success=False,
            duplicate_ticket_ids=duplicate_ids,
        )
    if cc_contacts:
        try:
            ticket = set_ticket_email_ccs(ticket["id"], cc_contacts)
        except ZendeskAPIError as exc:
            return _outreach_ticket_response(
                ticket,
                created=True,
                message=(
                    f"Created ticket {ticket.get('id')} but failed to add CCs: "
                    f"{exc}; re-run to retry."
                ),
                fallbacks=response_fallbacks,
                success=False,
            )
    return _outreach_ticket_response(
        ticket,
        created=True,
        message=f"Created private outreach ticket {ticket.get('id')}.",
        fallbacks=response_fallbacks,
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
    html_body: Annotated[
        str,
        Field(
            description=(
                "The internal note as an HTML fragment. Posted as a private "
                "(non-public) comment visible only to agents \u2014 NOT to the "
                "ticket requester/end user. This server cannot post a public "
                "customer reply; if asked to reply, write a clearly labelled "
                "draft for a human agent to send. Provide HTML: use `<br>`/`<p>` for "
                "line breaks, `<strong>` for bold, and `<a href>` for links. "
                "Literal `<`, `>`, and `&` must be HTML-escaped; Zendesk "
                "sanitizes to a limited HTML subset, so keep markup basic."
            )
        ),
    ],
) -> ZendeskInternalNoteResponse:
    """Post an internal (private) HTML note to a Zendesk ticket by its numeric ID.

    The comment is added with `public=False`, so it is an internal agent note
    and is **not** visible to the ticket requester/end user. Use it to record
    triage findings, cross-references, or context for other agents. This server
    has no tool that can post a customer-visible/public reply, so it is
    impossible to answer the customer through the MCP server. When asked to
    "reply to the customer", write the proposed reply as an internal note
    clearly labelled as a draft for a human support agent to send, and tell the
    requesting human that a support agent still has to post it publicly. The
    note is sent as HTML (`html_body`), so bold text and links render as intended.

    This tool only posts the note; it does not modify tags. To route/tag a
    ticket, call `add_zendesk_ticket_tags` separately.

    The numeric `ticket_id` must already be known; this tool does not search
    for tickets. Credentials are read from the server environment
    (`ZENDESK_SUBDOMAIN`, `ZENDESK_EMAIL`, `ZENDESK_API_TOKEN`); this tool
    never accepts or logs them.
    """
    try:
        result: dict[str, Any] = add_internal_note(ticket_id, html_body)
    except ZendeskAPIError as exc:
        return ZendeskInternalNoteResponse(
            success=False,
            message=str(exc),
            ticket_id=ticket_id,
        )

    updated_ticket = _as_dict(result.get("ticket"))
    resolved_id = updated_ticket.get("id", ticket_id)
    comment_id = _created_comment_id(_as_dict(result.get("audit")))
    return ZendeskInternalNoteResponse(
        success=True,
        message=(
            f"Posted an internal-only note to Zendesk ticket {resolved_id}; "
            "it is not visible to the customer."
        ),
        ticket_id=resolved_id,
        comment_id=comment_id,
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

    Tags are Zendesk's label mechanism. This reads the ticket's current tags
    and writes back the union (existing + supplied) via a ticket update, so
    the ticket's existing tags — and any tagger-backed custom fields — are
    preserved and never dropped. Adding a tag that is already present is a
    no-op.

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
