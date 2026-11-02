"""probe exec: run a command under a run and own that run while it executes (raw args, service hold, deferred update)."""

from __future__ import annotations
import os

import typer
from ....sdk import agent_session
from ....sdk.run.launch import daemon_channel
from probe.cli.cli import app
from probe.cli.commands.entity_text import AuthoredBy, _authored_by_value, authored_by_opt


def _hold_run_with_service(handle) -> tuple[str, dict] | None:
    """`probe exec`: tell the Probe service this process wraps `handle`'s run
    (`run.hold`), so its updater's quiet check sees the run without scanning
    lock files. `(run id, owner)` for the release, or None (no service, an
    older one, Windows): the run lock is what it reads then. Never raises."""
    try:
        run_id = getattr(handle, "id", None)
        if not isinstance(run_id, str) or not run_id:
            return None
        from probe.cli.lifecycle import service_calls

        owner = service_calls.hold_run(run_id)
        return (run_id, owner) if owner is not None else None
    except Exception:  # noqa: BLE001 -- never in the way of the run
        return None


def _release_run_with_service(run_id: str, owner: dict) -> None:
    """The run is over: the Probe service drops its hold. Never raises."""
    try:
        from probe.cli.lifecycle import service_calls

        service_calls.release_run(run_id, owner)
    except Exception:  # noqa: BLE001
        pass


# -- exec (process correlation) ---------------------------------------------
_RAW_ARGS = "probe.raw_args"


class _RawArgsCommand(typer.core.TyperCommand):
    """Keeps the args click was handed, before parsing.

    `probe exec -- python train.py` and `probe exec RUN -- python train.py` parse
    alike: click consumes the `--` and binds the first token after it to the
    optional RUN, so the first reads as "wrap run `python`". Only the raw args
    say which side of the `--` the positional came from.
    """

    def parse_args(self, ctx, args):  # type: ignore[override]
        ctx.meta[_RAW_ARGS] = list(args)
        return super().parse_args(ctx, args)


def _positional_after_separator(raw: object, run: str, rest: list[str]) -> bool:
    """Whether click bound RUN from the first token AFTER `--` (so it is the
    command, not a run ref). After it, click leaves every later token in `rest`;
    before it, the whole command after `--` is still in `rest`."""
    if not isinstance(raw, list) or "--" not in raw:
        return False
    at = raw.index("--")
    return raw[at + 1 : at + 2] == [run] and list(rest) == raw[at + 2 :]


@app.command(
    cls=_RawArgsCommand,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="run a command under a run: probe exec [--project P] -- cmd ... (or: probe exec RUN -- cmd ...)",
)
def exec(
    ctx: typer.Context,
    run: str = typer.Argument(None, help="an EXISTING run ref; omit to open one here"),
    cwd: str = typer.Option(None, "--cwd"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="slug of an EXISTING experiment"),
    slug: str = typer.Option(None, "--slug", help="this run's slug; omit for a petname"),
    name: str = typer.Option(None, "--name"),
    description: str = typer.Option(None, "--description"),
    tag: list[str] = typer.Option(None, "--tag"),
    external_id: str = typer.Option(None, "--external-id"),
    config: list[str] = typer.Option(None, "--config", metavar="k=v"),
    parent: str = typer.Option(
        None, "--parent", help="the run this one re-attempts or branches from (id or petname)"
    ),
    relation: Relation = typer.Option(
        None, "--relation", help="retry|resume|fork|branch; required with --parent"
    ),
    intent: str = typer.Option(
        None, "--intent", help="what this run is meant to show (free text, kept in its metadata)"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
    launcher: str = typer.Option(
        None,
        "--launcher",
        help="override launcher detection: modal|ray|sbatch|kubectl for submit-and-return",
    ),
    detached_launcher: bool = typer.Option(
        False,
        "--detached-launcher",
        help="this command SUBMITS and returns; do not treat its exit code as the job's",
    ),
    token_ttl: str = typer.Option(
        None,
        "--token-ttl",
        help="give the job a per-run token (PROBE_TOKEN in the launcher's environment) living this long, e.g. 36h, 7d, 2w -- the run's expected length plus margin; a hand-off always gets one (default 30d)",
    ),
    outputs: str = typer.Option(
        None,
        "--outputs",
        help="the folder whose new/changed files are captured at exit (default: --cwd or the current folder; a relative path is taken from --cwd)",
    ),
    no_capture_outputs: bool = typer.Option(
        False,
        "--no-capture-outputs",
        help="do not capture the command's output files or its printed log (also PROBE_CAPTURE_OUTPUTS=0)",
    ),
    input_paths: list[str] = typer.Option(
        None,
        "--input",
        metavar="PATH",
        help="a file (glob, or folder) the command READS, hashed when it starts: for steps that are not "
        "Python (head, jq, shuf), whose reads Probe cannot see. Repeatable; identity only, never contents",
    ),
    output_paths: list[str] = typer.Option(
        None,
        "--output",
        metavar="PATH",
        help="a file (glob, or folder) the command WRITES, hashed when it exits (if it changed). "
        "Repeatable; identity only, never contents",
    ),
) -> None:
    """Execute a command under a run, and OWN that run while it executes.

    This is the honest wrapper. It opens the run (or takes one you already
    opened), beats for as long as the child lives, hands the child
    ``PROBE_RUN_ID`` + ``PROBE_RUN_EPOCH`` so ``probe.init()`` inside it joins
    the SAME run, and closes the run from the child's real exit code.

    BLOCKING vs SUBMIT is the distinction that matters. `python train.py` and
    `modal run` block until the work finishes, so this process's lifetime is the
    run's and its exit code is the job's. `sbatch`, `ray job submit` and `modal
    deploy` return the moment a scheduler accepts the job -- wrapping one of
    those would mark the run completed, exit 0, while the work had not started.
    For those the run is opened AWAITING ATTACH: it lands 'created', owned by
    nobody, and the job's own `probe.init()` becomes its owner when it starts.
    Detection unwraps `python -m` / `uv run` / `uvx`; `--launcher` overrides it
    and `--detached-launcher` covers anything unrecognised.

    CAPTURE: everything the command prints is teed to your terminal and saved
    as the run's `probe/run.log`, and the files it creates or changes in its
    folder (`--outputs`, else `--cwd`, else here) are captured as `outputs/...`
    when it exits -- uploaded up to 64 MB; bigger ones recorded where they live
    on storage that lasts, or listed in `probe/outputs-manifest.json` on a
    throwaway machine. `--no-capture-outputs` turns both off. A submit-and-return
    launcher captures nothing: the job's own `probe.init()` does.

    NAMED FILES (F39): what a Python command reads and writes is recorded by the
    read hook; a shell step's (`head`, `cat | shuf`, `jq`) is not. `--input PATH`
    and `--output PATH` (repeatable; globs and folders) name them: inputs are
    hashed before the command starts, outputs when it exits (only those it
    created or changed), with the recorder's hasher (rows counted, the
    `.probe.config` `hash` floor), and sent as the run's reads and writes. A
    submit-and-return launcher sends only the inputs. Under a `.probe.config`
    `hash` folder the run opens and records identities only, without its log.

    With no run, no --project/--experiment and no active project, it refuses
    before the command starts: every run has a project.
    """
    argv = list(ctx.args)
    if argv and argv[0] == "--":
        argv = argv[1:]
    raw_args = (getattr(ctx, "meta", None) or {}).get(_RAW_ARGS)
    if isinstance(run, str) and _positional_after_separator(raw_args, run, argv):
        # `probe exec -- python train.py`: "python" is the command, not a run.
        argv = [run, *argv]
        run = None
    # Click consumes the `--` separator and then binds the first remaining token
    # to the optional positional, so `probe exec --project p -- python train.py`
    # arrives with run="python" and argv=["train.py"]. Creation flags are the
    # unambiguous signal that the caller is OPENING a run here rather than
    # naming one, so the positional is the start of their command -- put it back.
    # isinstance, not `is not None`: called directly as a Python function (the
    # version-notice tests do) the typer defaults are OptionInfo objects rather
    # than None, and every flag would read as supplied.
    opening_here = any(
        isinstance(v, str) and v
        for v in (project, experiment, slug, name, description, external_id, intent)
    ) or any(isinstance(v, list) and v for v in (tag, config))
    if run is not None and opening_here:
        argv = [run, *argv]
        run = None
    if not argv:
        raise typer.BadParameter("probe exec requires a command after --")

    # Before the run opens: a bad --token-ttl must not leave a run awaiting a job.
    token_ttl_seconds = _parse_duration(token_ttl) if isinstance(token_ttl, str) and token_ttl else None
    # Same OptionInfo caution as above: `is True` / isinstance, never truthiness.
    hands_off = detached_launcher is True or (
        launcher.lower() in _LAUNCHER_ALIASES
        if isinstance(launcher, str) and launcher
        else _is_submit_launcher(argv)
    )
    # F39: the files a non-Python step names. A hand-off's outputs land after
    # this process is gone, so only its inputs are hashed (at start).
    named_inputs = [p for p in input_paths if isinstance(p, str) and p] if isinstance(input_paths, list) else []
    named_outputs = (
        [p for p in output_paths if isinstance(p, str) and p] if isinstance(output_paths, list) and not hands_off else []
    )
    from ....sdk.recording_rules import recording_rules as _exclusions
    from ....sdk.capture import outputs as _sdk_outputs

    exec_cwd = cwd if isinstance(cwd, str) and cwd else None
    # `.probe.config` `hash` where the command runs, or any `hash`/`read`/`off`
    # path the command names (an argument, a word of a shell string, an
    # --input/--output): the run records identities only, never its console
    # log, which may print the file's records (set while the child runs; it
    # inherits it).
    from ...lifecycle import write_gate as _write_gate

    log_off = _exclusions.cwd_excluded(exec_cwd).excluded or _write_gate.names_excluded(
        [*argv, *named_inputs, *named_outputs], os.path.abspath(exec_cwd or os.getcwd())
    )
    log_before = os.environ.get(_sdk_outputs.LOG_ENV)

    from probe.foundation.durable import run_lock

    # ONE client, ONE handle, held for the child's whole life. Opening the run
    # through a first client and then re-attaching through a second took the
    # process-bound flock TWICE: `c.run(heartbeat=True)` claims it via
    # _hold_run_lock, Client.close() does not release it (only a terminal
    # set_status does), and flock refuses a second fd in the same process -- so
    # both the explicit acquire and attach's own claim failed silently and
    # `probe exec` ran with no auto-update protection at all, which is the one
    # thing the flock tier exists for.
    #
    # `raise_permanent=False`: this process carries the wrapped job's run --
    # its beats, its console log, its captured outputs -- through the SDK, which
    # must never raise into the job over one refused write (`Client.write`),
    # nor report each failed one on stderr or in its exit code (`_new_client`).
    # Every other verb is a single write a refusal should fail (L14).
    #
    # The launcher is the run's process for the job's whole life (R41): its
    # create, beats, log and close, and every write of the job it starts (which
    # inherits the mark), are the run's, never its agent being active. A
    # backgrounded `probe exec` closing at 3 a.m. adds no agent-hours.
    agent_session.mark_run_process()
    with _client(raise_permanent=False) as c:
        claim = None
        if run is None:
            # An active project (`probe project use`) still wins; with none and
            # no --project/--experiment `c.run` refuses before the command starts.
            resolved_project = _ambient_project(project if isinstance(project, str) else None)
            # Parentage is a pair. One half alone is either a relation with no
            # parent to mean it, or a parent with a guessed relation -- and the
            # server stores whatever word arrives as a claim someone reads later.
            if (parent is None) != (relation is None):
                raise typer.BadParameter("--parent and --relation go together")
            # The parent's UUID, not the ref typed: `parent_run_id` is a UUID
            # field, and a petname reaching the server as one is rejected.
            parent_id = _ref(c, "run", parent).row["id"] if parent else None
            # The command rides the run's "run started" message to the daemon,
            # and names the launch the retry detector compares (L6).
            from ....sdk.run.launch import launch as _launch

            with daemon_channel.launch_command(argv), _launch.launching(
                argv, cwd if isinstance(cwd, str) else None
            ):
                handle = c.run(
                    experiment=experiment if isinstance(experiment, str) else None,
                    project=_project_slug(c, resolved_project) if resolved_project else None,
                    name=name if isinstance(name, str) else None,
                    slug=slug if isinstance(slug, str) else None,
                    description=description if isinstance(description, str) else None,
                    tags=list(tag) if isinstance(tag, list) and tag else None,
                    external_id=external_id if isinstance(external_id, str) else None,
                    config=_kv_pairs(config) if isinstance(config, list) and config else None,
                    intent=intent if isinstance(intent, str) else None,
                    parent_run_id=parent_id,
                    parent_relation=relation.value if relation else None,
                    # A hand-off opens the row for a job that has not started; a
                    # blocking wrap opens it owned, beating from this process.
                    awaiting_attach=hands_off,
                    heartbeat=not hands_off,
                    # `run start`'s own deprecation notice sends people here, so the
                    # command the CLI steers to must be able to say a PERSON wrote
                    # the name. Without it a researcher's own title, typed through
                    # an agent, is stamped `agent` with no override -- on the one
                    # verb they are being told to use.
                    authored_by=_authored_by_value(authored_by),
                    # The server cannot see the difference between a launcher and
                    # the work itself; this is the signal that makes "held open but
                    # nothing inside ever reported" expressible.
                    launcher=True,
                    # This process is the launcher, not the work: it must not tee
                    # or sweep ITSELF. `execute` below captures the child.
                    capture_outputs=False,
                )
            _print_link("run", handle.id)
            _label_status_line_soon(experiment if isinstance(experiment, str) and experiment else resolved_project)
            # A beating handle already holds the flock; a hand-off holds nothing
            # on purpose. Either way there is no second claim to take.
        else:
            # Wrapping a run someone else opened: this process still owns the
            # child, so it takes the flock tier explicitly.
            claim = None if hands_off else run_lock.acquire(run)
            handle = _run_handle(c, run, owns_process=not hands_off)
        # The Probe service's updater sees the run directly while this process
        # wraps it (`run.hold`); the run lock above stays, for an older service
        # and the CLI's own updater. A hand-off wraps nothing.
        held = None if hands_off else _hold_run_with_service(handle)
        minted, why_not = None, None
        try:
            if not hands_off and token_ttl_seconds is not None:
                # A blocking launcher (`modal run`) whose job runs elsewhere:
                # the job gets the run's own token through the launcher's
                # environment, and this process still records the exit code.
                minted, why_not = _mint_handoff_token(c, handle.id, token_ttl_seconds)
                typer.echo(
                    f"probe: the job's PROBE_TOKEN records run {handle.slug or handle.id} only and expires "
                    f"{_when(minted.get('expires_at'))}; forward it with PROBE_RUN_ID and PROBE_RUN_EPOCH"
                    if minted is not None else f"probe: {why_not}",
                    err=True,
                )
            if hands_off:
                # The job's credential: a per-run token that records this run
                # only, safe in a plain job spec. An older server has none; the
                # job then needs a token from the researcher's secret store.
                minted, why_not = _mint_handoff_token(c, handle.id, token_ttl_seconds)
                hint = _forwarding_hint(argv, handle.id, handle.write_epoch, token_minted=minted is not None)
                # The agent session too (audit E2), so the job's runs carry the
                # session tag the Probe daemon finds them by.
                session_lines = "".join(
                    f"\n         {key}={value}"
                    for key, value in agent_session.forwarding_env().items()
                )
                ref = handle.slug or handle.id
                if minted is not None:
                    token_line = f"         PROBE_TOKEN={minted['token']}\n"
                    life = (
                        f"\n       the token records this run only and expires {_when(minted.get('expires_at'))}"
                        + ("" if token_ttl_seconds
                           else " (default 30 days: set --token-ttl to the run's expected length plus margin)")
                        + f"; extend it with `probe run token {ref} --extend 7d`"
                    )
                else:
                    token_line = "         PROBE_TOKEN from your secret store (probe token create)\n"
                    life = f"\n       ({why_not})" if why_not else ""
                typer.echo(
                    f"probe: run {ref} is awaiting attach.\n"
                    f"       forward these into the job or it reports nothing:\n"
                    + token_line
                    + f"         PROBE_RUN_ID={handle.id}\n"
                    f"         PROBE_RUN_EPOCH={handle.write_epoch}"
                    + session_lines
                    + life
                    + (f"\n       {hint}" if hint else ""),
                    err=True,
                )
            if log_off:
                os.environ[_sdk_outputs.LOG_ENV] = "0"
            named = None
            if named_inputs or named_outputs:
                from ....sdk.capture import lineage as _sdk_inputs

                named = _sdk_inputs.NamedFiles(
                    c, handle.id, inputs=named_inputs, outputs=named_outputs, base=exec_cwd
                )
                named.start()
            # finalize=False for a hand-off: this process's exit code belongs to
            # the SUBMITTER, and recording it as the run's is the precise lie
            # this branch exists to avoid.
            result = handle.execute(
                argv,
                cwd=cwd,
                # The launcher submits with the run's own token, so what it
                # forwards from its environment is never the researcher's key.
                env=_job_token_env(minted, why_not),
                finalize=not hands_off,
                outputs=outputs if isinstance(outputs, str) and outputs else None,
                capture_outputs=False if no_capture_outputs is True else None,
            )
            if named is not None:
                named.finish()
        finally:
            if log_off:
                if log_before is None:
                    os.environ.pop(_sdk_outputs.LOG_ENV, None)
                else:
                    os.environ[_sdk_outputs.LOG_ENV] = log_before
            if claim is not None:
                claim.release()
            if held is not None:
                # Before the update check below: the service must not still
                # read this run as in flight when that check comes.
                _release_run_with_service(*held)
            # The wrapped process is gone and our claim with it. `_version_notice`
            # refused an upgrade at the START of this command (`exec` is on the
            # denylist, correctly), and this is the moment that refusal stops
            # being permanent.
            #
            # Inside the `finally` on purpose: it must run whether the child
            # succeeded, failed, or was Ctrl-C'd, since the run is over either
            # way. That is also why _apply_deferred_update swallows everything --
            # a raise here would replace the propagating exception and corrupt
            # the exit code this command exists to hand back.
            _apply_deferred_update()
    # A child killed by signal N comes back as -N; handed to exit() as is, the
    # OS keeps its low byte (SIGTERM -15 -> 241). Report it the way a shell
    # does, 128+N, so `probe exec` is transparent to whatever reads the code.
    code = result.returncode
    raise typer.Exit(128 - code if code < 0 else code)
from probe.cli.commands.flag_values import _kv_pairs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_link  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ambient_project, _project_slug, _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.exec_launchers import _LAUNCHER_ALIASES, _forwarding_hint, _is_submit_launcher  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.runs import Relation  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.tokens import _job_token_env, _mint_handoff_token, _parse_duration, _when  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.after_command import _label_status_line_soon  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.update_spawn import _apply_deferred_update  # noqa: E402 -- pieces need each other; the front door loads this one first
