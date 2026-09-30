"""Auto-generated stub for module: actions_api."""
from typing import Any, Callable, Optional

from .bootstrap import get_action_record
from .models import ActionRecord, RedisServer
from .response import unwrap_platform
from .transport import _rpc_model

# Classes
class ActionsApi:
    # ``AnalyticsClient.actions`` -- what the platform knows about this worker's launch.
    #
    #     Args:
    #         session_provider: Called for the session to ride on each request. A callable rather
    #             than a session because a handle taken once is a handle that goes stale when the
    #             client's session is rebuilt -- the same reason
    #             :attr:`~.analytics_client.AnalyticsClient.rpc` is a property.

    def __init__(self: Any, session_provider: Callable[[], Any]) -> None: ...

    REDIS_SERVER_BY_INSTANCE: str

    def fetch_redis_server(self: Any, instance_id: str) -> Optional[Any]:
        """
        The Redis server record for one instance, or ``None`` if there is no such record.
        
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
        ...

    def get_action_details(self: Any, action_id: Optional[str] = None) -> Any:
        """
        The record for the action that launched this worker.
        
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
        ...

