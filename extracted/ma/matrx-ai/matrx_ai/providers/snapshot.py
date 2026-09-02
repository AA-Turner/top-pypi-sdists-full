"""Per-iteration request-payload snapshot helper.

Each provider builds its final, SDK-ready request dict inside ``execute()``
(typically via ``self.to_provider_config(...)``).  To be able to reproduce
exactly what the model saw, we stash that dict on the active
``ExecutionState`` (the executor's owned per-task scratch slot — never
``AppContext.metadata``, which is shared across concurrent agents).

The executor reads the payload back after ``client.execute()`` returns and
writes the whole thing to ``chat.request_snapshot`` as a side-effect task —
by default for every persisted run (``REQUEST_SNAPSHOT_CAPTURE_DEFAULT``,
D-33), unless the request opted out or is ephemeral (``store=False``).

The capture runs unconditionally (cheap field assignment) so the request-level
gate only controls the *write* path, not the *capture* path.  Callers can flip
the per-request override at request time without any provider-side branching.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from matrx_connect.chat_timing import chat_timing_mark

from matrx_ai.orchestrator.execution_state import try_get_execution_state


def capture_request_payload(
    config_data: Any,
    *,
    provider: str | None = None,
    wire_format: str | None = None,
    debug: bool = False,
) -> None:
    """Store the provider's final request dict on the active ExecutionState.

    Accepts plain dicts and dataclasses (e.g. ``GoogleProviderConfig``).
    Never raises — snapshotting must never interfere with the actual API
    call.  Called once per iteration from each provider's ``execute()``.
    Silent no-op when no executor is active (e.g. a provider used outside
    the orchestrator), which is the right behaviour for tests/scripts.

    Also runs the dumb tool-set observer (``inspect_outbound_payload``)
    on the same payload — a third-party log of whether the SDK is about
    to receive duplicate tool names. Read-only, never alters anything.
    Toggle via ``LOCAL_TOOL_DEBUG`` in ``matrx_ai.tools.validate``.

    Optional debug pretty-print
    ---------------------------
    When ``debug=True`` AND ``provider`` is given, this also emits a
    human-readable per-provider rendering via
    ``matrx_ai.providers.debug_pretty_print.format_provider_payload``.
    The pretty-print is a fully separate code path from the snapshot
    capture — it cannot affect ``state.snapshot_payload`` and never
    raises (any exception is swallowed). Keeping the kwargs default to
    ``None``/``False`` means every existing caller is a no-op.
    """
    from matrx_utils import vcprint

    # vcprint(config_data, "[CAPTURE REQUEST PAYLOAD] Full Config Data", color="pink")
    # _outer_type = type(config_data).__name__
    # vcprint(_outer_type, "[CAPTURE REQUEST PAYLOAD] config_data type", color="pink")
    # _msgs = (
    #     config_data.get("messages")
    #     if isinstance(config_data, dict)
    #     else getattr(config_data, "messages", None)
    # )
    # _msgs_type = type(_msgs).__name__
    # vcprint(_msgs_type, "[CAPTURE REQUEST PAYLOAD] messages type", color="pink")
    try:
        state = try_get_execution_state()
        if state is None:
            return
        payload: Any
        if dataclasses.is_dataclass(config_data) and not isinstance(config_data, type):
            payload = dataclasses.asdict(config_data)
        else:
            payload = config_data
        state.snapshot_payload = payload
        # Stamp the provider alongside the payload — same seam, same call, so
        # the two can never disagree. The snapshot writer reads this rather
        # than guessing from response metadata (which carries no provider key).
        if provider:
            state.snapshot_provider = provider
    except Exception:
        pass

    # Pre-flight observer — same payload that's about to hit the SDK.
    # Imported lazily so the module's no-op path stays cheap and so a
    # broken validator can never break snapshot capture.
    try:
        from matrx_ai.tools.validate import inspect_outbound_payload

        chat_timing_mark("payload_captured", "provider payload captured — SDK call next")
        inspect_outbound_payload(config_data)
    except Exception:
        pass

    # Opt-in human-readable per-provider rendering. Defaults to off so
    # legacy call sites (no kwargs) get the existing behaviour exactly.
    # The formatter NEVER raises — any failure here is swallowed so a
    # broken debug path can never break the request path.
    if debug and provider:
        try:
            from matrx_ai.providers.debug_pretty_print import format_provider_payload

            vcprint(
                format_provider_payload(provider, config_data, wire_format=wire_format),
                title=f"[DEBUG_PRETTY_PRINT] {provider}",
                color="cyan",
            )
        except Exception:
            pass
