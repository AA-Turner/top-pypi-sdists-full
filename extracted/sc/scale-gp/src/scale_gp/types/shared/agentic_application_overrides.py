# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["AgenticApplicationOverrides", "InitialState", "PartialTrace"]


class InitialState(BaseModel):
    current_node: str

    state: Dict[str, object]


class PartialTrace(BaseModel):
    duration_ms: int

    node_id: str

    operation_input: str

    operation_output: str

    operation_type: str

    start_timestamp: str

    workflow_id: str

    operation_metadata: Optional[Dict[str, object]] = None


class AgenticApplicationOverrides(BaseModel):
    """Execution override options for agentic applications"""

    concurrent: Optional[bool] = None

    initial_state: Optional[InitialState] = None

    partial_trace: Optional[List[PartialTrace]] = None

    return_span: Optional[bool] = None

    use_channels: Optional[bool] = None
