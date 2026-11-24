"""The free-tier model ceiling — guests and free accounts never run a premium model.

THE ONE SWAP (FREE-ALLOWANCE.md § Premium is catalog data; Arman 2026-10-17: "free stuff
for anyone, never premium models"). Every chat/media call resolves its model in ONE place,
``UnifiedAIClient._execute_dispatch``; that is where :func:`swap_for_free_tier` runs, so
``/ai/chat``, ``/ai/manual``, agents, sub-agents, workflows, tool loops and every other path
that hands ``UnifiedAIClient.execute`` a model inherit it. The client's model choice is never
trusted for a free tier: the decision reads only the request's identity (through the host
resolver) and catalog data.

* A model is premium for a tier when its ``ai.model_definition.cost_rating`` is above the
  tier's ceiling, when it is flagged ``is_premium`` (and the policy counts the flag), or —
  for turn models — when it has no rating and the policy treats unrated as premium. A
  per-model ``metadata.free_tier`` of ``"allow"`` / ``"deny"`` overrides all of that.
* Premium is SWAPPED DOWN, never refused, when a target exists: the model's own
  ``guest_fallback_id`` (guest) / ``mid_fallback_id`` (free) when that target is itself
  within the ceiling AND produces every media output the original does, else the tier's
  default model (chat models only — read from the declared outputs, never ``interaction``:
  an image model is never answered by a chat model). The person is told in one line (an ``info`` event,
  ``code="model_swapped"``, once per request) ONLY when they picked the original model themselves;
  a model they never chose is swapped silently (:func:`tell_model_swapped`, Arman 2026-11-20).
* A premium model with no in-ceiling target is REFUSED at the paid-call seam by
  :func:`admit_free_tier_model` (beside the top-tier gate) — the backstop that also covers
  the direct seam callers (STT, decisions, Live/Lyria) that never pass ``_execute_dispatch``.
  A caller refusal: never retried, rerouted or filed as a provider failure.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers a
SYNCHRONOUS ``ctx -> FreeTierPolicy | None`` memory read with
:func:`set_free_tier_policy_resolver` (None = a paid person, or nothing to apply). With none
registered nothing is swapped and that is announced once.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from matrx_connect.fix_actions import FIX_SIGN_UP, FIX_UPGRADE_PLAN
from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

FREE_TIER_MODEL_REFUSED = "free_tier_model_refused"
MODEL_SWAPPED_INFO_CODE = "model_swapped"
#: The request-context key holding the swap sentence; the executor stamps it on the answer row as ``model_swap``.
MODEL_SWAP_NOTE_KEY = "model_swap_note"
#: The request-context key where the HOST records a ceiling decision that is not a swap — a person the
#: host exempted (``{"decision": "exempt", ...}``) or whose tier it could not resolve (``{"decision":
#: "unknown", ...}``). The dispatch copies it onto the call's ``chat.request.metadata.model_ceiling`` so a
#: later reader sees why a premium model ran for a free-plan person. matrx-ai never decides or reads it.
MODEL_CEILING_KEY = "model_ceiling"
_TURN = "turn"


@dataclass(frozen=True)
class FreeTierPolicy:
    """What one request's tier may run. Built by the host from knobs, held in memory."""

    tier: Literal["guest", "free"]
    max_cost_rating: int
    default_model: str = ""
    unrated_is_premium: bool = True
    premium_flag_counts: bool = True


class FreeTierModelRefusedError(Exception):
    """A guest or free account asked for a premium model that has no free-tier stand-in."""

    is_caller_refusal = True
    http_status = 403

    def __init__(self, *, model_name: str, tier: str, user_id: str) -> None:
        self.model_name = model_name
        self.tier = tier
        self.user_id = user_id
        self.code = FREE_TIER_MODEL_REFUSED
        self.fix_action = FIX_SIGN_UP if tier == "guest" else FIX_UPGRADE_PLAN
        door = "Sign up free" if tier == "guest" else "Upgrade"
        # The person's sentence never names a model (Arman, 2026-11-16: a podcast showed
        # "gemini-2.5-pro-preview-tts needs a paid plan"). The model rides ``envelope()`` for us.
        self.message = f"This needs a paid plan. {door} to use it. Not run."
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details=self.envelope(),
        )
        super().__init__(self.message)

    def envelope(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "model_name": self.model_name,
            "tier": self.tier,
            "fix_action": self.fix_action,
            "user_id": self.user_id,
        }


#: The refusal sentence, current wording ("This needs ...") and the older one that named the model
#: ("<model> needs ..."), which stage rows written before 2026-11-16 still carry.
_REFUSAL_SENTENCE = re.compile(r"(?:This|\S+) needs a paid plan\. (?:Upgrade|Sign up free) to use it\. Not run\.")
_FALLBACK_WRAPPER = re.compile(r"\(fallback model also failed:\s*\)")


def is_free_tier_refusal(error: object) -> bool:
    """True when ``error`` is ONLY this ceiling's caller refusal — an exception, an envelope, or the text a
    stage or tool flattened it to (several refusals joined by "fallback model also failed" included).

    A refusal is the platform working as designed (the person sees it with its upgrade door), so a funnel
    that files failures as incidents asks here first. Text with anything else in it is not a refusal.
    """
    if isinstance(error, BaseException):
        if getattr(error, "code", None) == FREE_TIER_MODEL_REFUSED:
            return True
        error = str(error)
    if isinstance(error, dict):
        if error.get("error") == FREE_TIER_MODEL_REFUSED or error.get("error_type") == FREE_TIER_MODEL_REFUSED:
            return True
        error = error.get("message") or error.get("error") or ""
    if not isinstance(error, str) or not _REFUSAL_SENTENCE.search(error):
        return False
    rest = _FALLBACK_WRAPPER.sub("", _REFUSAL_SENTENCE.sub("", error))
    return not rest.strip(" \t\n.;,")


PolicyResolver = Callable[[Any], "FreeTierPolicy | None"]

_resolver: PolicyResolver | None = None
_unwired_announced = False
#: request ids already told about a swap (bounded) — one line per request, not per turn.
_told: OrderedDict[str, None] = OrderedDict()
#: Memory bound on the told-once set (plumbing, not a behavior: evicting oldest keys only risks one repeat note).
_TOLD_REMEMBERED = 20_000


def set_free_tier_policy_resolver(resolver: PolicyResolver | None) -> None:
    """Host wiring: a SYNCHRONOUS ``ctx -> FreeTierPolicy | None`` memory read."""
    global _resolver
    _resolver = resolver


_warmer: Callable[[Any], Awaitable[None]] | None = None


def set_free_tier_policy_warmer(warmer: Callable[[Any], Awaitable[None]] | None) -> None:
    """Host wiring (optional; a resolver carrying a ``warm`` attribute is wired the same way): an ASYNC ``ctx -> None`` the dispatch awaits ONCE before the synchronous
    resolver is asked, so a cold memory read can be made real (one awaited read) before the run's tier
    is decided. It must never raise a run's failure; a raise is announced and the resolver runs as before."""
    global _warmer
    _warmer = warmer


async def warm_policy_for(ctx: Any) -> None:
    """Await the host's warmer (if wired) for ``ctx``; never raises."""
    warmer = _warmer or getattr(_resolver, "warm", None)
    if ctx is None or warmer is None:
        return
    try:
        await warmer(ctx)
    except Exception as exc:  # noqa: BLE001 — announced; the resolver still answers from memory
        vcprint(
            f"[FreeTierModels] policy warmer raised ({type(exc).__name__}: {exc})",
            color="red",
            log_level="ERROR",
        )


def policy_for(ctx: Any) -> FreeTierPolicy | None:
    """The free-tier policy for this request, or None (paid / unwired / no context)."""
    global _unwired_announced
    if ctx is None:
        return None
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[FreeTierModels] no policy resolver wired by the host — guests and free "
                "accounts are NOT held below the premium-model ceiling in this process.",
                color="red",
                log_level="WARNING",
            )
        return None
    try:
        return _resolver(ctx)
    except Exception as exc:  # noqa: BLE001 — announced; a broken read never kills a run
        vcprint(
            f"[FreeTierModels] policy resolver raised ({type(exc).__name__}: {exc}) — "
            "no ceiling applied to this call.",
            color="red",
            log_level="ERROR",
        )
        return None


def _rating(row: Any) -> int | None:
    raw = getattr(row, "cost_rating", None)  # orm-getattr-ok: generated model row / CatalogModel
    if raw is None:
        raw = getattr(row, "model_cost_rating", None)  # orm-getattr-ok: CallProfile
    try:
        return int(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def _override(row: Any) -> str | None:
    meta = getattr(row, "metadata", None) or {}  # orm-getattr-ok: generated model row
    value = meta.get("free_tier") if isinstance(meta, dict) else None
    return value if value in ("allow", "deny") else None


#: Output modalities a stand-in must also produce. Text is never on this list: every model
#: answers in text, and a text answer is exactly what an image request must NOT receive.
_MEDIA_OUTPUTS = frozenset({"image", "video", "audio", "embedding"})


def media_outputs(row: Any) -> frozenset[str]:
    """The non-text outputs a catalog row declares (``capabilities.output``).

    ``interaction`` is the CALL shape ("turn" / "single" / "realtime"), never the modality:
    on the live catalog every Gemini image model and every Veo model is ``"turn"``. Live
    2026-11-02 (workflow runs d38f7bcc…, 5088a12b…): keying "is this a chat model?" on
    ``interaction`` sent a free account's ``gemini-3-pro-image`` step to the tier's default
    CHAT model, which answered in prose, and the step failed "provider returned no images".
    The modality is read here, from the declared outputs, and nowhere else.
    """
    caps = getattr(row, "capabilities", None)  # orm-getattr-ok: generated model row / CatalogModel
    if isinstance(caps, dict):
        declared = caps.get("output") or []
    else:
        declared = getattr(caps, "output", None) or []
        if not declared and caps is not None:
            declared = [m for m in ("image", "video", "audio", "embedding")
                        if getattr(caps, f"produces_{m}", False)]
    if isinstance(declared, str):
        declared = [declared]
    return frozenset(str(m).lower() for m in declared) & _MEDIA_OUTPUTS


def _answers_like(candidate: Any, original: Any) -> bool:
    """A stand-in answers the same request only when it produces every media output the
    original does — an image model is never answered by a chat model."""
    return media_outputs(original) <= media_outputs(candidate)


def is_premium_for(row: Any, policy: FreeTierPolicy, *, interaction: str = _TURN) -> bool:
    """Catalog data only: is this model above the policy's line?"""
    override = _override(row)
    if override == "allow":
        return False
    if override == "deny":
        return True
    if policy.premium_flag_counts and bool(getattr(row, "is_premium", False)):  # orm-getattr-ok
        return True
    rating = _rating(row)
    if rating is None:
        # Unrated follows the ``unrated_model_policy`` knob for every TURN-called model —
        # chat AND media. An unrated paid media model (grok-imagine-image-2.0, the ElevenLabs
        # music / sound / speech-to-speech rows: all ``interaction: "turn"``) is premium under
        # the default policy, exactly as before e68a653c1; exempting media by modality made
        # them free for free-tier accounts. Modality decides only what may STAND IN
        # (``_answers_like``), never whether the knob applies.
        return policy.unrated_is_premium and interaction == _TURN
    return rating > policy.max_cost_rating


async def _load(name_or_id: str) -> Any | None:
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance as model_mgr

    if not name_or_id:
        return None
    return await model_mgr.load_model(name_or_id)


async def free_tier_target(
    model_name: str,
    policy: FreeTierPolicy,
    *,
    interaction: str = _TURN,
    allow_default: bool = True,
) -> tuple[str, str] | None:
    """THE decision. ``None`` = run as asked. ``(name, "")`` = run ``name`` instead.
    ``("", reason)`` = premium with no in-ceiling stand-in (the seam refuses it)."""
    row = await _load(model_name)
    if row is None or not is_premium_for(row, policy, interaction=interaction):
        return None
    column = "guest_fallback_id" if policy.tier == "guest" else "mid_fallback_id"
    fallback_id = getattr(row, column, None)  # orm-getattr-ok: generated model row
    if fallback_id:
        target = await _load(str(fallback_id))
        if (
            target is not None
            and target.name
            and _answers_like(target, row)
            and _can_do_the_job(target, row)
            and not is_premium_for(target, policy, interaction=interaction)
        ):
            return str(target.name), ""
    # The tier's default is a CHAT model: it stands in only for a chat model (no media output),
    # whatever the ``interaction`` says (an image model is ``"turn"`` too).
    if allow_default and interaction == _TURN and policy.default_model and not media_outputs(row):
        default = await _load(policy.default_model)
        if (
            default is not None
            and default.name
            and default.name != getattr(row, "name", None)
            and _answers_like(default, row)
        ):
            return str(default.name), ""
    # No DECLARED stand-in. A media model the platform's own feature picked (a podcast's voice,
    # its video clips) must still run for a free tier, so the catalog is searched for the nearest
    # in-ceiling model of the same provider and the same inputs and outputs. Live 2026-11-16: 33
    # premium media rows had no fallback and a free account's podcast died at its audio step.
    if media_outputs(row):
        auto = await _nearest_in_ceiling(row, policy, interaction=interaction)
        if auto:
            return auto, ""
    return "", f"no free-tier model stands in for {model_name}"


def _voice_ids(row: Any) -> frozenset[str]:
    """The voices the catalog links to this model (``ai.voices.metadata.models``)."""
    from matrx_ai.catalog.manager import ai_catalog_manager

    return ai_catalog_manager.tts_voice_ids_for_model(str(getattr(row, "name", "") or ""))


def _can_do_the_job(candidate: Any, original: Any) -> bool:
    """A stand-in must be able to do what the original does. For a voiced model (TTS) that means
    carrying every voice the original carries: a guest podcast's chosen voice on a stand-in with
    no linked voices is refused at the voice step, after the run started (2026-11-18)."""
    wanted = _voice_ids(original)
    return not wanted or wanted <= _voice_ids(candidate)


def _modalities(row: Any, side: str) -> frozenset[str]:
    caps = getattr(row, "capabilities", None)  # orm-getattr-ok: generated model row / CatalogModel
    declared = caps.get(side) if isinstance(caps, dict) else getattr(caps, side, None)
    if isinstance(declared, str):
        declared = [declared]
    return frozenset(str(m).lower() for m in (declared or []))


def _interaction(row: Any) -> str:
    caps = getattr(row, "capabilities", None)  # orm-getattr-ok
    value = caps.get("interaction") if isinstance(caps, dict) else getattr(caps, "interaction", None)
    return str(value or _TURN)


def _shared_prefix(a: str, b: str) -> int:
    n = 0
    for x, y in zip(a, b, strict=False):
        if x != y:
            break
        n += 1
    return n


async def _all_models() -> list[Any]:
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance as model_mgr

    return list(await model_mgr.load_all_models())


async def _nearest_in_ceiling(row: Any, policy: FreeTierPolicy, *, interaction: str) -> str:
    """The catalog's nearest in-ceiling model that answers the same request as ``row``: same
    provider, same call shape, exactly the same inputs and outputs (a music model never voices a
    script, an image-to-video model never answers text-to-video), live. Nearest = same family
    first (longest shared name prefix), then the highest rating under the line. "" when none."""
    provider = getattr(row, "provider_id", None)  # orm-getattr-ok
    name = str(getattr(row, "name", "") or "")
    if not provider or not name:
        return ""
    try:
        rows = await _all_models()
    except Exception as exc:  # noqa: BLE001 — announced; the seam backstop still refuses
        vcprint(f"[FreeTierModels] stand-in search failed for {name!r}: {exc!r}", color="red", log_level="ERROR")
        return ""
    inputs, outputs, shape = _modalities(row, "input"), _modalities(row, "output"), _interaction(row)
    best: tuple[int, int, str] | None = None
    for cand in rows:
        cand_name = str(getattr(cand, "name", "") or "")
        if (
            not cand_name
            or cand_name == name
            or str(getattr(cand, "provider_id", "") or "") != str(provider)  # orm-getattr-ok
            or getattr(cand, "is_deprecated", False)  # orm-getattr-ok
            or getattr(cand, "retired_at", None)  # orm-getattr-ok
            or getattr(cand, "deleted_at", None)  # orm-getattr-ok
            or _interaction(cand) != shape
            or _modalities(cand, "output") != outputs
            or _modalities(cand, "input") != inputs
            or is_premium_for(cand, policy, interaction=interaction)
            or not _can_do_the_job(cand, row)
        ):
            continue
        key = (_shared_prefix(cand_name.lower(), name.lower()), _rating(cand) or 0, cand_name)
        if best is None or key > best:
            best = key
    if best is None:
        return ""
    vcprint(
        f"[FreeTierModels] {policy.tier}: no declared stand-in for {name}; nearest in-ceiling is {best[2]}",
        color="cyan",
        log_level="INFO",
    )
    return best[2]


async def stand_in_row(model_ref: str, policy: FreeTierPolicy) -> Any | None:
    """The catalog row that WILL answer in place of ``model_ref`` under ``policy`` (decided by
    :func:`free_tier_target`, the one decision the dispatch swap also uses), or None when the model
    runs as asked or no stand-in exists. Read-only: it swaps nothing and says nothing, so a client can
    name the answering model BEFORE the person sends (the chat's agent pill)."""
    target = await free_tier_target(model_ref, policy)
    if target is None or not target[0]:
        return None
    return await _load(target[0])


async def _label(name: str) -> str:
    """The model's display name (``common_name``) — what a person reads."""
    try:
        row = await _load(name)
    except Exception:  # noqa: BLE001 — the name is still honest
        return name
    return str(getattr(row, "common_name", None) or name) if row is not None else name  # orm-getattr-ok


async def tell_model_swapped(
    ctx: Any, original: str, new: str, policy: FreeTierPolicy, *, person_picked: bool = False
) -> None:
    """The ONE swap notice (``code="model_swapped"``, once per request and original model): every hop that swaps a
    free-tier model down goes through here — the dispatch swap below and a host's early hop (aidream's
    ``swap_model_for_auth_tier``).

    🚨 SPOKEN ONLY WHEN THE PERSON PICKED THE MODEL (Arman, 2026-11-20). ``person_picked`` is True only when
    the request named the model itself (``UnifiedConfig.model_picked_by_person``: the person's model picker).
    A model the person never chose (an agent's default, the plain chat page) is swapped SILENTLY: no stream
    notice and no sentence on the saved answer. Telling someone who just opened chat that their service was
    degraded is a message nobody approved (common-docs/policies/no-unapproved-restrictions.md). The swap is
    still recorded for staff on the call's swap trace (``model_swaps_this_turn`` → ``chat.request``)."""
    if not person_picked:
        vcprint(
            f"[FreeTierModels] {policy.tier} swap {original} -> {new} not announced: the person did not pick {original}",
            color="cyan",
            log_level="INFO",
        )
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    key = f"{request_id}:{original}"
    if request_id and key in _told:
        return
    if request_id:
        _told[key] = None
        while len(_told) > _TOLD_REMEMBERED:
            _told.popitem(last=False)
    emitter = getattr(ctx, "emitter", None)
    if emitter is None:
        return
    door = "Sign up free" if policy.tier == "guest" else "Upgrade"
    original_label, new_label = await _label(original), await _label(new)
    words = f"Ran on {new_label}. {door} for {original_label}."
    # The same sentence rides the answer's saved row (``chat.message.metadata.model_swap``, stamped by the executor
    # with ``provider_iteration``), so a reloaded chat says what model answered as the live one did (CGU-M3 W3).
    metadata = getattr(ctx, "metadata", None)
    if isinstance(metadata, dict):
        metadata[MODEL_SWAP_NOTE_KEY] = words
    try:
        from matrx_connect.context.events import InfoPayload

        await emitter.send_info(
            InfoPayload(
                code=MODEL_SWAPPED_INFO_CODE,
                system_message=f"free-tier model swap ({policy.tier}): {original} -> {new}",
                user_message=words,
                metadata={
                    "original_model": original,
                    "model": new,
                    "tier": policy.tier,
                    "fix_action": "sign_up" if policy.tier == "guest" else "upgrade_plan",
                    "model_swap_reason": "free_tier",
                },
            )
        )
    except Exception as exc:  # noqa: BLE001 — a notice never breaks the run
        vcprint(f"[FreeTierModels] swap notice not emitted: {exc!r}", color="yellow")


async def swap_for_free_tier(config: Any, profile: Any) -> bool:
    """Called by ``_execute_dispatch`` right after the profile resolves. When the request's
    tier may not run ``profile``'s model and a stand-in exists, rewrites ``config.model``
    (dropping any offering pin, which named the old model's route) and returns True — the
    caller re-resolves. Otherwise returns False and changes nothing.

    A device-served run (``served_via``) is never swapped: its one route is the person's own
    computer, and a stand-in would be a cloud model they did not pick (L5 R1)."""
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers.device.route_guard import is_device_served

    if is_device_served(config) or is_device_served(profile):
        return False

    ctx = try_get_app_context()
    await warm_policy_for(ctx)
    policy = policy_for(ctx)
    if policy is None:
        return False
    interaction = str(getattr(getattr(profile, "capabilities", None), "interaction", _TURN) or _TURN)
    original = str(getattr(profile, "model_name", "") or getattr(config, "model", "") or "")
    try:
        target = await free_tier_target(original, policy, interaction=interaction)
    except Exception as exc:  # noqa: BLE001 — the seam backstop still judges the call
        vcprint(
            f"[FreeTierModels] swap lookup failed for {original!r}: {type(exc).__name__}: {exc}",
            color="red",
            log_level="ERROR",
        )
        return False
    if target is None or not target[0]:
        return False
    new_name = target[0]
    # THIS TURN ONLY (CGU-10 IMG8 #2): the stand-in answers this turn; the stored chat keeps the
    # person's model and pin (``to_storage_dict`` reads the snapshot), so a later upgrade runs it again.
    from matrx_ai.config.unified_config import swap_model_this_turn_only

    swap_model_this_turn_only(config, new_name, swap_reason="free_tier", swapped_from=original)
    metadata = getattr(config, "metadata", None)
    if isinstance(metadata, dict):
        metadata["original_model"] = original
        metadata["model_swap_reason"] = "free_tier"
    vcprint(
        f"[FreeTierModels] {policy.tier} swap: {original} -> {new_name} "
        f"(user_id={getattr(ctx, 'user_id', None)})",
        color="cyan",
        log_level="INFO",
    )
    await tell_model_swapped(
        ctx, original, new_name, policy, person_picked=bool(getattr(config, "model_picked_by_person", False))
    )
    return True


def _finish_admitted_run(ctx: Any, name: str, policy: FreeTierPolicy) -> None:
    """A premium model with no in-ceiling stand-in, inside a run already admitted: it runs, loudly."""
    vcprint(
        f"[FreeTierModels] {policy.tier} user={getattr(ctx, 'user_id', None) or '<none>'} model={name}: "
        "no in-ceiling stand-in inside an admitted run — run as asked (a started run is never refused).",
        color="yellow",
        log_level="WARNING",
    )
    metadata = getattr(ctx, "metadata", None)
    if isinstance(metadata, dict):
        metadata[MODEL_CEILING_KEY] = {"decision": "admitted_run", "model": name, "tier": policy.tier}


async def admit_free_tier_model(profile: Any, *, in_admitted_run: bool | None = None) -> None:
    """The seam backstop: refuse a premium model that reached the paid call for a free tier.

    A device-served run (the person's own computer, ``route_kind == "device"``) is always
    admitted: it costs 0.0 and spends nobody's money, so there is nothing to ceiling.

    A RUN THAT HAS STARTED IS NEVER REFUSED (USAGE-GATE.md rule 5; Arman 2026-11-16): the refusal
    happens only at a run's first paid call. ``in_admitted_run`` is whether this call belongs to a
    run already admitted BEFORE it (the seam reads it before any gate remembers the run; None = read
    it here, :func:`usage_gate.admission_of`). A premium model with no stand-in inside such a run —
    a later step of a podcast, workflow or research run, a sub-agent, a retry, a resume — runs as
    asked: announced, and recorded on the call's ``model_ceiling`` (``decision: "admitted_run"``).
    """
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers.device.route_guard import is_device_served

    if is_device_served(profile):
        return

    ctx = try_get_app_context()
    if in_admitted_run is None:
        from matrx_ai.providers.usage_gate import admission_of

        in_admitted_run = admission_of(ctx)
    await warm_policy_for(ctx)
    policy = policy_for(ctx)
    if policy is None:
        return
    name = str(getattr(profile, "model_name", "") or "")
    try:
        row = await _load(name) or await _load(str(getattr(profile, "model_id", "") or ""))
    except Exception as exc:  # noqa: BLE001 — judged on the profile alone
        vcprint(f"[FreeTierModels] backstop lookup failed for {name!r}: {exc!r}", color="yellow")
        row = None
    # The CALL shape comes from the profile when it declares one, else from the catalog row. A direct
    # seam caller's hand-built route (a rerank, a Fastino extraction) carries no capabilities; reading
    # that absence as "turn" made every unrated non-turn model premium, and a free account's transcript
    # autolabel was refused 15 times in one hour (ops.system_error, 2026-11-20).
    declared = getattr(getattr(profile, "capabilities", None), "interaction", None)
    interaction = str(declared or (_interaction(row) if row is not None else _TURN))
    if not is_premium_for(row if row is not None else profile, policy, interaction=interaction):
        return
    if in_admitted_run:
        _finish_admitted_run(ctx, name, policy)
        return
    refusal = FreeTierModelRefusedError(
        model_name=name, tier=policy.tier, user_id=str(getattr(ctx, "user_id", "") or "")
    )
    vcprint(
        f"[FreeTierModels] refused {policy.tier} user={refusal.user_id or '<none>'} model={name}",
        color="yellow",
        log_level="WARNING",
    )
    raise refusal


__all__ = [
    "FREE_TIER_MODEL_REFUSED",
    "MODEL_CEILING_KEY",
    "MODEL_SWAPPED_INFO_CODE",
    "MODEL_SWAP_NOTE_KEY",
    "FreeTierModelRefusedError",
    "FreeTierPolicy",
    "admit_free_tier_model",
    "free_tier_target",
    "is_free_tier_refusal",
    "is_premium_for",
    "media_outputs",
    "policy_for",
    "stand_in_row",
    "set_free_tier_policy_resolver",
    "set_free_tier_policy_warmer",
    "warm_policy_for",
    "swap_for_free_tier",
    "tell_model_swapped",
]
