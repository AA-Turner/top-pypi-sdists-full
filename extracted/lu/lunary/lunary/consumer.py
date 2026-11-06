import time
import atexit
import json
import requests
import logging
from threading import Thread
import jsonpickle
from .config import get_config

logger = logging.getLogger(__name__)

# The ingestion API can also return free-form exception text. Only these
# fixed messages from its auth and project checks are safe to repeat.
_KNOWN_API_MESSAGES = {
    401: (
        "Invalid API key",
        "This project does not exist",
        "Org API key cannot access this route",
        "Unauthorized access to project",
        "Invalid access token",
    ),
    402: ("Incorrect project id format",),
}

_HTTP_HINTS = {
    400: "The endpoint rejected the request. Check the event format.",
    401: "Authentication failed. Check the project API key.",
    402: "Check the project ID and workspace billing.",
    403: "Access denied. Check project permissions.",
    404: "The ingestion endpoint was not found. Check the API URL.",
    408: "The endpoint timed out waiting for the request.",
    413: "The event batch is too large.",
    422: "The endpoint could not validate the event batch.",
    429: "The endpoint rate-limited the request.",
    502: "The gateway received an invalid upstream response.",
    503: "The ingestion service or gateway is unavailable.",
    504: "The gateway timed out waiting for the ingestion service.",
}


def _http_error_reason(response):
    status = response.status_code
    content = response.content or b""
    if status in _KNOWN_API_MESSAGES and 0 < len(content) <= 4096:
        try:
            body = json.loads(content)
        except (ValueError, RecursionError):
            body = None
        if isinstance(body, dict):
            if status == 402 and body.get("code") == "PAYMENT_REQUIRED":
                return "Payment is required to access this workspace."
            for message in _KNOWN_API_MESSAGES[status]:
                if body.get("message") == message:
                    return message + "."
    if status in _HTTP_HINTS:
        return _HTTP_HINTS[status]
    if 500 <= status < 600:
        return "The server or gateway failed to process the batch."
    return "The endpoint returned an HTTP error."


def _send_error_reason(error, fallback):
    if isinstance(error, requests.exceptions.HTTPError) and error.response is not None:
        return _http_error_reason(error.response), error.response.status_code
    # Requests timeout, TLS and proxy errors can also be ConnectionErrors.
    for error_class, reason in (
        (requests.exceptions.ConnectTimeout, "The connection timed out."),
        (requests.exceptions.ReadTimeout, "The endpoint did not respond in time."),
        (requests.exceptions.Timeout, "The request timed out."),
        (requests.exceptions.SSLError, "The TLS connection failed. Check certificate trust."),
        (requests.exceptions.ProxyError, "The connection through the proxy failed."),
        (requests.exceptions.ConnectionError, "The connection to the ingestion endpoint failed."),
    ):
        if isinstance(error, error_class):
            return reason, "n/a"
    return fallback, "n/a"


class Consumer(Thread):
    def __init__(self, event_queue, app_id=None):
        self.running = True
        self.event_queue = event_queue
        self.app_id = app_id

        Thread.__init__(self, daemon=True)
        atexit.register(self.stop)

    def run(self):
        while self.running:
            self.send_batch()
            time.sleep(0.5)

        self.send_batch()

    def send_batch(self):
        config = get_config()
        batch = self.event_queue.get_batch()

        verbose = config.verbose
        api_url = config.api_url


        if len(batch) > 0:
            token = batch[0].get("appId") or self.app_id or config.app_id
            if not token:
                logger.error("API key not found. Please provide an API key.")
                return

    
            logger.debug(f"Sending {len(batch)} events.")

            fallback = "The SDK could not encode the event batch."
            try:
                logger.debug(f"Sending events to {api_url}")

                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            
                data = jsonpickle.encode({"events": batch}, unpicklable=False)
                fallback = "The SDK could not complete the ingestion request."
                response = requests.post(
                    api_url + "/v1/runs/ingest",
                    data=data,
                    headers=headers,
                    verify=config.ssl_verify)
                response.raise_for_status()

                logger.debug("Events sent. status_code=%s", response.status_code)
            except Exception as e:
                reason, http_status = _send_error_reason(e, fallback)
                logger.error(
                    "Error sending events. %s Batch will not be retried. "
                    "error_type=%s http_status=%s batch_size=%d.",
                    reason,
                    type(e).__name__,
                    http_status,
                    len(batch),
                    exc_info=verbose,
                )

    def stop(self):
        self.running = False
        self.join()
