"""Controller for AgentStage execution.

This module provides the controller that orchestrates AgentStage execution,
including template rendering, AI execution, and task dispatch.

The controller is designed with dependency injection for testability.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from abstra_internals.entities.agents.template import JinjaTemplateRenderer
from abstra_internals.repositories.project.project import AgentPermission, AgentStage


@dataclass
class AgentContext:
    """Context data available during agent execution.

    Attributes:
        trigger_task: The task data that triggered this agent execution.
        additional_data: Any additional context variables.
    """

    trigger_task: Dict[str, Any]
    additional_data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_task(
        cls,
        task: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> "AgentContext":
        return cls(
            trigger_task=task,
            additional_data=additional_context or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {"trigger_task": self.trigger_task}
        result.update(self.additional_data)
        return result


@dataclass
class AgentExecutionResult:
    """Result of an agent execution."""

    success: bool
    output: str
    tasks_to_send: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None


class AIExecutorProtocol(Protocol):
    """Protocol for AI execution backend."""

    def execute(
        self,
        prompt: str,
        permissions: List[AgentPermission],
        **kwargs: Any,
    ) -> AgentExecutionResult: ...


class AgentStageController:
    """Controller for orchestrating AgentStage execution."""

    def __init__(
        self,
        template_renderer: JinjaTemplateRenderer,
        ai_executor: AIExecutorProtocol,
    ):
        self._template_renderer = template_renderer
        self._ai_executor = ai_executor

    def build_prompt(
        self,
        template: str,
        task: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        context = AgentContext.from_task(task, additional_context)
        return self._template_renderer.render(template, context.to_dict())

    def build_prompt_from_file(
        self,
        file_path: str,
        task: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        context = AgentContext.from_task(task, additional_context)
        return self._template_renderer.render_from_file(file_path, context.to_dict())

    def execute(
        self,
        stage: AgentStage,
        prompt: str,
        **kwargs: Any,
    ) -> AgentExecutionResult:
        return self._ai_executor.execute(
            prompt=prompt,
            permissions=stage.permissions,
            **kwargs,
        )

    def execute_from_template(
        self,
        stage: AgentStage,
        template: str,
        task: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AgentExecutionResult:
        prompt = self.build_prompt(template, task, additional_context)
        return self.execute(stage, prompt, **kwargs)

    def execute_from_file(
        self,
        stage: AgentStage,
        task: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AgentExecutionResult:
        prompt = self.build_prompt_from_file(
            str(stage.file_path),
            task,
            additional_context,
        )
        return self.execute(stage, prompt, **kwargs)
