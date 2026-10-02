"""WebhookEventHandler のイベント別トップレベル type 切替の検証 (#2037)。

受信側 (chatboardfront monitoring.js) はトップレベル type で処理を分岐するため、
HITL 系は "vnc_hitl_event"、PROGRESS_MESSAGE は "progress_message" へ切り替わること、
および content 形状が本体 PodWebhookSubscriber と同型であることを、
実 aiohttp サーバーで受信して確認する。
"""

import pytest

from agenticstar_platform.events import EventType, StreamingEvent
from agenticstar_platform.events.handlers import WebhookEventHandler
from agenticstar_platform.events.models import ExecutionMessage, build_content_data

aiohttp = pytest.importorskip("aiohttp")
from aiohttp import web  # noqa: E402


async def _receive_payloads(events):
    """実 HTTP サーバーを起動し、events を送信して受信ペイロード一覧を返す"""
    received = []

    async def notify(request):
        received.append(await request.json())
        return web.json_response({"ok": True})

    app = web.Application()
    app.router.add_post("/webhook/notify", notify)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]

    try:
        handler = WebhookEventHandler(
            webhook_url=f"http://127.0.0.1:{port}/webhook/notify",
            conversation_id="conv-1",
            message_id="msg-1",
            request_source="external",
        )
        for event in events:
            await handler(event)
    finally:
        await runner.cleanup()
    return received


async def test_webhook_top_level_type_routing():
    payloads = await _receive_payloads([
        StreamingEvent(EventType.PHASE_START, "e1", "処理開始"),
        StreamingEvent(
            EventType.HITL_REQUIRED_BROWSER_VNC, "e1", "VNC接続してください",
            metadata={"vnc_url": "https://vnc.example/x", "action": "connect"},
        ),
        StreamingEvent(EventType.HITL_COMPLETED, "e1", "HITL完了", metadata={"action": "done"}),
        StreamingEvent(EventType.PROGRESS_MESSAGE, "e1", "ファイルを解析中..."),
        StreamingEvent(EventType.COMPLETION_SUCCESS, "e1", "最終回答です"),
    ])

    assert len(payloads) == 5

    # 通常イベントは従来どおり append_message + {"content": ...}
    assert payloads[0]["type"] == "append_message"
    assert payloads[0]["data"]["chunk_type"] == "content"
    assert payloads[0]["data"]["content"] == {"content": "処理開始"}

    # HITL 系はトップレベル type ごと vnc_hitl_event、content は metadata 素のまま
    assert payloads[1]["type"] == "vnc_hitl_event"
    assert payloads[1]["data"]["chunk_type"] == "vnc_hitl_event"
    assert payloads[1]["data"]["content"] == {
        "vnc_url": "https://vnc.example/x", "action": "connect",
    }
    assert payloads[2]["type"] == "vnc_hitl_event"

    # PROGRESS_MESSAGE は progress_message + 独自形式 content
    assert payloads[3]["type"] == "progress_message"
    assert payloads[3]["data"]["chunk_type"] == "progress_message"
    assert payloads[3]["data"]["content"] == {"progress_message": "ファイルを解析中..."}

    # 完了イベントの finish_reason / request_source は従来互換
    assert payloads[4]["type"] == "append_message"
    assert payloads[4]["data"]["finish_reason"] == "stop"
    assert all(p["data"]["request_source"] == "external" for p in payloads)


def test_build_content_data_shapes():
    vnc = StreamingEvent(
        EventType.HITL_REQUIRED_BROWSER_VNC, "e1", "VNC", metadata={"vnc_url": "u"},
    )
    assert build_content_data(vnc, "vnc_hitl_event") == {"vnc_url": "u"}

    vnc_no_meta = StreamingEvent(EventType.HITL_COMPLETED, "e1", "done")
    assert build_content_data(vnc_no_meta, "vnc_hitl_event") == {}

    progress = StreamingEvent(EventType.PROGRESS_MESSAGE, "e1", "解析中...")
    assert build_content_data(progress, "progress_message") == {"progress_message": "解析中..."}

    normal = StreamingEvent(EventType.PHASE_START, "e1", "開始", metadata={"k": "v"})
    assert build_content_data(normal, "content") == {"content": "開始", "k": "v"}


def test_execution_message_from_streaming_event_shapes():
    """DB 保存経路 (DatabaseEventHandler が使う変換) も同じ content 形状になること"""
    msg = ExecutionMessage.from_streaming_event(
        event=StreamingEvent(
            EventType.HITL_REQUIRED_BROWSER_VNC, "e1", "VNC", metadata={"vnc_url": "u"},
        ),
        user_id="u1", conversation_id="c1", message_id="m1",
        chunk_type="vnc_hitl_event",
    )
    assert msg.chunk_type == "vnc_hitl_event"
    assert msg.content_data == {"vnc_url": "u"}

    msg = ExecutionMessage.from_streaming_event(
        event=StreamingEvent(EventType.PROGRESS_MESSAGE, "e1", "解析中..."),
        user_id="u1", conversation_id="c1", message_id="m1",
    )
    assert msg.chunk_type == "progress_message"
    assert msg.content_data == {"progress_message": "解析中..."}
