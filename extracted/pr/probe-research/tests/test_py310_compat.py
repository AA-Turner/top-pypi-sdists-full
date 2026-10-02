"""Clean install in ML environments (plan 2.11, D29).

* Python 3.10: the three 3.11-only names come from ``probe._compat``, never the
  standard library, and its ``StrEnum`` behaves exactly like 3.11's.
* The SDK never imports the CLI (``probe.cli``'s initializer loads typer and every
  command): logging, delivery, the run lock and diagnostics all work in an
  environment where the CLI's and MCP server's dependencies do not exist.
* The ``cli`` / ``mcp`` / ``all`` extras say the same thing core says (release N
  of two), and the console scripts turn a missing extra into a message.

These run on every interpreter; the 3.10 CI leg runs them on 3.10 too.
"""

from __future__ import annotations

import ast
import enum
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from probe import _compat
from tests.served_fake_app import child_env, serve

_SRC = Path(__file__).resolve().parents[1] / "src" / "probe"
_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"

#: Modules that are the CLI (or the daemon, which drives the CLI) and may import
#: it, and the console-script shim that exists to import it.
_CLI_SIDE = {"cli", "daemon", "_entry.py"}


def _imports(path: Path):
    """Every (module, name) an import statement in ``path`` names, relative
    imports resolved, including imports inside functions."""
    try:
        package = list(path.relative_to(_SRC.parent).parts[:-1])
    except ValueError:  # a test or a script: no package of its own
        package = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name, None, node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package[: len(package) - (node.level - 1)]
                module = ".".join(base + ([node.module] if node.module else []))
            else:
                module = node.module or ""
            for alias in node.names:
                yield module, alias.name, node.lineno


def _sources():
    return [p for p in sorted(_SRC.rglob("*.py")) if "__pycache__" not in p.parts]


def test_nothing_imports_a_311_only_name_from_the_standard_library():
    """The package, and the tests and scripts that run on the 3.10 leg."""
    agent = _SRC.parents[1]
    others = sorted((agent / "tests").glob("*.py")) + sorted((agent / "scripts").glob("*.py"))
    offenders = []
    for path in _sources() + others:
        if path.name == "_compat.py":
            continue
        for module, name, line in _imports(path):
            if (module, name) in {("enum", "StrEnum"), ("datetime", "UTC")} or module == "tomllib":
                offenders.append(f"{path.name}:{line} {module}.{name or ''}")
    assert offenders == [], "import these from probe._compat:\n" + "\n".join(offenders)


def test_the_sdk_never_imports_the_cli():
    """Round-3 finding: `run.py` took the run lock from `probe.cli.run_lock` and
    the outbox worker reported through `probe.cli.telemetry`; importing either
    loads the whole CLI, and without its dependencies both were lost silently
    behind the `except Exception` at every call site."""
    offenders = []
    for path in _sources():
        if path.relative_to(_SRC).parts[0] in _CLI_SIDE:
            continue
        for module, name, line in _imports(path):
            full = f"{module}.{name}" if name else module
            if module == "probe.cli" or module.startswith("probe.cli.") or full.startswith("probe.cli."):
                offenders.append(f"{path.relative_to(_SRC)}:{line} {full}")
    assert offenders == [], "use probe._shared instead:\n" + "\n".join(offenders)


def test_the_cli_names_of_the_moved_modules_are_the_same_objects():
    """A monkeypatch through either name must be seen by both."""
    from probe._shared import run_lock, telemetry
    from probe.cli import run_lock as cli_run_lock
    from probe.cli import telemetry as cli_telemetry

    assert cli_run_lock is run_lock and cli_telemetry is telemetry


def test_the_strenum_backport_behaves_like_311s():
    backport = _compat._strenum_backport()

    class Colour(backport):
        RED = "red"
        GREEN = enum.auto()

    assert Colour.RED == "red" and isinstance(Colour.RED, str)
    assert str(Colour.RED) == "red" and f"{Colour.RED}" == "red" and format(Colour.RED, ">4") == " red"
    assert Colour.GREEN.value == "green"
    assert json.dumps({"c": Colour.RED}) == '{"c": "red"}'
    assert Colour("red") is Colour.RED
    with pytest.raises(TypeError):

        class Bad(backport):
            ONE = 1

    if sys.version_info >= (3, 11):
        class Real(enum.StrEnum):
            RED = "red"
            GREEN = enum.auto()

        for ours, theirs in ((Colour.RED, Real.RED), (Colour.GREEN, Real.GREEN)):
            assert (str(ours), f"{ours}", ours.value) == (str(theirs), f"{theirs}", theirs.value)


def test_utc_and_tomllib_are_the_311_ones():
    from datetime import timedelta

    assert _compat.UTC.utcoffset(None) == timedelta(0)
    assert _compat.tomllib.loads('a = 1\n[b]\nc = "d"\n') == {"a": 1, "b": {"c": "d"}}


def _pyproject() -> dict:
    return _compat.tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))


def test_the_cli_and_mcp_extras_say_what_core_says():
    """Release N of the two-release split: core still carries these, and the
    extras must not drift from it (release N+1 deletes them from core)."""
    project = _pyproject()["project"]

    def by_name(specs):
        return {spec.split(";")[0].replace(" ", "").split("<")[0].split(">")[0].split("=")[0]
                .split("[")[0]: spec for spec in specs}

    core = by_name(project["dependencies"])
    extras = project["optional-dependencies"]
    for extra in ("cli", "mcp"):
        for name, spec in by_name(extras[extra]).items():
            assert name in core, (
                f"{name} left core. GATE -- plan 2.11 (D29), root TODOS.md \"Packaging (plan "
                "2.11, D29)\" and tests/test_release_sync.py::test_release_n1_waits_for_the_"
                "self_reinstall: release N+1 must not ship before `probe._entry` reinstalls "
                "itself with [all] and the pre-N -> N+1 upgrade test exists. Do NOT edit this "
                "assertion away; finish the gate, then change this test with it."
            )
            assert core.get(name) == spec, f"[{extra}] {spec!r} but core says {core.get(name)!r}"
    assert extras["all"] == ["probe-research[cli,mcp]"]
    assert project["requires-python"] == ">=3.10"
    assert "Programming Language :: Python :: 3.10" in project["classifiers"]


def test_the_console_scripts_go_through_the_guarded_entry_points():
    scripts = _pyproject()["project"]["scripts"]
    assert scripts == {
        "probe": "probe._entry:main",
        "probe-research-mcp": "probe._entry:mcp_main",
        "probe-research-mcp-http": "probe._entry:mcp_http_main",
    }


#: Runs first in a child: every listed module is absent, as in an environment
#: that installed the SDK alone. Attempts are recorded so a swallowed
#: ImportError cannot pass for "not needed".
_ABSENT = textwrap.dedent(
    """
    import importlib.abc, sys
    ABSENT = {absent!r}
    ATTEMPTS = []

    class Absent(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path=None, target=None):
            if name in ABSENT or name.split(".")[0] in ABSENT or any(
                name.startswith(a + ".") for a in ABSENT
            ):
                ATTEMPTS.append(name)
                raise ModuleNotFoundError(f"No module named {{name!r}}", name=name)
            return None

    sys.meta_path.insert(0, Absent())
    """
)

#: What the `cli` and `mcp` extras bring that a core install would not have.
#: (`anyio` stays: httpx, a core dependency, needs it. `click` comes with typer;
#: httpx probes it for its own optional CLI and copes without it.)
_EXTRAS_ONLY = ("typer", "questionary", "click", "mcp", "tiktoken")
_MUST_NOT_TRY = {"typer", "questionary", "mcp", "tiktoken", "probe.cli"}


def test_the_sdk_lifecycle_runs_without_the_cli_or_mcp_dependencies(app, tmp_path):
    """log, drain, the run lock, diagnostics and finish -- with typer,
    questionary, mcp, anyio, tiktoken and `probe.cli` itself absent."""
    app.seed_experiment("e1")
    code = _ABSENT.format(absent=_EXTRAS_ONLY + ("probe.cli",)) + textwrap.dedent(
        """
        import json, probe
        from probe.sdk import diagnostics

        run = probe.init(experiment="e1", name="core-only")
        locked = run._run_lock is not None or run._run_lock_leased
        probe.log({"loss": 0.5}, step=0)
        probe.log({"loss": 0.25}, step=1)
        diagnostics.capture_swallowed(
            RuntimeError("probe"), site="py310.test", base_url="http://127.0.0.1:9", spool_dir="."
        )
        probe.finish()
        # What the SDK reaches lazily (the worker's delivery report, the
        # no-run crash report): importable here, where the CLI is not.
        import probe._shared.run_lock, probe._shared.telemetry, probe.sdk.outbox_worker
        print(json.dumps({
            "run": run.id, "locked": locked, "attempts": ATTEMPTS,
            "cli_loaded": "probe.cli" in sys.modules,
        }))
        """
    )
    with serve(app) as url:
        # Not the launcher hand-off: another test in this worker can leave
        # PROBE_RUN_ID in os.environ (the Miles integration sets it for real),
        # and a child that inherits it attaches instead of creating a run.
        env = {k: v for k, v in child_env(url).items() if not k.startswith("PROBE_RUN_")}
        proc = subprocess.run(
            [sys.executable, "-c", code],
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=tmp_path,
        )
    assert proc.returncode == 0, proc.stderr[-3000:]
    result = json.loads(proc.stdout.strip().splitlines()[-1])
    tried = {name for name in result["attempts"] if name.split(".")[0] in _MUST_NOT_TRY
             or name == "probe.cli" or name.startswith("probe.cli.")}
    assert tried == set(), f"the SDK tried to import a CLI/MCP dependency: {sorted(tried)}"
    assert result["locked"], "no run lock: auto-update could land mid-run"
    assert not result["cli_loaded"]
    assert app.runs[result["run"]]["status"] == "completed"
    steps = sorted(p["step_index"] for p in app.metric_points_posted[result["run"]])
    assert steps == [0, 1]


@pytest.mark.parametrize(
    "script, extra",
    [("main", "cli"), ("mcp_main", "mcp")],
)
def test_a_missing_extra_is_a_message_not_a_traceback(script, extra):
    code = _ABSENT.format(absent=_EXTRAS_ONLY) + textwrap.dedent(
        f"""
        from probe import _entry
        result = _entry.{script}()
        raise SystemExit(result)
        """
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert proc.returncode == 1
    assert "Traceback" not in proc.stderr
    assert f"`{extra}` dependencies" in proc.stderr
    assert "pip install 'probe-research[all]'" in proc.stderr


def test_an_unrelated_missing_module_keeps_its_traceback(monkeypatch):
    """Only the extras' own modules are explained; anything else is a bug."""
    from probe import _entry

    error = ModuleNotFoundError("No module named 'nonsense'", name="nonsense")
    assert _entry._missing_dependency(error, _entry._CLI_MODULES) is None
    typer_missing = ModuleNotFoundError("No module named 'typer.main'", name="typer.main")
    assert _entry._missing_dependency(typer_missing, _entry._CLI_MODULES) == "typer"


def test_generated_models_import_strenum_from_compat():
    """scripts/gen_models.py still targets 3.11 (a 3.10 target writes
    `class X(str, Enum)`, whose str() is "X.member"), then points the one
    3.11-only import at probe._compat."""
    sys.path.insert(0, str(_PYPROJECT.parent / "scripts"))
    try:
        import gen_models
    finally:
        sys.path.pop(0)
    generated = "from __future__ import annotations\n\nfrom enum import StrEnum\nfrom typing import Any\n"
    assert gen_models.py310_imports(generated) == (
        "from __future__ import annotations\n\nfrom probe._compat import StrEnum\nfrom typing import Any\n"
    )
    with pytest.raises(SystemExit):
        gen_models.py310_imports("from enum import Enum\n")
