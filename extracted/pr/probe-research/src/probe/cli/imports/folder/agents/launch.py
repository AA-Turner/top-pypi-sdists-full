"""launch the importing agent: one headless run, and one relaunch without the override when the agent refused it."""

from __future__ import annotations
import threading
import uuid
from pathlib import Path

from probe.cli.imports.folder.agents import agents as registry  # `registry.which_agent`: a patch of the registry reaches the relaunch check
from probe.cli.imports.folder.agents.activity import Activity
from probe.cli.imports.folder.agents.agents import Agent
from probe.cli.imports.folder.agents.argv import _settings_argv
from probe.cli.imports.folder.agents.flags import supported_flags
from probe.cli.imports.folder.agents.launch_once import _launch_once


def launch_agent(
    folder: Path,
    prompt: str,
    *,
    agent: Agent = Agent.CLAUDE,
    workdir: Path | None = None,
    tools: str | None = None,
    model: str | None = None,
    heading: str = "",
    label: str = "",
    timeout: float | None = None,
    stream=None,
    raw_stream=None,
    progress: bool = True,
    total: int = 0,
    session_id: str | None = None,
    resume: str | None = None,
    paint_to=None,
    cancel_event: threading.Event | None = None,
    path_prepend: str | None = None,
    settings=None,
    meter=None,
    on_relaunch=None,
) -> tuple[bool, str]:
    """Run one headless agent over `folder`; `(ok, tail)`. See `_launch_once`.

    `settings` is the import lane's model and effort
    (`import_agent_settings.LaneSettings`), in place of `model`; `meter`
    (`import_agent_settings.Meter`) counts the launch, its tokens or their
    absence, and a refusal, under `settings.lane`. Without them the launch is
    exactly what it was before either existed.

    ONE RELAUNCH, WITHOUT THE OVERRIDE, and only when all three hold: this
    launch carried a model or effort the lane's built-in value would not have
    (env or server); the agent refused THAT setting in its own structured error
    (`_refusal`); and it refused before any tool call or work item (`acted`),
    so nothing it was asked to do has been written. A model one account type
    cannot use is the case this exists for: about four seconds, no output
    tokens. The relaunch runs the lane's built-in settings under a FRESH
    session id (a refused Claude session may already exist under the old one)
    and hands that id to `on_relaunch`, so a caller tracking its session
    follows. Any other failure, or a second one, is returned as always.
    """
    effort = None
    if settings is not None:
        model, effort = settings.model, settings.effort
    options = dict(
        agent=agent, workdir=workdir, tools=tools, heading=heading, label=label,
        timeout=timeout, stream=stream, raw_stream=raw_stream, progress=progress,
        total=total, paint_to=paint_to, cancel_event=cancel_event, path_prepend=path_prepend,
    )
    state = Activity(total=total or 0, sent_effort=effort)
    ok, tail = _launch_once(
        folder, prompt, model=model, effort=effort, session_id=session_id, resume=resume,
        state=state, **options,
    )
    _meter_launch(meter, settings, state)
    if ok or not _relaunchable(agent, settings, state, cancel_event):
        return ok, tail
    if meter is not None:
        meter.rejected(settings.lane)
    fresh = str(uuid.uuid4()) if agent is Agent.CLAUDE and (session_id or resume) else None
    if on_relaunch is not None:
        on_relaunch(fresh)
    fallback = settings.fallback()
    state = Activity(total=total or 0, sent_effort=fallback.effort)
    ok, tail = _launch_once(
        folder, prompt, model=fallback.model, effort=fallback.effort, session_id=fresh,
        resume=None, state=state, **options,
    )
    _meter_launch(meter, settings, state)
    return ok, tail


def _meter_launch(meter, settings, state: Activity) -> None:
    """One started launch into its lane's counts. Never raises: metering is
    observability, and an import must not stop over it."""
    if meter is None or settings is None or not state.started:
        return
    try:
        meter.launched(settings.lane, state.usage)
    except Exception:
        pass


def _carried(agent: Agent, supported: frozenset[str] | None, model, effort) -> dict:
    """What `_settings_argv` would actually put on this binary's argv."""
    args = _settings_argv(agent, supported, model, effort)
    pairs = dict(zip(args[::2], args[1::2]))
    return {"model": pairs.get("-m") or pairs.get("--model"),
            "effort": pairs.get("--effort") or pairs.get("-c")}


def _relaunchable(agent: Agent, settings, state: Activity, cancel_event) -> bool:
    """Whether a failed launch may run again without its override (see
    `launch_agent`): the agent refused a setting this launch carried and the
    lane's built-in value would not have, before doing any work."""
    if settings is None or not state.started or state.acted or state.refused is None:
        return False
    if cancel_event is not None and cancel_event.is_set():
        return False
    binary = registry.which_agent(agent)
    if binary is None:
        return False
    supported = supported_flags(binary, agent)
    fallback = settings.fallback()
    sent = _carried(agent, supported, settings.model, settings.effort)[state.refused]
    return sent is not None and sent != _carried(
        agent, supported, fallback.model, fallback.effort
    )[state.refused]
