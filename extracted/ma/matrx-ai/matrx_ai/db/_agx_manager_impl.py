from __future__ import annotations

from typing import Any

from matrx_utils import vcprint

from matrx_ai.db._registry import get_base, get_model

AgxDefinitionBase = get_base("DefinitionBase")
AgxDefinitionVersionBase = get_base("DefinitionVersionBase")
AgxShortcutBase = get_base("ShortcutBase")


AgxDefinition = get_model("Definition")
AgxDefinitionVersion = get_model("DefinitionVersion")
AgxShortcut = get_model("Shortcut")

from matrx_ai.agents.types import AgentConfig  # noqa: E402
from matrx_ai.client_host.agent_source import (  # noqa: E402
    definition_from_row,
    definition_to_agent_config,
)


def _row_to_config(row: Any) -> AgentConfig:
    is_version = hasattr(row, "version_number")
    try:
        return definition_to_agent_config(definition_from_row(row, is_version=is_version))
    except Exception as exc:
        vcprint(
            {"error": str(exc), "agent_id": str(getattr(row, "id", "?"))},
            "[agx_manager] Invalid execution definition",
            color="red",
        )
        raise


class AgxDefinitionManager(AgxDefinitionBase):
    _instance: AgxDefinitionManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AgxDefinitionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: AgxDefinition) -> None:
        pass

    async def to_config(self, agent_id: str) -> AgentConfig:
        agent: AgxDefinition = await self.load_by_id(agent_id)
        return _row_to_config(agent)


class AgxDefinitionVersionManager(AgxDefinitionVersionBase):
    _instance: AgxDefinitionVersionManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AgxDefinitionVersionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: AgxDefinitionVersion) -> None:
        pass

    async def to_config(self, version_id: str) -> AgentConfig:
        version: AgxDefinitionVersion = await self.load_by_id(version_id)
        return _row_to_config(version)


class AgxShortcutManager(AgxShortcutBase):
    _instance: AgxShortcutManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AgxShortcutManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: AgxShortcut) -> None:
        pass


definition_manager_instance = AgxDefinitionManager()
definition_version_manager_instance = AgxDefinitionVersionManager()
shortcut_manager_instance = AgxShortcutManager()


async def agent_viewer_access(agent_id: str, user_id: str) -> bool:
    """Canonical access check — ``iam.has_access_for(user, 'agent', id, 'viewer')``.

    Arman's ruling (2026-08-12, the ``agent.definition.is_public`` cut): anything
    you can VIEW, you may duplicate and run — viewer-level access replaces every
    former ``is_public`` check. Builtins pass via the Matrx System org's
    ``global_readable`` lane; shares/org grants pass via their own lanes. ONE
    source of truth — never re-implement visibility/org/grant semantics here.
    Fail-closed: any error reads as no access.
    """
    if not user_id:
        return False
    try:
        from matrx_orm import call_function

        result = await call_function(
            AgxDefinition._database, "iam", "has_access_for",
            str(user_id), "agent", str(agent_id), "viewer", mode="scalar",
        )
        return bool(result)
    except Exception:  # noqa: BLE001 — fail closed, never raise into callers
        vcprint(
            f"[agx_manager] agent viewer-access check failed for {agent_id}",
            color="yellow",
        )
        return False

# Backward-compat aliases for call sites not yet renamed.
agx_agent_manager_instance = definition_manager_instance
agx_version_manager_instance = definition_version_manager_instance
agx_shortcut_manager_instance = shortcut_manager_instance


class AgxManagers:
    _instance: AgxManagers | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AgxManagers:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.definition: AgxDefinitionManager = definition_manager_instance
        self.definition_version: AgxDefinitionVersionManager = definition_version_manager_instance
        self.shortcut: AgxShortcutManager = shortcut_manager_instance
        # Legacy property names — same manager instances.
        self.agx_agent: AgxDefinitionManager = definition_manager_instance
        self.agx_version: AgxDefinitionVersionManager = definition_version_manager_instance
        self.agx_shortcut: AgxShortcutManager = shortcut_manager_instance

    async def load_for_execution(self, resolved_id: str, is_version: bool = False) -> AgentConfig:
        from matrx_ai.client_host.agent_source import try_load_from_execution_source

        loaded = await try_load_from_execution_source(resolved_id, is_version=is_version)
        if loaded is not None:
            return loaded
        if is_version:
            return await self.definition_version.to_config(resolved_id)
        return await self.definition.to_config(resolved_id)


agx = AgxManagers()
