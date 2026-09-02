"""Pure control-rule application — compile, outbound, inbound. No DB, no I/O.

Outbound runs in TWO passes:

PASS 1 — scalar rules, per canonical key, precedence:
    1. const                       -> always send rule.const (wins over the
                                      incoming value; sent even when unset)
    2. supported: false            -> drop the key entirely
    3. value_map lookup            -> canonical -> provider value
                                      (explicit null result = OMIT the key;
                                       a MISS follows on_unmapped: "nearest" (DEFAULT
                                       — closest MAPPED value in the ai.setting
                                       canonical_values order, ties toward the LATER
                                       position) | "drop" (loud, explicit-only — never
                                       the default; permitted ONLY when the target
                                       genuinely lacks the capability) | "error" (raise).
                                       THE EQUIVALENCE LAW (2026-08-17): every value an
                                       offering claims to support must convert for EVERY
                                       canonical value; silently dropping an unmapped
                                       value is a severe defect, not normal behaviour.
                                       See /home/user/matrx-common-docs/systems/platform/configuration-equivalence/FEATURE.md)
    4. clamp                       -> numeric min/max
    5. provider_key rename         -> default = same key; a dotted path expands
                                      into nested dicts
    then defaults: rule ``default`` is a PROVIDER-vocabulary value applied when
    the canonical key is unset (skips value_map/clamp, lands at provider_key).
    ``send_when_unset=True`` strengthens it: the default ALSO backfills when a
    SET value was eliminated (value_map->null omit / on_unmapped drop), so the
    provider key is always sent.

PASS 2 — processor rules, deterministically ordered by
    (processor_config["order"] (default 100), key). Each named processor
    (catalog/processors.py) receives (canonical, assembled params, context) and
    owns its key's translation entirely; keys listed in
    processor_config["consumes"] are skipped by pass 1 (the processor reads
    them from the canonical dict itself). A processor rule MAY carry ``default``
    (ai_045): when the canonical key is unset, the default is backfilled into
    the CANONICAL dict (canonical vocabulary, not provider vocabulary) before
    the processor runs — so an unset config resolves through the processor
    exactly as if the caller had sent the default. A processor rule MAY carry ``clamp``
    (ai_038): the canonical value is clamped — with an Adjustment — before the
    processor runs, so DB rules can express the provider's numeric range for a
    processor-owned key (value_map/const remain exclusive with processor).

Canonical keys starting with "_" are canonicalizer metadata (e.g.
``_reasoning_effort_derived``) — read by processors, never sent to a provider.

Every drop/omit/map/clamp/const is reported as an ``Adjustment`` so callers can
voice the yellow "CAPABILITY ADJUSTMENT" message instead of silently mutating
the user's request. Defaults (and a const with no competing incoming value) are
silent — nothing of the user's was changed.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict

from matrx_ai.catalog.models import (
    PASSTHROUGH_RULE,
    Adjustment,
    AdjustmentAction,
    CatalogSetting,
    ControlRule,
    ResolvedCallProfile,
)
from matrx_ai.catalog.equivalence import nearest_equivalent
from matrx_ai.catalog.processors import ProcessorContext, get_processor, has_processor


class UnmappedValueError(ValueError):
    """on_unmapped="error" fired: a value_map miss this rule declares fatal."""


# ── dotted-path helpers (shared with the parity validator) ───────────────────
def expand_dotted(target: dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    node = target
    for part in parts[:-1]:
        child = node.get(part)
        if not isinstance(child, dict):
            child = {}
            node[part] = child
        node = child
    node[parts[-1]] = value


def flatten_dotted(params: dict[str, Any], _prefix: str = "") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in params.items():
        dotted = f"{_prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten_dotted(value, f"{dotted}."))
        else:
            flat[dotted] = value
    return flat


def _dotted_get(params: dict[str, Any], dotted_key: str) -> tuple[bool, Any]:
    node: Any = params
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return False, None
        node = node[part]
    return True, node


# ── rule merge (implicit passthrough <- api <- offering, per FIELD) ──────────
def merge_rule_dicts(
    api_rule: dict[str, Any] | None, offering_rule: dict[str, Any] | None
) -> ControlRule:
    merged: dict[str, Any] = {}
    if api_rule:
        merged.update(api_rule)
    if offering_rule:
        merged.update(offering_rule)  # offering wins per field
    return ControlRule.model_validate(merged)


def compile_controls(
    api_params: dict[str, ControlRule],
    offering_overrides: dict[str, ControlRule],
    settings: dict[str, CatalogSetting] | None = None,
    voice_genders: dict[str, str] | None = None,
) -> CompiledControlsMap:
    keys = set(api_params) | set(offering_overrides)
    rules: dict[str, ControlRule] = {}
    for key in keys:
        api_rule = api_params.get(key)
        off = offering_overrides.get(key)
        rules[key] = merge_rule_dicts(
            api_rule.model_dump(exclude_unset=True) if api_rule is not None else None,
            off.model_dump(exclude_unset=True) if off is not None else None,
        )
    # value_order for on_unmapped="nearest": the ai.setting dictionary's
    # canonical_values IS the canonical order for ordered enums.
    value_orders: dict[str, list[Any]] = {}
    for key in keys:
        setting = (settings or {}).get(key)
        if setting is not None and setting.canonical_values:
            value_orders[key] = list(setting.canonical_values)
    return CompiledControlsMap(
        rules=rules, value_orders=value_orders, voice_genders=dict(voice_genders or {})
    )


def validate_rules_against_settings(
    rules: dict[str, ControlRule], settings: dict[str, CatalogSetting]
) -> list[str]:
    errors: list[str] = []
    for key, rule in rules.items():
        if rule.processor is not None and not has_processor(rule.processor):
            errors.append(
                f"'{key}': processor '{rule.processor}' is not a registered catalog processor"
            )
        setting = settings.get(key)
        if setting is None:
            errors.append(f"control key '{key}' is not a registered ai.setting")
            continue
        if rule.value_map is not None and setting.value_type == "enum":
            allowed = {str(v) for v in (setting.canonical_values or [])}
            unknown = sorted(set(rule.value_map) - allowed)
            if unknown:
                errors.append(
                    f"'{key}': value_map keys {unknown} not in setting.canonical_values {sorted(allowed)}"
                )
        if rule.ui_values is not None and setting.value_type == "enum":
            allowed = {str(v) for v in (setting.canonical_values or [])}
            unknown = sorted({str(v) for v in rule.ui_values} - allowed)
            if unknown:
                errors.append(
                    f"'{key}': ui_values {unknown} not in setting.canonical_values "
                    f"{sorted(allowed)} — the UI vocabulary must be canonical"
                )
        if rule.to_default is not None and setting.value_type == "enum":
            allowed = {str(v) for v in (setting.canonical_values or [])}
            unknown = sorted({str(v) for v in rule.to_default} - allowed)
            if unknown:
                errors.append(
                    f"'{key}': to_default {unknown} not in setting.canonical_values "
                    f"{sorted(allowed)} — the explicit-default vocabulary must be canonical"
                )
        if rule.to_default is not None and rule.value_map is not None:
            ambiguous = sorted({str(v) for v in rule.to_default} & set(rule.value_map))
            if ambiguous:
                errors.append(
                    f"'{key}': {ambiguous} listed in BOTH to_default and value_map — "
                    "ambiguous data; a value must declare exactly one resolution"
                )
        if rule.clamp is not None:
            if (
                setting.canonical_min is not None
                and rule.clamp.min is not None
                and rule.clamp.min < setting.canonical_min
            ):
                errors.append(
                    f"'{key}': clamp.min {rule.clamp.min} below canonical_min {setting.canonical_min}"
                )
            if (
                setting.canonical_max is not None
                and rule.clamp.max is not None
                and rule.clamp.max > setting.canonical_max
            ):
                errors.append(
                    f"'{key}': clamp.max {rule.clamp.max} above canonical_max {setting.canonical_max}"
                )
    return errors


# ── the compiled map ─────────────────────────────────────────────────────────
class CompiledControlsMap(BaseModel):
    model_config = ConfigDict(frozen=True)

    rules: dict[str, ControlRule] = {}
    # Canonical enum order per key (ai.setting.canonical_values) — the "nearest"
    # metric for on_unmapped="nearest". Populated by compile_controls(settings=...).
    value_orders: dict[str, list[Any]] = {}
    # canonical voice token -> gender, from ai.voices. Voice equivalence is
    # gender-preserving by law; without this the tts_voice metric has nothing to
    # measure and refuses (a loud drop) rather than crossing gender.
    voice_genders: dict[str, str] = {}

    def rule_for(self, key: str) -> ControlRule:
        return self.rules.get(key, PASSTHROUGH_RULE)

    def _nearest_in(self, key: str, value: str, candidates: Any) -> str | None:
        # Equivalence is per-SETTING, not one global metric — see
        # catalog/equivalence.py (ratio for aspect_ratio, family for formats,
        # the canonical scale for ordered enums, None where no honest nearest
        # exists). Returning None here makes the caller drop LOUDLY rather than
        # invent an answer.
        return nearest_equivalent(
            key,
            value,
            candidates,
            self.value_orders.get(key, ()),
            genders=self.voice_genders,
        )

    def _nearest_mapped(self, key: str, value: str, value_map: dict[str, Any]) -> str | None:
        return self._nearest_in(key, value, value_map)

    def outbound(
        self, canonical: dict[str, Any], *, context: dict[str, Any] | None = None
    ) -> tuple[dict[str, Any], list[Adjustment]]:
        out: dict[str, Any] = {}
        adjustments: list[Adjustment] = []

        # Processor rules own their key + declared consumed keys — pass 1 skips both.
        processor_rules = [
            (rule.processor_config.get("order", 100), key, rule)
            for key, rule in self.rules.items()
            if rule.processor is not None
        ]
        processor_owned: set[str] = set()
        for _, key, rule in processor_rules:
            processor_owned.add(key)
            processor_owned.update(rule.processor_config.get("consumes", []))

        # Keys whose SET value was eliminated (map->null / unmapped drop) —
        # send_when_unset=True backfills their default below.
        eliminated: set[str] = set()

        # ── PASS 1: scalar rules ─────────────────────────────────────────────
        for key, value in canonical.items():
            if key.startswith("_"):
                continue  # canonicalizer metadata — processor input, never wire
            if key in processor_owned:
                continue
            rule = self.rule_for(key)
            if rule.const is not None:
                continue  # const rules emit below whether or not a value came in
            if value is None:
                continue  # unset — the rule default (below) may still apply
            if rule.supported is False:
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="dropped",
                        canonical_value=value,
                        sent_value=None,
                        reason=f"'{key}' is not supported by this api/offering",
                    )
                )
                continue

            sent = value
            if (
                rule.to_default is not None
                and isinstance(value, str)
                and value in rule.to_default
            ):
                # THE EXPLICIT DEFAULT DECLARATION (Rule 3) — a DECLARED decision
                # that this canonical value resolves to the offering's default,
                # never an inferred conversion. Takes precedence over
                # value_map/on_unmapped: a declared decision beats a lookup.
                if rule.default is not None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="to_default",
                            canonical_value=value,
                            sent_value=rule.default,
                            expected=True,
                            reason=(
                                f"'{key}'={value!r} is DECLARED to resolve to this "
                                f"offering's default ({rule.default!r}) — see to_default"
                            ),
                        )
                    )
                    expand_dotted(out, rule.provider_key or key, rule.default)
                else:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="to_default",
                            canonical_value=value,
                            sent_value=None,
                            expected=True,
                            reason=(
                                f"'{key}'={value!r} is DECLARED to resolve to this "
                                f"offering's default, and no default is set — omitted"
                            ),
                        )
                    )
                continue
            if rule.value_map is not None and isinstance(value, str):
                lookup = value
                if value not in rule.value_map:
                    # value_map MISS — on_unmapped decides.
                    if rule.on_unmapped == "error":
                        vcprint(
                            f"'{key}'={value!r} has no value_map entry and the rule "
                            f"declares on_unmapped='error'. Mapped values: "
                            f"{sorted(rule.value_map)}. Fix the caller or the rule.",
                            title="🚨 AI CATALOG UNMAPPED VALUE",
                            color="red",
                        )
                        raise UnmappedValueError(
                            f"'{key}'={value!r} is not mapped for this api/offering "
                            f"(mapped: {sorted(rule.value_map)})"
                        )
                    if rule.on_unmapped == "nearest":
                        nearest = self._nearest_mapped(key, value, rule.value_map)
                        if nearest is not None:
                            lookup = nearest
                        else:
                            adjustments.append(
                                Adjustment(
                                    key=key,
                                    action="dropped",
                                    canonical_value=value,
                                    sent_value=None,
                                    expected=False,
                                    reason=(
                                        f"'{key}'={value!r} is not mapped and no nearest "
                                        f"mapped value exists in the canonical order — dropped"
                                    ),
                                )
                            )
                            eliminated.add(key)
                            continue
                    else:  # "drop" — an EXPLICIT, non-default rule declaration (nearest
                        # is the default per THE EQUIVALENCE LAW, 2026-08-17); still loud
                        adjustments.append(
                            Adjustment(
                                key=key,
                                action="dropped",
                                canonical_value=value,
                                sent_value=None,
                                expected=False,
                                reason=(
                                    f"'{key}'={value!r} is not mapped for this "
                                    f"api/offering — dropped"
                                ),
                            )
                        )
                        eliminated.add(key)
                        continue
                mapped = rule.value_map[lookup]
                if mapped is None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="omitted",
                            canonical_value=value,
                            sent_value=None,
                            reason=f"'{key}'={value!r} maps to null — omitted for this api/offering",
                        )
                    )
                    eliminated.add(key)
                    continue
                if mapped != value:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="mapped",
                            canonical_value=value,
                            sent_value=mapped,
                            reason=f"'{key}'={value!r} mapped to {mapped!r} for this api/offering",
                        )
                    )
                sent = mapped

            if (
                rule.clamp is not None
                and isinstance(sent, int | float)
                and not isinstance(sent, bool)
            ):
                clamped: float = sent
                if rule.clamp.min is not None and clamped < rule.clamp.min:
                    clamped = rule.clamp.min
                if rule.clamp.max is not None and clamped > rule.clamp.max:
                    clamped = rule.clamp.max
                if isinstance(sent, int) and float(clamped).is_integer():
                    clamped = int(clamped)
                if clamped != sent:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="clamped",
                            canonical_value=sent,
                            sent_value=clamped,
                            reason=f"'{key}'={sent!r} clamped to {clamped!r} for this api/offering",
                        )
                    )
                    sent = clamped

            expand_dotted(out, rule.provider_key or key, sent)

        # const — always send the fixed provider value; wins over any incoming value.
        for key, rule in self.rules.items():
            if rule.const is None or key in processor_owned:
                continue
            incoming = canonical.get(key)
            if incoming is not None and incoming != rule.const:
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="const",
                        canonical_value=incoming,
                        sent_value=rule.const,
                        reason=(
                            f"'{key}' is fixed to {rule.const!r} for this api/offering — "
                            f"replaced {incoming!r}"
                        ),
                    )
                )
            expand_dotted(out, rule.provider_key or key, rule.const)

        # Defaults — provider values applied when the canonical value is unset
        # (or, with send_when_unset=True, when the set value was eliminated).
        for key, rule in self.rules.items():
            if (
                rule.supported is False
                or rule.default is None
                or rule.const is not None
                or rule.processor is not None
            ):
                continue
            value_was_set = canonical.get(key) is not None
            if value_was_set and not (rule.send_when_unset and key in eliminated):
                continue
            target = rule.provider_key or key
            present, _ = _dotted_get(out, target)
            if not present:
                expand_dotted(out, target, rule.default)

        # ── PASS 2: processors, deterministic (order, key) ───────────────────
        for _, key, rule in sorted(processor_rules, key=lambda item: (item[0], item[1])):
            # ai_045: a processor rule honors ``default`` too — the CANONICAL
            # value is backfilled when the caller left the key unset, so the
            # processor translates the default exactly as it would a caller
            # value (e.g. the premium anthropic "-max" offerings default
            # reasoning_effort to "xhigh"). Silent, like scalar defaults —
            # nothing of the user's was changed. Unlike scalar defaults this
            # is provider-INDEPENDENT vocabulary: the processor still owns
            # the translation.
            if rule.default is not None and canonical.get(key) is None:
                canonical = {**canonical, key: rule.default}
            # clamp composes with a processor (ai_038): the canonical value is
            # clamped BEFORE the processor reads it, so DB rules can carry the
            # provider's real numeric range for processor-owned keys (e.g.
            # anthropic temperature max 1.0). Reported as an Adjustment.
            if rule.clamp is not None:
                incoming = canonical.get(key)
                if isinstance(incoming, int | float) and not isinstance(incoming, bool):
                    clamped: float = incoming
                    if rule.clamp.min is not None and clamped < rule.clamp.min:
                        clamped = rule.clamp.min
                    if rule.clamp.max is not None and clamped > rule.clamp.max:
                        clamped = rule.clamp.max
                    if isinstance(incoming, int) and float(clamped).is_integer():
                        clamped = int(clamped)
                    if clamped != incoming:
                        adjustments.append(
                            Adjustment(
                                key=key,
                                action="clamped",
                                canonical_value=incoming,
                                sent_value=clamped,
                                reason=(
                                    f"'{key}'={incoming!r} clamped to {clamped!r} "
                                    f"before processor {rule.processor!r}"
                                ),
                            )
                        )
                        canonical = {**canonical, key: clamped}
            fn = get_processor(rule.processor)  # loud UnknownProcessorError on a bad name
            ctx = ProcessorContext(
                key=key,
                config=rule.processor_config,
                adjustments=adjustments,
                extra=dict(context or {}),
                # The per-MODEL truth a processor's per-FAMILY maps cannot
                # carry: what this offering actually accepts, and the canonical
                # order to reconcile against. See
                # ProcessorContext.reconcile_supported.
                supported_values=frozenset(str(v) for v in (rule.ui_values or ())),
                value_order=tuple(
                    str(v) for v in self.value_orders.get(key, ()) if isinstance(v, str)
                ),
            )
            result = fn(canonical, out, ctx)
            if result is not None:
                out = result

        return out, adjustments

    def inbound(self, provider_params: dict[str, Any]) -> dict[str, Any]:
        flat = flatten_dotted(provider_params)
        out: dict[str, Any] = {}
        consumed: set[str] = set()

        for key, rule in self.rules.items():
            provider_key = rule.provider_key or key
            if provider_key not in flat:
                continue
            consumed.add(provider_key)
            value = flat[provider_key]
            if rule.value_map:
                inverse: dict[Any, str] = {}
                for canonical_value, provider_value in rule.value_map.items():
                    if provider_value is None:
                        continue
                    try:
                        already = provider_value in inverse
                    except TypeError:
                        continue  # unhashable provider value — not invertible
                    # Prefer identity pairs so e.g. {"xhigh": "high", "high": "high"}
                    # inverts "high" -> "high", not "high" -> "xhigh".
                    if not already or canonical_value == provider_value:
                        inverse[provider_value] = canonical_value
                try:
                    if value in inverse:
                        value = inverse[value]
                except TypeError:
                    pass
            out[key] = value

        # Best effort: unknown flat provider keys pass through under their own name.
        for provider_key, value in flat.items():
            if provider_key in consumed or "." in provider_key:
                continue
            out.setdefault(provider_key, value)
        return out


# ResolvedCallProfile declares ``controls: CompiledControlsMap`` as a forward
# ref (models.py cannot import this module — controls.py imports models.py).
# Resolve it here, where CompiledControlsMap is in scope.
ResolvedCallProfile.model_rebuild()

__all__ = [
    "Adjustment",
    "AdjustmentAction",
    "CompiledControlsMap",
    "compile_controls",
    "merge_rule_dicts",
    "validate_rules_against_settings",
    "expand_dotted",
    "flatten_dotted",
]
