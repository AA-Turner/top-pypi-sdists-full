"""The probe-contracts copy inside the built wheel equals contracts/, file for file (hatch_build.py).

One source in the repo; the only copy is the one the build makes. Built both ways a release
can build it: straight from the checkout, and from the sdist (`python -m build`).
"""

from __future__ import annotations

import os
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
CONTRACTS = AGENT.parent / "contracts" / "probe_contracts"
VENDORED_AS = "probe/_vendor/probe_contracts/"


def _source_files() -> dict[str, bytes]:
    return {
        path.relative_to(CONTRACTS).as_posix(): path.read_bytes()
        for path in CONTRACTS.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def _build(project: Path, out: Path, *targets: str) -> None:
    flags = [flag for target in targets for flag in ("-t", target)]
    env = {"PATH": os.defpath, "HOME": str(out), "PYTHONDONTWRITEBYTECODE": "1"}
    built = subprocess.run([sys.executable, "-m", "hatchling", "build", *flags, "-d", str(out)],
                           cwd=project, capture_output=True, text=True, timeout=120, env=env)
    assert built.returncode == 0, built.stderr


def _vendored(wheel: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(wheel) as archive:
        return {name.removeprefix(VENDORED_AS): archive.read(name)
                for name in archive.namelist() if name.startswith(VENDORED_AS)}


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> dict[str, Path]:
    if not CONTRACTS.is_dir():
        pytest.skip("not a research-os checkout: contracts/ is absent")
    out = tmp_path_factory.mktemp("contracts-vendor")
    _build(AGENT, out / "checkout", "wheel", "sdist")
    sdist = next((out / "checkout").glob("*.tar.gz"))
    with tarfile.open(sdist) as archive:
        archive.extractall(out / "unpacked", filter="data")
    _build(next((out / "unpacked").iterdir()), out / "from-sdist", "wheel")
    return {"checkout": next((out / "checkout").glob("*.whl")),
            "from-sdist": next((out / "from-sdist").glob("*.whl"))}


@pytest.mark.parametrize("how", ["checkout", "from-sdist"])
def test_the_wheel_vendors_contracts_byte_for_byte(built, how):
    assert _vendored(built[how]) == _source_files()
