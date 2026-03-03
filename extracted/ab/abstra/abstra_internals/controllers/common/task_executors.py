from typing import Any, Dict, List, Optional

from abstra_internals.email_templates import task_waiting_template
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ScriptContext
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.project.project import (
    ComponentStage,
    FormStage,
    ScriptStage,
    Stage,
)
from abstra_internals.repositories.tasks import TaskDTO, TaskPayload
from abstra_internals.validators.task_schema import (
    TaskSchemaValidationError,
    TaskSchemaValidationException,
    TaskSchemaValidator,
)

_JSON_SCHEMA_TYPES = {
    "object",
    "array",
    "string",
    "number",
    "integer",
    "boolean",
    "null",
}


def _normalize_task_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a task schema to the {task_type: json_schema} format.

    If the schema is a flat JSON Schema (has "type" with a JSON Schema type value),
    wrap it as {"default": schema} so the validator's "default" fallback works.
    Otherwise assume it's already in {task_type: json_schema} format.
    """
    if schema.get("type") in _JSON_SCHEMA_TYPES:
        return {"default": schema}
    return schema


class TaskExecutor:
    def __init__(self, repos: Repositories) -> None:
        self.repos = repos
        self.project = self.repos.project.load(include_disabled_stages=False)

    def _get_target_stages(self, type: str, current_stage: Stage) -> List[Stage]:
        """Get the list of target stages for a task type."""
        project = self.repos.project.load(include_disabled_stages=False)

        next_stages: List[Stage] = []
        module_name = project.find_module_containing_stage(current_stage.id)
        if module_name is not None:
            if project.is_stage_module_output(current_stage.id):
                parent_component_stage = project.get_component_by_module_name(
                    module_name
                )
                if parent_component_stage is not None:
                    next_stages = [
                        project.get_stage_raises(t.target_id)
                        for t in parent_component_stage.workflow_transitions
                        if t.matches(type)
                    ]
            else:
                next_stages = [
                    project.get_stage_raises(t.target_id)
                    for t in current_stage.workflow_transitions
                    if t.matches(type)
                ]
        else:
            next_stages = [
                project.get_stage_raises(t.target_id)
                for t in current_stage.workflow_transitions
                if t.matches(type)
            ]

        # Expand ComponentStages to their input stages
        expanded_stages: List[Stage] = []
        for stage in next_stages:
            if isinstance(stage, ComponentStage):
                module = stage.package_name
                if module is not None:
                    input_stages = self.project.get_inputs_for_module(module)
                    expanded_stages.extend(input_stages)
                else:
                    expanded_stages.append(stage)
            else:
                expanded_stages.append(stage)

        return expanded_stages

    def _validate_task_for_stages(
        self, type: str, payload: TaskPayload, target_stages: List[Stage]
    ) -> Optional[TaskSchemaValidationError]:
        """
        Validate task payload against all target stages' schemas.

        Returns the first validation error encountered, or None if all pass.
        """
        validator = TaskSchemaValidator()

        # Register schemas for all target stages
        for stage in target_stages:
            task_schema = getattr(stage, "task_schema", None)
            if task_schema:
                normalized = _normalize_task_schema(task_schema)
                validator.register_stage_schema(stage.id, normalized)

        # Validate against each target stage
        for stage in target_stages:
            error = validator.validate(stage.id, type, payload)
            if error:
                return error

        return None

    def send_task(
        self,
        type: str,
        current_stage: Stage,
        payload: TaskPayload,
        execution: Optional[Execution] = None,
        show_warning: bool = True,
    ) -> None:
        # Get all target stages
        next_stages = self._get_target_stages(type, current_stage)

        if len(next_stages) == 0 and show_warning:
            print(
                f"[WARNING] No transitions found for task type {type} in stage {current_stage.id}"
            )
            return

        # Validate against all target stages BEFORE sending any tasks
        validation_error = self._validate_task_for_stages(type, payload, next_stages)
        if validation_error:
            raise TaskSchemaValidationException(validation_error)

        # All validations passed, now send the tasks
        for stage in next_stages:
            task = self.repos.tasks.send_task(
                type=type,
                payload=payload,
                source_stage_id=current_stage.id,
                target_stage_id=stage.id,
                execution_id=execution.id if execution else None,
            )
            self._send_waiting_thread_notification(task)
            if execution:
                execution.context.sent_tasks.append(task.id)
            if isinstance(stage, ScriptStage):
                self.repos.producer.enqueue_fire_and_forget(
                    context=ScriptContext(task_id=task.id),
                    stage_id=stage.id,
                )

    def _send_waiting_thread_notification(self, task: TaskDTO):
        stage = self.project.get_stage(task.target_stage_id)
        if not stage:
            raise Exception(f"Stage {task.target_stage_id} not found")

        if not (isinstance(stage, FormStage) and stage.notification_trigger.enabled):
            return

        recipient_emails = stage.notification_trigger.get_recipients(task.payload)
        if not recipient_emails:
            return

        self.repos.email.send(
            task_waiting_template.generate_email(
                recipient_emails=recipient_emails, form=stage
            )
        )
