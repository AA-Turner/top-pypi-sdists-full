#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
End-to-end test for the featrixevents library.

Posts ~500 synthetic events with featrix_post_event(), then calls the
new /events/build-model endpoint to confirm Featrix can:
  1. Receive and store events via the public ingest API.
  2. Materialize those events back into a training dataset.
  3. Spin up a real foundational-model training session.

This is a *real* network test — no mocks. It writes rows to the
production user_events table under a namespaced event_group_id so the
data is identifiable and harmless.

Run with:
    pytest featrixevents/tests/test_e2e_collect_and_build.py -s

No FEATRIX_API_KEY export needed on this machine -- get_api_key() (below)
uses the same fallback chain featrixsphere.FeatrixSphere() uses internally:
FEATRIX_API_KEY env var, else ~/.featrix / ~/.featrix/config /
~/.featrix_default_key. Only skips if none of those resolve to a key.
"""

import os
import random
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest
import requests

from featrixevents import featrix_post_event, FeatrixEventError

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from tests._api_session import get_api_key  # noqa: E402  (needs the sys.path insert above)


DEFAULT_BASE_URL = os.getenv("FEATRIX_BASE_URL", "https://sphere-api.featrix.com")
API_KEY = get_api_key()

NUM_EVENTS = 500
INGEST_WORKERS = 16  # well under the 100 events/sec/org rate limit at ~200ms latency
INGEST_MAX_SECONDS = 120
BUILD_POLL_INTERVAL = 15
# Stall-detector: if no status/progress change for this many seconds, fail.
TRAIN_STALL_TIMEOUT = 900
# Hard wall-clock cap so a test run can't wedge a CI box forever.
TRAIN_WALL_TIMEOUT = 3600

# Columns we synthesize. `outcome` is the learnable target.
EXPECTED_COLUMNS = {
    "user_tier",
    "pages_viewed",
    "time_on_site",
    "prior_purchases",
    "source",
    "outcome",
}


pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="No Featrix API key found (env var or ~/.featrix) — e2e test needs a real ingest key",
)


def _make_synthetic_event(rng: random.Random) -> dict:
    """One synthetic page-session event with a learnable outcome.

    `outcome` is biased by user_tier + prior_purchases + time_on_site so a
    foundational model + SP should beat the class prior. We're not asserting
    on model quality here, just on round-trip + training completion — but
    we want the data to be non-degenerate so training has something to do.
    """
    tier = rng.choices(
        ["free", "pro", "enterprise"],
        weights=[0.6, 0.3, 0.1],
    )[0]
    source = rng.choice(["organic", "ads", "referral", "email", "social"])
    pages = max(1, int(rng.gauss(4, 2)))
    time_on_site = round(max(2.0, rng.gauss(45.0, 25.0)), 1)
    prior_purchases = rng.choices(
        [0, 1, 2, 3, 5, 10],
        weights=[0.45, 0.25, 0.15, 0.08, 0.05, 0.02],
    )[0]

    # Bias the target so it's learnable.
    score = 0.0
    score += {"free": 0.0, "pro": 0.4, "enterprise": 0.7}[tier]
    score += min(prior_purchases / 5.0, 1.0) * 0.5
    score += (time_on_site / 120.0) * 0.3
    score += rng.gauss(0, 0.2)
    outcome = "converted" if score > 0.55 else "not_converted"

    return {
        "user_tier": tier,
        "pages_viewed": pages,
        "time_on_site": time_on_site,
        "prior_purchases": prior_purchases,
        "source": source,
        "outcome": outcome,
    }


def _ingest_one(event_group_id: str, payload: dict) -> str:
    """Post one event. Returns event_id. Re-raises on failure."""
    result = featrix_post_event(
        auth_key_id=API_KEY,
        event_group_id=event_group_id,
        event_payload=payload,
        base_url=DEFAULT_BASE_URL,
        timeout=30.0,
    )
    assert result.get("success") is True, f"ingest result missing success: {result}"
    event_id = result.get("event_id")
    assert event_id, f"ingest result missing event_id: {result}"
    return event_id


def _post_build_model(event_group_id: str, name: str) -> dict:
    """Call /events/build-model and return the JSON response."""
    url = f"{DEFAULT_BASE_URL.rstrip('/')}/events/build-model"
    body = {
        "event_group_id": event_group_id,
        "name": name,
        "max_events": NUM_EVENTS * 2,
    }
    resp = requests.post(
        url,
        headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
        json=body,
        timeout=1800,
    )
    if resp.status_code not in (200, 201, 202):
        raise AssertionError(
            f"build-model failed: HTTP {resp.status_code}: {resp.text[:1000]}"
        )
    return resp.json()


def _get_session(session_id: str) -> dict:
    url = f"{DEFAULT_BASE_URL.rstrip('/')}/compute/session/{session_id}"
    resp = requests.get(
        url,
        headers={"X-Api-Key": API_KEY},
        timeout=60,
    )
    if resp.status_code != 200:
        raise AssertionError(
            f"session lookup failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )
    return resp.json()


def _wait_for_training(session_id: str) -> dict:
    """Poll /compute/session/{id} until status leaves the in-flight set.

    Stall-detector: if neither status nor any job's status changes for
    TRAIN_STALL_TIMEOUT seconds, fail. Also enforces TRAIN_WALL_TIMEOUT
    as a hard cap.
    """
    in_flight = {"queued", "starting", "running", "training", "in_progress", None, ""}
    success_states = {"done", "completed", "finished", "ready"}
    failure_states = {"failed", "error", "aborted", "cancelled"}

    started = time.time()
    last_change = time.time()
    last_fingerprint = None
    last_seen = None

    while True:
        now = time.time()
        if now - started > TRAIN_WALL_TIMEOUT:
            pytest.fail(
                f"Wall-clock timeout ({TRAIN_WALL_TIMEOUT}s) waiting on session "
                f"{session_id}. Last seen: {last_seen}"
            )
        if now - last_change > TRAIN_STALL_TIMEOUT:
            pytest.fail(
                f"Stall timeout: no status change for {TRAIN_STALL_TIMEOUT}s on "
                f"session {session_id}. Last seen: {last_seen}"
            )

        try:
            payload = _get_session(session_id)
        except AssertionError as e:
            # 404 right after dispatch can happen if the session is still
            # being registered. Tolerate a few before failing.
            if now - started < 60:
                time.sleep(BUILD_POLL_INTERVAL)
                continue
            raise

        session = payload.get("session", payload)
        status = (session.get("status") or "").lower()
        jobs = payload.get("jobs") or {}
        job_summary = tuple(
            sorted(
                (jid, (j.get("status") or "").lower())
                for jid, j in jobs.items()
            )
        )
        fingerprint = (status, job_summary)
        last_seen = {"status": status, "jobs": dict(jobs)}

        if fingerprint != last_fingerprint:
            last_change = now
            last_fingerprint = fingerprint
            print(
                f"[{int(now - started)}s] session={session_id[:12]}... "
                f"status={status!r} jobs={len(jobs)}"
            )

        if status in failure_states:
            pytest.fail(
                f"Training failed: session={session_id}, status={status}, "
                f"jobs={jobs}"
            )

        if status in success_states:
            return payload

        if status not in in_flight:
            # Unknown status — surface it so we can learn what's happening.
            print(f"[warn] unknown session status {status!r}; continuing to poll")

        time.sleep(BUILD_POLL_INTERVAL)


def test_e2e_collect_events_and_build_model():
    """Post 500 events, fetch them back via /events/build-model, train an ES.

    Asserts:
      - All 500 events are accepted by the ingest endpoint.
      - /events/build-model reports the right row count and column set.
      - Training reaches a terminal success state without manual help.
    """
    assert API_KEY, "No Featrix API key found (env var or ~/.featrix)"

    event_group_id = str(uuid.uuid4())
    run_label = f"featrixevents-e2e-{event_group_id[:8]}"
    rng = random.Random(0xFEA72)  # deterministic synthetic data

    print(f"\n==> e2e run: event_group_id={event_group_id} label={run_label}")
    print(f"==> base url: {DEFAULT_BASE_URL}")
    print(f"==> posting {NUM_EVENTS} events with {INGEST_WORKERS} workers")

    # --- Phase 1: ingest events in parallel -------------------------------
    payloads = [_make_synthetic_event(rng) for _ in range(NUM_EVENTS)]

    ingest_start = time.time()
    event_ids: list = []
    errors: list = []
    with ThreadPoolExecutor(max_workers=INGEST_WORKERS) as pool:
        futures = [
            pool.submit(_ingest_one, event_group_id, p) for p in payloads
        ]
        for fut in as_completed(futures, timeout=INGEST_MAX_SECONDS):
            try:
                event_ids.append(fut.result())
            except (FeatrixEventError, AssertionError, Exception) as e:
                errors.append(repr(e))

    ingest_elapsed = time.time() - ingest_start
    print(f"==> ingest done in {ingest_elapsed:.1f}s: "
          f"{len(event_ids)} ok, {len(errors)} failed")
    if errors:
        # Show the first few errors so the failure mode is obvious.
        for e in errors[:5]:
            print(f"    err: {e}")
    assert not errors, f"{len(errors)} ingest calls failed (first: {errors[0] if errors else None})"
    assert len(event_ids) == NUM_EVENTS, (
        f"Expected {NUM_EVENTS} event_ids, got {len(event_ids)}"
    )
    # All event_ids should be unique UUIDs.
    assert len(set(event_ids)) == NUM_EVENTS, "Server returned duplicate event_ids"

    # --- Phase 2: build a model from the collected events -----------------
    print(f"==> calling /events/build-model")
    build_result = _post_build_model(event_group_id, run_label)
    print(f"==> build-model returned: "
          f"session_id={build_result.get('session_id')} "
          f"num_events={build_result.get('num_events')} "
          f"queued={build_result.get('queued')} "
          f"cols={build_result.get('columns')}")

    assert build_result.get("success") is True, build_result
    assert build_result.get("num_events") == NUM_EVENTS, (
        f"Expected {NUM_EVENTS} events from build-model, "
        f"got {build_result.get('num_events')}"
    )
    columns = set(build_result.get("columns") or [])
    missing = EXPECTED_COLUMNS - columns
    assert not missing, (
        f"build-model flattened columns are missing {missing}; got {columns}"
    )
    session_id = build_result.get("session_id")
    assert session_id, "build-model returned no session_id"

    # --- Phase 3: wait for the foundational-model training to finish -----
    print(f"==> waiting for training on session {session_id}")
    final_payload = _wait_for_training(session_id)

    session = final_payload.get("session", final_payload)
    final_status = (session.get("status") or "").lower()
    print(f"==> final session status: {final_status}")
    print(f"==> session dump: {session}")
    # _wait_for_training only returns on terminal success.
    assert final_status in {"done", "completed", "finished", "ready"}, (
        f"Unexpected terminal status: {final_status}"
    )
