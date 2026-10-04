"""Every run built from an agent definition carries the agent's tool policy on its config.

THE GAP (independent review, 2026-10-03): a responder turn (a Holder answering an SMS thread,
a chosen responder on a mirrored session) rebuilt its config from the responder's definition
with no policy stamped, so the host funnel saw "switch on, nothing forbidden" every turn.
``AgentConfig`` now stamps ``auto_tools_disabled`` / ``excluded_tools`` onto ``config`` at
construction, so every path that loads a definition carries them (TOOL-SOURCES.md rule R).
"""

from __future__ import annotations

from copy import deepcopy

from matrx_ai.agents.types import AgentConfig
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig


def test_the_switch_and_the_forbidden_list_ride_the_config() -> None:
    cfg = AgentConfig(
        name="Text Holder",
        config=UnifiedConfig(model="m", messages=MessageList(_messages=[])),
        variable_defaults={},
        excluded_tools=["cloud_browser"],
        auto_tools_disabled=True,
    )
    # A responder turn deep-copies the definition's config.
    responder_config = deepcopy(cfg.config)
    assert responder_config.agent_auto_tools_disabled is True
    assert responder_config.agent_excluded_tools == ["cloud_browser"]
