from agentic_devtools.ai_providers import copilot as copilot_module


def test_normalize_task_state_maps_known_aliases() -> None:
    assert copilot_module._normalize_task_state("requested") == "queued"
    assert copilot_module._normalize_task_state("waiting") == "waiting_for_user"
    assert copilot_module._normalize_task_state("running") == "in_progress"


def test_normalize_task_state_preserves_non_alias_values() -> None:
    assert copilot_module._normalize_task_state("completed") == "completed"
    assert copilot_module._normalize_task_state("") == ""
    assert copilot_module._normalize_task_state(42) == 42
