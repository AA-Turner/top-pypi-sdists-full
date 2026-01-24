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

    created_after: Annotated[str, PropertyInfo(alias="createdAfter")]

    created_before: Annotated[str, PropertyInfo(alias="createdBefore")]

    has_email_from_address: Annotated[str, PropertyInfo(alias="hasEmailFromAddress")]

    has_email_to_address: Annotated[str, PropertyInfo(alias="hasEmailToAddress")]

    has_participant_emails: Annotated[SequenceNotStr[str], PropertyInfo(alias="hasParticipantEmails")]

    last_email_after: Annotated[str, PropertyInfo(alias="lastEmailAfter")]

    last_email_before: Annotated[str, PropertyInfo(alias="lastEmailBefore")]

    limit: float

    offset: float

    some_email_has_direction: Annotated[Literal["INBOUND", "OUTBOUND"], PropertyInfo(alias="someEmailHasDirection")]

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

    sort_by: Annotated[Literal["createdAt", "lastEmailAt", "subject"], PropertyInfo(alias="sortBy")]

    sort_order: Annotated[Literal["asc", "desc"], PropertyInfo(alias="sortOrder")]

    stale_threshold_days: Annotated[float, PropertyInfo(alias="staleThresholdDays")]

    subject_contains: Annotated[str, PropertyInfo(alias="subjectContains")]
