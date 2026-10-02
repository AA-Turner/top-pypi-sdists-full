"""`agenticstar_platform.workflow` runner の契約 / 障害試験（marketplace-3.0 03、AC-01/06/07/10/11/12/14 の SDK 部分）。

固定する契約:
1. executor 注入 env の検証（汎用設定へ fallback しない、protocol / UUID）。設定不正では Agent を呼ばない
2. 入力の digest / size / 形式検証、`/workspace/input` は read-only、work へコピー、from_parameters の設定ファイル生成
3. context.manifest の ack の後にだけ Agent を起動。tool.invoked の ack が無ければ write を開始しない（期限後も承認しない）
4. 宣言 output だけを root fd 経由で回収（symlink / traversal / FIFO / root 差し替え / サイズ / schema 拒否）。required 欠落は成功にしない
5. envelope v2: outcome は「どう終わったか」の 7 値（completed / incomplete / failed / timeout / stopped / denied / skipped）。
   write の成否は outcome を決めず、効果不明は had_mutating_success = None で表す（front が自動 retry しない根拠）
6. completion は同じ completion_id / payload で再送、409 terminal は再実行せず終了、保存できなければ exit 2、
   所有権未証明なら送らない、再起動で Agent を再実行しない
7. token / traceback / 本文は Agent プロセス・監査・ログへ出ない。配下プロセスは回収前に止める
8. SIGTERM は協調停止（`failed/runner_stopped`。効果不明）へ変換する。それ以外の障害（想定外の例外 / cancel / ワークスペース破損）は
   completion を送らず例外のまま非0 で終わる（00 §7: 非0 終了 = 効果不明 = executor `failed/agent_exit_nonzero` = hold。
   SDK は終了コードを保証しない）
"""
from __future__ import annotations

import asyncio
import json
import os
import signal
import stat
import sys
from pathlib import Path

import httpx
import pytest

from agenticstar_platform.workflow import (
    OUTCOMES,
    EffectTally,
    WorkflowConfigError,
    WorkflowRunner,
    arun,
    build_envelope,
    decide_outcome,
    run as sync_run,
    validate_env,
)
from agenticstar_platform.workflow.files import (
    OutputCollectionError,
    WorkspaceRoot,
    collect_outputs,
    relative_path,
    safe_join,
)
from agenticstar_platform.workflow.schema import SchemaError, parse_yaml_strict, validate_value

from .fake_runtime import EXECUTION_ID, TOKEN, FakeRuntime

FIX = "tests.workflow.agent_fixtures"
EDIT_OUTPUT = {"name": "instructions_edit", "path": "instructions.md", "source": "work", "format": "markdown", "required": False}


def env_for(base_url: str = "http://front.test/api/mp/runtime/v1/executions") -> dict[str, str]:
    return {"ASTER_RUNTIME_PROTOCOL": "mp-workflow/1", "ASTER_RUNTIME_BASE_URL": base_url,
            "ASTER_RUNTIME_TOKEN": TOKEN, "EXECUTION_ID": EXECUTION_ID}


@pytest.fixture(autouse=True)
def _sdk_on_path(monkeypatch):
    sdk_root = str(Path(__file__).resolve().parents[2])
    monkeypatch.setenv("PYTHONPATH", sdk_root)
    monkeypatch.delenv("ASTER_RUNTIME_TOKEN", raising=False)
    monkeypatch.chdir(sdk_root)


async def run_with(fake: FakeRuntime, entry: str, workspace: Path, **kw):
    runner = WorkflowRunner(entrypoint=f"{FIX}:{entry}", env=env_for(), workspace=str(workspace), transport=fake.transport,
                            python=kw.pop("python", None),
                            cancel_poll_seconds=kw.pop("cancel_poll_seconds", 0.3), child_grace_seconds=kw.pop("child_grace_seconds", 3.0))
    return await runner.run()


# ---------------------------------------------------------------------------
# 1. env
# ---------------------------------------------------------------------------
def test_validate_env_rejects_missing_protocol_and_bad_ids():
    ok = validate_env(env_for())
    assert ok["EXECUTION_ID"] == EXECUTION_ID
    with pytest.raises(WorkflowConfigError):
        validate_env({k: v for k, v in env_for().items() if k != "ASTER_RUNTIME_TOKEN"})
    with pytest.raises(WorkflowConfigError):
        validate_env({**env_for(), "ASTER_RUNTIME_PROTOCOL": "mp-workflow/2"})
    with pytest.raises(WorkflowConfigError):
        validate_env({**env_for(), "EXECUTION_ID": "abc"})
    with pytest.raises(WorkflowConfigError):
        validate_env({**env_for(), "ASTER_RUNTIME_BASE_URL": "front.test"})
    with pytest.raises(WorkflowConfigError):
        validate_env({"DB_HOST": "x", "EXECUTION_ID": EXECUTION_ID})  # 旧 runner の DB env には fallback しない


# ---------------------------------------------------------------------------
# 2〜6. happy path（回答案 / 模擬送信）
# ---------------------------------------------------------------------------
async def test_reply_agent_end_to_end(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_reply", tmp_path)
    assert res.exit_code == 0 and res.completion_saved and (res.outcome, res.outcome_reason_code) == ("completed", "completed")
    assert res.had_mutating_success is False
    inp = tmp_path / "input" / "instructions.md"
    assert inp.read_bytes() == b"# do it\n" and not (inp.stat().st_mode & stat.S_IWUSR)
    assert (tmp_path / "work" / "instructions.md").exists()
    assert json.loads((tmp_path / "work" / "settings" / "agent.yaml").read_text()) == {"product_code": "P-100", "language": "ja"}
    types = [e["event_type"] for e in fake.audit_events]
    assert types[:2] == ["context.manifest"] * 2 and types[2:] == ["tool.invoked", "tool.effect"]  # start + owner fence
    assert fake.calls.index(f"POST /api/mp/runtime/v1/executions/{EXECUTION_ID}/audit") < fake.calls.index(
        f"POST /api/mp/runtime/v1/executions/{EXECUTION_ID}/artifacts")
    assert len(fake.artifacts) == 1 and next(iter(fake.artifacts.values()))["logical_name"] == "reply"  # 未編集の入力は再保存しない
    env = fake.completion["envelope"]
    assert env["version"] == 2 and env["envelope_version"] == 2 and env["counts"]["read_calls"] == 1 and env["resumed"] is False
    assert fake.completion["output_artifact_ids"] == [res.artifacts[0]["artifact_id"]]
    state = json.loads((tmp_path / ".aster_workflow_state.json").read_text())
    assert state["completion_id"] == fake.completion["completion_id"] and state["started"] and state["completion"]["envelope"] == env


async def test_send_agent_records_effect_and_completes(tmp_path: Path):
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_send", tmp_path)
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", True)
    inv = [e for e in fake.audit_events if e["event_type"] == "tool.invoked"][0]
    eff = [e for e in fake.audit_events if e["event_type"] == "tool.effect"][0]
    assert inv["metadata"]["action_ref"] == eff["metadata"]["action_ref"]
    assert "token" not in json.dumps(fake.audit_events).lower()


async def test_seven_outcomes_are_reachable(tmp_path: Path):
    # effect の無い write: Agent は完遂（completed）。効果は不明 = had None（outcome は下げない）
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_unobserved", tmp_path / "a")
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed") and res.had_mutating_success is None
    assert fake.completion["envelope"]["counts"]["mutating_unresolved"] == 1
    # status unknown の effect も同じ
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_unknown_effect", tmp_path / "b")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", None)
    # 既知の write 失敗（成功なし）: Agent が正常に戻ったなら完遂。失敗は counts に残る
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_failed_effect", tmp_path / "c")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", False)
    assert fake.completion["envelope"]["counts"]["mutating_failed"] == 1
    # denied/policy_denied
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_denied", tmp_path / "d")
    assert (res.outcome, res.outcome_reason_code) == ("denied", "policy_denied")
    # skipped/no_target（宣言された skip 理由。skip は成果物を作らないので required output より先）
    fake = FakeRuntime()
    res = await run_with(fake, "run_skip", tmp_path / "e")
    assert (res.outcome, res.outcome_reason_code) == ("skipped", "no_target")
    # read_only、read だけ、output なし = 完遂
    fake = FakeRuntime()
    fake.contract["outputs"] = []
    res = await run_with(fake, "run_read_only", tmp_path / "f")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", False)
    # failed/agent_error
    fake = FakeRuntime()
    res = await run_with(fake, "run_error", tmp_path / "g")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error")


async def test_denial_partial_failure_and_shared_action_ref(tmp_path: Path):
    # 成功の後の拒否 → denied（had=true のまま）。report があっても completed にしない
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_send_then_denied", tmp_path / "a")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("denied", "policy_denied", True)
    # 成功 + 失敗の混在: 完遂（書き込みの失敗は成否にしない）。両方とも counts に残る
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_partial_failure", tmp_path / "b")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", True)
    c = fake.completion["envelope"]["counts"]
    assert (c["mutating_success"], c["mutating_failed"]) == (1, 1)
    # 同じ action_ref を共有しても effect は呼出し単位: 2 回目は未観測 → 効果不明
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_shared_action_ref", tmp_path / "c")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("completed", "completed", True)
    assert fake.completion["envelope"]["counts"]["mutating_unresolved"] == 1
    # 外部行為前の policy 不明 → skipped/policy_unavailable（front が再照合）。required output が無くても skip が先
    fake = FakeRuntime()
    res = await run_with(fake, "run_policy_unavailable", tmp_path / "d")
    assert (res.outcome, res.outcome_reason_code) == ("skipped", "policy_unavailable")
    # skip でも report の保存に失敗したら次工程へ進む outcome を出さない
    fake = FakeRuntime()
    fake.fail_upload_times = 100
    res = await run_with(fake, "run_skip_with_report", tmp_path / "e")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "artifact_save_failed")


async def test_agent_exception_is_failed_and_traceback_not_leaked(tmp_path: Path, capfd):
    fake = FakeRuntime()
    res = await run_with(fake, "run_error", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error") and res.exit_code == 0
    assert fake.completion["envelope"]["error_class"] == "RuntimeError"
    out, err = capfd.readouterr()
    assert "secret-value-123" not in json.dumps(fake.audit_events) and "secret-value-123" not in json.dumps(fake.completion)
    assert "secret-value-123" not in out + err and "RuntimeError" in err  # 本文は Pod ログへも写さない（クラス名だけ）


async def test_sync_entrypoint_and_required_output_missing(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_sync", tmp_path)
    assert res.outcome == "completed"
    fake2 = FakeRuntime()
    fake2.contract["outputs"] = [{"name": "reply", "path": "reply.md", "format": "markdown", "required": True},
                                 {"name": "summary", "path": "summary.md", "format": "markdown", "required": True}]
    res = await run_with(fake2, "run_sync", tmp_path / "b")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "required_output_missing") and res.completion_saved


async def test_edited_input_is_uploaded_only_when_declared_and_changed(tmp_path: Path):
    fake = FakeRuntime()
    fake.contract["outputs"].append(EDIT_OUTPUT)
    res = await run_with(fake, "run_edit_instructions", tmp_path)
    assert res.outcome == "completed" and sorted(a["logical_name"] for a in fake.artifacts.values()) == ["instructions_edit", "reply"]
    fake = FakeRuntime()
    fake.contract["outputs"].append(EDIT_OUTPUT)
    res = await run_with(fake, "run_reply", tmp_path / "b")
    assert [a["logical_name"] for a in fake.artifacts.values()] == ["reply"]


# ---------------------------------------------------------------------------
# 3. 監査の ack が無ければ進めない / 期限後は承認しない
# ---------------------------------------------------------------------------
async def test_manifest_not_persisted_means_agent_not_started(tmp_path: Path):
    # manifest の監査が保存できない = 所有権を証明できていない → Agent を起動せず、**completion も送らない**
    # （所有者かもしれない他 instance の実行を横から terminal にしない。executor の照合 completion_missing に収束）
    fake = FakeRuntime()
    fake.fail_audit_types = {"context.manifest"}
    res = await run_with(fake, "run_reply", tmp_path)
    assert res.outcome is None and res.completion_saved is False and fake.completion is None and res.exit_code == 2
    assert not (tmp_path / "output" / "reply.md").exists() and not fake.artifacts
    state = json.loads((tmp_path / ".aster_workflow_state.json").read_text())
    assert not state.get("started") and not state.get("fence_owner")
    assert (state.get("tally") or {}).get("persist_failures") == 1


async def test_tool_invoked_without_ack_blocks_the_write_and_is_not_success(tmp_path: Path):
    fake = FakeRuntime(effect_mode="idempotent_write")
    fake.fail_audit_types = {"tool.invoked"}
    res = await run_with(fake, "run_audit_blocked", tmp_path)
    assert (tmp_path / "output" / "reply.md").read_text().startswith("blocked:AuditNotPersisted")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "audit_persist_failed")  # 未 ack の必須監査 = 正常成功にしない


async def test_invoked_after_agent_deadline_is_not_acknowledged(tmp_path: Path):
    # ゲートの単体: agent_deadline を過ぎていれば保存済みでも承認しない（tally にも数えない）
    fake = FakeRuntime(effect_mode="idempotent_write")
    runner = WorkflowRunner(entrypoint=f"{FIX}:run_send", env=env_for(), workspace=str(tmp_path), transport=fake.transport)
    from agenticstar_platform.workflow.runtime_client import RuntimeClient
    from datetime import datetime, timedelta, timezone
    runner._client = RuntimeClient(env_for()["ASTER_RUNTIME_BASE_URL"], EXECUTION_ID, TOKEN, transport=fake.transport)
    runner._agent_deadline = datetime.now(timezone.utc) - timedelta(seconds=1)
    reply = await runner._on_audit({"event_id": "i-1", "event_type": "tool.invoked", "metadata": {"tool": "w", "effect_kind": "send"}})
    assert reply["accepted"] is False and runner._tally.counts()["tool_calls"] == 0 and runner._stop_reason == "deadline"
    await runner._client.aclose()
    # 結合: 期限で止められた Agent は write を始められず timeout で終端（既発生の効果は無い）
    fake = FakeRuntime(effect_mode="idempotent_write", deadline_seconds=3)  # 回収猶予 300s があるので実行窓 3s は削られない
    res = await run_with(fake, "run_slow_write_after_deadline", tmp_path / "b", cancel_poll_seconds=0.2)
    assert (res.outcome, res.outcome_reason_code) == ("timeout", "execution_timeout")
    out = tmp_path / "b" / "output" / "reply.md"
    assert not out.exists() or out.read_text() == "blocked\n"
    assert fake.completion["envelope"]["counts"]["tool_calls"] == 0


async def test_deadline_arriving_after_start_is_adopted(tmp_path: Path):
    # 起動時に期限が無い（executor が観測前）→ 途中で確定した（既に過ぎた）期限を採用して止める。延長はしない
    from datetime import datetime, timedelta, timezone
    fake = FakeRuntime(effect_mode="idempotent_write", deadline_seconds=None)

    async def expire_later():
        await asyncio.sleep(1.0)
        fake.execution_deadline = datetime.now(timezone.utc) - timedelta(seconds=1)
    task = asyncio.create_task(expire_later())
    res = await run_with(fake, "run_slow_write_after_deadline", tmp_path, cancel_poll_seconds=0.2)
    await task
    assert (res.outcome, res.outcome_reason_code) == ("timeout", "execution_timeout")
    assert fake.completion["envelope"]["counts"]["tool_calls"] == 0


async def test_manifest_duplicate_from_another_workspace_blocks_start(tmp_path: Path):
    # 別 instance（入れ替わり Pod）の manifest が既に保存済み → 所有者でない: Agent を起動せず、completion も送らない
    fake = FakeRuntime(effect_mode="idempotent_write")
    fake.audit_ids.add(f"context-manifest-{EXECUTION_ID}")
    res = await run_with(fake, "run_send", tmp_path / "a")
    assert res.outcome is None and res.completion_saved is False and fake.completion is None and res.exit_code == 2
    assert not [e for e in fake.audit_events if e["event_type"] == "tool.invoked"]
    state = json.loads((tmp_path / "a" / ".aster_workflow_state.json").read_text())
    assert state.get("fence_lost") and not state.get("started")
    # 同じ workspace で再起動しても（B は保存済みで duplicates になる）所有者にならない
    res = await run_with(fake, "run_send", tmp_path / "a")
    assert res.outcome is None and fake.completion is None
    # 自分の初回 accepted の応答を失った（A + B を保存後に 500）→ 再送は A dup + B dup で所有の証拠にならない → 安全側（起動しない）。
    # front は A が重複でも B を commit するので、負けた instance の lost-ack と区別できない
    fake = FakeRuntime(effect_mode="idempotent_write")
    fake.persist_then_500 = {"context.manifest": 1}
    res = await run_with(fake, "run_send", tmp_path / "b")
    assert res.outcome is None and fake.completion is None
    assert len([e for e in fake.audit_events if e["event_type"] == "context.manifest"]) == 2
    # accepted を観測済み（state.fence_owner）で Agent 未起動のまま再起動 → A dup + B dup は自分のもの → 起動して良い
    fake = FakeRuntime(effect_mode="idempotent_write")
    ws = tmp_path / "b2"
    ws.mkdir()
    inst = "22222222-3333-4444-8555-666666666666"
    fake.audit_ids.update({f"context-manifest-{EXECUTION_ID}", f"context-manifest-{EXECUTION_ID}-{inst}"})
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"runner_instance": inst, "fence_owner": "x"}))
    res = await run_with(fake, "run_send", ws)
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed")
    # 503 が処理前に返り、その間に別 instance が A を保存した → こちらの再送は A dup + B accepted → 所有者でない
    fake = FakeRuntime(effect_mode="idempotent_write")
    fake.reject_all_writes = True

    async def other_owner_appears():
        await asyncio.sleep(0.8)
        fake.audit_ids.add(f"context-manifest-{EXECUTION_ID}")
        fake.reject_all_writes = False
    task = asyncio.create_task(other_owner_appears())
    res = await run_with(fake, "run_send", tmp_path / "c")
    await task
    assert res.outcome is None and fake.completion is None and not [e for e in fake.audit_events if e["event_type"] == "tool.invoked"]


async def test_short_execution_window_is_not_consumed_by_cleanup_margin(tmp_path: Path):
    fake = FakeRuntime(deadline_seconds=5)  # 実行 5s + 回収 300s → Agent は 5s 使える
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed")


async def test_journal_failure_refuses_ack(tmp_path: Path, monkeypatch):
    from agenticstar_platform.workflow import runner as runner_mod
    orig = runner_mod._State.set

    def failing_set(self, key, value):
        if key == "tally":
            raise OSError("disk full")
        return orig(self, key, value)
    monkeypatch.setattr(runner_mod._State, "set", failing_set)
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_audit_blocked", tmp_path)
    assert (tmp_path / "output" / "reply.md").read_text().startswith("blocked:AuditNotPersisted")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "audit_persist_failed")
    # skip の journal 失敗も成功に化けない（Agent には例外、outcome は保存失敗）
    fake = FakeRuntime()
    res = await run_with(fake, "run_skip_with_report", tmp_path / "s")
    assert (res.outcome, res.outcome_reason_code) == ("failed", "audit_persist_failed")


async def test_collection_failure_is_not_hidden_by_skip(tmp_path: Path):
    fake = FakeRuntime()
    fake.contract["outputs"] = [{"name": "result", "path": "result.json", "format": "json", "required": False}]
    res = await run_with(fake, "run_skip_bad_output", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "output_invalid")


def test_deadline_adoption_provisional_and_explicit():
    from datetime import datetime, timedelta, timezone
    from agenticstar_platform.workflow.runner import WorkflowRunner as _R
    r = _R.__new__(_R)
    r._agent_deadline = r._execution_deadline = r._collection_deadline = None
    r._execution_explicit = r._collection_explicit = False
    now = datetime.now(timezone.utc)
    ex = now + timedelta(seconds=5)
    r._set_deadlines({"deadlines": {"execution": ex.isoformat(), "collection": None}, "contract": {"limits": {}}})
    assert r._execution_deadline == ex and r._collection_deadline == ex + timedelta(seconds=300) and r._agent_deadline == ex
    coll = ex + timedelta(seconds=305)
    r._set_deadlines({"deadlines": {"execution": ex.isoformat(), "collection": coll.isoformat()}})
    assert r._collection_deadline == coll and r._collection_explicit  # 暫定値は確定値で置き換わる（後ろでも）
    later = coll + timedelta(seconds=100)
    r._set_deadlines({"deadlines": {"execution": ex.isoformat(), "collection": later.isoformat()}})
    assert r._collection_deadline == coll  # 確定値同士は延ばさない
    r2 = _R.__new__(_R)
    r2._agent_deadline = r2._execution_deadline = r2._collection_deadline = None
    r2._execution_explicit = r2._collection_explicit = False
    r2._set_deadlines({"deadlines": {}, "contract": {"limits": {"execution_timeout_seconds": 60}}})
    assert not r2._execution_explicit and abs((r2._execution_deadline - now).total_seconds() - 60) < 2
    r2._set_deadlines({"deadlines": {"execution": ex.isoformat(), "collection": coll.isoformat()}})
    assert r2._execution_deadline == ex and r2._execution_explicit and r2._agent_deadline == ex
    # 実行期限だけが確定値で置き換わったら、そこから導く回収の暫定値も作り直す（古い実行期限に取り残さない）
    r3 = _R.__new__(_R)
    r3._agent_deadline = r3._execution_deadline = r3._collection_deadline = None
    r3._execution_explicit = r3._collection_explicit = False
    r3._set_deadlines({"deadlines": {}, "contract": {"limits": {"execution_timeout_seconds": 60}}})
    provisional_collection = r3._collection_deadline
    ex600 = now + timedelta(seconds=600)
    r3._set_deadlines({"deadlines": {"execution": ex600.isoformat(), "collection": None}, "contract": {"limits": {}}})
    assert r3._execution_deadline == ex600 and r3._execution_explicit and not r3._collection_explicit
    assert r3._collection_deadline == ex600 + timedelta(seconds=300) > provisional_collection
    assert r3._agent_deadline == ex600


async def test_input_format_mismatch_is_rejected(tmp_path: Path):
    fake = FakeRuntime()
    fake.contract["files"][0]["format"] = "json"   # 契約は JSON、manifest は markdown → schema 検証を迂回させない
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "input_integrity")


async def test_transient_500_on_audit_is_retried(tmp_path: Path):
    fake = FakeRuntime(effect_mode="idempotent_write")
    fake.fail_invoked_500_times = 1
    res = await run_with(fake, "run_send", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed")


# ---------------------------------------------------------------------------
# 4. 回収の安全性（AC-07）
# ---------------------------------------------------------------------------
def test_relative_path_and_safe_join_reject_traversal(tmp_path: Path):
    for bad in ("/etc/passwd", "../x", "a/../../b", "a\\b", ""):
        with pytest.raises(OutputCollectionError):
            relative_path(bad)
    (tmp_path / "escape").symlink_to("/etc")
    with pytest.raises(OutputCollectionError):
        safe_join(tmp_path, "escape/hostname")


def _roots(tmp_path: Path):
    for d in ("input", "work", "output"):
        (tmp_path / d).mkdir(exist_ok=True)
    return {d: WorkspaceRoot(tmp_path / d) for d in ("input", "work", "output")}


def test_collect_outputs_rejects_symlink_hardlink_size_and_bad_json(tmp_path: Path):
    roots = _roots(tmp_path)
    out = tmp_path / "output"
    (out / "reply.md").write_text("ok")
    reply = [{"name": "reply", "path": "reply.md", "format": "markdown", "required": True}]
    (out / "leak.md").symlink_to("/etc/hostname")
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "leak", "path": "leak.md", "format": "markdown"}])
    (out / "leak.md").unlink()
    (out / "big.md").write_bytes(b"x" * (20 * 1024 * 1024 + 1))
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "big", "path": "big.md", "format": "text"}])
    (out / "big.md").unlink()
    (out / "other.md").write_text("x")
    os.link(out / "other.md", out / "hl.md")
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "hl", "path": "hl.md", "format": "text"}])
    (out / "r.json").write_text('{"a": 1, "a": 2}')
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "r", "path": "r.json", "format": "json"}])
    (out / "r.json").write_text('{"a": ' + "9" * 1000 + '}')
    with pytest.raises(OutputCollectionError):  # 表現できない巨大数（OverflowError を外へ出さない）
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "r", "path": "r.json", "format": "json",
                                          "schema": {"type": "object", "additionalProperties": False,
                                                     "properties": {"a": {"type": "number"}}}}])
    (out / "r.json").write_text('{"a": "x"}')
    with pytest.raises(OutputCollectionError):  # schema 違反
        collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[],
                        outputs=reply + [{"name": "r", "path": "r.json", "format": "json",
                                          "schema": {"type": "object", "additionalProperties": False,
                                                     "properties": {"a": {"type": "integer"}}}}])
    # 編集対象（source=work）は 1MiB 上限（files に editable 宣言が無い素の source=work でも同じ）
    (tmp_path / "work" / "instructions.md").write_bytes(b"y" * (1024 * 1024 + 1))
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"],
                        files=[{"name": "instructions", "path": "instructions.md", "format": "markdown", "editable": True}],
                        outputs=reply + [EDIT_OUTPUT])
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"], files=[],
                        outputs=reply + [EDIT_OUTPUT])
    # 未編集でも required な work output は実行の output として保存する（任意なら回収しない）
    (tmp_path / "input" / "instructions.md").write_bytes(b"same")
    (tmp_path / "work" / "instructions.md").write_bytes(b"same")
    edit_files = [{"name": "instructions", "path": "instructions.md", "format": "markdown", "editable": True}]
    got = collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"], files=edit_files,
                          outputs=reply + [{**EDIT_OUTPUT, "required": True}])
    assert [c.logical_name for c in got] == ["reply", "instructions_edit"]
    got = collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"], files=edit_files,
                          outputs=reply + [EDIT_OUTPUT])
    assert [c.logical_name for c in got] == ["reply"]
    # 入力 file の schema は同じ work path の編集にだけ適用（output/ の同名ファイルには継承しない）
    (out / "settings.json").write_text('{"free": true}')
    in_files = [{"name": "settings", "path": "settings.json", "format": "json",
                 "schema": {"type": "object", "additionalProperties": False, "properties": {"a": {"type": "integer"}}}}]
    got = collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"], files=in_files,
                          outputs=reply + [{"name": "settings_out", "path": "settings.json", "format": "json"}])
    assert [c.logical_name for c in got] == ["reply", "settings_out"]
    (tmp_path / "work" / "settings.json").write_text('{"free": true}')
    with pytest.raises(OutputCollectionError):
        collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots["input"], files=in_files,
                        outputs=reply + [{"name": "settings_edit", "path": "settings.json", "format": "json", "source": "work"}])
    (out / "settings.json").unlink()
    got = collect_outputs(output_root=roots["output"], work_root=roots["work"], files=[], outputs=reply)
    assert [c.logical_name for c in got] == ["reply"] and got[0].content == b"ok" and (out / "other.md").exists()
    for r in roots.values():
        r.close()


async def test_symlinked_output_and_swapped_root_are_rejected(tmp_path: Path):
    fake = FakeRuntime()
    fake.contract["outputs"].append({"name": "leak", "path": "leak.md", "format": "markdown", "required": False})
    res = await run_with(fake, "run_escape", tmp_path / "a")
    assert res.outcome == "failed" and fake.completion["envelope"]["error_class"] == "OutputCollectionError" and not fake.artifacts
    fake = FakeRuntime()
    res = await run_with(fake, "run_swap_output_root", tmp_path / "b")
    # root fd は Agent 起動前に固定 → 差し替え後の symlink（/etc）ではなく元の output dir から回収される
    assert res.outcome == "completed" and [a["logical_name"] for a in fake.artifacts.values()] == ["reply"]
    assert next(iter(fake.artifacts.values()))["sha256"] == __import__("hashlib").sha256(b"ok\n").hexdigest()


async def test_fifo_output_does_not_block_collection(tmp_path: Path):
    fake = FakeRuntime()
    res = await asyncio.wait_for(run_with(fake, "run_fifo", tmp_path), timeout=30)
    assert res.outcome == "failed" and fake.completion["envelope"]["error_class"] == "OutputCollectionError"


async def test_input_digest_mismatch_is_rejected_before_agent(tmp_path: Path):
    fake = FakeRuntime()
    orig = fake.handle

    def tampered(request):
        r = orig(request)
        if request.url.path.endswith("/content"):
            return type(r)(200, content=b"tampered\n")
        return r
    fake.transport = type(fake.transport)(tampered)
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "input_integrity")
    assert not (tmp_path / "output" / "reply.md").exists()


def test_strict_yaml_and_schema_subset():
    assert parse_yaml_strict(b'{"a": 1}') == {"a": 1}
    assert parse_yaml_strict(b"a: yes\n") == {"a": "yes"}  # YAML 1.1 の bool 変換をしない
    assert parse_yaml_strict(b"d: 2026-09-13\n") == {"d": "2026-09-13"}  # 暗黙の日時変換をしない（文字列のまま）
    # 数値 / bool は YAML 1.2 core（front contract.js parseYamlToJson と同じ）: 60 進 / 下線区切りは文字列、指数は数値、
    # True/FALSE は bool、先頭 0 / 16 進 / 8 進 / 2 進の plain は曖昧な数値として拒否、明示 tag は拒否
    assert parse_yaml_strict(b"a: 1:20\nb: 1e3\nc: 1_000\nd: 1e-7\ne: True\nf: FALSE\ng: 0\nh: 0.5\ni: ~\nj: <<\n") == {
        "a": "1:20", "b": 1000.0, "c": "1_000", "d": 1e-7, "e": True, "f": False, "g": 0, "h": 0.5, "i": None, "j": "<<"}
    assert parse_yaml_strict(b"<<: 1\n") == {"<<": 1}                      # core schema に merge は無い（front と同じ）
    assert parse_yaml_strict(b"%YAML 1.2\n---\na: 1\n") == {"a": 1}
    for bad in (b"a: 1\na: 2\n", b"x: &a 1\ny: *a\n", b"x: &a 1\ny: 2\n", b"d: !!timestamp 2026-09-13\n", b"t: !!python/object:x {}\n",
                b"a: 1\n---\nb: 2\n", b"[" * 3000 + b"]" * 3000, b"a: .inf\n", b"a: 0x1f\n", b"a: 01\n", b"a: 0o7\n", b"a: 0b1\n",
                b"a: !!int 1\n", b"a: !!str x\n", b"a: -01\n", b"%YAML 1.1\n---\na: yes\n", b"%YAML 1.3\n---\na: 1\n",
                b"%TAG !e! tag:x,2000:\n---\na: 1\n"):
        with pytest.raises(SchemaError) as ei:
            parse_yaml_strict(bad)
        assert "python/object" not in str(ei.value)  # 診断に本文の tag / key を写さない
    from agenticstar_platform.workflow.schema import parse_json_strict
    with pytest.raises(SchemaError):
        parse_json_strict(b"[" * 3000 + b"]" * 3000)
    with pytest.raises(SchemaError) as ei:
        parse_json_strict(b'{"secret-key-xyz": 1, "secret-key-xyz": 2}')
    assert "secret-key-xyz" not in str(ei.value)
    with pytest.raises(SchemaError) as ei:
        validate_value({"type": "object", "additionalProperties": False, "properties": {}}, {"secret-key-xyz": 1})
    assert "secret-key-xyz" not in str(ei.value)
    from agenticstar_platform.workflow.files import render_from_parameters
    assert parse_yaml_strict(render_from_parameters("yaml", {"n": 1e-7, "t": "1:20", "b": True})) == {"n": 1e-7, "t": "1:20", "b": True}
    validate_value({"type": "object", "additionalProperties": False, "properties": {"n": {"type": "integer"}}}, {"n": 1.0})
    with pytest.raises(SchemaError):
        validate_value({"type": "object", "additionalProperties": False, "properties": {}}, {"extra": 1})
    with pytest.raises(SchemaError):
        validate_value({"type": "object", "additionalProperties": False, "$ref": "#/x"}, {})


async def test_cleanup_uncertain_without_restart_is_failed_and_effects_unknown(tmp_path: Path, monkeypatch):
    """再起動を伴わない経路: Agent は正常に終わったが、子プロセス群を止め切れなかった (まだ外部 write を出しうる)。
    完遂 (completed) を名乗らず failed/cleanup_uncertain にし、効果は不明 (had = None) にする = front は自動 retry せず人へ回す。
    取消は stopped のまま (既に hold に収束する終端の理由は上書きしない)。"""
    original = WorkflowRunner._terminate_group

    async def leaves_survivors(self, proc):
        await original(self, proc)
        self._cleanup_uncertain = True   # SIGKILL を生き残ったプロセスがいる状況

    monkeypatch.setattr(WorkflowRunner, "_terminate_group", leaves_survivors)
    fake = FakeRuntime()
    res = await run_with(fake, "run_reply", tmp_path / "a")
    env = fake.completion["envelope"]
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("failed", "cleanup_uncertain", None)
    assert env["runner"]["cleanup_uncertain"] is True and env["runner"]["restarted"] is False
    # 観測済みの成功は消さない (had = True のまま)。理由コードで front が hold する
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_send", tmp_path / "b")
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("failed", "cleanup_uncertain", True)


# ---------------------------------------------------------------------------
# 5. outcome 遷移
# ---------------------------------------------------------------------------
def test_decide_outcome_table():
    t = EffectTally()
    kw = dict(agent_error=None, stop_reason=None, outputs_collected=0, required_missing=[], effect_mode="read_only")
    # 観測 0 件でも Agent が正常に戻れば完遂（成否 = Agent が完遂したか）
    assert decide_outcome(tally=t, **kw) == ("completed", "completed", False)
    t.record("tool.invoked", "i1", {"tool": "r", "effect_kind": "read"})
    assert decide_outcome(tally=t, **kw) == ("completed", "completed", False)
    t.record("tool.invoked", "i2", {"tool": "w", "effect_kind": "write"})
    kw["effect_mode"] = "idempotent_write"
    # effect の無い write: outcome は下げない。効果は不明 = had None（front は不成功なら自動 retry しない）
    assert decide_outcome(tally=t, **{**kw, "outputs_collected": 1}) == ("completed", "completed", None)
    assert decide_outcome(tally=t, **{**kw, "agent_error": "RuntimeError"}) == ("failed", "agent_error", None)
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "deadline"}) == ("timeout", "execution_timeout", None)
    t.record("tool.effect", "e2", {"invoked_event_id": "i2", "action_ref": "i2", "status": "ok"})
    assert decide_outcome(tally=t, **{**kw, "outputs_collected": 1}) == ("completed", "completed", True)
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "cancel"}) == ("stopped", "cancelled", True)
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "deadline"}) == ("timeout", "execution_timeout", True)
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "terminal"}) == ("stopped", "terminal_elsewhere", True)
    # runner 自身の停止（Pod 停止 signal）= 実行環境の異常 failed/runner_stopped。例外より優先。観測済みの成功は消さない
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "stopped"}) == ("failed", "runner_stopped", True)
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "stopped",
                                      "agent_error": "RuntimeError"}) == ("failed", "runner_stopped", True)
    assert decide_outcome(tally=t, **{**kw, "agent_error": "RuntimeError"}) == ("failed", "agent_error", True)
    # 成功の後の拒否は denied（had は保つ）、必須 output 欠落より優先
    t.record("tool.denied", "d0", {"tool": "w", "reason_code": "policy_denied"})
    assert decide_outcome(tally=t, **{**kw, "required_missing": ["reply"]}) == ("denied", "policy_denied", True)
    t.denials.clear()
    # write の失敗は成否にしない: 成功と混在しても、失敗だけでも、Agent が正常に戻れば完遂
    t.record("tool.invoked", "i3", {"tool": "w", "effect_kind": "send"})
    t.record("tool.effect", "e3", {"invoked_event_id": "i3", "status": "failed"})
    assert decide_outcome(tally=t, **{**kw, "outputs_collected": 1}) == ("completed", "completed", True)
    t4 = EffectTally()
    t4.record("tool.invoked", "i4", {"tool": "w", "effect_kind": "send"})
    t4.record("tool.effect", "e4", {"invoked_event_id": "i4", "status": "failed"})
    assert decide_outcome(tally=t4, **{**kw, "outputs_collected": 1}) == ("completed", "completed", False)
    assert decide_outcome(tally=t4, **{**kw, "agent_error": "RuntimeError"}) == ("failed", "agent_error", False)  # 効果なしと確定
    # journal の往復で観測が消えない
    t5 = EffectTally.from_dict(json.loads(json.dumps(t.to_dict())))
    assert t5.counts() == t.counts() and t5.mutating_success == 1
    t2 = EffectTally()
    t2.record("tool.denied", "d1", {"tool": "w", "reason_code": "policy_denied"})
    assert decide_outcome(tally=t2, **{**kw, "outputs_collected": 1}) == ("denied", "policy_denied", False)
    # runner の停止 / 他所終端 / 再起動・cleanup 未完は、成功を観測していなければ効果不明（None）
    t8 = EffectTally()
    t8.record("tool.invoked", "i8", {"tool": "r", "effect_kind": "read"})
    assert decide_outcome(tally=t8, **{**kw, "stop_reason": "stopped"}) == ("failed", "runner_stopped", None)
    assert decide_outcome(tally=t8, **{**kw, "stop_reason": "terminal"}) == ("stopped", "terminal_elsewhere", None)
    assert decide_outcome(tally=t8, **{**kw, "effects_uncertain": True, "agent_error": "RuntimeError"}) == ("failed", "agent_error", None)
    assert decide_outcome(tally=t8, **{**kw, "stop_reason": "cancel"}) == ("stopped", "cancelled", False)
    t9 = EffectTally()
    t9.persist_failures = 1
    assert decide_outcome(tally=t9, **kw) == ("failed", "audit_persist_failed", None)  # 監査を保存できない = 効果不明
    t3 = EffectTally()
    t3.skip_reason = "nothing_to_do"
    assert decide_outcome(tally=t3, **kw) == ("skipped", "nothing_to_do", False)
    t3.skip_reason = "policy_unavailable"
    assert decide_outcome(tally=t3, **{**kw, "required_missing": ["reply"]}) == ("skipped", "policy_unavailable", False)
    # 外部行為の前の skip (policy_unavailable) は、write を 1 件でも呼んだ後には名乗れない (front が認定に関わらず再実行するため)
    t10 = EffectTally()
    t10.record("tool.invoked", "i10", {"tool": "w", "effect_kind": "send"})
    t10.skip_reason = "policy_unavailable"
    assert decide_outcome(tally=t10, **kw) == ("failed", "skip_after_effect", None)
    t10.record("tool.effect", "e10", {"invoked_event_id": "i10", "status": "failed"})
    assert decide_outcome(tally=t10, **kw) == ("failed", "skip_after_effect", False)
    # write が成功していても同じ (成功 1 件 + effect 未記録 1 件 + policy_unavailable → 完遂にも skipped にもしない。Codex 2 巡目)
    t11 = EffectTally()
    t11.record("tool.invoked", "a", {"tool": "w", "effect_kind": "send"})
    t11.record("tool.effect", "ea", {"invoked_event_id": "a", "status": "ok"})
    t11.record("tool.invoked", "b", {"tool": "w", "effect_kind": "send"})
    t11.skip_reason = "policy_unavailable"
    assert decide_outcome(tally=t11, **{**kw, "outputs_collected": 1}) == ("failed", "skip_after_effect", True)
    assert decide_outcome(tally=t11, **{**kw, "required_missing": ["reply"]}) == ("failed", "skip_after_effect", True)
    t10.skip_reason = "no_target"   # 再実行を起こさない skip はそのまま (次工程へ進むだけ)
    assert decide_outcome(tally=t10, **kw) == ("skipped", "no_target", False)
    # 観測した成功は後の報告で消えない（sticky）。帰属不明の effect は効果不明（None）
    t6 = EffectTally()
    t6.record("tool.invoked", "i6", {"tool": "w", "effect_kind": "send"})
    t6.record("tool.effect", "e6a", {"invoked_event_id": "i6", "status": "ok"})
    t6.record("tool.effect", "e6b", {"invoked_event_id": "i6", "status": "failed"})
    assert decide_outcome(tally=t6, **{**kw, "outputs_collected": 1}) == ("completed", "completed", True)
    assert t6.counts()["effect_conflicts"] == 1
    t7 = EffectTally()
    t7.record("tool.invoked", "i7", {"tool": "r", "effect_kind": "read"})
    t7.record("tool.effect", "e7", {"invoked_event_id": "nope", "status": "unknown"})
    assert decide_outcome(tally=t7, **kw) == ("completed", "completed", None)
    assert t7.counts()["orphan_effects"] == 1
    env = build_envelope(outcome="completed", reason="completed", had_mutating_success=True, tally=t)
    assert env["version"] == 2 and env["counts"]["mutating_success"] == 1 and env["tools"][1]["status"] == "ok"
    assert "gate_requested" not in env and "verification" not in env and env["runner"] is None
    assert build_envelope(outcome="failed", reason="runner_stopped", had_mutating_success=None, tally=t)["had_mutating_success"] is None
    assert OUTCOMES == ("completed", "incomplete", "failed", "timeout", "stopped", "denied", "skipped")


# ---------------------------------------------------------------------------
# 6. 取消 / 期限 / completion の再送・409 / 再起動
# ---------------------------------------------------------------------------
async def test_cancel_stops_agent_and_keeps_effects(tmp_path: Path):
    fake = FakeRuntime()

    async def cancel_soon():
        await asyncio.sleep(1.0)
        fake.cancel_requested_at = "2026-09-13T00:00:00Z"
    task = asyncio.create_task(cancel_soon())
    res = await run_with(fake, "run_slow", tmp_path, cancel_poll_seconds=0.2)
    await task
    assert (res.outcome, res.outcome_reason_code) == ("stopped", "cancelled") and res.completion_saved
    assert (tmp_path / "output" / "reply.md").exists() and fake.artifacts


async def test_deadline_stops_agent_as_timeout(tmp_path: Path):
    fake = FakeRuntime(deadline_seconds=17)
    res = await run_with(fake, "run_slow", tmp_path, cancel_poll_seconds=0.2)
    assert (res.outcome, res.outcome_reason_code) == ("timeout", "execution_timeout") and res.completion_saved


async def test_completion_resend_and_terminal_409(tmp_path: Path):
    fake = FakeRuntime()
    fake.fail_completion_times = 2
    res = await run_with(fake, "run_reply", tmp_path)
    assert res.completion_saved and fake.calls.count(f"POST /api/mp/runtime/v1/executions/{EXECUTION_ID}/completion") == 3
    fake2 = FakeRuntime()
    fake2.state = "terminal"
    res = await run_with(fake2, "run_reply", tmp_path / "b")
    assert res.already_terminal and res.exit_code == 0 and not (tmp_path / "b" / "output" / "reply.md").exists()


async def test_completion_unsavable_exits_2(tmp_path: Path):
    """completion を保存できなければ exit 2（terminal 未保存）。executor は非0 終了を `failed/agent_exit_nonzero`
    （効果不明）で終端し front が hold する（00 §7）。SDK は終了コードで retry / hold を制御しない。"""
    fake = FakeRuntime()
    fake.fail_completion_times = 99
    res = await arun(f"{FIX}:run_reply", env=env_for(), workspace=str(tmp_path), transport=fake.transport)
    assert (res.outcome, res.outcome_reason_code) == ("completed", "completed")
    assert res.exit_code == 2 and not res.completion_saved and fake.completion is None
    # 起動 fence の監査が保存できない（所有権を証明できていない）→ completion を送らず exit 2
    fake2 = FakeRuntime()
    fake2.fail_audit_types = {"context.manifest"}
    res2 = await arun(f"{FIX}:run_reply", env=env_for(), workspace=str(tmp_path / "nofence"),
                      transport=fake2.transport)
    assert res2.exit_code == 2 and not res2.completion_saved and fake2.completion is None


async def test_restart_does_not_rerun_agent(tmp_path: Path):
    # completion 構築前に落ちた: started fence だけ残る → Agent を再実行せず効果不明で終端
    fake = FakeRuntime(effect_mode="idempotent_write")
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / ".aster_workflow_state.json").write_text(json.dumps(
        {"started": "2026-09-13T00:00:00+00:00", "fence_owner": "2026-09-13T00:00:00+00:00"}))
    res = await run_with(fake, "run_send", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "runner_restarted")
    assert not [e for e in fake.audit_events if e["event_type"] == "tool.invoked"] and not (tmp_path / "output" / "reply.md").exists()
    # journal した観測（成功した write）は再起動後も 0 に戻らない
    fake = FakeRuntime(effect_mode="idempotent_write")
    ws = tmp_path / "j"
    ws.mkdir()
    t = EffectTally()
    t.record("tool.invoked", "i1", {"tool": "mock_send", "effect_kind": "send"})
    t.record("tool.effect", "e1", {"invoked_event_id": "i1", "status": "ok"})
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"started": "x", "fence_owner": "x", "tally": t.to_dict()}))
    res = await run_with(fake, "run_send", ws)
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success) == ("failed", "runner_restarted", True)
    assert fake.completion["envelope"]["counts"]["mutating_success"] == 1
    # completion 構築後に落ちた: 保存済み payload を同じ ID で再送
    fake = FakeRuntime()
    ws = tmp_path / "b"
    ws.mkdir()
    payload = build_envelope(outcome="completed", reason="completed", had_mutating_success=False, tally=EffectTally())
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"started": "x", "fence_owner": "x",
                                                                "completion_id": "11111111-2222-4333-8444-555555555555",
                                                                "completion": {"envelope": payload, "output_artifact_ids": []}}))
    fake.contract["outputs"] = []
    res = await run_with(fake, "run_send", ws)
    assert res.completion_saved and fake.completion["completion_id"] == "11111111-2222-4333-8444-555555555555"
    assert not [e for e in fake.audit_events if e["event_type"] != "context.manifest"]
    # 回収 root を開けない状態（output/ が symlink に差し替えられた / workspace が壊れた）で再起動 →
    # 回収せず例外のまま非0 終了（executor が `failed/agent_exit_nonzero` で hold）。artifact も completion も作らない
    fake = FakeRuntime(effect_mode="idempotent_write")
    ws = tmp_path / "broken"
    ws.mkdir()
    (tmp_path / "elsewhere").mkdir()
    (ws / "output").symlink_to(tmp_path / "elsewhere", target_is_directory=True)
    t = EffectTally()
    t.record("tool.invoked", "i1", {"tool": "mock_send", "effect_kind": "send"})
    t.record("tool.effect", "e1", {"invoked_event_id": "i1", "status": "ok"})
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"started": "x", "fence_owner": "x", "tally": t.to_dict()}))
    with pytest.raises(OutputCollectionError):
        await run_with(fake, "run_send", ws)
    assert fake.completion is None and not fake.artifacts
    # started はあるが fence_owner が無い state（本番では作られない = 所有権未証明）→ completion を送らない
    fake = FakeRuntime()
    ws = tmp_path / "nofence"
    ws.mkdir()
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"started": "x"}))
    res = await run_with(fake, "run_send", ws)
    assert res.completion_saved is False and fake.completion is None and res.exit_code == 2


async def test_recovery_stops_previous_agent_group_before_collection(tmp_path: Path):
    # runner だけが再起動し、前の Agent プロセスグループが同じ PID namespace に残っている → 回収前に止める
    import subprocess
    import time as _time
    from agenticstar_platform.workflow.runner import WorkflowRunner as _R
    prev = subprocess.Popen(["sleep", "300"], start_new_session=True)  # noqa: S603,S607
    try:
        ticks = _R._start_ticks(prev.pid)
        fake = FakeRuntime(effect_mode="idempotent_write")
        tmp_path.mkdir(exist_ok=True)
        (tmp_path / ".aster_workflow_state.json").write_text(json.dumps(
            {"started": "x", "fence_owner": "x",
             "agent_process": {"pgid": prev.pid, "start_ticks": ticks}}))
        res = await run_with(fake, "run_send", tmp_path, child_grace_seconds=1.0)
        assert (res.outcome, res.outcome_reason_code) == ("failed", "runner_restarted")
        for _ in range(50):
            if prev.poll() is not None:
                break
            _time.sleep(0.1)
        assert prev.poll() is not None
        # 起動時刻が違う（PID 再利用: この runner の起動後に始まった別プロセス）なら触らない
        other = subprocess.Popen(["sleep", "300"], start_new_session=True)  # noqa: S603,S607
        try:
            (tmp_path / "k").mkdir()
            (tmp_path / "k" / ".aster_workflow_state.json").write_text(json.dumps(
                {"started": "x", "fence_owner": "x",
                 "agent_process": {"pgid": other.pid, "start_ticks": _R._start_ticks(other.pid) - 1,
}}))
            await run_with(FakeRuntime(effect_mode="idempotent_write"), "run_send", tmp_path / "k", child_grace_seconds=1.0)
            assert other.poll() is None
        finally:
            other.kill()
            other.wait()
    finally:
        if prev.poll() is None:
            prev.kill()
        prev.wait()
    # リーダーが死んで子孫だけ残った session: 数値の session id は再利用されるので、無関係な session と区別できない
    # （起動時刻の区間でも区別できない）→ **kill せず** cleanup_uncertain（回収もしない）
    sh = subprocess.Popen(["sh", "-c", "sleep 300 & sleep 300 & wait"], start_new_session=True)  # noqa: S603,S607
    _time.sleep(0.3)
    kids = [pid for pid, _t, _s in _R._group_members(sh.pid) if pid != sh.pid]
    assert kids
    sh.kill()
    sh.wait()
    try:
        (tmp_path / "l").mkdir()
        (tmp_path / "l" / "elsewhere").mkdir()
        (tmp_path / "l" / "output").symlink_to(tmp_path / "l" / "elsewhere", target_is_directory=True)  # 開けない root
        (tmp_path / "l" / ".aster_workflow_state.json").write_text(json.dumps(
            {"started": "x", "fence_owner": "x",
             "agent_process": {"pgid": sh.pid, "start_ticks": 12345}}))
        fake_l = FakeRuntime(effect_mode="idempotent_write")
        res = await run_with(fake_l, "run_send", tmp_path / "l", child_grace_seconds=1.0)
        assert (res.outcome, res.outcome_reason_code) == ("failed", "runner_restarted")
        assert fake_l.completion["envelope"]["runner"]["cleanup_uncertain"] is True and not fake_l.artifacts
        assert fake_l.completion["envelope"]["error_class"] is None   # 回収しないので root を開きにも行かない
        assert all(_R._pid_alive(k) for k in kids)   # 所有を立証できないプロセスは殺さない
    finally:
        for k in kids:
            try:
                os.kill(k, 9)
            except ProcessLookupError:
                pass


async def test_artifact_upload_retries_then_succeeds(tmp_path: Path):
    fake = FakeRuntime()
    fake.fail_upload_times = 1
    res = await run_with(fake, "run_reply", tmp_path)
    assert res.outcome == "completed" and len(fake.artifacts) == 1


# ---------------------------------------------------------------------------
# 7. プロセス境界 / IPC / 空環境 / 旧 runner
# ---------------------------------------------------------------------------
async def test_descendant_processes_are_stopped_before_collection(tmp_path: Path):
    fake = FakeRuntime()
    fake.contract["outputs"].append({"name": "pid", "path": "pid.txt", "format": "text", "required": False})
    res = await run_with(fake, "run_orphan_child", tmp_path, child_grace_seconds=2.0)
    assert res.outcome == "completed"
    pid = int((tmp_path / "output" / "pid.txt").read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


async def test_noisy_stdout_does_not_break_control_channel(tmp_path: Path):
    fake = FakeRuntime()
    res = await asyncio.wait_for(run_with(fake, "run_noisy_stdout", tmp_path), timeout=60)
    assert res.outcome == "completed"


def test_legacy_runner_api_unchanged():
    from agenticstar_platform import runner as legacy
    assert callable(legacy.run_marketplace_agent) and callable(legacy.arun_marketplace_agent)
    assert legacy.REQUIRED_IDENTITY_ENV == ("EXECUTION_ID", "CONVERSATION_ID", "USER_ID", "MESSAGE_ID")


def test_workflow_imports_without_autonomous_or_db_extras():
    import subprocess
    code = ("import sys; import agenticstar_platform.workflow as w; "
            "assert 'asyncpg' not in sys.modules and 'src' not in sys.modules; print(w.PROTOCOL)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True,
                         env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[2])})
    assert out.stdout.strip() == "mp-workflow/1"


# ---------------------------------------------------------------------------
# 8. 障害時の契約（00 §7）: completion を送れない障害は例外のまま非0 で終わる。SDK は終了コードを保証しない
#    （terminal 未保存の非0 終了 = executor `failed/agent_exit_nonzero` = front hold、exit 0 + 未保存 = completion_missing = hold）
# ---------------------------------------------------------------------------
def _pipe_fd_count() -> int:
    n = 0
    for fd in os.listdir("/proc/self/fd"):
        try:
            if os.readlink(f"/proc/self/fd/{fd}").startswith("pipe:"):
                n += 1
        except OSError:
            continue
    return n


async def test_agent_spawn_failure_completes_and_leaks_no_fd(tmp_path: Path):
    """image に interpreter が無い（spawn が ENOENT）: Agent は起動していないので failed/agent_error を送り、制御 pipe の fd も残さない。"""
    fake = FakeRuntime()
    has_proc = os.path.isdir("/proc/self/fd")
    before = _pipe_fd_count() if has_proc else 0
    res = await run_with(fake, "run_reply", tmp_path, python=str(tmp_path / "no-such-python"))
    assert (res.outcome, res.outcome_reason_code, res.exit_code) == ("failed", "agent_error", 0)
    assert res.completion_saved and fake.completion["envelope"]["error_class"] == "AgentSpawnFailed"
    if has_proc:
        assert _pipe_fd_count() == before


async def test_cancel_during_agent_startup_cleans_up_fds_and_the_child(tmp_path: Path, monkeypatch):
    """子プロセスの初期化中（connect_read_pipe）に cancel が飛んでも、掴んだ pipe fd を閉じ、起動途中の子を止めてから
    例外を再送出する（completion は送らない）。"""
    import asyncio as _asyncio
    fake = FakeRuntime()
    has_proc = os.path.isdir("/proc/self/fd")
    before = _pipe_fd_count() if has_proc else 0
    pids: list[int] = []

    async def cancelled_connect(self, *a, **kw):
        pids.append(json.loads((tmp_path / ".aster_workflow_state.json").read_text())["agent_process"]["pgid"])
        raise _asyncio.CancelledError()
    monkeypatch.setattr(type(_asyncio.get_running_loop()), "connect_read_pipe", cancelled_connect)
    with pytest.raises(_asyncio.CancelledError):
        await run_with(fake, "run_reply", tmp_path)
    monkeypatch.undo()
    assert fake.completion is None and pids
    for _ in range(50):
        if not WorkflowRunner._group_members(pids[0]):
            break
        await _asyncio.sleep(0.1)
    assert not WorkflowRunner._group_members(pids[0])
    if has_proc:
        assert _pipe_fd_count() == before


async def test_failures_before_the_agent_starts_propagate_without_completion(tmp_path: Path, monkeypatch):
    """入力の展開 / artifact 取得 / workspace の用意 / 起動 fence の永続化に失敗したら例外のまま終わる（completion は送らない、
    Agent は起動しない = 効果なし）。executor は非0 終了を効果不明として hold にする。"""
    ws = tmp_path / "stage"
    (ws / "input" / "instructions.md").mkdir(parents=True)   # os.replace が IsADirectoryError
    fake = FakeRuntime()
    with pytest.raises(OSError):
        await run_with(fake, "run_reply", ws)
    assert fake.completion is None

    fake2 = FakeRuntime()
    fake2.fail_download_times = 99
    with pytest.raises(Exception) as caught:
        await run_with(fake2, "run_reply", tmp_path / "dl")
    assert "RuntimeApiError" in type(caught.value).__name__ and fake2.completion is None

    ws3 = tmp_path / "brokenws"
    ws3.mkdir()
    (ws3 / "input").write_text("not a directory")            # mkdir が FileExistsError
    (ws3 / ".aster_workflow_state.json").write_text(json.dumps({"fence_owner": "x"}))
    fake3 = FakeRuntime()
    with pytest.raises(OSError):
        await run_with(fake3, "run_reply", ws3)
    assert fake3.completion is None

    # 起動 fence を durable に書けないなら Agent を起動しない（再起動で外部 write を繰り返さない）
    from agenticstar_platform.workflow import runner as runner_mod
    orig = runner_mod._State.set

    def failing_set(self, key, value):
        if key == "started":
            raise OSError("disk full")
        return orig(self, key, value)
    monkeypatch.setattr(runner_mod._State, "set", failing_set)
    fake4 = FakeRuntime(effect_mode="idempotent_write")
    with pytest.raises(OSError):
        await run_with(fake4, "run_send", tmp_path / "fence")
    assert fake4.completion is None
    assert not [e for e in fake4.audit_events if e["event_type"].startswith("tool.")]   # Agent は動いていない


async def test_unexpected_failure_propagates_without_completion(tmp_path: Path, monkeypatch):
    """想定外の例外（所有権の前後どちらでも）は completion を送らずそのまま外へ出す。所有権後なら fence_owner は state に
    残っており、再起動時に Agent を再実行しない（started）。"""
    from agenticstar_platform.workflow import runner as runner_mod

    async def boom(self, *a, **kw):
        raise RuntimeError("unexpected")
    monkeypatch.setattr(runner_mod.WorkflowRunner, "_finish", boom)
    fake = FakeRuntime(effect_mode="idempotent_write")
    with pytest.raises(RuntimeError):
        await run_with(fake, "run_send", tmp_path)
    assert fake.completion is None
    state = json.loads((tmp_path / ".aster_workflow_state.json").read_text())
    assert state.get("fence_owner") and state.get("started")
    monkeypatch.undo()

    def bad_manifest(self, ctx):
        raise RuntimeError("before ownership")
    monkeypatch.setattr(runner_mod.WorkflowRunner, "_manifest", bad_manifest)
    fake2 = FakeRuntime()
    with pytest.raises(RuntimeError):
        await run_with(fake2, "run_reply", tmp_path / "u")
    assert fake2.completion is None


def test_read_error_is_normalized_to_collection_failure(tmp_path: Path, monkeypatch):
    """回収中の読み出し I/O エラー（EIO）も OutputCollectionError に正規化する = runner は failed/output_invalid を送れる。"""
    root = WorkspaceRoot(tmp_path)
    target = tmp_path / "reply.md"
    target.write_bytes(b"x" * 32)
    ino = target.stat().st_ino
    real_read = os.read

    def flaky_read(fd, n):
        if os.fstat(fd).st_ino == ino:
            raise OSError(5, "Input/output error")
        return real_read(fd, n)
    monkeypatch.setattr(os, "read", flaky_read)
    try:
        with pytest.raises(OutputCollectionError):
            root.read_regular("reply.md", 1024)
    finally:
        monkeypatch.undo()
        root.close()


async def test_restart_resend_needs_no_state_writes(tmp_path: Path, monkeypatch):
    """再起動後の再送: 保存済み payload と同じ内容なら state を書き直さない = state が一切書けなくてもそのまま送れる。"""
    from agenticstar_platform.workflow import runner as runner_mod
    tally = EffectTally()
    tally.record("tool.invoked", "i1", {"tool": "mock_send", "effect_kind": "send"})
    tally.record("tool.effect", "e1", {"invoked_event_id": "i1", "status": "ok"})
    envelope = build_envelope(outcome="failed", reason="runner_restarted", had_mutating_success=True, tally=tally,
                              error_class=None, runner={"stop_reason": None})
    ws = tmp_path / "resend"
    ws.mkdir()
    (ws / ".aster_workflow_state.json").write_text(json.dumps(
        {"started": "x", "fence_owner": "x", "completion_id": "11111111-2222-3333-4444-555555555555",
         "completion": {"envelope": envelope, "output_artifact_ids": []}}))

    def failing_save(self):
        raise OSError("read-only file system")
    monkeypatch.setattr(runner_mod._State, "save", failing_save)
    fake = FakeRuntime(effect_mode="idempotent_write")
    res = await run_with(fake, "run_reply", ws)
    assert (res.outcome, res.completion_saved, res.exit_code) == ("failed", True, 0)
    assert fake.completion["completion_id"] == "11111111-2222-3333-4444-555555555555"
    assert fake.completion["envelope"]["counts"]["mutating_success"] == 1


async def test_manifest_audit_failure_after_ownership_holds(tmp_path: Path):
    """所有権を証明済み（前回 manifest 保存後の再起動）で監査が保存できない場合は failed/audit_persist_failed を送る
    （Agent は起動していないので回収もしない）。"""
    ws = tmp_path / "auditdown"
    ws.mkdir()
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"fence_owner": "x"}))
    fake = FakeRuntime()
    fake.fail_audit_types = {"context.manifest"}
    res = await run_with(fake, "run_reply", ws)
    assert (res.outcome, res.outcome_reason_code, res.exit_code) == ("failed", "audit_persist_failed", 0)
    assert res.completion_saved and fake.completion["envelope"]["counts"]["audit_persist_failures"] == 1
    assert not [e for e in fake.audit_events if e["event_type"].startswith("tool.")] and not fake.artifacts


async def test_unreadable_completion_response_is_still_saved(tmp_path: Path):
    """completion の 2xx 応答が JSON でなくても「保存された」扱い（送り直しで別 envelope にしない）。"""
    fake = FakeRuntime()
    fake.completion_body_not_json = True
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code, res.completion_saved, res.exit_code) == ("completed", "completed", True, 0)
    assert fake.completion["envelope"]["outcome"] == "completed"


async def test_unreadable_state_file_raises_before_any_request(tmp_path: Path):
    """state を読めない（ディレクトリに差し替えられた / EIO）: 所有権も保存済み payload も分からないので何も送らず例外。"""
    (tmp_path / ".aster_workflow_state.json").mkdir(parents=True)
    fake = FakeRuntime()
    with pytest.raises(OSError):
        await run_with(fake, "run_reply", tmp_path)
    assert fake.completion is None and fake.calls == []    # /context も叩かない（state を読むのが先）


async def test_context_contract_violation_raises_even_after_ownership(tmp_path: Path):
    """/context が契約外（protocol 不一致）なら所有権の有無に関わらず WorkflowConfigError（completion は送らない）。"""
    ws = tmp_path / "owned"
    ws.mkdir()
    (ws / ".aster_workflow_state.json").write_text(json.dumps({"fence_owner": "x"}))
    fake = FakeRuntime()
    fake.context_protocol_override = "mp-workflow/2"
    with pytest.raises(WorkflowConfigError):
        await run_with(fake, "run_reply", ws)
    assert fake.completion is None and not [e for e in fake.audit_events if e["event_type"] != "context.manifest"]


async def test_cancel_stops_the_agent_and_closes_the_collection_roots(tmp_path: Path, monkeypatch):
    """task.cancel()（Pod 停止の cancel）は例外のまま外へ出る（completion は送らない = executor が hold）。開いた回収 root
    （directory fd）は必ず閉じ、Agent の子プロセスも残さない。"""
    from agenticstar_platform.workflow import runner as runner_mod
    opened: list[int] = []
    closed: list[int] = []
    open_roots = runner_mod.WorkflowRunner._open_roots      # staticmethod
    close_root = runner_mod.WorkspaceRoot.close

    def open_spy(*dirs):
        roots = open_roots(*dirs)
        opened.extend(id(r) for r in roots.values())
        return roots

    def close_spy(self):
        closed.append(id(self))
        close_root(self)
    monkeypatch.setattr(runner_mod.WorkflowRunner, "_open_roots", staticmethod(open_spy))
    monkeypatch.setattr(runner_mod.WorkspaceRoot, "close", close_spy)
    fake = FakeRuntime(effect_mode="idempotent_write")
    task = asyncio.ensure_future(run_with(fake, "run_send_then_wait", tmp_path, child_grace_seconds=2.0))
    for _ in range(500):
        await asyncio.sleep(0.02)
        if any(e["event_type"] == "tool.effect" for e in fake.audit_events):
            break
    else:
        task.cancel()
        raise AssertionError("agent did not reach the observed effect")
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert fake.completion is None and len(opened) == 3 and set(opened) <= set(closed)
    pgid = json.loads((tmp_path / ".aster_workflow_state.json").read_text())["agent_process"]["pgid"]
    for _ in range(50):
        if not runner_mod.WorkflowRunner._group_members(pgid):
            break
        await asyncio.sleep(0.1)
    assert not runner_mod.WorkflowRunner._group_members(pgid)   # 子プロセス群は止まっている


async def test_redirect_is_not_a_saved_completion(tmp_path: Path):
    """ingress / SSO が 302 + HTML を返した応答を「front が保存した」と誤認しない（front は redirect を返さない）→ exit 2。"""
    fake = FakeRuntime()
    fake.completion_redirect = True
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.completion_saved, res.already_terminal, res.exit_code) == ("completed", False, False, 2)
    assert fake.completion is None and fake.state == "running"
    fake2 = FakeRuntime()
    fake2.fail_context = (302, "")
    with pytest.raises(Exception) as caught:
        await run_with(fake2, "run_reply", tmp_path / "redirect")
    assert "302" in str(caught.value) and fake2.completion is None


async def test_client_close_failure_does_not_clobber_the_result(tmp_path: Path, monkeypatch):
    """後片付け（transport の aclose）の失敗で、保存済み completion の戻り値 / 終了コードを壊さない。"""
    from agenticstar_platform.workflow.runtime_client import RuntimeClient

    async def broken_close(self):
        raise OSError("transport is already gone")
    monkeypatch.setattr(RuntimeClient, "aclose", broken_close)
    fake = FakeRuntime()
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.completion_saved, res.exit_code) == ("completed", True, 0)


async def test_unretryable_send_failure_exits_2(tmp_path: Path):
    """送信経路が再送対象外の例外（応答本文の decode 失敗 等）で落ちたら terminal 未保存 = exit 2。"""
    fake = FakeRuntime()
    fake.completion_raises = httpx.DecodingError("corrupt response body")
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.exit_code, res.completion_saved, res.already_terminal) == (2, False, False)
    assert fake.completion is None and json.loads((tmp_path / ".aster_workflow_state.json").read_text()).get("fence_owner")


# ---------------------------------------------------------------------------
# 9. 同期入口 run() と協調停止（SIGTERM）
# ---------------------------------------------------------------------------
def test_config_error_exits_3(tmp_path: Path):
    """設定不正は Agent を呼ばずに終了コード 3（exit_process=False なら WorkflowConfigError）。"""
    bad = {**env_for(), "ASTER_RUNTIME_PROTOCOL": "mp-workflow/2", "ASTER_WORKSPACE": str(tmp_path)}
    with pytest.raises(SystemExit) as exc:
        sync_run(f"{FIX}:run_reply", env=bad, workspace=str(tmp_path))
    assert exc.value.code == 3
    with pytest.raises(WorkflowConfigError):
        sync_run(f"{FIX}:run_reply", env=bad, workspace=str(tmp_path), exit_process=False)


async def test_stop_requested_before_ownership_does_not_start_the_agent(tmp_path: Path):
    """停止要求を **所有権を取る前** に受理したら、fence を取らず Agent も起動せず、completion も送らずに exit 2
    （効果は 1 つも無いので executor の照合で収束させてよい）。"""
    fake = FakeRuntime()
    runner = WorkflowRunner(entrypoint=f"{FIX}:run_send", env=env_for(), workspace=str(tmp_path), transport=fake.transport)
    runner.request_stop()
    res = await runner.run()
    assert (res.exit_code, res.outcome, res.completion_saved) == (2, None, False)
    assert fake.completion is None and fake.audit_events == []      # 起動 fence（context.manifest）を取っていない


async def test_sigterm_while_the_agent_runs_completes_failed_runner_stopped(tmp_path: Path):
    """SIGTERM（Pod 停止）は例外にせず停止理由 `stopped` へ変換し、子プロセス群の停止 → 回収 → `failed/runner_stopped` の
    completion まで走って 0 で終わる（front は runner の停止理由を効果不明として人へ回す = 効果を出したかもしれない実行を自動再実行しない）。"""
    fake = FakeRuntime(effect_mode="idempotent_write")
    runner = WorkflowRunner(entrypoint=f"{FIX}:run_send_then_wait", env=env_for(), workspace=str(tmp_path),
                            transport=fake.transport, cancel_poll_seconds=0.3, child_grace_seconds=3.0, stop_on_sigterm=True)
    task = asyncio.ensure_future(runner.run())
    for _ in range(500):
        await asyncio.sleep(0.02)
        if any(e["event_type"] == "tool.effect" for e in fake.audit_events):
            break
    else:
        task.cancel()
        raise AssertionError("agent did not reach the observed effect")
    os.kill(os.getpid(), signal.SIGTERM)   # 本物の signal を自プロセスへ（loop の handler が停止要求を記録する）
    res = await asyncio.wait_for(task, timeout=60)
    assert (res.outcome, res.outcome_reason_code, res.had_mutating_success, res.exit_code) == ("failed", "runner_stopped", True, 0)
    env = fake.completion["envelope"]
    assert env["runner"]["stop_reason"] == "stopped" and env["counts"]["mutating_success"] == 1
    assert asyncio.get_running_loop().remove_signal_handler(signal.SIGTERM) is False   # handler は外されている


async def test_connection_token_refresh_through_runner(tmp_path: Path):
    """executer-marketplace #55: Agent は context.connection_token で接続 token を取り直せる (期限まで余裕があれば再利用)。"""
    fake = FakeRuntime()
    res = await run_with(fake, "run_connection_token", tmp_path)
    assert res.exit_code == 0 and res.completion_saved
    out = (tmp_path / "output" / "reply.md").read_text()
    assert "first=tok-1 second=tok-1 type=Bearer unbound=WorkflowError" in out
    assert fake.connection_token_calls == ["gitlab", "slack"], "2 回目の gitlab は期限まで余裕があるので取りに行かない"


async def test_connection_token_is_refetched_when_expiring(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_connection_token_expiring", tmp_path)
    assert res.exit_code == 0
    assert fake.connection_token_calls == ["gitlab", "gitlab"], "期限まで min_ttl を切っていれば毎回取り直す"


def test_token_expiring_rules():
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.context import _token_expiring

    now = datetime.now(timezone.utc)
    assert _token_expiring(None, 300) is False                       # 期限なし (PAT 等)
    assert _token_expiring((now + timedelta(hours=1)).isoformat(), 300) is False
    assert _token_expiring((now + timedelta(seconds=60)).isoformat(), 300) is True
    assert _token_expiring("not-a-date", 300) is True                # 読めない値は取り直す
    assert _token_expiring((now + timedelta(hours=1)).replace(tzinfo=None).isoformat(), 300) is False  # tz 無しは UTC


class _FakeIpc:
    def __init__(self, replies):
        self.replies, self.ops = list(replies), []

    async def call(self, op, **payload):
        self.ops.append(op)
        return self.replies.pop(0)


def _context(ipc):
    from agenticstar_platform.workflow.context import WorkflowContext

    spec = {k: "x" for k in ("execution_id", "project_id", "run_id", "agent_id", "marketplace_agent_id",
                             "root_execution_id", "entry_ref", "operation_key", "effect_mode")}
    spec.update({"attempt": 1, "input_dir": "/tmp", "work_dir": "/tmp", "output_dir": "/tmp"})
    return WorkflowContext(spec, ipc)


async def test_cached_connection_token_is_not_returned_after_cancel():
    """手元の token を返す時も取消 / 期限を確かめる (Codex: キャッシュ命中で停止確認を飛ばさない)。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp},
                    {"stop_reason": "cancel"}])
    ctx = _context(ipc)
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t1"
    ctx._last_check = 0.0  # 前回の確認から max_age を過ぎた
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")
    assert ipc.ops == ["connection_token", "check"], "2 回目は取り直さずに停止だけ確かめる"


async def test_runner_does_not_hand_out_token_when_stopped_during_fetch():
    """取得を待つ間に取消を検知したら、取れた token でも子へ渡さない。"""
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        return None

    runner._refresh_control = _refresh
    runner._check_deadline_now = lambda: None

    class _Client:
        async def get_connection_token(self, slot):
            runner._stop_reason = "cancel"  # 取得中に取消が観測された
            return {"access_token": "t", "token_type": "Bearer", "expires_at": None}

    runner._client = _Client()
    reply = await runner._on_connection_token("gitlab")
    assert reply == {"ok": False, "error": "execution cancel", "stop_reason": "cancel"}



async def test_cached_connection_token_is_not_returned_past_the_agent_deadline():
    """停止確認から max_age 以内でも、Agent の期限を過ぎていれば手元の token を返さない (期限は毎回ローカル判定)。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    ctx._spec["agent_deadline"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    ctx._last_check = __import__("time").monotonic()  # 直前に停止確認済み (rate-limit で IPC しない)
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")
    assert ipc.ops == ["connection_token"]



# ---------------------------------------------------------------------------
# 3.0.5 公開前レビューの指摘（live 読み取りの 409 / 停止後の token / 期限不明の token / slot / 再送回数）
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("code,outcome", [("cancelled", ("stopped", "cancelled")), ("run_closed", ("stopped", "cancelled")),
                                          ("deadline_exceeded", ("timeout", "execution_timeout"))])
async def test_live_reject_while_staging_inputs_ends_through_the_normal_stop_path(tmp_path: Path, code, outcome):
    """front は取消 / run の終端 / 期限の後の入力取得を 409 で拒否する。runner は例外で落ちずに停止理由へ写し、
    Agent を起動せずに completion を送る（変更前と同じ終端）。"""
    fake = FakeRuntime()
    fake.download_reject = (409, code)
    res = await run_with(fake, "run_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == outcome
    assert res.completion_saved and fake.completion is not None
    assert not (tmp_path / "output" / "reply.md").exists(), "Agent は起動しない"
    assert fake.completion["envelope"]["had_mutating_success"] is False


async def test_other_api_errors_while_staging_still_propagate(tmp_path: Path):
    """live の 409 以外（契約外の 4xx）は従来どおり例外のまま（completion は送らない）。"""
    fake = FakeRuntime()
    fake.download_reject = (404, "not_found")
    with pytest.raises(Exception) as caught:
        await run_with(fake, "run_reply", tmp_path)
    assert type(caught.value).__name__ == "RuntimeApiError" and fake.completion is None


async def test_refused_refresh_drops_the_cached_token_and_latches_stop():
    """取り直しを停止で断られたら、手元の token も以後は返さない（IPC もしない）。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp},
                    {"ok": False, "error": "execution terminal", "stop_reason": "terminal"}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab", min_ttl=7200)   # 期限まで 2 時間を切っている = 取り直す → 停止で拒否
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")                 # 既定の min_ttl なら手元の値が使える状況でも返さない
    assert ipc.ops == ["connection_token", "connection_token"]
    assert await ctx.is_cancel_requested()


async def test_refused_refresh_without_stop_does_not_fall_back_to_the_cached_token():
    """失効 / 再認可待ちで断られた token は手元に残さない（次の呼び出しは取り直しに行く）。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp},
                    {"ok": False, "error": "connection_unavailable"},
                    {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab", min_ttl=7200)
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t2"
    assert ipc.ops == ["connection_token"] * 3


async def test_token_is_not_returned_when_the_deadline_passes_while_waiting_for_the_runner():
    """IPC を待つ間に Agent の期限を過ぎたら、取れた token でも返さない（返す直前に手元の時計で確かめる）。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

    class _LateIpc(_FakeIpc):
        async def call(self, op, **payload):
            ctx._spec["agent_deadline"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
            return await super().call(op, **payload)

    ipc = _LateIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")


async def test_token_without_expiry_is_refetched_after_the_refresh_interval(monkeypatch):
    """期限の分からない token（PAT / 上流が期限を返さない）も一定間隔で取り直す（期限切れの値を返し続けない）。"""
    import time as _time

    from agenticstar_platform.workflow import context as ctx_mod

    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": None},
                    {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": None}])
    ctx = _context(ipc)
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t1"
    ctx._last_check = _time.monotonic()
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t1", "間隔内は手元の値"
    monkeypatch.setattr(ctx_mod, "UNKNOWN_EXPIRY_REFRESH_SECONDS", 0.0)
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t2", "間隔を過ぎたら取り直す"
    assert ipc.ops == ["connection_token", "connection_token"]


async def test_runner_rechecks_remote_cancel_after_the_fetch():
    """取得の後は取消 / 終端を front に取り直して確かめる（watchdog の次の確認を待たない）。"""
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None
    forced: list[tuple[bool, object]] = []

    async def _refresh(force=False, attempts=None):
        forced.append((force, attempts))
        if force:
            runner._stop_reason = "cancel"   # 取得中に front で取消された

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            return {"access_token": "t", "token_type": "Bearer", "expires_at": None}

    runner._client = _Client()
    reply = await runner._on_connection_token("gitlab")
    assert reply == {"ok": False, "error": "execution cancel", "stop_reason": "cancel"}
    assert forced == [(False, None), (True, 2)], "取得後の確認は試行 2 回まで（IPC を長く塞がない）"


@pytest.mark.parametrize("code,stop", [("cancelled", "cancel"), ("run_closed", "cancel"), ("deadline_exceeded", "deadline")])
async def test_runner_maps_live_reject_on_token_fetch_to_stop(code, stop):
    from agenticstar_platform.workflow.errors import RuntimeApiError
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        return None

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            raise RuntimeApiError(409, code)

    runner._client = _Client()
    reply = await runner._on_connection_token("gitlab")
    assert reply["ok"] is False and reply["stop_reason"] == stop and runner._stop_reason == stop


async def test_runner_does_not_stop_on_other_token_errors():
    from agenticstar_platform.workflow.errors import RuntimeApiError
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        return None

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            raise RuntimeApiError(409, "reauth_required")

    runner._client = _Client()
    assert await runner._on_connection_token("gitlab") == {"ok": False, "error": "reauth_required"}
    assert runner._stop_reason is None


@pytest.mark.parametrize("slot", ["", ".", "..", "a/b", "1abc", "a" * 65, "\ud800", "gitlab\n"])
async def test_client_rejects_dot_slots_before_requesting(slot):
    """front と同じ形の slot だけ送る。"." / ".." は quote しても残り URL の正規化で …/token 等の別のパスに届く。
    符号化できない文字は quote が例外を出す。要求を出さずに WorkflowError で拒否する。"""
    import httpx

    from agenticstar_platform.workflow.errors import WorkflowError
    from agenticstar_platform.workflow.runtime_client import RuntimeClient

    seen: list[str] = []
    client = RuntimeClient("https://front.test/api/mp/runtime/v1/executions", EXECUTION_ID, "tok",
                           transport=httpx.MockTransport(lambda r: (seen.append(str(r.url)), httpx.Response(200, json={}))[1]))
    with pytest.raises(WorkflowError):
        await client.get_connection_token(slot)
    await client.aclose()
    assert seen == []


async def test_client_encodes_the_slot_and_retries_token_fetch_at_most_twice():
    import httpx

    from agenticstar_platform.workflow.errors import RuntimeApiError
    from agenticstar_platform.workflow.runtime_client import RuntimeClient

    seen: list[str] = []

    def handler(request):
        seen.append(request.url.raw_path.decode())
        return httpx.Response(503, json={"code": "connection_unavailable"})

    client = RuntimeClient("https://front.test/api/mp/runtime/v1/executions", EXECUTION_ID, "tok",
                           transport=httpx.MockTransport(handler))
    with pytest.raises(RuntimeApiError) as caught:
        await client.get_connection_token("git_lab-2")
    await client.aclose()
    assert caught.value.code == "connection_unavailable"
    assert len(seen) == 2, "token の取得は 2 回まで（既定の 6 回再送で runner の IPC を塞がない）"
    assert seen[0].endswith("/connections/git_lab-2/token")


async def test_post_fetch_context_check_is_bounded_to_two_attempts(tmp_path: Path):
    """取得後の取消確認（/context）が 5xx でも試行は 2 回で、token は手元の停止 / 期限だけで判断して渡す。"""
    import httpx

    from agenticstar_platform.workflow.runner import WorkflowRunner

    calls: list[str] = []

    def handler(request):
        path = request.url.path
        calls.append(path)
        if path.endswith("/token"):
            return httpx.Response(200, json={"access_token": "t", "token_type": "Bearer", "expires_at": None})
        return httpx.Response(503, json={"code": "runtime_unavailable"})

    from agenticstar_platform.workflow.runtime_client import RuntimeClient

    runner = WorkflowRunner(entrypoint=f"{FIX}:run_reply", env=env_for(), workspace=str(tmp_path))
    runner._client = RuntimeClient("https://front.test/api/mp/runtime/v1/executions", EXECUTION_ID, TOKEN,
                                   transport=httpx.MockTransport(handler))
    runner._last_context_check = __import__("time").monotonic()   # 取得前の確認は rate-limit 内（IPC しない）
    reply = await runner._on_connection_token("gitlab")
    await runner._client.aclose()
    assert reply["ok"] is True and reply["access_token"] == "t"
    assert sum(1 for c in calls if c.endswith("/context")) == 2



async def test_concurrent_calls_do_not_return_a_token_refused_meanwhile():
    """並行する呼び出し: 手元の値を返す途中（取消確認の IPC 待ち）に別の呼び出しが取り直しを断られても、
    古い値を後から返さない（connection_token は直列。渡す直前に、その間に取り直しが断られていないかを確かめる）。"""
    import asyncio
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    gate = asyncio.Event()

    class _GatedIpc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            if op == "check":
                await gate.wait()
                return {"stop_reason": None}
            return self.replies.pop(0)

    ipc = _GatedIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp},
                     {"ok": False, "error": "reauth_required"},
                     {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    ctx._last_check = 0.0
    a = asyncio.create_task(ctx.connection_token("gitlab"))               # 手元の値 → 取消確認で待つ
    b = asyncio.create_task(ctx.connection_token("gitlab", min_ttl=7200))  # 取り直し → 断られる
    for _ in range(5):
        await asyncio.sleep(0)
    assert ipc.ops == ["connection_token", "check"], "a が返し終えるまで b は取り直しに行かない"
    gate.set()
    with pytest.raises(WorkflowError, match="refused while being handed out"):
        await a          # 渡す前に b の取り直しが断られた
    with pytest.raises(WorkflowError):
        await b
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t2", "断られた値は手元に残らない"


async def test_stop_latch_is_not_cleared_by_an_older_check():
    """並行して停止が立った後に、先に出していた確認の「停止なし」が返っても停止を戻さない。"""
    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            ctx._stopped = True          # 確認を待つ間に、別の呼び出しが停止を受け取った
            return {"stop_reason": None}

    ctx = _context(_Ipc([]))
    assert await ctx.is_cancel_requested(max_age=0.0) is True
    assert await ctx.is_cancel_requested() is True


async def test_runner_reports_a_known_stop_even_when_the_fetch_fails():
    """取得を待つ間に停止を知ったら、取得の失敗理由（connection_unavailable 等）ではなく停止として返す。"""
    from agenticstar_platform.workflow.errors import RuntimeApiError
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        return None

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            runner._stop_reason = "cancel"   # watchdog が取得中に取消を観測
            raise RuntimeApiError(503, "connection_unavailable")

    runner._client = _Client()
    assert await runner._on_connection_token("gitlab") == {"ok": False, "error": "execution cancel", "stop_reason": "cancel"}



def _gated_ipc(gate, gate_at: int):
    class _GatedIpc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            if len(self.ops) == gate_at:
                await gate.wait()
            return self.replies.pop(0)
    return _GatedIpc


@pytest.mark.parametrize("refusal,expect_refetch", [({"ok": False, "error": "reauth_required"}, True),
                                                    ({"ok": False, "error": "execution cancel", "stop_reason": "cancel"}, False)])
async def test_cancelled_refresh_still_applies_the_refusal(refusal, expect_refetch):
    """取り直しの途中で呼び出し元が取り消されても、断られた結果（手元の値の破棄 / 停止の固定）は反映する。
    次の呼び出しは古い値を返さない（IPC は取り消された要求の応答を捨てるので、反映は shield した task が行う）。"""
    import asyncio
    import time as _time
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    gate = asyncio.Event()
    ipc = _gated_ipc(gate, 2)([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}, refusal,
                               {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    a = asyncio.create_task(ctx.connection_token("gitlab", min_ttl=7200))
    for _ in range(5):
        await asyncio.sleep(0)
    a.cancel()
    with pytest.raises(asyncio.CancelledError):
        await a
    ctx._last_check = _time.monotonic()   # 取消確認は rate-limit 内（手元の値を返せる状況）
    b = asyncio.create_task(ctx.connection_token("gitlab"))
    for _ in range(5):
        await asyncio.sleep(0)
    assert ipc.ops == ["connection_token", "connection_token"], "b は取り直しの反映が終わるまで待つ"
    gate.set()
    if expect_refetch:
        assert (await b)["access_token"] == "t2"
        assert ipc.ops == ["connection_token"] * 3
    else:
        with pytest.raises(WorkflowError):
            await b
        assert ipc.ops == ["connection_token"] * 2


async def test_cached_token_that_goes_stale_during_the_cancel_check_is_refetched():
    """取消確認を待つ間に期限まで min_ttl を切ったら、手元の値ではなく取り直した値を返す。"""
    from datetime import datetime, timedelta, timezone

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            if op == "check":
                soon = (datetime.now(timezone.utc) + timedelta(milliseconds=500)).isoformat()
                ctx._tokens["gitlab"][0]["expires_at"] = soon   # 確認を待つ間に時間が過ぎた
                return {"stop_reason": None}
            return self.replies.pop(0)

    ipc = _Ipc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp},
                {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    ctx._last_check = 0.0
    assert (await ctx.connection_token("gitlab", min_ttl=1))["access_token"] == "t2"
    assert ipc.ops == ["connection_token", "check", "connection_token"]


async def test_runner_returns_a_known_stop_for_an_empty_slot():
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = "cancel"
    runner._stop_requested, runner._agent_deadline = False, None
    assert await runner._on_connection_token("") == {"ok": False, "error": "execution cancel", "stop_reason": "cancel"}



def _handoff_ctx(mutate):
    """取り直しの応答を返した直後（task の完了より前）に mutate(ctx) を call_soon で走らせる context。
    task の完了から呼び出し元の再開までの間に状態が変わる経路を再現する。"""
    import asyncio
    from datetime import datetime, timedelta, timezone

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            asyncio.get_running_loop().call_soon(mutate, ctx)
            return {"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}

    ctx = _context(_Ipc([]))
    return ctx


@pytest.mark.parametrize("what", ["stop", "deadline", "dropped", "refused"])
async def test_token_is_revalidated_after_the_last_await(what):
    """task が値を返してから呼び出し元が再開するまでの間に、停止 / 期限 / 手元の値の破棄が起きたら渡さない。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    def mutate(ctx):
        if what == "stop":
            ctx._stopped = True
        elif what == "deadline":
            ctx._spec["agent_deadline"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        elif what == "dropped":
            ctx._tokens.pop("gitlab", None)
        else:   # 後の呼び出しの取り直しが断られた
            ctx._tokens.pop("gitlab", None)
            ctx._token_refusals["gitlab"] = ctx._token_refusals.get("gitlab", 0) + 1

    ctx = _handoff_ctx(mutate)
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")


async def test_fetched_token_that_is_already_expired_is_not_cached_or_returned():
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    past = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": past},
                    {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": future}])
    ctx = _context(ipc)
    with pytest.raises(WorkflowError, match="expired"):
        await ctx.connection_token("gitlab")
    assert "gitlab" not in ctx._tokens
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t2"


async def test_abandoned_waiter_does_not_fetch_after_getting_the_lock():
    """ロック待ちのまま取り消された呼び出しは、後でロックを取っても取り直しを出さない（runner の直列 IPC を塞がない）。"""
    import asyncio
    from datetime import datetime, timedelta, timezone

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    gate = asyncio.Event()
    ipc = _gated_ipc(gate, 1)([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}])
    ctx = _context(ipc)
    a = asyncio.create_task(ctx.connection_token("gitlab"))
    waiters = [asyncio.create_task(ctx.connection_token("other")) for _ in range(3)]
    for _ in range(5):
        await asyncio.sleep(0)
    for w in waiters:
        w.cancel()
    await asyncio.gather(*waiters, return_exceptions=True)
    gate.set()
    assert (await a)["access_token"] == "t1"
    for _ in range(10):
        await asyncio.sleep(0)
    assert ipc.ops == ["connection_token"], "取り消された待ち手は IPC を出さない"
    assert not ctx._bg_tasks, "終わった task への参照は残さない"


async def test_runner_refuses_when_sigterm_arrives_during_the_post_fetch_check():
    """取得後の取消確認を待つ間に停止 signal が来たら、応答の中身（token なし等）に関わらず停止として返す。"""
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        if force:
            runner._stop_requested = True   # SIGTERM

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            return {"token_type": "Bearer"}   # token が無い応答

    runner._client = _Client()
    assert await runner._on_connection_token("gitlab") == {"ok": False, "error": "execution stopped", "stop_reason": "stopped"}


async def test_runner_refuses_when_the_deadline_passes_during_the_pre_fetch_check():
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None
    fetched: list[str] = []

    async def _refresh(force=False, attempts=None):
        runner._agent_deadline = datetime.now(timezone.utc) - timedelta(seconds=1)

    runner._refresh_control = _refresh

    class _Client:
        async def get_connection_token(self, slot):
            fetched.append(slot)
            return {"access_token": "t"}

    runner._client = _Client()
    reply = await runner._on_connection_token("gitlab")
    assert reply["stop_reason"] == "deadline" and fetched == []



def _minting_ipc():
    """取り直すたびに新しい token（期限 1 時間）を返す IPC。取消確認は常に「停止なし」。"""
    from datetime import datetime, timedelta, timezone

    class _Ipc(_FakeIpc):
        n = 0

        async def call(self, op, **payload):
            self.ops.append(op)
            if op == "check":
                return {"stop_reason": None}
            type(self).n += 1
            exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
            return {"ok": True, "access_token": f"t{type(self).n}", "token_type": "Bearer", "expires_at": exp}

    return _Ipc([])


@pytest.mark.parametrize("ttls", [(3600, 3600), (300, 7200), (300, 300, 300)])
async def test_sharing_a_slot_concurrently_does_not_fail_spuriously(ttls):
    """同じ slot を並行で使っても、後の呼び出しの取り直しが成功した場合は失敗させず新しい方を渡す
    （期限まで min_ttl を切った token を並行で取り直し続けても、毎回全員が値を受け取る）。"""
    import asyncio

    ipc = _minting_ipc()
    ctx = _context(ipc)
    for _ in range(20):
        got = await asyncio.gather(*(ctx.connection_token("gitlab", min_ttl=t) for t in ttls))
        assert all(g["access_token"] for g in got)
        assert got[-1]["access_token"] == ctx._tokens["gitlab"][0]["access_token"], "最後に渡した値は手元の最新"


async def test_handoff_gives_the_newer_token_when_a_later_refresh_succeeded():
    """a が手元の値を渡しかけている間に b が取り直しに成功したら、a も新しい値を受け取る。"""
    import asyncio
    import time as _time

    ipc = _minting_ipc()
    ctx = _context(ipc)
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t1"
    ctx._last_check = _time.monotonic()
    a = asyncio.create_task(ctx.connection_token("gitlab"))              # 手元の t1 を確かめる
    b = asyncio.create_task(ctx.connection_token("gitlab", min_ttl=7200))  # 取り直して t2
    got_a, got_b = await asyncio.gather(a, b)
    assert got_b["access_token"] == "t2" and got_a["access_token"] == "t2"



async def test_lock_waiter_cancelled_right_after_the_lock_is_released_does_not_fetch():
    """ロックが離された直後（待ち手が起こされた後・走る前）に呼び出し元が取り消されても取り直さない
    （取消は shield の外側の future に同期で届くので、待ち手は走る前に気づく）。"""
    import asyncio
    from datetime import datetime, timedelta, timezone

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    gate = asyncio.Event()
    holder: dict = {}

    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            if len(self.ops) == 1:
                await gate.wait()
                asyncio.get_running_loop().call_soon(holder["b"].cancel)   # ロック解放と同じ周回で取り消す
            return {"ok": True, "access_token": f"t{len(self.ops)}", "token_type": "Bearer", "expires_at": exp}

    ipc = _Ipc([])
    ctx = _context(ipc)
    a = asyncio.create_task(ctx.connection_token("gitlab"))
    for _ in range(3):
        await asyncio.sleep(0)
    holder["b"] = asyncio.create_task(ctx.connection_token("other"))
    for _ in range(3):
        await asyncio.sleep(0)
    gate.set()
    assert (await a)["access_token"] == "t1"
    res = await asyncio.gather(holder["b"], return_exceptions=True)
    assert isinstance(res[0], asyncio.CancelledError)
    for _ in range(10):
        await asyncio.sleep(0)
    assert ipc.ops == ["connection_token"]


async def test_cancelled_cancel_check_still_latches_the_stop():
    """is_cancel_requested() の途中で呼び出し元が取り消されても、届いた停止は記録する（以後の手元の token も渡さない）。"""
    import asyncio
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    exp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    gate = asyncio.Event()

    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            if op == "check":
                await gate.wait()
                return {"stop_reason": "cancel"}
            return {"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": exp}

    ipc = _Ipc([])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    ctx._last_check = 0.0
    c = asyncio.create_task(ctx.is_cancel_requested())
    for _ in range(3):
        await asyncio.sleep(0)
    c.cancel()
    await asyncio.gather(c, return_exceptions=True)
    gate.set()
    for _ in range(10):
        await asyncio.sleep(0)
    assert ctx._stopped is True
    with pytest.raises(WorkflowError):
        await ctx.connection_token("gitlab")
    assert ipc.ops == ["connection_token", "check"]
    assert not ctx._bg_tasks


async def test_runner_check_reports_a_stop_signal_that_arrived_during_the_refresh():
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None

    async def _refresh(force=False, attempts=None):
        runner._stop_requested = True   # SIGTERM が確認の途中で来た（確認自体は失敗して何も変えない）

    runner._refresh_control = _refresh
    assert await runner._dispatch({"op": "check"}) == {"stop_reason": "stopped"}



async def test_cancel_check_returns_the_latch_as_of_resume():
    """確認の応答（停止なし）を受けてから呼び出し元が再開するまでに、並行する確認が停止を固定したら、停止を返す
    （ensure_can_act は通さない）。connection_token を呼ばない Agent にも関わる。"""
    import asyncio

    from agenticstar_platform.workflow.errors import WorkflowError

    class _Ipc(_FakeIpc):
        async def call(self, op, **payload):
            self.ops.append(op)
            asyncio.get_running_loop().call_soon(setattr, ctx, "_stopped", True)   # 別の確認が先に停止を固定
            return {"stop_reason": None}

    ctx = _context(_Ipc([]))
    with pytest.raises(WorkflowError):
        await ctx.ensure_can_act()


async def test_expired_refresh_result_also_drops_the_previous_token():
    """取り直した結果が既に期限切れなら、断られた時と同じく前の値も渡さない（次の呼び出しは取り直す）。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.errors import WorkflowError

    past = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    ipc = _FakeIpc([{"ok": True, "access_token": "t1", "token_type": "Bearer", "expires_at": future},
                    {"ok": True, "access_token": "t2", "token_type": "Bearer", "expires_at": past},
                    {"ok": True, "access_token": "t3", "token_type": "Bearer", "expires_at": future}])
    ctx = _context(ipc)
    await ctx.connection_token("gitlab")
    with pytest.raises(WorkflowError, match="expired"):
        await ctx.connection_token("gitlab", min_ttl=7200)
    assert "gitlab" not in ctx._tokens and ctx._token_refusals["gitlab"] == 1
    assert (await ctx.connection_token("gitlab"))["access_token"] == "t3"



# ---------------------------------------------------------------------------
# #2369: runner が知っている停止をどの応答でも子へ伝える / IPC 書き込みの切断は WorkflowError
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("msg", [{"op": "log", "message": "x"}, {"op": "skip", "reason": "no-such"},
                                 {"op": "audit", "event": {"event_type": "tool.invoked", "event_id": "e1"}}])
async def test_runner_answers_carry_a_known_stop(msg):
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = "cancel"
    runner._stop_requested, runner._agent_deadline = False, None
    runner.execution_id = EXECUTION_ID

    async def _refresh(force=False, attempts=None):
        return None

    runner._refresh_control = _refresh
    reply = await runner._answer(dict(msg))
    assert reply["stop_reason"] == "cancel"


async def test_runner_answers_without_a_stop_are_unchanged():
    from agenticstar_platform.workflow.runner import WorkflowRunner

    runner = WorkflowRunner.__new__(WorkflowRunner)
    runner._stop_reason = None
    runner._stop_requested, runner._agent_deadline = False, None
    runner.execution_id = EXECUTION_ID
    assert await runner._answer({"op": "log", "message": "x"}) == {"ok": True}


def _pipes():
    import os

    to_child_r, to_child_w = os.pipe()
    to_runner_r, to_runner_w = os.pipe()
    return to_child_r, to_child_w, to_runner_r, to_runner_w


async def test_ipc_reader_latches_a_stop_from_the_reply_to_a_cancelled_request():
    """取り消された要求の応答（待ち手がいない）でも、親が載せた停止は子で固定する（本物の pipe）。"""
    import asyncio
    import json
    import os

    from agenticstar_platform.workflow.context import WorkflowContext, _Ipc

    to_child_r, to_child_w, to_runner_r, to_runner_w = _pipes()
    ipc = _Ipc(to_child_r, to_runner_w)
    spec = {k: "x" for k in ("execution_id", "project_id", "run_id", "agent_id", "marketplace_agent_id",
                             "root_execution_id", "entry_ref", "operation_key", "effect_mode")}
    spec.update({"attempt": 1, "input_dir": "/tmp", "work_dir": "/tmp", "output_dir": "/tmp"})
    ctx = WorkflowContext(spec, ipc)
    try:
        call = asyncio.create_task(ipc.call("log", message="hello"))
        loop = asyncio.get_running_loop()

        def _read_frame():
            import select

            ready, _, _ = select.select([to_runner_r], [], [], 5.0)   # 書けていなければ CI を止めずに失敗させる
            assert ready, "child did not write the request frame"
            return os.read(to_runner_r, 65536)

        frame = await loop.run_in_executor(None, _read_frame)
        rid = json.loads(frame.decode().splitlines()[0])["id"]
        call.cancel()
        await asyncio.gather(call, return_exceptions=True)
        os.write(to_child_w, (json.dumps({"id": rid, "ok": True, "stop_reason": "cancel"}) + "\n").encode())
        for _ in range(200):
            if ctx._stopped:
                break
            await asyncio.sleep(0.01)
        assert ctx._stopped is True
        assert await ctx.is_cancel_requested() is True
    finally:
        os.close(to_child_w)   # reader thread を終わらせる (失敗しても後始末する)
        for _ in range(200):
            if ipc._reader is None or ipc._reader.done():
                break
            await asyncio.sleep(0.01)
        os.close(to_runner_r)


async def test_ipc_write_to_a_closed_channel_is_a_workflow_error():
    """親が制御 channel を閉じた後の書き込みは BrokenPipeError ではなく WorkflowError（Agent は WorkflowError を捕まえればよい）。"""
    import asyncio
    import os

    from agenticstar_platform.workflow.context import _Ipc
    from agenticstar_platform.workflow.errors import WorkflowError

    to_child_r, to_child_w, to_runner_r, to_runner_w = _pipes()
    ipc = _Ipc(to_child_r, to_runner_w)
    os.close(to_runner_r)   # 親が読み取り側を閉じた
    try:
        with pytest.raises(WorkflowError, match="control channel"):
            await ipc.call("log", message="hello")
        ipc._out.close()        # 閉じたファイルへの書き込み (ValueError) も同じ
        with pytest.raises(WorkflowError, match="control channel"):
            await ipc.call("log", message="again")
    finally:
        os.close(to_child_w)   # reader thread を終わらせる
        for _ in range(200):
            if ipc._reader is None or ipc._reader.done():
                break
            await asyncio.sleep(0.01)



async def test_runner_answer_does_not_turn_a_pending_stop_into_a_stop_reason():
    """_answer は既に確定した停止だけを載せる。done を処理する瞬間に停止 signal / 期限が来ていても、ここで停止理由に
    確定させない (Agent が戻った後の done を stopped / timeout に変えない。3.0.5 と同じ終わり方)。"""
    from datetime import datetime, timedelta, timezone

    from agenticstar_platform.workflow.runner import WorkflowRunner

    for pending in ("signal", "deadline"):
        runner = WorkflowRunner.__new__(WorkflowRunner)
        runner._stop_reason = None
        runner._stop_requested = pending == "signal"
        runner._agent_deadline = datetime.now(timezone.utc) - timedelta(seconds=1) if pending == "deadline" else None
        runner.execution_id = EXECUTION_ID
        reply = await runner._answer({"op": "done", "status": "ok"})
        assert "stop_reason" not in reply and runner._stop_reason is None
