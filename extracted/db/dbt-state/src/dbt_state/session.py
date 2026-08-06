import atexit
import logging
import time
import typing as t
import uuid
from datetime import timedelta

from query_cache_common.models.services import client_telemetry_service_models

from dbt_state.config import RunCacheConfig
from dbt_state.dispatcher import TelemetryDispatcher
from dbt_state.version import __version__, dbt_version, sqlglot_version

logger = logging.getLogger(__name__)


class SessionManager:
    def __init__(self, session_id: t.Optional[str] = None):
        self._session_id = session_id or uuid.uuid4().hex
        self._telemetry_dispatcher: t.Optional[TelemetryDispatcher] = None
        self._started = False
        self._start_time: t.Optional[float] = None

    def start(
        self, run_cache_config: RunCacheConfig, telemetry_dispatcher: TelemetryDispatcher
    ) -> None:
        try:
            if self._started:
                return
            self._start_time = time.monotonic()
            self._started = True
            self._telemetry_dispatcher = telemetry_dispatcher
            atexit.register(self._close)
            config = run_cache_config.to_json(exclude_sensitive=True)

            request = client_telemetry_service_models.SessionStartRequest(
                dbt_run_cache_version=__version__,
                dbt_version=dbt_version,
                sqlglot_version=sqlglot_version,
                config=config,
            )

            assert self._telemetry_dispatcher is not None
            self._telemetry_dispatcher.add_event(request)
            logger.info("Session start event queued: session_id=%s", self._session_id)
        except Exception as e:
            logger.warning("Failed to report client session start: %s", e)

    def end(
        self,
        result: client_telemetry_service_models.ClientResult,
        description: str,
        metrics: t.Dict[str, t.Any],
    ) -> None:
        if not self._started or not self._telemetry_dispatcher or not self._start_time:
            return

        try:
            duration = timedelta(seconds=time.monotonic() - self._start_time)
            request = client_telemetry_service_models.SessionEndRequest(
                result=result,
                result_description=description,
                session_duration=duration,
                metrics=metrics,
            )

            self._telemetry_dispatcher.add_event(request)
            logger.info("Session end event queued: session_id=%s", self._session_id)

            self._started = False
            self._start_time = None
        except Exception as e:
            logger.warning("Failed to report client session end: %s", e)

    def _close(self) -> None:
        try:
            assert self._telemetry_dispatcher is not None
            self._telemetry_dispatcher.shutdown(flush=True)
        except Exception as e:
            logger.warning(
                "[CLIENT %s] failed to shutdown telemetry dispatcher: %s",
                self._session_id,
                e,
            )
