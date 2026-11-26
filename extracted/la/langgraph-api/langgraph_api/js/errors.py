from collections.abc import Mapping
from typing import Any


class RemoteException(Exception):
    error: str

    def __init__(
        self, error: str, *args: object, details: Mapping[str, Any] | None = None
    ) -> None:
        super().__init__(*args)
        self.error = error
        self.details = dict(details or {})

    # Used to nudge the serde to encode like BaseException
    # @see /api/langgraph_api/shared/serde.py:default
    def dict(self):
        return {"error": self.error, "message": str(self), **self.details}
