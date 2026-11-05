"""The user a Session runs for, as the Workflows platform attests it.

Anyone allowed to start a Session Workflow writes its whole start input, so the worker never takes
the caller from it. The Workflows API mints an executor identity token only for the user who
started this on-behalf-of execution, and only to the worker serving it.
"""

import base64
import json
from datetime import timedelta

from temporalio.exceptions import ApplicationError

import mistralai.workflows as workflows
from mistralai.vibe_agents import session_workflow as wire
from mistralai.workflows.core.config.config import config as workflows_config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.worker_client.errors import SDKError

SESSION_CALLER_UNAVAILABLE_ERROR_TYPE = "SessionCallerUnavailable"


# Every run resolves its caller, so a short Workflows API or Albe outage must not end a long Session:
# with Temporal's default 1 s initial and 100 s maximum interval, 9 attempts back off for about 4 minutes.
@workflows.activity(retry_policy_max_attempts=9, start_to_close_timeout=timedelta(seconds=30))
async def resolve_session_caller() -> wire.Principal:
    context = retrieve_context()
    if context is None or not context.execution_token or not context.on_behalf_of:
        raise _caller_unavailable("The Session's caller is attested only for an on-behalf-of Workflow execution")
    try:
        async with get_worker_client(headers=workflows_config.worker.mistral_api_headers) as client:
            response = await client.executor_identity_token_async(execution_token=context.execution_token)
    except SDKError as error:
        # A run with no user, an unknown execution token (the worker registers it before the Workflow
        # runs), a worker the deployment does not let act for that user, or an execution that is no
        # longer running gets the same answer on every attempt.
        if error.status_code in (400, 403, 404, 409):
            raise _caller_unavailable(f"The Workflows API refused to attest the Session's caller: {error}") from None
        raise
    return _principal_from_identity_token(response.token)


def _principal_from_identity_token(token: str) -> wire.Principal:
    # shortcut: parses Albe's kazekit Session claim from the identity token; replace when abraxas
    # ExecutorIdentityTokenResponse returns the identity fields.
    # The Workflows API handed this token to the worker's own credential, so its claims are read, not
    # verified.
    try:
        payload = token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        return wire.Principal.model_validate(claims["data"])
    except (IndexError, KeyError, TypeError, ValueError):
        raise _caller_unavailable("The executor identity token does not name a complete identity") from None


def _caller_unavailable(message: str) -> ApplicationError:
    return ApplicationError(message, type=SESSION_CALLER_UNAVAILABLE_ERROR_TYPE, non_retryable=True)
