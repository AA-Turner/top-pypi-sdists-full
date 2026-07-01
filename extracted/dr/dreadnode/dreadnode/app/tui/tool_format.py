"""Pre-render helpers for tool calls — NOT the tool display layer.

The actual tool display layer lives in :mod:`dreadnode.app.tui.widgets.tool`
(the ``ToolCall`` Textual widget + ``render_tool_call`` Rich renderer).
This module is the pre-render step those consumers need: given a tool
name + args, produce a compact label (``"read(pyproject.toml)"``); given
a tool name + args + result, produce a one-line summary (``"Read 42
lines."``). Messages have no equivalent pre-render module because
``Message.content`` — the wire format is already
displayable — whereas tool calls require computation to pick an
interesting arg to show inline and to compress large results.

The reason this lives at the ``tui/`` top level rather than inside the
``widgets/`` folder is that it has no Textual/Rich dependency — that
lets :class:`CapabilitiesManager` import it to re-seed the registry on
every runtime refresh without pulling widget code into the manager
layer.

The registry API (:func:`register_tool_key_args`, :func:`register_tool_summarizer`,
:func:`clear_tool_registry`) lets capabilities teach the TUI about
their own tools without editing this file. The :class:`CapabilitiesManager`
seeds it from each tool's JSON Schema via :func:`derive_key_args_from_schema`
on every ``/api/tools`` refresh. Built-in tools get sensible defaults
via :data:`_BUILTIN_TOOL_KEY_ARGS` installed at import time, and tools
with no usable schema fall back to the first short string argument.
"""

import json
import re
import typing as t
from pathlib import Path

from dreadnode.tools.web_search import NO_RESULTS_WARNING

_PATH_ARGS = {"file_path", "path", "filename", "url"}


def _abbreviate_home_path(path: str) -> str:
    """Replace ``$HOME/...`` with ``~/...`` for display.

    Cache paths land under ``~/.dreadnode/...`` by default, and the raw
    absolute form leaks the user's home dir / username into log captures
    and screenshots. Only abbreviates when the path actually sits under
    home — custom-cache overrides that point elsewhere render verbatim.
    """
    if not path:
        return path
    try:
        home = Path.home()
        rel = Path(path).resolve().relative_to(home.resolve())
    except (ValueError, OSError, RuntimeError):
        return path
    return f"~/{rel.as_posix()}" if str(rel) != "." else "~"


# =============================================================================
# Registration API
# =============================================================================

Summarizer = t.Callable[[str, dict[str, t.Any], t.Any], str | None]

# Populated by :func:`register_tool_key_args`. Lowercased tool name →
# ordered list of argument keys to try when building a compact label.
_TOOL_KEY_ARGS: dict[str, list[str]] = {}

# Populated by :func:`register_tool_summarizer`. Lowercased tool name →
# a ``(name, args, result) -> str | None`` callable that returns a
# compact one-line summary of the result. ``None`` means "fall back to
# the generic first-line summarizer".
_TOOL_SUMMARIZERS: dict[str, Summarizer] = {}


def register_tool_key_args(name: str, keys: list[str]) -> None:
    """Register the preferred argument keys for a tool's compact label."""
    if not name:
        return
    _TOOL_KEY_ARGS[name.lower()] = list(keys)


def register_tool_summarizer(name: str, summarizer: Summarizer) -> None:
    """Register a per-tool result summarizer."""
    if not name:
        return
    _TOOL_SUMMARIZERS[name.lower()] = summarizer


def clear_tool_registry() -> None:
    """Reset the registry and re-install the built-in defaults."""
    _TOOL_KEY_ARGS.clear()
    _TOOL_SUMMARIZERS.clear()
    for name, keys in _BUILTIN_TOOL_KEY_ARGS.items():
        _TOOL_KEY_ARGS[name] = list(keys)
    _TOOL_SUMMARIZERS.update(_BUILTIN_TOOL_SUMMARIZERS)


def derive_key_args_from_schema(schema: dict[str, t.Any] | None) -> list[str]:
    """Pick argument keys to show in a compact label from a JSON Schema.

    Prefers the schema's ``required`` list in order, then falls back to
    the order of ``properties``. Keeps only string-typed properties
    (including ``anyOf``/``oneOf`` with a string branch) since non-string
    values rarely make useful inline labels. Returns at most three keys.
    """
    if not isinstance(schema, dict):
        return []
    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return []

    required = schema.get("required")
    ordered: list[str] = []
    seen: set[str] = set()
    if isinstance(required, list):
        for name in required:
            if isinstance(name, str) and name in properties and name not in seen:
                ordered.append(name)
                seen.add(name)
    for name in properties:
        if isinstance(name, str) and name not in seen:
            ordered.append(name)
            seen.add(name)

    def _is_string_like(prop: t.Any) -> bool:
        if not isinstance(prop, dict):
            return False
        prop_type = prop.get("type")
        if prop_type == "string":
            return True
        if isinstance(prop_type, list) and "string" in prop_type:
            return True
        for key in ("anyOf", "oneOf"):
            branches = prop.get(key)
            if isinstance(branches, list) and any(_is_string_like(b) for b in branches):
                return True
        return False

    keys = [name for name in ordered if _is_string_like(properties.get(name))]
    return keys[:3]


# =============================================================================
# Built-in seed data
# =============================================================================
#
# These are the tools ``dreadnode.tools.default_tools()`` ships — the
# "built-in" capability group the runtime server always exposes. They
# are seeded on import and re-installed by :func:`clear_tool_registry`.

_BUILTIN_TOOL_KEY_ARGS: dict[str, list[str]] = {
    # Execution tools
    "bash": ["command", "cmd"],
    "shell": ["command", "cmd"],
    "execute": ["cmd"],
    "python": ["code"],
    "dreadnode_cli": ["command"],
    # File tools
    "read": ["file_path", "path", "filename", "url"],
    "read_file": ["file_path", "path"],
    "write": ["file_path", "path"],
    "write_file": ["file_path", "path"],
    "edit": ["file_path", "path"],
    "edit_file": ["path", "file_path"],
    "multiedit": ["path"],
    "insert_lines": ["path"],
    "delete_lines": ["path"],
    "apply_patch": ["patch_text"],
    # Search tools
    "grep": ["pattern", "query"],
    "search": ["pattern", "query"],
    "glob": ["pattern"],
    "find": ["pattern", "path"],
    "ls": ["path"],
    # Web tools
    "web_search": ["query"],
    "fetch": ["url"],
    "web_extract": ["urls"],
    # Reporting and recall tools
    "report": ["title", "filename", "source_path"],
    "session_search": ["query"],
    # Interaction tools
    "think": ["thought"],
    # ``ask_user`` uses a custom label resolver — see ``_ask_user_label_from_args``.
    "ask_user": [],
    "finish_task": ["summary"],
}


def _first_line(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    first = lines[0]
    if len(lines) > 1:
        return f"{first[:100]}..."
    return first[:120] + ("..." if len(first) > 120 else "")


def _get_result_text(res: t.Any) -> str:
    if isinstance(res, str):
        return res
    if isinstance(res, dict):
        return (
            str(res.get("stdout", ""))
            or str(res.get("output", ""))
            or str(res.get("error", ""))
            or str(res.get("stderr", ""))
        )
    if isinstance(res, list):
        # Multimodal content-part lists (e.g. a ``read`` image result is a text
        # caption + an image part). Pull text out of each part and skip image/
        # video / audio parts, whose repr would otherwise bloat or corrupt the summary.
        parts: list[str] = []
        for x in res:
            if isinstance(x, dict):
                parts.append(str(x.get("text", "")))
                continue
            text = getattr(x, "text", None)
            if isinstance(text, str):
                parts.append(text)
                continue
            if getattr(x, "type", None) in ("image_url", "file", "input_audio"):
                continue
            parts.append(str(x))
        return "\n".join(p for p in parts if p)
    return str(res)


_READ_EOF_RE = re.compile(r"\(End of file — (?P<n>\d+) lines? total\)")
_READ_PAGE_RE = re.compile(r"\(Showing lines \d+-\d+ of (?P<n>\d+)\.")
_READ_DIR_ENTRIES_RE = re.compile(r"\((?P<n>\d+) entries\)")
_READ_DIR_PAGE_RE = re.compile(r"\(Showing (?P<shown>\d+) of (?P<total>\d+) entries")


def _summarize_read(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    text = _get_result_text(result)
    if not text:
        return None

    head = text.splitlines()[0] if text else ""
    # Image/video reads return a "Read <media> · <fmt> · <size>" caption (the
    # path is already shown in the call label, so it is intentionally not repeated).
    if head.startswith(("Read image", "Read video")):
        return head
    if head.startswith("PDF: "):
        return f"PDF: {head.removeprefix('PDF: ').rsplit('/', 1)[-1]}."

    dir_page = _READ_DIR_PAGE_RE.search(text)
    if dir_page:
        return f"Listed {dir_page.group('shown')} of {dir_page.group('total')} entries."
    dir_total = _READ_DIR_ENTRIES_RE.search(text)
    if dir_total:
        n = int(dir_total.group("n"))
        return f"Listed {n} entr{'ies' if n != 1 else 'y'}."

    page = _READ_PAGE_RE.search(text)
    if page:
        return f"Read partial file ({page.group('n')} lines total)."
    eof = _READ_EOF_RE.search(text)
    if eof:
        n = int(eof.group("n"))
        return f"Read {n} line{'s' if n != 1 else ''}."

    # Older/foreign result text without our footers — fall back to a raw count.
    lines = len(text.splitlines())
    return f"Read {lines} line{'s' if lines != 1 else ''}."


_SEARCH_NO_MATCH_RE = re.compile(r"^(No matches found|No files found)")
_SEARCH_FOUND_RE = re.compile(r"^(?P<header>Found .+?)(?:\s*\([^)]*\))?$")


def _summarize_search(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    text = _get_result_text(result).strip()
    if not text:
        return None

    first = text.splitlines()[0].strip()

    if _SEARCH_NO_MATCH_RE.match(first):
        return f"{first}."

    found = _SEARCH_FOUND_RE.match(first)
    if found:
        return f"{found.group('header').strip()}."

    # glob's default content is "path\npath\n..." with no header. Notice
    # lines start with "(" — exclude them from the count.
    file_lines = [
        line for line in text.splitlines() if line.strip() and not line.strip().startswith("(")
    ]
    n = len(file_lines)
    return f"Found {n} result{'s' if n != 1 else ''}."


def _summarize_list(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    text = _get_result_text(result).strip()
    if not text:
        return None
    if text.startswith("Empty directory"):
        return "Empty directory."
    items = sum(
        1 for line in text.splitlines() if line.strip() and not line.strip().startswith("(")
    )
    return f"Listed {items} item{'s' if items != 1 else ''}."


def _summarize_shell(_name: str, args: dict[str, t.Any], result: t.Any) -> str | None:
    text = _get_result_text(result)
    cmd = str(args.get("command", "") or args.get("cmd", "") or "").strip()
    if cmd.startswith("ls"):
        items = sum(1 for line in text.splitlines() if line.strip())
        return f"Listed {items} item{'s' if items != 1 else ''}."
    return _first_line(text) or None


def _summarize_edit(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    text = _get_result_text(result)
    return _first_line(text) or "File edited."


_REPORT_RESULT_RE = re.compile(r"^Saved (?P<format>markdown|text) report to (?P<path>.+)$")


def parse_report_result(result: t.Any) -> tuple[str, str] | None:
    """Pull ``(format, absolute_path)`` out of a ``report`` tool's return string.

    The contract is owned by ``dreadnode.tools.report.report`` —
    ``"Saved {format} report to {path}"`` where format ∈ {markdown, text}.
    Returns None if the string doesn't match (e.g. the tool errored,
    a custom report-like tool wrote a different shape, or a downstream
    rewrap mangled the prefix). Callers must handle the None case
    rather than crash on malformed input.
    """
    text = _get_result_text(result)
    if not text:
        return None
    match = _REPORT_RESULT_RE.match(text.strip())
    if match is None:
        return None
    return match.group("format"), match.group("path")


def _summarize_report(_name: str, args: dict[str, t.Any], result: t.Any) -> str | None:
    parsed = parse_report_result(result)
    if parsed is None:
        return _first_line(_get_result_text(result)) or None
    _format, path = parsed
    display_path = _abbreviate_home_path(path)
    content = args.get("content")
    if not isinstance(content, str):
        return display_path
    lines = len(content.splitlines())
    return f"Wrote {lines} line{'s' if lines != 1 else ''} to {display_path}"


def _ask_user_label_from_args(args: dict[str, t.Any]) -> str | None:
    """Compact label for the ``ask_user`` bundle shape.

    For 1-question prompts surface the question text; for bundles
    surface the count so the header doesn't dump a list of dicts.
    """
    questions = args.get("questions")
    if not isinstance(questions, list) or not questions:
        return None
    if len(questions) > 1:
        return f"{len(questions)} questions"
    first = questions[0]
    if isinstance(first, dict):
        prompt = first.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            return prompt.strip()
    return None


def _report_label_from_args(args: dict[str, t.Any]) -> str | None:
    for key in ("title", "filename", "source_path"):
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    content = args.get("content")
    if not isinstance(content, str):
        return None
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*$", stripped)
        return heading.group(1).strip() if heading else stripped
    return None


def _try_parse_structured_payload(result: t.Any) -> dict[str, t.Any] | None:
    if isinstance(result, dict):
        return result
    if not isinstance(result, str):
        return None
    try:
        parsed = json.loads(result)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _summarize_web_search(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    payload = _try_parse_structured_payload(result)
    if payload is None:
        return _first_line(_get_result_text(result)) or None

    results = payload.get("results")
    if not isinstance(results, list):
        return _first_line(_get_result_text(result)) or None

    count = payload.get("result_count", len(results))
    if not isinstance(count, int):
        count = len(results)
    if count > 0:
        return f"Found {count} web result{'s' if count != 1 else ''}."

    # Zero-hit payloads conflate genuinely-empty / all-filtered / backend-error;
    # the agent has the full structured payload but the TUI viewer only sees
    # this summary, so name the backend and surface the first warning.
    raw_backend = payload.get("backend")
    backend = raw_backend if isinstance(raw_backend, str) else None
    suffix = f" ({backend})" if backend else ""

    warnings = payload.get("warnings")
    detail = (
        next(
            (w.strip().rstrip(".") for w in warnings if isinstance(w, str) and w.strip()),
            None,
        )
        if isinstance(warnings, list)
        else None
    )

    if payload.get("success") is False:
        return f"Web search failed{suffix}: {detail}." if detail else f"Web search failed{suffix}."

    if detail and detail != NO_RESULTS_WARNING.rstrip("."):
        return f"No web results{suffix}: {detail}."
    return f"No web results{suffix}." if backend else "No web results found."


def _summarize_fetch(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    payload = _try_parse_structured_payload(result)
    if payload is None:
        return _first_line(_get_result_text(result)) or None

    title = payload.get("title")
    final_url = payload.get("final_url") or payload.get("url")
    truncated = bool(payload.get("truncated"))

    if isinstance(title, str) and title.strip():
        suffix = " (truncated)." if truncated else "."
        return f"Fetched {title.strip()}{suffix}"
    if isinstance(final_url, str) and final_url.strip():
        suffix = " (truncated)." if truncated else "."
        return f"Fetched {final_url.strip()}{suffix}"
    return "Fetched web content."


def _summarize_web_extract(_name: str, _args: dict[str, t.Any], result: t.Any) -> str | None:
    payload = _try_parse_structured_payload(result)
    if payload is None:
        return _first_line(_get_result_text(result)) or None

    requested = payload.get("requested_count")
    extracted = payload.get("extracted_count")
    if not isinstance(requested, int) or not isinstance(extracted, int):
        return _first_line(_get_result_text(result)) or None

    if requested == 0:
        return "No pages extracted."
    if extracted == requested:
        return f"Extracted {extracted} page{'s' if extracted != 1 else ''}."
    return f"Extracted {extracted} of {requested} pages."


_BUILTIN_TOOL_SUMMARIZERS: dict[str, Summarizer] = {
    "read": _summarize_read,
    "read_file": _summarize_read,
    "glob": _summarize_search,
    "find": _summarize_search,
    "search": _summarize_search,
    "grep": _summarize_search,
    "ls": _summarize_list,
    "list_directory": _summarize_list,
    "list": _summarize_list,
    "web_search": _summarize_web_search,
    "fetch": _summarize_fetch,
    "web_extract": _summarize_web_extract,
    "bash": _summarize_shell,
    "shell": _summarize_shell,
    "run_command": _summarize_shell,
    "execute": _summarize_shell,
    "edit": _summarize_edit,
    "replace": _summarize_edit,
    "write": _summarize_edit,
    "write_file": _summarize_edit,
    "patch": _summarize_edit,
    "report": _summarize_report,
}


# Seed on import so the first render before any refresh still works.
clear_tool_registry()


def _truncate_arg(val: str, key: str, max_len: int) -> str:
    """Truncate a tool argument for display, preserving the meaningful part."""
    short = val.strip().replace("\n", " ")
    if len(short) <= max_len:
        return short
    # For path-like args, keep the filename and truncate the middle
    if key in _PATH_ARGS or "/" in short:
        # Find the last path component
        last_sep = short.rfind("/")
        if last_sep > 0:
            tail = short[last_sep:]  # e.g. "/conversation.py"
            if len(tail) < max_len - 4:  # room for ".../" prefix
                head_budget = max_len - len(tail) - 3  # 3 for "..."
                return short[:head_budget] + "..." + tail
    # Default: truncate from the right
    return short[:max_len] + "..."


def _format_tool_label(name: str, args: dict[str, t.Any], max_arg_len: int = 60) -> str:
    """Format tool name with its key argument: ``read(pyproject.toml)``."""
    if name.lower() == "report":
        label = _report_label_from_args(args)
        if label:
            return f"{name}({_truncate_arg(label, 'title', max_arg_len)})"
        return name

    if name.lower() == "ask_user":
        label = _ask_user_label_from_args(args)
        if label:
            return f"{name}({_truncate_arg(label, 'prompt', max_arg_len)})"
        return name

    key_names = _TOOL_KEY_ARGS.get(name.lower(), [])
    for key in key_names:
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            return f"{name}({_truncate_arg(val, key, max_arg_len)})"
        if isinstance(val, list):
            values = [item.strip() for item in val if isinstance(item, str) and item.strip()]
            if values:
                first = _truncate_arg(values[0], key, max_arg_len)
                if len(values) == 1:
                    return f"{name}({first})"
                return f"{name}({first}, +{len(values) - 1})"
    # Fallback: show first string arg if short enough
    for val in args.values():
        if isinstance(val, str) and val.strip() and len(val) < 40:
            short = val.strip().replace("\n", " ")
            return f"{name}({short})"
    return name


def _summarize_tool_result(name: str, args: dict[str, t.Any], result: t.Any) -> str | None:
    """Return a compact one-line summary of a tool result.

    Routes through the registered summarizer for ``name`` (if any),
    otherwise falls back to the generic first-line summary. Always
    honors the shared "output truncated/saved" markers before dispatch.
    """
    if result is None:
        return None

    text = _get_result_text(result)
    if not text.strip():
        return None

    offload_match = re.search(
        r"\.\.\. \[(?P<lines>\d+) lines truncated — full output saved to (?P<path>[^\]]+)\] \.\.\.",
        text,
    )
    if offload_match:
        lines = offload_match.group("lines")
        path = offload_match.group("path")
        return f"Output truncated ({lines} lines). Saved to {path}."

    if "full output saved to" in text:
        path_match = re.search(r"full output saved to (?P<path>[^\s\]]+)", text)
        if path_match:
            return f"Output saved to {path_match.group('path')}."

    summarizer = _TOOL_SUMMARIZERS.get(name.lower())
    if summarizer is not None:
        return summarizer(name, args, result)

    return _first_line(text) or None
