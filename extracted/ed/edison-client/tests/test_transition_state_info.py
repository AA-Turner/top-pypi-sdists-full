"""Verify that message info (is_human, reference_context) survives TransitionState serialization.

The committed fixture at crow-ui/test/data/transition-with-preamble.json is consumed
by a Jest test that runs the real useMessageCollection hook to verify frontend filtering.
To regenerate the fixture after changes, run:
    uv run python -m edison_client.tests.test_transition_state_info --regenerate
"""

import json
from pathlib import Path

from aviary.core import Message
from ldp.agent.simple_agent import SimpleAgentState
from ldp.data_structures import Transition

from edison_client.models.client import TransitionState

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "crow-ui"
    / "test"
    / "data"
    / "transition-with-preamble.json"
)


def _build_transition_state() -> TransitionState:
    preamble = Message(
        role="user",
        content="## e14c Code Reference\nYour environment includes the e14c library...",
        info={"is_human": False, "reference_context": True},
    )
    human_msg = Message(role="user", content="What proteins interact with p53?")
    assistant_msg = Message(role="assistant", content="Let me investigate that.")

    return TransitionState(
        transition=Transition(
            timestep=0,
            agent_state=SimpleAgentState(),
            next_agent_state=SimpleAgentState(
                messages=[preamble, human_msg, assistant_msg]
            ),
            observation=[],
            next_observation=[],
        )
    )


def test_serialization_preserves_info():
    state = _build_transition_state()
    data = state.model_dump(mode="json", context={"include_info": True})

    msgs = data["transition"]["next_agent_state"]["messages"]
    assert msgs[0]["info"] == {"is_human": False, "reference_context": True}
    assert msgs[0]["content"].startswith("## e14c Code Reference")
    assert msgs[1]["info"] is None
    assert msgs[2]["info"] is None


def test_serialized_output_matches_committed_fixture():
    state = _build_transition_state()
    data = state.model_dump(mode="json", context={"include_info": True})
    fixture = {"agent_state": [{"state": data}]}

    committed = json.loads(FIXTURE_PATH.read_text())
    assert fixture == committed, (
        "Serialization output differs from committed fixture. "
        f"Regenerate with: uv run python {Path(__file__)}"
    )


if __name__ == "__main__":
    _state = _build_transition_state()
    _data = _state.model_dump(mode="json", context={"include_info": True})
    _fixture = {"agent_state": [{"state": _data}]}
    FIXTURE_PATH.write_text(json.dumps(_fixture, indent=2) + "\n")
    print(f"Wrote fixture to {FIXTURE_PATH}")
