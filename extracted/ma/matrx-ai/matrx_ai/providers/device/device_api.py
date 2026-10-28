"""``DeviceChat`` — the client a ``device_chat`` route dispatches to.

A model on a person's Matrx 2 computer speaks the OpenAI Chat Completions dialect (llama-server),
so this client is ``GenericOpenAIChat`` with the same translator and streaming parser (the
Moonshot precedent). Only the TRANSPORT differs: ``AsyncOpenAI`` sends through
:class:`~matrx_ai.providers.device.relay_transport.RelayStreamTransport`, which turns the call into
the relay's ``POST /v1/devices/{D}/stream`` (never an internet endpoint, never retried by the SDK).

PER CALL: :meth:`execute` reads the device and its ModelKey from ``profile.served_via`` /
``profile.provider_model_id`` and the person's token from the ambient ``AppContext``, and binds
them to the transport's contextvar for this call only.

ALWAYS STREAMED: a device answers as server-sent events. A call the loop asks for without
streaming is sent streamed and collected (the emitter sees the same chunks either way).

ERRORS: every failure leaves here as ONE typed :class:`DeviceRouteError` (``classify.py``),
``is_retryable=False``. COST: the usage says ``api="device_chat"`` and ``device_served``, so it
costs 0.0 (``TokenUsage.calculate_cost``).
"""

from __future__ import annotations

import logging
import re
import uuid
from typing import Any

import httpx
import openai as openai_sdk
from openai import AsyncOpenAI

from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat

logger = logging.getLogger(__name__)

#: Placeholder base URL — never dialed. The relay transport replaces the wire entirely.
DEVICE_BASE_URL = "https://device.invalid"
#: ``TokenUsage.api`` of a device-served call (the wire route).
DEVICE_USAGE_API = "device_chat"
#: The desktop protocol's ModelKey (``desktop_protocol.ModelKey``).
MODEL_KEY_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*(/[a-z0-9][a-z0-9._-]*)?$")


def device_model_key(metadata: Any, name: str | None) -> str | None:
    """The key Matrx 2 runs a catalog model under: ``metadata.desktop_id`` when it has one, else
    the catalog name (matrx-desktop ``app/shared/models/catalog-view.ts`` ``modelKey``; the host's
    twin is aidream ``services/ai_catalog/local_models/seed.py``)."""
    desktop_id = metadata.get("desktop_id") if isinstance(metadata, dict) else None
    key = str(desktop_id or name or "").strip()
    return key or None


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


#: llama-server (the desktop's b9076, started with ``--jinja`` and a server-wide
#: ``--reasoning-budget``) takes thinking per request only as the chat template's own switch:
#: ``chat_template_kwargs.enable_thinking`` (Qwen3 / Qwen3.5 templates honour it; a template
#: without it ignores the key). There is no per-request depth the desktop uses, so every level
#: means thinking ON within the server's budget — applied, nothing to announce.
_THINKING_OFF = frozenset({"none"})


def device_thinking(reasoning_effort: Any) -> bool | None:
    """``enable_thinking`` for a device request: False for ``none``, True for a level, None
    (the template's own default) when unset or ``auto``."""
    if reasoning_effort is None or str(reasoning_effort) == "auto":
        return None
    return str(reasoning_effort) not in _THINKING_OFF


class DeviceChat(GenericOpenAIChat):
    """OpenAI-compatible chat on a person's own device (``wire_format == "device_chat"``)."""

    def __init__(self) -> None:
        super().__init__(
            base_url=DEVICE_BASE_URL,
            api_key="device",
            provider_name="device",
        )

    @property
    def client(self) -> AsyncOpenAI:
        if self._client_pinned or self._client is not None:
            return self._client  # type: ignore[return-value]
        from matrx_ai.providers.device.relay_transport import RelayStreamTransport
        from matrx_ai.providers.keys import NO_SDK_RETRIES
        from matrx_ai.providers.outbound_capture import make_capture_http_client

        self._client = AsyncOpenAI(
            api_key="device",
            max_retries=NO_SDK_RETRIES,
            base_url=self._base_url,
            http_client=make_capture_http_client(
                sdk=openai_sdk, transport=RelayStreamTransport()
            ),
        )
        return self._client

    @client.setter
    def client(self, value: AsyncOpenAI) -> None:
        self._client = value
        self._client_pinned = True

    def to_provider_config(self, config: Any, profile: Any) -> dict[str, Any]:
        data = super().to_provider_config(config, profile)
        data["stream"] = True
        stream_options = dict(data.get("stream_options") or {})
        stream_options["include_usage"] = True
        data["stream_options"] = stream_options
        # The model's controls (its device offering's setting profile) already shaped the value to
        # what its chat template accepts; a template reads it only from chat_template_kwargs.
        shaped = data.pop("reasoning_effort", None)
        thinking = device_thinking(
            shaped if shaped is not None else getattr(config, "reasoning_effort", None)
        )
        kwargs = dict(data.get("chat_template_kwargs") or {})
        if thinking is not None:
            # Qwen 3 / Qwen 3.5 / Gemma 4 / GLM templates: the boolean switch.
            kwargs["enable_thinking"] = thinking
        if shaped is not None and str(shaped) not in ("auto", *_THINKING_OFF):
            # gpt-oss (low/medium/high) and Mistral Small 4 (high) templates: the level by name.
            kwargs["reasoning_effort"] = str(shaped)
        if kwargs:
            data["chat_template_kwargs"] = kwargs
        return data

    def _target(self, profile: Any) -> Any:
        from matrx_ai.providers.device.classify import make_device_error
        from matrx_ai.providers.device.errors import DeviceInvalidRequestError
        from matrx_ai.providers.device.relay_transport import DeviceCallTarget

        served_via = getattr(profile, "served_via", None)
        if served_via is None or getattr(profile, "route_kind", None) != "device":
            raise make_device_error(
                DeviceInvalidRequestError,
                "device_chat dispatched without a device route (served_via); nothing was sent",
            )
        local_id = str(served_via.local_model_id)
        model_key = str(getattr(profile, "provider_model_id", "") or "")
        facts = (getattr(profile, "offering_metadata", None) or {}).get("device_facts") or {}
        own_file = facts.get("source") == "device_model_file" or (
            local_id != str(getattr(profile, "model_id", "")) and _is_uuid(local_id)
        )
        reported = (facts.get("model_key") or {}).get("value") if isinstance(facts.get("model_key"), dict) else None
        if own_file and not (reported and reported == model_key):
            # A person's own model file runs under the key its computer published on the file
            # row (any ModelKey: own-<name>-<hash8>, or a dropped download's folder run key),
            # carried by the resolver. No key reported yet: refused, never guessed.
            raise make_device_error(
                DeviceInvalidRequestError,
                f"own model file {served_via.local_model_id} has no ModelKey reported by its "
                "computer yet; nothing was sent",
                details={"reason": "own_file_key_unknown"},
            )
        if not MODEL_KEY_PATTERN.match(model_key) or len(model_key) > 128:
            raise make_device_error(
                DeviceInvalidRequestError,
                f"{model_key!r} is not a Matrx 2 model key; nothing was sent",
                details={"reason": "bad_model_key"},
            )
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        token = str(getattr(ctx, "token", None) or "")  # orm-getattr-ok: AppContext
        return DeviceCallTarget(
            device_id=str(served_via.app_instance_id), model_key=model_key, token=token
        )

    async def execute(self, unified_config: Any, profile: Any, debug: bool = False) -> Any:
        import dataclasses

        from matrx_ai.providers.device.classify import device_error_for
        from matrx_ai.providers.device.errors import DeviceRouteError
        from matrx_ai.providers.device.relay_transport import (
            peer_accepts_chat_title,
            reset_device_call,
            set_device_call,
        )
        from matrx_ai.providers.errors import mark_billing_checked

        target = self._target(profile)
        # chat_title rides only to a device that declares protocol 1.92+: an older strict schema refuses the unknown param.
        if await peer_accepts_chat_title(target):
            title = await conversation_title_for_device(unified_config)
            if title:
                target = dataclasses.replace(target, chat_title=title)
        bound = set_device_call(target)
        try:
            response = await super().execute(unified_config, profile, debug=debug)
        except (openai_sdk.OpenAIError, httpx.HTTPError, DeviceRouteError) as exc:
            # A relay/device answer (or the transport's own typed refusal). Anything else is a
            # bug on our side and propagates as itself.
            typed = device_error_for(exc)
            # A device call bills nobody: nothing to capture, and the billing net is told so.
            mark_billing_checked(typed)
            if typed is exc:
                raise
            raise typed from exc
        finally:
            reset_device_call(bound)

        usage = getattr(response, "usage", None)
        if usage is not None:
            usage.api = DEVICE_USAGE_API
            usage.metadata["device_served"] = True
            usage.metadata["served_via"] = {
                "provider": "device",
                "app_instance_id": target.device_id,
            }
        return response


def real_conversation_title(raw: Any) -> str | None:
    """A conversation's own title, or None: an empty one and an ``Auto:`` placeholder are not titles."""
    from matrx_ai.db.conversation_gate import has_auto_title_prefix

    title = str(raw).strip() if isinstance(raw, str) else ""
    return None if not title or has_auto_title_prefix(title) else title[:200]


#: How much of the first user message names a chat that has no title of its own yet.
PREVIEW_CHARS = 60


def first_user_preview(messages: Any, limit: int = PREVIEW_CHARS) -> str | None:
    """The opening words of the first user message, whitespace collapsed, cut at a word and ended with an ellipsis."""
    from matrx_ai.config.message_flags import text_of

    for message in messages or []:
        role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
        if str(getattr(role, "value", role)) != "user":
            continue
        words = " ".join(text_of(message).split())
        if not words:
            continue
        if len(words) <= limit:
            return words
        cut = words[:limit].rsplit(" ", 1)[0] or words[:limit]
        return cut.rstrip(" ,.;:-") + "…"
    return None


async def conversation_title_for_device(unified_config: Any = None) -> str | None:
    """The title of the conversation this call belongs to, read at dispatch (the context carries only its id).

    A conversation still titled with an ``Auto:`` placeholder (or empty) is named by a short preview of its first
    user message: its opening words, never a generic label.
    """
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.db._registry import get_model

    ctx = try_get_app_context()
    conversation_id = getattr(ctx, "conversation_id", None)  # orm-getattr-ok: AppContext
    title: str | None = None
    if conversation_id:
        try:
            rows = await get_model("Conversation").filter(id=conversation_id).values("title")
            title = real_conversation_title(rows[0].get("title")) if rows else None
        except Exception as exc:  # the title is a courtesy to a busy refusal; a failed read must not fail the chat
            logger.warning("device chat: conversation title unreadable (%s): %s", conversation_id, exc)
    return title or first_user_preview(getattr(unified_config, "messages", None))


__all__ = ["DEVICE_BASE_URL", "DEVICE_USAGE_API", "DeviceChat", "device_model_key"]
