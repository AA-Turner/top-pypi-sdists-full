from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from anteroom.db import get_db, init_db
from anteroom.services import mission_storage, workflow_storage

_PYTHON = sys.executable


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    (anteroom_dir / "config.yaml").write_text(
        'ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n'
    )
    monkeypatch.setenv("HOME", str(tmp_path))


def _run_aroom(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    repo_root = str(Path(__file__).resolve().parents[2] / "src")
    env["PYTHONPATH"] = repo_root if not existing else repo_root + os.pathsep + existing
    return subprocess.run([_PYTHON, "-m", "anteroom", *args], capture_output=True, text=True, timeout=30, env=env)


def _seed_db(tmp_path: Path) -> tuple[dict, dict]:
    db_path = tmp_path / ".anteroom" / "chat.db"
    db = init_db(db_path) if not db_path.exists() else get_db(db_path)
    session = mission_storage.create_session(db, title="Observe Mission", status="active")
    item = mission_storage.create_item(db, session_id=session["id"], summary="Ship it", status="blocked")
    run = workflow_storage.create_workflow_run(
        db,
        workflow_id="observe-flow",
        workflow_version="1",
        target_kind="mission_item",
        target_ref=item["id"],
    )
    mission_storage.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref=run["id"])
    workflow_storage.update_workflow_run(db, run["id"], status="waiting_for_approval", current_step_id="gate")
    workflow_storage.create_approval_request(
        db,
        run_id=run["id"],
        step_id="gate",
        tool_name="bash",
        tool_args={"command": "git push"},
        risk_tier="high",
    )
    return session, run


def test_observe_help(tmp_path: Path) -> None:
    result = _run_aroom("observe", "--help")
    assert result.returncode == 0
    assert "Mission session ID/prefix or workflow run ID/prefix" in result.stdout


def test_observe_mission(tmp_path: Path) -> None:
    session, _run = _seed_db(tmp_path)
    result = _run_aroom("observe", session["id"])
    output = result.stdout + result.stderr
    assert result.returncode == 0
    assert "Observe Mission" in output
    assert "Ship it" in output
    assert "Pending approvals" in output


def test_observe_workflow_json(tmp_path: Path) -> None:
    _session, run = _seed_db(tmp_path)
    result = _run_aroom("observe", run["id"], "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["kind"] == "workflow"
    assert payload["pending_approvals"][0]["tool_name"] == "bash"
