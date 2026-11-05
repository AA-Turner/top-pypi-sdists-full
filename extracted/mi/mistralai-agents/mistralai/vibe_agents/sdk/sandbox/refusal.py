"""The sandbox creates that no retry fixes, and the reason each gives.

A backend raises a refused create as a non-retryable `ApplicationError` of one of these types,
whose message says what to fix. A Session on either host ends with that message, rather than with
Temporal's "Activity task failed" or a raw `ApplicationError`.
"""

from collections.abc import Iterator

from temporalio.exceptions import ApplicationError

MISTRAL_SANDBOX_ACCESS_DENIED_ERROR_TYPE = "MistralSandboxAccessDeniedError"
MISTRAL_SANDBOX_QUOTA_EXCEEDED_ERROR_TYPE = "MistralSandboxQuotaExceededError"
KOYEB_SANDBOX_DEPLOYMENT_FAILED_ERROR_TYPE = "KoyebSandboxDeploymentFailedError"
SANDBOX_CREATE_REFUSAL_TYPES = frozenset(
    {
        MISTRAL_SANDBOX_ACCESS_DENIED_ERROR_TYPE,
        MISTRAL_SANDBOX_QUOTA_EXCEEDED_ERROR_TYPE,
        KOYEB_SANDBOX_DEPLOYMENT_FAILED_ERROR_TYPE,
    }
)


def cause_chain(error: BaseException) -> Iterator[BaseException]:
    """`error` and its causes, outermost first."""

    seen: set[int] = set()
    current: BaseException | None = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__


def sandbox_create_refusal_error(error: BaseException) -> ApplicationError | None:
    """The refusal behind a failed sandbox create, if `error` comes from one.

    In-process the refusal is `error` itself or its cause. In a Workflow it is the cause of an
    `ActivityError`, possibly under more wrappers.
    """

    for cause in cause_chain(error):
        if isinstance(cause, ApplicationError) and cause.type in SANDBOX_CREATE_REFUSAL_TYPES:
            return cause
    return None


def sandbox_create_refusal(error: BaseException) -> str | None:
    """The reason a sandbox create failed for good, if `error` comes from one."""

    refused = sandbox_create_refusal_error(error)
    return (refused.message or None) if refused is not None else None
