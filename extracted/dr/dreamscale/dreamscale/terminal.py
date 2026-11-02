from __future__ import annotations

import atexit
import re
import time
from collections.abc import Callable
from contextlib import contextmanager, suppress
from typing import Any

from rich.console import Console
from rich.status import Status
from rich.text import Text

from dreamscale.policy.types import LatencyStats, RunResult


class ProgressPrinter:
    def __init__(
        self,
        *,
        console: Console | None = None,
        clock: Callable[[], float] = time.monotonic,
        show_header: bool = True,
    ) -> None:
        self._console = console or Console(highlight=False, soft_wrap=True)
        self._clock = clock
        self._header_printed = not show_header
        self._status: Status | None = None
        self._status_line: _LiveStatusLine | None = None
        # Start of the current compute wait, so the ready line can say how long it took.
        self._wait_started_at: float | None = None
        atexit.register(self.close)

    def __call__(self, message: str) -> None:
        self._print_header_once()
        for line in str(message).splitlines():
            self._print_line(line.rstrip())

    @property
    def console(self) -> Console:
        """The console this printer draws on, header printed, any live status cleared."""
        self._print_header_once()
        self._stop_status()
        return self._console

    def _print_header_once(self) -> None:
        if self._header_printed:
            return
        self._console.print(Text("Dreamscale", style="bold #00ffd1"))
        self._header_printed = True

    def _print_line(self, line: str) -> None:
        line = _compact_compute_line(line)
        if not line:
            self._stop_status()
            self._console.print("")
            return
        if line.startswith("  ") and ":" in line:
            self._stop_status()
            self._console.print(_detail_text(line))
            return
        if line.startswith("x ") or line.startswith("X ") or line.startswith("! "):
            self._stop_status()
            self._console.print(Text(line, style="bold red"))
            return
        if line.startswith("✗ "):
            self._stop_status()
            self._console.print(Text(line, style="bold red"))
            return
        line = self._track_wait(line)
        if _is_live_status_line(line) and self._console.is_terminal:
            self._update_status(line)
            return
        self._stop_status()
        self._console.print(_line_text(line))

    def _track_wait(self, line: str) -> str:
        match = _ELAPSED_LINE_RE.fullmatch(line)
        if match and match["label"] in _WAIT_LABELS:
            elapsed = int(match["elapsed"])
            if self._wait_started_at is None:
                self._wait_started_at = self._clock() - elapsed
            if elapsed == 0 and not self._console.is_terminal:
                # Redirected output prints each line once; a frozen "0s elapsed" would
                # read as the whole wait. The ready line reports the duration instead.
                return f"{match['label'].rstrip('…')}…{match['suffix']}"
            return line
        if line == "✓ Compute ready" and self._wait_started_at is not None:
            waited = int(max(0.0, self._clock() - self._wait_started_at))
            self._wait_started_at = None
            return f"{line} after {waited}s" if waited else line
        return line

    def _update_status(self, line: str) -> None:
        renderable = _LiveStatusLine.from_line(
            line,
            style=_line_style(line),
            clock=self._clock,
        )
        if self._status_line is not None:
            renderable.continue_clock(self._status_line)
        self._status_line = renderable
        if self._status is None:
            self._status = self._console.status(
                renderable,
                spinner="line",
                spinner_style="bold cyan",
                refresh_per_second=12.5,
            )
            self._status.start()
            return
        self._status.update(renderable)

    def _stop_status(self) -> None:
        if self._status is None:
            return
        with suppress(Exception):
            self._status.stop()
        self._status = None
        self._status_line = None

    def close(self) -> None:
        self._stop_status()


def make_progress_printer(
    *,
    console: Console | None = None,
    clock: Callable[[], float] = time.monotonic,
    show_header: bool = True,
) -> Callable[[str], None]:
    return ProgressPrinter(console=console, clock=clock, show_header=show_header)


@contextmanager
def compute_progress(
    callback: Callable[[str], None],
    *,
    clock: Callable[[], float] = time.monotonic,
    ready_message: str = "Compute is ready.",
):
    """Render default readiness output and close its animation on every exit.

    Custom callbacks retain the original messages; their caller owns their
    lifecycle. Existing shared renderers remain usable after the wait ends.
    """
    owned = callback is print
    progress = ProgressPrinter(clock=clock, show_header=False) if owned else callback
    try:
        yield progress
        if owned:
            progress(ready_message)
    finally:
        if isinstance(progress, ProgressPrinter):
            progress.close()
            if owned:
                atexit.unregister(progress.close)


def _compact_compute_line(line: str) -> str:
    labels = {
        "Starting your compute": "Starting compute",
        "Waiting for your compute to become available": "Waiting for compute",
        "Restoring archived model storage": "Restoring model storage",
    }
    match = _ELAPSED_LINE_RE.fullmatch(line)
    if match and match.group("label") in labels:
        estimate = re.search(r"\(estimate (\d+)s(?:; model load can take longer)?\)",
                             match.group("suffix"))
        queue = re.search(r"position (\d+) in the queue(?: \(about (\d+)s\))?",
                          match.group("suffix"))
        suffix = f" · estimate ~{_minutes(estimate[1])}m" if estimate else ""
        if queue:
            about = f", about ~{_minutes(queue[2])}m" if queue[2] else ""
            suffix += f" · position {queue[1]} in the queue{about}"
        return f"{labels[match['label']]}: {match['elapsed']}s elapsed{suffix}"
    if line.startswith("Compute is ready"):
        return "✓ Compute ready"
    if line == "Connection interrupted while compute starts; retrying this session…":
        return "Reconnecting to compute…"
    retry = re.fullmatch(r"Retrying compute allocation in (\d+)s\.", line)
    if retry:
        return f"Waiting for compute: 0s elapsed · retry after {retry[1]}s"
    return line


def _minutes(seconds: str) -> str:
    return f"{int(seconds) / 60:.1f}".rstrip("0").rstrip(".")


def describe_resolved_policy(config: Any) -> str:
    backend = getattr(config, "backend", "unknown")
    rtc = getattr(config, "rtc", "off")
    rtc_contract = getattr(config, "rtc_contract", None)
    rtc_value = rtc
    if rtc == "on" and rtc_contract:
        # The kind, named as --rtc takes it (train_time / inference_time), when known.
        mode = getattr(config, "effective_rtc_mode", None)
        rtc_value = f"{mode if mode in ('inference_time', 'train_time') else rtc} ({rtc_contract})"
    parts = [
        f"backend={backend}",
        f"rtc={rtc_value}",
        f"calibration={getattr(config, 'calibration', 'default')}",
        f"control={getattr(config, 'control', 'balanced')}",
    ]
    action_hz = getattr(config, "action_hz", None)
    if action_hz is not None:
        parts.append(f"action_hz={float(action_hz):g}Hz")
    chunk_size = getattr(config, "chunk_size", None)
    if chunk_size is not None:
        parts.append(f"chunk={int(chunk_size)}")
    return ", ".join(parts)


def describe_runtime_summary(
    *,
    transport_mode: str | None,
    runtime_stats: Any,
    calibration_profile: Any | None,
) -> str | None:
    if runtime_stats is None:
        return None
    requests = int(getattr(runtime_stats, "requests_submitted", 0) or 0)
    chunks = int(getattr(runtime_stats, "chunks_received", 0) or 0)
    calibration_samples = int(getattr(runtime_stats, "calibration_samples", 0) or 0)
    rtc_requests = int(getattr(runtime_stats, "rtc_requests", 0) or 0)
    rtc_reference_chunks = int(
        getattr(runtime_stats, "rtc_reference_chunks", 0) or 0
    )
    rtc_reference_actions = int(
        getattr(runtime_stats, "rtc_reference_actions", 0) or 0
    )
    rtc_delay_samples = int(
        getattr(runtime_stats, "rtc_eligible_delay_samples", 0) or 0
    )
    rtc_delay_steps = int(getattr(runtime_stats, "rtc_merge_delay_steps", 0) or 0)
    rtc_overcoverage_steps = int(
        getattr(runtime_stats, "rtc_overcoverage_steps", 0) or 0
    )
    rtc_undercoverage_steps = int(
        getattr(runtime_stats, "rtc_undercoverage_steps", 0) or 0
    )
    rtc_hold_gap_steps = int(
        getattr(runtime_stats, "rtc_hold_or_starvation_gap_steps", 0) or 0
    )
    underruns = int(getattr(runtime_stats, "underruns", 0) or 0)
    stale_chunks = int(getattr(runtime_stats, "stale_chunks_dropped", 0) or 0)
    hold_position = int(getattr(runtime_stats, "hold_position_count", 0) or 0)
    if (
        requests <= 0
        and chunks <= 0
        and calibration_samples <= 0
        and rtc_requests <= 0
        and underruns <= 0
        and stale_chunks <= 0
        and hold_position <= 0
    ):
        return None
    parts = []
    if transport_mode:
        parts.append(f"transport={transport_mode}")
    parts.extend(
        [
            f"requests={requests}",
            f"chunks={chunks}",
            f"rtc_requests={rtc_requests}",
            f"underruns={underruns}",
            f"stale_chunks={stale_chunks}",
            f"hold_position={hold_position}",
        ]
    )
    if rtc_requests > 0:
        parts.extend(
            [
                f"rtc_reference_chunks={rtc_reference_chunks}",
                f"rtc_reference_actions={rtc_reference_actions}",
            ]
        )
        parts.append(f"rtc_delay_samples={rtc_delay_samples}")
        if rtc_delay_samples > 0:
            parts.append(
                f"rtc_mean_delay_steps={rtc_delay_steps / rtc_delay_samples:.2f}"
            )
        parts.extend(
            [
                f"rtc_overcoverage_steps={rtc_overcoverage_steps}",
                f"rtc_undercoverage_steps={rtc_undercoverage_steps}",
                f"rtc_hold_gap_steps={rtc_hold_gap_steps}",
            ]
        )
    latency_health = getattr(calibration_profile, "latency_health", None)
    if latency_health:
        parts.append(f"latency={latency_health}")
    confidence = getattr(calibration_profile, "calibration_confidence", None)
    if confidence:
        parts.append(f"calibration_confidence={confidence}")
    calibration_usage = getattr(
        calibration_profile,
        "runtime_calibration_usage",
        None,
    )
    if calibration_usage:
        parts.append(f"calibration_usage={calibration_usage}")
    return ", ".join(parts)


def format_run_summary(result: RunResult) -> tuple[str, ...]:
    """Format one run without inferring task or physical-execution success."""
    if result.stop_reason == "act_callback":
        lines = ["Run ended: act callback requested stop."]
    elif result.stop_reason == "interrupted":
        lines = ["Run interrupted: partial results retained."]
    elif result.stop_reason == "error":
        lines = [f"Run failed: {result.error_type or 'error'}; partial results retained."]
    else:
        limit = result.max_actions if result.max_actions is not None else result.actions
        lines = [f"Run ended: {limit}-step limit reached."]

    lines.append(
        f"  control: {result.actions} control steps in {result.elapsed_s:.2f}s"
    )
    if result.startup_wait_ms or result.startup_holds or result.execution_underruns:
        lines.append(
            f"  startup: {result.startup_wait_ms:.1f}ms; {result.startup_holds} hold steps; "
            f"execution underruns: {result.execution_underruns} steps"
        )
    if result.action_attempts > result.actions:
        lines.append(f"  dispatch: {result.action_attempts - result.actions} unconfirmed attempts")
    if result.loop_cleanup_error_type:
        lines.append(f"  loop cleanup unconfirmed: {result.loop_cleanup_error_type}")
    policy_line = f"  policy: {result.policy_calls} responses"
    policy_latency = _latency_range(result.timing.policy_response_ms)
    if policy_latency is not None:
        policy_line += f"; {policy_latency}"
    lines.append(policy_line)

    data_plane_latency = _latency_range(result.timing.data_plane_rtt_ms)
    if data_plane_latency is not None:
        lines.append(f"  data-plane RTT: {data_plane_latency}")

    worker_parts = []
    for label, stats in (
        ("queue", result.timing.worker_queue_ms),
        ("preprocess", result.timing.worker_preprocess_ms),
        ("inference", result.timing.worker_inference_ms),
        ("postprocess", result.timing.worker_postprocess_ms),
    ):
        if (
            stats.samples > 0
            and stats.p50_ms is not None
            and stats.p95_ms is not None
        ):
            worker_parts.append(
                f"{stats.p50_ms:.1f}ms {label} p50 / {stats.p95_ms:.1f}ms p95"
            )
    if worker_parts:
        lines.append(f"  worker: {'; '.join(worker_parts)}")

    lines.append(f"  buffer: {result.underruns} underruns")
    route_parts = [
        value
        for value in (
            result.model,
            result.region,
            _transport_label(result.transport_mode, result.fallback_reason),
        )
        if value
    ]
    if route_parts:
        route = " · ".join(route_parts)
        if result.fallback_reason:
            route += f" ({result.fallback_reason})"
        lines.append(f"  route: {route}")
    return tuple(lines)


def _latency_range(stats: LatencyStats) -> str | None:
    if stats.samples <= 0 or stats.p50_ms is None or stats.p95_ms is None:
        return None
    return f"{stats.p50_ms:.1f}ms p50 / {stats.p95_ms:.1f}ms p95"


def _transport_label(
    transport_mode: str | None,
    fallback_reason: str | None,
) -> str | None:
    if transport_mode in ("quic", "quic_punch"):
        return "QUIC"
    if transport_mode == "relay":
        return "HTTPS fallback" if fallback_reason else "HTTPS relay"
    if transport_mode == "wss_tunnel":
        return "WebSocket"
    return None


_WAIT_LABELS = frozenset({
    "Starting compute", "Waiting for compute", "Restoring model storage",
})

# The suffix may follow a space or a comma (the queue line: "…: 0s elapsed, position 1 in
# the queue"); either way the line ticks live.
_ELAPSED_LINE_RE = re.compile(
    r"^(?P<label>.+): (?P<elapsed>\d+)s elapsed(?P<suffix>(?:[ ,].*)?)$"
)


class _LiveStatusLine:
    def __init__(
        self,
        *,
        label: str,
        suffix: str,
        initial_elapsed_s: int | None,
        style: str | None,
        clock: Callable[[], float],
    ) -> None:
        self._label = label
        self._suffix = suffix
        self._initial_elapsed_s = initial_elapsed_s
        self._style = style
        self._clock = clock
        self._started_at = clock()

    @classmethod
    def from_line(
        cls,
        line: str,
        *,
        style: str | None,
        clock: Callable[[], float],
    ) -> _LiveStatusLine:
        match = _ELAPSED_LINE_RE.match(line)
        if match is None:
            return cls(
                label=line,
                suffix="",
                initial_elapsed_s=None,
                style=style,
                clock=clock,
            )
        return cls(
            label=match.group("label"),
            suffix=match.group("suffix"),
            initial_elapsed_s=int(match.group("elapsed")),
            style=style,
            clock=clock,
        )

    def continue_clock(self, previous: _LiveStatusLine) -> None:
        # Heartbeats contain rounded seconds. Resetting the local origin on
        # each one makes a second linger or jump whenever a heartbeat arrives.
        if (
            self._label == previous._label
            and self._initial_elapsed_s is not None
            and previous._initial_elapsed_s is not None
        ):
            self._started_at = previous._started_at
            self._initial_elapsed_s = previous._initial_elapsed_s

    def text(self) -> Text:
        if self._initial_elapsed_s is None:
            return Text(self._label, style=self._style)
        elapsed = self._initial_elapsed_s + int(max(0.0, self._clock() - self._started_at))
        return Text(f"{self._label}: {elapsed}s elapsed{self._suffix}", style=self._style)

    def __rich_console__(self, _console: Console, _options: Any) -> Any:
        yield self.text()

    def __str__(self) -> str:
        return self.text().plain


def _is_live_status_line(line: str) -> bool:
    normalized = line.lower()
    return normalized.startswith((
        "homing…", "connecting robot…", "starting compute", "restoring model storage",
        "reconnecting to compute…", "preparing task…",
        "checking prediction…", "running ·", "disconnecting…", "returning home…",
        "building · step", "reading ",
        # dreamscale train and datasets: the upload bar and a run's phases.
        "uploading ━", "uploading ─", "queued", "checking data", "converting data",
        "starting on ", "training · step", "saving · step",
    )) or any(
        token in normalized
        for token in (
            "waiting",
            "starting your compute",
            "calibrating",
            "retrying compute allocation",
        )
    )


def _line_style(line: str) -> str | None:
    lowered = line.lower()
    if line.startswith("✓ "):
        return "green"
    if line.startswith("Sign in to Dreamscale"):
        return "bold"
    if any(
        token in lowered
        for token in (
            "warning",
            "fallback",
            "unavailable",
            "low balance",
            "traffic is high",
            "no usable samples",
            "compute availability",
        )
    ):
        return "yellow"
    if any(
        token in lowered
        for token in (
            "ready",
            "connected",
            "inference started",
            "calibration complete",
            "compute is ready",
        )
    ):
        return "green"
    if any(token in lowered for token in ("runtime selected", "run summary")):
        return "dim"
    return None


def _line_text(line: str) -> Text:
    if line.startswith("  https://") or line.startswith("https://"):
        text = Text()
        prefix = "  " if line.startswith("  ") else ""
        if prefix:
            text.append(prefix)
        text.append(line.strip(), style="bold cyan underline")
        return text
    if line.startswith("Code: "):
        text = Text()
        text.append("Code:", style="dim")
        text.append(" ")
        text.append(line.removeprefix("Code: "), style="bold cyan")
        return text
    text = Text()
    text.append(line, style=_line_style(line))
    return text


def _detail_text(line: str) -> Text:
    stripped = line.strip()
    label, _, value = stripped.partition(":")
    label_style = {
        "cause": "yellow",
        "fix": "green",
    }.get(label, "dim")
    text = Text("  ")
    text.append(f"{label}:", style=f"bold {label_style}")
    if value:
        text.append(value)
    return text
