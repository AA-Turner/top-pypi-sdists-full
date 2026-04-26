from pathlib import Path

from anteroom.services.memory_save_status import format_memory_save_result


def test_active_memory_status_is_confident_and_recallable() -> None:
    msg = format_memory_save_result(
        {
            "fqn": "@user/memory/pref-123",
            "memory_status": "active",
            "category": "preference",
            "scope": "user",
        },
        data_dir=Path.home() / ".anteroom",
    )

    assert "active memory" in msg.text
    assert "eligible for recall" in msg.text
    assert "FQN: @user/memory/pref-123" in msg.text
    assert "may" not in msg.text.lower()
    assert msg.metadata["memory_save"]["recallable"] is True
    assert msg.metadata["memory_save"]["review_required"] is False
    assert msg.metadata["memory_save"]["storage"] == "~/.anteroom"


def test_candidate_memory_status_is_confident_and_not_recallable() -> None:
    msg = format_memory_save_result(
        {"fqn": "@user/memory/pref-456", "memory_status": "candidate", "category": "preference", "scope": "user"},
        data_dir="/tmp/anteroom",
    )

    assert "memory candidate" in msg.text
    assert "not active or recallable until approved" in msg.text
    assert "FQN: @user/memory/pref-456" in msg.text
    assert "may" not in msg.text.lower()
    assert msg.metadata["memory_save"]["recallable"] is False
    assert msg.metadata["memory_save"]["review_required"] is True


def test_pending_review_memory_status_is_not_recallable() -> None:
    msg = format_memory_save_result({"memory_status": "pending_review"}, data_dir=None)

    assert "pending-review item" in msg.text
    assert "not active or recallable until approved" in msg.text
    assert "FQN:" not in msg.text
    assert msg.metadata["memory_save"]["review_required"] is True


def test_inactive_terminal_statuses_are_not_recallable() -> None:
    msg = format_memory_save_result({"fqn": "@user/memory/x", "memory_status": "archived"}, data_dir=None)

    assert "status 'archived'" in msg.text
    assert "not active or recallable" in msg.text
    assert msg.metadata["memory_save"]["recallable"] is False


def test_error_result_preserves_failure_text_without_storage_claim() -> None:
    msg = format_memory_save_result({"error": "denied"}, data_dir="/tmp/anteroom")

    assert msg.text == "Memory save failed: denied"
    assert msg.metadata == {"memory_save": {"error": "denied"}}
