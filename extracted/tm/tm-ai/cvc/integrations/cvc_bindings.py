"""
CVC-internal glue for channel adapters.

This module is intentionally thin — it provides the canonical
*signatures* for the commit hook and agent runner the channel
registry expects, plus concrete factory functions that the gateway
wires in once the runtime is up.

  - :func:`build_commit_hook` — every inbound channel message becomes
    a CVC cognitive commit. This is the **time machine** guarantee:
    the user's message is preserved in the Merkle DAG before the
    agent ever sees it. If the agent crashes or lies later, the
    conversation is still recoverable.

  - :func:`build_agent_runner` — forwards channel messages into the
    live gateway chat pipeline (the same one the dashboard uses).

  - :func:`make_logging_commit_hook` / :func:`make_echo_agent_runner`
    — fallbacks used during early bootstrap / unit tests. The gateway
    swaps them out for the real factories in the lifespan.

Both real builders lazily import the heavy CVC machinery so that
channels stay importable in unit tests without dragging FastAPI / git
in.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, Optional

from .channels.base import InboundMessage


logger = logging.getLogger(__name__)


# Type aliases — match exactly what ChannelRegistry expects.
CommitHook = Callable[[InboundMessage, str], Awaitable[Optional[str]]]
AgentRunner = Callable[[InboundMessage], Awaitable[Optional[str]]]


# ─────────────────────────────────────────────────────────────────────────────
# Fallback factories — used in unit tests and during early bootstrap.
# ─────────────────────────────────────────────────────────────────────────────


def make_logging_commit_hook() -> CommitHook:
    """Fallback commit hook used in unit tests and during early bootstrap.

    Doesn't touch CVC's engine; just records the inbound into the
    registry's last_activity_at and logs the would-be commit hash so
    you can see channel traffic flowing. Replace with :func:`build_commit_hook`
    once the engine is booted.
    """

    counter = {"n": 0}

    async def _hook(msg: InboundMessage, prompt: str) -> Optional[str]:
        counter["n"] += 1
        h = f"log-{msg.channel}-{counter['n']:06d}"
        logger.info(
            "logging_commit_hook: would commit %s — chat=%s user=%s text=%d chars",
            h, msg.chat_id, msg.user_name or msg.user_id, len(msg.text),
        )
        return h

    return _hook


def make_echo_agent_runner() -> AgentRunner:
    """Fallback agent runner used in unit tests and during early bootstrap.

    Just echoes the inbound back. Replace with :func:`build_agent_runner`
    once the gateway chat pipeline is ready.
    """

    async def _runner(msg: InboundMessage) -> Optional[str]:
        return (
            f"👋 CVC echo ({msg.channel}): received your message in "
            f"{len(msg.text)} chars. The real agent pipeline will replace "
            f"this stub once the gateway finishes bootstrapping."
        )

    return _runner


# ─────────────────────────────────────────────────────────────────────────────
# Real implementations — wired by the gateway after the runtime is up.
# ─────────────────────────────────────────────────────────────────────────────


def build_commit_hook(workspace_path: Optional[str] = None) -> CommitHook:
    """Build a real commit hook bound to the CVC engine.

    The hook creates a transient commit for every inbound message —
    the user's words go into the Merkle DAG BEFORE the agent runs.
    The agent's eventual reply is added as a follow-up commit by the
    gateway chat pipeline.

    If the engine can't be initialised, returns the fallback logging
    hook so channels still work; the time-machine guarantee is lost
    for that one message but the user-facing UX is preserved.
    """
    try:
        from cvc.operations.engine import (
            CVCEngine,
            CVCCommitRequest,
        )
        from cvc.core.models import CVCConfig, ContextMessage
        from cvc.core.database import ContextDatabase
    except Exception as exc:  # noqa: BLE001
        logger.warning("build_commit_hook: engine import failed, using fallback: %s", exc)
        return make_logging_commit_hook()

    async def _hook(msg: InboundMessage, prompt: str) -> Optional[str]:
        try:
            ws = workspace_path or _default_workspace()
            config = CVCConfig.for_project(project_root=_path(ws) if ws else None)
            config.ensure_dirs()
            db = ContextDatabase(config)
            eng = CVCEngine(config, db)
            # Push the inbound as a user message into the context window.
            # Note: we set role="user" and stash the channel in `name` so
            # the agent can still see where it came from when it later
            # loads the conversation history.
            eng.push_message(ContextMessage(
                role="user",
                content=f"Inbound from {msg.channel} ({msg.user_name or msg.user_id}):\n{prompt}",
                name=msg.channel,
            ))
            response = eng.commit(
                CVCCommitRequest(
                    message=f"channel-inbound/{msg.channel}/{msg.chat_id}",
                )
            )
            if not response.success:
                logger.warning(
                    "build_commit_hook: commit returned failure: %s",
                    response.message,
                )
                return None
            return response.commit_hash
        except Exception as exc:  # noqa: BLE001
            logger.warning("build_commit_hook: commit failed: %s", exc)
            return None

    return _hook


def build_agent_runner(workspace_path: Optional[str] = None) -> AgentRunner:
    """Build a real agent runner that forwards channel messages into the
    CVC gateway chat pipeline (the same one the dashboard uses).

    Opens a transient session per inbound, pushes the message, waits
    for the agent's final reply, and returns the reply text. If the
    pipeline is unavailable, returns the fallback echo runner.
    """
    try:
        # Lazy import — the gateway chat pipeline pulls in fastapi,
        # git, etc. We don't want unit tests to require those.
        from cvc.gateway.chat import run_chat_turn  # type: ignore
    except Exception as exc:  # noqa: BLE001
        logger.warning("build_agent_runner: gateway import failed, using fallback: %s", exc)
        return make_echo_agent_runner()

    async def _runner(msg: InboundMessage) -> Optional[str]:
        try:
            return await run_chat_turn(
                workspace_path=workspace_path,
                channel=msg.channel,
                chat_id=msg.chat_id,
                user_id=msg.user_id,
                user_name=msg.user_name,
                thread_id=msg.thread_id,
                text=msg.text,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("build_agent_runner: chat turn crashed")
            return f"⚠️ CVC chat turn failed: {exc}"

    return _runner


def _path(p: str | None) -> Path | None:
    """Convert a string to a Path if non-empty, else None."""
    if not p:
        return None
    return Path(p)


def _default_workspace() -> str:
    """Best-effort default workspace path for the commit hook."""
    try:
        from cvc.workspace_manager import WorkspaceManager
        loaded = WorkspaceManager.load_active_workspace()
        return str(loaded) if loaded else ""
    except Exception:
        try:
            return str(__import__("pathlib").Path.cwd())
        except Exception:
            return ""
