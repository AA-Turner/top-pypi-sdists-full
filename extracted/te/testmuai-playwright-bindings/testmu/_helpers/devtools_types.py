from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RequestTiming:
    start_ms: float
    ttfb_ms: float | None = None
    duration_ms: float | None = None


@dataclass
class NetworkEntry:
    id: str
    sequence: int
    method: str
    url: str
    domain: str
    path: str
    query_params: dict[str, str]
    resource_type: str
    request_headers: dict[str, str]
    request_body: str | None
    request_body_truncated: bool = False

    response_status: int | None = None
    response_headers: dict[str, str] | None = None
    response_body: str | None = None
    response_body_truncated: bool = False

    timing: RequestTiming | None = None
    failed: bool = False
    failure_reason: str | None = None


@dataclass
class ConsoleEntry:
    sequence: int
    level: str              # "log", "warning", "error", "info", "debug" (normalized)
    text: str               # full message text — NOT truncated, objects resolved via args
    url: str                # source file URL
    line_number: int
    timestamp_ms: float
    is_exception: bool = False
    stack_trace: str | None = None


@dataclass(frozen=True)
class CoreWebVitals:
    lcp_ms: float | None = None
    cls: float | None = None
    inp_ms: float | None = None
    fcp_ms: float | None = None
    ttfb_ms: float | None = None


@dataclass
class CookieEntry:
    name: str
    value: str
    domain: str
    path: str
    expires: float          # epoch seconds, -1 for session cookies
    http_only: bool
    secure: bool
    same_site: str          # "Strict", "Lax", "None"


@dataclass
class ApiCallEntry:
    """One agent-executed API call: unresolved request + binding response.

    `request` carries the PRE-resolution template form ({{secrets.*}} intact) —
    never the resolved request. `response` is the execute_api return verbatim
    (response_body capped by the producer).
    """
    sequence: int
    request: dict
    response: dict


@dataclass
class WebSocketFrame:
    """One captured WebSocket frame. `payload` is the frame text, or base64 when
    `is_binary`. `connection_id` is denormalized onto the frame so queries that
    merge frames across connections keep each frame's origin. `seq` is monotonic
    across all connections (merge order); `frame_index` is per-connection."""
    connection_id: str
    direction: str              # "sent" | "received"
    payload: str
    is_binary: bool = False
    truncated: bool = False
    ts_ms: float = 0.0
    seq: int = 0
    frame_index: int = 0


@dataclass
class WebSocketConnection:
    """One captured WebSocket connection plus its frames. In-memory only."""
    connection_id: str
    url: str
    domain: str
    path: str
    opened_ts_ms: float
    closed_ts_ms: float | None = None
    close_reason: str | None = None
    error: str | None = None
    frames: list[WebSocketFrame] = field(default_factory=list)
    dropped_frames: int = 0


@dataclass
class SSEMessage:
    """One captured Server-Sent Events message. `connection_id` is denormalized
    onto the message so queries that merge messages across connections keep each
    message's origin. `seq` is monotonic across all connections (merge order);
    `message_index` is per-connection (survives ring eviction)."""
    connection_id: str            # denormalized, e.g. "sse_0"
    data: str                     # multi-line `data:` joined with "\n"; may be JSON
    event: str | None = None      # CDP eventName "" or "message" -> None
    id: str | None = None         # last-event-id (inherited per WHATWG; None until first non-NUL id)
    retry: int | None = None      # reconnection time (ms); None unless a valid `retry:` was seen
    transport: str = "eventsource"  # "eventsource" | "fetch" | "xhr" | "other"
    truncated: bool = False
    ts_ms: float = 0.0
    seq: int = 0                  # GLOBAL monotonic across all connections
    message_index: int = 0        # per-connection monotonic (survives ring eviction)


@dataclass
class SSEConnection:
    """One captured SSE connection plus its messages. In-memory only."""
    connection_id: str
    url: str
    domain: str
    path: str
    opened_ts_ms: float
    closed_ts_ms: float | None = None
    error: str | None = None
    transport: str = "eventsource"
    messages: list[SSEMessage] = field(default_factory=list)
    dropped_messages: int = 0
