"""Provider-payload pretty-printers for human inspection during debug.

This module is read-only with respect to the provider request payloads — it
NEVER mutates ``config_data``. It produces a single human-readable string per
provider that shows:

  * the system prompt (verbatim, fully expanded),
  * every message and every part inside it (role + part-type + content),
  * every tool / function declaration with its name, description, and the
    raw parameters object exactly as the provider receives it.

Why a separate module
---------------------
``vcprint`` already pretty-prints the raw ``config_data`` dict via Rich, but
that view is optimised for showing JSON structure, not for reading a long
system prompt or seeing how a multi-part user message was assembled. This
module gives that secondary, human-eye-friendly view without touching the
existing capture path or the per-provider translators.

Wiring (later, after review)
----------------------------
The intended wiring — once the output is approved — is one of:

  1. A conditional call from ``capture_request_payload`` (single hook for all
     providers), gated on ``ctx.debug``.
  2. A ``pretty_print`` method on each translator that delegates here.

Neither is wired up yet. Importing this module has zero side effects.

Provider shapes handled
-----------------------
* OpenAI (Responses API): the dict returned by ``OpenAITranslator.to_openai``.
  Top-level ``input`` items can be role-bearing messages OR flat items
  (``function_call``, ``function_call_output``, ``reasoning``,
  ``web_search_call``, ``message``).
* Anthropic (Messages API): the dict returned by
  ``AnthropicTranslator.to_anthropic``. ``system`` is a string (or a list of
  system blocks); ``messages`` carry user/assistant turns with typed content
  blocks (``text`` / ``image`` / ``document`` / ``tool_use`` / ``tool_result``
  / ``thinking`` / ``redacted_thinking``).
* Google (Gemini): the ``GoogleProviderConfig`` TypedDict returned by
  ``GoogleTranslator.to_google``. ``contents`` is a list of ``types.Content``
  Pydantic objects; ``config`` is a ``types.GenerateContentConfig`` Pydantic
  object that carries the system instruction, generation parameters, tools
  (wrapped in ``types.Tool(function_declarations=[…])``), and thinking
  config. We resolve everything via ``model_dump`` so the formatter only
  ever walks plain dicts.
* OpenAI Chat-Completions style (xAI / Groq / Cerebras / Together /
  generic-openai a.k.a. HuggingFace / vLLM / llama.cpp / Ollama): one
  shared ``format_openai_chat_payload`` covers all five — they all emit
  ``{"model", "messages": [...], "tools": [{"type": "function",
  "function": {...}}], "temperature", ...}`` with system as a ``role:
  system`` entry.

Providers WITHOUT a dedicated formatter
---------------------------------------
The following request paths do not go through ``capture_request_payload``
at all — they bypass the snapshot system because their request payload
isn't an LLM message-array shape:

  * OpenAI TTS         (``wire_format="openai_tts"``, audio.speech.create)
  * Google video gen   (``GoogleVideoGeneration``, generate_videos)
  * ElevenLabs TTS     (text_to_dialogue.convert)

If anything ever DOES route those payloads into this dispatcher, it will
emit a loud ``UNSUPPORTED`` banner instead of silently falling back to a
JSON dump. See ``_KNOWN_UNSUPPORTED`` below.
"""

from __future__ import annotations

import dataclasses
import json
from typing import Any

# ----------------------------------------------------------------------------
# Layout constants
# ----------------------------------------------------------------------------
_LINE_WIDTH = 100
_HEAVY = "=" * _LINE_WIDTH
_LIGHT = "-" * _LINE_WIDTH

# Strings longer than this — and not user-authored prose-like text — are
# replaced with a head + length marker. Tool ``parameters`` are NEVER
# touched by this rule (the user explicitly wants to see them verbatim);
# this only affects opaque blobs like ``encrypted_content`` or inline base64
# document data we surface in the message dump.
_OPAQUE_BLOB_THRESHOLD = 400


# ----------------------------------------------------------------------------
# Conversion helpers
# ----------------------------------------------------------------------------
def _to_jsonable(obj: Any) -> Any:
    """Convert provider-specific objects to plain JSON-safe Python values.

    Handles, in order:
      * ``None`` / scalars — returned as-is.
      * Pydantic v2 models (``model_dump``) — preferred for google-genai
        ``Content`` / ``GenerateContentConfig`` / ``Part`` / ``Tool``.
      * Dataclasses — ``dataclasses.asdict``.
      * dict / list / tuple — recurse.
      * Anything else — ``str(obj)`` so the output is never crashy.

    NEVER mutates the input; returns fresh containers.
    """
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    # Pydantic v2 first (covers google-genai types).
    model_dump = getattr(obj, "model_dump", None)
    if callable(model_dump):
        try:
            return model_dump(exclude_none=True)
        except Exception:
            pass
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        try:
            return dataclasses.asdict(obj)
        except Exception:
            pass
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(item) for item in obj]
    return str(obj)


def _strip_none(value: Any) -> Any:
    """Remove ``None`` leaves AND empty containers from a JSON-safe tree.

    Use this for parts/contents that won't carry semantic empty-dict
    markers. For places where an empty dict means something (e.g. Google's
    ``{"google_search": {}}`` built-in tool), use ``_drop_none_leaves``.
    """
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k, v in value.items():
            cleaned = _strip_none(v)
            if cleaned is None:
                continue
            if isinstance(cleaned, (dict, list)) and not cleaned:
                continue
            out[k] = cleaned
        return out
    if isinstance(value, list):
        return [_strip_none(item) for item in value]
    return value


def _drop_none_leaves(value: Any) -> Any:
    """Like ``_strip_none`` but preserves empty dicts and lists.

    Used for Google's ``GenerateContentConfig`` because its built-in tools
    are signalled by empty dicts (``{"google_search": {}}``). Removing
    those would silently lose the fact that grounding/search/code-exec is
    enabled — exactly the kind of "nothing is left out" failure the user
    is trying to avoid.
    """
    if isinstance(value, dict):
        return {k: _drop_none_leaves(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_drop_none_leaves(item) for item in value]
    return value


def _indent(text: str, prefix: str) -> str:
    """Prefix every line of ``text`` with ``prefix``. Empty input → empty."""
    if not text:
        return ""
    return "\n".join(prefix + line for line in str(text).splitlines())


def _abbreviate_opaque(value: str, *, label: str = "blob") -> str:
    """Shorten an opaque blob (encrypted reasoning, base64 image, etc.).

    Keeps the first 80 and last 40 characters verbatim with an inline
    ``<… N chars truncated …>`` marker between them. NOT applied to tool
    parameters or to user prose — only to fields that are known to be
    machine-only opaque payloads.
    """
    if len(value) <= _OPAQUE_BLOB_THRESHOLD:
        return value
    head, tail = value[:80], value[-40:]
    truncated = len(value) - len(head) - len(tail)
    return f"{head} <… {truncated} {label} chars truncated …> {tail}"


def _format_params(params: Any, indent: str = "      ") -> str:
    """Render a tool parameters / input_schema object as indented JSON.

    The user explicitly wants this verbatim, so no truncation, no key
    reordering. ``default=str`` handles any oddball value the provider
    accepted (functions, classes) without raising.
    """
    safe = _to_jsonable(params)
    body = json.dumps(safe, indent=2, ensure_ascii=False, default=str, sort_keys=False)
    return _indent(body, indent)


# ----------------------------------------------------------------------------
# Section / header helpers
# ----------------------------------------------------------------------------
def _heavy_header(title: str, subtitle: str | None = None) -> list[str]:
    lines = ["", _HEAVY, f"  {title}"]
    if subtitle:
        lines.append(f"  {subtitle}")
    lines.append(_HEAVY)
    return lines


def _section(title: str) -> list[str]:
    """Light section divider — e.g. ``──── SYSTEM ──────────…``"""
    label = f" {title} "
    pad = max(4, _LINE_WIDTH - len(label))
    left = 4
    right = pad - left
    return ["", "─" * left + label + "─" * right]


# ----------------------------------------------------------------------------
# OpenAI (Responses API)
# ----------------------------------------------------------------------------
def format_openai_payload(
    config_data: dict[str, Any],
    *,
    wire_format: str | None = None,
) -> str:
    """Render an OpenAI Responses-API request dict as a debug-friendly string.

    Recognized top-level shape (anything else is shown via JSON fallback):

        {
            "model": str,
            "input": [
                {"role": "user|developer|assistant|system", "content": [parts]},
                {"type": "message", "role": "...", "id": "...", "content": [parts]},
                {"type": "function_call", "call_id": ..., "name": ..., "arguments": "..."},
                {"type": "function_call_output", "call_id": ..., "output": "..."},
                {"type": "reasoning", "id": ..., "summary": ..., "encrypted_content": "..."},
                {"type": "web_search_call", "id": ..., "status": ..., "action": ...},
                ...
            ],
            "tools": [{"type": "function", "name", "description", "parameters"}, ...],
            "max_output_tokens": ..., "temperature": ..., "top_p": ..., ...
        }
    """
    cfg = config_data if isinstance(config_data, dict) else _to_jsonable(config_data)
    if not isinstance(cfg, dict):
        return _fallback_dump("openai", cfg)

    model = cfg.get("model", "?")
    out: list[str] = []
    out.extend(_heavy_header(
        title=f"PROVIDER: openai (wire_format={wire_format or 'n/a'})",
        subtitle=f"MODEL:    {model}",
    ))

    input_items = cfg.get("input") or []
    # ------------------------------------------------------------------
    # Pull the developer/system message(s) out so they get their own
    # SYSTEM section (matches user expectation that "system prompt" shows
    # at the top, regardless of OpenAI's role naming).
    # ------------------------------------------------------------------
    system_items: list[dict[str, Any]] = []
    other_items: list[Any] = []
    for item in input_items:
        if isinstance(item, dict) and item.get("role") in ("developer", "system"):
            system_items.append(item)
        else:
            other_items.append(item)

    if system_items:
        out.extend(_section("SYSTEM (developer)"))
        for sys_item in system_items:
            for line in _openai_render_content(sys_item.get("content", [])):
                out.append(line)

    out.extend(_section(f"MESSAGES ({len(other_items)})"))
    if not other_items:
        out.append("  (no messages)")
    for idx, item in enumerate(other_items, start=1):
        out.extend(_openai_render_input_item(item, idx))

    tools = cfg.get("tools") or []
    out.extend(_section(f"TOOLS ({len(tools)})"))
    if not tools:
        out.append("  (no tools)")
    for idx, tool in enumerate(tools, start=1):
        out.extend(_openai_render_tool(tool, idx))

    # Anything left we haven't already shown — model parameters, response
    # format, tool_choice, include items, store flag, reasoning config, etc.
    consumed = {"model", "input", "tools"}
    extras = {k: v for k, v in cfg.items() if k not in consumed and v is not None}
    if extras:
        out.extend(_section("OTHER PARAMETERS"))
        for k, v in extras.items():
            out.append(f"  {k}: {_short_value(v)}")

    out.append(_HEAVY)
    return "\n".join(out)


def _openai_render_input_item(item: Any, idx: int) -> list[str]:
    """Render one OpenAI Responses-API top-level input item."""
    if not isinstance(item, dict):
        return [f"  [{idx}] {item!r}"]

    item_type = item.get("type")
    role = item.get("role")

    if item_type == "function_call":
        return [
            f"  [{idx}] type=function_call",
            f"      name:      {item.get('name')}",
            f"      call_id:   {item.get('call_id')}",
            f"      id:        {item.get('id')}",
            f"      status:    {item.get('status', '—')}",
            "      arguments:",
            _indent(_pretty_maybe_json(item.get("arguments")), "        "),
        ]

    if item_type == "function_call_output":
        return [
            f"  [{idx}] type=function_call_output",
            f"      call_id:   {item.get('call_id')}",
            "      output:",
            _indent(_pretty_maybe_json(item.get("output")), "        "),
        ]

    if item_type == "reasoning":
        summary = item.get("summary")
        encrypted = item.get("encrypted_content") or ""
        lines = [
            f"  [{idx}] type=reasoning",
            f"      id:                 {item.get('id')}",
            f"      summary:            {_short_value(summary)}",
        ]
        if encrypted:
            lines.append(
                f"      encrypted_content:  {_abbreviate_opaque(str(encrypted), label='encrypted')}"
            )
        return lines

    if item_type == "web_search_call":
        lines = [
            f"  [{idx}] type=web_search_call",
            f"      id:      {item.get('id')}",
            f"      status:  {item.get('status')}",
        ]
        action = item.get("action")
        if action:
            lines.append("      action:")
            lines.append(_indent(_pretty_json(action), "        "))
        return lines

    if item_type == "message" or role:
        # Both shapes go through the same renderer — the explicit
        # ``{"type": "message", ...}`` wrapper and the chat-style
        # ``{"role": ..., "content": [...]}`` carry the same data here.
        message_id = item.get("id")
        header = f"  [{idx}] role={role or '?'}"
        if message_id:
            header += f"  id={message_id}"
        if item_type:
            header += f"  type={item_type}"
        lines = [header, "      parts:"]
        lines.extend(_openai_render_content(item.get("content", []), part_indent="      "))
        return lines

    # Unknown item shape — dump as JSON so nothing is silently lost.
    return [f"  [{idx}] (unknown item shape)", _indent(_pretty_json(item), "      ")]


def _openai_render_content(
    content: Any,
    *,
    part_indent: str = "",
) -> list[str]:
    """Render an OpenAI ``content`` field (list of typed parts, or a string)."""
    if isinstance(content, str):
        return [_indent(content, part_indent + "  ")]
    if not isinstance(content, list):
        return [_indent(_pretty_json(content), part_indent + "  ")]

    out: list[str] = []
    for pidx, part in enumerate(content):
        if not isinstance(part, dict):
            out.append(f"{part_indent}  [{pidx}] {part!r}")
            continue
        ptype = part.get("type", "?")
        if ptype in ("input_text", "output_text"):
            text = part.get("text", "")
            out.append(f"{part_indent}  [{pidx}] type={ptype}")
            out.append(_indent(text, part_indent + "      "))
        elif ptype == "refusal":
            out.append(f"{part_indent}  [{pidx}] type=refusal")
            out.append(_indent(part.get("refusal", ""), part_indent + "      "))
        elif ptype == "input_image":
            out.append(f"{part_indent}  [{pidx}] type=input_image")
            url = part.get("image_url")
            if url:
                # If image_url is a data URL, show only its prefix.
                shown = _abbreviate_opaque(str(url), label="image_url") if isinstance(url, str) else _pretty_json(url)
                out.append(_indent(f"image_url: {shown}", part_indent + "      "))
            file_id = part.get("file_id")
            if file_id:
                out.append(_indent(f"file_id:   {file_id}", part_indent + "      "))
        elif ptype == "input_file":
            out.append(f"{part_indent}  [{pidx}] type=input_file")
            for k in ("file_id", "filename", "file_data"):
                v = part.get(k)
                if v is None:
                    continue
                shown = _abbreviate_opaque(str(v), label=k) if k == "file_data" else v
                out.append(_indent(f"{k}: {shown}", part_indent + "      "))
        else:
            out.append(f"{part_indent}  [{pidx}] type={ptype}")
            out.append(_indent(_pretty_json(part), part_indent + "      "))
    return out


def _openai_render_tool(tool: Any, idx: int) -> list[str]:
    """Render one OpenAI Responses-API tool entry."""
    if not isinstance(tool, dict):
        return [f"  [{idx}] {tool!r}"]
    ttype = tool.get("type", "function")

    if ttype == "function":
        # OpenAI Responses-API flat shape: name/description/parameters at the
        # top level. (The Chat-Completions shape nests under ``"function"`` —
        # we accept both for resilience.)
        if "function" in tool and isinstance(tool["function"], dict):
            inner = tool["function"]
            name = inner.get("name", "?")
            description = inner.get("description", "")
            parameters = inner.get("parameters", {})
        else:
            name = tool.get("name", "?")
            description = tool.get("description", "")
            parameters = tool.get("parameters", {})
        return [
            f"  [{idx}] type=function",
            f"      name:        {name}",
            "      description:",
            _indent(description or "(none)", "        "),
            "      parameters:",
            _format_params(parameters),
        ]

    # Built-in tool types: web_search, file_search, code_interpreter, etc.
    return [
        f"  [{idx}] type={ttype}",
        _indent(_pretty_json({k: v for k, v in tool.items() if k != "type"}), "      "),
    ]


# ----------------------------------------------------------------------------
# OpenAI Chat-Completions style (xAI / Groq / Cerebras / Together / Generic)
# ----------------------------------------------------------------------------
def format_openai_chat_payload(
    config_data: dict[str, Any],
    *,
    wire_format: str | None = None,
    provider_label: str = "openai-compatible",
) -> str:
    """Render an OpenAI Chat-Completions request dict as a debug-friendly string.

    Recognized top-level shape (the dict produced by
    ``XAITranslator.to_xai`` / ``GroqTranslator.to_groq`` /
    ``CerebrasTranslator.to_cerebras`` / ``TogetherTranslator.to_together``
    / ``GenericOpenAITranslator.to_generic_openai``):

        {
            "model": str,
            "messages": [
                {"role": "system",    "content": str},
                {"role": "user",      "content": str | list[parts]},
                {"role": "assistant", "content": str | None,
                 "tool_calls": [{"id", "type": "function",
                                 "function": {"name", "arguments": str}}]},
                {"role": "tool", "tool_call_id": str, "content": str},
            ],
            "tools": [{"type": "function",
                       "function": {"name", "description", "parameters"}}],
            "tool_choice": ..., "temperature", "top_p", "max_tokens" |
            "max_completion_tokens", "stop", "stream", "response_format", ...
        }

    The system prompt for this style is the ``role: system`` entry inside
    ``messages``, not a separate field — we pull it out so the rendered
    output looks symmetric with the other providers.

    Some endpoints accept multimodal content as a list of typed parts
    (``{"type": "text", "text": ...}`` / ``{"type": "image_url",
    "image_url": {...}}``); the renderer handles that shape too.
    """
    cfg = config_data if isinstance(config_data, dict) else _to_jsonable(config_data)
    if not isinstance(cfg, dict):
        return _fallback_dump(provider_label, cfg)

    model = cfg.get("model", "?")
    out: list[str] = []
    out.extend(_heavy_header(
        title=f"PROVIDER: {provider_label} (Chat-Completions, wire_format={wire_format or 'n/a'})",
        subtitle=f"MODEL:    {model}",
    ))

    messages = cfg.get("messages") or []
    # Pull system messages out so they get their own SYSTEM section, matching
    # the other providers' layouts. We preserve order otherwise.
    system_msgs: list[dict[str, Any]] = []
    other_msgs: list[Any] = []
    for m in messages:
        if isinstance(m, dict) and m.get("role") == "system":
            system_msgs.append(m)
        else:
            other_msgs.append(m)

    out.extend(_section("SYSTEM"))
    if not system_msgs:
        out.append("  (none)")
    else:
        for sidx, m in enumerate(system_msgs):
            content = m.get("content")
            if len(system_msgs) > 1:
                out.append(f"  [system #{sidx}]")
            if isinstance(content, str):
                out.append(_indent(content, "  " if len(system_msgs) == 1 else "      "))
            else:
                out.append(_indent(_pretty_json(content), "      "))

    out.extend(_section(f"MESSAGES ({len(other_msgs)})"))
    if not other_msgs:
        out.append("  (no messages)")
    for idx, msg in enumerate(other_msgs, start=1):
        out.extend(_openai_chat_render_message(msg, idx))

    tools = cfg.get("tools") or []
    out.extend(_section(f"TOOLS ({len(tools)})"))
    if not tools:
        out.append("  (no tools)")
    for idx, tool in enumerate(tools, start=1):
        out.extend(_openai_chat_render_tool(tool, idx))

    consumed = {"model", "messages", "tools"}
    extras = {k: v for k, v in cfg.items() if k not in consumed and v is not None}
    if extras:
        out.extend(_section("OTHER PARAMETERS"))
        for k, v in extras.items():
            if isinstance(v, (dict, list)):
                out.append(f"  {k}:")
                out.append(_indent(_pretty_json(v), "    "))
            else:
                out.append(f"  {k}: {_short_value(v)}")

    out.append(_HEAVY)
    return "\n".join(out)


def _openai_chat_render_message(msg: Any, idx: int) -> list[str]:
    if not isinstance(msg, dict):
        return [f"  [{idx}] {msg!r}"]

    role = msg.get("role", "?")
    lines = [f"  [{idx}] role={role}"]

    if role == "tool":
        # Tool result message — one ``tool_call_id`` and a string content.
        lines.append(f"      tool_call_id: {msg.get('tool_call_id')}")
        content = msg.get("content")
        lines.append("      content:")
        lines.append(_indent(_pretty_maybe_json(content), "        "))
        return lines

    content = msg.get("content")
    if content is None:
        lines.append("      content: (null)")
    elif isinstance(content, str):
        lines.append("      content:")
        lines.append(_indent(content, "        "))
    elif isinstance(content, list):
        # Multimodal content — list of parts.
        lines.append("      content:")
        for pidx, part in enumerate(content):
            lines.extend(_openai_chat_render_content_part(part, pidx))
    else:
        lines.append("      content:")
        lines.append(_indent(_pretty_json(content), "        "))

    tool_calls = msg.get("tool_calls") or []
    if tool_calls:
        lines.append(f"      tool_calls ({len(tool_calls)}):")
        for tcidx, tc in enumerate(tool_calls):
            lines.extend(_openai_chat_render_tool_call(tc, tcidx))
    return lines


def _openai_chat_render_content_part(part: Any, pidx: int) -> list[str]:
    indent_part = "        "
    indent_body = "            "
    if not isinstance(part, dict):
        return [f"{indent_part}[{pidx}] {part!r}"]

    ptype = part.get("type", "?")
    if ptype == "text":
        return [
            f"{indent_part}[{pidx}] type=text",
            _indent(part.get("text", ""), indent_body),
        ]

    if ptype == "image_url":
        image_url = part.get("image_url")
        if isinstance(image_url, dict):
            url = image_url.get("url", "")
            detail = image_url.get("detail")
            lines = [
                f"{indent_part}[{pidx}] type=image_url",
                f"{indent_body}url:    {_abbreviate_opaque(str(url), label='image_url')}",
            ]
            if detail:
                lines.append(f"{indent_body}detail: {detail}")
            return lines
        return [
            f"{indent_part}[{pidx}] type=image_url",
            f"{indent_body}image_url: {_abbreviate_opaque(str(image_url), label='image_url')}",
        ]

    if ptype in ("input_audio", "audio"):
        audio = part.get(ptype) or {}
        if isinstance(audio, dict):
            data = str(audio.get("data") or "")
            return [
                f"{indent_part}[{pidx}] type={ptype}",
                f"{indent_body}format: {audio.get('format', '?')}",
                f"{indent_body}data:   {_abbreviate_opaque(data, label='audio_b64')}",
            ]

    return [
        f"{indent_part}[{pidx}] type={ptype}",
        _indent(_pretty_json(part), indent_body),
    ]


def _openai_chat_render_tool_call(tc: Any, tcidx: int) -> list[str]:
    indent_tc = "        "
    indent_body = "          "
    if not isinstance(tc, dict):
        return [f"{indent_tc}[{tcidx}] {tc!r}"]
    fn = tc.get("function") or {}
    name = fn.get("name", "?")
    args = fn.get("arguments", "")
    return [
        f"{indent_tc}[{tcidx}] id={tc.get('id')}  type={tc.get('type', 'function')}",
        f"{indent_body}name: {name}",
        f"{indent_body}arguments:",
        _indent(_pretty_maybe_json(args), indent_body + "  "),
    ]


def _openai_chat_render_tool(tool: Any, idx: int) -> list[str]:
    """Render one Chat-Completions tool: ``{"type": "function", "function": {...}}``"""
    if not isinstance(tool, dict):
        return [f"  [{idx}] {tool!r}"]

    ttype = tool.get("type", "function")
    if ttype == "function":
        # Chat-Completions wraps under ``"function"``; some servers also accept
        # the flat shape — handle both.
        if isinstance(tool.get("function"), dict):
            inner = tool["function"]
        else:
            inner = tool
        name = inner.get("name", "?")
        description = inner.get("description", "")
        parameters = inner.get("parameters", {})
        return [
            f"  [{idx}] type=function",
            f"      name:        {name}",
            "      description:",
            _indent(description or "(none)", "        "),
            "      parameters:",
            _format_params(parameters),
        ]

    return [
        f"  [{idx}] type={ttype}",
        _indent(_pretty_json({k: v for k, v in tool.items() if k != "type"}), "      "),
    ]


# ----------------------------------------------------------------------------
# Anthropic (Messages API)
# ----------------------------------------------------------------------------
def format_anthropic_payload(
    config_data: dict[str, Any],
    *,
    wire_format: str | None = None,
) -> str:
    """Render an Anthropic Messages-API request dict as a debug-friendly string.

    Recognized top-level shape:

        {
            "model": str,
            "system": str | list[{"type": "text", "text": "..."}],
            "messages": [
                {"role": "user|assistant", "content": [block, ...]},
                ...
            ],
            "tools": [{"name", "description", "input_schema"}, ...],
            "tool_choice": ..., "thinking": ..., "max_tokens": ..., ...
        }

    Recognized content-block ``type`` values: ``text``, ``image``, ``document``,
    ``tool_use``, ``tool_result``, ``thinking``, ``redacted_thinking``,
    ``server_tool_use``, ``web_search_tool_result``.
    """
    cfg = config_data if isinstance(config_data, dict) else _to_jsonable(config_data)
    if not isinstance(cfg, dict):
        return _fallback_dump("anthropic", cfg)

    model = cfg.get("model", "?")
    out: list[str] = []
    out.extend(_heavy_header(
        title=f"PROVIDER: anthropic (wire_format={wire_format or 'n/a'})",
        subtitle=f"MODEL:    {model}",
    ))

    out.extend(_section("SYSTEM"))
    system = cfg.get("system")
    if not system:
        out.append("  (none)")
    elif isinstance(system, str):
        out.append(_indent(system, "  "))
    elif isinstance(system, list):
        # Anthropic also accepts a list of system blocks (text + cache_control).
        for sidx, block in enumerate(system):
            if isinstance(block, dict) and block.get("type") == "text":
                out.append(f"  [system block #{sidx}]")
                out.append(_indent(block.get("text", ""), "      "))
                cc = block.get("cache_control")
                if cc:
                    out.append(f"      cache_control: {_short_value(cc)}")
            else:
                out.append(_indent(_pretty_json(block), "  "))
    else:
        out.append(_indent(_pretty_json(system), "  "))

    messages = cfg.get("messages") or []
    out.extend(_section(f"MESSAGES ({len(messages)})"))
    if not messages:
        out.append("  (no messages)")
    for idx, msg in enumerate(messages, start=1):
        out.extend(_anthropic_render_message(msg, idx))

    tools = cfg.get("tools") or []
    out.extend(_section(f"TOOLS ({len(tools)})"))
    if not tools:
        out.append("  (no tools)")
    for idx, tool in enumerate(tools, start=1):
        out.extend(_anthropic_render_tool(tool, idx))

    consumed = {"model", "system", "messages", "tools"}
    extras = {k: v for k, v in cfg.items() if k not in consumed and v is not None}
    if extras:
        out.extend(_section("OTHER PARAMETERS"))
        for k, v in extras.items():
            out.append(f"  {k}: {_short_value(v)}")

    out.append(_HEAVY)
    return "\n".join(out)


def _anthropic_render_message(msg: Any, idx: int) -> list[str]:
    if not isinstance(msg, dict):
        return [f"  [{idx}] {msg!r}"]

    role = msg.get("role", "?")
    content = msg.get("content", [])
    lines = [f"  [{idx}] role={role}"]

    if isinstance(content, str):
        lines.append("      content (string):")
        lines.append(_indent(content, "        "))
        return lines

    if not isinstance(content, list):
        lines.append(_indent(_pretty_json(content), "      "))
        return lines

    lines.append("      content:")
    for bidx, block in enumerate(content):
        lines.extend(_anthropic_render_block(block, bidx))
    return lines


def _anthropic_render_block(block: Any, bidx: int) -> list[str]:
    indent_part = "        "
    indent_body = "            "
    if not isinstance(block, dict):
        return [f"{indent_part}[{bidx}] {block!r}"]

    btype = block.get("type", "?")
    head = f"{indent_part}[{bidx}] type={btype}"

    if btype == "text":
        return [head, _indent(block.get("text", ""), indent_body)]

    if btype == "thinking":
        thinking_text = block.get("thinking", "")
        sig = block.get("signature")
        lines = [head, _indent(thinking_text, indent_body)]
        if sig:
            lines.append(
                f"{indent_body}signature: {_abbreviate_opaque(str(sig), label='signature')}"
            )
        return lines

    if btype == "redacted_thinking":
        data = block.get("data", "")
        return [
            head,
            f"{indent_body}data: {_abbreviate_opaque(str(data), label='redacted')}",
        ]

    if btype == "tool_use":
        return [
            head,
            f"{indent_body}name:  {block.get('name')}",
            f"{indent_body}id:    {block.get('id')}",
            f"{indent_body}input:",
            _format_params(block.get("input", {}), indent=indent_body + "  "),
        ]

    if btype == "tool_result":
        lines = [
            head,
            f"{indent_body}tool_use_id: {block.get('tool_use_id')}",
            f"{indent_body}is_error:    {block.get('is_error', False)}",
        ]
        inner = block.get("content")
        if isinstance(inner, str):
            lines.append(f"{indent_body}content (string):")
            lines.append(_indent(inner, indent_body + "  "))
        elif isinstance(inner, list):
            lines.append(f"{indent_body}content (blocks):")
            for nbidx, nested in enumerate(inner):
                lines.extend(_anthropic_render_block(nested, nbidx))
        elif inner is not None:
            lines.append(f"{indent_body}content:")
            lines.append(_indent(_pretty_json(inner), indent_body + "  "))
        return lines

    if btype == "image":
        source = block.get("source", {})
        return _media_block_lines(head, "image", source, indent_body)

    if btype == "document":
        source = block.get("source", {})
        return _media_block_lines(head, "document", source, indent_body)

    # Anthropic server tools etc. — fall through with a JSON dump so nothing
    # is silently lost.
    return [head, _indent(_pretty_json({k: v for k, v in block.items() if k != "type"}), indent_body)]


def _media_block_lines(
    head: str,
    kind: str,
    source: dict[str, Any],
    indent_body: str,
) -> list[str]:
    """Render an Anthropic ``image`` / ``document`` block compactly.

    Anthropic media blocks come in two flavours:
      * ``{"type": "base64", "media_type": "...", "data": "<base64>"}``
      * ``{"type": "url", "url": "..."}``
    Either way we never dump the raw base64 — we abbreviate it.
    """
    if not isinstance(source, dict):
        return [head, f"{indent_body}source: {source!r}"]

    src_type = source.get("type", "?")
    lines = [head, f"{indent_body}source.type:       {src_type}"]
    if "media_type" in source:
        lines.append(f"{indent_body}source.media_type: {source.get('media_type')}")
    if "url" in source:
        lines.append(f"{indent_body}source.url:        {source.get('url')}")
    if "data" in source:
        data = str(source.get("data") or "")
        lines.append(
            f"{indent_body}source.data:       {_abbreviate_opaque(data, label=f'{kind}_b64')}"
        )
    return lines


def _anthropic_render_tool(tool: Any, idx: int) -> list[str]:
    if not isinstance(tool, dict):
        return [f"  [{idx}] {tool!r}"]
    name = tool.get("name", "?")
    description = tool.get("description", "")
    schema = tool.get("input_schema", {})
    lines = [
        f"  [{idx}] name: {name}",
        "      description:",
        _indent(description or "(none)", "        "),
        "      input_schema:",
        _format_params(schema),
    ]
    # Anthropic computer-use / server-tools carry a ``type`` we should show.
    if "type" in tool:
        lines.insert(1, f"      type: {tool['type']}")
    return lines


# ----------------------------------------------------------------------------
# Google (Gemini)
# ----------------------------------------------------------------------------
def format_google_payload(
    config_data: Any,
    *,
    wire_format: str | None = None,
) -> str:
    """Render a Google Gemini request as a debug-friendly string.

    Accepts the ``GoogleProviderConfig`` TypedDict produced by
    ``GoogleTranslator.to_google``. ``contents`` is a list of
    ``types.Content`` Pydantic objects and ``config`` is a
    ``types.GenerateContentConfig`` Pydantic object — both are normalised
    to plain dicts via ``model_dump`` before rendering.
    """
    if not isinstance(config_data, dict):
        config_data = _to_jsonable(config_data)
    if not isinstance(config_data, dict):
        return _fallback_dump("google", config_data)

    model = config_data.get("model", "?")
    contents_raw = config_data.get("contents") or []
    config_raw = config_data.get("config")

    contents = [_strip_none(_to_jsonable(c)) for c in contents_raw]
    # We deliberately do NOT pass ``cfg`` through ``_strip_none`` because
    # google-genai uses empty-dict marker types to enable built-in tools
    # (``{"google_search": {}}``, ``{"url_context": {}}``, ``{"code_execution": {}}``).
    # Stripping empty containers would swallow the very signal we need to show.
    # We do strip None leaves so optional fields don't add noise.
    cfg = _to_jsonable(config_raw) if config_raw is not None else {}
    if isinstance(cfg, dict):
        cfg = _drop_none_leaves(cfg)

    out: list[str] = []
    out.extend(_heavy_header(
        title=f"PROVIDER: google (wire_format={wire_format or 'n/a'})",
        subtitle=f"MODEL:    {model}",
    ))

    # SYSTEM lives on config.system_instruction (string OR Content-shaped).
    out.extend(_section("SYSTEM"))
    sys_instr = cfg.get("system_instruction") if isinstance(cfg, dict) else None
    if not sys_instr:
        out.append("  (none)")
    elif isinstance(sys_instr, str):
        out.append(_indent(sys_instr, "  "))
    elif isinstance(sys_instr, dict):
        # Content-shaped: {"parts": [{"text": "..."}], "role": "user"}
        parts = sys_instr.get("parts", [])
        if isinstance(parts, list):
            for part in parts:
                if isinstance(part, dict) and "text" in part:
                    out.append(_indent(part.get("text", ""), "  "))
                else:
                    out.append(_indent(_pretty_json(part), "  "))
        else:
            out.append(_indent(_pretty_json(sys_instr), "  "))
    else:
        out.append(_indent(_pretty_json(sys_instr), "  "))

    out.extend(_section(f"MESSAGES ({len(contents)})"))
    if not contents:
        out.append("  (no messages)")
    for idx, content in enumerate(contents, start=1):
        out.extend(_google_render_content(content, idx))

    # Tools live on config.tools as a list of Tool wrappers; we want each
    # function_declaration as its own row.
    declarations: list[dict[str, Any]] = []
    raw_tools = cfg.get("tools") if isinstance(cfg, dict) else []
    raw_tools = raw_tools if isinstance(raw_tools, list) else []
    builtin_tools: list[dict[str, Any]] = []
    for tool_wrapper in raw_tools:
        if not isinstance(tool_wrapper, dict):
            builtin_tools.append({"raw": tool_wrapper})
            continue
        fdecls = tool_wrapper.get("function_declarations")
        if isinstance(fdecls, list) and fdecls:
            declarations.extend(d for d in fdecls if isinstance(d, dict))
        else:
            # Built-in google tools (google_search, url_context, code_execution, …).
            builtin_tools.append(tool_wrapper)

    out.extend(_section(f"TOOLS ({len(declarations)} function declarations, {len(builtin_tools)} built-in)"))
    if not declarations and not builtin_tools:
        out.append("  (no tools)")
    for idx, decl in enumerate(declarations, start=1):
        out.extend(_google_render_function_declaration(decl, idx))
    for idx, btool in enumerate(builtin_tools, start=1):
        out.extend(_google_render_builtin_tool(btool, idx))

    # Tool config (mode etc.).
    if isinstance(cfg, dict) and cfg.get("tool_config"):
        out.extend(_section("TOOL_CONFIG"))
        out.append(_indent(_pretty_json(cfg["tool_config"]), "  "))

    # Thinking config / generation parameters / response modalities / etc.
    consumed = {"system_instruction", "tools", "tool_config"}
    extras = {k: v for k, v in (cfg.items() if isinstance(cfg, dict) else []) if k not in consumed and v is not None}
    if extras:
        out.extend(_section("OTHER CONFIG"))
        for k, v in extras.items():
            if isinstance(v, (dict, list)):
                out.append(f"  {k}:")
                out.append(_indent(_pretty_json(v), "    "))
            else:
                out.append(f"  {k}: {_short_value(v)}")

    out.append(_HEAVY)
    return "\n".join(out)


def _google_render_content(content: Any, idx: int) -> list[str]:
    if not isinstance(content, dict):
        return [f"  [{idx}] {content!r}"]
    role = content.get("role", "?")
    parts = content.get("parts", [])
    lines = [f"  [{idx}] role={role}", "      parts:"]
    if not isinstance(parts, list):
        lines.append(_indent(_pretty_json(parts), "        "))
        return lines
    for pidx, part in enumerate(parts):
        lines.extend(_google_render_part(part, pidx))
    return lines


def _google_render_part(part: Any, pidx: int) -> list[str]:
    indent_part = "        "
    indent_body = "            "
    if not isinstance(part, dict):
        return [f"{indent_part}[{pidx}] {part!r}"]

    if part.get("text") is not None and not part.get("thought"):
        return [
            f"{indent_part}[{pidx}] type=text",
            _indent(part.get("text") or "", indent_body),
        ]

    if part.get("thought"):
        # ``thought`` can be either ``True`` (with ``text`` carrying the
        # thought) or carry its own thought_signature for OpenAI-style
        # encrypted reasoning passthrough.
        lines = [
            f"{indent_part}[{pidx}] type=thinking",
            _indent(part.get("text") or "", indent_body),
        ]
        sig = part.get("thought_signature")
        if sig:
            lines.append(
                f"{indent_body}thought_signature: {_abbreviate_opaque(str(sig), label='signature')}"
            )
        return lines

    fc = part.get("function_call")
    if fc:
        lines = [
            f"{indent_part}[{pidx}] type=function_call",
            f"{indent_body}name: {fc.get('name')}",
            f"{indent_body}id:   {fc.get('id', '—')}",
            f"{indent_body}args:",
            _format_params(fc.get("args", {}), indent=indent_body + "  "),
        ]
        return lines

    fr = part.get("function_response")
    if fr:
        lines = [
            f"{indent_part}[{pidx}] type=function_response",
            f"{indent_body}name: {fr.get('name')}",
            f"{indent_body}id:   {fr.get('id', '—')}",
            f"{indent_body}response:",
            _indent(_pretty_json(fr.get("response")), indent_body + "  "),
        ]
        return lines

    inline = part.get("inline_data")
    if inline:
        mime = inline.get("mime_type", "?")
        data = str(inline.get("data") or "")
        return [
            f"{indent_part}[{pidx}] type=inline_data",
            f"{indent_body}mime_type: {mime}",
            f"{indent_body}data:      {_abbreviate_opaque(data, label='inline_b64')}",
        ]

    fd = part.get("file_data")
    if fd:
        return [
            f"{indent_part}[{pidx}] type=file_data",
            f"{indent_body}mime_type: {fd.get('mime_type', '?')}",
            f"{indent_body}file_uri:  {fd.get('file_uri', '?')}",
        ]

    if part.get("executable_code"):
        ec = part["executable_code"]
        return [
            f"{indent_part}[{pidx}] type=executable_code",
            f"{indent_body}language: {ec.get('language', '?')}",
            f"{indent_body}code:",
            _indent(ec.get("code", ""), indent_body + "  "),
        ]

    if part.get("code_execution_result"):
        cer = part["code_execution_result"]
        return [
            f"{indent_part}[{pidx}] type=code_execution_result",
            f"{indent_body}outcome: {cer.get('outcome', '?')}",
            f"{indent_body}output:",
            _indent(cer.get("output", ""), indent_body + "  "),
        ]

    # Unknown — show keys we kept after _strip_none.
    return [
        f"{indent_part}[{pidx}] (unknown part shape)",
        _indent(_pretty_json(part), indent_body),
    ]


def _google_render_function_declaration(decl: dict[str, Any], idx: int) -> list[str]:
    name = decl.get("name", "?")
    description = decl.get("description", "")
    # google-genai accepts BOTH "parameters" (legacy) and
    # "parameters_json_schema" (typed schema). Show whichever is set.
    params = decl.get("parameters") or decl.get("parameters_json_schema") or {}
    return [
        f"  [{idx}] name: {name}",
        "      description:",
        _indent(description or "(none)", "        "),
        "      parameters:",
        _format_params(params),
    ]


def _google_render_builtin_tool(tool: dict[str, Any], idx: int) -> list[str]:
    # Strip the function_declarations key (already rendered separately, if any)
    # and show whatever's left — typically google_search / url_context /
    # code_execution / google_maps wrappers.
    body = {k: v for k, v in tool.items() if k != "function_declarations"}
    return [
        f"  [builtin {idx}]",
        _indent(_pretty_json(body), "      "),
    ]


# ----------------------------------------------------------------------------
# Dispatcher
# ----------------------------------------------------------------------------
# Mapping from canonical provider name → formatter function. The provider
# name is the same string each provider's ``execute()`` already passes to
# ``stamp_call_meta(provider=…)``, so wiring this up adds zero new
# vocabulary. Both ``generic_openai`` and ``huggingface`` route through the
# Chat-Completions formatter (HuggingFaceChat is a thin GenericOpenAIChat
# subclass).
_FORMATTERS: dict[str, Any] = {
    "openai": format_openai_payload,
    "anthropic": format_anthropic_payload,
    "google": format_google_payload,
    "xai": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="xai"
    ),
    "groq": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="groq"
    ),
    "cerebras": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="cerebras"
    ),
    "together": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="together"
    ),
    "generic_openai": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="generic_openai"
    ),
    "huggingface": lambda cfg, *, wire_format=None: format_openai_chat_payload(
        cfg, wire_format=wire_format, provider_label="huggingface"
    ),
}


# Provider/wire_format combinations that are KNOWN not to flow through this
# debugger today. They bypass ``capture_request_payload`` entirely because
# their request payload isn't an LLM message-array shape (audio bytes,
# video config, etc.). If anything ever DOES route them here, we want a
# loud, explicit, greppable banner — not a silent JSON fallback.
#
# Format: ``(provider, wire_format) → human-readable reason``. ``wire_format``
# of ``None`` means "any wire_format for this provider that isn't in the
# regular formatter map".
_KNOWN_UNSUPPORTED: dict[tuple[str, str | None], str] = {
    ("openai", "openai_tts"):
        "OpenAI TTS uses audio.speech.create(), bypasses capture_request_payload.",
    ("google", "google_video"):
        "Google video generation uses generate_videos() with GenerateVideosConfig + "
        "GenerateVideosSource — not the GenerateContentConfig shape this module renders.",
    ("elevenlabs", None):
        "ElevenLabs TTS uses text_to_dialogue.convert() and never builds a "
        "matrx-ai-style request dict.",
}


def format_provider_payload(
    provider: str,
    config_data: Any,
    *,
    wire_format: str | None = None,
) -> str:
    """Pick the right per-provider formatter and return its output string.

    Resolution order:
      1. (provider, wire_format) is in ``_KNOWN_UNSUPPORTED`` → big warning
         banner explaining why this debugger can't render it.
      2. (provider, None) is in ``_KNOWN_UNSUPPORTED`` → same banner.
      3. provider has a registered formatter → dispatch to it.
      4. Unknown provider → ``_fallback_dump`` JSON-prints the payload AND
         emits a "no dedicated formatter" warning so it's never silent.

    Returning a string keeps the call site simple — the caller can pass it
    straight to ``vcprint`` or any other sink.
    """
    key = provider.lower()
    reason = _KNOWN_UNSUPPORTED.get((key, wire_format)) or _KNOWN_UNSUPPORTED.get((key, None))
    if reason is not None:
        return _unsupported_banner(provider, wire_format, reason, config_data)

    fn = _FORMATTERS.get(key)
    if fn is None:
        return _fallback_dump(provider, config_data, wire_format=wire_format)
    return fn(config_data, wire_format=wire_format)


def _unsupported_banner(
    provider: str,
    wire_format: str | None,
    reason: str,
    config_data: Any,
) -> str:
    """Big, loud banner for known-unsupported provider/wire_format combos.

    The banner is greppable (``[DEBUG_PRETTY_PRINT] UNSUPPORTED``) so this
    is easy to find in CI logs and obvious in a terminal.
    """
    bang = "!" * _LINE_WIDTH
    out: list[str] = ["", bang, bang]
    out.append(
        f"  [DEBUG_PRETTY_PRINT] UNSUPPORTED: provider={provider!r} "
        f"wire_format={wire_format!r}"
    )
    out.append(f"  REASON: {reason}")
    out.append(
        "  ACTION: a dedicated formatter for this request shape has NOT been "
        "implemented yet."
    )
    out.append(
        "  The raw payload is dumped below as JSON so nothing is hidden — "
        "but layout will be ugly."
    )
    out.append(bang)
    out.append(bang)
    safe = _strip_none(_to_jsonable(config_data))
    out.append(_indent(_pretty_json(safe), "  "))
    out.append(bang)
    return "\n".join(out)


def _fallback_dump(
    provider: str,
    config_data: Any,
    *,
    wire_format: str | None = None,
) -> str:
    """Last-resort renderer — JSON-pretty-print the converted payload.

    Used for provider strings we don't recognize at all. We still emit a
    warning banner so callers know the layout came from the fallback path
    rather than a dedicated formatter (avoids the silent-success failure
    mode where someone trusts a misleading rendering).
    """
    bang = "!" * _LINE_WIDTH
    out: list[str] = ["", bang]
    out.append(
        f"  [DEBUG_PRETTY_PRINT] WARNING: no dedicated formatter for "
        f"provider={provider!r} (wire_format={wire_format!r})."
    )
    out.append(
        "  Falling back to a raw JSON dump. Add this provider to "
        "matrx_ai.providers.debug_pretty_print._FORMATTERS to fix."
    )
    out.append(bang)
    safe = _strip_none(_to_jsonable(config_data))
    out.append(_indent(_pretty_json(safe), "  "))
    out.append(bang)
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Misc small helpers
# ----------------------------------------------------------------------------
def _pretty_json(value: Any) -> str:
    return json.dumps(_to_jsonable(value), indent=2, ensure_ascii=False, default=str, sort_keys=False)


def _pretty_maybe_json(value: Any) -> str:
    """If ``value`` is a JSON string, parse + re-pretty. Otherwise show as-is."""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped and stripped[0] in "{[":
            try:
                parsed = json.loads(stripped)
                return _pretty_json(parsed)
            except json.JSONDecodeError:
                pass
        return value
    return _pretty_json(value)


def _short_value(value: Any) -> str:
    """One-line repr for a parameter — keep small ints/strings, json the rest."""
    if isinstance(value, (bool, int, float)) or value is None:
        return repr(value)
    if isinstance(value, str):
        if len(value) <= 200:
            return value
        return _abbreviate_opaque(value, label="value")
    safe = _to_jsonable(value)
    return json.dumps(safe, ensure_ascii=False, default=str, sort_keys=False)
