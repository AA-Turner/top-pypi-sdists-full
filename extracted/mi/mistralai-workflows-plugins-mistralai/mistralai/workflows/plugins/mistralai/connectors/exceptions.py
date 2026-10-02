from typing import Any

from temporalio.exceptions import ApplicationError


class ConnectorToolCallError(ApplicationError):
    def __init__(self, connector_id_or_name: str, response: Any = None) -> None:
        super().__init__(
            f"[{connector_id_or_name}] connector tool call failed",
            response,
            type="ConnectorToolCallError",
            non_retryable=True,
        )
