"""The first-Turn command of a Workflow start input.

Like ``send_message``, kept out of the package ``__init__``, which imports no Harness module.
"""

from pydantic import ValidationError

from mistralai.vibe.harness.runtime.genai import GenAITraceParent
from mistralai.vibe.harness.runtime.session.commands import StartTurnCommand
from mistralai.vibe.harness.runtime.session.initial_turn import InitialTurnRefusedError, build_initial_turn_command
from mistralai.vibe_agents.session_workflow.inputs import SessionWorkflowInitialTurn
from mistralai.vibe_agents.session_workflow.user_message import read_user_message


def build_start_input_turn_command(
    initial_turn: SessionWorkflowInitialTurn, *, genai_trace_parent: GenAITraceParent | None = None
) -> StartTurnCommand:
    """Return the command that starts the first Turn of a Workflow start input.

    The control plane checks a start with it and the Worker runs it, so both apply the same rules.
    Raise ``InitialTurnRefusedError`` with reason ``rejected`` if the Harness cannot read or run a block.
    """

    try:
        blocks, context_messages = read_user_message(initial_turn)
    except ValidationError as error:
        raise InitialTurnRefusedError("rejected", str(error)) from error
    # The first message has no ID of its own, so it uses the Turn ID as its message entry ID and idempotency key.
    return build_initial_turn_command(
        blocks,
        turn_id=initial_turn.turn_id,
        context_messages=context_messages,
        message_entry_id=initial_turn.turn_id,
        idempotency_key=initial_turn.turn_id,
        genai_trace_parent=genai_trace_parent,
    )


__all__ = ["build_start_input_turn_command"]
