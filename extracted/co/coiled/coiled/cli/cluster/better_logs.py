import re
import time
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

import click
from rich.console import Console
from rich.errors import MarkupError

import coiled

from ..utils import CONTEXT_SETTINGS
from .utils import find_cluster

COLORS = [
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
]


@click.command(
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--cluster",
    default=None,
    help="Cluster for which to show logs, default is most recent",
)
@click.option(
    "--no-scheduler",
    default=False,
    is_flag=True,
    help="Don't include scheduler logs",
)
@click.option(
    "--workers",
    default="all",
    help=(
        "All worker logs included by default, specify 'none' or "
        "comma-delimited list of names, states, or internal IP addresses"
    ),
)
@click.option(
    "--label",
    default="private_ip_address",
    type=click.Choice(
        ["private_ip_address", "name", "id", "public_ip_address", "none"],
        case_sensitive=False,
    ),
)
@click.option(
    "--system",
    default=False,
    is_flag=True,
    help="Just show system logs",
)
@click.option(
    "--combined",
    default=False,
    is_flag=True,
    help="Show combined system and dask logs",
)
@click.option(
    "--tail",
    default=False,
    is_flag=True,
    help="Keep tailing logs",
)
@click.option(
    "--since",
    default=None,
    help="By default will show logs from start of cluster (or 30s ago if tailing)",
)
@click.option(
    "--until",
    default=None,
    help="Show logs up to and including this time, by default will go through present time.",
)
@click.option(
    "--filter",
    default=None,
    help="Filter log messages",
)
@click.option(
    "--color/--no-color",
    default=True,
    is_flag=True,
    help="Use for color in logs",
)
@click.option(
    "--show-all-timestamps",
    default=False,
    is_flag=True,
    help="Prepend datetime to all log messages",
)
@click.option(
    "--interval",
    default=3,
    help="Tail polling interval",
)
@click.argument(
    "cluster_arg",
    default=None,
    required=False,
)
def better_logs_cli(
    account: Optional[str],
    cluster: Optional[str],
    no_scheduler: bool,
    workers: str,
    label: str,
    system: bool,
    combined: bool,
    tail: bool,
    interval: int,
    since: Optional[str],
    until: Optional[str],
    color: bool,
    filter: Optional[str],
    show_all_timestamps: bool,
    cluster_arg: Optional[str],
):
    dask = not system or combined
    system = system or combined
    label = label.lower()

    if tail and until:
        raise click.ClickException("You can't use --until when tailing logs.")

    cluster = cluster or cluster_arg

    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster or "")

    instance_labels_dict = make_instance_labels(
        label=label,
        no_scheduler=no_scheduler,
        scheduler_id=cluster_info.get("scheduler", {}).get("instance", {}).get("id"),
        workers=workers,
        workers_info=cluster_info["workers"],
    )

    console = Console(force_terminal=color)

    cluster_id = cluster_info["id"]
    cluster_name = cluster_info["name"]
    cluster_state = cluster_info["current_state"]["state"]

    if tail and cluster_state in (
        "stopped",
        "error",
    ):
        tail = False
        console.print(f"[red]Cluster state is {cluster_state} so not tailing.[/red]")

    if (workers or not no_scheduler) and not instance_labels_dict:
        # exit here if there are no instances, otherwise passing empty list to
        # coiled.better_cluster_logs will result in pulling logs for all instances
        console.print("[red]no instances match specified filters[/]")
        return

    console.print(f"=== Logs for {cluster_name} ({cluster_id}) ===\n")
    better_logs(
        cluster_id=cluster_id,
        instance_labels_dict=instance_labels_dict,
        show_label=label != "none",
        show_all_instances=workers == "all" and not no_scheduler,
        console=console,
        dask=dask,
        system=system,
        tail=tail,
        interval=interval,
        since=since,
        until=until,
        filter=filter,
        show_all_timestamps=show_all_timestamps,
        color=color,
    )


def make_instance_labels(label, no_scheduler, scheduler_id, workers, workers_info):
    # instance ID's for which to show logs, key maps to label to use
    instances = {}
    if not no_scheduler and scheduler_id:
        instances[scheduler_id] = {
            "label": "scheduler" if label != "none" else "",
            "color": COLORS[-1],
        }

    def worker_label(worker: dict):
        if label == "none":
            return ""
        return (
            worker.get("name", str(worker["instance"]["id"]))
            if label == "name"
            else worker["instance"].get(label, str(worker["instance"]["id"]))
        )

    # TODO when tailing "all" workers, this won't include workers that appear after we start
    #  (addressing this is future enhancement)

    if workers:
        worker_attrs_to_match = workers.split(",")

        def filter_worker(worker):
            if worker.get("name") and worker["name"] in worker_attrs_to_match:
                # match on name
                return True
            elif (
                worker.get("instance", {}).get("private_ip_address")
                and worker["instance"]["private_ip_address"] in worker_attrs_to_match
            ):
                # match on private IP
                return True
            elif (
                worker.get("current_state", {}).get("state")
                and worker["current_state"]["state"] in worker_attrs_to_match
            ):
                # match on state
                return True

            return False

        instances.update({
            worker["instance"]["id"]: dict(label=worker_label(worker), color=COLORS[idx % len(COLORS)])
            for idx, worker in enumerate(workers_info)
            if worker.get("instance") and (workers == "all" or filter_worker(worker))
        })

    return instances


def better_logs(
    *,
    cluster_id: int,
    instance_labels_dict: dict,
    show_label: bool,
    show_all_instances: bool,
    console=None,
    color: bool = True,
    dask: bool = True,
    system: bool = False,
    tail: bool = False,
    tail_max_times: Optional[int] = None,
    interval: int = 3,
    since: Optional[str] = None,
    until: Optional[str] = None,
    filter: Optional[str] = None,
    show_timestamp: bool = True,
    show_all_timestamps: bool = False,
    start_sentinel: str = "",
    stop_sentinel: str = "",
):
    console = console or Console(force_terminal=color)

    from_timestamp = ts_ms_from_string(since)
    until_timestamp = ts_ms_from_string(until)
    last_events = set()

    if tail and not from_timestamp:
        # for tail, start with logs from 30s ago if start isn't specified
        current_ms = int(time.time_ns() // 1e6)
        from_timestamp = current_ms - (30 * 1000)

    waiting_for_start_sentinel = bool(start_sentinel)

    while True:
        events = coiled.better_cluster_logs(
            cluster_id=cluster_id,
            # function returns all instances if none specified, we'll use that
            # in order to not exclude instances that show up while tailing
            instance_ids=None if show_all_instances else list(instance_labels_dict.keys()),
            dask=dask,
            system=system,
            since_ms=from_timestamp,
            until_ms=until_timestamp,
            filter=filter,
        )

        if last_events:
            events = [e for e in events if e["timestamp"] != from_timestamp or event_dedupe_key(e) not in last_events]

        if events:
            from_timestamp = events[-1]["timestamp"]
            last_events = {event_dedupe_key(e) for e in events if e["timestamp"] == from_timestamp}

            # filter using sentinels
            events, waiting_for_start_sentinel, found_stop_sentinel = filter_events(
                events, start_sentinel, stop_sentinel, waiting_for_start_sentinel
            )

            print_events(
                console=console,
                events=events,
                instances=instance_labels_dict,
                show_label=show_label,
                show_timestamp=show_timestamp,
                show_all_timestamps=show_all_timestamps,
                pretty=color,
            )

            if found_stop_sentinel:
                break

        if tail and (tail_max_times is None or tail_max_times > 0):
            # TODO stop tailing once cluster is stopped/errored (future MR)
            if tail_max_times:
                tail_max_times -= 1
            time.sleep(interval)
        elif not tail and until_timestamp is None and events:
            # if there's no specified end time of range, then it's possible there are more events we want after
            # the last event that we got back, so make another request with the updated start time of range
            continue
        else:
            break


def filter_events(events, start_sentinel, stop_sentinel, waiting_for_start_sentinel) -> Tuple[list, bool, bool]:
    found_stop_sentinel = False

    if start_sentinel or stop_sentinel:
        show_from = 0
        show_to = -1
        for i, event in enumerate(events):
            if waiting_for_start_sentinel and start_sentinel in event["message"]:
                waiting_for_start_sentinel = False
                # remove everything before (first) start sentinel
                # handle sentinel inside longer message
                pos = event["message"].find(start_sentinel)
                event["message"] = event["message"][pos + len(start_sentinel) :].strip()
                # if there's text after start sentinel, include event with sentinel, otherwise start at next
                # this is especially important because multiple lines can be joined into one event
                show_from = i if event["message"] else i + 1

            if show_to == -1 and stop_sentinel in event["message"]:
                found_stop_sentinel = True
                # remove everything after (first) stop sentinel
                # handle sentinel inside longer message
                pos = event["message"].find(stop_sentinel)
                event["message"] = event["message"][:pos].strip()
                # if there's text before stop sentinel, include event with sentinel, otherwise stop at previous
                show_to = i + 1 if event["message"] else i

            if not waiting_for_start_sentinel and show_to > -1:
                # minor optimization
                break
        if waiting_for_start_sentinel:
            events = []
        elif show_from or show_to > -1:
            events = events[show_from:show_to]

    return events, waiting_for_start_sentinel, found_stop_sentinel


def event_dedupe_key(event):
    return f"{event['timestamp']}#{event['instance_id']}#{event['message']}"


def print_events(
    console,
    events: List[dict],
    instances: dict,
    pretty=True,
    show_label=True,
    show_timestamp=True,
    show_all_timestamps=False,
):
    pfunc = console.print if pretty else print
    for e in events:
        line = format_log_event(
            e,
            instances,
            pretty=pretty,
            show_label=show_label,
            show_timestamp=show_timestamp,
            show_all_timestamps=show_all_timestamps,
        )
        try:
            pfunc(line)
        except MarkupError:
            print(line)


def format_log_event(
    event: dict, instances: dict, pretty: bool, show_label: bool, show_timestamp: bool, show_all_timestamps: bool
) -> str:
    message = event["message"]

    if show_label:
        if event.get("instance_id") and event.get("instance_id") in instances:
            label = instances[event["instance_id"]]["label"]
            color = instances[event["instance_id"]]["color"]
        else:
            # we might not know about instance if it showed up while we're tailing all worker logs
            label = event.get("instance_id") or event.get("instance")
            color = COLORS[0]
    else:
        label = ""
        color = ""

    time_string = ""

    if show_timestamp and event.get("timestamp"):
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        t = datetime.utcfromtimestamp(event["timestamp"] / 1000)

        if show_all_timestamps or not message_has_timestamp(message, t):
            time_string = f"{t.strftime(time_format)} "

    # indent multiline log messages
    if "\n" in message:
        message = message.replace("\n", "\n  ")

    if label:
        formatted_label = f"[{color}]({label})[/{color}] \t" if pretty else f"({label}) \t"
    else:
        formatted_label = ""

    return f"{formatted_label}{time_string}{message}"


def message_has_timestamp(message: str, t: datetime):
    # naively check if timestamp already present in message by looking for year
    # if it's not in log message, then prepend
    if str(t.year) in message:
        return True


def ts_ms_from_string(timestring: Optional[str]) -> Optional[int]:
    # input can be
    #   int: timestamp (ms)
    #   string in ISO 8601 format
    #   string representing delta (e.g, "1h15m")

    if not timestring:
        return None

    if timestring.isnumeric():
        return int(timestring)

    delta_regex = re.compile(r"^((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?$")
    match = delta_regex.match(timestring)
    if match:
        match_parts = {key: int(val) for key, val in match.groupdict().items() if val}

        delta = timedelta(**match_parts)
        if delta:
            t = datetime.now(tz=timezone.utc) - delta
            return int(t.timestamp() * 1000)

    try:
        t = datetime.fromisoformat(timestring)
        # interpret as UTC if not specified (rather than local time)
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    else:
        return int(t.timestamp() * 1000)

    raise ValueError(
        f"Unable to convert '{timestring}' into a timestamp, you can use number (timestamp in ms), "
        f"ISO format, or delta such as 5m."
    )
