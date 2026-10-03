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

Canonical keys starting with "_" are engine metadata (e.g. ``_converted``,
written by ``bridge_numbers``) — read by processors, never sent to a provider.

K6 RULE LANGUAGE (settings-translation item C5) — acts in PASS 1, per key, after
const / declared drop / supported:false and before to_default / value_map:
    off          the value MEANS off (translation_defaults.is_off_value):
                 {"send": v} sends v · {"floor": true} continues with the lowest
                 accepted value · {"omit": true, "why"} behaves exactly as unset
    from_number  a NUMBER becomes a scale value through the rule's cut-offs
                 (``to: null`` = declared, silent drop)
    accepts      the value must be accepted; else the nearest accepted one
                 (equivalence.nearest_accepted; Adjustment mapped/computed)
    to_number    a scale value becomes a number through the rule's table
    drop         {"drop": true, "why"}: a declared drop (expected, silent)
For a processor rule, off / accepts act on the canonical value BEFORE the
processor runs; the processor reads from_number / to_number itself (its rule
is on ``ProcessorContext.rule``). A rule carrying none of them behaves exactly
as before C5 (seed semantics: ``ui_values`` without ``accepts`` enforces
nothing new).

Every drop/omit/map/clamp/const is reported as an ``Adjustment`` so callers can
voice the yellow "CAPABILITY ADJUSTMENT" message instead of silently mutating
the user's request. Defaults (and a const with no competing incoming value) are
silent — nothing of the user's was changed.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.equivalence import nearest_accepted, nearest_equivalent
from matrx_ai.catalog.families import SettingFamilies, convert_through_families
from matrx_ai.catalog.models import (
    PASSTHROUGH_RULE,
    Adjustment,
    AdjustmentAction,
    CatalogSetting,
    CellRef,
    ControlRule,
    ResolvedCallProfile,
)
from matrx_ai.catalog.processors import ProcessorContext, get_processor, has_processor

# The canonical output-ceiling key every chat api maps to its provider name
# (max_tokens / max_completion_tokens / max_output_tokens / maxOutputTokens).
OUTPUT_CEILING_KEY = "max_output_tokens"


class UnmappedValueError(ValueError):
    """on_unmapped="error" fired: a value_map miss this rule declares fatal."""


def _is_accepted(value: Any, accepts: list[Any]) -> bool:
    # bool is an int in Python: True must never satisfy an accepted 1.
    for accepted in accepts:
        if isinstance(accepted, bool) or isinstance(value, bool):
            if accepted is value:
                return True
        elif accepted == value:
            return True
    return False


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
    families: SettingFamilies | None = None,
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
        rules=rules,
        value_orders=value_orders,
        voice_genders=dict(voice_genders or {}),
        families=families if families is not None else _families_from(settings),
    )


# ── K5: ai.offering_rules_compiled rows -> compiled controls ────────────────
# Layer precedence (K1): the most specific cell wins WHOLE — no field merge.
LAYER_PRECEDENCE: dict[str, int] = {"offering": 3, "profile": 2, "api": 1}

# The view-row columns this reader needs (K5: "with cell_id, layer, state,
# version", per available offering x setting key; ``rule`` is the K3 column).
VIEW_ROW_FIELDS: tuple[str, ...] = (
    "offering_id",
    "setting_key",
    "rule",
    "cell_id",
    "layer",
    "state",
    "version",
)


class ViewRowError(ValueError):
    """A K5 view row that cannot be read — quarantines its offering."""


def select_cells_from_view(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, dict[str, Any]]]:
    """Group K5 view rows into ``{offering_id: {setting_key: row}}``.

    The view already resolves one row per (offering, key). If it ever returns
    more than one, the most specific LAYER wins whole (K1); two rows at the
    same layer for one key are ambiguous data and raise ``ViewRowError``
    rather than picking one silently.
    """
    chosen: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        missing = [f for f in ("offering_id", "setting_key", "rule", "layer") if row.get(f) is None]
        if missing:
            raise ViewRowError(f"ai.offering_rules_compiled row missing {missing}: {row!r}")
        layer = str(row["layer"])
        if layer not in LAYER_PRECEDENCE:
            raise ViewRowError(f"ai.offering_rules_compiled row has unknown layer {layer!r}")
        per_offering = chosen.setdefault(str(row["offering_id"]), {})
        key = str(row["setting_key"])
        current = per_offering.get(key)
        if current is None:
            per_offering[key] = row
            continue
        rank, current_rank = LAYER_PRECEDENCE[layer], LAYER_PRECEDENCE[str(current["layer"])]
        if rank == current_rank:
            raise ViewRowError(
                f"ai.offering_rules_compiled: two {layer!r} cells for offering "
                f"{row['offering_id']} key {key!r} ({current.get('cell_id')}, {row.get('cell_id')})"
            )
        if rank > current_rank:
            per_offering[key] = row
    return chosen


def compile_controls_from_cells(
    cell_rows: dict[str, dict[str, Any]],
    settings: dict[str, CatalogSetting] | None = None,
    voice_genders: dict[str, str] | None = None,
    families: SettingFamilies | None = None,
) -> CompiledControlsMap:
    """One offering's K5 rows (``{setting_key: row}``) -> CompiledControlsMap.

    Each key's rule is its cell's ``rule`` taken WHOLE (``ControlRule``
    validated, no merge with any other layer), and the cell's id/layer/state
    ride in ``cells`` so every Adjustment for that key names its cell (K9)."""
    rules: dict[str, ControlRule] = {}
    cells: dict[str, CellRef] = {}
    for key, row in cell_rows.items():
        rule = row["rule"]
        rules[key] = rule if isinstance(rule, ControlRule) else ControlRule.model_validate(rule)
        if row.get("cell_id") is not None and row.get("state") is not None:
            version = row.get("version")
            cells[key] = CellRef(
                cell_id=str(row["cell_id"]),
                layer=str(row["layer"]),
                state=str(row["state"]),
                version=int(version) if version is not None else None,
            )
    value_orders: dict[str, list[Any]] = {}
    for key in rules:
        setting = (settings or {}).get(key)
        if setting is not None and setting.canonical_values:
            value_orders[key] = list(setting.canonical_values)
    return CompiledControlsMap(
        rules=rules,
        value_orders=value_orders,
        voice_genders=dict(voice_genders or {}),
        cells=cells,
        families=families if families is not None else _families_from(settings),
    )


def _families_from(settings: dict[str, CatalogSetting] | None) -> SettingFamilies | None:
    # The manager builds ONE SettingFamilies per load and passes it in; this
    # fallback serves direct callers (tests, tools) that pass settings only.
    return SettingFamilies.from_settings(settings) if settings else None


# Family data absent (ai.setting.family not populated): conversion is off and
# foreign keys drop exactly as before C6 — announced once per process.
_family_absence_announced: list[bool] = []


def _announce_family_absence_once() -> None:
    if _family_absence_announced:
        return
    _family_absence_announced.append(True)
    vcprint(
        "[catalog] setting families absent (ai.setting.family / value_positions not "
        "loaded) — K7 family conversion is OFF; canonical keys a target does not "
        "declare are dropped as before settings-translation C6.",
        color="blue",
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
        # K6: accepts / to_number keys / from_number targets speak the canonical
        # vocabulary of an enum setting, exactly like ui_values.
        if setting.value_type == "enum":
            allowed = {str(v) for v in (setting.canonical_values or [])}
            for field, values in (
                ("accepts", rule.accepts or []),
                ("to_number", list(rule.to_number or {})),
            ):
                unknown = sorted({str(v) for v in values} - allowed)
                if unknown:
                    errors.append(
                        f"'{key}': {field} {unknown} not in setting.canonical_values "
                        f"{sorted(allowed)} — the K6 vocabulary must be canonical"
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
    # THE MODEL'S REAL OUTPUT MAXIMUM (ai.model_definition.max_tokens), stamped
    # per call by ``with_output_maximum`` at profile build. An output ceiling is
    # a NUMBER with a hard per-model range, and under THE EQUIVALENCE LAW its
    # conversion is a clamp: an agent authored on a 128K model and run on a 16K
    # one must send 16K, never the 128K that the provider 400s
    # (live 2026-10-02: Groq qwen3.8-27b rejected max_completion_tokens=32000 on
    # /agents/battle). Applied in ``outbound`` BEFORE pass 1 and the processors,
    # so every translator — scalar provider_key or a processor that consumes
    # the key (Anthropic) — reads the clamped value. ``None`` = the catalog
    # declares no maximum; nothing is invented.
    output_maximum: int | None = None
    # K9: canonical key -> the translation cell (K3) that supplied its rule,
    # filled only when rules come from ai.offering_rules_compiled (K5). Empty
    # in copy mode; Adjustments then carry cell_id/layer/cell_state = None.
    cells: dict[str, CellRef] = {}
    # K7: every setting's family + value positions (shared by reference across
    # every compiled map of one catalog load). ``None`` = family data absent:
    # no conversion, foreign keys drop as before C6, ordinals keep list order.
    families: SettingFamilies | None = None

    def with_output_maximum(self, maximum: Any) -> CompiledControlsMap:
        """This map, carrying the model's real output maximum (or unchanged)."""
        try:
            value = int(maximum) if maximum is not None and not isinstance(maximum, bool) else None
        except (TypeError, ValueError):
            value = None
        if value is None or value <= 0:
            return self
        return self.model_copy(update={"output_maximum": value})

    def rule_for(self, key: str) -> ControlRule:
        return self.rules.get(key, PASSTHROUGH_RULE)

    def _nearest_in(self, key: str, value: str, candidates: Any) -> str | None:
        # K7: an ordinal with declared POSITIONS measures by position, not by
        # its canonical_values list order (that list put 4k next to 0.5k, so
        # 4k reached 1k on a {1k, 2k} model).
        if self.families is not None:
            candidates = list(candidates)
            by_position = self.families.nearest_by_position(key, value, candidates)
            if by_position is not None:
                return by_position
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

    def _nearest_accepted(self, key: str, value: Any, accepts: list[Any]) -> Any:
        if self.families is not None:
            by_position = self.families.nearest_by_position(key, value, accepts)
            if by_position is not None:
                return next((a for a in accepts if str(a) == by_position), by_position)
        return nearest_accepted(
            key, value, accepts, self.value_orders.get(key, ()), genders=self.voice_genders
        )

    def _declares(self, key: str) -> bool:
        """Does this target carry ``key`` (its own rule, or a processor's
        ``consumes``)? A passthrough map (no rules) carries everything."""
        if not self.rules or key in self.rules:
            return True
        return any(key in rule.processor_config.get("consumes", []) for rule in self.rules.values())

    def _surface(self) -> tuple[set[str], set[str], set[str]]:
        """(processor-owned keys, keys of unsupported/dropped processors, keys
        under a declared drop) — the same partition ``outbound`` applies."""
        owned: set[str] = set()
        unsupported: set[str] = set()
        declared_drop: set[str] = set()
        for key, rule in self.rules.items():
            consumed = [key, *rule.processor_config.get("consumes", [])]
            if rule.processor is not None:
                if rule.supported is False or rule.drop:
                    unsupported.update(consumed)
                    if rule.drop:
                        declared_drop.update(consumed)
                else:
                    owned.update(consumed)
            elif rule.drop:
                declared_drop.add(key)
        return owned, unsupported - owned, declared_drop - owned

    def carries(self, key: str) -> bool:
        """Does this target NATIVELY carry ``key``? K6: a rule that says
        ``supported: false`` does not — it converts through its family (K7).
        A passthrough map (no rules) carries everything."""
        if not self.rules:
            return True
        owned, unsupported, declared_drop = self._surface()
        if key in owned:
            return True
        rule = self.rules.get(key)
        return (
            rule is not None
            and rule.supported is not False
            and not rule.drop
            and key not in unsupported
            and key not in declared_drop
        )

    def translate_foreign(
        self, canonical: dict[str, Any], *, model: Any = "?"
    ) -> tuple[dict[str, Any], list[Adjustment], list[str]]:
        """THE GATE every seam runs before ``outbound`` (chat + media).

        Families loaded (K7): every canonical key this target does not natively
        carry — undeclared, or ``supported: false`` — converts through its
        family (catalog/families.py); only a family with no member that can
        carry it drops, as an UNEXPECTED Adjustment (the client warning). A
        declared ``{"drop": true}`` is left for ``outbound`` (expected, silent).

        Families absent: exactly the pre-C6 declared-keys gate — a key with no
        rule and no processor ``consumes`` claim is dropped (expected, computed);
        ``supported: false`` is left for ``outbound`` to drop.

        Returns (canonical without the removed keys, Adjustments, removed keys).
        Passthrough profiles (rules == {}, the host-catalog client mode) carry
        everything and are returned unchanged."""
        if not self.rules:
            return canonical, [], []
        if self.families is None:
            _announce_family_absence_once()
            declared = set(self.rules)
            for rule in self.rules.values():
                declared.update(rule.processor_config.get("consumes", []))
            foreign = sorted(
                key for key in canonical if not key.startswith("_") and key not in declared
            )
            if not foreign:
                return canonical, [], []
            vcprint(
                f"[outbound_params] dropped foreign canonical key(s) not declared by "
                f"this api/offering's control rules: {foreign} (model={model})",
                color="yellow",
            )
            kept = {k: v for k, v in canonical.items() if k not in foreign}
            adjustments = [
                Adjustment(
                    key=key,
                    action="dropped",
                    canonical_value=canonical[key],
                    sent_value=None,
                    expected=True,  # pre-C6 behaviour: silent to the client
                    provenance="computed",
                    reason=(
                        f"'{key}' is not declared by this api/offering's control "
                        "rules (foreign key) — dropped"
                    ),
                )
                for key in foreign
            ]
            return kept, self.stamp_cells(adjustments), foreign

        _, _, declared_drop = self._surface()
        sources: list[str] = []
        unset: list[str] = []
        for key in sorted(canonical):
            if key.startswith("_") or canonical[key] is None:
                continue
            if self.carries(key):
                continue
            if D.is_unset_posture(canonical[key]):
                # C3c: "auto" MEANS not set. A key this target does not carry,
                # set to "not set", is simply absent — no conversion, no drop,
                # no warning (and a processor never sees it either).
                unset.append(key)
                continue
            if key in declared_drop:
                continue
            sources.append(key)
        if unset:
            canonical = {k: v for k, v in canonical.items() if k not in unset}
        if not sources:
            return canonical, [], unset
        converted, adjustments = convert_through_families(self, canonical, sources)
        if adjustments:
            vcprint(
                f"[outbound_params] {len(sources)} canonical key(s) not carried by "
                f"this api/offering went through their setting family: "
                + "; ".join(a.reason for a in adjustments)
                + f" (model={model})",
                color="yellow",
            )
        return converted, self.stamp_cells(adjustments), sorted(sources + unset)

    def _output_ceiling(self) -> tuple[int | float | None, str]:
        """(the output ceiling pass 0 enforces, its provenance).

        An OFFERING-layer cell that declares a ``clamp.max`` on the output
        ceiling is the host's real limit (a host fact, not a model fact) — pass
        0 yields to it and records ``declared``. Only when no such cell exists
        does the model maximum stand in as the ``computed`` safety net."""
        cell = self.cells.get(OUTPUT_CEILING_KEY)
        rule = self.rules.get(OUTPUT_CEILING_KEY)
        if (
            cell is not None
            and cell.layer == "offering"
            and rule is not None
            and rule.clamp is not None
            and rule.clamp.max is not None
        ):
            ceiling = rule.clamp.max
            return (int(ceiling) if float(ceiling).is_integer() else ceiling), "declared"
        return self.output_maximum, "computed"

    def _speaks_posture(self, key: str, value: str, *, dropped: bool) -> bool:
        """Would PASS 1 put this posture value (``auto``) on the wire — as
        itself, through the rule's map/accepts/to_number, or its nearest?
        False = it could only be dropped, so it is treated as unset (C3c)."""
        rule = self.rule_for(key)
        if dropped or rule.supported is False or rule.drop or rule.const is not None:
            return rule.const is not None
        if rule.accepts is not None and not _is_accepted(value, rule.accepts):
            nearest = self._nearest_accepted(key, value, rule.accepts)
            if nearest is None:
                return False
            value = nearest
        if rule.to_number:
            return (
                value in rule.to_number or self._nearest_in(key, value, rule.to_number) is not None
            )
        if rule.to_default is not None and value in rule.to_default:
            return True
        if rule.value_map is not None:
            if value in rule.value_map:
                return True
            if rule.on_unmapped == "nearest":
                return self._nearest_mapped(key, value, rule.value_map) is not None
            return False
        return True

    def _floor_value(self, key: str, rule: ControlRule) -> Any:
        """K6 ``off: {"floor": true}`` — the lowest value this rule accepts
        (``accepts``, else ``ui_values``, else the non-null value_map keys),
        ordered by the setting's canonical order; postures excluded."""
        pool = rule.accepts or rule.ui_values
        if pool is None and rule.value_map:
            pool = [k for k, v in rule.value_map.items() if v is not None]
        candidates = [v for v in (pool or []) if not (isinstance(v, str) and v in D.HOUSE_VALUES)]
        if not candidates:
            return None
        order = [str(v) for v in self.value_orders.get(key, ())]
        if all(isinstance(v, int | float) and not isinstance(v, bool) for v in candidates):
            return min(candidates)
        ranked = [v for v in candidates if str(v) in order]
        if not ranked:
            return None
        return min(ranked, key=lambda v: order.index(str(v)))

    def bridge_numbers(self, canonical: dict[str, Any]) -> tuple[dict[str, Any], list[Adjustment]]:
        """THE TARGET-AWARE number -> scale conversion (K6 ``from_number``).

        Replaces canonicalize's global budget->effort tier (and its
        ``_reasoning_effort_derived`` flag). canonicalize no longer picks an
        effort: when the caller set only the number (thinking_budget) it
        records the REQUEST ``canonical["_convert"] = {target: source}``, and
        THIS target converts it through its own rule ``from_number`` — else the
        declared default steps (today's tiers, so a rule that carries none
        translates exactly as before). The result is recorded in
        ``canonical["_converted"]`` ({target: source}) so a processor that owns
        the raw number treats the converted value as unset. A target that does
        not carry the sibling gets nothing (it would only be dropped).

        Runs at the top of ``outbound``. A raw canonical dict without
        ``_convert`` is never bridged — what the caller passed is what the
        rules see."""
        adjustments: list[Adjustment] = []
        out = canonical
        requested = out.get("_convert") or {}
        for source, target in D.NUMBER_TO_SCALE_BRIDGES.items():
            if requested.get(target) != source:
                continue
            number = out.get(source)
            if (
                number is None
                or isinstance(number, bool)
                or not isinstance(number, int | float)
                or out.get(target) is not None
                or not self._declares(target)
            ):
                continue
            rule = self.rule_for(target)
            steps = rule.from_number or D.DEFAULT_FROM_NUMBER.get(target)
            if not steps:
                continue
            converted = D.step_lookup(steps, number)
            if converted is None:
                # from_number declares this range a drop (``to: null``).
                adjustments.append(
                    Adjustment(
                        key=target,
                        action="dropped",
                        canonical_value=number,
                        sent_value=None,
                        expected=True,
                        reason=(
                            f"'{source}'={number!r} converts to no '{target}' on this "
                            "target (from_number declares a drop)"
                        ),
                    )
                )
                continue
            out = {
                **out,
                target: converted,
                "_converted": {**(out.get("_converted") or {}), target: source},
            }
            # K9/K10: the conversion is provenance the rejection record reads
            # (a budget-only config carries no canonical effort of its own).
            # Only when the converted value can reach the wire — a target that
            # drops the sibling records that drop in outbound instead.
            if not self.carries(target):
                continue
            adjustments.append(
                Adjustment(
                    key=target,
                    action="mapped",
                    canonical_value=number,
                    sent_value=converted,
                    expected=True,
                    provenance="declared" if rule.from_number else "computed",
                    converted_from=source,
                    reason=(
                        f"'{source}'={number!r} converted to '{target}'={converted!r} "
                        "by this target's from_number"
                        + ("" if rule.from_number else " (declared default steps)")
                    ),
                )
            )
        return out, self.stamp_cells(adjustments)

    def outbound(
        self, canonical: dict[str, Any], *, context: dict[str, Any] | None = None
    ) -> tuple[dict[str, Any], list[Adjustment]]:
        out: dict[str, Any] = {}
        # ── BRIDGE: target-aware number -> scale (K6 from_number) ────────────
        canonical, adjustments = self.bridge_numbers(canonical)

        # ── PASS 0: the output ceiling (see ``output_maximum``) ───────────────
        # A conversion, not a drop: silent to the client, loud in the log. An
        # offering-layer cell declaring the ceiling wins (``declared``); the
        # model maximum is the ``computed`` safety net when none does.
        ceiling, ceiling_provenance = self._output_ceiling()
        requested = canonical.get(OUTPUT_CEILING_KEY)
        if (
            ceiling is not None
            and isinstance(requested, int | float)
            and not isinstance(requested, bool)
            and requested > ceiling
        ):
            adjustments.append(
                Adjustment(
                    key=OUTPUT_CEILING_KEY,
                    action="clamped",
                    canonical_value=requested,
                    sent_value=ceiling,
                    provenance=ceiling_provenance,  # type: ignore[arg-type]
                    reason=(
                        f"'{OUTPUT_CEILING_KEY}'={requested!r} clamped to the "
                        + (
                            f"offering's declared output ceiling {ceiling!r}"
                            if ceiling_provenance == "declared"
                            else f"model's real output maximum {ceiling!r} "
                            "(ai.model_definition.max_tokens)"
                        )
                    ),
                )
            )
            canonical = {**canonical, OUTPUT_CEILING_KEY: ceiling}

        # Processor rules own their key + declared consumed keys — pass 1 skips both.
        #
        # `supported: false` BEATS a processor (2026-09-10): the anthropic_chat
        # API gives `temperature` a processor and the Claude 5 offerings override
        # it with supported:false; the processor still ran, temperature went on
        # the wire, and every Opus 5 call died with "temperature is deprecated
        # for this model". An unsupported processor rule drops its key AND the
        # keys it consumes, with Adjustments, and never runs.
        processor_rules = [
            (rule.processor_config.get("order", 100), key, rule)
            for key, rule in self.rules.items()
            if rule.processor is not None and rule.supported is not False and not rule.drop
        ]
        processor_owned: set[str] = set()
        for _, key, rule in processor_rules:
            processor_owned.add(key)
            processor_owned.update(rule.processor_config.get("consumes", []))
        unsupported_processor_keys: set[str] = set()
        # K6 declared drop on a processor rule: the processor never runs and its
        # key + consumed keys drop like supported:false — expected, with the why.
        declared_drop_why: dict[str, str] = {}
        for key, rule in self.rules.items():
            if rule.processor is not None and (rule.supported is False or rule.drop):
                unsupported_processor_keys.add(key)
                unsupported_processor_keys.update(rule.processor_config.get("consumes", []))
                if rule.drop:
                    for dropped_key in [key, *rule.processor_config.get("consumes", [])]:
                        declared_drop_why[dropped_key] = rule.why or ""
            elif rule.drop:
                declared_drop_why[key] = rule.why or ""
        unsupported_processor_keys -= processor_owned

        # Keys whose SET value was eliminated (map->null / unmapped drop) —
        # send_when_unset=True backfills their default below.
        eliminated: set[str] = set()
        # K6 off={"omit"}: wire(off) == wire(unset) — the defaults below treat
        # these keys as unset.
        off_omitted: set[str] = set()

        # C3c — "auto" MEANS UNSET (the chair's ruling: a posture that means
        # "not set" is never a surprise). With setting families loaded, an
        # "auto" this target cannot speak — a declared drop, supported:false,
        # or a scalar rule whose map/accepts has no place for it — is treated
        # exactly like an absent key: no drop Adjustment, no warning, the
        # rule's default applies as for any unset key. A rule that DOES speak
        # it (maps it, accepts it, sends it raw) is untouched, as are
        # processor-owned keys (processors read "auto" as unset themselves,
        # ai_041). Families absent (pre-C6 catalogs): unchanged.
        if self.families is not None:
            unset_postures = [
                key
                for key, value in canonical.items()
                if not key.startswith("_")
                and D.is_unset_posture(value)
                and key not in processor_owned
                and not self._speaks_posture(
                    key,
                    value,
                    dropped=key in declared_drop_why or key in unsupported_processor_keys,
                )
            ]
            if unset_postures:
                canonical = {k: v for k, v in canonical.items() if k not in unset_postures}

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
            if key in declared_drop_why:
                # K6 {"drop": true, "why"} — a DECLARED drop: expected, silent.
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="dropped",
                        canonical_value=value,
                        sent_value=None,
                        expected=True,
                        reason=f"'{key}' is declared dropped here: {declared_drop_why[key]}",
                    )
                )
                continue
            if rule.supported is False or key in unsupported_processor_keys:
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

            # ── K6: off · from_number · accepts · to_number ─────────────────
            if rule.off is not None and D.is_off_value(key, value):
                if rule.off.omit:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="omitted",
                            canonical_value=value,
                            sent_value=None,
                            expected=True,
                            reason=f"'{key}'={value!r} is off; declared omitted here: {rule.off.why}",
                        )
                    )
                    off_omitted.add(key)
                    continue
                if "send" in rule.off.model_fields_set:
                    if rule.off.send != value:
                        adjustments.append(
                            Adjustment(
                                key=key,
                                action="mapped",
                                canonical_value=value,
                                sent_value=rule.off.send,
                                reason=f"'{key}'={value!r} is off; declared off sends {rule.off.send!r}",
                            )
                        )
                    expand_dotted(out, rule.provider_key or key, rule.off.send)
                    continue
                floor = self._floor_value(key, rule)
                if floor is None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="dropped",
                            canonical_value=value,
                            sent_value=None,
                            expected=False,
                            provenance="computed",
                            reason=(
                                f"'{key}'={value!r} is off and declares off=floor, but this "
                                "rule names no accepted value to floor to — dropped"
                            ),
                        )
                    )
                    eliminated.add(key)
                    continue
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="mapped",
                        canonical_value=value,
                        sent_value=floor,
                        reason=f"'{key}'={value!r} is off; declared off=floor sends the lowest accepted value {floor!r}",
                    )
                )
                value = floor
            if rule.from_number and isinstance(value, int | float) and not isinstance(value, bool):
                converted = D.step_lookup(rule.from_number, value)
                if converted is None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="dropped",
                            canonical_value=value,
                            sent_value=None,
                            expected=True,
                            reason=f"'{key}'={value!r} — from_number declares this range a drop",
                        )
                    )
                    continue
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="mapped",
                        canonical_value=value,
                        sent_value=converted,
                        reason=f"'{key}'={value!r} converted to {converted!r} by from_number",
                    )
                )
                value = converted
            if rule.accepts is not None and not _is_accepted(value, rule.accepts):
                nearest = self._nearest_accepted(key, value, rule.accepts)
                if nearest is None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="dropped",
                            canonical_value=value,
                            sent_value=None,
                            expected=False,
                            provenance="computed",
                            reason=(
                                f"'{key}'={value!r} is not accepted here (accepts: "
                                f"{rule.accepts}) and has no nearest equivalent — dropped"
                            ),
                        )
                    )
                    eliminated.add(key)
                    continue
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="mapped",
                        canonical_value=value,
                        sent_value=nearest,
                        provenance="computed",
                        reason=(
                            f"'{key}'={value!r} is not accepted here (accepts: {rule.accepts}) "
                            f"— sent the nearest accepted value {nearest!r}"
                        ),
                    )
                )
                value = nearest
            if rule.to_number and isinstance(value, str):
                lookup: str | None = value if value in rule.to_number else None
                via_nearest_number = False
                if lookup is None:
                    lookup = self._nearest_in(key, value, rule.to_number)
                    via_nearest_number = lookup is not None
                if lookup is None:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="dropped",
                            canonical_value=value,
                            sent_value=None,
                            expected=False,
                            provenance="computed",
                            reason=(
                                f"'{key}'={value!r} has no to_number entry and no nearest "
                                "one — dropped"
                            ),
                        )
                    )
                    eliminated.add(key)
                    continue
                number = rule.to_number[lookup]
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="mapped",
                        canonical_value=value,
                        sent_value=number,
                        provenance="computed" if via_nearest_number else "declared",
                        reason=f"'{key}'={value!r} converted to {number!r} by to_number",
                    )
                )
                value = number

            sent = value
            if (
                rule.to_default is not None
                and isinstance(value, str)
                and not rule.to_number
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
            if rule.value_map is not None and isinstance(value, str) and not rule.to_number:
                lookup = value
                # K9: a value the map names is DECLARED; one the nearest
                # metric picked is COMPUTED.
                via_nearest = False
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
                            via_nearest = True
                        else:
                            adjustments.append(
                                Adjustment(
                                    key=key,
                                    action="dropped",
                                    canonical_value=value,
                                    sent_value=None,
                                    expected=False,
                                    provenance="computed",
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
                            provenance="computed" if via_nearest else "declared",
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
                            provenance="computed" if via_nearest else "declared",
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
            if rule.const is None or key in processor_owned or rule.drop:
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
                or rule.drop
                or rule.default is None
                or rule.const is not None
                or rule.processor is not None
            ):
                continue
            value_was_set = canonical.get(key) is not None and key not in off_omitted
            if value_was_set and not (rule.send_when_unset and key in eliminated):
                continue
            target = rule.provider_key or key
            present, _ = _dotted_get(out, target)
            if not present:
                expand_dotted(out, target, rule.default)

        # A DEFAULT is a value too: a ceiling default authored for a bigger model
        # is capped like a caller's (pass 0 only saw the caller's value).
        ceiling_rule = self.rule_for(OUTPUT_CEILING_KEY)
        if ceiling is not None and OUTPUT_CEILING_KEY not in processor_owned:
            target = ceiling_rule.provider_key or OUTPUT_CEILING_KEY
            present, sent = _dotted_get(out, target)
            if (
                present
                and isinstance(sent, int | float)
                and not isinstance(sent, bool)
                and sent > ceiling
            ):
                expand_dotted(out, target, ceiling)

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
            # K6 off / accepts act on the canonical value BEFORE the processor
            # (from_number / to_number are read by the processor off ctx.rule).
            off_send: tuple[bool, Any] = (False, None)
            incoming = canonical.get(key)
            converted = key in (canonical.get("_converted") or {})
            if rule.off is not None and not converted and D.is_off_value(key, incoming):
                if rule.off.omit:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="omitted",
                            canonical_value=incoming,
                            sent_value=None,
                            expected=True,
                            reason=f"'{key}'={incoming!r} is off; declared omitted here: {rule.off.why}",
                        )
                    )
                    canonical = {k: v for k, v in canonical.items() if k != key}
                elif "send" in rule.off.model_fields_set:
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="mapped",
                            canonical_value=incoming,
                            sent_value=rule.off.send,
                            reason=f"'{key}'={incoming!r} is off; declared off sends {rule.off.send!r}",
                        )
                    )
                    canonical = {k: v for k, v in canonical.items() if k != key}
                    off_send = (True, rule.off.send)
                else:
                    floor = self._floor_value(key, rule)
                    adjustments.append(
                        Adjustment(
                            key=key,
                            action="mapped" if floor is not None else "dropped",
                            canonical_value=incoming,
                            sent_value=floor,
                            expected=floor is not None,
                            provenance="declared" if floor is not None else "computed",
                            reason=(
                                f"'{key}'={incoming!r} is off; declared off=floor sends the "
                                f"lowest accepted value {floor!r}"
                                if floor is not None
                                else f"'{key}'={incoming!r} is off=floor with no accepted value — dropped"
                            ),
                        )
                    )
                    canonical = (
                        {**canonical, key: floor}
                        if floor is not None
                        else {k: v for k, v in canonical.items() if k != key}
                    )
            incoming = canonical.get(key)
            if (
                rule.accepts is not None
                and incoming is not None
                and not converted
                and not _is_accepted(incoming, rule.accepts)
            ):
                nearest = self._nearest_accepted(key, incoming, rule.accepts)
                adjustments.append(
                    Adjustment(
                        key=key,
                        action="mapped" if nearest is not None else "dropped",
                        canonical_value=incoming,
                        sent_value=nearest,
                        expected=nearest is not None,
                        provenance="computed",
                        reason=(
                            f"'{key}'={incoming!r} is not accepted here (accepts: {rule.accepts}) "
                            + (
                                f"— the processor got the nearest accepted value {nearest!r}"
                                if nearest is not None
                                else "and has no nearest equivalent — dropped"
                            )
                        ),
                    )
                )
                canonical = (
                    {**canonical, key: nearest}
                    if nearest is not None
                    else {k: v for k, v in canonical.items() if k != key}
                )
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
                # K6: ``accepts`` (capability) when declared, else ui_values —
                # the pre-C5 contract, unchanged for rules without accepts.
                supported_values=frozenset(
                    str(v)
                    for v in (rule.accepts if rule.accepts is not None else (rule.ui_values or ()))
                ),
                value_order=tuple(
                    str(v) for v in self.value_orders.get(key, ()) if isinstance(v, str)
                ),
                output_maximum=(int(ceiling) if ceiling is not None else None),
                rule=rule,
                accepts=frozenset(str(v) for v in (rule.accepts or ())),
            )
            result = fn(canonical, out, ctx)
            if result is not None:
                out = result
            if off_send[0]:
                expand_dotted(out, rule.provider_key or key, off_send[1])

        return out, self.stamp_cells(adjustments)

    def stamp_cells(self, adjustments: list[Adjustment]) -> list[Adjustment]:
        """K9: stamp each Adjustment with the cell that decided its key.

        A no-op (same list back) while no cells are loaded — copy mode reads
        ai.api.rules / ai.offering.override, which have no cells."""
        if not self.cells:
            return adjustments
        stamped: list[Adjustment] = []
        for adj in adjustments:
            cell = self.cells.get(adj.key)
            if cell is None or adj.cell_id is not None:
                stamped.append(adj)
                continue
            stamped.append(
                adj.model_copy(
                    update={"cell_id": cell.cell_id, "layer": cell.layer, "cell_state": cell.state}
                )
            )
        return stamped

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
    "compile_controls_from_cells",
    "select_cells_from_view",
    "LAYER_PRECEDENCE",
    "VIEW_ROW_FIELDS",
    "ViewRowError",
    "merge_rule_dicts",
    "validate_rules_against_settings",
    "expand_dotted",
    "flatten_dotted",
]
