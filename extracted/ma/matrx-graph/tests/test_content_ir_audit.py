"""The audit machinery is the only thing standing between us and silent loss.

Every assertion here is about the MECHANISM, not about a harness: the audit is
handed a raw payload and its two registers, and the test reads what the audit
itself produced. Two of these are planted failures — a key nobody declared, and
a value big enough that a dishonest ``size`` would be invisible — because a
suite that cannot fail proves nothing.
"""

from __future__ import annotations

import logging

import pytest

from matrx_graph.content_ir.audit import DroppedValue, KeyAudit, TranslationReport, UnknownKeys

MAPPED = {"title", "url"}
DROPPED = {"tracking_id": "provider click-tracking handle", "layout": "provider UI chrome"}


def _audit() -> KeyAudit:
    return KeyAudit(
        "acme",
        family="widget",
        adapter_hint="aidream/services/widget_kinds/{provider}_adapter.py",
    )


def test_a_fully_declared_payload_is_fully_accounted() -> None:
    audit = _audit()
    audit.check("top", {"title": "T", "url": "u", "layout": "grid"}, MAPPED, DROPPED)
    report = audit.report()
    assert report.fully_accounted
    assert report.unknown == []
    assert report.provider == "acme"


def test_an_undeclared_key_screams_rather_than_disappearing(caplog) -> None:
    """PLANTED FAILURE — ``surprise_field`` is in neither register.

    If the audit ever stops reporting it, a provider can add a paid field and
    nobody finds out. The banner must also name the file to edit, or the
    scream is noise.
    """
    audit = _audit()
    with caplog.at_level(logging.ERROR):
        audit.check("top", {"title": "T", "surprise_field": 42}, MAPPED, DROPPED)
        report = audit.report()

    assert not report.fully_accounted
    assert report.unknown == [UnknownKeys(section="top", keys=["surprise_field"])]

    # vcprint's red banner rides the root logger at ERROR, which is what makes
    # it land durably in ``public.app_log`` on the host.
    banner = caplog.text
    assert "UNKNOWN ACME KEYS" in banner
    assert "WIDGET KIND ADAPTER" in banner
    assert "aidream/services/widget_kinds/acme_adapter.py" in banner
    assert "surprise_field" in banner


def test_the_scream_is_family_agnostic() -> None:
    """A family that declares nothing still gets a banner it can act on."""
    audit = KeyAudit("acme")
    audit.check("top", {"nope": 1}, (), {})
    report = audit.report()
    assert report.unknown == [UnknownKeys(section="top", keys=["nope"])]


def test_check_captures_every_declared_drop_that_is_present() -> None:
    """SHOW-WHAT-YOU-HIDE: declaring the register is declaring both legs."""
    audit = _audit()
    audit.check("top", {"title": "T", "layout": "grid", "tracking_id": "abc"}, MAPPED, DROPPED)
    dropped = {d.path: d for d in audit.report().dropped}
    assert set(dropped) == {"top.layout", "top.tracking_id"}
    assert dropped["top.layout"].preview == "grid"
    assert dropped["top.layout"].reason == DROPPED["layout"]
    assert dropped["top.tracking_id"].kind_of == "str"


def test_an_absent_or_empty_drop_is_not_reported() -> None:
    """Nothing is hidden if the source never sent it — reporting it is noise."""
    audit = _audit()
    audit.check("top", {"title": "T", "layout": "", "tracking_id": None}, MAPPED, DROPPED)
    assert audit.report().dropped == []


def test_path_prefix_controls_where_a_drop_is_reported() -> None:
    audit = _audit()
    audit.check("top", {"layout": "grid"}, MAPPED, DROPPED, path_prefix="")
    audit.check("items", {"layout": "grid"}, MAPPED, DROPPED, path_prefix="items[3].")
    assert sorted(d.path for d in audit.report().dropped) == ["items[3].layout", "layout"]


def test_a_big_dropped_list_reports_its_honest_size() -> None:
    """PLANTED FAILURE — a truncated preview must not shrink ``size``.

    Arman has to be able to read "454 entries" off the report and decide. If
    ``size`` ever became ``len(preview)`` every large drop would read as 5 and
    look harmless, which is exactly the lie this field exists to prevent.
    """
    audit = _audit()
    big = [f"row-{i}" for i in range(454)]
    audit.check("top", {"layout": big}, MAPPED, DROPPED)
    entry = audit.report().dropped[0]

    assert entry.size == 454, "size must be the FULL magnitude, never the preview length"
    assert entry.preview == big[: KeyAudit.PREVIEW_ENTRIES]
    assert len(entry.preview) < entry.size, "the preview is bounded; the size is not"
    assert entry.kind_of == "list"


def test_a_big_dropped_string_reports_its_honest_size() -> None:
    audit = _audit()
    huge = "x" * 114_000
    audit.check("top", {"layout": huge}, MAPPED, DROPPED)
    entry = audit.report().dropped[0]

    assert entry.size == 114_000
    assert entry.preview == huge[: KeyAudit.PREVIEW_CHARS]
    assert len(entry.preview) == KeyAudit.PREVIEW_CHARS


def test_a_dropped_dict_reports_entry_count_not_characters() -> None:
    audit = _audit()
    blob = {f"k{i}": i for i in range(40)}
    audit.check("top", {"layout": blob}, MAPPED, DROPPED)
    entry = audit.report().dropped[0]
    assert entry.size == 40
    assert entry.kind_of == "dict"
    assert len(entry.preview) == KeyAudit.PREVIEW_ENTRIES


def test_the_audit_never_raises_on_a_hostile_payload() -> None:
    """A new provider key must never break a live call — report, never raise."""
    audit = _audit()
    audit.check("top", {"a": object(), "b": {1: 2}, "c": [None]}, MAPPED, DROPPED)
    assert not audit.report().fully_accounted


def test_the_report_is_a_strict_schema() -> None:
    with pytest.raises(Exception):
        TranslationReport(provider="acme", surprise="x")
    with pytest.raises(Exception):
        DroppedValue(path="p", reason="r", kind_of="str", surprise="x")


def test_the_report_round_trips_as_json() -> None:
    """It rides the wire to the demo's hidden-data tab — it must survive."""
    audit = _audit()
    audit.check("top", {"layout": ["a", "b"], "surprise": 1}, MAPPED, DROPPED)
    report = audit.report()
    assert TranslationReport.model_validate_json(report.model_dump_json()) == report


def test_the_package_module_does_not_import_the_host() -> None:
    """matrx-graph is standalone — an aidream import here fails the build."""
    import ast
    from pathlib import Path

    import matrx_graph.content_ir.audit as mod
    import matrx_graph.content_ir.translate as tmod

    for module in (mod, tmod):
        tree = ast.parse(Path(module.__file__).read_text())
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                assert not name.split(".")[0] == "aidream", f"{module.__name__} imports {name}"
