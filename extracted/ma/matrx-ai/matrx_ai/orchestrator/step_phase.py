"""Emit an agent-step liveness phase from anywhere inside matrx-ai.

THE LIVENESS CONTRACT (``SPEC-workflow-ui-contract`` §5.1) says a step must
show what it is DOING, and that the RUNNER emits it — never a workflow author.
matrx-graph's ``_ActionExecutor`` owns the two bookends (``preparing`` on
entry, ``complete`` on return) because it is the one place every action
converges. The moments in BETWEEN happen deep inside this package, where
there is no ``NodeExecutionContext`` to reach for — a provider retry, a
structured-output validation — so those funnels call :func:`emit_step_phase`,
which finds the live emitter on the ambient ``AppContext`` instead.

The label is folded onto the CLOSED vocabulary by matrx-graph
(``map_agent_step_phase``), the same fold the workflow emitter applies, so
there is exactly one vocabulary and no way to widen it from here.

Best-effort by contract: no emitter, no ``send_phase``, or a throwing emitter
all cost one debug line. Liveness is never load-bearing — a lost marker
changes nothing about execution.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def emit_step_phase(phase: str, emitter: object | None = None) -> None:
    """Announce ``phase`` on ``emitter`` (default: the ambient AppContext's)."""
    from matrx_graph.types.events import map_agent_step_phase

    label = map_agent_step_phase(phase)
    if label is None:
        return
    if emitter is None:
        try:
            from matrx_connect.context.app_context import try_get_app_context

            ctx = try_get_app_context()
        except Exception:  # noqa: BLE001 — no context is a normal script case
            return
        if ctx is None:
            return
        emitter = getattr(ctx, "emitter", None)
    send_phase = getattr(emitter, "send_phase", None)
    if send_phase is None:
        return
    try:
        await send_phase(label)
    except Exception:  # noqa: BLE001 — liveness is never load-bearing
        logger.debug("step phase emit failed (phase=%s)", label, exc_info=True)
