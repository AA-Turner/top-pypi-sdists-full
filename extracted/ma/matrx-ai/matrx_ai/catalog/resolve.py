"""resolve_call_profile — the ONE routing seam.

Every dispatch asks the catalog (`ai.provider` / `ai.model_definition` /
`ai.endpoint` / `ai.api` / `ai.offering` / `ai.setting`) exactly once and gets
back everything the call needs: which client to hit (api.translator_key), what
model id goes on the wire, where to call it (endpoint.base_url/auth), what the
model can do, how its controls translate, and what it costs.

Inbound model refs route through ``ai_catalog_manager.resolve_model_ref`` — the
alias map (ai.model_alias) resolves INSIDE ``AiModelManager.load_model`` (the
one funnel every entry path shares), so the loader receives the canonical id.
There is no legacy path and no mode switch. A model with no available offering
cannot be routed and RAISES — never a silent fallback.
"""

from __future__ import annotations

from matrx_utils import vcprint

from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.manager import AiCatalogManager, ai_catalog_manager
from matrx_ai.catalog.models import CatalogOffering, CatalogVoice, ResolvedCallProfile
from matrx_ai.catalog.routes import client_attr_for_wire_format
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities


def _match_endpoint_hint(
    offerings: list[CatalogOffering], manager: AiCatalogManager, endpoint_hint: str
) -> list[CatalogOffering]:
    matched: list[CatalogOffering] = []
    for offering in offerings:
        endpoint = manager.endpoint(offering.endpoint_id)
        if endpoint is None:
            continue
        if endpoint_hint in (endpoint.vendor, endpoint.internal_name, endpoint.id):
            matched.append(offering)
    return matched


def _resolve_pinned_offering(
    offerings: list[CatalogOffering],
    manager: AiCatalogManager,
    *,
    offering_id: str,
    model_id: str,
    model_name: str,
) -> CatalogOffering:
    """Resolve a PINNED offering exactly — or RAISE loudly, never fall back.

    The pin is the owner's doctrine made executable: "when we list a model,
    we're not listing the model, we're listing the exact call." A pin that is
    unavailable or belongs to another model is a caller/config bug and must
    scream — silently substituting the preferred offering would defeat the
    entire point of pinning.
    """
    pin = str(offering_id)
    for offering in offerings:
        if offering.id == pin:
            return offering

    # Not routable — diagnose WHY, loudly.
    known = manager.offering(pin)
    if known is None:
        detail = (
            f"offering '{pin}' does not exist in the catalog (no ai.offering row, "
            f"or the row is quarantined)."
        )
    elif str(known.model_id) != str(model_id):
        detail = (
            f"offering '{pin}' belongs to model_id '{known.model_id}', not the "
            f"requested model '{model_name}' ({model_id}). The pin must be cleared "
            f"or re-selected when the model changes."
        )
    elif not known.is_available:
        detail = f"offering '{pin}' exists for this model but is_available=false."
    else:
        endpoint = manager.endpoint(known.endpoint_id)
        if endpoint is None or not endpoint.is_active:
            detail = (
                f"offering '{pin}' exists and is available, but its endpoint "
                f"'{known.endpoint_id}' is missing or inactive."
            )
        else:
            detail = (
                f"offering '{pin}' exists but its api '{known.api_id}' is missing "
                f"or quarantined."
            )
    vcprint(
        f"PINNED offering for model '{model_name}' ({model_id}) cannot be routed: "
        f"{detail} A pinned offering NEVER silently falls back to the preferred "
        f"one — fix the pin or unset it.",
        title="🚨 AI CATALOG PINNED-OFFERING FAILURE",
        color="red",
    )
    raise CatalogRoutingError(
        f"resolve_call_profile: pinned offering '{pin}' is not routable for model "
        f"'{model_name}' ({model_id}) — {detail}"
    )


def select_tts_default_voice(
    model_name: str, voices: tuple[CatalogVoice, ...]
) -> str | None:
    """Return the unique model-linked default voice, raising on ambiguity."""
    default_voice_ids: list[str] = []
    for voice in voices:
        defaults = voice.metadata.get("default_for_models", ())
        if isinstance(defaults, str):
            defaults = (defaults,)
        if model_name in defaults:
            default_voice_ids.append(voice.provider_voice_id)
    if len(default_voice_ids) > 1:
        vcprint(
            f"Model {model_name!r} has multiple catalog default voices: "
            f"{default_voice_ids}. Exactly one ai.voices row may list it in "
            "metadata.default_for_models.",
            title="🚨 TTS VOICE CATALOG AMBIGUITY",
            color="red",
        )
        raise CatalogRoutingError(
            f"Multiple default TTS voices for model {model_name!r}: {default_voice_ids}"
        )
    return default_voice_ids[0] if default_voice_ids else None


async def resolve_call_profile(
    model_ref: str,
    endpoint_hint: str | None = None,
    *,
    offering_id: str | None = None,
) -> ResolvedCallProfile:
    # Lazy import: the model manager's ORM path resolves get_model("AiModel"),
    # which must not fire on a bare ``import matrx_ai.catalog``.
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    # Alias resolution (id -> name -> ai.model_alias) lives INSIDE
    # AiModelManager.load_model — the ONE funnel every entry path shares.
    # No second resolution here.
    model = await ai_model_manager_instance.load_model(model_ref)
    if model is None and offering_id is not None:
        # PIN RECOVERY: mid-loop re-dispatch carries the offering's
        # provider_model_id in config.model (UnifiedAIClient rewrites it at
        # dispatch), which may not be a resolvable model ref when it diverges
        # from the canonical name. The pin itself names the exact call, so the
        # model is recoverable FROM the pin. Loud, deterministic, pin-only.
        manager = ai_catalog_manager
        await manager.ensure_loaded()
        pinned = manager.offering(str(offering_id))
        if pinned is not None:
            model = await ai_model_manager_instance.load_model(str(pinned.model_id))
            if model is not None:
                vcprint(
                    f"resolve_call_profile: model ref '{model_ref}' did not resolve "
                    f"directly; recovered model '{getattr(model, 'name', '?')}' from "
                    f"pinned offering '{offering_id}'.",
                    color="yellow",
                )
    if model is None:
        raise CatalogRoutingError(f"resolve_call_profile: unknown model '{model_ref}'")

    # CLIENT-HOST / RUNTIME path: a model served by the injected catalog (or the
    # runtime registry) has no ai.endpoint / ai.api / ai.offering rows — the
    # profile is synthesized from the model dict itself (explicit wire_format /
    # endpoints / loud api_class derivation; passthrough controls; pricing off
    # the dict).
    from matrx_ai.catalog.host_catalog import CatalogModel, build_catalog_call_profile

    if isinstance(model, CatalogModel):
        if offering_id is not None:
            raise CatalogRoutingError(
                f"resolve_call_profile: model '{model_ref}' is served by the "
                f"client-host/runtime catalog, which has no ai.offering rows — the "
                f"pinned offering '{offering_id}' cannot apply. Unset the pin."
            )
        return build_catalog_call_profile(model)

    manager = ai_catalog_manager
    await manager.ensure_loaded()

    model_id = str(model.id)
    offerings = manager.offerings_for(model_id)

    if endpoint_hint is not None:
        offerings = _match_endpoint_hint(offerings, manager, endpoint_hint)
        if not offerings:
            vcprint(
                f"Model '{model.name}' ({model_id}) has NO available ai.offering on "
                f"endpoint '{endpoint_hint}'. Check ai.offering rows / the endpoint vendor.",
                title="🚨 AI CATALOG RESOLVE FAILURE",
                color="red",
            )
            raise CatalogRoutingError(
                f"resolve_call_profile: no available offering for model '{model.name}' "
                f"on endpoint '{endpoint_hint}'"
            )

    if not offerings:
        vcprint(
            f"Model '{model.name}' ({model_id}) exists in ai.model_definition but has "
            f"ZERO available ai.offering rows (or every offering's endpoint is inactive/"
            f"quarantined). The FE can still list it from model_definition — that is "
            f"the trap. Create an ai.offering: model_id + endpoint_id + api_id + "
            f"provider_model_id.",
            title="🚨 AI CATALOG RESOLVE FAILURE",
            color="red",
        )
        raise CatalogRoutingError(
            f"resolve_call_profile: model '{model.name}' ({model_id}) has no available "
            f"ai.offering — the catalog cannot route it"
        )

    if offering_id is not None:
        # PINNED: resolve exactly that offering or RAISE — never the preferred.
        offering = _resolve_pinned_offering(
            offerings,
            manager,
            offering_id=offering_id,
            model_id=model_id,
            model_name=getattr(model, "name", "") or model_id,
        )
        resolution_route: str = "pinned"
    else:
        offering = offerings[0]  # priority-ordered by the manager
        resolution_route = "preferred"
    endpoint = manager.endpoint(offering.endpoint_id)
    api = manager.api(offering.api_id)
    if endpoint is None or api is None:  # pragma: no cover — offerings_for guarantees both
        raise CatalogRoutingError(
            f"resolve_call_profile: offering '{offering.id}' points at missing "
            f"endpoint '{offering.endpoint_id}' / api '{offering.api_id}'"
        )

    # The offering may sharpen the model's declared capabilities for THIS route
    # (sparse per-top-level-key merge, offering wins) — e.g. the same model served
    # by two providers where only one hosts web search.
    capabilities = resolve_model_capabilities(
        model, capabilities_override=offering.capabilities_override
    )

    # Provider identity comes from the provider_id FK, never a varchar column.
    provider_id = getattr(model, "provider_id", None)
    provider_name = manager.provider_name(provider_id)
    if not provider_name:
        raise CatalogRoutingError(
            f"resolve_call_profile: model '{model.name}' ({model_id}) has no resolvable "
            f"ai.provider via provider_id={provider_id!r} — the FK is required on "
            "every model row"
        )

    model_state = manager.model_state(model_id)
    voices = manager.tts_voices(endpoint.vendor, getattr(model, "name", "") or "")
    model_name = getattr(model, "name", "") or ""
    default_voice = select_tts_default_voice(model_name, voices)
    return ResolvedCallProfile(
        resolution_route=resolution_route,
        model_id=model_id,
        model_name=model_name,
        provider_model_id=offering.provider_model_id,
        offering_id=offering.id,
        endpoint_id=endpoint.id,
        api_id=api.id,
        provider_name=provider_name,
        vendor=endpoint.vendor,
        wire_format=api.translator_key,
        client_attr=client_attr_for_wire_format(api.translator_key),
        base_url=endpoint.base_url,
        auth_ref=endpoint.auth_ref,
        byok_secret_key=endpoint.byok_secret_key,
        capabilities=capabilities,
        controls=manager.compiled_controls(api.id, offering.id),
        request_defaults=api.request_defaults,
        pricing=offering.pricing if offering.pricing else getattr(model, "pricing", None),
        usage_basis=offering.usage_basis,
        token_billed=offering.token_billed,
        model_is_deprecated=bool(model_state.get("is_deprecated", False)),
        model_is_primary=bool(model_state.get("is_primary", False)),
        offering_metadata=offering.metadata,
        tts_voice_ids=tuple(voice.provider_voice_id for voice in voices),
        tts_default_voice_id=default_voice,
    )


def _mark_tts_reroute(
    original: ResolvedCallProfile,
    rerouted: ResolvedCallProfile,
    requested_tier: str | None,
) -> ResolvedCallProfile:
    """A caller pinned model A and we are calling model B — say so, LOUDLY.

    Catalog tier routing is allowed to override an explicit model pin (that is
    what quality tiers are FOR), but it must never be invisible: it silently
    moved every 1-2 host podcast off its pinned gemini-2.5-pro-preview-tts onto
    gemini-3.1-flash-tts-preview for days (2026-08-10) because the
    ``high_quality`` tier tag sat on the flash offering. The audio changed, the
    voice count changed, and nothing anywhere said the model had changed.

    Reroute-and-log, never raise: killing a live paid render over routing would
    be worse than rendering on a sibling model.

    Returns the profile stamped ``resolution_route="tier_reroute"`` so the
    deviation also lands DURABLY on TokenUsage.offering_route → cx_request.
    A console banner is read by nobody at 2am; the column is queryable.
    """
    if rerouted.model_name == original.model_name:
        return rerouted
    vcprint(
        f"TTS ROUTED AWAY FROM THE REQUESTED MODEL: {original.model_name!r} → "
        f"{rerouted.model_name!r} (vendor={original.vendor!r}, "
        f"requested quality tier={requested_tier or 'high_quality'!r}, "
        f"deprecated={original.model_is_deprecated}).\n"
        f"The tier tags in ai.offering.metadata.tts.quality_tiers decide this — "
        f"if {original.model_name!r} should have served this call, add the tier "
        f"to ITS offering. To pin a model past tier routing, pass offering_id.",
        title="🔀 TTS MODEL REROUTE",
        color="yellow",
    )
    return rerouted.model_copy(update={"resolution_route": "tier_reroute"})


async def resolve_tts_call_profile(
    model_ref: str,
    quality: str | None = None,
    *,
    offering_id: str | None = None,
) -> ResolvedCallProfile:
    """Resolve a TTS call, including catalog-owned quality/default routing."""
    profile = await resolve_call_profile(model_ref, offering_id=offering_id)
    caps = profile.capabilities
    if not (caps.produces_audio and not caps.produces_text):
        return profile
    if offering_id is not None:
        return profile

    tts_meta = profile.offering_metadata.get("tts")
    requested_tier = (quality or "").strip().lower() or None
    current_tiers: tuple[str, ...] = ()
    if isinstance(tts_meta, dict):
        raw_tiers = tts_meta.get("quality_tiers", ())
        current_tiers = (raw_tiers,) if isinstance(raw_tiers, str) else tuple(raw_tiers)

    needs_catalog_selection = profile.model_is_deprecated or (
        requested_tier is not None and requested_tier not in current_tiers
    )
    if not needs_catalog_selection:
        return profile

    if profile.offering_id.startswith("catalog:"):
        from matrx_ai.catalog.host_catalog import (
            CatalogModel,
            build_catalog_call_profile,
            get_model_catalog,
            list_runtime_models,
        )

        rows = [model.to_dict() for model in list_runtime_models()]
        host = get_model_catalog()
        if host is not None:
            rows.extend(await host.list_models())
        candidates: list[tuple[bool, str]] = []
        target = requested_tier or "high_quality"
        for row in rows:
            candidate = CatalogModel(row)
            candidate_profile = build_catalog_call_profile(candidate)
            tts = candidate_profile.offering_metadata.get("tts", {})
            tiers = tts.get("quality_tiers", ()) if isinstance(tts, dict) else ()
            if isinstance(tiers, str):
                tiers = (tiers,)
            if (
                candidate_profile.vendor == profile.vendor
                and target in tiers
                and candidate_profile.capabilities.produces_audio
                and not candidate_profile.capabilities.produces_text
                and not candidate_profile.model_is_deprecated
            ):
                candidates.append((not bool(tts.get("is_default")), candidate_profile.model_name))
        if not candidates:
            raise CatalogRoutingError(
                f"Host model_catalog has no TTS model for vendor={profile.vendor!r}, "
                f"quality={target!r}. Add a model dict with tts.quality_tiers."
            )
        candidates.sort()
        rerouted = await resolve_call_profile(candidates[0][1])
        return _mark_tts_reroute(profile, rerouted, requested_tier)

    manager = ai_catalog_manager
    await manager.ensure_loaded()
    selected = manager.tts_offering(profile.vendor, requested_tier)
    if selected is None:
        reason = "deprecated model" if profile.model_is_deprecated else f"quality={requested_tier!r}"
        vcprint(
            f"TTS catalog cannot route {reason} for vendor '{profile.vendor}'. Seed "
            "ai.offering.metadata.tts.quality_tiers/is_default; no code fallback exists.",
            title="🚨 TTS CATALOG RESOLUTION FAILURE",
            color="red",
        )
        raise CatalogRoutingError(
            f"No catalog TTS offering for vendor={profile.vendor!r}, "
            f"quality={requested_tier or 'high_quality'!r}"
        )
    if selected.id == profile.offering_id:
        return profile
    rerouted = await resolve_call_profile(str(selected.model_id), offering_id=selected.id)
    return _mark_tts_reroute(profile, rerouted, requested_tier)


def resolve_tts_voice(profile: ResolvedCallProfile, requested: str | None) -> str:
    """Resolve one provider voice from the model-linked ``ai.voices`` catalog."""
    voice = (requested or "").strip()
    if voice and voice in profile.tts_voice_ids:
        return voice
    if voice:
        raise CatalogRoutingError(
            f"TTS voice {voice!r} is not available for model {profile.model_name!r} "
            f"(vendor={profile.vendor!r}). Select a model-linked ai.voices entry."
        )
    if profile.tts_default_voice_id:
        return profile.tts_default_voice_id
    raise CatalogRoutingError(
        f"No catalog voice is resolvable for model {profile.model_name!r}. "
        "Seed enabled ai.voices rows with metadata.models and exactly one "
        "metadata.default_for_models entry; no code fallback exists."
    )


def validate_tts_voices(
    profile: ResolvedCallProfile,
    requested: list[str] | tuple[str, ...],
) -> None:
    """Validate every explicit multi-speaker voice without collapsing speakers."""
    for voice in requested:
        resolve_tts_voice(profile, voice)


__all__ = [
    "client_attr_for_wire_format",
    "resolve_call_profile",
    "resolve_tts_call_profile",
    "resolve_tts_voice",
    "select_tts_default_voice",
    "validate_tts_voices",
]
