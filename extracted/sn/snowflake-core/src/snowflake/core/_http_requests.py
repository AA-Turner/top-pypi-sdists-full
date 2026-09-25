"""Helpers related to sending/receiving HTTP requests."""

import contextvars
import datetime
import json
import logging
import os
import re
import ssl
import threading
import typing

from decimal import Decimal
from typing import Optional
from urllib.parse import quote

import urllib3

from pydantic import SecretStr

from snowflake.core.exceptions import SnowflakePythonError

from ._common import TokenType
from ._constants import SESSION_TOKEN_EXPIRED_ERROR_CODE


if typing.TYPE_CHECKING:
    import snowflake.core

    from ._generated import Configuration

logger = logging.getLogger(__name__)

PrimitiveTypes = typing.TypeVar("PrimitiveTypes", float, bool, bytes, bytearray, str, int)
PRIMITIVE_TYPES = (float, bool, bytes, bytearray, str, int)
NATIVE_TYPES_MAPPING = {
    "int": int,
    "long": int,  # TODO remove as only py3 is supported?
    "float": float,
    "str": str,
    "bool": bool,
    "date": datetime.date,
    "datetime": datetime.datetime,
    "object": object,
    "bytes": bytes,
    "bytearray": bytearray,
}
DEFAULT_RETRY_TIMEOUT_SECONDS = 600.0  # default 10 minutes for query retries
STATUS_CODES_MAPPING = {
    200: "OK",
    202: "Long Running Query",
    429: "Rate Limited",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}


_DOT_SEGMENT_RE = re.compile(r"^\.\.?$")


def _validate_path_param(name: str, value: str) -> str:
    if _DOT_SEGMENT_RE.match(value):
        raise ValueError(f"Invalid value {value!r} for path parameter '{name}': identifiers may not be '.' or '..'.")
    return value


def resolve_url(
    resource_path: str, path_params: dict[str, str], collection_formats: dict[typing.Any, typing.Any], safe_quoting: str
) -> str:
    if path_params:
        path_params = sanitize_for_serialization(path_params)
        path_params_list = parameters_to_tuples(path_params, collection_formats)
        resource_path = resource_path.format(
            **{k: quote(_validate_path_param(k, str(v)), safe=safe_quoting) for k, v in path_params_list}
        )
    return resource_path


class ToDictProto(typing.Protocol):
    def to_dict(self) -> dict[typing.Any, typing.Any]: ...


@typing.overload
def sanitize_for_serialization(obj: None) -> None: ...
@typing.overload
def sanitize_for_serialization(obj: PrimitiveTypes) -> PrimitiveTypes: ...
@typing.overload
def sanitize_for_serialization(obj: Decimal) -> str: ...
@typing.overload
def sanitize_for_serialization(obj: list[typing.Any]) -> list[typing.Any]: ...
@typing.overload
def sanitize_for_serialization(obj: tuple[typing.Any, ...]) -> tuple[typing.Any, ...]: ...
@typing.overload
def sanitize_for_serialization(obj: typing.Union[datetime.datetime, datetime.date]) -> str: ...
@typing.overload
def sanitize_for_serialization(obj: dict[typing.Any, typing.Any]) -> dict[typing.Any, typing.Any]: ...
@typing.overload
def sanitize_for_serialization(obj: ToDictProto) -> dict[typing.Any, typing.Any]: ...
def sanitize_for_serialization(
    obj: typing.Union[
        None,
        float,
        bool,
        bytes,
        bytearray,
        str,
        int,
        Decimal,
        list[typing.Any],
        tuple[typing.Any, ...],
        datetime.datetime,
        datetime.date,
        dict[typing.Any, typing.Any],
        ToDictProto,
    ],
) -> typing.Union[
    None,
    float,
    bool,
    bytes,
    bytearray,
    str,
    int,
    list[typing.Any],
    tuple[typing.Any, ...],
    dict[typing.Any, typing.Any],
]:
    """Build a JSON POST object.

    If obj is None, return None.
    If obj is str, int, long, float, bool, return directly.
    if obj is decimal.Decimal, convert to string, using scientific notation if needed.
    If obj is datetime.datetime, datetime.date
        convert to string in iso8601 format.
    If obj is list, sanitize each element in the list.
    If obj is dict, return the dict.
    If obj is OpenAPI model, return the properties dict.

    :param obj: The data to serialize.
    :return: The serialized form of data.
    """
    if obj is None:
        return None
    elif isinstance(obj, PRIMITIVE_TYPES):
        return obj
    elif isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, SecretStr):
        return obj.get_secret_value()
    elif isinstance(obj, list):
        return [sanitize_for_serialization(sub_obj) for sub_obj in obj]
    elif isinstance(obj, tuple):
        return tuple(sanitize_for_serialization(sub_obj) for sub_obj in obj)
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

    if isinstance(obj, dict):
        obj_dict = obj
    else:
        # Convert model obj to dict except
        # attributes `openapi_types`, `attribute_map`
        # and attributes which value is not None.
        # Convert attribute name to json key in
        # model definition for request.
        # Prefer to use `to_dict_without_readonly_properties` if the model has
        if hasattr(obj, "to_dict_without_readonly_properties"):
            obj_dict = obj.to_dict_without_readonly_properties()
        else:
            obj_dict = obj.to_dict()

    return {key: sanitize_for_serialization(val) for key, val in obj_dict.items()}


def parameters_to_tuples(
    params: typing.Union[dict[typing.Any, typing.Any], list[tuple[typing.Any, typing.Any]]],
    collection_formats: typing.Optional[dict[typing.Any, typing.Any]],
) -> list[tuple[typing.Any, typing.Any]]:
    """Get parameters as list of tuples, formatting collections.

    :param params: Parameters as dict or list of two-tuples
    :param dict collection_formats: Parameter collection formats
    :return: Parameters as list of tuples, collections formatted
    """
    new_params: list[tuple[typing.Any, typing.Any]] = []
    if collection_formats is None:
        collection_formats = {}
    for k, v in params.items() if isinstance(params, dict) else params:
        if k in collection_formats:
            collection_format = collection_formats[k]
            if collection_format == "multi":
                new_params.extend((k, value) for value in v)
            else:
                if collection_format == "ssv":
                    delimiter = " "
                elif collection_format == "tsv":
                    delimiter = "\t"
                elif collection_format == "pipes":
                    delimiter = "|"
                else:  # csv is the default
                    delimiter = ","
                new_params.append((k, delimiter.join(str(value) for value in v)))
        else:
            new_params.append((k, v))
    return new_params


class SFPoolManager:
    """Sends HTTP requests over a urllib3 manager.

    The pool options of the ``Configuration`` this instance belongs to are held in
    ``pool_kwargs`` and put in scope for the duration of each request, where the manager
    picks them up to resolve a pool. urllib3 folds them into its connection pool key, so
    configurations that disagree about TLS verification, trust store or client certificate
    never share a connection pool, while equivalent ones keep sharing connections.
    """

    def __init__(self, manager: urllib3.PoolManager, pool_kwargs: dict[str, typing.Any]) -> None:
        self._manager = manager
        self._pool_kwargs = pool_kwargs

    # Having this typed is non-trivial across multiple
    #  urllib3 major versions
    def _send(  # type: ignore[no-untyped-def]
        self,
        method: str,
        url: str,
        fields,
        headers: typing.Optional[dict[str, str]],
        urlopen_kw: dict[str, typing.Any],
    ):
        """Send one request with this configuration's pool options in scope."""
        token = _POOL_KWARGS.set(self._pool_kwargs)
        try:
            return self._manager.request(method=method, url=url, fields=fields, headers=headers, **urlopen_kw)
        finally:
            _POOL_KWARGS.reset(token)

    # Having this typed is non-trivial across multiple
    #  urllib3 major versions
    def request(  # type: ignore[no-untyped-def]
        self,
        root: "snowflake.core.Root",
        method: str,
        url: str,
        fields=None,
        headers: typing.Optional[dict[str, str]] = None,
        **urlopen_kw: typing.Any,
    ):
        if headers is None:
            headers = dict()
        need_auth = url_needs_auth(url)
        if need_auth:
            if root._session_token is None:
                # This should never trigger
                raise Exception("session token is missing while making a request")
            headers.update(get_session_headers(root.token_type, root._session_token, root.external_session_id))
        logger.debug("making an http %s call to '%s'", method.upper(), url)
        try:
            r = self._send(method, url, fields, headers, urlopen_kw)
        except urllib3.exceptions.MaxRetryError as e:
            if (
                isinstance(e.reason, urllib3.exceptions.SSLError)
                and isinstance(e.reason.args[0], ssl.SSLCertVerificationError)
                and "Hostname mismatch" in e.reason.args[0].verify_message
            ):
                raise SnowflakePythonError(
                    "This SSL error occurs when the hostname contains underscores, please see "
                    "https://docs.snowflake.com/en/user-guide/organizations-connect for how to set "
                    "the hostname correctly."
                ) from e
            raise

        try:
            content_type = r.headers.get("Content-Type")
            if content_type in {"text/event-stream", "application/octet-stream"}:
                resp_json = dict()
            else:
                resp_json = json.loads(r.data)
        except Exception:
            resp_json = dict()
        if (
            need_auth
            and isinstance(resp_json, dict)
            and resp_json.get("error_code") == SESSION_TOKEN_EXPIRED_ERROR_CODE
            and hasattr(root, "_connection")
            and root._connection.rest is not None
        ):
            # Try renewing session token and try request again
            logger.debug("session expired, renewing session")
            root._connection.rest._renew_session()
            if need_auth:
                if root._session_token is None:
                    # This should never trigger
                    raise Exception("session token is missing right after renewal")
                headers.update(get_session_headers(root.token_type, root._session_token, root.external_session_id))
            logger.debug("repeating an http with new session token %s call to '%s'", method.upper(), url)
            r = self._send(method, url, fields, headers, urlopen_kw)
        return r


# The pool options of the request being sent, published by SFPoolManager for the manager to read.
_POOL_KWARGS: contextvars.ContextVar[typing.Optional[dict[str, typing.Any]]] = contextvars.ContextVar(
    "snowflake_core_pool_kwargs", default=None
)


class _PoolManager(urllib3.PoolManager):
    """A manager that resolves pools with the pool options of the configuration being served.

    urllib3 resolves a pool from the host alone, which would hand a configuration a pool that
    was built for a different one.
    """

    def connection_from_host(
        self,
        host: Optional[str],
        port: Optional[int] = None,
        scheme: Optional[str] = "http",
        pool_kwargs: Optional[dict[str, typing.Any]] = None,
    ) -> urllib3.HTTPConnectionPool:
        return super().connection_from_host(host, port, scheme, pool_kwargs or _POOL_KWARGS.get())


class _ProxyManager(_PoolManager, urllib3.ProxyManager):
    """A :class:`_PoolManager` that reaches its hosts through a proxy."""


# urllib3 managers are shared across the process. There is one manager per distinct proxy.
_ManagerKey = tuple[str, frozenset[tuple[str, str]]]
MANAGERS: dict[Optional[_ManagerKey], urllib3.PoolManager] = {}
_MANAGERS_LOCK = threading.Lock()


def get_session_headers(
    token_type: TokenType, session_token: str, external_session_id: Optional[str] = None
) -> dict[str, str]:
    if token_type is TokenType.EXTERNAL_SESSION_WITH_PAT:
        return {
            "Authorization": f"Bearer {session_token}",
            "X-Snowflake-External-Session-ID": external_session_id or "",
            "X-Snowflake-Authorization-Token-Type": "PAT_WITH_EXTERNAL_SESSION_ID",
        }
    return {"Authorization": f'Snowflake Token="{session_token}"'}


def url_needs_auth(url: str) -> bool:
    """Whether a URL needs the authentication headers to work.

    For now this is all URLs, since Python connector takes care of authentication and
    session related actions.
    """
    return True


def _proxy_setup(configuration: "Configuration") -> Optional[dict[str, typing.Any]]:
    if configuration.proxy:
        return {"proxy_url": configuration.proxy, "proxy_headers": configuration.proxy_headers}
    # To keep compatibility with driver behavior
    if http_url := (os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")):
        return {"proxy_url": http_url, "proxy_headers": {}}
    return None


def _resolve_ca_cert(configuration: "Configuration") -> Optional[str]:
    """Resolve the CA bundle to use for TLS verification."""
    if env_ca_cert := (os.getenv("SSL_CERT_FILE") or os.getenv("ssl_cert_file")):
        return env_ca_cert
    return configuration.ssl_ca_cert


def _manager_key(proxy_kwargs: Optional[dict[str, typing.Any]]) -> Optional[_ManagerKey]:
    """Return the key under which the manager for these proxy settings is registered."""
    if proxy_kwargs is None:
        return None
    # Header dicts are turned into frozensets to be hashable, the way urllib3 does it in
    # poolmanager._default_key_normalizer().
    return proxy_kwargs["proxy_url"], frozenset((proxy_kwargs["proxy_headers"] or {}).items())


def _get_manager(proxy_kwargs: Optional[dict[str, typing.Any]]) -> urllib3.PoolManager:
    """Return the manager for these proxy settings, creating it on first use."""
    key = _manager_key(proxy_kwargs)
    manager = MANAGERS.get(key)
    if manager is not None:
        return manager
    with _MANAGERS_LOCK:
        manager = MANAGERS.get(key)
        if manager is None:
            manager = _PoolManager() if proxy_kwargs is None else _ProxyManager(**proxy_kwargs)
            logger.debug("created a new urllib3 manager")
            MANAGERS[key] = manager
    return manager


def _pool_kwargs(configuration: "Configuration", maxsize: typing.Optional[int] = None) -> dict[str, typing.Any]:
    """Collect the connection pool options of a single configuration."""
    if maxsize is None:
        maxsize = configuration.connection_pool_maxsize or 4

    pool_kwargs: dict[str, typing.Any] = {
        "maxsize": maxsize,
        "cert_reqs": ssl.CERT_REQUIRED if configuration.verify_ssl else ssl.CERT_NONE,
        "ca_certs": _resolve_ca_cert(configuration),
        "cert_file": configuration.cert_file,
        "key_file": configuration.key_file,
    }
    if configuration.assert_hostname is not None:
        pool_kwargs["assert_hostname"] = configuration.assert_hostname

    if configuration.retries is not None:
        pool_kwargs["retries"] = configuration.retries

    if configuration.socket_options is not None:
        pool_kwargs["socket_options"] = configuration.socket_options

    return pool_kwargs


def create_connection_pool(configuration: "Configuration", maxsize: typing.Optional[int] = None) -> SFPoolManager:
    """Return the pool manager that ``configuration`` should send its requests through."""
    return SFPoolManager(_get_manager(_proxy_setup(configuration)), _pool_kwargs(configuration, maxsize))
