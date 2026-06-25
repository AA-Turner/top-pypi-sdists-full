"""Helpers for emitting context-generation completion notifications.

Recipient resolution uses the shared NotificationRecipientBuilder which reads
per-user CorpUserSettings.notificationSettings to decide whether to deliver via
Slack/Email. Notifications are sent directly to the integrations service
/private/notifications/send endpoint, bypassing GMS and avoiding the system-auth
requirement that a GraphQL mutation would impose.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Literal

import requests

from acryl_datahub_cloud.metadata.schema_classes import (
    NotificationMessageClass,
    NotificationRequestClass,
    NotificationTemplateTypeClass,
)
from acryl_datahub_cloud.notifications.notification_recipient_builder import (
    NotificationRecipientBuilder,
)
from datahub.ingestion.graph.client import DataHubGraph

logger = logging.getLogger(__name__)

SCENARIO_TRIGGERED_RUN = "CONTEXT_GENERATION_TRIGGERED_RUN_COMPLETED"
SCENARIO_PROPOSAL_DIGEST = "CONTEXT_GENERATION_PROPOSAL_DIGEST"

NotificationType = Literal[
    "TRIGGERED_RUN_COMPLETED", "TRIGGERED_RUN_FAILED", "PROPOSAL_DIGEST"
]

_INTEGRATIONS_HOST = os.environ.get(
    "DATAHUB_INTEGRATIONS_HOST", "datahub-integrations-service"
)
_INTEGRATIONS_PORT = os.environ.get("DATAHUB_INTEGRATIONS_PORT", "9003")
_SEND_NOTIFICATION_URL = (
    f"http://{_INTEGRATIONS_HOST}:{_INTEGRATIONS_PORT}/private/notifications/send"
)

# Maps the short NotificationType name to the full NotificationTemplateType value.
# The notification_type parameter uses short names (TRIGGERED_RUN_COMPLETED) while the
# PDL enum uses a BROADCAST_CONTEXT_GENERATION_ prefix. Keep this explicit so new
# values fail loudly here rather than silently at runtime.
_TEMPLATE_TYPE_MAP: Dict[str, str] = {
    "TRIGGERED_RUN_COMPLETED": NotificationTemplateTypeClass.BROADCAST_CONTEXT_GENERATION_TRIGGERED_RUN_COMPLETED,
    "TRIGGERED_RUN_FAILED": NotificationTemplateTypeClass.BROADCAST_CONTEXT_GENERATION_TRIGGERED_RUN_FAILED,
    "PROPOSAL_DIGEST": NotificationTemplateTypeClass.BROADCAST_CONTEXT_GENERATION_PROPOSAL_DIGEST,
}


def send_context_generation_notification(
    graph: DataHubGraph,
    recipient_builder: NotificationRecipientBuilder,
    actor_urns: List[str],
    scenario: str,
    notification_type: NotificationType,
    parameters: Dict[str, str],
    is_default_enabled: bool = True,
) -> bool:
    """Resolve recipients and POST directly to the integrations service.

    Args:
        graph: DataHubGraph client used for recipient settings lookups.
        recipient_builder: filters actor_urns to opted-in recipients.
        actor_urns: candidate user URNs to notify.
        scenario: scenario type string (e.g. CONTEXT_GENERATION_TRIGGERED_RUN_COMPLETED).
        notification_type: template variant to render.
        parameters: key/value parameters for the template renderer.
        is_default_enabled: if True, users with no explicit preference are notified.

    Returns:
        True if the notification was sent. False if no recipients or on error.
    """
    if not actor_urns:
        return False

    recipients = recipient_builder.build_actor_recipients(
        actor_urns,
        scenario,
        is_default_enabled,
    )
    if not recipients:
        logger.info(
            "No recipients opted in to %s; skipping notification emit.", scenario
        )
        return False

    template_type = _TEMPLATE_TYPE_MAP.get(notification_type)
    if not template_type:
        logger.error(
            "Unknown notification_type %r — add it to _TEMPLATE_TYPE_MAP.",
            notification_type,
        )
        return False

    notification_request = NotificationRequestClass(
        message=NotificationMessageClass(
            template=template_type,
            parameters={k: str(v) for k, v in parameters.items()},
        ),
        recipients=list(recipients),
    )

    try:
        response = requests.post(
            _SEND_NOTIFICATION_URL,
            json=notification_request.to_obj(),
            timeout=30,
        )
        response.raise_for_status()
        return True
    except Exception:
        logger.exception(
            "Failed to send context-generation notification to integrations service "
            "(scenario=%s, type=%s, url=%s)",
            scenario,
            notification_type,
            _SEND_NOTIFICATION_URL,
        )
        return False
