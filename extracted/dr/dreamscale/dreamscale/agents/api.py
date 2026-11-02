"""Public managed LLM runs using the SDK's saved account and local journals."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from decimal import Decimal
from pathlib import Path

from dreamscale_transport.llm import Effort, SessionRequest, Speed, ToolReceipt, TurnResult

from dreamscale.config import (
    API_KEY_ENV,
    LEGACY_API_KEY_ENV,
    dreamscale_home,
    env_with_legacy,
    load_config,
)
from dreamscale.model_names import resolve_llm_model

from .client import Gateway
from .runner import RobotAdapter
from .runner import run as run_loop

RunResult = TurnResult | ToolReceipt | None


async def arun(
    adapter: RobotAdapter,
    *,
    model: str,
    instruction: str,
    effort: Effort = "medium",
    speed: Speed = "standard",
    max_cost: Decimal | float | None = None,
    api_key: str | None = None,
    control_plane_url: str | None = None,
    print_fn: Callable[[str], object] = print,
) -> RunResult:
    """Run an attended robot adapter through the managed LLM gateway.

    Uses ``dreamscale login`` credentials or DREAMSCALE_API_KEY by default.
    No provider key is needed. There is no default spending cap; ``max_cost``
    optionally caps credits. Each run uses a new private journal in
    ``~/.dreamscale/llm-runs`` (or DREAMSCALE_HOME).

    The gateway must qualify the adapter profile before admission. The adapter
    must enforce local motion safety and supply measured receipts.
    This function takes ownership of stopping and closing it, including on
    validation errors, admission failure, or cancellation. Cancellation stops
    hardware before gateway cleanup; uncertain motion is never replayed.

    Returns the terminal TurnResult, an uncertain ToolReceipt, or None at the
    100-call run limit. The 30-minute run limit raises TimeoutError. Model
    completion is the model's report, not independent success verification.
    ``print_fn`` receives progress and provider public summaries only.
    """
    gateway = None
    handed_off = False
    try:
        request = SessionRequest(
            model=resolve_llm_model(model),
            profile=adapter.describe(),
            instruction=instruction,
            effort=effort,
            speed=speed,
            max_cost=Decimal(str(max_cost)) if max_cost is not None else None,
        )
        account = load_config()
        key = api_key or env_with_legacy(API_KEY_ENV, LEGACY_API_KEY_ENV) or account.api_key
        if not key:
            raise ValueError("Run dreamscale login before starting a managed LLM task.")
        gateway = Gateway(control_plane_url or account.control_plane_url, key)
        # Use our own safe local identity; server session IDs are not filesystem paths.
        journal_path = dreamscale_home() / "llm-runs" / f"{request.request_id}.jsonl"
        sid = await gateway.create(request)
        handed_off = True
        return await run_loop(adapter, gateway, sid, journal_path, print_fn=print_fn)
    finally:
        try:
            if not handed_off:
                try:
                    await adapter.stop()
                finally:
                    await adapter.close()
        finally:
            if gateway is not None:
                await gateway.aclose()


def run(
    adapter: RobotAdapter,
    *,
    model: str,
    instruction: str,
    effort: Effort = "medium",
    speed: Speed = "standard",
    max_cost: Decimal | float | None = None,
    api_key: str | None = None,
    control_plane_url: str | None = None,
    print_fn: Callable[[str], object] = print,
) -> RunResult:
    """Synchronous counterpart of :func:`arun`; use arun in an async application."""
    _require_sync("arun")
    return asyncio.run(
        arun(
            adapter,
            model=model,
            instruction=instruction,
            effort=effort,
            speed=speed,
            max_cost=max_cost,
            api_key=api_key,
            control_plane_url=control_plane_url,
            print_fn=print_fn,
        )
    )


def run_yam(
    *,
    model: str,
    instruction: str,
    config_path: str | Path | None = None,
    effort: Effort = "medium",
    speed: Speed = "standard",
    max_cost: Decimal | float | None = None,
    max_joint_step: float = 0.15,
    max_joint_velocity: float = 1.0,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], object] = print,
) -> RunResult:
    """Run the configured YAM with the CLI's attended arming, homing and cleanup.

    Uses the configuration saved by ``dreamscale robots yam setup`` and account saved
    by ``dreamscale login``. Confirms workspace readiness before arming; Ctrl+C
    blocks further dispatch and holds measured positions. No default spend cap.
    """
    _require_sync("arun with a RobotAdapter")
    from .yam_cli import run_yam_llm

    return run_yam_llm(
        model=model,
        instruction=instruction,
        config_path=config_path,
        effort=effort,
        speed=speed,
        max_cost=max_cost,
        max_joint_step=max_joint_step,
        max_joint_velocity=max_joint_velocity,
        input_fn=input_fn,
        print_fn=print_fn,
    )


def _require_sync(alternative: str) -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    raise RuntimeError(f"An event loop is running; use dreamscale.agents.{alternative} instead.")
