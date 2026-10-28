"""`probe repair`: the install pipeline in repair mode (plan clean-uninstall-reinstall R-T6).

Checks every part of this machine's Probe and fixes what fails, in the
install's own order -- the CLI first, identity before any worker starts:

    cli            the active env (its receipt, its update path's import, the
                   service's start), uv's folder or a dangling link at the
                   tool path, `active.json`, the `probe` command, migration
                   leftovers: `install_pipeline.install_cli` in repair mode (a
                   broken active env is rebuilt in a new generation folder);
                   a pipx install moves to uv's
    keeper         `keeper-off` from an earlier uninstall cleared, the OS
                   keeper and the lifeboat installed, `runtime.json` naming
                   the active env
    identity       the daemon key and the environment's credentials held to
                   the signed-in account (`identity_check`)
    service        running on the active env (restarted onto it)
    integrations   each coding agent's plugins usable, one of each
                   (`integration_repair`)

It ends COMPLETE or INCOMPLETE with the reasons (exit 0 / 1); refused while an
uninstall runs, or without uv (exit 2). `--json` writes the wizard's NDJSON
events (`probe.core.events`). `npx probe-research repair` runs it from the
newest release when the installed CLI is too broken to run it.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from probe.core import events

REFUSED_EXIT = 2
INCOMPLETE_EXIT = 1
#: How long a restarted service gets to answer from the active env.
SERVICE_WAIT_S = 10.0


@dataclass
class Part:
    """One part's outcome."""

    lines: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    skipped: str = ""


def _say(line: str) -> None:
    from probe.cli import tui

    tui.say(line)


def target_version(active: str | None, running: str) -> str:
    """The version a repair rebuilds: the NEWER of the active one and this
    running CLI's -- never a release older than `install_pipeline.MIN_CHECKABLE`
    (0.328.0), whose env the health check cannot judge (it imports
    `probe.core.adopt`): a broken 0.320 is replaced by this release, never
    rebuilt as itself."""
    from probe._shared import handoff

    from probe.cli import install_pipeline

    found = [v for v in (active, running) if handoff.release(v)]
    best = max(found, key=handoff.release) if found else running
    return best if install_pipeline.checkable(best) else running


def repair_cli() -> tuple[Part, object]:
    """The CLI's install. `(part, the install_cli outcome or None)`."""
    from probe import __version__
    from probe._shared import installs

    from probe.cli import bootstrap, install_pipeline

    part = Part()
    foreign = None
    try:
        foreign = install_pipeline.foreign_install()
        if foreign is not None and foreign[0] != "pipx":
            foreign = None  # a pip environment is the person's own (the SDK's): left as it is
        tools = installs.tool_dir()
        active = installs.active(tools)
        if active is None and installs.tool_state(tools) == installs.ToolPath.PLAIN:
            active = installs.tool_env(tools)
        version = target_version(installs.env_version(active) if active is not None else None, __version__)
    except Exception as exc:  # noqa: BLE001
        part.problems.append(f"the CLI's install could not be read: {exc}")
        return part, None
    out = install_pipeline.install_cli(version, mode=install_pipeline.Mode.REPAIR)
    if out.refused:
        part.problems.append(out.refused)
        return part, out
    if out.unmanaged:
        part.skipped = "this machine updates the CLI in place (Windows, or another filesystem): nothing to repair"
        return part, out
    if out.busy:
        part.problems.append(f"{out.busy} (run `probe repair` again when it ends)")
        return part, out
    part.lines.extend(out.lines)
    part.problems.extend(out.problems)
    if out.waiting and not out.ok:
        part.problems.append(f"CLI {version} {install_pipeline.QUIET_SWITCH} ({out.waiting})")
    elif out.waiting:
        part.lines.append(out.waiting)
    if out.ok and foreign is not None:
        part.lines.extend(install_pipeline.migrate_foreign(foreign))
    if out.ok and not out.changed and not out.lines:
        part.lines.append(f"the CLI ({out.version}, {out.env}) works")
    if not out.ok and not part.problems:
        part.problems.append("the CLI did not end up working")
    with_binary = bootstrap._installed_binary()  # noqa: SLF001
    if out.ok and with_binary is None:
        part.problems.append("no `probe` command is on PATH or in ~/.local/bin")
    return part, out


def repair_keeper(cli_out) -> Part:
    """`keeper-off` cleared, the keeper and lifeboat installed, runtime.json."""
    from probe._shared import installs

    from probe.cli import install_pipeline

    part = Part()
    install_pipeline.clear_keeper_off()
    if cli_out is not None and getattr(cli_out, "env", None) is not None and getattr(cli_out, "version", None):
        try:
            from probe.service import client

            if client.write_runtime(str(installs.env_python(cli_out.env)), cli_out.version):
                part.lines.append(f"runtime.json names {cli_out.env} now")
        except Exception as exc:  # noqa: BLE001
            part.problems.append(f"runtime.json could not be written: {exc}")
    try:
        from probe.service import keeper, lifeboat

        said = keeper.install(lifeboat.login_env())
    except Exception as exc:  # noqa: BLE001
        said = f"failed: {exc!r}"
    if said.startswith("failed"):
        part.problems.append(f"the OS keeper and lifeboat: {said}")
    elif said.startswith("not wanted"):
        part.skipped = f"the OS keeper: {said}"
    else:
        part.lines.append(f"the OS keeper and lifeboat: {said}")
    return part


def _hello(version: str) -> dict | None:
    from probe.service import client
    from probe.service.protocol import Client

    conn = client.connect(2.0)
    if conn is None:
        return None
    try:
        return conn.hello(Client.CLI, version)
    except Exception:  # noqa: BLE001
        return None
    finally:
        conn.close()


def _runs_from(hello: dict, env, version: str | None) -> bool:
    import os

    if version and hello.get("service_version") != version:
        return False
    found = hello.get("env")
    if env is None or not isinstance(found, str):
        return True
    return os.path.realpath(found) == os.path.realpath(str(env))


def repair_service(cli_out) -> Part:
    """The Probe service, running on the active env: restarted onto it when it
    runs another (a rebuilt generation, an older version)."""
    from probe.service import client
    from probe.service.protocol import Client, Method

    part = Part()
    env = getattr(cli_out, "env", None)
    version = getattr(cli_out, "version", None) or ""
    try:
        hello = _hello(version)
        if hello is not None and not _runs_from(hello, env, version):
            try:
                client.call(Method.STOP, client=Client.CLI, client_version=version)
            except client.ServiceError as exc:
                part.lines.append(f"the Probe service runs {hello.get('service_version')} and could not stop now "
                                  f"({exc.message}); it starts on {version} next time")
                return part
            except OSError:
                pass
            deadline = time.monotonic() + SERVICE_WAIT_S
            while time.monotonic() < deadline and _hello(version) is not None:
                time.sleep(0.1)
            part.lines.append(f"stopped the Probe service on {hello.get('service_version')} "
                              f"({hello.get('env') or '?'})")
            hello = None
        if hello is None:
            outcome = client.ensure(wait=SERVICE_WAIT_S)
            if outcome == client.Ensured.CONFINED:
                part.skipped = "the Probe service is not started from a confined process (it starts outside)"
                return part
            hello = _hello(version)
            if hello is None:
                part.problems.append(f"the Probe service did not start ({outcome}); see `probe service status`")
                return part
            part.lines.append(f"the Probe service runs {hello.get('service_version')}")
        elif not part.lines:
            part.lines.append(f"the Probe service runs {hello.get('service_version')}")
        if not _runs_from(hello, env, version):
            part.problems.append(f"the Probe service runs {hello.get('service_version')} from {hello.get('env')}, "
                                 f"not {version} from {env}")
    except Exception as exc:  # noqa: BLE001
        part.problems.append(f"the Probe service could not be checked: {type(exc).__name__}: {exc}")
    return part


def repair_identity() -> Part:
    from probe.cli import identity_check

    report = identity_check.reconcile()
    return Part(lines=list(report.lines), problems=list(report.problems))


def repair_integrations(sources: list[str]) -> dict:
    from probe.cli import integration_repair

    # A plugin the person disabled is theirs to turn back on (`probe wizard`):
    # reported, never re-enabled here.
    return {source: integration_repair.repair(source, enable_disabled=False) for source in sources}


def _agents() -> list[str]:
    try:
        from probe.cli import setup as wizard

        return list(wizard.detectable_sources())
    except Exception:  # noqa: BLE001
        return []


def _step(name, part: Part, *, agent: str | None = None) -> None:
    if part.problems:
        events.step(name, events.Status.FAILED, "; ".join(part.problems), agent=agent)
    elif part.skipped:
        events.step(name, events.Status.DONE, part.skipped, agent=agent)
    else:
        events.step(name, events.Status.DONE, "; ".join(part.lines), agent=agent)


def run(*, json_output: bool = False) -> int:
    """`probe repair`. The exit status: 0 complete, 1 incomplete, 2 refused."""
    import typer

    from probe.cli import install_pipeline

    code = 0
    with events.session(json_output):
        # An install entry: an uninstall that stopped halfway is finished first.
        refused = install_pipeline.refusal(finish=True)
        if refused:
            events.error(events.ErrorCode.FAILED, refused)
            _say(f"probe repair: refused: {refused}")
            raise typer.Exit(REFUSED_EXIT)
        cleared = install_pipeline.clear_stale_barrier()
        if cleared:
            _say(cleared)
        agents = _agents()
        events.begin_result("repair", [None, *agents])
        problems: list[str] = []

        events.step(events.Step.REPAIR_CLI, events.Status.STARTED)
        cli, cli_out = repair_cli()
        _step(events.Step.REPAIR_CLI, cli)
        if cli_out is not None and getattr(cli_out, "refused", "") and not getattr(cli_out, "unmanaged", False):
            for line in cli.problems:
                _say(f"probe repair: refused: {line}")
            events.agent_result(None, requested={"repair": True}, actual=None, ok=False,
                                message="; ".join(cli.problems))
            raise typer.Exit(REFUSED_EXIT)
        parts = [("the CLI", cli)]

        events.step(events.Step.KEEPER, events.Status.STARTED)
        keeper = repair_keeper(cli_out)
        _step(events.Step.KEEPER, keeper)
        parts.append(("the keeper", keeper))

        # Identity BEFORE the service (and its daemon workers) starts again.
        events.step(events.Step.IDENTITY, events.Status.STARTED)
        identity = repair_identity()
        _step(events.Step.IDENTITY, identity)
        parts.append(("the credentials", identity))

        events.step(events.Step.SERVICE, events.Status.STARTED)
        service = repair_service(cli_out)
        _step(events.Step.SERVICE, service)
        parts.append(("the service", service))

        for title, part in parts:
            for line in part.lines:
                _say(f"{title}: {line}")
            if part.skipped:
                _say(f"{title}: {part.skipped}")
            for line in part.problems:
                _say(f"! {title}: {line}")
            problems.extend(part.problems)
        events.agent_result(None, requested={"repair": True}, actual={"problems": len(problems)},
                            ok=not problems, message="; ".join(problems))

        for source, done in repair_integrations(agents).items():
            part = Part(lines=done.lines, problems=done.problems)
            _step(events.Step.REPAIR_INTEGRATIONS, part, agent=source)
            for line in done.lines:
                _say(f"{source}: {line}")
            for line in done.problems:
                _say(f"! {source}: {line}")
            problems.extend(done.problems)
            events.agent_result(source, requested={"repair": True}, actual={"problems": len(done.problems)},
                                ok=not done.problems, message="; ".join(done.problems))

        if problems:
            _say(f"Probe is INCOMPLETE on this machine ({len(problems)} problem(s) above).")
            code = INCOMPLETE_EXIT
        else:
            _say("Probe is complete on this machine.")
        if code:
            raise typer.Exit(code)
    return code
