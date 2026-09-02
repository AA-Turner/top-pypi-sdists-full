"""Agent-run manager bundle (``arm``) — the resumable-run primitive's DB layer.

Aggregates the two matrx-orm managers behind the ``RunCheckpointer``
(``matrx_ai.agent_runners._checkpoint``): the run-level row (``agent_run``)
and the per-stage / per-paid-asset checkpoint row (``agent_run_stage``).
Mirrors the host ``pexm`` / ``fxm`` bundles, but lives inside matrx-ai because
the agent_runners that consume it (podcast, research, ...) live here and must
not import ``aidream/db``. Models/bases are injected by the host via
``matrx_ai.configure(db_models=..., db_bases=...)`` and read back through the
registry — exactly like ``cx_managers``.

Public API
----------
::

    from matrx_ai.db.arm_managers import arm

    run = await arm.runs.create_item(kind="podcast", created_by=uid, status="processing")
    await arm.stages.create_item(run_id=run.id, stage_key="create_script", status="completed", output={...})
    done = await arm.stages.filter_items(run_id=run.id, status="completed")
"""

from __future__ import annotations

from typing import Any

from matrx_ai.db._registry import get_base, get_model

# agent_run / agent_run_stage live in the `chat` schema; the host registers them
# under their prefix-free registry keys. Local aliases stay stable.
AgentRunBase = get_base("AgentRunBase")
AgentRunStageBase = get_base("AgentRunStageBase")

AgentRun = get_model("AgentRun")
AgentRunStage = get_model("AgentRunStage")


class AgentRunManager(AgentRunBase):
    _instance: "AgentRunManager | None" = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "AgentRunManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Any) -> None:
        pass


class AgentRunStageManager(AgentRunStageBase):
    _instance: "AgentRunStageManager | None" = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "AgentRunStageManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Any) -> None:
        pass


agent_run_manager_instance = AgentRunManager()
agent_run_stage_manager_instance = AgentRunStageManager()


class ArmManagers:
    """Singleton aggregator for the agent-run managers."""

    _instance: "ArmManagers | None" = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "ArmManagers":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # chat.agent_run — one row per resumable pipeline invocation.
        self.runs = agent_run_manager_instance
        # chat.agent_run_stage — one row per stage / per paid asset checkpoint.
        self.stages = agent_run_stage_manager_instance


arm = ArmManagers()


__all__ = ["ArmManagers", "arm"]
