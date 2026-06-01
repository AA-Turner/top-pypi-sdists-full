"""Tests for the interactive `efterlev init` wizard (v0.1.172, C3).

Covers the deterministic, non-prompt surface: the `efterlev start`
sidecar write+load round-trip, the loader's robustness, init_workspace
boundary persistence, and that non-interactive init is unchanged. The
prompt loop itself (typer.prompt) is exercised via the manual smoke in
the PR; here we test the pieces around it.
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.init_wizard import SUPPORTED_BASELINE, InitWizardResult
from efterlev.cli.main import app
from efterlev.cli.start_cli import (
    START_SIDECAR_MARKER,
    StartAnswers,
    load_start_sidecar,
)
from efterlev.config import BoundaryConfig, load_config

runner = CliRunner()


# --- start sidecar write + load round-trip -----------------------------


def test_start_out_writes_json_sidecar(tmp_path: Path) -> None:
    out = tmp_path / "fedramp-20x-path.md"
    result = runner.invoke(
        app,
        ["start", "--partition", "govcloud", "--architecture", "serverless", "--out", str(out)],
    )
    assert result.exit_code == 0, result.output
    sidecar = tmp_path / "fedramp-20x-path.json"
    assert sidecar.is_file()
    data = json.loads(sidecar.read_text())
    assert data["_efterlev"] == START_SIDECAR_MARKER
    assert data["partition"] == "govcloud"
    assert data["architecture"] == "serverless"


def test_start_no_out_writes_no_sidecar(tmp_path: Path) -> None:
    """Without --out, start prints to stdout and writes nothing."""
    result = runner.invoke(app, ["start", "--architecture", "vms"])
    assert result.exit_code == 0
    assert list(tmp_path.glob("*.json")) == []


def test_load_sidecar_round_trip(tmp_path: Path) -> None:
    answers = StartAnswers(
        cloud="aws",
        partition="govcloud",
        impact_level="moderate",
        architecture="serverless",
        posture="soc2",
    )
    sidecar = tmp_path / "fedramp-20x-path.json"
    sidecar.write_text(
        json.dumps({"_efterlev": START_SIDECAR_MARKER, "version": 1, **answers.__dict__})
    )
    loaded = load_start_sidecar([tmp_path])
    assert loaded is not None
    assert loaded.partition == "govcloud"
    assert loaded.posture == "soc2"


def test_load_sidecar_none_when_absent(tmp_path: Path) -> None:
    assert load_start_sidecar([tmp_path]) is None


def test_load_sidecar_ignores_unmarked_json(tmp_path: Path) -> None:
    (tmp_path / "other.json").write_text(json.dumps({"hello": "world"}))
    assert load_start_sidecar([tmp_path]) is None


def test_load_sidecar_tolerates_bad_json(tmp_path: Path) -> None:
    (tmp_path / "broken.json").write_text("{not valid json")
    assert load_start_sidecar([tmp_path]) is None


def test_load_sidecar_picks_newest(tmp_path: Path) -> None:
    import os
    import time

    old = tmp_path / "old.json"
    old.write_text(
        json.dumps({"_efterlev": START_SIDECAR_MARKER, "version": 1, "partition": "commercial"})
    )
    # Force a clearly older mtime on the first file.
    old_time = time.time() - 100
    os.utime(old, (old_time, old_time))
    new = tmp_path / "new.json"
    new.write_text(
        json.dumps({"_efterlev": START_SIDECAR_MARKER, "version": 1, "partition": "govcloud"})
    )
    loaded = load_start_sidecar([tmp_path])
    assert loaded is not None
    assert loaded.partition == "govcloud"


def test_load_sidecar_coerces_bad_field_to_default(tmp_path: Path) -> None:
    """A hand-edited sidecar with an invalid enum value falls back to default,
    not a crash."""
    (tmp_path / "x.json").write_text(
        json.dumps(
            {"_efterlev": START_SIDECAR_MARKER, "version": 1, "partition": "mars", "cloud": "aws"}
        )
    )
    loaded = load_start_sidecar([tmp_path])
    assert loaded is not None
    assert loaded.partition == "commercial"  # invalid "mars" → default


# --- InitWizardResult shape --------------------------------------------


def test_wizard_result_defaults() -> None:
    r = InitWizardResult()
    assert r.baseline == SUPPORTED_BASELINE
    assert r.llm_backend == "anthropic"
    assert r.llm_region is None
    assert r.boundary_include == []


# --- init_workspace boundary persistence -------------------------------


def test_init_workspace_persists_boundary(tmp_path: Path) -> None:
    from efterlev.workspace import init_workspace

    init_workspace(
        tmp_path,
        "fedramp-20x-moderate",
        boundary_config=BoundaryConfig(include=["infra/prod/**"], exclude=["**/test/**"]),
    )
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.boundary.include == ["infra/prod/**"]
    assert config.boundary.exclude == ["**/test/**"]


def test_init_workspace_no_boundary_is_empty(tmp_path: Path) -> None:
    from efterlev.workspace import init_workspace

    init_workspace(tmp_path, "fedramp-20x-moderate")
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.boundary.include == []
    assert config.boundary.exclude == []


# --- non-interactive init backward-compat ------------------------------


def test_init_non_tty_skips_wizard(tmp_path: Path) -> None:
    """CliRunner provides no TTY, so a bare `init` must NOT prompt — it
    inits with defaults exactly as before v0.1.172."""
    result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "Interactive setup" not in result.output
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.baseline.id == "fedramp-20x-moderate"
    assert config.llm.backend == "anthropic"


def test_init_flags_skip_wizard_even_with_no_interactive_default(tmp_path: Path) -> None:
    """Passing a config flag forces the scripted path (no wizard)."""
    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--llm-backend", "anthropic"])
    assert result.exit_code == 0, result.output
    assert "Interactive setup" not in result.output


def test_init_no_interactive_flag(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--no-interactive"])
    assert result.exit_code == 0, result.output
    assert "Interactive setup" not in result.output


# --- OpenAI backend default model (launch-readiness regression) --------


def test_init_openai_without_model_defaults_to_gpt_5_4_mini(tmp_path: Path) -> None:
    """`init --llm-backend=openai` with no --llm-model must pin the validated
    recommended model. Without this fix the config gets model=None, and the
    gap agent falls back to its Claude default ('claude-opus-4-7'), which the
    OpenAI API 404s. Regression for the broken default install path
    (interactive wizard never asks for a model either)."""
    from efterlev.config import DEFAULT_OPENAI_MODEL

    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--llm-backend", "openai"])
    assert result.exit_code == 0, result.output
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.llm.backend == "openai"
    assert config.llm.model == DEFAULT_OPENAI_MODEL == "gpt-5.4-mini"
    # No cross-provider Claude fallback baked into an OpenAI workspace.
    assert not config.llm.fallback_model.startswith("claude")


def test_init_openai_with_explicit_model_is_honored(tmp_path: Path) -> None:
    """An explicit --llm-model (e.g. gpt-5 for the safer failure mode) wins
    over the gpt-5.4-mini default."""
    result = runner.invoke(
        app,
        ["init", "--target", str(tmp_path), "--llm-backend", "openai", "--llm-model", "gpt-5"],
    )
    assert result.exit_code == 0, result.output
    config = load_config(tmp_path / ".efterlev" / "config.toml")
    assert config.llm.backend == "openai"
    assert config.llm.model == "gpt-5"
