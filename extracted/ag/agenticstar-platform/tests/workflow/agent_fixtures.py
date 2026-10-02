"""テスト用の Agent entrypoint（子プロセスから import される）。"""
from __future__ import annotations

import asyncio
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


async def run_connection_token_expiring(context):
    """期限まで min_ttl を切った token は毎回取り直す。"""
    a = await context.connection_token("gitlab", min_ttl=3600 * 2)
    b = await context.connection_token("gitlab", min_ttl=3600 * 2)
    (context.output_dir / "reply.md").write_text(f"{a['access_token']} {b['access_token']}\n", encoding="utf-8")
