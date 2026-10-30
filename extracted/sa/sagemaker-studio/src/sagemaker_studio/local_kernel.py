"""
AWS Notebook local kernel support.

The AWS Notebook desktop app runs notebooks on a kernel on the user's machine. That kernel has no
SageMaker Unified Studio project behind it: connections and the AWS credentials to use them come
from the app itself, through a loopback HTTP API the app starts for its kernels. Everywhere else
(a SageMaker Unified Studio space, any remote kernel) the SDK behaves as it always has.

How the SDK knows where it is
-----------------------------
The app starts the kernel server with two environment variables, which the kernels inherit:

* ``AWS_NOTEBOOK_APP_URL``: the API's base URL, ``http://127.0.0.1:<port>`` (loopback only);
* ``AWS_NOTEBOOK_APP_TOKEN``: the per-launch token every request carries as
  ``Authorization: Bearer <token>``.

A non-blank ``AWS_NOTEBOOK_APP_URL`` makes this a local kernel (:attr:`RuntimeMode.LOCAL`);
without it the SDK is :attr:`RuntimeMode.REMOTE`. Nothing has to be called at startup.
:func:`configure_local_kernel` exists for embedders and tests that want to point the SDK at an
app explicitly.

What a local kernel does differently
------------------------------------
* Connections resolve by id through the app's ``connections.get`` operation, the analog of
  DataZone's ``GetConnection``: ``POST <url>/api/connections/get`` with
  ``{"identifier": <id>, "withSecret": true}`` returns the connection record with its
  ``connectionCredentials`` (``accessKeyId``, ``secretAccessKey``, ``sessionToken``,
  ``expiration``). ``connections.list`` (``POST <url>/api/connections/list``, a bare array of
  records without credentials, empty when signed out) lists the connections in the signed-in
  session's scope, which is what ``Project().connections`` answers. The app identifies connections
  by id only, so lookups by name or type are not available
  (:class:`~sagemaker_studio.exceptions.UnsupportedInModeError`).
* Credentials come from the app and nowhere else: no AWS profile, shared config/credentials
  file or ``AWS_*`` variable is read by the SDK, and no DataZone client is built. They are asked
  for again shortly before the ``expiration`` the previous answer carried, so long-lived clients
  and SQL engines follow the app's session. DuckDB's ``credential_chain`` secrets reach the same
  session through the kernel server's container credentials endpoint
  (``AWS_CONTAINER_CREDENTIALS_FULL_URI``), so they follow it too.
* Signed out, the app answers ``403 AccessDeniedException``; the SDK raises
  :class:`~sagemaker_studio.exceptions.CredentialsUnavailableError` with the app's message
  before any AWS call. Every failure body is ``{"error": {"code", "message"}}``.
* ``pandas.read_catalog_table`` and ``DataFrame.to_catalog_table`` are not installed: both go
  through the project's default connection, which a local kernel does not have.

SQL on a local kernel
---------------------
The notebook frontend forwards the id of the connection attached to a cell as
``sqlutils.sql(..., connection_id=...)``; a cell with no connection calls ``sqlutils.sql(...)``.

* A ``LAKEHOUSE`` catalog connection whose ``configurations`` carry
  ``{"classification": "athena", "properties": {"workgroupName": ...}}`` runs on Athena with that
  workgroup (``Connection.sql_engine_type == "ATHENA"``); the connection's top-level ``catalog``,
  when present, is the Athena catalog unless the query names one. ``ATHENA`` connections keep
  working.
* An ``S3`` connection is not a DuckDB source in any mode (a cell naming one is refused as on
  SageMaker Unified Studio compute). A cell with no connection reads ``s3://`` with the engine's
  one ``credential_chain`` secret, which resolves the signed-in session through the kernel server's
  container credentials; ``sqlutils.attach_local_catalogs()`` re-creates it on sign-in and profile
  switch, ``detach_local_catalogs()`` drops it on sign-out, and a signed-out read is refused before
  it runs.
* ``sqlutils.attach_local_catalogs()`` attaches every ``LAKEHOUSE`` connection's Glue catalogs and
  every ``ATHENA`` connection's workgroup to that DuckDB under the Data Explorer's names, afresh on
  each call, signing with ``credential_chain`` secrets; see
  :mod:`sagemaker_studio.sql_engine.duckdb_engine.catalogs`.
* Apart from those secrets, nothing the SDK keeps between cells holds credentials: SQL engines are
  built per statement (``persist_session`` is ignored); a ``Connection`` or ``create_client()``
  client the notebook keeps asks the app again before its ``expiration``.

Errors
------
All are :class:`~sagemaker_studio.exceptions.StudioContextError`\\ s:
:class:`~sagemaker_studio.exceptions.UnsupportedInModeError` (a lookup the app cannot serve),
:class:`~sagemaker_studio.exceptions.CredentialsUnavailableError` (signed out),
:class:`~sagemaker_studio.exceptions.CredentialsExpiredError` (AWS named the token inside a
query: ``ExpiredToken``, ``InvalidAccessKeyId``, ``SignatureDoesNotMatch``),
:class:`~sagemaker_studio.exceptions.AccessDeniedError` (any other ``403`` inside a query, naming
the location and who was refused: the signed-in identity, or the access role the catalogs the
statement ran against sign with),
:class:`~sagemaker_studio.exceptions.LocalAppError` (the app answered an error envelope:
``.code``, ``.status``, ``.detail``) and
:class:`~sagemaker_studio.exceptions.LocalAppUnavailableError` (the app could not be reached).
:func:`current_context` reports the mode and whether the app was last found signed in (by
``sqlutils.attach_local_catalogs()``, from what the credential chain resolved, or by a
connection's credential request); :func:`configure_local_kernel` / :func:`reset_local_kernel`
point the SDK at an app explicitly, for embedders and tests.
"""

from __future__ import annotations

import http.client
import json
import logging
import os
import re
import threading
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional

from sagemaker_studio.exceptions import LocalAppError, LocalAppUnavailableError

logger = logging.getLogger(__name__)

#: The app's API base URL (``http://127.0.0.1:<port>``), set by the app for its kernels.
APP_URL_ENV_VAR = "AWS_NOTEBOOK_APP_URL"
#: The bearer token every request to the app's API carries.
APP_TOKEN_ENV_VAR = "AWS_NOTEBOOK_APP_TOKEN"
#: Operations live at ``<url>/api/<family>/<operation>`` and are called with POST.
API_PREFIX = "/api/"
#: The operation that answers a connection, and with ``withSecret`` its credentials.
CONNECTIONS_GET = "connections/get"
#: The operation that lists the connections in the signed-in session's scope, without credentials.
CONNECTIONS_LIST = "connections/list"
#: Seconds to wait for the app to answer.
DEFAULT_TIMEOUT_SECONDS = 10.0
#: Credentials this close to their ``expiration`` are asked for again before use.
REFRESH_WINDOW = timedelta(minutes=5)
#: Credentials the app hands out without an ``expiration`` are re-checked this often.
DEFAULT_CREDENTIALS_LIFETIME = timedelta(hours=1)

_LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "::1")


class RuntimeMode(Enum):
    """Where the SDK is running."""

    #: An AWS Notebook local kernel: connections and credentials from the app's API.
    LOCAL = 1
    #: Anywhere else (a SageMaker Unified Studio space ...): DataZone, as always.
    REMOTE = 2


@dataclass(frozen=True)
class StudioContext:
    """
    The runtime the SDK is operating in.

    Attributes:
        mode: :attr:`RuntimeMode.LOCAL` or :attr:`RuntimeMode.REMOTE`.
        reason: How the mode was decided, for logs and the UI.
        app_url: The app API's base URL on a local kernel (never the token).
        signed_in: On a local kernel, whether the app was last found signed in: ``True`` when
            the AWS credential chain resolved the app's session as ``sqlutils.attach_local_catalogs()``
            ran, or a connection's credentials were vended; ``False`` when the chain had nothing to
            resolve or the app refused them (signed out); ``None`` when neither has happened yet.
        signed_in_detail: The reason, when ``signed_in`` is ``False`` and one was given.
    """

    mode: RuntimeMode
    reason: str = ""
    app_url: Optional[str] = None
    signed_in: Optional[bool] = None
    signed_in_detail: str = ""

    def describe(self) -> Dict[str, Any]:
        """JSON-friendly summary for the kernel and the UI."""
        return {
            "mode": self.mode.name,
            "reason": self.reason,
            "app_url": self.app_url,
            "signed_in": self.signed_in,
            "signed_in_detail": self.signed_in_detail,
        }


REMOTE_CONTEXT = StudioContext(RuntimeMode.REMOTE, f"{APP_URL_ENV_VAR} is not set")


# --- credentials helpers ----------------------------------------------------------------------


def parse_iso_datetime(value: Any) -> Optional[datetime]:
    """
    ISO 8601 text as a ``datetime`` carrying whatever offset the text does (none for naive
    text). A trailing ``Z`` is accepted, which ``datetime.fromisoformat`` only does from Python
    3.11 on, and fractional seconds of any length are read to microsecond precision (Python 3.10
    accepts exactly 3 or 6 digits; the app's records carry 9, DataZone's wire format). Unreadable
    text is logged and gives ``None``: an expiration the app or a provider wrote in a shape this
    code does not know must not fail the connection lookup.
    """
    text = str(value).strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    text = _FRACTIONAL_SECONDS.sub(_microseconds, text)
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        logger.warning("Ignoring an unreadable credentials expiration: %r", value)
        return None


#: The fractional-seconds field of an ISO 8601 timestamp: a time ``HH:MM:SS`` followed by ``.``
#: or ``,`` and digits (not a date separator or an offset).
_FRACTIONAL_SECONDS = re.compile(r"(?<=\d{2}:\d{2}:\d{2})[.,](\d+)")


def _microseconds(match: "re.Match[str]") -> str:
    """Truncate or zero-pad a fractional-seconds field to the six digits ``fromisoformat`` wants."""
    return "." + match.group(1)[:6].ljust(6, "0")


def parse_expiration(value: Any) -> Optional[datetime]:
    """
    An ``expiration`` as the app or DataZone give it (ISO 8601 text, ``Z`` accepted, or a
    ``datetime``) as an aware UTC ``datetime``; ``None`` when absent or unreadable.
    """
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = parse_iso_datetime(value)
        if parsed is None:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def expires_soon(expiration: Any, window: timedelta = REFRESH_WINDOW) -> bool:
    """Whether credentials with this ``expiration`` should be asked for again before use."""
    parsed = parse_expiration(expiration)
    if parsed is None:
        return False
    return parsed - datetime.now(timezone.utc) <= window


def refreshable_credentials(fetch: Callable[[], Any], method: str = "aws-notebook-app"):
    """
    botocore credentials that call ``fetch`` for fresh keys shortly before they expire.

    ``fetch`` returns an object with ``access_key_id``, ``secret_access_key``, ``session_token``
    and ``expiration`` (a :class:`~sagemaker_studio.connections.connection.ConnectionCredentials`);
    it is called once now and again whenever botocore finds the keys about to expire, so a
    client built on these follows the app's session without being rebuilt. Keys without an
    ``expiration`` are re-checked after :data:`DEFAULT_CREDENTIALS_LIFETIME`.
    """
    from botocore.credentials import RefreshableCredentials

    def refresh() -> Dict[str, Any]:
        creds = fetch()
        if creds is None or not creds.access_key_id or not creds.secret_access_key:
            raise RuntimeError("No AWS credentials were returned for the connection")
        expiration = parse_expiration(getattr(creds, "expiration", None)) or (
            datetime.now(timezone.utc) + DEFAULT_CREDENTIALS_LIFETIME
        )
        return {
            "access_key": creds.access_key_id,
            "secret_key": creds.secret_access_key,
            "token": creds.session_token,
            "expiry_time": expiration.isoformat(),
        }

    return RefreshableCredentials.create_from_metadata(
        metadata=refresh(), refresh_using=refresh, method=method
    )


# --- the app API ------------------------------------------------------------------------------


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """
    Refuse every redirect. urllib's default handler follows a 3xx answer by copying the request
    headers, ``Authorization`` among them, onto a new request for wherever ``Location`` points,
    without checking that host. A redirect to another machine would carry the app's bearer token
    off this one, past the loopback check on the base URL. Returning ``None`` makes urllib raise
    the 3xx as :class:`urllib.error.HTTPError`, which :meth:`AppApiClient.call` reports.
    """

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


class AppApiClient:
    """
    HTTP client for the AWS Notebook app's loopback API.

    Requests go straight to the URL: no proxy from the environment is used, and a redirect is
    refused rather than followed, since the request headers (the token among them) would travel
    with it.

    Args:
        url: The API base URL (``http://127.0.0.1:<port>``). Only http(s) on loopback is
            accepted: the token must never travel further than this machine.
        token: The bearer token. Without one every call fails with a clear error.
        timeout: Seconds to wait for the app.
    """

    def __init__(self, url: str, token: Optional[str], timeout: float = DEFAULT_TIMEOUT_SECONDS):
        self.url = (url or "").strip().rstrip("/")
        self._token = (token or "").strip() or None
        self.timeout = timeout
        self._url_problem = self._check_url(self.url)
        # Loopback only: never route through an HTTP(S)_PROXY from the environment, and never
        # follow a redirect (the bearer token would go with it).
        self._opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), _NoRedirectHandler
        )

    @staticmethod
    def _check_url(url: str) -> Optional[str]:
        if not url:
            return f"{APP_URL_ENV_VAR} is empty"
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return f"{APP_URL_ENV_VAR} must be an http(s) URL, got {url!r}"
        if parsed.hostname not in _LOOPBACK_HOSTS:
            return f"{APP_URL_ENV_VAR} must point at this machine (loopback), got {url!r}"
        return None

    @classmethod
    def from_env(cls, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> Optional["AppApiClient"]:
        """The client the environment describes, or ``None`` when ``AWS_NOTEBOOK_APP_URL`` is unset."""
        url = os.environ.get(APP_URL_ENV_VAR, "").strip()
        if not url:
            return None
        return cls(url, os.environ.get(APP_TOKEN_ENV_VAR), timeout=timeout)

    def call(self, operation: str, body: Mapping[str, Any]) -> Dict[str, Any]:
        """
        Run one operation whose answer is a JSON object (``"connections/get"``) and return it.

        Raises:
            LocalAppError: The app answered an error envelope (its code and message are kept).
            LocalAppUnavailableError: The app could not be reached, the URL or token is not
                usable, the answer was not a JSON object, or the app answered a redirect (never
                followed).
        """
        answer = self._call(operation, body)
        if not isinstance(answer, dict):
            raise LocalAppUnavailableError(
                f"The AWS Notebook app answered a JSON {type(answer).__name__}, not an object "
                f"({operation})"
            )
        return answer

    def call_for_list(self, operation: str, body: Mapping[str, Any]) -> List[Dict[str, Any]]:
        """
        Run one operation whose answer is a bare JSON array of objects (``"connections/list"``,
        which answers DataZone's ``ConnectionSummary[]`` with no envelope around it).

        Raises:
            LocalAppError: The app answered an error envelope.
            LocalAppUnavailableError: As for :meth:`call`, or the answer was not an array of objects.
        """
        answer = self._call(operation, body)
        if not isinstance(answer, list) or not all(isinstance(row, dict) for row in answer):
            raise LocalAppUnavailableError(
                f"The AWS Notebook app answered a JSON {type(answer).__name__}, not an array of "
                f"objects ({operation})"
            )
        return answer

    def _call(self, operation: str, body: Mapping[str, Any]) -> Any:
        """The round trip behind :meth:`call` and :meth:`call_for_list`: any JSON value the app answered."""
        if self._url_problem:
            raise LocalAppUnavailableError(self._url_problem)
        if self._token is None:
            raise LocalAppUnavailableError(
                f"{APP_TOKEN_ENV_VAR} is not set; the AWS Notebook app's API needs its token"
            )
        request = urllib.request.Request(
            f"{self.url}{API_PREFIX}{operation}",
            data=json.dumps(dict(body)).encode("utf-8"),
            method="POST",
        )
        request.add_header("Content-Type", "application/json")
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", f"Bearer {self._token}")
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                answer = self._decode(response.read(), response.status, operation)
        except urllib.error.HTTPError as e:
            raise self._error_from(e, operation) from None
        except (urllib.error.URLError, OSError, http.client.HTTPException) as e:
            # HTTPException (e.g. IncompleteRead when the loopback connection drops mid-body)
            # derives from Exception, not OSError, so it needs naming here.
            raise LocalAppUnavailableError(
                f"Could not reach the AWS Notebook app at {self.url}: {e}"
            ) from e
        envelope = answer.get("error") if isinstance(answer, dict) else None
        if isinstance(envelope, Mapping):  # an envelope with a 200 status; treat it as an error
            raise LocalAppError(
                str(envelope.get("code", "Error")), str(envelope.get("message", "")), 200, operation
            )
        return answer

    def get_connection(self, connection_id: str, with_secret: bool = True) -> Dict[str, Any]:
        """The connection record; with ``with_secret`` also its ``connectionCredentials``."""
        return self.call(
            CONNECTIONS_GET, {"identifier": connection_id, "withSecret": bool(with_secret)}
        )

    def list_connections(self, connection_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        The connection records in the signed-in session's scope, without credentials, optionally
        those of one type. Signed out, the app has nothing in scope and answers an empty array.
        """
        body: Dict[str, Any] = {}
        if connection_type:
            body["type"] = connection_type
        return self.call_for_list(CONNECTIONS_LIST, body)

    def _error_from(self, error: urllib.error.HTTPError, operation: str) -> Exception:
        if 300 <= error.code < 400:
            return LocalAppUnavailableError(
                f"The AWS Notebook app answered HTTP {error.code} with a redirect, which this "
                f"client does not follow ({operation})"
            )
        try:
            body = error.read()
        except Exception:  # noqa: BLE001 - the body is optional here
            body = b""
        try:
            answer = self._decode(body, error.code, operation)
        except LocalAppUnavailableError:
            return LocalAppUnavailableError(
                f"The AWS Notebook app answered HTTP {error.code} without an error envelope "
                f"({operation})"
            )
        envelope = answer.get("error") if isinstance(answer, dict) else None
        if not isinstance(envelope, Mapping):
            return LocalAppUnavailableError(
                f"The AWS Notebook app answered HTTP {error.code} without an error envelope "
                f"({operation})"
            )
        return LocalAppError(
            str(envelope.get("code", f"HTTP_{error.code}")),
            str(envelope.get("message", error.reason or "")),
            error.code,
            operation,
        )

    @staticmethod
    def _decode(body: bytes, status: int, operation: str) -> Any:
        """The JSON value the app answered (an object, or the bare array ``connections/list`` answers)."""
        try:
            return json.loads(body.decode("utf-8")) if body else {}
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise LocalAppUnavailableError(
                f"The AWS Notebook app answered HTTP {status} with a body that is not JSON "
                f"({operation})"
            ) from e

    def __repr__(self) -> str:  # never print the token
        return f"AppApiClient(url={self.url!r}, token={'set' if self._token else 'unset'})"


# --- the kernel -------------------------------------------------------------------------------


class LocalKernel:
    """
    The SDK's view of the AWS Notebook local kernel it runs in: the app's API and what the last
    credential request observed. Created by :func:`local_kernel` from the environment.
    """

    def __init__(self, client: AppApiClient, default_region: Optional[str] = None):
        self.client = client
        self.default_region = default_region
        self._lock = threading.Lock()
        self._signed_in: Optional[bool] = None
        self._signed_in_detail = ""
        self._provider: Any = None

    def observe_credentials(self, vended: bool, detail: str = "") -> None:
        """
        Record whether credentials were found, for :meth:`context`: what a ``withSecret`` request
        was answered, or what the AWS credential chain resolved when
        ``sqlutils.attach_local_catalogs()`` ran (the kernel server's container credentials, the
        app's signed-in session). ``detail`` is the reason when they were not.
        """
        with self._lock:
            self._signed_in = vended
            self._signed_in_detail = "" if vended else detail

    def context(self) -> StudioContext:
        with self._lock:
            signed_in, detail = self._signed_in, self._signed_in_detail
        return StudioContext(
            RuntimeMode.LOCAL,
            f"{APP_URL_ENV_VAR} is set",
            app_url=self.client.url,
            signed_in=signed_in,
            signed_in_detail=detail,
        )

    def connection_provider(self):
        """The provider that resolves connections through the app's API."""
        if self._provider is None:
            from sagemaker_studio.connections.providers.app_api import AppApiConnectionProvider

            self._provider = AppApiConnectionProvider(self)
        return self._provider


_kernel: Optional[LocalKernel] = None
_resolved = False
_lock = threading.Lock()
_reset_listeners: List[Callable[[], None]] = []


def local_kernel() -> Optional[LocalKernel]:
    """
    The local kernel this process is, or ``None`` outside the AWS Notebook app.

    Decided once from the environment on first use (see the module docstring) and kept until
    :func:`reset_local_kernel`.
    """
    global _kernel, _resolved
    if _resolved:
        return _kernel
    with _lock:
        if not _resolved:
            client = AppApiClient.from_env()
            if client is not None:
                _kernel = LocalKernel(client)
                logger.info("Running as an AWS Notebook local kernel; app API at %s", client.url)
            _resolved = True
    return _kernel


def configure_local_kernel(
    app_url: str,
    token: Optional[str],
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    default_region: Optional[str] = None,
) -> StudioContext:
    """
    Point the SDK at an AWS Notebook app explicitly, instead of reading the environment.

    For embedders and tests; the kernel the app starts needs no call. State built for a previous
    configuration (SQL engines, DuckDB secrets, the Project) is dropped.
    """
    global _kernel, _resolved
    with _lock:
        _kernel = LocalKernel(AppApiClient(app_url, token, timeout=timeout), default_region)
        _resolved = True
    _notify_reset()
    logger.info("Configured as an AWS Notebook local kernel; app API at %s", _kernel.client.url)
    return _kernel.context()


def reset_local_kernel() -> None:
    """Forget the local-kernel decision; the environment is read again on next use."""
    global _kernel, _resolved
    with _lock:
        _kernel = None
        _resolved = False
    _notify_reset()


def add_reset_listener(listener: Callable[[], None]) -> None:
    """Register a callback run by :func:`configure_local_kernel` and :func:`reset_local_kernel`."""
    if listener not in _reset_listeners:
        _reset_listeners.append(listener)


def _notify_reset() -> None:
    for listener in list(_reset_listeners):
        try:
            listener()
        except Exception:  # noqa: BLE001 - one listener must not stop the others
            logger.warning("A local-kernel reset listener failed", exc_info=True)


def is_local_kernel() -> bool:
    return local_kernel() is not None


def current_context() -> StudioContext:
    kernel = local_kernel()
    return kernel.context() if kernel is not None else REMOTE_CONTEXT


def runtime_mode() -> RuntimeMode:
    return current_context().mode


__all__ = [
    "API_PREFIX",
    "APP_TOKEN_ENV_VAR",
    "APP_URL_ENV_VAR",
    "AppApiClient",
    "CONNECTIONS_GET",
    "CONNECTIONS_LIST",
    "DEFAULT_CREDENTIALS_LIFETIME",
    "DEFAULT_TIMEOUT_SECONDS",
    "LocalKernel",
    "REFRESH_WINDOW",
    "REMOTE_CONTEXT",
    "RuntimeMode",
    "StudioContext",
    "add_reset_listener",
    "configure_local_kernel",
    "current_context",
    "expires_soon",
    "is_local_kernel",
    "local_kernel",
    "parse_expiration",
    "refreshable_credentials",
    "reset_local_kernel",
    "runtime_mode",
]
