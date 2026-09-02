"""
DB Dependency Registry for matrx-ai package.

This module provides a configuration-based approach for injecting database
models, manager base classes, and manager instances that come from the host
application's DB layer. This allows matrx-ai to function as a proper
installable package without directly importing from the host codebase.

Usage (host application startup):

    from matrx_ai.db._registry import configure_db

    configure_db(
        models={"AiModel": AiModel, "CxMessage": CxMessage, ...},
        # AI-catalog models (ai schema — consumed by matrx_ai.catalog):
        #   "AiModel"      -> ai.model_definition (host class ModelDefinition)
        #   "AiProvider"   -> ai.provider
        #   "AiEndpoint"   -> ai.endpoint (one row per vendor)
        #   "AiApi"        -> ai.api (one row per wire contract)
        #   "AiModelAlias" -> ai.model_alias (name routing)
        #   "AiOffering"   -> ai.offering
        #   "AiSetting"    -> ai.setting
        bases={"CxConversationBase": CxConversationBase, ...},
        instances={"guest_executions_manager": gm_instance, ...},
        extras={"RenderDefinitionDTO": RenderDefinitionDTO, ...},
    )

Usage (within matrx-ai package):

    from matrx_ai.db._registry import get_model, get_base, get_instance
    AiModel = get_model("AiModel")
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any

_models: dict[str, Any] = {}
_bases: dict[str, Any] = {}
_instances: dict[str, Any] = {}
_extras: dict[str, Any] = {}
_configured = False


class DBNotConfiguredError(RuntimeError):
    pass


def _not_configured_msg(kind: str, name: str) -> str:
    return (
        f"matrx-ai DB {kind} '{name}' not registered. "
        f"Call matrx_ai.configure() or matrx_ai.db._registry.configure_db() "
        f"before accessing DB functionality."
    )


def configure_db(
    *,
    models: dict[str, Any] | None = None,
    bases: dict[str, Any] | None = None,
    instances: dict[str, Any] | None = None,
    extras: dict[str, Any] | None = None,
) -> None:
    global _configured
    if models:
        _models.update(models)
    if bases:
        _bases.update(bases)
    if instances:
        _instances.update(instances)
    if extras:
        _extras.update(extras)
    _configured = True


def is_configured() -> bool:
    return _configured


def has_requirements(
    *,
    models: Collection[str] = (),
    bases: Collection[str] = (),
    instances: Collection[str] = (),
    extras: Collection[str] = (),
) -> bool:
    """Return whether every named host DB artifact is currently registered."""
    return (
        all(name in _models for name in models)
        and all(name in _bases for name in bases)
        and all(name in _instances for name in instances)
        and all(name in _extras for name in extras)
    )


def get_model(name: str) -> Any:
    if name not in _models:
        raise DBNotConfiguredError(_not_configured_msg("model", name))
    return _models[name]


def get_base(name: str) -> Any:
    if name not in _bases:
        raise DBNotConfiguredError(_not_configured_msg("base class", name))
    return _bases[name]


def get_instance(name: str) -> Any:
    if name not in _instances:
        raise DBNotConfiguredError(_not_configured_msg("instance", name))
    return _instances[name]


def get_extra(name: str) -> Any:
    if name not in _extras:
        raise DBNotConfiguredError(_not_configured_msg("extra", name))
    return _extras[name]
