# Copyright 2023 Agnostiq Inc.


"""Unit tests for Dispatch management futures module."""

from unittest.mock import MagicMock

import covalent as ct

from covalent_cloud.dispatch_management.results_manager import (
    AssetScope,
    FutureResult,
    FutureVar,
    Result,
)


class TestFutureVar:

    MOCK_DISPATCH_ID = "mock-dispatch-id"
    MOCK_TASK_ID = 1
    MOCK_NAME = "mock-name"
    MOCK_VALUE = "mock-value"

    def test_init(self):
        """Test FutureVar init method."""

        mock_result_manager = MagicMock()

        future_var = FutureVar(
            mock_result_manager,
            AssetScope.RESULT,
            self.MOCK_NAME,
            self.MOCK_DISPATCH_ID,
            self.MOCK_TASK_ID,
        )
        assert future_var._dispatch_id == self.MOCK_DISPATCH_ID
        assert future_var._task_id == self.MOCK_TASK_ID
        assert future_var._name == self.MOCK_NAME
        assert future_var._value is None
        assert future_var._downloaded is False

    def test_load_result_scope(self):
        """Test FutureVar load for a result scope asset"""
        mock_result_manager = MagicMock()

        future_var = FutureVar(
            mock_result_manager,
            AssetScope.RESULT,
            self.MOCK_NAME,
            self.MOCK_DISPATCH_ID,
            None,
        )

        future_var.load()
        mock_result_manager.download_result_asset.assert_called()
        mock_result_manager.load_result_asset.assert_called()
        mock_result_manager.load_node_asset.assert_not_called()

    def test_load_lattice_scope(self):
        """Test FutureVar load for a lattice scope asset."""
        mock_result_manager = MagicMock()

        future_var = FutureVar(
            mock_result_manager,
            AssetScope.LATTICE,
            self.MOCK_NAME,
            self.MOCK_DISPATCH_ID,
            None,
        )

        future_var.load()
        mock_result_manager.download_lattice_asset.assert_called()
        mock_result_manager.load_lattice_asset.assert_called()

    def test_load_node_scope(self):
        """Test FutureVar load for a lattice scope asset."""
        mock_result_manager = MagicMock()

        future_var = FutureVar(
            mock_result_manager,
            AssetScope.NODE,
            self.MOCK_NAME,
            self.MOCK_DISPATCH_ID,
            self.MOCK_TASK_ID,
        )

        future_var.load()
        mock_result_manager.download_node_asset.assert_called()
        mock_result_manager.load_node_asset.assert_called()


class TestFutureResult:

    MOCK_DISPATCH_ID = "mock-dispatch-id"
    MOCK_PARENT_DISPATCH_ID = "mock-parent-dispatch-id"
    MOCK_DISPATCH_NAME = "mock-dispatch-name"
    MOCK_START_TIME = "mock-start-time"
    MOCK_END_TIME = "mock-end-time"
    MOCK_STATUS = "mock-status"
    MOCK_LATTICE = "mock-lattice"
    MOCK_RESULT = "mock-result"
    MOCK_INPUTS = "mock-inputs"
    MOCK_ERROR = "mock-error"

    MOCK_TASK_ID = 1

    def test_from_result_object(self):
        """Test FutureResult attribute properties."""

        dispatch_id = "test_from_result_object"

        @ct.electron
        def task(x):
            return x**2

        @ct.lattice
        def workflow(x):
            return task(x)

        workflow.build_graph(2)
        res = Result(workflow, dispatch_id)

        fr = FutureResult._from_result_object(res)
        assert fr.__dict__ == res.__dict__
