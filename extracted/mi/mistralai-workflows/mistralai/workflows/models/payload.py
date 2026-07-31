from enum import StrEnum
from typing import Any

from mistralai.extra.workflows.encoding.models import (
    EncodedPayload as EncodedPayloadBase,
)
from mistralai.extra.workflows.encoding.models import (
    EncodedPayloadOptions,
)
from mistralai.extra.workflows.encoding.models import (
    WorkflowContext as WorkflowContextBase,
)
from pydantic import BaseModel, Field

from mistralai.workflows.constants import INTERNAL_METADATA_PREFIX


class WorkflowContext(WorkflowContextBase):
    """Extended WorkflowContext with extensions support for connector integration."""

    on_behalf_of: bool | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)
    # Worker-only channel populated by interceptors (e.g. the connector
    # interceptor's resolved bindings), not by workflow callers. Travels
    # alongside `extensions` but under a caller-inaccessible metadata key,
    # so downstream readers (ToolCallClient, RemoteSession) can trust its
    # contents as interceptor-owned without forgery checks.
    trusted_extensions: dict[str, Any] = Field(default_factory=dict)


class EncodedPayload(EncodedPayloadBase):
    """Extended EncodedPayload that uses WorkflowContext with extensions support."""

    context: WorkflowContext
    encoding_options: list[EncodedPayloadOptions] = Field(description="The encoding of the payload", default=[])
    payload: bytes = Field(description="The encoded payload")


class PayloadMetadataKeys(StrEnum):
    ENCODING = "encoding"
    ENCODING_ORIGINAL = "encoding-orig"
    NAMESPACE = "namespace"
    EXECUTION_ID = "execution_id"
    PARENT_WORKFLOW_EXEC_ID = "parent_workflow_exec_id"
    ROOT_WORKFLOW_EXEC_ID = "root_workflow_exec_id"
    EMPTY_PAYLOAD = "empty_payload"
    ENCODING_OPTIONS = "encoding_options"
    EXECUTION_TOKEN = f"{INTERNAL_METADATA_PREFIX}execution_token"
    EXTENSIONS = f"{INTERNAL_METADATA_PREFIX}extensions"
    TRUSTED_EXTENSIONS = f"{INTERNAL_METADATA_PREFIX}trusted_extensions"
    ON_BEHALF_OF = f"{INTERNAL_METADATA_PREFIX}on_behalf_of"
    IS_UNENCODED_MEMO = "is_unencoded_memo"


class PayloadWithContext(BaseModel):
    """Format of payloads sent through temporal server"""

    context: WorkflowContext
    payload: Any
    empty: bool = False
