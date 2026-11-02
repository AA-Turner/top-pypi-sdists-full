from mistralai.observability.otel import AttributeMaskCallback, CallbackRedactionPolicy, OperationDataTransformer

from .errors import SdkError

type RedactionPolicy = OperationDataTransformer | AttributeMaskCallback
type Redaction = RedactionPolicy | list[RedactionPolicy] | tuple[RedactionPolicy, ...]


def resolve_redaction(redaction: Redaction) -> tuple[OperationDataTransformer, ...]:
    """Turn ``Agent(redaction=...)`` into the ordered policies the worker applies; ``[]`` disables redaction."""

    policies = redaction if isinstance(redaction, list | tuple) else (redaction,)
    return tuple(_resolve_policy(policy) for policy in policies)


def _resolve_policy(policy: object) -> OperationDataTransformer:
    if isinstance(policy, OperationDataTransformer):
        return policy
    if callable(policy):
        return CallbackRedactionPolicy(policy)
    raise SdkError(
        "Agent redaction must be a redaction policy, a (key, value) -> value | None function, or a list of them; "
        f"got {type(policy).__name__}"
    )
