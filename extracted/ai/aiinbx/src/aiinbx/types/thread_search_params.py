# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["ThreadSearchParams"]


class ThreadSearchParams(TypedDict, total=False):
    conversation_state: Annotated[
        Literal["awaiting_reply", "needs_reply", "active", "stale"], PropertyInfo(alias="conversationState")
    ]
    """Filter threads by conversation state"""

    created_after: Annotated[str, PropertyInfo(alias="createdAfter")]
    """Filter threads created after this date"""

    created_before: Annotated[str, PropertyInfo(alias="createdBefore")]
    """Filter threads created before this date"""

    has_email_from_address: Annotated[str, PropertyInfo(alias="hasEmailFromAddress")]
    """Filter threads with emails from this address"""

    has_email_to_address: Annotated[str, PropertyInfo(alias="hasEmailToAddress")]
    """Filter threads with emails to this address"""

    has_participant_emails: Annotated[SequenceNotStr[str], PropertyInfo(alias="hasParticipantEmails")]
    """Filter threads that include all of these email addresses as participants"""

    last_email_after: Annotated[str, PropertyInfo(alias="lastEmailAfter")]
    """Filter threads with last email after this date"""

    last_email_before: Annotated[str, PropertyInfo(alias="lastEmailBefore")]
    """Filter threads with last email before this date"""

    limit: float
    """Number of threads to return (1-100)"""

    offset: float
    """Number of threads to skip"""

    some_email_has_direction: Annotated[Literal["INBOUND", "OUTBOUND"], PropertyInfo(alias="someEmailHasDirection")]
    """Filter threads containing emails with this direction"""

    some_email_has_status: Annotated[
        Literal[
            "DRAFT",
            "QUEUED",
            "ACCEPTED",
            "SENT",
            "RECEIVED",
            "FAILED",
            "BOUNCED",
            "COMPLAINED",
            "REJECTED",
            "READ",
            "ARCHIVED",
        ],
        PropertyInfo(alias="someEmailHasStatus"),
    ]
    """Filter threads containing emails with this status"""

    sort_by: Annotated[Literal["createdAt", "lastEmailAt", "subject"], PropertyInfo(alias="sortBy")]
    """Field to sort by"""

    sort_order: Annotated[Literal["asc", "desc"], PropertyInfo(alias="sortOrder")]
    """Sort order"""

    stale_threshold_days: Annotated[float, PropertyInfo(alias="staleThresholdDays")]
    """Days to consider a thread stale (used with conversationState=stale)"""

    subject_contains: Annotated[str, PropertyInfo(alias="subjectContains")]
    """Filter threads where subject contains this text"""
