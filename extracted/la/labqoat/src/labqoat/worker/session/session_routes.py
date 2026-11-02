"""The local transport accelerates a narrow set of existing worker operations."""

from typing import ClassVar


class SessionRoutes:
    """Keep large asset and telemetry uploads on their existing streaming data paths."""

    routes: ClassVar[dict[str, str]] = {
        "/api/v1/worker/assignments/begin": "begin",
        "/api/v1/worker/assignments/finish": "finish",
        "/api/v1/worker/assignments/heartbeat": "heartbeat",
        "/api/v1/worker/runs/batch": "submit",
    }

    @staticmethod
    def operation(method: str, path: str) -> str | None:
        """Map only exact POST routes; arbitrary URLs cannot gain session authority."""
        return SessionRoutes.routes.get(path) if method == "POST" else None
