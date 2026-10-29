"""テスト用の Agent entrypoint（子プロセスから import される）。"""
from __future__ import annotations

import asyncio
import json
import os


async def run_reply(context):
    """回答案: work の instructions.md を読み、output/reply.md を書く。read tool を 1 回監査する。"""
    inv = await context.audit.tool_invoked("read_instructions", effect_kind="read", target="instructions.md")
    text = (context.work_dir / "instructions.md").read_text(encoding="utf-8")
    await context.audit.tool_effect(inv, status="ok", count=1)
    reply = f"# reply\n\nproduct={context.parameters['product_code']}\n\n{text.strip()}\n"
    (context.output_dir / "reply.md").write_text(reply, encoding="utf-8")
    settings = (context.work_dir / "settings" / "agent.yaml").read_text(encoding="utf-8")
    assert "product_code" in settings
    assert os.environ.get("ASTER_RUNTIME_TOKEN") is None  # token は Agent コードへ渡さない
    await context.log("reply written")


async def run_send(context):
    """模擬送信: write を tool.invoked の ack 後に実行し、effect を対応付ける。"""
    await context.ensure_can_act()
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", action_ref=f"send:{context.operation_key[:8]}",
                                           target="mock://inbox")
    (context.output_dir / "reply.md").write_text("sent\n", encoding="utf-8")
    await context.audit.tool_effect(inv, status="ok", count=1, action_ref=f"send:{context.operation_key[:8]}")


async def run_send_then_wait(context):
    """効果を 1 つ観測してから待つ（親を外から止める / 落とす試験用。親が止めるので自分では終わらない）。"""
    await context.ensure_can_act()
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    (context.output_dir / "reply.md").write_text("sent\n", encoding="utf-8")
    await context.audit.tool_effect(inv, status="ok", count=1)
    await asyncio.sleep(60)


async def run_unobserved(context):
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    (context.output_dir / "reply.md").write_text("sent?\n", encoding="utf-8")
    del inv  # effect を記録しない = 効果不明


async def run_error(context):
    (context.output_dir / "reply.md").write_text("partial\n", encoding="utf-8")
    raise RuntimeError("boom secret-value-123")


async def run_slow(context):
    (context.output_dir / "reply.md").write_text("started\n", encoding="utf-8")
    for _ in range(600):
        if await context.is_cancel_requested(max_age=0.5):
            return
        await asyncio.sleep(0.1)


async def run_audit_blocked(context):
    """監査が保存できないときは write を開始しない。"""
    try:
        await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    except Exception as e:  # noqa: BLE001
        (context.output_dir / "reply.md").write_text(f"blocked:{type(e).__name__}\n", encoding="utf-8")
        return
    (context.output_dir / "reply.md").write_text("MUST NOT HAPPEN\n", encoding="utf-8")


async def run_escape(context):
    """traversal / symlink を試みる Agent（回収で拒否されること）。"""
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")
    link = context.output_dir / "leak.md"
    link.symlink_to("/etc/hostname")


def run_sync(context):
    (context.output_dir / "reply.md").write_text("sync\n", encoding="utf-8")


async def run_unknown_effect(context):
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    await context.audit.tool_effect(inv, status="unknown")
    (context.output_dir / "reply.md").write_text("sent?\n", encoding="utf-8")


async def run_failed_effect(context):
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    await context.audit.tool_effect(inv, status="failed", error="ConnectionError")
    (context.output_dir / "reply.md").write_text("diagnostic\n", encoding="utf-8")


async def run_denied(context):
    await context.audit.tool_denied("mock_send", reason="policy forbids send", reason_code="policy_denied")
    (context.output_dir / "reply.md").write_text("diagnostic\n", encoding="utf-8")


async def run_skip(context):
    await context.skip("no_target")


async def run_edit_instructions(context):
    (context.work_dir / "instructions.md").write_text("# edited\n", encoding="utf-8")
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")


async def run_orphan_child(context):
    """配下プロセスを残したまま return する（runner がグループごと止めること）。"""
    import subprocess
    p = subprocess.Popen(["sleep", "300"])  # noqa: S603,S607
    (context.output_dir / "pid.txt").write_text(str(p.pid), encoding="utf-8")
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")


async def run_fifo(context):
    os.mkfifo(context.output_dir / "reply.md")


async def run_noisy_stdout(context):
    print("[1,2,3]")            # 制御チャネルに混ざらない
    print("x" * (300 * 1024))   # 巨大行
    print("partial", end="")    # 未終端
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")


async def run_bad_json_output(context):
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")
    (context.output_dir / "result.json").write_text('{"a": 1, "a": 2}', encoding="utf-8")


async def run_swap_output_root(context):
    """output/ 自体を外部 symlink に置き換える Agent（root fd で固定しているので外へ出ない）。"""
    import shutil
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")
    parent = context.output_dir.parent
    shutil.move(str(context.output_dir), str(parent / "output.moved"))
    os.symlink("/etc", str(context.output_dir))


async def run_slow_write_after_deadline(context):
    while not await context.is_cancel_requested(max_age=0.2):
        await asyncio.sleep(0.1)
    try:
        await context.audit.tool_invoked("mock_send", effect_kind="send")
        (context.output_dir / "reply.md").write_text("MUST NOT\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        (context.output_dir / "reply.md").write_text("blocked\n", encoding="utf-8")


async def run_read_only(context):
    inv = await context.audit.tool_invoked("read_instructions", effect_kind="read", target="instructions.md")
    (context.work_dir / "instructions.md").read_text(encoding="utf-8")
    await context.audit.tool_effect(inv, status="ok")


async def run_send_then_denied(context):
    """成功した write の後に拒否: denied が成功より優先し、had_mutating_success は保つ。"""
    inv = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://inbox")
    await context.audit.tool_effect(inv, status="ok", count=1)
    await context.audit.tool_denied("mock_send", reason="policy forbids second send", reason_code="policy_denied")
    (context.output_dir / "reply.md").write_text("report\n", encoding="utf-8")


async def run_partial_failure(context):
    inv1 = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://a")
    await context.audit.tool_effect(inv1, status="ok")
    inv2 = await context.audit.tool_invoked("mock_send", effect_kind="send", target="mock://b")
    await context.audit.tool_effect(inv2, status="failed", error="ConnectionError")
    (context.output_dir / "reply.md").write_text("report\n", encoding="utf-8")


async def run_shared_action_ref(context):
    """同じ action_ref を共有する 2 回の呼出し: 2 回目に effect が無ければ効果不明（1 回目の成功を共有しない）。"""
    inv1 = await context.audit.tool_invoked("mock_send", effect_kind="send", action_ref="send:same")
    await context.audit.tool_effect(inv1, status="ok", action_ref="send:same")
    await context.audit.tool_invoked("mock_send", effect_kind="send", action_ref="send:same")
    (context.output_dir / "reply.md").write_text("report\n", encoding="utf-8")


async def run_policy_unavailable(context):
    await context.policy_unavailable()


async def run_skip_with_report(context):
    await context.skip("no_target")
    (context.output_dir / "reply.md").write_text("nothing to do\n", encoding="utf-8")


async def run_skip_bad_output(context):
    await context.skip("nothing_to_do")
    (context.output_dir / "result.json").write_text("{not json", encoding="utf-8")


async def run_connection_token(context):
    """接続 token を取り直す: 期限まで余裕があれば 2 回目は前回の値 (runner に行かない)、束ねていない slot は失敗。"""
    first = await context.connection_token("gitlab")
    second = await context.connection_token("gitlab")
    try:
        await context.connection_token("slack")
        unbound = "no-error"
    except Exception as e:  # noqa: BLE001
        unbound = type(e).__name__
    (context.output_dir / "reply.md").write_text(
        f"first={first['access_token']} second={second['access_token']} type={first['token_type']} unbound={unbound}\n",
        encoding="utf-8")


async def run_gate_decision(context):
    """確認の決定を回答に書き出す（無ければnone）。書き換えられないことと、manifestに本文が無いことも書く。"""
    gd = context.gate_decision
    if gd is None:
        text = "none"
    else:
        try:
            gd["note"] = "changed"
            writable = True
        except TypeError:
            writable = False
        text = "|".join([gd["gate_id"], gd["decision"], gd["decided_by"], str(gd["note"]), str(gd["decided_at"]),
                         f"writable={writable}", f"manifest={sorted(context.manifest['gate_decision'].items())}"])
    (context.output_dir / "reply.md").write_text(text + "\n", encoding="utf-8")


async def run_start_input(context):
    """runの開始の入力を回答に書き出す（無ければnone）。書き換えられないことも書く。"""
    si = context.start_input
    if si is None:
        text = "none"
    else:
        try:
            si["kind"] = "changed"
            writable = True
        except TypeError:
            writable = False
        text = json.dumps({**dict(si), "writable": writable, "in_manifest": "start_input" in context.manifest},
                          ensure_ascii=False, sort_keys=True)
    (context.output_dir / "reply.md").write_text(text + "\n", encoding="utf-8")


async def run_connection_token_expiring(context):
    """期限まで min_ttl を切った token は毎回取り直す。"""
    a = await context.connection_token("gitlab", min_ttl=3600 * 2)
    b = await context.connection_token("gitlab", min_ttl=3600 * 2)
    (context.output_dir / "reply.md").write_text(f"{a['access_token']} {b['access_token']}\n", encoding="utf-8")


async def run_read_wait_then_effect(context):
    """read を承認された後、効果を送る前に待つ（その間に取消 / run の終端が入る試験用）。"""
    inv = await context.audit.tool_invoked("read_instructions", effect_kind="read", target="instructions.md")
    (context.output_dir / "reply.md").write_text("read\n", encoding="utf-8")
    await asyncio.sleep(1.5)
    await context.audit.tool_effect(inv, status="ok", count=1)


async def run_nan_metadata(context):
    """監査の metadata に送れない値（NaN / Infinity）を入れる。SDK はキーごと捨てて警告し、残りは送る。"""
    inv = await context.audit.tool_invoked("read_instructions", effect_kind="read", target="instructions.md",
                                           score=float("nan"), ratio=float("inf"), note="kept")
    await context.audit.tool_effect(inv, status="ok", count=1)
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")


async def _raw_call(context, op, **payload):
    """制御チャネルへ ensure_ascii=True の JSON を直接書いて応答を待つ（孤立したサロゲートも \\ud800 で書ける）。"""
    ipc = context._ipc
    ipc._ensure_reader()
    rid = next(ipc._ids)
    fut = asyncio.get_running_loop().create_future()
    ipc._pending[rid] = fut
    try:
        await asyncio.get_running_loop().run_in_executor(
            None, ipc._write_frame, json.dumps({"id": rid, "op": op, **payload}).encode("ascii") + b"\n")
        return await fut
    finally:
        ipc._pending.pop(rid, None)


def _raw_frame(context, line: bytes) -> None:
    """応答を待たない 1 行（runner が読み捨てるはずの行）。"""
    context._ipc._write_frame(line + b"\n")


async def run_raw_ipc_bad_audit(context):
    """SDK を通らずに制御チャネルへ、送れない値（NaN・孤立したサロゲート）、形の違う event、深い入れ子、
    整数でない id、読めない深さの行を書く。runner は落ちず、送れない監査は保存できなかった監査として数える。"""
    def ev(eid, **meta):
        return {"event_id": eid, "event_type": "tool.invoked", "decision": "ok",
                "metadata": {"tool": "x", "effect_kind": "read", **meta}}
    deep: list = []
    for _ in range(600):
        deep = [deep]
    await context._ipc.call("audit", event=ev("tool-invoked-nan", v=float("nan")))
    await context._ipc.call("audit", event="not-an-object")
    await _raw_call(context, "audit", event=ev("tool-invoked-surrogate", v="\ud800"))
    await context._ipc.call("audit", event=ev("tool-invoked-deep", v=deep))   # 送れる（front が入れ子を捨てる）
    _raw_frame(context, json.dumps({"id": "\ud800", "op": "check"}).encode("ascii"))
    _raw_frame(context, b"[" * 100000 + b"]" * 100000)
    await context.is_cancel_requested()   # 上の 2 行を読み捨てた後も応答が返る
    (context.output_dir / "reply.md").write_text("ok\n", encoding="utf-8")


async def run_raw_ipc_bad_done(context):
    """制御チャネルへ直接、文字列でない error_class（NaN を含む）の done を書く。envelope には載せない。"""
    await context._ipc.call("done", status="error", error_class={"x": float("nan")})
    await asyncio.sleep(5)


async def run_raw_ipc_long_done(context):
    """front の上限（128 文字 = UTF-16 の単位）を超える error_class の done。切って載せる（超えたままだと front が
    completion ごと拒む）。parameters の product_code が "astral" なら BMP 外の文字（1 文字 = 2 単位）で送る。"""
    ec = "\U0001F600" * 100 if context.parameters.get("product_code") == "astral" else "E" * 150
    await context._ipc.call("done", status="error", error_class=ec)
    await asyncio.sleep(5)


# ----- 完遂できなかった（incomplete）と終了時の報告（3.2.1 AU-23） -----
async def run_incomplete(context):
    """指示が無い: 完遂できなかったと宣言して戻る（理由は report_completion() と同じく正規化される）。"""
    await context.incomplete("Missing-Instructions", comment="instructions.md is empty")


async def run_incomplete_then_raise(context):
    """宣言の後に例外で抜ける（incomplete のまま。報告の comment は Agent の説明）。"""
    await context.incomplete("missing_instructions", comment="no instructions")
    raise RuntimeError("boom secret-value-123")


async def run_incomplete_twice(context):
    await context.incomplete("missing_instructions", comment="first")
    await context.incomplete("bad_config", comment="second")


async def run_incomplete_long_comment(context):
    """front の上限（2,048 = UTF-16 の単位）を超える説明。BMP の外の文字は 1 文字 = 2 単位。"""
    await context.incomplete("bad_config", comment="あ" * 2000 + "\U0001F600" * 100)


async def run_incomplete_bad_reason(context):
    """理由に文章を渡す（理由コードにならないので incomplete になる）。"""
    await context.incomplete("The instructions file was empty, so nothing could be drafted", comment=None)


async def run_incomplete_with_reply(context):
    """成果物を書いてから宣言する（書いた成果物は保存される）。"""
    (context.output_dir / "reply.md").write_text("partial\n", encoding="utf-8")
    await context.incomplete("bad_config")


async def run_denied_then_incomplete(context):
    await context.audit.tool_denied("mock_send", reason="policy forbids send", reason_code="policy_denied")
    await context.incomplete("missing_instructions", comment="denied first")


async def run_incomplete_then_slow(context):
    """宣言してから待つ（その間に取消が入る試験用）。"""
    await context.incomplete("missing_instructions", comment="waiting")
    (context.output_dir / "reply.md").write_text("partial\n", encoding="utf-8")
    await asyncio.sleep(30)


async def run_raw_ipc_bad_incomplete(context):
    """SDK を通らずに制御チャネルへ、形の違う理由（object）と文字列でない comment の incomplete を書く。"""
    await context._ipc.call("incomplete", reason={"x": 1}, comment=123)


async def run_incomplete_exception_comment(context):
    """comment に例外を渡す（本文に秘密の値）。文字列でないので載せない。"""
    try:
        raise RuntimeError("token=secret-value-123 rejected")
    except RuntimeError as e:
        await context.incomplete("bad_config", comment=e)


async def run_sdk_error(context):
    """SDK の例外（URL の query・応答の本文に秘密の値）。報告に出るのはクラス名・error_code・ホスト名だけ。"""
    import httpx

    from agenticstar_platform.security.base import SecurityAPIError
    request = httpx.Request("POST", "https://example.services.ai.azure.com/contentsafety/text:analyze?key=SECRET-KEY-1")
    try:
        raise httpx.ProxyError("503 body-secret-2", request=request)
    except httpx.RequestError as e:  # SDK の azure.py と同じく except の中で変換する（暗黙の __context__）
        raise SecurityAPIError(f"failed: {e}", error_code="REQUEST_ERROR")  # noqa: B904


async def run_error_long_class_name(context):
    """クラス名が front の上限を超える例外（error_class は 128、報告の comment は 2,048 単位で切る）。"""
    raise type("E" * 3000, (RuntimeError,), {})("secret-value-123")


# ----- 公開の偽物（3.2.1 AU-24） -----
async def run_custom_contract(context):
    """偽物に渡した契約・parameters・入力・接続を使う Agent。"""
    brief = json.loads((context.work_dir / "in" / "brief.json").read_text(encoding="utf-8"))
    token = await context.connection_token("crm")
    inv = await context.audit.tool_invoked("read_brief", effect_kind="read", target="in/brief.json")
    await context.audit.tool_effect(inv, status="ok", count=1)
    (context.output_dir / "summary.txt").write_text(
        f"{brief['topic']}|{context.parameters['tone']}|{token['access_token']}|{token['expires_at']}|{context.effect_mode}\n",
        encoding="utf-8")
