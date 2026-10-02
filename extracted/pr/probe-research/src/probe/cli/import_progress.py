"""Read-only completion summaries for the two user-facing import categories."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
import time

from .import_jobs import Kind, State


def number(value):
    return (value if isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0 else None)


def completion_known(job):
    progress = job.get("progress") or {}
    return (job["state"] == State.SUCCEEDED
            or all(number(progress.get(field)) is not None
                   for field in ("completion_completed", "completion_total"))
            or progress.get("phase") == "scanning"
            or (job["state"] == State.QUEUED and not progress.get("completed")
                and (job.get("attempt") or 0) <= 1))


def counts(job):
    progress = job.get("progress") or {}
    payload = job.get("payload") or {}
    total = number(progress.get("completion_total"))
    done = number(progress.get("completion_completed"))
    if total is None:
        inventory = payload.get("files" if job.get("kind") == Kind.TRANSCRIPTS else "targets")
        if isinstance(inventory, list):
            total = len(inventory)
    if total is None and progress.get("phase") != "scanning":
        total = number(progress.get("total"))
    if job["state"] == State.SUCCEEDED and done is None:
        return total, total
    if done is None:
        # Older workers publish processing counters. Never count a scan or a
        # file-preparation pass as a completed upload.
        preparing = (progress.get("phase") == "scanning"
                     or progress.get("message") == "Reading reviewed files")
        done = 0 if preparing or not completion_known(job) else number(progress.get("completed")) or 0
    return min(done, total) if total is not None else done, total


class Estimates:
    """Observe legacy workers too; no worker restart or journal writes required."""

    def __init__(self):
        self.samples = {}

    def rate(self, job, now):
        done, total = counts(job)
        progress = job.get("progress") or {}
        key = job.get("id", "")
        if (job["state"] != State.RUNNING or progress.get("waiting_for_connection")
                or progress.get("phase") == "scanning" or total is None or not completion_known(job)):
            self.samples.pop(key, None)
            return None
        stamp = (job.get("attempt"), progress.get("phase"), total)
        previous = self.samples.get(key)
        if previous is None or previous[0] != stamp or done < previous[2]:
            self.samples[key] = (stamp, now, done, None, job.get("kind") != Kind.FOLDER and done > 0)
        elif not previous[4] and done > previous[2]:
            self.samples[key] = (stamp, now, done, None, True)
        elif done > previous[2] and now > previous[1]:
            self.samples[key] = (stamp, now, done, (done - previous[2]) / (now - previous[1]), True)
        sample = self.samples[key]
        if sample[3] and now - sample[1] < 300:
            return sample[3]
        eta = number(progress.get("eta_seconds"))
        try:
            at = datetime.fromisoformat(progress["eta_updated_at"].replace("Z", "+00:00"))
            fresh = 0 <= (datetime.now(timezone.utc) - at).total_seconds() < 300
        except (KeyError, TypeError, ValueError):
            fresh = False
        if eta and total > done and fresh:
            return (total - done) / eta
        return None


@dataclass
class Summary:
    title: str
    unit: str
    state: str
    completed: float
    total: float | None
    fraction: float
    eta: float | None = None
    active: bool = False
    measured: bool = True


def _inventory(job):
    """Frozen session versions, scoped to their approved account/destination."""
    payload = job.get("payload") or {}
    rows = payload.get("files")
    if not isinstance(rows, list):
        return None, set()
    scope = json.dumps(payload.get("account"), sort_keys=True)
    completed_ids = {tuple(pair) for pair in (job.get("progress") or {}).get("completion_ids", [])
                     if isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, str) for v in pair)}
    keys, complete = set(), set()
    done, total = counts(job)
    finished = job["state"] == State.SUCCEEDED and done == total
    for row in rows:
        if not isinstance(row, dict) or not all(field in row for field in ("agent", "session_id", "sha256", "size")):
            return None, set()
        key = (scope, row["agent"], row["session_id"], row["sha256"], row["size"])
        keys.add(key)
        if finished or (row["agent"], row["session_id"]) in completed_ids:
            complete.add(key)
    return keys, complete


def summarize(jobs, kind, estimates=None, *, completed_since: datetime | None = None):
    title, unit = ("Session imports", "sessions") if kind == Kind.TRANSCRIPTS else ("File imports", "files")
    saved = [job for job in jobs if job.get("kind") == kind]
    receipts = set()
    if kind == Kind.TRANSCRIPTS:
        # Expiry hides overview rows, not receipts: a later successful import
        # must still settle an older partial snapshot after leaving the view.
        for job in saved:
            receipts |= _inventory(job)[1]

    # Canceled work stays in Details for an explicit resume. Its remaining
    # inventory must not make unrelated active work look unfinished, but its
    # receipts above still settle sessions completed before cancellation.
    saved = [job for job in saved if job["state"] != State.CANCELED]

    def outstanding(job):
        done, total = counts(job)
        if job["state"] != State.SUCCEEDED:
            return True
        if total is None or done == total:
            return False
        keys, _ = _inventory(job) if kind == Kind.TRANSCRIPTS else (None, set())
        return keys is None or not keys <= receipts

    def recent_completion(job):
        if completed_since is None:
            return True
        # Older saved jobs may predate finished_at. Use their last durable
        # timestamp, but retain records whose age cannot be established.
        for field in ("finished_at", "updated_at", "created_at"):
            try:
                at = datetime.fromisoformat(job[field].replace("Z", "+00:00"))
                if at.tzinfo is None:
                    at = at.replace(tzinfo=timezone.utc)
                return at > completed_since
            except (KeyError, AttributeError, TypeError, ValueError):
                continue
        return True

    unfinished = [job for job in saved if outstanding(job)]
    if unfinished:
        start = min((job.get("created_at", "") for job in unfinished), default="")
        selected = unfinished + [job for job in saved if not outstanding(job)
                                 and recent_completion(job)
                                 and start and (job.get("finished_at") or "") >= start]
    else:
        selected = sorted((job for job in saved if recent_completion(job)),
                          key=lambda job: job.get("created_at", ""), reverse=True)[:1]
    if not selected:
        return Summary(title, unit, "Not started", 0, 0, 0)

    done, total, unknown = 0, 0, False
    measured = all(completion_known(job) for job in selected)
    union, known_complete, missing_bounds, maximum_done = set(), set(), 0, 0
    for job in selected:
        completed, count = counts(job)
        unknown |= count is None
        keys, complete = _inventory(job) if kind == Kind.TRANSCRIPTS else (None, set())
        if keys is not None:
            union |= keys
            known_complete |= complete
            missing_bounds += max(0, len(keys) - (completed or 0))
            maximum_done = max(maximum_done, completed or 0)
        else:
            done += completed or 0
            total += count or 0
    if union:
        # Older running jobs have counts but no per-session completion IDs.
        # This lower bound avoids double-counting overlapping queued snapshots.
        done += min(len(union), max(len(known_complete), maximum_done, len(union) - missing_bounds))
        total += len(union)

    running = [job for job in unfinished if job["state"] == State.RUNNING]
    queued = sum(job["state"] == State.QUEUED for job in unfinished)
    attention = sum(job["state"] in {State.FAILED, State.INTERRUPTED} for job in unfinished)
    waiting = any((job.get("progress") or {}).get("waiting_for_connection") for job in running)
    scanning = any((job.get("progress") or {}).get("phase") == "scanning" for job in running)
    state = ("Waiting for connection" if waiting else "Scanning" if scanning else "Importing" if running
             else "Queued" if queued else "Needs attention" if attention else "Complete")
    if state == "Complete" and not unknown and done < total:
        state = "Partially complete"
    if attention and (running or queued):
        state += " · needs attention"
    active = bool(running or queued)
    fraction = min(1, done / total) if total and not unknown and measured else 0
    if state == "Complete":
        fraction = 1
    elif fraction == 1:
        # Completion is only final once the worker has verified its receipts.
        fraction = .99
        if running and not queued and not attention:
            state = "Finishing"
    eta = None
    rates_by_id = ({job.get("id"): estimates.rate(job, time.monotonic()) for job in selected}
                   if estimates is not None else {})
    if estimates is not None and running and measured and not (unknown or attention or waiting or scanning):
        rates = [rates_by_id[job.get("id")] for job in running]
        if all(rate is not None for rate in rates):
            if kind == Kind.FOLDER:
                if not queued:
                    eta = max(max(0, counts(job)[1] - counts(job)[0]) / rate
                              for job, rate in zip(running, rates))
            else:
                eta = max(0, total - done) / sum(rates)
    return Summary(title, unit, state, done, None if unknown else total, fraction, eta, active, measured)
