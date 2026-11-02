"""Typed authored execution through the ordinary SDK publication and Run boundaries."""

import asyncio
import inspect
import sys
from contextlib import redirect_stdout
from functools import partial
from pathlib import Path
from typing import ClassVar, get_origin

import click
from click.core import ParameterSource

from labqoat.cli.commands.authored.authored_target import AuthoredTarget
from labqoat.cli.commands.authored.budget_advice import BudgetAdvice
from labqoat.cli.commands.authored.launch_advice import LaunchAdvice
from labqoat.cli.commands.authored.launch_output import LaunchOutput
from labqoat.cli.commands.authored.launch_session import LaunchSession
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_banner import RunBanner
from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.commands.authored.run_group import RunGroup
from labqoat.cli.commands.authored.run_observer import RunObserver
from labqoat.cli.commands.authored.target_signature import TargetSignature
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.project_checks import ProjectChecks
from labqoat.cli.strict_command import StrictCommand
from labqoat.client import Client
from labqoat.compute.function import Function
from labqoat.compute.local_entrypoint import LocalEntrypoint
from labqoat.compute.value_codec import ValueCodec
from labqoat.runs.run_handle import RunHandle
from labqoat.cli.mutation_key import MutationKey
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.output.cli_failure import CliFailure


class LaunchCommand(StrictCommand):
    """Invoke local entrypoints or durable remote functions with one foreground default."""

    def __init__(self, target: AuthoredTarget) -> None:
        """Capture flags before any credential lookup, upload, or remote mutation."""
        self.target = target
        self.signature = TargetSignature(target)
        declared = self.signature.options()
        taken = {name for parameter in declared for name in parameter.opts}
        self.trailing = [
            option
            for option in RunGroup.launch_options()
            if isinstance(option, click.Option) and not taken & set(option.opts)
        ]
        for option in self.trailing:
            option.hidden = True
        super().__init__(
            target.name,
            params=[*declared, *self.trailing],
            help=inspect.getdoc(target.function),
            context_settings={"help_option_names": ["-h", "--help"]},
        )

    TRUE: ClassVar[frozenset[str]] = frozenset({"true", "1", "yes", "on"})
    FALSE: ClassVar[frozenset[str]] = frozenset({"false", "0", "no", "off"})

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Accept `--flag true|false` and `--flag=false` for a boolean parameter as its on or off switch."""
        switches = {
            name: option.secondary_opts[0]
            for option in self.params
            if isinstance(option, click.Option) and option.is_flag and option.secondary_opts
            for name in option.opts
        }
        return super().parse_args(ctx, self.switched(args, switches))

    @classmethod
    def switched(cls, args: list[str], switches: dict[str, str]) -> list[str]:
        """Rewrite explicit boolean values into the flag's own on and off spellings; leave anything else to Click."""
        values = cls.TRUE | cls.FALSE
        rewritten: list[str] = []
        index = 0
        while index < len(args):
            name, equals, value = args[index].partition("=")
            if name in switches and not equals and index + 1 < len(args) and args[index + 1].lower() in values:
                index, equals, value = index + 1, "=", args[index + 1]
            known = name in switches and equals and value.lower() in values
            rewritten.append((switches[name] if value.lower() in cls.FALSE else name) if known else args[index])
            index += 1
        return rewritten

    def invoke(self, ctx: click.Context) -> object:
        """Own the Client and detach only durably accepted work, never a host-side process."""
        self._hoist(ctx)
        options = ctx.parent.params if ctx.parent is not None else {}
        detached = bool(options.get("detach"))
        self._validate(options, detached)
        self._arguments(ctx.params)
        ProjectChecks.enforce(Path(inspect.getfile(self.target.function)), ProcessRunner(timeout_seconds=600.0))
        LaunchAdvice.announce(sys.modules.get(self.target.function.__module__))
        context = ContextAccessor.current()
        client = context.client()
        reading = BudgetAdvice.announce(client, context.project_name())
        try:
            value = self._execute(client, ctx.params, options)
            self._render(value, detached)
        except KeyboardInterrupt as error:
            raise CliFailure("Disconnected. Accepted Runs continue; use their IDs to reconnect.", 130) from error
        finally:
            BudgetAdvice.finish(reading)
            client.close()
        return None

    def _hoist(self, ctx: click.Context) -> None:
        """Launch options written after the target count as if written before it, unless a parameter owns the name."""
        for option in self.trailing:
            name = str(option.name)
            value = ctx.params.pop(name, None)
            if ctx.parent is not None and ctx.get_parameter_source(name) is ParameterSource.COMMANDLINE:
                ctx.parent.params[name] = value

    def _arguments(self, arguments: dict[str, object]) -> None:
        """Validate portable remote argument schemas before uploads or credential resolution."""
        if not isinstance(self.target.declaration, Function):
            return
        try:
            for name, value in arguments.items():
                if self.signature.reference(name) is None:
                    ValueCodec(self.signature.annotations[name]).encode(value)
        except (TypeError, ValueError) as error:
            raise click.UsageError(str(error)) from error

    def _validate(self, options: dict[str, object], detached: bool) -> None:
        """Reject platform flags that cannot control an arbitrary local function."""
        if detached and options.get("wait_timeout") is not None:
            raise click.UsageError("--wait-timeout cannot be combined with --detach.")
        if isinstance(self.target.declaration, Function):
            return
        if options.get("seed") or options.get("key"):
            raise click.UsageError(
                "--seed and --key apply to remote functions; local entrypoints own their submissions."
            )
        if (detached or options.get("wait_timeout") is not None) and get_origin(
            self.signature.annotations["return"]
        ) is not RunHandle:
            raise click.UsageError(
                "--detach and --wait-timeout require a remote function or a local entrypoint returning RunHandle."
            )

    def _execute(self, client: Client, arguments: dict[str, object], options: dict[str, object]) -> object:
        """Inject explicit authority and preserve authored stdout as diagnostics."""
        declaration = self.target.declaration
        with redirect_stdout(sys.stderr):
            arguments = self.signature.resolve(client, arguments)
            if isinstance(declaration, Function):
                key = MutationKey.resolve(options.get("key"))
                runs = client.runs.with_options(key=key, seed=int(str(options.get("seed", 0))))
                return runs.submit(declaration, **arguments)
            return self._local(declaration, client, arguments)

    def _title(self, handle: RunHandle[object]) -> str:
        """A submitted function is known by its app and name; an entrypoint's run is asked for its own."""
        declaration = self.target.declaration
        if isinstance(declaration, Function):
            return f"{declaration.app_name}/{declaration.local.__name__}"
        if not OutputStyle.interactive(sys.stderr):
            return ""
        return str(handle.client.get(handle.id).name or "")

    def _local(self, declaration: LocalEntrypoint[..., object], client: Client, arguments: dict[str, object]) -> object:
        """A launcher that returns one run is followed by that run; any other is followed as a group."""
        if get_origin(self.signature.annotations["return"]) is RunHandle:
            return self._settled(declaration(client, **arguments))
        context = click.get_current_context(silent=True)
        values = context.parent.params if context is not None and context.parent is not None else {}
        owner = declaration.app_name or Path(declaration.local.__code__.co_filename).stem
        session = LaunchSession(client, f"{owner}/{self.target.name}", ConsoleOptions.current(values))
        return session.run(partial(self._launch, declaration, arguments))

    def _launch(
        self, declaration: LocalEntrypoint[..., object], arguments: dict[str, object], client: Client
    ) -> object:
        """Call the launcher with the client its session scoped to the group."""
        return self._settled(declaration(client, **arguments))

    @staticmethod
    def _settled(value: object) -> object:
        """Drive an asynchronous launcher to its result."""
        return asyncio.run(value) if inspect.iscoroutine(value) else value

    def _render(self, value: object, detached: bool) -> None:
        """Treat returned handles as durable work and ordinary values as completed local results."""
        if detached and not isinstance(value, RunHandle):
            raise click.ClickException("The entrypoint did not return the declared durable RunHandle.")
        if isinstance(value, RunHandle):
            link = f"{ContextAccessor.current().profile.base_url.rstrip('/')}/runs/{value.id}"
            for line in RunBanner.lines(OutputStyle.current(sys.stderr), value.id, self._title(value), link):
                click.echo(line, err=True)
            if detached:
                LaunchOutput.accepted(value)
            else:
                with ObservationDeadline.current(value.id).watching():
                    LaunchOutput.value(RunObserver.result(value), value.result_type, value)
        else:
            LaunchOutput.value(value, self.signature.annotations["return"])
