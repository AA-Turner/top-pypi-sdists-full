"""Tests for connector plugin discovery, metadata indexing, and interceptor setup.

Covers _build_plugin_metadata_index, ConnectorAuthInterceptor, and
collect_plugin_interceptors.
"""

from __future__ import annotations

from types import ModuleType
from typing import Any
from unittest.mock import MagicMock, patch

from mistralai.workflows import workflow
from mistralai.workflows.plugins._discovery import (
    ContributionInfo,
    collect_plugin_interceptors,
)
from mistralai.workflows.plugins.mistralai.connectors import connector, uses_connectors
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    CONNECTORS_KEY,
    MISTRALAI_PLUGIN_KEY,
)
from mistralai.workflows.plugins.mistralai.connectors.interceptor import (
    ConnectorAuthInterceptor,
    _build_plugin_metadata_index,
)

# ---------------------------------------------------------------------------
# _build_plugin_metadata_index tests
# ---------------------------------------------------------------------------


class TestBuildPluginMetadataIndex:
    """Tests for _build_plugin_metadata_index."""

    def test_workflow_with_connectors(self) -> None:
        @workflow.define(name="test-index-with-connectors")
        @uses_connectors(connector("slack"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        index = _build_plugin_metadata_index([MyWorkflow])
        assert "test-index-with-connectors" in index
        connectors = index["test-index-with-connectors"][MISTRALAI_PLUGIN_KEY][CONNECTORS_KEY]
        assert len(connectors) == 1
        assert connectors[0]["connector_name"] == "slack"

    def test_workflow_without_connectors(self) -> None:
        @workflow.define(name="test-index-no-connectors")
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        index = _build_plugin_metadata_index([MyWorkflow])
        assert "test-index-no-connectors" not in index

    def test_multiple_workflows_mixed(self) -> None:
        @workflow.define(name="test-index-mixed-with")
        @uses_connectors(connector("github"))
        class WithConnectors:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        @workflow.define(name="test-index-mixed-without")
        class WithoutConnectors:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        index = _build_plugin_metadata_index([WithConnectors, WithoutConnectors])
        assert "test-index-mixed-with" in index
        assert "test-index-mixed-without" not in index

    def test_empty_workflows_list(self) -> None:
        index = _build_plugin_metadata_index([])
        assert index == {}


# ---------------------------------------------------------------------------
# ConnectorAuthInterceptor tests
# ---------------------------------------------------------------------------


class TestConnectorAuthInterceptor:
    """Tests for ConnectorAuthInterceptor metadata indexing and subclass creation."""

    def test_metadata_stored(self) -> None:
        @workflow.define(name="test-interceptor-meta")
        @uses_connectors(connector("slack"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        interceptor = ConnectorAuthInterceptor(workflows=[MyWorkflow])
        assert "test-interceptor-meta" in interceptor._metadata_by_name

    def test_workflow_interceptor_class_returns_subclass(self) -> None:
        @workflow.define(name="test-interceptor-class")
        @uses_connectors(connector("slack"))
        class MyWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        interceptor = ConnectorAuthInterceptor(workflows=[MyWorkflow])
        mock_input = MagicMock()
        cls = interceptor.workflow_interceptor_class(mock_input)
        assert cls is not None
        # The returned class should carry the metadata
        assert "test-interceptor-class" in cls._metadata_by_name

    def test_workflow_interceptor_class_metadata_isolated(self) -> None:
        """Each call creates a distinct subclass with its own metadata."""

        @workflow.define(name="test-interceptor-isolation-a")
        @uses_connectors(connector("slack"))
        class WfA:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        @workflow.define(name="test-interceptor-isolation-b")
        @uses_connectors(connector("github"))
        class WfB:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        interceptor_a = ConnectorAuthInterceptor(workflows=[WfA])
        interceptor_b = ConnectorAuthInterceptor(workflows=[WfB])

        cls_a = interceptor_a.workflow_interceptor_class(MagicMock())
        cls_b = interceptor_b.workflow_interceptor_class(MagicMock())

        assert "test-interceptor-isolation-a" in cls_a._metadata_by_name
        assert "test-interceptor-isolation-b" not in cls_a._metadata_by_name
        assert "test-interceptor-isolation-b" in cls_b._metadata_by_name
        assert "test-interceptor-isolation-a" not in cls_b._metadata_by_name


# ---------------------------------------------------------------------------
# collect_plugin_interceptors tests
# ---------------------------------------------------------------------------


class TestCollectPluginInterceptors:
    """Tests for collect_plugin_interceptors from _discovery.py."""

    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_no_plugins(self, mock_list: MagicMock) -> None:
        mock_list.return_value = []
        result = collect_plugin_interceptors([])
        assert result == []

    @patch("mistralai.workflows.plugins._discovery.importlib.import_module")
    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_plugin_with_hook(self, mock_list: MagicMock, mock_import: MagicMock) -> None:
        mock_list.return_value = [ContributionInfo("fakeplugin", True, "fakeplugin-dist", "1.0.0")]

        mock_interceptor = MagicMock()
        mock_module = ModuleType("mistralai.workflows.plugins.fakeplugin")
        mock_module.get_worker_interceptors = MagicMock(return_value=[mock_interceptor])  # type: ignore[attr-defined]
        mock_import.return_value = mock_module

        result = collect_plugin_interceptors([])
        assert len(result) == 1
        assert result[0] is mock_interceptor

    @patch("mistralai.workflows.plugins._discovery.importlib.import_module")
    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_plugin_without_hook(self, mock_list: MagicMock, mock_import: MagicMock) -> None:
        mock_list.return_value = [ContributionInfo("nohook", True, "nohook-dist", "1.0.0")]

        mock_module = ModuleType("mistralai.workflows.plugins.nohook")
        mock_import.return_value = mock_module

        result = collect_plugin_interceptors([])
        assert result == []

    @patch("mistralai.workflows.plugins._discovery.importlib.import_module")
    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_plugin_with_non_callable_hook(self, mock_list: MagicMock, mock_import: MagicMock) -> None:
        """A plugin where get_worker_interceptors exists but is not callable."""
        mock_list.return_value = [ContributionInfo("badhook", True, "badhook-dist", "1.0.0")]

        mock_module = ModuleType("mistralai.workflows.plugins.badhook")
        mock_module.get_worker_interceptors = "not a function"  # type: ignore[attr-defined]
        mock_import.return_value = mock_module

        result = collect_plugin_interceptors([])
        assert result == []

    @patch("mistralai.workflows.plugins._discovery.importlib.import_module")
    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_multiple_plugins_contribute_interceptors(self, mock_list: MagicMock, mock_import: MagicMock) -> None:
        mock_list.return_value = [
            ContributionInfo("plugin_a", True, "a-dist", "1.0.0"),
            ContributionInfo("plugin_b", True, "b-dist", "2.0.0"),
        ]

        interceptor_a = MagicMock()
        interceptor_b1 = MagicMock()
        interceptor_b2 = MagicMock()

        module_a = ModuleType("mistralai.workflows.plugins.plugin_a")
        module_a.get_worker_interceptors = MagicMock(return_value=[interceptor_a])  # type: ignore[attr-defined]

        module_b = ModuleType("mistralai.workflows.plugins.plugin_b")
        module_b.get_worker_interceptors = MagicMock(return_value=[interceptor_b1, interceptor_b2])  # type: ignore[attr-defined]

        def side_effect(name: str) -> Any:
            if "plugin_a" in name:
                return module_a
            return module_b

        mock_import.side_effect = side_effect

        result = collect_plugin_interceptors([])
        assert len(result) == 3
        assert result[0] is interceptor_a
        assert result[1] is interceptor_b1
        assert result[2] is interceptor_b2

    @patch("mistralai.workflows.plugins._discovery.importlib.import_module")
    @patch("mistralai.workflows.plugins._discovery.list_plugins")
    def test_workflows_passed_to_hook(self, mock_list: MagicMock, mock_import: MagicMock) -> None:
        """Verify that the workflows list is forwarded to the plugin hook."""
        mock_list.return_value = [ContributionInfo("myplugin", True, "my-dist", "1.0.0")]

        mock_module = ModuleType("mistralai.workflows.plugins.myplugin")
        mock_hook = MagicMock(return_value=[])
        mock_module.get_worker_interceptors = mock_hook  # type: ignore[attr-defined]
        mock_import.return_value = mock_module

        sentinel_workflows: list[type] = [type("FakeWf", (), {})]
        collect_plugin_interceptors(sentinel_workflows)
        mock_hook.assert_called_once_with(sentinel_workflows)
