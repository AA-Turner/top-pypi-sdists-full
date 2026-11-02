"""Resolving the lakehouse connection a Databaas admin registered.

The admin flow this serves: create a Zitadel service user with a
`client_credentials` machine client, grant it permissions on the Lakekeeper
warehouse, and register it as an Airflow connection. No S3 keys appear anywhere
in that list — object storage is reached by asking Lakekeeper to sign.

Three resolution routes are tried in order, matching what the image's MQTT
trigger already does so there is one behaviour to learn:

1. ``AIRFLOW_CONN_<CONN_ID>`` in the environment — how the chart delivers
   connections (`airflowConnections.items` renders one Secret of these). This
   route is pure stdlib, so a container or notebook with the variable set needs
   no Airflow installed.
2. ``Connection.get_connection_from_secrets`` — the secrets-backend chain.
3. ``BaseHook.get_connection`` — the metadata database.

Failure is loud. The prior art caught every exception here and returned None,
which the caller turned into a local filesystem sink: a typo'd conn_id or an
expired secret then redirected a production write to an ephemeral pod disk and
the task went green. That is the worst failure mode in the prior art and it is
not reproduced.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from databaas_utils.errors import ConfigurationError, ConnectionNotConfigured
from databaas_utils.settings import DEFAULT_WAREHOUSE, LakehouseSettings

log = logging.getLogger(__name__)

DEFAULT_CONN_ID = "databaas_lakehouse"
#: Accepted as an alias so Infoplaza's existing `lakekeeper` connection keeps
#: working through the migration.
LEGACY_CONN_ID = "lakekeeper"

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


@dataclass
class ConnectionData:
    """An Airflow connection, normalised.

    Its own type rather than Airflow's `Connection` because the env route must
    work where Airflow is not installed.
    """

    conn_id: str
    host: str | None = None
    schema: str | None = None
    login: str | None = None
    password: str | None = field(default=None, repr=False)
    port: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_airflow(cls, conn: Any) -> ConnectionData:
        """Normalise an Airflow ``Connection`` object."""
        return cls(
            conn_id=getattr(conn, "conn_id", "") or "",
            host=conn.host,
            schema=getattr(conn, "schema", None),
            login=conn.login,
            password=conn.password,
            port=conn.port,
            extra=_parse_extra(conn.extra),
        )


def _parse_extra(raw: Any) -> dict[str, Any]:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _from_env(conn_id: str) -> ConnectionData | None:
    """``AIRFLOW_CONN_<CONN_ID>``, in either the JSON or the URI form."""
    raw = os.environ.get(f"AIRFLOW_CONN_{conn_id.upper()}")
    if raw is None:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        from urllib.parse import parse_qsl, unquote, urlsplit

        parsed = urlsplit(raw)
        query = dict(parse_qsl(parsed.query))
        extra_raw = query.pop("__extra__", None)
        return ConnectionData(
            conn_id=conn_id,
            host=parsed.hostname,
            schema=(parsed.path or "").lstrip("/") or None,
            login=unquote(parsed.username) if parsed.username else None,
            password=unquote(parsed.password) if parsed.password else None,
            port=parsed.port,
            extra=_parse_extra(extra_raw) if extra_raw is not None else query,
        )
    if not isinstance(data, dict):
        return None
    return ConnectionData(
        conn_id=conn_id,
        host=data.get("host"),
        schema=data.get("schema"),
        login=data.get("login"),
        password=data.get("password"),
        port=data.get("port"),
        extra=_parse_extra(data.get("extra")),
    )


def _from_secrets(conn_id: str) -> ConnectionData | None:
    # airflow.models.connection, not airflow.sdk: only the former carries
    # get_connection_from_secrets on Airflow 3.1.8. Importing the wrong one
    # makes this route dead code that fails silently into the next.
    try:
        from airflow.models.connection import Connection
    except ImportError:
        return None
    try:
        return ConnectionData.from_airflow(
            Connection.get_connection_from_secrets(conn_id)
        )
    except Exception as exc:
        log.debug("secrets backend did not resolve %r: %s", conn_id, exc)
        return None


def _from_hook(conn_id: str) -> ConnectionData | None:
    try:
        from airflow.sdk import BaseHook
    except ImportError:
        return None
    try:
        return ConnectionData.from_airflow(BaseHook.get_connection(conn_id))
    except Exception as exc:
        log.debug("hook did not resolve %r: %s", conn_id, exc)
        return None


def resolve_connection(conn_id: str = DEFAULT_CONN_ID) -> ConnectionData:
    """The connection for `conn_id`, tried via env, secrets, then hook.

    Raises rather than returning None: an unresolvable connection is a
    configuration problem, and every caller here would otherwise have to invent
    its own fallback.

    Raises:
        ConnectionNotConfigured: If no route finds the connection.
    """
    for route in (_from_env, _from_secrets, _from_hook):
        found = route(conn_id)
        if found is not None:
            return found
    raise ConnectionNotConfigured(
        conn_id,
        "not found in AIRFLOW_CONN_* , the secrets backend, or the metadata "
        "database. A Databaas admin registers this connection from a Zitadel "
        "service account; see https://docs.databaas.eu/pipelines/service-account",
    )


def _coerce_verify(value: Any) -> bool | str:
    if value is None:
        return True
    if isinstance(value, bool):
        return value
    text = str(value).strip()
    if text.lower() in _TRUE:
        return True
    if text.lower() in _FALSE:
        return False
    return text  # a CA bundle path


def settings_from_connection(
    conn: ConnectionData, *, namespace: str | None = None
) -> LakehouseSettings:
    """Map connection fields onto settings.

    `schema` carries the warehouse: it is Airflow's "which database" slot, it
    renders as a labelled form field rather than a JSON key, and it is what
    every other data connection uses. `extra.warehouse` stays accepted for
    compatibility, and `schema` wins. With neither, it is `databaas-lakehouse`.

    Setting up the connection is described at
    https://docs.databaas.eu/pipelines/service-account.

    Raises:
        ConfigurationError: If the host or token settings are missing.
    """
    extra = conn.extra or {}
    host = (conn.host or "").strip()
    if not host:
        raise ConfigurationError(
            f"connection {conn.conn_id!r} has no host — it must be the Lakekeeper "
            "server root, e.g. https://lakekeeper.example.com"
        )
    if conn.port and ":" not in host.rsplit("/", 1)[-1]:
        host = f"{host.rstrip('/')}:{conn.port}"

    warehouse = conn.schema or extra.get("warehouse") or DEFAULT_WAREHOUSE

    values: dict[str, Any] = {
        "base_url": host,
        "warehouse": warehouse,
        "namespace": extra.get("namespace"),
        "region": extra.get("region"),
        "endpoint": extra.get("endpoint"),
        "verify": _coerce_verify(extra.get("verify")),
        "token_url": extra.get("token_url") or extra.get("oauth2_server_uri"),
        "project_id": extra.get("project_id"),
        "scope": extra.get("scope") or extra.get("oauth2_scope"),
        # Some Zitadel consoles only offer a downloadable JSON key for a
        # machine user, not a plain client secret. LakehouseSettings.from_mapping
        # checks this before login/password, so its presence here wins
        # regardless of what else is set.
        "service_account_key": extra.get("service_account_key"),
        "audience": extra.get("audience"),
    }
    if conn.login:
        values["client_id"] = conn.login
        values["client_secret"] = conn.password
        if not values["token_url"]:
            raise ConfigurationError(
                f"connection {conn.conn_id!r} has a login (the OAuth client id), so "
                "its extras must define 'token_url' — the Zitadel token endpoint"
            )
        if not (values["project_id"] or values["scope"]):
            raise ConfigurationError(
                f"connection {conn.conn_id!r} must define 'project_id' (or an "
                "explicit 'scope') in extras — Lakekeeper rejects a token without "
                "the project audience"
            )
    else:
        # No login: the password field carries a bearer token verbatim.
        values["token"] = conn.password

    return LakehouseSettings.from_mapping(values, namespace=namespace)


def get_settings(
    conn_id: str = DEFAULT_CONN_ID, *, namespace: str | None = None
) -> LakehouseSettings:
    """Settings for `conn_id`. Raises if it cannot be resolved.

    Args:
        conn_id: The Airflow connection to read.
        namespace: Overrides the connection's default namespace.

    Raises:
        ConnectionNotConfigured: If the connection does not exist.
        ConfigurationError: If its fields are incomplete.
    """
    return settings_from_connection(resolve_connection(conn_id), namespace=namespace)
