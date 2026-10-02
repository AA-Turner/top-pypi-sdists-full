#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""Status-poll pacing shared by every wait loop in the client."""

import time

# Ceiling for the adaptive interval, and how fast it grows: the interval is
# elapsed/20, so a job 5 minutes in polls every 15s and anything past 20
# minutes polls every 60s. At most ~5% extra latency noticing completion on
# a long job. 2026-09-24: fixed 10s polling of multi-hour trainings was
# ~150k GET /compute/session/<id> a day, and each poll fans out to several
# Supabase reads on the router.
MAX_ADAPTIVE_POLL_SECONDS = 60.0
_ELAPSED_FRACTION = 0.05


def adaptive_poll_interval(base_interval: float, start_time: float) -> float:
    """Seconds to sleep before the next status poll: the caller's
    base_interval while a job is young, backing off with elapsed time up to
    MAX_ADAPTIVE_POLL_SECONDS. A base_interval above the ceiling is kept."""
    elapsed = max(0.0, time.time() - start_time)
    return max(base_interval, min(MAX_ADAPTIVE_POLL_SECONDS, elapsed * _ELAPSED_FRACTION))


# Job statuses after which a job can no longer be "waiting to start".
_TERMINAL_JOB_STATUSES = frozenset(('failed', 'error', 'cancelled', 'done'))


def job_awaiting_start(job: dict) -> bool:
    """True while a non-terminal job exists but hasn't begun real work, so a
    wait loop should treat the time as queued, not as a stall.

    Two server-reported shapes:
      - no `started_at` yet: the session chain claimed the job but the node
        hasn't picked it up (waiting on a worker slot between pipeline steps);
      - `gpu_slot_wait_started_at` set: the node's celery task started (so
        `started_at` IS set and status reads 'running') but it is held in
        celery_app._wait_for_gpu_training_slot until a GPU training slot
        frees. The node clears the marker the moment it launches.

    2026-09-25 taco: an ES job held 68 min behind "4/4 running" with
    started_at set and no epochs; the waiter counted all of it as no-progress
    and the QA client failed it at the 3600s stall budget.
    """
    status = job.get('status')
    if hasattr(status, 'value'):
        status = status.value
    if status in _TERMINAL_JOB_STATUSES:
        return False
    return (not job.get('started_at')) or bool(job.get('gpu_slot_wait_started_at'))
