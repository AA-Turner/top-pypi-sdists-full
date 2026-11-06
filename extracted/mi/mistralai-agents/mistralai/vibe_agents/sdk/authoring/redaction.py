from mistralai.observability.otel import AttributeMaskCallback, CallbackRedactionPolicy, OperationDataTransformer

from .errors import SdkError

type RedactionPolicy = OperationDataTransformer | AttributeMaskCallback
"""One way the agent's traces mask secrets and personal data: a redaction policy or a
``(key, value)`` function.

``OperationDataTransformer`` is what a redaction policy is, such as ``RegexRedactionPolicy``: an
object whose ``transform`` method returns the value to record, or ``None`` to drop it.
``OperationDataValue`` is a trace field's value: a string, a number, a boolean, bytes, ``None``,
or a list or a mapping of these."""
type Redaction = RedactionPolicy | list[RedactionPolicy] | tuple[RedactionPolicy, ...]
"""What ``Agent(redaction=...)`` takes: one ``RedactionPolicy`` or a list of them, applied in order.
``[]`` turns redaction off."""


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
