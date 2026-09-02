"""Typed shapes for the AI catalog (ai.endpoint / ai.api / ai.offering / ai.setting).

These models parse the LOCKED rule contract the catalog seeder writes. Control
rules ride in an ENVELOPE — ``{"params": {<canonical_key>: ControlRule>}, "constraints": []}``:

    api.rules["params"] / offering.override["params"] :: Record<canonical_key, ControlRule>
    ControlRule = {
        "provider_key": "dotted.path.or.flat"?,   # rename; default = same key
        "value_map":   {canonical -> provider}?,  # null result = OMIT the key
        "to_default":  [canonical values]?,       # THE EXPLICIT DEFAULT DECLARATION (RULE 3):
                                                  # canonical values that DELIBERATELY resolve to
                                                  # this offering's `default` rather than being
                                                  # converted or dropped. This is the ONLY way to
                                                  # express "this value should resolve to the
                                                  # model's default" as a DECLARED decision — it
                                                  # must never be indistinguishable from a lookup
                                                  # miss, and it must never be the norm. Takes
                                                  # PRECEDENCE over value_map/on_unmapped: a
                                                  # declared decision beats an inferred conversion.
                                                  # Resolves to `default` when one is set, else the
                                                  # key is omitted. Recorded as
                                                  # Adjustment(action="to_default", expected=True)
                                                  # — a DECLARED default is not a surprise, so it
                                                  # stays silent to the client (see
                                                  # providers/outbound_params.py::warn_client_about_dropped_settings).
                                                  # Members must be canonical_values of the setting
                                                  # (like ui_values) and must NOT also appear in
                                                  # value_map — that combination is ambiguous data
                                                  # and is rejected at validation.
                                                  # See
                                                  # /home/user/matrx-common-docs/systems/platform/configuration-equivalence/FEATURE.md
        "on_unmapped": "drop" | "nearest" | "error" (default "nearest"),
                                                  # a value_map MISS: DEFAULT is "nearest" —
                                                  # snap to the nearest MAPPED value in the
                                                  # ai.setting canonical_values order (ties
                                                  # break toward the LATER position); "drop"
                                                  # (loud) is an EXPLICIT, non-default choice —
                                                  # permitted only when the target genuinely
                                                  # lacks the capability, never the norm; or
                                                  # raise. THE EQUIVALENCE LAW: an offering that
                                                  # claims a setting must convert every canonical
                                                  # value for it — silently dropping is a severe
                                                  # defect. See
                                                  # /home/user/matrx-common-docs/systems/platform/configuration-equivalence/FEATURE.md
        "clamp":       {"min": n?, "max": n?}?,   # numeric clamp
        "supported":   bool (default true),       # false = drop key entirely
        "default":     <provider value applied when canonical value unset>?,
        "send_when_unset": bool (default false),  # strengthens `default`: ALSO backfill the
                                                  # default when a SET value was eliminated
                                                  # (value_map->null omit / on_unmapped drop),
                                                  # guaranteeing the provider key is always sent.
                                                  # `default` alone keeps today's semantics:
                                                  # fill only when the canonical key is unset.
        "const":       <always send this provider value, ignoring any incoming value>?,
        "processor":   "registered_processor_name"?,  # escape hatch — the named code fn
                                                  # (catalog/processors.py) owns this key's
                                                  # translation entirely; exclusive with
                                                  # value_map/const. clamp COMPOSES with a
                                                  # processor: the canonical value is clamped
                                                  # (pass 2, with an Adjustment) BEFORE the
                                                  # processor runs — so DB rules can carry the
                                                  # provider's numeric range for a
                                                  # processor-owned key (ai_038)
        "processor_config": {...}?,               # per-rule data for the processor; reserved
                                                  # engine keys: "order" (int, pass-2 run order,
                                                  # default 100), "consumes" (canonical keys the
                                                  # processor consumes — skipped by scalar pass)
        "ui_values":   [canonical values]?,       # THE SUPPORTED VOCABULARY (ai_041): the exact
                                                  # enum options this model/key accepts — the
                                                  # model's NATIVE vocabulary plus the house
                                                  # values ("auto" = leave unset, "none" = send
                                                  # nothing). It is what the settings UI offers
                                                  # AND what outbound ENFORCES: a canonical value
                                                  # outside this set is reconciled to the nearest
                                                  # supported one (Adjustment
                                                  # action="unsupported_value"), never forwarded
                                                  # to the provider. Inbound never reads it.
                                                  # Without it, the DB
                                                  # resolver (ai.resolve_model_config) derives
                                                  # options from the IDENTITY entries of
                                                  # value_map (k -> k); non-identity entries
                                                  # (xhigh -> high) are translation-compat only
                                                  # and NEVER shown to users.
    }

Effective rule per key = deep-merge per FIELD:
    implicit passthrough  <-  api.rules["params"][key]  <-  offering.override["params"][key]
(offering wins per field). ``extra="forbid"`` on every rule AND on the envelope —
an unknown field is a data bug and quarantines the row at load (see
``manager.py``), never a silent passthrough.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, RootModel, model_validator

from matrx_ai.providers.resolved_capabilities import ResolvedModelCapabilities

if TYPE_CHECKING:  # circular-by-design: controls.py imports ControlRule from here.
    from matrx_ai.catalog.controls import CompiledControlsMap

SettingValueType = Literal[
    "number", "integer", "boolean", "string", "enum", "string_array", "object"
]

AliasKind = Literal["alias", "deprecated", "latest"]

ApiTransport = Literal["sdk", "http", "websocket"]


class ClampSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    min: float | None = None
    max: float | None = None


class ControlRule(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    provider_key: str | None = None
    value_map: dict[str, Any] | None = None
    # THE EXPLICIT DEFAULT DECLARATION (Rule 3, module docstring). Canonical
    # values in this list resolve to `default` (or omit, if no default) rather
    # than through value_map/on_unmapped — a declared decision, never a miss.
    to_default: list[Any] | None = None
    on_unmapped: Literal["drop", "nearest", "error"] = "nearest"
    clamp: ClampSpec | None = None
    supported: bool = True
    default: Any = None
    send_when_unset: bool = False
    const: Any = None
    processor: str | None = None
    processor_config: dict[str, Any] = {}
    # UI-only vocabulary (see module docstring). Never read by outbound/inbound.
    ui_values: list[Any] | None = None

    @model_validator(mode="after")
    def _validate_field_combos(self) -> ControlRule:
        # A processor owns its key's translation — a rule that also carries a
        # VALUE-REWRITING scalar transform (value_map/const) is ambiguous data
        # and must fail loudly. clamp is NOT ambiguous: it is a numeric range
        # constraint applied to the canonical value BEFORE the processor runs
        # (controls.py pass 2), letting DB rules express the provider's real
        # range (and the DB-side ai.resolve_model_config UI resolver read it)
        # for processor-owned keys like anthropic temperature (ai_038).
        if self.processor is not None:
            conflicts = [
                name
                for name, value in (
                    ("value_map", self.value_map),
                    ("const", self.const),
                )
                if value is not None
            ]
            if conflicts:
                raise ValueError(
                    f"processor={self.processor!r} is exclusive with {conflicts} — "
                    "a processor owns the key's translation entirely; remove the scalar fields"
                )
        elif self.processor_config:
            raise ValueError("processor_config requires processor to be set")
        # const ignores the incoming value, so a transform of that value is dead data.
        if self.const is not None and (self.value_map is not None or self.clamp is not None):
            raise ValueError(
                "const is exclusive with value_map/clamp — const ignores the incoming value"
            )
        return self


# The implicit rule for any canonical key with no api/offering entry:
# pass the key through untouched under its own name.
PASSTHROUGH_RULE = ControlRule()


AdjustmentAction = Literal[
    "dropped",
    "omitted",
    "mapped",
    "clamped",
    "const",
    "effort_ceiling",
    "unsupported_value",
    # THE EXPLICIT DEFAULT DECLARATION (Rule 3) fired: the canonical value was
    # listed in `to_default` and DELIBERATELY resolved to this offering's
    # default rather than being converted or dropped. Greppable and visibly
    # distinct from `mapped` / `dropped` / `unsupported_value` on purpose — it
    # must never look like an accident.
    "to_default",
]


class Adjustment(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    action: AdjustmentAction
    canonical_value: Any = None
    sent_value: Any = None
    reason: str
    # Was this outcome DECLARED, or a surprise?
    #
    # `supported: false` (the model genuinely lacks the capability) and a
    # value_map entry pointing at null are decisions someone wrote down —
    # expected, and the client is not told. An UNEXPECTED drop is a value the
    # caller set that this offering silently would not carry, and under THE
    # EQUIVALENCE LAW that must reach the user as a WARNING
    # (common-docs/systems/platform/configuration-equivalence/FEATURE.md). Conversions
    # are never reported to the client — they are the system working.
    expected: bool = True


class ControlsMap(RootModel[dict[str, ControlRule]]):
    def rules(self) -> dict[str, ControlRule]:
        return self.root


class RulesEnvelope(BaseModel):
    """The ``{"params": ..., "constraints": ...}`` envelope on ai.api.rules and
    ai.offering.override. ``extra="forbid"`` — an unknown envelope key is a data
    bug and quarantines the row."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    params: dict[str, ControlRule] = {}
    constraints: list[Any] = []


class CatalogSetting(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    value_type: SettingValueType
    canonical_min: float | None = None
    canonical_max: float | None = None
    canonical_values: list[Any] | None = None
    default_value: Any = None
    ui: dict[str, Any] = {}
    description: str | None = None


class CatalogEndpoint(BaseModel):
    """One row per vendor being called (ai.endpoint) — WHO we call + how to auth."""

    model_config = ConfigDict(frozen=True)

    id: str
    # The RECORDED "who am I calling" fact (ai.endpoint.vendor, unique) — the
    # cost-grouping key behind ModelPricing.api / TokenUsage.api. REQUIRED: an
    # endpoint row without one QUARANTINES loudly rather than silently billing
    # under an empty vendor. NEVER sliced back out of a translator_key (that
    # guess tagged extraction_gliner and xai_realtime as ""), and NOT the same
    # fact as ai.provider — that is the model's CREATOR (Meta, for a Llama
    # served by Groq), never the API being called.
    vendor: str
    internal_name: str
    display_name: str
    base_url: str | None = None
    auth_ref: dict[str, Any] = {}
    byok_secret_key: str | None = None
    priority: int = 100
    is_active: bool = True


class CatalogApi(BaseModel):
    """One row per wire contract (ai.api) — HOW the call is shaped on the wire."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    display_name: str
    # The wire route token (unique) — the SAME token as the UnifiedAIClient
    # dispatch attr (openai_chat, google_image, ...) or a registered specialized
    # execution route (extraction/realtime/embeddings). Formerly
    # ai.service.wire_format.
    translator_key: str
    transport: ApiTransport = "sdk"
    rules: RulesEnvelope = RulesEnvelope()
    request_defaults: dict[str, Any] = {}
    description: str | None = None


class CatalogOffering(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    model_id: str
    endpoint_id: str
    api_id: str
    provider_model_id: str
    priority: int = 100
    is_available: bool = True
    pricing: Any = None
    usage_basis: str | None = None
    # The RECORDED billing fact: this offering bills on real provider tokens, so a
    # NULL usage_basis is intentional rather than an unset field. NEVER inferred from
    # a translator_key / api_class / model name — that guess is how customers get
    # mis-charged. Source: ai.offering.token_billed.
    token_billed: bool = False
    capabilities_override: dict[str, Any] = {}
    override: RulesEnvelope = RulesEnvelope()
    metadata: dict[str, Any] = {}


class CatalogVoice(BaseModel):
    """One enabled voice row from ``ai.voices``."""

    model_config = ConfigDict(frozen=True)

    provider: str
    provider_voice_id: str
    name: str
    # male | female | neutral | unknown | None. Load-bearing for tts_voice
    # equivalence — see catalog/equivalence.py and the cross-repo law
    # common-docs/systems/platform/configuration-equivalence/FEATURE.md.
    gender: str | None = None
    sort_order: int = 0
    metadata: dict[str, Any] = {}


class ResolvedCallProfile(BaseModel):
    # ``model_`` is a Pydantic-protected namespace; we deliberately use model_* names.
    model_config = ConfigDict(frozen=True, protected_namespaces=())

    # HOW this profile's offering was chosen: "preferred" = priority order (the
    # default), "pinned" = the caller pinned an exact offering_id and got exactly
    # it. Sibling-offering overload fallback re-resolves with a new pin, so a
    # fallback dispatch reads "pinned" here — the FALLBACK fact is recorded by
    # the executor (RerouteNote + TokenUsage.offering_route), not the resolver.
    # "tier_reroute" = the caller named a model but catalog QUALITY-TIER routing
    # served a DIFFERENT one (TTS quality tiers / a deprecated model). It rides
    # into TokenUsage.offering_route → cx_request, so "we did not call what you
    # asked for" is queryable instead of invisible — the silence that hid every
    # podcast being moved off gemini-2.5-pro-preview-tts for days (2026-08-10).
    resolution_route: Literal["pinned", "preferred", "tier_reroute"] = "preferred"

    model_id: str
    model_name: str
    provider_model_id: str
    offering_id: str
    endpoint_id: str
    api_id: str
    # The model's CREATOR (ai.provider via the provider_id FK) — "Meta" for a Llama
    # served by Groq. This is a display/lineage fact. It is NOT "who am I calling":
    # for that (routing identity, cost grouping) use ``vendor``.
    provider_name: str
    # The API vendor actually being called (ai.endpoint.vendor): openai, groq, google,
    # xai, together, replicate, elevenlabs, cerebras, huggingface, fastino, mock,
    # generic_openai. The cost-grouping key — see CatalogEndpoint.vendor.
    vendor: str
    # The wire route (ai.api.translator_key). The field keeps its historical name —
    # every provider client + translator dispatches on it.
    wire_format: str
    # Execution channel — identical to wire_format for UnifiedAIClient routes;
    # specialized routes map to "extraction", "realtime", or "embedding".
    client_attr: str
    base_url: str | None = None
    auth_ref: dict[str, Any] = {}
    byok_secret_key: str | None = None
    capabilities: ResolvedModelCapabilities
    controls: CompiledControlsMap
    # Trusted, provider-native body defaults from ai.api.request_defaults.
    # Translators apply these only at their structural wire seam (rather than
    # treating them as user-controllable scalar parameters).
    request_defaults: dict[str, Any] = {}
    pricing: Any = None
    usage_basis: str | None = None
    token_billed: bool = False
    model_is_deprecated: bool = False
    model_is_primary: bool = False
    offering_metadata: dict[str, Any] = {}
    tts_voice_ids: tuple[str, ...] = ()
    tts_default_voice_id: str | None = None
    # NOTE: ``legacy_api_class`` is GONE (B2-media + B4 flips complete). Every
    # provider client — chat and media — takes this whole profile; param shaping
    # is ``controls``, structural branching reads capabilities / model ids.


__all__ = [
    "SettingValueType",
    "AliasKind",
    "ApiTransport",
    "Adjustment",
    "AdjustmentAction",
    "ClampSpec",
    "ControlRule",
    "PASSTHROUGH_RULE",
    "ControlsMap",
    "RulesEnvelope",
    "CatalogSetting",
    "CatalogEndpoint",
    "CatalogApi",
    "CatalogOffering",
    "CatalogVoice",
    "ResolvedCallProfile",
]
