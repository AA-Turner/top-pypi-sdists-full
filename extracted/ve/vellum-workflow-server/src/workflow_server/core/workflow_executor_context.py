from dataclasses import field
from uuid import UUID
from typing import Any, Optional

from vellum.client.core import UniversalBaseModel
from vellum.workflows.context import ExecutionContext

DEFAULT_TIMEOUT_SECONDS = 60 * 30


class BaseExecutorContext(UniversalBaseModel):
    inputs: dict
    state: Optional[dict] = None
    timeout: int = DEFAULT_TIMEOUT_SECONDS
    files: dict[str, str]
    environment_api_key: str
    execution_id: UUID
    module: str
    execution_context: ExecutionContext = field(default_factory=ExecutionContext)
    request_start_time: int
    stream_start_time: int = 0
    vembda_public_url: Optional[str] = None
    node_output_mocks: Optional[list[Any]] = None
    environment_variables: Optional[dict[str, str]] = None

    @property
    def container_overhead_latency(self) -> int:
        return self.stream_start_time - self.request_start_time if self.stream_start_time else -1

    @property
    def trace_id(self) -> UUID:
        return self.execution_context.trace_id

    def __hash__(self) -> int:
        # do we think we need anything else for a unique hash for caching?
        return hash(str(self.execution_id))


class WorkflowExecutorContext(BaseExecutorContext):
    node_id: Optional[UUID] = None  # Sent during run from node UX


class NodeExecutorContext(BaseExecutorContext):
    node_module: str
    node_name: str
