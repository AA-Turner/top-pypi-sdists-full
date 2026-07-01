"""REST + WebSocket surface for the agentic loop (budget, guardrails, trajectory)."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


def register_loop_routes(app: FastAPI) -> None:
    """Mount /api/loop/* routes on the gateway."""

    from cvc.dashboard import loop_state

    @app.get("/api/loop/state")
    async def loop_state_endpoint() -> Dict[str, Any]:
        return loop_state.snapshot()

    @app.get("/api/loop/config")
    async def loop_config_endpoint() -> Dict[str, Any]:
        from cvc.agent.loop.budget import IterationBudget
        from cvc.agent.loop.compression import CompressionConfig
        from cvc.agent.loop.output_limits import DEFAULT_LIMITS

        cfg = CompressionConfig()
        return {
            "budget": {
                "default_parent_max": IterationBudget.DEFAULT_PARENT_MAX,
                "default_subagent_max": IterationBudget.DEFAULT_SUBAGENT_MAX,
            },
            "compression": {
                "trigger_tokens": getattr(cfg, "trigger_tokens", None),
                "target_ratio": getattr(cfg, "target_ratio", None),
                "keep_recent": getattr(cfg, "keep_recent", None),
            },
            "output_limits": dict(DEFAULT_LIMITS),
            "guardrails": {
                "max_identical_per_turn": 3,
                "max_total_per_turn": 50,
            },
        }

    @app.websocket("/ws/loop")
    async def ws_loop(websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            from cvc.gateway import _get_event_bus
        except Exception:
            await websocket.close(code=1011)
            return

        bus = _get_event_bus()
        sub_id = f"loop-{id(websocket)}"
        sub = bus.subscribe(sub_id, replay=False)
        try:
            await websocket.send_json(
                {"event": "loop.snapshot", "data": loop_state.snapshot()}
            )
            while sub.active:
                try:
                    envelope = await asyncio.wait_for(sub.get(), timeout=4.0)
                    if envelope.event.startswith("loop.") or envelope.event.startswith(
                        "trajectory."
                    ):
                        await websocket.send_json(
                            {
                                "event": envelope.event,
                                "data": envelope.data,
                                "timestamp": envelope.timestamp,
                            }
                        )
                except asyncio.TimeoutError:
                    await websocket.send_json(
                        {"event": "loop.snapshot", "data": loop_state.snapshot()}
                    )
        except WebSocketDisconnect:
            pass
        except Exception:
            logger.debug("Loop WebSocket error", exc_info=True)
        finally:
            try:
                bus.unsubscribe(sub_id)
            except Exception:
                pass
