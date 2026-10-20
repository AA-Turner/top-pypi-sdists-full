"""Installed software survives a new task (owner ruling 16), in a real container.

Two containers share one home directory, like two Fargate tasks sharing the
person's EFS home: the first installs a package with apt and a tool into
/usr/local; the second starts from a FRESH root (the image again) and must have
both back after ``cloud-computer-software replay``. The control run proves the
break: a fresh root without the replay has neither.

Needs Docker and the network (apt); skipped otherwise.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "docker/cloud-computer/cloud-computer-software.sh"
IMAGE = "ubuntu:24.04"

#: The image build's part (Dockerfile): user, script, hook, then the baselines LAST.
IMAGE_SETUP = r"""
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null && apt-get install -y -qq --no-install-recommends rsync >/dev/null
id browser-worker >/dev/null 2>&1 || useradd -M -d /home/browser-worker browser-worker
install -m 0755 /src/cloud-computer-software.sh /usr/local/bin/cloud-computer-software
mkdir -p /usr/local/share/cloud-computer /run/cloud-computer
printf '%s\n' 'DPkg::Post-Invoke { "/usr/local/bin/cloud-computer-software record >/dev/null 2>&1 || true"; };' \
  > /etc/apt/apt.conf.d/90-cloud-computer-record
apt-mark showmanual | sort -u > /usr/local/share/cloud-computer/image-packages.txt
find /etc/apt /usr/share/keyrings /usr/local /opt -xdev \( -type f -o -type l \) 2>/dev/null | sort -u \
  > /usr/local/share/cloud-computer/image-files.txt
"""


def _docker(home: Path, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "run", "--rm", "-v", f"{home}:/home/browser-worker", "-v", f"{SCRIPT.parent}:/src:ro",
         IMAGE, "bash", "-c", IMAGE_SETUP + script],
        capture_output=True, text=True, timeout=900,
    )


@pytest.fixture
def home(tmp_path: Path) -> Path:
    if shutil.which("docker") is None or subprocess.run(["docker", "info"], capture_output=True).returncode:
        pytest.skip("docker not available")
    h = tmp_path / "home"
    h.mkdir()
    return h


def test_apt_and_usr_local_installs_come_back_on_a_fresh_root(home: Path) -> None:
    first = _docker(home, r"""
apt-get install -y -qq --no-install-recommends jq >/dev/null   # the apt hook records it
printf '#!/bin/sh\necho mine\n' > /usr/local/bin/mytool && chmod +x /usr/local/bin/mytool
/usr/local/bin/cloud-computer-software record                  # save-before-stop records the rest
""")
    assert first.returncode == 0, first.stderr[-2000:]
    assert (home / ".matrx/system/apt-packages.txt").read_text().split() == ["jq"]
    assert "/usr/local/bin/mytool" in (home / ".matrx/system/files.txt").read_text()

    # The break: a new task's root without the replay has lost both.
    control = _docker(home, "command -v jq || echo NO_JQ; test -e /usr/local/bin/mytool || echo NO_TOOL")
    assert "NO_JQ" in control.stdout and "NO_TOOL" in control.stdout

    second = _docker(home, r"""
/usr/local/bin/cloud-computer-software replay
cat /run/cloud-computer/software.json
jq --version
mytool
stat -c '%a %U' /usr/local/bin/mytool
""")
    assert second.returncode == 0, second.stderr[-2000:]
    assert '"state":"done"' in second.stdout
    assert "jq-" in second.stdout and "mine" in second.stdout
    assert "755 root" in second.stdout  # owner and mode come back, not the home's
    # Still recorded for the next task, and nothing the image ships was recorded.
    assert (home / ".matrx/system/apt-packages.txt").read_text().split() == ["jq"]
