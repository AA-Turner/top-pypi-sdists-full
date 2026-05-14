import importlib.metadata
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from abstra_internals.environment import (
    CLOUD_SAMPLE_RATE,
    LOCAL_SAMPLE_RATE,
    LOGFORMAT,
    LOGLEVEL,
    NOISY_LOGLEVEL,
)
from abstra_internals.utils.env import is_dev_env, is_test_env

internal_logger = lambda: logging.getLogger("abstra_internal")  # noqa: E731


class DevSDK:
    @classmethod
    def init(cls, *_args, **_kwargs):
        del _args, _kwargs

    @classmethod
    def capture_exception(cls, exception: BaseException):
        internal_logger().exception(
            msg=f"[ABSTRA_LOGGER] Exception captured: {exception}"
        )

    @classmethod
    def capture_message(cls, message):
        internal_logger().info(f"[ABSTRA_LOGGER] Message captured: {message}")

    @classmethod
    def flush(cls):
        pass


LoggerEnvironment = Literal["cloud", "local"]


def _format(message: str, attrs: Optional[Dict[str, Any]]) -> str:
    """Append non-null attrs as `k=v k=v ...` after the message, separated by ` | `."""
    if not attrs:
        return message
    pairs = []
    for k, v in attrs.items():
        if v is None:
            continue
        if isinstance(v, (str, int, float, bool)):
            pairs.append(f"{k}={v}")
        else:
            pairs.append(f"{k}={json.dumps(v, default=str)}")
    return f"{message} | {' '.join(pairs)}" if pairs else message


class AbstraLogger:
    environment: LoggerEnvironment = "local"

    @classmethod
    def init(cls, environment: Optional[LoggerEnvironment]):
        cls.environment = environment or "local"
        logging.basicConfig(level=LOGLEVEL(), format=LOGFORMAT())

        # Silence verbose dependencies
        logging.getLogger("pika").setLevel(NOISY_LOGLEVEL())
        logging.getLogger("werkzeug").setLevel(NOISY_LOGLEVEL())

        try:
            cls.get_sdk().init(
                dsn="https://9bbccd1a46ddb8a563483c6afc61ca35@o1317386.ingest.us.sentry.io/4507024713383936",
                traces_sample_rate=0.01,
                profiles_sample_rate=0.01,
                environment=cls.environment,
                enable_tracing=True,
                sample_rate=CLOUD_SAMPLE_RATE
                if AbstraLogger.environment == "cloud"
                else LOCAL_SAMPLE_RATE,
                release=importlib.metadata.distribution("abstra").version,
                shutdown_timeout=0,
                disabled_integrations=[
                    LoggingIntegration(),
                ],
            )
        except Exception:
            internal_logger().error(
                "[ABSTRA_LOGGER] Error reporting has been turned off."
            )

    @classmethod
    def capture_exception(cls, exception: BaseException):
        cls.get_sdk().capture_exception(exception)
        cls.get_sdk().flush()

    @classmethod
    def capture_message(cls, message: str):
        cls.get_sdk().capture_message(message)
        cls.get_sdk().flush()

    @classmethod
    def warning(cls, message: str, attrs: Optional[Dict[str, Any]] = None):
        internal_logger().warning(_format(message, attrs))

    @classmethod
    def info(cls, message: str, attrs: Optional[Dict[str, Any]] = None):
        internal_logger().info(_format(message, attrs))

    @classmethod
    def debug(cls, message: str, attrs: Optional[Dict[str, Any]] = None):
        internal_logger().debug(_format(message, attrs))

    @classmethod
    def error(cls, message: str, attrs: Optional[Dict[str, Any]] = None):
        internal_logger().error(_format(message, attrs))

    # High-volume lifecycle logging emits a single-line JSON object shaped like
    # `tracing-subscriber`'s output ({timestamp, level, fields, target}) so Fluent
    # Bit's Merge_Log lifts attrs into top-level Elasticsearch fields under
    # `log_processed.fields.*` — same query path as central-scheduler/dispatcher.
    #
    # Writes directly to fd 1 via os.write() so the line is unaffected by:
    # (a) StdioPatcher's monkey-patching of sys.stdout.write — fd 1 is what Docker
    #     captures, and os.write goes there directly, never touching sys.stdout. This
    #     means lifecycle calls inside `with SDKContext(...)` blocks DON'T leak into
    #     the user-facing execution-logs view via BroadcastController, and
    # (b) ABSTRA_LOGLEVEL — internal lifecycle logging always emits regardless of
    #     the Python logger's level.
    # os.write() is atomic for buffers <= PIPE_BUF (typically 4096 bytes on Linux),
    # which comfortably covers any realistic lifecycle line.
    @classmethod
    def lifecycle(cls, message: str, attrs: Optional[Dict[str, Any]] = None):
        fields: Dict[str, Any] = {"message": message}
        if attrs:
            for k, v in attrs.items():
                if v is not None:
                    fields[k] = v
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": "INFO",
            "fields": fields,
            "target": "abstra_internal",
        }
        try:
            os.write(1, (json.dumps(payload, default=str) + "\n").encode("utf-8"))
        except Exception:
            pass

    @classmethod
    def get_sdk(cls):
        if is_test_env() or is_dev_env():
            return DevSDK

        return sentry_sdk
