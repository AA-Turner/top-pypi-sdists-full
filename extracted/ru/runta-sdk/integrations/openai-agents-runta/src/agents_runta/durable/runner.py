from __future__ import annotations

import asyncio
import traceback
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from agents import RunConfig, Runner, RunState, SQLiteSession
from agents.sandbox import Manifest, SandboxRunConfig
from agents.sandbox.session.sandbox_session import SandboxSession
from agents.sandbox.snapshot import SnapshotBase, SnapshotSpec

from agents_runta.sandbox import RuntaSandboxClient, RuntaSandboxClientOptions

from .store import (
    DurablePointerStore,
    DurableSessionNotFoundError,
    DurableSessionRecord,
)


@dataclass
class DurableRunConfig:
    durable_id: str | None = None
    state_dir: str | Path | None = None
    resume: bool = False
    resume_last: bool = False
    force_new: bool = False
    sandbox: bool = True
    sandbox_options: RuntaSandboxClientOptions = field(default_factory=RuntaSandboxClientOptions)
    sandbox_manifest: Manifest | None = None
    sandbox_snapshot: SnapshotSpec | SnapshotBase | None = None
    stop_on_exit: bool = True
    delete_on_success: bool = False


async def run(
    starting_agent: Any,
    input: str | list[Any] | RunState[Any],
    *,
    durable: DurableRunConfig | None = None,
    run_config: RunConfig | None = None,
    context: Any | None = None,
    max_turns: int | None = 10,
    hooks: Any | None = None,
    error_handlers: Any | None = None,
    previous_response_id: str | None = None,
    auto_previous_response_id: bool = False,
    conversation_id: str | None = None,
    runta_client: RuntaSandboxClient | None = None,
) -> Any:
    durable = durable or DurableRunConfig()
    client = runta_client or RuntaSandboxClient()
    store = DurablePointerStore(durable.state_dir)
    record = _load_or_create_record(store, durable)

    sqlite_session = SQLiteSession(record.sqlite_session_id, db_path=store.sqlite_path)
    sandbox_session: SandboxSession | None = None

    try:
        record.status = "running"
        record.last_error = None
        store.save(record)

        if durable.sandbox:
            sandbox_session = await _resolve_sandbox_session(client, durable, record)
            record.sandbox_session_state = client.serialize_session_state(sandbox_session.state)
            store.save(record)

        runner_input: str | list[Any] | RunState[Any] = input
        runner_context = context
        if record.run_state_json is not None and not isinstance(input, RunState):
            runner_input = await RunState.from_json(
                starting_agent,
                record.run_state_json,
                context_override=context,
            )
            runner_context = None

        effective_run_config = _with_sandbox(run_config, sandbox_session)
        result = await Runner.run(
            starting_agent,
            runner_input,
            context=runner_context,
            max_turns=max_turns,
            hooks=hooks,
            run_config=effective_run_config,
            error_handlers=error_handlers,
            previous_response_id=previous_response_id,
            auto_previous_response_id=auto_previous_response_id,
            conversation_id=conversation_id,
            session=sqlite_session,
        )

        if sandbox_session is not None:
            record.sandbox_session_state = client.serialize_session_state(sandbox_session.state)

        interruptions = getattr(result, "interruptions", None)
        if interruptions:
            record.status = "interrupted"
            record.run_state_json = result.to_state().to_json()
        else:
            record.status = "completed"
            record.run_state_json = None
        record.last_error = None
        store.save(record)

        return result
    except BaseException as exc:
        if sandbox_session is not None:
            record.sandbox_session_state = client.serialize_session_state(sandbox_session.state)
        record.status = (
            "interrupted"
            if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt, InterruptedError))
            else "failed"
        )
        record.last_error = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": "".join(traceback.format_exception_only(type(exc), exc)).strip(),
        }
        store.save(record)
        raise
    finally:
        if durable.stop_on_exit and sandbox_session is not None:
            try:
                await sandbox_session.stop()
                record.sandbox_session_state = client.serialize_session_state(sandbox_session.state)
                store.save(record)
            except BaseException:
                if record.status == "completed":
                    raise
        if durable.delete_on_success and record.status == "completed" and sandbox_session is not None:
            await client.delete(sandbox_session)
            record.sandbox_session_state = None
            store.save(record)


def _load_or_create_record(
    store: DurablePointerStore,
    config: DurableRunConfig,
) -> DurableSessionRecord:
    if config.force_new:
        return store.create(config.durable_id)
    if config.resume_last:
        return store.load_last()
    if config.resume:
        if config.durable_id is None:
            return store.load_unfinished()
        return store.load(config.durable_id)
    try:
        return store.load_unfinished()
    except DurableSessionNotFoundError:
        pass
    return store.create(config.durable_id)


async def _resolve_sandbox_session(
    client: RuntaSandboxClient,
    config: DurableRunConfig,
    record: DurableSessionRecord,
) -> SandboxSession:
    if record.sandbox_session_state is not None:
        state = client.deserialize_session_state(record.sandbox_session_state)
        return await client.resume(state)
    return await client.create(
        manifest=config.sandbox_manifest,
        snapshot=config.sandbox_snapshot,
        options=config.sandbox_options,
    )


def _with_sandbox(run_config: RunConfig | None, session: SandboxSession | None) -> RunConfig | None:
    if session is None:
        return run_config
    sandbox_config = SandboxRunConfig(session=session)
    if run_config is None:
        return RunConfig(sandbox=sandbox_config)
    return replace(run_config, sandbox=sandbox_config)
