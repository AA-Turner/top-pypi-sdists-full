import contextlib
from contextlib import contextmanager
import os
import sys
import time
from typing import List, Optional

from botocore.exceptions import ClientError
import click
import colorama

from anyscale.anyscale_halo import Halo
from anyscale.client.openapi_client.models import (
    CloudAnalyticsEventCloudProviderError,
    CloudAnalyticsEventCloudResource,
)
from anyscale.utils.imports.gcp import try_import_gcp_exceptions


_process_start_time = time.time()


def bold(text: str, color: Optional[int] = None) -> str:
    """Outputs the text into ANSI-supported bolded text.

    `colorama.Style.BRIGHT` corresponds to bold"""
    return f"{colorama.Style.BRIGHT}{color if color else ''}{text}{colorama.Style.RESET_ALL}"


# 2 is used for consistency across other indenting / padding in CLI
INDENT = " " * 2


def pad_string(text: str, padding: int = 10) -> str:
    """Pads the remainder of text with spaces (`spaces == padding - len(text)`)

    NOTE: `padding` should be longer than `len(text)` for this to be useful"""
    return f"{text: <{padding}}"


class BlockLogger:
    """
    Logger class for the CLI. Supports formatting in blocks if `block_label` is provided to
    the methods. Also supports anyscale.connect style logging if `block_label` is not
    provided.
    """

    def __init__(
        self,
        log_output: bool = True,
        t0: float = _process_start_time,
        spinner_manager: Optional[Halo] = None,
    ) -> None:
        self.t0 = t0
        # Flag to disable all terminal output from CLILogger (useful for SDK)
        self.log_output = log_output
        self.current_block: Optional[str] = None
        self.spinner_manager = spinner_manager
        self.indent_level: int = 0

    def open_block(
        self, block_label: str, block_title: Optional[str] = None, auto_close=False
    ) -> None:
        """
        Prints block title from the given block_label and sets self.current_block. "Output"
        is a generic block that does not need to follow the standard convention.

        if auto_close is set, automatically closes the block before opening a new one
        """
        if not self.log_output:
            return
        assert (
            auto_close or self.current_block is None or self.current_block == "Output"
        ), f"Block {self.current_block} is already open. Please close before opening block {block_label}."

        if auto_close:
            self.close_block()
        self.current_block = block_label
        print(
            f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}{block_title if block_title else block_label}{colorama.Style.RESET_ALL}",
            file=sys.stderr,
        )

    def close_block(self, block_label: Optional[str] = None) -> None:
        """ Closes the current block
        If a label is specified, it must match the current open block label.
        raise an AssertionError if we try to close a different block

        Prints newline so there is separation before next block is opened.
        """
        if not self.log_output:
            return
        if block_label:
            assert (
                self.current_block == block_label
            ), f"Attempting to close block {block_label}, but block {self.current_block} is currently open."
        self.current_block = None
        print(file=sys.stderr)

    @staticmethod
    def highlight(text: str) -> str:
        return bold(text, colorama.Fore.MAGENTA)

    def zero_time(self) -> None:
        self.t0 = time.time()

    def info(
        self, *msg: str, block_label: Optional[str] = None, end: str = "\n"
    ) -> None:
        if not self.log_output:
            return
        if block_label:
            # Check block_label if provided.
            assert (
                self.current_block == block_label
            ), f"Attempting to log to block {block_label}, but block {self.current_block} is currently open."
            print(INDENT * self.indent_level, end="", file=sys.stderr)
            print(
                *msg, file=sys.stderr,
            )
        else:
            print(
                "{}{}(anyscale +{}){} ".format(
                    colorama.Style.BRIGHT,
                    colorama.Fore.CYAN,
                    self._time_string(),
                    colorama.Style.RESET_ALL,
                ),
                end="",
                file=sys.stderr,
            )
            print(INDENT * self.indent_level, end="", file=sys.stderr)
            print(
                *msg, file=sys.stderr, end=end,
            )

    def debug(self, *msg: str) -> None:
        if not self.log_output:
            return
        if os.environ.get("ANYSCALE_DEBUG") == "1":
            print(
                "{}{}(anyscale +{}){} ".format(
                    colorama.Style.DIM,
                    colorama.Fore.CYAN,
                    self._time_string(),
                    colorama.Style.RESET_ALL,
                ),
                end="",
            )
            print(INDENT * self.indent_level, end="", file=sys.stderr)
            print(*msg)

    def warning(self, *msg: str) -> None:
        if not self.log_output:
            return
        print(
            "{}{}[Warning]{} ".format(
                colorama.Style.NORMAL, colorama.Fore.YELLOW, colorama.Style.RESET_ALL,
            ),
            end="",
            file=sys.stderr,
        )
        print(*msg, file=sys.stderr)

    def _time_string(self) -> str:
        delta = time.time() - self.t0
        hours = 0
        minutes = 0
        while delta > 3600:
            hours += 1
            delta -= 3600
        while delta > 60:
            minutes += 1
            delta -= 60
        output = ""
        if hours:
            output += f"{hours}h"
        if minutes:
            output += f"{minutes}m"
        output += f"{round(delta, 1)}s"
        return output

    def error(self, *msg: str) -> None:
        prefix_msg = f"(anyscale +{self._time_string()})"
        self.print_red_error_message(prefix_msg, end_char="")

        print(*msg, file=sys.stderr)

    def confirm_missing_permission(self, msg):
        if self.spinner_manager:
            self.spinner_manager.stop()

        self.warning(msg)

        self.print_red_error_message(
            "[DANGER] To continue without these permissions press 'y', or press 'N' to abort.",
            end_char="",
        )

        click.confirm(
            "", abort=True,
        )

        if self.spinner_manager:
            self.spinner_manager.start()

    def print_red_error_message(self, error_msg, end_char="\n"):
        print(
            "{}{}{} {}".format(
                colorama.Style.BRIGHT,
                colorama.Fore.RED,
                error_msg,
                colorama.Style.RESET_ALL,
            ),
            end=end_char,
            file=sys.stderr,
        )

    @contextmanager
    def indent(self):
        """ Indent all output within the context
        """
        try:
            self.indent_level += 1
            yield
        finally:
            self.indent_level -= 1

    @contextmanager
    def spinner(self, msg: str):
        """DEPRECATED:

        See https://github.com/manrajgrover/halo/issues/179.
        This `Halo` spinner is not compatible with newer Python notebook versions.
        (iPython and Jupyter)

        Use `rich.spinner.Spinner` or `rich.progress.Progress` instead.

        ---
        Create a spinner with the starting text.

        To update the text next to the spinner, set `spinner.text = "new_text"`
        The spinner will be stopped when the context is exited.
        Spinner is only enabled for interactive shell
        """

        enable_spinner = self.is_interactive_cli_enabled()

        with Halo(
            text=msg, spinner="dots", stream=sys.stderr, enabled=enable_spinner
        ) as spinner:
            yield spinner

    def is_interactive_cli_enabled(self) -> bool:
        """Check if shell is interactive
        """

        default_env_var = "1" if sys.stderr.isatty() else "0"
        return os.environ.get("ANYSCALE_CLI_INTERACTIVE_UX", default_env_var) == "1"


class LogsLogger(BlockLogger):
    """ This logger is used to print customer logs to STDOUT with no decoration
    """

    def log(self, msg: str):
        print(msg)


class StringLogger(LogsLogger):
    """ This logger is used to print customer logs to a string with no decoration
    """

    def __init__(self):
        super().__init__(False)
        self.out_string = ""

    def log(self, msg: str):
        self.out_string += f"{msg}\n"

    def is_interactive_cli_enabled(self) -> bool:
        """Check if shell is interactive
        """
        return False


class CloudSetupLogger(LogsLogger):
    def __init__(
        self,
        log_output: bool = True,
        t0: float = _process_start_time,
        spinner_manager: Optional[Halo] = None,
    ):
        self.cloud_resource_errors: List[CloudAnalyticsEventCloudProviderError] = []
        super().__init__(log_output, t0, spinner_manager)

    def log_resource_exception(
        self, resource: CloudAnalyticsEventCloudResource, exc: Exception
    ):
        """
        Record the error in the logger if the exception is an unhandled exception
        """
        if resource in (
            CloudAnalyticsEventCloudResource.GCP_DEPLOYMENT,
            CloudAnalyticsEventCloudResource.GCP_FILESTORE,
            CloudAnalyticsEventCloudResource.GCP_FIREWALL_POLICY,
            CloudAnalyticsEventCloudResource.GCP_PROJECT,
            CloudAnalyticsEventCloudResource.GCP_SERVICE_ACCOUNT,
            CloudAnalyticsEventCloudResource.GCP_STORAGE_BUCKET,
            CloudAnalyticsEventCloudResource.GCP_SUBNET,
            CloudAnalyticsEventCloudResource.GCP_VPC,
            CloudAnalyticsEventCloudResource.GCP_WORKLOAD_IDENTITY_PROVIDER,
        ):
            # exceptions from GCP
            GoogleAPICallError, HttpError = try_import_gcp_exceptions()
            if isinstance(exc, GoogleAPICallError):
                self.log_resource_error(
                    resource, exc.reason, exc.code, "GoogleAPICallError",
                )
                return
            elif isinstance(exc, HttpError):
                reason = None
                with contextlib.suppress(Exception):
                    for error_detail in exc.error_details:
                        if error_detail.get("reason"):
                            reason = str(error_detail["reason"])
                            break
                self.log_resource_error(resource, reason, exc.status_code, "HttpError")
                return
        elif isinstance(exc, ClientError):
            # boto3 client error
            self.log_resource_error(
                resource,
                exc.response.get("Error", {}).get("Code"),
                exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode"),
                "ClientError",
            )
            return
        else:
            unhandled_exception = f"UnknownExceptionType_{exc.__class__.__name__}"
            self.log_resource_error(
                resource, None, None, unhandled_exception,
            )
            return

    def log_resource_error(
        self,
        cloud_resource: CloudAnalyticsEventCloudResource,
        error_reason: Optional[str] = None,
        status_code: Optional[int] = None,
        unhandled_exception: Optional[str] = None,
    ):
        """
        Append the error in the logger. If the error is already logged, it will be deduplicated.
        """
        formatted_error_str = error_reason if error_reason else "unknown"
        if status_code:
            formatted_error_str = f"{formatted_error_str},{status_code}"
        if unhandled_exception:
            formatted_error_str = f"{formatted_error_str},{unhandled_exception}"
        for error in self.cloud_resource_errors:
            if (
                error.cloud_resource == cloud_resource
                and error.error_code == formatted_error_str
            ):
                # deduplicated errors
                return
        self.cloud_resource_errors.append(
            CloudAnalyticsEventCloudProviderError(
                cloud_resource=cloud_resource, error_code=formatted_error_str
            )
        )

    def get_cloud_provider_errors(self) -> List[CloudAnalyticsEventCloudProviderError]:
        return self.cloud_resource_errors

    def clear_cloud_provider_errors(self):
        self.cloud_resource_errors = []
