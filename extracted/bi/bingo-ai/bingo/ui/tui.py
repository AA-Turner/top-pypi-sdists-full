"""풀스크린 TUI 셸 — Claude Code 스타일 하단 고정 입력창.

구성:
- 상단: 스크롤되는 출력 영역. Rich Console(file=self, force_terminal=True)로
  받은 ANSI를 버퍼에 누적하고 prompt_toolkit의 ANSI() 로 렌더한다.
- 하단: 항상 고정된 입력창(TextArea). 명령 실행 중에도 유지된다.
- 실행: 제출된 입력을 백그라운드 스레드에서 처리하므로 도는 동안에도
  입력창이 반응한다. Esc / Ctrl-C 로 협조적 취소(CancelToken).

TUI 는 순수 셸이다. 라우팅·실행·슬래시 처리는 cli.py 가 주입한
`handle_input(text, ui)` 콜백이 담당한다. TUI 는 출력 Console 과
CancelToken 을 소유하고 콜백에 넘긴다.
"""
from __future__ import annotations

import shutil
import threading
from typing import Callable

from rich.console import Console

from ..engine.cancel import CancelToken

# 출력 버퍼 상한 — 넘으면 앞부분을 잘라 렌더 비용/메모리를 제한한다.
_BUFFER_CAP = 400_000
_BUFFER_KEEP = 300_000

# 슬래시 명령 — "/" 입력 시 자동완성 메뉴에 설명과 함께 노출.
# cli._dispatch_input 이 실제 처리를 담당한다(여기는 표시용 목록).
# 설명 텍스트는 언어별 i18n 키로 런타임에 채운다(_build_slash_commands).
_SLASH_STRING_KEYS: list[tuple[str, str]] = [
    ("/target", "tui_sc_target"),
    ("/model", "tui_sc_model"),
    ("/status", "tui_sc_status"),
    ("/clear", "tui_sc_clear"),
    ("/session", "tui_sc_session"),
    ("/help", "tui_sc_help"),
    ("/exit", "tui_sc_exit"),
]


class BingoTUI:
    """prompt_toolkit 풀스크린 애플리케이션 셸."""

    def __init__(self, config) -> None:
        self.config = config
        self.target: str = ""

        # ── i18n ───────────────────────────────────────────────────
        # 하드코딩 대신 현재 언어의 문자열 사전을 로드한다.
        from ..lang.strings import get_strings
        self.s: dict = get_strings(getattr(config, "lang", "en") or "en")
        # 슬래시 자동완성 설명(언어별)
        self._slash_commands: dict[str, str] = {
            cmd: self.s.get(key, cmd) for cmd, key in _SLASH_STRING_KEYS
        }

        # ── 출력 파이프라인 ────────────────────────────────────────
        self._buffer = ""
        self._lock = threading.Lock()
        _cols = max(40, shutil.get_terminal_size((100, 30)).columns - 2)
        # Rich 가 self.write()/self.flush() 로 ANSI 를 흘려보낸다.
        self.console = Console(
            file=self,
            force_terminal=True,
            color_system="truecolor",
            highlight=False,
            width=_cols,
            soft_wrap=False,
        )

        # ── 실행 상태 ──────────────────────────────────────────────
        self._busy = False
        self._cancel: CancelToken | None = None
        self._queue: list[str] = []
        self._history: list[str] = []

        # ── 뷰 상태 ────────────────────────────────────────────────
        self._follow = True   # True 면 항상 맨 아래(최신)를 보여줌

        # 주입되는 콜백/앱 참조 (run 에서 세팅)
        self.handle_input: Callable[[str, "BingoTUI"], None] | None = None
        # 실행 중 입력 처리: True 반환 시 실시간 힌트로 소비됨, False 면 큐잉.
        self.on_busy_input: Callable[[str], bool] | None = None
        self._on_start: Callable[["BingoTUI"], None] | None = None
        self._app = None
        self._out_window = None
        self._input_field = None

    # ── Rich file 인터페이스 ──────────────────────────────────────
    def write(self, data: str) -> int:
        if not data:
            return 0
        with self._lock:
            self._buffer += data
            if len(self._buffer) > _BUFFER_CAP:
                self._buffer = self._buffer[-_BUFFER_KEEP:]
        self._invalidate()
        return len(data)

    def flush(self) -> None:  # Rich Console 요구
        pass

    def isatty(self) -> bool:
        return False

    # ── 공개 헬퍼 (콜백에서 사용) ─────────────────────────────────
    def print(self, *args, **kwargs) -> None:
        """편의: ui.print(...) == ui.console.print(...)"""
        self.console.print(*args, **kwargs)

    @property
    def cancel_token(self) -> CancelToken | None:
        return self._cancel

    def is_cancelled(self) -> bool:
        return self._cancel is not None and self._cancel.is_set()

    def clear(self) -> None:
        with self._lock:
            self._buffer = ""
        self._follow = True
        self._invalidate()

    def reload_strings(self, config=None) -> None:
        """언어 변경 후 문자열 사전·슬래시 설명을 다시 로드."""
        if config is not None:
            self.config = config
        from ..lang.strings import get_strings
        self.s = get_strings(getattr(self.config, "lang", "en") or "en")
        self._slash_commands = {
            cmd: self.s.get(key, cmd) for cmd, key in _SLASH_STRING_KEYS
        }
        self._invalidate()

    def exit_app(self) -> None:
        app = self._app
        if app is not None:
            try:
                app.exit()
            except Exception:
                pass

    def run_in_terminal(self, fn: Callable[[], None]) -> None:
        """TUI 를 잠시 벗어나 일반 터미널에서 fn 실행 (예: /model 대화형).

        이 메서드는 워커 스레드(_worker)에서 호출된다. prompt_toolkit 의
        run_in_terminal 은 ensure_future 로 "호출 스레드의 현재 이벤트 루프"에
        코루틴을 스케줄하는데, 워커 스레드엔 실행 중인 루프가 없다. 그래서
        메인 이벤트루프(app.loop)에 run_coroutine_threadsafe 로 스케줄하고
        완료까지 블록한다. in_executor=True 로 blocking fn(rich Prompt.ask 등)이
        메인 루프를 막지 않게 한다. 이러면 앱이 alternate screen 을 벗어나
        프롬프트가 깨끗한 터미널에 단독 표시되고, 끝나면 자동으로 TUI 복귀한다.
        """
        import asyncio
        app = self._app
        loop = getattr(app, "loop", None) if app is not None else None
        if loop is not None:
            try:
                from prompt_toolkit.application.run_in_terminal import (
                    run_in_terminal as _rit,
                )

                async def _bridge():
                    # 메인 루프 컨텍스트에서 실행되므로 _rit 의 ensure_future 가
                    # 정상적으로 이 루프에 스케줄된다.
                    return await _rit(fn, in_executor=True)

                fut = asyncio.run_coroutine_threadsafe(_bridge(), loop)
                fut.result()  # fn 완료까지 워커 블록
                return
            except Exception:
                # 루프 종료 등 예외 → 폴백으로 직접 실행 (최후 안전망)
                pass
        fn()

    # ── 내부: 무효화(다시 그림) ───────────────────────────────────
    def _invalidate(self) -> None:
        app = self._app
        if app is None:
            return
        try:
            app.invalidate()  # prompt_toolkit: 스레드-세이프
        except Exception:
            pass

    # ── 렌더 콜백 ─────────────────────────────────────────────────
    def _get_output(self):
        from prompt_toolkit.formatted_text import ANSI
        if self._follow and self._out_window is not None:
            # 큰 값을 주면 prompt_toolkit 이 콘텐츠 끝으로 클램프 → 자동 스크롤
            try:
                self._out_window.vertical_scroll = 10 ** 9
            except Exception:
                pass
        with self._lock:
            return ANSI(self._buffer)

    def _get_status(self):
        from prompt_toolkit.formatted_text import ANSI
        mc = self.config.get_active_model_config()
        model = mc.display_name() if mc else self.s.get("tui_no_model", "(no model)")
        tgt = self.target or self.s.get("tui_no_target", "(no target)")
        if self._busy:
            _run = self.s.get("tui_running", "Running")
            _stop = self.s.get("tui_stop_hint", "Esc/Ctrl-C to stop")
            _live = self.s.get("tui_type_hint", "type to add a hint")
            body = f"\x1b[38;2;255;170;0m● {_run}\x1b[0m  \x1b[38;5;244m{_stop} · {_live}\x1b[0m"
        else:
            _idle = self.s.get("tui_idle", "Idle")
            body = f"\x1b[38;2;0;229;255m○ {_idle}\x1b[0m"
        _ql = self.s.get("tui_queue", "queue")
        q = f"  \x1b[38;5;244m({_ql} {len(self._queue)})\x1b[0m" if self._queue else ""
        tail = f"  \x1b[38;5;244m{model} · {tgt}\x1b[0m"
        return ANSI(f" {body}{q}{tail}")

    def _get_prompt(self):
        from prompt_toolkit.formatted_text import ANSI
        return ANSI("\x1b[38;2;0;255;65m❯\x1b[0m ")

    # ── 입력 제출 (메인 이벤트루프 스레드에서 호출됨) ─────────────
    def _on_accept(self, buff) -> bool:
        text = buff.text
        # 입력창 비우기
        buff.document = buff.document.__class__("")
        if not text.strip():
            return False
        self._history.append(text)

        low = text.strip().lower()
        # UI 고유 명령은 메인 스레드에서 즉시 처리 (앱 종료/클리어는 스레드 금지)
        if low in ("/exit", "/quit", "exit", "quit"):
            self.exit_app()
            return False
        if low == "/clear":
            self.clear()
            return False

        # 사용자 입력 에코
        self.console.print(f"[#546e7a]❯[/] {text}")

        if self._busy:
            # 실행 중: 살아있는 작업이 실시간 힌트를 받으면 즉시 주입,
            # 아니면(대화 등) 큐잉해서 끝난 뒤 실행.
            if self.on_busy_input is not None and self.on_busy_input(text):
                self.console.print(f"[#00d4aa]{self.s.get('tui_hint_injected', '↳ hint injected')}[/]")
            else:
                self._queue.append(text)
                self.console.print(f"[#546e7a]{self.s.get('tui_queued', '(busy — queued)')}[/]")
            self._invalidate()
            return False

        self._dispatch(text)
        return False

    # ── 백그라운드 실행 ───────────────────────────────────────────
    def _dispatch(self, text: str) -> None:
        if self.handle_input is None:
            self.console.print(f"[#ff1744]{self.s.get('tui_no_handler', 'Internal error: no input handler')}[/]")
            return
        self._busy = True
        self._cancel = CancelToken()
        self._invalidate()

        def _worker() -> None:
            try:
                self.handle_input(text, self)
            except Exception as e:  # 실행 중 예외는 출력만, 셸은 유지
                import traceback
                self.console.print(f"[#ff1744]Error: {e}[/]")
                self.console.print(f"[dim]{traceback.format_exc()[-400:]}[/]")
            finally:
                self._busy = False
                self._cancel = None
                self._invalidate()
                # 큐에 남은 다음 입력 처리
                if self._queue:
                    nxt = self._queue.pop(0)
                    self._dispatch(nxt)

        threading.Thread(target=_worker, daemon=True, name="bingo-task").start()

    # ── 키바인딩 ──────────────────────────────────────────────────
    def _build_keybindings(self):
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.filters import Condition
        kb = KeyBindings()

        # 실행 중일 때만 Esc 를 즉시(eager) 잡는다. prompt_toolkit 은 Esc 를
        # 이스케이프 시퀀스(방향키 등)의 첫 바이트로 의심해 기본적으로 다음
        # 키를 기다리는데, busy 일 때만 eager 로 만들면 Esc 단독으로도 즉시
        # 취소가 걸린다. 대기 중엔 eager 아니므로 좌/우 방향키 커서 이동 정상.
        _busy_cond = Condition(lambda: self._busy)

        @kb.add("c-c")
        def _(event) -> None:
            if self._busy and self._cancel is not None:
                self._cancel.set()
                self._invalidate()
            else:
                event.app.exit()

        @kb.add("escape", eager=_busy_cond)
        def _(event) -> None:
            if self._busy and self._cancel is not None:
                self._cancel.set()
                self._invalidate()

        @kb.add("c-d")
        def _(event) -> None:
            if not self._busy:
                event.app.exit()

        @kb.add("c-l")
        def _(event) -> None:
            self.clear()

        @kb.add("pageup")
        def _(event) -> None:
            self._follow = False
            if self._out_window is not None:
                self._out_window.vertical_scroll = max(
                    0, self._out_window.vertical_scroll - 10
                )

        @kb.add("pagedown")
        def _(event) -> None:
            if self._out_window is not None:
                self._out_window.vertical_scroll += 10

        @kb.add("end")
        def _(event) -> None:
            self._follow = True
            self._invalidate()

        return kb

    # ── 슬래시 자동완성 ───────────────────────────────────────────
    def _build_completer(self):
        """"/" 로 시작할 때만 슬래시 명령을 설명과 함께 제안."""
        from prompt_toolkit.completion import Completer, Completion

        _commands = self._slash_commands

        class _SlashCompleter(Completer):
            def get_completions(self, document, complete_event):
                text = document.text_before_cursor
                if not text.startswith("/"):
                    return
                word = text  # 줄 전체가 곧 명령 토큰
                for cmd, desc in _commands.items():
                    if cmd.startswith(word):
                        yield Completion(
                            cmd,
                            start_position=-len(word),
                            display=cmd,
                            display_meta=desc,
                        )

        return _SlashCompleter()

    # ── 실행 ──────────────────────────────────────────────────────
    def _build_app(self):
        from prompt_toolkit.application import Application
        from prompt_toolkit.layout import Layout
        from prompt_toolkit.layout.containers import HSplit, Window, FloatContainer, Float
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.menus import CompletionsMenu
        from prompt_toolkit.widgets import TextArea, Frame
        from prompt_toolkit.styles import Style

        self._out_window = Window(
            content=FormattedTextControl(text=self._get_output, focusable=False),
            wrap_lines=True,
        )
        status_window = Window(
            content=FormattedTextControl(text=self._get_status),
            height=1,
        )
        self._input_field = TextArea(
            height=1,
            multiline=False,
            wrap_lines=False,
            prompt=self._get_prompt,
            accept_handler=self._on_accept,
            completer=self._build_completer(),
            complete_while_typing=True,
        )
        # 하단 고정 입력창을 테두리 프레임으로 감싼다.
        input_frame = Frame(self._input_field, style="class:inputframe")

        body = HSplit([
            self._out_window,
            status_window,
            input_frame,
        ])
        # 자동완성 메뉴는 Float 로 입력창 위에 겹쳐 뜬다.
        root = FloatContainer(
            content=body,
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=8, scroll_offset=1),
                ),
            ],
        )

        style = Style.from_dict({
            "sep": "#2a2a2a",
            "inputframe": "#00ff41",
            "frame.border": "#00ff41",
            "completion-menu.completion": "bg:#1c1c1c #c9d1d9",
            "completion-menu.completion.current": "bg:#00ff41 #000000",
            "completion-menu.meta.completion": "bg:#1c1c1c #546e7a",
            "completion-menu.meta.completion.current": "bg:#00d4aa #000000",
        })

        return Application(
            layout=Layout(root, focused_element=self._input_field),
            key_bindings=self._build_keybindings(),
            style=style,
            full_screen=True,
            mouse_support=False,
        )

    def run(self) -> None:
        self._app = self._build_app()
        if self._on_start is not None:
            try:
                self._on_start(self)
            except Exception:
                pass
        self._app.run()


def run_tui(config, handle_input, on_start=None, on_busy_input=None) -> BingoTUI:
    """풀스크린 TUI 실행.

    handle_input(text, ui): 백그라운드 스레드에서 호출되는 라우팅/실행 콜백.
      ui.console 로 출력하고 ui.cancel_token 으로 협조적 취소를 감시한다.
    on_start(ui): 앱 시작 직후 1회 (배너 출력 등).
    on_busy_input(text)->bool: 실행 중 제출된 입력 처리. True 면 실시간
      힌트로 소비된 것으로 간주, False 면 TUI 가 큐잉한다.
    """
    ui = BingoTUI(config)
    ui.handle_input = handle_input
    ui._on_start = on_start
    ui.on_busy_input = on_busy_input
    ui.run()
    return ui
