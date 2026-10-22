"""A provider's MCP server that stumbles is asked again — when that is safe — and a failure says whose it was.

Every call to a person's connected MCP server (an agent's tool call, a sync, an import, a workflow step) goes
through ``ExternalMCPClient.call_tool``; this module is its rule for failures, so every connection inherits it.

WHEN A CALL IS ASKED AGAIN
- It never reached the provider (could not connect, it said "slow down" — 429 / rate limit): nothing was done
  there, so any tool is asked again.
- It may have reached the provider and no answer came back (a timeout, a dropped connection, a 500/502/503/504 —
  a gateway that gave up may already have passed the call on): asked again ONLY
  when the tool declares it is safe to repeat (MCP ``readOnlyHint`` or ``idempotentHint``). A write that may
  or may not have happened is never sent twice; it is reported as unconfirmed.
Attempts and the wait between them are knobs (``agents.tool_dispatch``: ``connection_retry_attempts``,
``connection_retry_wait_seconds``; the wait doubles each time).

WHAT A FAILURE SAYS
The provider by name, what happened in plain words, how many times it was asked, and that our side did its
part — never an empty "Failed to call MCP server:" (live 2026-10-17: a timeout's own text is empty).
"""

from __future__ import annotations

import re
import time
from contextvars import ContextVar
from typing import Any
from urllib.parse import urlparse

from matrx_ai.tools.knobs import _positive_float, tool_dispatch_knob

ATTEMPTS_KEY = "connection_retry_attempts"
WAIT_KEY = "connection_retry_wait_seconds"
#: KNOB MIRROR of platform.feature_knob "agents.tool_dispatch" "connection_retry_attempts"
ATTEMPTS_MIRROR = 3
#: KNOB MIRROR of platform.feature_knob "agents.tool_dispatch" "connection_retry_wait_seconds"
WAIT_MIRROR = 2.0

NOT_REACHED = "not_reached"  # nothing happened at the provider: safe to ask again for any tool
NO_ANSWER = "no_answer"  # it may have happened: ask again only a tool that is safe to repeat

#: An answer that says "you were refused before anything was done" (rate limits, overload). A PLAN cap
#: (Notion's ``usage_limit_reached``) is not one: asking again answers the same.
# Whole phrases or a LEADING status only — never a bare number anywhere in the text: "title must be at most 500
# characters" is the provider refusing the request, not the provider failing (adversarial review 2026-10-18).
_SLOW_DOWN = re.compile(r"^\W*(HTTP\s*)?429\b|\brate[ _-]?limit(ed|ing)?\b|\btoo many requests\b", re.I)
#: An error reply (``isError``) that says the provider itself failed on the way (not that the request was wrong).
_PROVIDER_STUMBLED = re.compile(r"^\W*(HTTP\s*)?50[0234]\b|\b(internal server error|bad gateway|service unavailable"
                                r"|gateway time-?out|temporarily unavailable|try again later|overloaded"
                                r"|upstream (connect|request) (error|timeout)"
                                r"|(request|api|server|upstream|gateway|connection|backend) timed out)\b", re.I)
#: JSON-RPC: the provider failed while handling the call (-32603 internal error; -32000..-32099 server errors) —
#: as opposed to refusing the request itself (-32600 invalid request, -32601 no such method, -32602 invalid params).
_RPC_PROVIDER_FAILED = re.compile(r"MCP error (-32603|-320\d\d)\b")
_RPC_REFUSED = re.compile(r"MCP error -3260[012]\b")
#: A plan or usage cap the provider says will answer the same if asked again (Notion: ``usage_limit_reached``, "do not
#: retry automatically"): never a stumble, even when its wording also says "try again later" (live 2026-10-21: three
#: retries of one capped Notion query).
_PLAN_CAP = re.compile(r"\busage_limit_reached\b|\bdo not retry\b|\bdon'?t retry\b", re.I)
#: The words ``failure_words`` puts on a call this layer already asked again: an outer loop must not repeat it.
_ASKED_AGAIN = re.compile(r"\basked \d+ times\b")
#: A URL's query may carry a key or a signature: never in a failure's words.
_QUERY = re.compile(r"\?[^\s\'\"]+")


def already_asked_again(text: str) -> bool:
    """This layer already asked the provider again before failing: an outer retry loop stops instead of stacking."""
    return bool(_ASKED_AGAIN.search(text or ""))


def attempts() -> int:
    try:
        return max(1, int(float(str(tool_dispatch_knob(ATTEMPTS_KEY, ATTEMPTS_MIRROR)).strip('"'))))
    except (TypeError, ValueError):
        return ATTEMPTS_MIRROR


def wait_before(attempt: int) -> float:
    """Seconds to wait before attempt ``attempt + 1`` (doubling)."""
    return _positive_float(tool_dispatch_knob(WAIT_KEY, WAIT_MIRROR), WAIT_MIRROR) * (2 ** (attempt - 1))


#: When the caller's own deadline ends (``time.monotonic()``), set by the agent tool executor around a dispatch: the
#: connection's budget counts from the dispatch, not from after its token refresh (adversarial re-review R-C1c).
DISPATCH_ENDS_AT: ContextVar[float | None] = ContextVar("mcp_dispatch_ends_at", default=None)


class Deadline:
    """One call's whole time budget, shared by every attempt and every wait between them, so the call answers in
    its own words before the caller's deadline does (the agent dispatch ceiling: adversarial review 2026-10-18 —
    with both at 120s a hung provider never reached its retry, and the ceiling's generic "safe to repeat" could
    double a write). The first attempt gets half the time left (a slow, healthy provider keeps a real chance);
    later attempts share the rest. No budget: every attempt may use the client's own timeout."""

    #: The shortest attempt worth making (seconds): less cannot hear any answer.
    SHORTEST = 0.5

    def __init__(self, budget_seconds: float | None, tries: int, *, repeatable: bool = True) -> None:
        self.tries = max(1, tries)
        self.repeatable = repeatable
        dispatch_end = DISPATCH_ENDS_AT.get()
        if dispatch_end is not None and dispatch_end <= time.monotonic():
            dispatch_end = None  # inherited by background work that outlived its tool call: not this call's deadline
        ends = [x for x in ((time.monotonic() + budget_seconds) if budget_seconds else None, dispatch_end) if x]
        # the call answers a full first wait before the caller's deadline: room to say what happened
        self.end = (min(ends) - wait_before(1)) if ends else None

    def _waits_after(self, attempt: int) -> float:
        return sum(wait_before(k) for k in range(attempt, self.tries))

    def for_attempt(self, attempt: int, longest: float) -> float:
        if self.end is None:
            return longest
        usable = max(0.0, self.end - time.monotonic() - self._waits_after(attempt))
        # a tool that is never asked again after no answer gets the whole time (a slow write must not become
        # "unconfirmed" early); a read's first attempt keeps two thirds, so a slow, healthy provider still answers
        share = usable if (attempt >= self.tries or not self.repeatable) else usable * 2 / 3 if attempt == 1 else usable / 2
        return max(self.SHORTEST, min(longest, share))

    def room_for_another(self, attempt: int) -> bool:
        """Another attempt still fits (its wait plus a moment to answer)."""
        return self.end is None or self.end - time.monotonic() > wait_before(attempt) + self.SHORTEST


def safe_to_repeat(tool_def: Any) -> bool:
    """The tool says repeating it changes nothing (MCP ``readOnlyHint`` / ``idempotentHint``)."""
    for ann in getattr(tool_def, "annotations", None) or []:
        if isinstance(ann, dict) and (ann.get("readOnlyHint") is True or ann.get("idempotentHint") is True):
            return True
    return False


def classify(exc: BaseException) -> str | None:
    """Was a raised failure the provider not answering (and could anything have happened there)? None: not a
    stumble — the request itself was refused or wrong, and asking again would answer the same."""
    import httpx

    if isinstance(exc, httpx.ConnectError | httpx.ConnectTimeout | httpx.PoolTimeout):
        return NOT_REACHED
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # only a rate limit promises nothing was done; a gateway that gave up (502/504) or a busy server (503) may have
        # passed the call on, so a write is never sent again on it
        return NOT_REACHED if code == 429 else NO_ANSWER if code >= 500 else None
    if isinstance(exc, httpx.TimeoutException | httpx.RemoteProtocolError | httpx.ReadError | httpx.WriteError):
        return NO_ANSWER
    if isinstance(exc, TimeoutError | ConnectionError):
        return NO_ANSWER
    text = str(exc)
    if _PLAN_CAP.search(text):
        return None  # a plan cap answers the same if asked again
    if _RPC_REFUSED.search(text):
        return None  # the request itself was wrong: asking again answers the same
    if _SLOW_DOWN.search(text):
        return NOT_REACHED
    if _RPC_PROVIDER_FAILED.search(text) or _PROVIDER_STUMBLED.search(text):
        return NO_ANSWER
    return None


def classify_reply(text: str) -> str | None:
    """An error REPLY (the provider answered ``isError``): a stumble only when it says slow down or that the
    provider itself failed; a refusal of the request is the provider's real answer."""
    if _PLAN_CAP.search(text or ""):
        return None
    if _SLOW_DOWN.search(text or ""):
        return NOT_REACHED
    if _PROVIDER_STUMBLED.search(text or ""):
        return NO_ANSWER
    return None


def provider_name(server_url: str | None, tool_name: str = "") -> str:
    """"Notion" from ``https://mcp.notion.com/mcp`` (or from a ``notion:`` tool name)."""
    host = (urlparse(server_url or "").hostname or "").lower()
    parts = [p for p in host.split(".") if p and p not in ("mcp", "api", "www", "app", "com", "io", "net", "org", "dev", "ai", "co")]
    word = parts[-1] if parts else (tool_name.split(":", 1)[0] if ":" in tool_name else "")
    return word[:1].upper() + word[1:] if word else "The connected service"


def cause(exc: BaseException | None, *, timeout: float | None = None, reply: str | None = None) -> str:
    """What happened, in plain words."""
    import httpx

    if reply is not None:
        return f"it answered with an error: {_QUERY.sub('?…', reply.strip())[:200]}"
    if isinstance(exc, httpx.ConnectError | httpx.ConnectTimeout):
        return "it could not be reached"
    if isinstance(exc, httpx.TimeoutException | TimeoutError):
        return f"it did not answer within {int(timeout)} seconds" if timeout else "it did not answer in time"
    if isinstance(exc, httpx.RemoteProtocolError | httpx.ReadError | ConnectionError):
        return "it dropped the connection before answering"
    if isinstance(exc, httpx.HTTPStatusError):
        return f"it answered {exc.response.status_code}"
    text = _QUERY.sub("?…", str(exc or "").strip())
    return f"{type(exc).__name__}: {text[:200]}" if text else type(exc).__name__


def failure_words(*, provider: str, tool: str, kind: str, why: str, tries: int, repeatable: bool) -> tuple[str, str]:
    """(message, suggested_action) for a call that did not come back."""
    asked = f"asked {tries} times" if tries > 1 else "asked once"
    if kind == NO_ANSWER and not repeatable:
        return (f"{provider} did not confirm “{tool}”: {why}. It was not sent again, because it may already have "
                f"been done on {provider}'s side. Nothing failed on ours.",
                f"Check in {provider} whether it was done before trying again.")
    return (f"{provider} did not answer “{tool}” ({why}; {asked}). The problem is on {provider}'s side; "
            "nothing failed on ours.",
            f"Try again in a few minutes; if {provider} keeps failing, its own status page will say so.")


__all__ = ["DISPATCH_ENDS_AT", "Deadline", "ATTEMPTS_KEY", "NOT_REACHED", "NO_ANSWER", "WAIT_KEY", "attempts", "cause", "classify", "classify_reply",
           "already_asked_again", "failure_words", "provider_name", "safe_to_repeat", "wait_before"]
