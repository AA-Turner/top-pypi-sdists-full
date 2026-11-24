"""A published workflow version compiles once per process (L-SPEED round 6a, item 5).

Before: one mandate call compiled its workflow in the route preflight (``input_surface``), in the
holder, and again when the run was read back (``_child_contract`` / ``run_result``). A published
version never changes and ``CompiledGraph`` is frozen, so ``compile_version`` / ``compile_stored``
keep it by (registry, registry generation, version id). A draft compiles every time; a registry
change (a node type registered or replaced) compiles afresh.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_graph import NodeRegistry, compile_stored, compile_version, register_builtin_nodes
from tests.test_scheduler_ready_nodes_do_not_wait import _podcast_shape, _Sleeper


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Sleeper())
    return registry


def test_a_published_version_is_compiled_once() -> None:
    registry = _registry()
    first = compile_version(_podcast_shape(), version_id="v-once-1", registry=registry)
    again = compile_version(_podcast_shape(), version_id="v-once-1", registry=registry)
    assert again is first
    row = SimpleNamespace(id="v-once-1", is_version=True, definition=_podcast_shape())
    assert compile_stored(row, registry=registry) is first


def test_a_draft_compiles_every_time() -> None:
    registry = _registry()
    draft = SimpleNamespace(id="draft-1", is_version=False, definition=_podcast_shape())
    assert compile_stored(draft, registry=registry) is not compile_stored(draft, registry=registry)
    assert compile_version(_podcast_shape(), version_id=None, registry=registry) is not compile_version(
        _podcast_shape(), version_id=None, registry=registry
    )


def test_a_registry_change_compiles_afresh() -> None:
    registry = _registry()
    first = compile_version(_podcast_shape(), version_id="v-once-2", registry=registry)
    registry.register(_Sleeper(), overwrite=True)
    assert compile_version(_podcast_shape(), version_id="v-once-2", registry=registry) is not first


def test_clearing_the_registry_compiles_afresh() -> None:
    registry = _registry()
    first = compile_version(_podcast_shape(), version_id="v-once-3", registry=registry)
    before = registry.generation
    registry.clear()
    assert registry.generation > before
    register_builtin_nodes(registry)
    registry.register(_Sleeper())
    assert compile_version(_podcast_shape(), version_id="v-once-3", registry=registry) is not first
