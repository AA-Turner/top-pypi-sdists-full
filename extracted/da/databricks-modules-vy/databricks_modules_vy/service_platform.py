"""Utilities for Service Platform API access and raw landing support.

This module contains:
- Authentication and request/retry handling via ``ServicePlatformApi``.
- Helpers for creating and maintaining landing run paths in Unity Catalog volumes.
- JSON writers for raw API landing.

The landing-oriented helpers are primarily intended for APIs with many pages,
where responses accumulate into large payload volumes and landing raw responses
first gives better stability and recovery options.
"""

import datetime as dt
import json
import random
import time
import uuid
from dataclasses import dataclass
from typing import Any, Iterable

import requests

import databricks_modules_vy.logging as log_utils


def _json_default(value: Any) -> str:
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _serialize_json_compact(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=_json_default)


@dataclass
class TokenConfig:
    """A simple dataclass to hold the configuration for the Service Platform API.

    Attributes:
        client_id (str): The client ID for the Service Platform API.
        client_secret (str): The client secret for the Service Platform API.
        access_token_url (str): The URL for the access token endpoint.
            i.e. "https://auth.cognito.vydev.io/oauth2/token"
        scopes (str | Iterable[str]): Scope value(s) to authenticate with.
            A single string is used as-is, while an iterable is joined with
            spaces for the OAuth token request.
    """

    client_id: str
    client_secret: str
    access_token_url: str
    scopes: str | Iterable[str]


def volume_fqn_to_path(volume_fqn: str) -> str:
    """Convert a Unity Catalog volume FQN to a Databricks volume path.

    Args:
        volume_fqn (str): Volume identifier in the format
            "<catalog>.<schema>.<volume>".

    Returns:
        str: Databricks volume path in the format
            "/Volumes/<catalog>/<schema>/<volume>".

    Raises:
        ValueError: If ``volume_fqn`` is not in the expected three-part format.

    Example:
        person.catalog.raw_landing -> /Volumes/person/catalog/raw_landing
    """
    parts = volume_fqn.split(".")
    if len(parts) != 3:
        raise ValueError(
            "volume_fqn must be in format '<catalog>.<schema>.<volume>', " f"got '{volume_fqn}'"
        )
    return f"/Volumes/{parts[0]}/{parts[1]}/{parts[2]}"


def build_landing_run_paths(
    volume_fqn: str, dataset_name: str, run_timestamp: dt.datetime | None = None
) -> tuple[str, str]:
    """Build a dataset root path and a unique run path for raw API landing.

    Args:
        volume_fqn (str): Volume identifier in the format
            "<catalog>.<schema>.<volume>".
        dataset_name (str): Dataset subfolder under the volume root.
        run_timestamp (datetime.datetime | None): UTC timestamp used to build
            date and run identifiers. If ``None``, current UTC time is used.

    Returns:
        tuple[str, str]:
            - dataset_root_path: Root path for the dataset.
            - run_path: Unique run folder under ``date=YYYY-MM-DD/run=<run_id>``.
    """
    run_timestamp = run_timestamp or dt.datetime.now(dt.timezone.utc)
    date_folder = run_timestamp.strftime("%Y-%m-%d")
    run_id = f"{run_timestamp.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"

    dataset_root_path = f"{volume_fqn_to_path(volume_fqn)}/{dataset_name}"
    run_path = f"{dataset_root_path}/date={date_folder}/run={run_id}"
    return dataset_root_path, run_path


def cleanup_landing_runs_by_count(
    dbutils: Any, dataset_root_path: str, keep_last_runs: int
) -> list[str]:
    """Delete old landed runs and keep only the newest N run folders.

    Args:
        dbutils (Any): Databricks ``dbutils`` object.
        dataset_root_path (str): Dataset landing root path that contains
            ``date=*`` folders.
        keep_last_runs (int): Number of most recent runs to retain.

    Returns:
        list[str]: Deleted run paths.

    Raises:
        ValueError: If ``keep_last_runs`` is less than 1.
    """
    if keep_last_runs < 1:
        raise ValueError("keep_last_runs must be >= 1")

    try:
        date_dirs = [
            item.path
            for item in dbutils.fs.ls(dataset_root_path)
            if item.path.rstrip("/").split("/")[-1].startswith("date=")
        ]
    except Exception:
        return []

    run_paths: list[str] = []
    for date_dir in sorted(date_dirs, reverse=True):
        try:
            runs_in_date = [
                item.path
                for item in dbutils.fs.ls(date_dir)
                if item.path.rstrip("/").split("/")[-1].startswith("run=")
            ]
        except Exception:
            continue
        run_paths.extend(sorted(runs_in_date, reverse=True))

    if len(run_paths) <= keep_last_runs:
        return []

    paths_to_delete = run_paths[keep_last_runs:]
    for path in paths_to_delete:
        dbutils.fs.rm(path, True)

    # Remove now-empty date folders to keep the landing tree tidy.
    for date_dir in date_dirs:
        try:
            children = dbutils.fs.ls(date_dir)
        except Exception:
            continue

        if not children:
            try:
                dbutils.fs.rm(date_dir, True)
            except Exception:
                pass

    return paths_to_delete


def get_latest_landing_run_path(dbutils: Any, volume_fqn: str, dataset_name: str) -> str | None:
    """Get the most recent run path for a landed dataset.

    Args:
        dbutils (Any): Databricks ``dbutils`` object.
        volume_fqn (str): Volume identifier in the format
            "<catalog>.<schema>.<volume>".
        dataset_name (str): Dataset subfolder under the volume root.

    Returns:
        str | None: Latest run path, or ``None`` when no runs are found.
    """
    dataset_root_path = f"{volume_fqn_to_path(volume_fqn)}/{dataset_name}"

    try:
        date_dirs = [
            item.path
            for item in dbutils.fs.ls(dataset_root_path)
            if item.path.rstrip("/").split("/")[-1].startswith("date=")
        ]
    except Exception:
        return None

    if not date_dirs:
        return None

    for date_dir in sorted(date_dirs, reverse=True):
        try:
            run_dirs = [
                item.path
                for item in dbutils.fs.ls(date_dir)
                if item.path.rstrip("/").split("/")[-1].startswith("run=")
            ]
        except Exception:
            continue

        if run_dirs:
            return sorted(run_dirs, reverse=True)[0]

    return None


def write_json_to_volume(
    dbutils: Any,
    file_path: str,
    payload: dict[str, Any],
    overwrite: bool = True,
    max_attempts: int = 3,
    backoff_seconds: float = 1.0,
) -> None:
    """Write a JSON payload to a volume path with retry.

    Args:
        dbutils (Any): Databricks ``dbutils`` object.
        file_path (str): Target file path.
        payload (dict[str, Any]): JSON-serializable payload to write.
        overwrite (bool): Whether to overwrite existing file at ``file_path``.
        max_attempts (int): Maximum write attempts before failing.
        backoff_seconds (float): Base backoff in seconds used between retries.

    Raises:
        Exception: Re-raises the final write exception if all attempts fail.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    body = _serialize_json_compact(payload)

    for attempt in range(1, max_attempts + 1):
        try:
            dbutils.fs.put(file_path, body, overwrite)
            return
        except Exception:
            if attempt >= max_attempts:
                raise
            sleep_seconds = backoff_seconds * (2 ** (attempt - 1))
            time.sleep(sleep_seconds)


def estimate_json_payload_bytes(payload: dict[str, Any]) -> int:
    """Estimate UTF-8 byte size of a compact JSON payload."""
    return len(_serialize_json_compact(payload).encode("utf-8"))


def write_json_lines_to_volume(
    dbutils: Any,
    file_path: str,
    payloads: list[dict[str, Any]],
    overwrite: bool = True,
    max_attempts: int = 3,
    backoff_seconds: float = 1.0,
) -> None:
    """Write newline-delimited JSON payloads to a volume path with retry."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    body = "\n".join(_serialize_json_compact(payload) for payload in payloads)
    if body:
        body += "\n"

    for attempt in range(1, max_attempts + 1):
        try:
            dbutils.fs.put(file_path, body, overwrite)
            return
        except Exception:
            if attempt >= max_attempts:
                raise
            sleep_seconds = backoff_seconds * (2 ** (attempt - 1))
            time.sleep(sleep_seconds)


class ServicePlatformApi:
    """Class to interact with the Service Platform API.

    This class provides methods to handle authentication and make HTTP GET and POST requests
    to the Service Platform API. It uses OAuth2 client credentials flow to obtain access tokens.

    Attributes:
        api_url (str): The base URL for the Service Platform API.
        token_config (TokenConfig): The configuration details for token generation.
    """

    def __init__(self, api_url: str, token_config: TokenConfig):
        """Initialize the ServicePlatformApi class.

        Args:
            api_url (str): The base URL for the Service Platform API.
            token_config (TokenConfig): An instance of TokenConfig containing authentication details.

        Raises:
            Exception: If the token generation fails.
        """
        self._api_url = api_url
        self._token_config = token_config
        self._session = requests.Session()
        self._max_retries = 5
        self._backoff_factor_seconds = 1.0
        self._max_backoff_seconds = 30.0
        self._token_max_retries = 3
        self._token_timeout_seconds = 30
        self._retryable_status_codes = {408, 425, 429, 500, 502, 503, 504}
        self._access_token = self._get_access_token()

    def _scope_value(self) -> str:
        """Return OAuth scope(s) as a single space-delimited string.

        Returns:
            str: Scope value suitable for token request payload.
        """
        if isinstance(self._token_config.scopes, str):
            return self._token_config.scopes
        return " ".join(self._token_config.scopes)

    def _sleep_with_backoff(self, attempt: int) -> None:
        """Sleep using exponential backoff with jitter.

        Args:
            attempt (int): 1-based retry attempt number.
        """
        exponential = self._backoff_factor_seconds * (2 ** (attempt - 1))
        jitter = random.uniform(0, 1)
        sleep_seconds = min(self._max_backoff_seconds, exponential + jitter)
        time.sleep(sleep_seconds)

    def _request_with_retry(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> requests.Response:
        """Execute an HTTP request with retry and token-refresh handling.

        Args:
            method (str): HTTP method, for example ``GET`` or ``POST``.
            path (str): Endpoint path relative to ``self._api_url``.
            params (dict[str, Any] | None): Query string parameters.
            json_payload (dict[str, Any] | None): JSON request body.
            headers (dict[str, str] | None): Additional request headers.
            timeout (int): Request timeout in seconds.

        Returns:
            requests.Response: Successful HTTP response.

        Raises:
            requests.exceptions.RequestException: If all retries fail.
            RuntimeError: If an unexpected retry state is reached.
        """
        request_headers = dict(headers or {})
        request_headers["Authorization"] = f"Bearer {self._access_token}"

        refresh_token_once = True

        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._session.request(
                    method=method,
                    url=self._api_url + path,
                    params=params,
                    json=json_payload,
                    headers=request_headers,
                    timeout=timeout,
                )
            except requests.exceptions.RequestException:
                if attempt >= self._max_retries:
                    raise
                self._sleep_with_backoff(attempt)
                continue

            if response.status_code == 401 and refresh_token_once:
                self._access_token = self._get_access_token()
                request_headers["Authorization"] = f"Bearer {self._access_token}"
                refresh_token_once = False
                continue

            if response.ok:
                return response

            if response.status_code in self._retryable_status_codes and attempt < self._max_retries:
                log_utils.lp(
                    "Retryable status code "
                    f"{response.status_code} for {method} {path} "
                    f"(attempt {attempt}/{self._max_retries}). Retrying."
                )
                self._sleep_with_backoff(attempt)
                continue

            response.raise_for_status()

        raise RuntimeError("Unexpected retry state reached in _request_with_retry")

    def _get_access_token(self) -> str:
        """Fetch an OAuth access token using client credentials flow.

        Returns:
            str: Access token.

        Raises:
            Exception: If token request fails.
        """
        token_response = None
        for attempt in range(1, self._token_max_retries + 1):
            try:
                token_response = self._session.post(
                    self._token_config.access_token_url,
                    data={"grant_type": "client_credentials", "scope": self._scope_value()},
                    auth=(self._token_config.client_id, self._token_config.client_secret),
                    timeout=self._token_timeout_seconds,
                )

                if (
                    token_response.status_code in self._retryable_status_codes
                    and attempt < self._token_max_retries
                ):
                    self._sleep_with_backoff(attempt)
                    continue

                token_response.raise_for_status()
                return token_response.json()["access_token"]
            except requests.exceptions.RequestException as e:
                if attempt >= self._token_max_retries:
                    if token_response is not None:
                        print(token_response.text)
                    raise e
                self._sleep_with_backoff(attempt)

        raise RuntimeError("Unexpected retry state reached in _get_access_token")

    def post(
        self, path: str, json: dict = None, headers: dict = None, timeout: int = 30
    ) -> requests.Response:
        """Send a POST request to the API.

        Args:
            path (str): The endpoint path (relative to the base URL).
            json (dict, optional): The JSON payload to include in the request. Defaults to None.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.
            timeout (int, optional): The request timeout in seconds. Defaults to 30.

        Returns:
            requests.Response: The response object from the API.

        Raises:
            requests.exceptions.HTTPError: If the API returns an error response.
        """
        request_headers = dict(headers or {})
        request_headers["Connection"] = "keep-alive"
        return self._request_with_retry(
            method="POST", path=path, json_payload=json, headers=request_headers, timeout=timeout
        )

    def get(
        self, path: str, params: dict = None, headers: dict = None, timeout: int = 30
    ) -> requests.Response:
        """Send a GET request to the API.

        Args:
            path (str): The endpoint path (relative to the base URL).
            params (dict, optional): Query parameters to include in the request. Defaults to None.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.
            timeout (int, optional): The request timeout in seconds. Defaults to 30.

        Returns:
            requests.Response: The response object from the API.

        Raises:
            requests.exceptions.HTTPError: If the API returns an error response.
        """
        request_headers = dict(headers or {})
        request_headers["accept"] = "application/json"
        return self._request_with_retry(
            method="GET", path=path, params=params, headers=request_headers, timeout=timeout
        )
