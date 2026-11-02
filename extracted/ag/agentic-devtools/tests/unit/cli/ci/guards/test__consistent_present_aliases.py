from agentic_devtools.cli.ci import guards as guards_module


def test_returns_none_value_or_conflict_for_present_aliases() -> None:
    assert guards_module._consistent_present_aliases({}, ("id", "task_id")) is None
    assert guards_module._consistent_present_aliases({"id": 7}, ("id", "task_id")) == 7
    assert guards_module._consistent_present_aliases({"id": 7, "task_id": 7}, ("id", "task_id")) == 7
    assert guards_module._consistent_present_aliases({"id": 1, "task_id": True}, ("id", "task_id")) is (
        guards_module._ALIAS_CONFLICT
    )


def test_detects_type_collapsing_conflicts_in_nested_alias_values() -> None:
    assert (
        guards_module._consistent_present_aliases(
            {"tasks": [{"pull_request_id": 1}], "items": [{"pull_request_id": True}]},
            ("tasks", "items"),
        )
        is guards_module._ALIAS_CONFLICT
    )

    assert guards_module._consistent_present_aliases(
        {"tasks": [{"pull_request_id": 1}], "items": [{"pull_request_id": 1}]},
        ("tasks", "items"),
    ) == [{"pull_request_id": 1}]

    assert (
        guards_module._consistent_present_aliases(
            {"tasks": {"pull_request_id": 1}, "items": {"task_id": 1}},
            ("tasks", "items"),
        )
        is guards_module._ALIAS_CONFLICT
    )
