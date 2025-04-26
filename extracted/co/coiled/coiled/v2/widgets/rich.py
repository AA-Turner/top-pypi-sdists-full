from __future__ import annotations

import datetime
import math
import sys
from collections import Counter
from pathlib import Path
from textwrap import dedent
from types import TracebackType
from typing import Any, Dict, Iterable, List, Mapping, Tuple, Type, cast

import jmespath
import rich
import rich.align
import rich.bar
import rich.box
import rich.console
import rich.layout
import rich.live
import rich.panel
import rich.progress
import rich.table
from rich.console import RenderableType

from coiled.types import PackageLevelEnum

from ...capture_environment import ResolvedPackageInfo
from ...errors import ClusterCreationError
from ...utils import get_details_url
from ..states import (
    CombinedProcessStateEnum,
    ProcessStateEnum,
    combined_state_to_description,
    get_combined_process_state,
)
from . import EXECUTION_CONTEXT
from .interface import ClusterWidget
from .util import get_instance_types, get_worker_statuses

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

# This is annoying. I think Ian explained to me that the reason
# we need to manage the size so manually is that if we aren't explicit,
# Jupyter notebooks (but not IPython terminal) messes up the size.
BASE_CONSOLE_HEIGHT = 17
WAITING_PROGRESS_HEIGHT = 9
WAITING_CONSOLE_HEIGHT = BASE_CONSOLE_HEIGHT + WAITING_PROGRESS_HEIGHT
DONE_PROGRESS_HEIGHT = 6
DONE_CONSOLE_HEIGHT = BASE_CONSOLE_HEIGHT + DONE_PROGRESS_HEIGHT
CONSOLE_WIDTH = 80


def level_to_str(level: PackageLevelEnum) -> str | None:
    if level >= PackageLevelEnum.CRITICAL:
        return "Critical"
    elif level >= PackageLevelEnum.WARN:
        return "Warning"
    elif level >= PackageLevelEnum.NONE:
        return "Low"
    else:
        return None


def print_rich_package_table(
    packages_with_notes: List[ResolvedPackageInfo],
    packages_with_errors: List[Tuple[ResolvedPackageInfo, PackageLevelEnum]],
):
    console = rich.console.Console(width=CONSOLE_WIDTH)

    home_dir = str(Path.home())

    if packages_with_notes:
        note_table = rich.table.Table(expand=True, box=rich.box.MINIMAL)
        note_table.add_column("Package")
        note_table.add_column("Note", overflow="fold")
        for pkg in packages_with_notes:
            note_table.add_row(pkg["name"], cast(str, pkg["note"]).replace(home_dir, "~", 1))
        console.print(rich.panel.Panel(note_table, title="[bold green]Package Info[/bold green]"))
    if packages_with_errors and any(level_to_str(level) for _, level in packages_with_errors):
        error_table = rich.table.Table(expand=True, box=rich.box.MINIMAL)
        error_table.add_column("Package")
        error_table.add_column("Error")
        error_table.add_column("Level")
        for pkg_info, level in sorted(packages_with_errors, key=lambda p: (p[1], p[0]["name"]), reverse=True):
            level_str = level_to_str(level)
            if level_str is not None:
                error_table.add_row(pkg_info["name"], pkg_info["error"], level_str)
        console.print(rich.panel.Panel(error_table, title="[bold red]Not Synced with Cluster[/bold red]"))


def format_seconds(seconds, decimals=0, variant="long"):
    """
    Format a number of seconds into a human-readable time delta.
    ported from formatSeconds in frontend/src/utils/index.ts
    """
    is_long = variant == "long"
    if seconds < 0:
        raise ValueError(f"Invalid time: {seconds} seconds")
    if seconds < 1:
        return f"{seconds:.{decimals}f} {'seconds' if is_long else 's'}" if decimals > 0 and seconds > 0 else "0"
    remainder = seconds
    years = math.floor(remainder / 60 / 60 / 24 / 365.25)
    remainder = remainder - years * 24 * 60 * 60 * 365.25
    days = math.floor(remainder / 60 / 60 / 24)
    remainder = remainder - days * 24 * 60 * 60
    hours = math.floor(remainder / 60 / 60) if years == 0 else 0
    remainder = remainder - hours * 60 * 60
    minutes = math.floor(remainder / 60) if years == 0 and days == 0 else 0
    remainder = remainder - minutes * 60
    seconds = remainder if years == 0 and days == 0 and hours == 0 else 0
    seconds = round(seconds)
    year_postfix = " year" + ("s " if years > 1 else " ") if is_long else "yr "
    day_postfix = " day" + ("s " if days > 1 else " ") if is_long else "d "
    hour_postfix = " hour" + ("s " if hours > 1 else " ") if is_long else "h "
    minute_postfix = " minute" + ("s " if minutes > 1 else " ") if is_long else "m "
    second_postfix = " second" + ("s " if seconds > 1 else " ") if is_long else "s "
    return (
        (f"{years}{year_postfix}" if years > 0 else "")
        + (f"{days}{day_postfix}" if days > 0 else "")
        + (f"{hours}{hour_postfix}" if hours > 0 else "")
        + (f"{minutes}{minute_postfix}" if minutes > 0 else "")
        + (f"{seconds}{second_postfix}" if seconds > 0 else "")
    ).strip()


class LightRichClusterWidget(ClusterWidget):
    """A Rich renderable showing cluster status."""

    n_workers: int
    _cluster_details: Mapping[str, Any] | None
    _progress: rich.progress.Progress

    def __init__(
        self,
        n_workers: int = 0,
        transient: bool = False,
        console: rich.console.Console | None = None,
        *,
        title: str,
        server: str | None = None,
        workspace: str | None = None,
        extra_link_title: str | None = None,
        extra_link: str | None = None,
        width: int = 80,
        include_total_cost: bool = True,
    ):
        """Set up the renderable widget."""
        self.__started = False
        self.server = server
        self.workspace = workspace
        self._cluster_details = None
        self._final_update = None
        self._extra_link_title = extra_link_title or "Server"
        self._extra_link = extra_link
        self._trailer = None
        self._width = width
        self._loader_frames = ["...", " ..", "  .", "   ", ".  ", ".. "]
        self._frame = 0
        self._include_total_cost = include_total_cost
        self.last_updated_utc = datetime.datetime.now(datetime.timezone.utc)
        if console:
            self.console = console
        else:
            self.console = rich.console.Console()
            self.console.size = (CONSOLE_WIDTH, BASE_CONSOLE_HEIGHT)

        self._progress = progress = rich.progress.Progress(
            "{task.description}",
            rich.progress.BarColumn(
                complete_style="progress.remaining",
                bar_width=self._width - 20,
            ),
            expand=True,
        )
        self._task = progress.add_task("Starting", total=5)
        self._title = title

        # Calls _get_renderable, so the progress bar must be set up first.
        self.live = rich.live.Live(
            transient=transient,
            console=self.console,
            get_renderable=self._get_renderable,
        )

    def start(self):
        """Start the live instance."""
        if self.__started:
            return
        self.__started = True
        self.live.start(refresh=False)

    def stop(self):
        """Stop the live instance."""
        if not self.__started:
            return
        self.__started = False
        self.live.stop()

    def __enter__(self) -> LightRichClusterWidget:
        """Enter a live-updating context.

        Example
        -------
        with RichClusterWidget(n_workers) as w:
            # do stuff
        """
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the live-updating context and reset the display ID.

        Keep the widget around for user inspection if there was a cluster creation
        error, otherwise remove it.
        """
        if exc_type == ClusterCreationError and self.live.transient:
            self.live.transient = False
        self.stop()

    def update(
        self,
        cluster_details: Mapping[str, Any] | None,
        logs,
        *args,
        final_update=None,
        server: str | None = None,
        workspace: str | None = None,
        extra_link: str | None = None,
        trailer: str | None = None,
        **kwargs,
    ) -> None:
        """Update cluster data.

        Note: this does not trigger any refreshing, that is handled by the Live
        instance, which does it periodically.
        """
        self.start()
        if server is not None:
            self.server = server

        if workspace is not None:
            self.workspace = workspace

        if cluster_details is not None:
            self._cluster_details = cluster_details

        if extra_link is not None:
            self._extra_link = extra_link

        if trailer is not None:
            self._trailer = trailer

        # track when the widget last received new data about the cluster
        # (which is less often than the widget renders)
        self.last_updated_utc = datetime.datetime.now(datetime.timezone.utc)

        if final_update is not None:
            self._final_update = final_update

        # We explicitly refresh to make sure updated info is shown.
        # (Bad timing can lead auto-refresh to not show the update before we stop.)
        self.live.refresh()

    def _get_renderable(self) -> rich.console.RenderableType:
        """Construct the rendered layout."""

        current_loader_frame = self._loader_frames[self._frame]

        if self._cluster_details:
            approx_cloud_cost_per_hour = self._cluster_details.get("cloud_cost_per_hour") or (
                self._cluster_details["cost_per_hour"] * 0.05
            )
            approx_cloud_total = self._cluster_details.get("cloud_total_cost") or (
                self._cluster_details["total_cost"] * 0.05
            )

            uptime = self._cluster_details["billable_time"] or 0.0
            scheduler_combined_process_state = get_combined_process_state(self._cluster_details["scheduler"])
            scheduler_instance_type, _ = get_instance_types(self._cluster_details)
            region = self._cluster_details["cluster_options"]["region_name"]
            zone = self._cluster_details["cluster_options"]["zone_name"]
            zone_desc = f" ({zone})" if zone else ""
            link = get_details_url(self.server, self.workspace, self._cluster_details["id"])
            env_name = self._cluster_details["senv_alias"]["name"]
            if env_name.startswith("package-sync-"):
                env_name = ""
                local_env_name = Path(sys.prefix).name
                env_line = f"[bold green]Synced local Python environment:[/bold green] {local_env_name}"
            else:
                local_env_name = ""
                env_line = f"[bold green]Environment:[/bold green] {env_name}"

            if not scheduler_instance_type:
                scheduler_instance_type = current_loader_frame
        else:
            approx_cloud_cost_per_hour = 0.0
            approx_cloud_total = 0.0
            uptime = 0.0
            scheduler_combined_process_state = None
            scheduler_instance_type = current_loader_frame
            region = current_loader_frame
            zone_desc = ""
            link = current_loader_frame
            env_line = ""

        config = (
            ("[bold green]Region:[/bold green]", rich.align.Align.left(f"{region}{zone_desc}")),
            ("[bold green]VM Type:[/bold green]", rich.align.Align.left(f"{scheduler_instance_type}")),
        )

        # It's nice to show both hourly and total cost, but `coiled run` (currently) won't update widget
        # while the user's script is running, so total wouldn't change over time and would be unhelpful.
        total_cost = (
            [
                (
                    "[bold green]Approx cloud total:[/bold green]",
                    rich.align.Align.right(f"${approx_cloud_total:.2f}"),
                )
            ]
            if self._include_total_cost
            else []
        )
        costing = (
            ("[bold green]Uptime:[/bold green]", rich.align.Align.right(f"{format_seconds(uptime, variant='short')}")),
            (
                "[bold green]Approx cloud cost:[/bold green]",
                rich.align.Align.right(f"${approx_cloud_cost_per_hour:.2f}/hr"),
            ),
            *total_cost,
        )

        linked_details_link = (
            f"[link={link}]{link}[/link]" if EXECUTION_CONTEXT == "notebook" else f"[link]{link}[/link]"
        )

        self._frame = (self._frame + 1) % len(self._loader_frames)

        self._progress.update(
            task_id=self._task,
            description="Preparing"
            if scheduler_combined_process_state is None
            else combined_state_to_description[scheduler_combined_process_state],
            completed={
                None: 0,
                CombinedProcessStateEnum.instance_queued: 1,
                CombinedProcessStateEnum.instance_starting: 2,
                CombinedProcessStateEnum.instance_running: 3,
                CombinedProcessStateEnum.downloading: 4,
                CombinedProcessStateEnum.ready: 5,
                CombinedProcessStateEnum.stopping: 0,
                CombinedProcessStateEnum.stopped: 0,
                CombinedProcessStateEnum.error: 0,
            }[scheduler_combined_process_state],
        )

        def _table(rows: tuple[tuple[RenderableType, RenderableType], ...]) -> rich.table.Table:
            t = rich.table.Table(
                box=None,
                show_header=False,
                show_footer=False,
                collapse_padding=True,
                pad_edge=False,
                show_edge=False,
                expand=True,
            )
            t.add_column()
            t.add_column(width=20)

            for k, v in rows:
                t.add_row(k, v)

            return t

        config_table = _table(config)
        costing_table = _table(costing)

        table = rich.table.Table.grid(expand=True)
        table.add_column()
        table.add_column()
        table.add_row(config_table, rich.align.Align.right(costing_table))

        hostname_line = None
        if self._extra_link:
            formatted_extra_link = (
                current_loader_frame if self._extra_link == "..." else f"[link]{self._extra_link}[/link]"
            )
            hostname_line = f"[bold green]{self._extra_link_title}: [/bold green]{formatted_extra_link}"

        return rich.panel.Panel(
            rich.console.Group(
                "",
                *(() if not hostname_line else (hostname_line,)),
                f"[bold green]Details: [/bold green]{linked_details_link}",
                "",
                self._progress.get_renderable(),
                "",
                env_line,
                table,
                "",
                *(() if self._trailer is None else (self._trailer,)),
            ),
            title=self._title,
            width=self._width,
        )


class RichClusterWidget(ClusterWidget):
    """A Rich renderable showing cluster status."""

    n_workers: int
    _cluster_details: Mapping[str, Any] | None
    _progress: rich.progress.Progress

    def __init__(
        self,
        n_workers: int = 0,
        transient: bool = False,
        console: rich.console.Console | None = None,
        *,
        server: str | None,
        workspace: str | None,
    ):
        """Set up the renderable widget."""
        self.server = server
        self.workspace = workspace
        self._cluster_details = None
        self._final_update = None
        self._loader_frames = ["...", " ..", "  .", "   ", ".  ", ".. "]
        self._frame = 0
        self.last_updated_utc = datetime.datetime.now(datetime.timezone.utc)
        if console:
            self.console = console
        else:
            self.console = rich.console.Console()
            self.console.size = (CONSOLE_WIDTH, BASE_CONSOLE_HEIGHT)

        self._progress = progress = rich.progress.Progress(
            "{task.description}",
            rich.progress.BarColumn(complete_style="progress.remaining"),
            rich.progress.TextColumn("[progress.percentage]{task.completed}"),
        )
        self._error_progress = error_progress = rich.progress.Progress(
            "{task.description}",
            rich.progress.BarColumn(complete_style="red", finished_style="red"),
            rich.progress.TextColumn("[progress.percentage]{task.completed}"),
        )
        self._provision_task = progress.add_task("Provisioning", total=n_workers)
        self._boot_task = progress.add_task("Booting instance", total=n_workers)

        self._downloading_extracting_task = progress.add_task("Downloading environment", total=n_workers)
        self._ready_task = progress.add_task("Ready", total=n_workers)
        self._stopping_task = progress.add_task("Stopping", total=n_workers)
        self._stopped_task = progress.add_task("Stopped", total=n_workers)

        # In order to make the bar red for errors, the error progress bar is a different instance
        # of rich.progress.Progress.
        # But we still want this bar aligned with the others, since rich doesn't know these two groups
        # are related, it doesn't automatically know how much right-padding to add
        # after the word "Error", so we calculate that ourselves here.
        max_len = max(len(t.description) for t in progress.tasks)
        self._error_task = error_progress.add_task(
            "Error" + " " * (max_len - len("Error")), total=n_workers, visible=False
        )

        # Calls _get_renderable, so the progress bar must be set up first.
        self.live = rich.live.Live(
            transient=transient,
            console=self.console,
            get_renderable=self._get_renderable,
        )

    def start(self):
        """Start the live instance."""
        self.live.start(refresh=False)

    def stop(self):
        """Stop the live instance."""
        self.live.stop()

    def __enter__(self) -> RichClusterWidget:
        """Enter a live-updating context.

        Example
        -------
        with RichClusterWidget(n_workers) as w:
            # do stuff
        """
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the live-updating context and reset the display ID.

        Keep the widget around for user inspection if there was a cluster creation
        error, otherwise remove it.
        """
        if exc_type == ClusterCreationError and self.live.transient:
            self.live.transient = False
        self.stop()

    def update(
        self,
        cluster_details: Mapping[str, Any] | None,
        logs,
        *args,
        final_update=None,
        **kwargs,
    ) -> None:
        """Update cluster data.

        Note: this does not trigger any refreshing, that is handled by the Live
        instance, which does it periodically.
        """
        self._cluster_details = cluster_details

        # track when the widget last received new data about the cluster
        # (which is less often than the widget renders)
        self.last_updated_utc = datetime.datetime.now(datetime.timezone.utc)

        if final_update:
            self._final_update = final_update

        # We explicitly refresh to make sure updated info is shown.
        # (Bad timing can lead auto-refresh to not show the update before we stop.)
        self.live.refresh()

    def _ipython_display_(self) -> None:
        """Render in a notebook context.

        Note: this is *not* called in an IPython terminal context. Instead,
        _repr_mimebundle_ is used in the IPython terminal.
        """
        self.console.print(self._get_renderable(), new_line_start=True)

    def __rich_console__(
        self, console: rich.console.Console, options: rich.console.ConsoleOptions
    ) -> rich.console.RenderResult:
        """Implement the Rich console interface.

        In particular, this is used in ``_repr_mimebundle_`` to display to an IPython
        terminal.
        """
        yield self._get_renderable()

    def _repr_mimebundle_(self, include: Iterable[str], exclude: Iterable[str], **kwargs) -> Dict[str, str]:
        """Display the widget in an IPython console context.

        This is adapted from the code in `rich.jupyter.JupyterMixin`. We can't
        use that mixin because it doesn't allow you to specify your own console
        (instead using the global one). We want our own console because we
        manually set the size to not take up the full terminal.
        """
        console = self.console
        segments = list(console.render(self, console.options))  # type: ignore
        text = console._render_buffer(segments)  # Unfortunate private member access...
        data = {"text/plain": text}
        if include:
            data = {k: v for (k, v) in data.items() if k in include}
        if exclude:
            data = {k: v for (k, v) in data.items() if k not in exclude}
        return data

    def _get_renderable(self) -> rich.console.RenderableType:
        """Construct the rendered layout."""
        progress = self._progress
        error_progress = self._error_progress
        current_loader_frame = self._loader_frames[self._frame]
        if self._cluster_details:
            desired_workers = self._cluster_details["desired_workers"]
            n_workers = len(jmespath.search("workers[*]", self._cluster_details) or [])
            scheduler_status = self._cluster_details["scheduler"]["current_state"]["state"]
            scheduler_ready = ProcessStateEnum(scheduler_status) == ProcessStateEnum.started
            if not scheduler_ready:
                scheduler_status += current_loader_frame

            dashboard_address = (
                jmespath.search("scheduler.dashboard_address", self._cluster_details) or None
                if scheduler_ready
                else None
            )

            scheduler_instance_type, worker_instance_types = get_instance_types(self._cluster_details)
            region = self._cluster_details["cluster_options"]["region_name"]
            zone = self._cluster_details["cluster_options"]["zone_name"]
            zone_desc = f" ({zone})" if zone else ""
            cluster_name = self._cluster_details["name"]
            env_name = self._cluster_details["senv_alias"]["name"]
            if env_name.startswith("package-sync-"):
                env_name = ""

            statuses = get_worker_statuses(self._cluster_details)
            progress.update(
                self._provision_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.instance_queued]
                + statuses[CombinedProcessStateEnum.instance_starting],
            )
            progress.update(
                self._downloading_extracting_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.downloading],
            )
            progress.update(
                self._boot_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.instance_running],
            )
            progress.update(
                self._ready_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.ready],
            )
            progress.update(
                self._stopping_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.stopping],
            )
            progress.update(
                self._stopped_task,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.stopped],
            )
            error_progress.update(
                self._error_task,
                visible=statuses[CombinedProcessStateEnum.error] > 0,
                total=n_workers,
                completed=statuses[CombinedProcessStateEnum.error],
            )
        else:
            scheduler_status = current_loader_frame
            dashboard_address = None
            scheduler_instance_type = current_loader_frame
            worker_instance_types = Counter()
            region = current_loader_frame
            zone_desc = ""
            cluster_name = ""
            env_name = ""
            desired_workers = ""
            n_workers = []

        show_worker_states = bool(desired_workers or n_workers)

        dashboard_label = (
            f"[link={dashboard_address}]{dashboard_address}[/link]" if dashboard_address else current_loader_frame
        )
        if any(k for k, v in worker_instance_types.items()):
            worker_instance_types_label = ", ".join(
                f"{k or 'Unknown'} ({v:,})" for k, v in worker_instance_types.items()
            )
        else:
            worker_instance_types_label = current_loader_frame

        worker_line = (
            f"""
            [bold green]Workers:[/bold green]   {worker_instance_types_label or current_loader_frame}
            """
            if show_worker_states
            else ""
        )

        config = dedent(f"""
            [bold green]Region:[/bold green] {region}{zone_desc}

            [bold green]Scheduler:[/bold green] {scheduler_instance_type or current_loader_frame}
            {worker_line}
            [bold green]Workers Requested:[/bold green] {desired_workers}
            """)

        # Prevent environment name from line wrapping
        if len(env_name) > 31:
            env_name = env_name[:28] + "..."

        env_line = (
            f"""
            [bold green]Env:[/bold green] {env_name}
            """
            if env_name
            else ""
        )

        status = dedent(f"""
            [bold green]Name:[/bold green] {cluster_name}
            {env_line}
            [bold green]Scheduler Status:[/bold green] {scheduler_status}

            [bold green]Dashboard:[/bold green] {dashboard_label}""")

        """Define the layout."""
        layout = rich.layout.Layout(name="root")
        self._frame = (self._frame + 1) % len(self._loader_frames)

        if show_worker_states:
            if self._final_update is None:
                progress_height = WAITING_PROGRESS_HEIGHT
                console_size = (CONSOLE_WIDTH, WAITING_CONSOLE_HEIGHT)
            else:
                progress_height = DONE_PROGRESS_HEIGHT
                console_size = (CONSOLE_WIDTH, DONE_CONSOLE_HEIGHT)
        else:
            progress_height = 0
            console_size = (CONSOLE_WIDTH, BASE_CONSOLE_HEIGHT)

        self.console.size = console_size

        if self._cluster_details is None:
            link = ""
        else:
            link = get_details_url(self.server, self.workspace, self._cluster_details["id"])
            assert link is not None  # typechecker, go away please

        linked_details_link = (
            f"[link={link}]{link}[/link]" if EXECUTION_CONTEXT == "notebook" else f"[link]{link}[/link]"
        )

        layout_panels = [
            rich.layout.Layout(
                rich.panel.Panel(
                    rich.align.Align.center(linked_details_link),
                    title="[bold green frame]Coiled Cluster",
                ),
                name="header",
                size=3,
            ),
            rich.layout.Layout(name="body", size=11),
        ]

        if show_worker_states:
            layout_panels.append(rich.layout.Layout(name="progress", size=progress_height))

        layout.split(*layout_panels)
        layout["body"].split_row(
            rich.layout.Layout(name="overview"),
            rich.layout.Layout(name="configuration"),
        )

        time = self.last_updated_utc.astimezone(LOCAL_TIMEZONE).strftime("%Y/%m/%d %H:%M:%S %Z")
        if show_worker_states:
            if self._final_update is None:
                layout["progress"].update(
                    rich.panel.Panel(
                        rich.align.Align.center(
                            rich.console.Group(progress.get_renderable(), error_progress.get_renderable()),
                            vertical="middle",
                        ),
                        title=f"Dask Worker States ({time})",
                    )
                )
            else:
                layout["progress"].update(
                    rich.panel.Panel(
                        rich.align.Align.center(self._final_update, vertical="middle"),
                        title=f"({time})",
                    )
                )
        layout["body"]["overview"].update(rich.panel.Panel(status, title="Overview"))
        layout["body"]["configuration"].update(rich.panel.Panel(config, title="Configuration"))
        return layout
