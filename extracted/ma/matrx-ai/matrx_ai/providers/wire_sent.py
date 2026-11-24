"""The ONE home of the "request reached the wire" stamp: set at the TRANSPORT (cost adversary pass 7, P7 + P8).

``errors.stamp_request_sent_on_failure`` (the model funnel) keeps a tracker; an exception escaping after the tracker
says "sent" is stamped ``was_request_sent`` and a host books its cost as unknown (catalog price, or filed). Until pass 7
the tracker was set by ``snapshot.capture_request_payload``, BEFORE the SDK call, so:

* P7 (charged for nothing): google-genai validates a request client-side (pydantic) after the snapshot and before any
  connection; that ValidationError was stamped "sent" and booked at the catalog price.
* P8 (money lost): openai / xai / groq speech never ran the snapshot, so a ValueError raised after a BILLED speech call
  carried no stamp and was booked free and filed nowhere.

Here the tracker is set where the request actually leaves the process, for every SDK by construction:

* ``httpx`` and ``httpx2`` ``Client`` / ``AsyncClient._send_single_request`` (the transport hand-off, after the request
  event hooks; every OpenAI-built, Anthropic, Groq, Cerebras, Together and google-genai sync client).
* ``aiohttp.ClientSession._request`` (google-genai's async path when aiohttp is installed).
* ``grpc.aio`` multi-callables (xai_sdk): a gRPC call is noted when it is handed to the channel.

An HTTP request is SENT when the transport returned a response, or raised anything but a never-connected error
(connect error / connect timeout / pool timeout / bad URL): those raise before the first request byte goes out.

Only PROVIDER requests count: a request issued while a provider SDK frame is on the stack (``PROVIDER_SDK_MODULES``),
or on a client marked with ``mark_provider_client`` (``outbound_capture.make_capture_http_client``, our raw provider
call sites). A media fetch or a database read inside the funnel before the provider call is not a send.

``install_wire_sent_hooks`` is idempotent and runs from ``stamp_request_sent_on_failure`` itself, so a tracker can
never exist without the hooks. Outside a tracker every hook is one ContextVar read. Never raises into the call.
"""

from __future__ import annotations

import functools
import sys
from typing import Any

#: Top-level packages (and our own raw-HTTP provider modules) whose frames make an outbound request a provider send.
PROVIDER_SDK_MODULES: tuple[str, ...] = (
    "openai",
    "anthropic",
    "groq",
    "google.genai",
    "together",
    "cerebras",
    "replicate",
    "elevenlabs",
    "huggingface_hub",
    "xai_sdk",
    "cohere",
    "mistralai",
    "fal_client",
    "matrx_ai.providers.typesafe",
    "matrx_ai.providers.fastino",
)

_PROVIDER_CLIENT_ATTR = "_matrx_provider_client"
_INSTALLED_ATTR = "_matrx_wire_sent_wrapped"
_installed = False

# Never-connected transport errors: raised before any request byte left the process.
_NEVER_SENT_NAMES = ("ConnectError", "ConnectTimeout", "PoolTimeout", "UnsupportedProtocol", "InvalidURL")


def mark_provider_client(client: Any) -> Any:
    """Mark ``client`` as a provider client: every request it sends counts as a provider send. Returns it."""
    try:
        setattr(client, _PROVIDER_CLIENT_ATTR, True)
    except Exception:  # noqa: BLE001 — a slotted client is still counted by its SDK frames
        pass
    return client


def _tracking() -> list[bool] | None:
    from matrx_ai.providers.errors import _REQUEST_SENT_TRACKER

    holder = _REQUEST_SENT_TRACKER.get()
    if holder is None or holder[0]:
        return None  # outside a funnel, or already sent: nothing to decide
    return holder


def _module_matches(name: str) -> bool:
    return any(name == m or name.startswith(m + ".") for m in PROVIDER_SDK_MODULES)


def _is_provider_request(client: Any) -> bool:
    if getattr(client, _PROVIDER_CLIENT_ATTR, False):
        return True
    frame = sys._getframe(1)
    while frame is not None:
        if _module_matches(str(frame.f_globals.get("__name__", ""))):
            return True
        frame = frame.f_back
    return False


def _never_sent_classes() -> tuple[type[BaseException], ...]:
    from matrx_ai.providers.http_flavors import transport_classes

    found: list[type[BaseException]] = list(transport_classes(*_NEVER_SENT_NAMES))
    try:
        import aiohttp

        found += [aiohttp.ClientConnectorError, aiohttp.InvalidURL]
    except Exception:  # noqa: BLE001 — aiohttp is optional
        pass
    return tuple(found)


def _wrap_async_send(original: Any) -> Any:
    @functools.wraps(original)
    async def send(self: Any, *args: Any, **kwargs: Any) -> Any:
        holder = _tracking()
        if holder is None or not _is_provider_request(self):
            return await original(self, *args, **kwargs)
        try:
            response = await original(self, *args, **kwargs)
        except BaseException as exc:
            if not isinstance(exc, _never_sent_classes()):
                holder[0] = True
            raise
        holder[0] = True
        return response

    setattr(send, _INSTALLED_ATTR, True)
    return send


def _wrap_sync_send(original: Any) -> Any:
    @functools.wraps(original)
    def send(self: Any, *args: Any, **kwargs: Any) -> Any:
        holder = _tracking()
        if holder is None or not _is_provider_request(self):
            return original(self, *args, **kwargs)
        try:
            response = original(self, *args, **kwargs)
        except BaseException as exc:
            if not isinstance(exc, _never_sent_classes()):
                holder[0] = True
            raise
        holder[0] = True
        return response

    setattr(send, _INSTALLED_ATTR, True)
    return send


def _wrap_grpc_call(original: Any) -> Any:
    @functools.wraps(original)
    def call(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = original(self, *args, **kwargs)
        holder = _tracking()
        if holder is not None:
            holder[0] = True  # the RPC is handed to the channel
        return result

    setattr(call, _INSTALLED_ATTR, True)
    return call


def _patch(cls: Any, name: str, wrapper: Any) -> None:
    original = getattr(cls, name, None)
    if original is None or getattr(original, _INSTALLED_ATTR, False):
        return
    setattr(cls, name, wrapper(original))


def install_wire_sent_hooks() -> None:
    """Install the transport stamp on every installed transport flavor. Idempotent; never raises."""
    global _installed
    if _installed:
        return
    _installed = True
    try:
        from matrx_ai.providers.http_flavors import HTTPX_FLAVORS

        for flavor in HTTPX_FLAVORS:
            _patch(flavor.AsyncClient, "_send_single_request", _wrap_async_send)
            _patch(flavor.Client, "_send_single_request", _wrap_sync_send)
    except Exception:  # noqa: BLE001
        pass
    try:
        import aiohttp

        _patch(aiohttp.ClientSession, "_request", _wrap_async_send)
    except Exception:  # noqa: BLE001 — aiohttp is optional
        pass
    try:
        from grpc.aio import _channel as grpc_aio_channel

        for name in ("UnaryUnaryMultiCallable", "UnaryStreamMultiCallable", "StreamUnaryMultiCallable",
                     "StreamStreamMultiCallable"):
            _patch(getattr(grpc_aio_channel, name), "__call__", _wrap_grpc_call)
    except Exception:  # noqa: BLE001 — grpc is optional
        pass


def wire_sent_seams() -> dict[str, bool]:
    """Which transport seams carry the stamp (a drift test reads this: a renamed private method fails loudly)."""
    install_wire_sent_hooks()
    seams: dict[str, bool] = {}
    from matrx_ai.providers.http_flavors import HTTPX_FLAVORS

    for flavor in HTTPX_FLAVORS:
        for cls in (flavor.AsyncClient, flavor.Client):
            seams[f"{flavor.__name__}.{cls.__name__}._send_single_request"] = getattr(
                getattr(cls, "_send_single_request", None), _INSTALLED_ATTR, False
            )
    try:
        import aiohttp

        seams["aiohttp.ClientSession._request"] = getattr(aiohttp.ClientSession._request, _INSTALLED_ATTR, False)
    except ImportError:
        pass
    try:
        from grpc.aio import _channel as grpc_aio_channel

        seams["grpc.aio.UnaryUnaryMultiCallable.__call__"] = getattr(
            grpc_aio_channel.UnaryUnaryMultiCallable.__call__, _INSTALLED_ATTR, False
        )
        seams["grpc.aio.UnaryStreamMultiCallable.__call__"] = getattr(
            grpc_aio_channel.UnaryStreamMultiCallable.__call__, _INSTALLED_ATTR, False
        )
    except ImportError:
        pass
    return seams
