import asyncio
from typing import Callable, TypeVar

from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.exceptions import WorkflowError

logger = get_logger(__name__)

T = TypeVar("T")

# A mounted token can briefly be empty/unreadable while the kubelet rotates it, and the credential readers
# raise retryable errors, so a blip shouldn't abort startup.
CREDENTIALS_STARTUP_READ_ATTEMPTS = 3
CREDENTIALS_STARTUP_READ_BACKOFF_SECONDS = 1.0


async def read_credential_at_startup(read: Callable[[], T], credential: str) -> T:
    """Read a mounted credential at startup, retrying transient mount failures."""
    for attempt in range(1, CREDENTIALS_STARTUP_READ_ATTEMPTS + 1):
        try:
            return read()
        except WorkflowError as exc:
            if attempt == CREDENTIALS_STARTUP_READ_ATTEMPTS:
                raise
            logger.warning(
                "failed to read credential at startup; retrying",
                credential=credential,
                attempt=attempt,
                **extract_error_context(exc),
            )
            await asyncio.sleep(CREDENTIALS_STARTUP_READ_BACKOFF_SECONDS)
    raise AssertionError("unreachable")
