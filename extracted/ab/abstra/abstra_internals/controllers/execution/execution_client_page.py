from typing import Callable, Dict

import abstra_internals.interface.contract as contract
from abstra_internals.controllers.execution.connection_protocol import (
    ConnectionProtocol,
)
from abstra_internals.controllers.execution.execution_client import ExecutionClient
from abstra_internals.entities.execution_context import PageContext, Request, Response
from abstra_internals.interface.sdk.user_exceptions import AuthorizationRequired
from abstra_internals.utils import serialize


class PageClient(ExecutionClient):
    context: PageContext
    conn: ConnectionProtocol
    response: Response
    production_mode: bool
    _before_send: "Callable[[], None] | None"
    _streamed: bool

    def __init__(
        self, context: PageContext, conn: ConnectionProtocol, production_mode: bool
    ) -> None:
        self.context = context
        self.conn = conn
        self.response = Response(headers={}, status=200, body="")
        self.production_mode = production_mode
        self._before_send = None
        self._streamed = False

    def handle_failure(self, e: Exception) -> None:
        if isinstance(e, AuthorizationRequired):
            self.set_response(e.status_code, e.message, {})
        else:
            self.set_response(500, "An exception occurred during execution.", {})
        try:
            self.conn.send(self.response)
            close_dto = contract.CloseDTO(exit_status="EXCEPTION", exception=e)
            self._send(contract.ExecutionEndedMessage(close_dto, self.production_mode))
        except (BrokenPipeError, EOFError):
            pass

    def handle_success(self) -> None:
        try:
            if self._before_send:
                self._before_send()
            if not self._streamed:
                self.conn.send(self.response)
            if self.response.status >= 500:
                close_dto = contract.CloseDTO(
                    exit_status="EXCEPTION",
                    exception=Exception(self.response.body),
                )
            else:
                close_dto = contract.CloseDTO(exit_status="SUCCESS")
            self._send(contract.ExecutionEndedMessage(close_dto, self.production_mode))
        except AuthorizationRequired as e:
            self.set_response(e.status_code, e.message, {})
            try:
                self.conn.send(self.response)
                close_dto = contract.CloseDTO(exit_status="EXCEPTION", exception=e)
                self._send(
                    contract.ExecutionEndedMessage(close_dto, self.production_mode)
                )
            except (BrokenPipeError, EOFError):
                pass
        except (BrokenPipeError, EOFError):
            pass

    def send_stream_start(self, status: int, headers: Dict[str, str]) -> None:
        self._streamed = True
        self.conn.send(
            {"__page_stream__": "start", "status": status, "headers": headers}
        )

    def send_stream_chunk(self, data: object) -> None:
        self.conn.send({"__page_stream__": "chunk", "data": data})

    def send_stream_end(self) -> None:
        self.conn.send({"__page_stream__": "end"})

    def send_stream_error(self, error: str) -> None:
        self.conn.send({"__page_stream__": "error", "error": error})

    def set_response(self, status: int, body: str, headers: Dict[str, str]) -> None:
        self.response = Response(
            status=status,
            body=body,
            headers=headers,
        )

    def get_request(self) -> Request:
        return self.context.request

    def handle_start(self, execution_id: str):
        self._send(contract.ExecutionStartedMessage(execution_id))

    def handle_abandoned(self) -> None:
        pass

    def _send(self, msg: contract.Message) -> None:
        str_data = serialize(msg.to_json())
        try:
            self.conn.send(str_data)
        except (EOFError, BrokenPipeError):
            pass
