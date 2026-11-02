"""Grouping class that surfaces all wf_* singleton managers behind one object.

Mirrors `matrx_ai.db.agx_manager.AgxManagers`. Populated lazily from the
registry — the actual manager instances are registered by the host app after
running matrx-orm generation on the wf_* tables.

Usage (after configure_db has run):

    from matrx_graph.db import wf

    definition = await wf.wf_definition.load_by_id(definition_id)
    await wf.wf_definition.update_wf_definition(definition_id, name='new name')

Calling `wf.wf_definition` before configure_db() raises DBNotConfiguredError.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.db._registry import get_instance


class WfManagers:
    _instance: WfManagers | None = None

    def __new__(cls) -> WfManagers:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def wf_definition(self) -> Any:
        return get_instance("wf_definition_manager")

    @property
    def wf_definition_version(self) -> Any:
        return get_instance("wf_definition_version_manager")

    @property
    def wf_run(self) -> Any:
        return get_instance("wf_run_manager")

    @property
    def wf_checkpoint(self) -> Any:
        return get_instance("wf_checkpoint_manager")

    @property
    def wf_node_outcome(self) -> Any:
        return get_instance("wf_node_outcome_manager")


wf = WfManagers()
