"""Tests for `efterlev scope` — inherited-control declaration (v0.1.171).

Covers: the config round-trip, the inheritance-profile table integrity,
the declare/show/clear commands, and the deterministic apply cross-check
(clean → inherited claim+evidence written; contradicted → flagged, not
written). Plus the gap skip-set helper.

All deterministic — no LLM, no network.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.cli.scope_cli import (
    INHERITANCE_PROFILES,
    INHERITED_CLAIM_KIND,
    INHERITED_DETECTOR_ID,
    available_profiles,
    inherited_ksis_in_store,
    partition_inherited,
    profile_ksis,
    rationale_for,
)
from efterlev.config import Config, ScopeConfig, load_config, save_config

runner = CliRunner()


# --- profile table integrity -------------------------------------------


def test_profiles_nonempty_and_have_rationales() -> None:
    assert available_profiles()
    for profile, entries in INHERITANCE_PROFILES.items():
        assert entries, f"profile {profile} is empty"
        for ksi, rationale in entries:
            assert ksi.startswith("KSI-"), f"{profile}: {ksi} not a KSI id"
            assert len(rationale) > 20, f"{profile}/{ksi}: rationale too thin"


def test_profile_ksis_match_real_catalog() -> None:
    """Every KSI in every profile must be a real FRMR catalog id."""
    from efterlev.frmr.loader import load_frmr
    from efterlev.paths import vendored_catalogs_dir

    doc = load_frmr(vendored_catalogs_dir() / "frmr" / "FRMR.documentation.json")
    real = set(doc.indicators.keys())
    for profile in available_profiles():
        for ksi in profile_ksis(profile):
            assert ksi in real, f"{profile} references non-existent {ksi}"


def test_rationale_for_known_and_unknown() -> None:
    known = profile_ksis("aws-serverless")[0]
    assert "immutable" in rationale_for("aws-serverless", known).lower() or rationale_for(
        "aws-serverless", known
    )
    # Unknown profile/ksi → generic operator rationale.
    generic = rationale_for(None, "KSI-XXX-YYY")
    assert "operator" in generic.lower()


# --- partition cross-check (pure) --------------------------------------


def test_partition_no_evidence_all_clean() -> None:
    clean, contradicted = partition_inherited(["KSI-A", "KSI-B"], set())
    assert clean == ["KSI-A", "KSI-B"]
    assert contradicted == []


def test_partition_evidence_contradicts() -> None:
    clean, contradicted = partition_inherited(["KSI-A", "KSI-B", "KSI-C"], {"KSI-B"})
    assert clean == ["KSI-A", "KSI-C"]
    assert contradicted == ["KSI-B"]


# --- ScopeConfig round-trip --------------------------------------------


def test_scope_config_roundtrip(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.toml"
    config = Config(
        scope=ScopeConfig(inherited=["KSI-CNA-IBP"], inherited_profile="aws-serverless")
    )
    save_config(config, cfg_path)
    loaded = load_config(cfg_path)
    assert loaded.scope.inherited == ["KSI-CNA-IBP"]
    assert loaded.scope.inherited_profile == "aws-serverless"


def test_scope_config_empty_omits_section(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.toml"
    save_config(Config(), cfg_path)
    text = cfg_path.read_text()
    assert "[scope]" not in text  # default empty → no section emitted
    assert load_config(cfg_path).scope.inherited == []


# --- declare / show / clear (CLI, via a real init'd workspace) ---------


def _init_workspace(tmp_path: Path) -> Path:
    """Minimal real workspace so config + FRMR cache exist."""
    result = runner.invoke(
        app, ["init", "--target", str(tmp_path), "--baseline", "fedramp-20x-moderate"]
    )
    assert result.exit_code == 0, result.output
    return tmp_path


def test_declare_profile_writes_config(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.scope.inherited == profile_ksis("aws-serverless")
    assert config.scope.inherited_profile == "aws-serverless"


def test_declare_unknown_profile_errors(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(
        app, ["scope", "declare", "--profile", "nonsense", "--target", str(tmp_path)]
    )
    assert result.exit_code == 2
    assert "unknown profile" in result.output


def test_declare_explicit_ksi(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(
        app,
        ["scope", "declare", "--ksi", "KSI-CNA-IBP", "--target", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.scope.inherited == ["KSI-CNA-IBP"]


def test_declare_rejects_fake_ksi(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(
        app, ["scope", "declare", "--ksi", "KSI-FAKE-XYZ", "--target", str(tmp_path)]
    )
    assert result.exit_code == 2
    assert "not real KSI ids" in result.output


def test_declare_nothing_errors(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(app, ["scope", "declare", "--target", str(tmp_path)])
    assert result.exit_code == 2
    assert "nothing to declare" in result.output


def test_show_empty(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    result = runner.invoke(app, ["scope", "show", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "No inherited controls declared" in result.output


def test_clear_removes_declaration(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    result = runner.invoke(app, ["scope", "clear", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "Cleared" in result.output
    assert load_config(tmp_path / ".efterlev" / "config.toml").scope.inherited == []


# --- apply: clean path (no contradicting evidence) ---------------------


def _seed_evidence(
    root: Path,
    ksi_by_record: dict[str, list[str]],
    *,
    boundary_state: str | None = None,
) -> None:
    """Write evidence records into the store DB citing given KSIs.

    ksi_by_record maps a record id → ksis_evidenced list. Detector id is a
    normal scanner (NOT scope_inherited) so it counts as contradicting.
    `boundary_state` (v0.1.222) optionally tags every record — used to
    verify out_of_boundary evidence does NOT contradict an inheritance
    declaration.
    """
    efterlev = root / ".efterlev"
    blob_dir = efterlev / "store"
    blob_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, content_ref TEXT, "
        "derived_from TEXT, primitive TEXT, agent TEXT, model TEXT, "
        "prompt_hash TEXT, timestamp TEXT, metadata TEXT)"
    )
    for rid, ksis in ksi_by_record.items():
        blob = f"{rid}.json"
        # iter_evidence's structural filter requires detector_id +
        # source_ref + timestamp to recognize a blob as Evidence.
        payload: dict[str, object] = {
            "evidence_id": f"sha256:{rid}",
            "detector_id": "scan_terraform",
            "ksis_evidenced": ksis,
            "source_ref": {"file": "infra/main.tf", "line_start": 1, "line_end": 2},
            "timestamp": "2026-05-20T00:00:00Z",
        }
        if boundary_state is not None:
            payload["boundary_state"] = boundary_state
        (blob_dir / blob).write_text(json.dumps(payload), encoding="utf-8")
        conn.execute(
            "INSERT OR REPLACE INTO provenance_records "
            "(record_id, record_type, content_ref, derived_from, primitive, timestamp, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rid, "evidence", blob, "[]", "scan_terraform@0.1.0", "2026-05-20T00:00:00Z", "{}"),
        )
    conn.commit()
    conn.close()


def test_apply_clean_writes_inherited_claims(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    # No contradicting evidence seeded → all clean.
    result = runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "marked implemented (inherited)" in result.output
    # All 4 profile KSIs now in the inherited skip-set.
    assert inherited_ksis_in_store(tmp_path) == set(profile_ksis("aws-serverless"))


def test_apply_contradiction_flags_not_marks(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    # Seed scanner evidence citing KSI-CNA-MAT → contradiction.
    _seed_evidence(tmp_path, {"ev-mat": ["KSI-CNA-MAT"]})
    result = runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "NOT marked" in result.output
    assert "KSI-CNA-MAT" in result.output
    inherited = inherited_ksis_in_store(tmp_path)
    # The contradicted KSI is NOT inherited; the other 3 are.
    assert "KSI-CNA-MAT" not in inherited
    assert "KSI-CNA-IBP" in inherited


def test_apply_out_of_boundary_evidence_does_not_contradict(tmp_path: Path) -> None:
    """Out-of-boundary evidence must NOT contradict an inheritance declaration
    (v0.1.222): a dev_sandbox resource citing KSI-CNA-MAT would otherwise block
    "CNA-MAT inherited from platform" even though the in-boundary workspace has
    no such config. Same boundary discipline as agent gap (v0.1.219)."""
    _init_workspace(tmp_path)
    runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    # Same KSI as the contradiction test — but the evidence is out_of_boundary.
    _seed_evidence(tmp_path, {"ev-mat-oob": ["KSI-CNA-MAT"]}, boundary_state="out_of_boundary")
    result = runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    # No contradiction — all profile KSIs inherited, CNA-MAT included.
    assert "NOT marked" not in result.output
    assert inherited_ksis_in_store(tmp_path) == set(profile_ksis("aws-serverless"))


def test_apply_idempotent(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    runner.invoke(
        app, ["scope", "declare", "--profile", "aws-serverless", "--target", str(tmp_path)]
    )
    runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    first = inherited_ksis_in_store(tmp_path)
    result = runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "already recorded inherited" in result.output
    assert inherited_ksis_in_store(tmp_path) == first


def test_apply_writes_inheritance_basis_evidence(tmp_path: Path) -> None:
    """Inherited KSIs get an inheritance-basis evidence record (so the
    RFC-0017 gate's inventory item passes), tagged scope_inherited."""
    _init_workspace(tmp_path)
    runner.invoke(app, ["scope", "declare", "--ksi", "KSI-CNA-IBP", "--target", str(tmp_path)])
    runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        ev = [
            p for _rid, p in store.iter_evidence() if p.get("detector_id") == INHERITED_DETECTOR_ID
        ]
    assert len(ev) == 1
    assert ev[0]["ksis_evidenced"] == ["KSI-CNA-IBP"]
    assert "[INHERITED" in ev[0]["content"]["rationale"]


def test_inherited_claim_carries_loud_marker(tmp_path: Path) -> None:
    _init_workspace(tmp_path)
    runner.invoke(app, ["scope", "declare", "--ksi", "KSI-CNA-IBP", "--target", str(tmp_path)])
    runner.invoke(app, ["scope", "apply", "--target", str(tmp_path)])
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        claims = store.iter_claims_by_metadata_kind(INHERITED_CLAIM_KIND)
    assert len(claims) == 1
    _rid, metadata, payload = claims[0]
    assert metadata["ksi_id"] == "KSI-CNA-IBP"
    assert payload["content"]["status"] == "implemented"
    assert "[INHERITED" in payload["content"]["rationale"]
