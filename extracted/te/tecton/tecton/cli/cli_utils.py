import functools
import os
import re
import sys
from datetime import datetime
from datetime import timezone
from difflib import unified_diff
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import click
from attr import asdict
from colorama import Fore
from colorama import Style
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton_core.errors import FailedPreconditionError
from tecton_core.errors import TectonAbortedError
from tecton_core.errors import TectonAlreadyExistsError
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonDeadlineExceededError
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonNotFoundError
from tecton_core.errors import TectonNotImplementedError
from tecton_core.errors import TectonOperationCancelledError
from tecton_core.errors import TectonResourceExhaustedError


_CLIENT_VERSION_INFO_RESPONSE_HEADER = "x-tecton-client-version-info"
_CLIENT_VERSION_WARNING_RESPONSE_HEADER = "x-tecton-client-version-warning"
_INDENTATION_SIZE = 4


def cli_indent(indentation_level=1):
    return " " * (indentation_level * _INDENTATION_SIZE)


def timestamp_to_string(value: timestamp_pb2.Timestamp) -> str:
    t = datetime.fromtimestamp(value.ToSeconds())
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def human_fco_type(fco_type: str, plural=False) -> str:
    name_map = {
        "virtual_data_source": ("DataSource", "DataSources"),
        "batch_data_source": ("BatchDataSource", "BatchDataSources"),
        "stream_data_source": ("StreamDataSource", "StreamDataSources"),
        "entity": ("Entity", "Entities"),
        "transformation": ("Transformation", "Transformations"),
        "feature_table": ("FeatureTable", "FeatureTables"),
        "feature_view": ("FeatureView", "FeatureViews"),
        "batch_feature_view": ("BatchFeatureView", "BatchFeatureViews"),
        "on_demand_feature_view": ("OnDemandFeatureView", "OnDemandFeatureViews"),
        "stream_feature_view": ("StreamFeatureView", "StreamFeatureViews"),
        "batch_window_aggregate_feature_view": ("BatchWindowAggregateFeatureView", "BatchWindowAggregateFeatureViews"),
        "stream_window_aggregate_feature_view": (
            "StreamWindowAggregateFeatureView",
            "StreamWindowAggregateFeatureViews",
        ),
        "feature_service": ("FeatureService", "FeatureServices"),
    }
    if plural:
        return name_map[fco_type][1]
    else:
        return name_map[fco_type][0]


def bold(x):
    return Style.BRIGHT + x + Style.NORMAL


def ask_user(message: str, options: List[str], default=None, let_fail=False) -> Optional[str]:
    options_idx = {o.lower(): i for i, o in enumerate(options)}

    while True:
        if len(options) > 1:
            printer.safe_print(message, "[" + "/".join(options) + "]", end="> ")
        else:
            printer.safe_print(message, end="> ")

        try:
            user_input = input().strip().lower()
        except EOFError:
            return None

        if user_input == "" and default:
            return default

        if user_input in options_idx:
            return options[options_idx[user_input]]
        else:
            # If there is only one input option, typing "!" will select it.
            if user_input == "!" and len(options) == 1:
                return options[0]
            elif let_fail:
                return None


def confirm_or_exit(message, expect=None):
    try:
        if expect:
            if ask_user(message, options=[expect], let_fail=True) is not None:
                return
            else:
                printer.safe_print("Aborting")
                sys.exit(1)
        else:
            if ask_user(message, options=["y", "N"], default="N") == "y":
                return
            else:
                printer.safe_print("Aborting")
                sys.exit(1)
    except KeyboardInterrupt:
        printer.safe_print("Aborting")
        sys.exit(1)


def color_line(x):
    if x.startswith("+"):
        return Fore.GREEN + x + Fore.RESET
    elif x.startswith("-"):
        return Fore.RED + x + Fore.RESET
    return x


def color_diff(lines):
    return map(color_line, lines)


def indent_line(lines, indent):
    return (" " * indent + x for x in lines)


# TODO: Reuse this in other places that does the same (engine.py)
def pprint_dict(kv, colwidth, indent=0):
    for k, v in kv.items():
        printer.safe_print(indent * " " + f"{k.ljust(colwidth)} {v}")


def pprint_attr_obj(key_map, obj, colwidth):
    o = asdict(obj)
    pprint_dict({key_map[key]: o[key] for key in o}, colwidth)


def code_diff(diff_item, indent):
    return re.split(
        "\n",
        "".join(
            indent_line(
                color_diff(
                    unified_diff(
                        diff_item.val_existing.splitlines(keepends=True),
                        diff_item.val_declared.splitlines(keepends=True),
                    )
                ),
                indent,
            )
        ),
        3,
    )[-1]


def print_version_msg(message, is_warning=False):
    if isinstance(message, list):
        message = message[-1] if len(message) > 0 else ""
    color = Fore.YELLOW
    if is_warning:
        message = "⚠️  " + message
    printer.safe_print(color + message + Fore.RESET, file=sys.stderr)


def display_principal(principal, default="", width=0):
    principal_type = principal.WhichOneof("basic_info")

    if principal_type == "user":
        return f"{principal.user.login_email : <{width}}(User Email)"
    if principal_type == "service_account":
        identifier = (
            f"{principal.service_account.name  : <{width}}(Service Account Name)"
            if principal.service_account.name
            else f"{principal.service_account.id  : <{width}}(" f"Service Account Id)"
        )
        return identifier
    return default


def display_table(headings: List[str], display_rows: List[Tuple]):
    table = Displayable.from_table(headings=headings, rows=display_rows, max_width=0, center_align=True)
    printer.safe_print(table)


def plural(x, singular, plural):
    if x == 1:
        return singular
    else:
        return plural


def no_color_convention() -> bool:
    """Follow convention for ANSI coloring of CLI tools. See no-color.org."""
    for key, value in os.environ.items():
        if key == "NO_COLOR" and value != "":
            return True
    return False


def py_path_to_module(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root))[: -len(".py")].replace("./", "").replace("/", ".").replace("\\", ".")


def check_version():
    try:
        response = metadata_service.instance().Nop(request=empty_pb2.Empty())
        client_version_msg_info = response._headers().get(_CLIENT_VERSION_INFO_RESPONSE_HEADER)
        client_version_msg_warning = response._headers().get(_CLIENT_VERSION_WARNING_RESPONSE_HEADER)

        # Currently, only _CLIENT_VERSION_INFO_RESPONSE_HEADER and _CLIENT_VERSION_WARNING_RESPONSE_HEADER
        # metadata is used in the response, whose values have str type.
        # The returned types have 3 cases as of PR #3696:
        # - Metadata value type is List[str] if it's returned from go proxy if direct http is used.
        # - Metadata value is first str in List[str] returned from go proxy if grpc gateway is used.
        # - Metadata value type is str if direct grpc is used.
        # The default values of keys that don't exist are empty strings in any of the 3 cases.
        if client_version_msg_info:
            print_version_msg(client_version_msg_info)
        if client_version_msg_warning:
            print_version_msg(client_version_msg_warning, is_warning=True)
    except Exception as e:
        printer.safe_print("Error connecting to tecton server: ", e, file=sys.stderr)
        sys.exit(1)


def click_exception_wrapper(func):
    """
    Decorator for click commands so that non-Click exceptions are re-raised as ClickExceptions,
    which are displayed gracefully and suppress a stack trace by the click library.

    NOTE: This decorator should be included after Click decorators to ensure exceptions are
    raised as ClickExceptions.

    Example:
    -------
    @click.command()
    @click_exception_wrapper
    def my_command():
        pass

    :param func: function that this decorator wraps
    :return: wrapped function that handles exceptions gracefully
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            TectonAPIInaccessibleError,
            TectonAPIValidationError,
            FailedPreconditionError,
            TectonNotFoundError,
            TectonNotImplementedError,
            TectonInternalError,
            TectonOperationCancelledError,
            TectonDeadlineExceededError,
            TectonResourceExhaustedError,
            TectonAbortedError,
            TectonAlreadyExistsError,
            PermissionError,
        ) as e:
            raise click.ClickException(e)

    return wrapper
