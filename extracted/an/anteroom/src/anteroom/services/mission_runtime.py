"""Shared runtime helpers for hosting mission scheduling and workflow execution."""

from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..config import AppConfig
    from .mission_adapters import MissionAdapterRegistry
    from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)


def create_workflow_engine_factory(
    config: AppConfig,
    db: Any,
    *,
    event_bus: Any | None = None,
    artifact_registry: Any | None = None,
    skill_registry: Any | None = None,
    audit_writer: Any | None = None,
) -> Callable[[], WorkflowEngine]:
    """Build a factory for workflow execution engines used by mission hosting."""

    def _make_engine() -> WorkflowEngine:
        from ..services.workflow_engine import WorkflowEngine
        from ..services.workflow_runners import create_default_registry

        ai_service = None
        tool_executor = None
        tools_openai = None
        try:
            from ..services.ai_service import create_ai_service
            from ..tools import ToolRegistry, register_default_tools

            ai_service = create_ai_service(config.ai)
            tool_reg = ToolRegistry()
            working_dir = str(Path.cwd())
            register_default_tools(tool_reg, working_dir=working_dir)
            workflow_safety = copy.copy(config.safety)
            workflow_safety.approval_mode = config.workflow.approval_mode
            tool_reg.set_safety_config(workflow_safety, working_dir=working_dir)
            tool_executor = tool_reg.call_tool
            tools_openai = tool_reg.get_openai_tools()
        except Exception as exc:
            logger.warning("Could not initialize workflow runtime tools: %s", exc)

        credential_resolver = None
        if config.workflow.credentials:
            from ..services.workflow_credentials import CredentialResolver

            credential_resolver = CredentialResolver(config.workflow.credentials)

        resolved_artifact_registry = artifact_registry
        resolved_skill_registry = skill_registry
        if resolved_artifact_registry is None or resolved_skill_registry is None:
            try:
                from ..cli.skills import SkillRegistry
                from ..services.artifact_registry import ArtifactRegistry

                resolved_artifact_registry = ArtifactRegistry()
                resolved_artifact_registry.load_from_db(db)
                resolved_skill_registry = SkillRegistry()
                resolved_skill_registry.load()
                resolved_skill_registry.load_from_artifacts(resolved_artifact_registry)
            except Exception as exc:
                logger.debug("Could not initialize artifact/skill registries: %s", exc)
                resolved_artifact_registry = artifact_registry
                resolved_skill_registry = skill_registry

        resolved_audit_writer = audit_writer
        if resolved_audit_writer is None:
            try:
                from ..services.audit import create_audit_writer

                resolved_audit_writer = create_audit_writer(config)
            except Exception:
                logger.debug("Could not create audit writer for mission runtime")

        try:
            from ..services.spec_gates import register_spec_gates

            register_spec_gates(db)
        except Exception:
            logger.debug("Could not register spec gates for mission runtime")

        return WorkflowEngine(
            db,
            config.workflow,
            create_default_registry(),
            effective_approval_mode=config.workflow.approval_mode,
            ai_service=ai_service,
            tool_executor=tool_executor,
            tools_openai=tools_openai,
            event_bus=event_bus,
            egress_allowed_domains=list(config.ai.allowed_domains) if config.ai.allowed_domains else [],
            egress_block_localhost=config.ai.block_localhost_api,
            credential_resolver=credential_resolver,
            artifact_registry=resolved_artifact_registry,
            skill_registry=resolved_skill_registry,
            audit_writer=resolved_audit_writer,
        )

    return _make_engine


def create_mission_adapter_registry(
    config: AppConfig,
    db: Any,
    *,
    workflow_engine_factory: Callable[[], WorkflowEngine] | None = None,
    event_bus: Any | None = None,
    artifact_registry: Any | None = None,
    skill_registry: Any | None = None,
    audit_writer: Any | None = None,
) -> MissionAdapterRegistry:
    """Create the default mission adapter registry for app or CLI hosting."""

    from .mission_adapters import create_default_adapter_registry

    if not config.workflow.enabled:
        return create_default_adapter_registry()

    factory = workflow_engine_factory or create_workflow_engine_factory(
        config,
        db,
        event_bus=event_bus,
        artifact_registry=artifact_registry,
        skill_registry=skill_registry,
        audit_writer=audit_writer,
    )
    return create_default_adapter_registry(db=db, engine=factory())
