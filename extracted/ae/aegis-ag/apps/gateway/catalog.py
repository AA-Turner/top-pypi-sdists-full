"""Gateway adapter catalog and operator-facing setup metadata."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

CHAT_BOT_ADAPTER_ID = "messaging.chat-bot"
WEBHOOK_ADAPTER_ID = "messaging.webhook"
TELEGRAM_ADAPTER_ID = "messaging.telegram"


@dataclass(frozen=True, slots=True)
class GatewayAdapterSpec:
    key: str
    adapter_id: str
    surface: str
    operator_action: str
    identity_mapping: str | None = None
    supported_updates: tuple[str, ...] = ()
    delivery_defaults: Mapping[str, str] = ()

    def setup_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "adapter_id": self.adapter_id,
            "surface": self.surface,
            "operator_action": self.operator_action,
        }
        if self.identity_mapping is not None:
            payload["identity_mapping"] = self.identity_mapping
        if self.supported_updates:
            payload["supported_updates"] = self.supported_updates
        if self.delivery_defaults:
            payload["delivery_defaults"] = dict(self.delivery_defaults)
        return payload


GATEWAY_ADAPTER_SPECS = (
    GatewayAdapterSpec(
        key="chat_bot",
        adapter_id=CHAT_BOT_ADAPTER_ID,
        surface="local-chat",
        operator_action="none",
    ),
    GatewayAdapterSpec(
        key="webhook",
        adapter_id=WEBHOOK_ADAPTER_ID,
        surface="generic-webhook",
        operator_action="supply callback_url in inbound payload",
    ),
    GatewayAdapterSpec(
        key="telegram",
        adapter_id=TELEGRAM_ADAPTER_ID,
        surface="telegram-bot-api",
        operator_action="configure TELEGRAM_BOT_TOKEN and forward Bot API updates into the gateway",
        identity_mapping="chat.id + from.id (+ message_thread_id when present)",
        supported_updates=("message", "edited_message", "callback_query"),
        delivery_defaults={
            "private": "allow",
            "group": "review",
            "supergroup": "review",
            "channel": "review",
        },
    ),
)


def gateway_adapter_ids() -> dict[str, str]:
    return {spec.key: spec.adapter_id for spec in GATEWAY_ADAPTER_SPECS}


def gateway_adapter_setup() -> dict[str, dict[str, Any]]:
    return {spec.key: spec.setup_payload() for spec in GATEWAY_ADAPTER_SPECS}
