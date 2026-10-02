#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
HTTP Client functionality for FeatrixSphere API.

This module provides the base HTTP client mixin that handles all
communication with the FeatrixSphere server.
"""

import json
import sys
import time
import logging
import requests
from typing import Dict, Any, Optional, BinaryIO
from requests.exceptions import HTTPError, ConnectionError, Timeout
from .exceptions import FeatrixAuthenticationError, FeatrixPredictionError

logger = logging.getLogger(__name__)

# Server auto-clears stale upgrade locks after 15 min; we wait a bit longer.
# Forensic metadata for a prediction (who asked, for which job/model):
# stored on the server's prediction record, never sent to the model. A
# header, because on most predict routes the JSON body IS the record.
CUSTOMER_METADATA_HEADER = "X-Featrix-Customer-Metadata"


def customer_metadata_headers(customer_metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """{CUSTOMER_METADATA_HEADER: json} for a predict call, or {} when there
    is none. The server rejects anything but a JSON object of <= 16 KB."""
    if customer_metadata is None:
        return {}
    if not isinstance(customer_metadata, dict):
        raise TypeError(f"customer_metadata must be a dict, got {type(customer_metadata).__name__}")
    return {CUSTOMER_METADATA_HEADER: json.dumps(customer_metadata, default=str)}


_NODE_UPGRADE_MAX_WAIT_SECONDS = 20 * 60
_NODE_UPGRADE_RETRY_DELAY_SECONDS = 15.0

# sphere-api-router's org job-queue-limit (quota_exceeded) is a depth cap, not
# a timed window — it clears only when one of the org's own pending jobs gets
# dispatched, which depends on other orgs' fair-queue rotation and how long
# whatever's currently running takes. That can easily outlast the normal
# upload retry budget when a caller kicks off a big batch of trainings at
# once (queues 8+, hits the cap, waits for earlier ones to start). Wait it
# out like a node upgrade — one friendly announcement, not a WARNING log per
# retry — instead of guessing via exponential backoff and giving up early.
_ORG_QUEUE_MAX_WAIT_SECONDS = 60 * 60
_ORG_QUEUE_FALLBACK_RETRY_DELAY_SECONDS = 15.0

# Server returns 503 with these `detail.status` values to signal "model not ready
# yet" — e.g. predictor is mid-training, no checkpoint written. Not transient;
# retrying won't help. Caller surfaces it via PredictionResult.training_status.
TRAINING_IN_PROGRESS_STATUSES = frozenset({
    "training_in_progress_no_checkpoint",
    "training_in_progress",
    "training_not_started",
    "no_training_started",
})


def _retry_after_seconds(response: Optional[requests.Response]) -> Optional[float]:
    """Parse the Retry-After header into seconds. Supports delta-seconds form only."""
    if response is None:
        return None
    raw = response.headers.get('Retry-After') if response.headers else None
    if not raw:
        return None
    try:
        secs = float(raw.strip())
    except (TypeError, ValueError):
        return None
    if secs <= 0:
        return None
    return min(secs, 120.0)


def _is_stalled_node_busy(response: Optional[requests.Response]) -> bool:
    """True if this 409 is the router/node "no capacity anywhere, try again" signal.

    src/api.py's `_check_gpu_busy()` returns 409 with `detail="stalled-node-busy"`
    when every usable GPU is below the training-admission floor; sphere-api-router
    re-dispatches across all other nodes first and only lets this escape to the
    client once every node has said the same thing. It means "no capacity right
    now", not "this request is invalid" — safe (and correct) to retry with
    backoff, unlike other 409 uses on this API (e.g. duplicate-dispatch-blocked,
    resource-already-exists) which are permanent/informational, not transient.
    """
    if response is None or response.status_code != 409:
        return False
    try:
        body = response.json()
    except (ValueError, AttributeError):
        return False
    return isinstance(body, dict) and body.get('detail') == 'stalled-node-busy'


def _quota_exceeded_info(response: Optional[requests.Response]) -> Optional[Dict[str, Any]]:
    """Return the response body if this 429 is sphere-api-router's org
    job-queue-limit signal (`quota_exceeded`: this org already has
    `pending_count` jobs queued, at its `queue_limit`), else None. Distinct
    from other 429s on this API (e.g. the per-org predict concurrency
    limiter) which are short, timed, and fine to retry with the normal
    upload budget.
    """
    if response is None or response.status_code != 429:
        return None
    try:
        body = response.json()
    except (ValueError, AttributeError):
        return None
    return body if isinstance(body, dict) and body.get('quota_exceeded') else None


def _extract_training_status(response: requests.Response) -> Optional[Dict[str, Any]]:
    """Return the status dict if response is a soft-503 training-in-progress signal, else None.

    Documented, contractual shape (docs/internal/misc/PREDICTION_API_RESPONSES.md):
    the status fields (`status`, `message`, `training_info`, ...) live at the
    TOP LEVEL of the body, not nested under `detail`. Also checks the legacy
    `detail`-nested shape for compute nodes mid-rollout of the api.py fix.
    """
    if response is None or response.status_code != 503:
        return None
    try:
        body = response.json()
    except (ValueError, AttributeError):
        return None
    if not isinstance(body, dict):
        return None
    if body.get('status') in TRAINING_IN_PROGRESS_STATUSES:
        return body
    detail = body.get('detail')
    if isinstance(detail, dict) and detail.get('status') in TRAINING_IN_PROGRESS_STATUSES:
        return detail
    return None


class HTTPClientMixin:
    """
    Mixin providing HTTP client functionality.

    Classes using this mixin must have:
        - self._session: requests.Session
        - self._base_url: str
        - self._default_max_retries: int
        - self._default_timeout: int
        - self._retry_base_delay: float
        - self._retry_max_delay: float
    """

    def _make_request(
        self,
        method: str,
        endpoint: str,
        max_retries: Optional[int] = None,
        max_retry_time: Optional[float] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint (e.g., "/session/123/predict")
            max_retries: Maximum retry attempts
            max_retry_time: Maximum total retry time in seconds
            **kwargs: Additional arguments passed to requests

        Returns:
            Response object

        Raises:
            HTTPError: If request fails after retries
        """
        if max_retries is None:
            max_retries = self._default_max_retries

        # Auto-add /compute prefix for session endpoints
        if endpoint.startswith('/session/') and not endpoint.startswith('/compute/session/'):
            endpoint = f"/compute{endpoint}"

        # Special handling for upload endpoints
        is_upload = '/upload_with_new_session' in endpoint
        if is_upload:
            if 'timeout' not in kwargs:
                kwargs['timeout'] = 600  # 10 minutes for uploads
            if max_retry_time is None:
                # Rolling node upgrades / busy backends can hold an upload endpoint at a
                # steady 502/503/504 for 10+ minutes straight (observed: 9 attempts, 720s,
                # all 504 — the previous 600s budget was exhausted mid-outage). Match the
                # same order of magnitude as _NODE_UPGRADE_MAX_WAIT_SECONDS so a large
                # foundation upload doesn't die while the server is still recovering.
                max_retry_time = 1800.0
        else:
            if 'timeout' not in kwargs:
                kwargs['timeout'] = self._default_timeout
            if max_retry_time is None:
                max_retry_time = 120.0

        url = f"{self._base_url}{endpoint}"
        start_time = time.time()
        attempt = 0
        last_error = None
        node_upgrading_announced = False
        queue_wait_announced = False

        while True:
            attempt += 1
            elapsed = time.time() - start_time

            try:
                response = self._session.request(method, url, **kwargs)
                response.raise_for_status()
                if attempt > 1:
                    logger.info(
                        f"Recovered: {method} {endpoint} succeeded after "
                        f"{attempt} attempts ({time.time() - start_time:.1f}s)"
                    )
                if node_upgrading_announced:
                    print("Node upgrade complete, resuming.", file=sys.stderr, flush=True)
                if queue_wait_announced:
                    print("Queue slot freed up, resuming.", file=sys.stderr, flush=True)
                return response

            except HTTPError as e:
                last_error = e
                status_code = e.response.status_code if e.response is not None else None

                # Auth failure — don't retry, raise a clear error
                if status_code == 401:
                    try:
                        detail = e.response.json().get('error', '')
                    except Exception:
                        detail = ''
                    msg = detail or (
                        "Authentication required. "
                        "Set your API key in ~/.featrix (as api_key=sk_live_...) "
                        "or the FEATRIX_API_KEY environment variable."
                    )
                    raise FeatrixAuthenticationError(msg, status_code=401) from e

                # Extract server error detail (used for upgrade detection and re-raising).
                # Compute nodes return 503 for NodeUpgradingException; older nodes returned 500.
                detail = ''
                if status_code in (500, 503) and e.response is not None:
                    try:
                        body = e.response.json()
                        detail = body.get('detail', '') or body.get('error', '')
                        if isinstance(detail, dict):
                            detail = detail.get('message', '') or detail.get('detail', '') or ''
                    except Exception:
                        detail = ''

                # Node upgrading — wait it out instead of failing after a few retries.
                # Accept 500 (legacy) and 503 (current). Honor Retry-After if present.
                is_upgrading = (
                    status_code in (500, 503)
                    and isinstance(detail, str)
                    and ('NodeUpgradingException' in detail or 'is currently upgrading' in detail)
                )
                if is_upgrading:
                    if elapsed < _NODE_UPGRADE_MAX_WAIT_SECONDS:
                        if not node_upgrading_announced:
                            print(
                                "Your assigned node is upgrading, stand by....",
                                file=sys.stderr,
                                flush=True,
                            )
                            node_upgrading_announced = True
                        delay = _retry_after_seconds(e.response) or _NODE_UPGRADE_RETRY_DELAY_SECONDS
                        time.sleep(delay)
                        continue

                # Org job-queue is full — wait it out on its own, more patient
                # budget rather than the general 429 handling below (which is
                # sized for short, timed limiters, not "wait for one of your
                # own queued jobs to dispatch").
                quota_info = _quota_exceeded_info(e.response)
                if quota_info is not None:
                    if elapsed < _ORG_QUEUE_MAX_WAIT_SECONDS:
                        if not queue_wait_announced:
                            pending = quota_info.get('pending_count')
                            limit = quota_info.get('queue_limit')
                            print(
                                f"Organization job queue is full ({pending}/{limit} pending) — "
                                "waiting for a slot to free up...",
                                file=sys.stderr,
                                flush=True,
                            )
                            queue_wait_announced = True
                        delay = _retry_after_seconds(e.response) or _ORG_QUEUE_FALLBACK_RETRY_DELAY_SECONDS
                        time.sleep(delay)
                        continue
                    logger.warning(
                        f"Organization job queue still full on {method} {endpoint} after "
                        f"{elapsed:.0f}s — giving up"
                    )
                    raise

                # Soft-503: training-in-progress signal. Don't retry, don't raise —
                # return the response so callers (e.g. predict()) can surface it.
                if status_code == 503 and _extract_training_status(e.response) is not None:
                    return e.response

                # Retry on certain status codes. 429 (rate limited — e.g.
                # sphere-api-router's per-org predict concurrency limiter)
                # honors Retry-After when the server sends one instead of
                # guessing via exponential backoff, and always logs at
                # WARNING (not DEBUG like the transient 5xx codes below) —
                # a 429 means the caller is genuinely exceeding a quota, which
                # is worth surfacing even when the retry succeeds. 409 is only
                # retried for the specific stalled-node-busy signal (checked
                # below) — other 409 uses on this API are permanent, not
                # transient, and must still raise immediately.
                is_stalled_busy = status_code == 409 and _is_stalled_node_busy(e.response)
                if status_code in (429, 500, 502, 503, 504) or is_stalled_busy:
                    # For uploads, gate on max_retry_time only — a large upload that hits
                    # a transient 5xx mid session-creation shouldn't burn its whole retry
                    # budget on just 5 attempts. Mirrors the ConnectionError/Timeout branch.
                    attempts_ok = is_upload or (attempt < max_retries)
                    if attempts_ok and elapsed < max_retry_time:
                        retry_after = _retry_after_seconds(e.response) if status_code == 429 else None
                        delay = retry_after if retry_after is not None else min(
                            self._retry_base_delay * (2 ** (attempt - 1)),
                            self._retry_max_delay
                        )
                        if status_code == 429:
                            logger.warning(
                                f"HTTP 429 rate limited on {method} {endpoint}, "
                                f"retrying in {delay:.1f}s (attempt {attempt}/{max_retries})"
                            )
                        else:
                            logger.debug(
                                f"HTTP {status_code} on {method} {endpoint}, "
                                f"retrying in {delay:.1f}s (attempt {attempt}, elapsed {elapsed:.0f}s)"
                            )
                        time.sleep(delay)
                        continue
                    logger.warning(
                        f"HTTP {status_code} on {method} {endpoint} after "
                        f"{attempt} attempts ({elapsed:.1f}s) — giving up"
                    )

                if status_code == 500 and detail:
                    raise FeatrixPredictionError(detail, status_code=500) from e
                raise

            except (ConnectionError, Timeout) as e:
                last_error = e

                # If we're already in a known node-upgrade window, the node may close
                # the TLS connection mid-request as it cycles. Treat connection errors
                # as "still upgrading" and keep waiting at the upgrade cadence rather
                # than burning the small max_retries budget.
                if node_upgrading_announced and elapsed < _NODE_UPGRADE_MAX_WAIT_SECONDS:
                    logger.warning(
                        f"Connection error on {method} {endpoint} during node upgrade, "
                        f"waiting {_NODE_UPGRADE_RETRY_DELAY_SECONDS:.0f}s before retry"
                    )
                    time.sleep(_NODE_UPGRADE_RETRY_DELAY_SECONDS)
                    continue

                # For uploads, gate on max_retry_time only — a 24MB upload that dies
                # mid-stream from a transient TLS reset shouldn't burn 5 quick attempts.
                # For non-uploads, keep the original max_retries cap.
                attempts_ok = is_upload or (attempt < max_retries)
                if attempts_ok and elapsed < max_retry_time:
                    delay = min(
                        self._retry_base_delay * (2 ** (attempt - 1)),
                        self._retry_max_delay
                    )
                    logger.debug(
                        f"Connection error on {method} {endpoint}, "
                        f"retrying in {delay:.1f}s (attempt {attempt}, elapsed {elapsed:.0f}s)"
                    )
                    time.sleep(delay)
                    continue
                logger.warning(
                    f"Connection error on {method} {endpoint} after "
                    f"{attempt} attempts ({elapsed:.0f}s) — giving up"
                )
                raise

        # Should not reach here, but just in case
        if last_error:
            raise last_error

    def _unwrap_response(self, response_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unwrap server response, handling wrapper formats.

        The server may wrap responses as:
        - {"response": {...}}
        - {"_meta": {...}, "data": {...}}
        - {"_meta": {...}, "response": {...}}

        Captures server metadata when present.
        """
        if isinstance(response_json, dict):
            if '_meta' in response_json:
                self._last_server_metadata = response_json['_meta']
                if 'data' in response_json:
                    return response_json['data']
                if 'response' in response_json:
                    return response_json['response']
            # Handle response wrapper (no _meta)
            if 'response' in response_json and len(response_json) == 1:
                return response_json['response']
        return response_json

    @property
    def last_server_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Metadata from the most recent server response.

        Contains server info like compute_cluster_time, compute_cluster,
        compute_cluster_version, etc.
        """
        return getattr(self, '_last_server_metadata', None)

    def _get_json(
        self,
        endpoint: str,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a GET request and return JSON response."""
        response = self._make_request("GET", endpoint, max_retries=max_retries, **kwargs)
        result = self._unwrap_response(response.json())
        response.close()
        return result

    def _get_bytes(
        self,
        endpoint: str,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> bytes:
        """Make a GET request and return raw bytes (for binary content like images)."""
        response = self._make_request("GET", endpoint, max_retries=max_retries, **kwargs)
        return response.content

    def _post_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a POST request with JSON data and return JSON response."""
        if data is not None:
            kwargs['json'] = data
        response = self._make_request("POST", endpoint, max_retries=max_retries, **kwargs)
        result = self._unwrap_response(response.json())
        response.close()
        return result

    def _delete_json(
        self,
        endpoint: str,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a DELETE request and return JSON response."""
        response = self._make_request("DELETE", endpoint, max_retries=max_retries, **kwargs)
        result = self._unwrap_response(response.json())
        response.close()
        return result

    def _put_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a PUT request with JSON data and return JSON response."""
        if data is not None:
            kwargs['json'] = data
        response = self._make_request("PUT", endpoint, max_retries=max_retries, **kwargs)
        result = self._unwrap_response(response.json())
        response.close()
        return result

    def _post_multipart(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a POST request with multipart/form-data and return JSON response."""
        response = self._make_request(
            "POST", endpoint,
            data=data, files=files,
            max_retries=max_retries,
            **kwargs
        )
        result = self._unwrap_response(response.json())
        response.close()
        return result


class ClientContext:
    """
    Context object passed to resource classes to access HTTP client.

    This allows resource classes (FoundationalModel, Predictor, etc.) to
    make API calls without directly inheriting from the main client.
    """

    def __init__(self, client: 'HTTPClientMixin'):
        self._client = client

    @property
    def base_url(self) -> str:
        return self._client._base_url

    @property
    def current_project_id(self) -> Optional[str]:
        return getattr(self._client, '_current_project_id', None)

    def get_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._client._get_json(endpoint, **kwargs)

    def post_json(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        return self._client._post_json(endpoint, data, **kwargs)

    def delete_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._client._delete_json(endpoint, **kwargs)

    def put_json(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        return self._client._put_json(endpoint, data, **kwargs)

    def post_multipart(self, endpoint: str, data: Dict[str, Any] = None,
                       files: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        return self._client._post_multipart(endpoint, data, files, **kwargs)

    def get_bytes(self, endpoint: str, **kwargs) -> bytes:
        return self._client._get_bytes(endpoint, **kwargs)

    def dataframe_to_file(self, df) -> tuple:
        return self._client._dataframe_to_file(df)
