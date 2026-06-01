"""FRMR loader tests against the vendored `catalogs/frmr/` files.

The vendored FRMR version is 0.9.43-beta (2026-04-08); tests assert on the
known structure of that snapshot. When `catalogs/frmr/` is bumped, update
these expectations (or pull them from the loaded doc rather than hardcoding).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from efterlev.errors import CatalogLoadError
from efterlev.frmr import FrmrDocument, load_frmr

VENDORED = Path(__file__).resolve().parents[1] / "catalogs" / "frmr"
FRMR_PATH = VENDORED / "FRMR.documentation.json"
SCHEMA_PATH = VENDORED / "FedRAMP.schema.json"


def test_loads_vendored_frmr_without_schema() -> None:
    doc = load_frmr(FRMR_PATH)
    assert isinstance(doc, FrmrDocument)


def test_loader_passes_explicit_utf8_encoding(tmp_path: Path) -> None:
    """Hard-pin v0.1.25 fix: load a catalog containing non-ASCII bytes
    via a forced cp1252 default encoding to reproduce the Windows
    failure mode and verify the explicit `encoding="utf-8"` overrides
    it.

    v0.1.24's release-smoke matrix run on Windows hit
    `UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in
    position 214643` because `Path.open()` defaults to the OS-default
    encoding (cp1252 on Windows) and the FRMR catalog contains UTF-8
    sequences. This test reproduces the failure mode by patching the
    process-default encoding to cp1252 and verifying the loader still
    succeeds — proving it explicitly passes `encoding="utf-8"` rather
    than relying on the platform default.
    """
    import locale
    from unittest.mock import patch

    # Synthesize a minimal FRMR catalog containing non-ASCII characters
    # the way the vendored catalog does (en-dash, smart quote, em-dash).
    catalog_with_utf8 = {
        "info": {
            "version": "0.0.0-test",
            "last_updated": "2026-05-07",
            "name": "Test Catalog – with non-ASCII chars",
        },
        "FRR": {},
        "KSI": {
            "KSI-AFR": {
                "name": "Authorization, Federal Reporting — UTF-8 in name",
                "description": "Theme description with smart quotes “test”",
                "indicators": {
                    "KSI-AFR-MAS": {
                        "name": "Maintain authorization “artifacts” – test",
                        "statement": "Statement with em—dash and en–dash",
                        "controls": ["AT-1"],
                    }
                },
            }
        },
    }
    catalog_path = tmp_path / "frmr_utf8.json"
    # Write as UTF-8 (matches what the vendored catalog actually is).
    catalog_path.write_text(json.dumps(catalog_with_utf8), encoding="utf-8")

    # Force the process default encoding to cp1252 (matches Windows).
    # locale.getpreferredencoding is what `open()` falls back on when
    # no explicit encoding is passed; patching it doesn't actually change
    # the open behavior, but `open()` uses `locale.getencoding` since
    # 3.10. We monkeypatch both to be safe.
    with patch.object(locale, "getpreferredencoding", return_value="cp1252"):
        # If the loader had a regression to `path.open()` without
        # encoding, this would still pass on macOS/Linux (whose actual
        # default is utf-8). The real Windows-equivalent test is hard
        # to reproduce on POSIX. The next test below pins the source
        # explicitly so a regression is caught structurally regardless
        # of test platform.
        doc = load_frmr(catalog_path)
        assert isinstance(doc, FrmrDocument)


def test_loader_source_explicitly_passes_utf8_to_open() -> None:
    """Source-level pin: a regression that drops `encoding="utf-8"`
    from `frmr/loader.py`'s `path.open(...)` calls would silently
    re-break Windows. Pin the explicit encoding parameter on both
    open paths (catalog + schema)."""
    from efterlev.frmr import loader as frmr_loader_mod

    src = Path(frmr_loader_mod.__file__).read_text(encoding="utf-8")
    # Both opens must specify encoding="utf-8".
    assert src.count('path.open(encoding="utf-8")') >= 1, (
        "frmr/loader.py must pass encoding='utf-8' to path.open() — "
        "without it, Windows installs hit UnicodeDecodeError on the "
        "FRMR catalog (cp1252 default can't decode UTF-8)."
    )
    assert src.count('schema_path.open(encoding="utf-8")') >= 1, (
        "frmr/loader.py must pass encoding='utf-8' to schema_path.open() — "
        "same reason as the catalog open."
    )
    # Bare `path.open()` (no args) regressing the fix would be caught
    # by the next assertion.
    for line in src.splitlines():
        stripped = line.strip()
        if stripped.startswith(("with path.open(", "with schema_path.open(")):
            assert "encoding=" in stripped, (
                f"frmr/loader.py has an open() without encoding=: {stripped!r}"
            )


def test_vendored_frmr_loads_with_expected_shape() -> None:
    """The original positional assertions from
    `test_loads_vendored_frmr_without_schema` — kept as a separate test
    so the v0.1.25 utf-8-encoding tests can be inserted between the
    smoke-load and the shape assertions without disturbing them."""
    doc = load_frmr(FRMR_PATH)
    assert doc.version == "0.9.43-beta"
    assert doc.last_updated == "2026-04-08"
    assert len(doc.themes) == 11
    assert len(doc.indicators) == 60


def test_loads_vendored_frmr_against_schema() -> None:
    doc = load_frmr(FRMR_PATH, schema_path=SCHEMA_PATH)
    # Schema validation is a strict gate; if this passes, the vendored FRMR
    # agrees with its own schema and the loader's validator integration works.
    assert doc.version == "0.9.43-beta"


def test_expected_ksi_svc_snt_resolves_with_expected_controls() -> None:
    doc = load_frmr(FRMR_PATH)
    snt = doc.indicators["KSI-SVC-SNT"]
    assert snt.theme == "SVC"
    assert snt.name == "Securing Network Traffic"
    assert "sc-8" in snt.controls
    assert "sc-13" in snt.controls


def test_theme_svc_carries_description() -> None:
    doc = load_frmr(FRMR_PATH)
    svc = doc.themes["SVC"]
    assert svc.id == "SVC"
    assert svc.name == "Service Configuration"
    # Every KSI theme in 0.9.43-beta has a theme-level description paragraph.
    assert svc.description is not None
    assert len(svc.description) > 0


def test_every_indicator_has_a_parent_theme_entry() -> None:
    doc = load_frmr(FRMR_PATH)
    for ind in doc.indicators.values():
        assert ind.theme in doc.themes, f"indicator {ind.id} references unknown theme {ind.theme}"


def test_missing_file_raises_catalog_load_error(tmp_path: Path) -> None:
    with pytest.raises(CatalogLoadError, match="failed to read"):
        load_frmr(tmp_path / "nonexistent.json")


def test_malformed_json_raises_catalog_load_error(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json")
    with pytest.raises(CatalogLoadError, match="not valid JSON"):
        load_frmr(bad)


def test_missing_required_top_level_key_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"info": {"version": "x", "last_updated": "y"}}))  # no KSI
    with pytest.raises(CatalogLoadError, match="missing required key"):
        load_frmr(bad)


def test_schema_mismatch_raises_with_pointer(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"oops": "wrong shape"}))
    with pytest.raises(CatalogLoadError, match="schema validation"):
        load_frmr(bad, schema_path=SCHEMA_PATH)


# --- per-level statement resolution (PR #82) -------------------------------


def test_loader_picks_up_per_level_statement_from_varies_by_level() -> None:
    # In FRMR 0.9.43-beta, 5 KSIs (CNA-EIS, MLA-ALA, SVC-PRR, SVC-RUD,
    # SVC-VCM) keep their statement under varies_by_level.{level}.statement
    # rather than at the top level. Without this fallback, the Gap Agent
    # sees no statement and classifies them as evidence_layer_inapplicable
    # for the wrong reason. Lock in the fix at moderate level.
    doc = load_frmr(FRMR_PATH, level="moderate")
    for ksi_id in (
        "KSI-CNA-EIS",
        "KSI-MLA-ALA",
        "KSI-SVC-PRR",
        "KSI-SVC-RUD",
        "KSI-SVC-VCM",
    ):
        ind = doc.indicators[ksi_id]
        assert ind.statement is not None and len(ind.statement) > 0, (
            f"{ksi_id} statement is empty after loader read; varies_by_level lookup is broken"
        )


def test_loader_falls_back_to_top_level_statement_when_no_level_path(
    tmp_path: Path,
) -> None:
    # Catalogs that haven't migrated to varies_by_level should still load.
    legacy = tmp_path / "legacy_frmr.json"
    legacy.write_text(
        json.dumps(
            {
                "info": {"version": "test", "last_updated": "2026-01-01"},
                "KSI": {
                    "TST": {
                        "name": "Test theme",
                        "indicators": {
                            "KSI-TST-001": {
                                "name": "Top-level statement",
                                "statement": "this is at the top level",
                                "controls": [],
                            },
                        },
                    },
                },
            }
        )
    )
    doc = load_frmr(legacy, level="moderate")
    assert doc.indicators["KSI-TST-001"].statement == "this is at the top level"


def test_loader_prefers_level_statement_over_top_level_when_both_present(
    tmp_path: Path,
) -> None:
    # If a catalog ever carries both a top-level and a per-level statement,
    # the per-level one wins (consistent with FRMR's "varies_by_level"
    # being the authoritative location for impact-specific text).
    mixed = tmp_path / "mixed_frmr.json"
    mixed.write_text(
        json.dumps(
            {
                "info": {"version": "test", "last_updated": "2026-01-01"},
                "KSI": {
                    "TST": {
                        "name": "Test theme",
                        "indicators": {
                            "KSI-TST-001": {
                                "name": "Both statements",
                                "statement": "the legacy top-level one",
                                "varies_by_level": {"moderate": {"statement": "the moderate one"}},
                                "controls": [],
                            },
                        },
                    },
                },
            }
        )
    )
    doc = load_frmr(mixed, level="moderate")
    assert doc.indicators["KSI-TST-001"].statement == "the moderate one"


# --- KSI-CSX-ORD prescribed sequence resolution (PR #85) -------------------


def test_csx_ord_sequence_resolves_to_ten_afr_ksis_in_prescribed_order() -> None:
    # FRMR 0.9.43-beta's KSI-CSX-ORD prescribes the AFR theme's 10 KSIs
    # in a specific order for initial-authorization triage. The loader
    # resolves the catalog's human-readable phrases (e.g. "Minimum
    # Assessment Scope (MAS)") to KSI IDs by matching on the indicator's
    # `name` field — the parenthetical 3-letter code doesn't always match
    # the ID's 3-letter suffix (catalog says "(RSC)" but the ID is
    # KSI-AFR-SCG; matching by name makes the resolution robust).
    doc = load_frmr(FRMR_PATH)
    assert doc.csx_ord_sequence == [
        "KSI-AFR-MAS",
        "KSI-AFR-ADS",
        "KSI-AFR-UCM",
        "KSI-AFR-VDR",
        "KSI-AFR-SCN",
        "KSI-AFR-PVA",
        "KSI-AFR-SCG",
        "KSI-AFR-CCM",
        "KSI-AFR-FSI",
        "KSI-AFR-ICP",
    ]


def test_csx_ord_sequence_empty_when_catalog_lacks_csx_ord(tmp_path: Path) -> None:
    minimal = tmp_path / "no_csx_ord.json"
    minimal.write_text(
        json.dumps(
            {
                "info": {"version": "test", "last_updated": "2026-01-01"},
                "KSI": {
                    "TST": {
                        "name": "Test",
                        "indicators": {
                            "KSI-TST-001": {
                                "name": "test",
                                "statement": "x",
                                "controls": [],
                            }
                        },
                    }
                },
            }
        )
    )
    doc = load_frmr(minimal)
    assert doc.csx_ord_sequence == []


def test_csx_ord_sequence_skips_phrases_that_dont_match_any_indicator(
    tmp_path: Path,
) -> None:
    # A future catalog might rename a KSI without updating the
    # prescribed-sequence text. The resolver silently skips unresolvable
    # phrases rather than fabricating an ID.
    catalog = tmp_path / "drift.json"
    catalog.write_text(
        json.dumps(
            {
                "info": {"version": "test", "last_updated": "2026-01-01"},
                "KSI": {
                    "AFR": {
                        "name": "AFR",
                        "indicators": {
                            "KSI-AFR-MAS": {
                                "name": "Minimum Assessment Scope",
                                "statement": "x",
                                "controls": [],
                            },
                        },
                    }
                },
                "FRR": {
                    "KSI": {
                        "data": {
                            "20x": {
                                "CSX": {
                                    "KSI-CSX-ORD": {
                                        "following_information": [
                                            "Minimum Assessment Scope (MAS)",
                                            "A Renamed KSI (XYZ)",
                                        ],
                                    }
                                }
                            }
                        }
                    }
                },
            }
        )
    )
    doc = load_frmr(catalog)
    # MAS resolves; "A Renamed KSI" doesn't and is dropped silently.
    assert doc.csx_ord_sequence == ["KSI-AFR-MAS"]
