"""Build and install both distributions, then count with no cache/network/source tree."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import sysconfig
import venv
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]


def _environment(home):
    # Never forward developer credentials into package builders or tracebacks.
    return {"PATH": os.defpath, "HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}


@pytest.fixture(scope="module")
def distributions(tmp_path_factory):
    root = tmp_path_factory.mktemp("mcp-budget-dist")
    project = root / "project"
    project.mkdir()
    for name in ("pyproject.toml", "README.md"):
        shutil.copy2(_ROOT / name, project / name)
    for name in ("src", "skills"):
        shutil.copytree(_ROOT / name, project / name, ignore=shutil.ignore_patterns("__pycache__"))
    built = subprocess.run(
        [sys.executable, "-m", "hatchling", "build", "-t", "wheel", "-t", "sdist"],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=60,
        env=_environment(root),
    )
    assert built.returncode == 0, built.stderr
    return {
        "wheel": next((project / "dist").glob("*.whl")),
        "sdist": next((project / "dist").glob("*.tar.gz")),
    }


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
def test_installed_distribution_counts_offline_without_a_source_checkout(
    distributions, tmp_path, kind
):
    # ensurepip uses Python's bundled wheel; no package index or external installer.
    environment = tmp_path / "venv"
    # Symlinks also support relocatable python-build-standalone interpreters.
    venv.EnvBuilder(with_pip=False, symlinks=os.name != "nt").create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    seeded = subprocess.run(
        [str(python), "-m", "ensurepip", "--upgrade"],
        cwd=tmp_path,
        env=_environment(tmp_path),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert seeded.returncode == 0, seeded.stderr
    dependencies = list(
        dict.fromkeys([sysconfig.get_path("purelib"), sysconfig.get_path("platlib")])
    )
    install = subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "--disable-pip-version-check",
            "install",
            "--no-index",
            "--no-deps",
            "--no-build-isolation",
            str(distributions[kind]),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        # Expose only installed build dependencies while building the sdist.
        env={**_environment(tmp_path), "PYTHONPATH": os.pathsep.join(dependencies)},
    )
    assert install.returncode == 0, install.stderr
    home = tmp_path / "home"
    home.mkdir()
    cache = home / "never-created-cache"
    code = """
import hashlib, json, os, socket, sys
from pathlib import Path
def no_network(event, args):
    if event == 'socket.__new__' and args[1] == socket.AF_UNIX:
        return  # asyncio's local wakeup socket, not an external network read
    if event.startswith('socket.'):
        raise AssertionError('network attempted: ' + event)
sys.addaudithook(no_network)
# Installed wheel takes precedence. Dependency paths come AFTER its site-packages;
# PYTHONPATH/source checkout must never mask a missing wheel resource.
sys.path.extend(json.loads(sys.argv[1]))
import probe
from probe.mcp import budget
assert Path(probe.__file__).is_relative_to(Path(sys.prefix)), probe.__file__
assert budget._encoding is None
assert 'tiktoken' not in sys.modules
assets = Path(budget.__file__).parent / '_tokenizer'
assert hashlib.sha256((assets / 'o200k_base.tiktoken').read_bytes()).hexdigest() == budget.VOCABULARY_SHA256
assert hashlib.sha256((assets / 'o200k_base.json').read_bytes()).hexdigest() == budget.CONFIG_SHA256
assert 'MIT License' in (assets / 'LICENSE').read_text()
assert budget.count_tokens('こんにちは世界 🌍') == 4
assert budget.count_tokens('<|endoftext|><|endofprompt|>') == 13
assert budget.Budget().fits({'text': 'hello world'})
assert not Path(os.environ['TIKTOKEN_CACHE_DIR']).exists()

# Exercise every public tool against fixtures through the installed runtime.
# Only the tests directory is added, never agent/src or the editable .pth file.
sys.path.append(sys.argv[2])
from tests.test_mcp_delivery import _Service, _wire, _bounded, _TOOL_ARGUMENTS
from tests.test_mcp_browse_delivery import Tree, node
class PackageService(_Service):
    def browse_research(self, **kwargs):
        return Tree([node('project', 'packaged-fixture')])(kwargs)
for name, arguments in {**_TOOL_ARGUMENTS, 'browse': {}}.items():
    page = _bounded(_wire(PackageService(), name, {**arguments, 'token_budget': 512}))
    assert page, name
assert Path(probe.__file__).is_relative_to(Path(sys.prefix)), probe.__file__
"""
    env = {**_environment(home), "TIKTOKEN_CACHE_DIR": str(cache), "DATA_GYM_CACHE_DIR": str(cache)}
    checked = subprocess.run(
        [str(python), "-c", code, json.dumps(dependencies), str(_ROOT)],
        cwd=home,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert checked.returncode == 0, checked.stderr
