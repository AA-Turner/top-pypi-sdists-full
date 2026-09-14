from collections.abc import Callable

import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.review_orchestration import Finding, Reservation
from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingHandoff, finding_payload_digest


@pytest.fixture
def handoff_data() -> dict[str, object]:
    finding = Finding(
        review_id=1,
        reviewer_id=2,
        comment_id=3,
        suppressed_body=None,
        thread_id="thread-1",
        path="src/example.py",
        side="RIGHT",
        supporting_files=(),
        side_effects=("branch-write",),
        status="reserved",
        attempt_id="attempt-1",
        task_id=None,
        session_id=None,
    )
    finding_id = finding.identity("https://github.com/example/project/pull/7")
    payload = AgentTasksPayload(
        prompt="repair one finding",
        model="gpt-5.6-luna",
        base_ref="main",
        head_ref="feature",
        custom_agent="agdt.address-copilot-review.evaluate-and-respond",
        create_pull_request=False,
    )
    return {
        "run_id": "00000000-0000-4000-8000-000000000001",
        "pr_url": "https://github.com/example/project/pull/7",
        "base_ref": "main",
        "head_ref": "feature",
        "expected_head": "a" * 40,
        "finding_id": finding_id,
        "payload_digest": finding_payload_digest(finding_id, payload),
        "attempt_id": "attempt-1",
        "deadline_at": 200,
        "reservation": {
            "finding_id": finding_id,
            "attempt_id": "attempt-1",
            "head_sha": "a" * 40,
            "resources": ["effect:branch-write", "file:src/example.py"],
        },
        "finding": finding.model_dump(),
        "authorized_actions": ["repair"],
        "remaining_failure_budgets": {
            "throttling": 3,
            "transport": 3,
            "credential": 1,
            "oauth": 1,
            "repair": 2,
        },
    }


@pytest.fixture
def handoff(handoff_data: dict[str, object]) -> SingleFindingHandoff:
    return SingleFindingHandoff.model_validate(handoff_data)


@pytest.fixture
def payload():
    from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload

    return AgentTasksPayload(
        prompt="repair one finding",
        model="gpt-5.6-luna",
        base_ref="main",
        head_ref="feature",
        custom_agent="agdt.address-copilot-review.evaluate-and-respond",
        create_pull_request=False,
    )


class FakeHost:
    def __init__(
        self,
        *,
        reservation_result: bool = True,
        acceptance=None,
        persistence_result: bool = True,
    ) -> None:
        self.reservation_result = reservation_result
        self.acceptance = acceptance
        self.persistence_result = persistence_result
        self.calls: list[tuple[str, object]] = []
        self.timeouts: list[tuple[str, int]] = []

    def reserve_branch_write(self, value: SingleFindingHandoff, timeout_seconds: int) -> bool:
        self.calls.append(("reserve", value))
        self.timeouts.append(("reserve", timeout_seconds))
        return self.reservation_result

    def create_task_if_head(self, handoff: SingleFindingHandoff, payload, timeout_seconds: int):
        self.calls.append(("create", (handoff, payload)))
        self.timeouts.append(("create", timeout_seconds))
        if isinstance(self.acceptance, Exception):
            raise self.acceptance
        return self.acceptance

    def persist_acceptance(self, handoff: SingleFindingHandoff, acceptance, timeout_seconds: int) -> bool:
        self.calls.append(("persist", (handoff, acceptance)))
        self.timeouts.append(("persist", timeout_seconds))
        return self.persistence_result


@pytest.fixture
def fake_host() -> Callable[..., FakeHost]:
    return FakeHost


@pytest.fixture
def reservation(handoff_data: dict[str, object]) -> Reservation:
    return Reservation.model_validate(handoff_data["reservation"])
