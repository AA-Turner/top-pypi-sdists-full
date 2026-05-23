import unittest
from unittest.mock import MagicMock

import pytest

from abstra_internals.controllers.tasks import DataRequest, TasksController


def _make_controller():
    controller = MagicMock()
    controller.list_tasks = TasksController.list_tasks.__get__(controller)
    return controller


class TestListTasks(unittest.TestCase):
    def test_no_stage_returns_paginated_all_tasks(self):
        controller = _make_controller()
        items = [MagicMock(name="t1"), MagicMock(name="t2")]
        controller._list_all_tasks.return_value = (items, 42)

        result = controller.list_tasks(limit=5, offset=10)

        controller._list_tasks_sent_to_stage.assert_not_called()
        controller._list_tasks_sent_by_stage.assert_not_called()
        controller._list_all_tasks.assert_called_once()
        passed_req: DataRequest = controller._list_all_tasks.call_args[0][0]
        self.assertEqual(passed_req.limit, 5)
        self.assertEqual(passed_req.offset, 10)
        self.assertIsNone(passed_req.filter.stage)
        self.assertIsNone(passed_req.filter.status)
        self.assertEqual(result, {"tasks": items, "total": 42})

    def test_stage_with_sent_to_dispatches_to_helper(self):
        controller = _make_controller()
        items = [MagicMock(name="t1"), MagicMock(name="t2"), MagicMock(name="t3")]
        controller._list_tasks_sent_to_stage.return_value = items

        result = controller.list_tasks(stage_ids=["stage-1"], direction="sent_to")

        controller._list_tasks_sent_to_stage.assert_called_once_with("stage-1")
        controller._list_tasks_sent_by_stage.assert_not_called()
        controller._list_all_tasks.assert_not_called()
        self.assertEqual(result, {"tasks": items, "total": 3})

    def test_stage_with_sent_by_dispatches_to_helper(self):
        controller = _make_controller()
        items = [MagicMock(name="t1")]
        controller._list_tasks_sent_by_stage.return_value = items

        result = controller.list_tasks(stage_ids=["stage-2"], direction="sent_by")

        controller._list_tasks_sent_by_stage.assert_called_once_with("stage-2")
        controller._list_tasks_sent_to_stage.assert_not_called()
        controller._list_all_tasks.assert_not_called()
        self.assertEqual(result, {"tasks": items, "total": 1})

    def test_stage_ids_without_direction_filters_via_all_tasks_helper(self):
        controller = _make_controller()
        controller._list_all_tasks.return_value = ([], 0)

        controller.list_tasks(stage_ids=["stage-3"])

        controller._list_all_tasks.assert_called_once()
        passed_req: DataRequest = controller._list_all_tasks.call_args[0][0]
        self.assertEqual(passed_req.filter.stage, ["stage-3"])
        controller._list_tasks_sent_to_stage.assert_not_called()
        controller._list_tasks_sent_by_stage.assert_not_called()

    def test_multiple_stage_ids_filter_all_tasks(self):
        controller = _make_controller()
        controller._list_all_tasks.return_value = ([], 0)

        controller.list_tasks(stage_ids=["stage-a", "stage-b"])

        passed_req: DataRequest = controller._list_all_tasks.call_args[0][0]
        self.assertEqual(passed_req.filter.stage, ["stage-a", "stage-b"])

    def test_status_and_dates_propagate_to_all_tasks_helper(self):
        controller = _make_controller()
        controller._list_all_tasks.return_value = ([], 0)

        controller.list_tasks(
            status=["pending", "locked"],
            start_date="2026-01-01",
            end_date="2026-12-31",
        )

        passed_req: DataRequest = controller._list_all_tasks.call_args[0][0]
        self.assertEqual(passed_req.filter.status, ["pending", "locked"])
        self.assertEqual(passed_req.filter.start_date, "2026-01-01")
        self.assertEqual(passed_req.filter.end_date, "2026-12-31")

    def test_direction_without_stage_ids_raises(self):
        controller = _make_controller()

        with pytest.raises(ValueError, match="exactly one stage"):
            controller.list_tasks(direction="sent_to")

    def test_direction_with_multiple_stages_raises(self):
        controller = _make_controller()

        with pytest.raises(ValueError, match="exactly one stage"):
            controller.list_tasks(stage_ids=["a", "b"], direction="sent_to")


if __name__ == "__main__":
    unittest.main()
