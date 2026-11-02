"""Bound local delegation to the credentials delivered for currently occupied physical slots."""

import secrets
from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class SessionCredentials:
    """Lookup derives the attempt from trusted delivery data rather than authored IPC input."""

    _inputs: dict[str, tuple[str, str]] = field(default_factory=dict, init=False)

    def register(self, envelope: JsonDocument) -> None:
        """Retain only the current invocation's identity and delegated secret."""
        credential = JsonDocument.expect_scalar(envelope["credential_id"], str)
        secret = JsonDocument.expect_scalar(envelope["secret"], str)
        attempt = JsonDocument.expect_scalar(envelope["attempt_id"], str)
        self._inputs[credential] = (secret, attempt)

    def resolve(self, request: JsonDocument) -> str:
        """Reject unregistered credentials and all supervisor-only operations."""
        credential = JsonDocument.expect_scalar(request.get("credential"), str)
        secret = JsonDocument.expect_scalar(request.get("secret"), str)
        known = self._inputs.get(credential)
        if known is None or not secrets.compare_digest(known[0], secret):
            raise WorkerApiError("Local worker session credential is invalid", 401)
        if request.get("op") not in {"begin", "finish", "heartbeat", "telemetry", "submit", "observe"}:
            raise WorkerApiError("Local worker session operation is invalid", 403)
        return known[1]

    def release(self, attempt: str) -> None:
        """Forget local authority only after the authored process and its physical slot are released."""
        self._inputs = {key: value for key, value in self._inputs.items() if value[1] != attempt}
