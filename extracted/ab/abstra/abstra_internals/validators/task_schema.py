from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import jsonschema
from jsonschema import ValidationError

JSONSchema = Dict[str, Any]


@dataclass
class TaskSchemaValidationError:
    """Error details from schema validation failure."""

    task_type: str
    message: str
    path: List[str]
    stage_id: Optional[str] = None

    def __str__(self) -> str:
        path_str = ".".join(str(p) for p in self.path) if self.path else "(root)"
        stage_info = f" for stage '{self.stage_id}'" if self.stage_id else ""
        return f"Validation error for task type '{self.task_type}'{stage_info} at {path_str}: {self.message}"


class TaskSchemaValidationException(Exception):
    """Exception raised when task payload fails schema validation."""

    def __init__(self, error: TaskSchemaValidationError):
        self.error = error
        super().__init__(str(error))


class TaskSchemaValidator:
    """
    Validates task payloads against JSON schemas.

    Supports registering schemas per stage and task type, then validating
    payloads before tasks are sent.
    """

    def __init__(
        self, schema_registry: Optional[Dict[str, Dict[str, JSONSchema]]] = None
    ):
        """
        Initialize validator with optional pre-populated registry.

        Args:
            schema_registry: Optional dict mapping stage_id -> {task_type -> JSONSchema}
        """
        self._registry: Dict[str, Dict[str, JSONSchema]] = schema_registry or {}

    def register_stage_schema(
        self, stage_id: str, task_schemas: Dict[str, JSONSchema]
    ) -> None:
        """
        Register task schemas for a stage.

        Args:
            stage_id: The stage identifier
            task_schemas: Dict mapping task_type to JSONSchema
        """
        self._registry[stage_id] = task_schemas

    def get_schema(self, stage_id: str, task_type: str) -> Optional[JSONSchema]:
        """
        Get schema for a specific stage and task type.

        Returns:
            The JSONSchema if found, None otherwise
        """
        stage_schemas = self._registry.get(stage_id, {})
        return stage_schemas.get(task_type)

    def has_schema_for_stage(self, stage_id: str) -> bool:
        """
        Check if any schema is registered for a stage.

        Returns:
            True if the stage has a task_schema defined, False otherwise
        """
        return stage_id in self._registry and bool(self._registry[stage_id])

    def validate(
        self,
        stage_id: str,
        task_type: str,
        payload: Dict[str, Any],
    ) -> Optional[TaskSchemaValidationError]:
        """
        Validate payload against schema.

        Args:
            stage_id: Target stage identifier
            task_type: Type of task being sent
            payload: The payload to validate

        Returns:
            None if valid, TaskSchemaValidationError if invalid

        Validation rules:
        - If stage has no task_schema defined: any task is accepted
        - If stage has task_schema but task_type is not in it: validation fails
        - If stage has task_schema with task_type: payload must match the schema
        """
        # No schema for stage means any payload is accepted
        if not self.has_schema_for_stage(stage_id):
            return None

        stage_schemas = self._registry[stage_id]
        schema = stage_schemas.get(task_type)

        # Fall back to "default" schema if the exact task_type is not found
        if schema is None:
            schema = stage_schemas.get("default")

        # Stage has schema but task_type is not defined - fail
        if schema is None:
            available_types = list(stage_schemas.keys())
            return TaskSchemaValidationError(
                task_type=task_type,
                message=f"Task type '{task_type}' is not defined in stage schema. Available types: {available_types}",
                path=[],
                stage_id=stage_id,
            )

        try:
            jsonschema.validate(instance=payload, schema=schema)
            return None
        except ValidationError as e:
            return TaskSchemaValidationError(
                task_type=task_type,
                message=str(e.message),
                path=[str(p) for p in e.path],
                stage_id=stage_id,
            )

    def validate_or_raise(
        self,
        stage_id: str,
        task_type: str,
        payload: Dict[str, Any],
    ) -> None:
        """
        Validate payload and raise exception if invalid.

        Args:
            stage_id: Target stage identifier
            task_type: Type of task being sent
            payload: The payload to validate

        Raises:
            TaskSchemaValidationException: If payload fails validation
        """
        error = self.validate(stage_id, task_type, payload)
        if error:
            raise TaskSchemaValidationException(error)
