import logging
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def _tag_trace_id(event: dict) -> None:
    if "request" not in event:
        return

    if not isinstance(event["request"], dict):
        return

    url = event["request"].get("url")
    if not isinstance(url, str):
        return

    if not url.endswith("/workflow/stream"):
        return

    body = event["request"].get("data")
    if not isinstance(body, dict):
        return

    execution_context = body.get("execution_context")
    if not isinstance(execution_context, dict):
        return

    trace_id = execution_context.get("trace_id")
    if not isinstance(trace_id, str):
        return

    if "tags" not in event:
        event["tags"] = {}

    event["tags"]["vellum_trace_id"] = trace_id


def before_send(event: dict, hint: dict) -> Optional[dict]:
    if "exc_info" in hint:
        _, _, _ = hint["exc_info"]

    _tag_trace_id(event)

    return event


def init_sentry(*, sentry_log_level: Optional[int], dsn: str) -> None:
    sentry_logging = LoggingIntegration(
        level=sentry_log_level,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    integrations = [sentry_logging]

    sentry_sdk.init(
        dsn=dsn,
        integrations=integrations,
        environment="production",
        traces_sample_rate=0.0,
        send_default_pii=True,
        before_send=before_send,  # type: ignore
        max_request_body_size="always",
        max_value_length=10_000,
    )
