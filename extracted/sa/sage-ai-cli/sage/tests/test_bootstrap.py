"""Tests for core/bootstrap.py — orchestration + per-phase logic.

Mocks every external boundary (subprocess, httpx, gsutil, llama_cpp).
"""

from __future__ import annotations

import subprocess
import sys
import types
from pathlib import Path

import pytest


# ── Helpers ───────────────────────────────────────────────────────────

def _make_run(returncode: int = 0, stdout: str = "", stderr: str = ""):
    def _run(cmd, capture_output=True, text=True, timeout=None, **kw):
        return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)
    return _run


# ── BootstrapOptions / BootstrapResult ────────────────────────────────

def test_bootstrap_options_defaults(monkeypatch):
    # Force the high-disk tier so the test is deterministic regardless of
    # what the host's free disk actually is. Without this, on a 30GB-free
    # machine the picker selects qwen2.5-coder-7b and the assertion fails.
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap, "_free_gb_at", lambda _p: 200.0)
    opts = bootstrap.BootstrapOptions()
    assert opts.pull_models is True
    assert opts.set_default is True
    assert opts.prewarm is True
    assert opts.build_llama_cpp is True
    assert opts.install_deps is True
    assert opts.build_rag is True
    assert opts.mirror_datasets is True
    assert opts.finetune is False  # heavy: opt-in
    assert "qwen3-coder-next" in opts.ollama_models
    assert "nomic-embed-text" in opts.ollama_models
    assert "codealpaca-20k" in opts.mirror_dataset_names


def test_phase_outcome_emoji_mapping():
    from sage.core.bootstrap import PhaseOutcome
    assert PhaseOutcome("x", "ok", 0.0).emoji == "✓"
    assert PhaseOutcome("x", "skipped", 0.0).emoji == "⊘"
    assert PhaseOutcome("x", "failed", 0.0).emoji == "✗"
    assert PhaseOutcome("x", "weird", 0.0).emoji == "?"


def test_bootstrap_result_summary_renders():
    from sage.core.bootstrap import BootstrapResult, PhaseOutcome
    r = BootstrapResult()
    r.add(PhaseOutcome("alpha", "ok", 1.5, "did the thing"))
    r.add(PhaseOutcome("beta", "failed", 0.5, "boom"))
    r.total_duration_s = 2.0
    s = r.summary()
    assert "alpha" in s and "beta" in s
    assert "✓" in s and "✗" in s
    assert "2.0s" in s


def test_bootstrap_result_all_ok_false_with_failure():
    from sage.core.bootstrap import BootstrapResult, PhaseOutcome
    r = BootstrapResult()
    r.add(PhaseOutcome("a", "ok", 0.0))
    r.add(PhaseOutcome("b", "failed", 0.0))
    assert r.all_ok is False


def test_bootstrap_result_all_ok_with_skipped():
    from sage.core.bootstrap import BootstrapResult, PhaseOutcome
    r = BootstrapResult()
    r.add(PhaseOutcome("a", "ok", 0.0))
    r.add(PhaseOutcome("b", "skipped", 0.0))
    assert r.all_ok is True


# ── Phase: pull-ollama-models ──────────────────────────────────────────

def test_phase_pull_skipped_without_ollama(monkeypatch):
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: False)
    status, detail = bootstrap.phase_pull_ollama_models(bootstrap.BootstrapOptions())
    assert status == "skipped"
    assert "ollama not installed" in detail


def test_phase_pull_skips_already_installed(monkeypatch):
    from sage.core import bootstrap

    # Force high-disk tier so opts.ollama_models is deterministic.
    monkeypatch.setattr(bootstrap, "_free_gb_at", lambda _p: 200.0)
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)

    class _Resp:
        def json(self): return {"models": [
            {"name": "qwen3-coder-next:latest"},
            {"name": "qwen2.5-coder-7b:latest"},
            {"name": "llama3.2:latest"},
            {"name": "nomic-embed-text:latest"},
        ]}
    fake_httpx = types.SimpleNamespace(get=lambda *a, **kw: _Resp())
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)

    opts = bootstrap.BootstrapOptions(quiet=True)
    status, detail = bootstrap.phase_pull_ollama_models(opts)
    assert status == "skipped"


def test_phase_pull_calls_subprocess_for_missing(monkeypatch):
    from sage.core import bootstrap

    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)

    class _Resp:
        def json(self): return {"models": [{"name": "llama3.2:latest"}]}
    monkeypatch.setitem(sys.modules, "httpx",
                        types.SimpleNamespace(get=lambda *a, **kw: _Resp()))

    calls = []
    def fake_run(cmd, **kw):
        calls.append(cmd)
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(bootstrap.subprocess, "run", fake_run)

    opts = bootstrap.BootstrapOptions(
        quiet=True, ollama_models=("qwen3-coder-next", "nomic-embed-text"))
    status, detail = bootstrap.phase_pull_ollama_models(opts)
    assert status == "ok"
    assert len(calls) == 2
    assert all("ollama" in c[0] and c[1] == "pull" for c in calls)


def test_phase_pull_records_failures(monkeypatch):
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)
    monkeypatch.setitem(sys.modules, "httpx",
                        types.SimpleNamespace(
                            get=lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("offline"))
                        ))
    monkeypatch.setattr(bootstrap.subprocess, "run", _make_run(1))
    opts = bootstrap.BootstrapOptions(quiet=True, ollama_models=("a", "b"))
    status, detail = bootstrap.phase_pull_ollama_models(opts)
    assert status == "failed"
    assert "rc=1" in detail


# ── Phase: set-default-model ───────────────────────────────────────────

def test_phase_set_default_skipped_when_unchanged(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core import bootstrap
    monkeypatch.setattr("sage.core.auto_model.auto_pick_default_model",
                        lambda current: current)
    status, detail = bootstrap.phase_set_default_model(bootstrap.BootstrapOptions())
    assert status == "skipped"


def test_phase_set_default_updates_when_picker_disagrees(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import load_config, save_config, SageConfig
    from sage.core import bootstrap

    # Pin a known starting default. Without this, if the SageConfig default
    # ever happens to match the picker's return value, the picker
    # short-circuits to "skipped" instead of "ok" — making this test flaky
    # under test-order-dependent state pollution.
    save_config(SageConfig(default_model="llama_cpp:starting-default"))

    monkeypatch.setattr("sage.core.auto_model.auto_pick_default_model",
                        lambda current: "ollama:qwen3-coder-next")
    # Sanity-check the patch actually applied (catches cleanup bugs from
    # earlier tests in the same session).
    from sage.core.auto_model import auto_pick_default_model
    assert auto_pick_default_model("anything") == "ollama:qwen3-coder-next"

    status, detail = bootstrap.phase_set_default_model(bootstrap.BootstrapOptions())
    assert status == "ok", f"phase returned {status!r} ({detail})"
    cfg = load_config()
    assert cfg.default_model == "ollama:qwen3-coder-next"


# ── Phase: prewarm ────────────────────────────────────────────────────

def test_phase_prewarm_skipped_for_non_ollama_model(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="llama_cpp:something"))
    from sage.core import bootstrap
    status, detail = bootstrap.phase_prewarm(bootstrap.BootstrapOptions())
    assert status == "skipped"


def test_phase_prewarm_calls_keep_alive(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="ollama:qwen3-coder-next"))
    from sage.core import bootstrap
    monkeypatch.setattr("sage.core.keep_alive.prewarm", lambda name: True)
    status, detail = bootstrap.phase_prewarm(bootstrap.BootstrapOptions())
    assert status == "ok"
    assert "qwen3-coder-next" in detail


def test_phase_prewarm_failure_when_ollama_down(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="ollama:qwen3-coder-next"))
    from sage.core import bootstrap
    monkeypatch.setattr("sage.core.keep_alive.prewarm", lambda name: False)
    status, detail = bootstrap.phase_prewarm(bootstrap.BootstrapOptions())
    assert status == "failed"


# ── Phase: build-llama-cpp ─────────────────────────────────────────────

def test_phase_build_llama_cpp_skipped_without_install(monkeypatch):
    from sage.core import bootstrap
    if "llama_cpp" in sys.modules:
        monkeypatch.delitem(sys.modules, "llama_cpp", raising=False)
    monkeypatch.setattr("builtins.__import__", lambda name, *a, **kw: (
        (_ for _ in ()).throw(ImportError("no llama_cpp")) if name == "llama_cpp"
        else __import__(name, *a, **kw)
    ))
    status, detail = bootstrap.phase_build_llama_cpp(bootstrap.BootstrapOptions(quiet=True))
    assert status == "skipped"


def test_phase_build_llama_cpp_succeeds_when_pip_returns_zero(monkeypatch):
    from sage.core import bootstrap
    fake_lc = types.SimpleNamespace(__file__="/fake/llama_cpp/__init__.py")
    monkeypatch.setitem(sys.modules, "llama_cpp", fake_lc)
    monkeypatch.setattr(bootstrap.subprocess, "run", _make_run(0))
    status, detail = bootstrap.phase_build_llama_cpp(bootstrap.BootstrapOptions(quiet=True))
    assert status == "ok"


def test_phase_build_llama_cpp_records_pip_failure(monkeypatch):
    from sage.core import bootstrap
    fake_lc = types.SimpleNamespace(__file__="/fake/llama_cpp/__init__.py")
    monkeypatch.setitem(sys.modules, "llama_cpp", fake_lc)
    monkeypatch.setattr(bootstrap.subprocess, "run", _make_run(2))
    status, detail = bootstrap.phase_build_llama_cpp(bootstrap.BootstrapOptions(quiet=True))
    assert status == "failed"
    assert "rc=2" in detail


# ── Phase: install-optional-deps ───────────────────────────────────────

def test_phase_install_deps_skipped_when_all_present(monkeypatch):
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap.importlib, "import_module", lambda name: types.SimpleNamespace())
    status, detail = bootstrap.phase_install_optional_deps(
        bootstrap.BootstrapOptions(quiet=True))
    assert status == "skipped"


def test_phase_install_deps_calls_pip_for_missing(monkeypatch):
    import importlib
    from sage.core import bootstrap

    def fake_import(name):
        if name == "sqlite_vec":
            raise ImportError("nope")
        return types.SimpleNamespace()
    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.setattr(bootstrap.subprocess, "run", _make_run(0))
    status, detail = bootstrap.phase_install_optional_deps(
        bootstrap.BootstrapOptions(quiet=True))
    assert status == "ok"
    assert "sqlite-vec" in detail


def test_phase_install_deps_records_pip_failure(monkeypatch):
    import importlib
    from sage.core import bootstrap

    def fake_import(name):
        raise ImportError("nope")
    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.setattr(bootstrap.subprocess, "run", _make_run(1, stderr="pip exploded"))
    status, detail = bootstrap.phase_install_optional_deps(
        bootstrap.BootstrapOptions(quiet=True))
    assert status == "failed"
    assert "pip rc=1" in detail


# ── Phase: build-rag-index ─────────────────────────────────────────────

def test_phase_build_rag_returns_skipped_for_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    class _Stub:
        dim = 4
        def embed(self, texts):
            return [[1.0, 0, 0, 0]] * len(texts)

    # Patch the embedder used by RAGIndex so we don't hit Ollama
    import sage.core.rag as rag
    monkeypatch.setattr(rag, "OllamaEmbedder", lambda *a, **kw: _StubEmbedder())

    class _StubEmbedder:
        dim = 4
        def embed(self, texts):
            return [[1.0, 0, 0, 0]] * len(texts)

    monkeypatch.setattr(rag, "OllamaEmbedder", lambda *a, **kw: _StubEmbedder())
    from sage.core import bootstrap
    opts = bootstrap.BootstrapOptions(cwd=tmp_path / "empty", quiet=True)
    (tmp_path / "empty").mkdir()
    status, detail = bootstrap.phase_build_rag_index(opts)
    assert status == "skipped"


def test_phase_build_rag_indexes_when_files_present(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    class _StubEmbedder:
        dim = 4
        def embed(self, texts):
            return [[1.0, 0, 0, 0]] * len(texts)
    import sage.core.rag as rag
    monkeypatch.setattr(rag, "OllamaEmbedder", lambda *a, **kw: _StubEmbedder())

    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "a.py").write_text("def foo(): pass\n")
    (proj / "b.py").write_text("def bar(): pass\n")

    from sage.core import bootstrap
    opts = bootstrap.BootstrapOptions(cwd=proj, quiet=True)
    status, detail = bootstrap.phase_build_rag_index(opts)
    assert status == "ok"
    assert "files" in detail and "chunks" in detail


# ── Phase: mirror-datasets ─────────────────────────────────────────────

def test_phase_mirror_datasets_skipped_without_gsutil(monkeypatch):
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: False)
    status, detail = bootstrap.phase_mirror_datasets(bootstrap.BootstrapOptions(quiet=True))
    assert status == "skipped"


def test_phase_mirror_datasets_calls_mirror_all(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core import bootstrap
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)

    captured = {}
    def fake_mirror_all(self, selected, *, skip_existing=True, languages=None):
        captured["names"] = [d.name for d in selected]
        return {"mirrored": ["x"], "skipped": [], "failed": []}
    monkeypatch.setattr("sage.training.datasets.DatasetMirror.mirror_all",
                        fake_mirror_all)

    opts = bootstrap.BootstrapOptions(quiet=True,
                                      mirror_dataset_names=("codealpaca-20k", "mbpp"))
    status, detail = bootstrap.phase_mirror_datasets(opts)
    assert status == "ok"
    assert sorted(captured["names"]) == ["codealpaca-20k", "mbpp"]
    assert "mirrored=1" in detail


# ── Phase: finetune-background ─────────────────────────────────────────

def test_phase_finetune_background_uses_popen(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="ollama:fake"))
    from sage.core import bootstrap

    captured = {}
    class _Pop:
        def __init__(self, cmd, **kw):
            captured["cmd"] = cmd
            captured["kw"] = kw
    monkeypatch.setattr("subprocess.Popen", _Pop)
    opts = bootstrap.BootstrapOptions(quiet=True, finetune_background=True, cwd=tmp_path)
    status, detail = bootstrap.phase_finetune_background(opts)
    assert status == "ok"
    assert "background" in detail
    assert "finetune" in captured["cmd"]


def test_phase_finetune_foreground_uses_call(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="ollama:fake"))
    from sage.core import bootstrap

    monkeypatch.setattr("subprocess.call", lambda cmd, cwd: 0)
    opts = bootstrap.BootstrapOptions(quiet=True, finetune_background=False, cwd=tmp_path)
    status, detail = bootstrap.phase_finetune_background(opts)
    assert status == "ok"


def test_phase_finetune_records_call_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import save_config, SageConfig
    save_config(SageConfig(default_model="ollama:fake"))
    from sage.core import bootstrap

    monkeypatch.setattr("subprocess.call", lambda cmd, cwd: 5)
    opts = bootstrap.BootstrapOptions(quiet=True, finetune_background=False, cwd=tmp_path)
    status, detail = bootstrap.phase_finetune_background(opts)
    assert status == "failed"
    assert "rc=5" in detail


# ── Top-level run_bootstrap ────────────────────────────────────────────

def test_run_bootstrap_skips_disabled_phases(monkeypatch):
    from sage.core import bootstrap
    opts = bootstrap.BootstrapOptions(
        quiet=True,
        pull_models=False, set_default=False, prewarm=False,
        build_llama_cpp=False, install_deps=False, build_rag=False,
        mirror_datasets=False, finetune=False,
    )
    result = bootstrap.run_bootstrap(opts)
    assert all(p.status == "skipped" for p in result.phases)
    assert result.all_ok is True


def test_run_bootstrap_records_per_phase_outcomes(monkeypatch):
    from sage.core import bootstrap
    # Force every individual phase to skip via _have_cmd / config
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: False)
    opts = bootstrap.BootstrapOptions(
        quiet=True, build_llama_cpp=False, install_deps=False,
        build_rag=False, finetune=False,
    )
    result = bootstrap.run_bootstrap(opts)
    # Should have one outcome per phase tuple (8)
    assert len(result.phases) == len(bootstrap.PHASES)


def test_run_bootstrap_phase_exception_marked_failed(monkeypatch):
    """When a phase's underlying logic raises, _run() must catch + mark failed."""
    from sage.core import bootstrap
    def boom(opts):
        raise RuntimeError("kaboom")
    # PHASES holds direct function refs; rebuild the tuple with our boom in slot 0
    new_phases = ((bootstrap.PHASES[0][0], boom, bootstrap.PHASES[0][2]),
                  *bootstrap.PHASES[1:])
    monkeypatch.setattr(bootstrap, "PHASES", new_phases)
    opts = bootstrap.BootstrapOptions(
        quiet=True, set_default=False, prewarm=False,
        build_llama_cpp=False, install_deps=False, build_rag=False,
        mirror_datasets=False, finetune=False,
    )
    result = bootstrap.run_bootstrap(opts)
    failed = [p for p in result.phases if p.status == "failed"]
    assert any("kaboom" in p.detail for p in failed)


# ── Ensure-Ollama-running helper (Bug 3) ───────────────────────────────


class _OllamaResponses:
    """Cycle through scripted httpx.get responses for tests."""

    def __init__(self, script):
        self._script = list(script)
        self._idx = 0

    def __call__(self, url, *args, **kwargs):
        i = min(self._idx, len(self._script) - 1)
        self._idx += 1
        entry = self._script[i]
        if isinstance(entry, type) and issubclass(entry, Exception):
            raise entry("simulated")
        resp = types.SimpleNamespace(status_code=entry)
        resp.json = lambda: {"models": []}
        return resp


def test_ensure_ollama_running_returns_true_when_already_up(monkeypatch):
    from sage.core import bootstrap

    fake_httpx = types.SimpleNamespace(get=_OllamaResponses([200]))
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    popen_calls = []
    monkeypatch.setattr(bootstrap.subprocess, "Popen",
                        lambda *a, **kw: popen_calls.append((a, kw)) or types.SimpleNamespace(pid=12345))

    assert bootstrap._ensure_ollama_running() is True
    assert popen_calls == []


def test_ensure_ollama_running_starts_daemon_then_succeeds(monkeypatch):
    from sage.core import bootstrap

    fake_httpx = types.SimpleNamespace(get=_OllamaResponses([ConnectionError, 200]))
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)
    popen_calls = []
    monkeypatch.setattr(bootstrap.subprocess, "Popen",
                        lambda *a, **kw: popen_calls.append(a) or types.SimpleNamespace(pid=12345))
    monkeypatch.setattr(bootstrap.time, "sleep", lambda s: None)

    assert bootstrap._ensure_ollama_running(timeout=2.0) is True
    assert len(popen_calls) == 1
    argv = popen_calls[0][0]
    assert argv[0] == "ollama"
    assert "serve" in argv


def test_ensure_ollama_running_returns_false_when_daemon_never_ready(monkeypatch):
    from sage.core import bootstrap

    fake_httpx = types.SimpleNamespace(get=_OllamaResponses([ConnectionError]))
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: True)
    monkeypatch.setattr(bootstrap.subprocess, "Popen",
                        lambda *a, **kw: types.SimpleNamespace(pid=12345))
    monkeypatch.setattr(bootstrap.time, "sleep", lambda s: None)

    assert bootstrap._ensure_ollama_running(timeout=0.5) is False


def test_ensure_ollama_running_returns_false_when_ollama_not_installed(monkeypatch):
    from sage.core import bootstrap

    fake_httpx = types.SimpleNamespace(get=_OllamaResponses([ConnectionError]))
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    monkeypatch.setattr(bootstrap, "_have_cmd", lambda c: False)
    popen_calls = []
    monkeypatch.setattr(bootstrap.subprocess, "Popen",
                        lambda *a, **kw: popen_calls.append(a) or types.SimpleNamespace(pid=12345))
    monkeypatch.setattr(bootstrap.time, "sleep", lambda s: None)

    assert bootstrap._ensure_ollama_running(timeout=1.0) is False
    assert popen_calls == []


def test_phase_prewarm_starts_ollama_if_needed(monkeypatch):
    from sage.core import bootstrap
    from sage.config import SageConfig

    # `phase_prewarm` calls load_config() with no args, which uses the
    # frozen default CONFIG_PATH from import time. Patch load_config itself
    # so the test doesn't depend on the host's ~/.sage/config.json.
    monkeypatch.setattr(
        "sage.config.load_config",
        lambda *a, **kw: SageConfig(default_model="ollama:llama3.2"),
    )

    ensure_calls = []
    monkeypatch.setattr(
        bootstrap, "_ensure_ollama_running",
        lambda timeout=15.0: ensure_calls.append(timeout) or True,
    )

    prewarm_calls = []
    monkeypatch.setattr(
        "sage.core.keep_alive.prewarm",
        lambda model, **kw: prewarm_calls.append(model) or True,
    )

    opts = bootstrap.BootstrapOptions()
    status, _detail = bootstrap.phase_prewarm(opts)
    assert status == "ok"
    assert ensure_calls, "phase_prewarm must call _ensure_ollama_running"
    assert prewarm_calls == ["llama3.2"]


def test_phase_build_rag_index_starts_ollama_if_needed(tmp_path, monkeypatch):
    from sage.core import bootstrap

    ensure_calls = []
    monkeypatch.setattr(
        bootstrap, "_ensure_ollama_running",
        lambda timeout=15.0: ensure_calls.append(timeout) or True,
    )

    class _FakeIndex:
        def __init__(self, _cwd):
            pass

        def reindex(self):
            return {"files_seen": 1, "chunks_added": 1, "vec_backend": "sqlite-vec"}

    monkeypatch.setattr("sage.core.rag.RAGIndex", _FakeIndex)

    (tmp_path / "x.py").write_text("def f():\n    pass\n")
    opts = bootstrap.BootstrapOptions(cwd=tmp_path)
    status, _detail = bootstrap.phase_build_rag_index(opts)
    assert status == "ok"
    assert ensure_calls, "phase_build_rag_index must call _ensure_ollama_running"


# ── CLI integration ───────────────────────────────────────────────────

def test_bootstrap_cli_command_registered():
    """The `sage ext bootstrap` command should be registered."""
    from sage.cli_extensions import extensions_app
    cmd_names = {c.name for c in extensions_app.registered_commands}
    assert "bootstrap" in cmd_names


def test_bootstrap_cli_runs_with_all_skip_flags(monkeypatch):
    """Smoke test the CLI wrapper end-to-end with everything skipped."""
    from typer.testing import CliRunner
    from sage.cli_extensions import extensions_app
    runner = CliRunner()
    result = runner.invoke(extensions_app, [
        "bootstrap", "--quiet",
        "--no-pull-models", "--no-set-default", "--no-prewarm",
        "--no-build-llama-cpp", "--no-install-deps",
        "--no-build-rag", "--no-mirror-datasets",
    ])
    assert result.exit_code == 0
    assert "summary" in result.stdout.lower()
