"""Dumb observer for the actual outbound provider payload.

Receives the literal dict (or dataclass-converted dict) that's about to be
handed to a provider SDK and reports (1) whether any tool ``name`` value
appears more than once under the top-level ``tools`` key, and (2) whether
any tool name is not provider-serializable (fails ``^[a-zA-Z0-9_-]{1,64}$``
— e.g. an internal colon-namespaced name that slipped past the wire-name
seam in ``BaseTranslator.build_provider_tools``). The observer:

  - Has zero provider knowledge — no Anthropic shape, no Google
    function_declarations special-casing, no OpenAI variant handling.
    It walks the ``tools`` value generically and collects every string
    found under a ``name`` key.
  - Does NOT canonicalize, NOT resolve UUIDs, NOT theorize about future
    state. It just counts the literal name strings the provider is
    about to receive.
  - Never raises.
  - Logs green when clean, red JSON when duplicates exist.

Hooked into ``capture_request_payload`` (the single shared post-
translation point every provider already calls) so every model sees the
same check with one consistent log line.

Toggle via ``LOCAL_TOOL_DEBUG`` below. Set to False (or remove the
import + call from snapshot.py) once we're satisfied the duplicate-tool
class of bug is structurally prevented.
"""
from __future__ import annotations

import dataclasses
import json
from typing import Any

from matrx_utils import vcprint

# Flip to False to disable the observer without removing the call. The
# observer never blocks the API call; this just controls whether it
# logs anything at all.
LOCAL_TOOL_DEBUG: bool = True


def _collect_names(value: Any, out: list[str]) -> None:
    """Recursively walk ``value`` and append every string found under a
    ``name`` key to ``out``. Provider-agnostic — works for whatever
    shape the post-translation payload happens to be (Anthropic's flat
    list, Google's ``function_declarations`` nested list, OpenAI's
    chat-completions or responses-API variants — anything)."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k == "name" and isinstance(v, str):
                out.append(v)
            else:
                _collect_names(v, out)
    elif isinstance(value, list):
        for item in value:
            _collect_names(item, out)


def _declaration_field(decl: Any, key: str) -> Any:
    """Read ``key`` from a declaration that may be a dict (OpenAI/Anthropic
    payloads), a pydantic object (Google ``types.Tool`` /
    ``FunctionDeclaration``), or a protobuf message (xAI ``chat_pb2.Tool``).
    Attribute access covers the last two."""
    if isinstance(decl, dict):
        return decl.get(key)
    return getattr(decl, key, None)


def _collect_declaration_names(tools: Any, out: list[str]) -> None:
    """Collect ONLY declaration-level tool names — top-level ``name``,
    OpenAI Chat's / xAI's ``function.name``, and Google's nested
    ``function_declarations`` / ``functionDeclarations`` entries. Unlike
    :func:`_collect_names`, this never descends into parameter schemas, so
    an arbitrary ``name`` string inside a schema (a default value, an
    example) can't trip name-validity checks. Declarations may be dicts,
    pydantic objects (Google) or protobufs (xAI) — see
    :func:`_declaration_field`."""
    if not isinstance(tools, (list, tuple)):
        return
    for decl in tools:
        name = _declaration_field(decl, "name")
        if isinstance(name, str) and name:
            out.append(name)
            continue
        fn = _declaration_field(decl, "function")
        fn_name = _declaration_field(fn, "name") if fn is not None else None
        if isinstance(fn_name, str) and fn_name:
            out.append(fn_name)
            continue
        for key in ("function_declarations", "functionDeclarations"):
            nested = _declaration_field(decl, key)
            if isinstance(nested, (list, tuple)):
                for entry in nested:
                    entry_name = _declaration_field(entry, "name")
                    if isinstance(entry_name, str) and entry_name:
                        out.append(entry_name)


def inspect_outbound_payload(config_data: Any) -> bool:
    """Look at the literal payload going to the SDK; report duplicates.

    Returns True when no duplicate names are found under ``tools``;
    False otherwise. Returning False does NOT block the call — the
    observer is read-only by design.

    Caller (``capture_request_payload``) gates on ``LOCAL_TOOL_DEBUG``
    so the cost is one ``if`` check when the flag is off.
    """
    if not LOCAL_TOOL_DEBUG:
        return True

    try:
        payload: Any = config_data
        if dataclasses.is_dataclass(payload) and not isinstance(payload, type):
            payload = dataclasses.asdict(payload)

        if not isinstance(payload, dict):
            return True

        tools = payload.get("tools")
        if not tools:
            # Google's payload nests tools inside a GenerateContentConfig
            # object at payload["config"].tools — attribute access, not a
            # dict key. Without this the observer never inspects a single
            # Gemini declaration.
            cfg = payload.get("config")
            if cfg is not None and not isinstance(cfg, (str, int, float, bool)):
                tools = getattr(cfg, "tools", None)
        if not tools:
            return True

        names: list[str] = []
        _collect_names(tools, names)

        declaration_names: list[str] = []
        _collect_declaration_names(tools, declaration_names)

        if not names:
            # Non-dict payload shapes (Google pydantic objects, xAI
            # protobufs) are invisible to the recursive dict walk — fall
            # back to the declaration-level collector for the dup check.
            names = list(declaration_names)

        if not names:
            return True

        seen_counts: dict[str, int] = {}
        for n in names:
            seen_counts[n] = seen_counts.get(n, 0) + 1

        duplicates = {n: c for n, c in seen_counts.items() if c > 1}

        # Independent second layer for the wire-name contract: the primary
        # conversion lives in BaseTranslator.build_provider_tools; this
        # observer sees the LITERAL payload, so it catches any path that
        # bypassed the seam (a hand-assembled tools array, a future
        # translator that skips the chokepoint, a regression). Checked on
        # declaration-level names only — schema internals can legitimately
        # contain arbitrary "name" strings.
        from matrx_ai.config.wire_names import is_wire_safe

        unserializable = sorted({n for n in declaration_names if not is_wire_safe(n)})

        if not duplicates and not unserializable:
            vcprint(
                "[TOOL VALIDATOR] Tools valid. No Duplicates",
                color="green",
                log_level="DEBUG",
                stdout=False,
            )
            return True

        if unserializable:
            report = {
                "error": "UNSERIALIZABLE TOOL NAMES IN OUTBOUND PAYLOAD",
                "invalid_tool_names": unserializable,
                "why": (
                    "Providers enforce ^[a-zA-Z0-9_-]{1,64}$ on tool names. An "
                    "internal colon-namespaced name reached the literal provider "
                    "payload — the wire-name seam (BaseTranslator."
                    "build_provider_tools / matrx_ai.config.wire_names) was "
                    "bypassed or regressed. The provider WILL 400 this request."
                ),
                "all_names": sorted(seen_counts.keys()),
            }
            vcprint(
                json.dumps(report, indent=2, default=str),
                "🚨 [TOOL VALIDATOR] INVALID TOOL NAME(S) WILL 400 AT PROVIDER — "
                "wire-name conversion missed",
                color="red",
            )

        if duplicates:
            report = {
                "error": "DUPLICATE TOOL NAMES IN OUTBOUND PAYLOAD",
                "duplicate_tool_names": sorted(duplicates.keys()),
                "occurrence_counts": duplicates,
                "total_name_occurrences": len(names),
                "unique_names": len(seen_counts),
            }
            vcprint(
                json.dumps(report, indent=2, default=str),
                "[TOOL VALIDATOR] DUPLICATE TOOLS WILL FAIL AT PROVIDER",
                color="red",
            )
        return False
    except Exception as exc:
        # Never let the observer interfere with the actual API call.
        vcprint(
            f"[TOOL VALIDATOR] observer error (non-fatal): {exc!r}",
            color="yellow",
        )
        return True
