from __future__ import annotations

import asyncio
import threading
import time
from typing import TYPE_CHECKING

from .shell_stack import (
    Application,
    BeforeInput,
    Buffer,
    BufferControl,
    CompletionsMenu,
    Condition,
    ConditionalContainer,
    Dimension,
    FileHistory,
    FormattedText,
    FormattedTextControl,
    HSplit,
    KeyBindings,
    Layout,
    PROMPT_TOOLKIT_AVAILABLE,
    PromptSession,
    ScrollablePane,
    Style,
    Window,
    has_completions,
)
from .shell_ui import (
    BRAND_ACCENT,
    BRAND_ACCENT_STRONG,
    BRAND_DARK,
    BRAND_LIGHT,
    BRAND_MUTED,
    COMMAND_PALETTE_VISIBLE_ROWS,
    LIVE_DIFF_ADD_FG,
    LIVE_DIFF_CONTEXT_FG,
    LIVE_DIFF_FILE_FG,
    LIVE_DIFF_HUNK_FG,
    LIVE_DIFF_REMOVE_FG,
    USER_HISTORY_BG,
    USER_HISTORY_FG,
)

if TYPE_CHECKING:
    from .shell import ProductizedShell


def prompt_toolkit_loop_running() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


def run_prompt_toolkit_application(application):
    if prompt_toolkit_loop_running():
        return application.run(in_thread=True)
    return application.run()


def run_prompt_toolkit_prompt(session, *args, **kwargs):
    if prompt_toolkit_loop_running():
        kwargs = dict(kwargs)
        kwargs["in_thread"] = True
    return session.prompt(*args, **kwargs)


def prompt_toolkit_composer_available(shell: ProductizedShell) -> bool:
    if not PROMPT_TOOLKIT_AVAILABLE:
        return False
    return not any(
        component is None
        for component in (
            Application,
            Buffer,
            BufferControl,
            Condition,
            BeforeInput,
            ConditionalContainer,
            CompletionsMenu,
            Dimension,
            FormattedTextControl,
            HSplit,
            Layout,
            Window,
            has_completions,
        )
    )


def shell_history(shell: ProductizedShell):
    return FileHistory(str(shell.runtime.paths.state_dir / "shell-history.txt"))


def build_prompt_buffer(shell: ProductizedShell):
    from .shell import ShellCompleter

    return Buffer(
        multiline=True,
        completer=ShellCompleter(shell),
        complete_while_typing=True,
        history=shell_history(shell),
    )


def build_input_window(shell: ProductizedShell, buffer):
    return Window(
        BufferControl(
            buffer=buffer,
            input_processors=[BeforeInput("› ", style="class:composer-prefix")],
            focus_on_click=True,
        ),
        wrap_lines=True,
        dont_extend_height=True,
        height=Dimension(min=1, preferred=1, max=6),
    )


def build_command_palette(shell: ProductizedShell):
    return ConditionalContainer(
        content=CompletionsMenu(max_height=COMMAND_PALETTE_VISIBLE_ROWS, scroll_offset=1),
        filter=has_completions,
    )


def build_queue_preview_window(shell: ProductizedShell):
    return ConditionalContainer(
        content=Window(
            FormattedTextControl(lambda: shell._render_queued_followup_fragments()),
            wrap_lines=True,
            dont_extend_height=True,
        ),
        filter=Condition(lambda: bool(shell._pending_commands)),
    )


def build_divider_window(shell: ProductizedShell):
    return Window(
        FormattedTextControl([("class:composer-divider", shell._composer_divider())]),
        height=1,
        dont_extend_height=True,
    )


def build_status_window(shell: ProductizedShell):
    return Window(
        FormattedTextControl(lambda: shell._status_bar_fragments()),
        height=1,
        dont_extend_height=True,
    )


def _intent_notice_visible(shell: ProductizedShell) -> bool:
    if not shell._startup_should_surface_intent_notices():
        return False
    shell._sync_intent_runtime_notices()
    return bool(shell._intent_runtime_notices)


def _intent_notice_fragments(shell: ProductizedShell):
    if not _intent_notice_visible(shell):
        return FormattedText([])
    fragments: list[tuple[str, str]] = []
    for index, (title, body) in enumerate(shell._intent_runtime_notices):
        if index:
            fragments.append(("", "\n"))
        fragments.append(("class:intent-ready-title", title))
        fragments.append(("class:intent-ready-body", f" · {body}"))
    startup_status = _startup_status_fragments(shell)
    if startup_status:
        fragments.append(("", "\n"))
        fragments.extend(startup_status)
    return FormattedText(fragments)


def _startup_status_fragments(shell: ProductizedShell) -> list[tuple[str, str]]:
    if not shell._intent_runtime_ready_seen or shell._startup_transcript_primed:
        return []
    if shell._pending_commands:
        title = "✦ intent queue"
        body = "aegis intent is queuing the turn ↵"
    elif getattr(shell, "_startup_prime_started", False):
        title = "✦ intent recall"
        body = "aegis intent is recalling 🧠"
    else:
        title = "✦ intent recall"
        body = "aegis intent is recalling 🧠"
    return [
        ("class:intent-ready-title", title),
        ("class:intent-ready-body", f" · {body}"),
    ]


def build_intent_notice_window(shell: ProductizedShell):
    return ConditionalContainer(
        content=Window(
            FormattedTextControl(lambda: _intent_notice_fragments(shell)),
            wrap_lines=True,
            dont_extend_height=True,
        ),
        filter=Condition(lambda: _intent_notice_visible(shell)),
    )


def build_intent_notice_spacer(shell: ProductizedShell):
    return ConditionalContainer(
        content=Window(height=1, dont_extend_height=True),
        filter=Condition(lambda: _intent_notice_visible(shell)),
    )


def build_composer_body(shell: ProductizedShell, *, input_window, command_palette, top_windows=()):
    children = [
        build_intent_notice_window(shell),
        build_intent_notice_spacer(shell),
        *top_windows,
        build_status_window(shell),
        build_divider_window(shell),
        command_palette,
        input_window,
        build_divider_window(shell),
    ]
    body = HSplit(
        children
    )
    if top_windows and ScrollablePane is not None:
        return ScrollablePane(
            body,
            show_scrollbar=False,
            display_arrows=False,
        )
    return body


def _startup_transition_result(
    shell: ProductizedShell,
    *,
    buffer_text: str = "",
    idle_seconds: float = 0.0,
) -> str | None:
    if buffer_text.strip():
        return None
    if not shell._startup_intent_dispatch_ready():
        return None
    if getattr(shell, "_startup_prime_started", False):
        return None
    if not shell._startup_transcript_primed:
        ready_seen_at = getattr(shell, "_intent_runtime_ready_seen_at", None)
        if ready_seen_at is not None and time.monotonic() - ready_seen_at < 0.4:
            return None
        if shell._startup_user_turn_submitted and shell._pending_commands:
            return "__aegis.startup.prime__"
        if idle_seconds >= 1.5:
            return "__aegis.startup.prime__"
        return None
    if shell._pending_commands:
        return "__aegis.startup.dispatch-pending__"
    return None


def read_command(shell: ProductizedShell) -> str:
    if not PROMPT_TOOLKIT_AVAILABLE:
        return input(f"{shell._composer_divider()}\n› ")
    if not prompt_toolkit_composer_available(shell):
        from .shell import ShellCompleter

        session = PromptSession(
            multiline=True,
            completer=ShellCompleter(shell),
            complete_while_typing=True,
            history=shell_history(shell),
            reserve_space_for_menu=COMMAND_PALETTE_VISIBLE_ROWS,
        )
        return run_prompt_toolkit_prompt(
            session,
            shell._prompt_label(),
            style=shell._prompt_style(),
            key_bindings=shell._build_key_bindings(),
            prompt_continuation=shell._prompt_continuation(),
            erase_when_done=True,
        )

    buffer = build_prompt_buffer(shell)
    application_holder: dict[str, Application] = {}
    stop_monitor = threading.Event()
    opened_at = time.monotonic()
    last_cron_check = 0.0

    def maybe_exit_for_startup_transition() -> None:
        application = application_holder.get("app")
        if application is None:
            return
        result = _startup_transition_result(
            shell,
            buffer_text=buffer.text,
            idle_seconds=max(0.0, time.monotonic() - opened_at),
        )
        if result is None:
            return
        if result == "__aegis.startup.prime__":
            if shell._startup_prime_started:
                return
            shell._startup_prime_started = True

            def _prime_in_background() -> None:
                try:
                    shell._prime_startup_transcript_if_needed()
                finally:
                    shell._startup_prime_started = False
                    try:
                        application.exit(result="__aegis.startup.prime__")
                    except Exception:
                        return

            threading.Thread(
                target=_prime_in_background,
                name="aegis-startup-prime",
                daemon=True,
            ).start()
            application.invalidate()
            return
        try:
            application.exit(result=result)
        except Exception:
            return

    def maybe_exit_for_cron_tick() -> None:
        nonlocal last_cron_check
        application = application_holder.get("app")
        if application is None:
            return
        now = time.monotonic()
        if now - last_cron_check < 5.0:
            return
        last_cron_check = now
        if shell._startup_prime_started or not shell._startup_transcript_primed:
            return
        try:
            has_due = shell.runtime.has_due_cron_jobs(session_id=shell.session_id)
        except Exception:
            return
        if not has_due:
            return
        try:
            application.exit(result="__aegis.cron.tick__")
        except Exception:
            return

    def submit(event) -> None:
        raw_command = event.current_buffer.text
        if not raw_command.strip():
            return
        if shell._startup_should_hold_user_command(raw_command):
            event.current_buffer.append_to_history()
            shell._mark_startup_user_turn_submitted(raw_command)
            shell._enqueue_followup_command(raw_command)
            event.current_buffer.text = ""
            event.app.invalidate()
            maybe_exit_for_startup_transition()
            return
        if raw_command:
            event.current_buffer.append_to_history()
        shell._mark_startup_user_turn_submitted(raw_command)
        event.app.exit(result=raw_command)

    bindings = shell._build_key_bindings(submit=submit)
    input_window = build_input_window(shell, buffer)
    command_palette = build_command_palette(shell)
    queue_preview_window = build_queue_preview_window(shell)
    composer_body = build_composer_body(
        shell,
        input_window=input_window,
        command_palette=command_palette,
        top_windows=(queue_preview_window,),
    )
    application = Application(
        layout=Layout(composer_body, focused_element=input_window),
        key_bindings=bindings,
        style=shell._prompt_style(),
        full_screen=False,
        erase_when_done=True,
        refresh_interval=0.2,
    )
    application_holder["app"] = application

    def monitor_startup_transition() -> None:
        while not stop_monitor.is_set():
            maybe_exit_for_startup_transition()
            maybe_exit_for_cron_tick()
            if stop_monitor.wait(0.05):
                return

    threading.Thread(target=monitor_startup_transition, daemon=True).start()
    result = run_prompt_toolkit_application(application)
    stop_monitor.set()
    if result is None:
        raise EOFError
    return str(result)


def prompt_label(shell: ProductizedShell) -> str:
    divider = shell._composer_divider()
    if not PROMPT_TOOLKIT_AVAILABLE:
        return f"{divider}\n› "
    return FormattedText(
        [
            ("class:composer-divider", f"{divider}\n"),
            ("class:composer-prefix", "› "),
        ]
    )


def prompt_continuation():
    if not PROMPT_TOOLKIT_AVAILABLE:
        return "  "
    return FormattedText([("class:composer-prefix", "  ")])


def prompt_style():
    if not PROMPT_TOOLKIT_AVAILABLE:
        return None
    return Style.from_dict(prompt_style_map())


def prompt_style_map() -> dict[str, str]:
    return {
        "": f"fg:{BRAND_LIGHT}",
        "composer-divider": f"fg:{BRAND_ACCENT}",
        "composer-prefix": f"fg:{BRAND_ACCENT_STRONG} bold",
        "queue-user": f"{USER_HISTORY_FG} bg:{USER_HISTORY_BG}",
        "progress-title": f"fg:{BRAND_ACCENT} bold",
        "progress-active": f"fg:{BRAND_LIGHT}",
        "progress-active-marker": f"fg:{BRAND_MUTED} bold",
        "progress-active-detail": f"fg:{BRAND_LIGHT}",
        "progress-meta": f"fg:{BRAND_LIGHT}",
        "progress-tool": f"fg:{BRAND_LIGHT} bold",
        "progress-tool-rail": f"fg:{BRAND_DARK}",
        "progress-tool-emoji": f"fg:{BRAND_ACCENT}",
        "progress-tool-verb": f"fg:{BRAND_MUTED}",
        "progress-tool-label": f"fg:{BRAND_ACCENT_STRONG} bold",
        "progress-tool-gap": f"fg:{BRAND_LIGHT}",
        "progress-tool-body": f"fg:{BRAND_LIGHT}",
        "progress-tool-duration": f"fg:{BRAND_MUTED}",
        "progress-intent": f"fg:{BRAND_ACCENT_STRONG} bold",
        "progress-output-file": f"fg:{LIVE_DIFF_FILE_FG} bold",
        "progress-output-hunk": f"fg:{LIVE_DIFF_HUNK_FG} bold",
        "progress-output-add": f"fg:{LIVE_DIFF_ADD_FG} bold",
        "progress-output-remove": f"fg:{LIVE_DIFF_REMOVE_FG} bold",
        "progress-output-context": f"fg:{LIVE_DIFF_CONTEXT_FG}",
        "progress-output-body": f"fg:{BRAND_LIGHT}",
        "progress-queue": f"fg:{BRAND_LIGHT}",
        "progress-hint": f"fg:{BRAND_LIGHT}",
        "progress-stream": f"fg:{BRAND_ACCENT_STRONG}",
        "intent-ready-title": f"fg:{BRAND_ACCENT} bold",
        "intent-ready-body": f"fg:{BRAND_LIGHT}",
        "stream-response-body": f"fg:{BRAND_LIGHT}",
        "clarify-title": f"fg:{BRAND_ACCENT} bold",
        "clarify-question": f"fg:{BRAND_LIGHT} bold",
        "clarify-choice": f"fg:{BRAND_LIGHT}",
        "clarify-hint": f"fg:{BRAND_MUTED}",
        "completion-menu": "bg:#1b2029",
        "completion-menu.completion": f"bg:#1b2029 fg:{BRAND_LIGHT}",
        "completion-menu.completion.current": f"bg:#2a3343 fg:{BRAND_ACCENT_STRONG} bold",
        "completion-menu.meta.completion": f"bg:#1b2029 fg:{BRAND_MUTED}",
        "completion-menu.meta.completion.current": f"bg:#2a3343 fg:{BRAND_LIGHT}",
        "scrollbar.background": "bg:#1b2029",
        "scrollbar.button": f"bg:{BRAND_ACCENT}",
        "status-bar-edge": f"bg:#1b2029 fg:{BRAND_LIGHT}",
        "status-bar-model": f"bg:#1b2029 fg:{BRAND_ACCENT_STRONG} bold",
        "status-bar-sep": f"bg:#1b2029 fg:{BRAND_MUTED}",
        "status-bar-muted": f"bg:#1b2029 fg:{BRAND_LIGHT}",
        "status-bar-stream": f"bg:#1b2029 fg:{BRAND_ACCENT_STRONG} bold",
        "status-bar-level": f"bg:#1b2029 fg:{BRAND_ACCENT} bold",
        "status-bar-growth-bracket": f"bg:#1b2029 fg:{BRAND_ACCENT} bold",
        "status-bar-growth-fill": f"bg:#1b2029 fg:{BRAND_ACCENT_STRONG} bold",
        "status-bar-growth-empty": f"bg:#1b2029 fg:{BRAND_DARK}",
        "status-bar-good": "bg:#1b2029 fg:#8cc28a bold",
        "status-bar-warn": f"bg:#1b2029 fg:{BRAND_ACCENT_STRONG} bold",
        "status-bar-critical": "bg:#1b2029 fg:#e17c64 bold",
    }


def build_key_bindings(*, submit=None, allow_exit: bool = True) -> KeyBindings:
    bindings = KeyBindings()
    submit_handler = submit or (lambda event: event.current_buffer.validate_and_handle())

    @bindings.add("enter")
    def _(event) -> None:
        submit_handler(event)

    @bindings.add("escape", "enter")
    def _(event) -> None:
        event.current_buffer.insert_text("\n")

    if allow_exit:

        @bindings.add("c-c")
        def _(event) -> None:
            raise KeyboardInterrupt

        @bindings.add("c-d")
        def _(event) -> None:
            raise EOFError
    else:

        @bindings.add("c-c")
        def _(event) -> None:
            event.current_buffer.text = ""

        @bindings.add("c-d")
        def _(event) -> None:
            event.current_buffer.text = ""

    return bindings
