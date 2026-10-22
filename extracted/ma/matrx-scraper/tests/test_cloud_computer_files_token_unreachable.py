"""An agent on a Cloud Computer cannot reach the machine files token (review 3 D2).

The token (``cloud_files:write``) lets its holder delete the person's cloud files
directly, past the sync's delete cap and hold. Agents run as the worker's own uid,
as children of the worker. This test starts a real worker-shaped process that goes
through the real boundary (``cloud_computer_launch``), renews the session the real
way (``MachineFilesSession.renew``), starts a child with the agent daemon's real
environment (``AgentDaemon._env``), and that child then looks everywhere an agent
shell could: its own environment, every ``/proc/<pid>/environ`` and ``cmdline``,
the worker's memory through ``/proc/<pid>/mem``, the home and the token file.

On origin/main before this fix (the worker kept the token in its environment and
wrote the renewed one to ``~/.matrx/cloud-sync/session.json``) the child finds it
in ``/proc/<worker>/environ`` and in ``session.json``. Linux only (``/proc``).

The modules are loaded by file path (all three are stdlib-only), so the same proof
also runs in a bare container replay: ``python -m pytest`` on this file, or
``python tests/test_cloud_computer_files_token_unreachable.py <worker-dir>``.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

WORKER_DIR = Path(__file__).resolve().parents[1] / "matrx_scraper/cloud_browser/worker"
LAUNCH_TOKEN = "eyJhbGciOiJFUzI1NiJ9.launch-token-" + "L" * 40 + ".sig"
RENEWED_TOKEN = "eyJhbGciOiJFUzI1NiJ9.renewed-token-" + "R" * 40 + ".sig"
OLD_IMAGE_TOKEN = "eyJhbGciOiJFUzI1NiJ9.old-image-token-" + "O" * 40 + ".sig"

WORKER = r'''
import asyncio, importlib.util, json, os, pathlib, subprocess, sys
src, home, token_file, probe = sys.argv[1:5]
renewed = sys.stdin.readline().strip()  # never in argv or the environment: the probe reads both

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(src, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

launch_mod, agent, files = load("cloud_computer_launch"), load("machine_agent"), load("cloud_files_sync")
if hasattr(launch_mod, "launch_from_environment"):
    launch = launch_mod.launch_from_environment(os.environ, token_file=pathlib.Path(token_file))
else:  # the server.py lines before the fix
    launch = launch_mod.CloudComputerLaunch(
        files_token=os.environ.get("MATRX_CLOUD_FILES_TOKEN", ""),
        files_url=os.environ.get("MATRX_CLOUD_FILES_URL", ""),
        process_env=dict(os.environ),
    )

class Bridge:
    def __init__(self, token):
        self.token = token
    async def session(self):
        return {"token": renewed, "expires_at": 4102444800, "knobs": {}}

session = files.MachineFilesSession(bridge=Bridge(launch.files_token),
                                    state_dir=pathlib.Path(home) / ".matrx/cloud-sync")
asyncio.run(session.renew(force=True))
held = [launch.files_token, session.bridge.token]  # both stay in this process's memory
env = agent.AgentDaemon(home, launch_env=launch.process_env)._env()
out = subprocess.run([sys.executable, "-c", probe, str(os.getpid()), home, token_file],
                     env=env, capture_output=True, text=True, check=True).stdout
print(json.dumps({"worker_has_token": bool(held[0]), "found": json.loads(out)}))
'''

PROBE = r'''
import json, os, sys
worker, home, token_file = sys.argv[1:4]
tokens = [(k + "-token-").encode() for k in ("launch", "renewed", "old-image")]
found = set()
def look(where, data):
    for t in tokens:
        if t in data:
            found.add(where + " <- " + t.decode().rstrip("-"))
look("own environment", "\0".join(f"{k}={v}" for k, v in os.environ.items()).encode())
for pid in [p for p in os.listdir("/proc") if p.isdigit() and p != str(os.getpid())]:
    for name in ("environ", "cmdline"):
        try:
            with open(f"/proc/{pid}/{name}", "rb") as fh:
                look(("worker" if pid == worker else "process") + " " + name, fh.read())
        except OSError:
            pass
try:
    with open(f"/proc/{worker}/maps") as maps, open(f"/proc/{worker}/mem", "rb") as mem:
        for line in maps:
            span, perms = line.split()[:2]
            if not perms.startswith("r"):
                continue
            lo, hi = (int(x, 16) for x in span.split("-"))
            try:
                mem.seek(lo)
                look("worker memory", mem.read(hi - lo))
            except (OSError, ValueError, OverflowError):
                pass
except OSError:
    pass
for root in (home, os.path.dirname(token_file)):
    for dirpath, _, names in os.walk(root):
        for n in names:
            try:
                with open(os.path.join(dirpath, n), "rb") as fh:
                    look("file " + os.path.relpath(os.path.join(dirpath, n), root), fh.read())
            except OSError:
                pass
print(json.dumps(sorted(found)))
'''


def probe(worker_dir: Path, scratch: Path) -> dict:
    """Run the worker-shaped process the way the image does; the child reports what it found."""
    home = scratch / "home"
    (home / ".matrx/cloud-sync").mkdir(parents=True)
    # What an older image left in the person's home (EFS keeps it across tasks).
    (home / ".matrx/cloud-sync/session.json").write_text(
        json.dumps({"token": OLD_IMAGE_TOKEN, "expires_at": 1}))
    secret = scratch / "run-cloud-computer-files"
    secret.mkdir(mode=0o700)
    token_file = secret / "token"
    env = {k: v for k, v in os.environ.items() if "TOKEN" not in k}
    if os.environ.get("CLOUD_COMPUTER_REPLAY") == "1":
        # A container replay: the real entrypoint already moved the token to its file.
        token_file = Path("/run/cloud-computer-files/token")
    else:
        # What the image's root entrypoint does before anything starts (on an image
        # without that step, the token is still in the environment: both are tried).
        token_file.write_text(LAUNCH_TOKEN)
        env["MATRX_CLOUD_FILES_TOKEN"] = LAUNCH_TOKEN
    env["MATRX_CLOUD_FILES_URL"] = "https://bridge.invalid"
    out = subprocess.run(
        [sys.executable, "-c", WORKER, str(worker_dir), str(home), str(token_file), PROBE],
        input=RENEWED_TOKEN + "\n", env=env, capture_output=True, text=True, timeout=120,
    )
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


@pytest.mark.skipif(not Path("/proc/self/environ").exists(), reason="needs Linux /proc")
def test_an_agent_child_of_the_worker_cannot_read_the_files_token(tmp_path: Path) -> None:
    result = probe(WORKER_DIR, tmp_path)
    assert result["worker_has_token"], "the worker itself must still hold the token"
    assert result["found"] == [], f"an agent process can read the files token: {result['found']}"


if __name__ == "__main__":
    import tempfile

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else WORKER_DIR
    with tempfile.TemporaryDirectory() as tmp:
        print(json.dumps(probe(target, Path(tmp))))
