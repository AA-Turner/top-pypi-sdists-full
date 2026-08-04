"""DEV mode: a coding assistant that talks to the model directly.

Unlike PENTEST mode (which drives AgentLoop), DEV mode needs no target URL.
It streams a normal chat completion, injecting the currently-open editor file
as context. When the model returns a full updated file in a fenced block, the
app can drop it straight into the editor for the user to review and save.
"""
from __future__ import annotations

import re
import threading
from typing import Callable

_FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)

_DEV_SYSTEM = (
    "You are Bingo in DEV mode: a senior coding assistant embedded in a web "
    "IDE. Help with reading, writing, and fixing code. Be concise.\n\n"
    "The IDE streams your fenced code block straight into the editor pane as "
    "you type it, and WRITES IT TO DISK, so the chat stays clean. Rules:\n"
    "- Keep prose OUTSIDE code fences short (one or two lines).\n"
    "- On the line RIGHT BEFORE the opening fence, name the target file with "
    "`FILE: relative/path.ext` (relative to the project root). Use it for "
    "every file you create OR modify — including the currently open file.\n"
    "- Output the COMPLETE file in ONE fenced code block — no partial "
    "snippets, no ellipses, no '// ...'.\n"
    "- Put the language after the opening fence (```css, ```python, …).\n"
    "- Close the fence with ``` and do not open a second block for the same "
    "file.\n\n"
    "Example:\n"
    "Here is a minimal page.\n"
    "FILE: index.html\n"
    "```html\n"
    "<!doctype html><title>Hi</title>\n"
    "```"
)

# `FILE: path` hint that may precede a fenced block.
_FILE_HINT_RE = re.compile(r"^\s*FILE:\s*(.+?)\s*$", re.IGNORECASE)


_LANG_NAME = {"ko": "한국어", "zh": "中文", "en": "English"}


def _lang_directive(lang: str) -> str:
    """Force replies into the UI language, not whatever the user last typed."""
    name = _LANG_NAME.get(lang or "en", "English")
    return f"\n\nAlways respond in {name}, regardless of the language of the " \
           "user's message. Code, identifiers, and file paths stay as-is."


def parse_file_hint(line: str) -> str | None:
    """Return the path from a `FILE: path` line, or None."""
    m = _FILE_HINT_RE.match(line or "")
    return m.group(1).strip() if m else None


def extract_code_block(text: str) -> str | None:
    """Return the last fenced code block body, or None."""
    blocks = _FENCE_RE.findall(text or "")
    return blocks[-1].rstrip("\n") if blocks else None


class DevSession:
    """Streams a direct chat completion with optional file context.

    on_event(type, data) is called from a worker thread:
      dev_chunk {text}  · streamed tokens
      dev_done  {full}  · complete response text
      dev_error {error} · failure
    """

    def __init__(self, config, on_event: Callable[[str, dict], None]) -> None:
        self._config = config
        self._on_event = on_event
        self._thread: threading.Thread | None = None

    @property
    def running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def ask(self, user_message: str, file_name: str, file_text: str,
            history: list[dict] | None = None) -> None:
        from ..models.registry import ModelRegistry
        from ..models.base import Message

        model_cfg = self._config.get_active_model_config()
        if not model_cfg:
            self._on_event("dev_error", {"error": "No model configured."})
            return

        # DEV writes whole files; give the reply room so large files are not
        # cut off mid-block. Copy the config so pentest requests are unchanged.
        try:
            import dataclasses

            if getattr(model_cfg, "max_tokens", 0) < 16000:
                model_cfg = dataclasses.replace(model_cfg, max_tokens=16000)
        except Exception:
            pass

        ctx = ""
        if file_name and file_text:
            ctx = (
                f"\n\nCurrently open file `{file_name}`:\n"
                f"```\n{file_text}\n```"
            )
        lang = getattr(self._config, "lang", "en")
        messages = [Message(role="system",
                            content=_DEV_SYSTEM + _lang_directive(lang))]
        # Replay prior conversation so the model keeps its memory of this folder,
        # regardless of which model is now connected.
        for turn in (history or []):
            role = turn.get("role")
            content = turn.get("content")
            if role in ("user", "assistant") and content:
                messages.append(Message(role=role, content=content))
        messages.append(Message(role="user", content=user_message + ctx))

        def _run() -> None:
            full = ""
            try:
                model = ModelRegistry.build(model_cfg)
                for chunk in model.chat_stream(messages):
                    if getattr(chunk, "failure", None) or getattr(chunk, "error", None):
                        err = getattr(chunk, "error", None) or chunk.failure.message
                        self._on_event("dev_error", {"error": str(err)})
                        return
                    piece = getattr(chunk, "text", "") or ""
                    if piece:
                        full += piece
                        self._on_event("dev_chunk", {"text": piece})
            except Exception as exc:
                self._on_event("dev_error", {"error": str(exc)})
                return
            self._on_event("dev_done", {"full": full})

        self._thread = threading.Thread(target=_run, daemon=True, name="bingo-dev")
        self._thread.start()
