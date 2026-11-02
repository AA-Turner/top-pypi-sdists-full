"""Preferences resolver — merges built-ins → user prefs → recipes.

The dispatcher calls ``resolve_settings`` once per pipeline run. Host injects
a ``PrefsStoreProtocol`` implementation that reads the user_analysis_preferences
and analysis_recipes tables.
"""

from __future__ import annotations

from typing import Any, Protocol

from .context import ResolvedSettings
from .registry import get_specs_for_mime


class PrefsStoreProtocol(Protocol):
    async def load_user_preferences(self, user_id: str) -> dict[str, Any] | None: ...

    async def load_matching_recipes(
        self,
        *,
        user_id: str,
        mime_type: str,
        classification_hint: str | None,
        filename: str | None,
    ) -> list[dict[str, Any]]: ...

    async def load_pattern_catalog(self) -> list[dict[str, Any]]:
        """Built-in + code-shipped pattern catalog. Hosts can override."""
        ...


# ── default in-process implementation (used standalone) ───────────────────────

class _BuiltinOnlyPrefsStore:
    """Fallback when no host store is injected — uses built-ins only."""

    async def load_user_preferences(self, user_id: str) -> dict[str, Any] | None:
        return None

    async def load_matching_recipes(self, **kwargs: Any) -> list[dict[str, Any]]:
        return []

    async def load_pattern_catalog(self) -> list[dict[str, Any]]:
        # Lazy import so the analysis package stays loadable without PDF deps.
        try:
            from ..specific_handlers.pdf.redact.patterns import get_pattern_catalog
            return get_pattern_catalog()
        except Exception:
            return []


_DEFAULT_STORE = _BuiltinOnlyPrefsStore()


async def resolve_settings(
    *,
    user_id: str,
    mime_type: str,
    classification_hint: str | None = None,
    filename: str | None = None,
    inline_payload_limit_bytes: int = 256 * 1024,
    ocr_provider_id: str = "tesseract",
    store: PrefsStoreProtocol | None = None,
) -> ResolvedSettings:
    """Build the final settings the dispatcher will execute."""
    store = store or _DEFAULT_STORE  # type: ignore[assignment]

    specs = get_specs_for_mime(mime_type)
    enabled = {s.kind for s in specs}
    tiers = {s.kind: tuple(s.tiers) for s in specs}
    params = {s.kind: dict(s.params) for s in specs}

    pattern_catalog = await store.load_pattern_catalog()
    user_prefs = await store.load_user_preferences(user_id) or {}
    recipes = await store.load_matching_recipes(
        user_id=user_id,
        mime_type=mime_type,
        classification_hint=classification_hint,
        filename=filename,
    )

    # ── apply user prefs ──────────────────────────────────────────────────
    per_detector_enabled = user_prefs.get("per_detector_enabled") or {}
    for kind, on in per_detector_enabled.items():
        if not on and kind in enabled:
            enabled.discard(kind)
        elif on and kind not in enabled and kind in tiers:
            enabled.add(kind)

    user_tier_defaults = user_prefs.get("default_tier_per_detector") or {}
    for kind, t in user_tier_defaults.items():
        if kind in tiers:
            tiers[kind] = (t,)  # collapse to single chosen tier when user picks

    custom_patterns = user_prefs.get("custom_patterns") or []
    if isinstance(custom_patterns, list):
        pattern_catalog = list(pattern_catalog) + list(custom_patterns)

    default_redaction_mode = user_prefs.get("default_redaction_mode") or "reversible"
    substitute_formats = dict(user_prefs.get("substitute_formats") or {})

    # ── apply per-file-type overrides ─────────────────────────────────────
    per_type = (user_prefs.get("per_file_type_overrides") or {}).get(mime_type) or {}
    for kind, on in (per_type.get("per_detector_enabled") or {}).items():
        if not on:
            enabled.discard(kind)
    for kind, t in (per_type.get("default_tier_per_detector") or {}).items():
        if kind in tiers:
            tiers[kind] = (t,)

    # ── apply recipes (most-specific last so they win) ────────────────────
    # store returns ordered list: user-scoped → team → account
    for recipe in recipes:
        for kind, on in (recipe.get("detector_overrides") or {}).items():
            if isinstance(on, bool):
                if not on:
                    enabled.discard(kind)
                else:
                    enabled.add(kind)
            elif isinstance(on, dict):
                # {enabled: bool, params: {...}, tiers: [...]}
                if on.get("enabled") is False:
                    enabled.discard(kind)
                elif on.get("enabled") is True:
                    enabled.add(kind)
                if "tiers" in on and kind in tiers:
                    tiers[kind] = tuple(on["tiers"])
                if "params" in on and kind in params:
                    params[kind].update(on["params"])
        pattern_overrides = recipe.get("pattern_overrides") or {}
        for pid in pattern_overrides.get("disabled_ids") or []:
            pattern_catalog = [p for p in pattern_catalog if p.get("id") != pid]
        for added in pattern_overrides.get("added") or []:
            pattern_catalog.append(added)
        if recipe.get("redaction_mode"):
            default_redaction_mode = recipe["redaction_mode"]
        if recipe.get("substitute_formats"):
            substitute_formats.update(recipe["substitute_formats"])

    return ResolvedSettings(
        enabled_detectors=enabled,
        detector_tiers=tiers,
        detector_params=params,
        pattern_catalog=pattern_catalog,
        default_redaction_mode=default_redaction_mode,
        substitute_formats=substitute_formats,
        inline_payload_limit_bytes=inline_payload_limit_bytes,
        ocr_provider_id=ocr_provider_id,
    )


__all__ = ["PrefsStoreProtocol", "resolve_settings"]
