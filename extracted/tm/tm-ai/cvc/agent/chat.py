"""
cvc.agent.chat — The main agentic REPL loop.

This is the heart of the CVC Agent — a Claude Code-style interactive
coding assistant that runs in your terminal with Time Machine capabilities.

The loop:
  1. Accept user input (or slash command)
  2. Add to conversation history
  3. Send to LLM with tool definitions
  4. If LLM returns tool calls → execute each, send results back → goto 3
  5. If LLM returns text → stream and wait for next input
  6. Auto-commit at configurable intervals
  7. Push all messages to CVC context window

Features (v0.9):
  - Token-by-token streaming responses
  - Multi-file auto-context on startup
  - Diff-based editing with fuzzy matching
  - Automatic error recovery / retry loop
  - /undo command for file changes
  - Per-session cost tracking
  - Image/screenshot support
  - Persistent memory across sessions
  - Parallel tool execution
  - Tab completion for slash commands
  - .cvcignore file support
  - Session resume
  - /web command for web search
  - Git integration
"""

from __future__ import annotations
from cvc._subprocess_compat import HIDDEN_KW

import asyncio
import base64
import json
import logging
import mimetypes
import os
import sys
import time
from pathlib import Path
from typing import Any

from cvc.agent.context_autopilot import AutopilotConfig, ContextAutopilot
from cvc.agent.continuation import COMPLETION_SIGNAL, ContinuationEngine
from cvc.agent.cost_tracker import CostTracker
from cvc.agent.executor import ToolExecutor
from cvc.agent.hooks import HookEngine, HookEvent
from cvc.agent.llm import AgentLLM, RetriesExhaustedError
from cvc.agent.permissions import PermissionEngine
from cvc.agent.renderer import (
    THEME,
    StreamingRenderer,
    agent_banner,
    animate_thinking,
    console,
    get_input_with_completion,
    get_pending_paste_images,
    print_help,
    print_input_prompt,
    render_auto_commit,
    render_autopilot_action,
    render_autopilot_continuation,
    render_autopilot_diagnostics,
    render_command_output,
    render_context_health,
    render_cost_summary,
    render_diff_preview,
    render_error,
    render_git_startup_info,
    render_git_status,
    render_goodbye,
    render_info,
    render_memory,
    render_narration,
    render_status,
    render_success,
    render_thinking,
    render_thinking_done,
    render_token_usage,
    render_tool_call_result,
    render_tool_call_start,
    render_tool_call_start_with_step,
    render_tool_dud_warning,
    render_tool_error,
    render_turn_summary,
    render_undo_result,
    render_web_results,
)
from cvc.agent.sandbox import Sandbox
from cvc.agent.settings import load_settings
from cvc.agent.system_prompt import build_system_prompt
from cvc.agent.telepathy_executor import TelepathicToolExecutor
from cvc.agent.tools import AGENT_TOOLS, MODEL_CATALOG_AGENT, get_relevant_tools
from cvc.core.database import ContextDatabase
from cvc.core.models import (
    ContextMessage,
    CVCCommitRequest,
    CVCConfig,
    GlobalConfig,
)
from cvc.operations.engine import CVCEngine

logger = logging.getLogger("cvc.agent")

# Auto-commit every N assistant turns (CLI optimized for automatic persistence)
AUTO_COMMIT_INTERVAL = int(os.environ.get("CVC_AGENT_AUTO_COMMIT", "2"))  # Changed from 5 to 2 for aggressive auto-save

# ── Unstoppable Loop (v2.72.0) ──────────────────────────────────────────
# CVC inherits upstream-grade hardening: high default ceiling + grace call +
# synthetic max-iter handoff + exit-reason taxonomy. Every limit is env-
# overridable so heavy UI/refactor tasks never silently freeze mid-stream.
# Defaults are intentionally higher than upstream (90) because CVC workloads
# routinely span 50–80 tool calls per turn (multi-file edits, vibe coding).
MAX_TOOL_ITERATIONS = int(os.environ.get("CVC_MAX_AGENT_ITERATIONS", "120"))  # was 25
MAX_RETRY_ATTEMPTS = 2    # Retry failed tool calls
MAX_EMPTY_RETRIES = int(os.environ.get("CVC_MAX_EMPTY_RETRIES", "3"))         # was 1
GRACE_CALL_ENABLED = os.environ.get("CVC_GRACE_CALL", "1") not in ("0", "false", "no")

# ── Model cost tiers ────────────────────────────────────────────────────
# Premium models (Opus 4.5/4.6) cost 3x per request on GitHub Copilot.
# Tighter iteration limits + lower max_tokens to avoid burning requests.
_EXPENSIVE_MODEL_KEYWORDS = ("opus",)
_MAX_TOOL_OUTPUT_EXPENSIVE = 5000    # chars of tool output fed back to expensive models
_MAX_TOOL_OUTPUT_STANDARD = 8000     # chars for standard models (Sonnet, etc.)
_MAX_TOOL_OUTPUT_GITHUB = 6000       # chars for GitHub Copilot (token-sensitive)
_MAX_ITERS_EXPENSIVE = 10            # iteration cap for expensive models
_MAX_TOKENS_EXPENSIVE_FIRST = 4096   # first turn max_tokens for expensive models
_MAX_TOKENS_EXPENSIVE_TOOL = 8192    # tool iteration max_tokens for expensive models


def _is_expensive_model(model_name: str) -> bool:
    """Check if a model is in the expensive/premium tier (e.g. Opus)."""
    name_lower = model_name.lower()
    return any(kw in name_lower for kw in _EXPENSIVE_MODEL_KEYWORDS)


# ---------------------------------------------------------------------------
# Human-readable argument formatting for each tool type
# ---------------------------------------------------------------------------

def _extract_plan(text: str) -> tuple[str | None, str | None]:
    """
    Extract a plan block from agent response text.

    Detects patterns like:
      Plan:
        1. Read the file
        2. Fix the bug
        3. Run tests

    Returns (plan_text, remaining_narrative).
    If no plan found, returns (None, None).
    """
    import re as _re

    # Look for "Plan:" followed by numbered steps
    plan_match = _re.search(
        r'(?:^|\n)\s*(?:Plan|Steps|Approach|Strategy):\s*\n((?:\s*\d+[\.\)]\s*.+\n?)+)',
        text,
        _re.IGNORECASE | _re.MULTILINE,
    )
    if plan_match:
        plan_text = plan_match.group(0).strip()
        # Everything before the plan is narrative
        before = text[:plan_match.start()].strip()
        after = text[plan_match.end():].strip()
        narrative = (before + "\n" + after).strip() if (before or after) else None
        return plan_text, narrative

    return None, None


def _humanize_tool_args(tool_name: str, args: dict[str, Any]) -> str:
    """
    Turn raw tool arguments into a concise, human-readable description.

    Instead of  grep(pattern='mode', path='src/')
    Shows       'mode' in src/
    """
    def _short(val: Any, limit: int = 40) -> str:
        s = str(val)
        return s if len(s) <= limit else s[:limit - 1] + "…"

    def _basename(path: str) -> str:
        """Short basename or last 2 path components."""
        p = Path(path)
        parts = p.parts
        if len(parts) <= 2:
            return str(p)
        return str(Path(*parts[-2:]))

    try:
        if tool_name == "read_file":
            path = args.get("path", "")
            return _basename(path)

        elif tool_name == "write_file":
            path = args.get("path", "")
            return _basename(path)

        elif tool_name == "edit_file":
            path = args.get("path", "")
            return _basename(path)

        elif tool_name == "patch_file":
            path = args.get("path", "")
            return _basename(path)

        elif tool_name == "bash":
            cmd = args.get("command", "")
            return f"`{_short(cmd, 50)}`"

        elif tool_name == "glob":
            pattern = args.get("pattern", "")
            path = args.get("path", ".")
            if path and path != ".":
                return f"'{pattern}' in {_basename(path)}"
            return f"'{pattern}'"

        elif tool_name == "grep":
            pattern = args.get("pattern", "")
            path = args.get("path", "")
            if path:
                return f"'{_short(pattern, 30)}' in {_basename(path)}"
            return f"'{_short(pattern, 40)}'"

        elif tool_name == "list_dir":
            path = args.get("path", ".")
            return _basename(path)

        elif tool_name == "web_search":
            query = args.get("query", "")
            return f"'{_short(query, 50)}'"

        elif tool_name == "cvc_commit":
            msg = args.get("message", "")
            return f"'{_short(msg, 40)}'"

        elif tool_name == "cvc_branch":
            name = args.get("name", "")
            return name

        elif tool_name == "cvc_restore":
            ref = args.get("ref", args.get("commit", ""))
            return _short(str(ref), 20)

        elif tool_name == "cvc_merge":
            src = args.get("source", args.get("branch", ""))
            return src

        elif tool_name == "cvc_search":
            query = args.get("query", "")
            return f"'{_short(query, 40)}'"

        elif tool_name == "cvc_smart_search":
            query = args.get("query", "")
            filters = []
            if args.get("branch"):
                filters.append(f"branch={args['branch']}")
            if args.get("since"):
                filters.append(f"since={args['since']}")
            if args.get("commit_type"):
                filters.append(f"type={args['commit_type']}")
            filter_str = f" [{', '.join(filters)}]" if filters else ""
            return f"'{_short(query, 30)}'{filter_str}"

        elif tool_name == "cvc_diff":
            return ""

        elif tool_name in ("cvc_status", "cvc_log"):
            return ""

        # Fallback: show first arg value only
        if args:
            first_val = next(iter(args.values()))
            return _short(first_val, 40)
        return ""
    except Exception:
        return ""


# v2.92.10 — Tool-call dud helpers (CLI mirror of the gateway's
# _is_dud_tool_call / _ZERO_ARG_SAFE_TOOLS predicates). The CLI chat
# loop has its own dispatch path (`_execute_tools_parallel`) and was
# missing dedup that the gateway's SSE/WS path gained in v2.92.4.
# Without this, MiniMax-M3 / Mistral-class models that emit
# speculative empty tool_use blocks produce:
#   - 5× yellow [cvc.agent.executor] WARNING lines in the terminal
#   - 5× "Error: write_file requires argument(s)..." in the LLM context
#   - the model sees 5× the same error and keeps retrying forever
# Now we (a) detect duds UP FRONT, (b) suppress the noisy terminal
# output, (c) collapse to one warning line per turn, (d) inject a
# single nudge into the model's context.
_ZERO_ARG_SAFE_TOOLS: frozenset[str] = frozenset({
    "ask_user",
    "cvc_status",
    "cvc_log",
    "cvc_diff",
    "cvc_search",
    "cvc_smart_search",
    "cvc_list_documents",
    "task_list",
    "think",
    "context_compact",
    "todo",
    "save_memory",
})


def _is_dud_tool_call_cli(tc) -> bool:
    """v2.92.10 — Mirror of cvc.gateway._is_dud_tool_call, kept in
    chat.py so the CLI loop doesn't need to import from gateway.py
    (gateway.py is huge and chat.py already has its own runtime).

    Returns True when the model emitted a tool_use block with empty,
    None, or otherwise unusable arguments. The CLI loop uses this to
    (a) collapse display into a single warning line per turn, (b)
    skip the executor's per-call WARNING log, (c) skip adding the
    full "Error: X requires..." string to the model context, and
    instead inject one consolidated nudge.

    Three classes of dud:
      1. arguments is None (model emitted no JSON args at all)
      2. arguments is not a dict (model emitted str/list/int instead)
      3. arguments is a dict but every required arg (per
         executor._REQUIRED_ARGS) is missing or blank
      4. arguments is a dict with all values blank / empty string
         (catches schemas not in _REQUIRED_ARGS)
    """
    args = getattr(tc, "arguments", None)
    if args is None:
        return True
    if not isinstance(args, dict):
        return True
    # Zero-arg-safe whitelist: ask_user({}), cvc_status({}), etc. are
    # valid calls the gateway/executor handle specially. Without this,
    # any legitimate no-arg call would be flagged as a dud and the
    # model would loop on the "stop emitting duds" nudge.
    if not args and getattr(tc, "name", "") in _ZERO_ARG_SAFE_TOOLS:
        return False
    if not args:
        return True
    # Per-tool required-arg check (mirrors executor._REQUIRED_ARGS)
    try:
        from cvc.agent.executor import _REQUIRED_ARGS as _RA  # type: ignore
        required = _RA.get(getattr(tc, "name", ""), ())
    except Exception:
        required = ()
    if required:
        if all(
            (args.get(r) is None)
            or (isinstance(args.get(r), str) and not args.get(r).strip())
            for r in required
        ):
            return True
    # Generic fallback: every value is blank / falsy
    if not any(
        bool(v) and (not isinstance(v, str) or v.strip())
        for v in args.values()
    ):
        return True
    return False


def _is_dud_result(result: str) -> bool:
    """v2.92.10 — Heuristic fallback for when `_is_dud_tool_call_cli`
    doesn't catch a dud but the executor returns the canonical error
    string. Used by the post-execution dedup pass — if the executor
    produced a "requires argument(s)" or "was called with no
    arguments" string, we still treat it as a dud for display and
    nudge purposes, even though we let the real executor path run.
    """
    if not result:
        return False
    head = result[:200]
    return (
        "requires argument(s)" in head
        or "was called with no arguments" in head
    )


def _is_wsl() -> bool:
    """Detect Windows Subsystem for Linux (WSL 1 and WSL 2)."""
    if not sys.platform.startswith("linux"):
        return False
    try:
        with open("/proc/version") as _f:
            return "microsoft" in _f.read().lower()
    except Exception:
        return False


def _grab_clipboard_images() -> list[tuple[str, str]]:
    """
    Grab image(s) from the system clipboard.

    Returns a list of (base64_data, mime_type) tuples.
    Priority order:
      1. WSL: powershell.exe bridge → Windows clipboard (must come first for WSL)
      2. Pillow PIL.ImageGrab       → cross-platform (Windows, macOS, native Linux+xclip)
      3. Windows ctypes CF_DIB      → zero-dependency Win32 fallback
      4. macOS: pngpaste / osascript → when PIL unavailable or fails
      5. Native Linux: xclip / wl-paste
    Returns an empty list if no image is found or clipboard contains only text/files.
    """
    import io as _io
    images: list[tuple[str, str]] = []

    # ── Strategy 1: WSL — bridge to the Windows clipboard via powershell.exe ─
    # Must come FIRST because PIL.ImageGrab uses xclip in Linux which doesn't
    # cross the WSL boundary to the Windows clipboard.
    if sys.platform.startswith("linux") and _is_wsl():
        import subprocess as _sp
        try:
            # Write clipboard image as raw PNG bytes to stdout via .NET WinForms
            _ps_script = (
                "Add-Type -AssemblyName System.Windows.Forms;"
                "Add-Type -AssemblyName System.Drawing;"
                "$img = [System.Windows.Forms.Clipboard]::GetImage();"
                "if ($img -ne $null) {"
                "  $ms = New-Object System.IO.MemoryStream;"
                "  $img.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png);"
                "  $bytes = $ms.ToArray();"
                "  $stdout = [System.Console]::OpenStandardOutput();"
                "  $stdout.Write($bytes, 0, $bytes.Length);"
                "  $stdout.Flush()"
                "}"
            )
            result = _sp.run(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", _ps_script],
                capture_output=True, timeout=8,
            )
            if result.returncode == 0 and result.stdout:
                b64 = base64.b64encode(result.stdout).decode("utf-8")
                return [(b64, "image/png")]
            logger.debug("WSL powershell.exe clipboard bridge: no image (returncode=%s)", result.returncode)
        except FileNotFoundError:
            logger.debug("WSL clipboard bridge: powershell.exe not found")
        except Exception as _e:
            logger.debug("WSL clipboard bridge failed: %s", _e)

    # ── Strategy 2: Pillow PIL.ImageGrab (Windows / macOS / native Linux) ────
    # Skip for WSL — PIL uses xclip on Linux which can't see the Windows clipboard.
    if not (sys.platform.startswith("linux") and _is_wsl()):
        try:
            from PIL import Image as _PILImage
            from PIL import ImageGrab as _ImageGrab

            grabbed = _ImageGrab.grabclipboard()
            # grabclipboard() returns:
            #   PIL.Image   → image is in clipboard  ✓
            #   list[str]   → file paths copied (not an image)
            #   None        → clipboard empty or text-only
            if isinstance(grabbed, _PILImage.Image):
                buf = _io.BytesIO()
                # Ensure RGBA/P → RGB for clean PNG encoding
                img_rgb = grabbed.convert("RGB") if grabbed.mode in ("RGBA", "P", "CMYK") else grabbed
                img_rgb.save(buf, format="PNG")
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                return [(b64, "image/png")]
            elif isinstance(grabbed, list):
                # Files were copied — load any that are images
                for fpath in grabbed:
                    try:
                        fpath_str = str(fpath)
                        ext = fpath_str.lower().rsplit(".", 1)[-1]
                        if ext in ("png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff"):
                            img = _PILImage.open(fpath_str)
                            buf = _io.BytesIO()
                            img.convert("RGB").save(buf, format="PNG")
                            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                            images.append((b64, "image/png"))
                    except Exception as _e:
                        logger.debug("Clipboard file-image load failed: %s", _e)
                if images:
                    return images
            # grabbed is None → nothing in clipboard, fall through
        except ImportError:
            logger.debug("Pillow not available for clipboard image grab (install Pillow>=10.0.0)")
        except Exception as _e:
            logger.debug("PIL.ImageGrab.grabclipboard() failed: %s", _e)

    if images:
        return images

    # ── Strategy 2b: Clipboard text is an image file path ────────────────────
    # Some apps (e.g. WhatsApp Desktop) put the file path as CF_UNICODETEXT
    # rather than CF_HDROP, so PIL.ImageGrab.grabclipboard() returns None.
    # Detect this and load the image directly from the file path.
    if sys.platform == "win32":
        _clip_text = ""
        try:
            import ctypes as _ct2
            CF_UNICODETEXT = 13
            _u32 = _ct2.windll.user32
            _k32 = _ct2.windll.kernel32
            if _u32.OpenClipboard(0):
                try:
                    h = _u32.GetClipboardData(CF_UNICODETEXT)
                    if h:
                        _k32.GlobalLock.restype = _ct2.c_wchar_p
                        _clip_text = (_k32.GlobalLock(h) or "").strip()
                        _k32.GlobalUnlock(h)
                finally:
                    _u32.CloseClipboard()
        except Exception:
            pass
        if _clip_text:
            _cp = Path(_clip_text)
            _img_exts = {"png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff"}
            if _cp.suffix.lower().lstrip(".") in _img_exts and _cp.exists():
                try:
                    from PIL import Image as _PILPath
                    img = _PILPath.open(str(_cp))
                    buf = _io.BytesIO()
                    img.convert("RGB").save(buf, format="PNG")
                    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                    return [(b64, "image/png")]
                except Exception as _e:
                    logger.debug("Clipboard file-path image load failed: %s", _e)

    # ── Strategy 3: Windows ctypes CF_DIB (requires PIL for BMP→PNG) ─────────
    if sys.platform == "win32":
        try:
            import ctypes
            import struct as _struct

            CF_DIB = 8
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            if user32.OpenClipboard(0):
                try:
                    if user32.IsClipboardFormatAvailable(CF_DIB):
                        h_data = user32.GetClipboardData(CF_DIB)
                        if h_data:
                            kernel32.GlobalLock.restype = ctypes.c_void_p
                            kernel32.GlobalSize.restype = ctypes.c_size_t  # 64-bit safe
                            ptr = kernel32.GlobalLock(h_data)
                            if ptr:
                                try:
                                    size = kernel32.GlobalSize(h_data)
                                    dib_data = ctypes.string_at(ptr, size)

                                    # Prepend BMP file header to make a valid BMP
                                    bih_size = _struct.unpack_from("<I", dib_data, 0)[0]
                                    bits_pp = _struct.unpack_from("<H", dib_data, 14)[0] if bih_size >= 16 else 24
                                    if bits_pp <= 8:
                                        clr_used = _struct.unpack_from("<I", dib_data, 32)[0] if bih_size >= 36 else 0
                                        color_table = (clr_used or (1 << bits_pp)) * 4
                                    else:
                                        color_table = 0
                                    offset = 14 + bih_size + color_table
                                    bmp_file_size = 14 + len(dib_data)
                                    bmp_header = _struct.pack("<2sIHHI", b"BM", bmp_file_size, 0, 0, offset)
                                    bmp_data = bmp_header + dib_data

                                    # PIL required for BMP→PNG (API doesn't accept BMP)
                                    try:
                                        from PIL import Image as _PILImg
                                        img = _PILImg.open(_io.BytesIO(bmp_data))
                                        buf = _io.BytesIO()
                                        img.convert("RGB").save(buf, format="PNG")
                                        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                                        images.append((b64, "image/png"))
                                    except ImportError:
                                        logger.debug(
                                            "Clipboard: ctypes got DIB data but Pillow is needed "
                                            "to convert BMP→PNG. Install Pillow>=10.0.0."
                                        )
                                finally:
                                    kernel32.GlobalUnlock(h_data)
                finally:
                    user32.CloseClipboard()
        except Exception as _e:
            logger.debug("Clipboard ctypes grab failed: %s", _e)

    if images:
        return images

    # ── Strategy 4: macOS fallbacks (pngpaste → osascript) ───────────────────
    # Used when PIL.ImageGrab is unavailable or fails to detect the image.
    if sys.platform == "darwin":
        import os as _os
        import subprocess as _sp
        import tempfile as _tempfile

        # 4a: pngpaste (brew install pngpaste) — writes PNG to stdout
        try:
            result = _sp.run(["pngpaste", "-"], capture_output=True, timeout=3)
            if result.returncode == 0 and result.stdout:
                b64 = base64.b64encode(result.stdout).decode("utf-8")
                return [(b64, "image/png")]
        except (FileNotFoundError, _sp.TimeoutExpired):
            pass
        except Exception as _e:
            logger.debug("macOS pngpaste clipboard grab failed: %s", _e)

        # 4b: osascript — write clipboard image to a temp PNG file
        # Tries PNG format first, then TIFF (Cmd+Shift+4 screenshots are TIFF)
        for _clip_type, _ext, _mime in (
            ("«class PNGf»", ".png", "image/png"),
            ("«class TIFF»", ".tiff", "image/tiff"),
        ):
            _tmppath = None
            try:
                with _tempfile.NamedTemporaryFile(suffix=_ext, delete=False) as _tmpf:
                    _tmppath = _tmpf.name
                _script = (
                    f'set tmpFile to (POSIX file "{_tmppath}")\n'
                    f'set imgData to the clipboard as {_clip_type}\n'
                    f'set tmpHandle to open for access tmpFile with write permission\n'
                    f'set eof tmpHandle to 0\n'
                    f'write imgData to tmpHandle\n'
                    f'close access tmpHandle'
                )
                result = _sp.run(
                    ["osascript", "-e", _script],
                    capture_output=True, timeout=5,
                )
                if result.returncode == 0 and _tmppath and _os.path.getsize(_tmppath) > 0:
                    with open(_tmppath, "rb") as _f:
                        raw = _f.read()
                    # Convert TIFF → PNG via PIL if available
                    if _ext == ".tiff":
                        try:
                            from PIL import Image as _PTIF
                            buf = _io.BytesIO()
                            _PTIF.open(_io.BytesIO(raw)).convert("RGB").save(buf, format="PNG")
                            raw = buf.getvalue()
                            _mime = "image/png"
                        except Exception:
                            pass  # send TIFF as-is; most APIs handle it
                    b64 = base64.b64encode(raw).decode("utf-8")
                    return [(b64, _mime)]
            except _sp.TimeoutExpired:
                pass
            except Exception as _e:
                logger.debug("macOS osascript clipboard grab (%s) failed: %s", _clip_type, _e)
            finally:
                if _tmppath:
                    try:
                        _os.unlink(_tmppath)
                    except Exception:
                        pass

    # ── Strategy 5: Native Linux subprocess (xclip / wl-paste) ──────────────
    # Not used for WSL (handled above); only for bare Linux with X11/Wayland.
    if sys.platform.startswith("linux") and not _is_wsl():
        import subprocess as _sp
        for cmd in (
            ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
            ["wl-paste", "--type", "image/png"],
        ):
            try:
                result = _sp.run(cmd, capture_output=True, timeout=2)
                if result.returncode == 0 and result.stdout:
                    b64 = base64.b64encode(result.stdout).decode("utf-8")
                    return [(b64, "image/png")]
            except (FileNotFoundError, _sp.TimeoutExpired):
                continue
            except Exception as _e:
                logger.debug("Clipboard subprocess grab failed (%s): %s", cmd[0], _e)

    return images


def _build_image_message(
    messages: list[dict[str, Any]],
    provider: str,
    b64_data: str,
    mime_type: str,
    text: str,
) -> None:
    """Append a multimodal user message with an image to the conversation."""
    if provider == "anthropic":
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": b64_data,
                    },
                },
                {"type": "text", "text": text},
            ],
        })
    elif provider == "openai":
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{b64_data}",
                    },
                },
                {"type": "text", "text": text},
            ],
        })
    else:
        # Google and others use the Anthropic-style format
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": b64_data,
                    },
                },
                {"type": "text", "text": text},
            ],
        })


class AgentSession:
    """
    Manages a single interactive coding session.

    Holds the conversation history, CVC engine, tool executor,
    and LLM client. Handles the agentic loop including tool calling,
    streaming, cost tracking, and error recovery.
    """

    def __init__(
        self,
        workspace: Path,
        config: CVCConfig,
        engine: CVCEngine,
        db: ContextDatabase,
        llm: AgentLLM,
        allowed_tools: list[str] | None = None,
        disallowed_tools: list[str] | None = None,
        resume_session=None,
    ) -> None:
        self.workspace = workspace
        self.config = config
        self.engine = engine
        self.db = db
        self.llm = llm

        # ── COGNOME memory runtime (automatic, workspace-scoped) ──────
        # Attaches the single shared memory interception point to this
        # AgentLLM.  After this line, every self.llm.chat()/chat_stream()
        # call auto-injects a compiled Engram — no user command required.
        try:
            from cvc.operations.cognome_runtime import CognomeRuntime
            self.memory_runtime = CognomeRuntime.for_engine(engine)
            self.llm.set_memory_runtime(self.memory_runtime)
        except Exception as _mem_exc:  # pragma: no cover — defensive
            logger.debug("COGNOME runtime attach deferred: %s", _mem_exc)
            self.memory_runtime = None

        # ── Permission engine (Claude Code-style) ────────────────────────
        settings = load_settings(workspace)
        perm_engine = PermissionEngine()

        # Load allow/deny/ask rules from settings files
        perm_engine.load_rules(
            allow=list(settings.allow_permissions),
            deny=list(settings.deny_permissions),
            ask=list(settings.permission_ask),
        )

        # CLI overrides (--allowedTools / --disallowedTools)
        perm_engine.add_cli_rules(
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
        )

        # Load trust mode settings
        perm_engine.load_trust_settings(
            trust_mode=settings.trust_mode,
            trusted_commands=settings.trusted_commands,
            blocked_commands=settings.blocked_commands,
        )

        self.settings = settings
        self.permission_engine = perm_engine
        self.hook_engine = HookEngine(workspace)

        # Load hooks from settings
        hooks_list = settings.hooks_flat
        if hooks_list:
            self.hook_engine.load_from_settings(hooks_list)

        self.executor = ToolExecutor(
            workspace, engine,
            permission_engine=perm_engine,
            hook_engine=self.hook_engine,
        )
        self.telepathic_executor = TelepathicToolExecutor(self.executor, engine)

        # Wire up the interactive permission prompt
        self.executor._permission_prompt_callback = self._prompt_permission

        # v2.91.43: Wire up workspace-switch callback. The executor's
        # `cvc_switch_workspace` tool calls this when the LLM wants to
        # change workspace mid-session. We re-anchor the chat class's
        # ``self.workspace`` (used for path-relative decisions and
        # display) and rebuild the executor's sandbox. Engine/llm stay
        # the same (those are project-scoped, not workspace-scoped).
        self.executor._workspace_switch_callback = self._on_workspace_switched

        # Wire up sub-agent config (provider/model/key needed by Agent tool)
        self.executor._subagent_config = {
            "provider": config.provider,
            "api_key": llm.api_key if hasattr(llm, "api_key") else "",
            "model": config.model,
            "base_url": llm._api_url if hasattr(llm, "_api_url") else "",
        }

        # ── Cognitive Hooks (Phase B, Sofia 2026-05-09) ─────────────────
        # Wires F1 (CCLE), F3 (User Model), F4 (Prompt Evolution),
        # F5 (Dreaming), F7 (Predictive Loader), F8 (Skill Graph),
        # F10 (Metacognition) into the live agent loop.
        # All failures are silent — cognitive features must never
        # block the main conversation path.
        self._cognitive_hooks: Any = None
        self._cognitive_started = False
        try:
            from cvc.operations.cognitive_hooks import CognitiveHookManager
            self._cognitive_hooks = CognitiveHookManager(
                engine=engine,
                adapter=None,  # adapter is optional; LLM-driven features no-op without it
                original_goal="",
            )
        except Exception as _ch_exc:  # pragma: no cover — defensive
            logger.debug("CognitiveHookManager attach deferred: %s", _ch_exc)

        # Wire up ask_user callback
        self.executor._ask_user_callback = self._ask_user_interactive

        # Restore cost tracker from previous session if resuming
        if resume_session is not None:
            restored = resume_session.restore_cost_tracker()
            if restored:
                restored.model = config.model
                self.cost_tracker = restored
            else:
                self.cost_tracker = CostTracker(model=config.model)
        else:
            self.cost_tracker = CostTracker(model=config.model)

        # Conversation history (OpenAI format for portability)
        self.messages: list[dict[str, Any]] = []

        # Session tracking
        self.turn_count = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self._assistant_turns_since_commit = 0

        # Turn-level prompt tracking for retry system
        self._turn_prompts: dict[int, str] = {}  # turn_id → original user input

        # Clipboard image dedup — track hash of the last clipboard image
        # we attached so we don't re-send the same screenshot on every prompt
        self._last_clipboard_hash: str | None = None

        # Extended thinking / effort level
        self._effort_level: str = os.environ.get("CVC_EFFORT_LEVEL", "")

        # Plan mode (read-only tools)
        self._plan_mode: bool = False

        # Session tracking
        from cvc.agent.sessions import create_session
        self._session = create_session(
            workspace=str(workspace),
            provider=config.provider,
            model=config.model,
            branch=engine.active_branch,
        )

        # Plugins and Skills
        try:
            from cvc.agent.plugins import discover_plugins
            self._plugins = discover_plugins(workspace)
        except Exception:
            self._plugins = []
        try:
            from cvc.agent.skills import discover_skills, filter_by_persona
            self._skills = discover_skills(workspace)
            # ── Persona-driven skill filter (v2.23.5) ────────────────
            # If a persona is active in this workspace and it has an
            # explicit `skills` list, restrict runtime auto-invoke /
            # /skill lookup to that subset. Empty list = no filter.
            self._persona_id: str = "default"
            self._persona_system_prompt: str | None = None
            try:
                from cvc.dashboard.personas_api import (
                    _get_persona,
                    get_active_persona_id,
                )
                self._persona_id = get_active_persona_id(Path(workspace))
                _persona = _get_persona(self._persona_id) if self._persona_id else None
                if _persona:
                    persona_skills = _persona.get("skills") or []
                    if persona_skills:
                        self._skills = filter_by_persona(self._skills, persona_skills)
                    sp = _persona.get("system_prompt")
                    if sp:
                        self._persona_system_prompt = str(sp)
                    logger.info(
                        "Persona '%s' active: %d skills loaded, system_prompt=%s",
                        self._persona_id, len(self._skills),
                        "yes" if self._persona_system_prompt else "no",
                    )
            except Exception as exc:
                logger.debug("Persona resolution skipped: %s", exc)
        except Exception:
            self._skills = []
            self._persona_id = "default"
            self._persona_system_prompt = None

        # Context Autopilot — self-healing context engine
        self.autopilot = ContextAutopilot(
            model=config.model,
            config=AutopilotConfig(
                enabled=os.environ.get("CVC_AUTOPILOT", "1") != "0",
            ),
        )
        self._health_bar: str = ""  # Cached health bar for the prompt

        # ── Cat 2 loop subsystems (budget / guardrails / compressor / recorder) ──
        # Wires the new agentic-loop modules and registers them so the
        # dashboard `/api/loop/state` + `cvc loop state` show live values.
        # All failures are silent — never block the chat path.
        self.continuation = ContinuationEngine()
        self._loop_budget = None
        self._loop_guardrails = None
        self._loop_compressor = None
        self._loop_recorder = None
        try:
            from cvc.agent.loop.budget import IterationBudget
            from cvc.agent.loop.guardrails import ToolCallGuardrailController
            from cvc.agent.loop.compression import ContextCompressor
            from cvc.agent.loop.trajectory import TrajectoryRecorder
            from cvc.dashboard import loop_state as _loop_state

            self._loop_budget = IterationBudget(
                max_iterations=int(os.environ.get("CVC_MAX_ITER", "200")),
            )
            self._loop_guardrails = ToolCallGuardrailController()
            self._loop_compressor = ContextCompressor()

            session_id = getattr(self._session, "session_id", None) or "session"
            traj_dir = Path.home() / ".cvc" / "trajectories"
            traj_dir.mkdir(parents=True, exist_ok=True)
            traj_path = traj_dir / f"{session_id}.jsonl"
            self._loop_recorder = TrajectoryRecorder(
                traj_path,
                enabled=os.environ.get("CVC_TRAJECTORY", "1") != "0",
            )

            _loop_state.register_loop(
                budget=self._loop_budget,
                guardrails=self._loop_guardrails,
                compressor=self._loop_compressor,
                recorder=self._loop_recorder,
            )
        except Exception as _loop_exc:  # pragma: no cover — defensive
            logger.debug("Loop subsystems attach deferred: %s", _loop_exc)


        # PERF: Build auto-context, memory, and git context in parallel
        # using threads (they're all I/O-bound file reads).
        import concurrent.futures
        auto_ctx = ""
        memory_ctx = ""
        git_ctx = ""

        def _load_auto_context():
            try:
                from cvc.agent.auto_context import build_auto_context
                return build_auto_context(workspace)
            except Exception as e:
                logger.debug("Auto-context failed: %s", e)
                return ""

        def _load_memory_context():
            try:
                from cvc.agent.memory import build_memory_context
                return build_memory_context(str(workspace))
            except Exception as e:
                logger.debug("Memory context failed: %s", e)
                return ""

        def _load_git_context():
            try:
                from cvc.agent.git_integration import format_git_status, git_status
                gs = git_status(workspace)
                if gs.get("is_git"):
                    return format_git_status(gs)
            except Exception as e:
                logger.debug("Git context failed: %s", e)
            return ""

        def _load_lessons_context():
            try:
                # Lessons stored in .cvc/lessons.md (internal, per-workspace)
                lessons_path = Path(workspace) / ".cvc" / "lessons.md"
                if lessons_path.exists():
                    return lessons_path.read_text(encoding="utf-8").strip()
            except Exception as e:
                logger.debug("Lessons context failed: %s", e)
            return ""

        def _load_instructions_context():
            try:
                from cvc.agent.instructions import load_instructions
                return load_instructions(workspace)
            except Exception as e:
                logger.debug("Instructions context failed: %s", e)
            return ""

        def _load_memory_index():
            try:
                from cvc.agent.memory import load_memory_index
                return load_memory_index(str(workspace))
            except Exception as e:
                logger.debug("Memory index failed: %s", e)
            return ""

        def _load_api_context() -> str:
            try:
                from cvc.agent.api_docs import build_api_context
                return build_api_context(workspace)
            except Exception as e:
                logger.debug("API context failed: %s", e)
            return ""

        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
            f_auto = pool.submit(_load_auto_context)
            f_mem = pool.submit(_load_memory_context)
            f_git = pool.submit(_load_git_context)
            f_lessons = pool.submit(_load_lessons_context)
            f_instructions = pool.submit(_load_instructions_context)
            f_memindex = pool.submit(_load_memory_index)
            f_apictx = pool.submit(_load_api_context)
            auto_ctx = f_auto.result(timeout=5)
            memory_ctx = f_mem.result(timeout=5)
            git_ctx = f_git.result(timeout=5)
            lessons_ctx = f_lessons.result(timeout=5)
            instructions_ctx = f_instructions.result(timeout=5)
            memory_index_ctx = f_memindex.result(timeout=5)
            api_ctx = f_apictx.result(timeout=5)

        # Token-sensitive providers: limit injected context sizes
        _is_token_sensitive = config.provider in ("github",)
        if _is_token_sensitive:
            _MAX_CTX = 3000  # chars per context section
            auto_ctx = auto_ctx[:_MAX_CTX] if len(auto_ctx) > _MAX_CTX else auto_ctx
            memory_ctx = memory_ctx[:_MAX_CTX] if len(memory_ctx) > _MAX_CTX else memory_ctx
            git_ctx = git_ctx[:1500] if len(git_ctx) > 1500 else git_ctx
            lessons_ctx = lessons_ctx[:2000] if len(lessons_ctx) > 2000 else lessons_ctx
            instructions_ctx = instructions_ctx[:_MAX_CTX] if len(instructions_ctx) > _MAX_CTX else instructions_ctx
            memory_index_ctx = memory_index_ctx[:1500] if len(memory_index_ctx) > 1500 else memory_index_ctx
            api_ctx = api_ctx[:2000] if len(api_ctx) > 2000 else api_ctx

        # Build and set the system prompt
        system_prompt = build_system_prompt(
            workspace=workspace,
            provider=config.provider,
            model=config.model,
            branch=engine.active_branch,
            agent_id=config.agent_id,
            auto_context=auto_ctx,
            memory_context=memory_ctx,
            git_context=git_ctx,
            lessons_context=lessons_ctx,
            instructions_context=instructions_ctx,
            memory_index_context=memory_index_ctx,
            api_context=api_ctx,
        )
        # Persona override: if active persona supplies a system prompt, replace
        # the built one (v2.23.5). Keeps CLI in lock-step with dashboard
        # `/api/chat` persona behavior.
        if getattr(self, "_persona_system_prompt", None):
            system_prompt = self._persona_system_prompt  # type: ignore[assignment]
        self.messages.append({"role": "system", "content": system_prompt})

        # ── Cognition Compiler (Cogs) — compiled cognitive cache ─────────
        try:
            from cvc.cogs.integration import CogBridge

            cogs_enabled = os.environ.get("CVC_COGS", "1") != "0"
            cvc_root = workspace / ".cvc"
            self.cog_bridge: CogBridge | None = CogBridge(
                cvc_root=cvc_root,
                enabled=cogs_enabled,
            )
            # Wire the LLM caller — a thin async wrapper around the session's LLM
            async def _cog_llm_caller(prompt: str) -> str:
                resp = await self.llm.chat(
                    messages=[{"role": "user", "content": prompt}],
                    tools=[],
                    temperature=0.3,
                    max_tokens=4096,
                )
                return resp.text or ""

            self.cog_bridge.set_llm_caller(_cog_llm_caller)
        except Exception as exc:
            logger.debug("Cogs integration disabled: %s", exc)
            self.cog_bridge = None

        # Load existing CVC context if available
        self._load_existing_context()

    def _load_existing_context(self) -> None:
        """
        Resume policy (v2.90.6+):

        Previous CVC versions blindly replayed the entire prior conversation
        into the LLM message list on every startup. That caused a fresh
        unrelated question (e.g. "what time is it?") to land on top of a
        stale debugging session — and the model naturally tried to continue
        the prior task instead of answering the new one.

        CVC's design intent is the opposite: the Merkle DAG is for
        *on-demand* recall via `cvc_recall` / `cvc_get_context` tools, not
        for blunt context injection. So:

          - If the user explicitly opted in (`--continue` / `--resume <id>`),
            full prior conversation IS replayed (legacy behavior).
          - Otherwise, we inject ONLY a short system breadcrumb telling the
            agent that prior sessions exist and how to recall them on demand.

        The user can also bring back the old behavior per-session by setting
        env CVC_RESUME=1.
        """
        existing = self.engine.context_window
        if not existing:
            return

        # Did the user explicitly ask to continue?
        explicit_resume = bool(getattr(self, "resume_session", None)) \
            or os.environ.get("CVC_RESUME", "0") == "1"

        if not explicit_resume:
            # Lightweight breadcrumb — no replay.
            convo_count = sum(
                1 for m in existing if m.role in ("user", "assistant")
            )
            if convo_count > 0:
                self.messages.append({
                    "role": "system",
                    "content": (
                        f"[CVC Time Machine] {convo_count} message(s) from prior "
                        f"session(s) are stored in this workspace's Merkle DAG "
                        f"but are NOT injected by default. Treat the user's next "
                        f"message as a fresh request. Use the `cvc_recall` or "
                        f"`cvc_get_context` tools ONLY if the user explicitly "
                        f"references prior work, asks you to continue something, "
                        f"or the request is clearly ambiguous without history. "
                        f"Do NOT volunteer recall on simple/general queries."
                    ),
                })
            return

        # Only restore user/assistant messages.
        # Tool messages CANNOT be restored as role="tool" because the
        # preceding assistant message lacks the structured tool_calls
        # field (CVC stores it as plain text like "[Tool calls: ...]").
        # Injecting orphan tool results breaks Gemini (functionResponse
        # without functionCall) and Anthropic (tool_result without
        # tool_use), causing 0 output tokens or API errors.
        # Tool result info is already captured in the assistant message
        # summaries anyway, so no context is lost.
        conversation_msgs = [
            m for m in existing
            if m.role in ("user", "assistant")
        ]

        if not conversation_msgs:
            return

        # Token-sensitive providers get tighter history limits
        _is_token_sensitive = getattr(self, "config", None) and getattr(self.config, "provider", "") in ("github",)

        # For large histories, inject a summary of older messages
        # and the full recent messages to stay within token limits
        MAX_FULL_MESSAGES = 5 if _is_token_sensitive else 10
        MAX_MSG_PREVIEW_LEN = 50 if _is_token_sensitive else 100

        if len(conversation_msgs) > MAX_FULL_MESSAGES:
            # Summarize older messages
            older = conversation_msgs[:-MAX_FULL_MESSAGES]
            recent = conversation_msgs[-MAX_FULL_MESSAGES:]

            summary_parts = []
            for msg in older:
                if msg.role in ("user", "assistant") and msg.content:
                    preview = msg.content[:MAX_MSG_PREVIEW_LEN].replace("\n", " ")
                    summary_parts.append(f"[{msg.role}]: {preview} ... [Tool Output Omitted]")

            if summary_parts:
                # Limit summary to avoid token explosion
                _max_summary = 10 if _is_token_sensitive else 20
                summary_text = "\n".join(summary_parts[-_max_summary:])
                self.messages.append({
                    "role": "system",
                    "content": (
                        f"[CVC Time Machine] Previous session restored. "
                        f"{len(existing)} total messages.\n"
                        f"Summary of older conversation ({len(older)} messages):\n\n"
                        f"{summary_text}\n\n"
                        f"Full recent conversation follows."
                    ),
                })

            # Inject recent messages — truncate long ones for token-sensitive providers
            for msg in recent:
                content = msg.content
                if _is_token_sensitive and len(content) > 2000:
                    content = content[:2000] + "\n... (truncated for token efficiency)"
                self.messages.append({"role": msg.role, "content": content})
        else:
            # Small enough to inject everything
            self.messages.append({
                "role": "system",
                "content": (
                    f"[CVC Time Machine] Previous session restored. "
                    f"{len(existing)} messages in context history. "
                    f"Full conversation follows."
                ),
            })
            for msg in conversation_msgs:
                content = msg.content
                if _is_token_sensitive and len(content) > 2000:
                    content = content[:2000] + "\n... (truncated for token efficiency)"
                self.messages.append({"role": msg.role, "content": content})

    def _prompt_permission(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        """Interactive permission prompt — shown when a tool needs ASK_USER approval."""
        from cvc.agent.renderer import render_permission_panel

        decision = render_permission_panel(
            tool_name,
            arguments,
            trust_mode=self.permission_engine.get_trust_mode(),
        )

        # Handle trust-all escalation
        if decision == "trust_all":
            self.permission_engine.trust_all_session()
            return "allow_once"

        # Handle deny with feedback — inject feedback into conversation
        if decision.startswith("deny_feedback:"):
            feedback = decision[len("deny_feedback:"):]
            if feedback:
                # Add the user's alternative suggestion to the conversation
                self.messages.append({
                    "role": "user",
                    "content": f"I denied that action. Instead: {feedback}",
                })
            return "deny"

        return decision

    def _ask_user_interactive(
        self,
        question: str,
        options: list[str] | None = None,
    ) -> str:
        """Handle ask_user tool calls with interactive Rich prompts."""
        from rich.panel import Panel as _Panel

        console.print()
        console.print(
            _Panel(
                question,
                title="[bold #CCAA44]Agent Question[/bold #CCAA44]",
                border_style="#8B0000",
                padding=(0, 2),
            )
        )
        if options:
            from cvc.agent.menus import arrow_select
            menu_options = [(opt, opt) for opt in options]
            result = arrow_select(question, menu_options, default=0)
            return result if result is not None else "(user cancelled)"
        else:
            try:
                return input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                return "(user cancelled)"

    def _get_active_tools(self, *, iteration: int = 1, has_tool_calls: bool = False) -> list[dict]:
        """Return tool definitions, filtered by plan mode and relevance."""
        if getattr(self, "_plan_mode", False):
            from cvc.agent.tools import READ_ONLY_TOOLS
            return [
                t for t in AGENT_TOOLS
                if t["function"]["name"] in READ_ONLY_TOOLS
            ]
        # Smart tool filtering: only send relevant tools to reduce token cost
        user_query = getattr(self, "_current_user_input", "")
        if user_query:
            return get_relevant_tools(
                user_query,
                iteration=iteration,
                has_tool_calls=has_tool_calls,
            )
        return AGENT_TOOLS

    def _expand_at_mentions(self, text: str) -> str:
        """Expand @path/to/file mentions by injecting file contents."""
        import re
        mentions = re.findall(r'@([\w./\\-]+(?:\.\w+)?)', text)
        if not mentions:
            return text

        injections = []
        for mention in mentions:
            p = Path(mention)
            candidate = p if p.is_absolute() else (self.workspace / p)
            try:
                if candidate.is_file():
                    content = candidate.read_text(encoding="utf-8", errors="replace")
                    if len(content) > 20000:
                        content = content[:20000] + f"\n... (truncated, {len(content) - 20000:,} chars omitted)"
                    injections.append(f"\n\n<file path=\"{mention}\">\n{content}\n</file>")
                    render_info(f"📎  @{mention} ({len(content):,} chars)")
                elif candidate.is_dir():
                    items = sorted(candidate.iterdir())[:50]
                    listing = "\n".join(
                        f"  {item.name}{'/' if item.is_dir() else ''}"
                        for item in items
                    )
                    injections.append(f"\n\n<directory path=\"{mention}\">\n{listing}\n</directory>")
                    render_info(f"📁  @{mention} ({len(items)} items)")
            except Exception:
                pass

        if injections:
            return text + "".join(injections)
        return text

    async def run_turn(self, user_input: str) -> None:
        """
        Process one user turn through the agentic loop.

        This may involve multiple LLM calls if the model uses tools.
        Uses streaming for text responses and parallel execution for
        multiple tool calls.
        """
        self.turn_count += 1

        # ── Track current input for smart tool filtering ─────────────────
        self._current_user_input = user_input

        # ── Cognitive Hooks: lazy session_start (Phase B) ────────────────
        # Fires once per Chat instance on the first turn — injects User
        # Model + Predictive Loader context into the system prompt.
        if self._cognitive_hooks is not None and not self._cognitive_started:
            self._cognitive_started = True
            try:
                self._cognitive_hooks.original_goal = user_input
                injections = await self._cognitive_hooks.on_session_start()
                if injections:
                    payload = "\n\n".join(
                        f"[{k}]\n{v}" for k, v in injections.items() if v
                    )
                    if payload:
                        self.messages.insert(
                            0 if not self.messages else 1,
                            {"role": "system", "content": payload},
                        )
                        logger.debug(
                            "CognitiveHooks: injected %d context blocks (%d chars)",
                            len(injections), len(payload),
                        )
            except Exception as _csx:
                logger.debug("CognitiveHooks session_start failed (non-fatal): %s", _csx)

        # ── Turn tracking for retry system ───────────────────────────────
        turn_id = self.executor.start_new_turn()
        self._turn_prompts[turn_id] = user_input

        # ── @ file mentions: inject file contents ────────────────────────
        user_input = self._expand_at_mentions(user_input)

        # ── Auto-invoke matching skills ──────────────────────────────────
        if self._skills:
            from cvc.agent.skills import find_matching_skills
            matched = find_matching_skills(self._skills, user_input)
            if matched:
                try:
                    from cvc.skills.usage import bump_use
                except Exception:  # pragma: no cover
                    bump_use = None  # type: ignore
            for skill in matched:
                self.messages.append({
                    "role": "system",
                    "content": f"[Auto-Skill: {skill.name}]\n{skill.content}",
                })
                # Phase B (3.2): auto-invoked skill = content loaded → bump_use.
                if bump_use is not None:
                    try:
                        bump_use(skill.name)
                    except Exception:
                        pass

        # Add user message
        self.messages.append({"role": "user", "content": user_input})

        # Push to CVC context
        self.engine.push_message(ContextMessage(role="user", content=user_input))

        # ── Cognitive Cache pre-flight: try Cog before LLM ───────────────
        cog_handled = False
        if self.cog_bridge is not None:
            try:
                hit = await self.cog_bridge.try_cache(user_input)
                if hit is not None and not hit.is_shadow:
                    # Promoted Cog — execute directly, skip LLM entirely
                    exec_result = await hit.execute()
                    if exec_result.ok:
                        answer = str(exec_result.output)
                        console.print(
                            f"\n  [{THEME['success']}]⚡ Cog hit[/{THEME['success']}] "
                            f"[{THEME['hash']}]{hit.cog.cog_id[:12]}[/{THEME['hash']}] "
                            f"[{THEME['text_dim']}]({exec_result.elapsed_ms:.0f}ms, 0 tokens)[/{THEME['text_dim']}]"
                        )
                        self.messages.append({"role": "assistant", "content": answer})
                        self.engine.push_message(
                            ContextMessage(role="assistant", content=f"[Cog {hit.cog.cog_id[:12]}] {answer}")
                        )
                        cog_handled = True
                elif hit is not None and hit.is_shadow:
                    # Shadow Cog — run LLM normally, compare afterwards
                    shadow_result = await hit.execute()
                    self._pending_shadow = {
                        "cog_id": hit.cog.cog_id,
                        "output": shadow_result.output if shadow_result.ok else None,
                    }
            except Exception as exc:
                logger.debug("Cog cache pre-flight failed: %s", exc)

        if not cog_handled:
            await self._agentic_loop()

            # ── Shadow mode comparison ───────────────────────────────────
            shadow = getattr(self, "_pending_shadow", None)
            if shadow is not None and self.cog_bridge is not None:
                llm_text = ""
                for m in reversed(self.messages):
                    if isinstance(m, dict) and m.get("role") == "assistant":
                        llm_text = m.get("content", "")
                        break
                if shadow.get("output") is not None and llm_text:
                    try:
                        promoted = await self.cog_bridge.record_shadow_agreement(
                            shadow["cog_id"], llm_text, shadow["output"]
                        )
                        if promoted:
                            console.print(
                                f"  [{THEME['success']}]⚡ Cog promoted![/{THEME['success']}] "
                                f"[{THEME['hash']}]{shadow['cog_id'][:12]}[/{THEME['hash']}] "
                                f"[{THEME['text_dim']}]— future matching queries will skip the LLM[/{THEME['text_dim']}]"
                            )
                    except Exception as exc:
                        logger.debug("Shadow comparison failed: %s", exc)
                self._pending_shadow = None

        # Update session tracking
        import time as _t
        self._session.turn_count = self.turn_count
        self._session.last_active = _t.time()
        self._session.save_cost(self.cost_tracker)
        self._session.save()

    async def run_turn_no_append(self, user_input: str) -> None:
        """
        Like run_turn but does NOT append the user message (already added,
        e.g. with image data attached). Still increments turn count and
        pushes a text summary to CVC context.
        """
        self.turn_count += 1

        # ── Turn tracking for retry system ───────────────────────────────
        turn_id = self.executor.start_new_turn()
        self._turn_prompts[turn_id] = user_input

        # Push plain text to CVC context (image data not stored)
        self.engine.push_message(ContextMessage(role="user", content=user_input))

        await self._agentic_loop()

    async def _agentic_loop(self) -> None:
        """Core agentic loop — streams LLM responses, handles tool calls."""
        # Agentic loop
        iterations = 0
        _empty_retries = 0  # Track retries for empty responses
        _MAX_EMPTY_RETRIES = MAX_EMPTY_RETRIES  # tunable via CVC_MAX_EMPTY_RETRIES (default 3)
        _exit_reason: str = "unknown"          # upstream-parity exit-reason taxonomy
        _grace_used = False                     # one-shot final synth call after cap
        _autopilot_active = self.continuation.enabled
        _is_expensive = _is_expensive_model(self.llm.model)
        _default_max = _MAX_ITERS_EXPENSIVE if _is_expensive else MAX_TOOL_ITERATIONS
        max_iters = getattr(self, "_max_turns", 0) or (
            self.continuation.state.max_iterations if _autopilot_active
            else _default_max
        )
        if _is_expensive:
            # Cap even autopilot iterations for expensive models
            max_iters = min(max_iters, _MAX_ITERS_EXPENSIVE)

        # ── UI/UX: Action tracking for turn summary ──
        _turn_actions: list[dict[str, Any]] = []
        _total_prompt_tokens = 0
        _total_completion_tokens = 0
        _plan_display_mode = getattr(self, "_plan_display_mode", self.settings.plan_display)

        _context_overflow_retried = False  # Track context overflow auto-retry

        # v2.92.10 — Per-turn dud-nudge guard. The CLI loop now detects
        # dud tool calls (empty args / missing required args) BEFORE
        # dispatching to the executor and bypasses the real dispatch —
        # the executor's per-call `logger.warning("Tool X called with
        # missing required args…")` is silenced, the noisy terminal
        # WARNING line is collapsed into a single yellow warning, and
        # the model gets one consolidated nudge instead of N copies
        # of the same "Error: X requires argument(s)..." string in
        # its context. Reset on each new user turn (handled implicitly
        # because this is the start of a new `_run_agentic_loop`
        # invocation).
        _dud_nudge_sent_cli = False

        while iterations < max_iters:
            iterations += 1

            # ── Pre-flight context validation ─────────────────────────
            # Estimate total tokens BEFORE sending to the LLM. If the
            # payload exceeds 85% of the model's context limit, run
            # autopilot compaction NOW (not after the failed call).
            from cvc.agent.context_autopilot import estimate_messages_tokens, get_context_limit
            _est_tokens = estimate_messages_tokens(self.messages)
            _ctx_limit = get_context_limit(self.llm.model)
            if _est_tokens > _ctx_limit * 0.85:
                render_info(
                    f"Context at ~{_est_tokens:,} tokens "
                    f"({_est_tokens * 100 // _ctx_limit}% of {_ctx_limit:,} limit) "
                    f"— auto-compacting…"
                )
                self.messages, _health = self.autopilot.run(
                    self.messages, engine=self.engine
                )
                if _health.actions_taken:
                    render_autopilot_action(_health.actions_taken)
                # Re-estimate after compaction
                _est_tokens = estimate_messages_tokens(self.messages)
                if _est_tokens > _ctx_limit * 0.95:
                    render_error(
                        f"Context still at {_est_tokens:,} tokens after compaction. "
                        f"Consider starting a new session (/clear) or using /compact."
                    )
                    break

            render_thinking(model=self.llm.model)
            _thinking_task = asyncio.create_task(animate_thinking())

            try:
                # Use streaming for the response
                response_text = ""
                tool_calls = []
                prompt_tokens = 0
                completion_tokens = 0
                cache_read_tokens = 0
                gemini_parts = None
                finish_reason = ""

                streamer = StreamingRenderer()
                streaming_started = False
                _streamer_rendered = False  # True once streamer.finish() has shown the panel
                _stream_scrubber = None  # Phase D 4.8 — lazy-init StreamingContextScrubber

                # PERF: Use lower max_tokens for first turn (conversational
                # responses rarely exceed 4K). Higher for tool iterations
                # where the model needs room for analysis + planning.
                # COST: Expensive models (Opus) get tighter budgets to
                # reduce verbosity and request consumption.
                # GitHub Copilot: use moderate limits to reduce token burn.
                if _is_expensive:
                    max_tok = _MAX_TOKENS_EXPENSIVE_TOOL if iterations > 1 else _MAX_TOKENS_EXPENSIVE_FIRST
                elif self.llm.provider == "github":
                    max_tok = 8192 if iterations > 1 else 4096
                else:
                    max_tok = 16384 if iterations > 1 else 8192

                # PERF: temperature=0.5 for tool iterations (more deterministic,
                # faster decoding). 0.7 for conversational first response.
                temp = 0.5 if iterations > 1 else 0.7

                # PERF: Gemini 3 thinking level selection.
                # gemini-3-pro-preview (3.0): LOW, HIGH only
                # gemini-3.1-pro-preview (3.1): LOW, MEDIUM, HIGH
                # gemini-3-flash-preview: MINIMAL, LOW, MEDIUM, HIGH
                #
                # Strategy: SPEED FIRST for agentic use.
                # Pro models: always LOW — responds in seconds, still
                # smarter than non-thinking models.  MEDIUM adds latency
                # (~10-15s/call) and HIGH triggers Deep Think Mini
                # (several minutes).  For a coding agent doing 5-10 tool
                # iterations, LOW is the only viable option.
                # Flash: MEDIUM everywhere — Flash is inherently fast so
                # MEDIUM adds negligible latency while keeping quality.
                _is_pro = "pro" in self.llm.model and "flash" not in self.llm.model
                if _is_pro:
                    _think = "LOW"         # Pro: always LOW for speed
                else:
                    _think = "MEDIUM"      # Flash: MEDIUM (fast enough)

                async for event in self.llm.chat_stream(
                    messages=self.messages,
                    tools=self._get_active_tools(
                        iteration=iterations,
                        has_tool_calls=bool(tool_calls) or iterations > 1,
                    ),
                    temperature=temp,
                    max_tokens=max_tok,
                    thinking_level=_think,
                    effort_level=self._effort_level,
                ):
                    if event.type == "text_delta":
                        # Phase D item 4.8 — streaming PII / memory-context scrubber
                        # Strips any <memory-context> spans that may leak from the
                        # model's hidden reasoning. Silent fallback on import failure.
                        try:
                            if _stream_scrubber is None:
                                from cvc.core.memory_manager import (
                                    StreamingContextScrubber as _SCS,
                                )
                                _stream_scrubber = _SCS()
                            _visible = _stream_scrubber.feed(event.text)
                        except Exception:
                            _visible = event.text
                        if not _visible:
                            continue
                        if not streaming_started:
                            _thinking_task.cancel()  # stop elapsed counter
                            render_thinking_done()
                            streamer.start()
                            streaming_started = True
                        streamer.add_text(_visible)
                        response_text += _visible

                    elif event.type == "tool_call_start":
                        if not streaming_started:
                            # Model went straight to tool calls, no text
                            _thinking_task.cancel()
                            render_thinking_done()
                        if streaming_started:
                            # Text before tool calls = progress narration
                            # Render as lightweight narration, not a full Agent panel
                            streamer.finish(as_narration=True)
                            _streamer_rendered = True
                            streaming_started = False
                        if event.tool_call:
                            tool_calls.append(event.tool_call)

                    elif event.type == "done":
                        prompt_tokens = event.prompt_tokens
                        completion_tokens = event.completion_tokens
                        cache_read_tokens = event.cache_read_tokens
                        finish_reason = event._provider_meta.get("finish_reason", "")
                        if event._provider_meta.get("gemini_parts"):
                            gemini_parts = event._provider_meta["gemini_parts"]

                # Phase D 4.8 — flush any held-back partial tag at stream end
                try:
                    if _stream_scrubber is not None:
                        _trailing = _stream_scrubber.flush()
                        if _trailing:
                            if not streaming_started:
                                _thinking_task.cancel()
                                render_thinking_done()
                                streamer.start()
                                streaming_started = True
                            streamer.add_text(_trailing)
                            response_text += _trailing
                except Exception:
                    pass

                if streaming_started:
                    response_text = streamer.finish()
                    _streamer_rendered = True

            except Exception as exc:
                # Cancel the thinking animation FIRST so it doesn't
                # overwrite the error message with a \r line update.
                _thinking_task.cancel()
                render_thinking_done()

                # Show clean error to user (no traceback)
                error_msg = str(exc)
                # Extract just the first meaningful line for display
                first_line = error_msg.split('\n')[0]
                render_error(first_line)
                logger.debug("LLM call failed: %s", exc, exc_info=True)

                # If the inner retry loop already exhausted retries (e.g.
                # persistent 429), do NOT re-retry in this outer loop —
                # that just produces a second identical error message.
                if isinstance(exc, RetriesExhaustedError):
                    if "rate-limited" in str(exc).lower():
                        render_info(
                            "You've hit the API rate limit. "
                            "Wait a minute, or switch models: /model"
                        )
                    else:
                        render_info(
                            "All retries exhausted. Try: /model"
                        )
                    break

                # Auto-retry on transient errors (timeouts, connection, 503, 429, overloaded)
                _err_lower = str(exc).lower()
                _is_transient = (
                    "timeout" in _err_lower
                    or "connection" in _err_lower
                    or "503" in _err_lower
                    or "502" in _err_lower
                    or "429" in _err_lower
                    or "overloaded" in _err_lower
                    or "temporarily" in _err_lower
                    or "service unavailable" in _err_lower
                )
                if iterations <= 2 and _is_transient:
                    render_info("Retrying…")
                    await asyncio.sleep(1.0 if "503" in _err_lower or "429" in _err_lower else 0.3)
                    continue

                # ── Context overflow recovery ────────────────────────
                # If the error is about context/payload being too large,
                # auto-compact the conversation and retry ONCE.
                _is_context_overflow = (
                    "context" in _err_lower
                    or "too long" in _err_lower
                    or "too large" in _err_lower
                    or "too many tokens" in _err_lower
                    or "max.*token" in _err_lower
                    or "payload" in _err_lower
                    or "content length" in _err_lower
                    or "prompt is too long" in _err_lower
                    or "maximum context" in _err_lower
                    or "request too large" in _err_lower
                    or "413" in _err_lower
                )
                if _is_context_overflow and not _context_overflow_retried:
                    _context_overflow_retried = True
                    render_info(
                        "Context too large for model — auto-compacting and retrying…"
                    )
                    self.messages, _health = self.autopilot.run(
                        self.messages, engine=self.engine
                    )
                    if _health.actions_taken:
                        render_autopilot_action(_health.actions_taken)
                    continue  # Retry the LLM call with compacted context

                break
            finally:
                # Always stop the elapsed-time ticker — safe to cancel multiple times
                _thinking_task.cancel()
                render_thinking_done()  # Finalize reasoning line (idempotent)

            # Track costs
            turn_cost = self.cost_tracker.add_usage(
                prompt_tokens, completion_tokens, cache_read_tokens
            )
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            _total_prompt_tokens += prompt_tokens
            _total_completion_tokens += completion_tokens

            if tool_calls:
                # ── v2.92.10 — Dud call dedup & bypass ───────────────
                # Some streaming chat models (MiniMax-M3, Mistral, etc.)
                # emit speculative empty tool_use blocks alongside the
                # real ones. Without dedup, each dud trips the
                # executor's required-arg validator (logs a yellow
                # WARNING line) and returns the same "Error: X
                # requires argument(s)..." string — repeated N times in
                # the LLM context and N yellow WARNING lines in the
                # terminal. The model then loops on the same error.
                #
                # Fix: detect duds here, before the executor sees them,
                # bypass `_execute_tools_parallel` for duds, emit a
                # single collapsed warning, and inject one consolidated
                # nudge into the model's context. Real tool calls still
                # run through the normal path.
                _real_tool_calls = []
                _dud_tool_calls: list = []
                for _tc in tool_calls:
                    if _is_dud_tool_call_cli(_tc):
                        _dud_tool_calls.append(_tc)
                    else:
                        _real_tool_calls.append(_tc)
                if _dud_tool_calls:
                    # ── Render a single collapsed yellow warning ──
                    # Imported at module top; renderer is in
                    # cvc.agent.renderer. If for any reason the
                    # function is missing, degrade gracefully.
                    try:
                        render_tool_dud_warning(_dud_tool_calls)
                    except Exception:
                        try:
                            _names = ", ".join(
                                f"{tc.name} ({len(_dud_tool_calls)}\u00d7)"
                                for tc in _dud_tool_calls
                            )
                            render_info(
                                f"\u26a0 Dud tool calls suppressed: {_names}. "
                                "Model emitted empty args; the agent "
                                "will retry with real arguments."
                            )
                        except Exception:
                            pass
                    # ── Inject one consolidated nudge into LLM context ──
                    if not _dud_nudge_sent_cli:
                        # The model only needs to see this nudge ONCE
                        # per turn, regardless of how many duds it
                        # subsequently emits.
                        self.messages.append({
                            "role": "user",
                            "content": (
                                "[cvc: your previous tool call had empty "
                                "or missing arguments. Please re-emit "
                                "the call with the real arguments, or "
                                "skip this tool and try a different "
                                "approach. Do NOT call the same tool "
                                "again without arguments.]"
                            ),
                        })
                        _dud_nudge_sent_cli = True
                    # ── Append synthetic tool_results for each dud ──
                    # The LLM provider needs a tool_result for every
                    # tool_use_id it emitted, otherwise the next LLM
                    # call gets a "missing tool_result" error and the
                    # loop stalls. We emit a terse synthetic result so
                    # the provider contract is honoured without
                    # polluting the model with the full error string.
                    for _tc in _dud_tool_calls:
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": _tc.id,
                            "content": (
                                "[cvc: dud call suppressed — call had "
                                "empty or missing arguments. Re-emit "
                                "with real arguments or skip.]"
                            ),
                        })
                    # If EVERY tool call was a dud, skip the executor
                    # entirely and let the loop continue — the model
                    # will see the nudge + synthetic tool_results and
                    # correct on its next iteration.
                    if not _real_tool_calls:
                        continue

                # Add assistant message with tool calls to history
                # (only for the real tool calls — duds have already
                # been short-circuited above).
                if _real_tool_calls:
                    assistant_msg: dict[str, Any] = {
                        "role": "assistant",
                        "content": response_text or None,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.name,
                                    "arguments": json.dumps(tc.arguments),
                                },
                            }
                            for tc in _real_tool_calls
                        ],
                    }

                    # Store raw Gemini parts — preserves thoughtSignature for Gemini 3
                    if gemini_parts:
                        assistant_msg["_gemini_parts"] = gemini_parts

                    self.messages.append(assistant_msg)

                    # ── Push assistant tool-call message to CVC context ──
                    tool_summary = ", ".join(tc.name for tc in _real_tool_calls)
                    self.engine.push_message(
                        ContextMessage(
                            role="assistant",
                            content=(
                                (response_text + "\n\n" if response_text else "")
                                + f"[Tool calls: {tool_summary}]"
                            ),
                        )
                    )

                # Show any text the model produced before tool calls
                # Render as NARRATION (lighter styling) instead of full panel
                if response_text and not _streamer_rendered and not streamer.is_active():
                    # Check for plan block in the text
                    _plan_text, _narrative = _extract_plan(response_text)
                    if _plan_text and _plan_display_mode != "plan-quiet":
                        from cvc.agent.renderer import (
                            render_plan_approval_prompt,
                            render_plan_block,
                        )
                        render_plan_block(_plan_text, _plan_display_mode)
                        if _plan_display_mode == "plan-approve":
                            if not render_plan_approval_prompt():
                                render_info("Plan cancelled by user.")
                                break
                        if _narrative:
                            render_narration(_narrative)
                    else:
                        render_narration(response_text)
                elif response_text and _streamer_rendered:
                    # Streamer already showed it as a panel — but if tool calls follow,
                    # future iterations will use narration style
                    pass

                # Execute REAL tool calls only — duds already bypassed above.
                # If every tool call was a dud, we already `continue`d above,
                # so `_real_tool_calls` is non-empty here.
                tool_calls = _real_tool_calls
                tool_results = await self._execute_tools_parallel(tool_calls, turn_actions=_turn_actions)

                # v2.92.10 — Post-execution dud-result dedup. The
                # up-front check (`_is_dud_tool_call_cli`) catches the
                # common case (None args / empty dict / `{"path": ""}`).
                # This backstop catches the partial-fill case where the
                # model emitted one required arg empty but the others
                # filled in — `_validate_required_args` returns the
                # canonical "Error: X requires argument(s) ..." string,
                # which we now also collapse instead of letting it pollute
                # the model's context.
                _post_dud_names: list[str] = []
                for tc, result in zip(tool_calls, tool_results):
                    if _is_dud_result(result):
                        _post_dud_names.append(tc.name)

                for tc, result in zip(tool_calls, tool_results):
                    # Truncate tool results for the LLM context to prevent
                    # overwhelming the model (especially Gemini thinking models
                    # which can exhaust output budgets on massive inputs).
                    # COST: Expensive models get tighter truncation to
                    # reduce context size and avoid verbose echo-back.
                    # GitHub Copilot uses intermediate limits (token-sensitive).
                    if _is_expensive:
                        _trunc_limit = _MAX_TOOL_OUTPUT_EXPENSIVE
                    elif self.llm.provider == "github":
                        _trunc_limit = _MAX_TOOL_OUTPUT_GITHUB
                    else:
                        _trunc_limit = _MAX_TOOL_OUTPUT_STANDARD
                    # v2.92.10 — Dud-result backstop: collapse the
                    # full "Error: X requires argument(s)..." string
                    # into a one-liner before adding to context. The
                    # full error string is still rendered to terminal
                    # via `render_tool_error` inside the executor path
                    # (we don't change that — it's user-visible info),
                    # but the LLM only sees the terse nudge.
                    if _is_dud_result(result):
                        llm_result = (
                            "[cvc: dud call suppressed — call had empty "
                            "or missing arguments. Re-emit with real "
                            "arguments or skip.]"
                        )
                    else:
                        llm_result = result[:_trunc_limit] if len(result) > _trunc_limit else result
                        if len(result) > _trunc_limit:
                            llm_result += f"\n\n... (truncated, {len(result) - _trunc_limit:,} chars omitted for LLM)"

                    # Add tool result to conversation
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": llm_result,
                    })

                    # ── Push tool result to CVC context ──
                    # Truncate very large tool outputs for storage
                    stored_result = result[:4000] if len(result) > 4000 else result
                    self.engine.push_message(
                        ContextMessage(
                            role="tool",
                            content=f"[{tc.name}] {stored_result}",
                            name=tc.name,
                            tool_call_id=tc.id,
                        )
                    )

                    # Auto-read files from error messages
                    if result.startswith("Error:") and not _is_dud_result(result):
                        await self._auto_context_from_error(result)

                # v2.92.10 — One nudge per turn (backstop path). If
                # post-execution duds slipped past the up-front check
                # (partial-fills), inject the nudge here so the model
                # gets the same correction signal regardless of which
                # detection layer caught the dud.
                if _post_dud_names and not _dud_nudge_sent_cli:
                    try:
                        render_tool_dud_warning(
                            [type("_NT", (), {"name": n})() for n in _post_dud_names]
                        )
                    except Exception:
                        pass
                    self.messages.append({
                        "role": "user",
                        "content": (
                            "[cvc: your previous tool call had empty or "
                            "missing arguments. Please re-emit the call "
                            "with the real arguments, or skip this tool "
                            "and try a different approach. Do NOT call "
                            "the same tool again without arguments.]"
                        ),
                    })
                    _dud_nudge_sent_cli = True

                # Record tool calls for stall detection
                self.continuation.record_tool_calls([tc.name for tc in tool_calls])

                # Update plan tracker from tool results
                for tc, result in zip(tool_calls, tool_results):
                    self.continuation.state.plan_tracker.match_and_complete(
                        tc.name, result
                    )

                # Continue the loop — the model needs to process tool results
                continue

            else:
                # No tool calls — this is a final text response

                # ── Empty response detection & retry ──
                # If the model returned 0 output tokens (common with Gemini
                # thinking models exhausting their budget), retry with
                # a higher token limit before giving up. (v2.72.0: default
                # bumped 1→3 to match upstream resilience.)
                if not response_text and not tool_calls and _empty_retries < _MAX_EMPTY_RETRIES:
                    _empty_retries += 1
                    logger.info(
                        "Empty response from LLM (finish_reason=%s) — retry %d/%d",
                        finish_reason or "unknown", _empty_retries, _MAX_EMPTY_RETRIES,
                    )
                    # Surface gently on retries >1 so user knows we're not frozen
                    if _empty_retries >= 2:
                        try:
                            render_info(
                                f"Empty stream from model — retrying ({_empty_retries}/{_MAX_EMPTY_RETRIES})…"
                            )
                        except Exception:
                            pass
                    continue
                if not response_text and not tool_calls and _empty_retries >= _MAX_EMPTY_RETRIES:
                    _exit_reason = "empty_response_exhausted"

                if response_text:
                    # Already rendered via streaming above
                    # Add to conversation history
                    self.messages.append({
                        "role": "assistant",
                        "content": response_text,
                    })

                    # Push to CVC context
                    self.engine.push_message(
                        ContextMessage(role="assistant", content=response_text)
                    )

                    # ── Extract plan on first text response ──
                    if not self.continuation.state.plan_tracker.steps:
                        self.continuation.state.plan_tracker.extract_plan(response_text)

                # ── Autopilot Continuation Check ──────────────────────
                # If autopilot is active and the task isn't complete,
                # inject a continuation prompt to keep the loop going.
                _tool_count_this_iter = len(tool_calls)
                if self.continuation.should_continue(
                    response_text or "",
                    _tool_count_this_iter,
                    session_cost=self.cost_tracker.total_cost_usd,
                ):
                    # Cost warning check
                    _cost_msg = self.continuation.check_cost_warning(
                        self.cost_tracker.total_cost_usd
                    )
                    if _cost_msg:
                        render_info(_cost_msg)
                        if self.continuation.state.cost_paused:
                            self.continuation.disable()
                            break

                    # Build and inject continuation prompt
                    _cont_prompt = self.continuation.build_continuation_prompt(
                        response_text or ""
                    )
                    self.messages.append({
                        "role": "user",
                        "content": _cont_prompt,
                    })
                    self.engine.push_message(
                        ContextMessage(role="user", content="[autopilot continuation]")
                    )

                    # Progress display
                    _remaining = self.continuation.state.plan_tracker.get_remaining()
                    render_autopilot_continuation(
                        iteration=self.continuation.state.continuation_count,
                        remaining_steps=len(_remaining),
                        total_steps=len(self.continuation.state.plan_tracker.steps),
                    )
                    continue  # Stay in loop

                # Strip completion signal from displayed text
                if response_text and COMPLETION_SIGNAL in response_text:
                    response_text = response_text.replace(COMPLETION_SIGNAL, "").strip()
                    # Update the last message
                    if self.messages and self.messages[-1].get("role") == "assistant":
                        self.messages[-1]["content"] = response_text

                # Show turn summary (replaces plain token usage display)
                if _turn_actions:
                    render_turn_summary(
                        _turn_actions,
                        prompt_tokens=_total_prompt_tokens,
                        completion_tokens=_total_completion_tokens,
                        turn_cost=turn_cost,
                        session_cost=self.cost_tracker.total_cost_usd,
                    )
                else:
                    # No tool calls this turn — just show token usage
                    render_token_usage(
                        prompt_tokens,
                        completion_tokens,
                        cache_read_tokens,
                        turn_cost,
                        self.cost_tracker.total_cost_usd,
                    )

                if response_text:
                    _exit_reason = "final_text"
                break  # Done with this turn

        # ── Unstoppable-Loop: post-loop handoff ─────────────────────────
        # If we hit the iteration cap (upstream-parity behaviour):
        #   1. Set exit_reason = budget_exhausted
        #   2. Perform ONE grace synthesis call (no tools) so the model can
        #      summarize what was done and what remains — never freeze silent.
        #   3. Surface the exit reason to the user.
        # Trigger grace synth on EITHER cause of silent exit:
        #   • iteration ceiling hit (budget_exhausted)
        #   • model returned empty text + no tools, N retries exhausted (empty_response_exhausted)
        # Without this, the dashboard sits silent after a tool burst — exactly
        # the symptom Jai's friend hit. (v2.72.1 fix.)
        _silent_exit = (
            (iterations >= max_iters)
            or (_exit_reason == "empty_response_exhausted")
        )
        if _silent_exit and GRACE_CALL_ENABLED and not _grace_used:
            if iterations >= max_iters:
                _exit_reason = "budget_exhausted"
            _grace_used = True
            try:
                if _exit_reason == "budget_exhausted":
                    render_info(
                        f"Reached iteration ceiling ({iterations}/{max_iters}). "
                        "Asking model for a final status summary…"
                    )
                else:
                    render_info(
                        "Model returned an empty response after retries — "
                        "asking it to summarize progress and the next step…"
                    )
            except Exception:
                pass
            try:
                _synth = {
                    "role": "user",
                    "content": (
                        "[SYSTEM] Tool-iteration budget reached "
                        f"({iterations}/{max_iters}). DO NOT call any more tools. "
                        "In 6–10 lines, summarize: (a) what was completed, "
                        "(b) what is still pending, (c) the single next action "
                        "the user should take to resume. Keep it tight."
                    ),
                }
                self.messages.append(_synth)
                _grace_text = ""
                async for _ev in self.llm.chat_stream(
                    messages=self.messages,
                    tools=[],  # no tools — pure summary
                    temperature=0.3,
                    max_tokens=1024,
                    thinking_level="LOW",
                    effort_level=self._effort_level,
                ):
                    if getattr(_ev, "type", "") == "text_delta":
                        _grace_text += getattr(_ev, "text", "")
                if _grace_text.strip():
                    self.messages.append(
                        {"role": "assistant", "content": _grace_text}
                    )
                    self.engine.push_message(
                        ContextMessage(role="assistant", content=_grace_text)
                    )
                    try:
                        # Render summary so user sees it in dashboard + CLI
                        _r = StreamingRenderer()
                        _r.start()
                        _r.add_text(_grace_text)
                        _r.finish()
                    except Exception:
                        # Fallback — just info-line it
                        try:
                            render_info(_grace_text[:2000])
                        except Exception:
                            pass
            except Exception as exc:
                logger.warning("Grace synth call failed: %s", exc)

        # ── UNIVERSAL HARD FALLBACK ──────────────────────────────────────
        # Regardless of how the loop exited (final_text/budget/empty/cost/
        # autopilot-stop/etc.), if the LAST thing in the conversation is
        # NOT an assistant text message, the dashboard will render zero
        # output and freeze on the previous tool card.  This catches:
        #   • model returned one empty text turn then autopilot stopped
        #   • cost cap paused mid-turn
        #   • any future exit path we add
        # Lifted OUT of the silent_exit branch (v2.72.1.1) — must run on
        # every code path that reaches the end of the loop. (v2.72.2 fix.)
        try:
            _last = self.messages[-1] if self.messages else {}
            _last_was_assistant_text = bool(
                isinstance(_last, dict)
                and _last.get("role") == "assistant"
                and isinstance(_last.get("content"), str)
                and _last.get("content", "").strip()
            )
        except Exception:
            _last_was_assistant_text = False

        if not _last_was_assistant_text:
            _reason_human = {
                "final_text": "the model stopped without sending a reply",
                "budget_exhausted": "I hit the tool-iteration budget",
                "empty_response_exhausted": "the model returned empty responses",
                "cost_paused": "the cost cap paused this turn",
            }.get(_exit_reason, f"exit_reason={_exit_reason}")
            _fallback = (
                f"⚠️ I couldn't generate a visible reply on this turn "
                f"({_reason_human}). Your last tool calls did run — say "
                f"'continue', 'retry', or rephrase and I'll pick it back up."
            )
            try:
                self.messages.append(
                    {"role": "assistant", "content": _fallback}
                )
                try:
                    self.engine.push_message(
                        ContextMessage(role="assistant", content=_fallback)
                    )
                except Exception:
                    pass
                try:
                    _r = StreamingRenderer()
                    _r.start()
                    _r.add_text(_fallback)
                    _r.finish()
                except Exception:
                    try:
                        render_info(_fallback)
                    except Exception:
                        pass
            except Exception as _fb_exc:
                logger.error("Hard fallback emit failed: %s", _fb_exc)

        logger.info(
            "agentic_loop exit reason=%s iterations=%d/%d empty_retries=%d grace=%s",
            _exit_reason, iterations, max_iters, _empty_retries, _grace_used,
        )

        # Auto-commit check
        self._assistant_turns_since_commit += 1
        if self._assistant_turns_since_commit >= AUTO_COMMIT_INTERVAL:
            self._auto_commit()

        # ── Context Autopilot: self-healing context management ───────────
        # Runs after every turn. Monitors context health and takes
        # graduated actions (thin → compact → aggressive compact) based
        # on utilization thresholds. CVC commits before any compaction
        # so nothing is ever lost.
        try:
            self.messages, health = self.autopilot.run(
                self.messages, engine=self.engine
            )

            # Show autopilot actions if any were taken
            if health.actions_taken:
                render_autopilot_action(health.actions_taken)

            # Cache the health bar for the input prompt
            self._health_bar = health.format_bar_rich(width=15)
        except Exception as exc:
            logger.warning("Autopilot post-turn run failed: %s", exc)
            # Non-fatal — continue without autopilot actions

    async def _execute_tools_parallel(
        self, tool_calls: list, turn_actions: list[dict[str, Any]] | None = None
    ) -> list[str]:
        """
        Execute tool calls using Dynamic Telepathy Branching.
        """
        total = len(tool_calls)

        if total <= 1:
            # Single tool call — execute directly to save DB overhead
            results = []
            for i, tc in enumerate(tool_calls, 1):
                result = await self._execute_single_tool(tc, step=i, total=total, turn_actions=turn_actions)
                results.append(result)
                # Cognitive metacognition pulse
                if self._cognitive_hooks is not None:
                    try:
                        self._cognitive_hooks.on_post_tool_use(tc.name)
                    except Exception:
                        pass
            return results

        # Format tool calls for the Telepathic Executor
        telepathy_payload = [
            {"id": tc.id, "name": tc.name, "args": tc.arguments}
            for tc in tool_calls
        ]

        # Dispatch to the new Telepathic Fan-out Engine
        telepathy_results = await self.telepathic_executor.execute_parallel(telepathy_payload)

        # Cognitive metacognition pulse for parallel fan-out
        if self._cognitive_hooks is not None:
            for tc in tool_calls:
                try:
                    self._cognitive_hooks.on_post_tool_use(tc.name)
                except Exception:
                    pass

        # Extract the outputs to feed back to the LLM
        return [res.get("output", str(res.get("error", "Unknown Telepathy Error"))) for res in telepathy_results]

    async def _execute_single_tool(
        self, tc, step: int = 0, total: int = 0,
        turn_actions: list[dict[str, Any]] | None = None,
    ) -> str:
        """Execute a single tool call with error recovery, diff preview, and output panels."""
        args_summary = _humanize_tool_args(tc.name, tc.arguments)

        # Use step progress indicator when there are multiple tools
        if total > 1:
            render_tool_call_start_with_step(tc.name, args_summary, step=step, total=total)
        else:
            render_tool_call_start(tc.name, args_summary)

        start_time = time.time()
        retry_count = 0
        result = ""

        while retry_count <= MAX_RETRY_ATTEMPTS:
            try:
                # Async-offload synchronous executor (Phase B, Sofia 2026-05-09).
                # The executor's tool dispatch is sync (subprocess, file I/O,
                # network) — running it inline blocks the event loop and
                # serializes the gateway's other coroutines. to_thread keeps
                # the loop responsive while the tool runs.
                result = await asyncio.to_thread(self.executor.execute, tc.name, tc.arguments)
                elapsed = time.time() - start_time

                # Check if the result indicates a recoverable error
                if result.startswith("Error:") and retry_count < MAX_RETRY_ATTEMPTS:
                    if tc.name == "edit_file" and "not found in" in result:
                        render_tool_error(tc.name, f"Retrying with fuzzy match... ({result[:80]})")
                        retry_count += 1
                        break
                    elif "File not found" in result:
                        render_tool_error(tc.name, "File not found, cannot retry")
                        break
                    else:
                        break

                render_tool_call_result(tc.name, result, elapsed)

                # ── Diff preview after file edits ──
                if tc.name in ("edit_file", "patch_file", "write_file") and not result.startswith("Error:"):
                    last_change = self.executor.get_last_change()
                    if last_change and last_change.old_content is not None:
                        rel = str(
                            last_change.path.relative_to(self.workspace)
                            if last_change.path.is_relative_to(self.workspace)
                            else last_change.path
                        )
                        render_diff_preview(rel, last_change.old_content, last_change.new_content)

                # ── Command output panel for bash ──
                if tc.name == "bash" and not result.startswith("Error:"):
                    cmd = tc.arguments.get("command", "")
                    render_command_output(
                        cmd,
                        self.executor._last_bash_output,
                        self.executor._last_bash_exit_code,
                    )

                # ── Track action for turn summary ──
                if turn_actions is not None:
                    _cat = "read" if tc.name in ("read_file", "glob", "grep", "list_dir") else \
                           "command" if tc.name == "bash" else \
                           "write" if tc.name in ("write_file", "edit_file", "patch_file") else \
                           "cvc" if tc.name.startswith("cvc_") else "other"
                    turn_actions.append({
                        "category": _cat,
                        "description": f"{_humanize_tool_args(tc.name, tc.arguments) or tc.name}",
                        "success": not result.startswith("Error:"),
                    })

                break

            except Exception as exc:
                retry_count += 1
                if retry_count <= MAX_RETRY_ATTEMPTS:
                    render_tool_error(tc.name, f"Retrying ({retry_count}/{MAX_RETRY_ATTEMPTS}): {exc}")
                    await asyncio.sleep(0.2)
                else:
                    result = f"Error: {exc}"
                    render_tool_error(tc.name, str(exc))

        return result

    async def _auto_context_from_error(self, error_text: str) -> None:
        """Auto-read files mentioned in error messages."""
        try:
            from cvc.agent.auto_context import extract_files_from_error
            files = extract_files_from_error(error_text, self.workspace)
            for fpath in files[:3]:  # Limit to 3 files
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    rel = fpath.relative_to(self.workspace) if fpath.is_relative_to(self.workspace) else fpath
                    # Inject as a system hint (don't pollute conversation)
                    self.messages.append({
                        "role": "system",
                        "content": (
                            f"[Auto-context] File mentioned in error: {rel}\n"
                            f"Content (first 2000 chars):\n{content[:2000]}"
                        ),
                    })
                except OSError:
                    pass
        except Exception:
            pass

    def _ensure_pageindex_llm(self) -> None:
        """
        Inject the LLM call function into the executor for PageIndex (Tier 4).

        Creates a synchronous wrapper around the async AgentLLM.chat() method
        so that PageIndex can call the LLM without tools/streaming.
        The same API key and provider already configured in the agent session
        is reused — no extra keys needed.
        """
        if self.executor._pageindex_llm_call is not None:
            return  # Already injected

        llm = self.llm

        def _sync_llm_call(prompt: str) -> str:
            """Synchronous LLM call for PageIndex operations."""
            import asyncio as _aio

            messages = [
                {"role": "user", "content": prompt},
            ]

            async def _call() -> str:
                resp = await llm.chat(
                    messages=messages,
                    tools=[],
                    temperature=0.3,
                    max_tokens=4096,
                )
                return resp.text.strip()

            # Try to get the running loop, or create a new one
            try:
                loop = _aio.get_running_loop()
                # We're inside an async context — use a thread to avoid deadlock
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    future = pool.submit(_aio.run, _call())
                    return future.result(timeout=120)
            except RuntimeError:
                # No running loop — safe to use asyncio.run()
                return _aio.run(_call())

        self.executor._pageindex_llm_call = _sync_llm_call

    def _auto_commit(self) -> None:
        """Auto-commit the current context as a checkpoint with full cognitive context."""
        msg = f"Auto-checkpoint at turn {self.turn_count}"
        extras = self._build_context_extras()
        result = self.engine.commit(CVCCommitRequest(message=msg, context_extras=extras))
        if result.success:
            render_auto_commit(msg, result.commit_hash or "")
            self._assistant_turns_since_commit = 0
            self.executor.reset_turn_context()

            # Feed the commit to the Cognition Compiler for auto-distillation
            if self.cog_bridge is not None and result.commit_hash:
                commit_messages = [
                    {"role": m.get("role", "user"), "content": m.get("content", "")}
                    for m in self.messages[-6:]  # last few turns
                    if isinstance(m, dict) and m.get("content")
                ]
                self.cog_bridge.on_commit(
                    result.commit_hash,
                    commit_messages,
                    input_tokens=self.cost_tracker.total_input_tokens,
                    output_tokens=self.cost_tracker.total_output_tokens,
                )

    def _build_context_extras(self) -> dict:
        """Gather full cognitive context for a commit.

        Merges executor tool context (files read/written, tool outputs,
        bash commands) with session metadata (cost, tokens, session_id,
        turn count) and user query history.
        """
        extras = self.executor.get_turn_context()

        # Session & cost metadata
        extras["session_id"] = self._session.id if self._session else None
        extras["turn_count"] = self.turn_count
        extras["input_tokens"] = self.cost_tracker.total_input_tokens
        extras["output_tokens"] = self.cost_tracker.total_output_tokens
        extras["cache_read_tokens"] = self.cost_tracker.total_cache_read_tokens
        extras["cost_usd"] = self.cost_tracker.total_cost_usd

        # Query history — user prompts for quick semantic recall
        extras["query_history"] = [
            {"role": "user", "content": prompt, "turn": tid}
            for tid, prompt in sorted(self._turn_prompts.items())
        ]

        return extras

    async def handle_slash_command(self, command: str) -> bool:
        """
        Handle a slash command. Returns True if the command was handled,
        False if we should exit.
        """
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("/exit", "/quit", "/q"):
            # Save cost data and session memory before exit
            self._session.save_cost(self.cost_tracker)
            self._session.save()
            self._save_session_memory()
            # Final commit before exit
            if self._assistant_turns_since_commit > 0:
                msg = f"Session end at turn {self.turn_count}"
                extras = self._build_context_extras()
                result = self.engine.commit(CVCCommitRequest(message=msg, context_extras=extras))
                if result.success:
                    render_success(f"Final commit: {result.commit_hash[:12]}")
                    self.executor.reset_turn_context()
            return False

        elif cmd == "/help":
            print_help()

        elif cmd == "/status":
            render_status(
                self.engine.active_branch,
                self.engine.head_hash or "(none)",
                len(self.engine.context_window),
                self.config.provider,
                self.config.model,
            )

        elif cmd == "/log":
            entries = self.engine.log(limit=20)
            if entries:
                console.print()
                for e in entries:
                    console.print(
                        f"  [{THEME['hash']}]{e['short']}[/{THEME['hash']}]  "
                        f"[{THEME['text_dim']}]{e['type']}[/{THEME['text_dim']}]  "
                        f"{e['message'][:60]}"
                    )
                console.print()
            else:
                render_info("No commits yet.")

        elif cmd == "/commit":
            msg = arg or f"Manual checkpoint at turn {self.turn_count}"
            extras = self._build_context_extras()
            result = self.engine.commit(CVCCommitRequest(message=msg, context_extras=extras))
            if result.success:
                render_success(f"Committed: {result.commit_hash[:12]} — {msg}")
                self._assistant_turns_since_commit = 0
                self.executor.reset_turn_context()

                # Feed the commit to the Cognition Compiler for auto-distillation
                if self.cog_bridge is not None and result.commit_hash:
                    commit_messages = [
                        {"role": m.get("role", "user"), "content": m.get("content", "")}
                        for m in self.messages[-6:]
                        if isinstance(m, dict) and m.get("content")
                    ]
                    self.cog_bridge.on_commit(
                        result.commit_hash,
                        commit_messages,
                        input_tokens=self.cost_tracker.total_input_tokens,
                        output_tokens=self.cost_tracker.total_output_tokens,
                    )
            else:
                render_error(result.message)

        elif cmd == "/branch":
            if not arg:
                render_error("Usage: /branch <name>")
            else:
                from cvc.core.models import CVCBranchRequest
                result = self.engine.branch(CVCBranchRequest(name=arg))
                if result.success:
                    render_success(f"Switched to branch '{arg}'")
                    self._rebuild_system_prompt()
                else:
                    render_error(result.message)

        elif cmd == "/restore":
            if not arg:
                render_error("Usage: /restore <commit_hash>")
            else:
                from cvc.core.models import CVCRestoreRequest
                result = self.engine.restore(CVCRestoreRequest(commit_hash=arg))
                if result.success:
                    render_success(f"Restored to {arg[:12]}")
                    self.messages.append({
                        "role": "system",
                        "content": (
                            f"[CVC] Context has been restored to commit {arg[:12]}. "
                            "You now have the conversation state from that point in time."
                        ),
                    })
                else:
                    render_error(result.message)

        elif cmd == "/search":
            if not arg:
                render_error("Usage: /search <query>")
            else:
                result = self.executor.execute("cvc_search", {"query": arg})
                console.print()
                for line in result.split("\n"):
                    console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
                console.print()

        elif cmd == "/smartsearch":
            if not arg:
                render_error(
                    "Usage: /smartsearch <query> [--branch X] [--type checkpoint] "
                    "[--since 7d] [--provider anthropic] [--keyword auth]"
                )
            else:
                # Parse flags from the argument string
                import shlex as _shlex
                try:
                    parts = _shlex.split(arg)
                except ValueError:
                    parts = arg.split()

                search_query_parts: list[str] = []
                smart_args: dict[str, Any] = {}
                i = 0
                while i < len(parts):
                    p = parts[i]
                    if p.startswith("--") and i + 1 < len(parts):
                        flag = p[2:]
                        val = parts[i + 1]
                        flag_map = {
                            "branch": "branch",
                            "type": "commit_type",
                            "provider": "provider",
                            "model": "model",
                            "since": "since",
                            "until": "until",
                            "keyword": "contains_keyword",
                        }
                        if flag in flag_map:
                            smart_args[flag_map[flag]] = val
                            i += 2
                            continue
                        elif flag == "tags":
                            smart_args["tags"] = val.split(",")
                            i += 2
                            continue
                    search_query_parts.append(p)
                    i += 1

                if not search_query_parts:
                    render_error("Smart search requires a query. Example: /smartsearch auth --since 7d")
                else:
                    smart_args["query"] = " ".join(search_query_parts)
                    result = self.executor.execute("cvc_smart_search", smart_args)
                    console.print()
                    for line in result.split("\n"):
                        console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
                    console.print()

        elif cmd == "/ingest":
            if not arg:
                render_error(
                    "Usage: /ingest <path-to-document>\n"
                    "  Ingest a PDF, text, Markdown, or code file into PageIndex (Tier 4).\n"
                    "  Example: /ingest docs/architecture.pdf"
                )
            else:
                # Ensure the LLM call function is injected
                self._ensure_pageindex_llm()
                console.print(f"  [{THEME['text']}]Ingesting document... (this may take a while for large files)[/{THEME['text']}]")
                result = self.executor.execute("cvc_ingest_document", {"path": arg.strip()})
                console.print()
                for line in result.split("\n"):
                    console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
                console.print()

        elif cmd == "/docsearch":
            if not arg:
                render_error(
                    "Usage: /docsearch <query> [--doc <doc_id>]\n"
                    "  Search indexed documents using LLM-powered tree navigation.\n"
                    "  Example: /docsearch authentication flow --doc abc123"
                )
            else:
                self._ensure_pageindex_llm()
                # Parse --doc flag
                import shlex as _shlex2
                try:
                    parts = _shlex2.split(arg)
                except ValueError:
                    parts = arg.split()

                doc_args: dict[str, Any] = {}
                query_parts: list[str] = []
                i = 0
                while i < len(parts):
                    if parts[i] == "--doc" and i + 1 < len(parts):
                        doc_args["doc_id"] = parts[i + 1]
                        i += 2
                        continue
                    elif parts[i] == "--max" and i + 1 < len(parts):
                        try:
                            doc_args["max_results"] = int(parts[i + 1])
                        except ValueError:
                            pass
                        i += 2
                        continue
                    query_parts.append(parts[i])
                    i += 1

                if not query_parts:
                    render_error("Document search requires a query. Example: /docsearch what is the architecture")
                else:
                    doc_args["query"] = " ".join(query_parts)
                    result = self.executor.execute("cvc_document_search", doc_args)
                    console.print()
                    for line in result.split("\n"):
                        console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
                    console.print()

        elif cmd == "/documents":
            self._ensure_pageindex_llm()
            result = self.executor.execute("cvc_list_documents", {})
            console.print()
            for line in result.split("\n"):
                console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
            console.print()

        elif cmd == "/clear":
            self.messages = [self.messages[0]]
            self.turn_count = 0
            render_success("Conversation cleared. CVC state preserved.")

        elif cmd == "/compact":
            msg_count = len(self.messages)
            if msg_count <= 3:
                render_info("Conversation too short to compact.")
            else:
                keep_start = self.messages[:1]
                keep_end = self.messages[-6:]
                removed = msg_count - len(keep_start) - len(keep_end)
                self.messages = keep_start + [{
                    "role": "system",
                    "content": f"[CVC] Conversation compacted. {removed} earlier messages summarized. Recent context preserved.",
                }] + keep_end
                render_success(f"Compacted: removed {removed} messages, keeping recent context.")

        elif cmd == "/health":
            # Context Autopilot health dashboard
            health = self.autopilot.assess_health(self.messages)
            render_context_health(health)
            if arg and arg.lower() in ("verbose", "v", "diag", "diagnostics"):
                render_autopilot_diagnostics(self.autopilot.get_diagnostics())

        elif cmd == "/model":
            if arg:
                self.config.model = arg
                self.llm.model = arg
                self.cost_tracker.model = arg
                self.autopilot.update_model(arg)
                self._rebuild_system_prompt()
                render_success(f"Model changed to: {arg}")
            else:
                self._interactive_model_switch()

        elif cmd == "/provider":
            self._interactive_provider_switch()

        elif cmd == "/init":
            self._run_cvc_init()

        elif cmd == "/serve":
            self._start_proxy_background()

        # ── New commands ─────────────────────────────────────────────────

        elif cmd == "/undo":
            result = self.executor.undo_last()
            render_undo_result(result)

        elif cmd == "/retry":
            await self._handle_retry_command(arg)

        elif cmd == "/cost":
            summary = self.cost_tracker.format_summary()
            render_cost_summary(summary)

        elif cmd == "/analytics":
            self._handle_analytics_command()

        elif cmd == "/web":
            if not arg:
                render_error("Usage: /web <search query>")
            else:
                await self._handle_web_search(arg)

        elif cmd == "/checkout":
            if not arg:
                render_error("Usage: /checkout <branch_name>")
            else:
                self._handle_checkout_command(arg)

        elif cmd == "/branches":
            self._handle_branches_command()

        elif cmd == "/merge":
            if not arg:
                render_error("Usage: /merge <source_branch>")
            else:
                self._handle_merge_command(arg)

        elif cmd == "/git":
            self._handle_git_command(arg)

        elif cmd == "/sync":
            self._handle_sync_command(arg)

        elif cmd == "/image":
            if not arg:
                render_error("Usage: /image <file_path> [prompt text]")
            else:
                await self._handle_image(arg)

        elif cmd == "/paste":
            await self._handle_paste(arg)

        elif cmd == "/memory":
            self._handle_memory()

        elif cmd == "/files":
            self._handle_files_command(arg)

        elif cmd == "/summary":
            self._handle_summary_command()

        elif cmd == "/diff":
            self._handle_diff_command(arg)

        elif cmd == "/continue":
            self._handle_continue_command()

        elif cmd in ("/permissions", "/perms"):
            self._handle_permissions_command(arg)

        elif cmd in ("/allowed-tools", "/allowedtools"):
            self._handle_allowed_tools_command()

        elif cmd == "/agents":
            self._handle_agents_command()

        elif cmd == "/tasks":
            self._handle_tasks_command()

        elif cmd == "/hooks":
            self._handle_hooks_command()

        elif cmd == "/plan":
            self._handle_plan_command(arg)

        elif cmd == "/context":
            self._handle_context_command()

        elif cmd == "/init-rules":
            await self._handle_init_command()

        elif cmd == "/copy":
            self._handle_copy_command()

        elif cmd in ("/clear", "/new"):
            self._handle_clear_command()

        elif cmd == "/config":
            self._handle_config_command()

        elif cmd == "/stats":
            self._handle_stats_command()

        elif cmd == "/export":
            self._handle_export_command(arg)

        elif cmd in ("/think", "/effort"):
            self._handle_think_command(arg)

        elif cmd == "/sessions":
            self._handle_sessions_command()

        elif cmd == "/fork":
            self._handle_fork_command(arg)

        elif cmd == "/rename":
            self._handle_rename_command(arg)

        elif cmd == "/rewind":
            self._handle_rewind_command(arg)

        elif cmd in ("/plugin", "/plugins"):
            self._handle_plugins_command()

        elif cmd in ("/skill", "/skills"):
            self._handle_skills_command(arg)

        elif cmd == "/cd":
            self._handle_cd_command(arg)

        elif cmd == "/add-dir":
            self._handle_add_dir_command(arg)

        elif cmd == "/fast":
            self._handle_fast_command(arg)

        elif cmd == "/doctor":
            self._handle_doctor_command()

        elif cmd == "/release-notes":
            self._handle_release_notes_command()

        elif cmd == "/trust":
            self._handle_trust_command(arg)

        elif cmd == "/plan-mode":
            self._handle_plan_mode_command(arg)

        elif cmd == "/autopilot":
            self._handle_autopilot_command(arg)

        elif cmd == "/mode":
            self._handle_mode_command(arg)

        elif cmd == "/auth":
            self._handle_auth_command()

        elif cmd == "/settings":
            self._handle_settings_command(arg)

        elif cmd == "/hive":
            await self._handle_hive_command(arg)

        elif cmd == "/agent":
            await self._handle_agent_create_command(arg)

        elif cmd == "/distill":
            await self._handle_distill_command(arg)

        elif cmd == "/cogs":
            self._handle_cogs_command(arg)

        else:
            # Check plugin commands before showing error
            plugin_handled = False
            cmd_name = cmd.lstrip("/")
            for plugin in self._plugins:
                for pcmd in plugin.commands:
                    if pcmd.name == cmd_name:
                        self.messages.append({
                            "role": "system",
                            "content": f"[Plugin: {plugin.name}/{pcmd.name}]\n{pcmd.content}",
                        })
                        render_success(f"Plugin command /{pcmd.name} activated ({plugin.name})")
                        plugin_handled = True
                        break
                if plugin_handled:
                    break
            if not plugin_handled:
                render_error(f"Unknown command: {cmd}. Type /help for available commands.")

        return True

    # ------------------------------------------------------------------
    # Cognition Compiler (Cogs) slash command handlers
    # ------------------------------------------------------------------

    async def _handle_distill_command(self, arg: str) -> None:
        """Handle /distill — manually trigger Cog distillation from recent commits."""
        if self.cog_bridge is None:
            render_error("Cognition Compiler is not enabled. Set CVC_COGS=1 to enable.")
            return

        recent_n = 5
        if arg.strip().isdigit():
            recent_n = int(arg.strip())

        render_info(f"Distilling last {recent_n} commits into a Cog...")

        try:
            cog = await self.cog_bridge.manual_distill(engine=self.engine, recent_n=recent_n)
        except Exception as exc:
            render_error(f"Distillation failed: {exc}")
            return

        if cog is None:
            render_info(
                "No Cog produced — the commit history may be too LLM-dependent "
                "(creative/open-ended) or too few commits are available."
            )
        else:
            console.print()
            console.print(
                f"  [{THEME['success']}]✓ Cog compiled:[/{THEME['success']}] "
                f"[{THEME['hash']}]{cog.short_id}[/{THEME['hash']}] — "
                f"[bold]{cog.signature.intent_summary}[/bold]"
            )
            console.print(
                f"  [{THEME['text_dim']}]Body: {cog.body.kind.value} | "
                f"Tags: {', '.join(cog.signature.tags) or '—'} | "
                f"Provenance: {len(cog.provenance)} commits[/{THEME['text_dim']}]"
            )
            console.print()

    def _handle_cogs_command(self, arg: str) -> None:
        """Handle /cogs — list compiled Cogs and ROI report."""
        if self.cog_bridge is None:
            render_error("Cognition Compiler is not enabled. Set CVC_COGS=1 to enable.")
            return

        from rich.table import Table

        cogs = self.cog_bridge.list_cogs()
        roi = self.cog_bridge.roi_report(top_n=10)

        console.print()
        if not cogs:
            render_info("No compiled Cogs yet. Cogs are auto-distilled after every 3 commits, or use /distill.")
            return

        table = Table(
            title="Compiled Cogs",
            border_style=THEME["primary_dim"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        table.add_column("ID", style=THEME["hash"], width=14)
        table.add_column("Intent", style=THEME["text"])
        table.add_column("Kind", style=THEME["accent"], width=10)
        table.add_column("Promoted", width=9)
        table.add_column("Hits", justify="right", width=6)
        table.add_column("Saved", justify="right", width=10)

        for c in cogs:
            promoted = "✓" if c.get("promoted") else "shadow"
            table.add_row(
                c.get("cog_id", "?")[:12] + "…",
                (c.get("intent_summary", "?"))[:50],
                str(c.get("kind", "?")),
                promoted,
                str(c.get("invocations", 0)),
                f"{c.get('tokens_saved_cumulative', 0):,} tok",
            )

        console.print(table)
        console.print(
            f"\n  [{THEME['success']}]Total tokens saved: "
            f"{roi.get('tokens_saved_cumulative', 0):,}[/{THEME['success']}]  "
            f"[{THEME['text_dim']}]across {roi.get('total_invocations', 0)} "
            f"invocations from {roi.get('total_cogs', 0)} Cogs[/{THEME['text_dim']}]"
        )
        console.print()

    def _handle_settings_command(self, arg: str) -> None:
        """Handle /settings [key] [value] — view or modify settings."""
        from cvc.agent.settings import load_settings, save_project_settings
        settings = load_settings(str(self.workspace))

        if not arg:
            # Show all settings
            console.print()
            console.print(f"  [{THEME['text']}]Settings for workspace: {self.workspace}[/{THEME['text']}]")
            console.print()
            fields = [
                ("Trust Mode", settings.trust_mode),
                ("Output Style", settings.output_style),
                ("Auto Memory", settings.auto_memory_enabled),
                ("Always Thinking", settings.always_thinking_enabled),
                ("Auto Compact Threshold", settings.auto_compact_threshold),
                ("Plan Display", settings.plan_display),
                ("Allowed Tools", ", ".join(settings.permission_allow) if settings.permission_allow else "(none)"),
                ("Denied Tools", ", ".join(settings.permission_deny) if settings.permission_deny else "(none)"),
                ("Trusted Commands", ", ".join(settings.trusted_commands) if settings.trusted_commands else "(none)"),
                ("Blocked Commands", ", ".join(settings.blocked_commands) if settings.blocked_commands else "(none)"),
            ]
            for label, val in fields:
                console.print(f"  [{THEME['text_dim']}]{label:25s}[/{THEME['text_dim']}]  {val}")
            console.print()
        else:
            parts = arg.split(maxsplit=1)
            if len(parts) < 2:
                render_error("Usage: /settings <key> <value>")
            else:
                key, value = parts
                try:
                    save_project_settings(str(self.workspace), key, value)
                    render_success(f"Setting '{key}' updated to '{value}'")
                except Exception as e:
                    render_error(str(e))

    def _handle_auth_command(self) -> None:
        """Handle /auth — Re-authenticate to CVC using Firebase."""
        from cvc.auth import login_flow
        login_flow()
        render_success("Authentication flow completed. You can restart CVC to apply changes.")

    async def _handle_hive_command(self, arg: str) -> None:
        """Handle /hive [write|read|stats] — interact with hive memory."""
        parts = arg.strip().split(maxsplit=1)
        subcmd = parts[0].lower() if parts else "stats"
        subarg = parts[1] if len(parts) > 1 else ""

        try:
            from cvc.sdk.hivemind import HiveMemory, HiveMind
            hive = HiveMind(workspace=str(self.workspace))
            memory = HiveMemory(hive)

            if subcmd == "write":
                if not subarg:
                    render_error("Usage: /hive write <content>")
                    return
                agent_id = self.config.agent_id or "cli-agent"
                entry = await memory.write(agent_id, subarg, category="general")
                render_success(f"Written to hive memory (commit: {entry.commit_hash[:8]})")

            elif subcmd == "read":
                entries = await memory.read(query=subarg or None, limit=10)
                if not entries:
                    render_info("No hive memory entries found.")
                else:
                    console.print()
                    for e in entries:
                        console.print(
                            f"  [{THEME['hash']}]{e.agent_id}[/{THEME['hash']}]  "
                            f"[{THEME['text_dim']}]{e.category}[/{THEME['text_dim']}]  "
                            f"{e.content[:80]}"
                        )
                    console.print()

            elif subcmd == "stats":
                stats = await memory.stats()
                console.print()
                console.print(f"  [{THEME['text']}]Hive Memory Stats[/{THEME['text']}]")
                console.print(f"  Total entries:        {stats.get('total_entries', 0)}")
                console.print(f"  Contributing agents:  {stats.get('agent_count', 0)}")
                cats = stats.get('categories', {})
                if cats:
                    console.print(f"  Categories:           {', '.join(f'{k}({v})' for k, v in cats.items())}")
                console.print()

            elif subcmd == "summary":
                ctx = await memory.summary_context(limit=10)
                if ctx:
                    console.print()
                    console.print(f"  [{THEME['text']}]{ctx}[/{THEME['text']}]")
                    console.print()
                else:
                    render_info("No hive memory summary available.")
            else:
                render_error("Usage: /hive [write|read|stats|summary]")
        except Exception as e:
            render_error(f"Hive memory error: {e}")

    async def _handle_agent_create_command(self, arg: str) -> None:
        """Handle /agent [create|create-from-prompt|list] — manage agent templates."""
        parts = arg.strip().split(maxsplit=1)
        subcmd = parts[0].lower() if parts else "list"
        subarg = parts[1] if len(parts) > 1 else ""

        try:
            if subcmd == "list":
                from cvc.sdk.registry import AgentRegistry
                registry = AgentRegistry(workspace=str(self.workspace))
                agents = registry.list()
                if not agents:
                    render_info("No agents registered.")
                else:
                    console.print()
                    for a in agents:
                        console.print(
                            f"  [{THEME['hash']}]{a.get('agent_id', '?')}[/{THEME['hash']}]  "
                            f"{a.get('name', '—')}  "
                            f"[{THEME['text_dim']}]{a.get('role', '—')}[/{THEME['text_dim']}]  "
                            f"squad={a.get('squad', '—')}"
                        )
                    console.print()

            elif subcmd == "create":
                if not subarg:
                    render_error("Usage: /agent create <agent_id> [name] [role]")
                    return
                create_parts = subarg.split()
                agent_id = create_parts[0]
                name = create_parts[1] if len(create_parts) > 1 else agent_id
                role = create_parts[2] if len(create_parts) > 2 else "worker"

                from cvc.sdk.hivemind import HiveMind
                hive = HiveMind(workspace=str(self.workspace))
                agent = hive.register_agent(agent_id, role=role, squad="alpha")
                render_success(f"Agent '{name}' ({agent_id}) created with role '{role}'")

            elif subcmd == "create-from-prompt":
                if not subarg:
                    render_error("Usage: /agent create-from-prompt <description>")
                    return
                render_info("Generating agent template from prompt...")
                # Use the LLM to generate a template
                from cvc.core.models import AgentTemplate
                gen_prompt = (
                    "Create an AI agent template based on this description. "
                    "Return ONLY valid JSON with keys: id, name, description, system_prompt, "
                    "tool_tier (full/standard/readonly/minimal), rank (private/corporal/sergeant/commander), "
                    "squad, capabilities (list), skills (list).\n\n"
                    f"Description: {subarg}"
                )
                gen_messages = [{"role": "user", "content": gen_prompt}]
                response = await self.llm.chat(gen_messages, max_tokens=2000)
                import json as _json
                try:
                    # Try to extract JSON from the response
                    text = response.get("content", "") if isinstance(response, dict) else str(response)
                    # Find JSON in the response
                    start = text.find("{")
                    end = text.rfind("}") + 1
                    if start >= 0 and end > start:
                        data = _json.loads(text[start:end])
                        template = AgentTemplate(**data)
                        console.print()
                        console.print(f"  [{THEME['text']}]Generated Agent: {template.name}[/{THEME['text']}]")
                        console.print(f"  ID: {template.id}")
                        console.print(f"  Tier: {template.tool_tier}  Rank: {template.rank}  Squad: {template.squad}")
                        console.print(f"  Capabilities: {', '.join(template.capabilities)}")
                        console.print()
                        render_success("Use /agent create <id> to register, or the dashboard Agent Creator for full control.")
                    else:
                        render_error("Could not parse agent template from LLM response.")
                except Exception as parse_err:
                    render_error(f"Failed to parse generated template: {parse_err}")

            else:
                render_error("Usage: /agent [list|create|create-from-prompt] <args>")
        except Exception as e:
            render_error(f"Agent command error: {e}")

    def _rebuild_system_prompt(self) -> None:
        """Rebuild the system prompt (e.g., after branch switch)."""
        auto_ctx = ""
        lessons_ctx = ""
        instructions_ctx = ""
        memory_index_ctx = ""
        try:
            from cvc.agent.auto_context import build_auto_context
            auto_ctx = build_auto_context(self.workspace)
        except Exception:
            pass
        try:
            lessons_path = Path(self.workspace) / ".cvc" / "lessons.md"
            if lessons_path.exists():
                lessons_ctx = lessons_path.read_text(encoding="utf-8").strip()
        except Exception:
            pass
        try:
            from cvc.agent.instructions import load_instructions
            instructions_ctx = load_instructions(self.workspace)
        except Exception:
            pass
        try:
            from cvc.agent.memory import load_memory_index
            memory_index_ctx = load_memory_index(str(self.workspace))
        except Exception:
            pass
        api_ctx = ""
        try:
            from cvc.agent.api_docs import build_api_context
            api_ctx = build_api_context(self.workspace)
        except Exception:
            pass

        # Token-sensitive providers: limit injected context sizes
        _is_token_sensitive = self.config.provider in ("github",)
        if _is_token_sensitive:
            _MAX_CTX = 3000
            auto_ctx = auto_ctx[:_MAX_CTX] if len(auto_ctx) > _MAX_CTX else auto_ctx
            lessons_ctx = lessons_ctx[:2000] if len(lessons_ctx) > 2000 else lessons_ctx
            instructions_ctx = instructions_ctx[:_MAX_CTX] if len(instructions_ctx) > _MAX_CTX else instructions_ctx
            memory_index_ctx = memory_index_ctx[:1500] if len(memory_index_ctx) > 1500 else memory_index_ctx
            api_ctx = api_ctx[:2000] if len(api_ctx) > 2000 else api_ctx

        self.messages[0]["content"] = build_system_prompt(
            workspace=self.workspace,
            provider=self.config.provider,
            model=self.config.model,
            branch=self.engine.active_branch,
            agent_id=self.config.agent_id,
            auto_context=auto_ctx,
            lessons_context=lessons_ctx,
            instructions_context=instructions_ctx,
            memory_index_context=memory_index_ctx,
            api_context=api_ctx,
        )

    async def _handle_web_search(self, query: str) -> None:
        """Run a web search and display results."""
        render_info(f"Searching the web for: {query}")
        try:
            from cvc.agent.web_search import format_search_results, web_search
            results = await web_search(query)
            text = format_search_results(results, query)
            render_web_results(text)
        except Exception as e:
            render_error(f"Web search failed: {e}")

    def _handle_git_command(self, arg: str) -> None:
        """Handle /git subcommands."""
        from cvc.agent.git_integration import (
            format_git_status,
            git_commit,
            git_diff_summary,
            git_log,
            git_status,
        )

        sub_parts = arg.strip().split(maxsplit=1) if arg else []
        sub_cmd = sub_parts[0].lower() if sub_parts else ""
        sub_arg = sub_parts[1] if len(sub_parts) > 1 else ""

        if sub_cmd == "commit":
            msg = sub_arg or f"CVC agent commit at turn {self.turn_count}"
            success, result = git_commit(self.workspace, msg)
            if success:
                render_success(f"Git commit: {result} — {msg}")
            else:
                render_error(f"Git commit failed: {result}")

        elif sub_cmd == "log":
            commits = git_log(self.workspace)
            if commits:
                console.print()
                for c in commits:
                    console.print(
                        f"  [{THEME['hash']}]{c['hash']}[/{THEME['hash']}]  "
                        f"{c['message'][:50]}  "
                        f"[{THEME['text_dim']}]{c['author']} • {c['time']}[/{THEME['text_dim']}]"
                    )
                console.print()
            else:
                render_info("No Git commits found.")

        elif sub_cmd == "diff":
            diff_text = git_diff_summary(self.workspace)
            console.print()
            for line in diff_text.split("\n"):
                console.print(f"  [{THEME['text']}]{line}[/{THEME['text']}]")
            console.print()

        else:
            # Default: show status
            status = git_status(self.workspace)
            render_git_status(format_git_status(status))

    def _handle_sync_command(self, arg: str) -> None:
        """Handle /sync — fetch + ff-pull + push for the active branch.

        Mirrors the dashboard composer's Sync button. Uses the same shared
        helper (``cvc.agent.git_integration.git_sync``) so CLI ↔ dashboard
        behaviour is identical by construction.

        Usage:
          /sync                 → origin, fetch + ff-pull + push
          /sync --no-push       → fetch + ff-pull only
          /sync --rebase        → fetch + rebase pull + push
          /sync <remote>        → use named remote instead of origin
        """
        from cvc.agent.git_integration import git_sync as _do_sync

        parts = (arg or "").split()
        remote = "origin"
        do_push = True
        do_rebase = False
        for tok in parts:
            if tok in ("--no-push", "--nopush"):
                do_push = False
            elif tok == "--push":
                do_push = True
            elif tok == "--rebase":
                do_rebase = True
            elif tok.startswith("--"):
                render_error(f"Unknown flag: {tok}")
                render_info("Usage: /sync [<remote>] [--no-push] [--rebase]")
                return
            else:
                remote = tok

        render_info(f"Syncing {remote}…")
        result = _do_sync(self.workspace, remote=remote, push=do_push, rebase=do_rebase)

        status = result.get("status", "error")
        msg = result.get("message", "")
        branch = result.get("branch") or "?"
        pulled = result.get("pulled", 0)
        pushed = result.get("pushed", 0)
        head = result.get("head") or ""

        if status == "ok":
            detail = f"{branch} ↔ {result.get('remote', remote)}"
            if head:
                detail += f"  ({head})"
            if pulled or pushed:
                render_success(f"Synced — pulled {pulled}, pushed {pushed}   [dim]{detail}[/dim]")
            else:
                render_success(f"Already up to date   [dim]{detail}[/dim]")
        elif status == "dirty":
            render_error(f"Sync refused: working tree dirty on {branch}.")
            render_info("Commit or stash changes first, then run /sync again.")
        elif status == "no_upstream":
            render_error(f"No upstream for {branch}.")
            render_info(msg)
        elif status == "diverged":
            render_error(f"Diverged: {msg}")
            render_info("Resolve manually (git pull --rebase or merge), then /sync.")
        else:
            render_error(f"Sync failed: {msg}")

    async def _handle_image(self, arg_str: str) -> None:
        """Handle /image command — load image file and optionally send with prompt.

        Usage:
            /image screenshot.png                → loads image, waits for next prompt
            /image screenshot.png fix this bug   → loads image + sends prompt together
        """
        # Split: first token is the file path, rest is the prompt text
        parts = arg_str.strip().split(maxsplit=1)
        path_str = parts[0]
        prompt_text = parts[1].strip() if len(parts) > 1 else ""

        path = Path(path_str)
        if not path.is_absolute():
            path = self.workspace / path
        path = path.resolve()

        if not path.exists():
            render_error(f"Image file not found: {path}")
            return

        # Read and encode the image
        try:
            image_data = path.read_bytes()
            b64_data = base64.b64encode(image_data).decode("utf-8")
            mime_type = mimetypes.guess_type(str(path))[0] or "image/png"

            text = prompt_text or f"I've attached an image from {path.name}. Please analyze it."
            _build_image_message(
                self.messages, self.config.provider,
                b64_data, mime_type, text,
            )

            render_success(f"Image loaded: {path.name} ({len(image_data) / 1024:.0f}KB)")

            if prompt_text:
                # Send immediately — no second prompt needed
                await self.run_turn_no_append(prompt_text)
            else:
                render_info(
                    "Image ready. Type your prompt, or just say what you need — "
                    "the image will be sent along with it."
                )

        except OSError as e:
            render_error(f"Failed to read image: {e}")

    async def _handle_paste(self, prompt_text: str = "") -> None:
        """Handle /paste command — grab clipboard image and optionally send with prompt.

        Usage:
            /paste                           → loads clipboard image, waits for next prompt
            /paste analyze this screenshot   → loads image + sends prompt in one action
        """
        images = _grab_clipboard_images()
        if not images:
            # Give actionable diagnosis instead of a generic error
            _pil_available = True
            try:
                from PIL import ImageGrab as _IG  # noqa: F401
            except ImportError:
                _pil_available = False

            if not _pil_available:
                render_error(
                    "No image found in clipboard — Pillow is not installed.\n"
                    "  Fix: pip install Pillow>=10.0.0"
                )
            else:
                # Give platform-specific guidance
                _is_wsl_env = _is_wsl()
                if _is_wsl_env:
                    render_error(
                        "No image found in WSL clipboard.\n"
                        "  Make sure you have copied a screenshot in Windows first\n"
                        "  (Win+Shift+S → select area), then run /paste.\n"
                        "  WSL uses powershell.exe to read the Windows clipboard."
                    )
                elif sys.platform == "darwin":
                    render_error(
                        "No image found in clipboard.\n"
                        "  Copy a screenshot first (Cmd+Shift+4 or Cmd+Shift+Ctrl+4),\n"
                        "  then run /paste.\n"
                        "  Tip: Install pngpaste for better macOS support: brew install pngpaste"
                    )
                else:
                    # Windows or native Linux — check if clipboard has text
                    _has_text = False
                    try:
                        if sys.platform == "win32":
                            import ctypes as _ct
                            _u32 = _ct.windll.user32
                            if _u32.OpenClipboard(0):
                                try:
                                    _has_text = bool(_u32.IsClipboardFormatAvailable(13))  # CF_UNICODETEXT
                                finally:
                                    _u32.CloseClipboard()
                    except Exception:
                        pass

                    if _has_text:
                        render_error(
                            "Clipboard contains text only — no image found.\n"
                            "  Copy a screenshot or image first, then run /paste."
                        )
                    else:
                        render_error(
                            "No image found in clipboard.\n"
                            "  Copy a screenshot (Win+Shift+S / Cmd+Shift+4) then run /paste."
                        )
            return

        for idx, (b64_data, mime_type) in enumerate(images):
            label = f"image {idx + 1}"

            text = prompt_text or f"I've pasted {label} from my clipboard. Please analyze it."
            _build_image_message(
                self.messages, self.config.provider,
                b64_data, mime_type, text,
            )

            render_success(f"✓ {label}")

        # Update clipboard hash so auto-detect doesn't re-send the same image
        import hashlib
        self._last_clipboard_hash = hashlib.sha256(images[0][0].encode()).hexdigest()

        if prompt_text:
            render_info(f"{len(images)} image(s) + prompt → sending…")
            await self.run_turn_no_append(prompt_text)
        else:
            render_info("  Type your prompt and press Enter to send with the image(s).")

    def _handle_memory(self) -> None:
        """Show persistent memory from past sessions."""
        try:
            from cvc.agent.memory import load_memory
            memory = load_memory()
            render_memory(memory)
        except Exception as e:
            render_error(f"Failed to load memory: {e}")

    def _handle_files_command(self, arg: str | None = None) -> None:
        """List files in the workspace with optional filtering."""
        try:
            import os
            from pathlib import Path

            workspace = self.workspace or Path.cwd()

            # Build exclude list
            exclude_dirs = {'.git', '.cvc', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'env', 'dist', 'build', '.egg-info'}
            exclude_extensions = {'.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe'}

            files_found = []

            for root, dirs, files in os.walk(workspace):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    # Skip excluded extensions
                    if any(file.endswith(ext) for ext in exclude_extensions):
                        continue

                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(workspace)

                    # Filter by pattern if provided
                    if arg and arg.lower() not in str(rel_path).lower():
                        continue

                    files_found.append(str(rel_path))

            if not files_found:
                render_info("No files found" + (f" matching '{arg}'" if arg else ""))
                return

            # Sort and display
            files_found.sort()

            from rich.panel import Panel
            file_list = "\n".join([f"  {f}" for f in files_found[:50]])
            if len(files_found) > 50:
                file_list += f"\n  ... and {len(files_found) - 50} more files"

            console.print(Panel(
                file_list,
                title=f"[bold]Files in {self.workspace.name}[/bold] ({len(files_found)} total)",
                border_style=THEME['primary'],
                padding=(1, 2)
            ))
        except Exception as e:
            render_error(f"Failed to list files: {e}")

    def _handle_summary_command(self) -> None:
        """Get a summary of the codebase structure."""
        try:
            import os
            from pathlib import Path

            workspace = self.workspace or Path.cwd()

            exclude_dirs = {'.git', '.cvc', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'env', 'dist', 'build', '.egg-info'}

            # Count files by type
            file_counts = {}
            total_size = 0
            total_lines = 0

            for root, dirs, files in os.walk(workspace):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    full_path = Path(root) / file
                    ext = full_path.suffix or "no_ext"

                    file_counts[ext] = file_counts.get(ext, 0) + 1

                    try:
                        size = full_path.stat().st_size
                        total_size += size

                        # Count lines for text files
                        if ext in {'.py', '.ts', '.js', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.md', '.txt', '.json', '.yaml', '.yml'}:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                total_lines += len(f.readlines())
                    except:
                        pass

            # Format output
            summary_lines = []
            summary_lines.append(f"[bold]📁  {self.workspace.name}[/bold]")
            summary_lines.append(f"  Total size: {total_size / (1024*1024):.1f} MB")
            summary_lines.append(f"  Total lines of code: {total_lines:,}")
            summary_lines.append("")
            summary_lines.append("[bold]File Types:[/bold]")

            for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
                summary_lines.append(f"  {ext:15} {count:5} files")

            from rich.panel import Panel
            console.print(Panel(
                "\n".join(summary_lines),
                title="[bold]Codebase Summary[/bold]",
                border_style=THEME['primary'],
                padding=(1, 2)
            ))
        except Exception as e:
            render_error(f"Failed to summarize codebase: {e}")

    def _handle_diff_command(self, arg: str | None = None) -> None:
        """Show recent diffs or specific file diffs."""
        try:
            from cvc.agent.git_integration import git_diff_summary

            # Get diffs for workspace
            diffs = git_diff_summary(self.workspace or Path.cwd())
            if not diffs or diffs.strip() == "":
                render_info("No recent changes found.")
                return

            from rich.panel import Panel

            # Show as formatted output
            console.print(Panel(
                diffs,
                title="[bold]Git Changes[/bold]",
                border_style=THEME['primary'],
                padding=(1, 2)
            ))
        except Exception as e:
            render_error(f"Failed to show diffs: {e}")

    def _handle_continue_command(self) -> None:
        """Continue with the AI from the last point in conversation."""
        if len(self.messages) <= 2:
            render_info("Continue: No previous conversation to continue from.")
            return

        # Find the last user or assistant message
        last_user_msg = None
        for msg in reversed(self.messages[1:]):  # Skip system message
            if msg['role'] in ('user', 'assistant'):
                last_user_msg = msg
                break

        if not last_user_msg:
            render_info("Continue: No previous messages to continue from.")
            return

        # Show last context
        from rich.panel import Panel
        context_preview = last_user_msg['content'][:200]
        if len(last_user_msg['content']) > 200:
            context_preview += "..."

        console.print(Panel(
            f"Last {last_user_msg['role']}: {context_preview}",
            title="[bold]Continuing from...[/bold]",
            border_style=THEME['primary_dim'],
            padding=(1, 2)
        ))

        render_success("Ready to continue. Send your next message.")

    def _handle_permissions_command(self, arg: str) -> None:
        """Show or modify active permission rules."""
        from rich.table import Table as _Tbl

        pe = self.permission_engine
        if arg:
            # /permissions allow Bash(npm *) or /permissions deny Edit(/secrets/*)
            parts = arg.strip().split(maxsplit=1)
            if len(parts) == 2 and parts[0] in ("allow", "deny"):
                from cvc.agent.permissions import PermissionRule
                rule = PermissionRule.parse(parts[1], parts[0])
                pe.add_rule(rule)
                render_success(f"Added {parts[0]} rule: {parts[1]}")
                return
            render_error(
                "Usage: /permissions [allow|deny] <rule>\n"
                "  Examples:\n"
                "    /permissions allow Bash(npm run *)\n"
                "    /permissions deny Edit(/secrets/*)\n"
                "    /permissions          (show current rules)"
            )
            return

        # Show current rules
        tbl = _Tbl(
            title="[bold]Permission Rules[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Action", style="bold", width=8)
        tbl.add_column("Tool", width=20)
        tbl.add_column("Pattern", width=40)

        if not pe._rules:
            render_info("No custom permission rules configured.")
            render_info("Read-only tools (read_file, grep, glob, list_dir, cvc_status, cvc_log) are always allowed.")
            return

        for rule in pe._rules:
            action_style = "#55AA55" if rule.action == "allow" else "#CC3333"
            tbl.add_row(
                f"[{action_style}]{rule.action}[/{action_style}]",
                rule.tool_name,
                rule.pattern or "*",
            )
        console.print(tbl)

        # Show session approvals
        if pe._session_approvals:
            console.print()
            render_info(f"Session approvals: {len(pe._session_approvals)} tools approved this session")

    def _handle_allowed_tools_command(self) -> None:
        """Show which tools are allowed/denied/ask based on current rules."""
        from cvc.agent.tools import AGENT_TOOLS

        console.print()
        for tool_def in AGENT_TOOLS:
            name = tool_def["function"]["name"]
            decision = self.permission_engine.evaluate(name, {})
            if decision.name == "ALLOWED":
                icon, style = "✓", "#55AA55"
            elif decision.name == "DENIED":
                icon, style = "✗", "#CC3333"
            else:
                icon, style = "?", "#CCAA44"
            console.print(f"  [{style}]{icon}[/{style}] {name}  [{THEME['text_dim']}]{decision.name}[/{THEME['text_dim']}]")
        console.print()

    def _handle_agents_command(self) -> None:
        """List available sub-agents."""
        from rich.table import Table as _Tbl

        from cvc.agent.subagent import get_available_agents

        agents = get_available_agents(self.workspace)

        tbl = _Tbl(
            title="[bold]Available Agents[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Name", style="bold", width=15)
        tbl.add_column("Tools", width=12)
        tbl.add_column("Max Turns", width=10)
        tbl.add_column("Description", width=50)

        for name, cfg in agents.items():
            tbl.add_row(
                name,
                str(len(cfg.tools)),
                str(cfg.max_turns),
                cfg.description[:50] + ("..." if len(cfg.description) > 50 else ""),
            )
        console.print(tbl)
        console.print()
        render_info("Use the 'agent' tool in your prompt — e.g. 'Use the Explore agent to find...'")

    def _handle_tasks_command(self) -> None:
        """List background tasks."""
        if not hasattr(self.executor, "_task_manager"):
            render_info("No background tasks have been created this session.")
            return

        tasks = self.executor._task_manager.list_all()
        if not tasks:
            render_info("No tasks.")
            return

        from rich.table import Table as _Tbl

        tbl = _Tbl(
            title="[bold]Background Tasks[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("ID", style=THEME["hash"], width=12)
        tbl.add_column("Status", width=10)
        tbl.add_column("Elapsed", width=10)
        tbl.add_column("Command", width=50)

        for task in tasks:
            status_style = {
                "running": "#CCAA44",
                "completed": "#55AA55",
                "failed": "#CC3333",
                "killed": "#AA6666",
            }.get(task.status, "white")
            tbl.add_row(
                task.id[:8],
                f"[{status_style}]{task.status}[/{status_style}]",
                task.elapsed_str,
                task.command[:50],
            )
        console.print(tbl)
        console.print()

    def _handle_hooks_command(self) -> None:
        """List configured hooks."""
        hooks = self.hook_engine._hooks
        if not hooks:
            render_info("No hooks configured. Add hooks in .cvc/settings.json under the 'hooks' key.")
            return

        from rich.table import Table as _Tbl

        tbl = _Tbl(
            title="[bold]Configured Hooks[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Event", width=15)
        tbl.add_column("Matcher", width=20)
        tbl.add_column("Command", width=40)

        for h in hooks:
            tbl.add_row(h.event.value, h.matcher, h.command[:40])
        console.print(tbl)
        console.print()

    # ── Phase 5 commands ─────────────────────────────────────────────────

    def _handle_plan_command(self, arg: str) -> None:
        """Toggle plan (read-only) mode. Rerun /plan to switch back to agent mode."""
        if arg.lower() == "off" or getattr(self, "_plan_mode", False):
            # Deactivate plan mode → back to agent mode
            self._plan_mode = False
            render_success("Agent mode restored — all tools are available.")
        else:
            # Activate plan mode
            self._plan_mode = True
            render_success(
                "Plan mode ON — read-only analysis only. "
                "Run /plan again to return to agent mode."
            )
            self.messages.append({
                "role": "system",
                "content": (
                    "[Plan Mode] You are now in plan mode. Analyze and reason about "
                    "the codebase WITHOUT modifying any files. Use only read-only tools "
                    "(read_file, glob, grep, list_dir, web_search, cvc_search, etc.). "
                    "Do NOT use write_file, edit_file, patch_file, or bash with side effects."
                ),
            })

    def _handle_context_command(self) -> None:
        """Show context window utilization as a colored grid."""
        from cvc.agent.llm import MODEL_LIMITS

        model = self.llm.model
        limit = MODEL_LIMITS.get(model, 128000)
        used = self.total_prompt_tokens + self.total_completion_tokens
        pct = min(used / limit * 100, 100.0) if limit else 0

        # Build colored bar
        bar_width = 40
        filled = int(bar_width * pct / 100)
        if pct < 50:
            color = THEME["success"]
        elif pct < 75:
            color = THEME["warning"]
        else:
            color = THEME["error"]

        bar = f"[{color}]{'█' * filled}[/{color}][{THEME['text_dim']}]{'░' * (bar_width - filled)}[/{THEME['text_dim']}]"

        console.print()
        console.print(f"  Context Usage: {bar}  {pct:.1f}%")
        console.print(f"  Tokens: {used:,} / {limit:,} (model: {model})")
        console.print(f"  Messages: {len(self.messages)}")
        console.print(f"  Turns: {self.turn_count}")
        console.print()

    def _handle_diff_command(self, arg: str) -> None:
        """Show git diff of uncommitted changes."""
        try:
            from cvc.agent.git_integration import git_diff_summary
            diff = git_diff_summary(self.workspace)
            if diff:
                from rich.syntax import Syntax
                console.print()
                console.print(Syntax(diff, "diff", theme="monokai", line_numbers=True))
                console.print()
            else:
                render_info("No uncommitted changes.")
        except Exception as e:
            render_error(f"Git diff failed: {e}")

    async def _handle_init_command(self) -> None:
        """Generate a CVC.md by analyzing the project."""
        render_info("Analyzing project to generate CVC.md...")

        # Gather project signals
        signals = []
        ws = self.workspace

        # Check for package manifests
        for name in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", "build.gradle"]:
            p = ws / name
            if p.exists():
                try:
                    content = p.read_text(encoding="utf-8")[:2000]
                    signals.append(f"# {name}\n{content}")
                except Exception:
                    pass

        # Check for README
        for name in ["README.md", "readme.md", "README.rst", "README.txt"]:
            p = ws / name
            if p.exists():
                try:
                    content = p.read_text(encoding="utf-8")[:3000]
                    signals.append(f"# {name}\n{content}")
                except Exception:
                    break

        # Directory structure (top 2 levels)
        tree_lines = []
        for item in sorted(ws.iterdir()):
            if item.name.startswith(".") or item.name.startswith("_"):
                continue
            tree_lines.append(item.name + ("/" if item.is_dir() else ""))
            if item.is_dir():
                try:
                    for sub in sorted(item.iterdir())[:10]:
                        tree_lines.append(f"  {sub.name}" + ("/" if sub.is_dir() else ""))
                except PermissionError:
                    pass
        signals.append("# Directory Structure\n" + "\n".join(tree_lines[:50]))

        # Generate CVC.md via LLM
        prompt = (
            "Based on the following project information, generate a CVC.md file "
            "(project instructions for the AI coding agent). Include:\n"
            "- Project overview (1-2 sentences)\n"
            "- Tech stack\n"
            "- Key conventions (naming, patterns, architecture)\n"
            "- Common commands (build, test, lint)\n"
            "- Important files/directories\n\n"
            "Keep it concise (under 100 lines). Output ONLY the markdown content.\n\n"
            + "\n\n".join(signals)
        )

        try:
            # Use the LLM to generate
            response = ""
            async for event in self.llm.chat_stream(
                messages=[
                    {"role": "system", "content": "You generate project documentation files. Be concise and practical."},
                    {"role": "user", "content": prompt},
                ],
                tools=[],
                temperature=0.3,
                max_tokens=4096,
            ):
                if event.type == "text_delta":
                    response += event.text

            if response:
                cvc_md_path = ws / "CVC.md"
                cvc_md_path.write_text(response.strip() + "\n", encoding="utf-8")
                render_success(f"Generated CVC.md at {cvc_md_path}")
                self._rebuild_system_prompt()
            else:
                render_error("Failed to generate CVC.md — empty response.")
        except Exception as e:
            render_error(f"Failed to generate CVC.md: {e}")

    def _handle_copy_command(self) -> None:
        """Copy the last assistant response to clipboard."""
        # Find last assistant message
        for msg in reversed(self.messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                text = msg["content"]
                try:
                    import subprocess
                    if sys.platform == "win32":
                        process = subprocess.Popen(
                            ["clip"], stdin=subprocess.PIPE, shell=True,
                                                    **HIDDEN_KW,
                        )
                        process.communicate(text.encode("utf-16le"))
                    elif sys.platform == "darwin":
                        process = subprocess.Popen(
                            ["pbcopy"], stdin=subprocess.PIPE,
                                                    **HIDDEN_KW,
                        )
                        process.communicate(text.encode("utf-8"))
                    else:
                        process = subprocess.Popen(
                            ["xclip", "-selection", "clipboard"],
                            stdin=subprocess.PIPE,
                                                    **HIDDEN_KW,
                        )
                        process.communicate(text.encode("utf-8"))
                    render_success("Last response copied to clipboard.")
                except Exception as e:
                    render_error(f"Failed to copy: {e}")
                return
        render_info("No assistant response to copy.")

    def _handle_clear_command(self) -> None:
        """Clear conversation history and start fresh."""
        # Keep system prompt
        system_msg = self.messages[0] if self.messages else None
        self.messages.clear()
        if system_msg:
            self.messages.append(system_msg)
        self.turn_count = 0
        self._assistant_turns_since_commit = 0
        render_success("Conversation cleared. Starting fresh.")

    def _handle_config_command(self) -> None:
        """Show current configuration."""
        from rich.table import Table as _Tbl

        tbl = _Tbl(
            title="[bold]CVC Configuration[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Setting", width=25)
        tbl.add_column("Value", width=50)

        tbl.add_row("Provider", self.config.provider)
        tbl.add_row("Model", self.config.model)
        tbl.add_row("Workspace", str(self.workspace))
        tbl.add_row("Branch", self.engine.active_branch)
        tbl.add_row("Plan Mode", str(getattr(self, "_plan_mode", False)))
        tbl.add_row("Turns", str(self.turn_count))
        tbl.add_row("Messages", str(len(self.messages)))
        tbl.add_row("Cost", self.cost_tracker.format_summary())

        # Show CVC.md status
        cvc_md = self.workspace / "CVC.md"
        cvc_md_alt = self.workspace / ".cvc" / "CVC.md"
        if cvc_md.exists():
            tbl.add_row("CVC.md", str(cvc_md))
        elif cvc_md_alt.exists():
            tbl.add_row("CVC.md", str(cvc_md_alt))
        else:
            tbl.add_row("CVC.md", "(not found — use /init to generate)")

        console.print(tbl)
        console.print()

    def _handle_stats_command(self) -> None:
        """Show detailed usage statistics."""
        console.print()
        console.print("  [bold]Session Statistics[/bold]")
        console.print("  ─────────────────────────")
        console.print(f"  Turns:              {self.turn_count}")
        console.print(f"  Messages:           {len(self.messages)}")
        console.print(f"  Prompt tokens:      {self.total_prompt_tokens:,}")
        console.print(f"  Completion tokens:  {self.total_completion_tokens:,}")
        console.print(f"  Total cost:         {self.cost_tracker.format_summary()}")
        console.print(f"  Provider:           {self.config.provider}")
        console.print(f"  Model:              {self.config.model}")
        console.print(f"  Branch:             {self.engine.active_branch}")

        # Tool usage stats from executor
        tool_counts = getattr(self.executor, "_tool_call_counts", {})
        if tool_counts:
            console.print()
            console.print("  [bold]Tool Usage[/bold]")
            console.print("  ─────────────────────────")
            for name, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
                console.print(f"  {name:<22} {count:>5}×")
        console.print()

    def _handle_export_command(self, arg: str) -> None:
        """Export conversation to a markdown file."""
        filename = arg.strip() or f"cvc-session-{int(time.time())}.md"
        if not filename.endswith(".md"):
            filename += ".md"

        lines = ["# CVC Agent Session\n"]
        lines.append(f"**Provider:** {self.config.provider}  ")
        lines.append(f"**Model:** {self.config.model}  ")
        lines.append(f"**Turns:** {self.turn_count}  ")
        lines.append(f"**Cost:** {self.cost_tracker.format_summary()}\n")
        lines.append("---\n")

        for msg in self.messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if role == "system":
                continue
            elif role == "user":
                lines.append(f"## User\n\n{content}\n")
            elif role == "assistant":
                lines.append(f"## Assistant\n\n{content}\n")
            elif role == "tool":
                name = msg.get("name", "tool")
                lines.append(f"### Tool: {name}\n\n```\n{content[:2000]}\n```\n")

        out_path = self.workspace / filename
        out_path.write_text("\n".join(lines), encoding="utf-8")
        render_success(f"Exported to {out_path}")

    def _handle_think_command(self, arg: str) -> None:
        """Toggle or set extended thinking effort.

        Extended thinking makes the LLM reason deeper before responding.
        Higher levels = more thorough but slower responses.

        - /think           → toggle between off and medium
        - /think off       → disable extended thinking (fastest)
        - /think low       → light reasoning (fast, good for simple tasks)
        - /think medium    → balanced reasoning (recommended)
        - /think high      → deep reasoning (slowest, best for complex tasks)
        """
        valid = ("off", "low", "medium", "high")
        if not arg:
            # Toggle: off → medium, anything → off
            current = self._effort_level or "off"
            if current == "off":
                self._effort_level = "medium"
                render_success(
                    "Extended thinking ON — [bold]medium[/bold] effort. "
                    "Run /think again to turn off."
                )
            else:
                self._effort_level = ""
                render_success(
                    "Extended thinking OFF — fastest responses. "
                    "Run /think again to re-enable."
                )
            return
        level = arg.strip().lower()
        if level == "off":
            self._effort_level = ""
            render_success("Extended thinking OFF — fastest responses.")
        elif level in valid:
            self._effort_level = level
            render_success(f"Extended thinking set to [bold]{level}[/bold].")
        else:
            render_error(f"Invalid level. Choose from: {', '.join(valid)}")

    def _handle_sessions_command(self) -> None:
        """List all sessions for this workspace."""
        from rich.table import Table as _Tbl

        from cvc.agent.sessions import list_sessions

        sessions = list_sessions(str(self.workspace))
        if not sessions:
            render_info("No sessions found.")
            return

        tbl = _Tbl(
            title="[bold]Sessions[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("ID", width=10)
        tbl.add_column("Name", width=20)
        tbl.add_column("Model", width=20)
        tbl.add_column("Turns", width=6, justify="right")
        tbl.add_column("Last Active", width=20)

        from datetime import datetime as _dt
        for s in sessions[:20]:
            try:
                last = _dt.fromtimestamp(s.last_active).strftime("%b %d %H:%M")
            except Exception:
                last = "?"
            current = "● " if s.id == self._session.id else "  "
            tbl.add_row(
                current + s.id[:8],
                s.name or "(unnamed)",
                s.model or "?",
                str(s.turn_count),
                last,
            )
        console.print(tbl)
        console.print()

    def _handle_fork_command(self, name: str) -> None:
        """Fork current session into a new one."""
        from cvc.agent.sessions import fork_session
        new = fork_session(self._session, name.strip())
        self._session = new
        render_success(f"Forked session → {new.id[:8]} ({new.name})")

    def _handle_rename_command(self, name: str) -> None:
        """Rename current session."""
        if not name.strip():
            render_error("Usage: /rename <name>")
            return
        self._session.name = name.strip()
        self._session.save()
        render_success(f"Session renamed to '{name.strip()}'")

    def _handle_rewind_command(self, arg: str) -> None:
        """Rewind the conversation by N turns."""
        n = 1
        if arg.strip().isdigit():
            n = int(arg.strip())
        if n < 1:
            render_error("Must rewind at least 1 turn.")
            return

        # Each turn consists of user + assistant + tool messages.
        # Find the last N user messages and remove everything after the (N+1)th-from-end user.
        user_indices = [
            i for i, m in enumerate(self.messages) if m.get("role") == "user"
        ]
        if n >= len(user_indices):
            render_error(f"Cannot rewind {n} turns — only {len(user_indices)} turns exist.")
            return

        cut_at = user_indices[-(n)]
        removed = len(self.messages) - cut_at
        self.messages = self.messages[:cut_at]
        self.turn_count = max(0, self.turn_count - n)
        render_success(f"Rewound {n} turn(s) — removed {removed} messages.")

    # ── Agentic Auto-Retry System ────────────────────────────────────────

    async def _handle_retry_command(self, arg: str) -> None:
        """
        Handle /retry slash command. Triggers the 3-step retry flow.

        Usage:
          /retry            — retry the most recent turn
          /retry <message>  — retry with additional context
        """
        turn_id = self.executor.get_latest_turn_id()
        if turn_id == 0:
            render_error("Nothing to retry — no file changes recorded.")
            return

        user_complaint = arg.strip() if arg.strip() else "The previous changes were not correct."
        await self._execute_retry_flow(turn_id, user_complaint)

    async def _execute_retry_flow(self, turn_id: int, user_complaint: str) -> None:
        """
        Execute the 3-step agentic retry flow:
          1. Diagnose what went wrong
          2. Revert files (if big issue, with human permission)
          3. Re-execute with lessons learned
        """
        from cvc.agent.renderer import (
            render_diagnosis_panel,
            render_retry_complete,
            render_retry_step,
            render_revert_header,
            render_revert_results,
        )
        from cvc.agent.retry import (
            build_retry_prompt,
            diagnose_issue,
            persist_lessons,
            rewind_messages_to_turn,
            show_file_select_menu,
            show_revert_menu,
        )

        # Get the file changes and original prompt for this turn
        turn_changes = self.executor.get_turn_changes(turn_id)
        original_prompt = self._turn_prompts.get(turn_id, "")

        if not turn_changes and not original_prompt:
            render_error("Cannot retry — no tracked changes or prompt for this turn.")
            return

        # Find the assistant's last response for context
        assistant_response = ""
        for msg in reversed(self.messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                assistant_response = msg["content"]
                break

        # ── Step 1: Diagnose ──────────────────────────────────────────
        render_retry_step(1, 3, "Analyzing what went wrong...")

        diagnosis = await diagnose_issue(
            llm=self.llm,
            original_prompt=original_prompt,
            user_complaint=user_complaint,
            file_changes=turn_changes,
            assistant_response=assistant_response,
            turn_id=turn_id,
            workspace=self.workspace,
        )

        render_diagnosis_panel(diagnosis)

        # ── Step 2: Revert (conditional) ──────────────────────────────
        if diagnosis.severity == "small":
            # Small issue: no revert needed, just fix in place
            render_retry_step(2, 3, "Minor issue — fixing in place (no revert needed).")
        else:
            # Big issue: show revert menu with human-in-the-loop
            render_retry_step(2, 3, "Major issue detected — requesting revert permission...")
            render_revert_header(len(diagnosis.files_affected))

            choice = show_revert_menu(diagnosis.files_affected)

            if choice == "cancel":
                render_info("Retry cancelled by user.")
                return
            elif choice == "all":
                # Revert all files for this turn
                results = self.executor.undo_turn(turn_id)
                render_revert_results(results)
            elif choice == "select":
                # Let user pick specific files
                selected = show_file_select_menu(diagnosis.files_affected)
                if not selected:
                    render_info("No files selected — retry cancelled.")
                    return
                selected_paths = [Path(self.workspace) / f for f in selected]
                results = self.executor.undo_specific_files(selected_paths, turn_id)
                render_revert_results(results)

            # Clean up conversation: remove the failed turn's messages
            self.messages = rewind_messages_to_turn(
                self.messages, turn_id, self._turn_prompts,
            )

        # ── Step 3: Re-execute with lessons ───────────────────────────
        render_retry_step(3, 3, "Re-executing with lessons learned...")

        # Persist lessons for future sessions
        persist_lessons(self.workspace, diagnosis)

        # Build the enhanced retry prompt
        retry_prompt = build_retry_prompt(diagnosis)

        # Execute the retry as a new turn
        await self.run_turn(retry_prompt)

        render_retry_complete(diagnosis.severity)

    async def _check_retry_intent(self, user_input: str) -> bool:
        """
        Check if user input suggests retry intent.
        If detected, offer to trigger retry flow automatically.

        Returns True if retry was triggered (caller should skip normal processing),
        False if normal processing should continue.
        """
        from cvc.agent.retry import detect_retry_intent

        if not detect_retry_intent(user_input):
            return False

        # Check if there are file changes to retry against
        turn_id = self.executor.get_latest_turn_id()
        if turn_id == 0:
            return False  # No changes to retry

        # Ask user if they want the auto-retry flow
        from cvc.agent.menus import arrow_confirm
        render_info("It looks like you want to retry the previous changes.")

        if arrow_confirm(
            "Run the auto-retry flow? (analyze → revert if needed → redo with lessons)",
            default_yes=True,
        ):
            await self._execute_retry_flow(turn_id, user_input)
            return True

        return False  # User declined, process as normal message

    def _handle_plugins_command(self) -> None:
        """List installed plugins."""
        if not self._plugins:
            render_info("No plugins installed. Place plugins in .cvc/plugins/ or ~/.cvc/plugins/.")
            return

        from rich.table import Table as _Tbl
        tbl = _Tbl(
            title="[bold]Installed Plugins[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Name", width=20)
        tbl.add_column("Version", width=10)
        tbl.add_column("Commands", width=8, justify="right")
        tbl.add_column("Description", width=35)

        for p in self._plugins:
            tbl.add_row(p.name, p.version, str(len(p.commands)), p.description[:35])
        console.print(tbl)
        console.print()

    def _handle_skills_command(self, arg: str) -> None:
        """List or invoke a skill."""
        if arg.strip():
            # Invoke a specific skill by name
            skill = None
            for s in self._skills:
                if s.name == arg.strip():
                    skill = s
                    break
            if not skill:
                render_error(f"Skill '{arg.strip()}' not found.")
                return
            # Inject skill content as system message
            self.messages.append({
                "role": "system",
                "content": f"[Skill: {skill.name}]\n{skill.content}",
            })
            # Phase B (3.2): record actual content load as a "use".
            try:
                from cvc.skills.usage import bump_use
                bump_use(skill.name)
            except Exception:
                pass
            render_success(f"Activated skill: {skill.name}")
            return

        if not self._skills:
            render_info("No skills found. Place skills in .cvc/skills/ or ~/.cvc/skills/.")
            return

        from rich.table import Table as _Tbl
        tbl = _Tbl(
            title="[bold]Available Skills[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Name", width=20)
        tbl.add_column("Auto-Invoke", width=10)
        tbl.add_column("Description", width=40)

        for s in self._skills:
            auto = "Yes" if s.auto_invoke_patterns else "No"
            tbl.add_row(s.name, auto, s.description[:40])
        console.print(tbl)
        console.print()
        # Phase B (3.2): listing the manifest counts as a "view" for each skill.
        try:
            from cvc.skills.usage import bump_view
            for s in self._skills:
                bump_view(s.name)
        except Exception:
            pass

    def _handle_checkout_command(self, branch_name: str) -> None:
        """Switch to an existing branch."""
        try:
            # Get all available branches
            branches = self.engine.db.index.list_branches()
            branch_names = [b.name for b in branches]

            if branch_name not in branch_names:
                render_error(f"Branch '{branch_name}' not found. Available branches:\n  " + "\n  ".join(branch_names))
                return

            # Switch to the branch
            branch_ptr = self.engine.db.index.get_branch(branch_name)
            if branch_ptr:
                self.engine._active_branch = branch_name
                render_success(f"Switched to branch '{branch_name}'")
                self._rebuild_system_prompt()
            else:
                render_error(f"Failed to switch to branch '{branch_name}'")
        except Exception as e:
            render_error(f"Failed to checkout branch: {e}")

    def _handle_branches_command(self) -> None:
        """List all available branches."""
        try:
            branches = self.engine.db.index.list_branches()

            if not branches:
                render_info("No branches found.")
                return

            from rich.table import Table

            table = Table(
                title="[bold]Branches[/bold]",
                border_style=THEME['primary'],
                show_header=True,
                header_style=f"bold {THEME['primary_bright']}",
            )
            table.add_column("Branch", style=THEME['branch'], width=30)
            table.add_column("HEAD", style=THEME['hash'], width=15)
            table.add_column("Status", style=THEME['text_dim'])

            active = self.engine.active_branch
            for b in branches:
                status = "● current" if b.name == active else ""
                head_display = b.head_hash[:12] if b.head_hash else "none"
                table.add_row(b.name, head_display, status)

            console.print(table)
            console.print()
        except Exception as e:
            render_error(f"Failed to list branches: {e}")

    def _handle_merge_command(self, source_branch: str) -> None:
        """Merge source branch into current branch."""
        try:
            from cvc.core.models import CVCMergeRequest

            target_branch = self.engine.active_branch

            if source_branch == target_branch:
                render_error("Cannot merge a branch into itself.")
                return

            # Verify source branch exists
            branches = self.engine.db.index.list_branches()
            branch_names = [b.name for b in branches]

            if source_branch not in branch_names:
                render_error(f"Source branch '{source_branch}' not found. Available branches:\n  " + "\n  ".join(branch_names))
                return

            render_info(f"Merging '{source_branch}' into '{target_branch}'...")

            # Create merge request
            request = CVCMergeRequest(
                source_branch=source_branch,
                target_branch=target_branch,
            )

            # Perform the merge
            result = self.engine.merge(request)

            if result.success:
                render_success(f"✓ Merged '{source_branch}' into '{target_branch}'")
                render_success(f"Merge commit: {result.commit_hash[:12]}")
                # Rebuild system prompt with merged context
                self._rebuild_system_prompt()
                # Add merge notification to conversation
                self.messages.append({
                    "role": "system",
                    "content": f"[CVC] Successfully merged branch '{source_branch}' into '{target_branch}' (commit {result.commit_hash[:12]}). Context has been unified.",
                })
            else:
                render_error(f"Merge failed: {result.message}")

        except Exception as e:
            render_error(f"Failed to merge branches: {e}")


    def _save_session_memory(self) -> None:
        """Save a summary of this session to persistent memory."""
        if self.turn_count < 1:
            return
        try:
            from cvc.agent.memory import generate_session_summary, save_memory_entry
            summary, topics = generate_session_summary(self.messages)
            save_memory_entry(
                workspace=str(self.workspace),
                summary=summary,
                topics=topics,
                model=self.config.model,
                turn_count=self.turn_count,
                cost_usd=self.cost_tracker.total_cost_usd,
            )
        except Exception as e:
            logger.debug("Failed to save session memory: %s", e)

    # ── Interactive helpers ───────────────────────────────────────────────

    def _interactive_model_switch(self) -> None:
        """Show current model and let user pick a new one interactively."""

        provider = self.config.provider
        current = self.config.model

        catalog = []
        if provider == "github":
            import httpx

            from cvc.agent.providers.github_auth import fetch_copilot_token
            from cvc.core.models import GlobalConfig
            gc = GlobalConfig.load()
            oauth_token = gc.api_keys.get("github")
            if not oauth_token:
                render_error("No GitHub token found. Run cvc init to authenticate.")
                return

            with console.status("Fetching available Copilot models...", spinner="dots"):
                token_data = fetch_copilot_token(oauth_token)
                if token_data:
                    copilot_token = token_data.get("token")
                    proxy_ep = token_data.get("endpoints", {}).get("api", "https://api.individual.githubcopilot.com")
                    try:
                        resp = httpx.get(
                            f"{proxy_ep.rstrip('/')}/models",
                            headers={
                                "Authorization": f"Bearer {copilot_token}",
                                "Accept": "application/json",
                                "editor-version": "vscode/1.85.0",
                                "editor-plugin-version": "copilot-chat/0.11.1"
                            },
                            timeout=10.0
                        )
                        resp.raise_for_status()
                        models_data = resp.json().get("data", [])
                        for m in models_data:
                            if m.get("policy", {}).get("state") == "disabled":
                                continue
                            catalog.append((m["id"], m.get("name", m["id"]), "Copilot Tier"))
                    except Exception as e:
                        render_error(f"Failed to fetch models: {e}")

        elif provider == "vertex":
            from cvc.adapters.vertex import (
                VERTEX_MODELS,
                fetch_vertex_models,
                get_vertex_credentials,
            )
            from cvc.core.models import GlobalConfig
            gc = GlobalConfig.load()
            try:
                _creds, adc_project = get_vertex_credentials()
                v_project = gc.vertex_project_id or adc_project
                v_location = gc.vertex_location or "us-central1"
                if v_project:
                    with console.status("Fetching Vertex AI models...", spinner="dots"):
                        fetched = fetch_vertex_models(v_project, v_location, timeout=8.0)
                        catalog = fetched if fetched else VERTEX_MODELS
                else:
                    catalog = VERTEX_MODELS
            except Exception:
                catalog = VERTEX_MODELS

        else:
            catalog = MODEL_CATALOG_AGENT.get(provider, [])

        console.print()
        render_info(f"Current model: [bold]{provider}[/bold] / [bold]{current}[/bold]")
        console.print()

        if not catalog:
            console.print(f"  [{THEME['text_dim']}]No model catalog for {provider}. "
                          f"Type [bold]/model <name>[/bold] to set manually.[/{THEME['text_dim']}]")
            return

        from cvc.agent.menus import arrow_select
        current_idx = 0
        menu_options = []
        descs = []
        for i, (mid, desc, tier) in enumerate(catalog):
            marker = " ●" if mid == current else ""
            menu_options.append((f"{mid}{marker}", mid))
            descs.append(f"{desc} ({tier})")
            if mid == current:
                current_idx = i

        new_model = arrow_select("Pick a model", menu_options, descriptions=descs, default=current_idx)
        if new_model is None:
            render_info("Keeping current model.")
            return

        self.config.model = new_model
        self.llm.model = new_model
        self.cost_tracker.model = new_model
        self.autopilot.update_model(new_model)
        self._rebuild_system_prompt()  # Update system prompt with new model name

        try:
            from cvc.core.models import GlobalConfig
            gc = GlobalConfig.load()
            gc.model = new_model
            gc.save()
        except Exception:
            pass

        render_success(f"Model switched to [bold]{new_model}[/bold]")

    def _handle_analytics_command(self) -> None:
        """Show detailed analytics for the current session and historical usage."""
        try:

            # Current session analytics
            session_cost = self.cost_tracker.total_cost_usd
            input_tokens = self.cost_tracker.total_input_tokens
            output_tokens = self.cost_tracker.total_output_tokens
            cache_tokens = self.cost_tracker.total_cache_read_tokens
            total_tokens = input_tokens + output_tokens + cache_tokens

            analytics = []
            analytics.append("[bold]📊  Session Analytics[/bold]")
            analytics.append("")
            analytics.append(f"  Total Tokens:     {total_tokens:,}")
            analytics.append(f"  Input Tokens:     {input_tokens:,}")
            analytics.append(f"  Output Tokens:    {output_tokens:,}")
            analytics.append(f"  Cache Tokens:     {cache_tokens:,}")
            analytics.append(f"  Session Cost:     ${session_cost:.4f}")
            analytics.append(f"  Turns:            {self.turn_count}")
            analytics.append(f"  Messages:         {len(self.messages)}")
            analytics.append(f"  Provider:         {self.config.provider}")
            analytics.append(f"  Model:            {self.config.model}")
            analytics.append(f"  Branch:           {self.engine.active_branch}")
            analytics.append(f"  Workspace:        {self.workspace.name}")
            analytics.append("")

            # Per-turn average
            if self.turn_count > 0:
                avg_cost = session_cost / self.turn_count
                avg_tokens = total_tokens / self.turn_count if total_tokens > 0 else 0
                analytics.append(f"  Avg Cost/Turn:    ${avg_cost:.4f}")
                analytics.append(f"  Avg Tokens/Turn:  {avg_tokens:.0f}")
                analytics.append("")

            # Commits
            try:
                commits = self.engine.db.index.list_commits(self.engine.active_branch)
                analytics.append(f"  Commits:          {len(commits)}")
            except:
                pass

            from rich.panel import Panel
            console.print(Panel(
                "\n".join(analytics),
                title="[bold]Session & Usage Analytics[/bold]",
                border_style=THEME['primary'],
                padding=(1, 2)
            ))

        except Exception as e:
            render_error(f"Failed to show analytics: {e}")

    def _interactive_provider_switch(self) -> None:
        """Let the user switch provider + model interactively."""
        providers = [
            ("anthropic", "Anthropic", "API Key (only right now we have that option only)"),
            ("google", "Google Gemini", "API Key (AI Studio key — generativelanguage.googleapis.com)"),
            ("vertex", "Google Cloud Vertex AI", "gcloud ADC login — enterprise Gemini & Model Garden"),
            ("github", "GitHub Copilot", "GitHub Authentication from the browser"),
            ("openai", "OpenAI", "API Key (only right now we have that option only)"),
            ("nvidia", "NVIDIA NIM", "API Key (free tier) — Nemotron 3 Super 120B + Kimi K2 + MiniMax M2"),
            ("minimax", "MiniMax", "API Key — MiniMax M3 / M2.7 / M2.5 / M2.1 / M2 family"),
            ("ollama", "Ollama", "Local models via Ollama — no API key needed!"),
            ("lmstudio", "LM Studio", "Local models via LM Studio server — no API key needed!"),
        ]

        console.print()
        render_info(f"Current provider: [bold]{self.config.provider}[/bold]")
        console.print()

        from cvc.agent.menus import arrow_select
        current_idx = 0
        menu_options = []
        descs = []
        for i, (key, name, desc) in enumerate(providers):
            marker = " ●" if key == self.config.provider else ""
            menu_options.append((f"{name}{marker}", key))
            descs.append(desc)
            if key == self.config.provider:
                current_idx = i

        new_provider = arrow_select("Pick a provider", menu_options, descriptions=descs, default=current_idx)
        if new_provider is None:
            render_info("Keeping current provider.")
            return

        if new_provider not in MODEL_CATALOG_AGENT and new_provider != "vertex":
            render_error(f"Unknown provider: {new_provider}")
            return

        from cvc.core.models import GlobalConfig
        gc = GlobalConfig.load()
        key = gc.api_keys.get(new_provider, "")

        env_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "vertex": "",  # Uses gcloud ADC
            "ollama": "",
            "lmstudio": "",
            "github": "GITHUB_TOKEN",
            "nvidia": "NVIDIA_API_KEY",
            "minimax": "MINIMAX_API_KEY",
        }
        env_key = env_map.get(new_provider, "")
        if env_key:
            key = key or os.getenv(env_key, "")

        if not key and new_provider not in ("ollama", "lmstudio", "vertex"):
            render_error(
                f"No API key for {new_provider}. "
                f"Run [bold]cvc setup[/bold] to configure it first."
            )
            return

        self.config.provider = new_provider
        self.llm.provider = new_provider
        self.llm.api_key = key

        # Build the correct base URL for the provider
        if new_provider == "vertex":
            from cvc.adapters.vertex import (
                build_vertex_base_url,
                get_vertex_access_token,
                get_vertex_credentials,
            )
            try:
                creds, adc_project = get_vertex_credentials()
                token, creds = get_vertex_access_token(creds)
            except RuntimeError as exc:
                render_error(str(exc))
                return
            v_project = gc.vertex_project_id or adc_project
            v_location = gc.vertex_location or "us-central1"
            if not v_project:
                render_error(
                    "Could not determine GCP project. "
                    "Run: gcloud config set project YOUR_PROJECT_ID"
                )
                return
            vertex_base_url = build_vertex_base_url(v_project, v_location)
            self.llm._api_url = vertex_base_url
            self.llm._vertex_credentials = creds
            # Rebuild the httpx client with OAuth2 token
            import httpx as _httpx_chat
            self.llm._client = _httpx_chat.AsyncClient(
                base_url=vertex_base_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=120.0,
            )
        else:
            base_url_map = {
                "anthropic": "https://api.anthropic.com",
                "openai": "https://api.openai.com",
                "google": "https://generativelanguage.googleapis.com",
                "ollama": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                "lmstudio": os.getenv("LMSTUDIO_HOST", "http://localhost:1234"),
                "nvidia": "https://integrate.api.nvidia.com",
                "minimax": os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io"),
            }
            self.llm._api_url = base_url_map.get(new_provider, "")

        render_success(f"Provider switched to [bold]{new_provider}[/bold]")
        self._interactive_model_switch()

        try:
            gc.provider = new_provider
            gc.model = self.config.model
            gc.save()
        except Exception:
            pass

    def _run_cvc_init(self) -> None:
        """Initialize CVC in the current workspace."""
        cvc_dir = self.workspace / ".cvc"
        if cvc_dir.exists():
            render_info(f"CVC already initialized at [bold]{cvc_dir}[/bold]")
            return
        try:
            config = CVCConfig.for_project(
                project_root=self.workspace,
                provider=self.config.provider,
                model=self.config.model,
                mode="cli",
            )
            config.ensure_dirs()
            from cvc.core.database import ContextDatabase as DB
            DB(config)
            render_success(f"CVC initialized at [bold]{cvc_dir}[/bold]")
        except Exception as exc:
            render_error(f"Failed to initialize CVC: {exc}")

    def _start_proxy_background(self) -> None:
        """Start the CVC proxy server in a background process."""
        import subprocess as _sp

        if self._is_proxy_running():
            render_info("CVC Proxy is already running on [bold]http://127.0.0.1:19333[/bold]")
            return

        try:
            if sys.platform == "win32":
                _sp.Popen(
                    ["cmd", "/c", "start", "CVC Proxy", "cvc", "serve"],
                    creationflags=_sp.CREATE_NEW_CONSOLE,
                )
            else:
                _sp.Popen(
                    ["cvc", "serve"],
                    stdout=_sp.DEVNULL,
                    stderr=_sp.DEVNULL,
                    start_new_session=True,
                )
            render_success("CVC Proxy starting in a new terminal window…")
            render_info("Connect your IDE to [bold]http://127.0.0.1:19333/v1[/bold]")
        except Exception as exc:
            render_error(f"Failed to start proxy: {exc}")
            render_info("Start it manually: [bold]cvc serve[/bold]")

    @staticmethod
    def _is_proxy_running(host: str = "127.0.0.1", port: int = 19333) -> bool:
        import socket
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (OSError, ConnectionRefusedError):
            return False

    # ── Phase 9 slash command handlers ───────────────────────────────

    def _handle_cd_command(self, path_str: str) -> None:
        """Change the working directory."""
        if not path_str:
            render_info(f"Current directory: [bold]{self.workspace}[/bold]")
            return
        target = Path(path_str)
        if not target.is_absolute():
            target = self.workspace / target
        target = target.resolve()
        if not target.is_dir():
            render_error(f"Not a directory: {target}")
            return
        self._on_workspace_switched(str(target))

    def _on_workspace_switched(self, new_workspace: str) -> None:
        """Callback fired by the executor's `cvc_switch_workspace` tool.

        v2.91.43: this was the missing link in the workspace-switch chain.
        The executor's `cvc_switch_workspace` would update
        ``self.executor.workspace`` and rebuild the sandbox, but the
        CHAT class's own ``self.workspace`` stayed at the old value, so
        path-relative decisions in the chat loop (display, status
        messages, follow-up tool calls) silently used the wrong
        directory. Now the executor's tool calls this callback, which
        re-anchors the chat class. Same logic as ``_handle_cd_command``
        minus the user-facing render (the tool already prints the
        confirmation).
        """
        from cvc.agent.sandbox import Sandbox
        target = Path(new_workspace).resolve()
        if not target.is_dir():
            # The executor already validated this, but defend against
            # TOCTOU races (folder deleted between validation and now).
            logger.warning(
                "_on_workspace_switched: %s is not a directory", target
            )
            return
        self.workspace = target
        self.executor.workspace = target
        self.executor.sandbox = Sandbox(target)
        # Also re-anchor the hook engine to the new root
        try:
            if hasattr(self.hook_engine, "workspace"):
                self.hook_engine.workspace = target
            if hasattr(self.hook_engine, "_workspace"):
                self.hook_engine._workspace = target
        except Exception:
            pass
        logger.info("workspace switched to %s", target)

    def _handle_add_dir_command(self, path_str: str) -> None:
        """Add an additional directory to the workspace scope."""
        if not path_str:
            render_error("Usage: /add-dir <path>")
            return
        target = Path(path_str).resolve()
        if not target.is_dir():
            render_error(f"Not a directory: {target}")
            return
        # Update sandbox to allow reads/writes in the new dir
        self.executor.sandbox._allowed_write.append(target)
        render_success(f"Added directory: [bold]{target}[/bold]")

    def _handle_fast_command(self, arg: str) -> None:
        """Toggle between fast and quality model.

        Uses the fastest available model for the user's CURRENT provider.
        """
        FAST_MODELS = {
            "anthropic": "claude-haiku-4-5",
            "openai": "gpt-5-mini",
            "google": "gemini-3-flash-preview",
            "ollama": "qwen2.5-coder:7b",
            "lmstudio": "qwen2.5-coder-32b-instruct",
        }
        if arg.lower() in ("off", "quality"):
            # Restore original model
            if hasattr(self, "_original_model"):
                self.config.model = self._original_model
                self.llm.model = self._original_model
                self.cost_tracker.model = self._original_model
                render_success(f"Quality mode restored: [bold]{self._original_model}[/bold]")
                del self._original_model
            else:
                render_info("Already using quality model.")
            return

        # Switch to fast model for current provider
        if not hasattr(self, "_original_model"):
            self._original_model = self.config.model
        fast = FAST_MODELS.get(self.config.provider, self.config.model)
        self.config.model = fast
        self.llm.model = fast
        self.cost_tracker.model = fast
        render_success(f"Fast mode: [bold]{fast}[/bold] (use /fast off to restore)")

    def _handle_doctor_command(self) -> None:
        """Run diagnostics on the CVC environment."""
        from rich.table import Table as _DocTbl
        tbl = _DocTbl(
            title="[bold]CVC Doctor — Diagnostics[/bold]",
            border_style=THEME["primary"],
            show_header=True,
            header_style=f"bold {THEME['primary_bright']}",
        )
        tbl.add_column("Check", width=30)
        tbl.add_column("Status", width=40)

        # CVC init
        cvc_dir = self.workspace / ".cvc"
        if cvc_dir.is_dir():
            tbl.add_row("CVC Initialized", f"[{THEME['success']}]✓ {cvc_dir}[/{THEME['success']}]")
        else:
            tbl.add_row("CVC Initialized", f"[{THEME['warning']}]✗ Not initialized[/{THEME['warning']}]")

        # Git repo
        git_dir = self.workspace / ".git"
        if git_dir.is_dir():
            tbl.add_row("Git Repository", f"[{THEME['success']}]✓ Found[/{THEME['success']}]")
        else:
            tbl.add_row("Git Repository", f"[{THEME['text_dim']}]○ Not a git repo[/{THEME['text_dim']}]")

        # Provider / Key
        key_status = "✓ Set" if (self.llm.api_key if hasattr(self.llm, "api_key") else "") else "○ Not required" if self.config.provider in ("ollama", "lmstudio") else "✗ Missing"
        tbl.add_row(
            f"Provider ({self.config.provider})",
            f"[{THEME['success']}]{key_status}[/{THEME['success']}]" if "✓" in key_status or "○" in key_status else f"[{THEME['warning']}]{key_status}[/{THEME['warning']}]",
        )
        tbl.add_row("Model", self.config.model)

        # CVC.md
        cvc_md = self.workspace / "CVC.md"
        cvc_md2 = self.workspace / ".cvc" / "CVC.md"
        if cvc_md.exists() or cvc_md2.exists():
            tbl.add_row("CVC.md", f"[{THEME['success']}]✓ Found[/{THEME['success']}]")
        else:
            tbl.add_row("CVC.md", f"[{THEME['text_dim']}]○ Not found (use /init-rules)[/{THEME['text_dim']}]")

        # Proxy
        if self._is_proxy_running():
            tbl.add_row("CVC Proxy", f"[{THEME['success']}]✓ Running on :19333[/{THEME['success']}]")
        else:
            tbl.add_row("CVC Proxy", f"[{THEME['text_dim']}]○ Not running[/{THEME['text_dim']}]")

        # Plugins & Skills
        tbl.add_row("Plugins loaded", str(len(self._plugins)))
        tbl.add_row("Skills loaded", str(len(self._skills)))

        # Hooks
        hook_count = len(self.hook_engine._hooks) if hasattr(self.hook_engine, "_hooks") else 0
        tbl.add_row("Hooks configured", str(hook_count))

        # Session
        tbl.add_row("Session ID", self._session.id[:12] + "…" if hasattr(self, "_session") else "N/A")
        tbl.add_row("Turns", str(self.turn_count))

        console.print(tbl)
        console.print()

    def _handle_mode_command(self, arg: str) -> None:
        """Handle /mode — VS Code-style approval mode (default | bypass | autopilot).

        - /mode             → show current mode
        - /mode default     → ask for every non-safe tool
        - /mode bypass      → auto-allow all tools (no prompts)
        - /mode autopilot   → auto-allow + agent continues multi-step autonomously

        Mode is synced to the gateway (if reachable) so the dashboard
        and CLI share state. Locally maps to permission_engine trust modes.
        """
        valid = ("default", "bypass", "autopilot")
        mode = (arg or "").strip().lower()

        if not mode:
            # Show current state
            current = getattr(self, "_approval_mode", "default")
            console.print(f"  Approval mode: [{THEME['accent']}]{current}[/{THEME['accent']}]")
            console.print(f"  [dim]Options: {' · '.join(valid)} — try /mode bypass[/dim]")
            return

        if mode not in valid:
            render_error(f"Invalid mode '{arg}'. Use: {', '.join(valid)}")
            return

        # Local effect — trust-mode mapping
        # default → smart (ask for risky), bypass/autopilot → yolo (auto-allow)
        local_trust = "yolo" if mode in ("bypass", "autopilot") else "smart"
        self.permission_engine.set_trust_mode(local_trust)
        self._approval_mode = mode

        # Try to sync to running gateway so dashboard reflects this too
        synced = False
        try:
            import urllib.request
            import json as _json
            req = urllib.request.Request(
                "http://127.0.0.1:8721/api/chat/approval-mode",
                data=_json.dumps({"mode": mode}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                if resp.status == 200:
                    synced = True
        except Exception:
            pass  # gateway not running — that's fine, CLI-only mode

        if mode == "autopilot":
            console.print(f"  [{THEME['warning']}]🚁 Autopilot ON — tools auto-allowed, agent continues multi-step[/{THEME['warning']}]")
        elif mode == "bypass":
            console.print(f"  [{THEME['warning']}]⚡ Bypass ON — all tools auto-allowed (no prompts)[/{THEME['warning']}]")
        else:
            render_success("Approval mode: DEFAULT — risky tools will ask for permission")
        if synced:
            console.print(f"  [dim]✓ synced to dashboard[/dim]")

    def _handle_trust_command(self, arg: str) -> None:
        """Handle /trust — toggle trust-all or set mode.

        - /trust           → toggle session trust-all ON/OFF
        - /trust strict     → set mode to strict
        - /trust smart      → set mode to smart (default)
        - /trust yolo       → set mode to yolo
        - /trust status     → show current status
        """
        if arg == "status":
            # Explicit status request
            self._show_trust_status()
            return

        if not arg:
            # Toggle session trust-all
            trust_all = self.permission_engine._session_trust_all
            if trust_all:
                # Turn OFF
                self.permission_engine._session_trust_all = False
                render_success("Session trust-all DEACTIVATED — permissions will be checked again.")
            else:
                # Turn ON
                self.permission_engine._session_trust_all = True
                console.print(f"  [{THEME['warning']}]⚠  Session trust-all ACTIVATED — all tools auto-allowed[/{THEME['warning']}]")
            return

        mode = arg.strip().lower()
        if mode not in ("strict", "smart", "yolo"):
            render_error(f"Invalid trust mode: '{arg}'. Use: strict, smart, yolo — or run /trust to toggle.")
            return

        self.permission_engine.set_trust_mode(mode)
        if mode == "yolo":
            console.print(f"  [{THEME['warning']}]⚠  Trust mode set to YOLO — all tools auto-allowed[/{THEME['warning']}]")
        elif mode == "strict":
            render_success("Trust mode set to STRICT — all writes/executes require approval")
        else:
            render_success("Trust mode set to SMART — safe commands auto-allowed, risky ones prompt")

        # Persist to local settings
        from cvc.agent.settings import save_project_settings
        save_project_settings(self.workspace, "trust_mode", mode, local=True)

    def _show_trust_status(self) -> None:
        """Show current trust mode and session trust-all status."""
        mode = self.permission_engine.get_trust_mode()
        trust_all = self.permission_engine._session_trust_all
        summary = self.permission_engine.get_rules_summary()

        console.print()
        console.print(f"  [{THEME['text_dim']}]Trust mode:[/{THEME['text_dim']}]  [bold {THEME['accent']}]{mode}[/bold {THEME['accent']}]")
        if trust_all:
            console.print(f"  [{THEME['warning']}]⚠  Session trust-all is ACTIVE[/{THEME['warning']}]  [{THEME['text_dim']}](run /trust to deactivate)[/{THEME['text_dim']}]")
        else:
            console.print(f"  [{THEME['text_dim']}]Session trust-all: OFF  (run /trust to activate)[/{THEME['text_dim']}]")

        if summary.get("session_approved"):
            console.print(f"  [{THEME['text_dim']}]Session approved:[/{THEME['text_dim']}]  {', '.join(summary['session_approved'])}")
        if summary.get("allow"):
            console.print(f"  [{THEME['text_dim']}]Allow rules:[/{THEME['text_dim']}]  {', '.join(summary['allow'][:5])}")
        if summary.get("deny"):
            console.print(f"  [{THEME['text_dim']}]Deny rules:[/{THEME['text_dim']}]  {', '.join(summary['deny'][:5])}")
        console.print()

    def _handle_plan_mode_command(self, arg: str) -> None:
        """Handle /plan-mode [plan-approve|plan-auto|plan-quiet] command."""
        valid = ("plan-approve", "plan-auto", "plan-quiet")
        if not arg:
            current = getattr(self, "_plan_display_mode", "plan-auto")
            console.print(f"  [{THEME['text_dim']}]Plan display:[/{THEME['text_dim']}]  [bold {THEME['accent']}]{current}[/bold {THEME['accent']}]")
            console.print(f"  [{THEME['text_dim']}]Options: {', '.join(valid)}[/{THEME['text_dim']}]")
            return

        mode = arg.strip().lower()
        if mode not in valid:
            render_error(f"Invalid plan mode: '{arg}'. Use: {', '.join(valid)}")
            return

        self._plan_display_mode = mode
        render_success(f"Plan display set to {mode}")

        # Persist to local settings
        from cvc.agent.settings import save_project_settings
        save_project_settings(self.workspace, "plan_display", mode, local=True)

    def _handle_autopilot_command(self, arg: str) -> None:
        """Handle /autopilot [on|off|yolo|status] command."""
        arg = (arg or "").strip().lower()

        if arg in ("", "status"):
            # Show current state
            state = self.continuation.state
            if state.enabled:
                mode_label = "Full Auto" if state.mode == "full_auto" else "Persistent"
                render_info(
                    f"Autopilot: [bold green]ON[/bold green] ({mode_label}) — "
                    f"iterations: {state.continuation_count}, "
                    f"max: {state.max_iterations}"
                )
            else:
                render_info("Autopilot: [bold red]OFF[/bold red] — agent stops after completing each response")
            return

        if arg == "on":
            self.continuation.enable(mode="persistent")
            render_success(
                "Autopilot ON — agent will continue working until the task is complete. "
                "Tool permissions still apply."
            )
        elif arg == "yolo":
            self.continuation.enable(mode="full_auto")
            # In full_auto mode, also set trust mode to yolo for auto-approvals
            self.permission_engine.load_trust_settings(trust_mode="yolo")
            render_success(
                "Autopilot YOLO — full auto mode enabled. "
                "All tools auto-approved, questions auto-responded."
            )
        elif arg == "off":
            self.continuation.disable()
            render_success("Autopilot OFF — standard single-response behavior restored.")
        else:
            render_error("Usage: /autopilot [on|off|yolo|status]")

    def _handle_release_notes_command(self) -> None:
        """Show CVC changelog/release notes."""
        changelog_paths = [
            self.workspace / "docs" / "CHANGELOG.md",
            self.workspace / "CHANGELOG.md",
        ]
        for p in changelog_paths:
            if p.exists():
                try:
                    content = p.read_text(encoding="utf-8")
                    # Show first 3000 chars
                    if len(content) > 3000:
                        content = content[:3000] + "\n\n... (truncated)"
                    from rich.markdown import Markdown as _Md
                    from rich.panel import Panel as _Pnl
                    console.print(_Pnl(
                        _Md(content),
                        title="[bold]Release Notes[/bold]",
                        border_style=THEME["primary"],
                    ))
                    return
                except Exception as e:
                    render_error(f"Failed to read changelog: {e}")
                    return
        render_info("No CHANGELOG.md found in docs/ or workspace root.")


async def _run_agent_async(
    workspace: Path,
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    no_think: bool = False,
    allowed_tools: list[str] | None = None,
    disallowed_tools: list[str] | None = None,
    print_mode: str | None = None,
    max_turns: int = 0,
    continue_session: bool = False,
    resume_id: str | None = None,
    autopilot: str | None = None,
) -> None:
    """Async implementation of the agent REPL."""
    # Phase E (4.4): Curator — schedule a background skill-maintenance pass
    # on CLI startup if the schedule says we're due. Runs in a daemon thread
    # via curator's internal forking; never blocks the REPL.
    try:
        from cvc.core.curator import maybe_run_curator
        maybe_run_curator(idle_for_seconds=float("inf"))
    except Exception:
        pass

    # Load configuration
    gc = GlobalConfig.load()

    provider = provider or os.getenv("CVC_PROVIDER", gc.provider)
    model = model or os.getenv("CVC_MODEL", gc.model)

    # Resolve API key
    if not api_key:
        env_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "ollama": "",
            "lmstudio": "",
            "github": "GITHUB_TOKEN",
            "vertex": "",  # Vertex uses gcloud ADC, not an API key
        }
        env_key = env_map.get(provider, "")
        api_key = os.getenv(env_key, "") if env_key else ""
        if not api_key:
            api_key = gc.api_keys.get(provider, "")

    if not api_key and provider not in ("ollama", "lmstudio", "vertex"):
        render_error(
            f"No API key found for {provider}. "
            "Run [bold]cvc setup[/bold] or set the environment variable."
        )
        return

    # Build CVC engine
    config = CVCConfig.for_project(
        project_root=workspace,
        provider=provider,
        model=model,
        mode="cli",
    )
    config.ensure_dirs()
    db = ContextDatabase(config)
    engine = CVCEngine(config, db)

    # The CVCEngine.__init__ now auto-hydrates context from the HEAD commit
    # and/or persistent cache, so the context_window is already populated.
    # Log cross-mode detection for the user.
    if engine.context_window:
        try:
            bp = db.index.get_branch(engine.active_branch)
            if bp:
                head_commit = db.index.get_commit(bp.head_hash)
                if head_commit and head_commit.metadata.mode and head_commit.metadata.mode != "cli":
                    logger.info(
                        "Cross-mode restore: %d messages from %s -> CLI (commit %s)",
                        len(engine.context_window),
                        head_commit.metadata.mode.upper(),
                        bp.head_hash[:12],
                    )
        except Exception:
            pass

    # Build LLM client
    base_url_map = {
        "anthropic": "https://api.anthropic.com",
        "openai": "https://api.openai.com",
        "google": "https://generativelanguage.googleapis.com",
        "ollama": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "lmstudio": os.getenv("LMSTUDIO_HOST", "http://localhost:1234"),
        "nvidia": "https://integrate.api.nvidia.com",
        "minimax": os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io"),
    }
    base_url = base_url_map.get(provider, "")
    if provider == "vertex":
        from cvc.adapters.vertex import build_vertex_base_url, get_vertex_credentials
        try:
            _creds, adc_project = get_vertex_credentials()
        except RuntimeError as exc:
            render_error(str(exc))
            return
        v_project = gc.vertex_project_id or os.getenv("VERTEX_PROJECT_ID", "") or adc_project
        v_location = gc.vertex_location or os.getenv("VERTEX_LOCATION", "us-central1")
        base_url = build_vertex_base_url(v_project, v_location)

    llm = AgentLLM(
        provider=provider,
        api_key=api_key or "",
        model=model,
        base_url=base_url,
        no_think=no_think,
    )

    # PERF: Pre-warm the TCP+TLS connection in the background while
    # we show the banner and do onboarding. This saves ~500ms-2s on
    # the first LLM request.
    _warm_task = asyncio.create_task(llm.warm_connection())

    try:
        from cvc import __version__ as version
    except ImportError:
        version = "0.9.0"

    # Show banner
    agent_banner(
        version=version,
        provider=provider,
        model=model,
        branch=engine.active_branch,
        workspace=str(workspace),
    )

    # NOTE: Thinking Model Notice removed in v1.7.6 — users found it
    # distracting.  CVC auto-routes thinking levels transparently.

    # ── Git status on startup ────────────────────────────────────────────
    try:
        from cvc.agent.git_integration import git_status
        gs = git_status(workspace)
        render_git_startup_info(gs)
    except Exception:
        pass

    # ── Trust Workspace Prompt ───────────────────────────────────────────
    try:
        from cvc.agent.trust import is_workspace_trusted, trust_workspace
        if not is_workspace_trusted(workspace):
            console.print(
                f"  [{THEME['warning']}]This workspace has not been trusted yet.[/{THEME['warning']}]"
            )
            from cvc.agent.menus import arrow_confirm
            if arrow_confirm("Do you trust this workspace?", default_yes=True):
                trust_workspace(workspace)
                render_success("Workspace trusted.")
            console.print()
    except Exception:
        pass

    # ── Smart onboarding: check CVC init & proxy status ──────────────────
    _scaffold_prompt = _smart_onboarding(workspace, config)

    # Ensure connection warming completes before first user input
    try:
        await _warm_task
    except Exception:
        pass

    # ── Session resume check ─────────────────────────────────────────────
    _session_resume = False
    target_session = None

    # Handle --continue / --resume flags
    if continue_session or resume_id:
        from cvc.agent.sessions import find_session, get_most_recent_session
        target_session = None
        if resume_id:
            target_session = find_session(resume_id)
            if not target_session:
                render_error(f"Session '{resume_id}' not found.")
        else:
            target_session = get_most_recent_session(str(workspace))
            if not target_session:
                render_info("No previous session found to continue.")

        if target_session:
            render_success(
                f"Continuing session: {target_session.name or target_session.id[:12]} "
                f"({target_session.turn_count} turns)"
            )
            _session_resume = True

    # Check CVC engine context window for resume
    if not _session_resume:
        existing_context = engine.context_window
        if existing_context and len(existing_context) > 2:
            # v2.90.6: do NOT auto-resume. Just inform the user that prior
            # context exists and how to bring it back if they want.
            convo_count = sum(
                1 for m in existing_context if m.role in ("user", "assistant")
            )
            render_info(
                f"{convo_count} message(s) of prior context available in this "
                f"workspace's Merkle DAG. Run `cvc --continue` to resume, or "
                f"just ask — the agent can recall on demand."
            )
            console.print()

    # ── Memory recall ────────────────────────────────────────────────────
    try:
        from cvc.agent.memory import get_relevant_memories
        memories = get_relevant_memories(str(workspace), limit=3)
        if memories and not _session_resume:
            recent = memories[-1]
            # Format the date nicely: "2026-02-17T20:23" → "Feb 17, 2026 at 20:23"
            raw_date = recent.get('date', '?')[:16]
            try:
                from datetime import datetime as _dt
                dt = _dt.fromisoformat(raw_date)
                nice_date = dt.strftime("%b %d, %Y at %H:%M")
            except Exception:
                nice_date = raw_date.replace("T", " at ")
            summary = recent.get('summary', '')
            if len(summary) > 80:
                summary = summary[:77] + "…"
            render_info(
                f"Last session: [bold]{nice_date}[/bold] — "
                f"Started with: {summary}"
            )
            console.print()
    except Exception:
        pass

    # Create session (restore cost data if resuming)
    _resume_target = target_session if _session_resume else None
    session = AgentSession(
        workspace=workspace,
        config=config,
        engine=engine,
        db=db,
        llm=llm,
        allowed_tools=allowed_tools,
        disallowed_tools=disallowed_tools,
        resume_session=_resume_target,
    )

    # Apply max_turns if specified
    if max_turns > 0:
        session._max_turns = max_turns

    # Enable autopilot if requested via CLI
    if autopilot:
        mode = "full_auto" if autopilot == "yolo" else "persistent"
        session.continuation.enable(mode=mode)
        if autopilot == "yolo":
            session.permission_engine.set_trust_mode("yolo")

    # ── Check for prompt_toolkit availability ────────────────────────────
    _has_prompt_toolkit = False
    try:
        import prompt_toolkit
        _has_prompt_toolkit = True
    except ImportError:
        pass

    # ── Fire SessionStart hooks ──────────────────────────────────────────
    session.hook_engine.fire(
        HookEvent.SESSION_START,
        {"workspace": str(workspace), "model": model, "branch": engine.active_branch},
    )

    # ── Non-interactive (print) mode ─────────────────────────────────────
    if print_mode:
        try:
            # Honour slash commands in -p mode too, so `cvc agent -p /help`
            # / `cvc agent -p /status` work without hitting the LLM.
            if print_mode.lstrip().startswith("/"):
                await session.handle_slash_command(print_mode.strip())
            else:
                await session.run_turn(print_mode)
        except Exception as exc:
            render_error(f"Error: {exc}")
            logger.error("Print mode error: %s", exc, exc_info=True)
        finally:
            session._session.save_cost(session.cost_tracker)
            session._session.save()
            session.hook_engine.fire(
                HookEvent.SESSION_STOP,
                {
                    "turns": session.turn_count,
                    "cost": session.cost_tracker.format_summary(),
                    "workspace": str(workspace),
                },
            )
            session._save_session_memory()
            await llm.close()
            db.close()
        return

    # REPL loop
    _scaffold_injected = False
    try:
        while True:
            # ── Auto-inject scaffold prompt on first iteration ────────
            if _scaffold_prompt and not _scaffold_injected:
                _scaffold_injected = True
                user_input = _scaffold_prompt
            else:
                try:
                    if _has_prompt_toolkit:
                        user_input = await get_input_with_completion(
                            branch=engine.active_branch,
                            turn=session.turn_count + 1,
                            health_bar=session._health_bar,
                        )
                    else:
                        user_input = await asyncio.to_thread(
                            print_input_prompt,
                            engine.active_branch,
                            session.turn_count + 1,
                            session._health_bar,
                        )
                except (KeyboardInterrupt, EOFError):
                    break

            if not user_input:
                continue

            # ── Multi-line input: backslash continuation ─────────────
            while user_input.endswith("\\"):
                user_input = user_input[:-1] + "\n"
                try:
                    continuation = await asyncio.to_thread(
                        lambda: input("  ... ").rstrip()
                    )
                    user_input += continuation
                except (KeyboardInterrupt, EOFError):
                    break

            # Handle slash commands
            if user_input.startswith("/"):
                should_continue = await session.handle_slash_command(user_input)
                if not should_continue:
                    break
                continue

            # ── Ctrl+V pasted images (from prompt_toolkit keybinding) ──
            # If the user pressed Ctrl+V during input and there was an
            # image in the clipboard, it's now in _pending_paste_images.
            _ctrlv_images = get_pending_paste_images()
            if _ctrlv_images:
                import hashlib as _hlv
                import re as _re
                # Strip ALL [image N] markers from user text before sending to LLM
                _marker_re = _re.compile(r'\s*\[image \d+\]\s*')
                clean_input = _marker_re.sub(' ', user_input).strip()

                for idx, (b64_data, mime_type) in enumerate(_ctrlv_images):
                    label = f"image {idx + 1}"
                    _build_image_message(
                        session.messages, session.config.provider,
                        b64_data, mime_type,
                        clean_input or "Please analyze this image.",
                    )
                    render_success(f"✓ {label}")
                session._last_clipboard_hash = _hlv.sha256(
                    _ctrlv_images[0][0].encode()
                ).hexdigest()
                try:
                    await session.run_turn_no_append(clean_input or "analyze this image")
                except KeyboardInterrupt:
                    render_info("Interrupted. Type /exit to quit.")
                except Exception as exc:
                    render_error(f"Unexpected error: {exc}")
                    logger.error("Turn error: %s", exc, exc_info=True)
                continue

            # ── Smart clipboard image detection ─────────────────────
            # Clipboard images are attached ONLY when the user
            # explicitly signals intent:
            #   1. Ctrl+V         → handled above (prompt_toolkit)
            #   2. /paste         → slash command
            #   3. Keyword-based  → prompt mentions "screenshot",
            #      "paste", "clipboard", "look at this", etc.
            #   4. File path      → prompt contains e.g. screenshot.png
            #
            # We intentionally do NOT auto-attach based on a new
            # clipboard hash alone — that could leak accidental or
            # private screenshots the user never intended to share.
            import hashlib as _hl
            import re as _word_re

            _image_keywords = {
                "screenshot", "pasted", "paste", "clipboard",
                "this picture", "this photo", "attached", "look at this",
                "see this", "check this",
            }
            _IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff"}
            _lower_input = user_input.lower()
            _auto_pasted = False

            # Strategy A: detect inline image file paths in the prompt
            _path_attached = False
            for token in user_input.split():
                _p = Path(token)
                if _p.suffix.lower() in _IMAGE_EXTS:
                    candidate = _p if _p.is_absolute() else (session.workspace / _p)
                    if candidate.exists():
                        try:
                            _idata = candidate.read_bytes()
                            _b64 = base64.b64encode(_idata).decode("utf-8")
                            _mime = mimetypes.guess_type(str(candidate))[0] or "image/png"
                            _build_image_message(
                                session.messages, session.config.provider,
                                _b64, _mime, user_input,
                            )
                            render_success(f"✓ image (file: {candidate.name})")
                            _path_attached = True
                        except OSError:
                            pass

            if _path_attached:
                _auto_pasted = True
            else:
                # Strategy B: clipboard image — ONLY when user explicitly
                # mentions image-related keywords.  We do NOT auto-attach
                # based on "new hash" alone because the user may have taken
                # an accidental or private screenshot that they never
                # intended to share with the LLM.
                # Use word-boundary matching to avoid false positives
                # (e.g. "images" should NOT trigger clipboard grab).
                _has_keyword = any(
                    _word_re.search(r'\b' + _word_re.escape(kw) + r'\b', _lower_input)
                    for kw in _image_keywords
                )
                if _has_keyword:
                    try:
                        clip_images = _grab_clipboard_images()
                    except Exception as _clip_exc:
                        logger.debug("Clipboard image grab failed: %s", _clip_exc)
                        clip_images = []
                    if clip_images:
                        _clip_hash = _hl.sha256(clip_images[0][0].encode()).hexdigest()
                        for idx, (b64_data, mime_type) in enumerate(clip_images):
                            label = f"image {idx + 1}"
                            _build_image_message(
                                session.messages, session.config.provider,
                                b64_data, mime_type, user_input,
                            )
                            render_success(f"✓ {label}")
                        session._last_clipboard_hash = _clip_hash
                        _auto_pasted = True

            # Run ordinary turn (skip if images were auto-pasted — run_turn for the text)
            try:
                # ── Auto-retry intent detection ──────────────────────────
                # Check if the user's short message suggests retry intent
                # (e.g., "this is wrong", "redo this", "try again")
                if not _auto_pasted and await session._check_retry_intent(user_input):
                    continue  # Retry flow handled it

                if _auto_pasted:
                    # Image messages already appended with user text;
                    # run the agentic loop without re-adding user message
                    await session.run_turn_no_append(user_input)
                else:
                    await session.run_turn(user_input)
            except KeyboardInterrupt:
                render_info("Interrupted. Type /exit to quit.")
                continue
            except Exception as exc:
                render_error(f"Unexpected error: {exc}")
                logger.error("Turn error: %s", exc, exc_info=True)
                continue

    finally:
        # Persist cost data before shutdown
        session._session.save_cost(session.cost_tracker)
        session._session.save()
        # Fire SessionStop hooks
        session.hook_engine.fire(
            HookEvent.SESSION_STOP,
            {
                "turns": session.turn_count,
                "cost": session.cost_tracker.format_summary(),
                "workspace": str(workspace),
            },
        )
        # ── Cognitive Hooks: on_session_stop (Phase B) ───────────────────
        # Triggers F3 (User Model update), F4 (Prompt Evolution check),
        # F10 (Metacognition snapshot persist).
        if getattr(session, "_cognitive_hooks", None) is not None:
            try:
                await session._cognitive_hooks.on_session_stop({
                    "turns": session.turn_count,
                    "workspace": str(workspace),
                })
            except Exception as _csx:
                logger.debug("CognitiveHooks session_stop failed (non-fatal): %s", _csx)
        # Save session memory
        session._save_session_memory()
        # Cleanup
        render_goodbye()
        await llm.close()
        db.close()


def _is_proxy_running_standalone(host: str = "127.0.0.1", port: int = 13421) -> bool:
    """Check if the CVC proxy is listening on the given port."""
    import socket
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (OSError, ConnectionRefusedError):
        return False


def _project_scaffolding_wizard(workspace: Path) -> str | None:
    """
    Multi-step arrow-key wizard for scaffolding a new project.

    Runs the official CLI scaffolding commands directly (e.g. ``uv init``,
    ``npx create-next-app``) instead of delegating file creation to the LLM.

    Returns a brief context prompt for the LLM (so it knows what was created),
    or None if the user cancels.
    """
    from cvc.agent.menus import arrow_confirm, arrow_select
    from cvc.agent.scaffolder import SCAFFOLD_RECIPES, run_scaffold

    console.print()
    console.print(
        f"  [{THEME['accent']}]This workspace looks empty.[/{THEME['accent']}]  "
        f"[{THEME['text_dim']}]Let's scaffold a new project.[/{THEME['text_dim']}]"
    )
    console.print()

    # ── Step 1: Project type ──
    project_types = [
        ("Web Application", "web"),
        ("API / Backend Service", "api"),
        ("CLI Tool", "cli"),
        ("Library / Package", "library"),
        ("AI Agent / Chatbot", "ai"),
        ("Mobile Application", "mobile"),
        ("Desktop Application", "desktop"),
        ("Other", "other"),
    ]
    project_type = arrow_select("What kind of project?", project_types)
    if project_type is None:
        return None

    # ── Step 2: Tech stack (dynamic) ──
    # The second element of each tuple is the *recipe key* in SCAFFOLD_RECIPES.
    # Stacks without a recipe (Kotlin Android, Swift iOS) fall back to LLM.
    stack_map: dict[str, list[tuple[str, str]]] = {
        "web": [
            ("React + TypeScript (Vite)", "React with TypeScript (Vite)"),
            ("Next.js", "Next.js (React framework)"),
            ("Vue.js", "Vue 3 with Vite"),
            ("Angular", "Angular with TypeScript"),
            ("Svelte / SvelteKit", "SvelteKit"),
            ("Python + Flask", "Flask web app"),
            ("Python + Django", "Django web app"),
            ("Python + FastAPI + Jinja", "FastAPI with Jinja2 templates"),
        ],
        "api": [
            ("Python + FastAPI", "FastAPI REST API"),
            ("Python + Flask", "Flask REST API"),
            ("Node.js + Express", "Express.js API"),
            ("Go + Gin", "Gin HTTP API"),
            ("Rust + Actix", "Actix-web API"),
            (".NET Web API", "ASP.NET Core Web API"),
        ],
        "cli": [
            ("Python + Click", "Click CLI app"),
            ("Python + Typer", "Typer CLI app"),
            ("Node.js + Commander", "Commander.js CLI"),
            ("Go", "Go CLI with cobra"),
            ("Rust + Clap", "Rust CLI with clap"),
        ],
        "library": [
            ("Python package", "Python library with pyproject.toml"),
            ("npm package (TypeScript)", "TypeScript npm package"),
            ("Rust crate", "Rust library crate"),
            ("Go module", "Go library module"),
        ],
        "ai": [
            ("Python + OpenAI SDK", "OpenAI chat agent"),
            ("Python + LangChain", "LangChain agent"),
            ("Python + AutoGen", "AutoGen multi-agent"),
            ("TypeScript + Vercel AI SDK", "Vercel AI SDK bot"),
        ],
        "mobile": [
            ("React Native", "React Native (Expo)"),
            ("Flutter", "Flutter app"),
            ("Kotlin (Android)", "Kotlin Android app"),
            ("Swift (iOS)", "Swift iOS app"),
        ],
        "desktop": [
            ("Electron", "Electron desktop app"),
            ("Tauri", "Tauri desktop app"),
            ("Python + PyQt", "PyQt6 desktop app"),
            (".NET MAUI", ".NET MAUI cross-platform app"),
        ],
    }

    stacks = stack_map.get(project_type)
    if stacks:
        stack_choice = arrow_select("Pick a tech stack", stacks)
        if stack_choice is None:
            return None
    else:
        # "other" — free-text
        stack_choice = console.input(
            f"  [{THEME['text_dim']}]Describe your tech stack:[/{THEME['text_dim']}] "
        ).strip()
        if not stack_choice:
            return None

    # ── Step 3: Confirm ──
    type_label = next(l for l, v in project_types if v == project_type)
    stack_label = stack_choice if isinstance(stack_choice, str) else stack_choice
    # For display, find the human label from the stacks list
    if stacks:
        for label, val in stacks:
            if val == stack_choice:
                stack_label = label
                break

    console.print()
    console.print(f"  [{THEME['accent']}]Project:[/{THEME['accent']}]  {type_label}")
    console.print(f"  [{THEME['accent']}]Stack:[/{THEME['accent']}]    {stack_label}")
    console.print()

    if not arrow_confirm("Scaffold this project?", default_yes=True):
        return None

    # ── Step 4: Execute scaffolding ──────────────────────────────────
    # If a deterministic recipe exists, run it directly instead of
    # delegating to the LLM.
    if stack_choice in SCAFFOLD_RECIPES:
        import re as _re

        _ANSI_RE = _re.compile(r"\x1b\[[0-9;]*[mGKABCDEFHJST]")

        def _on_cmd(cmd: str, idx: int, total: int) -> None:
            console.print(
                f"  [{THEME['accent']}]Step {idx}/{total}[/{THEME['accent']}] │ "
                f"[{THEME['text_dim']}]{cmd}[/{THEME['text_dim']}]"
            )

        def _on_output(line: str) -> None:
            clean = _ANSI_RE.sub("", line).strip()
            # Skip blank / progress-bar lines (npm spam) and very short noise
            if len(clean) < 3:
                return
            if all(c in " .-=>|\\/" for c in clean):
                return
            console.print(
                f"    [{THEME['text_dim']}]{clean[:120]}[/{THEME['text_dim']}]",
                highlight=False,
            )

        console.print()
        result = run_scaffold(
            workspace, stack_choice, on_command=_on_cmd, on_output=_on_output
        )

        if result.success:
            file_count = len(result.files_created)
            render_success(
                f"Scaffolded [bold]{stack_label}[/bold] project "
                f"({file_count} files created)"
            )
            if result.files_created:
                # Show a compact tree of top-level entries
                shown = result.files_created[:15]
                for f in shown:
                    console.print(f"    [{THEME['text_dim']}]{f}[/{THEME['text_dim']}]")
                if len(result.files_created) > 15:
                    console.print(
                        f"    [{THEME['text_dim']}]… and "
                        f"{len(result.files_created) - 15} more[/{THEME['text_dim']}]"
                    )
            console.print()
            # Return a context summary so the LLM knows what exists
            files_brief = ", ".join(result.files_created[:20])
            return (
                f"The workspace has been automatically scaffolded as a {type_label} "
                f"project using {stack_label}. The project structure is already set up "
                f"with dependencies installed. Files: {files_brief}. "
                f"Do NOT re-create or overwrite these files. "
                f"Ask the user what they'd like to build next."
            )
        else:
            # Scaffold failed — show error, fall back to LLM
            render_error(f"Scaffolding failed: {result.output}")
            console.print(
                f"  [{THEME['text_dim']}]Falling back to AI-assisted scaffolding…"
                f"[/{THEME['text_dim']}]"
            )
            console.print()

    # Fallback: no recipe (e.g. Kotlin, Swift, Other) or recipe failed
    return (
        f"Create a new {type_label} project using {stack_label} in the current workspace. "
        f"Set up the standard project structure with proper configuration files, "
        f"a README, .gitignore, dependency manifests, and a minimal working example. "
        f"Follow current best practices for this stack."
    )


def _smart_onboarding(workspace: Path, config: CVCConfig) -> str | None:
    """
    Run at agent startup to check readiness and offer to fix issues inline.

    Returns a scaffold prompt string if the user completed the scaffolding
    wizard, or None otherwise.
    """

    cvc_dir = workspace / ".cvc"
    hints_shown = False
    scaffold_prompt: str | None = None

    if not cvc_dir.exists():
        console.print(
            f"  [{THEME['warning']}]![/{THEME['warning']}] "
            f"CVC is not initialized in this workspace."
        )
        console.print(
            f"  [{THEME['text_dim']}]Without init, time-travel features (commit, branch, restore) "
            f"won't persist.[/{THEME['text_dim']}]"
        )

        from cvc.agent.menus import arrow_confirm
        if arrow_confirm("Initialize CVC here now?", default_yes=True):
            try:
                config.ensure_dirs()
                from cvc.core.database import ContextDatabase as _DB
                _DB(config)
                render_success(f"CVC initialized at [bold]{cvc_dir}[/bold]")
            except Exception as exc:
                render_error(f"Failed to initialize: {exc}")
        else:
            render_info(
                "Skipped. You can run [bold]/init[/bold] anytime, or [bold]cvc init[/bold] from your shell."
            )
        console.print()
        hints_shown = True

    # ── Scaffold wizard for empty workspaces ─────────────────────────────
    from cvc.agent.auto_context import is_empty_workspace
    if is_empty_workspace(workspace):
        scaffold_prompt = _project_scaffolding_wizard(workspace)

    if not hints_shown:
        pass

    return scaffold_prompt


def run_agent(
    workspace: Path | None = None,
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    no_think: bool = False,
    allowed_tools: list[str] | None = None,
    disallowed_tools: list[str] | None = None,
    print_mode: str | None = None,
    max_turns: int = 0,
    continue_session: bool = False,
    resume_id: str | None = None,
    autopilot: str | None = None,
) -> None:
    """
    Start the CVC Agent interactive REPL.

    This is the main entry point called by the CLI.
    """
    if workspace is None:
        workspace = Path.cwd()
    workspace = workspace.resolve()

    # Handle piped stdin for non-interactive mode
    if print_mode is None and not sys.stdin.isatty():
        # Reading from pipe: cat file | cvc agent -p "prompt"
        # If -p wasn't given, read stdin as the prompt
        stdin_data = sys.stdin.read().strip()
        if stdin_data:
            print_mode = stdin_data

    try:
        asyncio.run(_run_agent_async(
            workspace, provider, model, api_key,
            no_think=no_think,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
            print_mode=print_mode,
            max_turns=max_turns,
            continue_session=continue_session,
            resume_id=resume_id,
            autopilot=autopilot,
        ))
    except KeyboardInterrupt:
        pass
