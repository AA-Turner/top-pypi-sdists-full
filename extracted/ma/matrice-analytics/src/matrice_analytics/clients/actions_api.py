"""Routes answered by **be-actions**, reached through the platform gateway.

be-actions answers **five** of the twenty-four endpoints in :mod:`.models` -- 1 and 9 to 12.
**Two of those five are here**, because they are the two ``AnalyticsClient`` owns: the record
of the action that launched this worker, and the Redis server an instance publishes to.

The other three are this same producer's and are deliberately elsewhere, which is worth
stating because it is the rule the whole package is grouped by.
``/v1/actions/facial_recognition_servers/{id}`` and its update sibling live on ``FRClient``,
and ``/v1/actions/lpr_servers/{id}`` on ``LPRClient`` -- same producer, same URL prefix,
different client. **A route belongs to the client that owns the id it is keyed by**, and
those three are keyed by a server id that only those clients hold. Grouping by producer
instead would put them here, where nothing could supply the id.

The consequence for this module is that being a ``/v1/actions/`` route says nothing about
which client owns it, so the unwrap is bound per route rather than inherited -- see
:mod:`.` for the producer map.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from .bootstrap import get_action_record
from .models import ActionRecord, RedisServer
from .response import unwrap_platform
from .transport import _rpc_model


class ActionsApi:
    """``AnalyticsClient.actions`` -- what the platform knows about this worker's launch.

    Args:
        session_provider: Called for the session to ride on each request. A callable rather
            than a session because a handle taken once is a handle that goes stale when the
            client's session is rebuilt -- the same reason
            :attr:`~.analytics_client.AnalyticsClient.rpc` is a property.
    """

    #: Connection details for the Redis an instance publishes to.
    REDIS_SERVER_BY_INSTANCE = "/v1/actions/get_redis_server_by_instance_id/{instance_id}"

    def __init__(self, session_provider: Callable[[], Any]) -> None:
        self._session_provider = session_provider

    def get_action_details(self, action_id: Optional[str] = None) -> ActionRecord:
        """The record for the action that launched this worker.

        ``get_``, not ``fetch_``: this is **the only cached route of the twenty-four**. The
        first call in a process pays one round trip and every later call is free, because the
        record describes a launch that has already finished -- re-reading it cannot tell this
        process anything new. Forty cameras in one container therefore cost one GET between
        them, not forty.

        The model is rebuilt on each call rather than cached alongside the record, and that
        is deliberate. ``frozen=True`` stops a field being **rebound**; it does nothing about
        the contents of ``action_details`` and ``job_params``, which are the two fields every
        consumer actually reads. A shared model instance would hand every caller the same
        mutable dicts. Rebuilding the model costs ~6 µs against a round trip (measured
        2026-09-21), which is the trade being made.

        **Ordering, and it matters.** The model is built from the copy
        :func:`~.bootstrap.get_action_record` hands back, never from the stored record.
        Validation replaces only the **outermost** mapping and passes nested values through
        by reference, so a model built from the cached document would let a caller reach the
        cache through ``record.job_params`` and change what every later caller reads.

        Args:
            action_id: The action to read. Omit it and the id is resolved from the launch
                environment, which is what a worker asking about itself wants.

        Returns:
            The record, typed.

        Raises:
            CallFailure: No action id could be resolved, or the read did not succeed. An
                absent record is **not** an answer on this route -- a worker whose own launch
                record is missing has nothing to fall back to.
        """
        record = get_action_record(action_id, session=self._session_provider())
        return ActionRecord.model_validate(record)

    def fetch_redis_server(self, instance_id: str) -> Optional[RedisServer]:
        """The Redis server record for one instance, or ``None`` if there is no such record.

        ``fetch_``, so this is a round trip on **every** call. Nothing caches it: unlike the
        action record, which describes a launch that has already happened, a server record
        can change under a running worker.

        Args:
            instance_id: The instance whose Redis is wanted.

        Returns:
            The record, or ``None`` when the platform reports no such instance. Absence is an
            answer on this route, not a failure.

        Raises:
            CallFailure: No base URL produced either a record or an absence.
        """
        return _rpc_model(
            self._session_provider(),
            self.REDIS_SERVER_BY_INSTANCE.format(instance_id=instance_id),
            what=f"the Redis server for instance {instance_id}",
            unwrap=unwrap_platform,
            validate=RedisServer.model_validate,
        )


__all__ = ["ActionsApi"]
