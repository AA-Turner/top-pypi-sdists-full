"""Tests for build_review_graph()."""

from __future__ import annotations

import builtins
import importlib
from unittest.mock import patch

import pytest
from langgraph.graph.state import CompiledStateGraph

from agentic_devtools.orchestration.review import graph as graph_module
from agentic_devtools.orchestration.review.graph import (
    _load_real_nodes,
    _stub_fetch_pr_details,
    _stub_post_results,
    _stub_review_files,
    _stub_scaffold_comments,
    _stub_source_context,
    _stub_summarize_and_decide,
    build_review_graph,
)


class TestBuildReviewGraph:
    """Tests for the graph construction helper."""

    def test_returns_compiled_state_graph(self) -> None:
        """build_review_graph() returns a CompiledStateGraph."""
        compiled = build_review_graph()
        assert isinstance(compiled, CompiledStateGraph)

    def test_graph_contains_all_expected_nodes(self) -> None:
        """The graph contains all expected node names."""
        compiled = build_review_graph()
        node_names = set(compiled.get_graph().nodes.keys())
        expected = {
            "__start__",
            "__end__",
            "fetch_pr_details",
            "source_context",
            "scaffold_comments",
            "review_files",
            "summarize_and_decide",
            "post_results",
        }
        assert expected == node_names

    def test_graph_edge_ordering(self) -> None:
        """Nodes are connected in the correct order."""
        compiled = build_review_graph()
        edges = [(edge.source, edge.target) for edge in compiled.get_graph().edges]

        assert ("__start__", "fetch_pr_details") in edges
        # fetch_pr_details always routes to source_context (unconditional edge)
        assert ("fetch_pr_details", "source_context") in edges
        assert ("source_context", "scaffold_comments") in edges
        assert ("scaffold_comments", "review_files") in edges
        assert ("review_files", "summarize_and_decide") in edges
        assert ("summarize_and_decide", "post_results") in edges
        assert ("post_results", "__end__") in edges

    def test_graph_fetch_does_not_have_direct_edge_to_scaffold(self) -> None:
        """fetch_pr_details no longer has a direct edge to scaffold_comments."""
        compiled = build_review_graph()
        edges = [(edge.source, edge.target) for edge in compiled.get_graph().edges]
        assert ("fetch_pr_details", "scaffold_comments") not in edges

    def test_graph_preserves_llm_config_path_channel(self) -> None:
        """Declared llm_config_path reaches nodes in the compiled graph state."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        captured: dict[str, object] = {}

        def capture_fetch(state: dict[str, object]) -> dict[str, object]:
            captured["llm_config_path"] = state.get("llm_config_path")
            return {}

        try:
            graph_module._NODE_REGISTRY.update(
                {
                    "fetch_pr_details": capture_fetch,
                    "source_context": _stub_source_context,
                    "scaffold_comments": _stub_scaffold_comments,
                    "review_files": _stub_review_files,
                    "summarize_and_decide": _stub_summarize_and_decide,
                    "post_results": _stub_post_results,
                }
            )
            with patch.object(graph_module, "_load_real_nodes"):
                compiled = build_review_graph()
                compiled.invoke(
                    {
                        "pr_id": 123,
                        "files": [],
                        "threads": [],
                        "config": {},
                        "file_results": [],
                        "errors": [],
                        "llm_config_path": "/repo/.agdt/config/llm-providers.yml",
                    }
                )
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

        assert captured["llm_config_path"] == "/repo/.agdt/config/llm-providers.yml"

    def test_stub_nodes_return_expected_shapes(self) -> None:
        """Fallback stubs preserve the expected node output shapes."""
        assert _stub_fetch_pr_details({}) == {}
        assert _stub_source_context({}) == {}
        assert _stub_scaffold_comments({}) == {}
        assert _stub_review_files({}) == {"file_results": []}
        assert _stub_summarize_and_decide({}) == {}
        assert _stub_post_results({}) == {}

    def test_load_real_nodes_tolerates_module_not_found_errors(self) -> None:
        """Missing optional-dependency modules leave the existing registry entries unchanged."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            blocked = (
                "fetch_pr_details",
                "source_context",
                "scaffold_comments",
                "review_files",
                "summarize_and_decide",
                "post_results",
            )
            if any(target in name for target in blocked):
                # Simulate langgraph being the missing optional dep so
                # exc.name is set to the known optional package name.
                err = ModuleNotFoundError("No module named 'langgraph'")
                err.name = "langgraph"
                raise err
            return original_import(name, globals, locals, fromlist, level)

        try:
            with patch.object(builtins, "__import__", side_effect=fake_import):
                _load_real_nodes()
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

        assert graph_module._NODE_REGISTRY == original_registry

    def test_load_real_nodes_propagates_non_module_not_found_import_errors(self) -> None:
        """ImportError that is not ModuleNotFoundError propagates instead of being swallowed."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if "fetch_pr_details" in name:
                # Simulate a missing name inside an installed module (not ModuleNotFoundError)
                raise ImportError("cannot import name 'fetch_pr_details_node'")
            return original_import(name, globals, locals, fromlist, level)

        try:
            with patch.object(builtins, "__import__", side_effect=fake_import):
                with pytest.raises(ImportError, match="cannot import name"):
                    _load_real_nodes()
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

    def test_load_real_nodes_propagates_transitive_dep_module_not_found(self) -> None:
        """ModuleNotFoundError for a non-optional transitive dep propagates."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if "fetch_pr_details" in name:
                # Simulate a transitive dependency of a node module being absent.
                err = ModuleNotFoundError("No module named 'some_transitive_dep'")
                err.name = "some_transitive_dep"
                raise err
            return original_import(name, globals, locals, fromlist, level)

        try:
            with patch.object(builtins, "__import__", side_effect=fake_import):
                with pytest.raises(ModuleNotFoundError, match="some_transitive_dep"):
                    _load_real_nodes()
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

    @pytest.mark.parametrize(
        "node_name",
        ["source_context", "scaffold_comments", "review_files", "summarize_and_decide", "post_results"],
    )
    def test_load_real_nodes_propagates_transitive_dep_for_each_node(self, node_name: str) -> None:
        """Transitive-dep re-raise path is exercised for each of the four nodes after fetch_pr_details."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            # Allow fetch_pr_details to succeed so we reach the targeted node.
            if node_name in name:
                err = ModuleNotFoundError("No module named 'some_transitive_dep'")
                err.name = "some_transitive_dep"
                raise err
            return original_import(name, globals, locals, fromlist, level)

        try:
            with patch.object(builtins, "__import__", side_effect=fake_import):
                with pytest.raises(ModuleNotFoundError, match="some_transitive_dep"):
                    _load_real_nodes()
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

    def test_provider_factory_is_bound_via_closure_not_state(self) -> None:
        """Factory injected into build_review_graph is bound to the node via closure, not state."""
        original_registry = graph_module._NODE_REGISTRY.copy()
        captured_factory: list[object] = []

        def capture_review_files(state: dict[str, object], *, provider_factory: object = None) -> dict[str, object]:
            captured_factory.append(provider_factory)
            return {"file_results": []}

        sentinel_factory = object()

        try:
            graph_module._NODE_REGISTRY.update(
                {
                    "fetch_pr_details": _stub_fetch_pr_details,
                    "source_context": _stub_source_context,
                    "scaffold_comments": _stub_scaffold_comments,
                    "review_files": capture_review_files,
                    "summarize_and_decide": _stub_summarize_and_decide,
                    "post_results": _stub_post_results,
                }
            )
            with patch.object(graph_module, "_load_real_nodes"):
                compiled = build_review_graph(provider_factory=sentinel_factory)
                result = compiled.invoke(
                    {
                        "pr_id": 1,
                        "files": [],
                        "threads": [],
                        "config": {},
                        "file_results": [],
                        "errors": [],
                    }
                )
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

        assert len(captured_factory) == 1
        assert captured_factory[0] is sentinel_factory
        assert "_provider_factory" not in result

    def test_graph_without_provider_factory_does_not_wrap_review_files(self) -> None:
        """build_review_graph without a factory leaves the review_files node unwrapped."""
        original_registry = graph_module._NODE_REGISTRY.copy()

        try:
            graph_module._NODE_REGISTRY.update(
                {
                    "fetch_pr_details": _stub_fetch_pr_details,
                    "source_context": _stub_source_context,
                    "scaffold_comments": _stub_scaffold_comments,
                    "review_files": _stub_review_files,
                    "summarize_and_decide": _stub_summarize_and_decide,
                    "post_results": _stub_post_results,
                }
            )
            with patch.object(graph_module, "_load_real_nodes"):
                compiled = build_review_graph()
                result = compiled.invoke(
                    {
                        "pr_id": 1,
                        "files": [],
                        "threads": [],
                        "config": {},
                        "file_results": [],
                        "errors": [],
                    }
                )
        finally:
            graph_module._NODE_REGISTRY.clear()
            graph_module._NODE_REGISTRY.update(original_registry)

        assert result.get("file_results") == []

    def test_module_import_does_not_require_langgraph(self) -> None:
        """Reloading the module succeeds even when LangGraph imports are unavailable."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name in {"langgraph.graph", "langgraph.graph.state"}:
                raise ImportError("missing langgraph")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            reloaded = importlib.reload(graph_module)

        assert hasattr(reloaded, "build_review_graph")
        importlib.reload(graph_module)
