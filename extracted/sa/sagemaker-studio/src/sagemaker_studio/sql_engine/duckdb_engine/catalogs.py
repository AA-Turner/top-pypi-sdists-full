"""
The project's data catalogs on the kernel's DuckDB: every ``LAKEHOUSE`` connection's Glue catalogs
and every ``ATHENA`` connection's workgroup, attached under the Data Explorer's names.

``sqlutils.attach_local_catalogs()`` is the entry point: the kernel calls it at start and the
frontend on every change (sign-in, sign-out, profile switch, a connection added or removed). Each
call starts over from the project's listing (:meth:`LocalCatalogs.attach_all`): detach every
database the SDK attached, drop every secret it made (and the ``iceberg`` extension's vended
``__internal_ic_*`` credentials), attach what the listing says. A cell refreshes nothing; it only
puts its ``catalog_name`` / ``schema_name`` on DuckDB's ``search_path`` (``duckdbutils``). The same
code runs on an AWS Notebook local kernel (the app lists; the kernel server's container credentials
are the chain) and on SageMaker Unified Studio compute (DataZone lists; the space's role is the
chain).

What is attached
----------------
* A ``LAKEHOUSE`` connection's Glue catalogs, one ``ATTACH`` each through Glue's Iceberg REST
  endpoint: its ``AwsDataCatalog`` and every S3 Tables catalog under its ``s3tablescatalog`` (Glue
  ``GetCatalogs`` under the connection's account). Aliases are the Data Explorer's
  (:func:`catalog_alias`): the default connection's catalogs keep their names, any other
  connection's are prefixed with the connection name minus ``.catalog`` (``sales_AwsDataCatalog``).
* An ``ATHENA`` connection as its workgroup through DuckDB's ``athena`` extension, which the kernel
  must have loaded (``ATTACH 'athena://<region>[/<workgroup>]'``, aliased by the connection name
  minus ``.sql``, :func:`athena_alias`, with ``CATALOG`` when it names another data catalog).
* Two connections wanting one alias: the first in the round's order (lakehouse catalogs, default
  connection first, then by name; Athena connections after) holds it whether or not its ATTACH
  succeeded, so the alias means the same connection on every round; the other is not attached.

Credentials
-----------
No connection's credentials are fetched. Every ATTACH names a ``credential_chain`` secret with
``REFRESH auto``, which DuckDB resolves and refreshes itself: connections without an access role
share one per region (:func:`chain_secret_name`); a connection naming an access role gets its own
with ``CHAIN 'sts'`` and ``ASSUME_ROLE_ARN`` (:func:`role_secret_name`). Every secret is scoped to
:data:`SECRET_SCOPE`, a prefix no statement names, so it never signs an ``s3://`` read and is
recognisable as the SDK's; the Glue ``GetCatalogs`` listing signs the same way. A connection whose
secret, listing or ATTACH fails is recorded on its :class:`AttachedCatalog`, never raised; signed
out, nothing is attached. The engine's own unscoped ``credential_chain`` secret (a connection-less
cell's ``s3://`` reads) is ``duckdbutils``' to re-create in the same round and drop on sign-out.
Logging names secrets, never their contents.
"""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

import boto3

from sagemaker_studio.connections.providers import ConnectionRecord
from sagemaker_studio.connections.providers.app_api import (
    TYPE_ATHENA,
    TYPE_LAKEHOUSE,
    athena_workgroup,
    aws_location,
)
from sagemaker_studio.sql_engine.duckdb_engine import _one_row

logger = logging.getLogger(__name__)

AWS_DATA_CATALOG = "AwsDataCatalog"
#: Glue's parent catalog of the S3 Tables catalogs (one per table bucket).
S3_TABLES_CATALOG = "s3tablescatalog"
#: The default lakehouse connection, whose catalogs keep their own names (the Data Explorer's rule).
_DEFAULT_LAKEHOUSE_NAME = re.compile(r"^(project\.default_lakehouse|default\.catalog)$")
#: The suffix the connection manager gives the Athena half of a Glue connection pair
#: (``sales.catalog`` and ``sales.sql``), which an Athena connection's alias drops.
_ATHENA_NAME_SUFFIX = re.compile(r"\.sql$")
#: Every secret the SDK makes for the attached databases starts with this.
SECRET_PREFIX = "sagemaker_studio_catalogs"
#: The scope of every secret the SDK makes: a prefix no statement names, which marks the secret
#: as the SDK's and keeps it off every ``s3://`` lookup.
SECRET_SCOPE = "sagemaker-studio-catalogs://"
#: What the ``iceberg`` extension names the temporary secrets it makes of credentials a catalog
#: vends for a table (``__internal_ic_<table id>``, scoped to the table's location).
VENDED_SECRET_PREFIX = "__internal_ic_"
#: How a database is attached: an Athena connection through the ``athena`` extension, a lakehouse
#: connection's catalog from Glue's Iceberg REST endpoint.
ROUTE_ATHENA = "athena"
ROUTE_GLUE = "glue"
_PLAIN_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_NO_ATHENA_EXTENSION = (
    "the athena DuckDB extension is not loaded, so the connection cannot be attached; "
    "load it and call sqlutils.attach_local_catalogs()"
)
_NO_ACCOUNT_OR_REGION = (
    "the connection names no AWS account or region, so its catalogs cannot be attached"
)
_NO_REGION = "the connection names no AWS region, so its workgroup cannot be attached"


# --- the Data Explorer's naming rules (one copy here, one in the frontend) ---------------------


def is_default_lakehouse(connection_name: str) -> bool:
    return bool(_DEFAULT_LAKEHOUSE_NAME.match(connection_name or ""))


def catalog_alias(lakehouse_connection_name: str, catalog_name: str) -> str:
    """
    The name a lakehouse connection's catalog is attached as, which is the name the Data Explorer
    shows it under: the default connection's catalogs as they are, other connections' prefixed
    with the connection name (``sales_orders``) so two connections' catalogs cannot collide.
    """
    if is_default_lakehouse(lakehouse_connection_name):
        return catalog_name
    return f"{re.sub(r'[.]catalog$', '', lakehouse_connection_name or '')}_{catalog_name}"


def athena_alias(athena_connection_name: str) -> str:
    """
    The name an Athena connection is attached as: the connection's name without the ``.sql`` the
    connection manager gives the Athena half of a Glue connection pair (``sales.sql`` as
    ``sales``), so an unquoted ``sales.<database>.<table>`` reads as DuckDB reads names. Any other
    name is kept as it is.
    """
    return _ATHENA_NAME_SUFFIX.sub("", athena_connection_name or "")


def glue_catalog_id(account: str, s3_tables_catalog: Optional[str] = None) -> str:
    """The Glue catalog id: the account for ``AwsDataCatalog``, ``<account>:s3tablescatalog/<name>`` for an S3 Tables catalog."""
    return f"{account}:{S3_TABLES_CATALOG}/{s3_tables_catalog}" if s3_tables_catalog else account


def _secret_word(value: str) -> str:
    """A value as part of a secret name: DuckDB keeps names lower case; anything odd becomes ``_``."""
    return re.sub(r"[^A-Za-z0-9_]", "_", value or "").lower()


def chain_secret_name(region: str) -> str:
    """The shared secret of the kernel's own identity in ``region``: ``sagemaker_studio_catalogs_us_west_2``."""
    return f"{SECRET_PREFIX}_{_secret_word(region)}"


def role_secret_name(connection_id: str) -> str:
    """The secret assuming a connection's access role: ``sagemaker_studio_catalogs_role_<connection id>``."""
    return f"{SECRET_PREFIX}_role_{_secret_word(connection_id)}"


# --- DuckDB statements -------------------------------------------------------------------------


def sql_literal(value: Any) -> str:
    """Single-quote a value for a DuckDB statement that cannot take bound parameters."""
    return "'" + str(value).replace("'", "''") + "'"


def sql_identifier(name: str) -> str:
    """Double-quote an identifier: an alias may hold spaces, dots or hyphens."""
    return '"' + str(name).replace('"', '""') + '"'


def search_path_identifier(name: str) -> str:
    """An identifier as DuckDB's ``search_path`` setting reads it: quoted unless it needs no quotes."""
    return name if _PLAIN_IDENTIFIER.match(name) else sql_identifier(name)


def search_path_entry(catalog: str, schema: Optional[str] = None) -> str:
    """
    One ``search_path`` entry: the catalog, and the schema when named (``"my data_orders".sales``);
    with no schema DuckDB resolves the catalog's default schema, which an attached Glue catalog
    may not have.
    """
    entry = search_path_identifier(catalog)
    return f"{entry}.{search_path_identifier(schema)}" if schema else entry


def search_path_catalog(search_path: str) -> Optional[str]:
    """
    The catalog of the first entry of DuckDB's ``search_path`` setting, as a name again (what
    :func:`search_path_entry` quoted, unquoted): a cell's ``catalog_name`` while the cell runs in a
    catalog. ``None`` for an empty path.
    """
    text = search_path.lstrip()
    if not text:
        return None
    if not text.startswith('"'):
        end = len(text)
        for separator in ".,":
            at = text.find(separator)
            if at != -1:
                end = min(end, at)
        return text[:end].strip()
    name: List[str] = []
    i = 1
    while i < len(text):
        if text[i] == '"':
            if text.startswith('""', i):  # a quote inside the name, doubled
                name.append('"')
                i += 2
                continue
            break
        name.append(text[i])
        i += 1
    return "".join(name)


def catalogs_named(statement: str, search_path: str, aliases: Iterable[str]) -> List[str]:
    """
    Which of ``aliases`` a statement runs against: the catalog first on ``search_path`` (a cell's
    ``catalog_name``) and every alias the statement qualifies a name with (``alias.schema.table``,
    the alias bare or double-quoted). DuckDB reads identifiers case-insensitively, so this does
    too; a name qualified by something else (``other.alias.table``) is a schema, not the alias.
    """
    current = search_path_catalog(search_path)
    lowered = statement.lower()
    named: List[str] = []
    for alias in aliases:
        if current is not None and alias.lower() == current.lower():
            named.append(alias)
            continue
        quoted = re.escape(sql_identifier(alias).lower()) + r"\s*\."
        bare = (
            r"(?<![\w\".])" + re.escape(alias.lower()) + r"\s*\."
            if _PLAIN_IDENTIFIER.match(alias)
            else None
        )
        if re.search(quoted, lowered) or (bare is not None and re.search(bare, lowered)):
            named.append(alias)
    return named


def create_chain_secret_statement(name: str, region: str) -> str:
    """
    ``CREATE OR REPLACE`` of the shared secret of the kernel's own identity in ``region``: the
    ``credential_chain`` provider resolves it (the container credentials in both modes),
    ``REFRESH auto`` renews it, and it is scoped as :data:`SECRET_SCOPE` says.
    """
    return (
        f"CREATE OR REPLACE SECRET {name} (TYPE s3, PROVIDER credential_chain, REFRESH auto, "
        f"REGION {sql_literal(region)}, SCOPE {sql_literal(SECRET_SCOPE)})"
    )


def create_role_secret_statement(name: str, role_arn: str, region: str) -> str:
    """
    ``CREATE OR REPLACE`` of a secret assuming a connection's access role from the same chain
    (``CHAIN 'sts'`` with ``ASSUME_ROLE_ARN``); ``REFRESH auto`` is what STS credentials need.
    """
    return (
        f"CREATE OR REPLACE SECRET {name} (TYPE s3, PROVIDER credential_chain, CHAIN 'sts', "
        f"ASSUME_ROLE_ARN {sql_literal(role_arn)}, REFRESH auto, "
        f"REGION {sql_literal(region)}, SCOPE {sql_literal(SECRET_SCOPE)})"
    )


def glue_attach_statement(
    alias: str,
    account: str,
    region: str,
    secret_name: str,
    s3_tables_catalog: Optional[str] = None,
    unstaged_creates: bool = False,
) -> str:
    """
    ``ATTACH IF NOT EXISTS`` of a Glue catalog through Glue's Iceberg REST endpoint, signing with
    ``secret_name``. ``unstaged_creates``: with ``STAGE_CREATE_TABLES false``, as the endpoint refuses
    a staged create ("Stage create is not supported"), DuckDB's default for ``CREATE TABLE``.
    """
    unstaged = ", STAGE_CREATE_TABLES false" if unstaged_creates else ""
    return (
        f"ATTACH IF NOT EXISTS {sql_literal(glue_catalog_id(account, s3_tables_catalog))} "
        f"AS {sql_identifier(alias)} (TYPE ICEBERG, "
        f"ENDPOINT {sql_literal(f'glue.{region}.amazonaws.com/iceberg')}, "
        f"AUTHORIZATION_TYPE 'sigv4', SECRET {sql_literal(secret_name)}{unstaged})"
    )


def _has_unstaged_creates() -> bool:
    """
    Whether this DuckDB's iceberg extension takes ``STAGE_CREATE_TABLES``: DuckDB 2's does. 1.x's
    refuses the option, and with it the whole ATTACH, so it attaches without (reading as before; only
    a CREATE TABLE fails).
    """
    try:
        import duckdb

        return int(duckdb.__version__.split(".")[0]) >= 2
    except Exception:  # noqa: BLE001 - no DuckDB, or a version it can't read: attach as before
        return False


def athena_attach_statement(
    alias: str,
    region: str,
    workgroup: Optional[str],
    secret_name: str,
    catalog: Optional[str] = None,
) -> str:
    """
    ``ATTACH IF NOT EXISTS`` of an Athena connection, as the ``athena`` extension spells it: the
    region and the workgroup in the path (none named: the extension's default, ``primary``),
    ``SECRET``, and ``CATALOG`` only when the data catalog is not the extension's default
    (``AwsDataCatalog``). One ATTACH exposes one data catalog, each database of it a schema.
    """
    path = f"athena://{region}" + (f"/{workgroup}" if workgroup else "")
    options = ["TYPE athena", f"SECRET {sql_literal(secret_name)}"]
    if catalog and catalog != AWS_DATA_CATALOG:
        options.append(f"CATALOG {sql_literal(catalog)}")
    return f"ATTACH IF NOT EXISTS {sql_literal(path)} AS {sql_identifier(alias)} ({', '.join(options)})"


def detach_statement(alias: str) -> str:
    return f"DETACH DATABASE IF EXISTS {sql_identifier(alias)}"


def drop_secret_statement(name: str) -> str:
    return f"DROP SECRET IF EXISTS {sql_identifier(name)}"


# --- what DuckDB holds ----------------------------------------------------------------------------


def present_secrets(duck) -> Optional[List[str]]:
    """
    The SDK's secrets DuckDB holds now, by name: every secret scoped to :data:`SECRET_SCOPE`,
    whichever process made it. ``None`` when the engine cannot answer, which is not the same as
    holding none.
    """
    try:
        rows = duck.sql("SELECT name, scope FROM duckdb_secrets()").fetchall()
    except Exception:  # noqa: BLE001 - an engine that cannot answer
        logger.warning(
            "Could not read duckdb_secrets(); only the secrets on record are dropped", exc_info=True
        )
        return None
    found: List[str] = []
    for row in rows or []:
        name, scope = (list(row) + [None, None])[:2]
        scopes = scope if isinstance(scope, (list, tuple)) else [scope]
        if name and any(str(s).startswith(SECRET_SCOPE) for s in scopes if s is not None):
            found.append(str(name))
    return found


def vended_secret_names(duck) -> List[str]:
    """The temporary secrets the ``iceberg`` extension holds vended table credentials in, by name."""
    try:
        rows = duck.sql(
            f"SELECT name FROM duckdb_secrets() WHERE starts_with(name, {sql_literal(VENDED_SECRET_PREFIX)})"
        ).fetchall()
    except Exception:  # noqa: BLE001 - an engine that cannot answer holds none we can drop
        logger.warning(
            "Could not read duckdb_secrets(); vended table credentials, if any, stay", exc_info=True
        )
        return []
    return [str(row[0]) for row in rows or [] if row and row[0]]


def drop_secrets(duck, names: Iterable[str]) -> List[str]:
    """``DROP SECRET IF EXISTS`` each name; best effort, like every drop. Returns the names dropped."""
    dropped: List[str] = []
    for name in names:
        try:
            duck.sql(drop_secret_statement(name) + ";")
            dropped.append(name)
        except Exception:  # noqa: BLE001 - best effort
            logger.warning(
                "Could not drop DuckDB secret %s; it stays until the next round",
                name,
                exc_info=True,
            )
    return dropped


def _athena_extension_loaded(duck) -> bool:
    """Whether the ``athena`` DuckDB extension is loaded, which attaching an Athena connection needs."""
    try:
        row = _one_row(
            duck,
            "SELECT count(*) FROM duckdb_extensions() WHERE extension_name = 'athena' AND loaded",
        )
        return bool(row and row[0])
    except Exception:  # noqa: BLE001 - an engine that cannot answer has no such extension
        logger.warning(
            "Could not read duckdb_extensions(); Athena connections cannot be attached",
            exc_info=True,
        )
        return False


# --- the project's records -----------------------------------------------------------------------


def _record_location(
    record: Mapping[str, Any],
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """``(account, region, access role)`` from a record's first physical endpoint, ``None`` when absent."""
    where = aws_location(record)
    access_role = None
    endpoints = record.get("physicalEndpoints")
    if isinstance(endpoints, Sequence) and endpoints and isinstance(endpoints[0], Mapping):
        location = endpoints[0].get("awsLocation")
        if isinstance(location, Mapping) and location.get("accessRole"):
            access_role = str(location["accessRole"])
    return where["account"], where["region"], access_role


def _record_name(record: Mapping[str, Any]) -> str:
    return str(record.get("name") or "")


def _record_type(record: Mapping[str, Any]) -> str:
    return str(record.get("type") or "").upper()


def _record_id(record: Mapping[str, Any]) -> str:
    return str(record.get("connectionId") or "")


def _athena_catalog(record: Mapping[str, Any]) -> str:
    """The data catalog an Athena record names (its top-level ``catalog``), ``AwsDataCatalog`` when none."""
    return str(record.get("catalog") or AWS_DATA_CATALOG)


#: The session name the S3 Tables listing assumes a connection's access role under.
_ROLE_SESSION_NAME = "sagemaker-studio-duckdb-catalogs"


def chain_credentials() -> Tuple[bool, str]:
    """
    Whether the AWS SDK's default credential chain (what this module's secrets, the engine's own
    and :func:`_aws_client` sign with) resolves credentials now and, if not, why. On a local kernel
    the chain reaches the app's signed-in session through the kernel server, so nothing to resolve
    means signed out, and the reason is the app's when the server passed it on, else botocore's.
    The credentials are not kept.
    """
    try:
        found = boto3.Session().get_credentials()
    except Exception as e:  # noqa: BLE001 - botocore's reason, recorded, never raised from here
        return False, _chain_failure_reason(e)
    if found is None:
        return False, "The AWS credential chain resolves no credentials"
    return True, ""


def _chain_failure_reason(error: Exception) -> str:
    message = str(error).strip()
    start = message.find("{")
    if start >= 0:
        try:
            envelope = json.loads(message[start:])
        except ValueError:
            envelope = None
        failure = envelope.get("error") if isinstance(envelope, dict) else None
        reason = failure.get("message") if isinstance(failure, dict) else None
        if isinstance(reason, str) and reason:
            return reason
    return message.splitlines()[0] if message else type(error).__name__


def _aws_client(service: str, region: str, role_arn: Optional[str]):
    """
    A boto3 client of ``service`` in ``region`` signing as the connection's catalogs do: the default
    credential chain or, with an access role, that role assumed from it through STS (as a ``CHAIN
    'sts'`` secret does). Credentials resolve at the first call, so a chain with nothing to resolve
    fails there, in the caller's hands.
    """
    session = boto3.Session(region_name=region)
    if not role_arn:
        return session.client(service)
    assumed = session.client("sts").assume_role(
        RoleArn=role_arn, RoleSessionName=_ROLE_SESSION_NAME
    )
    credentials = assumed["Credentials"]
    return boto3.client(
        service,
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def _is_s3_tables_child(catalog: Mapping[str, Any]) -> bool:
    """
    Whether a ``GetCatalogs`` entry is a table bucket under ``s3tablescatalog``: Glue names the
    parent in ``ParentCatalogNames`` (``["s3tablescatalog"]``) or, with that absent, only in the
    ``CatalogId`` (``<account>:s3tablescatalog/<bucket>``). The parent catalog itself is neither.
    """
    parents = catalog.get("ParentCatalogNames") or []
    if parents:
        return parents[0] == S3_TABLES_CATALOG
    catalog_id = str(catalog.get("CatalogId") or "")
    return f":{S3_TABLES_CATALOG}/" in catalog_id


def _list_s3_tables_catalogs(
    account: str, region: str, role_arn: Optional[str] = None
) -> List[str]:
    """
    The S3 Tables catalogs (table buckets) under a lakehouse connection's ``s3tablescatalog``: Glue
    ``GetCatalogs`` under the connection's ``account`` (``ParentCatalogId``; without it Glue lists
    the caller's account, another one for a cross-account connection) in ``region``, signed as the
    connection's catalogs are. Every table bucket, with databases or not.
    """
    glue = _aws_client("glue", region, role_arn)
    names: List[str] = []
    params: Dict[str, Any] = {"ParentCatalogId": account, "Recursive": True}
    while True:
        response = glue.get_catalogs(**params)
        for catalog in response.get("CatalogList") or []:
            if _is_s3_tables_child(catalog) and catalog.get("Name"):
                names.append(str(catalog["Name"]))
        next_token = response.get("NextToken")
        if not next_token:
            logger.info(
                "Account %s has %d S3 Tables catalog(s) in %s: %s",
                account,
                len(names),
                region,
                names,
            )
            return names
        params["NextToken"] = next_token


# --- state ---------------------------------------------------------------------------------------


@dataclass
class CatalogSecret:
    """A secret the SDK made for the attached databases to sign with."""

    name: str
    region: str
    #: The access role it assumes; ``None`` for the shared secret of the kernel's own identity.
    role_arn: Optional[str] = None
    #: The connection whose access role it assumes; ``None`` for the shared secret.
    connection_id: Optional[str] = None
    created_at: Optional[datetime] = None

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "region": self.region,
            "role_arn": self.role_arn,
            "connection_id": self.connection_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


@dataclass(frozen=True)
class RoleSigner:
    """The access role every database a statement ran against signs with, and whose databases they are."""

    role_arn: str
    #: The aliases the statement ran against, all signing as the role.
    aliases: List[str]
    #: The connection name(s) those databases were attached for.
    connections: List[str]


@dataclass
class AttachedCatalog:
    """One database the SDK attached (or tried to) for a connection: a Glue catalog, or an Athena connection."""

    alias: str
    connection_id: str
    connection_name: str
    #: The data catalog: ``AwsDataCatalog`` or the S3 Tables catalog's (table bucket's) name for a
    #: lakehouse connection, the one the workgroup exposes for an Athena connection.
    catalog: str
    #: :data:`ROUTE_GLUE` or :data:`ROUTE_ATHENA`.
    route: str
    #: The secret the ATTACH signs with; ``None`` when none could be made.
    secret: Optional[str] = None
    attached: bool = True
    error: Optional[str] = None

    def describe(self) -> Dict[str, Any]:
        return {
            "alias": self.alias,
            "connection_id": self.connection_id,
            "connection_name": self.connection_name,
            "catalog": self.catalog,
            "route": self.route,
            "secret": self.secret,
            "attached": self.attached,
            "error": self.error,
        }


@dataclass
class _Target:
    """One database to attach, and the statement that attaches it."""

    alias: str
    connection_id: str
    connection_name: str
    catalog: str
    route: str
    secret: str
    statement: str


def _glue_target(
    connection_id: str, connection_name: str, catalog: str, account: str, region: str, secret: str
) -> _Target:
    """A lakehouse connection's catalog, from Glue's Iceberg REST endpoint, signing with ``secret``."""
    alias = catalog_alias(connection_name, catalog)
    s3_tables_catalog = None if catalog == AWS_DATA_CATALOG else catalog
    return _Target(
        alias,
        connection_id,
        connection_name,
        catalog,
        ROUTE_GLUE,
        secret,
        glue_attach_statement(
            alias,
            account,
            region,
            secret,
            s3_tables_catalog,
            unstaged_creates=_has_unstaged_creates(),
        ),
    )


def _athena_target(record: Mapping[str, Any], region: str, secret: str) -> _Target:
    """An Athena connection, as its workgroup in its region, signing with ``secret``."""
    connection_id, name, catalog = _record_id(record), _record_name(record), _athena_catalog(record)
    alias = athena_alias(name)
    return _Target(
        alias,
        connection_id,
        name,
        catalog,
        ROUTE_ATHENA,
        secret,
        athena_attach_statement(alias, region, athena_workgroup(record), secret, catalog),
    )


class LocalCatalogs:
    """
    The databases and secrets on one DuckDB engine for the project's connections; one per kernel
    (``duckdbutils`` keeps it and passes the engine and the listing in).

    ``_round_lock`` serialises the rounds (:meth:`attach_all`, :meth:`reset`); ``_lock`` guards the
    records and is held only while they are read or written, never across a DuckDB statement or an
    AWS call. The rounds run under the engine's lock (``engine._lock``), taken before these two.
    """

    def __init__(self) -> None:
        self._round_lock = threading.RLock()
        self._lock = threading.RLock()
        self._attached: Dict[str, AttachedCatalog] = {}
        self._secrets: Dict[str, CatalogSecret] = {}

    # -- what is there -----------------------------------------------------------------------

    def attached(self) -> List[AttachedCatalog]:
        """Every database the SDK attached, or tried to, since the last :meth:`reset`."""
        with self._lock:
            return sorted(self._attached.values(), key=lambda c: c.alias)

    def secrets(self) -> List[CatalogSecret]:
        with self._lock:
            return sorted(self._secrets.values(), key=lambda s: s.name)

    def empty(self) -> bool:
        with self._lock:
            return not self._attached and not self._secrets

    def role_signing(self, statement: str, search_path: str) -> Optional[RoleSigner]:
        """
        The access role every attached database ``statement`` runs against (:func:`catalogs_named`)
        signs with, for naming who a refusal was answered to. ``None`` when the statement runs
        against no attached database, against one signing as the kernel's own identity, or against
        databases signing as different identities (the refused one cannot then be told apart).
        """
        with self._lock:
            attached = {
                alias: record for alias, record in self._attached.items() if record.attached
            }
            role_of = {name: secret.role_arn for name, secret in self._secrets.items()}
        named = catalogs_named(statement, search_path, attached)
        if not named:
            return None
        roles: Set[Optional[str]] = set()
        connections: List[str] = []
        for alias in named:
            record = attached[alias]
            roles.add(role_of.get(record.secret or ""))
            if record.connection_name not in connections:
                connections.append(record.connection_name)
        if len(roles) != 1:
            return None
        role = roles.pop()
        return RoleSigner(role, named, connections) if role else None

    # -- kernel start, and every change the frontend reports --------------------------------

    def attach_all(self, duck, records: Sequence[ConnectionRecord]) -> List[AttachedCatalog]:
        """
        Start over from ``records`` (the project's listing, without credentials): :meth:`reset`,
        then attach every ``LAKEHOUSE`` connection's Glue catalogs and every ``ATHENA`` connection's
        workgroup, each signing with its region's shared secret or a secret assuming its access
        role. One connection failing never stops the others; the outcome is on each
        :class:`AttachedCatalog`. An empty listing attaches nothing. Holds the round lock throughout
        and the records lock only around each record, so a reader is answered while the round waits
        on DuckDB or AWS.
        """
        with self._round_lock:
            self.reset(duck)
            if not records:
                logger.info("The project lists no connections (signed out?); nothing is attached")
                return self.attached()
            started = time.monotonic()
            lakehouses = sorted(
                (r for r in records if _record_type(r) == TYPE_LAKEHOUSE),
                key=lambda r: (not is_default_lakehouse(_record_name(r)), _record_name(r)),
            )
            athenas = sorted(
                (r for r in records if _record_type(r) == TYPE_ATHENA), key=_record_name
            )
            logger.info(
                "Attaching the project's catalogs to DuckDB: %d connection(s) listed, %d lakehouse and %d Athena",
                len(records),
                len(lakehouses),
                len(athenas),
            )
            athena_loaded = bool(athenas) and _athena_extension_loaded(duck)
            if athenas and not athena_loaded:
                logger.warning(
                    "%d Athena connection(s) not attached: the athena DuckDB extension is not loaded",
                    len(athenas),
                )
            # alias -> its holder's outcome this round, to notice collisions
            taken: Dict[str, AttachedCatalog] = {}
            for record in lakehouses:
                connection_id, name = _record_id(record), _record_name(record)
                account, region, role = _record_location(record)
                if not account or not region:
                    self._fail_connection(
                        connection_id,
                        name,
                        _NO_ACCOUNT_OR_REGION,
                        catalog_alias(name, AWS_DATA_CATALOG),
                        AWS_DATA_CATALOG,
                        ROUTE_GLUE,
                    )
                    continue
                try:
                    secret = self._ensure_secret(duck, connection_id, region, role)
                except (
                    Exception
                ) as e:  # noqa: BLE001 - no credentials to resolve, or DuckDB refused the secret
                    self._fail_connection(
                        connection_id,
                        name,
                        str(e),
                        catalog_alias(name, AWS_DATA_CATALOG),
                        AWS_DATA_CATALOG,
                        ROUTE_GLUE,
                    )
                    continue
                try:
                    s3_tables = _list_s3_tables_catalogs(account, region, role)
                except Exception as e:  # noqa: BLE001 - the AwsDataCatalog still attaches
                    logger.warning(
                        "Could not list the S3 Tables catalogs of connection %r: %s", name, e
                    )
                    s3_tables = []
                for catalog in [AWS_DATA_CATALOG, *s3_tables]:
                    self._attach_unless_taken(
                        duck,
                        _glue_target(connection_id, name, catalog, account, region, secret.name),
                        taken,
                    )
            for record in athenas:
                connection_id, name = _record_id(record), _record_name(record)
                alias, catalog = athena_alias(name), _athena_catalog(record)
                if not athena_loaded:
                    self._fail_connection(
                        connection_id,
                        name,
                        _NO_ATHENA_EXTENSION,
                        alias,
                        catalog,
                        ROUTE_ATHENA,
                        log=False,
                    )
                    continue
                _account, region, role = _record_location(record)
                if not region:
                    self._fail_connection(
                        connection_id, name, _NO_REGION, alias, catalog, ROUTE_ATHENA
                    )
                    continue
                try:
                    secret = self._ensure_secret(duck, connection_id, region, role)
                except Exception as e:  # noqa: BLE001 - as above
                    self._fail_connection(connection_id, name, str(e), alias, catalog, ROUTE_ATHENA)
                    continue
                self._attach_unless_taken(duck, _athena_target(record, region, secret.name), taken)
            outcome = self.attached()
            failed = [c for c in outcome if not c.attached]
            logger.info(
                "Catalog round done in %.1fs: %d database(s) attached, %d not%s",
                time.monotonic() - started,
                len(outcome) - len(failed),
                len(failed),
                f" ({', '.join(c.alias for c in failed)})" if failed else "",
            )
            return outcome

    def reset(self, duck) -> Dict[str, AttachedCatalog]:
        """
        Detach every database the SDK attached and drop every secret it made (every secret scoped to
        :data:`SECRET_SCOPE`) and the ``iceberg`` extension's vended table credentials; a user's own
        databases and secrets are not touched. A database DuckDB would not detach stays on record
        with the reason; its secret goes all the same. Returns what stayed.
        """
        with self._round_lock:
            with self._lock:
                to_detach = [
                    self._attached[alias]
                    for alias in sorted(self._attached)
                    if self._attached[alias].attached
                ]
                names: Set[str] = set(self._secrets)
            kept: Dict[str, AttachedCatalog] = {}
            for record in to_detach:
                refusal = self._detach(duck, record.alias)
                if refusal is not None:
                    record.error = f"still attached: DuckDB would not detach it ({refusal})"
                    kept[record.alias] = record
            names.update(present_secrets(duck) or [])
            names.update(vended_secret_names(duck))
            dropped = drop_secrets(duck, sorted(names))
            if to_detach or dropped:
                logger.info(
                    "Detached %d of %d database(s) and dropped %d secret(s)%s",
                    len(to_detach) - len(kept),
                    len(to_detach),
                    len(dropped),
                    f"; still attached: {', '.join(sorted(kept))}" if kept else "",
                )
            with self._lock:
                self._attached = dict(kept)
                self._secrets.clear()
            return kept

    # -- pieces --------------------------------------------------------------------------------

    def _ensure_secret(
        self, duck, connection_id: str, region: str, role_arn: Optional[str]
    ) -> CatalogSecret:
        """The secret a connection's databases sign with: ``region``'s shared secret (made once
        per round) for a connection without an access role, else one of its own assuming the role.
        """
        if role_arn:
            name = role_secret_name(connection_id)
            statement = create_role_secret_statement(name, role_arn, region)
        else:
            name = chain_secret_name(region)
            with self._lock:
                existing = self._secrets.get(name)
            if existing is not None:
                return existing
            statement = create_chain_secret_statement(name, region)
        duck.sql(
            statement + ";"
        )  # resolves the chain (and assumes the role): outside the records lock
        secret = CatalogSecret(
            name, region, role_arn, connection_id if role_arn else None, datetime.now(timezone.utc)
        )
        with self._lock:
            self._secrets[name] = secret
        if role_arn:
            logger.info(
                "DuckDB secret %s created, assuming %s for connection %s",
                name,
                role_arn,
                connection_id,
            )
        else:
            logger.info("DuckDB secret %s created for the kernel's identity in %s", name, region)
        return secret

    def _fail_connection(
        self,
        connection_id: str,
        name: str,
        error: str,
        alias: str,
        catalog: str,
        route: str,
        log: bool = True,
    ) -> None:
        """Record under ``alias`` (its Athena alias, or its ``AwsDataCatalog``'s) that nothing of
        this connection is attached, so the failure shows in :meth:`attached`, not only in the log.
        """
        if log:
            logger.warning("Connection %r not attached: %s", name, error)
        with self._lock:
            if alias not in self._attached:
                self._attached[alias] = AttachedCatalog(
                    alias, connection_id, name, catalog, route, None, attached=False, error=error
                )

    def _attach_unless_taken(
        self, duck, target: _Target, taken: Dict[str, AttachedCatalog]
    ) -> None:
        """
        Attach ``target`` unless its alias is taken: by another connection this round (``taken``),
        or by a database of the previous round DuckDB would not detach (kept by :meth:`reset`). The
        first connection in the round's order holds the alias whether or not its ATTACH succeeded,
        so the alias means the same connection on every round; releasing it on a failed ATTACH would
        let a transient failure switch which catalog a query against the alias reads.
        """
        holder = taken.get(target.alias)
        if holder is not None:
            if holder.attached:
                logger.warning(
                    "%r of connection %r is not attached: connection %r already attaches a database as %r",
                    target.catalog,
                    target.connection_name,
                    holder.connection_name,
                    target.alias,
                )
            else:
                logger.warning(
                    "%r of connection %r is not attached: the alias %r is connection %r's, whose attach "
                    "failed (%s); it stays that connection's, so fix that or rename one of the two",
                    target.catalog,
                    target.connection_name,
                    target.alias,
                    holder.connection_name,
                    holder.error,
                )
            return
        with self._lock:
            stale = self._attached.get(target.alias)
        if stale is not None and stale.attached:
            stale.error = (
                f"still the previous database: DuckDB would not detach it, so {target.catalog!r} of connection "
                f"{target.connection_name!r} is not attached as {target.alias!r}; the next "
                "sqlutils.attach_local_catalogs() tries again"
            )
            logger.warning(stale.error)
            return
        attached = self._attach(
            duck, target
        )  # the ATTACH, a network call: outside the records lock
        taken[target.alias] = attached
        with self._lock:
            self._attached[target.alias] = attached

    def _attach(self, duck, target: _Target) -> AttachedCatalog:
        """Run the target's ATTACH; one database failing never stops the others."""
        logger.debug("%s", target.statement)  # names the secret; never holds credentials
        try:
            duck.sql(target.statement + ";")
        except Exception as e:  # noqa: BLE001 - recorded on the database
            logger.warning(
                "Could not attach %r of connection %r as %r through %s: %s",
                target.catalog,
                target.connection_name,
                target.alias,
                target.route,
                e,
            )
            return AttachedCatalog(
                target.alias,
                target.connection_id,
                target.connection_name,
                target.catalog,
                target.route,
                target.secret,
                attached=False,
                error=f"{target.route}: {e}",
            )
        logger.info(
            "Attached %r of connection %r as %r through %s",
            target.catalog,
            target.connection_name,
            target.alias,
            target.route,
        )
        return AttachedCatalog(
            target.alias,
            target.connection_id,
            target.connection_name,
            target.catalog,
            target.route,
            target.secret,
        )

    def _detach(self, duck, alias: str) -> Optional[str]:
        """``DETACH`` one database; ``None`` when DuckDB took it, else what it said."""
        try:
            duck.sql(detach_statement(alias) + ";")
            logger.info("Detached %r", alias)
            return None
        except Exception as e:  # noqa: BLE001 - reported to the caller
            logger.warning("Could not detach %r: %s", alias, e)
            return str(e)


#: The kernel's one record of what is attached: ``duckdbutils`` and the engine share it.
_state = LocalCatalogs()


__all__ = [
    "AWS_DATA_CATALOG",
    "ROUTE_ATHENA",
    "ROUTE_GLUE",
    "S3_TABLES_CATALOG",
    "SECRET_PREFIX",
    "SECRET_SCOPE",
    "VENDED_SECRET_PREFIX",
    "AttachedCatalog",
    "CatalogSecret",
    "LocalCatalogs",
    "athena_alias",
    "athena_attach_statement",
    "catalog_alias",
    "chain_secret_name",
    "create_chain_secret_statement",
    "create_role_secret_statement",
    "detach_statement",
    "drop_secret_statement",
    "drop_secrets",
    "glue_attach_statement",
    "glue_catalog_id",
    "is_default_lakehouse",
    "present_secrets",
    "role_secret_name",
    "search_path_entry",
    "search_path_identifier",
    "sql_identifier",
    "sql_literal",
    "vended_secret_names",
]
