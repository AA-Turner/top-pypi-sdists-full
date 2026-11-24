"""A tool that listens to its own streamed arguments gets them as the model writes them.

Live walk 2026-11-17: the Conductor's build showed nothing for ~70 s, then every step at once. The
Messages API buffers a tool's input by default and releases it in one burst; the proposer
(``tools/partial_args.py``) only hears what arrives, so its "proposed" steps arrived together.
``eager_input_streaming`` on the tool turns the buffering off — only for tools that listen.
"""

from __future__ import annotations

from matrx_ai.providers.anthropic.translator import with_eager_input_streaming
from matrx_ai.tools.partial_args import PartialArgsSpec, register_partial_args, unregister_partial_args


def test_only_a_listening_tool_streams_eagerly():
    register_partial_args("listening_tool", PartialArgsSpec(arrays=("nodes",)), lambda call: None)
    try:
        out = with_eager_input_streaming(
            [
                {"name": "listening_tool", "description": "", "input_schema": {"type": "object"}},
                {"name": "quiet_tool", "description": "", "input_schema": {"type": "object"}},
                {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},
            ]
        )
    finally:
        unregister_partial_args("listening_tool")
    assert out[0]["eager_input_streaming"] is True
    assert "eager_input_streaming" not in out[1]
    assert "eager_input_streaming" not in out[2]  # a server tool never carries it
