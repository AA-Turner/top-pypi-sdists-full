"""Synthetic, provider-free orchestration records."""

import pytest

from agentic_devtools.cli.github.review_orchestration import Finding


@pytest.fixture
def finding_data():
    return {
        "review_id": 17,
        "reviewer_id": 42,
        "comment_id": 23,
        "suppressed_body": None,
        "thread_id": "PRRT_example",
        "path": "src/example.py",
        "side": "RIGHT",
        "supporting_files": ["tests/test_example.py"],
        "side_effects": ["branch-write"],
        "status": "pending",
        "attempt_id": None,
        "task_id": None,
        "session_id": None,
    }


@pytest.fixture
def state_data(finding_data):
    return {
        "schema_version": 1,
        "run_id": "00000000-0000-4000-8000-000000000001",
        "pr_url": "https://github.com/example/project/pull/7",
        "expected_reviewer_id": 42,
        "authorized_actions": ["repair"],
        "started_at": 1000,
        "deadline_at": 4600,
        "next_due_at": 1000,
        "max_cycles": 12,
        "cycles": 0,
        "max_parallel": 2,
        "status": "waiting",
        "evidence": {
            "head_sha": "a" * 40,
            "fingerprint": "b" * 64,
            "reviewed_head_sha": "a" * 40,
            "review_id": 17,
            "reviewer_id": 42,
            "reviews": "complete",
            "threads": "complete",
            "checks": "complete",
            "tasks": "complete",
        },
        "findings": [finding_data],
        "reservations": [],
        "failures": {"throttling": 0, "transport": 0, "credential": 0, "oauth": 0, "repair": 0},
        "review_requested_head": None,
    }


@pytest.fixture
def reserve(state_data):
    def apply(status="accepted"):
        finding = state_data["findings"][0]
        finding.update(status=status, attempt_id="attempt-1", task_id="task-1", session_id="session-1")
        parsed = Finding.model_validate(finding)
        state_data["reservations"] = [
            {
                "finding_id": parsed.identity(state_data["pr_url"]),
                "attempt_id": "attempt-1",
                "head_sha": "a" * 40,
                "resources": sorted(parsed.resources()),
            }
        ]
        return state_data

    return apply
