"""ワークフローの「完遂できなかった」（`context.incomplete`）と終了時の報告（`completion_report`）（3.2.1、devdocs 3.3 AU-23 /
R33-289）。

固定する契約:
1. `incomplete(reason, comment)` で outcome `incomplete`、理由コード = reason（`report_completion()` と同じ正規化。合わなければ
   `incomplete`）。宣言の後に例外で抜けても incomplete。2 回目は最初の宣言を残す
2. 順: 監査の保存の失敗・取消・期限・他所の終端・runner の停止・拒否 → 宣言 → 例外 → 回収の失敗 → skip → 必須 output の欠落
3. envelope の `completion_report` = `{completed: false, reason_code, comment}`。incomplete は Agent の説明（無ければ欄なし）、
   failed/agent_error は伏せ字付きの原因の連鎖（秘密の値は出ない）。comment は 2,048（UTF-16 の単位）で切る。
   ほかの終わり方では欄ごと無い（3.2 までと同じ envelope）
"""
from __future__ import annotations

import asyncio
import enum
import json
import logging
from pathlib import Path

import pytest

from agenticstar_platform.workflow import (
    EffectTally,
    WorkflowRunner,
    build_envelope,
    decide_outcome,
)
from agenticstar_platform.workflow.context import _incomplete_reason
from agenticstar_platform.workflow.envelope import (
    build_completion_report,
    cut_utf16,
    report_comment,
)
from agenticstar_platform.workflow.testing import FakeRuntime

FIX = "tests.workflow.agent_fixtures"


@pytest.fixture(autouse=True)
def _sdk_on_path(monkeypatch):
    sdk_root = str(Path(__file__).resolve().parents[2])
    monkeypatch.setenv("PYTHONPATH", sdk_root)
    monkeypatch.delenv("ASTER_RUNTIME_TOKEN", raising=False)
    monkeypatch.chdir(sdk_root)


async def run_with(fake: FakeRuntime, entry: str, workspace: Path, **kw):
    runner = WorkflowRunner(entrypoint=f"{FIX}:{entry}", env=fake.runner_env(), workspace=str(workspace),
                            transport=fake.transport, cancel_poll_seconds=kw.pop("cancel_poll_seconds", 0.3),
                            child_grace_seconds=kw.pop("child_grace_seconds", 3.0))
    return await runner.run()


def _envelope(fake: FakeRuntime) -> dict:
    saved = fake.saved_completion()
    assert saved is not None
    return saved["envelope"]


# ---------------------------------------------------------------------------
# 1. 宣言 → incomplete（AC-33-289-1 の SDK の分）
# ---------------------------------------------------------------------------
async def test_declared_incomplete_ends_the_step_with_the_reason_and_comment(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "missing_instructions")
    assert res.exit_code == 0 and res.completion_saved and res.had_mutating_success is False
    env = _envelope(fake)
    assert env["completion_report"] == {"completed": False, "reason_code": "missing_instructions",
                                        "comment": "instructions.md is empty"}
    assert env["error_class"] is None and env["runner"]["agent_error"] is None


async def test_an_exception_after_the_declaration_stays_incomplete(tmp_path: Path, capfd):
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete_then_raise", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "missing_instructions")
    env = _envelope(fake)
    assert env["completion_report"] == {"completed": False, "reason_code": "missing_instructions", "comment": "no instructions"}
    assert env["error_class"] == "RuntimeError"   # 例外のクラス名は今どおり残る
    out, err = capfd.readouterr()
    assert "secret-value-123" not in json.dumps(fake.saved_completion()) and "secret-value-123" not in out + err


async def test_the_second_declaration_is_not_recorded(tmp_path: Path, caplog):
    fake = FakeRuntime()
    with caplog.at_level(logging.WARNING, logger="agenticstar_platform.workflow.runner"):
        res = await run_with(fake, "run_incomplete_twice", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "missing_instructions")
    assert _envelope(fake)["completion_report"]["comment"] == "first"
    assert any("already declared" in r.getMessage() for r in caplog.records)


async def test_a_sentence_as_the_reason_becomes_incomplete_without_a_comment(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete_bad_reason", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "incomplete")
    assert _envelope(fake)["completion_report"] == {"completed": False, "reason_code": "incomplete"}


async def test_the_comment_is_cut_to_the_front_limit(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete_long_comment", tmp_path)
    assert res.outcome == "incomplete"
    comment = _envelope(fake)["completion_report"]["comment"]
    # 2,000 字（2,000 単位）+ BMP の外の 24 字（48 単位）= 2,048 単位
    assert comment == "あ" * 2000 + "\U0001F600" * 24
    assert len(comment.encode("utf-16-le")) // 2 == 2048


async def test_outputs_written_before_the_declaration_are_saved(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete_with_reply", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "bad_config")
    assert fake.saved_artifacts()["reply"]["content"] == b"partial\n"
    assert _envelope(fake)["completion_report"] == {"completed": False, "reason_code": "bad_config"}


async def test_a_malformed_declaration_on_the_control_channel_is_cleaned(tmp_path: Path):
    """制御チャネルは Agent のプロセスが書ける: 形の違う理由は incomplete、文字列でない comment は載せない。"""
    fake = FakeRuntime()
    res = await run_with(fake, "run_raw_ipc_bad_incomplete", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "incomplete")
    assert _envelope(fake)["completion_report"] == {"completed": False, "reason_code": "incomplete"}


async def test_a_comment_that_is_not_a_string_is_left_out_with_a_warning(tmp_path: Path, capfd):
    """例外などを comment に渡しても、その本文（秘密の値が入りうる）を報告に載せない（runner 側と同じ扱い）。"""
    fake = FakeRuntime()
    res = await run_with(fake, "run_incomplete_exception_comment", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("incomplete", "bad_config")
    assert _envelope(fake)["completion_report"] == {"completed": False, "reason_code": "bad_config"}
    out, err = capfd.readouterr()
    assert "secret-value-123" not in json.dumps(fake.saved_completion()) and "secret-value-123" not in out + err
    assert "incomplete comment left out" in err and "RuntimeError" in err   # 子の警告（型の名前だけ）


# ---------------------------------------------------------------------------
# 2. 拒否・取消・期限は宣言より先
# ---------------------------------------------------------------------------
async def test_a_denial_comes_before_the_declaration(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_denied_then_incomplete", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("denied", "policy_denied")
    assert "completion_report" not in _envelope(fake)


async def test_a_cancellation_comes_before_the_declaration(tmp_path: Path):
    fake = FakeRuntime()

    async def cancel_after_the_declaration():
        for _ in range(400):   # 宣言の後に書く reply.md が出たら取消（最長 20 秒）
            if (tmp_path / "output" / "reply.md").exists():
                break
            await asyncio.sleep(0.05)
        fake.cancel_requested_at = "2026-10-28T00:00:00Z"
    task = asyncio.create_task(cancel_after_the_declaration())
    res = await run_with(fake, "run_incomplete_then_slow", tmp_path, cancel_poll_seconds=0.2)
    await task
    assert (res.outcome, res.outcome_reason_code) == ("stopped", "cancelled")
    # front は取消の後の completion を拒むので、送ろうとした envelope は state に残ったものを見る
    state = json.loads((tmp_path / ".aster_workflow_state.json").read_text())
    assert state["tally"]["incomplete_reason"] == "missing_instructions"   # 宣言は記録されていた
    assert state["completion"]["envelope"]["outcome"] == "stopped"
    assert "completion_report" not in state["completion"]["envelope"]


def test_outcome_order_with_a_declaration():
    kw = {"agent_error": None, "stop_reason": None, "outputs_collected": 0, "required_missing": [], "effect_mode": "read_only"}
    t = EffectTally()
    t.incomplete_reason = "missing_instructions"
    assert decide_outcome(tally=t, **kw) == ("incomplete", "missing_instructions", False)
    # 先に決まるもの
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "cancel"})[:2] == ("stopped", "cancelled")
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "deadline"})[:2] == ("timeout", "execution_timeout")
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "terminal"})[:2] == ("stopped", "terminal_elsewhere")
    assert decide_outcome(tally=t, **{**kw, "stop_reason": "stopped"})[:2] == ("failed", "runner_stopped")
    t_denied = EffectTally.from_dict(t.to_dict())
    t_denied.denials.append("policy_denied")
    assert decide_outcome(tally=t_denied, **kw)[:2] == ("denied", "policy_denied")
    t_persist = EffectTally.from_dict(t.to_dict())
    t_persist.persist_failures = 1
    assert decide_outcome(tally=t_persist, **kw)[:2] == ("failed", "audit_persist_failed")
    # 後に決まるもの（宣言が勝つ）
    assert decide_outcome(tally=t, **{**kw, "agent_error": "RuntimeError"})[:2] == ("incomplete", "missing_instructions")
    assert decide_outcome(tally=t, **{**kw, "collection_failed": True})[:2] == ("incomplete", "missing_instructions")
    assert decide_outcome(tally=t, **{**kw, "required_missing": ["reply"]})[:2] == ("incomplete", "missing_instructions")
    t_skip = EffectTally.from_dict(t.to_dict())
    t_skip.skip_reason = "no_target"
    assert decide_outcome(tally=t_skip, **kw)[:2] == ("incomplete", "missing_instructions")
    # 宣言が無ければ今どおり
    assert decide_outcome(tally=EffectTally(), **{**kw, "agent_error": "RuntimeError"})[:2] == ("failed", "agent_error")


# ---------------------------------------------------------------------------
# 3. 例外の報告（AC-33-289-2 の SDK の分）
# ---------------------------------------------------------------------------
async def test_an_agent_exception_reports_the_redacted_cause_chain(tmp_path: Path, capfd):
    fake = FakeRuntime()
    res = await run_with(fake, "run_error", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error")
    env = _envelope(fake)
    assert env["completion_report"] == {"completed": False, "reason_code": "agent_error", "comment": "RuntimeError"}
    assert env["error_class"] == "RuntimeError"
    out, err = capfd.readouterr()
    assert "secret-value-123" not in json.dumps(fake.saved_completion()) and "secret-value-123" not in out + err
    assert "agent entrypoint failed: RuntimeError [RuntimeError]" in err   # stderr への出力は今どおり


async def test_an_sdk_exception_reports_only_class_code_and_host(tmp_path: Path, capfd):
    fake = FakeRuntime()
    res = await run_with(fake, "run_sdk_error", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error")
    comment = _envelope(fake)["completion_report"]["comment"]
    assert comment == "SecurityAPIError(error_code=REQUEST_ERROR) <- ProxyError(host=example.services.ai.azure.com)"
    dumped = json.dumps(fake.saved_completion())
    for secret in ("SECRET-KEY-1", "body-secret-2", "contentsafety"):
        assert secret not in dumped
    out, err = capfd.readouterr()
    assert f"[{comment}]" in err


async def test_the_debug_traceback_does_not_reach_the_report(tmp_path: Path, monkeypatch, capfd):
    monkeypatch.setenv("ASTER_WORKFLOW_DEBUG_TRACEBACK", "1")
    fake = FakeRuntime()
    res = await run_with(fake, "run_error", tmp_path)
    assert res.outcome == "failed"
    assert _envelope(fake)["completion_report"]["comment"] == "RuntimeError"
    out, err = capfd.readouterr()
    assert "Traceback" in err and "secret-value-123" not in json.dumps(fake.saved_completion())


async def test_a_long_class_name_is_cut_in_the_report(tmp_path: Path):
    fake = FakeRuntime()
    res = await run_with(fake, "run_error_long_class_name", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error") and res.completion_saved
    env = _envelope(fake)
    assert env["error_class"] == "E" * 128 and env["completion_report"]["comment"] == "E" * 2048


async def test_a_done_without_the_cause_chain_reports_no_comment(tmp_path: Path):
    """SDK を通らない done（原因の連鎖 failure_summary が無い）: 報告は理由だけで comment の欄なし。"""
    fake = FakeRuntime()
    res = await run_with(fake, "run_raw_ipc_bad_done", tmp_path)
    assert (res.outcome, res.outcome_reason_code) == ("failed", "agent_error")
    assert _envelope(fake)["completion_report"] == {"completed": False, "reason_code": "agent_error"}


# ---------------------------------------------------------------------------
# 4. ほかの終わり方には載せない（AC-33-289-4: 今と同じ envelope）
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("entry,outcome", [("run_reply", "completed"), ("run_skip", "skipped"), ("run_denied", "denied")])
async def test_other_outcomes_carry_no_report(tmp_path: Path, entry, outcome):
    fake = FakeRuntime()
    res = await run_with(fake, entry, tmp_path)
    assert res.outcome == outcome
    assert "completion_report" not in _envelope(fake)


def test_build_envelope_adds_the_report_only_when_given():
    t = EffectTally()
    plain = build_envelope(outcome="completed", reason="completed", had_mutating_success=False, tally=t)
    assert "completion_report" not in plain
    report = build_completion_report("missing_instructions", "why")
    env = build_envelope(outcome="incomplete", reason="missing_instructions", had_mutating_success=False, tally=t,
                         completion_report=report)
    assert env["completion_report"] == {"completed": False, "reason_code": "missing_instructions", "comment": "why"}
    assert {k: v for k, v in env.items() if k != "completion_report"} == {**plain, "outcome": "incomplete",
                                                                         "outcome_reason_code": "missing_instructions"}
    assert build_completion_report("agent_error", None) == {"completed": False, "reason_code": "agent_error"}


# ---------------------------------------------------------------------------
# 5. 正規化・切り方・journal
# ---------------------------------------------------------------------------
class _Reason(str, enum.Enum):  # noqa: UP042 — StrEnum でない str の派生（str() が名前を返す）を確かめる
    MISSING = "missing_instructions"


@pytest.mark.parametrize("value,expected", [
    ("missing_instructions", "missing_instructions"),
    ("  Missing-Instructions ", "missing_instructions"),
    ("bad config", "bad_config"),
    (_Reason.MISSING, "missing_instructions"),        # str の派生は名前ではなく値
    ("", "incomplete"), (None, "incomplete"),
    ("x" * 33, "incomplete"), ("1st_try", "incomplete"), ("ValueError('secret')", "incomplete"),
])
def test_reason_normalization_matches_report_completion(value, expected):
    assert _incomplete_reason(value, "eid") == expected


def test_reason_normalization_is_the_same_as_the_chat_report():
    """会話の report_completion() の正規化（db/completion_report.normalize_reason）と同じ結果になる。"""
    pytest.importorskip("asyncpg")   # db パッケージは asyncpg を読み込む（[db] の extra）
    from agenticstar_platform.db.completion_report import normalize_reason
    for value in ("missing_instructions", "  Missing-Instructions ", "bad config", _Reason.MISSING, "", None,
                  "x" * 33, "1st_try", "ValueError('secret')", "UPPER", "a-b c"):
        assert _incomplete_reason(value, "eid") == normalize_reason(value, "incomplete", "eid")


def test_a_rejected_reason_is_logged_without_its_value(caplog):
    with caplog.at_level(logging.WARNING, logger="agenticstar_platform.workflow.context"):
        assert _incomplete_reason("token=secret-value-123 failed", "eid") == "incomplete"
    assert caplog.records and all("secret-value-123" not in r.getMessage() for r in caplog.records)


def test_comment_cutting_counts_utf16_units():
    assert cut_utf16("a" * 10, 4) == "aaaa"
    assert cut_utf16("\U0001F600" * 3, 5) == "\U0001F600" * 2   # 2 単位ずつ。半分は残さない
    assert report_comment("x" * 3000) == "x" * 2048
    assert report_comment("") is None and report_comment(None) is None and report_comment(123) is None
    assert report_comment("bad \ud800 surrogate") is None   # UTF-8 にできない値は送らない


def test_the_declaration_survives_the_tally_journal():
    t = EffectTally()
    t.incomplete_reason, t.incomplete_comment = "bad_config", "c" * 3000
    back = EffectTally.from_dict(json.loads(json.dumps(t.to_dict())))
    assert back.incomplete_reason == "bad_config" and back.incomplete_comment == "c" * 2048
    broken = EffectTally.from_dict({"incomplete_reason": "Not A Code", "incomplete_comment": "x"})
    assert broken.incomplete_reason is None and broken.incomplete_comment is None
    assert EffectTally.from_dict({}).incomplete_reason is None   # 3.2 の journal
