#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""Core implementation of featrix_post_event."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Union

import requests

from ._key_resolution import get_api_key

DEFAULT_BASE_URL = "https://sphere-api.featrix.com"
INGEST_PATH = "/events/ingest"


class FeatrixEventError(Exception):
    """Raised when posting an event fails."""

    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class FeatrixEventSectionObject(ABC):
    """Base class for a reusable, named bundle of event fields.

    Subclass this once per recurring concept your code emits events about
    (e.g. job/session identifiers, GPU telemetry) instead of hand-building
    the same payload dict at every call site. Pass instances directly as
    `event_payload` to featrix_post_event() -- their to_event_fields() dicts
    are merged together into the payload that gets sent.

    Example:
        class JobSection(FeatrixEventSectionObject):
            def __init__(self, session_id, job_id):
                self.session_id = session_id
                self.job_id = job_id

            def to_event_fields(self) -> dict:
                return {"session_id": self.session_id, "job_id": self.job_id}

        job_ctx = JobSection(session_id=sid, job_id=jid)  # built once
        featrix_post_event(
            auth_key_id=key,
            event_group_id=group,
            event_payload=[job_ctx, GpuMetricsSection(...)],  # reused everywhere
        )
    """

    @abstractmethod
    def to_event_fields(self) -> dict:
        """Return the fields this section contributes to the event payload."""
        raise NotImplementedError


def _resolve_event_payload(
    event_payload: Union[dict, Iterable[FeatrixEventSectionObject]],
) -> dict:
    """Normalize event_payload to a plain dict.

    Accepts either a dict (used as-is, unchanged behavior) or an iterable of
    FeatrixEventSectionObject instances, whose to_event_fields() dicts are
    merged together. Raises FeatrixEventError if two sections define the
    same key -- a silent overwrite there would be a real bug, not a feature.
    """
    if isinstance(event_payload, dict):
        return event_payload

    merged: dict = {}
    for section in event_payload:
        if not isinstance(section, FeatrixEventSectionObject):
            raise TypeError(
                "event_payload must be a dict or an iterable of "
                f"FeatrixEventSectionObject, got {type(section).__name__}"
            )
        fields = section.to_event_fields()
        collisions = set(fields) & set(merged)
        if collisions:
            raise FeatrixEventError(
                f"Duplicate event field(s) {sorted(collisions)} from "
                f"{type(section).__name__} collide with an earlier section"
            )
        merged.update(fields)
    return merged


def featrix_post_event(
    event_group_id: str,
    event_payload: Union[dict, Iterable[FeatrixEventSectionObject]],
    customer_metadata: Optional[dict] = None,
    auto_predictor_targets: Optional[list] = None,
    event_group_name: Optional[str] = None,
    entity_id: Optional[str] = None,
    state: Optional[str] = None,
    terminal: bool = False,
    data_version: Optional[int] = None,
    auth_key_id: Optional[str] = None,
    base_url: str = None,
    timeout: float = 30.0,
) -> dict:
    """
    Post an event to the Featrix platform.

    Args:
        event_group_id: UUID string grouping related events.
        event_payload: Either a dict to store as-is, or an iterable of
                       FeatrixEventSectionObject instances whose fields are
                       merged into the payload (see FeatrixEventSectionObject).
                       Every key here is a training-feature candidate for
                       whatever model this event_group_id auto-trains. Post
                       the facts known NOW -- for a state graph (entity_id
                       below), facts first posted after an entity entered a
                       state are never features of that state's row.
        customer_metadata: Optional dict of facts you want visible on this
                       event for debugging (e.g. a dataset name, an internal
                       run id) but that should NEVER become a training
                       feature. The server folds this under one reserved,
                       already-excluded-from-training key -- kept in the
                       data for inspection, never given a codec. Use this
                       instead of stuffing identifiers into `event_payload`.
        auto_predictor_targets: Optional list of {"target_column": "...",
                       "task_type": "regression"|"classification"} dicts --
                       declares that this event_group_id should also keep a
                       real predictor auto-trained for that column every
                       time the group's embedding space is built/extended
                       (server-side: event_retrain.py's sweeper). Only takes
                       effect on this group's FIRST registration (an
                       insert-if-absent on the server) -- posting it again
                       for an already-registered group is a no-op; use the
                       admin endpoint to change targets on an existing group.
        event_group_name: Optional stable, customer-meaningful name for this event
                       group (lowercase a-z0-9 joined by "-", "_" or "__", e.g.
                       "checkout-events"). Every model auto-trained from the group
                       publishes -- and is predicted and graded -- as
                       "{event_group_name}-{target_column}". Set on first registration;
                       names never change once set.
        entity_id: Optional -- the thing this event is about (one job run,
                       one order, ...), unique within your organization.
                       Events carrying an entity_id make the group a STATE
                       GRAPH: instead of one training row per event, the
                       server trains on each entity's state transitions --
                       what state comes next (`next_state`) and how long the
                       entity stays in the current one (`dwell_seconds`) --
                       each row built only from what was known when that
                       state began.
        state:         Optional -- the state this event moves the entity into
                       (requires entity_id). Omit it to post facts about the
                       entity's current state without changing it.
        terminal:      True when `state` ends the entity (e.g. "completed",
                       "failed"). Facts posted with a terminal event are kept
                       but never become features.
        data_version:  Optional non-negative int -- the version of the code
                       producing this event. Bump it when a change makes the
                       events you posted before it wrong or incompatible: the
                       first event with a higher version than the group has
                       seen becomes the group's floor, and models stop
                       training on older (and unversioned) events -- they are
                       kept, never deleted. The first version a group ever
                       sees only starts the labelling. Never a feature.
        auth_key_id: API key (e.g. "fx_..."). NOT a JWT. If omitted, resolved
                     via FEATRIX_API_KEY env var or ~/.featrix (file or
                     directory containing identity.env/config) -- same
                     resolution featrixsphere.FeatrixSphere() uses.
        base_url: Server URL. Defaults to FEATRIX_BASE_URL env var
                  or "https://sphere-api.featrix.com".
        timeout: Request timeout in seconds.

    Returns:
        Dict with "success" (bool), "event_id" (str UUID), "data_epoch"
        (int), "data_version" (int or None) and "trainable" (bool -- False
        when the event is below the group's data_version floor; "reason"
        then says why).

    Raises:
        FeatrixEventError: On auth failure, server error, connection error,
            a duplicate field across FeatrixEventSectionObject instances, or
            no API key resolvable from an argument, env var, or ~/.featrix.
    """
    if auth_key_id is None:
        auth_key_id = get_api_key()
    if not auth_key_id:
        raise FeatrixEventError(
            "No API key found. Pass auth_key_id=, set FEATRIX_API_KEY, or "
            "add one to ~/.featrix (file or directory with identity.env/config)."
        )

    if base_url is None:
        base_url = os.getenv("FEATRIX_BASE_URL", DEFAULT_BASE_URL)

    url = f"{base_url.rstrip('/')}{INGEST_PATH}"

    headers = {
        "X-Api-Key": auth_key_id,
        "Content-Type": "application/json",
    }

    body = ingest_body(
        event_group_id=event_group_id, event_payload=event_payload, customer_metadata=customer_metadata,
        auto_predictor_targets=auto_predictor_targets, event_group_name=event_group_name,
        entity_id=entity_id, state=state, terminal=terminal, data_version=data_version,
    )
    return _send("post", url, body=body, headers=headers, timeout=timeout, what="Event post")



def ingest_body(
    event_group_id: str,
    event_payload: Union[dict, Iterable[FeatrixEventSectionObject]],
    customer_metadata: Optional[dict] = None,
    auto_predictor_targets: Optional[list] = None,
    event_group_name: Optional[str] = None,
    entity_id: Optional[str] = None,
    state: Optional[str] = None,
    terminal: bool = False,
    data_version: Optional[int] = None,
) -> dict:
    """The JSON body of POST /events/ingest -- for senders that deliver it
    themselves (e.g. a durable outbox) instead of calling featrix_post_event.
    Arguments as for featrix_post_event."""
    body = {
        "event_group_id": event_group_id,
        "event_payload": _resolve_event_payload(event_payload),
    }
    if customer_metadata:
        body["customer_metadata"] = customer_metadata
    if auto_predictor_targets:
        body["auto_predictor_targets"] = auto_predictor_targets
    if event_group_name:
        body["event_group_name"] = event_group_name
    if entity_id:
        body["entity_id"] = entity_id
    if state:
        body["state"] = state
    if terminal:
        body["terminal"] = True
    if data_version is not None:
        body["data_version"] = data_version
    return body


def featrix_update_event(
    event_id: str,
    event_payload: Union[dict, Iterable[FeatrixEventSectionObject]],
    customer_metadata: Optional[dict] = None,
    auth_key_id: Optional[str] = None,
    base_url: str = None,
    timeout: float = 30.0,
) -> dict:
    """
    Replace an event you posted earlier, in place.

    For facts that get refined after the event was posted (a job's peak
    memory, which grows epoch by epoch): keep the "event_id"
    featrix_post_event returned and overwrite that same event instead of
    posting a new one, so the event group never holds a stale copy. The new
    payload replaces the old one entirely -- send every field, not a diff.
    State-graph events (posted with entity_id) can't be updated.

    Args:
        event_id: The "event_id" featrix_post_event returned.
        event_payload / customer_metadata: As for featrix_post_event.
        auth_key_id / base_url / timeout: As for featrix_post_event.

    Returns:
        Dict with "success" (bool) and "event_id" (str UUID).

    Raises:
        FeatrixEventError: On auth failure, no such event in your organization
            (HTTP 404), server error, or connection error.
    """
    if auth_key_id is None:
        auth_key_id = get_api_key()
    if not auth_key_id:
        raise FeatrixEventError(
            "No API key found. Pass auth_key_id=, set FEATRIX_API_KEY, or "
            "add one to ~/.featrix (file or directory with identity.env/config)."
        )
    if base_url is None:
        base_url = os.getenv("FEATRIX_BASE_URL", DEFAULT_BASE_URL)
    body = {"event_payload": _resolve_event_payload(event_payload)}
    if customer_metadata:
        body["customer_metadata"] = customer_metadata
    return _send(
        "put", f"{base_url.rstrip('/')}/events/{event_id}", body=body,
        headers={"X-Api-Key": auth_key_id, "Content-Type": "application/json"},
        timeout=timeout, what="Event update",
    )


def _send(method: str, url: str, *, body: dict, headers: dict, timeout: float, what: str) -> dict:
    try:
        send = requests.put if method == "put" else requests.post
        resp = send(url, json=body, headers=headers, timeout=timeout)
    except requests.ConnectionError as e:
        raise FeatrixEventError(f"Connection error: {e}") from e
    except requests.Timeout as e:
        raise FeatrixEventError(f"Request timed out after {timeout}s") from e

    if resp.status_code in (200, 201):
        return resp.json()

    # Error path
    try:
        error_body = resp.json()
        error_msg = error_body.get("error", resp.text)
    except Exception:
        error_msg = resp.text

    raise FeatrixEventError(
        f"{what} failed (HTTP {resp.status_code}): {error_msg}",
        status_code=resp.status_code,
        response_body=resp.text,
    )
