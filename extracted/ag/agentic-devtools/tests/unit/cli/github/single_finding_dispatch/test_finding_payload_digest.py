import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.single_finding_dispatch import finding_payload_digest


def test_finding_payload_digest_is_canonical(payload):
    assert (
        finding_payload_digest("b" * 64, payload) == "b659288f452eb8c129dbf90643f456236bb39cd7617510409692c6a7adf43f69"
    )


@pytest.mark.parametrize(
    ("finding_id", "payload", "error"),
    [
        (
            "not-a-finding",
            AgentTasksPayload(
                prompt="repair one finding",
                model="gpt-5.6-luna",
                base_ref="main",
                head_ref="feature",
                custom_agent="agdt.address-copilot-review.evaluate-and-respond",
                create_pull_request=False,
            ),
            "finding_id",
        ),
        ("b" * 64, object(), "AgentTasksPayload"),
    ],
)
def test_finding_payload_digest_validates_inputs(finding_id, payload, error):
    with pytest.raises((TypeError, ValueError), match=error):
        finding_payload_digest(finding_id, payload)
