"""K7 SETTING FAMILIES — a setting the target does not carry converts through
its family instead of vanishing (settings-translation item C6).

Arman, 2026-10-02: *"If I send a request to Opus with thinking levels set to
extremely high … to the image generation model. My request should go through,
and the thinking level should be converted to image resolution."*

Every ``ai.setting`` row names a FAMILY (``platform.categories`` dimension
``ai_setting_family``: intensity, length, randomness, shape, count, format,
voice, visibility, none) and an ordinal setting gives each canonical value a
POSITION 0..1 (``ai.setting.value_positions``). A canonical key the TARGET does
not natively carry — no rule and no processor claim, or a rule that says
``supported: false`` (K6: "not native here, convert through the family") —
converts to a sibling the target DOES carry:

    source value -> position -> the sibling's nearest accepted value

* Strings take their own position. A NUMBER reaches a position through the
  target's tables: the sibling's own ``from_number`` when it declares one,
  else the family's number -> scale bridge (``thinking_budget`` ->
  ``reasoning_effort`` steps, translation_defaults) and that scale's position.
  A numeric sibling is reached through its ``to_number`` table. ``True`` is
  position 1.0.
* OFF (``reasoning_effort="none"``, a budget <= 0, ``False``) has no position:
  it converts only to a sibling that can say off, else it is dropped silently
  — turning nothing off on a target that has nothing to turn off loses nothing.
* PRECEDENCE (K7): a sibling the caller set directly beats every conversion;
  when several sources convert into one sibling, the highest position wins.
* Each source converts into ONE sibling, preferring the one that speaks its
  own vocabulary (``high`` -> quality ``high``), then any positioned sibling,
  then numeric, then boolean; ties by key.
* Only a declared ``{"drop": true}`` (outbound handles it) or a family with no
  member that can carry the value drops — and that drop is UNEXPECTED
  (``expected=False``): the caller gets the one warning per request.

Conversions are silent to the client (THE EQUIVALENCE LAW) and recorded as
``Adjustment(key=<sibling>, action="mapped", converted_from=<source>)``.
Pure: no DB, no I/O. ``CompiledControlsMap.translate_foreign`` is the caller.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.models import Adjustment, CatalogSetting

if TYPE_CHECKING:
    from matrx_ai.catalog.controls import CompiledControlsMap

# The family that means "this setting has no siblings" (K7 ``none``).
NO_SIBLINGS_FAMILY = "none"
_NUMERIC_TYPES = frozenset({"number", "integer"})


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


class SettingFamilies(BaseModel):
    """The family + position data of every ``ai.setting``, built once per
    catalog load and shared (by reference) by every compiled map."""

    model_config = ConfigDict(frozen=True)

    family_of: dict[str, str] = {}
    members: dict[str, tuple[str, ...]] = {}
    positions: dict[str, dict[str, float]] = {}
    value_types: dict[str, str] = {}
    vocab: dict[str, tuple[str, ...]] = {}

    @classmethod
    def from_settings(cls, settings: dict[str, CatalogSetting]) -> SettingFamilies | None:
        """``None`` when no setting names a family — family data absent."""
        family_of = {key: s.family for key, s in settings.items() if s.family}
        if not family_of:
            return None
        members: dict[str, list[str]] = {}
        for key, family in sorted(family_of.items()):
            members.setdefault(family, []).append(key)
        positions: dict[str, dict[str, float]] = {}
        for key, s in settings.items():
            table = {
                str(value): float(position)
                for value, position in (s.value_positions or {}).items()
                if _is_number(position)
            }
            if table:
                positions[key] = table
        return cls(
            family_of=family_of,
            members={family: tuple(keys) for family, keys in members.items()},
            positions=positions,
            value_types={key: s.value_type for key, s in settings.items()},
            vocab={
                key: tuple(str(v) for v in s.canonical_values)
                for key, s in settings.items()
                if s.canonical_values
            },
        )

    def siblings(self, key: str) -> tuple[str, ...]:
        family = self.family_of.get(key)
        if family is None or family == NO_SIBLINGS_FAMILY:
            return ()
        return tuple(k for k in self.members.get(family, ()) if k != key)

    def nearest_by_position(self, key: str, value: Any, candidates: Iterable[Any]) -> str | None:
        """Nearest candidate by POSITION (``ai.setting.value_positions``), ties
        toward the higher position — never silently weaken what was asked.
        ``None`` when ``key`` or ``value`` has no position (the caller then
        uses the setting's own metric)."""
        table = self.positions.get(key)
        if not table or not isinstance(value, str) or value not in table:
            return None
        return _nearest(table, table[value], candidates)


def _nearest(table: dict[str, float], target: float, candidates: Iterable[Any]) -> str | None:
    best: str | None = None
    best_rank: tuple[float, float, str] | None = None
    for candidate in candidates:
        token = str(candidate)
        if token not in table:
            continue
        rank = (abs(table[token] - target), -table[token], token)
        if best_rank is None or rank < best_rank:
            best, best_rank = token, rank
    return best


def _off_value(
    controls: CompiledControlsMap, families: SettingFamilies, key: str
) -> tuple[bool, Any]:
    """(True, the value that means OFF for ``key``) when ``key`` can say off."""
    if key in D.OFF_AT_OR_BELOW:
        return True, 0
    for off in D.OFF_VALUES.get(key, ()):
        if isinstance(off, bool) or controls.rule_for(key).off is not None:
            return True, off
        if str(off) in families.vocab.get(key, ()):
            return True, off
    return False, None


def _accepted_pool(controls: CompiledControlsMap, families: SettingFamilies, key: str) -> list[str]:
    rule = controls.rule_for(key)
    pool: list[Any] | None = rule.accepts or rule.ui_values
    if pool is None and rule.value_map:
        pool = [k for k, v in rule.value_map.items() if v is not None]
    table = families.positions.get(key, {})
    # A DEGREE never converts into an OFF ("show thoughts" must not become
    # reasoning_summary="never"): off values are not conversion targets.
    offs = {str(v) for v in D.OFF_VALUES.get(key, ())}
    candidates = [str(v) for v in (pool or table) if str(v) in table and str(v) not in offs]
    if pool is None and not candidates:
        candidates = [v for v in table if v not in offs]
    return candidates


def _word_position(families: SettingFamilies, source: str, word: str) -> float | None:
    if word in families.positions.get(source, {}):
        return families.positions[source][word]
    family = families.family_of.get(source)
    for member in families.members.get(family or "", ()):
        if word in families.positions.get(member, {}):
            return families.positions[member][word]
    return None


def _number_position(
    controls: CompiledControlsMap, families: SettingFamilies, source: str, number: float
) -> float | None:
    """A number's position through its family's number -> scale bridge (the
    target's ``from_number`` for the bridge scale, else the declared default)."""
    bridge = D.NUMBER_TO_SCALE_BRIDGES.get(source)
    if bridge is None:
        return None
    steps = controls.rule_for(bridge).from_number or D.DEFAULT_FROM_NUMBER.get(bridge)
    word = D.step_lookup(steps, number) if steps else None
    if word is None:
        return None
    return families.positions.get(bridge, {}).get(str(word))


def _convert_value(
    controls: CompiledControlsMap,
    families: SettingFamilies,
    source: str,
    value: Any,
    target: str,
) -> tuple[Any, float, str] | None:
    """(value for ``target``, its position, provenance) or None."""
    rule = controls.rule_for(target)
    target_table = families.positions.get(target, {})
    if _is_number(value):
        bridge = D.NUMBER_TO_SCALE_BRIDGES.get(source)
        if rule.from_number or bridge == target:
            steps = rule.from_number or D.DEFAULT_FROM_NUMBER.get(target)
            word = D.step_lookup(steps, value) if steps else None
            if word is None:
                return None
            provenance = "declared" if rule.from_number else "computed"
            return word, target_table.get(str(word), 0.0), provenance
        position = _number_position(controls, families, source, value)
    elif isinstance(value, bool):
        position = 1.0 if value else None
    elif isinstance(value, str):
        position = families.positions.get(source, {}).get(value)
    else:
        position = None
    if position is None:
        return None

    if target_table:
        choice = _nearest(target_table, position, _accepted_pool(controls, families, target))
        if choice is None:
            return None
        return choice, target_table[choice], "computed"
    value_type = families.value_types.get(target)
    if value_type in _NUMERIC_TYPES and rule.to_number:
        words = {
            word: wp
            for word in rule.to_number
            if (wp := _word_position(families, source, word)) is not None
        }
        word = _nearest(words, position, words)
        if word is None:
            return None
        return rule.to_number[word], words[word], "declared"
    if value_type == "boolean":
        return position >= 0.5, position, "computed"
    return None


def declared_value_drop(controls: CompiledControlsMap, key: str, value: Any) -> str | None:
    """The ``why`` when ``key``'s own rule DECLARES this value a drop on this
    target, else None (settings-translation C3c — a per-value declared gap).

    The rule's value-level forms, read for a key the target does not carry
    natively: a ``value_map`` entry pointing at null (enums; a boolean reads as
    ``"true"`` / ``"false"``) or a ``from_number`` step whose ``to`` is null
    (numbers). Such a value is someone's written-down decision that it has no
    home here — dropped silently (expected), never a warning."""
    rule = controls.rules.get(key)
    if rule is None:
        return None
    if _is_number(value):
        if rule.from_number and D.step_lookup(rule.from_number, value) is None:
            return rule.why or f"'{key}'={value!r} is declared dropped here (from_number)"
        return None
    token = str(value).lower() if isinstance(value, bool) else value
    if (
        isinstance(token, str)
        and rule.value_map is not None
        and token in rule.value_map
        and rule.value_map[token] is None
    ):
        return rule.why or f"'{key}'={value!r} is declared dropped here (value_map)"
    return None


def _rank(families: SettingFamilies, value: Any, target: str) -> tuple[int, str]:
    table = families.positions.get(target)
    if table and isinstance(value, str) and value in table:
        tier = 0
    elif table:
        tier = 1
    elif families.value_types.get(target) in _NUMERIC_TYPES:
        tier = 2
    elif families.value_types.get(target) == "boolean":
        tier = 3
    else:
        tier = 4
    return tier, target


def convert_through_families(
    controls: CompiledControlsMap,
    canonical: dict[str, Any],
    sources: list[str],
) -> tuple[dict[str, Any], list[Adjustment]]:
    """Convert every key in ``sources`` (not natively carried by ``controls``)
    through its family. Returns the new canonical dict and the Adjustments.

    An UNDECLARED source (no rule, no processor claim) is always removed — it
    would otherwise ride PASSTHROUGH_RULE onto the wire. A DECLARED one
    (``supported: false``) that converted or was outranked stays in the dict,
    so ``outbound`` drops it exactly as before C6 (a processor reading the raw
    value sees what it always saw); one that cannot convert at all is removed
    with the UNEXPECTED drop. A raw number with a declared scale bridge
    (``thinking_budget`` -> ``reasoning_effort``) converts through that bridge
    exactly as ``bridge_numbers`` does, ``_converted`` marker included."""
    families = controls.families
    assert families is not None
    out = dict(canonical)
    adjustments: list[Adjustment] = []
    directly_set = {k for k, v in canonical.items() if v is not None and not k.startswith("_")}
    # target -> [(position, source, value, provenance, via_bridge)]
    proposals: dict[str, list[tuple[float, str, Any, str, bool]]] = {}
    requested = canonical.get("_convert") or {}

    def drop(
        key: str,
        value: Any,
        *,
        expected: bool,
        why: str,
        declared: bool = False,
        law: str | None = None,
    ) -> None:
        # A per-value DECLARED drop (C3c) leaves the dict exactly as the
        # unexpected drop it replaces did — only the verdict changes.
        if key in out and (declared or not expected or not controls._declares(key)):
            out.pop(key)
        adjustments.append(
            Adjustment(
                key=key,
                action="dropped",
                canonical_value=value,
                sent_value=None,
                expected=expected,
                provenance="declared" if declared else "computed",
                law=law,
                reason=f"'{key}'={value!r} is not carried by this api/offering; {why}",
            )
        )

    for source in sources:
        value = canonical[source]
        if not controls._declares(source):
            out.pop(source, None)  # never onto the wire under its own name
        family = families.family_of.get(source)
        carried = [s for s in families.siblings(source) if controls.carries(s)]
        declared_why = declared_value_drop(controls, source, value)
        if not carried and declared_why is not None:
            drop(source, value, expected=True, why=f"declared: {declared_why}", declared=True)
            continue
        if not carried:
            drop(
                source,
                value,
                expected=False,
                why=(
                    f"its family {family!r} has no member here — dropped"
                    if family and family != NO_SIBLINGS_FAMILY
                    else "it has no setting family to convert through — dropped"
                ),
            )
            continue
        spoken = sorted(s for s in carried if s in directly_set)
        if spoken:
            # The caller already said, in this target's own terms, how hard /
            # how long / how visible — that beats any conversion (K7).
            drop(
                source,
                value,
                expected=True,
                why=f"the caller set its sibling(s) {spoken} directly, which win",
                law="K7",
            )
            continue
        free = sorted(carried, key=lambda s: _rank(families, value, s))
        bridge = D.NUMBER_TO_SCALE_BRIDGES.get(source)
        if bridge in free and _is_number(value) and requested.get(bridge) == source:
            # The declared number -> scale bridge (bridge_numbers' semantics).
            rule = controls.rule_for(bridge)
            steps = rule.from_number or D.DEFAULT_FROM_NUMBER.get(bridge)
            word = D.step_lookup(steps, value) if steps else None
            if word is None:
                drop(source, value, expected=True, why=f"'{bridge}' from_number declares a drop")
                continue
            position = families.positions.get(bridge, {}).get(str(word), -1.0)
            provenance = "declared" if rule.from_number else "computed"
            proposals.setdefault(bridge, []).append((position, source, word, provenance, True))
            continue
        if value is False or D.is_off_value(source, value):
            for target in free:
                can_say_off, off = _off_value(controls, families, target)
                if can_say_off:
                    proposals.setdefault(target, []).append((-1.0, source, off, "computed", False))
                    break
            else:
                drop(
                    source,
                    value,
                    expected=True,
                    why=f"it means off and no {family!r} sibling here can say off — nothing to turn off",
                    # An off with nothing to turn off loses nothing the caller asked for.
                    law="K7",
                )
            continue
        for target in free:
            got = _convert_value(controls, families, source, value, target)
            if got is not None:
                converted, position, provenance = got
                proposals.setdefault(target, []).append(
                    (position, source, converted, provenance, False)
                )
                break
        else:
            if declared_why is not None:
                drop(source, value, expected=True, why=f"declared: {declared_why}", declared=True)
                continue
            drop(
                source,
                value,
                expected=False,
                why=f"no {family!r} sibling here ({sorted(free)}) can express it — dropped",
            )

    for target in sorted(proposals):
        ranked = sorted(proposals[target], key=lambda p: (-p[0], p[1]))
        _, source, converted, provenance, via_bridge = ranked[0]
        out[target] = converted
        if via_bridge and controls._declares(source):
            # A processor owning the raw number reads it, not the converted
            # scale value — exactly as after bridge_numbers.
            out["_converted"] = {**(out.get("_converted") or {}), target: source}
        adjustments.append(
            Adjustment(
                key=target,
                action="mapped",
                canonical_value=canonical[source],
                sent_value=converted,
                expected=True,
                provenance=provenance,  # type: ignore[arg-type]
                converted_from=source,
                reason=(
                    f"'{source}'={canonical[source]!r} is not carried by this api/offering — "
                    f"converted through the {families.family_of.get(source)!r} family to "
                    f"'{target}'={converted!r}"
                ),
            )
        )
        for _, loser, _, _, _ in ranked[1:]:
            drop(
                loser,
                canonical[loser],
                expected=True,
                why=f"'{source}' converts into '{target}' from a higher position and wins (K7)",
                law="K7",
            )
    return out, adjustments


__all__ = [
    "NO_SIBLINGS_FAMILY",
    "SettingFamilies",
    "convert_through_families",
    "declared_value_drop",
]
