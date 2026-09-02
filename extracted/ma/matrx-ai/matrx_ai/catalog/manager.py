"""AiCatalogManager — loads and compiles the ai.endpoint / ai.api / ai.offering /
ai.setting catalog (+ the ai.model_alias routing map).

Every rules blob is COMPILED + VALIDATED at load:
  • ``extra="forbid"`` on rules AND the {params, constraints} envelope
    (an unknown field is a data bug),
  • every rule key must exist in ``ai.setting``,
  • every ``processor`` name must be registered (catalog/processors.py),
  • ``value_map`` keys ⊆ ``setting.canonical_values`` for enum settings,
  • clamp bounds within the setting's canonical range,
  • ``api.translator_key`` must be a known UnifiedAIClient endpoint attr
    or a registered specialized execution route.

A row failing compilation is QUARANTINED (treated unavailable) with a red
vcprint banner and a module-level quarantine record the host can inspect —
never a process crash, never a silently-served bad row.

``resolve_model_ref(ref)`` is the ONE instant name-routing seam: it resolves a
model reference (id, name, or ai.model_alias alias) to the canonical model id.
Retry routing will grow here later — keep it a single function.
"""

from __future__ import annotations

import asyncio
from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict

from matrx_ai.catalog.controls import (
    CompiledControlsMap,
    compile_controls,
    validate_rules_against_settings,
)
from matrx_ai.catalog.models import (
    CatalogApi,
    CatalogEndpoint,
    CatalogOffering,
    CatalogSetting,
    CatalogVoice,
)
from matrx_ai.catalog.routes import SPECIAL_WIRE_FORMATS
from matrx_ai.db._registry import DBNotConfiguredError, get_model
from matrx_ai.providers.unified_client import UnifiedAIClient

# ── wire formats ─────────────────────────────────────────────────────────────
# ai.api.translator_key is the SAME token as the UnifiedAIClient dispatch attr
# (openai_chat, google_image, ...) or a registered specialized execution route
# (extraction, realtime, embeddings) that intentionally bypasses turn dispatch.
WIRE_FORMATS: frozenset[str] = (
    frozenset(UnifiedAIClient._PROVIDER_FACTORIES)
    | {UnifiedAIClient._GENERIC_OPENAI_CLIENT_ATTR}
    | SPECIAL_WIRE_FORMATS
)


class QuarantineRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: Literal["endpoint", "api", "offering", "setting", "alias"]
    row_id: str
    name: str
    errors: tuple[str, ...]


# Host-visible ledger of every quarantined row (reset on each reload).
QUARANTINED_ROWS: list[QuarantineRecord] = []


class CatalogCounts(BaseModel):
    """Served-state counts after a load/reload — the admin reload endpoint's
    summary source (aidream/services/ai_catalog/reload.py)."""

    model_config = ConfigDict(frozen=True)

    endpoints: int
    apis: int
    offerings: int
    settings: int
    providers: int
    models: int
    aliases: int
    quarantined: int


def _quarantine(
    kind: Literal["endpoint", "api", "offering", "setting", "alias"],
    row_id: str,
    name: str,
    errors: list[str],
) -> None:
    record = QuarantineRecord(kind=kind, row_id=row_id, name=name, errors=tuple(errors))
    QUARANTINED_ROWS.append(record)
    detail = "\n".join(f"    ● {e}" for e in errors)
    vcprint(
        f"ai.{kind} '{name}' ({row_id}) failed catalog compilation and is QUARANTINED "
        f"(treated unavailable) on {len(errors)} error(s):\n{detail}\n"
        f"  Fix the row in the ai schema; the rest of the catalog keeps serving. "
        f"This is LOUD but NON-FATAL.",
        title="🚨 AI CATALOG QUARANTINE",
        color="red",
    )


def _row_value(row: Any, field: str, default: Any = None) -> Any:
    value = getattr(row, field, default)
    return default if value is None else value


class AiCatalogManager:
    _instance: AiCatalogManager | None = None

    def __new__(cls) -> AiCatalogManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self._settings: dict[str, CatalogSetting] = {}
        self._endpoints: dict[str, CatalogEndpoint] = {}
        self._apis: dict[str, CatalogApi] = {}
        self._offerings: dict[str, CatalogOffering] = {}
        self._offerings_by_model: dict[str, list[CatalogOffering]] = {}
        self._voices_by_provider: dict[str, tuple[CatalogVoice, ...]] = {}
        self._model_state: dict[str, dict[str, Any]] = {}
        self._providers: dict[str, str] = {}  # provider id -> name
        self._compiled: dict[tuple[str, str], CompiledControlsMap] = {}
        # Name routing: model id set + name -> id + alias -> id (ai.model_alias).
        self._model_ids: frozenset[str] = frozenset()
        self._model_names: dict[str, str] = {}
        self._aliases: dict[str, str] = {}
        self._loaded = False
        self._load_lock = asyncio.Lock()

    # ── loading ──────────────────────────────────────────────────────────────
    async def ensure_loaded(self) -> None:
        if self._loaded:
            return
        async with self._load_lock:
            if not self._loaded:
                await self.reload()

    async def reload(self) -> None:
        AiEndpoint = get_model("AiEndpoint")
        AiApi = get_model("AiApi")
        AiOffering = get_model("AiOffering")
        AiSetting = get_model("AiSetting")

        endpoint_rows = await AiEndpoint.filter(deleted_at=None).all()
        api_rows = await AiApi.filter(deleted_at=None).all()
        offering_rows = await AiOffering.filter(deleted_at=None).all()
        setting_rows = await AiSetting.filter(deleted_at=None).all()

        providers: dict[str, str] = {}
        try:
            AiProvider = get_model("AiProvider")
            for row in await AiProvider.filter(deleted_at=None).all():
                providers[str(row.id)] = getattr(row, "name", "") or ""
        except DBNotConfiguredError:
            pass  # provider names degrade to the legacy model.provider varchar

        # Name-routing map: model ids + names (ai.model_definition) and aliases
        # (ai.model_alias) feed resolve_model_ref.
        models: list[dict[str, Any]] = []
        try:
            AiModel = get_model("AiModel")
            models = [
                {
                    "id": str(row.id),
                    "name": getattr(row, "name", "") or "",
                    "is_deprecated": bool(getattr(row, "is_deprecated", False) or False),
                    "is_primary": bool(getattr(row, "is_primary", False) or False),
                }
                for row in await AiModel.filter(deleted_at=None).all()
            ]
        except DBNotConfiguredError:
            pass

        aliases: list[dict[str, Any]] = []
        try:
            AiModelAlias = get_model("AiModelAlias")
            aliases = [self._alias_dict(r) for r in await AiModelAlias.filter(deleted_at=None).all()]
        except DBNotConfiguredError:
            pass

        voices: list[dict[str, Any]] = []
        try:
            Voices = get_model("Voices")
            voices = [
                self._voice_dict(row)
                for row in await Voices.filter(enabled=True, deleted_at=None).all()
            ]
        except DBNotConfiguredError:
            pass
        except Exception as exc:  # noqa: BLE001 — non-TTS routes keep serving
            vcprint(
                f"[catalog] ai.voices load failed ({exc!r}); TTS voice resolution "
                "will fail loudly, other catalog routes remain available.",
                color="red",
            )

        self.load_from_rows(
            endpoints=[self._endpoint_dict(r) for r in endpoint_rows],
            apis=[self._api_dict(r) for r in api_rows],
            offerings=[self._offering_dict(r) for r in offering_rows],
            settings=[self._setting_dict(r) for r in setting_rows],
            providers=providers,
            models=models,
            aliases=aliases,
            voices=voices,
        )

    @staticmethod
    def _endpoint_dict(row: Any) -> dict[str, Any]:
        return {
            "id": str(row.id),
            # NOT _row_value: a missing/NULL vendor must reach Pydantic as None so the
            # required field REJECTS the row into quarantine. Defaulting it to "" would
            # silently bill that endpoint's usage under an empty vendor.
            "vendor": getattr(row, "vendor", None),
            "internal_name": _row_value(row, "internal_name", ""),
            "display_name": _row_value(row, "display_name", ""),
            "base_url": getattr(row, "base_url", None),
            "auth_ref": _row_value(row, "auth_ref", {}),
            "byok_secret_key": getattr(row, "byok_secret_key", None),
            "priority": _row_value(row, "priority", 100),
            "is_active": _row_value(row, "is_active", True),
        }

    @staticmethod
    def _api_dict(row: Any) -> dict[str, Any]:
        return {
            "id": str(row.id),
            "name": _row_value(row, "name", ""),
            "display_name": _row_value(row, "display_name", ""),
            "translator_key": _row_value(row, "translator_key", ""),
            "transport": _row_value(row, "transport", "sdk"),
            "rules": _row_value(row, "rules", {"params": {}, "constraints": []}),
            "request_defaults": _row_value(row, "request_defaults", {}),
            "description": getattr(row, "description", None),
        }

    @staticmethod
    def _offering_dict(row: Any) -> dict[str, Any]:
        return {
            "id": str(row.id),
            "model_id": str(_row_value(row, "model_id", "")),
            "endpoint_id": str(_row_value(row, "endpoint_id", "")),
            "api_id": str(_row_value(row, "api_id", "")),
            "provider_model_id": _row_value(row, "provider_model_id", ""),
            "priority": _row_value(row, "priority", 100),
            "is_available": _row_value(row, "is_available", True),
            "pricing": getattr(row, "pricing", None),
            "usage_basis": getattr(row, "usage_basis", None),
            "token_billed": _row_value(row, "token_billed", False),
            "capabilities_override": _row_value(row, "capabilities_override", {}),
            "override": _row_value(row, "override", {"params": {}, "constraints": []}),
            "metadata": _row_value(row, "metadata", {}),
        }

    @staticmethod
    def _voice_dict(row: Any) -> dict[str, Any]:
        return {
            "provider": _row_value(row, "provider", ""),
            "provider_voice_id": _row_value(row, "provider_voice_id", ""),
            "name": _row_value(row, "name", ""),
            "gender": _row_value(row, "gender", None),
            "sort_order": _row_value(row, "sort_order", 0),
            "metadata": _row_value(row, "metadata", {}),
        }

    @staticmethod
    def _setting_dict(row: Any) -> dict[str, Any]:
        return {
            "key": _row_value(row, "key", ""),
            "value_type": _row_value(row, "value_type", ""),
            "canonical_min": getattr(row, "canonical_min", None),
            "canonical_max": getattr(row, "canonical_max", None),
            "canonical_values": getattr(row, "canonical_values", None),
            "default_value": getattr(row, "default_value", None),
            "ui": _row_value(row, "ui", {}),
            "description": getattr(row, "description", None),
        }

    @staticmethod
    def _alias_dict(row: Any) -> dict[str, Any]:
        return {
            "id": str(row.id),
            "alias": _row_value(row, "alias", ""),
            "model_id": str(_row_value(row, "model_id", "")),
            "kind": _row_value(row, "kind", "alias"),
        }

    def load_from_rows(
        self,
        *,
        endpoints: list[dict[str, Any]],
        apis: list[dict[str, Any]],
        offerings: list[dict[str, Any]],
        settings: list[dict[str, Any]],
        providers: dict[str, str] | None = None,
        models: list[dict[str, Any]] | None = None,
        aliases: list[dict[str, Any]] | None = None,
        voices: list[dict[str, Any]] | None = None,
    ) -> None:
        """Compile + validate raw row dicts into the served catalog (sync, pure).

        The seam unit tests and ``reload()`` share — fixture rows in tests, live
        rows in production. Replaces the entire served state atomically at the end.
        """
        QUARANTINED_ROWS.clear()

        # Voice GENDER is load-bearing for tts_voice equivalence (THE LAW, rule
        # 5): male -> male, female -> female, never crossed. Built here — before
        # offerings compile — so every CompiledControlsMap can resolve a voice
        # without the pure control layer ever touching a database.
        voice_genders: dict[str, str] = {}
        for raw in voices or []:
            token = str(raw.get("provider_voice_id") or "").strip().lower()
            gender = raw.get("gender")
            if token and gender:
                voice_genders[token] = str(gender).strip().lower()

        parsed_settings: dict[str, CatalogSetting] = {}
        for raw in settings:
            key = str(raw.get("key") or "<missing-key>")
            try:
                parsed_settings[key] = CatalogSetting.model_validate(raw)
            except Exception as exc:  # noqa: BLE001 — quarantine, never crash
                _quarantine("setting", key, key, [str(exc)])

        parsed_endpoints: dict[str, CatalogEndpoint] = {}
        for raw in endpoints:
            row_id = str(raw.get("id") or "<missing-id>")
            name = str(raw.get("vendor") or raw.get("internal_name") or row_id)
            errors: list[str] = []
            try:
                endpoint = CatalogEndpoint.model_validate(raw)
            except Exception as exc:  # noqa: BLE001
                _quarantine("endpoint", row_id, name, [str(exc)])
                continue
            if not endpoint.vendor.strip():
                # NOT NULL doesn't stop ''. An empty vendor silently merges this
                # endpoint's cost into the "" bucket — exactly the bug
                # ai.endpoint.vendor exists to prevent.
                errors.append("empty vendor — ai.endpoint.vendor is the cost-grouping fact")
            if errors:
                _quarantine("endpoint", row_id, name, errors)
                continue
            parsed_endpoints[endpoint.id] = endpoint

        parsed_apis: dict[str, CatalogApi] = {}
        for raw in apis:
            row_id = str(raw.get("id") or "<missing-id>")
            name = str(raw.get("name") or raw.get("translator_key") or row_id)
            errors = []
            try:
                api = CatalogApi.model_validate(raw)
            except Exception as exc:  # noqa: BLE001
                _quarantine("api", row_id, name, [str(exc)])
                continue
            if api.translator_key not in WIRE_FORMATS:
                errors.append(
                    f"unknown translator_key '{api.translator_key}' — not a UnifiedAIClient "
                    f"dispatch attr or special ({sorted(SPECIAL_WIRE_FORMATS)})"
                )
            errors.extend(validate_rules_against_settings(api.rules.params, parsed_settings))
            if errors:
                _quarantine("api", row_id, name, errors)
                continue
            parsed_apis[api.id] = api

        parsed_offerings: dict[str, CatalogOffering] = {}
        by_model: dict[str, list[CatalogOffering]] = {}
        compiled: dict[tuple[str, str], CompiledControlsMap] = {}
        for raw in offerings:
            row_id = str(raw.get("id") or "<missing-id>")
            name = str(raw.get("provider_model_id") or row_id)
            try:
                offering = CatalogOffering.model_validate(raw)
            except Exception as exc:  # noqa: BLE001
                _quarantine("offering", row_id, name, [str(exc)])
                continue
            endpoint = parsed_endpoints.get(offering.endpoint_id)
            api = parsed_apis.get(offering.api_id)
            missing: list[str] = []
            if endpoint is None:
                missing.append(
                    f"endpoint '{offering.endpoint_id}' is missing or quarantined"
                )
            if api is None:
                missing.append(f"api '{offering.api_id}' is missing or quarantined")
            if missing:
                _quarantine(
                    "offering",
                    row_id,
                    name,
                    [m + " — offering treated unavailable" for m in missing],
                )
                continue
            errors = validate_rules_against_settings(offering.override.params, parsed_settings)
            if errors:
                _quarantine("offering", row_id, name, errors)
                continue
            try:
                compiled[(offering.api_id, offering.id)] = compile_controls(
                    api.rules.params,
                    offering.override.params,
                    settings=parsed_settings,
                    voice_genders=voice_genders,
                )
            except Exception as exc:  # noqa: BLE001
                _quarantine("offering", row_id, name, [f"controls compilation failed: {exc}"])
                continue
            parsed_offerings[offering.id] = offering
            by_model.setdefault(offering.model_id, []).append(offering)

        voices_by_provider: dict[str, list[CatalogVoice]] = {}
        for raw in voices or []:
            try:
                voice = CatalogVoice.model_validate(raw)
            except Exception as exc:  # noqa: BLE001 — a bad voice cannot poison routing
                vcprint(
                    f"[catalog] ignored invalid ai.voices row: {exc}",
                    color="red",
                )
                continue
            voices_by_provider.setdefault(voice.provider.strip().lower(), []).append(voice)
        for provider_voices in voices_by_provider.values():
            provider_voices.sort(key=lambda item: (item.sort_order, item.provider_voice_id))

        for model_offerings in by_model.values():
            model_offerings.sort(key=lambda o: o.priority)

        # Name routing — model ids/names + ai.model_alias rows. Every alias kind
        # (alias / deprecated / latest) resolves identically at lookup.
        model_ids: set[str] = set()
        model_names: dict[str, str] = {}
        for m in models or []:
            mid = str(m.get("id") or "")
            mname = str(m.get("name") or "")
            if mid:
                model_ids.add(mid)
            # A DEPRECATED model keeps its id slot (history/read paths resolve
            # by id) but SURRENDERS the name slot, so an ai.model_alias row —
            # kind='deprecated', written when a duplicate row is merged into
            # its canonical (ai_038) — can redirect the name to the canonical
            # model. A deprecated name with no alias falls through unchanged
            # and the ORM loader still finds the row by name, so un-aliased
            # deprecated models behave exactly as before.
            if mid and mname and not m.get("is_deprecated"):
                model_names[mname] = mid

        alias_map: dict[str, str] = {}
        for raw in aliases or []:
            alias = str(raw.get("alias") or "").strip()
            model_id = str(raw.get("model_id") or "").strip()
            if not alias or not model_id:
                _quarantine(
                    "alias",
                    str(raw.get("id") or "<missing-id>"),
                    alias or "<missing-alias>",
                    ["ai.model_alias row missing alias or model_id"],
                )
                continue
            alias_map[alias] = model_id

        self._settings = parsed_settings
        self._endpoints = parsed_endpoints
        self._apis = parsed_apis
        self._offerings = parsed_offerings
        self._offerings_by_model = by_model
        self._voices_by_provider = {
            provider: tuple(items) for provider, items in voices_by_provider.items()
        }
        self._model_state = {
            str(model.get("id")): dict(model) for model in (models or []) if model.get("id")
        }
        self._providers = dict(providers or {})
        self._compiled = compiled
        self._model_ids = frozenset(model_ids)
        self._model_names = model_names
        self._aliases = alias_map
        self._loaded = True

    # ── reads ────────────────────────────────────────────────────────────────
    def offerings_for(self, model_id: str) -> list[CatalogOffering]:
        """Available offerings for a model, priority-ordered, quarantined rows excluded."""
        candidates = self._offerings_by_model.get(str(model_id), [])
        return [
            o
            for o in candidates
            if o.is_available
            and (ep := self._endpoints.get(o.endpoint_id)) is not None
            and ep.is_active
            and o.api_id in self._apis
        ]

    def endpoint(self, endpoint_id: str) -> CatalogEndpoint | None:
        return self._endpoints.get(str(endpoint_id))

    def api(self, api_id: str) -> CatalogApi | None:
        return self._apis.get(str(api_id))

    def offering(self, offering_id: str) -> CatalogOffering | None:
        return self._offerings.get(str(offering_id))

    def model_state(self, model_id: str) -> dict[str, Any]:
        return dict(self._model_state.get(str(model_id), {}))

    def tts_offering(self, vendor: str, quality: str | None) -> CatalogOffering | None:
        target = (quality or "high_quality").strip().lower()
        candidates: list[CatalogOffering] = []
        for offering in self._offerings.values():
            endpoint = self._endpoints.get(offering.endpoint_id)
            if endpoint is None or endpoint.vendor != vendor or not endpoint.is_active:
                continue
            if not offering.is_available:
                continue
            tts = offering.metadata.get("tts")
            if not isinstance(tts, dict):
                continue
            tiers = tts.get("quality_tiers", ())
            if isinstance(tiers, str):
                tiers = (tiers,)
            if target in tiers:
                candidates.append(offering)
        candidates.sort(
            key=lambda item: (
                not bool(item.metadata.get("tts", {}).get("is_default")),
                item.priority,
            )
        )
        return candidates[0] if candidates else None

    def tts_voices(self, vendor: str, model_name: str) -> tuple[CatalogVoice, ...]:
        matched: list[CatalogVoice] = []
        for voice in self._voices_by_provider.get(vendor.strip().lower(), ()):
            models = voice.metadata.get("models", ())
            if isinstance(models, str):
                models = (models,)
            if model_name in models or "*" in models:
                matched.append(voice)
        return tuple(matched)

    def setting(self, key: str) -> CatalogSetting | None:
        return self._settings.get(key)

    def settings(self) -> dict[str, CatalogSetting]:
        return dict(self._settings)

    def provider_name(self, provider_id: str | None) -> str | None:
        if provider_id is None:
            return None
        return self._providers.get(str(provider_id))

    def resolve_model_ref(self, ref: str) -> str:
        """Resolve a model reference to the canonical model id — id, then name,
        then ai.model_alias (any kind). Unknown refs return unchanged so the
        model loader raises its own loud error. The ONE routing map — retry
        routing grows here later."""
        key = str(ref).strip()
        if key in self._model_ids:
            return key
        by_name = self._model_names.get(key)
        if by_name is not None:
            return by_name
        by_alias = self._aliases.get(key)
        if by_alias is not None:
            return by_alias
        return key

    def counts(self) -> CatalogCounts:
        return CatalogCounts(
            endpoints=len(self._endpoints),
            apis=len(self._apis),
            offerings=len(self._offerings),
            settings=len(self._settings),
            providers=len(self._providers),
            models=len(self._model_ids),
            aliases=len(self._aliases),
            quarantined=len(QUARANTINED_ROWS),
        )

    def compiled_controls(self, api_id: str, offering_id: str) -> CompiledControlsMap:
        cached = self._compiled.get((str(api_id), str(offering_id)))
        if cached is not None:
            return cached
        # An offering that never compiled (or an unknown pair) gets pure passthrough —
        # reachable only if a caller bypasses offerings_for(), which excludes quarantined rows.
        return CompiledControlsMap(rules={})

    def export_model_routing(self, model_id: str) -> dict[str, Any] | None:
        """Serialize a model's primary offering routing facts for client hosts.

        Returns ``{"wire_format": <translator_key>, "control_rules": {key: rule_dict}}``
        for the model's highest-priority available offering, or None when the
        model has no usable offering. The rules are the SAME api ⊕ offering
        merge the server's own ``resolve_call_profile`` uses — client hosts
        (matrx-local) consume this from the model-catalog payload so their
        param shaping never diverges from the DB (the hardcoded per-wire
        fallback in ``host_catalog`` once sent budget-mode thinking to
        adaptive-only Anthropic models: a guaranteed 400).
        """
        offerings = self.offerings_for(str(model_id))
        if not offerings:
            return None
        offering = offerings[0]
        api = self._apis.get(offering.api_id)
        if api is None:
            return None
        compiled = self.compiled_controls(offering.api_id, offering.id)
        return {
            "wire_format": api.translator_key,
            "control_rules": {
                key: rule.model_dump(exclude_none=True)
                for key, rule in compiled.rules.items()
            },
        }


ai_catalog_manager = AiCatalogManager()

__all__ = [
    "WIRE_FORMATS",
    "SPECIAL_WIRE_FORMATS",
    "CatalogCounts",
    "QuarantineRecord",
    "QUARANTINED_ROWS",
    "AiCatalogManager",
    "ai_catalog_manager",
]
