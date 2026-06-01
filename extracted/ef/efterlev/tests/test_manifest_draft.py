"""Tests for `efterlev manifests draft <KSI>` — the interactive scaffolder.

The runner is interactive, so most coverage targets the pure pieces:
`load_template` (reads bundled per-KSI guidance) and `render_manifest_yaml`
(produces clean, schema-valid YAML that round-trips through the real
`EvidenceManifest` loader). The interactive runner is exercised for its
guard paths (non-TTY refusal, unknown KSI, existing-file refusal, and a
full happy-path walk with stubbed prompts).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from efterlev.cli import manifest_draft as md
from efterlev.models.manifest import EvidenceManifest

# --- load_template -----------------------------------------------------


def test_load_template_returns_questions_for_real_ksi() -> None:
    tmpl = md.load_template("KSI-AFR-ADS")
    assert tmpl is not None
    assert tmpl.ksi_id == "KSI-AFR-ADS"
    assert tmpl.name  # non-empty
    assert tmpl.description  # non-empty guidance
    assert len(tmpl.questions) >= 3
    assert all(isinstance(q, str) and q for q in tmpl.questions)


def test_load_template_none_for_unknown_ksi() -> None:
    assert md.load_template("KSI-NOPE-XXX") is None


def test_load_template_none_for_scanner_ksi() -> None:
    # A purely scanner-evidenceable KSI ships no manifest template.
    assert md.load_template("KSI-SVC-SNT") is None


# --- render_manifest_yaml ----------------------------------------------


def _render(**overrides: object) -> str:
    base = dict(
        ksi_id="KSI-AFR-ADS",
        name="Authorization Data Sharing",
        statement="We publish authorization artifacts to the FedRAMP Marketplace quarterly.",
        attested_by="vp-security@example.com",
        attested_at=date(2026, 5, 21),
        reviewed_at=date(2026, 5, 21),
        next_review=date(2026, 11, 21),
        supporting_docs=["./runbooks/ads.md"],
    )
    base.update(overrides)
    return md.render_manifest_yaml(**base)  # type: ignore[arg-type]


def test_render_round_trips_through_evidence_manifest() -> None:
    text = _render()
    loaded = EvidenceManifest.model_validate(yaml.safe_load(text))
    assert loaded.ksi == "KSI-AFR-ADS"
    assert len(loaded.evidence) == 1
    att = loaded.evidence[0]
    assert att.type == "attestation"
    assert att.attested_by == "vp-security@example.com"
    assert att.attested_at == date(2026, 5, 21)
    assert att.next_review == date(2026, 11, 21)
    assert att.supporting_docs == ["./runbooks/ads.md"]


def test_render_carries_no_template_help_or_draft() -> None:
    text = _render()
    assert "_template_help" not in text
    assert "DRAFT" not in text
    assert "questions" not in text


def test_render_omits_optional_fields_when_absent() -> None:
    text = _render(reviewed_at=None, next_review=None, supporting_docs=[])
    parsed = yaml.safe_load(text)
    ev = parsed["evidence"][0]
    assert "reviewed_at" not in ev
    assert "next_review" not in ev
    assert "supporting_docs" not in ev
    # Still valid without the optionals.
    EvidenceManifest.model_validate(parsed)


def test_render_includes_header_comment() -> None:
    text = _render()
    assert text.startswith("# KSI-AFR-ADS — Authorization Data Sharing")


# --- _add_months -------------------------------------------------------


def test_add_months_basic() -> None:
    assert md._add_months(date(2026, 1, 15), 6) == date(2026, 7, 15)


def test_add_months_year_rollover() -> None:
    assert md._add_months(date(2026, 10, 1), 6) == date(2027, 4, 1)


def test_add_months_clamps_day() -> None:
    # Aug 31 + 6mo -> Feb 28 (2027 is not a leap year).
    assert md._add_months(date(2026, 8, 31), 6) == date(2027, 2, 28)


# --- run_manifest_draft guards -----------------------------------------


def test_run_refuses_without_efterlev_dir(tmp_path: Path) -> None:
    rc = md.run_manifest_draft(tmp_path, "KSI-AFR-ADS", force=False)
    assert rc == 1


def test_run_non_tty_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / ".efterlev" / "manifests").mkdir(parents=True)
    # No FRMR cache -> catalog None -> KSI not validated against baseline.
    # run_manifest_draft imports is_interactive from first_run_wizard at call
    # time, so patching it on the source module rebinds what the function sees.
    import efterlev.cli.first_run_wizard as frw

    monkeypatch.setattr(frw, "is_interactive", lambda: False)
    rc = md.run_manifest_draft(tmp_path, "KSI-AFR-ADS", force=False)
    assert rc == 2


def test_run_refuses_unknown_template(tmp_path: Path) -> None:
    (tmp_path / ".efterlev" / "manifests").mkdir(parents=True)
    rc = md.run_manifest_draft(tmp_path, "KSI-SVC-SNT", force=False)
    assert rc == 2


def test_run_refuses_existing_without_force(tmp_path: Path) -> None:
    mdir = tmp_path / ".efterlev" / "manifests"
    mdir.mkdir(parents=True)
    (mdir / "ksi-afr-ads.yml").write_text("ksi: KSI-AFR-ADS\nevidence: []\n", encoding="utf-8")
    rc = md.run_manifest_draft(tmp_path, "KSI-AFR-ADS", force=False)
    assert rc == 2


def test_run_happy_path_writes_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mdir = tmp_path / ".efterlev" / "manifests"
    mdir.mkdir(parents=True)

    import efterlev.cli.first_run_wizard as frw

    monkeypatch.setattr(frw, "is_interactive", lambda: True)

    # Stub the interactive prompts: questions get a single answer each, then
    # attested_by, three dates (accept defaults via the typed value), then an
    # empty supporting-doc line to finish.
    template = md.load_template("KSI-AFR-ADS")
    assert template is not None
    n_questions = len(template.questions)

    answers = iter(
        ["We share the SSP and POA&M."] * n_questions
        + [
            "vp-security@example.com",  # attested_by
            "2026-05-21",  # attestation date
            "2026-05-21",  # last reviewed
            "2026-11-21",  # next review
            "./runbooks/ads.md",  # doc #1
            "",  # finish docs
        ]
    )
    monkeypatch.setattr(md.typer, "prompt", lambda *a, **k: next(answers))

    rc = md.run_manifest_draft(tmp_path, "KSI-AFR-ADS", force=False)
    assert rc == 0

    dest = mdir / "ksi-afr-ads.yml"
    assert dest.exists()
    loaded = EvidenceManifest.model_validate(yaml.safe_load(dest.read_text(encoding="utf-8")))
    assert loaded.ksi == "KSI-AFR-ADS"
    att = loaded.evidence[0]
    assert att.attested_by == "vp-security@example.com"
    assert "We share the SSP and POA&M." in att.statement
    assert att.supporting_docs == ["./runbooks/ads.md"]


def test_run_happy_path_no_answers_aborts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mdir = tmp_path / ".efterlev" / "manifests"
    mdir.mkdir(parents=True)

    import efterlev.cli.first_run_wizard as frw

    monkeypatch.setattr(frw, "is_interactive", lambda: True)
    # Every prompt returns empty -> no answers -> abort before writing.
    monkeypatch.setattr(md.typer, "prompt", lambda *a, **k: "")

    rc = md.run_manifest_draft(tmp_path, "KSI-AFR-ADS", force=False)
    assert rc == 1
    assert not (mdir / "ksi-afr-ads.yml").exists()
