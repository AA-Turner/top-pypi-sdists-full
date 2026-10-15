"""Total-order comparator: unit tests, mutation checks and a differential test.

``spec_kitty_events.total_order`` is checked against

* hand-written unit cases for each parsing rule;
* five mutants of the comparator (the naive one of worked example 4 and four others),
  each of which must be caught by the packaged fixtures;
* an independent reference implementation, written here from ``contracts/total-order.md``
  without sharing code with the library, on random rows (hypothesis).
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from spec_kitty_events import total_order
from spec_kitty_events.total_order import (
    CLOCK_MAX,
    ERROR_REASONS,
    UnorderableRow,
    order_key,
    order_rows,
)

_FIXTURES = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "spec_kitty_events"
    / "producer_contract"
    / "fixtures"
    / "total_order"
)
P = "01J00000000000000000000"
A, B, C = P + "ABA", P + "ABB", P + "ABC"


def _row(**members: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {"id": A, "time": "2026-10-13T10:00:00Z"}
    base.update(members)
    return base


def _ser(row: Any) -> bytes:
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


# --------------------------------------------------------------------- parsing rules
@pytest.mark.parametrize(
    "stamp",
    [
        "2026-10-13T10:00:00Z",
        "2026-10-13t10:00:00z",
        "2026-10-13T10:00:00+00:00",
        "2026-10-13T12:00:00+02:00",
        "2026-10-13T10:00:00-00:00",
        "2028-02-29T00:00:00Z",
        "2026-06-30T23:59:60Z",
        "2026-10-13T10:00:00.123456789Z",
        "0001-01-01T00:00:00Z",
        "9999-12-31T23:59:59Z",
        "2026-10-13T10:00:00+23:59",
    ],
)
def test_time_forms_that_parse(stamp: str) -> None:
    order_key(_row(time=stamp))


@pytest.mark.parametrize(
    "stamp",
    [
        "",
        "yesterday",
        "2026-10-13",
        "2026-10-13T10:00:00",
        "2026-10-13 10:00:00Z",
        "20261013T100000Z",
        "2026-13-01T00:00:00Z",
        "2027-02-29T00:00:00Z",
        "2026-10-13T24:00:00Z",
        "2026-10-13T10:60:00Z",
        "2026-10-13T10:00:61Z",
        "2026-10-13T10:00:00.1234567890Z",
        "2026-10-13T10:00:00.Z",
        "2026-10-13T10:00:00+24:00",
        "2026-10-13T10:00:00+00:60",
        "2026-10-13T10:00:00+0200",
        "0000-01-01T00:00:00Z",
        " 2026-10-13T10:00:00Z",
        "2026-10-13T10:00:00Z ",
        "２０２６-10-13T10:00:00Z",
    ],
)
def test_time_forms_that_do_not_parse(stamp: str) -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key(_row(time=stamp))
    assert caught.value.reason == "time_unparseable"


@pytest.mark.parametrize("value", [None, 5, True, ["2026-10-13T10:00:00Z"]])
def test_time_that_is_not_a_string(value: Any) -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key(_row(time=value))
    assert caught.value.reason == "time_unparseable"


def test_time_member_absent() -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key({"id": A})
    assert caught.value.reason == "time_unparseable"


def test_instants_are_compared_exactly_not_by_text_or_rounding() -> None:
    assert (
        order_key(_row(time="2026-10-13T12:00:00+02:00"))[2]
        == order_key(_row(time="2026-10-13T10:00:00Z"))[2]
    )
    assert (
        order_key(_row(time="2026-10-13T10:00:00.000000001Z"))[2]
        > order_key(_row(time="2026-10-13T10:00:00Z"))[2]
    )
    assert (
        order_key(_row(time="2026-06-30T23:59:60Z"))[2]
        == order_key(_row(time="2026-07-01T00:00:00Z"))[2]
    )
    assert (
        order_key(_row(time="2026-10-13T10:00:00.5Z"))[2] == Fraction(1, 2) + order_key(_row())[2]
    )


@pytest.mark.parametrize("value", [0, 1, CLOCK_MAX])
def test_clock_that_is_valid(value: int) -> None:
    assert order_key(_row(lamportclock=value))[:2] == (1, value)


@pytest.mark.parametrize(
    "value", [-1, CLOCK_MAX + 1, 2**63, None, True, False, "5", 5.0, 1e3, [1], {"v": 1}]
)
def test_clock_that_is_present_and_invalid(value: Any) -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key(_row(lamportclock=value))
    assert caught.value.reason == "clock_out_of_range"


def test_clock_absent_is_clockless_and_sorts_first() -> None:
    assert order_key(_row())[:2] == (0, 0)
    assert order_key(_row()) < order_key(_row(lamportclock=0))


@pytest.mark.parametrize("value", [None, "", 5, True, [], {}])
def test_id_missing(value: Any) -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key(_row(id=value) if value is not None else {"time": "2026-10-13T10:00:00Z"})
    assert caught.value.reason in {"id_missing", "id_not_normalizable"}
    if value in (None, ""):
        assert caught.value.reason == "id_missing"


@pytest.mark.parametrize(
    "value",
    [
        "nope",
        P + "ABI",
        P + "ABL",
        P + "ABO",
        P + "ABU",
        "0190a1b2c3d4",
        "0190a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5",
        P + "AB",
    ],
)
def test_id_that_does_not_normalize(value: str) -> None:
    with pytest.raises(UnorderableRow) as caught:
        order_key(_row(id=value))
    assert caught.value.reason == "id_not_normalizable"


def test_ids_normalize() -> None:
    assert order_key(_row(id=(P + "abc")))[3] == C
    assert (
        order_key(_row(id="0190A1B2-C3D4-7E5F-8A9B-0C1D2E3F4A5B"))[3]
        == "0190a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"
    )
    assert (
        order_key(_row(id="0190A1B2C3D47E5F8A9B0C1D2E3F4A5B"))[3]
        == "0190a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"
    )


def test_source_forms() -> None:
    assert order_key(_row())[4] == ""
    assert order_key(_row(source=None))[4] == ""
    assert order_key(_row(source=""))[4] == ""
    assert order_key(_row(source="/spec-kitty/missions/M"))[4] == "/spec-kitty/missions/M"
    for value in (5, True, ["x"], {"a": 1}):
        with pytest.raises(UnorderableRow) as caught:
            order_key(_row(source=value))
        assert caught.value.reason == "source_invalid"


def test_row_that_is_not_an_object() -> None:
    for value in (None, 5, "x", [], True):
        with pytest.raises(UnorderableRow) as caught:
            order_key(value)  # type: ignore[arg-type]
        assert caught.value.reason == "row_not_object"


def test_reason_for_a_row_with_several_defects_is_deterministic() -> None:
    row = {"id": "nope", "time": "yesterday", "lamportclock": -1, "source": 5}
    with pytest.raises(UnorderableRow) as caught:
        order_key(row)
    assert caught.value.reason == "id_not_normalizable"
    row["id"] = A
    with pytest.raises(UnorderableRow) as caught:
        order_key(row)
    assert caught.value.reason == "clock_out_of_range"
    row["lamportclock"] = 1
    with pytest.raises(UnorderableRow) as caught:
        order_key(row)
    assert caught.value.reason == "time_unparseable"


def test_source_compares_by_code_point_not_utf16() -> None:
    # U+FF5E (BMP) sorts before U+1F600 (astral) by code point; in UTF-16 the astral
    # lead surrogate 0xD83D sorts before 0xFF5E, so a UTF-16 comparator gets this wrong.
    low, high = "\uff5e", "\U0001f600"
    assert low < high
    result = order_rows([_row(source=high), _row(source=low)])
    assert [r["source"] for r in result.ordered] == [low, high]


# ----------------------------------------------------------------------- result shape
def test_result_accounts_for_every_row() -> None:
    rows = [_row(), _row(id="nope"), _row(), _row(id=B, time="x"), _row(id=B, lamportclock=1)]
    result = order_rows(rows)
    assert len(result.ordered) + len(result.errors) + result.collapsed == result.read == 5
    assert [e.position for e in result.errors] == [1, 3]
    assert {e.reason for e in result.errors} <= ERROR_REASONS


def test_error_rows_keep_their_input_position_and_row() -> None:
    bad = _row(time="soon")
    result = order_rows([_row(id=B), bad])
    assert result.errors[0].position == 1
    assert result.errors[0].row is bad


def test_empty_input() -> None:
    result = order_rows([])
    assert (result.ordered, result.errors, result.collapsed, result.conflicts, result.read) == (
        (),
        (),
        0,
        (),
        0,
    )


def test_accepts_any_iterable() -> None:
    assert len(order_rows(iter([_row(id=A), _row(id=B)])).ordered) == 2


def test_identical_rows_collapse_without_a_conflict() -> None:
    result = order_rows([_row(), _row(), _row()])
    assert (len(result.ordered), result.collapsed, result.conflicts) == (1, 2, ())


def test_rows_that_differ_beyond_id_conflict_and_the_smaller_bytes_survive() -> None:
    low, high = _row(data={"x": 1}), _row(data={"y": 1})
    for rows in ([low, high], [high, low]):
        result = order_rows(rows)
        assert result.ordered == (low,)
        assert result.conflicts == (("", A),)
        assert result.collapsed == 1


def test_json_one_and_true_and_one_point_zero_are_different_members() -> None:
    # Python equates 1, 1.0 and True; the conflict test must not.
    result = order_rows([_row(data={"x": 1}), _row(data={"x": True}), _row(data={"x": 1.0})])
    assert result.conflicts == (("", A),)
    assert result.collapsed == 2


def test_same_id_in_two_sources_are_two_rows() -> None:
    result = order_rows([_row(source="/b"), _row(source="/a")])
    assert [r["source"] for r in result.ordered] == ["/a", "/b"]
    assert result.collapsed == 0


def test_canonical_form_ignores_position_but_not_content() -> None:
    first = order_rows([_row(), _row(id="nope", extra=1), _row(id=B)])
    second = order_rows([_row(id=B), _row(), _row(id="nope", extra=1)])
    assert first.canonical() == second.canonical()
    assert (
        first.canonical() != order_rows([_row(), _row(id="nope", extra=2), _row(id=B)]).canonical()
    )


# ------------------------------------------------------- mutants, caught by the fixtures
def _load_cases() -> List[Dict[str, Any]]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(_FIXTURES.glob("*.json"))]


def _case_fails(order: Callable[[Sequence[Any]], Any], case: Dict[str, Any]) -> bool:
    """True if ``order`` gives a result other than the case's pinned one for the case's rows."""
    labelled = case["rows"]
    rows = [item["row"] for item in labelled]
    labels = [item["label"] for item in labelled]
    by_label = {item["label"]: item["row"] for item in labelled}
    expected = case["expected"]
    try:
        result = order(rows)
        ordered = [_ser(r) for r in result.ordered]
        errors = sorted((labels[e.position], e.reason) for e in result.errors)
        return not (
            ordered == [_ser(by_label[name]) for name in expected["ordered"]]
            and errors == sorted(expected["errors"].items())
            and result.collapsed == expected["collapsed"]
            and [list(k) for k in result.conflicts] == sorted(expected["conflicts"])
        )
    except Exception:
        return True


def _naive(rows: Sequence[Any]) -> Any:
    """Worked example 4: clock only when both rows have one, else (time, id). Not transitive."""
    import functools

    keyed = []
    for row in rows:
        try:
            keyed.append((row, order_key(row)))
        except UnorderableRow:
            pass

    def compare(x: Tuple[Any, Tuple[Any, ...]], y: Tuple[Any, Tuple[Any, ...]]) -> int:
        kx, ky = x[1], y[1]
        both = kx[0] == 1 and ky[0] == 1
        a = (kx[1], kx[2], kx[3]) if both else (kx[2], kx[3])
        b = (ky[1], ky[2], ky[3]) if both else (ky[2], ky[3])
        return (a > b) - (a < b)

    ordered = tuple(r for r, _ in sorted(keyed, key=functools.cmp_to_key(compare)))
    return total_order.OrderResult(
        ordered=ordered, errors=(), collapsed=0, conflicts=(), read=len(rows)
    )


def _patched(monkeypatch: pytest.MonkeyPatch, **changes: Any) -> Callable[[Sequence[Any]], Any]:
    for name, value in changes.items():
        monkeypatch.setattr(total_order, name, value)
    return order_rows


def test_mutant_naive_comparator_is_caught_by_example_4() -> None:
    assert any(_case_fails(_naive, c) for c in _load_cases() if c["id"].startswith("04-"))


def test_mutant_without_source_is_caught_by_example_7(monkeypatch: pytest.MonkeyPatch) -> None:
    original = total_order.order_key

    def no_source(row: Any) -> Any:
        key = original(row)
        return key[:4] + ("",)

    order = _patched(monkeypatch, order_key=no_source)
    assert any(_case_fails(order, c) for c in _load_cases() if c["id"].startswith("07-"))


def test_mutant_raw_id_dedupe_is_caught_by_example_8(monkeypatch: pytest.MonkeyPatch) -> None:
    original = total_order.order_key

    def raw_id(row: Any) -> Any:
        key = original(row)
        return key[:3] + (str(row["id"]),) + key[4:]

    order = _patched(monkeypatch, order_key=raw_id)
    assert any(_case_fails(order, c) for c in _load_cases() if c["id"].startswith("08-"))


def test_mutant_invalid_duplicate_survives_is_caught_by_example_9() -> None:
    """Dedupe first on raw (source, id), keep the smallest bytes, then validate the survivor."""

    def survivor_before_validation(rows: Sequence[Any]) -> Any:
        groups: Dict[Tuple[Any, Any], List[Any]] = {}
        for row in rows:
            if isinstance(row, dict):
                groups.setdefault((row.get("source"), str(row.get("id", "")).upper()), []).append(
                    row
                )
        survivors = [min(members, key=_ser) for members in groups.values()]
        return order_rows(survivors)

    assert any(
        _case_fails(survivor_before_validation, c)
        for c in _load_cases()
        if c["id"].startswith("09-")
    )


def test_mutant_dropping_error_rows_is_caught_by_examples_6_and_9() -> None:
    def drop_errors(rows: Sequence[Any]) -> Any:
        result = order_rows(rows)
        return total_order.OrderResult(
            ordered=result.ordered,
            errors=(),
            collapsed=result.collapsed,
            conflicts=result.conflicts,
            read=result.read,
        )

    failing = {c["id"][:2] for c in _load_cases() if _case_fails(drop_errors, c)}
    assert {"06", "09"} <= failing


def test_mutant_bool_clock_is_caught_by_the_clock_case(monkeypatch: pytest.MonkeyPatch) -> None:
    def lenient_clock(row: Any) -> Any:
        if "lamportclock" not in row:
            return (0, 0)
        value = row["lamportclock"]
        if not isinstance(value, int) or not 0 <= value <= CLOCK_MAX:  # accepts True
            raise UnorderableRow("clock_out_of_range")
        return (1, int(value))

    order = _patched(monkeypatch, _clock=lenient_clock)
    assert any(_case_fails(order, c) for c in _load_cases() if c["id"].startswith("10-"))


def test_mutant_truncating_fractions_is_caught_by_the_time_case(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = total_order._parse_instant

    def micro(value: Any) -> Fraction:
        instant = original(value)
        return Fraction(int(instant * 1_000_000), 1_000_000)  # rounds nanoseconds away

    order = _patched(monkeypatch, _parse_instant=micro)
    case = {
        "id": "x",
        "rows": [
            {"label": "L", "row": _row(id=B, time="2026-10-13T10:00:00.000000002Z")},
            {"label": "M", "row": _row(id=A, time="2026-10-13T10:00:00.000000009Z")},
        ],
        "expected": {
            "ordered": ["L", "M"],
            "errors": {},
            "collapsed": 0,
            "conflicts": [],
            "read": 2,
        },
    }
    assert _case_fails(order, case)  # ids would put M first once the nanoseconds are lost


# ------------------------------------------------------------ independent reference
_RFC = re.compile(
    r"^(\d{4})-(\d\d)-(\d\d)[Tt](\d\d):(\d\d):(\d\d)(?:\.(\d{1,9}))?([Zz]|[+-]\d\d:\d\d)$"
)
_ULID = re.compile(r"^[0-9A-HJKMNP-TV-Za-hjkmnp-tv-z]{26}$")
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_HEX = re.compile(r"^[0-9a-fA-F]{32}$")


def _ref_instant(value: Any) -> Optional[Fraction]:
    if not isinstance(value, str):
        return None
    m = _RFC.match(value)
    if not m:
        return None
    y, mo, d, h, mi, s = (int(x) for x in m.groups()[:6])
    frac = m.group(7) or ""
    off = m.group(8)
    if s > 60:
        return None
    sign_minutes = 0
    if off not in ("Z", "z"):
        oh, om = int(off[1:3]), int(off[4:6])
        if oh > 23 or om > 59:
            return None
        sign_minutes = (oh * 60 + om) * (1 if off[0] == "+" else -1)
    try:
        base = datetime(y, mo, d, h, mi, min(s, 59))
    except ValueError:
        return None
    base = base + timedelta(seconds=s - min(s, 59)) - timedelta(minutes=sign_minutes)
    seconds = int((base - datetime(1970, 1, 1)).total_seconds())
    return Fraction(seconds) + (Fraction(int(frac), 10 ** len(frac)) if frac else Fraction(0))


def _ref_id(value: Any) -> Tuple[Optional[str], str]:
    if value is None or value == "":
        return None, "id_missing"
    if not isinstance(value, str):
        return None, "id_not_normalizable"
    if len(value) == 26 and _ULID.match(value):
        return value.upper(), ""
    if len(value) == 36 and _UUID.match(value):
        return value.lower(), ""
    if len(value) == 32 and _HEX.match(value):
        v = value.lower()
        return f"{v[:8]}-{v[8:12]}-{v[12:16]}-{v[16:20]}-{v[20:]}", ""
    return None, "id_not_normalizable"


def _reference(rows: Sequence[Any]) -> Dict[str, Any]:
    valid: List[Tuple[Tuple[Any, ...], Any]] = []
    errors: List[Tuple[str, bytes]] = []
    for row in rows:
        if not isinstance(row, dict):
            errors.append(("row_not_object", _ser(row)))
            continue
        ident, why = _ref_id(row.get("id"))
        if ident is None:
            errors.append((why, _ser(row)))
            continue
        if "lamportclock" in row:
            clock = row["lamportclock"]
            if type(clock) is not int or clock < 0 or clock > 2**31 - 1:
                errors.append(("clock_out_of_range", _ser(row)))
                continue
            has, c = 1, clock
        else:
            has, c = 0, 0
        instant = _ref_instant(row.get("time"))
        if instant is None:
            errors.append(("time_unparseable", _ser(row)))
            continue
        source = row.get("source")
        if source is None:
            source = ""
        if not isinstance(source, str):
            errors.append(("source_invalid", _ser(row)))
            continue
        valid.append(((has, c, instant, ident, source), row))
    groups: Dict[Tuple[str, str], List[Tuple[Tuple[Any, ...], Any]]] = {}
    for key, row in valid:
        groups.setdefault((key[4], key[3]), []).append((key, row))
    winners = []
    collapsed = 0
    conflicts = []
    for group, members in groups.items():
        collapsed += len(members) - 1
        winners.append(min(members, key=lambda kr: _ser(kr[1])))
        without_id = {_ser({k: v for k, v in r.items() if k != "id"}) for _, r in members}
        if len(without_id) > 1:
            conflicts.append(list(group))
    winners.sort(key=lambda kr: kr[0])
    return {
        "ordered": [_ser(r) for _, r in winners],
        "errors": sorted(errors),
        "collapsed": collapsed,
        "conflicts": sorted(conflicts),
        "read": len(rows),
    }


_IDS = [
    A,
    B,
    C,
    P + "abc",
    P + "ABD",
    "0190a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b",
    "0190A1B2C3D47E5F8A9B0C1D2E3F4A5B",
    "nope",
    None,
    "",
]
_TIMES = [
    "2026-10-13T10:00:00Z",
    "2026-10-13T12:00:00+02:00",
    "2026-10-13T10:00:00.5Z",
    "2026-10-13T10:00:00.500000001Z",
    "2026-10-13T11:00:00Z",
    "2026-06-30T23:59:60Z",
    "2026-07-01T00:00:00Z",
    "yesterday",
    "",
    None,
    5,
]
_CLOCKS = [None, None, 0, 1, 2, CLOCK_MAX, CLOCK_MAX + 1, -1, True, "5", 5.0]
_SOURCES = [None, "", "/a", "/b", "\uff5e", "\U0001f600", 7]


@st.composite
def _rows(draw: st.DrawFn) -> List[Any]:
    count = draw(st.integers(0, 9))
    rows: List[Any] = []
    for _ in range(count):
        if draw(st.integers(0, 40)) == 0:
            rows.append(draw(st.sampled_from([None, 5, "x", []])))
            continue
        row: Dict[str, Any] = {}
        ident = draw(st.sampled_from(_IDS))
        if ident is not None:
            row["id"] = ident
        time = draw(st.sampled_from(_TIMES))
        if time is not None:
            row["time"] = time
        clock = draw(st.sampled_from(_CLOCKS))
        if clock is not None:
            row["lamportclock"] = clock
        source = draw(st.sampled_from(_SOURCES))
        if source is not None:
            row["source"] = source
        if draw(st.booleans()):
            row["data"] = {"x": draw(st.integers(0, 2))}
        rows.append(row)
    return rows


@settings(max_examples=400, deadline=None)
@given(_rows())
def test_matches_the_independent_reference(rows: List[Any]) -> None:
    result = order_rows(rows)
    expected = _reference(rows)
    form = result.canonical()
    assert form["ordered"] == expected["ordered"]
    assert form["errors"] == expected["errors"]
    assert form["collapsed"] == expected["collapsed"]
    assert form["conflicts"] == expected["conflicts"]
    assert form["read"] == expected["read"]


@settings(max_examples=300, deadline=None)
@given(_rows(), st.randoms(use_true_random=False))
def test_result_does_not_depend_on_input_order(rows: List[Any], rnd: Any) -> None:
    shuffled = list(rows)
    rnd.shuffle(shuffled)
    assert order_rows(rows).canonical() == order_rows(shuffled).canonical()


@settings(max_examples=300, deadline=None)
@given(_rows())
def test_ordered_rows_are_strictly_increasing_and_accounted_for(rows: List[Any]) -> None:
    result = order_rows(rows)
    keys = [order_key(r) for r in result.ordered]
    assert all(a < b for a, b in zip(keys, keys[1:]))  # strict: the order is total after dedupe
    assert len(result.ordered) + len(result.errors) + result.collapsed == len(rows)
    assert {e.reason for e in result.errors} <= ERROR_REASONS


@settings(max_examples=300, deadline=None)
@given(_rows())
def test_the_key_order_is_transitive_and_total_on_valid_rows(rows: List[Any]) -> None:
    keys = []
    for row in rows:
        try:
            keys.append(order_key(row))
        except UnorderableRow:
            pass
    for a in keys:
        for b in keys:
            assert (a < b) + (a == b) + (a > b) == 1
            for c in keys[:5]:
                if a <= b <= c:
                    assert a <= c


# ------------------------------------------------------- guards added after the squad round
def test_a_lone_surrogate_does_not_crash_the_order() -> None:
    row = _row(x=json.loads('"\\ud800"'))
    result = order_rows([row, dict(row)])
    assert (len(result.ordered), result.collapsed) == (1, 1)
    assert result.canonical()["read"] == 2


def test_a_trailing_newline_is_not_an_rfc_3339_timestamp() -> None:
    with pytest.raises(UnorderableRow):
        order_key(_row(time="2026-10-13T10:00:00Z\n"))


def test_year_zero_is_not_parseable_everywhere_so_it_is_not_parseable() -> None:
    with pytest.raises(UnorderableRow):
        order_key(_row(time="0000-01-01T00:00:00Z"))
