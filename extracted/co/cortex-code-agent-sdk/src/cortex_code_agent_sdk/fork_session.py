"""Top-level fork_session() helper — mirrors the TS SDK's forkSession().

Forks `session_id` into a durable new session/thread. CLI mode uses resume +
fork flags; API mode treats `session_id` as the source Agent API thread ID and
creates a fresh thread from a snapshot artifact. The new session ID is extracted
from the `system init` event and returned.

Usage:
    new_session_id = await fork_session(
        source_session_id,
        base_options=options,
        up_to_message_id="msg-uuid-at-fork-point",
    )
"""

from __future__ import annotations

from dataclasses import replace

from ._internal.transport.api import should_use_api_mode
from .client import CortexCodeSDKClient
from .types import CortexCodeAgentOptions, SystemMessage


async def fork_session(
    session_id: str,
    base_options: CortexCodeAgentOptions | None = None,
    *,
    up_to_message_id: str | None = None,
) -> str:
    """Fork a session into a new branch with a fresh session ID.

    Forks ``session_id`` into a durable new session/thread. CLI mode resumes
    with ``fork_session``; API mode creates a fresh Agent API thread from a
    snapshot artifact. The new session ID is extracted from the ``system init``
    event and returned.

    Args:
        session_id: UUID of the source session to fork from.
        base_options: Session options (cwd, model, connection, etc.) for the
            fork operation. Fork-specific fields are set internally and will
            be overridden if present.
        up_to_message_id: Optional message UUID to fork from. When provided,
            only messages up to and including that UUID are copied into the
            fork (branch from a specific point in the conversation).

    Returns:
        The ID of the newly created forked session/thread.

    Raises:
        RuntimeError: If the session did not emit a ``system init`` event with a
            ``session_id`` before exiting.

    Example::

        new_id = await fork_session(
            "original-session-uuid",
            base_options=CortexCodeAgentOptions(connection="snowhouse"),
            up_to_message_id="msg-uuid-at-fork-point",
        )
        # Resume the fork
        async for message in query(
            prompt="...",
            options=CortexCodeAgentOptions(resume=new_id),
        ):
            ...
    """
    if base_options is None:
        base_options = CortexCodeAgentOptions()

    if should_use_api_mode(base_options):
        fork_options = replace(
            base_options,
            session_id=session_id,
            fork_session=True,
            resume_session_at=up_to_message_id if up_to_message_id else None,
        )
    else:
        fork_options = replace(
            base_options,
            resume=session_id,
            fork_session=True,
            resume_session_at=up_to_message_id if up_to_message_id else None,
        )

    new_session_id: str | None = None
    client = CortexCodeSDKClient(options=fork_options)
    try:
        await client.connect()
        async for message in client.receive_messages():
            if (
                isinstance(message, SystemMessage)
                and message.subtype == "init"
            ):
                candidate = getattr(message, "session_id", None)
                if candidate is None:
                    candidate = message.data.get("session_id")
                if isinstance(candidate, str) and candidate:
                    new_session_id = candidate
                    break
    finally:
        await client.disconnect()

    if not new_session_id:
        raise RuntimeError(
            "fork_session: session did not return a session_id in the init message"
        )
    return new_session_id
