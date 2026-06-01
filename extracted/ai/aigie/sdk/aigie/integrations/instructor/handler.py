"""
Instructor callback handler for Aigie SDK.

Provides automatic tracing for Instructor structured output calls,
including validation retries and schema capture.
"""

import contextlib
import uuid
from datetime import datetime
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


class InstructorHandler:
    """
    Instructor handler for Aigie tracing.

    Automatically traces Instructor structured extraction including:
    - Chat completion calls
    - Response model schema
    - Validation retries
    - Token usage and costs

    Example:
        >>> import instructor
        >>> from openai import OpenAI
        >>> from pydantic import BaseModel
        >>> from aigie.integrations.instructor import InstructorHandler
        >>>
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>>
        >>> handler = InstructorHandler(trace_name="user-extraction")
        >>> client = instructor.from_openai(OpenAI())
        >>> # Manual tracking can be done through the handler
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_schemas: bool = True,
        capture_outputs: bool = True,
    ):
        """
        Initialize Instructor handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_schemas: Whether to capture Pydantic model schemas
            capture_outputs: Whether to capture structured outputs
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_schemas = capture_schemas
        self.capture_outputs = capture_outputs

        # State tracking
        self.trace_id: str | None = None
        self.call_span_id: str | None = None
        self.retry_count = 0

        # Statistics
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.total_retries = 0

        self._aigie = None

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    async def handle_call_start(
        self,
        messages: list[dict[str, Any]],
        response_model: Any,
        model: str,
        **kwargs,
    ) -> str:
        """
        Called when an instructor call starts.

        Args:
            messages: Chat messages being sent
            response_model: Pydantic model for response
            model: LLM model being used
            **kwargs: Additional parameters

        Returns:
            The span ID for tracking
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return ""

        # Generate trace ID if not set
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())

        self.retry_count = 0

        # Extract schema from response model
        schema = None
        model_name = None
        if response_model:
            if hasattr(response_model, "__name__"):
                model_name = response_model.__name__
            if hasattr(response_model, "model_json_schema") and self.capture_schemas:
                with contextlib.suppress(Exception):
                    schema = response_model.model_json_schema()

        trace_name = self.trace_name or f"Instructor: {model_name or 'extraction'}"

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "model": model,
                "response_model": model_name,
                "framework": "instructor",
                "max_retries": kwargs.get("max_retries", 1),
            }
        )

        # Create trace
        trace_data = {
            "id": self.trace_id,
            "name": trace_name,
            "type": "chain",
            "input": {
                "messages": messages[:5] if messages else [],  # Limit messages
                "response_model": model_name,
                "model": model,
            },
            "status": "pending",
            "tags": [*self.tags, "instructor"],
            "metadata": merge_metadata(trace_metadata),
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if self.user_id:
            trace_data["user_id"] = self.user_id
        if self.session_id:
            trace_data["session_id"] = self.session_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

        # Create call span
        self.call_span_id = str(uuid.uuid4())
        span_data = {
            "id": self.call_span_id,
            "trace_id": self.trace_id,
            "name": f"instructor:{model}",
            "type": "llm",
            "input": {
                "messages": messages[:5] if messages else [],
                "response_model": model_name,
                "schema": schema if self.capture_schemas else None,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": trace_metadata,
            "model": model,
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return self.call_span_id

    async def handle_call_end(
        self,
        result: Any,
        usage: dict[str, int] | None = None,
        error: str | None = None,
    ) -> None:
        """
        Called when an instructor call completes.

        Args:
            result: The structured output result
            usage: Token usage information
            error: Error message if call failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = datetime.now()
        success = error is None

        # Process usage
        if usage:
            self.total_input_tokens += usage.get("prompt_tokens", usage.get("input_tokens", 0))
            self.total_output_tokens += usage.get(
                "completion_tokens", usage.get("output_tokens", 0)
            )

        # Serialize result
        output_data = {}
        if result and self.capture_outputs:
            if hasattr(result, "model_dump"):
                try:
                    output_data["result"] = result.model_dump()
                except Exception:
                    output_data["result"] = str(result)[:1000]
            else:
                output_data["result"] = str(result)[:1000]

        output_data["retries"] = self.retry_count
        self.total_retries += self.retry_count

        # Update call span
        if self.call_span_id:
            span_update = {
                "id": self.call_span_id,
                "status": "success" if success else "failed",
                "output": output_data,
                "end_time": end_time.isoformat(),
                "prompt_tokens": self.total_input_tokens,
                "completion_tokens": self.total_output_tokens,
                "total_tokens": self.total_input_tokens + self.total_output_tokens,
            }

            if error:
                span_update["error"] = error
                span_update["error_message"] = error

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_UPDATE, span_update)

        # Update trace
        trace_update = {
            "id": self.trace_id,
            "status": "success" if success else "failed",
            "output": output_data,
            "end_time": end_time.isoformat(),
        }

        if error:
            trace_update["error"] = error
            trace_update["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)

    async def handle_retry(
        self,
        retry_number: int,
        error: str,
    ) -> str:
        """
        Called when a validation retry occurs.

        Args:
            retry_number: Current retry attempt number
            error: Validation error that triggered retry

        Returns:
            Span ID for the retry
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.retry_count = retry_number

        retry_span_id = str(uuid.uuid4())
        span_data = {
            "id": retry_span_id,
            "trace_id": self.trace_id,
            "parent_id": self.call_span_id,
            "name": f"retry:{retry_number}",
            "type": "chain",
            "input": {
                "retry_number": retry_number,
                "validation_error": error[:500],
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "retry_number": retry_number,
                    "framework": "instructor",
                }
            ),
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return retry_span_id

    async def handle_validation_error(
        self,
        error: str,
        model_name: str | None = None,
    ) -> None:
        """
        Called when a validation error occurs.

        Args:
            error: The validation error message
            model_name: Name of the Pydantic model
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        # Create a span for the validation error
        error_span_id = str(uuid.uuid4())
        span_data = {
            "id": error_span_id,
            "trace_id": self.trace_id,
            "parent_id": self.call_span_id,
            "name": f"validation_error:{model_name or 'unknown'}",
            "type": "chain",
            "input": {"model_name": model_name},
            "output": {"error": error[:500]},
            "status": "failed",
            "error": error[:500],
            "error_type": "validation_error",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "model_name": model_name,
                    "framework": "instructor",
                }
            ),
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

    def __repr__(self) -> str:
        return (
            f"InstructorHandler("
            f"trace_id={self.trace_id}, "
            f"retries={self.total_retries}, "
            f"tokens={self.total_input_tokens + self.total_output_tokens})"
        )
