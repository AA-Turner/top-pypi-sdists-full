"""The BAA gate at the provider-call boundary: HIPAA-mode work reaches only covered vendors.

THE RULE (HIPAA build contract). When the host says a call is HIPAA-gated, patient data reaches
ONLY a vendor + interaction the platform holds a Business Associate Agreement for. Refuse by
default; swap only a chat model. Every refusal and swap is told (nothing fails silently).

WHERE IT RUNS — the same two places the child-safety gate runs:

* :func:`admit_baa` in ``UnifiedAIClient._dispatch_with_billing_net`` — the seam every paid call
  passes (chat, media, STT, decisions, extraction, rerank, embeddings) — right after the
  child-safety refusal and BEFORE capture mode, so a captured call is refused exactly as a real
  one would be. A device route (``route_kind == "device"``) is refused: its relay is not covered.
* :func:`refuse_own_key_if_gated` right after the provider client's key preflight: a call about to
  run on the person's or organization's OWN key is refused unless the organization attested its
  keys are covered (``own_keys_ok``).
* :func:`swap_for_baa` in ``UnifiedAIClient._execute_dispatch`` after the free-tier swap: a
  non-covered CHAT model is replaced by the policy's chat stand-in (never above the free-tier
  ceiling), the offering pins dropped, and the person told once. Every other interaction
  (decision, extraction, agent, image, video, speech, realtime) is refused by :func:`admit_baa`.
* :func:`apply_baa_features` on the config of a covered call: hosted server tools are removed
  (web search / fetch / code execution / MCP connector run on the vendor outside the Messages or
  zero-retention API), OpenAI ``store`` is forced off and the 24h prompt-cache retention dropped.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers one async
``ctx -> policy | None`` with :func:`set_baa_policy_host`. The policy is duck-typed: ``reason``,
``organization_id``, ``chat_standin_model``, ``stt_standin_model``, ``own_keys_ok`` and
``covers(vendor, interaction) -> bool``. With no host nothing is gated, announced once. A host
that RAISES refuses the call (fail closed): HIPAA status that cannot be read is not "off".
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

HIPAA_NOT_COVERED = "hipaa_not_covered"
HIPAA_MODEL_SWAPPED_INFO_CODE = "model_swapped"
#: The sentence a HIPAA stand-in swap says (the stream notice, and a workflow agent step's ``metadata.model_swapped``).
HIPAA_SWAP_SENTENCE = "Ran on a covered model: the one first chosen uses a vendor that is not covered in HIPAA mode."

#: Readable vendor names for the refusal sentence (anything else is title-cased).
_VENDOR_LABELS = {
    "openai": "OpenAI", "xai": "xAI", "groq": "Groq", "google": "Google", "anthropic": "Anthropic",
    "typesafe": "TypeSafe", "fastino": "Fastino", "huggingface": "Hugging Face", "elevenlabs": "ElevenLabs",
    "livekit": "LiveKit", "device": "the device relay", "generic_openai": "a custom OpenAI-compatible service",
}


def vendor_label(vendor: str | None) -> str:
    v = str(vendor or "").strip()
    return _VENDOR_LABELS.get(v.lower(), v.title() or "an unknown service")


class BaaRefusedError(Exception):
    """A HIPAA-gated call asked for a vendor or feature with no BAA. A caller refusal: never
    retried, rerouted or filed as a provider failure."""

    is_caller_refusal = True
    http_status = 403

    def __init__(self, what: str, vendor: str | None = None, *, message: str | None = None) -> None:
        self.code = HIPAA_NOT_COVERED
        self.what = what
        self.vendor = vendor
        # Never the vendor's name in the person's sentence (Arman, 2026-11-18); ``vendor`` rides the details.
        uses = " uses a vendor that" if vendor else ","
        self.message = message or (
            f"This organization is in HIPAA mode. {what}{uses} has not signed a Business Associate "
            "Agreement with AI Matrx, so it is turned off here."
        )
        self.user_message = self.message
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details={"error": self.code, "message": self.message, "what": what, "vendor": vendor},
        )
        super().__init__(self.message)


PolicyHost = Callable[[Any], Awaitable[Any]]

_host: PolicyHost | None = None
_unwired_announced = False
_told: OrderedDict[str, None] = OrderedDict()
#: Memory bound on the told-once set (plumbing: evicting the oldest only risks one repeated note).
_TOLD_REMEMBERED = 20_000


def set_baa_policy_host(host: PolicyHost | None) -> None:
    """Host wiring: async ``ctx -> policy | None``. ``None`` unwires."""
    global _host
    _host = host


def baa_policy_host() -> PolicyHost | None:
    return _host


async def baa_policy(ctx: Any = None) -> Any:
    """The HIPAA policy for this call, or None. Raises :class:`BaaRefusedError` when the host
    cannot answer (fail closed)."""
    global _unwired_announced
    if _host is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[BaaGate] no host wired. HIPAA mode is NOT enforced at the provider boundary in "
                "this process.",
                color="red",
                log_level="WARNING",
            )
        return None
    if ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    try:
        return await _host(ctx)
    except BaaRefusedError:
        raise
    except Exception as exc:  # noqa: BLE001 — fail closed, loudly
        vcprint(
            f"[BaaGate] host could not read HIPAA status ({type(exc).__name__}: {exc}). Call refused.",
            color="red",
            log_level="ERROR",
        )
        raise BaaRefusedError(
            "This call",
            message=(
                "HIPAA mode could not be confirmed for this organization, so this AI call was not "
                "sent. Try again in a moment."
            ),
        ) from exc


def baa_interaction(profile: Any) -> str:
    """What this call does, in the ``baa_covered`` vocabulary: chat, image, video, tts,
    transcription, embedding, moderation, extraction, decision, agent, realtime, adapter."""
    caps = getattr(profile, "capabilities", None)
    mode = str(getattr(caps, "interaction", None) or "turn")
    if mode in ("turn", "single"):
        if getattr(caps, "produces_image", False):
            return "image"
        if getattr(caps, "produces_video", False):
            return "video"
        if getattr(caps, "produces_audio", False) and not getattr(caps, "produces_text", True):
            return "tts"
        if (
            getattr(caps, "supports_audio_input", False)
            and not getattr(caps, "supports_text_input", True)
            and getattr(caps, "produces_text", False)
        ):
            return "transcription"
        return "chat"
    if mode == "detection":
        return "moderation"
    return mode


def _vendor(profile: Any) -> str:
    return str(getattr(profile, "vendor", None) or getattr(profile, "provider_name", None) or "").lower()


def _model_words(profile: Any) -> str:
    # Never the model's name in the person's sentence (Arman, 2026-11-18).
    return "This model" if getattr(profile, "model_name", None) else "This AI call"


async def admit_baa(profile: Any) -> None:
    """The seam refusal: vendor + interaction not covered, or a device route, is refused."""
    policy = await baa_policy()
    if policy is None:
        return
    vendor = _vendor(profile)
    if getattr(profile, "route_kind", None) == "device":
        raise _refuse(_model_words(profile) + " on your own computer", "device", policy)
    interaction = baa_interaction(profile)
    if not policy.covers(vendor, interaction):
        what = _model_words(profile)
        if interaction != "chat":
            what = f"{what} ({interaction})"
        raise _refuse(what, vendor, policy)


def _refuse(what: str, vendor: str, policy: Any) -> BaaRefusedError:
    vcprint(
        f"[BaaGate] refused {what} vendor={vendor} reason={getattr(policy, 'reason', '?')} "
        f"org={getattr(policy, 'organization_id', None)}",
        color="yellow",
        log_level="WARNING",
    )
    return BaaRefusedError(what, vendor)


async def refuse_own_key_if_gated(profile: Any) -> None:
    """After the key preflight: a gated call about to run on an own key is refused unless the
    organization attested its keys are covered."""
    from matrx_ai.providers.keys import last_resolved_key_source

    if last_resolved_key_source() != "own":
        return
    policy = await baa_policy()
    if policy is None or getattr(policy, "own_keys_ok", False):
        return
    raise BaaRefusedError(
        f"{_model_words(profile)} on your own {vendor_label(_vendor(profile))} key",
        message=(
            "This organization is in HIPAA mode. Your own AI provider key is not covered by AI "
            "Matrx's Business Associate Agreement, so it is turned off here. An organization "
            "admin can attest the key is covered."
        ),
    )


#: Hosted server tools a covered vendor runs OUTSIDE the covered API (config flags).
def _hosted_tool_flags() -> tuple[str, ...]:
    from matrx_ai.providers.tool_adaptation import INTERNAL_TOOL_FLAGS

    return INTERNAL_TOOL_FLAGS


async def apply_baa_features(config: Any, profile: Any) -> list[str]:
    """On a gated call: drop hosted server tools, force OpenAI ``store`` off and drop the 24h
    prompt-cache retention. Returns what was changed (each one announced)."""
    policy = await baa_policy()
    if policy is None or config is None:
        return []
    changed: list[str] = []
    for flag in _hosted_tool_flags():
        if getattr(config, flag, None):
            setattr(config, flag, None)
            changed.append(flag)
    if _vendor(profile) == "openai":
        if hasattr(config, "store") and config.store is not False:
            config.store = False
            changed.append("store")
        if getattr(config, "extended_prompt_cache", False):
            config.extended_prompt_cache = False
            changed.append("extended_prompt_cache")
    if changed:
        vcprint(f"[BaaGate] HIPAA mode removed {', '.join(changed)} from {getattr(config, 'model', '?')}",
                color="cyan", log_level="INFO")
        if any(flag in changed for flag in _hosted_tool_flags()):
            await _tell_once(
                "hosted_tools",
                "Web search and other tools that run on the AI provider are off in HIPAA mode.",
                {"removed": changed},
            )
    return changed


async def swap_for_baa(config: Any, profile: Any) -> bool:
    """A non-covered CHAT model becomes the policy's chat stand-in (person told once). Returns
    True when ``config.model`` changed (the caller re-resolves). Anything else is left for
    :func:`admit_baa` to refuse. A device-served run is never moved to a cloud model."""
    from matrx_ai.providers.device.route_guard import is_device_served

    if is_device_served(config) or is_device_served(profile):
        return False
    policy = await baa_policy()
    if policy is None or baa_interaction(profile) != "chat":
        return False
    if policy.covers(_vendor(profile), "chat"):
        return False
    target = str(getattr(policy, "chat_standin_model", "") or "")
    original = str(getattr(profile, "model_name", "") or getattr(config, "model", "") or "")
    if not target or target == original:
        return False
    await _refuse_above_free_tier(target, original, profile)
    # THIS TURN ONLY (CGU-10 IMG8 #2): the stand-in answers this turn; the stored chat keeps the
    # person's model and pin (``to_storage_dict`` reads the snapshot), so a later upgrade runs it again.
    from matrx_ai.config.unified_config import swap_model_this_turn_only

    swap_model_this_turn_only(config, target, swap_reason="hipaa", swapped_from=original)
    metadata = getattr(config, "metadata", None)
    if isinstance(metadata, dict):
        metadata["original_model"] = original
        metadata["model_swap_reason"] = "hipaa"
    vcprint(f"[BaaGate] HIPAA swap: {original} -> {target}", color="cyan", log_level="INFO")
    await _tell_once(
        f"swap:{original}",
        HIPAA_SWAP_SENTENCE,
        {"original_model": original, "model": target, "model_swap_reason": "hipaa"},
        code=HIPAA_MODEL_SWAPPED_INFO_CODE,
    )
    return True


async def _refuse_above_free_tier(target: str, original: str, profile: Any) -> None:
    """The stand-in never lifts a guest or free account above its ceiling: refuse instead."""
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers.free_tier_models import _load, is_premium_for, policy_for

    tier = policy_for(try_get_app_context())
    if tier is None:
        return
    row = await _load(target)
    if row is None or is_premium_for(row, tier):
        raise BaaRefusedError(_model_words(profile), _vendor(profile))


async def _label(name: str) -> str:
    try:
        from matrx_ai.providers.free_tier_models import _label as free_label

        return await free_label(name)
    except Exception:  # noqa: BLE001 — the name is still honest
        return name


async def _tell_once(key: str, user_message: str, metadata: dict[str, Any], *, code: str = "hipaa_mode") -> None:
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    request_id = str(getattr(ctx, "request_id", "") or "")
    told_key = f"{request_id}:{key}"
    if request_id and told_key in _told:
        return
    if request_id:
        _told[told_key] = None
        while len(_told) > _TOLD_REMEMBERED:
            _told.popitem(last=False)
    ctx_meta = getattr(ctx, "metadata", None)
    if isinstance(ctx_meta, dict):
        notices = ctx_meta.setdefault("hipaa_notices", [])
        if isinstance(notices, list):
            notices.append({"what": key, "detail": user_message})
    emitter = getattr(ctx, "emitter", None)
    if emitter is None:
        return
    try:
        from matrx_connect.context.events import InfoPayload

        await emitter.send_info(
            InfoPayload(code=code, system_message=f"hipaa: {key}", user_message=user_message, metadata=metadata)
        )
    except Exception as exc:  # noqa: BLE001 — a notice never breaks the run
        vcprint(f"[BaaGate] notice not emitted: {exc!r}", color="yellow")


async def stt_standin_or_refuse() -> str | None:
    """Chat audio preprocessing under HIPAA mode: the covered transcription model to use, None when
    nothing is gated. Gated with no stand-in configured → refused."""
    policy = await baa_policy()
    if policy is None:
        return None
    model = str(getattr(policy, "stt_standin_model", "") or "")
    if not model:
        raise BaaRefusedError(
            "Transcribing audio in chat",
            message=(
                "This organization is in HIPAA mode and no covered transcription model is set, so "
                "audio in this chat cannot be transcribed here."
            ),
        )
    return model


async def stt_model_for_baa(profile: Any) -> str | None:
    """Direct transcription under HIPAA mode: the covered stand-in model to run INSTEAD of
    ``profile``, or None (nothing gated, the model is covered, or no stand-in is set — then
    :func:`admit_baa` refuses it at the seam with a typed :class:`BaaRefusedError`)."""
    policy = await baa_policy()
    if policy is None or policy.covers(_vendor(profile), "transcription"):
        return None
    target = str(getattr(policy, "stt_standin_model", "") or "")
    original = str(getattr(profile, "model_name", "") or "")
    if not target or target == original:
        return None
    vcprint(f"[BaaGate] HIPAA transcription swap: {original} -> {target}", color="cyan", log_level="INFO")
    return target


async def covered_sibling_filter(vendor: str) -> bool:
    """Overload reroute: may a sibling route on ``vendor`` carry this (chat) call?"""
    policy = await baa_policy()
    return policy is None or bool(policy.covers(str(vendor or "").lower(), "chat"))


__all__ = [
    "HIPAA_NOT_COVERED",
    "BaaRefusedError",
    "admit_baa",
    "apply_baa_features",
    "baa_interaction",
    "baa_policy",
    "baa_policy_host",
    "covered_sibling_filter",
    "refuse_own_key_if_gated",
    "set_baa_policy_host",
    "stt_model_for_baa",
    "stt_standin_or_refuse",
    "swap_for_baa",
    "vendor_label",
]
