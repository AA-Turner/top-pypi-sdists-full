"""Gateway messaging adapters."""


from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import tempfile
from typing import Any
from uuid import uuid4

from apps.provider_runtime import (
    EnvironmentSecretStore,
    SurfaceModelProviderCapability,
    load_provider_profile,
    provider_fallback_summary,
    provider_profile_from_payload,
    provider_profile_summary,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore, ProfileCredentialResolver
from packages.capabilities.runtime import (
    CapabilityDescriptor,
    ContextCapability,
    MemoryCapability,
    ModelProviderCapability,
    PlanningCapability,
    TelemetrySinkCapability,
)
from packages.context import ContextRuntime
from packages.contracts.runtime import (
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    GoalNode,
    MemoryRecord,
    ProfileState,
    SessionState,
    ActivityGraph,
)
from packages.gateway_core import (
    DEFAULT_GATEWAY_ACCOUNT_ID,
    FileGatewayIdentityStore,
    FileGatewaySessionStore,
    GatewayAccountRef,
    GatewayAttachmentRef,
    GatewayConversationRef,
    GatewayCoreDependencies,
    GatewayCoreService,
    GatewayExchange,
    GatewayIdentityRecord,
    GatewayInboundMessage,
    GatewayOutboundMessage,
    GatewayPolicyHint,
    GatewaySenderRef,
    InMemoryGatewayIdentityStore,
    InMemoryGatewaySessionStore,
)
from packages.kernel import KernelDependencies, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.evidence import MemoryRuntime
from packages.planning import PlanningDecision, PlanningMode, PlanningService
from packages.state import DEFAULT_CLONE_TEXT, LoadedProfile, ProfileLoader, build_prompt_contract
from packages.security.runtime import SecurityPolicy
from packages.storage import RuntimeStorageRepository
from packages.voice import VoiceInputRequest, VoiceInputResolution, VoiceTurnResult, build_provider_voice_service

from .plugins import GatewayAdapterDescriptor, GatewayPluginRegistry

CHAT_BOT_ADAPTER_ID = "messaging.chat-bot"
WEBHOOK_ADAPTER_ID = "messaging.webhook"
TELEGRAM_ADAPTER_ID = "messaging.telegram"
FEISHU_ADAPTER_ID = "messaging.feishu"
DISCORD_ADAPTER_ID = "messaging.discord"

from .runtime_support import *  # noqa: F401,F403

@dataclass(frozen=True, slots=True)
class ChatBotMessagingAdapter:
    app: GatewayApp
    adapter_id: str = CHAT_BOT_ADAPTER_ID

    def receive_text(
        self,
        *,
        conversation_id: str,
        external_user_id: str,
        body: str,
        account_id: str = DEFAULT_GATEWAY_ACCOUNT_ID,
        display_name: str | None = None,
        event_id: str | None = None,
        attachments: tuple[str, ...] = (),
        metadata: Mapping[str, object] | None = None,
        reply_body: str | None = None,
        target_trusted: bool = True,
        consent_given: bool = True,
        is_external: bool = False,
    ) -> GatewayExchange:
        attachment_refs = _attachment_refs(attachments)
        inbound_metadata = _object_map(metadata)
        inbound = GatewayInboundMessage(
            event_id=event_id or f"{self.adapter_id}:{conversation_id}:{external_user_id}",
            account=_account_ref(
                self.adapter_id,
                account_id=account_id,
                surface="local-chat",
            ),
            conversation=_conversation_ref(
                conversation_id,
                chat_type="direct",
            ),
            sender=_sender_ref(
                external_user_id,
                display_name=display_name,
            ),
            body=body,
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=target_trusted,
                consent_default=consent_given,
                is_external_default=is_external,
                audience_scope="direct",
            ),
            metadata=inbound_metadata,
        )
        return self.app.handle_message(
            inbound,
            reply_body=reply_body,
            attachment_refs=attachment_refs,
            metadata={
                "channel": "chat-bot",
                **inbound_metadata,
            },
        )

    def receive_voice(
        self,
        *,
        conversation_id: str,
        external_user_id: str,
        audio_bytes: bytes,
        audio_name: str,
        account_id: str = DEFAULT_GATEWAY_ACCOUNT_ID,
        audio_format: str | None = None,
        display_name: str | None = None,
        event_id: str | None = None,
        attachments: tuple[str, ...] = (),
        metadata: Mapping[str, object] | None = None,
        reply_body: str | None = None,
        target_trusted: bool = True,
        consent_given: bool = True,
        is_external: bool = False,
        voice_output_enabled: bool = False,
        output_audio_format: str = "mp3",
    ) -> GatewayVoiceExchange:
        attachment_refs = _attachment_refs(attachments)
        inbound_metadata = _object_map(metadata)
        inbound = GatewayInboundMessage(
            event_id=event_id or f"{self.adapter_id}:{conversation_id}:{external_user_id}:voice",
            account=_account_ref(
                self.adapter_id,
                account_id=account_id,
                surface="local-chat",
            ),
            conversation=_conversation_ref(
                conversation_id,
                chat_type="direct",
            ),
            sender=_sender_ref(
                external_user_id,
                display_name=display_name,
            ),
            body="voice-input",
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=target_trusted,
                consent_default=consent_given,
                is_external_default=is_external,
                audience_scope="direct",
            ),
            metadata=inbound_metadata,
        )
        return self.app.handle_voice_message(
            inbound,
            audio_bytes=audio_bytes,
            audio_name=audio_name,
            audio_format=audio_format,
            reply_body=reply_body,
            attachment_refs=attachment_refs,
            metadata={
                "channel": "chat-bot",
                **inbound_metadata,
            },
            voice_output_enabled=voice_output_enabled,
            output_audio_format=output_audio_format,
        )

@dataclass(frozen=True, slots=True)
class WebhookMessagingAdapter:
    app: GatewayApp
    adapter_id: str = WEBHOOK_ADAPTER_ID

    def receive_event(
        self,
        payload: Mapping[str, object],
        *,
        reply_body: str | None = None,
        target_trusted: bool = True,
        consent_given: bool = True,
        is_external: bool = False,
    ) -> GatewayExchange:
        attachments = tuple(str(item) for item in payload.get("attachments", ()))
        attachment_refs = _attachment_refs(attachments)
        inbound_metadata = {
            "channel": "webhook",
            **_object_map(payload.get("metadata")),
        }
        inbound = GatewayInboundMessage(
            event_id=str(payload.get("event_id") or payload.get("message_id") or payload["conversation_id"]),
            account=_account_ref(
                self.adapter_id,
                account_id=str(payload.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID),
                tenant_id=(
                    str(payload["tenant_id"])
                    if payload.get("tenant_id") is not None
                    else None
                ),
                surface="generic-webhook",
            ),
            conversation=_conversation_ref(
                str(payload["conversation_id"]),
                chat_type=str(payload.get("chat_type") or "external"),
            ),
            sender=_sender_ref(
                str(payload["external_user_id"]),
                display_name=(
                    str(payload["display_name"])
                    if payload.get("display_name") is not None
                    else None
                ),
            ),
            body=str(payload["body"]),
            reply_to_message_id=(
                str(payload["reply_to_message_id"])
                if payload.get("reply_to_message_id") is not None
                else (
                    str(payload["reply_to_event_id"])
                    if payload.get("reply_to_event_id") is not None
                    else None
                )
            ),
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=target_trusted,
                consent_default=consent_given,
                is_external_default=is_external,
                audience_scope=str(payload.get("chat_type") or "external"),
            ),
            metadata=inbound_metadata,
        )
        response_metadata = {
            "channel": "webhook",
            **_object_map(payload.get("metadata")),
        }
        callback_url = payload.get("callback_url")
        if callback_url is not None:
            response_metadata["callback_url"] = str(callback_url)
        return self.app.handle_message(
            inbound,
            reply_body=reply_body,
            reply_to_message_id=inbound.reply_to_message_id or inbound.event_id,
            attachment_refs=inbound.attachment_refs,
            metadata=response_metadata,
        )

    def receive_voice_event(
        self,
        payload: Mapping[str, object],
        *,
        reply_body: str | None = None,
        target_trusted: bool = True,
        consent_given: bool = True,
        is_external: bool = False,
        voice_output_enabled: bool = False,
        output_audio_format: str = "mp3",
    ) -> GatewayVoiceExchange:
        attachments = tuple(str(item) for item in payload.get("attachments", ()))
        attachment_refs = _attachment_refs(attachments)
        inbound_metadata = {
            "channel": "webhook",
            **_object_map(payload.get("metadata")),
        }
        inbound = GatewayInboundMessage(
            event_id=str(payload.get("event_id") or payload.get("message_id") or payload["conversation_id"]),
            account=_account_ref(
                self.adapter_id,
                account_id=str(payload.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID),
                tenant_id=(
                    str(payload["tenant_id"])
                    if payload.get("tenant_id") is not None
                    else None
                ),
                surface="generic-webhook",
            ),
            conversation=_conversation_ref(
                str(payload["conversation_id"]),
                chat_type=str(payload.get("chat_type") or "external"),
            ),
            sender=_sender_ref(
                str(payload["external_user_id"]),
                display_name=(
                    str(payload["display_name"])
                    if payload.get("display_name") is not None
                    else None
                ),
            ),
            body="voice-input",
            reply_to_message_id=(
                str(payload["reply_to_message_id"])
                if payload.get("reply_to_message_id") is not None
                else (
                    str(payload["reply_to_event_id"])
                    if payload.get("reply_to_event_id") is not None
                    else None
                )
            ),
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=target_trusted,
                consent_default=consent_given,
                is_external_default=is_external,
                audience_scope=str(payload.get("chat_type") or "external"),
            ),
            metadata=inbound_metadata,
        )
        response_metadata = {
            "channel": "webhook",
            **_object_map(payload.get("metadata")),
        }
        callback_url = payload.get("callback_url")
        if callback_url is not None:
            response_metadata["callback_url"] = str(callback_url)
        return self.app.handle_voice_message(
            inbound,
            audio_bytes=bytes(payload["audio_bytes"]),
            audio_name=str(payload.get("audio_name") or "voice-input.wav"),
            audio_format=str(payload.get("audio_format")) if payload.get("audio_format") is not None else None,
            reply_body=reply_body,
            reply_to_message_id=inbound.reply_to_message_id or inbound.event_id,
            attachment_refs=inbound.attachment_refs,
            metadata=response_metadata,
            voice_output_enabled=voice_output_enabled,
            output_audio_format=output_audio_format,
        )

@dataclass(frozen=True, slots=True)
class TelegramMessagingAdapter:
    app: GatewayApp
    adapter_id: str = TELEGRAM_ADAPTER_ID

    def receive_update(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str = DEFAULT_GATEWAY_ACCOUNT_ID,
        reply_body: str | None = None,
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayExchange:
        update_kind = "message"
        message = payload.get("message")
        callback_data: str | None = None
        if not isinstance(message, Mapping):
            message = payload.get("edited_message")
            if isinstance(message, Mapping):
                update_kind = "edited_message"
        if not isinstance(message, Mapping):
            callback_query = payload.get("callback_query")
            if isinstance(callback_query, Mapping):
                nested_message = callback_query.get("message")
                if isinstance(nested_message, Mapping):
                    message = nested_message
                    update_kind = "callback_query"
                    if callback_query.get("data") is not None:
                        callback_data = str(callback_query["data"])
                    if not isinstance(message.get("from"), Mapping) and isinstance(
                        callback_query.get("from"), Mapping
                    ):
                        message = {
                            **message,
                            "from": callback_query["from"],
                        }
        if not isinstance(message, Mapping):
            raise ValueError("telegram update requires message, edited_message, or callback_query.message")
        chat = message.get("chat")
        sender = message.get("from")
        if not isinstance(chat, Mapping) or not isinstance(sender, Mapping):
            raise ValueError("telegram update requires chat and from payloads")
        chat_id = str(chat["id"])
        chat_type = str(chat.get("type") or "private")
        thread_id = message.get("message_thread_id")
        normalized_chat_type = _normalized_chat_type(chat_type)
        attachment_refs = _attachment_refs(_telegram_attachment_ids(message))
        message_id = (
            str(message["message_id"])
            if message.get("message_id") is not None
            else None
        )
        metadata = {
            "channel": "telegram",
            "chat_type": chat_type,
            "update_kind": update_kind,
            "chat_id": chat_id,
        }
        if message_id is not None:
            metadata["message_id"] = message_id
        if sender.get("username") is not None:
            metadata["username"] = str(sender["username"])
        if thread_id is not None:
            metadata["message_thread_id"] = str(thread_id)
        if message.get("reply_to_message") is not None:
            metadata["reply_to_message_id"] = str(
                dict(message["reply_to_message"]).get("message_id") or ""
            )
        if callback_data is not None:
            metadata["callback_data"] = callback_data
        target_trusted_default, consent_default, external_default = _telegram_delivery_defaults(chat_type)
        resolved_thread_id = str(thread_id) if thread_id is not None else None
        inbound = GatewayInboundMessage(
            event_id=str(payload.get("update_id") or message.get("message_id") or chat["id"]),
            account=_account_ref(
                self.adapter_id,
                account_id=account_id,
                surface="telegram-bot-api",
            ),
            conversation=_conversation_ref(
                _telegram_conversation_id(chat_id, thread_id),
                parent_conversation_id=chat_id if resolved_thread_id is not None else None,
                thread_id=resolved_thread_id,
                chat_type=normalized_chat_type,
                metadata={"raw_chat_type": chat_type},
            ),
            sender=_sender_ref(
                str(sender["id"]),
                display_name=_telegram_display_name(sender),
                username=(
                    f"@{str(sender['username'])}"
                    if sender.get("username") is not None
                    else None
                ),
                is_bot=bool(sender.get("is_bot", False)),
            ),
            body=str(message.get("text") or message.get("caption") or callback_data or "telegram-event"),
            reply_to_message_id=(
                str(metadata.get("reply_to_message_id") or message_id or "") or None
            ),
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=(
                    target_trusted_default if target_trusted is None else target_trusted
                ),
                consent_default=consent_default if consent_given is None else consent_given,
                is_external_default=external_default if is_external is None else is_external,
                audience_scope=normalized_chat_type,
                metadata={"raw_chat_type": chat_type},
            ),
            metadata=metadata,
        )
        return self.app.handle_message(
            inbound,
            reply_body=reply_body,
            reply_to_message_id=inbound.reply_to_message_id or inbound.event_id,
            attachment_refs=attachment_refs,
            metadata={
                **metadata,
                "delivery_surface": "telegram-bot-api",
            },
        )

@dataclass(frozen=True, slots=True)
class DiscordMessagingAdapter:
    app: GatewayApp
    adapter_id: str = DISCORD_ADAPTER_ID

    def normalize_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str = DEFAULT_GATEWAY_ACCOUNT_ID,
        transport: str = "gateway",
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayInboundMessage:
        message_id = str(payload.get("id") or "").strip()
        if not message_id:
            raise ValueError("discord event requires id")
        channel_id = str(payload.get("channel_id") or "").strip()
        if not channel_id:
            raise ValueError("discord event requires channel_id")
        author = payload.get("author")
        if not isinstance(author, Mapping):
            raise ValueError("discord event requires author payload")
        member = payload.get("member")
        if member is not None and not isinstance(member, Mapping):
            raise ValueError("discord event member payload must be an object when present")
        chat_type = _discord_chat_type(payload)
        thread_id = str(payload.get("thread_id") or "").strip() or None
        parent_conversation_id = str(payload.get("parent_id") or "").strip() or None
        if chat_type == "topic":
            thread_id = thread_id or channel_id
        else:
            thread_id = None
            parent_conversation_id = None
        conversation_id = thread_id or channel_id
        attachment_refs = _discord_attachment_refs(payload.get("attachments"))
        reply_reference = payload.get("message_reference")
        reply_to_message_id = None
        if isinstance(reply_reference, Mapping) and reply_reference.get("message_id") is not None:
            reply_to_message_id = str(reply_reference["message_id"])
        elif payload.get("reply_to_message_id") is not None:
            reply_to_message_id = str(payload["reply_to_message_id"])
        target_trusted_default, consent_default, external_default = _discord_delivery_defaults(chat_type)
        metadata = {
            "channel": "discord",
            "guild_id": str(payload.get("guild_id") or ""),
            "channel_id": channel_id,
            "chat_type": chat_type,
            "transport": transport,
        }
        if parent_conversation_id is not None:
            metadata["parent_id"] = parent_conversation_id
        if thread_id is not None:
            metadata["thread_id"] = thread_id
        return GatewayInboundMessage(
            event_id=message_id,
            account=_account_ref(
                self.adapter_id,
                account_id=account_id,
                surface=f"discord-{transport}",
                metadata={"event_transport": transport},
            ),
            conversation=_conversation_ref(
                conversation_id,
                parent_conversation_id=parent_conversation_id,
                thread_id=thread_id,
                chat_type=chat_type,
                metadata={
                    "channel_id": channel_id,
                },
            ),
            sender=_sender_ref(
                str(author.get("id") or ""),
                display_name=_discord_display_name(author, member=member),
                username=(
                    f"@{str(author['username'])}"
                    if author.get("username") is not None
                    else None
                ),
                is_bot=bool(author.get("bot", False)),
                metadata={"global_name": str(author.get("global_name") or "")},
            ),
            body=_discord_body(payload),
            reply_to_message_id=reply_to_message_id,
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=(
                    target_trusted_default if target_trusted is None else target_trusted
                ),
                consent_default=consent_default if consent_given is None else consent_given,
                is_external_default=external_default if is_external is None else is_external,
                audience_scope=chat_type,
                metadata={"chat_type": chat_type},
            ),
            metadata=metadata,
        )

    def receive_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str = DEFAULT_GATEWAY_ACCOUNT_ID,
        transport: str = "gateway",
        reply_body: str | None = None,
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayExchange:
        inbound = self.normalize_event(
            payload,
            account_id=account_id,
            transport=transport,
            target_trusted=target_trusted,
            consent_given=consent_given,
            is_external=is_external,
        )
        return self.app.handle_message(
            inbound,
            reply_body=reply_body,
            reply_to_message_id=inbound.reply_to_message_id or inbound.event_id,
            attachment_refs=inbound.attachment_refs,
            metadata={
                **dict(inbound.metadata),
                "delivery_surface": inbound.account.surface or f"discord-{transport}",
            },
        )

    def build_reply_request(self, outbound: GatewayOutboundMessage) -> Mapping[str, object]:
        if outbound.adapter_id != self.adapter_id:
            raise ValueError("discord reply request requires a discord outbound message")
        return _discord_reply_request(outbound)

@dataclass(frozen=True, slots=True)
class FeishuMessagingAdapter:
    app: GatewayApp
    adapter_id: str = FEISHU_ADAPTER_ID

    def normalize_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str | None = None,
        transport: str = "long-connection",
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayInboundMessage:
        header = payload.get("header")
        if not isinstance(header, Mapping):
            raise ValueError("feishu event requires a header payload")
        event = payload.get("event")
        if not isinstance(event, Mapping):
            raise ValueError("feishu event requires an event payload")
        sender = event.get("sender")
        message = event.get("message")
        if not isinstance(sender, Mapping) or not isinstance(message, Mapping):
            raise ValueError("feishu event requires sender and message payloads")

        event_type = str(header.get("event_type") or "")
        if event_type and event_type != "im.message.receive_v1":
            raise ValueError(f"unsupported feishu event type: {event_type}")

        tenant_key = (
            str(header["tenant_key"])
            if header.get("tenant_key") is not None
            else (
                str(event["tenant_key"])
                if event.get("tenant_key") is not None
                else None
            )
        )
        resolved_account_id = account_id or (
            str(header["app_id"])
            if header.get("app_id") is not None
            else DEFAULT_GATEWAY_ACCOUNT_ID
        )

        chat_id = str(message.get("chat_id") or "")
        if not chat_id:
            raise ValueError("feishu message payload requires chat_id")
        chat_type = str(message.get("chat_type") or "group")
        normalized_chat_type = _normalized_chat_type(chat_type)
        message_id = str(message.get("message_id") or header.get("event_id") or "")
        if not message_id:
            raise ValueError("feishu message payload requires message_id")
        root_id = (
            str(message["root_id"])
            if message.get("root_id") is not None and str(message["root_id"]).strip()
            else None
        )
        parent_id = (
            str(message["parent_id"])
            if message.get("parent_id") is not None and str(message["parent_id"]).strip()
            else None
        )
        message_type = str(message.get("message_type") or "text")
        content = _feishu_message_content(message.get("content"))
        attachment_refs = _feishu_attachment_refs(content)
        conversation_id = f"{chat_id}:{root_id}" if root_id is not None else chat_id
        transport_label = str(transport or "event-subscription").strip() or "event-subscription"

        inbound_metadata = {
            "channel": "feishu",
            "event_type": event_type or "im.message.receive_v1",
            "chat_id": chat_id,
            "chat_type": chat_type,
            "message_type": message_type,
            "message_id": message_id,
            "tenant_key": tenant_key or "",
        }
        if root_id is not None:
            inbound_metadata["root_id"] = root_id
        if parent_id is not None:
            inbound_metadata["parent_id"] = parent_id
        mentions = event.get("mentions")
        if isinstance(mentions, list):
            inbound_metadata["mention_count"] = len(mentions)

        target_trusted_default = chat_type == "p2p"
        consent_default = chat_type == "p2p"
        external_default = chat_type != "p2p"
        inbound = GatewayInboundMessage(
            event_id=message_id,
            account=_account_ref(
                self.adapter_id,
                account_id=resolved_account_id,
                tenant_id=tenant_key,
                surface=f"feishu-{transport_label}",
                metadata={"event_transport": transport_label},
            ),
            conversation=_conversation_ref(
                conversation_id,
                parent_conversation_id=chat_id if root_id is not None else None,
                thread_id=root_id,
                chat_type=normalized_chat_type,
                metadata={
                    "raw_chat_type": chat_type,
                    "message_id": message_id,
                },
            ),
            sender=_sender_ref(
                _feishu_sender_user_id(sender),
                display_name=_feishu_display_name(sender),
                is_bot=str(sender.get("sender_type") or "user") != "user",
                metadata={
                    "sender_type": str(sender.get("sender_type") or "user"),
                    "tenant_key": (
                        str(sender["tenant_key"])
                        if sender.get("tenant_key") is not None
                        else ""
                    ),
                },
            ),
            body=_feishu_message_body(message_type, content),
            reply_to_message_id=parent_id or root_id or message_id,
            attachment_refs=attachment_refs,
            policy_hint=_policy_hint(
                target_trusted_default=(
                    target_trusted_default if target_trusted is None else target_trusted
                ),
                consent_default=consent_default if consent_given is None else consent_given,
                is_external_default=external_default if is_external is None else is_external,
                audience_scope=normalized_chat_type,
                metadata={
                    "raw_chat_type": chat_type,
                    "tenant_key": tenant_key or "",
                },
            ),
            metadata=inbound_metadata,
        )
        return inbound

    def receive_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str | None = None,
        transport: str = "long-connection",
        reply_body: str | None = None,
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayExchange:
        inbound = self.normalize_event(
            payload,
            account_id=account_id,
            transport=transport,
            target_trusted=target_trusted,
            consent_given=consent_given,
            is_external=is_external,
        )
        return self.app.handle_message(
            inbound,
            reply_body=reply_body,
            reply_to_message_id=inbound.event_id,
            attachment_refs=inbound.attachment_refs,
            metadata={
                **dict(inbound.metadata),
                "delivery_surface": inbound.account.surface or f"feishu-{transport}",
            },
        )

    def build_reply_request(self, outbound: GatewayOutboundMessage) -> Mapping[str, object]:
        if outbound.adapter_id != self.adapter_id:
            raise ValueError("feishu reply request requires a feishu outbound message")
        return _feishu_reply_request(outbound)
