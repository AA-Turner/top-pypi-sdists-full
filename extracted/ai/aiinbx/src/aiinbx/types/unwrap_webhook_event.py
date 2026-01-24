# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .outbound_email_opened_webhook_event import OutboundEmailOpenedWebhookEvent
from .inbound_email_received_webhook_event import InboundEmailReceivedWebhookEvent
from .outbound_email_bounced_webhook_event import OutboundEmailBouncedWebhookEvent
from .outbound_email_clicked_webhook_event import OutboundEmailClickedWebhookEvent
from .outbound_email_rejected_webhook_event import OutboundEmailRejectedWebhookEvent
from .outbound_email_delivered_webhook_event import OutboundEmailDeliveredWebhookEvent
from .outbound_email_complained_webhook_event import OutboundEmailComplainedWebhookEvent

__all__ = ["UnwrapWebhookEvent"]

UnwrapWebhookEvent: TypeAlias = Annotated[
    Union[
        InboundEmailReceivedWebhookEvent,
        OutboundEmailDeliveredWebhookEvent,
        OutboundEmailBouncedWebhookEvent,
        OutboundEmailComplainedWebhookEvent,
        OutboundEmailRejectedWebhookEvent,
        OutboundEmailOpenedWebhookEvent,
        OutboundEmailClickedWebhookEvent,
    ],
    PropertyInfo(discriminator="event"),
]
