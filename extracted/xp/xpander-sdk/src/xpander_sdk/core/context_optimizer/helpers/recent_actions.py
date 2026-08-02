"""Render the ``<recent_actions>`` block injected into continuation messages.

Walks the tail of the message list, pulls the most recent N tool calls,
pairs each with its originating assistant ``tool_calls`` entry to recover
args, redacts secrets, head/tail-trims args + result, and renders against
the templates in ``prompts.py``.
"""

import json
from datetime import datetime, timezone
from typing import Any, List

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.constants import (
    INCLUDE_RECENT_ACTIONS,
    RECENT_ACTIONS_ARGS_HEAD,
    RECENT_ACTIONS_ARGS_TAIL,
    RECENT_ACTIONS_COUNT,
    RECENT_ACTIONS_RESULT_HEAD,
    RECENT_ACTIONS_RESULT_TAIL,
)
from xpander_sdk.core.context_optimizer.helpers.secrets import (
    _redact_sensitive_payload,
    _redact_sensitive_text,
)
from xpander_sdk.core.context_optimizer.helpers.tool_result import (
    _head_tail_preview,
    unwrap_tool_result_content,
)
from xpander_sdk.core.context_optimizer.helpers.xml_safety import (
    _looks_like_error_payload,
    _strip_illegal_xml_chars,
    _xml_attr_escape,
)
from xpander_sdk.core.context_optimizer.prompts import (
    RECENT_ACTION_ENTRY_TEMPLATE,
    RECENT_ACTIONS_BLOCK_TEMPLATE,
)


def _build_recent_actions_block(
    messages: List[Message],
    n: int = RECENT_ACTIONS_COUNT,
) -> str:
    """Render the last ``n`` tool messages as a ``<recent_actions>`` XML block.

    Returns ``""`` when ``INCLUDE_RECENT_ACTIONS`` is False, when ``messages``
    is empty, or when no eligible tool messages remain after skip-list
    filtering. Pairs each tool message with its originating assistant
    ``tool_calls`` entry by ``tool_call_id`` to recover the request args.
    Args/result are head/tail-previewed and XML-escaped.
    """
    # Late-bind the feature flag against the ``context_optimizer`` module so
    # callers (and tests) can monkeypatch ``co.INCLUDE_RECENT_ACTIONS`` at
    # runtime without having to know which sub-module owns the constant.
    from xpander_sdk.core.context_optimizer import context_optimizer as _co

    if not _co.INCLUDE_RECENT_ACTIONS or not messages:
        return ""

    from xml.sax.saxutils import escape as xml_escape

    # Walk in reverse, collect indices of the last N tool messages.
    collected: List[int] = []
    for i in range(len(messages) - 1, -1, -1):
        m = messages[i]
        if getattr(m, "role", None) != "tool":
            continue
        collected.append(i)
        if len(collected) >= n:
            break

    if not collected:
        return ""

    # Reverse to chronological order for rendering.
    collected.reverse()

    entries: List[str] = []
    for entry_idx, msg_idx in enumerate(collected, start=1):
        m = messages[msg_idx]
        tool_name = getattr(m, "tool_name", None) or "<unknown>"
        tool_call_id = getattr(m, "tool_call_id", None)

        # Pair with assistant tool_calls request args.
        args_obj: Any = None
        if tool_call_id:
            for j in range(msg_idx - 1, -1, -1):
                prev = messages[j]
                if getattr(prev, "role", None) != "assistant":
                    continue
                tool_calls = getattr(prev, "tool_calls", None) or []
                try:
                    for tc in tool_calls:
                        if not isinstance(tc, dict):
                            continue
                        if tc.get("id") != tool_call_id:
                            continue
                        fn = tc.get("function") or {}
                        raw_args = fn.get("arguments") if isinstance(fn, dict) else None
                        if isinstance(raw_args, str):
                            try:
                                args_obj = json.loads(raw_args)
                            except Exception:
                                args_obj = raw_args
                        else:
                            args_obj = raw_args
                        break
                except Exception:
                    args_obj = None
                if args_obj is not None:
                    break
                # Stop scanning once we hit any assistant message — earlier
                # assistant messages won't own this tool_call_id.
                break

        if args_obj is None:
            args_obj = getattr(m, "tool_args", None)
        if args_obj is None:
            args_obj = {}

        # Status detection runs on the RAW (pre-redaction) result so the
        # heuristic still catches "internal server error" payloads even when
        # redaction would mask them.
        raw_result_text = unwrap_tool_result_content(getattr(m, "content", ""))
        status = "ok"
        if getattr(m, "tool_call_error", False):
            status = "error"
        elif _looks_like_error_payload(raw_result_text):
            status = "error"

        # Redact secrets before any payload leaves this function — args dict
        # walks structured keys, result text runs inline-pattern redaction.
        safe_args = _redact_sensitive_payload(args_obj)
        try:
            args_text = json.dumps(safe_args, default=str, ensure_ascii=False)
        except Exception:
            args_text = str(safe_args)
        result_text = _redact_sensitive_text(raw_result_text)

        ts_raw = getattr(m, "created_at", None) or ""
        if isinstance(ts_raw, (int, float)):
            try:
                ts_text = datetime.fromtimestamp(ts_raw, tz=timezone.utc).isoformat()
            except Exception:
                ts_text = str(ts_raw)
        else:
            ts_text = str(ts_raw)

        args_preview = _head_tail_preview(
            args_text, RECENT_ACTIONS_ARGS_HEAD, RECENT_ACTIONS_ARGS_TAIL
        )
        result_preview = _head_tail_preview(
            result_text, RECENT_ACTIONS_RESULT_HEAD, RECENT_ACTIONS_RESULT_TAIL
        )

        entries.append(
            RECENT_ACTION_ENTRY_TEMPLATE.format(
                idx=entry_idx,
                tool_name=_xml_attr_escape(tool_name),
                status=_xml_attr_escape(status),
                ts=_xml_attr_escape(ts_text),
                args=xml_escape(_strip_illegal_xml_chars(args_preview)),
                result=xml_escape(_strip_illegal_xml_chars(result_preview)),
            )
        )

    return RECENT_ACTIONS_BLOCK_TEMPLATE.format(
        count=len(entries),
        entries="\n".join(entries),
    )
