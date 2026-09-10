from agentic_devtools.cli.ci.guards import _page_parts


def test_extracts_tasks_and_explicit_end_from_valid_page() -> None:
    tasks, explicit_end, invalid = _page_parts({"tasks": [{"id": 1}], "has_more": False})

    assert tasks == [{"id": 1}]
    assert explicit_end is True
    assert invalid is False


def test_marks_conflicting_continuation_aliases_invalid() -> None:
    _tasks, _explicit_end, invalid = _page_parts({"tasks": [], "next": None, "next_token": "page-2"})

    assert invalid is True


def test_marks_conflicting_task_container_aliases_invalid() -> None:
    _tasks, _explicit_end, invalid = _page_parts({"tasks": [], "items": [{"id": 1}], "has_more": False})

    assert invalid is True


def test_marks_missing_or_unrecognized_task_containers_invalid() -> None:
    for page in ({"has_more": False}, {"data": {"unexpected": []}, "has_more": False}):
        _tasks, _explicit_end, invalid = _page_parts(page)

        assert invalid is True


def test_marks_conflicting_nested_task_containers_invalid() -> None:
    _tasks, _explicit_end, invalid = _page_parts({"data": {"tasks": [], "items": [{"id": 1}]}, "has_more": False})

    assert invalid is True


def test_marks_type_collapsing_top_level_task_aliases_invalid() -> None:
    _tasks, _explicit_end, invalid = _page_parts(
        {
            "tasks": [{"pull_request_id": 1}],
            "items": [{"pull_request_id": True}],
            "has_more": False,
        }
    )

    assert invalid is True


def test_marks_type_collapsing_nested_task_aliases_invalid() -> None:
    _tasks, _explicit_end, invalid = _page_parts(
        {
            "data": {
                "tasks": [{"pull_request_id": 1}],
                "items": [{"pull_request_id": True}],
            },
            "has_more": False,
        }
    )

    assert invalid is True
