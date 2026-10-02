"""Process fan-out for replay: one child interpreter per work item."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, TextIO

from bitfab.replay import (
    ProcessLauncher,
    ReplayItem,
    ReplayItemFinishProgress,
    ReplayItemStartProgress,
    ReplayWorkItem,
    carried_over_progress_counts,
    failed_replay_item,
)
from bitfab.replay_branch import DbBranchOptions
from bitfab.replay_memory import (
    ReplayMemoryThrottle,
    process_rss_bytes,
    throttle_disabled_by_env,
)

CHILD_POLL_SECONDS = 5.0
CHILD_TIMEOUT_SECONDS = 2400.0
_CHILD_OUTPUT_TAIL_LINES = 20
_CHILD_OUTPUT_TAIL_BYTES = 64 * 1024


class ReplayChildCancelled(Exception):
    """Raised inside a worker thread when the batch is being torn down."""


def _reap(process: subprocess.Popen[str]) -> None:
    for step in (
        lambda: os.killpg(os.getpgid(process.pid), signal.SIGKILL),
        process.kill,
        lambda: process.communicate(timeout=CHILD_POLL_SECONDS),
    ):
        with contextlib.suppress(Exception):
            step()


def _output_tail(log_path: Path) -> str:
    try:
        with log_path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            handle.seek(max(0, handle.tell() - _CHILD_OUTPUT_TAIL_BYTES))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        return ""
    return "\n".join(text.strip().splitlines()[-_CHILD_OUTPUT_TAIL_LINES:]).strip()


def _surface_child_message(message_path: Path, stderr: TextIO) -> None:
    try:
        message = message_path.read_text(encoding="utf-8").strip()
    except OSError:
        return
    if message:
        print(message, file=stderr)


def _run_child(
    argv: list[str],
    env: dict[str, str],
    cancel: threading.Event,
    timeout_seconds: float,
    log_path: Path,
    throttle: ReplayMemoryThrottle | None = None,
    index: int = 0,
) -> int:
    # A child's output goes to a file, never a pipe the parent buffers: a
    # chatty replay would otherwise grow the parent by however much it
    # printed, times max_concurrency. Only a bounded tail is ever read back.
    with log_path.open("wb") as log:
        process = subprocess.Popen(
            argv,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        deadline = time.monotonic() + timeout_seconds
        while True:
            try:
                process.wait(timeout=CHILD_POLL_SECONDS)
                return process.returncode
            except subprocess.TimeoutExpired:
                pass
            if throttle is not None:
                resident = process_rss_bytes(process.pid)
                if resident is not None:
                    throttle.observe(index, resident)
            if cancel.is_set():
                _reap(process)
                raise ReplayChildCancelled()
            if time.monotonic() >= deadline:
                _reap(process)
                return -1


def _progress_item(server_item: dict[str, Any], attempt: int) -> dict[str, Any]:
    original_trace_id = server_item.get("originalTraceId") or server_item.get(
        "sourceTraceId"
    )
    original_span_id = server_item.get("originalSpanId") or server_item.get(
        "sourceSpanId"
    )
    return {
        "original_trace_id": original_trace_id,
        "original_span_id": original_span_id,
        "source_trace_id": original_trace_id,
        "source_span_id": original_span_id,
        "attempt": attempt,
    }


def build_process_launcher(
    *,
    registry_path: str,
    replay_args: Sequence[str],
    environ: Mapping[str, str],
    max_concurrency: int | None,
    on_item_start: Callable[[ReplayItemStartProgress], None] | None = None,
    on_item_finish: Callable[[ReplayItemFinishProgress], None] | None = None,
    timeout_seconds: float = CHILD_TIMEOUT_SECONDS,
    stderr: TextIO = sys.stderr,
    memory_throttle: bool = False,
) -> ProcessLauncher:
    """Build the launcher that runs each replay work item in its own process.

    The parent has already minted the experiment and the per-item correlation
    ids, so a child never starts a replay of its own: it is handed one item
    and returns it. ``environ`` must be the environment the PARENT was invoked
    with, captured before the registry module booted, or every child inherits
    a world the parent already claimed.
    """

    def launch(
        work_items: list[ReplayWorkItem],
        experiment_id: str | None,
        replayed_trace_ids: list[str],
        carried_over_items: Sequence[ReplayItem] = (),
        db_branch: DbBranchOptions | bool | None = None,
    ) -> list[ReplayItem]:
        if not work_items:
            return []
        total = len(work_items) + len(carried_over_items)
        workdir = Path(tempfile.mkdtemp(prefix="bitfab-replay-work-"))
        cancel = threading.Event()
        lock = threading.Lock()
        counts = carried_over_progress_counts(list(carried_over_items))
        results: dict[int, ReplayItem] = {}
        throttle = (
            ReplayMemoryThrottle()
            if memory_throttle and not throttle_disabled_by_env()
            else None
        )
        held_back = {"reported": False}

        def report_held_back(index: int, waited: float) -> None:
            if waited <= 0 or throttle is None:
                return
            with lock:
                if held_back["reported"]:
                    return
                held_back["reported"] = True
            budget_gib = throttle.child_budget_bytes / (1024**3)
            print(
                f"[replay] Low memory: holding children back (waited {waited:.0f}s, "
                f"budgeting {budget_gib:.1f} GiB each). "
                "BITFAB_REPLAY_MEMORY_THROTTLE=off disables this.",
                file=stderr,
            )

        def report_start(server_item: dict[str, Any], attempt: int) -> None:
            with lock:
                counts["started"] += 1
                snapshot = dict(counts)
            if on_item_start is None:
                return
            with contextlib.suppress(Exception):
                on_item_start(
                    ReplayItemStartProgress(
                        type="started",
                        experiment_id=experiment_id,
                        test_run_id=experiment_id,
                        started=snapshot["started"],
                        completed=snapshot["completed"],
                        total=total,
                        succeeded=snapshot["succeeded"],
                        errored=snapshot["errored"],
                        item=_progress_item(server_item, attempt),
                    )
                )

        def report_finish(item: ReplayItem) -> None:
            with lock:
                counts["completed"] += 1
                if item["error"] is None:
                    counts["succeeded"] += 1
                else:
                    counts["errored"] += 1
                snapshot = dict(counts)
            if on_item_finish is None:
                return
            with contextlib.suppress(Exception):
                on_item_finish(
                    ReplayItemFinishProgress(
                        completed=snapshot["completed"],
                        total=total,
                        succeeded=snapshot["succeeded"],
                        errored=snapshot["errored"],
                        experiment_id=experiment_id,
                        test_run_id=experiment_id,
                        item=item,
                    )
                )

        def run_one(index: int) -> ReplayItem:
            server_item, attempt = work_items[index]
            if throttle is not None:
                report_held_back(index, throttle.admit(index, cancel))
                if cancel.is_set():
                    raise ReplayChildCancelled()
            report_start(server_item, attempt)
            assignment_path = workdir / f"assignment-{index}.json"
            result_path = workdir / f"result-{index}.json"
            hook_error_path = workdir / f"hook-error-{index}.txt"
            delivery_error_path = workdir / f"delivery-error-{index}.txt"
            assignment_path.write_text(
                json.dumps(
                    {
                        "experiment_id": experiment_id,
                        "server_item": server_item,
                        "replayed_trace_id": replayed_trace_ids[index],
                        "attempt": attempt,
                        "result_path": str(result_path),
                        "hook_error_path": str(hook_error_path),
                        "delivery_error_path": str(delivery_error_path),
                        **({} if db_branch is None else {"db_branch": db_branch}),
                    }
                ),
                encoding="utf-8",
            )
            argv = [
                sys.executable,
                "-m",
                "bitfab.replay_cli",
                "--registry",
                registry_path,
                *replay_args,
                "--execute-item",
                str(assignment_path),
            ]
            log_path = workdir / f"child-{index}.log"
            code = _run_child(
                argv,
                dict(environ),
                cancel,
                timeout_seconds,
                log_path,
                throttle,
                index,
            )
            _surface_child_message(delivery_error_path, stderr)
            if result_path.exists():
                item: ReplayItem = json.loads(result_path.read_text(encoding="utf-8"))
                # The child serialized its exceptions to plain dicts. `error`
                # already carries the readable message, and handing a dict to a
                # reader that expects an exception is worse than handing None.
                item["trace_error"] = None
                item["replay_error"] = None
                _surface_child_message(hook_error_path, stderr)
                return item
            tail = _output_tail(log_path)
            detail = f" Last output:\n{tail}" if tail else ""
            return failed_replay_item(
                server_item,
                attempt,
                f"Replay child exited {code} without writing a result.{detail}",
            )

        def guarded(index: int) -> ReplayItem:
            server_item, attempt = work_items[index]
            try:
                item = run_one(index)
            except ReplayChildCancelled:
                raise
            except Exception as cause:
                item = failed_replay_item(
                    server_item, attempt, f"Replay child could not be run: {cause}"
                )
            finally:
                if throttle is not None:
                    throttle.release(index)
            report_finish(item)
            return item

        try:
            with ThreadPoolExecutor(
                max_workers=max_concurrency or len(work_items)
            ) as pool:
                futures = {
                    pool.submit(guarded, index): index
                    for index in range(len(work_items))
                }
                try:
                    for future in as_completed(futures):
                        results[futures[future]] = future.result()
                except BaseException:
                    cancel.set()
                    if throttle is not None:
                        throttle.wake_all()
                    for future in futures:
                        future.cancel()
                    raise
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        return [results[index] for index in range(len(work_items))]

    return launch
