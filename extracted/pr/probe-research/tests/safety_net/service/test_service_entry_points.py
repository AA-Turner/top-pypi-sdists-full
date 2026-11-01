"""The service's start path, the frozen hand-off imports, and every hook script the plugins' manifests run.

Hooks are never executed here (they have side effects): each referenced script must exist, be
executable where the manifest execs or gates on `-x` it, and compile (`compile()`, `bash -n`).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[3]
#: The marketplaces each harness installs the plugins from (served from main: pinned paths).
MARKETPLACES = (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json", "kimi-marketplace.json")
_REFERENCED = re.compile(r"\$ROOT/([\w./-]+\.(?:py|sh))")
#: `exec "$ROOT/x"` or `[ -x "$ROOT/x" ]`: a file that is not executable makes the hook a silent no-op.
_MUST_EXEC = re.compile(r"(?:\bexec\s+|\[\s+-x\s+)\"\$ROOT/([\w./-]+)\"")
_SKIP_DIRS = {"tests", "node_modules", "fixtures"}


def _plugin_roots() -> list[Path]:
    roots = set()
    for name in MARKETPLACES:
        for plugin in json.loads((AGENT / name).read_text(encoding="utf-8"))["plugins"]:
            source = plugin["source"]
            roots.add((AGENT / (source if isinstance(source, str) else source["path"])).resolve())
    return sorted(roots)


def _commands(root: Path) -> list[str]:
    """Every `command` string in any JSON manifest of the plugin (hooks.json, routes, plugin.json)."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "command" and isinstance(value, str):
                    found.append(value)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in sorted(root.rglob("*.json")):
        if not _SKIP_DIRS & set(path.relative_to(root).parts):
            walk(json.loads(path.read_text(encoding="utf-8")))
    return found


def _hook_scripts() -> dict[Path, bool]:
    """Referenced script -> must it be executable."""
    scripts: dict[Path, bool] = {}
    for root in _plugin_roots():
        for command in _commands(root):
            for rel in _REFERENCED.findall(command):
                scripts[root / rel] = scripts.get(root / rel, False) or rel in _MUST_EXEC.findall(command)
    return scripts


def _compiles(path: Path) -> str | None:
    """What is wrong with the script's syntax, or None."""
    if path.suffix == ".py":
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            return f"{exc.msg} (line {exc.lineno})"
        return None
    done = subprocess.run(["/bin/bash", "-n", str(path)], capture_output=True, text=True, timeout=30)
    return (done.stderr.strip() or f"bash -n exited {done.returncode}") if done.returncode else None


def test_every_plugin_hook_script_exists_runs_and_compiles():
    scripts = _hook_scripts()
    assert len({p.parent for p in scripts}) >= 3, "found too few hook folders: the manifest walk is broken"
    missing = sorted(str(p.relative_to(AGENT)) for p in scripts if not p.is_file())
    assert not missing, f"hook manifests run scripts that are not there: {missing}"
    not_exec = sorted(str(p.relative_to(AGENT)) for p, must in scripts.items() if must and not p.stat().st_mode & 0o111)
    assert not not_exec, f"hooks exec (or gate on -x) these, but they are not executable: {not_exec}"
    # The scripts' own folders hold what they source and import: all of it must compile.
    folders = {p.parent for p in scripts}
    broken = {str(p.relative_to(AGENT)): why for folder in folders for p in sorted(folder.iterdir())
              if p.suffix in (".py", ".sh") and (why := _compiles(p))}
    assert not broken, f"hook scripts that do not compile: {broken}"


def test_every_path_a_plugin_manifest_names_exists():
    """`plugin.json`'s `"hooks": "./hooks/claude-reads.json"`, `"skills": "./agent-skills/"` and kin."""
    missing = []
    for root in _plugin_roots():
        for manifest in sorted(root.glob(".*-plugin/plugin.json")):
            for key, value in json.loads(manifest.read_text(encoding="utf-8")).items():
                if isinstance(value, str) and value.startswith("./") and not (root / value).exists():
                    missing.append(f"{manifest.relative_to(AGENT)}: {key} = {value}")
    assert not missing, f"plugin manifests name paths that are not there: {missing}"


def _run(argv: list[str], env: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *argv], env=env, cwd=env["HOME"], capture_output=True, text=True,
                          timeout=120, stdin=subprocess.DEVNULL)


def test_service_selftest_loads_its_start_path_and_starts_nothing(child_env):
    """`python -I -m probe.service --selftest`: imports the start path, prints it, exits; no socket, no process."""
    done = _run(["-I", "-m", "probe.service", "--selftest"], child_env)
    assert done.returncode == 0, done.stderr[-3000:]
    modules = json.loads(done.stdout)
    assert isinstance(modules, list) and all(isinstance(m, str) for m in modules)
    assert any(m.startswith("probe.") for m in modules), "the selftest loaded nothing of Probe's"
    assert not list(Path(child_env["HOME"]).rglob("*.sock")), "the selftest opened a service socket"


@pytest.mark.parametrize("program", [
    # `handoff.starts`: what an older release runs in a new env before exec'ing its update (frozen).
    "import probe.core.run, probe.core.adopt",
    "import probe",
])
def test_frozen_handoff_imports_load_under_isolation(program, child_env):
    done = _run(["-I", "-c", program], child_env)
    assert done.returncode == 0, f"`python -I -c {program!r}`: {done.stderr[-3000:]}"
