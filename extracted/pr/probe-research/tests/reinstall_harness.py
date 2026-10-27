"""A private, offline uv tool setup for the reinstall tests (plan clean-uninstall-reinstall V-T1).

Real `uv`, against hand-built wheels of a stand-in `probe-research`: its
`probe` command, and the modules every check imports (`probe.core.run`,
`probe.core.adopt`, `probe.service` with `--selftest`, `probe.cli.main`), so
the install pipeline's health checks run for real. Fakes of uv missed its
behaviour before (a plain `uv tool install` through the side-by-side link,
2026-10-26), so the layout cases here use uv itself. Everything lives under the
test's tmp folder: HOME, the uv tool and bin folders, the cache, every agent's
config folder. Nothing touches the machine's own uv tools or Probe state.
"""

from __future__ import annotations

import base64
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

VERSIONS = ("1.0.0", "1.0.1", "1.0.2")


def wheel(directory: Path, name: str, version: str, *, files: dict, extras=(), scripts: dict | None = None) -> None:
    dist = name.replace("-", "_")
    info = f"{dist}-{version}.dist-info"
    meta = ["Metadata-Version: 2.1", f"Name: {name}", f"Version: {version}"]
    meta += [f"Provides-Extra: {extra}" for extra in extras]
    payload = {path: data.encode() if isinstance(data, str) else data for path, data in files.items()}
    payload[f"{info}/METADATA"] = ("\n".join(meta) + "\n").encode()
    payload[f"{info}/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    if scripts:
        lines = "".join(f"{script} = {target}\n" for script, target in scripts.items())
        payload[f"{info}/entry_points.txt"] = f"[console_scripts]\n{lines}".encode()
    record = []
    for path, data in payload.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
        record.append(f"{path},sha256={digest},{len(data)}")
    record.append(f"{info}/RECORD,,")
    payload[f"{info}/RECORD"] = ("\n".join(record) + "\n").encode()
    with zipfile.ZipFile(directory / f"{dist}-{version}-py3-none-any.whl", "w") as whl:
        for path, data in payload.items():
            whl.writestr(path, data)


def probe_files(version: str) -> dict:
    return {
        "probe/__init__.py": f"__version__ = {version!r}\n",
        "probe/core/__init__.py": "",
        "probe/core/run.py": "",
        "probe/core/adopt.py": "",
        "probe/service/__init__.py": "",
        "probe/service/__main__.py": "import sys\nif '--selftest' in sys.argv:\n    print('[]')\n",
        "probe/cli/__init__.py": "",
        "probe/cli/main.py": f"def main():\n    print('probe {version}')\n",
    }


#: A release from before `probe.core.adopt` (0.328.0): the health check, which
#: imports it, can never pass for it.
OLD_VERSION = "0.320.0"


def build_wheels(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for version in VERSIONS:
        wheel(directory, "probe-research", version, files=probe_files(version),
              extras=("all", "daemon", "mcp-http", "cli"), scripts={"probe": "probe.cli.main:main"})
    old = {path: data for path, data in probe_files(OLD_VERSION).items() if path != "probe/core/adopt.py"}
    wheel(directory, "probe-research", OLD_VERSION, files=old, extras=("all", "daemon", "mcp-http", "cli"),
          scripts={"probe": "probe.cli.main:main"})
    return directory


class Machine:
    """One test's machine: its uv tool folder, scripts folder and versions folder."""

    def __init__(self, root: Path, wheels: Path, cache: Path) -> None:
        self.root = root
        self.tools = root / "share" / "uv" / "tools"
        self.bins = root / "bin"
        self.versions = root / "share" / "uv" / "probe-versions"
        self.env = {
            **os.environ,
            "UV_TOOL_DIR": str(self.tools),
            "UV_TOOL_BIN_DIR": str(self.bins),
            "UV_FIND_LINKS": str(wheels),
            "UV_NO_INDEX": "1",
            "UV_PYTHON": sys.executable,
            "UV_CACHE_DIR": str(cache),
        }

    @property
    def tool(self) -> Path:
        return self.tools / "probe-research"

    def uv(self, *args: str, check: bool = True, **env: str) -> subprocess.CompletedProcess:
        done = subprocess.run(["uv", *args], env={**self.env, **env}, capture_output=True, text=True, timeout=180)
        if check:
            assert done.returncode == 0, done.stderr[-2000:]
        return done

    def probe(self) -> str:
        """What `probe` on this machine's PATH answers."""
        done = subprocess.run([str(self.bins / "probe")], capture_output=True, text=True, timeout=60)
        assert done.returncode == 0, done.stderr[-2000:]
        return done.stdout.strip()


@pytest.fixture(scope="session")
def reinstall_wheels(tmp_path_factory) -> tuple[Path, Path]:
    if shutil.which("uv") is None:
        pytest.skip("needs uv on PATH")
    root = tmp_path_factory.mktemp("reinstall-wheels")
    return build_wheels(root / "wheels"), root / "cache"


@pytest.fixture
def uv_machine(reinstall_wheels, tmp_path, monkeypatch) -> Machine:
    """HOME, every agent's folder and uv's tool folders under tmp_path; the
    process environment pointed at them (the install pipeline runs uv itself)."""
    if sys.platform == "win32":
        pytest.skip("the side-by-side layout is POSIX only")
    wheels, cache = reinstall_wheels
    box = Machine(tmp_path / "m", wheels, cache)
    home = tmp_path / "home"
    home.mkdir()
    for name, value in {
        "HOME": home,
        "XDG_CONFIG_HOME": home / ".config",
        "XDG_DATA_HOME": tmp_path / "m" / "share",
        "XDG_STATE_HOME": home / ".local" / "state",
        "XDG_CACHE_HOME": home / ".cache",
        "CLAUDE_CONFIG_DIR": home / ".claude",
        "CODEX_HOME": home / ".codex",
        "PI_CODING_AGENT_DIR": home / ".pi" / "agent",
        "KIMI_CODE_HOME": home / ".kimi",
    }.items():
        monkeypatch.setenv(name, str(value))
    for name in ("UV_TOOL_DIR", "UV_TOOL_BIN_DIR", "UV_FIND_LINKS", "UV_NO_INDEX", "UV_PYTHON", "UV_CACHE_DIR"):
        monkeypatch.setenv(name, box.env[name])
    monkeypatch.delenv("UV_OFFLINE", raising=False)
    # The stand-in has no daemon libraries: `_dist` must not ask for what the
    # test process happens to have.
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    return box
