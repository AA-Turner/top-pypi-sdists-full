"""Regression tests for ``ToolRegistry.client_kinds_for_executor``.

This method is the surface→executor half of client delegation:
``tool_merge._resolve_active_client_kinds`` calls it for every request that
declares a ``client.surface``. The 2026-05-27 tool_* cutover shipped the
CALLER without the method — the resolver's blanket ``except Exception``
swallowed the AttributeError, every request resolved zero active client
executors, and every surface-routed client tool (user, update_plan, …) died
at dispatch with ``no_viable_executor`` for two weeks. These tests make that
class of failure structurally impossible to reship.
"""

from __future__ import annotations

from matrx_ai.tools.registry import ToolRegistry


class TestClientKindsForExecutor:
    def _registry(self) -> ToolRegistry:
        return ToolRegistry.get_instance()

    def test_method_exists_and_is_total(self) -> None:
        """The exact failure mode of the incident: the method must exist and
        never raise / never return empty for a non-empty input — even with no
        executor rows loaded."""
        registry = self._registry()
        saved = dict(registry._executor_parents)
        registry._executor_parents = {}
        try:
            kinds = registry.client_kinds_for_executor("matrx-user")
            assert "matrx-user" in kinds
        finally:
            registry._executor_parents = saved

    def test_includes_db_parent_chain(self) -> None:
        registry = self._registry()
        saved = dict(registry._executor_parents)
        registry._executor_parents = {
            "matrx-user.chat": "matrx-user",
            "matrx-user": None,
        }
        try:
            kinds = registry.client_kinds_for_executor("matrx-user.chat")
            assert kinds == {"matrx-user.chat", "matrx-user"}
        finally:
            registry._executor_parents = saved

    def test_dot_notation_fallback_without_db_rows(self) -> None:
        """A missing/stale tool_executor row must not kill delegation — the
        naming convention (``parent.child``) supplies structural ancestry."""
        registry = self._registry()
        saved = dict(registry._executor_parents)
        registry._executor_parents = {}
        try:
            kinds = registry.client_kinds_for_executor("chrome-extension.pilot")
            assert "chrome-extension" in kinds
            assert "chrome-extension.pilot" in kinds
        finally:
            registry._executor_parents = saved

    def test_parent_cycle_terminates(self) -> None:
        registry = self._registry()
        saved = dict(registry._executor_parents)
        registry._executor_parents = {"a": "b", "b": "a"}
        try:
            kinds = registry.client_kinds_for_executor("a")
            assert kinds == {"a", "b"}
        finally:
            registry._executor_parents = saved

    def test_delegation_end_to_end_routing(self) -> None:
        """Surface executor → active kinds → resolve_executor_binding ==
        'surface' for a client-bound tool. The full chain the chat surface
        depends on."""
        registry = self._registry()
        saved_parents = dict(registry._executor_parents)
        saved_binding = registry._bindings_by_tool.get("__test_user_tool__")
        registry._executor_parents = {"matrx-user": None}
        registry._bindings_by_tool["__test_user_tool__"] = {"matrx-user"}
        try:
            kinds = registry.client_kinds_for_executor("matrx-user")
            assert (
                registry.resolve_executor_binding("__test_user_tool__", set(kinds))
                == "surface"
            )
            # Server-direct run (no active client executors) → server.
            assert (
                registry.resolve_executor_binding("__test_user_tool__", set())
                == "server"
            )
        finally:
            registry._executor_parents = saved_parents
            if saved_binding is None:
                registry._bindings_by_tool.pop("__test_user_tool__", None)
            else:
                registry._bindings_by_tool["__test_user_tool__"] = saved_binding
