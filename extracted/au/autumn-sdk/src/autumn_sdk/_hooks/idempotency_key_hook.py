import json
import uuid
from typing import Union

import httpx

from .edge_clients import IDEMPOTENCY_KEY_HEADER, SDK_TRACK_KEY_EXTENSION, is_track_with_caller_key_header
from .types import BeforeRequestContext, BeforeRequestHook


def _is_write_check(operation_id: str, request: httpx.Request) -> bool:
    """A check that deducts, as sent on the wire: `send_event` or a lock."""
    if operation_id != "check":
        return False
    try:
        sent = json.loads(request.content or b"{}")
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(sent, dict) and (sent.get("send_event") is True or sent.get("lock") is not None)


def _keyed_track(request: httpx.Request) -> httpx.Request:
    """A track bound for the edge is keyed by its body's `idempotency_key`, which the edge and the Autumn API both
    claim. A key already in the body is kept (the API takes an empty one as none); otherwise the body is sent with a
    key made here. The key is kept on the call's own request, which every retry starts from, so they all send it."""
    try:
        sent = json.loads(request.content or b"{}")
    except (ValueError, UnicodeDecodeError):
        return request
    if not isinstance(sent, dict) or sent.get("idempotency_key"):
        return request
    key = request.extensions.setdefault(SDK_TRACK_KEY_EXTENSION, str(uuid.uuid4()))
    # The length follows the new body, the host the URL.
    headers = [
        (name, value) for name, value in request.headers.items() if name.lower() not in ("host", "content-length")
    ]
    content = json.dumps({**sent, "idempotency_key": key}).encode()
    return httpx.Request(
        request.method, request.url, headers=headers, content=content, extensions=dict(request.extensions)
    )


class IdempotencyKeyHook(BeforeRequestHook):
    """Under `use_edge`, a write carries an idempotency key: the caller's if set, else one made here once per call.
    Every retry and the edge's fallback resend that same key, so Autumn applies the write once. A write check carries
    it in the Idempotency-Key header; a track bound for the edge carries it in its body. A track the caller keyed by
    header is left as it is: it goes to Autumn alone (EdgeHook)."""

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        if not getattr(hook_ctx.config, "use_edge", False):
            return request
        if hook_ctx.operation_id == "track":
            # Without an edge a track is sent once, to Autumn, and needs no key of the SDK's.
            stays_with_autumn = not getattr(
                hook_ctx.config, "edge_url", None
            ) or is_track_with_caller_key_header(hook_ctx.operation_id, request)
            return request if stays_with_autumn else _keyed_track(request)
        if not _is_write_check(hook_ctx.operation_id, request):
            return request
        # Set on the call's own request, which every retry starts from, so they all send this key.
        request.headers.setdefault(IDEMPOTENCY_KEY_HEADER, str(uuid.uuid4()))
        return request
