"""Legacy prompt-table access — retired.

The ``prompts`` / ``prompt_builtins`` / ``prompt_apps`` tables were moved to
the DB graveyard. This module keeps the old import surface so callers that still
reference ``pm`` / ``PromptManagers`` fail loudly instead of pulling missing
ORM models at import time.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

_RETIRED = (
    "Legacy prompt tables were retired; use agx agents "
    "(Agent.from_agent / AgentConfigResolver / POST /ai/agents/{id}) instead."
)


class PromptType(StrEnum):
    PROMPT = "prompt"
    BUILTIN = "builtin"
    PROMPT_VERSION = "prompt_version"
    BUILTIN_VERSION = "builtin_version"


class _RetiredPromptAccess(RuntimeError):
    pass


def _raise_retired() -> None:
    raise _RetiredPromptAccess(_RETIRED)


class PromptManagers:
    _instance: PromptManagers | None = None

    def __new__(cls) -> PromptManagers:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._type_cache: dict[str, PromptType] = {}

    def get_type(self, prompt_id: str) -> PromptType | None:
        return self._type_cache.get(prompt_id)

    @property
    def cache_size(self) -> int:
        return len(self._type_cache)

    async def hydrate_builtins(self) -> int:
        return 0

    def hydrate_builtins_sync(self) -> int:
        return 0

    async def hydrate_builtin_versions(self) -> int:
        return 0

    async def get_config(self, prompt_id: str) -> Any:
        _raise_retired()

    async def get_prompt_config(self, prompt_id: str) -> Any:
        _raise_retired()

    async def get_builtin_config(self, builtin_id: str) -> Any:
        _raise_retired()

    async def get_version_config(self, version_id: str) -> Any:
        _raise_retired()

    async def get_builtin_version_config(self, version_id: str) -> Any:
        _raise_retired()

    async def get_config_by_source(self, agent_id: str, source: str | None = None) -> Any:
        _raise_retired()

    async def load_prompt(self, prompt_id: str) -> Any:
        _raise_retired()

    async def load_prompt_or_none(self, prompt_id: str) -> None:
        return None

    async def find_prompts(self, **kwargs: Any) -> list[Any]:
        return []

    async def create_prompt(self, **data: Any) -> Any:
        _raise_retired()

    async def load_builtin(self, builtin_id: str) -> Any:
        _raise_retired()

    async def load_builtin_or_none(self, builtin_id: str) -> None:
        return None

    async def find_builtins(self, **kwargs: Any) -> list[Any]:
        return []

    async def create_builtin(self, **data: Any) -> Any:
        _raise_retired()

    async def update_prompt(self, prompt_id: str, **updates: Any) -> Any:
        _raise_retired()

    async def update_builtin(self, builtin_id: str, **updates: Any) -> Any:
        _raise_retired()

    async def update_by_id(self, item_id: str, **updates: Any) -> Any:
        _raise_retired()

    async def load_by_id(self, item_id: str) -> Any:
        _raise_retired()

    async def load_without_cache(self, item_id: str) -> Any:
        _raise_retired()

    async def load_by_id_or_none(self, item_id: str) -> None:
        return None


pm = PromptManagers()
