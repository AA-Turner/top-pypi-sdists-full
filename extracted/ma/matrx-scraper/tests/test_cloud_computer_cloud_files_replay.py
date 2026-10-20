"""The Cloud folder and the agent daemon in real containers sharing one home (P2).

Like two Fargate tasks sharing the person's EFS home: container 1 mirrors the
person's cloud (a file-backed stand-in for the bridge, shared at /cloud), makes
a stub for the big file and uploads a machine edit; container 2 starts from a
FRESH root on the same home, must re-download nothing, opens the stub, and runs
the REAL sandbox daemon (matrx_agent, the exact commit and archive hash the
image pins) as ``browser-worker`` with the home as its workspace: a shell
command and an fs read through the daemon see the Cloud folder.

Needs Docker and the network (pip); skipped otherwise.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

WORKER = Path(__file__).resolve().parents[1] / "matrx_scraper/cloud_browser/worker"
DOCKERFILE = Path(__file__).resolve().parents[1] / "docker/cloud-computer/Dockerfile"
IMAGE = "python:3.12-slim"

FAKE_BRIDGE = r'''
import hashlib, json, os, pathlib
from cloud_files_sync import BridgeError
CLOUD = pathlib.Path("/cloud")
class FileBridge:
    def _db(self):
        p = CLOUD / "db.json"
        return json.loads(p.read_text()) if p.exists() else {"files": {}, "clock": 0}
    def _save(self, db): (CLOUD / "db.json").write_text(json.dumps(db))
    def write(self, path, data, updated=None):
        db = self._db(); db["clock"] += 1
        (CLOUD / "blobs").mkdir(exist_ok=True)
        sha = hashlib.sha256(data).hexdigest(); (CLOUD / "blobs" / sha).write_bytes(data)
        db["files"][path] = {"file_path": path, "size_bytes": len(data), "checksum": sha,
            "updated_at": updated or f"2026-10-17T00:00:{db['clock']:02d}+00:00"}
        self._save(db)
    async def changes(self, since, limit):
        rows = sorted((r for r in self._db()["files"].values() if r["updated_at"] > since),
                      key=lambda r: r["updated_at"])
        return {"files": rows, "next_cursor": rows[-1]["updated_at"] if rows else since}
    async def get(self, path):
        with open(CLOUD / "gets.log", "a") as f: f.write(path + "\n")
        return (CLOUD / "blobs" / self._db()["files"][path]["checksum"]).read_bytes()
    async def put(self, path, content, expected):
        cur = self._db()["files"].get(path)
        if expected and cur and cur["checksum"] != expected: raise BridgeError(412)
        self.write(path, content); return {}
    async def delete(self, path):
        db = self._db(); db["files"].pop(path, None); self._save(db)
    async def session(self): return {}
'''

SETUP = r"""
set -e
id browser-worker >/dev/null 2>&1 || useradd -M -d /home/browser-worker browser-worker
chown browser-worker /home/browser-worker /cloud
cp /src/cloud_files_sync.py /src/machine_agent.py /work/ 2>/dev/null || { mkdir -p /work; cp /src/cloud_files_sync.py /src/machine_agent.py /work/; }
cat > /work/fake_bridge.py <<'PY'
""" + FAKE_BRIDGE + r"""
PY
chmod -R a+rX /work
"""


def _docker(home: Path, cloud: Path, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "run", "--rm", "-v", f"{home}:/home/browser-worker", "-v", f"{cloud}:/cloud",
         "-v", f"{WORKER}:/src:ro", IMAGE, "bash", "-c", SETUP + script],
        capture_output=True, text=True, timeout=900,
    )


def _py(code: str) -> str:
    return (
        "cd /work && runuser -u browser-worker -- env HOME=/home/browser-worker "
        f"python3 - <<'PY'\nimport asyncio, pathlib\nfrom cloud_files_sync import CloudFilesSync, SyncKnobs\n"
        "from fake_bridge import FileBridge\nb = FileBridge()\n"
        "def mk(): return CloudFilesSync(pathlib.Path('/home/browser-worker/Cloud'), b, "
        "state_dir=pathlib.Path('/home/browser-worker/.matrx/cloud-sync'), "
        "knobs=SyncKnobs(mirror_max_file_bytes=1000, mirror_recent_days=100000))\n"
        f"{code}\nPY\n"
    )


@pytest.fixture
def dirs(tmp_path: Path) -> tuple[Path, Path]:
    if shutil.which("docker") is None or subprocess.run(["docker", "info"], capture_output=True).returncode:
        pytest.skip("docker not available")
    home, cloud = tmp_path / "home", tmp_path / "cloud"
    home.mkdir(); cloud.mkdir()
    return home, cloud


def _pinned_sdk() -> tuple[str, str]:
    text = DOCKERFILE.read_text()
    commit = re.search(r"ARG MATRX_SDK_COMMIT=(\w+)", text).group(1)  # type: ignore[union-attr]
    sha = re.search(r"ARG MATRX_SDK_SHA256=(\w+)", text).group(1)  # type: ignore[union-attr]
    return commit, sha


def test_the_cloud_folder_and_agent_daemon_survive_a_fresh_root(dirs: tuple[Path, Path]) -> None:
    home, cloud = dirs
    first = _docker(home, cloud, _py(r"""
b.write("notes/todo.txt", b"buy milk")
b.write("video/big.bin", b"x" * 5000)
s = mk(); asyncio.run(s.pull_once()); asyncio.run(s.fill_copies(limit=1000))
pathlib.Path("/home/browser-worker/Cloud/notes/todo.txt").write_text("buy milk and eggs")
pathlib.Path("/home/browser-worker/Cloud/from-machine.txt").write_text("made on the machine")
asyncio.run(s.push_once())
print("STATUS", s.status()["files"], s.status()["stubs"])
"""))
    assert first.returncode == 0, first.stderr[-3000:]
    assert "STATUS 3 1" in first.stdout
    db = json.loads((cloud / "db.json").read_text())["files"]
    assert set(db) == {"notes/todo.txt", "video/big.bin", "from-machine.txt"}
    assert (home / "Cloud/video/big.bin").read_text().startswith("MATRX CLOUD FILE")
    gets_after_first = (cloud / "gets.log").read_text().split()
    assert gets_after_first == ["notes/todo.txt"]

    commit, sha = _pinned_sdk()
    script2 = _py(r"""
s = mk()
assert s.initial_done and s.is_stub("video/big.bin"), s.status()
asyncio.run(s.pull_once()); asyncio.run(s.push_once())
print("REPLAYED", open("/cloud/gets.log").read().split())
""") + f"""
set -e
apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null
curl -fsSL -o /tmp/sdk.tgz https://codeload.github.com/armanisadeghi/matrx-sandbox/tar.gz/{commit}
echo "{sha}  /tmp/sdk.tgz" | sha256sum -c - >/dev/null
tar xzf /tmp/sdk.tgz -C /tmp
python3 -m venv /opt/matrx-agent
pip install -q httpx
/opt/matrx-agent/bin/pip install -q /tmp/matrx-sandbox-{commit}/sandbox-image/sdk
cd /work && runuser -u browser-worker -- env HOME=/home/browser-worker python3 - <<'PY'
import asyncio, json, os, pathlib, urllib.request
from cloud_files_sync import CloudFilesSync, SyncKnobs
from fake_bridge import FileBridge
from machine_agent import AgentDaemon, hydrate_for_request, run_exec
s = CloudFilesSync(pathlib.Path('/home/browser-worker/Cloud'), FileBridge(),
    state_dir=pathlib.Path('/home/browser-worker/.matrx/cloud-sync'),
    knobs=SyncKnobs(mirror_max_file_bytes=1000, mirror_recent_days=100000))
async def main():
    d = AgentDaemon('/home/browser-worker', launch_env=dict(os.environ))
    t = asyncio.create_task(d.run_forever())
    def call(method, path, body=None):
        req = urllib.request.Request(d.base_url + path, method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={{'x-matrx-agent-token': d.token, 'content-type': 'application/json'}})
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    for _ in range(100):
        try:
            call('GET', '/health'); break
        except Exception:
            await asyncio.sleep(0.3)
    body = {{'command': 'wc -c Cloud/video/big.bin && cat Cloud/notes/todo.txt && whoami && echo agent-wrote > Cloud/agent.txt', 'cwd': '/home/browser-worker'}}
    await hydrate_for_request('POST', 'exec', {{}}, body, s)
    out = await run_exec(d, body, timeout=60)
    print('EXEC', json.dumps(out))
    req = urllib.request.Request(d.base_url + '/fs/read?path=/home/browser-worker/Cloud/agent.txt',
        headers={{'x-matrx-agent-token': d.token}})
    print('READ', urllib.request.urlopen(req, timeout=30).read().decode()[:200])
    try:
        urllib.request.urlopen(d.base_url + '/fs/read?path=/etc/hostname', timeout=10)
        print('NOTOKEN open')
    except Exception as e:
        print('NOTOKEN refused', e)
    await s.push_once()
    t.cancel()
asyncio.run(main())
PY
"""
    second = _docker(home, cloud, script2)
    assert second.returncode == 0, (second.stdout[-2000:], second.stderr[-3000:])
    assert "REPLAYED ['notes/todo.txt']" in second.stdout  # nothing re-downloaded on a fresh root
    exec_line = next(line for line in second.stdout.splitlines() if line.startswith("EXEC "))
    out = json.loads(exec_line[5:])
    assert out["exit_code"] == 0, out
    assert "5000 Cloud/video/big.bin" in out["stdout"]  # the stub was fetched before the command ran
    assert "buy milk and eggs" in out["stdout"] and "browser-worker" in out["stdout"]
    assert "agent-wrote" in next(line for line in second.stdout.splitlines() if line.startswith("READ"))
    assert "NOTOKEN refused" in second.stdout
    db = json.loads((cloud / "db.json").read_text())["files"]
    assert "agent.txt" in db  # what the agent wrote on the machine reached the cloud


def test_a_held_rm_rf_survives_a_new_task_and_is_resolved_there(dirs: tuple[Path, Path]) -> None:
    """Review 2 N2/N4 replay on real files: ``rm -rf ~/Cloud/rev2`` (30 files) is
    held, a symlink out of the folder is added, the task is replaced; the new task
    still holds, keeps uploading past the symlink, and the person's RESTORE puts
    all 30 back with nothing deleted in the cloud."""
    home, cloud = dirs
    first = _docker(home, cloud, _py(r"""
import os, shutil
for i in range(30): b.write(f"rev2/{i}.txt", f"rev2 {i}".encode())
b.write("keep.txt", b"keep")
s = mk(); asyncio.run(s.pull_once()); asyncio.run(s.fill_copies(limit=1000))
shutil.rmtree("/home/browser-worker/Cloud/rev2")
os.makedirs("/home/browser-worker/Downloads", exist_ok=True)
os.symlink("/home/browser-worker/Downloads", "/home/browser-worker/Cloud/dl")
for _ in range(3): asyncio.run(s.push_once())
print("HELD", s.halt["reason"], s.halt["held"])
"""))
    assert first.returncode == 0, first.stderr[-3000:]
    assert "HELD mass_delete 30" in first.stdout
    assert len(json.loads((cloud / "db.json").read_text())["files"]) == 31
    second = _docker(home, cloud, _py(r"""
s = mk()
pathlib.Path("/home/browser-worker/Cloud/after.txt").write_text("written after the move")
for _ in range(2): asyncio.run(s.push_once())
assert s.halt and s.halt["held"] == 30, s.halt
print("SKIPPED", sorted(i["path"] for i in s.status()["skipped"]["items"]))
print("RESTORE", asyncio.run(s.resolve_held(s.halt["hold_id"], "restore")))
for _ in range(3): asyncio.run(s.push_once())
print("AFTER", s.halt, len(list(pathlib.Path("/home/browser-worker/Cloud/rev2").iterdir())))
"""))
    assert second.returncode == 0, second.stderr[-3000:]
    assert "SKIPPED ['dl']" in second.stdout
    assert "'restored': 30" in second.stdout and "AFTER None 30" in second.stdout
    db = json.loads((cloud / "db.json").read_text())["files"]
    assert len(db) == 32 and "after.txt" in db, "a held delete or the symlink lost data"
