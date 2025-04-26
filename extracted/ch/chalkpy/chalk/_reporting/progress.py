from __future__ import annotations

import collections
import sys
import time
import uuid
from datetime import datetime, timedelta
from functools import cached_property
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple

from rich import box
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    Task,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.style import Style
from rich.table import Table
from rich.text import Text
from tenacity import Retrying, retry_if_exception_message, stop_after_attempt
from tenacity.wait import wait_exponential_jitter

import chalk
from chalk import EnvironmentId
from chalk._reporting.models import BatchOpKind, BatchOpStatus, BatchReport
from chalk._reporting.rich.color import PASTELY_CYAN, SHADOWY_LAVENDER, UNDERLYING_CYAN
from chalk._reporting.rich.live import ChalkLive
from chalk.client import ChalkBaseException, ChalkError
from chalk.client.exc import CHALK_TRACE_ID_KEY
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    from chalk.client.client_impl import ChalkAPIClientImpl

_logger = get_logger(__name__)


_MAX_ERRORS_TO_DISPLAY = 10
_TTableRow = Tuple[str, str]

try:
    from IPython import get_ipython  # noqa  # pyright: ignore

    # n.b. sometimes this is the `ipython` shell, not a notebook.
    _running_in_jupyter_notebook = get_ipython() is not None
except ImportError:
    _running_in_jupyter_notebook = False


class MofOptionalNCompleteColumn(MofNCompleteColumn):
    """
    Just like MofNCompleteColumn but renders just the completed count,
    instead of `completed / ?` if there is no total
    """

    def render(self, task: Task) -> Text:
        """Show completed/total."""
        completed = int(task.completed)
        if task.total:
            total = int(task.total)
            total_width = len(str(total))
            fmt = f"{completed:{total_width}d}{self.separator}{total}"
        else:
            fmt = f"{completed}"
        return Text(fmt, style="progress.download")


OFFLINE_QUERY = "Offline Query"


class ProgressService:
    def __init__(
        self,
        operation_id: uuid.UUID,
        client: "ChalkAPIClientImpl",
        environment_id: EnvironmentId,
        num_computers: int,
        show_progress: bool,
        caller_method: Optional[str],
    ):
        """
        :param operation_id: The ID of the operation that the ProgressService
            is polling for. This is commonly a `DatasetRevision` ID.
        :param client: A ChalkClient instance
        :param caller_method: Passed only if the caller is a Dataset method. When we call Dataset methods,
            the ProgressService is implicitly called, so we want to explain to the user that their method
            will be executed once the ProgressService finishes polling for the operation to complete.
        """
        super().__init__()
        self.operation_id = operation_id
        self.client = client
        self.caller_method = caller_method
        self._environment_id = environment_id
        self._operation_kind: Optional[BatchOpKind] = None
        self._num_computers = num_computers
        self._shard_id = 0
        if show_progress and not (_running_in_jupyter_notebook or sys.stdout.isatty()):
            _logger.warning("Progress display is not supported in dumb terminals. Progress will not be shown.")
            show_progress = False
        if show_progress:
            self.resolver_progress = Progress(
                TextColumn("  "),
                TimeElapsedColumn(),
                BarColumn(
                    finished_style=Style(color=PASTELY_CYAN),
                    style=Style(color=SHADOWY_LAVENDER),
                    complete_style=Style(color=UNDERLYING_CYAN),
                ),
                MofOptionalNCompleteColumn(),
                TextColumn("runs", style=Style(color=PASTELY_CYAN)),
                TextColumn("{task.description}"),
            )
            self.main_progress = Progress(
                TextColumn("{task.description}"),
                SpinnerColumn(style=Style(color=SHADOWY_LAVENDER)),
                TimeElapsedColumn(),
            )
            self.explainer_text = (
                Text(
                    f"The `DatasetRevision` is still being computed. {caller_method}() will execute once computation is complete.",
                    style=Style(color=PASTELY_CYAN),
                )
                if caller_method
                else None
            )
            if self._num_computers > 1:
                self.shard_progress = Progress(
                    TextColumn("{task.description}"),
                    MofNCompleteColumn(),
                    BarColumn(
                        finished_style=Style(color=PASTELY_CYAN),
                        style=Style(color=SHADOWY_LAVENDER),
                        complete_style=Style(color=UNDERLYING_CYAN),
                    ),
                    TaskProgressColumn(),
                )
            else:
                self.shard_progress = None
        else:
            self.resolver_progress = None
            self.main_progress = None
            self.explainer_text = None
            self.shard_progress = None

    @cached_property
    def enclosure_panel(self) -> Panel | None:
        if self.main_progress is None or self.resolver_progress is None:
            return None
        if self.shard_progress is None:
            progress_bar_group = Group(self.main_progress, self.resolver_progress)
        else:
            blank_line = Padding(Text(""), pad=(0, 0, 0, 0))
            progress_bar_group = Group(self.shard_progress, blank_line, self.main_progress, self.resolver_progress)
        panel_content_table = Table.grid()
        if self.explainer_text is not None:
            panel_content_table.add_row(Padding(self.explainer_text, (0, 0, 1, 0)))
        panel_content_table.add_row(progress_bar_group)

        enclosure_panel = Panel.fit(
            panel_content_table, title="chalk", border_style=Style(color=PASTELY_CYAN), box=box.ROUNDED, padding=(1, 2)
        )

        return enclosure_panel

    def handle_resolver_update(self, batch_report: BatchReport, fqn_to_task_id: dict[str, TaskID]) -> None:
        if self.resolver_progress is None:
            return None
        for resolver_report in batch_report.resolvers:
            fqn = resolver_report.resolver_fqn
            if fqn not in fqn_to_task_id:
                short_name = fqn.split(".")[-1]
                fqn_to_task_id[fqn] = self.resolver_progress.add_task(
                    description=f"[ {short_name} ]",
                    total=resolver_report.progress.total or None,
                )

        for resolver_report in batch_report.resolvers:
            fqn = resolver_report.resolver_fqn
            resolver_task_id = fqn_to_task_id[fqn]

            rows_done_new = resolver_report.progress.computed + resolver_report.progress.failed
            self.resolver_progress.update(
                resolver_task_id,
                completed=rows_done_new,
                # total might change as the same resolver gets invoked in a separate node
                total=resolver_report.progress.total or None,
            )

    def handle_success(
        self,
        main_task_id: TaskID,
        operation_display_type: str,
        fqn_to_task_id: dict[str, TaskID],
        shard_task_id: TaskID | None,
    ):
        if shard_task_id is not None and self.shard_progress is not None:
            self.shard_progress.update(shard_task_id, advance=1)
        if self.enclosure_panel is not None:
            if self._shard_id == self._num_computers:
                self.enclosure_panel.title = "chalk ■"
        if self.main_progress is not None:
            if self._shard_id == self._num_computers:
                self.main_progress.update(main_task_id, description=f"{operation_display_type} completed", completed=1)
        if self.resolver_progress is not None:
            for task_id in fqn_to_task_id.values():
                self.resolver_progress.reset(task_id)

    def _get_failing_resolver(self, batch_report: BatchReport) -> Optional[str]:
        """
        :return: The name of the resolver that failed, or None if no resolver failed.
        """
        for resolver in batch_report.resolvers:
            if resolver.status == BatchOpStatus.FAILED:
                return resolver.resolver_fqn

    @staticmethod
    def _get_pkey_display_value(error: ChalkError) -> Optional[str]:
        if error.display_primary_key is None:
            return None

        value = ""
        if error.display_primary_key_fqn:
            value += error.display_primary_key_fqn + ": "

        value += error.display_primary_key

        return value

    def _get_error_details(self, errors: List[ChalkError]) -> List[_TTableRow]:
        if not errors:
            return [
                (
                    "Error Message",
                    "Unfortunately the cause of this error is unknown. Please contact Chalk for support and provide the Revision ID or the Trace ID above.",
                )
            ]

        truncated_from = None
        if len(errors) > _MAX_ERRORS_TO_DISPLAY:
            truncated_from = len(errors)
            errors = errors[:_MAX_ERRORS_TO_DISPLAY]

        grouped_details: Dict[int, List[_TTableRow]] = collections.defaultdict(list)
        for i, e in enumerate(errors):
            grouped_details[i].append((f"Error {i + 1}", e.message) if len(errors) > 1 else ("Error", e.message))
            if e.exception and e.exception.message:
                grouped_details[i].append((f"Exception", e.exception.message))
            if e.exception and e.exception.stacktrace:
                grouped_details[i].append((f"Stacktrace", e.exception.stacktrace))
            if val := self._get_pkey_display_value(e):
                grouped_details[i].append((f"Pkey", val))

        flattened_details = sum(list(grouped_details.values()), [])
        if truncated_from:
            flattened_details.append(
                ("Errors Truncated", f"Displaying only {_MAX_ERRORS_TO_DISPLAY} out of {truncated_from}")
            )

        return flattened_details

    def handle_and_raise_error(
        self,
        batch_report: BatchReport,
        main_task_id: TaskID,
        operation_display_type: str,
        is_fatal: bool = True,
    ) -> None:
        panel = self.enclosure_panel
        main_progress = self.main_progress
        if panel is None or main_progress is None:
            return

        all_errors = batch_report.all_errors or []
        if not all_errors and batch_report.error:
            # `all_errors` is added long after `error`.
            # We might be hitting old server code here,
            # make sure we can still talk to old server.
            all_errors.append(batch_report.error)

        progress_table = panel.renderable

        if is_fatal:
            self.handle_explainer_text_if_erring()
        else:
            self.handle_explainer_text_if_resolver_runtime_error()
        panel.border_style = Style(color="red" if is_fatal else "yellow")
        main_progress.update(
            main_task_id,
            description=f"Error occurred while executing {operation_display_type}",
        )

        key_to_display_key = {
            CHALK_TRACE_ID_KEY: "Trace ID",
        }

        metadata = batch_report.operation_metadata or {}
        metadata_tuples = [(key_to_display_key.get(k, k), v) for k, v in metadata.items()]
        failing_resolver = self._get_failing_resolver(batch_report)

        table_contents: List[_TTableRow] = [
            ("Revision ID", str(self.operation_id)),
            *metadata_tuples,
            *([("Failing Resolver", failing_resolver)] if failing_resolver else []),
            *self._get_error_details(all_errors),
        ]
        error_box = Table(
            box=box.SQUARE,
            show_lines=True,
            show_header=False,
            style=Style(color="red" if is_fatal else "yellow"),
            row_styles=[Style(color="red" if is_fatal else "yellow")] * len(table_contents),
        )

        for row in table_contents:
            error_box.add_row(*row)

        assert isinstance(progress_table, Table)
        progress_table.add_row(Padding(Text(""), (0, 0, 1, 0)))
        progress_table.add_row(error_box)

    def handle_explainer_text_if_erring(self):
        if self.explainer_text:
            assert self.caller_method is not None
            self.explainer_text.plain = (
                f"The computation for this `DatasetRevision` has failed. {self.caller_method}() cannot be executed."
            )
            self.explainer_text.style = Style(color="red")

    def handle_explainer_text_if_resolver_runtime_error(self):
        if self.explainer_text:
            assert self.caller_method is not None
            self.explainer_text.plain = f"The computation for this `DatasetRevision` has failed due to a resolver runtime error. {self.caller_method}() can still be executed."
            self.explainer_text.style = Style(color="yellow")

    def poll_report(
        self,
        timeout: float | timedelta | None,
        completion_timeout: float | timedelta | None,
    ) -> Iterable[BatchReport]:
        if completion_timeout is None:
            completion_deadline = datetime.max
        else:
            if not isinstance(completion_timeout, timedelta):
                completion_timeout = timedelta(seconds=completion_timeout)
            completion_deadline = datetime.now() + completion_timeout

        if timeout is None:
            must_receive_next_report_by = datetime.max
        else:
            if not isinstance(timeout, timedelta):
                timeout = timedelta(seconds=timeout)
            must_receive_next_report_by = datetime.now() + timeout

        while datetime.now() < must_receive_next_report_by and datetime.now() < completion_deadline:
            time.sleep(0.5)

            for attempt in Retrying(
                stop=stop_after_attempt(5),
                wait=wait_exponential_jitter(),
                reraise=True,
                retry=retry_if_exception_message(match="504|dialing"),
            ):
                with attempt:
                    batch_report = self.client.get_batch_report(self.operation_id, self._environment_id, self._shard_id)
                    if batch_report is not None:
                        if timeout is not None:
                            must_receive_next_report_by = datetime.now() + timeout
                        self._operation_kind = batch_report.operation_kind
                        yield batch_report
        else:
            if datetime.now() >= completion_deadline:
                raise TimeoutError(
                    f"Timed out waiting ({completion_timeout}) for completion of operation with id '{self.operation_id}' (chalkpy=={chalk.__version__})"
                )
            else:
                raise TimeoutError(
                    f"Timed out waiting ({timeout}) for next status report for operation with id '{self.operation_id}' (chalkpy=={chalk.__version__})"
                )

    def await_operation(self, must_fail_on_resolver_error: bool, timeout: float | timedelta | None) -> None:
        fqn_to_task_id: dict[str, TaskID] = {}
        initial_description = "Starting query execution"
        if self.main_progress is not None:
            main_task_id = self.main_progress.add_task(description=initial_description, total=1)
            if self.shard_progress is not None:
                shard_task_id = self.shard_progress.add_task(description="Processing Shards", total=self._num_computers)
            else:
                shard_task_id = None
        else:
            main_task_id = None
            shard_task_id = None

        with ChalkLive(self.enclosure_panel, auto_refresh=True):
            for batch_report in self.poll_report(timeout, completion_timeout=self.client.default_job_timeout):

                # Update main progress text
                if main_task_id is not None:
                    assert self.main_progress is not None
                    assert main_task_id is not None
                    if self.main_progress.tasks[main_task_id].description == initial_description:
                        description = f"Executing {OFFLINE_QUERY}: "
                        self.main_progress.update(main_task_id, description=description)

                self.handle_resolver_update(batch_report=batch_report, fqn_to_task_id=fqn_to_task_id)

                if batch_report.status == BatchOpStatus.COMPLETED:
                    self._shard_id += 1
                    if main_task_id is not None:
                        self.handle_success(
                            main_task_id=main_task_id,
                            operation_display_type=OFFLINE_QUERY,
                            fqn_to_task_id=fqn_to_task_id,
                            shard_task_id=shard_task_id,
                        )
                    if self._shard_id == self._num_computers:
                        break

                if batch_report.status == BatchOpStatus.FAILED:
                    if main_task_id is not None:
                        if all(e.is_resolver_runtime_error() for e in (batch_report.all_errors or ())):
                            # There is no chalk error, we should NOT raise an exception, but definitely warn the user
                            self.handle_and_raise_error(
                                batch_report=batch_report,
                                main_task_id=main_task_id,
                                operation_display_type=OFFLINE_QUERY,
                                is_fatal=must_fail_on_resolver_error,
                            )
                        else:
                            self.handle_and_raise_error(
                                batch_report=batch_report,
                                main_task_id=main_task_id,
                                operation_display_type=OFFLINE_QUERY,
                            )
                    if must_fail_on_resolver_error:
                        raise ChalkBaseException(
                            trace_id=(batch_report.operation_metadata or {}).get(CHALK_TRACE_ID_KEY),
                            errors=batch_report.all_errors,
                        )
                    break  # should have raised but just in case
