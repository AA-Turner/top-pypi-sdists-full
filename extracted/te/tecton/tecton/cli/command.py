import copy
import functools
import sys
import typing as t
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import List
from typing import Optional

import rich_click as click
from click import Command
from click import Context
from click import echo
from click import style
from rich_click import RichGroup

import tecton_core.tecton_pendulum as pendulum
from tecton import tecton_context
from tecton._internals.analytics import AnalyticsLogger
from tecton._internals.analytics import StateUpdateEventMetrics
from tecton._internals.analytics import StateUpdateResult
from tecton._internals.utils import cluster_url
from tecton.cli import printer
from tecton.cli import workspace_utils
from tecton_core import conf


analytics = AnalyticsLogger()


class TectonCommandCategory(Enum):
    WORKSPACE = "Workspace"
    IDENTITY = "Identity & Access"
    INFRA = "Infrastructure"
    OTHER = "Other"


class TectonCommand(click.Command):
    # used by integration tests
    skip_config_check = False

    """Base class for Click which implements required_auth and uses_workspace behavior, as well as analytics."""

    def __init__(
        self,
        *args,
        callback,
        requires_auth=True,
        uses_workspace=False,
        command_category=TectonCommandCategory.OTHER,
        deprecation_warning="",
        **kwargs,
    ):
        self.command_category = command_category
        self.deprecation_warning = deprecation_warning

        @functools.wraps(callback)
        @click.pass_context
        def wrapper(ctx, *cbargs, **cbkwargs):
            host = cluster_url()
            cluster_configured = host is not None

            command_names = []
            cur = ctx
            # The top level context is `cli` which we don't want to include.
            while cur:
                command_names.append(cur.command.name)
                cur = cur.parent
            command_names.reverse()

            # TODO(TEC-14547): Move `workspace` param usages to callback function.
            is_create_workspace_command = ctx.parent.info_name == "workspace" and ctx.info_name == "create"
            has_workspace_option = ctx.params.get("workspace", None) is not None
            if has_workspace_option and not is_create_workspace_command:
                workspace_name = ctx.params["workspace"]
                workspace_utils.check_workspace_exists(workspace_name)
                conf.set("TECTON_WORKSPACE", workspace_name)

            # Do not try logging events if cluster has never be configured or if user is trying to log in,
            # otherwise the CLI either won't be able to find the MDS or auth token might have expired
            if cluster_configured:
                if uses_workspace:
                    printer.safe_print(f'Using workspace "{tecton_context.get_current_workspace()}" on cluster {host}')
                start_time = pendulum.now("UTC")
                state_update_event = None
                try:
                    invoke_result = ctx.invoke(callback, *cbargs, **cbkwargs)
                    if isinstance(invoke_result, StateUpdateResult):
                        state_update_event = invoke_result.state_update_event_metrics
                except PermissionError as e:
                    state_update_event = StateUpdateEventMetrics.from_error_message(str(e))
                    printer.safe_print(f"Unable to execute command `{' '.join(command_names)}`: {str(e)}")
                execution_time = pendulum.now("UTC") - start_time
                if requires_auth:
                    if state_update_event:
                        # TODO: Include sub-command?
                        analytics.log_cli_event(command_names[1], execution_time, ctx.params, state_update_event)
                        if state_update_event.error_message:
                            sys.exit(1)
                    else:
                        analytics.log_cli_event(command_names[1], execution_time, ctx.params)
            elif not requires_auth or TectonCommand.skip_config_check:
                # Do not try executing anything besides unauthenticated commnds (`login`, `version`) when cluster hasn't been configured.
                state_update_event = ctx.invoke(callback, *cbargs, **cbkwargs)
            else:
                printer.safe_print(
                    f"`{' '.join(command_names)}` requires authentication. Please authenticate using `tecton login`."
                )
                sys.exit(1)

        super().__init__(*args, callback=wrapper, **kwargs)

    def invoke(self, ctx: Context) -> t.Any:
        """Given a context, this invokes the attached callback (if it exists)
        in the right way.

        Over-writes the base method for a better depredation warning
        """
        if self.deprecated:
            if self.deprecation_warning:
                message = "DeprecationWarning:" + self.deprecation_warning
            else:
                message = f"DeprecationWarning: The command {self.name} is deprecated."
            echo(style(message, fg="red"), err=True)

        if self.callback is not None:
            return ctx.invoke(self.callback, **ctx.params)


class TectonGroup(RichGroup):
    """Routes group.command calls to use TectonCommand instead of the base Click command"""

    def __init__(self, command_category=TectonCommandCategory.OTHER, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_category = command_category

    command_class = TectonCommand

    def _register_command_in_group(self, command_name: str, category_name: str) -> None:
        """Register a command in the appropriate command group for rich CLI display.

        Args:
            command_name: The name of the command to register
            category_name: The category name to group the command under
        """
        if "tecton" not in click.rich_click.COMMAND_GROUPS:
            click.rich_click.COMMAND_GROUPS["tecton"] = [
                {"name": category.value, "commands": []} for category in TectonCommandCategory
            ]

        category_exists = any(group["name"] == category_name for group in click.rich_click.COMMAND_GROUPS["tecton"])
        if category_exists:
            for group in click.rich_click.COMMAND_GROUPS["tecton"]:
                if group["name"] == category_name:
                    if command_name not in group["commands"]:
                        group["commands"].append(command_name)

    def add_command(self, cmd: Command, name: Optional[str] = None) -> None:
        self._register_command_in_group(cmd.name, cmd.command_category.value)
        super().add_command(cmd, name)

    def add_deprecated_command(self, cmd: Command, name: str, new_target: t.Optional[str] = None) -> None:
        deprecation_warning = f" The command `{self.name} {name}` is deprecated and will removed in a future version."
        if new_target:
            deprecation_warning += f" Use `{new_target}` instead."
        cmd = copy.copy(cmd)
        cmd.hidden = True
        cmd.deprecated = True
        cmd.deprecation_warning = deprecation_warning
        cmd.help = deprecation_warning + "\n\n" + cmd.help
        super().add_command(cmd, name)


TectonGroup.group_class = TectonGroup


@dataclass
class HiddenValue:
    """Wraps a string and displays it as ****. Used to hide passwords when showing the previous value in prompts."""

    value: str

    def __str__(self):
        return "*" * len(self.value)


class HiddenValueType(click.ParamType):
    name = "TEXT"  # Controls how this is displayed in help text

    def convert(self, value, param=None, ctx=None):
        if value is None:
            return None
        if isinstance(value, HiddenValue):
            return value
        return HiddenValue(value)


def tecton_config_option(
    key: str, param_decls: Optional[List[str]] = None, hide_input: bool = False, **kwargs
) -> Callable:
    """Decorator for a Click option which defaults to a value from tecton_core.conf and prompts if the key is not set.

    :arg key The tecton_core.conf key.
    :arg param_decls The Click param_decls.
    :arg hide_input Whether to hide user input in the prompt, as for passwords. Additionally, if a default is set,
         it will be obfuscated with `*` in the prompt.
    """
    if "prompt" not in kwargs:
        kwargs["prompt"] = True
    lower_key = key.lower().replace("_", "-")
    param_decls = param_decls or [f"--{lower_key}"]

    if hide_input:
        kwargs["type"] = HiddenValueType()
        default = HiddenValueType().convert(conf.get_or_none(key))
    else:

        def default():
            return conf.get_or_none(key)

    def decorator(f):
        @click.option(*param_decls, **kwargs, hide_input=hide_input, default=default)
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            def unwrap(v):
                return v.value if isinstance(v, HiddenValue) else v

            return f(**{k: unwrap(v) for k, v in kwargs.items()})

        return wrapper

    return decorator
