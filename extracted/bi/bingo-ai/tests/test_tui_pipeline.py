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
