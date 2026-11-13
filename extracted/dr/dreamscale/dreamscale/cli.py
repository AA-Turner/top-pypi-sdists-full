"""dreamscale CLI (typer, like the sandbox CLI). Every DreamscaleError renders
problem+cause+fix and exits 1."""

from __future__ import annotations

import inspect
from enum import StrEnum
from math import ceil
from pathlib import Path
from typing import Annotated

import click
import typer
from typer.completion import completion_init, install_callback
from typer.core import TyperCommand, TyperGroup

_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_CLI_KEEP_WARM_S = 300

completion_init()


def _keep_warm_option():
    # Hidden: shared models close on exit. Older non-shared models still honour it.
    return typer.Option(None, "--keep-warm", min=0, max=3600, hidden=True)


# --steady-send: an opt-in floor between requests (hidden). Bare, 400 ms; with "=MS", MS.
STEADY_SEND_DEFAULT_MS = 400
STEADY_SEND_MIN_MS, STEADY_SEND_MAX_MS = 50, 2000
_STEADY_SEND = "--steady-send"
_STEADY_SEND_VALUE = "--steady-send-ms"  # reached through --steady-send=MS


class SteadySendCommand(TyperCommand):
    """Reads --steady-send's value only after "=": `--steady-send=250` becomes the hidden
    value option, while a bare `--steady-send` stays a flag, so a following token is never
    taken as its value (`--steady-send 250` leaves 250 as an argument)."""

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        rewritten: list[str] = []
        for index, arg in enumerate(args):
            if arg == "--":
                rewritten.extend(args[index:])
                break
            if arg.startswith(f"{_STEADY_SEND}="):
                rewritten += [_STEADY_SEND_VALUE, arg.partition("=")[2]]
            else:
                rewritten.append(arg)
        return super().parse_args(ctx, rewritten)


def _check_steady_send_ms(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        ms = int(value)
    except ValueError:
        ms = None
    if ms is None or not STEADY_SEND_MIN_MS <= ms <= STEADY_SEND_MAX_MS:
        raise typer.BadParameter(
            f"{value!r} isn't a send interval. Use whole milliseconds from "
            f"{STEADY_SEND_MIN_MS} to {STEADY_SEND_MAX_MS}, e.g. --steady-send=400.",
            param_hint=f"'{_STEADY_SEND}'",
        )
    return ms


def _steady_send_options():
    return (
        typer.Option(False, _STEADY_SEND, hidden=True),
        typer.Option(None, _STEADY_SEND_VALUE, hidden=True, callback=_check_steady_send_ms),
    )


def _steady_send(flag: bool, ms: int | None) -> int | None:
    """The send floor in milliseconds, or None (absent: today's behaviour)."""
    if ms is not None:
        return ms
    return STEADY_SEND_DEFAULT_MS if flag else None


def _keep_warm(model: str, keep_warm: int | None, checkpoint: str | None = None) -> int:
    """Seconds to keep a session reserved after a task. The server ignores keep-warm for
    shared models, so the CLI asks for none and says nothing about it. A deployment's own
    keep-warm setting decides for its sessions, so the CLI adds no default there either."""
    from dreamscale.models_cmd import SHARED_BASE_MODELS, SHARED_MODELS

    if checkpoint not in (None, "base"):
        if keep_warm is not None:
            typer.echo(
                "--keep-warm doesn't apply to deployments; their own setting decides. "
                f"Set it with: dreamscale deployments keep-warm {checkpoint} 10m|30m|…|always",
                err=True,
            )
        return 0 if keep_warm is None else keep_warm
    if model in SHARED_MODELS or model in SHARED_BASE_MODELS:
        return 0
    return DEFAULT_CLI_KEEP_WARM_S if keep_warm is None else keep_warm


def _model_name(value: str | None) -> str | None:
    """--model takes a public name (pi0.5-bimanualyam) or the internal id; a name only the
    control plane lists resolves through it."""
    from dreamscale.model_names import resolve_model

    return resolve_model(value) if value else value


# Options every `dreamscale run <robot>` command shares: each call builds a fresh
# typer.Option, so robot commands declare the same flags with the same help.
def _instruction_option():
    return typer.Option(
        None, "--instruction", help="Run one task, then exit (default: prompt for tasks)."
    )


def _mode_option():
    return typer.Option(
        "auto", "--mode",
        help="async (replan continuously) or sync (finish each chunk). Default: the model's "
        "own (sync for Praxis-1, async for the rest).",
    )


def _engine_option():
    return typer.Option(
        None, "--engine",
        click_type=click.Choice(["standard", "lightning"]),
        help="Praxis-1's engine (experimental): standard (default) or lightning, the same "
        "actions faster.",
    )


def _max_actions_option():
    return typer.Option(
        None,
        "--max-actions",
        min=1,
        max=18000,
        help="Action limit per task (default: run until Ctrl+C).",
    )


_REGION_HELP = "Where to serve: auto (nearest), available, or a region id such as us-west."


def _region_option():
    return typer.Option("available", "--region", help=_REGION_HELP)


def _provider_option():
    return typer.Option(None, "--provider", help="Advanced: aws or modal.")


def _speed_option():
    return typer.Option(
        "standard", "--speed", help="standard, fast or ultrafast, where the model supports it."
    )


def _rtc_option():
    return typer.Option(
        "auto",
        "--rtc",
        help="Advanced real-time chunking: auto (the model's default), on, off, train_time "
        "or inference_time.",
    )


_DEPLOYMENT_ARG = "Deployment: <account>/<slug>, its slug, or its ckpt_… ID."


def _checkpoint_option():
    return typer.Option(
        None,
        "--deployment",
        "--checkpoint",
        help="Deployment to run: <account>/<slug>, its slug or its ckpt_… ID "
        "(`dreamscale deployments list`), or base.",
    )


def _context_option():
    return typer.Option(
        "auto",
        "--context",
        help="Isaac 0.5 frame history: auto (the deployment's own), on (last 3 frames) or "
        "off (1 frame).",
    )


def _action_smoothing_option():
    return typer.Option(
        "auto",
        "--action-smoothing",
        help="Chunk joining for async with RTC off: auto, continuation, motion or output.",
    )


def _smoothing_new_weight_option():
    return typer.Option(None, "--smoothing-new-weight", min=0, max=1, hidden=True)


def _smoothing_correction_steps_option():
    return typer.Option(
        None,
        "--smoothing-correction-steps",
        min=1,
        hidden=True,
        help="Motion: recurring correction gain. Handover: maximum duration in ticks.",
    )


def _smoothing_reference_speed_option():
    return typer.Option(
        None,
        "--smoothing-reference-speed",
        min=0.000001,
        hidden=True,
        help="Experimental adaptive response scale in joint units per second; not a safety "
        "limit.",
    )


def _trace_dir_option():
    return typer.Option(
        "--trace-dir", help="Save a recording of each task under this directory."
    )


def _trace_images_option():
    return typer.Option(
        False,
        "--trace-images",
        help="Include camera frames in recordings (needs --trace-dir).",
    )


def _effort_option():
    return typer.Option(
        None,
        "--effort",
        help="LLM reasoning effort: low, medium (default), high, xhigh or max.",
    )


def _max_cost_option():
    return typer.Option(
        None,
        "--max-cost",
        min=0.000001,
        max=1000,
        help="LLM credit limit per task (default: none).",
    )


# Policy-only options; an LLM run rejects them when given on the command line.
_POLICY_OPTIONS = (
    "mode", "max_actions", "keep_warm", "region", "provider", "rtc", "checkpoint", "context",
    "action_smoothing", "smoothing_new_weight", "smoothing_correction_steps",
    "smoothing_reference_speed", "trace_dir", "trace_images", "hud", "hud_job",
    "steady_send", "steady_send_ms", "engine",
)


def _is_llm(model: str) -> bool:
    from dreamscale_transport.llm import MODELS

    return model in MODELS


def _reject_policy_options(ctx: typer.Context) -> None:
    from click.core import ParameterSource

    for param in ctx.command.params:
        if (
            param.name in _POLICY_OPTIONS
            and ctx.get_parameter_source(param.name) == ParameterSource.COMMANDLINE
        ):
            raise typer.BadParameter(f"{param.opts[0]} does not apply to LLM execution.")


def _verbose_option():
    return typer.Option(False, "--verbose", help="Show diagnostic details.")


def _group(help_text: str) -> typer.Typer:
    return typer.Typer(
        context_settings=_CONTEXT_SETTINGS,
        invoke_without_command=True,
        no_args_is_help=False,
        help=help_text,
    )


def _show_group_help(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


class CreateFirstGroup(TyperGroup):
    """`dreamscale train --dataset …` runs the hidden `create`; any first word that isn't a
    subcommand goes there too, for its fix."""

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if args and args[0] not in self.commands and args[0] not in ctx.help_option_names:
            args = ["create", *args]
        return super().parse_args(ctx, args)


class SimTransport(StrEnum):
    auto = "auto"
    quic = "quic"
    relay = "relay"


app = typer.Typer(
    add_completion=False,
    context_settings=_CONTEXT_SETTINGS,
    no_args_is_help=True,
    help="Dreamscale: fast serverless inference for your robots.",
)
run_app = _group("Run a task on a physical robot.")
robots_app = _group("Set up and maintain robots.")
yam_app = _group("Set up and maintain YAM.")
so101_app = _group("Set up and maintain SO-101.")
franka_app = _group("Set up and maintain Franka (experimental).")
ur_app = _group("Set up and maintain a Universal Robots arm (experimental).")
xarm7_app = _group("Set up and maintain two xArm 7s (experimental).")
openarm_app = _group("Set up and maintain an Anvil OpenARM (experimental).")
models_app = _group("See and manage the models your organization can run.")
sessions_app = _group("Manage cloud sessions.")
deployments_app = _group("Deploy and manage your fine-tuned models.")
endpoints_app = _group("Older name for `dreamscale deployments`.")
checkpoints_app = _group("Older name for `dreamscale deployments`.")
integrations_app = _group("Connect Dreamscale to other tools.")
train_app = typer.Typer(
    cls=CreateFirstGroup,
    context_settings=_CONTEXT_SETTINGS,
    invoke_without_command=True,
    no_args_is_help=False,
    help="Fine-tune a base model on your LeRobot dataset, on Dreamscale's GPUs.\n\n"
    "Start a run: dreamscale train --dataset NAME --base BASE (or --dataset hf://owner/name). "
    "Its options: dreamscale train create --help",
)
datasets_app = _group("Keep your LeRobot datasets on Dreamscale and train on them.")
hud_app = _group("Record and grade runs on HUD (hud.ai).")
hugging_face_app = _group("Read your private Hugging Face repos.")
inspect_robots_app = _group("Evaluate Dreamscale models with Inspect Robots.")
auth_app = _group("Manage this machine's sign-in.")
for group_app in (
    run_app, robots_app, so101_app, yam_app, franka_app, ur_app, xarm7_app, openarm_app,
    models_app,
    sessions_app,
    deployments_app, endpoints_app, checkpoints_app, integrations_app, hud_app,
    hugging_face_app, inspect_robots_app, train_app, auth_app, datasets_app,
):
    group_app.callback()(_show_group_help)
robots_app.add_typer(so101_app, name="so101")
robots_app.add_typer(yam_app, name="yam")
robots_app.add_typer(franka_app, name="franka")  # FRANKA.experimental
robots_app.add_typer(ur_app, name="ur")
robots_app.add_typer(xarm7_app, name="xarm7")  # XARM7.experimental
robots_app.add_typer(openarm_app, name="openarm")  # OPENARM.experimental
app.add_typer(run_app, name="run")
app.add_typer(robots_app, name="robots")
app.add_typer(models_app, name="models")
app.add_typer(sessions_app, name="sessions")
# Integrations (--hud, --inspect-robots) work but stay out of help until they launch; set
# this to False to list them.
_LAUNCH_HIDDEN = True
app.add_typer(deployments_app, name="deployments")
app.add_typer(endpoints_app, name="endpoints", hidden=True)
app.add_typer(checkpoints_app, name="checkpoints", hidden=True)
app.add_typer(train_app, name="train")
app.add_typer(datasets_app, name="datasets")
app.add_typer(datasets_app, name="dataset", hidden=True)
# `dreamscale login` stays a top-level command; auth holds the rest of signing in.
app.add_typer(auth_app, name="auth")
integrations_app.add_typer(hud_app, name="hud")
integrations_app.add_typer(hugging_face_app, name="hugging-face")
integrations_app.add_typer(inspect_robots_app, name="inspect-robots")
app.add_typer(integrations_app, name="integrations", hidden=_LAUNCH_HIDDEN)
# A request's own Hugging Face token; without one the control plane uses the connected one.
_HF_TOKEN_HELP = (
    "Hugging Face token for this request (default: $HF_TOKEN, else your connected one)."
)


def _show_version(value: bool) -> None:
    if value:
        from dreamscale import __version__

        typer.echo(f"dreamscale {__version__}")
        # Status goes to stderr so `dreamscale --version` stays one parseable line.
        from dreamscale.update_check import update_status

        status = update_status(__version__)
        if status is not None:
            message, color, command = status
            typer.secho(message, err=True, fg=color)
            if command:
                typer.echo(f"Update: {command}", err=True)
        raise typer.Exit()


@app.callback()
def main(
    _version: bool = typer.Option(
        False,
        "--version",
        callback=_show_version,
        is_eager=True,
        expose_value=False,
        help="Show the version and exit.",
    ),
    _install_completion: bool = typer.Option(
        None,
        "--install-completion",
        callback=install_callback,
        expose_value=False,
        help="Install shell completion.",
    ),
) -> None:
    """Dreamscale command line."""
    from dreamscale import control

    control.CLIENT = "cli"


def _run(fn, **kwargs) -> None:
    from dreamscale import errors

    try:
        fn(**kwargs)
    except errors.DreamscaleError as error:
        typer.echo(error.render())
        raise typer.Exit(code=1) from error
    except KeyboardInterrupt as exc:
        typer.echo("Canceled. Cleaned up any active Dreamscale session.")
        raise typer.Exit(code=130) from exc


def _ensure_extras(extras, *, label, setup_command) -> None:
    """Install the optional packages a command needs the first time it runs, then rerun it."""
    from dreamscale.extras import ensure_extras

    _run(ensure_extras, extras=list(extras), label=label, setup_command=setup_command)


def _hud_options():
    return (
        typer.Option(
            False, "--hud", hidden=_LAUNCH_HIDDEN,
            help="Record each task on HUD with video and your grade.",
        ),
        typer.Option(
            None, "--hud-job", hidden=_LAUNCH_HIDDEN, help="HUD job name (needs --hud).",
        ),
    )


def _check_hud_options(hud: bool, hud_job: str | None) -> None:
    if hud_job is not None and not hud:
        raise typer.BadParameter("--hud-job names a HUD job; add --hud to record on HUD.")


def _ensure_hud_setup() -> None:
    """After the hud extra is installed: set HUD up first when this computer is not."""
    from dreamscale.integrations import hud as integration

    if integration.api_key() is None:
        typer.echo("HUD is not set up on this computer yet; setting it up now.")
        _run(integration.run_setup)


# `dreamscale login` is the way in; `auth login` is there for whoever looks for it under auth.
@auth_app.command("login", help="Sign in on this machine (same as `dreamscale login`).")
@app.command()
def login(
    api_key: str | None = typer.Option(
        None,
        "--api-key",
        help="Save this API key instead of signing in with a browser.",
        hide_input=True,
        prompt="API key",
        prompt_required=False,
    ),
) -> None:
    """Sign in on this machine."""
    from dreamscale import errors
    from dreamscale.quickstart import run_login
    from dreamscale.terminal import make_progress_printer

    print_fn = make_progress_printer()
    try:
        run_login(api_key=api_key, print_fn=print_fn)
    except errors.DreamscaleError as error:
        close = getattr(print_fn, "close", None)
        if close:
            close()
        typer.echo(error.render())
        raise typer.Exit(code=1) from error
    except KeyboardInterrupt as exc:
        close = getattr(print_fn, "close", None)
        if close:
            close()
        typer.echo("Canceled. Cleaned up any active Dreamscale session.")
        raise typer.Exit(code=130) from exc
    finally:
        close = getattr(print_fn, "close", None)
        if close:
            close()


@auth_app.command("whoami")
def auth_whoami() -> None:
    """Show the account and organization this machine is signed in as."""
    from dreamscale.quickstart import run_whoami

    _run(run_whoami)


@auth_app.command("logout")
def auth_logout() -> None:
    """Sign out on this machine and revoke its login key."""
    from dreamscale.quickstart import run_logout

    _run(run_logout)


@app.command()
def doctor(
    mode: str = typer.Argument(
        "core",
        help="What to check: core, sim, all, so101, yam, franka, ur, xarm7 or openarm.",
    ),
    config: Annotated[
        Path | None,
        typer.Option("--config", help="Rig config path (yam, franka, ur, xarm7, openarm)."),
    ] = None,
    model: str | None = typer.Option(
        None,
        "--model",
        callback=_model_name,
        help="With a robot: model to check access to.",
    ),
) -> None:
    """Check your setup."""
    from dreamscale.embodiments import EMBODIMENTS

    embodiment = EMBODIMENTS.get(mode.lower())
    if embodiment is not None:
        if config is not None and not embodiment.rig_config:
            raise typer.BadParameter(f"--config applies to robots with a rig file, not {mode}.")
        # Doctor opens the cameras too, so it installs what run and setup would.
        if embodiment.extras:
            _ensure_extras(
                list(embodiment.load(embodiment.extras)()), label=embodiment.label,
                setup_command=embodiment.setup_command,
            )
        _run_robot_command(
            embodiment.load(embodiment.doctor),
            **({"config_path": config} if config else {}),
            **({"model": model} if model is not None else {}),
        )
        return
    if config is not None:
        raise typer.BadParameter("--config applies to doctor yam.")
    if model is not None:
        raise typer.BadParameter("--model applies to a robot: doctor so101 or doctor yam.")
    from dreamscale.doctor import run_doctor

    _run(run_doctor, mode=mode)


def _sim_list(benchmark: str | None, task_suite: str | None, *, json_output: bool) -> None:
    """`dreamscale sim [<benchmark>] [--task-suite <suite>] --list`: offline, no --model."""
    from dreamscale.sim.benchmarks import BENCHMARK_MODELS
    from dreamscale.sim.task_list import run_list

    if benchmark is None and task_suite is not None:
        raise typer.BadParameter("--task-suite needs a benchmark: dreamscale sim <benchmark> "
                                 "--task-suite <suite> --list", param_hint="--task-suite")
    if benchmark is not None and benchmark not in BENCHMARK_MODELS:
        raise typer.BadParameter(
            "choose a benchmark: dreamscale sim libero, robocasa365, molmospaces, roboeval "
            "or abc",
            param_hint="benchmark",
        )
    try:
        run_list(benchmark, task_suite, json_output=json_output, print_fn=typer.echo)
    except ValueError as exc:
        raise typer.BadParameter(str(exc), param_hint="--task-suite") from exc


@app.command(cls=SteadySendCommand)
def sim(
    ctx: typer.Context,
    benchmark: str | None = typer.Argument(
        None, help="libero, robocasa365, molmospaces, roboeval or abc."
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        callback=_model_name,
        # No model list here: `dreamscale models list` shows only what the organization can run.
        help="Required: the model to run. `dreamscale models list` lists yours.",
    ),
    task_suite: str | None = typer.Option(
        None,
        "--task-suite",
        help=(
            "libero: libero_spatial (default), libero_object, libero_goal, libero_10 or "
            "libero_90. robocasa365: atomic or composite. molmospaces: benchmark or all "
            "(default). roboeval: a task (default lift_pot). abc: a task (default "
            "put_plastic_bottles_in_bin)."
        ),
    ),
    task_id: str | None = typer.Option(
        None,
        "--task-id",
        help="Task within the suite (default 0). molmospaces also takes all. abc: the "
        "episode number.",
    ),
    task_seed: int = typer.Option(
        0,
        "--task-seed",
        help="Seed for the task's initial state.",
    ),
    keep_warm: int | None = _keep_warm_option(),
    max_steps: int | None = typer.Option(
        None,
        "--max-steps",
        min=1,
        help="Action-step limit (default: the task's horizon).",
    ),
    max_duration: float | None = typer.Option(
        None,
        "--max-duration",
        min=0.1,
        help="Time limit in seconds, instead of --max-steps.",
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="No viewer; print a JSON summary at the end (with --list: the list as JSON).",
    ),
    transport: Annotated[
        SimTransport,
        typer.Option(
            "--transport",
            help="auto (QUIC, then relay), quic or relay.",
        ),
    ] = SimTransport.auto,
    region: str | None = typer.Option(
        None,
        "--region",
        help=_REGION_HELP,
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show diagnostic details."),
    output_root: Annotated[
        Path | None,
        typer.Option(
            "--output-root",
            help="Save the run's artifacts to this directory.",
        ),
    ] = None,
    steady_send: bool = _steady_send_options()[0],
    steady_send_ms: str | None = _steady_send_options()[1],
    list_tasks: bool = typer.Option(
        False,
        "--list",
        help="List the benchmarks, a benchmark's suites, or with --task-suite its tasks, "
        "instead of running one.",
    ),
) -> None:
    """Run a task on a simulated benchmark."""
    if list_tasks:
        _sim_list(benchmark, task_suite, json_output=non_interactive)
        return
    if (
        benchmark is None
        and task_suite is None
        and task_id is None
        and task_seed == 0
        and keep_warm is None
        and max_steps is None
        and max_duration is None
        and not non_interactive
        and transport == SimTransport.auto
        and region is None
        and not verbose
        and output_root is None
        and model is None
        and not steady_send
        and steady_send_ms is None
    ):
        typer.echo(ctx.get_help())
        raise typer.Exit()
    from dreamscale.sim.benchmarks import (
        BENCHMARK_LABELS,
        BENCHMARK_MODELS,
        DEFAULT_SUITES,
        default_task_horizon,
        validate_selection,
    )

    floor_ms = _steady_send(steady_send, steady_send_ms)
    steady = {"steady_send": floor_ms} if floor_ms is not None else {}

    if benchmark not in BENCHMARK_MODELS:
        raise typer.BadParameter(
            "choose a benchmark: dreamscale sim libero, robocasa365, molmospaces, roboeval "
            "or abc",
            param_hint="benchmark",
        )
    if benchmark == "libero":
        task_suite = task_suite or DEFAULT_SUITES[benchmark]
        task_id = task_id or "0"
    if model is None:
        from dreamscale import errors

        raise click.MissingParameter(
            f"Choose what {BENCHMARK_LABELS[benchmark]} runs. {errors.SEE_MODELS}",
            param_hint="'--model'",
            param_type="option",
        )
    keep_warm = _keep_warm(model, keep_warm)
    if benchmark in ("molmospaces", "roboeval", "abc"):
        task_suite = task_suite or DEFAULT_SUITES[benchmark]
        task_id = task_id or "0"
    if task_suite is None or task_id is None:
        missing = [
            flag
            for flag, value in (("--task-suite", task_suite), ("--task-id", task_id))
            if value is None
        ]
        raise typer.BadParameter(f"missing required option(s): {', '.join(missing)}")
    if max_steps is not None and max_duration is not None:
        raise typer.BadParameter("choose only one episode budget: --max-steps or --max-duration")
    if benchmark == "libero":  # the other benchmarks prepare their own simulator runtimes
        from dreamscale import errors

        _ensure_extras(["sim"], label="LIBERO", setup_command=errors.COMMAND_SIM)
    from dreamscale.sim.sim_arm import _sim_contract, run_sim
    from dreamscale.sim.verne_libero import is_verne_libero

    if benchmark == "libero" and is_verne_libero(model):
        # Verne V0.5 LIBERO (a catalog model on Verne deployments): upstream's own loop, its
        # 30 Hz poses driving LIBERO's 20 Hz OSC_POSE controller.
        from dreamscale.sim.verne_libero import run_verne_libero

        if not str(task_id).isdigit():
            raise typer.BadParameter("--task-id is a task number", param_hint="--task-id")
        _run(
            run_verne_libero,
            model=model, task_suite=task_suite, task_id=int(task_id), task_seed=task_seed,
            max_steps=max_steps if max_duration is None else max(1, ceil(max_duration * 20)),
            region=region, real_time=True, json_output=non_interactive,
            output_root=output_root,
        )
        return
    if benchmark == "abc":
        # The YAM robot's simulator: the robot's own session and run loop (sim/abc.py), not a
        # catalog sim.
        from dreamscale.sim.abc import run_abc

        try:
            task_id = validate_selection(benchmark, model, task_suite, task_id)
        except ValueError as exc:
            raise typer.BadParameter(str(exc), param_hint="--model") from exc
        _run(
            run_abc,
            model=model, task_suite=task_suite, task_id=task_id, task_seed=task_seed,
            max_steps=max_steps, max_duration=max_duration, view=not non_interactive,
            real_time=True, json_output=non_interactive, keep_warm=keep_warm,
            transport=transport.value, region=region, output_root=output_root, **steady,
        )
        return
    try:
        task_id = validate_selection(benchmark, model, task_suite, task_id)
        contract = _sim_contract(model)
    except ValueError as exc:
        raise typer.BadParameter(str(exc), param_hint="--model") from exc
    if benchmark == "molmospaces":
        from dreamscale.sim.molmospaces import run_molmospaces

        _run(
            run_molmospaces,
            model=model,
            task_suite=task_suite,
            task_id=task_id,
            task_seed=task_seed,
            max_steps=max_steps,
            max_duration=max_duration,
            view=not non_interactive,
            tui=not non_interactive,
            real_time=True,
            json_output=non_interactive,
            keep_warm=keep_warm,
            transport=transport.value,
            region=region,
            verbose=verbose,
            output_root=output_root,
            **steady,
        )
        return
    resolved_max_steps = (
        max(1, ceil(max_duration * contract.action_hz))
        if max_duration is not None
        else max_steps
        or default_task_horizon(benchmark, task_suite, task_id, action_hz=contract.action_hz)
    )

    _run(
        run_sim,
        **({"benchmark": benchmark} if benchmark != "libero" else {}),
        model=model,
        max_steps=resolved_max_steps,
        # A time limit counts every tick; a step budget counts what the sim's model counts.
        **({"count_holds": True} if max_duration is not None else {}),
        view=not non_interactive,
        tui=not non_interactive,
        real_time=True,
        transport=transport.value,
        region=region,
        task_suite=task_suite,
        task_id=task_id,
        task_seed=task_seed,
        keep_warm=keep_warm,
        verbose=verbose,
        json_output=non_interactive,
        output_root=output_root,
        **steady,
    )


@models_app.command("list")
def models(
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show where each model serves and its live state."
    ),
) -> None:
    """List models your organization can run."""
    from dreamscale.models_cmd import run_models

    _run(run_models, json_output=json_output, verbose=verbose)


@sessions_app.command("list")
def sessions(
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """List your open sessions."""
    from dreamscale.sessions_cmd import run_sessions

    _run(run_sessions, json_output=json_output)


@sessions_app.command("stop")
def stop(
    session_id: str = typer.Argument(None, help="Session ID."),
    all: bool = typer.Option(False, "--all", help="Stop all your open sessions."),
) -> None:
    """Stop a session, or all of them, to end billing."""
    from dreamscale.sessions_cmd import run_stop

    _run(run_stop, session_id=session_id, stop_all=all)


_MODEL_OPTION = typer.Option(
    "perceptron-isaac05-yam", "--model", help="Base model the weights fine-tune.",
    callback=_model_name,
)


_CAMERA_OPTION = typer.Option(
    None,
    "--camera",
    help="key=slot (base, left_wrist, right_wrist), repeated in the order your robot sends "
    "cameras.",
)
# Flags each base takes; the other base's are refused by name. Isaac 0.5, ABC-VLA and
# InternW0-Δ are unlisted for now: their --base still works, the flags only they take are
# hidden.
_ISAAC_ONLY = ("image_size", "action_dim", "state_dim", "chunk", "dataset", "context")
_DEFAULT_BASE_ONLY = (
    "path", "horizon", "executed", "token_length", "no_state_in_prompt", "delta_mask", "rtc",
    "rtc_max_delay",
)


_REGION_FALLBACK_OPTION = typer.Option(
    None, "--region-fallback/--no-region-fallback",
    help="If its region is full, start its server in the next-closest region (default on; "
    "each request then takes a little longer). Change it later with `dreamscale "
    "deployments fallback`.",
)


def _flag(name: str) -> str:
    return "--" + name.replace("_", "-")


def _base_labels(predicate=lambda base: True) -> str:
    """The listed deployment bases' names for help text, from their registry ("A, B or C");
    an unlisted base is never named."""
    from dreamscale import deploy_bases

    labels = [base.label for base in deploy_bases.bases() if base.listed_as and predicate(base)]
    return ", ".join(labels[:-1]) + (" or " if len(labels) > 1 else "") + labels[-1]


_CREATE_HELP = (
    f"Deploy fine-tuned weights of {_base_labels()} (pick with --base) from Hugging Face (any "
    "huggingface.co link works, including a checkpoint folder's page) or from a local folder "
    "(only the files the build reads are uploaded; a re-run sends nothing new)."
)
_RTC_HELP = (
    f"Set a {_base_labels(lambda base: base.set_rtc is not None)} deployment's RTC for its new "
    "sessions (no rebuild), as its base allows."
)


@deployments_app.command("create", help=_CREATE_HELP)
@endpoints_app.command("create", help=_CREATE_HELP)
def deployments_create(
    repo: str | None = typer.Argument(
        None, help="Hugging Face repo (hf://owner/name, owner/name or a huggingface.co link), "
        "or a local checkpoint folder (./folder). Omit with --official."
    ),
    base: str | None = typer.Option(
        None, "--base",
        help="Base model: pi0.5 (default), flux-3-action-base, lingbot-vla, hy-vla, "
        "xiaomi-robotics-1 or gr00t-n1.7. "
        "A folder `dreamscale train download` made needs none: its base is read from it."
    ),
    preset: str | None = typer.Option(
        None,
        "--preset",
        help="bimanual_yam, so101, arx5 or blank (default: detected from the repo).",
    ),
    camera: list[str] | None = _CAMERA_OPTION,
    image_size: str | None = typer.Option(
        None, "--image-size", help="HEIGHTxWIDTH, e.g. 360x640.", hidden=True
    ),
    action_dim: int | None = typer.Option(
        None, "--action-dim", help="Action dimension.", hidden=True
    ),
    state_dim: int | None = typer.Option(None, "--state-dim", help="State dimension.", hidden=True),
    chunk: int | None = typer.Option(
        None, "--chunk", help="Actions executed per chunk (1-50).", hidden=True
    ),
    hz: float | None = typer.Option(None, "--hz", help="Control rate in Hz the weights expect."),
    dataset: str | None = typer.Option(
        None,
        "--dataset",
        help="Dataset whose normalization stats to use, e.g. libero_spatial (see "
        "`deployments inspect`).",
        hidden=True,
    ),
    context: int | None = typer.Option(
        None, "--context", help="Observation frames: 1 or 3.", hidden=True
    ),
    path: str | None = typer.Option(
        None, "--path", help="π0.5: the checkpoint in the repo, e.g. checkpoints/55000 "
        "(default: the latest)."
    ),
    horizon: int | None = typer.Option(
        None, "--horizon", help="π0.5: actions the model predicts per chunk (default 50)."
    ),
    executed: int | None = typer.Option(
        None, "--executed", help="π0.5: actions executed per chunk (default: the horizon)."
    ),
    token_length: int | None = typer.Option(
        None, "--token-length", help="π0.5: prompt length in tokens (default 200)."
    ),
    no_state_in_prompt: bool = typer.Option(
        False, "--no-state-in-prompt", help="π0.5: the checkpoint was trained without the "
        "state in its prompt."
    ),
    delta_mask: str | None = typer.Option(
        None, "--delta-mask", help="π0.5: 1 or 0 per action, comma separated (1 = relative "
        "to the state), or none."
    ),
    rtc: str | None = typer.Option(
        None, "--rtc", help="π0.5: off, test-time or trained; Hy-VLA: off or trained "
        "(default: detected)."
    ),
    rtc_prefix: int | None = typer.Option(
        None, "--rtc-prefix", help="Hy-VLA trained RTC: at most this many planned actions "
        "pinned per request (default: all the checkpoint was trained on)."
    ),
    steps: int | None = typer.Option(
        None, "--steps", help="ABC-VLA: denoising steps (default 10, as upstream).",
        hidden=True,
    ),
    joint_unit: str | None = typer.Option(
        None, "--joint-unit",
        help="InternW0-Δ, or an ABC-VLA custom robot: its actions are joint positions in this "
        "unit (e.g. rad); omitted, they're model-defined.",
        hidden=True,
    ),
    rtc_max_delay: int | None = typer.Option(
        None, "--rtc-max-delay", help="π0.5: the delay trained RTC was trained with (1-15)."
    ),
    revision: str | None = typer.Option(None, "--revision", help="Branch, tag or commit."),
    # Older name: what the slug is made from (a deployment's name is its slug).
    name: str | None = typer.Option(None, "--name", hidden=True),
    hf_token: str | None = typer.Option(None, "--hf-token", help=_HF_TOKEN_HELP),
    region: str = typer.Option(
        "auto",
        "--region",
        help="Where it serves: a region id such as us-west or japan (the server lists the live "
        "ones), or auto: the nearest one its base serves, measured from here.",
    ),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once the build starts."),
    keep_warm: str | None = typer.Option(
        None,
        "--keep-warm",
        help="How long its server stays up after the last robot leaves: off, 10m, 30m, 1h, 2h, "
        "6h, 12h or always (billed as server time; default off).",
    ),
    slug: str | None = typer.Option(
        None,
        "--slug",
        help="Its name, the <model> of <account>/<model> (default: from the repo, plus the "
        "checkpoint's step).",
    ),
    region_fallback: bool | None = _REGION_FALLBACK_OPTION,
    official: str | None = typer.Option(
        None, "--official", help="Instead of a repo: one of the base's own published "
        "checkpoints by name (Verne V0.5: base, robotwin, libero; `deployments list` shows "
        "them)."
    ),
    arm: str | None = typer.Option(
        None, "--arm", help="Verne V0.5 custom robot: right for one arm (default both)."
    ),
) -> None:
    """Deploy fine-tuned weights (``_CREATE_HELP``: every registered deployment base)."""
    from dreamscale.checkpoints_cmd import (
        BASE_LABELS,
        BASE_MODEL,
        build_embodiment,
        detect_embodiment,
        downloaded_base,
        parse_base,
        parse_cameras,
        parse_image_size,
        parse_region,
        run_add,
    )

    given = {
        "image_size": image_size, "action_dim": action_dim, "state_dim": state_dim,
        "chunk": chunk, "dataset": dataset, "context": context, "path": path,
        "horizon": horizon, "executed": executed, "token_length": token_length,
        "no_state_in_prompt": no_state_in_prompt or None, "delta_mask": delta_mask, "rtc": rtc,
        "rtc_max_delay": rtc_max_delay, "arm": arm,
    }
    from dreamscale import deploy_bases
    from dreamscale.local_checkpoint import is_local_folder

    if official is not None:
        if repo is not None:
            raise typer.BadParameter("give a repo or --official, not both", param_hint="'repo'")
        if base is None:
            raise typer.BadParameter("an official checkpoint names its base with --base",
                                     param_hint="'--base'")
        try:
            chosen = parse_base(base)
        except ValueError as error:
            raise typer.BadParameter(str(error), param_hint="'--base'") from None
        create_official = deploy_bases.named(chosen).create_official
        if create_official is None:
            raise typer.BadParameter(f"{BASE_LABELS.get(chosen, chosen)} has no official "
                                     "checkpoints", param_hint="'--official'")
        create_official(
            official=official, preset=preset, camera=camera,
            given={k: v for k, v in given.items() if v is not None}, rtc=rtc, name=name,
            region=region, wait=not no_wait, keep_warm=keep_warm, slug=slug,
            region_fallback=region_fallback,
        )
        return
    if repo is None:
        raise typer.BadParameter("a repo or local folder is required (or --official)",
                                 param_hint="'repo'")
    local = is_local_folder(repo)
    try:
        chosen = parse_base(base or downloaded_base(repo, path))
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="'--base'") from None

    # A base with its own create (every base but Isaac 0.5's legacy path) takes every option;
    # Isaac 0.5 follows.
    create = deploy_bases.named(chosen).create
    if create is not None:
        create(
            repo=repo, given=given, preset=preset, camera=camera, hz=hz, path=path,
            executed=executed, steps=steps, joint_unit=joint_unit, rtc=rtc,
            rtc_prefix=rtc_prefix, revision=revision, name=name, hf_token=hf_token,
            region=region, wait=not no_wait, keep_warm=keep_warm, slug=slug,
            region_fallback=region_fallback,
        )
        return
    for flag, value in (("--rtc-prefix", rtc_prefix), ("--steps", steps),
                        ("--joint-unit", joint_unit)):
        if value is not None:
            raise typer.BadParameter(f"{flag} doesn't apply to {BASE_LABELS[chosen]} "
                                     "deployments.", param_hint=f"'{flag}'")
    default = deploy_bases.default()
    if local:
        raise typer.BadParameter(
            f"a local folder deploys on {default.label} only (Isaac 0.5 deploys from Hugging "
            "Face).",
            param_hint="'--base'",
        )
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES

    if keep_warm is not None and keep_warm not in KEEP_WARM_VALUES:
        raise typer.BadParameter(
            f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    for field in _DEFAULT_BASE_ONLY:
        if given[field] is not None:
            raise typer.BadParameter(f"{_flag(field)} applies to {default.label} (--base "
                                     f"{default.listed_as}) deployments only.")
    try:
        region = parse_region(region)
        detected = (
            detect_embodiment(repo=repo, revision=revision, hf_token=hf_token)
            if preset is None
            else None
        )
        embodiment = build_embodiment(
            preset=preset, detected=detected, cameras=parse_cameras(camera),
            image_size=parse_image_size(image_size), action_dim=action_dim,
            state_dim=state_dim, chunk=chunk, hz=hz, dataset=dataset, context=context,
        )
    except ValueError as error:
        raise typer.BadParameter(str(error)) from None
    result: dict = {}
    _run(
        lambda **kwargs: result.update(run_add(**kwargs)),
        repo=repo,
        model=BASE_MODEL,
        revision=revision,
        name=name,
        hf_token=hf_token,
        embodiment=embodiment,
        region=region,
        wait=not no_wait,
        **({"keep_warm": keep_warm} if keep_warm is not None else {}),
        **({"slug": slug} if slug is not None else {}),
        **({"region_fallback": region_fallback} if region_fallback is not None else {}),
    )
    if result.get("status") == "failed":
        raise typer.Exit(code=1)


@deployments_app.command("inspect")
@endpoints_app.command("inspect")
def deployments_inspect(
    repo: str = typer.Argument(
        ..., help="Hugging Face repo (hf://owner/name, owner/name or a huggingface.co link), "
        "or a local π0.5 checkpoint folder (./folder; nothing is uploaded)."
    ),
    base: str = typer.Option(
        "auto", "--base",
        help="pi0.5, flux-3-action-base, hy-vla or auto."
    ),
    path: str | None = typer.Option(
        None, "--path", help="π0.5: the checkpoint in the repo, e.g. checkpoints/55000."
    ),
    revision: str | None = typer.Option(None, "--revision", help="Branch, tag or commit."),
    hf_token: str | None = typer.Option(None, "--hf-token", help=_HF_TOKEN_HELP),
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """Show a repo's (or a local folder's) robot shape, what was detected and where from."""
    from dreamscale.checkpoints_cmd import downloaded_base, parse_base, run_inspect

    try:
        chosen = parse_base(base, allow_auto=True)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="'--base'") from None
    if chosen == "auto":
        try:
            chosen = downloaded_base(repo, path) or chosen
        except ValueError as error:
            raise typer.BadParameter(str(error), param_hint="'--base'") from None
    _run(
        run_inspect, repo=repo, revision=revision, hf_token=hf_token, json_output=json_output,
        base=chosen, path=path,
    )


@checkpoints_app.command("add")
def checkpoints_add(
    repo: str = typer.Argument(..., help="Hugging Face repo: hf://owner/name or owner/name."),
    model: str = _MODEL_OPTION,
    revision: str | None = typer.Option(None, "--revision", help="Branch, tag or commit."),
    name: str | None = typer.Option(None, "--name", help="Display name."),
    hf_token: str | None = typer.Option(None, "--hf-token", help=_HF_TOKEN_HELP),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once the build starts."),
) -> None:
    """Import fine-tuned weights from Hugging Face."""
    from dreamscale.checkpoints_cmd import run_add

    result: dict = {}
    _run(
        lambda **kwargs: result.update(run_add(**kwargs)),
        repo=repo,
        model=model,
        revision=revision,
        name=name,
        hf_token=hf_token,
        wait=not no_wait,
    )
    if result.get("status") == "failed":
        raise typer.Exit(code=1)


@deployments_app.command("list")
@endpoints_app.command("list")
@checkpoints_app.command("list")
def deployments_list(
    model: str | None = typer.Option(
        None, "--model", help="Only deployments of this model.", callback=_model_name
    ),
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """List your organization's deployments."""
    from dreamscale.checkpoints_cmd import run_list

    _run(run_list, model=model, json_output=json_output)


@deployments_app.command("show")
@endpoints_app.command("show")
@checkpoints_app.command("show")
def deployments_show(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """Show a deployment's status, build progress or error."""
    from dreamscale.checkpoints_cmd import run_show

    _run(run_show, checkpoint_id=checkpoint_id, json_output=json_output)


# Hidden, kept for old scripts: sessions run a deployment only when they name it.
@endpoints_app.command("use")
@checkpoints_app.command("use")
def deployments_default(
    checkpoint: str = typer.Argument(..., help="Deployment ID (ckpt_…), or `base`."),
    model: str | None = typer.Option(
        None,
        "--model",
        callback=_model_name,
        help="Model to set it for (default: the deployment's model, or "
        "perceptron-isaac05-yam for base).",
    ),
) -> None:
    """Make a deployment (or base) the default for its model."""
    from dreamscale.checkpoints_cmd import run_use

    _run(run_use, checkpoint=checkpoint, model=model)


@deployments_app.command("keep-warm")
def deployments_keep_warm(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
    value: str = typer.Argument(
        ...,
        help="How long its server stays up after the last robot leaves: off, 10m, 30m, 1h, "
        "2h, 6h, 12h or always (billed as server time).",
    ),
    take_over_from: str | None = typer.Option(
        None,
        "--take-over-from",
        help="Move always-on from this deployment once this one is warm.",
    ),
    robots: int | None = typer.Option(
        None,
        "--robots",
        min=1,
        max=64,
        help="Autoscaling deployments: how many robots stay ready (billed as at least that "
        "many robots while kept warm).",
    ),
    now: bool = typer.Option(
        False,
        "--now",
        help="Start it now rather than at the first robot, held for VALUE from now, and wait "
        "until it is ready (Ctrl-C stops waiting, not the server).",
    ),
) -> None:
    """Keep a deployment's server warm between runs."""
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES, run_keep_warm

    if value not in KEEP_WARM_VALUES:
        raise typer.BadParameter(f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="VALUE")
    if now and value == "off":
        raise typer.BadParameter("--now needs a keep-warm: 10m … always", param_hint="'--now'")
    _run(
        run_keep_warm,
        checkpoint_id=checkpoint_id,
        keep_warm=value,
        take_over_from=take_over_from,
        robots=robots,
        **({"now": True} if now else {}),
    )


@deployments_app.command("rtc", help=_RTC_HELP)
def deployments_rtc(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
    method: str = typer.Argument(..., help="off, test-time or trained, as the deployment's "
                                 "base allows (most run off or trained)."),
    max_delay: int | None = typer.Option(
        None, "--max-delay", help="π0.5: the delay trained RTC was trained with (1-15). "
        "FLUX 3 Action: the most planned actions pinned per request (default: all it trained)."
    ),
) -> None:
    """Set a deployment's RTC for its new sessions (``_RTC_HELP``: the bases with a setting)."""
    from dreamscale.checkpoints_cmd import parse_rtc, run_rtc

    try:
        parse_rtc(method)
    except ValueError as error:
        message = str(error).replace("--rtc", "METHOD")
        raise typer.BadParameter(message, param_hint="METHOD") from None
    _run(run_rtc, checkpoint_id=checkpoint_id, method=method, max_delay=max_delay)


@deployments_app.command("fallback")
def deployments_fallback(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
    setting: str = typer.Argument(..., help="on or off."),
) -> None:
    """Whether a deployment's server may start in the next-closest region when its own is
    full (on by default; the next-closest region is a little farther). For its next server;
    no rebuild."""
    from dreamscale.checkpoints_cmd import parse_on_off, run_fallback

    try:
        on = parse_on_off(setting)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="SETTING") from None
    _run(run_fallback, checkpoint_id=checkpoint_id, on=on)


@deployments_app.command("rename")
def deployments_rename(
    checkpoint_id: str = typer.Argument(
        ..., help="Deployment: <account>/<slug>, its slug, or its ckpt_… ID."
    ),
    slug: str | None = typer.Argument(
        None,
        help="Its new slug, the <model> of <account>/<model> (the old one keeps working until "
        "another deployment takes it).",
    ),
    slug_option: str | None = typer.Option(None, "--slug", hidden=True),
) -> None:
    """Rename a deployment: its name is its slug."""
    from dreamscale.checkpoints_cmd import run_rename

    if slug is not None and slug_option is not None and slug != slug_option:
        raise typer.BadParameter("give the new slug once")
    slug = slug or slug_option
    if slug is None:
        raise typer.BadParameter("give the new slug", param_hint="SLUG")
    _run(run_rename, checkpoint_id=checkpoint_id, slug=slug.strip())


@deployments_app.command("restart")
def deployments_restart(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
) -> None:
    """Stop the deployment's server now; with Always on a fresh one starts at once.

    A connected robot loses its connection and reconnects to a new server on its next
    request (the SDK holds it still meanwhile).
    """
    from dreamscale.checkpoints_cmd import run_restart

    _run(run_restart, checkpoint_id=checkpoint_id)


@deployments_app.command("stop")
def deployments_stop(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
) -> None:
    """Stop the deployment's server now and keep none warm (turns its keep-warm off).

    The next robot starts a fresh server; a connected robot loses its connection.
    """
    from dreamscale.checkpoints_cmd import run_stop

    _run(run_stop, checkpoint_id=checkpoint_id)


@deployments_app.command("rm")
@deployments_app.command("remove", hidden=True)
@endpoints_app.command("rm")
@checkpoints_app.command("rm")
def deployments_rm(
    checkpoint_id: str = typer.Argument(..., help=_DEPLOYMENT_ARG),
    yes: bool = typer.Option(False, "--yes", "-y", help="Delete without asking."),
) -> None:
    """Permanently delete a deployment (owners only). It cannot be undone."""
    from dreamscale.checkpoints_cmd import run_rm

    _run(run_rm, checkpoint_id=checkpoint_id, yes=yes)


def _run_train(fn, **kwargs) -> dict:
    """`_run` for training: Ctrl-C has already said what carries on, so exit quietly."""
    from dreamscale import errors

    try:
        return fn(**kwargs)
    except errors.DreamscaleError as error:
        typer.echo(error.render())
        raise typer.Exit(code=1) from error
    except KeyboardInterrupt as exc:
        raise typer.Exit(code=130) from exc


def _check_base(value: str | None) -> str | None:
    import re

    from dreamscale_transport import training_families

    if value in (None, "auto"):
        return None
    if re.fullmatch(r"tr_[0-9a-f]{24}", value):  # one of your runs: start from its checkpoint
        return value
    if training_families.is_base(value):  # a training base, or its alias
        return training_families.stored_base(value)
    if value.startswith(("hf://", "https://huggingface.co/")):
        raise typer.BadParameter(
            f"import it as a deployment first: dreamscale deployments create {value} (then "
            "--base <its name>); a checkpoint trains from its deployment"
        )
    # one of your deployments made from a run (its id, slug or account/slug): the server says
    # whether it is one; a run or deployment id is whole
    prefixed = value.startswith(("tr_", "ckpt_"))
    if (re.fullmatch(r"ckpt_[0-9a-f]{24}", value) if prefixed else re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}(/[A-Za-z0-9][A-Za-z0-9._-]{0,63})?", value
    )):
        return value
    raise typer.BadParameter(
        f"use auto, {', '.join(training_families.public_bases())}, one of your runs (tr_…) or "
        "one of your deployments"
    )


_TRAIN_POSITIONAL = typer.Argument(None, hidden=True, show_default=False)
_TRAIN_DATASETS = typer.Option(
    None, "--dataset", help="The dataset to train on: one of yours (towels, towels@2, "
    "acme/towels) or a Hugging Face one (hf://owner/name[@revision]). Repeat it for several "
    "Hugging Face datasets, which train together (they must match after the column mapping).",
    show_default=False,
)

_TRAIN_INPUT_OPTION = typer.Option(
    None, "--input", metavar="NAME=FILE.json",
    help="Something the base takes beside the dataset, as a JSON file (e.g. urdf=robot.json, "
    "the robot's URDF and its arms). Repeat for more.",
)
_TRAIN_CAMERA_OPTION = typer.Option(
    None, "--camera", help="A camera and its image slot, e.g. top=base (base, left_wrist, "
    "right_wrist); repeat for each. Default: chosen by the cameras' names."
)


def _rtc_choice(rtc: bool, no_rtc: bool) -> bool | None:
    """``--rtc`` / ``--no-rtc``, or None: the base's own default."""
    if rtc and no_rtc:
        raise typer.BadParameter("pass --rtc or --no-rtc, not both")
    return True if rtc else False if no_rtc else None


@train_app.command("create", hidden=True)
def train_create(
    positional: list[str] | None = _TRAIN_POSITIONAL,
    dataset: list[str] | None = _TRAIN_DATASETS,
    base: str | None = typer.Option(
        None, "--base", callback=_check_base,
        help="Start from pi0.5 (π0.5 base), flux-3-action-base (FLUX 3 Action), "
        "xiaomi-robotics-1 (Xiaomi-Robotics-1), gr00t-n1.7 (GR00T N1.7) or "
        "pi0.5-rtc-yam (π0.5 RTC YAM, our checkpoint trained on bimanual YAM; any robot) where "
        "your organization has them, one of your runs (tr_…: its latest checkpoint, or "
        "--base-step), or one of your deployments: one made from a run, or a π0.5 or FLUX 3 "
        "Action checkpoint you imported (the checkpoint it serves). Required.",
    ),
    base_step: int | None = typer.Option(
        None, "--base-step", min=1, help="With --base tr_…: start from this step's checkpoint."
    ),
    normalization: str | None = typer.Option(
        None, "--normalization", hidden=True,
        help="auto (default), inherit or recompute: a run continuing one of yours keeps its "
        "normalization (auto: unless the data moved far); recompute normalizes with this "
        "dataset, also from a base trained on another robot.",
    ),
    steps: int | None = typer.Option(
        None, "--steps", min=10, max=60_000, help="Training length in steps (default: Auto)."
    ),
    max_usd: float | None = typer.Option(
        None, "--max-usd", min=0.01, help="Train as long as this many dollars buys, instead."
    ),
    rtc: bool = typer.Option(
        False, "--rtc", help="Train with real-time chunking (RTC) where the base offers it "
        "(flux-3-action-base: experimental, off by default)."
    ),
    no_rtc: bool = typer.Option(
        False, "--no-rtc", help="Train without real-time chunking (RTC; on by default for pi0.5)."
    ),
    name: str | None = typer.Option(None, "--name", help="Display name (default: the dataset)."),
    hf_token: str | None = typer.Option(None, "--hf-token", help=_HF_TOKEN_HELP),
    yes: bool = typer.Option(False, "--yes", "-y", help="Accept the quote without asking."),
    quote: bool = typer.Option(
        False, "--quote", help="Show the quote and stop: nothing is started, even with --yes."
    ),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once the run starts."),
    json_output: bool = typer.Option(
        False, "--json", help="Print the run (with --quote: the quote) as JSON."
    ),
    no_clean: bool = typer.Option(
        False, "--no-clean", help="Train every episode as recorded: no auto-clean (it cuts out "
        "faulty stretches, trims idle starts and ends, and drops episodes that can't be trained "
        "on)."
    ),
    learning_rate: float | None = typer.Option(
        None, "--learning-rate", min=0, max=0.01,
        help="Peak learning rate. Default: the recipe's for the batch (continuing from one of "
        "your runs with --base tr_…: half the recipe's, at most that run's).",
    ),
    batch_size: int | None = typer.Option(
        None, "--batch-size", min=1,
        help="Global batch: π0.5 64, 128, 256 or 512; FLUX 3 Action 32, 64, 128 or 256. "
        "Default: from the data. The quote follows it.",
    ),
    warmup_steps: int | None = typer.Option(
        None, "--warmup-steps", min=1, help="Steps warming up to the peak learning rate. "
        "Default: the recipe's.",
    ),
    schedule: str | None = typer.Option(
        None, "--schedule", help="π0.5's learning rate after its warm-up: cosine (decays over "
        "the run) or constant. Default: the recipe's for the batch.",
    ),
    checkpoint_every: int | None = typer.Option(
        None, "--checkpoint-every", min=1, help="Save a deployable checkpoint every N steps "
        "(at most 20 a run; the last step always saves). Default: 5 a run.",
    ),
    prompt: str | None = typer.Option(None, "--prompt", hidden=True),
    no_hardware_check: bool = typer.Option(False, "--no-hardware-check", hidden=True),
    no_trim_idle: bool = typer.Option(False, "--no-trim-idle", hidden=True),
    state: str | None = typer.Option(
        None, "--state", help="The state's columns, joined in order (a+b). Default: "
        "observation.state."
    ),
    action: str | None = typer.Option(
        None, "--action", help="The action's columns, joined in order (a+b). Default: action."
    ),
    camera: list[str] | None = _TRAIN_CAMERA_OPTION,
    ee_state: str | None = typer.Option(
        None, "--ee-state", metavar="COLUMNS",
        help="For a base that learns end-effector poses: the measured pose columns, each arm's "
        "xyz then its rotation (a+b, or column[0-8,10-18]). With --ee-action and --ee-rotation.",
    ),
    ee_action: str | None = typer.Option(
        None, "--ee-action", metavar="COLUMNS",
        help="The commanded end-effector pose columns, laid out as --ee-state.",
    ),
    ee_rotation: str | None = typer.Option(
        None, "--ee-rotation",
        help="The poses' rotation: quat_xyzw, quat_wxyz, matrix, axis_angle or rot6d.",
    ),
    run_input: list[str] | None = _TRAIN_INPUT_OPTION,
    sample_weight: str | None = typer.Option(
        None, "--sample-weight", metavar="COLUMN",
        help="A one-value column with each episode's sample weight (the same value on every "
        "frame): its samples are drawn that many times as often; 0 leaves it out. π0.5 and "
        "FLUX 3 Action.",
    ),
    loss_mask: str | None = typer.Option(
        None, "--loss-mask", metavar="COLUMN",
        help="A one-value column, 1 on frames whose actions shouldn't train (0 elsewhere): they "
        "stay in their episode as context. π0.5 and FLUX 3 Action.",
    ),
    eval_fraction: float | None = typer.Option(
        None, "--eval-fraction", min=0.05, max=0.3,
        help="Hold this share of the episodes out (0.05-0.3) and report a held-out loss per "
        "checkpoint. Off by default. Held-out loss is a poor proxy for task success in "
        "diffusion and flow-matching policies (it often rises while the policy improves): try "
        "checkpoints on the robot.",
    ),
) -> None:
    """Quote and fine-tune a base model on a dataset (one confirm)."""
    from dreamscale import errors
    from dreamscale.train_cmd import run_create
    from dreamscale.trainings import parse_inputs, parse_mapping, upload_first

    if positional:
        # The form before --dataset: a folder uploads first; a name moves to the flag.
        first = positional[0]
        try:
            if first.startswith((".", "/", "~")) or Path(first).expanduser().is_dir():
                raise upload_first(first)
            raise errors.DreamscaleError(errors.ErrorInfo(
                code="dataset_flag_required",
                problem="dreamscale train takes --dataset and --base",
                cause=f"{first} was given without --dataset",
                fix=f"dreamscale train --dataset {first} --base BASE",
            ))
        except errors.DreamscaleError as error:
            typer.echo(error.render())
            raise typer.Exit(code=1) from error
    if not dataset:
        typer.echo(errors.catalog("dataset_required").render())
        raise typer.Exit(code=1)
    if steps is not None and max_usd is not None:
        raise typer.BadParameter("pass --steps or --max-usd, not both (neither: Auto)")
    if base_step is not None and not (base or "").startswith("tr_"):
        raise typer.BadParameter("--base-step goes with --base tr_…")
    if normalization not in (None, "auto", "inherit", "recompute"):
        raise typer.BadParameter("--normalization: auto, inherit or recompute")
    if schedule not in (None, "cosine", "constant"):
        raise typer.BadParameter("--schedule: cosine or constant")
    no_hardware_check = no_hardware_check or no_clean  # the older, hidden spelling
    inputs = _run_train(parse_inputs, specs=run_input) if run_input else None
    run = _run_train(
        run_create, dataset=dataset[0] if len(dataset) == 1 else dataset, base=base,
        steps=steps, max_usd=max_usd,
        rtc=_rtc_choice(rtc, no_rtc),
        name=name, hf_token=hf_token, learning_rate=learning_rate, prompt=prompt,
        hardware_check=not no_hardware_check, trim_idle=not no_trim_idle, yes=yes,
        wait=not no_wait, json_output=json_output, quote_only=quote, eval_fraction=eval_fraction,
        mapping=_run_train(
            parse_mapping, state=state, action=action, cameras=camera, weight=sample_weight,
            loss_mask=loss_mask, ee_state=ee_state, ee_action=ee_action, ee_rotation=ee_rotation,
        ),
        inputs=inputs,
        base_step=base_step, normalization=normalization, batch_size=batch_size,
        warmup_steps=warmup_steps, lr_schedule=schedule, checkpoint_every=checkpoint_every,
    )
    if run.get("status") == "failed":
        raise typer.Exit(code=1)


@datasets_app.command("upload")
def datasets_upload(
    folder: str = typer.Argument(..., help="The LeRobot dataset's root folder."),
    name: str | None = typer.Option(
        None, "--name", help="The dataset's name (default: the folder's, made valid)."
    ),
    no_check: bool = typer.Option(
        False, "--no-check", help="Skip reading the recordings here (training checks them again)."
    ),
    concurrency: int = typer.Option(8, "--concurrency", hidden=True, min=1, max=64),
    json_output: bool = typer.Option(False, "--json", help="Print the dataset as JSON."),
) -> None:
    """Upload a folder: what's new is sent, and a new version recorded. Rerun it to resume."""
    from dreamscale.datasets_cmd import run_upload

    _run_train(run_upload, folder=folder, name=name, check=not no_check,
               concurrency=concurrency, json_output=json_output)


@datasets_app.command("import")
def datasets_import(
    source: str = typer.Argument(
        ..., help="hf://OWNER/NAME, with /FOLDER and @REVISION if you need them."
    ),
    name: str | None = typer.Option(
        None, "--name", help="The dataset's name (default: the repo's)."
    ),
    hf_token: str | None = typer.Option(None, "--hf-token", help=_HF_TOKEN_HELP),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once the copy starts."),
    json_output: bool = typer.Option(False, "--json", help="Print the dataset as JSON."),
) -> None:
    """Copy a Hugging Face dataset in, on our side. Importing again copies only what changed."""
    from dreamscale.datasets_cmd import run_import

    _run_train(run_import, source=source, name=name, hf_token=hf_token, wait=not no_wait,
               json_output=json_output)


@datasets_app.command("list")
def datasets_list(
    json_output: bool = typer.Option(False, "--json", help="Print the datasets as JSON."),
) -> None:
    """Your datasets."""
    from dreamscale.datasets_cmd import run_list

    _run_train(run_list, json_output=json_output)


@datasets_app.command("show")
def datasets_show(
    name: str = typer.Argument(..., help="NAME, or NAME@N for one version."),
    json_output: bool = typer.Option(False, "--json", help="Print the dataset as JSON."),
) -> None:
    """A dataset's summary, versions and runs; follows a running import."""
    from dreamscale.datasets_cmd import run_show

    _run_train(run_show, name=name, json_output=json_output)


@datasets_app.command("download")
def datasets_download(
    name: str = typer.Argument(..., help="NAME, or NAME@N for one version."),
    folder: str | None = typer.Argument(None, help="Where to (default: ./NAME)."),
) -> None:
    """Download a version into a LeRobot folder. Rerun it to resume."""
    from dreamscale.datasets_cmd import run_download

    _run_train(run_download, name=name, folder=folder)


@datasets_app.command("rename")
def datasets_rename(
    name: str = typer.Argument(..., help="NAME"),
    new_name: str = typer.Argument(
        ..., help="Its new name (the old one keeps working until another dataset takes it)."
    ),
) -> None:
    """Rename a dataset."""
    from dreamscale.datasets_cmd import run_rename

    _run_train(run_rename, name=name, new_name=new_name)


@datasets_app.command("rm")
@datasets_app.command("remove", hidden=True)
def datasets_rm(
    name: str = typer.Argument(..., help="NAME for the whole dataset, or NAME@N for one version."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Delete without asking."),
) -> None:
    """Delete a dataset or one version, for good. What was made from it keeps working."""
    from dreamscale.datasets_cmd import run_rm

    _run_train(run_rm, name=name, yes=yes)


@train_app.command("list")
def train_list(
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """List your organization's training runs."""
    from dreamscale.train_cmd import run_list

    _run_train(run_list, json_output=json_output)


@train_app.command("show")
def train_show(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON."),
) -> None:
    """Show a training run; follows it live while it runs."""
    from dreamscale.train_cmd import run_show

    run = _run_train(run_show, run_id=run_id, json_output=json_output)
    if run.get("status") == "failed":
        raise typer.Exit(code=1)


@train_app.command("stop")
def train_stop(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Stop without asking."),
) -> None:
    """Stop a training run: it saves, you pay for the steps it completed, and it can resume."""
    from dreamscale.train_cmd import run_cancel

    _run_train(run_cancel, run_id=run_id, yes=yes)


@train_app.command("cancel", hidden=True)
def train_cancel(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Stop without asking."),
) -> None:
    """The older name of `stop`."""
    from dreamscale.train_cmd import run_cancel

    _run_train(run_cancel, run_id=run_id, yes=yes)


@train_app.command("resume")
def train_resume(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Accept the price without asking."),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once it resumes."),
    json_output: bool = typer.Option(False, "--json", help="Print the run as JSON."),
) -> None:
    """Resume a stopped training run for its remaining steps."""
    from dreamscale.train_cmd import run_resume

    run = _run_train(run_resume, run_id=run_id, yes=yes, wait=not no_wait,
                     json_output=json_output)
    if run.get("status") == "failed":
        raise typer.Exit(code=1)


@train_app.command("rm")
def train_rm(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Delete without asking."),
) -> None:
    """Permanently delete a training run (one still going is canceled first)."""
    from dreamscale.train_cmd import run_rm

    _run_train(run_rm, run_id=run_id, yes=yes)


@train_app.command("download")
def train_download(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    step: int | None = typer.Option(
        None, "--step", min=1, help="Checkpoint step (default: the latest)."
    ),
    output: str | None = typer.Option(
        None, "--output", "-o", help="File or folder to save it in (default: here)."
    ),
    link: bool = typer.Option(
        False, "--link", help="Print a signed link (valid an hour) instead of downloading."
    ),
) -> None:
    """Download a checkpoint and its training contract as a tar archive."""
    from dreamscale.train_cmd import run_download

    _run_train(run_download, run_id=run_id, step=step, output=output, link=link)


@train_app.command("deploy")
def train_deploy(
    run_id: str = typer.Argument(..., help="Training run ID (tr_…)."),
    step: int | None = typer.Option(
        None, "--step", min=1, help="Checkpoint step (default: the latest)."
    ),
    region: str = typer.Option(
        "auto", "--region",
        help="Where it serves: a region id such as us-west or japan, or auto: the nearest one "
        "its base serves, measured from here.",
    ),
    no_wait: bool = typer.Option(False, "--no-wait", help="Return once the build starts."),
    region_fallback: bool | None = _REGION_FALLBACK_OPTION,
) -> None:
    """Deploy a checkpoint of a training run (no form: the dataset defined the robot)."""
    from dreamscale.checkpoints_cmd import parse_region
    from dreamscale.train_cmd import run_deploy

    try:
        region = parse_region(region)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from None
    deployment = _run_train(
        run_deploy, run_id=run_id, step=step, region=region, region_fallback=region_fallback,
        wait=not no_wait,
    )
    if deployment.get("status") == "failed":
        raise typer.Exit(code=1)


def _ensure_so101() -> None:
    from dreamscale import errors

    _ensure_extras(["so101"], label="SO-101", setup_command=errors.COMMAND_QUICKSTART)


@so101_app.command("setup")
def robots_so101_setup(
    cli: bool = typer.Option(
        False, "--cli", help="Answer terminal prompts instead of using the setup page.",
    ),
    host: str = typer.Option("0.0.0.0", "--host", help="Setup page server host."),
    port: int = typer.Option(8765, "--port", min=1, max=65535, help="Setup page server port."),
) -> None:
    """Install SO-101 support, then choose its cameras and port."""
    if cli:
        from dreamscale.quickstart import run_quickstart

        _run(run_quickstart)
        return
    from dreamscale import errors
    from dreamscale.hardware.so101_setup import run_so101_page

    _ensure_extras(["so101"], label="SO-101", setup_command=errors.COMMAND_QUICKSTART)
    _run_robot_command(run_so101_page, host=host, port=port)


@so101_app.command("calibrate")
def robots_so101_calibrate() -> None:
    """Calibrate the arm, step by step."""
    from dreamscale.calibrate import run_calibrate

    _ensure_so101()

    _run(run_calibrate)


@so101_app.command("home")
def robots_so101_home(
    set_pose: bool = typer.Option(
        False,
        "--set",
        help="Save the current pose as home (motors go limp so you can pose the arm).",
    ),
) -> None:
    """Move to the home pose, then release motor torque."""
    from dreamscale.homing import run_home, run_set_home

    _ensure_so101()

    _run(run_set_home if set_pose else run_home)


@so101_app.command("release")
def robots_so101_release() -> None:
    """Release motor torque. Support the arm first."""
    from dreamscale.homing import run_release

    _ensure_so101()

    _run(run_release)


def _run_robot_command(fn, **kwargs):
    from dreamscale import errors
    from dreamscale.hardware.rig import RigFault

    try:
        _run(fn, **kwargs)
    except RigFault as exc:
        # The same problem/cause/fix shape as catalog errors, for every robot.
        typer.echo(errors.ErrorInfo(
            code="robot_fault",
            problem=str(exc),
            cause="the robot refused a command or could not confirm what it is doing",
            fix="keep the arm supported and the stop within reach, correct the reported "
            "item, then run the command again",
        ).render())
        raise typer.Exit(code=1) from exc
    except (RuntimeError, ValueError, OSError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


_run_yam_command = _run_robot_command


@yam_app.command("setup")
def robots_yam_setup(
    cli: bool = typer.Option(
        False,
        "--cli",
        help="Pick from numbered terminal prompts instead of LAN camera previews.",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
    host: str = typer.Option("0.0.0.0", "--host", help="Camera preview server host."),
    port: int = typer.Option(8765, "--port", min=1, max=65535, help="Camera preview server port."),
) -> None:
    """Install YAM support and assign cameras and CAN ports."""
    from dreamscale.extras import yam_extras
    from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH

    _ensure_extras(yam_extras(), label="YAM", setup_command="dreamscale robots yam setup")

    if cli:
        from dreamscale.hardware.yam_cli_setup import run_cli_setup

        _run_yam_command(run_cli_setup, config_path=config or DEFAULT_CONFIG_PATH)
    else:
        from dreamscale.hardware.yam_setup import run_setup

        _run_yam_command(run_setup, config_path=config or DEFAULT_CONFIG_PATH, host=host, port=port)


@yam_app.command("home")
def robots_yam_home(
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Move to the home pose, then release motor torque."""
    from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.yam_home import home_yam

    _ensure_extras(["yam"], label="YAM", setup_command="dreamscale robots yam setup")

    _run_yam_command(home_yam, config_path=config or DEFAULT_CONFIG_PATH)


@yam_app.command("release")
def robots_yam_release(
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Release motor torque. Support the arms first."""
    from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.yam_hold import release_yam

    _ensure_extras(["yam"], label="YAM", setup_command="dreamscale robots yam setup")

    _run_yam_command(release_yam, config_path=config or DEFAULT_CONFIG_PATH)


@franka_app.command("setup")
def robots_franka_setup(
    cli: bool = typer.Option(
        False, "--cli", help="Answer terminal prompts instead of using the setup page.",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
    host: str = typer.Option("0.0.0.0", "--host", help="Setup page server host."),
    port: int = typer.Option(8765, "--port", min=1, max=65535, help="Setup page server port."),
) -> None:
    """Install Franka support, choose its cameras and check the arm."""
    from dreamscale.embodiments import FRANKA
    from dreamscale.extras import franka_extras
    from dreamscale.hardware.franka_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.franka_setup import run_franka_page, run_franka_setup

    _experimental_notice(FRANKA)
    _ensure_extras(franka_extras(), label="Franka", setup_command="dreamscale robots franka setup")
    path = config or DEFAULT_CONFIG_PATH
    if cli:
        _run_robot_command(run_franka_setup, config_path=path)
    else:
        _run_robot_command(run_franka_page, config_path=path, host=host, port=port)


@ur_app.command("setup")
def robots_ur_setup(
    cli: bool = typer.Option(
        False, "--cli", help="Answer terminal prompts instead of using the setup page.",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
    host: str = typer.Option("0.0.0.0", "--host", help="Setup page server host."),
    port: int = typer.Option(8765, "--port", min=1, max=65535, help="Setup page server port."),
) -> None:
    """Install Universal Robots support, choose the arm, cameras and gripper, and check them."""
    from dreamscale.embodiments import UR
    from dreamscale.extras import ur_extras
    from dreamscale.hardware.ur_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.ur_setup import run_ur_page, run_ur_setup

    _experimental_notice(UR)
    _ensure_extras(
        ur_extras(), label="Universal Robots", setup_command="dreamscale robots ur setup"
    )
    path = config or DEFAULT_CONFIG_PATH
    if cli:
        _run_robot_command(run_ur_setup, config_path=path)
    else:
        _run_robot_command(run_ur_page, config_path=path, host=host, port=port)


@ur_app.command("home")
def robots_ur_home(
    set_pose: bool = typer.Option(
        False,
        "--set",
        help="Save where the arm is now as home (move it there with freedrive first).",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Move slowly to the home pose and open the gripper; the arm then holds."""
    from dreamscale.hardware.ur_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.ur_home import home_ur, set_home_ur

    _ensure_extras(["ur"], label="Universal Robots", setup_command="dreamscale robots ur setup")
    _run_robot_command(
        set_home_ur if set_pose else home_ur, config_path=config or DEFAULT_CONFIG_PATH
    )


@xarm7_app.command("setup")
def robots_xarm7_setup(
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Install xArm 7 support, choose each arm's address and gripper and the cameras, and check
    them."""
    from dreamscale.embodiments import XARM7
    from dreamscale.extras import xarm7_extras
    from dreamscale.hardware.xarm7_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.xarm7_setup import run_xarm7_setup

    _experimental_notice(XARM7)
    _ensure_extras(xarm7_extras(), label="xArm 7", setup_command="dreamscale robots xarm7 setup")
    _run_robot_command(run_xarm7_setup, config_path=config or DEFAULT_CONFIG_PATH)


@xarm7_app.command("home")
def robots_xarm7_home(
    set_pose: bool = typer.Option(
        False,
        "--set",
        help="Save where the arms are now as home (move them there in UFACTORY Studio first).",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Open the grippers and move both arms slowly to the home pose; the arms then hold."""
    from dreamscale.hardware.xarm7_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.xarm7_home import home_xarm7, set_home_xarm7

    _ensure_extras(["xarm7"], label="xArm 7", setup_command="dreamscale robots xarm7 setup")
    _run_robot_command(
        set_home_xarm7 if set_pose else home_xarm7, config_path=config or DEFAULT_CONFIG_PATH
    )


@openarm_app.command("setup")
def robots_openarm_setup(
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Say which arms and cameras your model was recorded with, on an Anvil Devbox."""
    from dreamscale.embodiments import OPENARM
    from dreamscale.hardware.openarm_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.openarm_setup import run_openarm_setup

    _experimental_notice(OPENARM)
    _run_robot_command(run_openarm_setup, config_path=config or DEFAULT_CONFIG_PATH)


@openarm_app.command("home")
def robots_openarm_home(
    set_pose: bool = typer.Option(
        False, "--set", help="Save where the arms are now as home.",
    ),
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Move the arms slowly to the home pose; they then hold."""
    from dreamscale.hardware.openarm_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.openarm_home import home_openarm, set_home_openarm

    _run_robot_command(
        set_home_openarm if set_pose else home_openarm, config_path=config or DEFAULT_CONFIG_PATH
    )


@franka_app.command("recover")
def robots_franka_recover(
    config: Annotated[Path | None, typer.Option("--config", help="Rig config path.")] = None,
) -> None:
    """Clear the arm's error after a reflex, once you have checked why it stopped."""
    from dreamscale.hardware.franka_config import DEFAULT_CONFIG_PATH
    from dreamscale.hardware.franka_runner import recover_franka

    _ensure_extras(["franka"], label="Franka", setup_command="dreamscale robots franka setup")
    _run_robot_command(recover_franka, config_path=config or DEFAULT_CONFIG_PATH)


@hud_app.command("setup")
def integrations_hud_setup(
    api_key: str | None = typer.Option(
        None,
        "--api-key",
        help="Save this HUD API key instead of prompting.",
        hide_input=True,
    ),
) -> None:
    """Install HUD support and save your HUD API key."""
    from dreamscale.integrations import hud as integration

    _ensure_extras(["hud"], label="HUD", setup_command=integration.SETUP_COMMAND)
    _run(integration.run_setup, api_key=api_key)


@hugging_face_app.command("setup")
def integrations_hugging_face_setup(
    token: str | None = typer.Option(
        None, "--token", help="Connect this read token instead of prompting.", hide_input=True,
    ),
) -> None:
    """Connect a read-only Hugging Face token to your Dreamscale account."""
    from dreamscale.integrations import hugging_face as integration

    _run(integration.run_setup, token=token)


@hugging_face_app.command("status")
def integrations_hugging_face_status() -> None:
    """Show the connected Hugging Face account and token."""
    from dreamscale.integrations import hugging_face as integration

    status: dict = {}
    _run(lambda: status.update(integration.run_status()))
    if status.get("failed_at"):
        raise typer.Exit(code=1)


@hugging_face_app.command("remove")
def integrations_hugging_face_remove(
    yes: bool = typer.Option(False, "--yes", "-y", help="Remove without asking."),
) -> None:
    """Disconnect Hugging Face: Dreamscale deletes the token."""
    from dreamscale.integrations import hugging_face as integration

    _run(integration.run_remove, yes=yes)


@inspect_robots_app.command("setup")
def integrations_inspect_robots_setup() -> None:
    """Install Inspect Robots support and check it works."""
    from dreamscale.integrations import inspect_robots as integration

    _ensure_extras(
        [integration.EXTRA], label="Inspect Robots", setup_command=integration.SETUP_COMMAND,
    )
    _run(integration.run_setup)


def _robot_run_command(embodiment):
    """`dreamscale run <robot>`: the shared options, with the robot's own joint units,
    defaults and (for a rig file) --config, all from its dreamscale.embodiments entry."""
    unit = embodiment.unit
    parameters = [
        ("ctx", typer.Context, inspect.Parameter.empty),
        ("instruction", str | None, _instruction_option()),
        ("model", str | None, typer.Option(
            None,
            "--model",
            callback=_model_name,
            help="Required: a model from `dreamscale models list`, or a deployment as "
            "<account>/<slug>."
            if embodiment.policy_models else
            f"Required: your deployment for {embodiment.label}, as <account>/<slug>.",
        )),
        ("mode", str, _mode_option()),
        ("engine", str | None, _engine_option()),
        *([("config", Annotated[Path | None, typer.Option("--config", help="Rig config path.")],
            None)] if embodiment.rig_config else []),
        ("max_actions", int | None, _max_actions_option()),
        ("keep_warm", int | None, _keep_warm_option()),
        ("region", str, _region_option()),
        ("region_fallback", bool | None, typer.Option(
            None, "--region-fallback/--no-region-fallback",
            help="Allow a shared-model session to start in the next supported region if "
            "its preferred region has no GPU. An explicit --region is strict by default.",
        )),
        ("provider", str | None, _provider_option()),
        ("speed", str, _speed_option()),
        ("rtc", str, _rtc_option()),
        ("checkpoint", str | None, _checkpoint_option()),
        ("context", str, _context_option()),
        ("effort", str | None, _effort_option()),
        ("max_cost", float | None, _max_cost_option()),
        ("max_joint_step", float | None, typer.Option(
            embodiment.max_joint_step,
            "--max-joint-step",
            min=0.000001,
            help=f"Max {unit} a command may lead the measured joint position.",
        )),
        ("max_joint_velocity", float | None, typer.Option(
            embodiment.max_joint_velocity,
            "--max-joint-velocity",
            min=0.000001,
            help=f"Joint speed cap in {unit} per second, homing included.",
        )),
        ("action_smoothing", str, _action_smoothing_option()),
        ("smoothing_new_weight", float | None, _smoothing_new_weight_option()),
        ("smoothing_correction_steps", int | None, _smoothing_correction_steps_option()),
        ("smoothing_reference_speed", float | None, _smoothing_reference_speed_option()),
        ("trace_dir", Annotated[Path | None, _trace_dir_option()], None),
        ("trace_images", bool, _trace_images_option()),
        ("hud", bool, _hud_options()[0]),
        ("hud_job", str | None, _hud_options()[1]),
        ("inspect_robots", bool, typer.Option(
            False,
            "--inspect-robots",
            hidden=_LAUNCH_HIDDEN,
            help="Record an Inspect Robots eval log, graded after each task.",
        )),
        ("task", str | None, typer.Option(
            None, "--task", hidden=_LAUNCH_HIDDEN,
            help="Inspect Robots task (needs --inspect-robots).",
        )),
        ("epochs", int | None, typer.Option(
            None, "--epochs", min=1, hidden=_LAUNCH_HIDDEN,
            help="Trials per scene (needs --inspect-robots).",
        )),
        ("log_dir", Annotated[Path | None, typer.Option(
            "--log-dir", hidden=_LAUNCH_HIDDEN,
            help="Eval log directory (needs --inspect-robots; default ./logs).",
        )], None),
        ("verbose", bool, _verbose_option()),
        ("steady_send", bool, _steady_send_options()[0]),
        ("steady_send_ms", str | None, _steady_send_options()[1]),
    ]

    def command(**options) -> None:
        _run_robot(embodiment, **options)

    command.__signature__ = inspect.Signature([
        inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=default,
                          annotation=annotation)
        for name, annotation, default in parameters
    ])
    command.__annotations__ = {name: annotation for name, annotation, _ in parameters}
    command.__name__ = f"run_{embodiment.name}_command"
    command.__doc__ = f"Run tasks on {embodiment.display_label}."
    return command


def _model_or_deployment(model, checkpoint):
    """`--model <account>/<slug>` (or a bare slug of yours) runs that deployment, as
    `--deployment` does: ``(model, deployment)``."""
    from dreamscale.checkpoints_cmd import is_own_deployment
    from dreamscale.model_names import is_account_ref

    if model is None:
        return model, checkpoint
    if is_account_ref(model):
        if checkpoint is not None and checkpoint != model:
            raise typer.BadParameter(
                f"{model} is a deployment; pass it as --model or --deployment, not both"
            )
        return None, model
    if checkpoint is None and is_own_deployment(model):
        return None, model
    return model, checkpoint


def _deployment_model(embodiment, model, checkpoint):
    """`--deployment ckpt_…`: the model its base runs it as on this robot (a π0.5 deployment
    built for this robot runs as pi0.5). A --model other than the default base's runs as
    given."""
    from dreamscale import errors
    from dreamscale.checkpoints_cmd import deployment_model_for_robot
    from dreamscale.policy.deployment import is_default_base

    if checkpoint in (None, "base") or (model is not None and not is_default_base(model)):
        return model
    try:
        return deployment_model_for_robot(embodiment, checkpoint, model)
    except errors.DreamscaleError as error:
        typer.echo(error.render())
        raise typer.Exit(code=1) from error


def _experimental_notice(embodiment) -> None:
    notice = embodiment.experimental_notice()
    if notice is not None:
        typer.secho(notice, err=True, fg="yellow")


def _run_robot(embodiment, *, ctx, model, instruction, effort, max_cost, config=None,
               **options) -> None:
    from dreamscale.model_names import resolve_llm_model

    region_fallback = options.pop("region_fallback", None)
    engine = options.pop("engine", None)
    session_options = {
        **({"region_fallback": region_fallback} if region_fallback is not None else {}),
        **({"engine": engine} if engine is not None else {}),
    }
    connect_options = {}
    if session_options:
        from dreamscale.policy.remote import aconnect

        async def session_connect(*args, **kwargs):
            return await aconnect(*args, **session_options, **kwargs)

        connect_options["connect"] = session_connect
    model, options["checkpoint"] = _model_or_deployment(model, options.get("checkpoint"))
    model = _deployment_model(embodiment, model, options.get("checkpoint"))
    if model is None:
        from dreamscale import errors

        hint = (errors.SEE_MODELS if embodiment.policy_models
                else "See your deployments: dreamscale deployments list")
        raise click.MissingParameter(
            f"Choose what {embodiment.label} runs. {hint}",
            param_hint="'--model'",
            param_type="option",
        )
    model = resolve_llm_model(model)
    _experimental_notice(embodiment)
    inspect_robots, task, epochs, log_dir = (
        options.pop(key) for key in ("inspect_robots", "task", "epochs", "log_dir")
    )
    steady_send = _steady_send(options.pop("steady_send"), options.pop("steady_send_ms"))
    if not inspect_robots and (task is not None or epochs is not None or log_dir is not None):
        raise typer.BadParameter("--task, --epochs and --log-dir need --inspect-robots.")
    hud, hud_job = options["hud"], options["hud_job"]
    _check_hud_options(hud, hud_job)
    if inspect_robots and _is_llm(model):
        raise typer.BadParameter("--inspect-robots records cloud policies, not LLM models.")
    if inspect_robots and hud:
        raise typer.BadParameter("--inspect-robots and --hud each record the run; choose one.")
    extras = list(embodiment.load(embodiment.extras)())
    rig = {"config_path": config} if embodiment.rig_config else {}
    if _is_llm(model):
        if embodiment.run_llm is None:
            raise typer.BadParameter(f"LLM models don't drive {embodiment.label} yet.")
        _reject_policy_options(ctx)
        _ensure_extras(extras, label=embodiment.label, setup_command=embodiment.setup_command)
        from dreamscale.attended.output import ProgressPrinter

        # The same terminal as a policy run: milestones shown, details in the log.
        print_fn = ProgressPrinter(verbose=options["verbose"], robot=embodiment.name)
        try:
            _run_robot_command(
                embodiment.load(embodiment.run_llm),
                model=model,
                instruction=instruction,
                **rig,
                effort=effort or "medium",
                speed=options["speed"],
                max_cost=max_cost,
                max_joint_step=options["max_joint_step"],
                max_joint_velocity=options["max_joint_velocity"],
                print_fn=print_fn,
            )
        finally:
            print_fn.close()
        return
    if effort is not None or max_cost is not None:
        raise typer.BadParameter("--effort and --max-cost apply only to LLM models.")
    _ensure_extras(
        [
            *extras, *(["trace"] if options["trace_dir"] else []), *(["hud"] if hud else []),
            *(["inspect-robots"] if inspect_robots else []),
        ],
        label=embodiment.label + (" and HUD" if hud else "")
        + (" and Inspect Robots" if inspect_robots else ""),
        setup_command=embodiment.setup_command,
    )
    if hud:
        _ensure_hud_setup()
    options["keep_warm"] = _keep_warm(model, options["keep_warm"], options["checkpoint"])
    from dreamscale.attended.output import ProgressPrinter

    verbose = options.pop("verbose")
    print_fn = ProgressPrinter(verbose=verbose, robot=embodiment.name)
    recorder = None
    try:
        if inspect_robots:
            instruction, recorder = _inspect_robots_recorder(
                embodiment, model=model, instruction=instruction, task=task, epochs=epochs,
                log_dir=log_dir, options=options, print_fn=print_fn,
            )
        _run_robot_command(
            embodiment.load(embodiment.run_policy),
            **connect_options,
            model=model,
            instruction=instruction,
            **({"config_path": config} if config is not None else {}),
            **options,
            **({"recorder": recorder} if recorder is not None else {}),
            **({"steady_send": steady_send} if steady_send is not None else {}),
            print_fn=print_fn,
        )
    finally:
        print_fn.close()


def _inspect_robots_recorder(embodiment, *, model, instruction, task, epochs, log_dir, options,
                             print_fn):
    """The tasks to run and the Inspect Robots eval log that records them."""
    from dreamscale.integrations.inspect_robots import plan_tasks
    from dreamscale.integrations.inspect_robots_recorder import InspectRobotsJob
    from dreamscale.policy.runtime.contract import runtime_contract_for_model

    try:
        plan = plan_tasks(
            instruction=instruction, task=task, epochs=epochs,
            max_actions=options["max_actions"],
            action_hz=runtime_contract_for_model(model).action_hz,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    options["max_actions"] = plan.max_actions
    job = InspectRobotsJob(
        model=model, embodiment=embodiment, log_dir=log_dir or "logs", task=plan.task,
        scenes=plan.scenes, max_steps=plan.max_actions, print_fn=print_fn,
    )
    job.announce()
    return plan.instructions, job


def _register_robot_commands() -> None:
    from dreamscale.embodiments import EMBODIMENTS

    for name, embodiment in EMBODIMENTS.items():
        run_app.command(name, cls=SteadySendCommand, hidden=embodiment.hidden)(
            _robot_run_command(embodiment)
        )


_register_robot_commands()


if __name__ == "__main__":
    app()
