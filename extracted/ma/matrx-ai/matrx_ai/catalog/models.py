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

K6 additions (settings-translation CONTRACTS.md; acting since item C5 — see
controls.py): ``off`` ({send}|{floor}|{omit, why}),
``from_number`` (ascending [{lte, to}]), ``to_number`` ({canonical: int}),
``accepts`` (capability list) and the declared drop ``{"drop": true, "why"}``.

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


class OffSpec(BaseModel):
    """K6 ``off`` — how an intensity setting's explicit OFF reaches the wire,
    distinct from UNSET. Exactly one form: ``{"send": <provider value>}``,
    ``{"floor": true}`` (the nearest-lowest value the model accepts) or
    ``{"omit": true, "why": "..."}`` (the only form under which wire(off) may
    equal wire(unset))."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    send: Any = None
    floor: bool | None = None
    omit: bool | None = None
    why: str | None = None

    @model_validator(mode="after")
    def _one_form(self) -> OffSpec:
        forms = [
            name
            for name, present in (
                ("send", "send" in self.model_fields_set),
                ("floor", bool(self.floor)),
                ("omit", bool(self.omit)),
            )
            if present
        ]
        if len(forms) != 1:
            raise ValueError(
                f"off must declare exactly one of send / floor / omit (got {forms or 'none'})"
            )
        if self.omit and not (self.why or "").strip():
            raise ValueError('off={"omit": true} requires a "why"')
        return self


class FromNumberStep(BaseModel):
    """One K6 ``from_number`` cut-off: numbers ``<= lte`` become ``to``
    (``lte: null`` = everything above the previous step; ``to: null`` = a
    declared, silent drop)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    lte: float | None
    to: Any = None


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

    # ── K6 rule-language additions (settings-translation CONTRACTS.md) ──────
    # They ACT (item C5) — semantics in controls.py's module docstring; the
    # tables a rule does not carry fall back to catalog/translation_defaults.py.
    # Every default is None so ``model_dump(exclude_none=True)``
    # (export_model_routing -> client hosts) and ``exclude_unset`` (the legacy
    # merge) are byte-identical for rows that do not carry them.
    off: OffSpec | None = None
    from_number: list[FromNumberStep] | None = None
    to_number: dict[str, int] | None = None
    # Capability: what the model ACCEPTS — enforced on every scalar and
    # processor rule (nearest accepted, provenance computed). ``ui_values``
    # stays what the UI offers and is NOT newly enforced (seed semantics).
    accepts: list[Any] | None = None
    # The declared-drop form ``{"drop": true, "why": ...}`` — the replacement
    # for "supported:false means drop" once C6 redefines supported:false.
    drop: bool | None = None
    why: str | None = None

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
        if self.drop and not (self.why or "").strip():
            raise ValueError('a declared drop {"drop": true} requires a "why"')
        if self.drop and self.supported:
            # A declared drop is never native here. Every reader that asks
            # ``rule.supported`` (translators deciding reasoning includes, the
            # speech compiler's speaker cap / direction) must see the same
            # answer as the engine's ``carries`` — so ``drop`` implies
            # ``supported=False`` in ONE place instead of at every reader
            # (C3c: a drop cell otherwise read as "supported" there).
            object.__setattr__(self, "supported", False)
        if self.from_number:
            bounds = [step.lte for step in self.from_number]
            if any(b is None for b in bounds[:-1]):
                raise ValueError('from_number: only the LAST step may have "lte": null')
            finite = [b for b in bounds if b is not None]
            if finite != sorted(finite) or len(set(finite)) != len(finite):
                raise ValueError("from_number: lte cut-offs must be strictly ascending")
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


# K9 — WHO decided an Adjustment. ``declared``: a rule wrote it down (value_map,
# clamp, to_default, const, supported:false, on_unmapped="drop", a processor's
# own table). ``computed``: no declaration covered it and the engine decided —
# the nearest-equivalent metric, the model's output maximum, the foreign-key
# gate, an SDK-drift or validation fallback.
AdjustmentProvenance = Literal["declared", "computed"]
CellLayer = Literal["api", "profile", "offering"]
CellState = Literal["approved", "agent", "proposed", "inherited"]


class CellRef(BaseModel):
    """The translation cell (K3) that decided a key, as read from the compiled
    view (K5). Absent (None) while rules still come from ai.api.rules /
    ai.offering.override (copy mode)."""

    model_config = ConfigDict(frozen=True)

    cell_id: str
    layer: CellLayer
    state: CellState
    version: int | None = None


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
    # K9 provenance — see AdjustmentProvenance. Defaults to "declared" so a
    # site that predates K9 claims nothing it was not; every engine fallback
    # sets "computed" explicitly.
    provenance: AdjustmentProvenance = "declared"
    # The cell that decided this key (K3/K5); None until cells exist. Stamped
    # by CompiledControlsMap.outbound from its ``cells`` map.
    cell_id: str | None = None
    layer: CellLayer | None = None
    cell_state: CellState | None = None
    # K7 family conversion: the canonical key the caller actually set, when this
    # Adjustment records its conversion INTO ``key`` (``canonical_value`` is the
    # caller's value, ``sent_value`` the value ``key`` carried into its rule).
    converted_from: str | None = None


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
    # K7 (settings-translation C6): the setting family slug (platform.categories
    # dimension ``ai_setting_family``) and, for an ordinal setting, each
    # canonical value's position 0..1. ``None`` until ai.setting carries them —
    # then family conversion stays off and foreign keys drop as before.
    family: str | None = None
    value_positions: dict[str, float] | None = None


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
    # Lifecycle (ai_075, ruled 2026-09-09): deprecated = hidden by default but
    # RUNNABLE (warned once per process); retired_at = dead — resolve_call_profile
    # refuses before a profile is ever built, so a profile with model_retired_at
    # set only exists for display/history readers.
    model_is_deprecated: bool = False
    model_is_primary: bool = False
    model_retired_at: str | None = None
    model_successor_id: str | None = None
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
    "AdjustmentProvenance",
    "CellLayer",
    "CellRef",
    "CellState",
    "ClampSpec",
    "ControlRule",
    "FromNumberStep",
    "OffSpec",
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
