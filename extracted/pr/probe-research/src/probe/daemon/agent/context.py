"""size each agent's context window and compact its history (summaries keep the logbook block, written by code)."""

from __future__ import annotations

import functools
import os
from dataclasses import dataclass, replace
from typing import Any, Callable
#: Conversation mode compacts once the context passes this many tokens (estimated).
#: The writer: 250K (Richard, 2026-10-07: "lets cap the writer to 250k tokens";
#: it was 950K, his "1m" of 09-28). Every round re-reads the whole context, and in
#: the 7 days to 10-07, 78% of writer spend ($763 of $972) was calls over 200K
#: tokens; under 272K OpenAI also bills gpt-6.1-sol at its short-context rate.
#: The reader: only the immediate reading matters (Richard, 2026-09-28: "compact
#: to 120k"). It never compacts: a turn that would pass its size starts the
#: conversation fresh instead (rule A, `reader_lane`; 2026-10-14).
#: Both are the client's own; the server can lower them (`writer_context_tokens`,
#: `read_context_tokens`; Richard 2026-10-07, T10: "server-pushed cap").
CONTEXT_TOKENS_ENV = "PROBE_DAEMON_CONTEXT_TOKENS"
READ_CONTEXT_TOKENS_ENV = "PROBE_READER_CONTEXT_TOKENS"
CONTEXT_TOKENS = int(os.environ.get(CONTEXT_TOKENS_ENV) or 250_000)
READ_CONTEXT_TOKENS = int(os.environ.get(READ_CONTEXT_TOKENS_ENV) or 120_000)


def _own_size(name: str, default: int) -> int:
    """A size the session's environment sets (`name`), else `default` (read at
    import). In the daemon host the module was imported once for every run, so a
    run reads its own environment here (`runctx`)."""
    from probe.daemon.host import runctx

    if runctx.current() is not None:
        try:
            return int(os.environ.get(name) or default)
        except ValueError:
            return default
    return default


def _lowered_by_server(own: int, lane: str) -> int:
    from probe.daemon.agent.model import model as model_mod

    server = model_mod.server_context_tokens(lane)
    return min(own, server) if server is not None and own > 0 else own


def writer_context_tokens() -> int:
    """The writer's size: CONTEXT_TOKENS, or the server's if that is lower."""
    from probe.daemon.agent.model import model as model_mod

    return _lowered_by_server(_own_size(CONTEXT_TOKENS_ENV, CONTEXT_TOKENS), model_mod.LANE_WRITE)


def read_context_tokens() -> int:
    """The reader's size: READ_CONTEXT_TOKENS, or the server's if that is lower."""
    from probe.daemon.agent.model import model as model_mod

    return _lowered_by_server(_own_size(READ_CONTEXT_TOKENS_ENV, READ_CONTEXT_TOKENS), model_mod.LANE_READ)
#: The writer compacts this many tokens before its size (swarm friction T18):
#: one bite (`bite.NEW_SHOWN_TOKENS`) under it, so the request a new bite makes
#: never reaches the model route's ceiling (`companion_daemon_prompt_ceiling_tokens`,
#: 10K over the writer's 250K), which refused 3 writer requests on 10-28.
COMPACT_ROOM_TOKENS = 40_000
#: Compaction's first tier keeps this many recent tool call / result pairs whole...
KEEP_TOOL_PAIRS = 6
#: ...and clears nothing unless that reclaims at least this many tokens (a clear
#: rewrites history, so the provider re-caches from there: not for a few tokens).
MIN_CLEAR_TOKENS = 20_000
#: Once the context passes its size, compaction brings it down to this share of
#: it. Every compaction rewrites the history, and the provider then re-caches all
#: of it at the write price; stopping just under the size made the next bite
#: cross it again, so a long session compacted (and re-cached ~1M tokens) on
#: nearly every bite (2026-10-05, "22 messages -> 22" once a minute).
COMPACT_TO = 0.5
#: The summarizing tier keeps the newest messages, whole, up to this share of the
#: size: a token budget, since one message can be a whole bite of the session.
#: The newest message stays even when it alone is bigger.
KEEP_SHARE = 0.25
#: Compaction also runs once the history is more than this many chat messages
#: on the wire (`wire_messages`), whatever its size: the server's model route
#: refuses a request of more than 2,000 (`MAX_CHAT_MESSAGES`,
#: `app/companion/chat_router.py`). A session of small bites reached 2,003 at
#: 245K tokens, under the writer's 250K size, and its next call was refused with
#: a 400 (strand-ai, 2026-10-11). The gap to 2,000 covers what the count leaves
#: out: the instructions' own messages and EARLIER_TURNS.
COMPACT_MESSAGES = 1_800
#: ...and the summarizing tier then keeps at most this many wire messages of the
#: newest (still within KEEP_SHARE), so the next count compaction is ~1,300
#: messages away, not one round.
KEEP_MESSAGES = 500
#: The user turn put between the summary and a kept tail that opens with the
#: model's own message (`user_turn_first`).
EARLIER_TURNS = "[earlier turns are summarized above]"


SUMMARY_PROMPT = """\
Summarize this conversation of the Probe daemon - your summary REPLACES it, so it must let the daemon carry \
on without redoing work. Write prose under these headings, and skip one only if it is empty:

## What the session is about
## What was recorded
What the landed writes recorded, in words.
## What failed or waits for the researcher
Failed or refused writes, and questions waiting.
## Where it left off
What was in progress.

Quote numbers and metric names exactly. Copy no ids or slugs: the daemon adds its logbook of landed writes below \
your summary. Reply with the summary only.

<messages>
{messages}
</messages>\
"""


def user_turn_first(messages: list) -> list:
    """The history with a user turn before the model's first message. Compaction
    keeps the summary (system parts) and a tail that can open with the model's
    own tool call; after the system messages, Gemini refuses a tool call that
    follows neither a user turn nor a tool result. Such a tail gets
    EARLIER_TURNS in front of it; any other history is returned as it is.

    A tail can also open with tool results whose calls were summarized away:
    the harness's cut pairs a call with its ToolReturnPart but not with a
    RetryPromptPart, so it can land right after a round whose calls all failed
    validation. Nothing can answer to those, so a request of only such results
    is dropped there (Pydantic AI would drop it on the way out and send the
    model's tool call straight after the system messages)."""
    from pydantic_ai.messages import (
        ModelRequest,
        ModelResponse,
        RetryPromptPart,
        SystemPromptPart,
        ToolReturnPart,
        UserPromptPart,
    )

    def orphaned(message: Any) -> bool:
        return bool(message.parts) and all(
            isinstance(p, ToolReturnPart) or (isinstance(p, RetryPromptPart) and p.tool_name is not None)
            for p in message.parts)

    out: list = []
    for i, message in enumerate(messages):
        if isinstance(message, ModelRequest) and all(isinstance(p, SystemPromptPart) for p in message.parts):
            out.append(message)
            continue
        if isinstance(message, ModelRequest) and orphaned(message):
            continue
        if isinstance(message, ModelResponse):
            return [*out, ModelRequest(parts=[UserPromptPart(EARLIER_TURNS)]), *messages[i:]]
        return messages if len(out) == i else [*out, *messages[i:]]
    if len(out) == len(messages):
        return messages
    # Nothing left but the system messages: the user turn the request needs.
    return [*out, ModelRequest(parts=[UserPromptPart(EARLIER_TURNS)])]


def wire_messages(messages: list) -> int:
    """How many chat messages `messages` are on the model route, which counts
    those, not Pydantic AI's: one per model response, one per part of a request
    (each tool result, prompt and system part is its own message,
    `OpenAIChatModel._map_user_message`). One round of three parallel reads is 2
    messages here and 4 on the wire."""
    from pydantic_ai.messages import ModelRequest

    return sum(len(m.parts) if isinstance(m, ModelRequest) else 1 for m in messages)


def newest_within(messages: list, wire: int) -> int:
    """How many of the newest `messages` fit in `wire` chat messages (at least
    one)."""
    total = 0
    for n, message in enumerate(reversed(messages)):
        total += wire_messages([message])
        if total > wire:
            return max(n, 1)
    return len(messages)


#: How a compaction summary opens (pydantic-ai-harness's `_SUMMARY_PREFIX`).
SUMMARY_HEAD = "Summary of previous conversation:\n\n"


def _summary_parts(message: Any) -> list[int]:
    """The indexes of a request's compaction-summary parts."""
    from pydantic_ai.messages import ModelRequest, SystemPromptPart

    if not isinstance(message, ModelRequest):
        return []
    return [i for i, p in enumerate(message.parts)
            if isinstance(p, SystemPromptPart) and p.content.startswith(SUMMARY_HEAD)]


def _prose(summary: str) -> str:
    """A summary without the logbook block (plain code's, or one the model wrote
    in its shape): everything from the block's heading on goes."""
    from probe.daemon.worker.bite import bite as bite_mod

    cut = summary.find(bite_mod.LANDED_HEAD)
    return summary if cut < 0 else summary[:cut].rstrip()


def _rewrite_summaries(messages: list, rewrite: Callable[[str], str]) -> list:
    """`messages` with each compaction summary's text rewritten; the same list
    when none changed."""
    out = list(messages)
    changed = False
    for m, message in enumerate(messages):
        for i in _summary_parts(message):
            part = message.parts[i]
            text = rewrite(part.content)
            if text != part.content:
                parts = list(out[m].parts)
                parts[i] = replace(part, content=text)
                out[m] = replace(out[m], parts=parts)
                changed = True
    return out if changed else messages


def _logbook_block(state: RunState) -> str | None:
    """`state`'s logbook block; None when it has none. A logbook that cannot be
    read says so in the block rather than failing the run."""
    if state.logbook is None:
        return None
    try:
        return state.logbook()
    except Exception as exc:  # noqa: BLE001 -- never the run's failure
        from probe.daemon.worker.bite import bite as bite_mod

        log.warning("the logbook block was not built: %s: %s", type(exc).__name__, exc)
        return f"{bite_mod.LANDED_HEAD}\n- the logbook could not be read just now"


def without_logbook(messages: list) -> list:
    """`messages` with every compaction summary cut to its prose."""
    return _rewrite_summaries(messages, _prose)


def with_logbook(messages: list, block: str | None) -> list:
    """`messages` with the compaction summary's prose followed by `block`, plain
    code's list of the landed writes. Whatever the model wrote in that block's
    shape is cut first, so the block is the logbook's alone. None: no block."""
    if block is None:
        return without_logbook(messages)
    return _rewrite_summaries(messages, lambda text: f"{_prose(text)}\n\n{block}")


@functools.cache
def server_tokenizer() -> Callable[[str], int] | None:
    """Tokens as the model route counts a prompt against its ceiling: o200k_base
    (`app/companion/chat_router.py` `_count_tokens`), from the vocabulary this
    package ships (`probe.foundation.token_budget.token_budget`; ~0.8 s to load, once per process). None
    without it (tiktoken is the `mcp` extra's): the harness's 4 characters per
    token, which read a bite of paths and diffs 12-28K tokens under the route's
    count (10-28). A text it cannot encode counts 4 characters per token."""
    try:
        from probe.foundation.token_budget.token_budget import count_tokens

        count_tokens("")
    except Exception as exc:  # noqa: BLE001 -- no tokenizer: the harness's own estimate
        log.info("compaction estimates by characters: no tokenizer (%s)", type(exc).__name__)
        return None

    def tokens(text: str) -> int:
        try:
            return count_tokens(text)
        except Exception:  # noqa: BLE001 -- a lone surrogate
            return len(text) // 4

    return tokens


def counted_compaction(state: RunState):
    """TieredCompaction that tells `state` each time it rewrote the history, and
    keeps a user turn first after it (`user_turn_first`). The size is the
    state's (the writer's by default); the reader never compacts.

    It runs once the context passes the size (less `state.compact_room`), counted
    with `state.tokenizer`, and compacts down to COMPACT_TO of it (the harness's
    own target is that lower mark; the size is our gate), the
    summary keeping the newest KEEP_SHARE of the size whole, and at most
    KEEP_MESSAGES wire messages. A history of more than COMPACT_MESSAGES wire
    messages is summarized whatever its size, since the model route refuses one
    past 2,000."""
    from pydantic_ai_harness.compaction import (
        ClearToolResults,
        SummarizingCompaction,
        TieredCompaction,
        estimate_context_tokens,
        estimate_token_count,
    )

    size = state.context_tokens or writer_context_tokens()
    if size <= 0:
        # Would compact before every request: refused, so the worker falls back to
        # bites (`worker._compaction_available`), as the harness's own
        # `target_tokens=0` refusal did before the floors below were added.
        raise ValueError(f"a context of {size} tokens cannot be compacted to")
    # Compacts once past `size` less the room, never so early that the target
    # (COMPACT_TO of the size) is half way to it.
    gate = size - min(max(0, state.compact_room), int(size * (1 - COMPACT_TO) / 2))
    tokenizer = state.tokenizer

    class KeptByCount(SummarizingCompaction):
        """Keeps the newest `keep_tokens`, but never more than KEEP_MESSAGES wire
        messages: when the newest KEEP_MESSAGES alone fit the token budget, the
        token cut would keep more of them, so the cut is by count. The summary
        it writes ends with plain code's logbook block (`with_logbook`)."""

        async def compact(self, messages: list, ctx: Any) -> list:
            n = newest_within(messages, KEEP_MESSAGES)
            if (self.keep_tokens is not None and n < len(messages)
                    and estimate_token_count(messages[-n:], self.tokenizer) <= self.keep_tokens):
                return await replace(self, keep_tokens=None, keep_messages=n).compact(messages, ctx)
            # The previous summary is the model's anchor without its logbook block,
            # so the model never sees ids to copy, and the new block is rebuilt.
            prose = without_logbook(messages)
            out = await super().compact(prose, ctx)
            if out is prose:
                return messages
            return with_logbook(out, _logbook_block(state))

    summarizer = KeptByCount(max_messages=1, keep_tokens=max(1, int(size * KEEP_SHARE)),
                             preserve_first_user_message=False,
                             summary_prompt=SUMMARY_PROMPT,
                             tool_return_max_chars=1_500,
                             summarization_capabilities=[UsageMeter(on_round=state.on_round)],
                             tokenizer=tokenizer)

    @dataclass
    class CountedCompaction(TieredCompaction):
        async def before_model_request(self, ctx: Any, request_context: Any) -> Any:
            before = request_context.messages
            over_size = estimate_context_tokens(list(before), self.tokenizer,
                                                model_request_parameters=request_context.model_request_parameters) > gate
            if not over_size and wire_messages(before) <= COMPACT_MESSAGES:
                request_context.messages = user_turn_first(before)
                return request_context
            n, wire = len(before), wire_messages(before)
            out = await super().before_model_request(ctx, request_context) if over_size else request_context
            if wire_messages(out.messages) > COMPACT_MESSAGES:
                # Too many messages for the model route, whatever their size (or the
                # cheap tier was enough for the size): the summarizing tier, by count.
                # It calls the model this request goes to, as the tiers above do.
                tier_ctx = ctx if request_context.model is ctx.model else replace(ctx, model=request_context.model)
                out.messages = await summarizer.compact(list(out.messages), tier_ctx)
            after = out.messages
            if after is not before and (len(after) != n or any(a is not b for a, b in zip(after, before))):
                log.info("compacted the conversation (%s): %s messages (%s on the wire) -> %s (%s)",
                         "size" if over_size else "count", n, wire, len(after), wire_messages(after))
                state.compacted()
            out.messages = user_turn_first(out.messages)
            return out

    return CountedCompaction(
        tiers=[ClearToolResults(max_tokens=1, keep_pairs=KEEP_TOOL_PAIRS, min_clear_tokens=MIN_CLEAR_TOKENS,
                                tokenizer=tokenizer),
               summarizer],
        target_tokens=max(1, int(size * COMPACT_TO)), tokenizer=tokenizer)
from probe.daemon.agent.guards import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.state import RunState, UsageMeter  # noqa: E402 -- pieces need each other; the front door loads this one first
