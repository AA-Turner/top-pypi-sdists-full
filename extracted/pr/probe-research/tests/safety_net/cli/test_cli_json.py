"""Golden JSON of read commands: the real `python -m probe.cli` against the served FakeApp.

Each command runs as a child (the pinned entry, so no module path is patched) with its own
HOME; stdout is parsed as JSON, ids and times are normalised, and the API calls it made are kept.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from pathlib import Path

import httpx
import pytest

from tests.conftest import FakeApp
from tests.served_fake_app import serve

TOKEN = "ros_pat_deadbeef"
WORKSPACE = "11111111-1111-1111-1111-111111111111"
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?")
#: The reads pinned, by name: argv after `probe`. `{run}` is the seeded run's id.
READS = {
    "project_list": ["project", "list"],
    "project_get": ["project", "get", "parity"],
    "experiment_list": ["experiment", "list", "--project", "parity"],
    "run_list": ["run", "list", "--project", "parity"],
    "run_get": ["run", "get", "{run}"],
}


class Backend(FakeApp):
    """The fake API, keeping every request's method, path and query."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[str] = []
        self.calls_lock = threading.Lock()

    def handler(self, request: httpx.Request) -> httpx.Response:
        with self.calls_lock:
            query = "&".join(f"{k}={v}" for k, v in sorted(request.url.params.multi_items()))
            self.calls.append(f"{request.method} {request.url.path}" + (f"?{query}" if query else ""))
        return super().handler(request)


def _post(app: FakeApp, path: str, body: dict) -> dict:
    answer = app.handler(httpx.Request("POST", f"http://test{path}", json=body,
                                       headers={"authorization": f"Bearer {TOKEN}"}))
    assert answer.status_code < 300, (path, answer.status_code, answer.text)
    return answer.json()


@pytest.fixture
def backend():
    app = Backend()
    project = _post(app, "/v1/projects", {"name": "Parity", "slug": "parity", "workspace_id": WORKSPACE})
    experiment = app.seed_experiment("exp-a", project_id=project["id"])
    run = _post(app, f"/v1/projects/{experiment['id']}/runs", {"name": "first run", "slug": "first-run"})
    app.calls.clear()  # the seeding is not a read under test
    names = {project["id"]: "<project>", experiment["id"]: "<experiment>", run["id"]: "<run>"}
    return app, names


def _normal(value, names: dict):
    if isinstance(value, dict):
        return {key: _normal(item, names) for key, item in value.items()}
    if isinstance(value, list):
        return [_normal(item, names) for item in value]
    if isinstance(value, str):
        value = UUID.sub(lambda m: names.setdefault(m.group(0), f"<uuid-{len(names) - 2}>"), value)
        return TIME.sub("<time>", value)
    return value


def _read(argv: list[str], env: dict, url: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "probe.cli", *argv], capture_output=True, text=True, timeout=120,
                          stdin=subprocess.DEVNULL, cwd=env["HOME"],
                          env={**env, "PROBE_BASE_URL": url, "PROBE_TOKEN": TOKEN})


def test_read_commands_print_the_same_json(backend, child_env, baseline):
    app, names = backend
    run_id = next(key for key, name in names.items() if name == "<run>")
    out = {}
    with serve(app) as url:
        for name, argv in READS.items():
            app.calls.clear()
            done = _read([word.replace("{run}", run_id) for word in argv], child_env, url)
            assert done.returncode == 0, f"probe {' '.join(argv)} exited {done.returncode}: {done.stderr[-2000:]}"
            out[name] = {
                "argv": " ".join(argv),
                "stdout": _normal(_json(done.stdout, argv), names),
                "requests": _normal(list(app.calls), names),
            }
    baseline("cli_json", out)


def _json(text: str, argv: list[str]):
    try:
        return json.loads(text)
    except ValueError:
        pytest.fail(f"`probe {' '.join(argv)}` printed no JSON:\n{text[:2000]}", pytrace=False)


def test_the_reads_reach_this_tree():
    """The child imports THIS checkout's `probe` (the venv's editable install), not another."""
    here = Path(__file__).resolve().parents[3] / "src"
    done = subprocess.run([sys.executable, "-I", "-c", "import probe, sys; sys.stdout.write(probe.__file__)"],
                          capture_output=True, text=True, timeout=60)
    assert Path(done.stdout).resolve().is_relative_to(here), done.stdout
