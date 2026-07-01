"""Backdated web toolset — ``web_search`` + ``web_fetch`` over the GR corpus.

Unlike the other built-in toolsets, this one is **not** sandbox-backed: the
tools talk to the GR web service over HTTP (see
:mod:`openreward.web_service`), so the toolset deliberately does not call
``Toolset.__init__`` (which requires ``env.sandbox``).

Declared on an env via class attribute::

    from openreward.toolsets import BackSearchToolset

    class MyEnv(Environment):
        toolsets = [BackSearchToolset]
        web_as_of = "2025-12-01"   # optional cutoff; see below

…or selected per session by name::

    with env.session(task=task, toolset="backsearch") as session:
        session.call_tool("web_search", {"query": "..."})

**Cutoff date.** The corpus is backdated; ``as_of`` is resolved *on every tool
call* in priority order: explicit ``as_of=`` constructor arg (a static pin) >
``env.web_as_of`` > ``OPENREWARD_WEB_AS_OF`` env var > backend default (today).
The server process must have ``OPENREWARD_API_KEY`` set for the tools to be
configured.

**Progressing-date environments.** Because the cutoff is read live (not
snapshotted in ``__init__``), an env whose simulated clock advances keeps the
tools bounded to its current day — no post-cutoff leakage. ``env.web_as_of``
may be a plain attribute, a ``property``, or a zero-arg callable::

    class TimeSteppedEnv(Environment):
        toolsets = [BackSearchToolset]

        @property
        def web_as_of(self) -> str:
            return self.sim_clock.today().isoformat()   # advances as the task steps

The framework caches one toolset instance per env for the whole session, so a
construction-time snapshot would freeze the date at the first call — reading it
live is what makes the advancing case work.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from pydantic import BaseModel

from openreward.environments.environment import tool
from openreward.environments.toolset import Toolset
from openreward.environments.types import TextBlock, ToolOutput
from openreward.tools.web import (
    FETCH_DESCRIPTION,
    MIN_SEARCH_QUERY_LENGTH,
    SEARCH_DESCRIPTION,
    WebToolResult,
    run_fetch,
    run_search,
)
from openreward.web_service import WebServiceConfig


# ── Pydantic parameter models ──

class WebSearchParams(BaseModel, extra="forbid"):
    query: str
    allowed_domains: Optional[list[str]] = None
    blocked_domains: Optional[list[str]] = None


class WebFetchParams(BaseModel, extra="forbid"):
    url: str
    prompt: str


# ── Toolset ──

def _to_tool_output(result: WebToolResult) -> ToolOutput:
    """Render a :class:`WebToolResult` as a (non-terminal) ``ToolOutput``.

    Soft errors (bad URL, blocked domain, ...) are surfaced to the model as
    plain text so it can recover, with the error code in ``metadata`` for
    programmatic inspection — they are not raised as transport errors.
    """
    metadata: dict[str, Any] = dict(result.data) if result.data else {}
    if not result.ok:
        metadata["error"] = result.error_code
    return ToolOutput(
        blocks=[TextBlock(text=result.output)],
        metadata=metadata or None,
        reward=0.0,
        finished=False,
    )


class BackSearchToolset(Toolset):
    """Backdated web search/fetch toolset (``web_search`` + ``web_fetch``).

    Does not require a sandbox. See module docstring for cutoff-date
    configuration.
    """

    @classmethod
    def name(cls) -> str:
        return "backsearch"

    def __init__(
        self,
        env: Optional[Any] = None,
        *,
        as_of: Optional[str] = None,
        config: Optional[WebServiceConfig] = None,
    ) -> None:
        # NOTE: intentionally does not call super().__init__ — web tools are
        # not sandbox-backed, so the Toolset sandbox contract does not apply.
        self.env = env
        self.config = config
        # An explicit constructor arg is a HARD PIN (static cutoff). Otherwise
        # the cutoff is resolved fresh on EVERY tool call (see _current_as_of),
        # so an environment whose simulated "now" advances — a task stepping
        # forward through time — bounds each search/fetch to its current day
        # with no construction-time snapshot. This matters
        # because the framework lazily builds and caches one toolset instance
        # per env for the whole session, so a snapshot taken in __init__ would
        # freeze the cutoff at the first tool call.
        self._pinned_as_of = as_of

    @property
    def as_of(self) -> Optional[str]:
        """The cutoff the next tool call would use, resolved live."""
        return self._current_as_of()

    def _current_as_of(self) -> Optional[str]:
        """Resolve the cutoff at call time.

        Priority: explicit constructor pin > ``env.web_as_of`` > the
        ``OPENREWARD_WEB_AS_OF`` env var > backend default (today).
        ``env.web_as_of`` may be a plain attribute, a ``property``, or a
        zero-arg callable (a sim-clock) — the callable is invoked each call so
        a progressing-date env stays correct. Validation is deferred to the
        engine, which surfaces a bad cutoff as a recoverable ``invalid-as-of``
        tool result.
        """
        if self._pinned_as_of is not None:
            return self._pinned_as_of
        src: Any = getattr(self.env, "web_as_of", None)
        if callable(src):
            src = src()
        return src or os.getenv("OPENREWARD_WEB_AS_OF") or None

    @tool
    async def web_search(self, params: WebSearchParams) -> ToolOutput:
        result = await run_search(
            query=params.query,
            as_of=self._current_as_of(),
            allowed_domains=params.allowed_domains,
            blocked_domains=params.blocked_domains,
            config=self.config,
        )
        return _to_tool_output(result)

    @tool
    async def web_fetch(self, params: WebFetchParams) -> ToolOutput:
        result = await run_fetch(
            url=params.url,
            prompt=params.prompt,
            as_of=self._current_as_of(),
            config=self.config,
        )
        return _to_tool_output(result)


# Surface the rich descriptions as the tools' docstrings (the environment
# framework reads ``fn.__doc__`` for each tool's description).
BackSearchToolset.web_search.__doc__ = SEARCH_DESCRIPTION
BackSearchToolset.web_fetch.__doc__ = FETCH_DESCRIPTION

# Re-exported for callers that build their own JSON schemas.
__all__ = ["BackSearchToolset", "WebSearchParams", "WebFetchParams", "MIN_SEARCH_QUERY_LENGTH"]
