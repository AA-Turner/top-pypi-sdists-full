"""Regression test for the NameError that crashed real user TUI sessions.

Bug observed 2026-05-18: user typing into drydock TUI got
`Error: name '_tool_stop_injected' is not defined` because
`_perform_llm_turn` referenced `_tool_stop_injected` as if it were
a closure variable from `_conversation_loop`, but it's actually a
local variable in a different method's scope. Python NameError when
the read site fired.

Fix: promote to `self._tool_stop_injected` so both methods see it,
with defensive init in `_reset_session`.
"""
from __future__ import annotations

import inspect

from drydock.core.agent_loop import AgentLoop


def test_perform_llm_turn_uses_self_for_tool_stop_injected():
    """All references inside _perform_llm_turn must use `self.` —
    bare `_tool_stop_injected` would NameError because that name
    is bound in `_conversation_loop`, a different method's scope."""
    src = inspect.getsource(AgentLoop._perform_llm_turn)
    bare_refs = src.count("_tool_stop_injected")
    self_refs = src.count("self._tool_stop_injected")
    assert bare_refs > 0, "expected _tool_stop_injected references in _perform_llm_turn"
    assert bare_refs == self_refs, (
        f"_perform_llm_turn has {bare_refs} _tool_stop_injected refs "
        f"but only {self_refs} are self.-prefixed — would NameError on the rest"
    )


def test_conversation_loop_writes_self_tool_stop_injected():
    """_conversation_loop should also use the self. attribute (both for
    initialization at the top of the prompt and for read/write inside
    the loop body), so the value persists across method boundaries."""
    src = inspect.getsource(AgentLoop._conversation_loop)
    # The init line should set self._tool_stop_injected (not bare local)
    assert "self._tool_stop_injected = False" in src, (
        "_conversation_loop must init self._tool_stop_injected"
    )
    # Any remaining bare reference would be a footgun for future refactors
    # (someone moves a block out and hits NameError).
    bare = src.count("_tool_stop_injected") - src.count("self._tool_stop_injected")
    # The comment line "# Promoted to self._tool_stop_injected" contains
    # the substring once without `self.` prefix; allow that one.
    assert bare <= 1, f"unexpected {bare} bare _tool_stop_injected refs in _conversation_loop"


def test_reset_session_initializes_tool_stop_injected():
    """Defensive init in _reset_session prevents NameError if
    _perform_llm_turn is ever called before _conversation_loop's
    own init line (e.g. via a session-resume code path)."""
    src = inspect.getsource(AgentLoop._reset_session)
    assert "_tool_stop_injected" in src, (
        "_reset_session must initialize self._tool_stop_injected"
    )
