"""Relationship Intelligence API operations for DealCloud SDK."""

from .dealcloud_ri import (
    RI_MAILBOX_STATUS_ERROR,
    DealCloudRelationshipIntelligence,
    ri_mailbox_response_failed,
    ri_mailbox_responses_all_succeeded,
)

__all__ = [
    "DealCloudRelationshipIntelligence",
    "RI_MAILBOX_STATUS_ERROR",
    "ri_mailbox_response_failed",
    "ri_mailbox_responses_all_succeeded",
]
