# Copyright 2023 Agnostiq Inc.

"""Unit tests for dispatching and related interface functions."""

from unittest.mock import MagicMock

import covalent as ct
import pytest

from covalent_cloud.dispatch_management.interface_functions import cancel, dispatch, get_result
from covalent_cloud.dispatch_management.results_manager import Result
from covalent_cloud.shared.classes.settings import Settings

COVALENT_CLOUD_URL = "http://localhost:48008"
MOCK_DISPATCH_ID = "mock-dispatch-id"
MOCK_STATUS = "mock-status"
MOCK_ARGS = [1, 2]
MOCK_KWARGS = {"a": 1, "b": 2}
MOCK_TASKS_LIST = ["task1", "task2"]
MOCK_COMPRESSED_TRANSPORTABLE_DATA = "mock-compressed-transportable-data"


def test_dispatch(mocker):
    """Test the workflow dispatching interface function."""

    @ct.lattice(executor="cloud", workflow_executor="cloud")
    @ct.electron(executor="cloud")
    def test_workflow(a, b):
        return a + b

    mock_dispatch_id = "mock-dispatch-id"
    mock_wrapper = MagicMock(return_value=mock_dispatch_id)
    mock_register = mocker.patch(
        "covalent_cloud.dispatch_management.interface_functions.register",
        return_value=mock_wrapper,
    )

    mock_start = mocker.patch(
        "covalent_cloud.dispatch_management.interface_functions.start",
        return_value=mock_dispatch_id,
    )
    default_settings = Settings()

    dispatch_id = dispatch(test_workflow)(2, 3)

    assert dispatch_id == "mock-dispatch-id"
    mock_register.assert_called()
    mock_start.assert_called_with(dispatch_id, default_settings)


@pytest.mark.parametrize("status_only", [True, False])
def test_get_result(mocker, status_only):
    """Test the workflow result retrieval interface function."""

    @ct.electron
    def task(x):
        return x**2

    @ct.lattice
    def workflow(x):
        return task(x)

    workflow.build_graph(3)
    dispatch_id = f"test_get_result_{status_only}"
    res_obj = Result(workflow, dispatch_id)
    res_obj._initialize_nodes()

    mock_fr = MagicMock()
    mock_rm = MagicMock()
    mock_rm.result_object = res_obj

    mock_get_from_dispatcher = mocker.patch(
        "covalent_cloud.dispatch_management.results_manager._get_result_export_from_dispatcher",
        return_value={"id": dispatch_id, "status": "RUNNING", "result_export": "result"},
    )

    mock_get_rm = mocker.patch(
        "covalent_cloud.dispatch_management.results_manager.get_result_manager",
        return_value=mock_rm,
    )

    mock_from_result_object = mocker.patch(
        "covalent_cloud.dispatch_management.results_manager.FutureResult._from_result_object",
        return_value=mock_fr,
    )

    result = get_result(dispatch_id=dispatch_id, status_only=status_only)
    if status_only:
        mock_get_from_dispatcher.assert_called_once()
        mock_get_rm.assert_not_called()
    else:
        mock_get_rm.assert_called()
        mock_rm._populate_result_object.assert_called()
        assert result == mock_fr
        mock_from_result_object.assert_called_with(res_obj)


@pytest.mark.parametrize(
    "input_task_ids, expected_task_ids",
    [
        (None, []),
        (1, [1]),
        ([1, 2, 3], [1, 2, 3]),
    ],
)
def test_cancel(mocker, input_task_ids, expected_task_ids):
    """Test the workflow cancellation interface function."""

    mock_get_client = mocker.patch(
        "covalent_cloud.dispatch_management.interface_functions.get_client"
    )

    dispatch_id = "test_dispatch_id"
    cancel(dispatch_id=dispatch_id, task_ids=input_task_ids)

    mock_get_client.assert_called_once()

    mock_get_client().put.assert_called_once_with(
        f"api/v2/lattices/{dispatch_id}/cancel",
        request_options={"params": {"task_ids": expected_task_ids}},
    )
