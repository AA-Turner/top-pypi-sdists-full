import json
from typing import Dict, Mapping, Tuple

from mistralai.extra.exceptions import WorkflowPayloadOffloadingException

from mistralai.workflows.core.encoding.constants import ACCEPTED_ENCODING_FORMATS, NEW_ENCODING_FORMAT
from mistralai.workflows.models import (
    EncodedPayloadOptions,
    PayloadMetadataKeys,
    WorkflowContext,
)


def is_custom_encoding_format(encoding: bytes | str) -> bool:
    """Check if the encoding is one of our custom formats (new or legacy)."""
    if isinstance(encoding, bytes):
        encoding = encoding.decode()
    return encoding in ACCEPTED_ENCODING_FORMATS


def build_temporal_payload_metadata(
    context: WorkflowContext, encoding_options: list[EncodedPayloadOptions], empty_payload: bool = False
) -> Dict[str, bytes]:
    """Build Temporal payload metadata from workflow context and encoding options."""
    metadata: Dict[str, bytes] = {
        PayloadMetadataKeys.ENCODING: NEW_ENCODING_FORMAT.encode(),
        PayloadMetadataKeys.NAMESPACE: context.namespace.encode(),
        PayloadMetadataKeys.EXECUTION_ID: context.execution_id.encode(),
        PayloadMetadataKeys.ENCODING_OPTIONS: b",".join(option.value.encode() for option in encoding_options),
    }

    if context.root_workflow_exec_id:
        metadata[PayloadMetadataKeys.ROOT_WORKFLOW_EXEC_ID] = context.root_workflow_exec_id.encode()
    if context.parent_workflow_exec_id:
        metadata[PayloadMetadataKeys.PARENT_WORKFLOW_EXEC_ID] = context.parent_workflow_exec_id.encode()
    if context.execution_token:
        metadata[PayloadMetadataKeys.EXECUTION_TOKEN] = context.execution_token.encode()
    if context.extensions:
        metadata[PayloadMetadataKeys.EXTENSIONS] = json.dumps(context.extensions).encode()
    if context.trusted_extensions:
        metadata[PayloadMetadataKeys.TRUSTED_EXTENSIONS] = json.dumps(context.trusted_extensions).encode()
    if context.on_behalf_of is not None:
        metadata[PayloadMetadataKeys.ON_BEHALF_OF] = b"true" if context.on_behalf_of else b"false"

    if empty_payload:
        metadata[PayloadMetadataKeys.EMPTY_PAYLOAD] = bytes(True)

    return metadata


def build_info_from_payload_metadata(
    metadata: Mapping[str, bytes],
) -> Tuple[WorkflowContext, list[EncodedPayloadOptions], bool]:
    """Extract workflow context and encoding options from Temporal payload metadata."""
    root_workflow_exec_id_bytes = metadata.get(PayloadMetadataKeys.ROOT_WORKFLOW_EXEC_ID)
    root_workflow_exec_id = root_workflow_exec_id_bytes.decode() if root_workflow_exec_id_bytes else None
    parent_workflow_exec_id_bytes = metadata.get(PayloadMetadataKeys.PARENT_WORKFLOW_EXEC_ID)
    parent_workflow_exec_id = parent_workflow_exec_id_bytes.decode() if parent_workflow_exec_id_bytes else None
    execution_token_bytes = metadata.get(PayloadMetadataKeys.EXECUTION_TOKEN)
    execution_token = execution_token_bytes.decode() if execution_token_bytes else None
    extensions_bytes = metadata.get(PayloadMetadataKeys.EXTENSIONS)
    extensions = json.loads(extensions_bytes) if extensions_bytes else {}
    trusted_extensions_bytes = metadata.get(PayloadMetadataKeys.TRUSTED_EXTENSIONS)
    trusted_extensions = json.loads(trusted_extensions_bytes) if trusted_extensions_bytes else {}

    on_behalf_of_bytes = metadata.get(PayloadMetadataKeys.ON_BEHALF_OF)
    on_behalf_of: bool | None = on_behalf_of_bytes == b"true" if on_behalf_of_bytes is not None else None

    workflow_context = WorkflowContext(
        namespace=metadata.get(PayloadMetadataKeys.NAMESPACE, b"").decode(),
        execution_id=metadata.get(PayloadMetadataKeys.EXECUTION_ID, b"").decode(),
        root_workflow_exec_id=root_workflow_exec_id,
        parent_workflow_exec_id=parent_workflow_exec_id,
        execution_token=execution_token,
        extensions=extensions,
        trusted_extensions=trusted_extensions,
        on_behalf_of=on_behalf_of,
    )

    empty = bool(metadata.get(PayloadMetadataKeys.EMPTY_PAYLOAD))
    encoding_options: list[EncodedPayloadOptions] = []
    encoding_options_bytes = metadata.get(PayloadMetadataKeys.ENCODING_OPTIONS, None)
    if encoding_options_bytes:
        for option in encoding_options_bytes.split(b","):
            option_str = option.decode()
            try:
                encoding_options.append(EncodedPayloadOptions(option_str))
            except ValueError:
                raise WorkflowPayloadOffloadingException(f"Unknown encoding option {option_str}")
    return workflow_context, encoding_options, empty
