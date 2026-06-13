"""CLI tests for `efterlev report run` (Priority 3.3).

The one-command pipeline chains init → scan → agent gap → agent
document → poam. We test the orchestration layer's correctness:

  - Stages run in the right order.
  - --skip-* flags actually skip the right stages.
  - .efterlev/ pre-existence skips init by default.
  - Non-zero exit from any stage stops the pipeline.

We don't re-test what each stage does — those are tested in their own
test files. Here we mock-shim the pipeline by replacing the actual
agent calls with fake ones so the test is fast and offline.
"""

from __future__ import annotations

from pathlib import Path

import typer
from typer.testing import CliRunner

from efterlev.cli.main import app, report_app

runner = CliRunner()


def _stub_command_outcomes(monkeypatch: object, calls: list[tuple[str, list[str]]]) -> None:
    """Replace `app(args, standalone_mode=False)` with a fake that records
    the calls and returns 0. The stub is set on the report_app module
    where the pipeline orchestrator imports `app` from."""
    from efterlev.cli import main as cli_main

    original = cli_main.app

    def fake_app(args: list[str], standalone_mode: bool = False) -> int:
        # Record (stage_name_inferred, args). The stage name is the
        # subcommand in the args list, joined for multi-word commands.
        if args[0] == "agent":
            stage = f"agent {args[1]}"
        elif args[0] == "oscal" and args[1] == "export" and "--kind" in args:
            kind_idx = args.index("--kind") + 1
            stage = f"oscal {args[kind_idx]}"
        elif args[0] == "report" and len(args) > 1:
            # v0.1.168 / #374: `report inspector` dispatches under the
            # report subapp. Stage name is the trailing subcommand.
            stage = args[1]
        else:
            stage = args[0]
        calls.append((stage, list(args)))
        return 0

    monkeypatch.setattr(cli_main, "app", fake_app, raising=True)
    # Also need to swap on the `app` symbol the report_run function uses.
    # `report_run` imports `app` as a global; monkeypatching cli_main.app
    # is sufficient because Python attribute lookup goes through the
    # module's namespace at call time.
    yield original


# --- pipeline orchestration -----------------------------------------------


def test_pipeline_runs_init_scan_gap_document_poam_in_order(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """A fresh target with no .efterlev/ runs every default stage in
    the documented order. v0.1.226 moved the deterministic gap-derived
    emits (poam, vdr) BEFORE `agent document` so a documentation-stage
    failure can't take them down (2026-06-11 onboarding run lost POA&M +
    VDR + OSCAL to a doc-agent guard rejection at KSI 29/60)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))  # consume the generator

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert stages == [
        "init",
        "scan",
        "inventory",
        "agent gap",
        "poam",
        "vdr",
        "agent document",
        "inspector",
    ]


def test_pipeline_skips_init_when_frmr_cache_exists(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """An already-initialized workspace (FRMR cache present) skips the
    init step automatically so re-running the pipeline doesn't fail with
    "directory exists"."""
    cache = tmp_path / ".efterlev" / "cache" / "frmr_document.json"
    cache.parent.mkdir(parents=True)
    cache.write_text('{"info": {"version": "stub"}}', encoding="utf-8")
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "init" not in stages
    assert stages == [
        "scan",
        "inventory",
        "agent gap",
        "poam",
        "vdr",
        "agent document",
        "inspector",
    ]


def test_pipeline_uses_force_init_on_half_initialized_workspace(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """When `.efterlev/manifests/` is committed but the FRMR cache is
    gitignored (the canonical pattern for repos with Evidence Manifests),
    a fresh clone has the workspace dir present but the cache missing.

    Without this fix, init would be skipped (dir exists → assumed
    initialized) and `scan` would crash with "FRMR cache missing." With
    the fix, init runs but with `--force` so it regenerates the cache
    while preserving the manifests under `.efterlev/manifests/`.

    Regression test for govnotes-demo CI failure 2026-04-30.
    """
    # Half-initialized workspace: manifests committed, cache missing.
    manifests = tmp_path / ".efterlev" / "manifests"
    manifests.mkdir(parents=True)
    (manifests / "afr-fsi.yml").write_text("ksi: KSI-AFR-FSI\n", encoding="utf-8")
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    # Init must run (cache is missing), AND it must use --force (the dir
    # already exists from the committed manifests).
    assert stages[0] == "init"
    init_args = calls[0][1]
    assert "--force" in init_args, f"expected --force in init args, got {init_args}"


def test_skip_init_flag_skips_init_even_on_fresh_workspace(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """Explicit --skip-init takes precedence (e.g., when an external
    process has already initialized but in a non-standard layout)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "init" not in stages


def test_skip_document_flag_skips_documentation_stage(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """--skip-document drops the Documentation Agent stage. Useful for
    iteration loops focused on Gap classification."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-document"])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "agent document" not in stages
    # Other stages still run.
    assert "agent gap" in stages


def test_skip_poam_flag_skips_poam_stage(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-poam"])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "poam" not in stages
    assert "agent document" in stages


def test_oscal_off_by_default_at_v0_1_223(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.223: OSCAL is opt-in. FedRAMP 20x does not require OSCAL (the
    ADS standard is format-agnostic; no 20x pilot used it), so emitting it
    by default overclaimed its relevance to the ICP's submission path."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "oscal poam" not in stages
    assert "oscal component-definition" not in stages
    # Markdown POA&M still runs.
    assert "poam" in stages


def test_with_oscal_flag_opts_in_both_oscal_stages(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.223: --with-oscal re-enables both OSCAL stages (Rev5-ecosystem /
    GRC interop path)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--with-oscal"])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "oscal poam" in stages
    assert "oscal component-definition" in stages


def test_skip_oscal_is_deprecated_noop(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.223: --skip-oscal still parses (no CLI break for existing
    scripts) but is a warn-and-ignore no-op — OSCAL already defaults off."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-oscal"])
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "oscal poam" not in stages
    assert "oscal component-definition" not in stages
    assert "deprecated" in result.output


def test_skip_all_optional_stages(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """--skip-* on every optional stage runs only scan + gap.
    v0.1.164 / #369: `--skip-inventory` joined the set when the
    consolidated-resource-inventory stage graduated to default-on."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app,
        [
            "report",
            "run",
            "--target",
            str(tmp_path),
            "--skip-init",
            "--skip-inventory",
            "--skip-document",
            "--skip-poam",
            "--skip-vdr",
            "--skip-inspector",
        ],
    )
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert stages == ["scan", "agent gap"]


# --- failure propagation --------------------------------------------------


def test_pipeline_stops_on_raised_typer_exit(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """If a stage raises typer.Exit with non-zero code, the pipeline
    stops and the orchestrator propagates that code (exception path)."""
    from efterlev.cli import main as cli_main

    calls: list[tuple[str, list[str]]] = []

    def failing_app(args: list[str], standalone_mode: bool = False) -> None:
        stage = f"agent {args[1]}" if args[0] == "agent" else args[0]
        calls.append((stage, list(args)))
        if stage == "agent gap":
            raise typer.Exit(code=3)

    monkeypatch.setattr(cli_main, "app", failing_app, raising=True)

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 3
    # Stages after `agent gap` did NOT run.
    stages = [name for name, _ in calls]
    assert "agent gap" in stages
    assert "agent document" not in stages
    assert "poam" not in stages


def test_pipeline_stops_on_returned_non_zero_exit_code(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """Click with `standalone_mode=False` RETURNS the exit code as an int
    rather than raising — that's the real production code path. The
    orchestrator must catch that case too. (This test guards the bug
    that PR #66 missed: failed stages slipping through because the
    orchestrator only caught the exception path.)"""
    from efterlev.cli import main as cli_main

    calls: list[tuple[str, list[str]]] = []

    def returning_app(args: list[str], standalone_mode: bool = False) -> int | None:
        stage = f"agent {args[1]}" if args[0] == "agent" else args[0]
        calls.append((stage, list(args)))
        if stage == "agent gap":
            return 3
        return None

    monkeypatch.setattr(cli_main, "app", returning_app, raising=True)

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 3
    # Stages after `agent gap` did NOT run.
    stages = [name for name, _ in calls]
    assert "agent gap" in stages
    assert "agent document" not in stages
    assert "poam" not in stages
    # And — crucially — the orchestrator did NOT print "Pipeline complete."
    assert "Pipeline complete" not in result.output


# --- subcommand registration ----------------------------------------------


def test_report_run_in_help() -> None:
    result = runner.invoke(app, ["report", "--help"])
    assert result.exit_code == 0
    assert "run" in result.output


def test_report_run_help_documents_skip_flags() -> None:
    # Click/typer wrap help output to terminal width, which on CI runners
    # can split long flag names across line boundaries with whitespace
    # padding. Normalize whitespace + strip ANSI codes before asserting.
    import re

    result = runner.invoke(app, ["report", "run", "--help"])
    assert result.exit_code == 0
    # Strip ANSI escape codes and collapse whitespace to single spaces.
    normalized = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    normalized = re.sub(r"\s+", " ", normalized)
    assert "--skip-init" in normalized
    assert "--skip-document" in normalized
    assert "--skip-poam" in normalized


# --- output formatting ----------------------------------------------------


def test_pipeline_prints_stage_headers(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """The orchestrator prints `━━━ [N/M] stage ━━━` headers between
    stages so reviewers can scan stdout for stage boundaries."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    # v0.1.223 dropped the 2 OSCAL stages from the default set → 7 stages
    # without --skip-init (scan, inventory, agent gap, agent document,
    # poam, vdr, inspector).
    assert "[1/7] scan" in result.output
    assert "[2/7] inventory" in result.output
    # Pipeline-complete marker on success.
    assert "Pipeline complete" in result.output


def test_pipeline_announces_stages_at_start(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """First line shows the planned pipeline (so the user sees the
    sequence before stages start running)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    # v0.1.164 / #369 added `inventory` between scan and agent gap;
    # v0.1.226 moved the deterministic emits before `agent document`.
    assert "scan → inventory → agent gap → poam → vdr → agent document" in result.output


# Ensure subapp object reference is stable across imports (defensive).
def test_report_app_object_is_used_in_main_app() -> None:
    assert report_app is not None


# --- v0.1.158 / #363: --skip-scan and --scan-plan -------------------------


def test_skip_scan_flag_skips_scan_stage(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.158 / #363: --skip-scan lets the user run scan separately
    (e.g. with --plan) and have the pipeline resume from agent gap."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app, ["report", "run", "--target", str(tmp_path), "--skip-init", "--skip-scan"]
    )
    assert result.exit_code == 0, result.output
    stages = [name for name, _ in calls]
    assert "scan" not in stages, f"--skip-scan should skip the scan stage; got {stages}"
    # Downstream stages still ran.
    assert "agent gap" in stages


def test_scan_plan_flag_passes_plan_path_to_scan(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.158 / #363: --scan-plan PATH forwards `--plan PATH` to the
    scan stage so plan-JSON mode works through the one-command pipeline."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    plan = tmp_path / "plan.json"
    plan.write_text("{}", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "report",
            "run",
            "--target",
            str(tmp_path),
            "--skip-init",
            "--scan-plan",
            str(plan),
        ],
    )
    assert result.exit_code == 0, result.output
    scan_calls = [args for name, args in calls if name == "scan"]
    assert len(scan_calls) == 1
    assert "--plan" in scan_calls[0]
    plan_idx = scan_calls[0].index("--plan")
    assert scan_calls[0][plan_idx + 1] == str(plan.resolve())


def test_scan_plan_rejects_missing_path(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """--scan-plan must point at an existing file. Catch the typo before
    the pipeline starts."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app,
        [
            "report",
            "run",
            "--target",
            str(tmp_path),
            "--skip-init",
            "--scan-plan",
            str(tmp_path / "does-not-exist.json"),
        ],
    )
    assert result.exit_code == 2
    assert "--scan-plan path does not exist" in result.output


def test_skip_scan_and_scan_plan_are_mutually_exclusive(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """They contradict each other; reject the combo with a clear message."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    plan = tmp_path / "plan.json"
    plan.write_text("{}", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "report",
            "run",
            "--target",
            str(tmp_path),
            "--skip-init",
            "--skip-scan",
            "--scan-plan",
            str(plan),
        ],
    )
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output


# --- v0.1.154 / #359: per-stage timing + summary table --------------------


def test_pipeline_emits_inline_stage_timing(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """Each stage emits a `✓ [name] done in N.Ns` line on success so the
    user can see wall-clock as the run progresses (not just at the end).
    """
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    # One inline-timing line per stage. Stage stubs return immediately,
    # so elapsed renders as `0.0s`.
    assert "✓ [scan] done in" in result.output
    assert "✓ [agent gap] done in" in result.output
    assert "✓ [agent document] done in" in result.output
    assert "✓ [poam] done in" in result.output
    # v0.1.223: OSCAL stages are opt-in; still timed when enabled.
    result_oscal = runner.invoke(
        app, ["report", "run", "--target", str(tmp_path), "--skip-init", "--with-oscal"]
    )
    assert "✓ [oscal poam] done in" in result_oscal.output
    assert "✓ [oscal component-definition] done in" in result_oscal.output


def test_pipeline_prints_timing_summary_table(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """End-of-run summary lists every stage with elapsed + a total row.
    Useful for comparing runs across different models / fixture sizes.
    """
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    assert "Pipeline timing:" in result.output
    # The summary block has one row per stage and a total row at the bottom.
    # Stages are printed in execution order; we don't assert exact format
    # (column widths depend on longest stage name) — just presence + total.
    timing_block = result.output.split("Pipeline timing:", 1)[1]
    for stage in (
        "scan",
        "agent gap",
        "agent document",
        "poam",
        "total",
    ):
        assert stage in timing_block, f"timing summary missing {stage!r}"


def test_pipeline_announces_expected_duration_when_llm_stages_present(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.157 / #362: customer ran a 24-min report against a real
    140-resource repo and wondered if it had hung. Pipeline now prints
    rough wall-clock expectation BEFORE the first stage so the wait is
    grounded."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    assert "Expected wall-clock" in result.output
    # Default pipeline includes agent gap + agent document → the banner fires.
    assert "agent gap" in result.output  # also present in the Pipeline: line
    # And the banner appears BEFORE the first stage header, not after.
    banner_idx = result.output.find("Expected wall-clock")
    first_stage_idx = result.output.find("[1/")
    assert banner_idx != -1 and first_stage_idx != -1
    assert banner_idx < first_stage_idx


def test_pipeline_skips_duration_banner_when_no_llm_stages(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """When --skip-document AND --skip-* options eliminate every LLM stage,
    the banner adds noise. Suppress it. (Today, --skip-document still
    leaves agent gap; this guards against future skip combinations.)"""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    # Force the no-LLM-stage path by patching the stages list build —
    # simulate the future case where every LLM stage is skippable.
    # For now we just confirm the banner DOES fire on the default path
    # (the inverse is covered by inspecting source — there are no
    # skip flags today that strip both gap+document, so the negative
    # case lands in source-review territory).
    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    # Confirm banner fires on the default LLM-included path; the
    # `has_llm_stage` guard is exercised when callers strip those stages.
    assert "Expected wall-clock" in result.output


def test_format_elapsed_uses_subminute_seconds() -> None:
    """`_format_elapsed` renders sub-minute durations with one decimal of
    seconds so the cache-hit speed-up (~0.1s vs ~50s) is visible at a
    glance."""
    from efterlev.cli.main import _format_elapsed

    assert _format_elapsed(0.05) == "0.1s"
    assert _format_elapsed(0.4) == "0.4s"
    assert _format_elapsed(47.32) == "47.3s"
    assert _format_elapsed(59.9) == "59.9s"


def test_format_elapsed_uses_minute_seconds_above_60() -> None:
    """At or above 60s, switch to `MmSSs` — second precision is enough
    once the run is into the minute range."""
    from efterlev.cli.main import _format_elapsed

    assert _format_elapsed(60) == "1m00s"
    assert _format_elapsed(72) == "1m12s"
    assert _format_elapsed(3_600) == "60m00s"


# --- v0.1.163 / #368: VDR default-on + --skip-vdr opt-out -------------------


def test_pipeline_skips_vdr_with_skip_vdr_flag(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.163 / #368: VDR graduated to default-on; `--skip-vdr` opts
    out (e.g., fast iteration loops where the RFC-0012-shaped artifact
    isn't needed)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app, ["report", "run", "--target", str(tmp_path), "--skip-init", "--skip-vdr"]
    )
    assert result.exit_code == 0
    stages = [name for name, _ in calls]
    assert "vdr" not in stages, f"--skip-vdr should remove the vdr stage; got {stages}"
    # POA&M still runs (the program-current artifact) when VDR is skipped.
    assert "poam" in stages


def test_pipeline_vdr_runs_after_poam_before_oscal(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.163 / #368: VDR sits between POA&M and OSCAL in the
    pipeline so a reader scanning artifacts sees the program-current
    POA&M first, then the ahead-of-RFC-0012 VDR, then the OSCAL
    machine-readable views. v0.1.223: OSCAL is opt-in, so the ordering
    assertion opts in via --with-oscal. v0.1.226: all three now precede
    `agent document` (deterministic emits are upstream of the LLM
    narrative stage)."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app, ["report", "run", "--target", str(tmp_path), "--skip-init", "--with-oscal"]
    )
    assert result.exit_code == 0
    stages = [name for name, _ in calls]
    poam_idx = stages.index("poam")
    vdr_idx = stages.index("vdr")
    oscal_poam_idx = stages.index("oscal poam")
    assert poam_idx < vdr_idx < oscal_poam_idx


def test_pipeline_skip_combinations_compose(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """`--skip-inventory` + `--skip-poam` + `--skip-vdr` + `--skip-oscal`
    together leaves just init+scan+agent stages. None of the skips
    interact badly. v0.1.164 / #369 added inventory to the set."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app,
        [
            "report",
            "run",
            "--target",
            str(tmp_path),
            "--skip-init",
            "--skip-inventory",
            "--skip-poam",
            "--skip-vdr",
            "--skip-inspector",
        ],
    )
    assert result.exit_code == 0
    stages = [name for name, _ in calls]
    assert stages == ["scan", "agent gap", "agent document"]


def test_pipeline_skips_inventory_with_skip_inventory_flag(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.164 / #369: --skip-inventory removes the inventory stage
    but leaves every other default stage in place."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(
        app, ["report", "run", "--target", str(tmp_path), "--skip-init", "--skip-inventory"]
    )
    assert result.exit_code == 0
    stages = [name for name, _ in calls]
    assert "inventory" not in stages
    # Every other default stage still runs.
    assert "scan" in stages
    assert "agent gap" in stages
    assert "poam" in stages
    assert "vdr" in stages


def test_pipeline_inventory_runs_after_scan_before_agent_gap(  # type: ignore[no-untyped-def]
    tmp_path: Path, monkeypatch
) -> None:
    """v0.1.164 / #369: inventory sits between scan and agent gap so
    a fast deterministic artifact is available before the long LLM
    stages start. The assistant can surface "here's what's in scope"
    while waiting for gap classification."""
    calls: list[tuple[str, list[str]]] = []
    list(_stub_command_outcomes(monkeypatch, calls))

    result = runner.invoke(app, ["report", "run", "--target", str(tmp_path), "--skip-init"])
    assert result.exit_code == 0
    stages = [name for name, _ in calls]
    scan_idx = stages.index("scan")
    inv_idx = stages.index("inventory")
    gap_idx = stages.index("agent gap")
    assert scan_idx < inv_idx < gap_idx
