#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
EventGroup class for FeatrixSphere API.

View of an event group fed by the (separate, write-only) featrixevents
library -- apps post events grouped by event_group_id via
featrixevents.featrix_post_event(); this class is how you query what's
accumulated for a group and whether/when a model has been trained from it,
and how you cut its models off from data you no longer want them to learn
from (reset / set_floors -- nothing is ever deleted).
"""

import logging
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Dict, Any, List, Optional, TYPE_CHECKING

from .foundational_model import _parse_datetime

if TYPE_CHECKING:
    from .http_client import ClientContext

logger = logging.getLogger(__name__)

# "Leave this floor as it is" for EventGroup.set_floors (None is a real
# min_data_version value: ignore versions).
UNCHANGED = object()


# TargetReadiness.state values.
READINESS_STATES = (
    'collecting', 'insufficient_labels', 'training', 'early', 'trained', 'stale', 'failed', 'unassessed',
)


@dataclass
class TargetReadiness:
    """
    Why one declared target has (or lacks) a model, and the numbers behind it.

    state is one of:
        collecting: the group has too few usable rows for any model yet
            (usable_rows of rows_required).
        insufficient_labels: enough rows, but the target's own values can't
            train a model yet -- too few labelled rows, a single value, or a
            class below the per-class minimum. reason says what more is needed.
        training: dispatched; the result is pending.
        early: trained on few examples; judged by its held-out predictions
            on them.
        trained: a model trained on the group's newest data serves.
        stale: a model serves, but newer data could not be used --
            blocked_by and reason say why; trained_at / events_trained_on
            describe the model still serving.
        failed: training was rejected or crashed; node_error has the reason.
        unassessed: not checked yet since readiness tracking began.

    Attributes:
        target_column: The target this describes.
        state: One of READINESS_STATES.
        reason: Plain-language explanation, with the numbers.
        checked_at: When this was last recorded.
        trained_at: When the serving model finished training, if one serves.
        events_trained_on: Events the serving (or in-training) model trained on.
        session_id: The serving (or in-training) model's session.
        class_counts: {label: count} of the labelled rows (classification).
        labelled_rows: Rows carrying a value for this target.
        usable_rows: Training rows the group's events make.
        rows_required: The minimum the blocking check needs.
        min_per_class: Per-class minimum (classification).
        distinct_values: Distinct values seen, when fewer than 2.
        blocked_by: For stale: the state that kept newer data out.
        node_error: For failed (or stale after a failure): the node's reason.
        raw: The full entry as the server sent it.
    """

    target_column: str
    state: str
    reason: str
    checked_at: Optional[datetime] = None
    trained_at: Optional[datetime] = None
    events_trained_on: Optional[int] = None
    session_id: Optional[str] = None
    class_counts: Optional[Dict[str, int]] = None
    labelled_rows: Optional[int] = None
    usable_rows: Optional[int] = None
    rows_required: Optional[int] = None
    min_per_class: Optional[int] = None
    distinct_values: Optional[int] = None
    blocked_by: Optional[str] = None
    node_error: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_response(cls, target_column: str, entry: Dict[str, Any]) -> 'TargetReadiness':
        return cls(
            target_column=target_column,
            state=entry.get('state', 'unassessed'),
            reason=entry.get('reason', ''),
            checked_at=_parse_datetime(entry.get('checked_at')),
            trained_at=_parse_datetime(entry.get('trained_at')),
            events_trained_on=entry.get('events_trained_on'),
            session_id=entry.get('session_id'),
            class_counts=entry.get('class_counts'),
            labelled_rows=entry.get('labelled_rows'),
            usable_rows=entry.get('usable_rows'),
            rows_required=entry.get('rows_required'),
            min_per_class=entry.get('min_per_class'),
            distinct_values=entry.get('distinct_values'),
            blocked_by=entry.get('blocked_by'),
            node_error=entry.get('node_error'),
            raw=dict(entry),
        )

    @property
    def has_model(self) -> bool:
        """True when a model answers predictions for this target (trained_at
        is the serving model's, carried on every state while one serves)."""
        return self.trained_at is not None


@dataclass
class EventGroup:
    """
    Represents an event group -- events posted via featrixevents, grouped by
    event_group_id.

    A group only appears once it has received at least one event (lazy
    registration server-side) -- an event_group_id that's never been posted
    to will 404 rather than return an empty group.

    Attributes:
        event_group_id: UUID grouping related events.
        event_count: Live count of events in this group. Only populated by
            FeatrixSphere.event_group()/refresh() (the detail fetch) -- list
            results leave this None, since counting every group in a page
            would be an expensive fan-out. Use event_count_at_last_train for
            a cheap (but possibly stale) figure in list results.
        event_count_at_last_train: Event count as of the last successful
            train/extend from this group.
        extend_count: Number of times a model has been extended from this
            group's events.
        auto_retrain_enabled: Whether the auto-retrain sweeper is enabled
            for this group.
        last_session_id: Session ID of the last model trained/extended from
            this group's events, if any.
        last_trained_at: When the last train/extend completed.
        consecutive_failures: Consecutive auto-retrain failures.
        last_failed_at: When the last auto-retrain failure happened.
        created_at: When this group was first registered (first event).
        updated_at: When this group's state was last updated.
        trainable_event_count: Live count of the events models train on --
            at/above both data floors. Detail fetch only, like event_count.
        data_epoch: The data epoch new events are stamped with. reset()
            starts a new one.
        min_data_epoch: Oldest epoch models train on.
        max_data_version_seen: Highest data_version any event has carried
            (featrix_post_event(data_version=...)); None before the first.
        min_data_version: Oldest data_version models train on; None = versions
            ignored. Raised automatically when an event arrives with a higher
            data_version than the group has seen.
        data_cutover_history: Every reset / version bump / floor change:
            [{kind, from, to, at, reason, by, source}, ...].
        model_cutover_status: The floors the current model trained under vs
            the group's now; "stale": True until the rebuild on the new data
            is promoted (the old model keeps serving meanwhile).
        below_floor_rows: Events posted below min_data_version since the last
            cut-over ({count, last_at, last_caller, last_data_version}) -- a
            producer still running old code. Detail fetch only.
        name: Stable routing name -- models publish as "{name}-{target}".
        display_name: Admin-set display name, if any.
        auto_predictor_targets: Targets auto-trained on every rebuild.
        predictor_sessions: {target_column: {session_id, predictor_id, ...}}
            for the trained predictors.
        target_readiness: {target_column: TargetReadiness} for every declared
            target -- why it has (or lacks) a model, with the numbers.

    Usage:
        group = client.event_group("...")
        print(f"{group.event_count} events, last trained {group.last_trained_at}")

        for group in client.list_event_groups():
            print(group.event_group_id, group.event_count_at_last_train)

        # Stop training on everything collected so far (kept, not deleted):
        group.reset(reason="producer posted cents as dollars before v2.3")
        # ...and undo it:
        group.set_floors(min_data_epoch=0, reason="reset was a mistake")
    """

    event_group_id: str
    event_count: Optional[int] = None
    event_count_at_last_train: int = 0
    extend_count: int = 0
    auto_retrain_enabled: bool = False
    last_session_id: Optional[str] = None
    last_trained_at: Optional[datetime] = None
    consecutive_failures: int = 0
    last_failed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    trainable_event_count: Optional[int] = None
    data_epoch: int = 0
    min_data_epoch: int = 0
    max_data_version_seen: Optional[int] = None
    min_data_version: Optional[int] = None
    data_cutover_history: List[Dict[str, Any]] = field(default_factory=list)
    model_cutover_status: Optional[Dict[str, Any]] = None
    below_floor_rows: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    auto_predictor_targets: List[Dict[str, Any]] = field(default_factory=list)
    predictor_sessions: Dict[str, Any] = field(default_factory=dict)
    target_readiness: Dict[str, TargetReadiness] = field(default_factory=dict)

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    @classmethod
    def from_response(cls, response: Dict[str, Any], ctx: Optional['ClientContext'] = None) -> 'EventGroup':
        """Create an EventGroup from an API response dict."""
        return cls(
            event_group_id=response.get('event_group_id', ''),
            event_count=response.get('event_count'),
            event_count_at_last_train=response.get('event_count_at_last_train', 0),
            extend_count=response.get('extend_count', 0),
            auto_retrain_enabled=response.get('auto_retrain_enabled', False),
            last_session_id=response.get('last_session_id'),
            last_trained_at=_parse_datetime(response.get('last_trained_at')),
            consecutive_failures=response.get('consecutive_failures', 0),
            last_failed_at=_parse_datetime(response.get('last_failed_at')),
            created_at=_parse_datetime(response.get('created_at')),
            updated_at=_parse_datetime(response.get('updated_at')),
            trainable_event_count=response.get('trainable_event_count'),
            data_epoch=response.get('data_epoch', 0),
            min_data_epoch=response.get('min_data_epoch', 0),
            max_data_version_seen=response.get('max_data_version_seen'),
            min_data_version=response.get('min_data_version'),
            data_cutover_history=response.get('data_cutover_history') or [],
            model_cutover_status=response.get('model_cutover_status'),
            below_floor_rows=response.get('below_floor_rows'),
            name=response.get('name'),
            display_name=response.get('display_name'),
            auto_predictor_targets=response.get('auto_predictor_targets') or [],
            predictor_sessions=response.get('predictor_sessions') or {},
            target_readiness={
                tc: TargetReadiness.from_response(tc, entry)
                for tc, entry in (response.get('target_readiness') or {}).items()
            },
            _ctx=ctx,
        )

    def refresh(self) -> 'EventGroup':
        """
        Re-fetch this group's detail in place, picking up a fresh live
        event_count and any other state that's changed.

        Returns:
            self, for chaining (e.g. `group.refresh().event_count`).
        """
        if not self._ctx:
            raise ValueError("EventGroup not connected to client")

        response = self._ctx.get_json(f"/events/groups/{self.event_group_id}")
        updated = EventGroup.from_response(response, ctx=self._ctx)
        for f in fields(self):
            if f.name not in ('event_group_id', '_ctx'):
                setattr(self, f.name, getattr(updated, f.name))
        return self

    def reset(self, reason: str) -> Dict[str, Any]:
        """
        Stop training this group's models on everything it has collected so
        far -- without deleting any of it. New events get a new data epoch
        and models train only on it; the current model keeps serving (its
        predictions carry a "data_cutover" notice) until the rebuild on the
        new data is promoted, which starts once there are enough new events.
        Undo with set_floors(min_data_epoch=<an older epoch>).

        Args:
            reason: Why the old data is being cut off (kept in
                data_cutover_history).

        Returns:
            The server's result: previous_epoch, data_epoch, min_data_epoch,
            min_data_version, max_data_version_seen, event_count,
            trainable_event_count, effective_at (events accepted before then
            may still land in the old epoch). This object is refreshed too.
        """
        if not self._ctx:
            raise ValueError("EventGroup not connected to client")
        # One attempt: a retry after a lost response would bump the epoch twice.
        result = self._ctx.post_json(f"/events/groups/{self.event_group_id}/reset", data={'reason': reason},
                                     max_retries=1)
        self.refresh()
        return result

    def set_floors(self, *, min_data_epoch: Any = UNCHANGED, min_data_version: Any = UNCHANGED,
                   reason: str) -> Dict[str, Any]:
        """
        Move this group's data floors -- lower one to bring older events back
        into training (undo a reset or a data_version bump), raise one to drop
        them again. Nothing is deleted either way.

        Args:
            min_data_epoch: Oldest epoch models train on, 0..data_epoch.
            min_data_version: Oldest data_version models train on,
                0..max_data_version_seen, or None to ignore versions.
            reason: Why (kept in data_cutover_history).
            A floor left as UNCHANGED stays as it is; pass at least one.

        Returns:
            The server's result (as for reset(), minus previous_epoch).
            This object is refreshed too.
        """
        if not self._ctx:
            raise ValueError("EventGroup not connected to client")
        body: Dict[str, Any] = {'reason': reason}
        if min_data_epoch is not UNCHANGED:
            body['min_data_epoch'] = min_data_epoch
        if min_data_version is not UNCHANGED:
            body['min_data_version'] = min_data_version
        if len(body) == 1:
            raise ValueError("set_floors: pass min_data_epoch and/or min_data_version")
        result = self._ctx.post_json(f"/events/groups/{self.event_group_id}/floors", data=body)
        self.refresh()
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'event_group_id': self.event_group_id,
            'event_count': self.event_count,
            'event_count_at_last_train': self.event_count_at_last_train,
            'extend_count': self.extend_count,
            'auto_retrain_enabled': self.auto_retrain_enabled,
            'last_session_id': self.last_session_id,
            'last_trained_at': self.last_trained_at.isoformat() if self.last_trained_at else None,
            'consecutive_failures': self.consecutive_failures,
            'last_failed_at': self.last_failed_at.isoformat() if self.last_failed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'trainable_event_count': self.trainable_event_count,
            'data_epoch': self.data_epoch,
            'min_data_epoch': self.min_data_epoch,
            'max_data_version_seen': self.max_data_version_seen,
            'min_data_version': self.min_data_version,
            'data_cutover_history': self.data_cutover_history,
            'model_cutover_status': self.model_cutover_status,
            'below_floor_rows': self.below_floor_rows,
            'name': self.name,
            'display_name': self.display_name,
            'auto_predictor_targets': self.auto_predictor_targets,
            'predictor_sessions': self.predictor_sessions,
            'target_readiness': {tc: r.raw for tc, r in self.target_readiness.items()},
        }

    def __repr__(self) -> str:
        count_str = f", event_count={self.event_count}" if self.event_count is not None else ""
        return f"EventGroup(event_group_id='{self.event_group_id}'{count_str})"
