"""Unit tests for keeping a task's structured-output contract on the root manager.

A gateway-dispatched child runs under a task-level JSON envelope. When that child
is an agno team, the override must land on the root manager only: members report
prose upward and the root renders the envelope once. Applying it to every member
makes each one write the full answer into the schema before the root does it
again, roughly tripling generation on the final leg.

Pure unit tests — no LLM calls, no network. Stubs duck-type the few attributes
``_configure_output`` reads.
"""

from __future__ import annotations

from types import SimpleNamespace

from xpander_sdk.models.shared import OutputFormat
from xpander_sdk.modules.backend.frameworks.agno import _configure_output

ENVELOPE = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "short_summary": {"type": "string"},
        "final_result": {"type": "string"},
    },
    "required": ["title", "short_summary", "final_result"],
}

OWN_SCHEMA = object()  # sentinel: the agent's own prebuilt output model


def _agent(output_format, *, use_json_mode=False, output_schema=None):
    return SimpleNamespace(
        output_format=output_format,
        output=SimpleNamespace(
            use_json_mode=use_json_mode,
            output_schema=output_schema,
            is_markdown=output_format == OutputFormat.Markdown,
        ),
    )


def _task(output_format=OutputFormat.Json, output_schema=ENVELOPE):
    return SimpleNamespace(output_format=output_format, output_schema=output_schema)


def test_root_wears_the_task_envelope():
    args: dict = {}
    _configure_output(args=args, agent=_agent(OutputFormat.Markdown), task=_task())

    assert args["use_json_mode"] is True
    assert args["markdown"] is False
    assert args["output_schema"] is not None


def test_member_keeps_markdown_and_no_schema():
    args: dict = {}
    _configure_output(
        args=args, agent=_agent(OutputFormat.Markdown), task=_task(), is_member=True
    )

    assert args["markdown"] is True
    assert args.get("use_json_mode") is not True
    assert "output_schema" not in args


def test_member_with_its_own_json_config_keeps_its_own_schema():
    """A member configured for JSON output stays JSON — on ITS schema, not the task's."""
    args: dict = {}
    _configure_output(
        args=args,
        agent=_agent(OutputFormat.Json, use_json_mode=True, output_schema=OWN_SCHEMA),
        task=_task(),
        is_member=True,
    )

    assert args["use_json_mode"] is True
    assert args["output_schema"] is OWN_SCHEMA


def test_member_voice_output_is_untouched():
    args: dict = {}
    _configure_output(
        args=args, agent=_agent(OutputFormat.Voice), task=_task(), is_member=True
    )

    assert args == {"use_json_mode": False, "markdown": False}


def test_root_default_is_still_the_root():
    """Omitting is_member must behave exactly like the root manager."""
    root_args: dict = {}
    explicit_args: dict = {}
    _configure_output(args=root_args, agent=_agent(OutputFormat.Markdown), task=_task())
    _configure_output(
        args=explicit_args,
        agent=_agent(OutputFormat.Markdown),
        task=_task(),
        is_member=False,
    )

    assert root_args.keys() == explicit_args.keys()
    assert root_args["use_json_mode"] == explicit_args["use_json_mode"] is True
