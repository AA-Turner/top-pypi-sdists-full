"""公開の偽のランタイム `agenticstar_platform.workflow.testing`（3.2.1、devdocs 3.3 AU-24 / R33-290）。

固定する契約:
1. 契約・parameters・入力の成果物・接続の token・効果の認定・期限・指示を引数で渡せ、保存された成果物・監査・completion を読める
2. 偽物は parameters の形・契約を検査しない（正は executor と管理コンソールの事前の検査）
3. 例の Agent（docs/examples/workflow_reply_agent.py）を偽物で 1 工程通せる
4. `agenticstar_platform.workflow` は testing を読み込まない（import を軽く保つ）
"""
from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest

from agenticstar_platform.workflow import arun
from agenticstar_platform.workflow.testing import (
    BASE_URL,
    EXECUTION_ID,
    TOKEN,
    FakeRuntime,
    sample_contract,
    sample_parameters,
)

SDK_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = SDK_ROOT / "docs" / "examples"
FIX = "tests.workflow.agent_fixtures"

CONTRACT = {
    "runtime_protocol": "mp-workflow/1",
    "effect_mode": "read_only",
    "parameters_schema": {"type": "object", "properties": {"tone": {"type": "string"}}, "required": ["tone"]},
    "env_bindings": {"TONE": "tone"},
    "files": [{"name": "brief", "path": "in/brief.json", "format": "json", "required": True}],
    "outputs": [{"name": "summary", "path": "summary.txt", "format": "text", "required": True}],
    "limits": {"execution_timeout_seconds": 300},
}


@pytest.fixture(autouse=True)
def _sdk_on_path(monkeypatch):
    monkeypatch.setenv("PYTHONPATH", str(SDK_ROOT))
    monkeypatch.delenv("ASTER_RUNTIME_TOKEN", raising=False)
    monkeypatch.chdir(SDK_ROOT)


async def test_a_custom_contract_runs_one_step_and_the_results_can_be_read(tmp_path: Path):
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    # parameters は契約の parameters_schema（tone は文字列）に合わないが、偽物は検査しない
    fake = FakeRuntime(contract=CONTRACT, parameters={"tone": 5}, inputs={"brief": '{"topic": "renewal"}'},
                       connections={"crm": ("crm-token", expires)}, effect_mode="idempotent_write")
    res = await arun(f"{FIX}:run_custom_contract", env=fake.runner_env(), workspace=str(tmp_path), transport=fake.transport)
    assert (res.outcome, res.outcome_reason_code, res.exit_code) == ("completed", "completed", 0)

    artifacts = fake.saved_artifacts()
    assert list(artifacts) == ["summary"]
    assert artifacts["summary"]["content"] == f"renewal|5|crm-token|{expires.isoformat()}|idempotent_write\n".encode()
    assert artifacts["summary"]["path"] == "summary.txt" and artifacts["summary"]["source"] == "output"

    events = fake.saved_audit_events()
    assert [e["event_type"] for e in events] == ["context.manifest", "context.manifest", "tool.invoked", "tool.effect"]
    assert events[2]["metadata"]["tool"] == "read_brief"

    completion = fake.saved_completion()
    assert completion["envelope"]["outcome"] == "completed"
    assert completion["output_artifact_ids"] == [artifacts["summary"]["artifact_id"]]
    assert fake.connection_token_calls == ["crm"]

    ctx = fake._ctx()   # 前の版の偽物と同じく、front の context の形
    assert ctx["env"] == {"TONE": "5"} and ctx["connections"] == {"crm": "provider-crm"}
    assert ctx["input_manifest"][0]["target_path"] == "in/brief.json" and ctx["input_manifest"][0]["format"] == "json"
    assert set(ctx["contract"]) == {"contract_digest", "image_digest", "parameters_schema", "files", "outputs",
                                    "effect_mode", "limits"}


async def test_the_sample_example_agent_runs_one_step(tmp_path: Path, monkeypatch):
    """AC-33-290-1 の形: 例の Agent を偽物で 1 工程通し、成果物と監査を読む。"""
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join([str(SDK_ROOT), str(EXAMPLES)]))
    fake = FakeRuntime(parameters={"product_code": "P-100", "language": "en"}, inputs={"instructions": b"Say thanks.\n"})
    res = await arun("workflow_reply_agent:run", env=fake.runner_env(), workspace=str(tmp_path), transport=fake.transport)
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed")
    assert fake.saved_artifacts()["reply"]["content"] == b"# Draft reply: P-100\n\nSay thanks.\n"
    assert [e["event_type"] for e in fake.saved_audit_events()][2:] == ["tool.invoked", "tool.effect"]


async def test_the_sample_example_agent_ends_incomplete_without_instructions(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join([str(SDK_ROOT), str(EXAMPLES)]))
    fake = FakeRuntime(inputs={"instructions": b"  \n"})
    res = await arun("workflow_reply_agent:run", env=fake.runner_env(), workspace=str(tmp_path), transport=fake.transport)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "missing_instructions")
    report = fake.saved_completion()["envelope"]["completion_report"]
    assert report["completed"] is False and report["reason_code"] == "missing_instructions" and report["comment"]
    assert fake.saved_artifacts() == {}


def test_defaults_are_the_sample_contract():
    fake = FakeRuntime()
    assert fake.contract == sample_contract() and fake.parameters == sample_parameters()
    assert [m["target_path"] for m in fake._input_manifest()] == ["instructions.md"]
    assert fake.connection_tokens == {}
    # 契約を渡したら parameters の既定は空、instructions のファイルが無ければ入力も無い
    own = FakeRuntime(contract=CONTRACT)
    assert own.parameters == {} and own._input_manifest() == []
    assert own.contract is not CONTRACT and own.contract["effect_mode"] == "read_only"


def test_an_input_that_is_not_a_contract_file_is_a_usage_error():
    with pytest.raises(ValueError, match="not a file of the contract"):
        FakeRuntime(inputs={"nope": b"x"})


def test_connection_tokens_accept_a_plain_token():
    fake = FakeRuntime(connections={"crm": "t-1", "erp": ("t-2", "2026-10-28T00:00:00+00:00")})
    assert fake.connection_tokens == {"crm": ("t-1", None), "erp": ("t-2", "2026-10-28T00:00:00+00:00")}


async def test_the_readers_return_copies(tmp_path: Path):
    fake = FakeRuntime()
    await arun(f"{FIX}:run_reply", env=fake.runner_env(), workspace=str(tmp_path), transport=fake.transport)
    fake.saved_artifacts()["reply"]["logical_name"] = "changed"
    fake.saved_audit_events()[0]["event_type"] = "changed"
    fake.saved_completion()["envelope"]["outcome"] = "changed"
    assert fake.saved_artifacts()["reply"]["logical_name"] == "reply"
    assert fake.saved_audit_events()[0]["event_type"] == "context.manifest"
    assert fake.saved_completion()["envelope"]["outcome"] == "completed"
    assert FakeRuntime().saved_completion() is None


def test_runner_env_points_at_the_fake():
    env = FakeRuntime.runner_env()
    assert env["EXECUTION_ID"] == EXECUTION_ID and env["ASTER_RUNTIME_PROTOCOL"] == "mp-workflow/1"
    assert env["ASTER_RUNTIME_BASE_URL"].endswith("/api/mp/runtime/v1/executions")


def test_the_workflow_package_does_not_import_testing():
    code = ("import sys; import agenticstar_platform.workflow; "
            "assert 'agenticstar_platform.workflow.testing' not in sys.modules; "
            "import agenticstar_platform.workflow.testing; assert 'asyncpg' not in sys.modules; print('ok')")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True,
                         env={**os.environ, "PYTHONPATH": str(SDK_ROOT)})
    assert out.stdout.strip() == "ok"



# ---------------------------------------------------------------------------
# 公開前レビュー（2026-10-28）の指摘
# ---------------------------------------------------------------------------
def _readme_testing_section() -> str:
    text = (SDK_ROOT / "README.md").read_text(encoding="utf-8")
    start = text.index("**Testing an agent without ASTER**")
    return text[start:text.index("\n### ", start)]


def test_the_readme_procedure_runs_as_written(tmp_path: Path):
    """README の「ASTER 無しで 1 工程を通す」手順を、書いてあるファイルとコマンドのとおりに回して completed になる
    （`PYTHONPATH=.` だと子が作業の場所で `.` を探して my_agent を読めず、saved_artifacts()["reply"] が KeyError）。"""
    section = _readme_testing_section()
    blocks = re.findall(r"```(\w+)\n(.*?)```", section, re.S)
    files = {body.splitlines()[0][2:].strip(): body for lang, body in blocks
             if lang == "python" and body.startswith("# ")}
    assert set(files) == {"my_agent/main.py", "try_it.py"}
    command = next(line for lang, body in blocks if lang == "bash" for line in body.splitlines()
                   if "python try_it.py" in line)
    project = tmp_path / "my_project"
    (project / "my_agent").mkdir(parents=True)
    (project / "my_agent" / "__init__.py").write_text("", encoding="utf-8")
    for name, body in files.items():
        (project / name).write_text(body, encoding="utf-8")
    # 試験の python はこの SDK を site-packages に持たないので、python の代わりに SDK を前に置いてから
    # try_it.py を実行する小さな起動役を使う（環境変数とコマンドの残りは README のまま）
    launcher = tmp_path / "launch.py"
    launcher.write_text(f"import runpy, sys\nsys.path.insert(0, {str(SDK_ROOT)!r})\n"
                        "runpy.run_path(sys.argv[1], run_name='__main__')\n", encoding="utf-8")
    shell = command.replace("python try_it.py", f"{shlex.quote(sys.executable)} {shlex.quote(str(launcher))} try_it.py")
    out = subprocess.run(["bash", "-c", shell], cwd=project, capture_output=True, text=True, timeout=120,
                         env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(tmp_path)})
    assert out.returncode == 0, out.stderr[-2000:]
    assert out.stdout.splitlines()[0] == "completed completed"
    assert "Thank the customer." in out.stdout


async def _post_audit(fake: FakeRuntime, *event_types: str) -> httpx.Response:
    events = [{"event_id": f"{t}-{uuid.uuid4()}", "event_type": t, "decision": "ok", "metadata": {}} for t in event_types]
    async with httpx.AsyncClient(transport=fake.transport, headers={"Authorization": f"Bearer {TOKEN}"}) as client:
        return await client.post(f"{BASE_URL}/{EXECUTION_ID}/audit", json={"events": events})


@pytest.mark.parametrize("close,code", [("cancel_requested_at", "cancelled"), ("run_closed", "run_closed"),
                                        ("deadline_passed", "deadline_exceeded")])
async def test_records_of_done_operations_are_accepted_after_the_run_is_closed(close, code):
    """front（#2625 の lateRecords）と同じく、取消・run の終端・期限の後でも terminal になるまでは tool.effect /
    tool.denied だけの監査を受ける。新しい操作（tool.invoked）や混ざった batch は今どおり 409。"""
    fake = FakeRuntime()
    setattr(fake, close, "2026-10-28T00:00:00Z" if close == "cancel_requested_at" else True)
    for types in (["tool.effect"], ["tool.denied"], ["tool.effect", "tool.denied"]):
        res = await _post_audit(fake, *types)
        assert res.status_code == 200, (types, res.text)
    for types in (["tool.invoked"], ["tool.effect", "tool.invoked"], ["context.manifest"]):
        res = await _post_audit(fake, *types)
        assert (res.status_code, res.json()["code"]) == (409, code), types
    assert [e["event_type"] for e in fake.saved_audit_events()] == ["tool.effect", "tool.denied", "tool.effect", "tool.denied"]
    fake.state = "terminal"   # terminal の後は記録も断る
    assert (await _post_audit(fake, "tool.effect")).status_code == 409


async def test_the_context_reports_the_end_of_the_run_as_cancellation():
    """front の /context は run の終端も cancel_requested_at で返す（runClosedAt）。"""
    fake = FakeRuntime()
    async with httpx.AsyncClient(transport=fake.transport, headers={"Authorization": f"Bearer {TOKEN}"}) as client:
        assert (await client.get(f"{BASE_URL}/{EXECUTION_ID}/context")).json()["cancel_requested_at"] is None
        fake.run_closed = True
        assert (await client.get(f"{BASE_URL}/{EXECUTION_ID}/context")).json()["cancel_requested_at"]
    fake.run_closed, fake.cancel_requested_at = False, "2026-10-28T00:00:00Z"
    assert fake._ctx()["cancel_requested_at"] == "2026-10-28T00:00:00Z"


def test_env_numbers_are_written_as_the_platform_writes_them():
    """front の envFromParameters は数を JSON.stringify で書く（5.0 → "5"）。"""
    contract = {**CONTRACT, "env_bindings": {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}}
    fake = FakeRuntime(contract=contract, parameters={"a": 5.0, "b": 3, "c": 0.5, "d": True, "e": "x", "f": [1]})
    assert fake._ctx()["env"] == {"A": "5", "B": "3", "C": "0.5", "D": "true", "E": "x"}
