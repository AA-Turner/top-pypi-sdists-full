"""Test an agent without a real model: ``agents.testing.ScriptedModel`` answers each model call in order.

``import mistralai.agents.testing`` and ``from mistralai.agents.testing import ScriptedModel`` work, as for
``mistralai.agents.experimental``; ``agents.testing`` is this module.
"""

# Unlike `pattern` and `redaction`, no Temporal passthrough or log quieting: these names import no
# `mistralai.workflows` module and no Temporal.
from mistralai.vibe_agents.sdk.testing import ReplyStep as ReplyStep
from mistralai.vibe_agents.sdk.testing import ScriptedModel, call, reply
from mistralai.vibe_agents.sdk.testing import ToolCallStep as ToolCallStep

__all__ = ["ScriptedModel", "call", "reply"]
