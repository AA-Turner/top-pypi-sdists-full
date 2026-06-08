"""Authorization-boundary scoping tests (Priority 4 of v1-readiness-plan)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from efterlev.boundary import (
    active_boundary_config,
    compute_boundary_state,
    get_active_boundary_config,
)
from efterlev.config import BoundaryConfig
from efterlev.models import Evidence, SourceRef

# --- compute_boundary_state ------------------------------------------------


def test_no_config_yields_undeclared() -> None:
    assert compute_boundary_state(Path("infra/main.tf"), None) == "boundary_undeclared"


def test_empty_config_yields_undeclared() -> None:
    cfg = BoundaryConfig()
    assert compute_boundary_state(Path("infra/main.tf"), cfg) == "boundary_undeclared"


def test_include_only_match_is_in_boundary() -> None:
    cfg = BoundaryConfig(include=["boundary/**"])
    assert compute_boundary_state(Path("boundary/main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("boundary/sub/iam.tf"), cfg) == "in_boundary"


def test_include_only_non_match_is_out_of_boundary() -> None:
    """An include declaration creates an explicit scope; paths outside are out."""
    cfg = BoundaryConfig(include=["boundary/**"])
    assert compute_boundary_state(Path("infra/main.tf"), cfg) == "out_of_boundary"
    assert compute_boundary_state(Path("commercial/eks.tf"), cfg) == "out_of_boundary"


def test_exclude_only_match_is_out_of_boundary() -> None:
    """exclude-only means 'everything except these'."""
    cfg = BoundaryConfig(exclude=["commercial/**"])
    assert compute_boundary_state(Path("commercial/main.tf"), cfg) == "out_of_boundary"


def test_exclude_only_non_match_is_in_boundary() -> None:
    """exclude-only means everything not excluded is in scope."""
    cfg = BoundaryConfig(exclude=["commercial/**"])
    assert compute_boundary_state(Path("infra/main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("boundary/sub/iam.tf"), cfg) == "in_boundary"


def test_exclude_wins_over_include() -> None:
    """A path matching both include and exclude is out_of_boundary.

    Rationale: explicit exclusion is a signal of intent; a broader inclusion
    should not silently override it. Customer-friendly precedence — `.gitignore`
    semantics that customers already understand."""
    cfg = BoundaryConfig(
        include=["infra/**"],
        exclude=["infra/legacy/**"],
    )
    assert compute_boundary_state(Path("infra/legacy/old.tf"), cfg) == "out_of_boundary"
    assert compute_boundary_state(Path("infra/prod/main.tf"), cfg) == "in_boundary"


def test_manifests_in_boundary_when_a_boundary_is_declared() -> None:
    """v0.1.9 fix (refined v0.1.176): when a boundary IS declared,
    customer-authored Evidence Manifests can't structurally be out-of-scope
    — without this special case, manifests got silently excluded from the
    POAM because canonical include patterns (`infra/terraform/**`,
    `.github/workflows/**`) didn't cover `.efterlev/manifests/`. But when NO
    boundary is declared, manifests follow the undeclared rule like
    everything else (v0.1.176 #383 — the unconditional in_boundary was
    polluting the workspace aggregate). Surfaced in the v0.1.8 govnotes
    shakedown; the no-config regression surfaced in the 2026-05-21 run."""
    # v0.1.176 / #383: when NO boundary is declared, manifests are
    # boundary_undeclared like everything else — nothing is "in boundary"
    # without a declared boundary. (Pre-v0.1.176 this returned in_boundary
    # unconditionally, which falsely flipped the workspace aggregate to
    # in_boundary on any manifests-present-but-no-[boundary] workspace.)
    assert (
        compute_boundary_state(Path(".efterlev/manifests/afr-fsi.yml"), None)
        == "boundary_undeclared"
    )

    # With a tight include that does NOT cover .efterlev/manifests/.
    # Pre-v0.1.9 manifests would land out_of_boundary; v0.1.9 keeps
    # them in.
    cfg = BoundaryConfig(include=["infra/terraform/**", ".github/workflows/**"])
    assert compute_boundary_state(Path(".efterlev/manifests/ced-rgt.yml"), cfg) == "in_boundary"

    # Even an explicit exclude covering manifests is overridden by the
    # special case — the manifest path is structurally in-scope.
    cfg_exclude = BoundaryConfig(include=["infra/**"], exclude=[".efterlev/**"])
    assert (
        compute_boundary_state(Path(".efterlev/manifests/inr-rir.yml"), cfg_exclude)
        == "in_boundary"
    )

    # Sanity — non-manifest .efterlev/ paths are NOT special-cased; they
    # follow normal config semantics.
    assert (
        compute_boundary_state(Path(".efterlev/cache/something.json"), cfg_exclude)
        == "out_of_boundary"
    )


def test_undeclared_workspace_with_manifests_stays_undeclared() -> None:
    """v0.1.176 / #383 regression: a workspace with procedural manifests but
    NO `[boundary]` config must aggregate to `boundary_undeclared`. Before
    the fix, manifest evidence's unconditional in_boundary flipped
    `_resolve_workspace_boundary_state` to `in_boundary`, suppressing the
    'boundary undeclared' warning and falsely telling a 3PAO scope was set.
    Mixed manifest + detector evidence, no config → every record undeclared.
    """
    from efterlev.reports.gap_report import _resolve_workspace_boundary_state

    states = {
        "ev-manifest": compute_boundary_state(Path(".efterlev/manifests/afr-fsi.yml"), None),
        "ev-detector": compute_boundary_state(Path("infra/terraform/s3.tf"), None),
    }
    assert states == {"ev-manifest": "boundary_undeclared", "ev-detector": "boundary_undeclared"}
    assert _resolve_workspace_boundary_state(states) == "boundary_undeclared"


def test_recursive_double_star() -> None:
    """`**` matches any number of intermediate directories."""
    cfg = BoundaryConfig(include=["**/main.tf"])
    assert compute_boundary_state(Path("main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("a/main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("a/b/c/main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("a/b.tf"), cfg) == "out_of_boundary"


def test_directory_pattern_matches_recursively_per_gitignore_semantics() -> None:
    """gitwildmatch / .gitignore semantics: a pattern that matches a directory
    matches everything under it. So `boundary/*` matches `boundary/main.tf`
    AND `boundary/sub/main.tf` because `boundary/sub` matches and the file is
    under it. Customer-friendly: customers writing either `boundary/*` or
    `boundary/**` get the same "everything under boundary/" result.

    The narrower "files directly in boundary, no recursion" semantic is
    expressible via something like `boundary/*.tf` (one segment, file
    extension restricted) — which is what customers typically want when they
    care about non-recursion."""
    cfg = BoundaryConfig(include=["boundary/*"])
    assert compute_boundary_state(Path("boundary/main.tf"), cfg) == "in_boundary"
    assert compute_boundary_state(Path("boundary/sub/main.tf"), cfg) == "in_boundary"


def test_extension_pattern_at_root_is_non_recursive() -> None:
    """`*.tf` at the root level — files with .tf extension at root, but the
    pattern travels (per gitignore semantics) so `*.tf` actually matches at
    every level when not anchored. Customers wanting "only root .tf" use
    a leading `/` per gitignore: `/*.tf`."""
    cfg = BoundaryConfig(include=["*.tf"])
    assert compute_boundary_state(Path("main.tf"), cfg) == "in_boundary"
    # `*.tf` un-anchored matches at any depth — gitignore semantics.
    assert compute_boundary_state(Path("a/b/c.tf"), cfg) == "in_boundary"


# --- active_boundary_config context ----------------------------------------


def test_get_active_returns_none_outside_context() -> None:
    assert get_active_boundary_config() is None


def test_active_context_sets_and_restores() -> None:
    cfg = BoundaryConfig(include=["x/**"])
    assert get_active_boundary_config() is None
    with active_boundary_config(cfg):
        assert get_active_boundary_config() is cfg
    assert get_active_boundary_config() is None


def test_active_context_nested() -> None:
    """Nested activation respects scope: inner shadows outer; outer restored on exit."""
    outer = BoundaryConfig(include=["a/**"])
    inner = BoundaryConfig(include=["b/**"])
    with active_boundary_config(outer):
        assert get_active_boundary_config() is outer
        with active_boundary_config(inner):
            assert get_active_boundary_config() is inner
        assert get_active_boundary_config() is outer
    assert get_active_boundary_config() is None


# --- Evidence.create boundary integration ---------------------------------


def _ev(file: str = "infra/main.tf", **kwargs: object) -> Evidence:
    return Evidence.create(
        detector_id="aws.test",
        source_ref=SourceRef(file=Path(file), line_start=1, line_end=2),
        timestamp=datetime(2026, 4, 27, tzinfo=UTC),
        **kwargs,  # type: ignore[arg-type]
    )


def test_evidence_create_default_is_undeclared_without_active_config() -> None:
    ev = _ev()
    assert ev.boundary_state == "boundary_undeclared"


def test_evidence_create_picks_up_active_config() -> None:
    cfg = BoundaryConfig(include=["boundary/**"], exclude=["boundary/legacy/**"])
    with active_boundary_config(cfg):
        in_scope = _ev(file="boundary/main.tf")
        out_explicit = _ev(file="boundary/legacy/old.tf")
        out_implicit = _ev(file="commercial/eks.tf")
    assert in_scope.boundary_state == "in_boundary"
    assert out_explicit.boundary_state == "out_of_boundary"
    assert out_implicit.boundary_state == "out_of_boundary"


def test_evidence_create_explicit_boundary_state_overrides_context() -> None:
    """Explicit boundary_state arg trumps active context (test/utility path)."""
    cfg = BoundaryConfig(include=["boundary/**"])
    with active_boundary_config(cfg):
        ev = _ev(file="commercial/eks.tf", boundary_state="in_boundary")
    assert ev.boundary_state == "in_boundary"


def test_boundary_state_is_part_of_evidence_id() -> None:
    """Adding boundary_state to the model means logically-equivalent Evidence
    in different boundary contexts hashes differently — appropriate, since the
    boundary changes the meaning of the record."""
    e1 = _ev(boundary_state="in_boundary")
    e2 = _ev(boundary_state="out_of_boundary")
    e3 = _ev(boundary_state="boundary_undeclared")
    assert e1.evidence_id != e2.evidence_id
    assert e1.evidence_id != e3.evidence_id
    assert e2.evidence_id != e3.evidence_id


# --- BoundaryConfig schema -------------------------------------------------


def test_boundary_config_default_is_empty_lists() -> None:
    cfg = BoundaryConfig()
    assert cfg.include == []
    assert cfg.exclude == []


def test_boundary_config_round_trip_through_save_load(tmp_path: Path) -> None:
    """Save + load round-trips include/exclude through TOML cleanly."""
    from efterlev.config import Config, load_config, save_config

    cfg = Config(
        boundary=BoundaryConfig(include=["boundary/**", "infra/prod/**"], exclude=["**/test/**"])
    )
    path = tmp_path / "config.toml"
    save_config(cfg, path)
    restored = load_config(path)
    assert restored.boundary.include == ["boundary/**", "infra/prod/**"]
    assert restored.boundary.exclude == ["**/test/**"]


def test_save_config_omits_boundary_section_when_empty(tmp_path: Path) -> None:
    """Empty BoundaryConfig is the default (boundary_undeclared); the section
    should not appear in saved TOML — keeps the file minimal and avoids
    suggesting a meaningful empty declaration."""
    from efterlev.config import Config, save_config

    cfg = Config()
    path = tmp_path / "config.toml"
    save_config(cfg, path)
    text = path.read_text()
    assert "[boundary]" not in text


def test_load_config_accepts_missing_boundary_section(tmp_path: Path) -> None:
    """A hand-edited config without `[boundary]` should load cleanly with the
    default empty BoundaryConfig (boundary_undeclared)."""
    from efterlev.config import load_config

    toml = tmp_path / "no_boundary.toml"
    toml.write_text(
        "[llm]\n"
        'backend = "anthropic"\n'
        'fallback_model = "claude-sonnet-4-6"\n'
        "\n[scan]\n"
        'target_dir = "."\n'
        'output_dir = "./out"\n'
        "\n[baseline]\n"
        'id = "fedramp-20x-moderate"\n'
    )
    config = load_config(toml)
    assert config.boundary.include == []
    assert config.boundary.exclude == []


def test_boundary_config_rejects_unknown_field() -> None:
    """`extra="forbid"` on the model — a typo'd field surfaces immediately."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        BoundaryConfig(includes=["x"])  # type: ignore[call-arg]


# --- in_scope_evidence (gap-agent boundary enforcement, v0.1.219) -----------


def _ev_with_boundary(state: str, name: str) -> Evidence:
    return Evidence.create(
        detector_id="aws.encryption_s3_at_rest",
        source_ref=SourceRef(file=Path(f"{name}.tf"), line_start=1, line_end=3),
        ksis_evidenced=["KSI-SVC-PRR"],
        controls_evidenced=["SC-28"],
        content={"resource_name": name, "encryption_state": "present"},
        timestamp=datetime(2026, 6, 7, tzinfo=UTC),
        boundary_state=state,  # type: ignore[arg-type]
    )


def test_in_scope_evidence_drops_only_out_of_boundary() -> None:
    """Regression for the govnotes-demo gap #27 boundary leak (2026-06-07):
    the Gap Agent must not be fed out_of_boundary evidence. in_boundary and
    boundary_undeclared are kept; out_of_boundary is dropped."""
    from efterlev.agents.gap import in_scope_evidence

    keep_in = _ev_with_boundary("in_boundary", "prod_db")
    keep_undeclared = _ev_with_boundary("boundary_undeclared", "app")
    drop_out = _ev_with_boundary("out_of_boundary", "dev_scratch")

    result = in_scope_evidence([keep_in, drop_out, keep_undeclared])

    ids = {ev.evidence_id for ev in result}
    assert keep_in.evidence_id in ids
    assert keep_undeclared.evidence_id in ids
    assert drop_out.evidence_id not in ids


def test_in_scope_evidence_noop_when_nothing_out_of_boundary() -> None:
    """Boundary-free workspaces (every validated eval fixture) are unaffected —
    all records are boundary_undeclared, so the filter is a no-op. This is why
    the fix carries zero regression risk to the maintainer-validated baselines."""
    from efterlev.agents.gap import in_scope_evidence

    evs = [_ev_with_boundary("boundary_undeclared", f"r{i}") for i in range(3)]
    assert in_scope_evidence(evs) == evs
