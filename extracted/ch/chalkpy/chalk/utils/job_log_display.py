"""Job log display and state management for monitoring background jobs."""

import datetime as dt
import re
import time
from typing import TYPE_CHECKING, Callable, Optional

from google.protobuf import timestamp_pb2
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.spinner import Spinner
from rich.style import Style
from rich.table import Table
from rich.text import Text

from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import GetJobQueueOperationSummaryResponse, JobQueueState
from chalk._gen.chalk.server.v1.log_pb2 import SearchLogEntriesRequest
from chalk._reporting.rich.color import (
    CITRUSY_YELLOW,
    GRASSY_GREEN,
    SERENDIPITOUS_PURPLE,
    SHADOWY_LAVENDER,
    SHY_RED,
    UNDERLYING_CYAN,
)
from chalk.utils.collections import FrozenOrderedSet

if TYPE_CHECKING:
    from chalk._gen.chalk.server.v1.log_pb2_grpc import LogSearchServiceStub


class JobLogDisplay:
    """Manages the display and state tracking for job monitoring.

    This class provides a generic interface for monitoring background jobs with
    status updates and log streaming. It can be used for any job type that uses
    the job queue system (training jobs, data processing jobs, etc.).
    """

    def __init__(self, max_logs_display: int = 10, title: str = "Jobs"):
        """Initialize the job log display.

        Parameters
        ----------
        max_logs_display
            Maximum number of recent logs to display
        title
            Title to display in the status table (e.g., "Model Training Jobs", "Processing Jobs")
        """
        super().__init__()
        self.job_states: dict[int, tuple[str, JobQueueState]] = {}
        self.recent_logs: list[tuple[str, str]] = []
        self.seen_log_content: set[tuple[str, str]] = set()
        self.max_logs_display = max_logs_display
        self.animation_frame = 0
        self.start_time = time.time()
        self.console = Console()
        self.title = title

        # Log following state
        self.latest_timestamp: Optional[timestamp_pb2.Timestamp] = None
        self.seen_log_ids: dict[str, bool] = {}

        # Terminal states that indicate the job has finished
        self.terminal_states = FrozenOrderedSet(
            {
                JobQueueState.JOB_QUEUE_STATE_COMPLETED,
                JobQueueState.JOB_QUEUE_STATE_FAILED,
                JobQueueState.JOB_QUEUE_STATE_CANCELED,
            }
        )

    def update_job_state(self, job_idx: int, state_name: str, state: JobQueueState) -> None:
        """Update the state of a specific job.

        Parameters
        ----------
        job_idx
            Index of the job
        state_name
            Human-readable name of the state
        state
            The JobQueueState enum value
        """
        self.job_states[job_idx] = (state_name, state)

    def add_log(self, timestamp: str, message: str) -> None:
        """Add a log entry to the recent logs.

        Parameters
        ----------
        timestamp
            Formatted timestamp string
        message
            Log message
        """
        self.recent_logs.append((timestamp, message))

    def is_all_terminal(self) -> bool:
        """Check if all jobs have reached a terminal state.

        Returns
        -------
        bool
            True if all jobs are in a terminal state
        """
        if not self.job_states:
            return False
        return all(state in self.terminal_states for _, state in self.job_states.values())

    def is_successful(self) -> bool:
        """Check if all jobs completed successfully.

        Returns
        -------
        bool
            True if all jobs completed successfully
        """
        return all(state == JobQueueState.JOB_QUEUE_STATE_COMPLETED for _, state in self.job_states.values())

    @staticmethod
    def clean_log_message(message: str) -> str:
        """Remove job metadata from log message.

        Parameters
        ----------
        message
            Raw log message

        Returns
        -------
        str
            Cleaned log message
        """
        # Remove patterns like "job(id=1, ... attempt_idx=1)"
        cleaned = re.sub(r"job\(id=\d+.*?attempt_idx=\d+\)\s*", "", message)
        return cleaned.strip()

    def get_status_renderable(self, state: JobQueueState, state_name: str):
        """Return the renderable (spinner or text) for a given job state.

        Parameters
        ----------
        state
            The JobQueueState enum value
        state_name
            Human-readable name of the state

        Returns
        -------
        Text or Columns
            Rich renderable for the status
        """
        display_name = state_name.replace("JOB_QUEUE_STATE_", "").replace("_", " ").title()

        if state == JobQueueState.JOB_QUEUE_STATE_COMPLETED:
            return Text(f"✓ {display_name}", style=Style(color=GRASSY_GREEN, bold=True))
        elif state == JobQueueState.JOB_QUEUE_STATE_FAILED:
            return Text(f"✗ {display_name}", style=Style(color=SHY_RED, bold=True))
        elif state == JobQueueState.JOB_QUEUE_STATE_CANCELED:
            return Text(f"⊗ {display_name}", style=Style(color=SHADOWY_LAVENDER))
        elif "RUNNING" in state_name:
            return Columns(
                [
                    Spinner("dots", style=Style(color=UNDERLYING_CYAN)),
                    Text(f"{display_name}", style=Style(color=UNDERLYING_CYAN, bold=True)),
                ],
                expand=False,
            )
        elif "PENDING" in state_name or "QUEUED" in state_name:
            return Columns(
                [
                    Spinner("dots2", style=Style(color=CITRUSY_YELLOW)),
                    Text(f"{display_name}", style=Style(color=CITRUSY_YELLOW)),
                ],
                expand=False,
            )
        else:
            return Text(f"◐ {display_name}", style=Style(color=SERENDIPITOUS_PURPLE))

    def format_elapsed_time(self) -> str:
        """Format elapsed time since job started.

        Returns
        -------
        str
            Formatted time string (HH:MM:SS or MM:SS)
        """
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def create_status_table(self) -> Table:
        """Create a status table showing current job states.

        Returns
        -------
        Table
            Rich table with job statuses
        """
        elapsed_str = self.format_elapsed_time()
        title_text = Text(self.title, style=Style(color=UNDERLYING_CYAN, bold=True))
        title_text.append(f" [{elapsed_str}]", style=Style(color=SHADOWY_LAVENDER, dim=True))

        table = Table(
            title=title_text,
            title_justify="left",
            box=None,
            show_header=True,
            header_style=Style(color=SHADOWY_LAVENDER, bold=True),
        )
        table.add_column("Job", style=Style(color=SHADOWY_LAVENDER))
        table.add_column("Status")

        if not self.job_states:
            waiting_status = Columns(
                [
                    Spinner("dots", style=Style(color=CITRUSY_YELLOW)),
                    Text("Waiting for jobs...", style=Style(color=CITRUSY_YELLOW, italic=True)),
                ],
                expand=False,
            )
            table.add_row("", waiting_status)
        else:
            for job_idx in sorted(self.job_states.keys()):
                state_name, state = self.job_states[job_idx]
                status_renderable = self.get_status_renderable(state, state_name)
                table.add_row(f"Job {job_idx}", status_renderable)

        return table

    def create_logs_panel(self) -> Panel:
        """Create a panel showing recent logs.

        Returns
        -------
        Panel
            Rich panel with recent log entries
        """
        if not self.recent_logs:
            num_dots = (self.animation_frame // 2) % 4
            dots = "." * num_dots
            log_content = Text(f"Waiting for logs{dots:<3}", style=Style(color=SHADOWY_LAVENDER, italic=True))
        else:
            log_lines: list[Text] = []
            for timestamp, message in self.recent_logs[-self.max_logs_display :]:
                line = Text()
                line.append(timestamp, style=Style(color=SERENDIPITOUS_PURPLE, bold=True))
                line.append(" ")
                cleaned_message = self.clean_log_message(message)
                line.append(cleaned_message, style=Style(color="white"))
                log_lines.append(line)
            log_content = Text("\n").join(log_lines)

        return Panel(
            log_content,
            title="Recent Logs",
            title_align="left",
            border_style=Style(color=SERENDIPITOUS_PURPLE),
        )

    def create_display(self) -> Group:
        """Create the full display with status and logs.

        Returns
        -------
        Group
            Rich group containing status table and logs panel
        """
        return Group(self.create_status_table(), Text(""), self.create_logs_panel())

    def increment_animation(self) -> None:
        """Increment the animation frame counter."""
        self.animation_frame += 1

    def print_final_summary(self) -> None:
        """Print the final summary of the job."""
        if self.is_successful():
            self.console.print(Text("✓ Job completed successfully", style=Style(color=GRASSY_GREEN, bold=True)))
        else:
            self.console.print(Text("✗ Job failed or was canceled", style=Style(color=SHY_RED, bold=True)))

    def poll_logs(
        self,
        log_stub: "LogSearchServiceStub",
        query: str,
        poll_interval: float,
        should_stop_callback: Callable[[], bool],
        output_callback: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        """Poll for new logs and display them.

        Parameters
        ----------
        log_stub
            The gRPC stub for log search service
        query
            The search query to filter logs
        poll_interval
            Time in seconds between polling for new logs
        should_stop_callback
            Callback that returns True when polling should stop
        output_callback
            Optional callback function that receives (timestamp, message) for each log entry.
            If None, logs are added to the display.
        """
        try:
            while not should_stop_callback():
                # Fetch logs starting from the latest timestamp we've seen
                req = SearchLogEntriesRequest(query=query)

                if self.latest_timestamp is not None:
                    req.start_time.CopyFrom(self.latest_timestamp)

                try:
                    resp = log_stub.SearchLogEntries(req)
                except Exception as e:
                    if output_callback:
                        output_callback("", f"[LOG ERROR] {e}")
                    else:
                        self.add_log("", f"[LOG ERROR] {e}")
                    time.sleep(poll_interval)
                    continue

                # Sort logs by timestamp (oldest first)
                sorted_logs = sorted(
                    resp.log_entries, key=lambda log: log.timestamp.seconds + log.timestamp.nanos / 1e9
                )

                # Display new logs and track the latest timestamp
                max_timestamp = self.latest_timestamp
                for log in sorted_logs:
                    if log.id not in self.seen_log_ids:
                        formatted_time = self._format_timestamp(log.timestamp)
                        formatted_message = log.message.replace("\n", " ")

                        if output_callback:
                            output_callback(formatted_time, formatted_message)
                        else:
                            self.add_log(formatted_time, formatted_message)

                        self.seen_log_ids[log.id] = True

                    # Track the maximum timestamp we've seen
                    if max_timestamp is None or not self._is_timestamp_after(max_timestamp, log.timestamp):
                        max_timestamp = log.timestamp

                # Update latest_timestamp after processing all logs in this batch
                if max_timestamp is not None and (
                    self.latest_timestamp is None
                    or max_timestamp.seconds > self.latest_timestamp.seconds
                    or (
                        max_timestamp.seconds == self.latest_timestamp.seconds
                        and max_timestamp.nanos > self.latest_timestamp.nanos
                    )
                ):
                    # Advance by 1 full second since server filters at second-level precision (RFC3339)
                    # Using nanosecond precision would cause the same logs to be re-fetched
                    self.latest_timestamp = timestamp_pb2.Timestamp(seconds=max_timestamp.seconds + 1, nanos=0)

                # Wait before next poll
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            pass

    @staticmethod
    def _format_timestamp(timestamp: timestamp_pb2.Timestamp) -> str:
        """Format a protobuf timestamp for display.

        Parameters
        ----------
        timestamp
            The protobuf timestamp to format

        Returns
        -------
        str
            Formatted timestamp string
        """
        dt_obj = dt.datetime.fromtimestamp(timestamp.seconds + timestamp.nanos / 1e9, tz=dt.timezone.utc)
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _is_timestamp_after(ts1: timestamp_pb2.Timestamp, ts2: Optional[timestamp_pb2.Timestamp]) -> bool:
        """Check if ts1 is after ts2.

        Parameters
        ----------
        ts1
            First timestamp
        ts2
            Second timestamp

        Returns
        -------
        bool
            True if ts1 is after ts2
        """
        if ts2 is None:
            return True
        if ts1.seconds > ts2.seconds:
            return True
        if ts1.seconds == ts2.seconds and ts1.nanos > ts2.nanos:
            return True
        return False

    def poll_job_status(
        self,
        get_status_callback: Callable[[], "GetJobQueueOperationSummaryResponse"],
        poll_interval: float,
        should_stop_callback: Callable[[], bool],
    ) -> None:
        """Poll for job status updates.

        Parameters
        ----------
        get_status_callback
            Callback function that returns the job queue operation summary
        poll_interval
            Time in seconds between polling for status
        should_stop_callback
            Callback that returns True when polling should stop
        """
        try:
            while not should_stop_callback():
                try:
                    response = get_status_callback()

                    if response.HasField("summary"):
                        # Update job states
                        for row_summary in response.summary.indexed_row_summaries.values():
                            job_idx = row_summary.job_idx if row_summary.HasField("job_idx") else 0
                            state_name = JobQueueState.Name(row_summary.state)
                            self.update_job_state(job_idx, state_name, row_summary.state)

                        # Stop when all jobs reach terminal state
                        if self.is_all_terminal():
                            return

                except Exception as e:
                    # Add error to logs
                    self.add_log("", f"[STATUS ERROR] {e}")

                # Wait before next poll
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            pass

    def follow_job(
        self,
        get_status_callback: Callable[[], "GetJobQueueOperationSummaryResponse"],
        log_stub: "LogSearchServiceStub",
        log_query: str,
        poll_interval: float = 2.0,
        output_callback: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        """Follow a job, displaying both status and logs.

        This method handles all the threading coordination and display logic
        for following a job in real-time.

        Parameters
        ----------
        get_status_callback
            Callback function that returns the job queue operation summary
        log_stub
            The gRPC stub for log search service
        log_query
            The search query to filter logs
        poll_interval
            Time in seconds between polling for status and logs. Defaults to 2.0 seconds.
        output_callback
            Optional callback function that receives (timestamp, message) for each log entry.
            If None, logs are displayed using Rich live display.
        """
        import threading

        from rich.live import Live

        # Flag to coordinate between threads
        should_stop = threading.Event()

        def status_done_callback():
            should_stop.set()

        def poll_status():
            try:
                self.poll_job_status(
                    get_status_callback=get_status_callback,
                    poll_interval=poll_interval,
                    should_stop_callback=should_stop.is_set,
                )
                status_done_callback()
            except KeyboardInterrupt:
                should_stop.set()

        def poll_logs_thread():
            self.poll_logs(
                log_stub=log_stub,
                query=log_query,
                poll_interval=poll_interval,
                should_stop_callback=should_stop.is_set,
                output_callback=output_callback,
            )

        # Start both polling threads
        status_thread = threading.Thread(target=poll_status, daemon=True)
        log_thread = threading.Thread(target=poll_logs_thread, daemon=True)

        status_thread.start()
        log_thread.start()

        # Use Live display if no callback is provided
        if output_callback is None:
            with Live(self.create_display(), console=self.console, refresh_per_second=4) as live:
                try:
                    while not should_stop.is_set():
                        live.update(self.create_display())
                        self.increment_animation()
                        time.sleep(0.25)
                except KeyboardInterrupt:
                    should_stop.set()

            # Print final summary
            self.print_final_summary()
        else:
            # When using callback, just wait for completion
            try:
                status_thread.join()
                log_thread.join()
            except KeyboardInterrupt:
                should_stop.set()
                status_thread.join(timeout=1)
                log_thread.join(timeout=1)
