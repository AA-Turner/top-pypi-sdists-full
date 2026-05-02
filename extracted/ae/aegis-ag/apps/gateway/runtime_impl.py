"""Gateway runtime façade over support, capability, app, adapter, and factory modules."""

from __future__ import annotations

from .runtime_support import (
    CHAT_BOT_ADAPTER_ID,
    DEFAULT_GATEWAY_ACCOUNT_ID,
    DISCORD_ADAPTER_ID,
    FEISHU_ADAPTER_ID,
    TELEGRAM_ADAPTER_ID,
    WEBHOOK_ADAPTER_ID,
)
from .runtime_app import (
    GatewayApp,
    GatewayVoiceExchange,
)
from .runtime_adapters import (
    ChatBotMessagingAdapter,
    DiscordMessagingAdapter,
    FeishuMessagingAdapter,
    TelegramMessagingAdapter,
    WebhookMessagingAdapter,
)
from .runtime_factory import (
    build_gateway_app,
    register_builtin_gateway_adapters,
)

__all__ = [
    "CHAT_BOT_ADAPTER_ID",
    "DEFAULT_GATEWAY_ACCOUNT_ID",
    "DISCORD_ADAPTER_ID",
    "FEISHU_ADAPTER_ID",
    "TELEGRAM_ADAPTER_ID",
    "WEBHOOK_ADAPTER_ID",
    "ChatBotMessagingAdapter",
    "DiscordMessagingAdapter",
    "FeishuMessagingAdapter",
    "GatewayApp",
    "GatewayVoiceExchange",
    "TelegramMessagingAdapter",
    "WebhookMessagingAdapter",
    "build_gateway_app",
    "register_builtin_gateway_adapters",
]
