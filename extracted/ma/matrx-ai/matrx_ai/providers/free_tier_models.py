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
  within the ceiling, else the tier's default model (turn models only — an image model is
  never answered by a chat model). The person is told in one line (an ``info`` event,
  ``code="model_swapped"``, once per request).
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

from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

FREE_TIER_MODEL_REFUSED = "free_tier_model_refused"
MODEL_SWAPPED_INFO_CODE = "model_swapped"
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
        self.fix_action = "sign_up" if tier == "guest" else "upgrade_plan"
        door = "Sign up free" if tier == "guest" else "Upgrade"
        self.message = f"{model_name} needs a paid plan. {door} to use it. Not run."
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
        if target is not None and target.name and not is_premium_for(
            target, policy, interaction=interaction
        ):
            return str(target.name), ""
    if allow_default and interaction == _TURN and policy.default_model:
        default = await _load(policy.default_model)
        if default is not None and default.name and default.name != getattr(row, "name", None):
            return str(default.name), ""
    return "", f"no free-tier model stands in for {model_name}"


async def _label(name: str) -> str:
    """The model's display name (``common_name``) — what a person reads."""
    try:
        row = await _load(name)
    except Exception:  # noqa: BLE001 — the name is still honest
        return name
    return str(getattr(row, "common_name", None) or name) if row is not None else name  # orm-getattr-ok


async def _tell(ctx: Any, original: str, new: str, policy: FreeTierPolicy) -> None:
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
    try:
        from matrx_connect.context.events import InfoPayload

        await emitter.send_info(
            InfoPayload(
                code=MODEL_SWAPPED_INFO_CODE,
                system_message=f"free-tier model swap ({policy.tier}): {original} -> {new}",
                user_message=f"Ran on {new_label}. {door} for {original_label}.",
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
    config.model = new_name
    for pin in ("offering_id", "runtime_offering_id"):
        if getattr(config, pin, None):
            setattr(config, pin, None)
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
    await _tell(ctx, original, new_name, policy)
    return True


async def admit_free_tier_model(profile: Any) -> None:
    """The seam backstop: refuse a premium model that reached the paid call for a free tier.

    A device-served run (the person's own computer, ``route_kind == "device"``) is always
    admitted: it costs 0.0 and spends nobody's money, so there is nothing to ceiling.
    """
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers.device.route_guard import is_device_served

    if is_device_served(profile):
        return

    ctx = try_get_app_context()
    policy = policy_for(ctx)
    if policy is None:
        return
    name = str(getattr(profile, "model_name", "") or "")
    interaction = str(getattr(getattr(profile, "capabilities", None), "interaction", _TURN) or _TURN)
    try:
        row = await _load(name) or await _load(str(getattr(profile, "model_id", "") or ""))
    except Exception as exc:  # noqa: BLE001 — judged on the profile alone
        vcprint(f"[FreeTierModels] backstop lookup failed for {name!r}: {exc!r}", color="yellow")
        row = None
    if not is_premium_for(row if row is not None else profile, policy, interaction=interaction):
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
    "MODEL_SWAPPED_INFO_CODE",
    "FreeTierModelRefusedError",
    "FreeTierPolicy",
    "admit_free_tier_model",
    "free_tier_target",
    "is_premium_for",
    "policy_for",
    "set_free_tier_policy_resolver",
    "swap_for_free_tier",
]
