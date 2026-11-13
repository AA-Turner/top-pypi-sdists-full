"""Tool calls verl's hermes parser drops (F1): a `<tool_call>` block whose JSON does not parse is logged and removed
from the content (`tool_parser.py:121-130`), so it never reaches `messages` or `_call_tool`. The wrap re-finds those
blocks with the parser's OWN `tool_call_regex` and the same checks, and hands them to the loop's recording, which
records each as a failed call (`name=""`, the raw block as its arguments). Never silently lost."""

from __future__ import annotations

import asyncio
import functools
import json
import logging
from typing import Any

from ..wrapping import is_wrapped, make_install, set_wrapped
from .recording import get_recording

logger = logging.getLogger(__name__)

PARSER_MODULE = "verl.experimental.agent_loop.tool_parser"
HERMES_PARSER = "HermesToolParser"
EXTRACT = "extract_tool_calls"
#: The error a dropped call's run reads.
DROPPED_ERROR = "the parser dropped this call: invalid JSON; the tool never ran"


def wrap_hermes_parser(cls: type) -> bool:
    """``cls.extract_tool_calls`` hands the blocks it dropped to the loop's recording. Once per class."""
    original = cls.__dict__.get(EXTRACT)
    if not callable(original) or is_wrapped(original):
        return False

    @functools.wraps(original)
    async def extract_tool_calls(self: Any, responses_ids: Any, *args: Any, **kwargs: Any) -> Any:
        result = await original(self, responses_ids, *args, **kwargs)
        recording = get_recording()
        if recording is not None:
            try:
                dropped = await asyncio.to_thread(find_dropped_calls, self, responses_ids)
                recording.keep_dropped(dropped)
            except Exception as exc:  # noqa: BLE001 -- fail open: the loop runs on, the call is not recorded
                logger.debug("probe: verl's dropped tool calls were not found (%s: %s)", type(exc).__name__, exc)
        return result

    set_wrapped(cls, EXTRACT, extract_tool_calls)
    return True


install = make_install(HERMES_PARSER, wrap_hermes_parser)


def find_dropped_calls(parser: Any, responses_ids: Any) -> list[str]:
    """The raw `<tool_call>` blocks hermes dropped from these ids: found by its own regex, failing its own parse
    (`json.loads`, then `name` and `arguments`, the name a string as `FunctionCall` takes it)."""
    regex = getattr(parser, "tool_call_regex", None)
    if regex is None:
        return []
    text = parser.tokenizer.decode(list(responses_ids))
    if parser.tool_call_start_token not in text or parser.tool_call_end_token not in text:
        return []
    return [match for match in regex.findall(text) if not _is_parsed(match)]


def _is_parsed(match: str) -> bool:
    try:
        call = json.loads(match)
        name, arguments = call["name"], call["arguments"]
        json.dumps(arguments, ensure_ascii=False)
    except Exception:  # noqa: BLE001 -- exactly what hermes catches
        return False
    return isinstance(name, str)
