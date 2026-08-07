"""풀스크린 TUI 파이프라인 회귀 테스트.

검증 대상:
- CancelToken: set/is_set/raise_if_cancelled/__bool__ 계약.
- Rich→ANSI 캡처: BingoTUI.console.print 가 버퍼에 ANSI 로 쌓이고
  prompt_toolkit ANSI() 로 파싱된다.
- 백그라운드 실행: handle_input 이 워커 스레드에서 호출되고 완료 후
  _busy 가 풀린다.
- 취소 폴링: _chat_reply 가 cancel 세팅 시 청크 경계에서 중단한다.
"""
from __future__ import annotations

import time

from bingo.engine.cancel import CancelToken, CancelledError
from bingo.ui.tui import BingoTUI
from bingo.models.base import StreamChunk


# ── CancelToken 계약 ──────────────────────────────────────────────
def test_cancel_token_contract():
    tok = CancelToken()
    assert tok.is_set() is False
    assert bool(tok) is False
    tok.raise_if_cancelled()  # 미세팅 → no-op

    tok.set()
    assert tok.is_set() is True
    assert bool(tok) is True
    try:
        tok.raise_if_cancelled()
        assert False, "expected CancelledError"
    except CancelledError:
        pass

    tok.clear()
    assert tok.is_set() is False


# ── Rich→ANSI 버퍼 파이프라인 ─────────────────────────────────────
class _FakeCfg:
    lang = "ko"

    def get_active_model_config(self):
        return None


def test_tui_console_writes_ansi_to_buffer():
    ui = BingoTUI(_FakeCfg())
    ui.console.print("[#00ff41]hello[/] world")
    # 버퍼에 텍스트가 쌓이고 ANSI 이스케이프가 포함된다.
    assert "hello" in ui._buffer
    assert "world" in ui._buffer
    assert "\x1b[" in ui._buffer  # truecolor ANSI


def test_tui_get_output_parses_ansi():
    from prompt_toolkit.formatted_text import ANSI
    ui = BingoTUI(_FakeCfg())
    ui.console.print("[#00e5ff]streamed[/]")
    out = ui._get_output()
    assert isinstance(out, ANSI)


def test_tui_clear_empties_buffer():
    ui = BingoTUI(_FakeCfg())
    ui.console.print("something")
    assert ui._buffer
    ui.clear()
    assert ui._buffer == ""
    assert ui._follow is True


def test_tui_buffer_cap_trims_old_output():
    ui = BingoTUI(_FakeCfg())
    # 상한 초과로 밀어넣고 앞부분이 잘리는지 확인.
    ui.write("A" * 500_000)
    assert len(ui._buffer) <= 400_000


# ── 백그라운드 실행 러너 ──────────────────────────────────────────
def test_tui_dispatch_runs_in_background_and_clears_busy():
    ui = BingoTUI(_FakeCfg())
    seen: dict = {}

    def _handle(text, u):
        seen["text"] = text
        seen["busy_during"] = u._busy
        seen["cancel"] = u.cancel_token

    ui.handle_input = _handle
    ui._dispatch("공격해줘")

    # 워커 완료 대기 (데몬 스레드)
    for _ in range(100):
        if not ui._busy and "text" in seen:
            break
        time.sleep(0.01)

    assert seen.get("text") == "공격해줘"
    assert seen.get("busy_during") is True
    assert isinstance(seen.get("cancel"), CancelToken)
    assert ui._busy is False
    assert ui.cancel_token is None


def test_tui_queues_input_while_busy():
    ui = BingoTUI(_FakeCfg())
    order: list[str] = []
    release = {"go": False}

    def _handle(text, u):
        order.append(text)
        # 첫 작업은 release 될 때까지 붙잡아 busy 유지
        if text == "first":
            for _ in range(200):
                if release["go"]:
                    break
                time.sleep(0.01)

    ui.handle_input = _handle
    ui._dispatch("first")
    # busy 인 동안 두 번째 입력 → 큐
    for _ in range(50):
        if ui._busy:
            break
        time.sleep(0.01)
    assert ui._busy is True

    # _on_accept 를 흉내내 큐잉
    ui._queue.append("second")
    release["go"] = True

    for _ in range(200):
        if len(order) >= 2:
            break
        time.sleep(0.01)

    assert order == ["first", "second"]


# ── _chat_reply 취소 폴링 ─────────────────────────────────────────
def test_chat_reply_stops_on_cancel(monkeypatch):
    import bingo.cli as cli
    from rich.console import Console

    class SlowModel:
        def chat_stream(self, messages, **kw):
            # 무한 스트림 — cancel 로만 멈춘다.
            i = 0
            while True:
                yield StreamChunk(text=f"chunk{i} ")
                i += 1

    class Cfg:
        lang = "ko"

        def get_active_model_config(self):
            return object()

    import bingo.models.registry as reg
    monkeypatch.setattr(reg.ModelRegistry, "build", staticmethod(lambda mc: SlowModel()))

    tok = CancelToken()
    tok.set()  # 시작 전부터 취소 상태 → 첫 청크 경계에서 즉시 중단

    history: list = []
    reply = cli._chat_reply(Cfg(), Console(), history, "안녕", cancel=tok)
    # 취소로 즉시 끊겼으므로 응답은 비었거나 매우 짧고, 히스토리는 남지 않는다.
    assert reply == ""
    assert history == []


# ── 실시간 힌트: submit_hint/drain thread-safe 계약 ────────────────
def test_agentloop_submit_hint_and_drain():
    import threading
    from bingo.engine.loop import AgentLoop

    lp = AgentLoop.__new__(AgentLoop)  # __init__ 우회 (모델 불필요)
    lp._pending_injections = []
    lp._live_hints = []
    lp._live_hints_lock = threading.Lock()

    assert lp.submit_hint("   ") is False          # 빈 힌트 무시
    assert lp.submit_hint("try boolean-based sqli") is True
    assert lp.submit_hint("skip captcha") is True
    assert lp._pending_injections == []            # 아직 drain 전
    lp._drain_live_hints()
    assert len(lp._pending_injections) == 2
    assert all(p.startswith("[User Hint] ") for p in lp._pending_injections)
    assert lp._live_hints == []                    # drain 후 비움
    lp._drain_live_hints()                          # 빈 상태 idempotent


# ── 연결 실패 감지: 전송 계층 unreachable ─────────────────────────
def test_conn_fail_counter_detects_and_resets():
    from bingo.engine.loop import AgentLoop
    from bingo.engine.executor import ToolResult

    lp = AgentLoop.__new__(AgentLoop)
    lp._consecutive_conn_fail_count = 0

    # SSL 핸드셰이크 타임아웃 / HTTP_CODE:000 → 증가
    lp._update_conn_fail_counter(ToolResult(output="HTTP_CODE:000\nSSL handshake timed out"))
    assert lp._consecutive_conn_fail_count == 1
    lp._update_conn_fail_counter(ToolResult(error="curl: (35) SSL connect error"))
    assert lp._consecutive_conn_fail_count == 2
    lp._update_conn_fail_counter(ToolResult(output="curl: (28) Operation timed out"))
    assert lp._consecutive_conn_fail_count == 3

    # 진짜 HTTP 응답을 받으면 리셋 (전송이 됐다는 뜻)
    lp._update_conn_fail_counter(ToolResult(output="HTTP/1.1 200 OK\n<html>"))
    assert lp._consecutive_conn_fail_count == 0

    # 200 안에 000 문자열이 있어도, 실제 HTTP 상태가 있으면 리셋 유지
    lp._update_conn_fail_counter(ToolResult(output="HTTP/2 403 Forbidden"))
    assert lp._consecutive_conn_fail_count == 0


def test_transport_bypass_mandate_injected_langs():
    from bingo.engine.loop import AgentLoop

    for lang, needle in (("ko", "포기"), ("zh", "放弃"), ("en", "give up")):
        lp = AgentLoop.__new__(AgentLoop)
        lp.lang = lang
        lp._pending_injections = []
        lp._consecutive_conn_fail_count = 3
        lp._inject_transport_bypass_mandate()
        assert len(lp._pending_injections) == 1
        msg = lp._pending_injections[0]
        assert "STOP BLOCKED" in msg
        assert needle in msg
        # 구체적 전송 우회 지시가 들어있어야 함
        assert "http2" in msg.lower() or "HTTP/2" in msg
        assert "tlsv1" in msg.lower()


# ── TUI 실행 중 입력 라우팅: 힌트 vs 큐 ────────────────────────────
def test_tui_busy_input_routes_hint_vs_queue():
    ui = BingoTUI(_FakeCfg())
    accepted: list = []
    # 평문만 힌트로 수락 (cli._busy_input 계약 모사)
    ui.on_busy_input = lambda t: (accepted.append(t) or True) if not t.startswith("/") else False
    ui._busy = True

    # 평문 → 힌트로 소비, 큐에 안 쌓임
    ui._on_accept(_FakeBuf("boolean sqli 로 바꿔"))
    assert accepted == ["boolean sqli 로 바꿔"]
    assert ui._queue == []

    # 슬래시 명령 → 힌트 거부 → 큐잉
    ui._on_accept(_FakeBuf("/status"))
    assert ui._queue == ["/status"]


class _FakeBuf:
    """prompt_toolkit Buffer 최소 모사 — text + document 교체."""
    def __init__(self, text: str) -> None:
        self.text = text
        self.document = _FakeDoc(text)


class _FakeDoc:
    def __init__(self, text: str) -> None:
        self.text = text

    def __call__(self, text: str = ""):  # buff.document.__class__("")
        return _FakeDoc(text)


# ── run_in_terminal: 메인 루프 스케줄 vs 폴백 ─────────────────────
def test_run_in_terminal_falls_back_when_no_loop():
    """앱 루프가 없으면(비실행/워커 단독) 폴백으로 fn 을 직접 실행한다."""
    ui = BingoTUI(_FakeCfg())
    ui._app = None  # 실행 전 → loop 없음
    ran: list = []
    ui.run_in_terminal(lambda: ran.append("direct"))
    assert ran == ["direct"]


def test_run_in_terminal_schedules_onto_app_loop():
    """앱 루프가 있으면 워커 스레드가 메인 루프에 스케줄하고 fn 을 실행한다.

    실제 prompt_toolkit run_in_terminal 은 실행 중 앱을 요구하므로, 여기서는
    ui.run_in_terminal 이 워커에서 호출됐을 때 app.loop 로 코루틴을
    run_coroutine_threadsafe 스케줄해 fn 이 그 루프 위에서 도는 계약만 검증한다.
    (get_app_or_none() 이 None 이면 in_terminal 은 즉시 yield 하고 fn 을 실행)
    """
    import asyncio
    import threading

    loop = asyncio.new_event_loop()
    ready = threading.Event()

    def _run_loop():
        asyncio.set_event_loop(loop)
        loop.call_soon(ready.set)
        loop.run_forever()

    t = threading.Thread(target=_run_loop, daemon=True)
    t.start()
    ready.wait(2)

    ui = BingoTUI(_FakeCfg())

    class _FakeApp:
        pass

    app = _FakeApp()
    app.loop = loop
    ui._app = app

    ran: dict = {}

    def _fn():
        ran["thread"] = threading.current_thread().name
        ran["done"] = True

    # 워커 스레드 흉내 — 이 스레드엔 실행 중 루프 없음.
    def _worker():
        ui.run_in_terminal(_fn)

    w = threading.Thread(target=_worker, name="bingo-task")
    w.start()
    w.join(3)

    loop.call_soon_threadsafe(loop.stop)
    t.join(2)

    assert ran.get("done") is True  # fn 이 실행됨(메인 루프 경유)


# ── Esc 즉시 취소: busy-gated eager + cancel.set() ─────────────────
def test_escape_binding_busy_gated_and_cancels():
    """실행 중일 때만 Esc 를 즉시(eager) 잡고, 핸들러가 cancel.set() 을 호출한다.

    대기 중엔 eager 아니므로 방향키/편집 동작(이스케이프 시퀀스)이 보존된다.
    """
    ui = BingoTUI(_FakeCfg())
    kb = ui._build_keybindings()

    # escape 바인딩 찾기
    esc = None
    for b in kb.bindings:
        keys = [getattr(k, "value", k) for k in b.keys]
        if "escape" in keys:
            esc = b
            break
    assert esc is not None, "escape binding not found"

    # busy-gated eager — 대기 중엔 eager 아님, 실행 중엔 eager.
    ui._busy = False
    assert bool(esc.eager()) is False
    ui._busy = True
    assert bool(esc.eager()) is True

    # busy + cancel 세팅 시 핸들러가 cancel.set() 호출.
    ui._cancel = CancelToken()
    esc.handler(object())  # event 인자는 escape 핸들러에서 미사용
    assert ui._cancel.is_set() is True
