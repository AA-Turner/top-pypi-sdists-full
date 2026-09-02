from __future__ import annotations

from websockets import ClientConnection, ConnectionClosed, connect
from httpx import URL

from .errors import AuthenticationError


# WebSocket close status codes
class WebSocketStatus:
    NORMAL_CLOSURE = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    NO_STATUS_RECEIVED = 1005
    ABNORMAL_CLOSURE = 1006
    INVALID_FRAME_PAYLOAD_DATA = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXT = 1010
    INTERNAL_SERVER_ERROR = 1011
    INVALID_JSON = 4000
    INVALID_JSON_RPC = 4001


def get_close_code_description(code: int) -> str:
    """Returns a human-readable description for a WebSocket close code."""
    descriptions = {
        WebSocketStatus.NORMAL_CLOSURE: "Normal closure (1000)",
        WebSocketStatus.GOING_AWAY: "Server going away (1001)",
        WebSocketStatus.PROTOCOL_ERROR: "Protocol error (1002)",
        WebSocketStatus.UNSUPPORTED_DATA: "Unsupported data (1003)",
        WebSocketStatus.NO_STATUS_RECEIVED: "No status received (1005)",
        WebSocketStatus.ABNORMAL_CLOSURE: "Abnormal closure (1006)",
        WebSocketStatus.INVALID_FRAME_PAYLOAD_DATA: "Invalid frame payload data (1007)",
        WebSocketStatus.POLICY_VIOLATION: "Policy violation (1008)",
        WebSocketStatus.MESSAGE_TOO_BIG: "Message too big (1009)",
        WebSocketStatus.MANDATORY_EXT: "Mandatory extension (1010)",
        WebSocketStatus.INTERNAL_SERVER_ERROR: "Internal server error (1011)",
        WebSocketStatus.INVALID_JSON: "Invalid JSON (4000)",
        WebSocketStatus.INVALID_JSON_RPC: "Invalid JSON-RPC (4001)",
    }

    if code in descriptions:
        return descriptions[code]
    elif 3000 <= code < 4000:
        return f"Library/framework code ({code})"
    elif 4000 <= code < 5000:
        return f"Application code ({code})"
    else:
        return f"Unknown code ({code})"


class WebSocketTransport:
    def __init__(self, debug: bool = False) -> None:
        self._ws: ClientConnection | None = None
        self._closed = False
        self._debug = debug

    @property
    def closed(self) -> bool:
        return self._closed

    async def connect(self, url: URL, headers: dict[str, str]) -> ClientConnection:
        try:
            ws = await connect(str(url), additional_headers=headers)
            self._ws = ws
            return ws
        except Exception as e:
            if "HTTP 401" in str(e):
                raise AuthenticationError(
                    "Authentication failed, invalid API token"
                ) from e

            raise e

    async def send(self, data: str) -> None:
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")
        await self._ws.send(data)

    async def close(self) -> None:
        self._closed = True

        if self._ws is not None:
            await self._ws.close()

    async def __aexit__(self):
        await self.close()

    async def __aiter__(self):
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")

        try:
            async for message in self._ws:
                yield message
        except ConnectionClosed as e:
            if self._debug:
                # Extract close code and reason from the received close frame
                code = e.rcvd.code if e.rcvd else WebSocketStatus.NO_STATUS_RECEIVED
                reason = e.rcvd.reason if e.rcvd else ""

                if code in (
                    WebSocketStatus.NORMAL_CLOSURE,
                    WebSocketStatus.GOING_AWAY,
                    WebSocketStatus.NO_STATUS_RECEIVED,
                ):
                    # Expected closure (including sandbox timeout)
                    print(f"Sandbox connection closed: {reason or 'server going away'}")
                else:
                    # Unexpected closure
                    code_description = get_close_code_description(code)
                    reason_str = f" ({reason})" if reason else ""
                    print(f"WebSocket closed: {code_description}{reason_str}")
            return
