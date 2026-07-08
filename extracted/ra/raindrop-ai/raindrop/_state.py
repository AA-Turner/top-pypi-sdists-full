"""Per-client mutable state for the Raindrop SDK.

The SDK predates the instance-based ``Raindrop`` client: all pipeline state
(write key, buffers, flush thread, partial-event merge tables, ...) lived as
``raindrop.analytics`` module globals, and both tests and host applications
read and assign those globals directly (e.g. ``analytics.max_queue_size =
500`` is documented in the README).

To support multiple independent clients per process WITHOUT changing that
contract, every pipeline function in ``raindrop.analytics`` now reads its
state through an explicit state object:

- ``ClientState`` is a plain attribute bag; each ``raindrop.Raindrop``
  instance owns one, giving it isolated buffers, config, and shutdown
  lifecycle.
- ``ModuleBackedState`` is the state of the *default* client behind the
  module-level API. It proxies attribute access straight to the
  ``raindrop.analytics`` module globals, so legacy reads/writes of those
  globals keep observing and steering the default pipeline exactly as
  before.
"""

from __future__ import annotations

import sys
import threading
import weakref
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:  # pragma: no cover - import cycle guard, typing only
    from raindrop.models import PartialTrackAIEvent

# Names that constitute pipeline state. Every one of these exists as a
# ``raindrop.analytics`` module global (the default client's storage) and as
# an attribute of ``ClientState`` (per-instance storage). Keep the two in
# sync when adding state.
STATE_FIELDS = (
    "write_key",
    "project_id",
    "_wizard_session",
    "api_url",
    "local_workshop_url",
    "max_queue_size",
    "max_text_field_chars",
    "upload_size",
    "upload_interval",
    "buffer",
    "flush_lock",
    "redact_pii",
    "_tracing_enabled",
    "_bypass_otel_for_tools",
    "flush_thread",
    "shutdown_event",
    "_direct_tool_spans_buffer",
    "_partial_buffers",
    "_partial_timers",
    "_partial_flush_queue",
    "_shutdown_deadline",
    "INTERACTION_TRACE_ID_REGISTRY",
    "INTERACTION_EVENT_ID_REGISTRY",
)


class ClientState:
    """Isolated pipeline state for one ``Raindrop`` client instance."""

    __slots__ = STATE_FIELDS + ("auth_hint", "client_ref")

    def __init__(self) -> None:
        self.write_key: str | None = None
        self.project_id: str | None = None
        self._wizard_session: str | None = None
        self.api_url: str = "https://api.raindrop.ai/v1/"
        self.local_workshop_url: str | None = None
        self.max_queue_size: int = 10_000
        # None = inherit the process-wide default (the raindrop.analytics
        # module global, settable via module init()); an int overrides the
        # per-field text cap for THIS client only.
        self.max_text_field_chars: int | None = None
        self.upload_size: int = 10
        self.upload_interval: float = 1.0
        self.buffer: list = []
        self.flush_lock = threading.Lock()
        self.redact_pii: bool = False
        self._tracing_enabled: bool = False
        self._bypass_otel_for_tools: bool = False
        self.flush_thread: threading.Thread | None = None
        self.shutdown_event = threading.Event()
        self._direct_tool_spans_buffer: list[dict[str, Any]] = []
        self._partial_buffers: dict[str, "PartialTrackAIEvent"] = {}
        self._partial_timers: dict[str, threading.Timer] = {}
        self._partial_flush_queue: list["PartialTrackAIEvent"] = []
        self._shutdown_deadline: float | None = None
        self.INTERACTION_TRACE_ID_REGISTRY: "weakref.WeakValueDictionary[int, Any]" = (
            weakref.WeakValueDictionary()
        )
        self.INTERACTION_EVENT_ID_REGISTRY: "weakref.WeakValueDictionary[str, Any]" = (
            weakref.WeakValueDictionary()
        )
        # Non-reversible identity of this client's write key (first 8 hex
        # chars of its SHA-256). Stamped on spans produced in this client's
        # context so the export guard can drop spans that would otherwise
        # ride a different org's exporter credential. None when no key.
        self.auth_hint: str | None = None
        # Weak ref to the owning Raindrop client. The background flush loop
        # uses it to detect a garbage-collected client and exit (after a
        # final drain) instead of spinning forever on a dead pipeline.
        self.client_ref: "weakref.ref | None" = None


class ModuleBackedState:
    """State view whose storage is the ``raindrop.analytics`` module globals.

    The default (module-level) client uses this so that the long-standing
    contract — tests and host apps reading/assigning ``analytics.buffer``,
    ``analytics.write_key``, ``analytics.max_queue_size``, ... — keeps
    steering the default pipeline. Attribute access is resolved on EVERY
    read, so an assignment like ``analytics.write_key = "k"`` is observed
    immediately by in-flight pipeline code.
    """

    __slots__ = ()

    @staticmethod
    def _module() -> Any:
        return sys.modules["raindrop.analytics"]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._module(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._module(), name, value)

    @property
    def auth_hint(self) -> str | None:
        from raindrop._tracing import auth_hint_for_key

        return auth_hint_for_key(getattr(self._module(), "write_key", None))


# What every pipeline function accepts via its ``state`` parameter.
RaindropState = Union[ClientState, ModuleBackedState]
