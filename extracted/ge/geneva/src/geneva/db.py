# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import base64
import contextlib
import copy
import hashlib
import logging
import warnings
from collections.abc import Callable, Iterable
from datetime import timedelta
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar
from urllib.parse import urlparse

import attrs
import lancedb
import pyarrow as pa
from lance_namespace import (
    LanceNamespace,
    ListNamespacesResponse,
    ListTablesResponse,
)
from lance_namespace import connect as namespace_connect
from lancedb import DBConnection, LanceNamespaceDBConnection
from lancedb.common import DATA, Credential
from lancedb.pydantic import LanceModel
from lancedb.table import Table as LanceDBTable
from lancedb.util import get_uri_scheme
from overrides import override
from yarl import URL

from geneva._namespace_client import with_geneva_user_agent
from geneva.checkpoint import CheckpointStore
from geneva.cluster import GenevaClusterType
from geneva.config import ConfigBase
from geneva.credentials import (
    refresh_storage_options as refresh_storage_options,
)
from geneva.credentials import (
    revend_storage_options as revend_storage_options,
)
from geneva.namespace_properties import is_sensitive_namespace_property
from geneva.packager import DockerUDFPackager, UDFPackager
from geneva.packager.autodetect import upload_local_env
from geneva.packager.uploader import Uploader

if TYPE_CHECKING:
    import lance
    from lance_namespace import MaterializedViewUdtfEntry

    from geneva.cluster.mgr import ClusterConfigManager, GenevaCluster
    from geneva.jobs.jobs import JobRecord, JobStateManager
    from geneva.manifest.mgr import GenevaManifest, ManifestConfigManager
    from geneva.query import GenevaQueryBuilder
    from geneva.table import Table
    from geneva.transformer import UDTF, Chunker

_LOG = logging.getLogger(__name__)

T = TypeVar("T")

SYSTEM_NAMESPACE = "__system"


def _directory_namespace_storage_properties(
    storage_options: dict[str, Any] | None,
) -> dict[str, str]:
    if not storage_options:
        return {}
    return {
        key if key.startswith("storage.") else f"storage.{key}": str(value)
        for key, value in storage_options.items()
    }


_REDACTED_NAMESPACE_VALUE = "********"


class _RedactedNamespaceProperties(dict[str, str]):
    def __repr__(self) -> str:
        return repr(
            {
                key: (
                    _REDACTED_NAMESPACE_VALUE
                    if is_sensitive_namespace_property(key)
                    else value
                )
                for key, value in self.items()
            }
        )

    __str__ = __repr__

    def copy(self) -> "_RedactedNamespaceProperties":
        return _RedactedNamespaceProperties(self)


def _as_namespace_client_properties(
    properties: dict[str, str] | None,
) -> dict[str, str] | None:
    if properties is None:
        return None
    if isinstance(properties, _RedactedNamespaceProperties):
        return properties
    return _RedactedNamespaceProperties(properties)


# Lance internal columns that are always available but not in the user schema
_LANCE_INTERNAL_COLUMNS = {"_rowid", "_rowaddr"}

# Key for storing worker host override in namespace_client_properties
WORKER_URI_KEY = "worker_uri"


@attrs.define
class NamespaceConfig:
    """Bundled namespace configuration for Geneva connections and table references.

    Groups the namespace client settings (implementation type, properties,
    pushdown operations) with the system namespace path that controls where
    system tables are located.
    """

    namespace_client_impl: str | None = None
    namespace_client_properties: dict[str, str] | None = attrs.field(
        default=None, repr=False
    )
    namespace_client_pushdown_operations: list[str] | None = None
    system_namespace: list[str] | None = None

    def get_worker_properties(self) -> dict[str, str] | None:
        """Transform properties for worker context.

        When workers connect to the namespace server, they should use the
        internal worker endpoint (worker_uri) instead of the external
        endpoint (uri) if available.
        """
        if self.namespace_client_properties is None:
            return None
        if WORKER_URI_KEY not in self.namespace_client_properties:
            return self.namespace_client_properties
        props = _RedactedNamespaceProperties(self.namespace_client_properties)
        worker_uri = props.pop(WORKER_URI_KEY)
        props["uri"] = worker_uri
        return props

    def connect_namespace_client(
        self, *, use_worker_props: bool = False
    ) -> LanceNamespace | None:
        """Create a LanceNamespace client, or ``None`` if not configured.

        Parameters
        ----------
        use_worker_props
            When ``True``, swap the external ``uri`` for the internal
            ``worker_uri`` endpoint (used inside Ray workers).
        """
        if (
            self.namespace_client_impl is None
            or self.namespace_client_properties is None
        ):
            return None
        props = (
            self.get_worker_properties()
            if use_worker_props
            else self.namespace_client_properties
        )
        assert props is not None
        props = with_geneva_user_agent(self.namespace_client_impl, props)
        return namespace_connect(self.namespace_client_impl, props)

    def for_worker(self) -> "NamespaceConfig":
        """Return a copy with properties transformed for worker context."""
        return attrs.evolve(
            self,
            namespace_client_properties=self.get_worker_properties(),
        )


_CLOUD_URI_SCHEMES: tuple[str, ...] = (
    "az://",
    "abfs://",
    "abfss://",
    "adls://",
    "s3://",
    "s3+ddb://",
    "gs://",
    "gcs://",
)


def _b64_str(value: str | bytes) -> str:
    """Base64-encode a JSON envelope / Arrow schema for the namespace API."""
    raw = value.encode("utf-8") if isinstance(value, str) else value
    return base64.b64encode(raw).decode("ascii")


def _build_udtf_entry(
    kind: str,
    *,
    spec_json: str,
    udtf_name: str,
    udtf_version: str,
    input_columns: list[str] | None,
    partition_by: str | None = None,
    num_cpus: float | int | None = None,
    num_gpus: float | int | None = None,
    memory: int | None = None,
    batch: bool | None = None,
    manifest_json: str | None = None,
    manifest_checksum: str | None = None,
) -> "MaterializedViewUdtfEntry":
    """Build a `MaterializedViewUdtfEntry` for the namespace API.

    The envelope is the JSON form of a `UDTFSpec` (kind=`udtf`) or
    `ChunkerSpec` (kind=`chunker`). It is base64-encoded for transport
    and the SHA-256 of the base64 payload accompanies it so the server
    can validate the round-trip.
    """
    from lance_namespace import MaterializedViewUdtfEntry

    envelope_b64 = _b64_str(spec_json)
    envelope_sha = hashlib.sha256(envelope_b64.encode("ascii")).hexdigest()
    return MaterializedViewUdtfEntry(
        kind=kind,
        udtf=envelope_b64,
        udtf_sha=envelope_sha,
        udtf_name=udtf_name,
        udtf_version=udtf_version,
        input_columns=input_columns,
        partition_by=partition_by,
        num_cpus=num_cpus,
        num_gpus=num_gpus,
        memory=memory,
        batch=batch,
        manifest=manifest_json,
        manifest_checksum=manifest_checksum,
    )


def _warn_if_cloud_uri_missing_storage_options(
    uri: str | None,
    storage_options: dict[str, str] | None,
    *,
    has_namespace_client: bool,
) -> None:
    """Emit a warning when a cloud URI is opened without storage_options.

    Catches the data-flow shape where credentials exist on a Connection but
    a chain of intermediary objects fails to thread them into the dataset
    open. Skipped when a namespace_client is in play (the client may vend
    credentials internally) or when the caller has explicitly populated
    storage_options.
    """
    if has_namespace_client:
        return
    if storage_options:
        return
    if uri is None:
        return
    if not uri.startswith(_CLOUD_URI_SCHEMES):
        return
    _LOG.warning(
        "Opening cloud URI %r with no storage_options. If credentials live "
        "in storage_options on your Connection rather than environment "
        "variables / instance metadata, this open will likely fail with "
        "'no Azure account name in URI' or similar. Check that the call site "
        "is forwarding storage_options from the surrounding Connection / "
        "TableReference.",
        uri,
    )


def open_lance_dataset(
    uri: str | None = None,
    *,
    namespace_config: NamespaceConfig | None = None,
    namespace_client: LanceNamespace | None = None,
    table_id: list[str] | None = None,
    version: int | None = None,
    storage_options: dict[str, str] | None = None,
    use_worker_props: bool = False,
) -> Any:
    """Open a Lance dataset, using namespace client when configured.

    Callers provide **either** a *uri* for direct storage access **or**
    namespace parameters (*namespace_config* / *namespace_client* +
    *table_id*) for catalog-managed access.  When both are supplied the
    namespace path takes precedence.

    Parameters
    ----------
    uri
        Physical dataset URI (used when no namespace client is available).
    namespace_config
        Namespace configuration.  A namespace client is created from it
        unless *namespace_client* is already supplied.
    namespace_client
        Pre-connected namespace client.  Takes precedence over
        *namespace_config*.
    table_id
        Namespace table identifier (required for namespace path).
    version
        Dataset version to open.
    storage_options
        Storage options forwarded to ``lance.dataset()``.
    use_worker_props
        When ``True`` and creating a client from *namespace_config*, use
        the internal worker endpoint instead of the external one.
    """
    import lance

    ns_client = namespace_client or (
        namespace_config.connect_namespace_client(use_worker_props=use_worker_props)
        if namespace_config
        else None
    )
    _warn_if_cloud_uri_missing_storage_options(
        uri,
        storage_options,
        has_namespace_client=ns_client is not None,
    )
    # Vended credentials snapshotted at plan time expire on long-running jobs;
    # re-vend fresh ones before opening so worker reads don't sign S3 requests
    # with an expired token. No-op for static / non-namespace credentials.
    if table_id is not None:
        storage_options = refresh_storage_options(
            storage_options,
            table_id=table_id,
            namespace_client=ns_client,
            namespace_config=namespace_config,
            use_worker_props=use_worker_props,
        )
    if ns_client is not None and table_id is not None:
        kwargs: dict[str, Any] = {
            "namespace_client": ns_client,
            "table_id": table_id,
        }
        if version is not None:
            kwargs["version"] = version
        if storage_options is not None:
            kwargs["storage_options"] = storage_options
        try:
            return lance.dataset(**kwargs)
        except Exception as exc:
            if uri is None:
                raise
            msg = str(exc).lower()
            namespace_arg_type_error = isinstance(exc, TypeError) and (
                "namespace_client" in msg or "table_id" in msg
            )
            directory_namespace_not_found = (
                "table not found" in msg
                and namespace_config is not None
                and namespace_config.namespace_client_impl == "dir"
            )
            if not namespace_arg_type_error and not directory_namespace_not_found:
                raise
            _LOG.warning(
                "Falling back to physical dataset URI for table_id=%s after "
                "namespace open failed: %s",
                table_id,
                exc,
            )
    kwargs = {}
    if version is not None:
        kwargs["version"] = version
    if storage_options is not None:
        kwargs["storage_options"] = storage_options
    return lance.dataset(uri, **kwargs)


def has_stable_row_ids(fragments: "Iterable[lance.LanceFragment]") -> bool:
    """Check if Lance fragments have stable row IDs enabled.

    Stable row IDs are indicated by presence of row_id_meta on fragment metadata.
    This is a Lance feature (added in v0.21.0) that ensures row identifiers remain
    constant even when table operations like compaction reorganize the physical data.

    Parameters
    ----------
    fragments : Iterable[lance.LanceFragment]
        Lance fragments to check (from dataset.get_fragments())

    Returns
    -------
    bool
        True if any fragment has stable row IDs enabled, False otherwise
    """
    return any(frag.metadata.row_id_meta is not None for frag in fragments)


def dataset_uses_stable_row_ids(dataset: "lance.LanceDataset") -> bool:
    """Return whether a Lance dataset manifest enables stable row IDs."""
    return dataset.has_stable_row_ids


class Connection:
    """Geneva Connection.

    Deliberately *not* a subclass of ``lancedb.DBConnection``. Geneva holds a
    real lancedb connection as ``_connect`` and delegates to it, so inheriting
    the ABC bought no behavior -- 19 of its 22 members are
    ``NotImplementedError`` stubs -- while making lancedb's namespace part of
    Geneva's contract: any method lancedb adds whose name Geneva already uses
    is rejected outright by ``EnforceOverrides`` at class-definition time,
    which is how ``create_materialized_view`` in lancedb 0.38 broke every
    Geneva job at import. Composition ends that coupling. See
    ``DBConnection.register`` below, which keeps ``isinstance`` working.
    """

    def __init__(
        self,
        uri: str,
        *,
        region: str = "us-east-1",
        api_key: Credential | None = None,
        host_override: str | None = None,
        storage_options: dict[str, str] | None = None,
        checkpoint_store: CheckpointStore | None = None,
        packager: UDFPackager | None = None,
        namespace_client_impl: str | None = None,
        namespace_client_properties: dict[str, str] | None = None,
        namespace_client_pushdown_operations: list[str] | None = None,
        system_namespace: list[str],
        executor_mode: bool = False,
        **kwargs,
    ) -> None:
        self._uri = uri
        self._region = region
        self._api_key = api_key
        self._host_override = host_override
        self._storage_options = storage_options
        self._checkpoint_store = checkpoint_store
        self._packager = packager or DockerUDFPackager()
        self._executor_mode = executor_mode
        ns_cfg = NamespaceConfig(
            namespace_client_impl=namespace_client_impl,
            namespace_client_properties=_as_namespace_client_properties(
                namespace_client_properties
            ),
            namespace_client_pushdown_operations=namespace_client_pushdown_operations,
        )
        self._ns_config = attrs.evolve(ns_cfg, system_namespace=system_namespace)

        self._jobs_manager: JobStateManager | None = None
        self._cluster_manager: ClusterConfigManager | None = None
        self._manifest_manager: ManifestConfigManager | None = None
        self._flight_client: Any | None = None
        self._namespace_connection: LanceNamespaceDBConnection | None = None
        self._system_namespace_ensured = False
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"<Geneva uri={self.uri}>"

    # -- Formerly inherited from lancedb's DBConnection --
    #
    # Everything else the ABC offered was a NotImplementedError stub, so these
    # two are the whole of what dropping the base class cost us.

    @property
    def uri(self) -> str:
        """URI of the database this connection points at."""
        return self._uri

    def list_namespaces(
        self,
        namespace_path: list[str] | None = None,
        page_token: str | None = None,
        limit: int | None = None,
    ) -> ListNamespacesResponse:
        """List the namespaces under ``namespace_path``."""
        return self._connect.list_namespaces(
            namespace_path=namespace_path, page_token=page_token, limit=limit
        )

    # -- Namespace property accessors (delegate to _ns_config) --

    @property
    def namespace_client_impl(self) -> str | None:
        return self._ns_config.namespace_client_impl

    @property
    def namespace_client_properties(self) -> dict[str, str] | None:
        return self._ns_config.namespace_client_properties

    @property
    def namespace_client_pushdown_operations(self) -> list[str] | None:
        return self._ns_config.namespace_client_pushdown_operations

    @property
    def system_namespace(self) -> list[str]:
        return self._ns_config.system_namespace or []

    def __getstate__(self) -> dict:
        return {
            "uri": self._uri,
            "api_key": self._api_key,
            "host_override": self._host_override,
            "storage_options": self._storage_options,
            "region": self._region,
            "namespace_client_impl": self.namespace_client_impl,
            "namespace_client_properties": self.namespace_client_properties,
            "namespace_client_pushdown_operations": (
                self.namespace_client_pushdown_operations
            ),
            "system_namespace": self.system_namespace,
            "executor_mode": self._executor_mode,
        }

    def __setstate__(self, state) -> None:
        state.pop("upload_dir", None)
        state.pop("is_system_db_root", None)
        state.pop("checkpoint_store", None)
        self.__init__(state.pop("uri"), **state)

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
        return None  # Don't suppress exceptions

    def close(self) -> None:
        """Close the connection."""
        if self._flight_client is not None:
            self._flight_client.close()

    @property
    def user_db_uri(self) -> str:
        """Original user database URI for this connection."""
        return str(self.uri)

    def _run_system_table_operation(
        self,
        table_name: str,
        operation: Callable[["Connection", list[str]], T],
        *,
        namespace: list[str] | None = None,
    ) -> T:
        """Run a system-table operation in its resolved location."""
        target_namespace = namespace if namespace is not None else self.system_namespace
        if target_namespace:
            _ensure_system_namespace_exists(self)
        return operation(self, target_namespace)

    def _directory_namespace_root_uri(self) -> str | None:
        if self.namespace_client_impl != "dir" or not self.namespace_client_properties:
            return None
        root = self.namespace_client_properties.get("root")
        return str(root) if root else None

    def _supports_stable_row_ids_on_create(self) -> bool:
        """Whether ``create_table`` can enable stable row IDs on this backend.

        True everywhere. ``_connect`` always resolves to a
        ``LanceNamespaceDBConnection``, which reads
        ``new_table_enable_stable_row_ids`` out of the per-request storage
        options and performs the Lance write client-side; a directory namespace
        gets there via the root-table detour in
        ``_create_directory_namespace_root_table``.

        This used to return False for ``rest`` namespaces -- i.e. every
        enterprise deployment -- which silently created materialized-view tables
        without stable row IDs. Stable row IDs are write-time only, so those
        tables could not be repaired afterwards (GEN-839).
        """
        return True

    def _create_directory_namespace_root_table(
        self,
        name: str,
        data: DATA | None,
        schema: pa.Schema | LanceModel | None,
        mode: str,
        *args,
        fill_value: float,
        storage_options: dict[str, Any] | None,
        **kwargs,
    ) -> Any:
        """Create table directly at directory namespace root, then register it.

        # TODO: Remove this workaround once LanceNamespaceDBConnection passes
        # storage_options (e.g. new_table_enable_stable_row_ids) through to the
        # underlying Lance write. At that point, all create_table calls can go
        # through the namespace connection uniformly.
        """
        from lance_namespace import RegisterTableRequest

        root = self._directory_namespace_root_uri()
        assert root is not None
        direct_conn = lancedb.connect(root, storage_options=self._storage_options)
        try:
            created = direct_conn.create_table(
                name,
                data,
                schema,
                mode,
                *args,
                fill_value=fill_value,
                storage_options=storage_options,
                **kwargs,
            )
        except Exception as exc:
            if (
                not kwargs.get("exist_ok", False)
                or "already exists" not in str(exc).lower()
            ):
                raise
            created = direct_conn.open_table(
                name, storage_options=self._storage_options
            )
        try:
            self.namespace_client().register_table(
                RegisterTableRequest(id=[name], location=f"{name}.lance")
            )
        except Exception as exc:
            if "already exists" not in str(exc).lower():
                raise
        return created

    def alter_or_create_system_table(
        self,
        table_name: str,
        model: Any,
        namespace: list[str] | None = None,
    ) -> tuple["Connection", list[str], LanceDBTable]:
        """Open or create a Geneva internal table in its resolved location."""
        from geneva.utils.schema import alter_or_create_table

        return self._run_system_table_operation(
            table_name,
            lambda target_db, target_namespace: (
                target_db,
                target_namespace,
                alter_or_create_table(
                    target_db,
                    table_name,
                    model,
                    namespace_path=target_namespace,
                ),
            ),
            namespace=namespace,
        )

    def namespace_client(self) -> LanceNamespace:
        """Returns namespace client from the underlying LanceDB connection."""
        return self._connect.namespace_client()

    @cached_property
    def _connect(self) -> DBConnection:
        if not self._namespace_connection:
            ns_client = self._ns_config.connect_namespace_client()
            assert ns_client is not None, (
                "namespace_client_properties must be set when "
                "namespace_client_impl is set"
            )

            ns_properties = self.namespace_client_properties
            self._namespace_connection = LanceNamespaceDBConnection(
                ns_client,
                storage_options=self._storage_options,
                namespace_client_pushdown_operations=self.namespace_client_pushdown_operations,
                namespace_client_impl=self.namespace_client_impl,
                namespace_client_properties=dict(ns_properties)
                if ns_properties
                else None,
                **self._kwargs,
            )
            if not hasattr(self._namespace_connection, "_uri"):
                self._namespace_connection._uri = self.uri  # pyright: ignore[reportAttributeAccessIssue]
        _LOG.info(f"using namespace connection: {self._namespace_connection=}")
        return self._namespace_connection

    @cached_property
    def _history(self) -> "JobStateManager":  # noqa: F821
        """Returns a JobStateManager that persists job executions and statuses"""
        from geneva.jobs import JobStateManager

        if self._jobs_manager is None:
            self._jobs_manager = JobStateManager(self)
        return self._jobs_manager

    @cached_property
    def flight_client(self) -> Any:
        if self._flight_client is not None:
            return self._flight_client
        import flightsql

        flightsql_client = flightsql.FlightSQLClient
        url = urlparse(self._host_override)
        hostname = url.hostname
        client = flightsql_client(
            host=hostname,
            port=10025,
            token="DATABASE_TOKEN",  # Dummy auth, not plugged in yet
            metadata={"database": self.uri},  # Name of the project-id
            features={"metadata-reflection": "true"},
            insecure=True,  # or False, up to you
        )
        self._flight_client = client
        return client

    def table_names(
        self, page_token: str | None = None, limit: int | None = None, *args, **kwargs
    ) -> Iterable[str]:
        """List all available tables and views."""
        return self._connect.table_names(
            *args, page_token=page_token, limit=limit or 10, **kwargs
        )

    def list_tables(
        self,
        namespace_path: list[str] | None = None,
        page_token: str | None = None,
        limit: int | None = None,
    ) -> ListTablesResponse:
        """List all tables in this database with pagination support.

        Parameters
        ----------
        namespace_path : list[str], optional
            The namespace to list tables in.
            None or empty list represents root namespace.
        page_token : str, optional
            Token for pagination. Use the token from a previous response
            to get the next page of results.
        limit : int, optional
            The maximum number of results to return.

        Returns
        -------
        ListTablesResponse
            Response containing table names and optional page_token for pagination.
        """
        return self._connect.list_tables(
            namespace_path=namespace_path,
            page_token=page_token,
            limit=limit,
        )

    def open_table(
        self,
        name: str,
        storage_options: dict[str, str] | None = None,
        index_cache_size: int | None = None,
        version: int | None = None,
        namespace: list[str] | None = None,
        *args,
        **kwargs,
    ) -> "Table":
        """Open a Lance Table.

        Parameters
        ----------
        name: str
            Name of the table.
        storage_options: dict[str, str], optional
            Additional options for the storage backend.
            Options already set on the connection will be inherited by the table,
            but can be overridden here. See available options at
            [https://lancedb.github.io/lancedb/guides/storage/](https://lancedb.github.io/lancedb/guides/storage/)
        namespace: list[str], optional
            Namespace path for the table (e.g., ["workspace"])

        """
        from .table import NativeTable

        # Merge (not ``or``) so a truthy-but-partial caller dict does not drop
        # the connection's credentials; caller options override on conflict.
        storage_options = {
            **(self._storage_options or {}),
            **(storage_options or {}),
        } or None

        # Support both namespace argument spellings to ease migration
        namespace_path = kwargs.pop("namespace_path", None)
        if namespace_path is not None:
            namespace = namespace_path

        namespace = namespace if namespace is not None else []
        tbl = NativeTable(
            self,
            name,
            namespace=namespace,
            index_cache_size=index_cache_size,
            storage_options=storage_options,
            version=version,
        )

        return tbl

    def _validate_existing_table_has_stable_row_ids(
        self, name: str, namespace_path: list[str] | None = None
    ) -> None:
        """Validate that an existing table has stable row IDs enabled.

        Called when exist_ok=True and stable row IDs are requested, to ensure
        the existing table matches the requested configuration.

        Raises:
            ValueError: If table exists with data but doesn't have stable row IDs
        """
        # Open directly (namespace-aware) rather than pre-checking root-only
        # table_names(): a not-found / unopenable table simply has nothing to
        # validate, so treat an open failure as the early-return case.
        try:
            table = self._connect.open_table(
                name,
                namespace_path=namespace_path,
                storage_options=self._storage_options,
            )
            # Lazy import: geneva.query imports geneva.db at module load.
            from geneva.query import open_read_dataset

            dataset = open_read_dataset(table)  # type: ignore[arg-type]
        except Exception as e:
            _LOG.debug(
                f"Could not check stable row ID status for existing table '{name}': {e}"
            )
            return

        # The manifest carries the flag, so this is answerable even when the
        # table currently has no fragments -- either brand new, or every row
        # deleted. The fragment-based check could not tell those apart from a
        # table that genuinely lacks stable row IDs, and skipped validation.
        if not dataset_uses_stable_row_ids(dataset):
            raise ValueError(
                f"Cannot open table '{name}' with exist_ok=True: "
                f"table exists but does not have stable row IDs enabled.\n\n"
                f"You requested stable row IDs, but the existing table "
                f"was created without them.\n\n"
                f"Options:\n"
                f"  1. Drop and recreate the table with stable row IDs\n"
                f"  2. Remove storage_options if stable row IDs are "
                f"not required\n"
                f"  3. Use mode='overwrite' to replace the table"
            )

    def create_table(  # type: ignore
        self,
        name: str,
        data: DATA | None = None,
        schema: pa.Schema | LanceModel | None = None,
        mode: str = "create",
        exist_ok: bool = False,
        on_bad_vectors: str = "error",
        fill_value: float = 0.0,
        storage_options: dict[str, str] | None = None,
        *args,
        **kwargs,
    ) -> "Table":  # type: ignore
        """Create a Table in the lake

        Parameters
        ----------
        name: str
            The name of the table
        data: The data to initialize the table, *optional*
            User must provide at least one of `data` or `schema`.
            Acceptable types are:

            - list-of-dict
            - pandas.DataFrame
            - pyarrow.Table or pyarrow.RecordBatch
        schema: The schema of the table, *optional*
            Acceptable types are:

            - pyarrow.Schema
            - lancedb.pydantic.LanceModel
        mode: str; default "create"
            The mode to use when creating the table.
            Can be either "create" or "overwrite".
            By default, if the table already exists, an exception is raised.
            If you want to overwrite the table, use mode="overwrite".
        exist_ok: bool, default False
            If a table by the same name already exists, then raise an exception
            if exist_ok=False. If exist_ok=True, then open the existing table;
            it will not add the provided data but will validate against any
            schema that's specified.
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contain NaNs.
            One of "error", "drop", "fill".
        """
        from .table import NativeTable

        # Handle new_table_enable_stable_row_ids validation and normalization
        # Accept both strings and booleans for user convenience; lancedb
        # requires storage_options values to be strings, and parses them with
        # Rust's str::parse::<bool>(), which only accepts exactly "true"/"false".
        # So case-fold strings here: str(True) == "True" would otherwise fall
        # through both branches and reach lancedb as an unparseable value.
        if storage_options:
            enable_stable = storage_options.get("new_table_enable_stable_row_ids")
            if isinstance(enable_stable, str):
                enable_stable = enable_stable.lower()
            if enable_stable in ("true", True, 1):
                storage_options = dict(storage_options)
                storage_options["new_table_enable_stable_row_ids"] = "true"

                # Validate exist_ok: ensure existing table has stable row IDs.
                # namespace_path is still in kwargs here (popped later), so
                # thread it through for non-root tables.
                if exist_ok:
                    self._validate_existing_table_has_stable_row_ids(
                        name,
                        namespace_path=kwargs.get("namespace_path")
                        or kwargs.get("namespace"),
                    )
            elif enable_stable in ("false", False, 0):
                storage_options = dict(storage_options)
                storage_options["new_table_enable_stable_row_ids"] = "false"

        if self._host_override:
            # in OSS, exist_ok is a separate param, but in phalanx it is set as "mode"
            # workaround until https://github.com/lancedb/lancedb/issues/2900
            if exist_ok and mode == "create":
                mode = "exist_ok"

            if storage_options:
                _LOG.warning(
                    "storage_options parameter is not supported when creating "
                    "tables on remote connections, ignoring"
                )
        else:
            # these params are not supported in remote connections
            kwargs.update(
                exist_ok=exist_ok,
                on_bad_vectors=on_bad_vectors,
                storage_options=storage_options,
            )

        # Extract namespace from kwargs before passing to lancedb
        # Support both 'namespace' (legacy) and 'namespace_path' (new) parameters
        namespace = kwargs.pop("namespace", None)
        namespace_path = kwargs.pop("namespace_path", None)
        if namespace_path is not None:
            namespace = namespace_path
        # Pass namespace_path to lancedb API
        if namespace is not None:
            kwargs["namespace_path"] = namespace
        if (
            self._directory_namespace_root_uri() is not None
            and (namespace or []) == []
            and storage_options
            and storage_options.get("new_table_enable_stable_row_ids")
        ):
            direct_kwargs = dict(kwargs)
            direct_kwargs.pop("namespace_path", None)
            direct_kwargs.pop("storage_options", None)
            created = self._create_directory_namespace_root_table(
                name,
                data,
                schema,
                mode,
                *args,
                fill_value=fill_value,
                storage_options=storage_options,
                **direct_kwargs,
            )
        else:
            if storage_options:
                kwargs["storage_options"] = storage_options
            conn = self._connect
            created = conn.create_table(
                name,
                data,
                schema,
                mode,
                *args,
                fill_value=fill_value,
                **kwargs,
            )
        try:
            physical_uri = getattr(created, "uri", None) or "<unknown>"
        except Exception as exc:
            physical_uri = f"<unavailable: {exc}>"
        _LOG.info(
            "created table name=%s namespace=%s uri=%s",
            name,
            namespace,
            physical_uri,
        )
        tbl = NativeTable(
            self,
            name,
            namespace=namespace,
            # Merge so a partial caller dict keeps the connection's credentials.
            storage_options={
                **(self._storage_options or {}),
                **(storage_options or {}),
            }
            or None,
        )
        return tbl

    def create_view(
        self,
        name: str,
        query: str,
        materialized: bool = False,
    ) -> "Table":
        """Create a View from a Query.

        Parameters
        ----------
        name: str
            Name of the view.
        query: str
            SQL query to create the view.
        materialized: bool, optional
            If True, the view is materialized.
        """
        if materialized:
            # idea, rename the provided name, and use it as the basis for the
            # materialized view.
            # - how do we add the udfs to the final materialized view table?
            NotImplementedError(
                "creating materialized view via sql query is not supported yet."
            )

        # TODO add test coverage here
        self.sql(f"CREATE VIEW {name} AS ({query})")  # type: ignore[attr-defined]
        return self.open_table(name)

    def create_materialized_view(
        self,
        name: str,
        query: "GenevaQueryBuilder",
        with_no_data: bool = True,
        *,
        auto_refresh: bool = False,
    ) -> "Table":
        """
        Create a materialized view

        Parameters
        ----------
        name: str
            Name of the materialized view.
        query: GenevaQueryBuilder
            Query to create the view.
        with_no_data: bool, optional
            If True, the view is materialized, if false it is ready for refresh.
        auto_refresh: bool, optional
            If True, the server will refresh the view when source-table data
            changes past the deployment-level threshold. Honored only for
            remote (``db://``) connections.
        """
        from geneva.query import GenevaQueryBuilder

        if not isinstance(query, GenevaQueryBuilder):
            raise ValueError(
                "Materialized views only support plain queries (where, select)"
            )

        if self.use_remote_dispatch():
            return self._create_materialized_view_remote(
                name,
                query=query,
                with_no_data=with_no_data,
                auto_refresh=auto_refresh,
            )

        tbl = query.create_materialized_view(self, name)
        if not with_no_data and hasattr(tbl, "refresh_view"):
            tbl.refresh_view(name)  # type: ignore[attr-defined]

        return tbl

    def _create_materialized_view_remote(
        self,
        name: str,
        *,
        query: "GenevaQueryBuilder",
        with_no_data: bool,
        auto_refresh: bool,
    ) -> "Table":
        """Dispatch a plain-query MV create through the namespace API."""
        from lance_namespace import CreateMaterializedViewRequest

        # Mirror the local schema shape: __source_row_id + __is_set + user cols.
        view_schema = query._schema_for_query(include_metacols=True)
        view_schema = view_schema.insert(0, pa.field("__is_set", pa.bool_()))
        view_schema = view_schema.insert(0, pa.field("__source_row_id", pa.int64()))

        source_query_json = _serialize_source_query_with_identity(query)
        output_schema_b64 = _b64_str(view_schema.serialize().to_pybytes())

        ns = self.namespace_client()
        request = CreateMaterializedViewRequest(
            id=[name],
            kind="query",
            source_query=source_query_json,
            output_schema=output_schema_b64,
            with_no_data=with_no_data,
            auto_refresh=auto_refresh,
        )
        ns.create_materialized_view(request)
        return self.open_table(name)

    def create_udtf_view(
        self,
        name: str,
        source: "GenevaQueryBuilder",
        udtf: "UDTF | Chunker",
        *,
        with_no_data: bool = True,
        auto_refresh: bool = False,
    ) -> "Table":
        """Create a UDTF-backed materialized view.

        .. warning::
            This API is in **beta** and may change in future releases.

        Pass an ``@udtf``-decorated object for a batch UDTF MV (N:M rows,
        full-overwrite refresh). Pass an ``@chunker``-decorated object for
        a chunker MV (1:N row expansion, incremental refresh). The two
        kinds differ in output-schema shape and refresh semantics; this
        method picks the right one from ``type(udtf)``.

        The view is created empty (UDTF) or with placeholder rows
        (chunker); call ``view.refresh()`` to populate it.

        Parameters
        ----------
        name : str
            Name for the new view table.
        source : GenevaQueryBuilder
            Query defining the source data.
        udtf : UDTF | Chunker
            The UDTF or chunker to execute on refresh.
        with_no_data : bool, optional
            If True (default), the view is created empty / with placeholders.
            If False, the server starts an initial refresh immediately.
            Honored only for remote (``db://``) connections.
        auto_refresh : bool, optional
            If True, the server will refresh the view when source-table data
            changes past the deployment-level threshold. Honored only for
            remote (``db://``) connections.
        """
        from geneva.query import GenevaQueryBuilder
        from geneva.transformer import UDTF, Chunker

        if not isinstance(source, GenevaQueryBuilder):
            raise ValueError("source must be a GenevaQueryBuilder")
        if isinstance(udtf, Chunker):
            return self._create_udtf_view(
                name,
                source,
                udtf,
                with_no_data=with_no_data,
                auto_refresh=auto_refresh,
            )
        if not isinstance(udtf, UDTF):
            raise TypeError(
                f"udtf must be a UDTF or Chunker, got {type(udtf).__name__}"
            )

        from geneva.packager import marshal_udtf
        from geneva.query import (
            MATVIEW_META_BASE_DBURI,
            MATVIEW_META_BASE_TABLE,
            MATVIEW_META_BASE_VERSION,
            MATVIEW_META_MANIFEST,
            MATVIEW_META_MANIFEST_CHECKSUM,
            MATVIEW_META_NAMESPACE_PATH,
            MATVIEW_META_QUERY,
            MATVIEW_META_UDTF,
            MATVIEW_META_VERSION,
        )

        # Validate input_columns against source schema if specified
        # Note: _rowid/_rowaddr are Lance internal columns always available
        if udtf.input_columns:
            src_schema = source._table.schema
            missing = [
                c
                for c in udtf.input_columns
                if c not in src_schema.names and c not in _LANCE_INTERNAL_COLUMNS
            ]
            if missing:
                raise ValueError(
                    f"UDTF input_columns {missing} not found in source schema. "
                    f"Available: {src_schema.names}"
                )

        # Serialize UDTF and source query
        udtf_spec = marshal_udtf(udtf)
        source_query_json = _serialize_source_query_with_identity(source)

        if self.use_remote_dispatch():
            return self._create_udtf_view_remote(
                name,
                udtf=udtf,
                udtf_spec_json=udtf_spec.to_json(),
                source_query_json=source_query_json,
                with_no_data=with_no_data,
                auto_refresh=auto_refresh,
            )

        # Get source table info
        local_tbl = source._table._ltbl
        db_uri = _get_db_uri(source._table.uri)

        # Build metadata
        metadata = {
            MATVIEW_META_UDTF: udtf_spec.to_json(),
            MATVIEW_META_QUERY: source_query_json,
            MATVIEW_META_BASE_TABLE: local_tbl.name,
            MATVIEW_META_BASE_DBURI: db_uri,
            MATVIEW_META_BASE_VERSION: str(local_tbl.version),
            MATVIEW_META_VERSION: "udtf",
        }

        # Snapshot the UDTF's manifest into the view metadata (if any).
        if udtf.manifest is not None:
            metadata[MATVIEW_META_MANIFEST] = udtf.manifest.to_json()
            metadata[MATVIEW_META_MANIFEST_CHECKSUM] = udtf.manifest.compute_checksum()

        # Store namespace path as $-delimited string (if source is in a child namespace)
        if source._table._namespace:
            metadata[MATVIEW_META_NAMESPACE_PATH] = "$".join(source._table._namespace)

        # Create empty table with UDTF output schema + metadata.
        # Delegates to self.create_table() which is namespace-aware.
        schema_with_meta = udtf.output_schema.with_metadata(metadata)
        empty_table = schema_with_meta.empty_table()
        storage_options: dict[str, str] = {}
        if self._supports_stable_row_ids_on_create():
            storage_options["new_table_enable_stable_row_ids"] = "true"

        return self.create_table(
            name, data=empty_table, storage_options=storage_options
        )

    def _create_udtf_view(
        self,
        name: str,
        source: "GenevaQueryBuilder",
        chunker: "Chunker",
        *,
        with_no_data: bool = True,
        auto_refresh: bool = False,
    ) -> "Table":
        """Chunker-MV implementation; called by :meth:`create_udtf_view`.

        Chunker views differ from batch UDTF views: each source row
        expands to zero or more output rows (1:N) and the view carries
        ``__source_row_id`` / ``__child_index`` metacolumns plus the
        inherited source projection.
        """
        from geneva.packager import marshal_chunker
        from geneva.query import (
            MATVIEW_META_BASE_DBURI,
            MATVIEW_META_BASE_TABLE,
            MATVIEW_META_BASE_VERSION,
            MATVIEW_META_CHUNKER,
            MATVIEW_META_MANIFEST,
            MATVIEW_META_MANIFEST_CHECKSUM,
            MATVIEW_META_NAMESPACE_PATH,
            MATVIEW_META_QUERY,
            MATVIEW_META_VERSION,
            MATVIEW_VERSION_CHUNKER,
        )

        # Validate input columns against query projection (not base table)
        if chunker.input_columns:
            projected = source._schema_for_query(include_metacols=False)
            projected_names = projected.names
            missing = [c for c in chunker.input_columns if c not in projected_names]
            if missing:
                raise ValueError(
                    f"Chunker input_columns {missing} not found "
                    f"in query projection. "
                    f"Available: {projected_names}"
                )

        # Serialize scalar UDTF and source query
        spec = marshal_chunker(chunker)
        source_query_json = _serialize_source_query_with_identity(source)

        # Build the output schema: __source_row_id + __child_index
        # + inherited source columns + UDTF output columns. When
        # inherit_input_columns is False, the chunker's input columns are
        # dropped from the inherited set (see below); a chunker can still bring
        # any of them back into the view by emitting them in its output schema.
        inherited_schema = source._schema_for_query(include_metacols=False)
        excluded = {"__source_row_id", "__child_index", "__is_set"}
        # When inherit_input_columns is False, the chunker's input columns are
        # still fetched to run the chunker but are not written into each output
        # row (avoids duplicating large inputs like video/audio bytes).
        if not chunker.inherit_input_columns and chunker.input_columns:
            excluded.update(chunker.input_columns)
        view_fields = [
            pa.field("__source_row_id", pa.int64()),
            pa.field("__child_index", pa.int32()),
        ]
        # Add inherited source columns
        view_fields.extend(
            field for field in inherited_schema if field.name not in excluded
        )
        # Add UDTF output columns
        view_fields.extend(chunker.output_schema)

        view_schema = pa.schema(view_fields)

        if self.use_remote_dispatch():
            return self._create_chunker_view_remote(
                name,
                chunker=chunker,
                chunker_spec_json=spec.to_json(),
                source_query_json=source_query_json,
                view_schema=view_schema,
                with_no_data=with_no_data,
                auto_refresh=auto_refresh,
            )

        # to_lance: fresh manifest needed for stable-row-ID capability detection
        if not dataset_uses_stable_row_ids(source._table.to_lance()):
            warnings.warn(
                f"Creating chunker materialized view from table "
                f"'{source._table.name}' without stable row IDs enabled.\n\n"
                "Without stable row IDs, chunker materialized views can only "
                "refresh to the same source version they were created from. "
                "Attempting to refresh to a different source version will fail "
                "because physical row IDs may have changed.\n\n"
                "For cross-version refresh support, create the source table "
                "with stable row IDs enabled.",
                UserWarning,
                stacklevel=2,
            )

        # Get source table info
        local_tbl = source._table._ltbl
        db_uri = _get_db_uri(source._table.uri)

        # Build metadata
        metadata = {
            MATVIEW_META_CHUNKER: spec.to_json(),
            MATVIEW_META_QUERY: source_query_json,
            MATVIEW_META_BASE_TABLE: local_tbl.name,
            MATVIEW_META_BASE_DBURI: db_uri,
            MATVIEW_META_BASE_VERSION: str(local_tbl.version),
            MATVIEW_META_VERSION: MATVIEW_VERSION_CHUNKER,
        }

        # Snapshot the chunker's manifest into the view metadata (if any).
        if chunker.manifest is not None:
            metadata[MATVIEW_META_MANIFEST] = chunker.manifest.to_json()
            metadata[MATVIEW_META_MANIFEST_CHECKSUM] = (
                chunker.manifest.compute_checksum()
            )

        # Store namespace path as $-delimited string (if source is in a child namespace)
        if source._table._namespace:
            metadata[MATVIEW_META_NAMESPACE_PATH] = "$".join(source._table._namespace)

        # Create empty table with the full schema + metadata.
        schema_with_meta = view_schema.with_metadata(metadata)
        empty_table = schema_with_meta.empty_table()
        storage_options: dict[str, str] = {}
        if self._supports_stable_row_ids_on_create():
            storage_options["new_table_enable_stable_row_ids"] = "true"

        return self.create_table(
            name, data=empty_table, storage_options=storage_options
        )

    def _create_udtf_view_remote(
        self,
        name: str,
        *,
        udtf: "UDTF",
        udtf_spec_json: str,
        source_query_json: str,
        with_no_data: bool,
        auto_refresh: bool,
    ) -> "Table":
        """Dispatch a UDTF-backed MV create through the namespace API."""
        from lance_namespace import CreateMaterializedViewRequest

        manifest_json = udtf.manifest.to_json() if udtf.manifest is not None else None
        manifest_checksum = (
            udtf.manifest.compute_checksum() if udtf.manifest is not None else None
        )
        entry = _build_udtf_entry(
            "udtf",
            spec_json=udtf_spec_json,
            udtf_name=udtf.name,
            udtf_version=udtf.version,
            input_columns=udtf.input_columns,
            partition_by=udtf.partition_by,
            num_cpus=udtf.num_cpus,
            num_gpus=udtf.num_gpus,
            memory=udtf.memory,
            manifest_json=manifest_json,
            manifest_checksum=manifest_checksum,
        )

        output_schema_b64 = _b64_str(udtf.output_schema.serialize().to_pybytes())

        ns = self.namespace_client()
        request = CreateMaterializedViewRequest(
            id=[name],
            kind="udtf",
            source_query=source_query_json,
            output_schema=output_schema_b64,
            udtf_spec=entry,
            with_no_data=with_no_data,
            auto_refresh=auto_refresh,
        )
        ns.create_materialized_view(request)
        return self.open_table(name)

    def _create_chunker_view_remote(
        self,
        name: str,
        *,
        chunker: "Chunker",
        chunker_spec_json: str,
        source_query_json: str,
        view_schema: pa.Schema,
        with_no_data: bool,
        auto_refresh: bool,
    ) -> "Table":
        """Dispatch a chunker-backed MV create through the namespace API."""
        from lance_namespace import CreateMaterializedViewRequest

        manifest_json = (
            chunker.manifest.to_json() if chunker.manifest is not None else None
        )
        manifest_checksum = (
            chunker.manifest.compute_checksum()
            if chunker.manifest is not None
            else None
        )
        entry = _build_udtf_entry(
            "chunker",
            spec_json=chunker_spec_json,
            udtf_name=chunker.name,
            udtf_version=chunker.version,
            input_columns=chunker.input_columns,
            num_cpus=chunker.num_cpus,
            num_gpus=chunker.num_gpus,
            memory=chunker.memory,
            batch=chunker.batch,
            manifest_json=manifest_json,
            manifest_checksum=manifest_checksum,
        )

        output_schema_b64 = _b64_str(view_schema.serialize().to_pybytes())

        ns = self.namespace_client()
        request = CreateMaterializedViewRequest(
            id=[name],
            kind="chunker",
            source_query=source_query_json,
            output_schema=output_schema_b64,
            udtf_spec=entry,
            with_no_data=with_no_data,
            auto_refresh=auto_refresh,
        )
        ns.create_materialized_view(request)
        return self.open_table(name)

    def drop_view(self, name: str) -> pa.Table:
        """Drop a view."""
        return self.sql(f"DROP VIEW {name}")  # type: ignore[attr-defined]

    def drop_table(self, name: str, *args, **kwargs) -> None:
        """Drop a table."""
        self._connect.drop_table(name, *args, **kwargs)

    def define_cluster(self, name: str, cluster: "GenevaCluster") -> None:  # noqa: F821
        """
        Define a persistent Geneva cluster. This will upsert the cluster definition by
        name. The cluster can then be provisioned using `context(cluster=name)`.

        Parameters
        ----------
        name: str
            Name of the cluster. This will be used as the key when upserting and
            provisioning the cluster. The cluster name must comply with RFC 12123.
        cluster: GenevaCluster
            The cluster definition to store.
        """
        from geneva.cluster.mgr import ClusterConfigManager

        if self._cluster_manager is None:
            self._cluster_manager = ClusterConfigManager(self)

        cluster.name = name
        self._cluster_manager.upsert(cluster)

    def list_clusters(self) -> list["GenevaCluster"]:  # noqa: F821
        """
        List the cluster definitions. These can be defined using `define_cluster()`.

        Returns
        -------
        list[GenevaCluster]
            List of Geneva cluster definitions
        """
        from geneva.cluster.mgr import ClusterConfigManager

        if self._cluster_manager is None:
            self._cluster_manager = ClusterConfigManager(self)
        return self._cluster_manager.list()

    def delete_cluster(self, name: str) -> None:  # noqa: F821
        """
        Delete a Geneva cluster definition.

        Parameters
        ----------
        name: str
            Name of the cluster to delete.
        """
        from geneva.cluster.mgr import ClusterConfigManager

        if self._cluster_manager is None:
            self._cluster_manager = ClusterConfigManager(self)

        self._cluster_manager.delete(name)

    def define_manifest(
        self,
        name: str,
        manifest: "GenevaManifest",  # noqa: F821
        uploader: Uploader | None = None,
    ) -> None:
        """
        Define a persistent Geneva Manifest that represents the files and dependencies
        used in the execution environment. This will upsert the manifest definition by
        name and upload the required artifacts. The manifest can then be used with
        `context(manifest=name)`.

        Parameters
        ----------
        name: str
            Name of the manifest. This will be used as the key when upserting and
            loading the manifest.
        manifest: GenevaManifest
            The manifest definition to use.
        uploader: Uploader, optional
            An optional, custom Uploader to use. If not provided, the uploader will be
            auto-detected based on the
            environment configuration.
        """
        warnings.warn(
            "Connection.define_manifest() is deprecated. "
            "Use @udf(manifest=...) on the UDF decorator instead — see "
            "GenevaManifest.create_pip() / .create_conda() (or "
            "Connection.capture_local_environment()).",
            DeprecationWarning,
            stacklevel=2,
        )

        from geneva.manifest.mgr import ManifestConfigManager

        if self._manifest_manager is None:
            self._manifest_manager = ManifestConfigManager(self)

        # Ensure the manifest table exists before creating Uploader
        # This guarantees the table location can be queried
        _ = self._manifest_manager.get_table()

        # If no uploader is provided, create one with manifest table context
        if uploader is None:
            uploader = self._default_manifest_uploader()

        with upload_local_env(
            # todo: implement excludes
            uploader=uploader,
            zip_output_dir=manifest.local_zip_output_dir,
            delete_local_zips=manifest.delete_local_zips,
            skip_site_packages=manifest.skip_site_packages,
        ) as zips:
            m = copy.deepcopy(manifest)
            m.name = name
            m.zips = zips
            m.checksum = manifest.compute_checksum()
            self._manifest_manager.upsert(m)

    def _default_manifest_uploader(self) -> Uploader:
        from geneva.manifest.mgr import MANIFEST_TABLE_NAME

        kwargs: dict[str, Any] = {}
        if self._storage_options is not None:
            kwargs["storage_options"] = self._storage_options
        return Uploader(
            namespace_config=self._ns_config,
            table_id=self.system_namespace + [MANIFEST_TABLE_NAME],
            **kwargs,
        )

    def list_manifests(self) -> list["GenevaManifest"]:  # noqa: F821
        """
        List the manifest definitions. These can be defined using `define_manifest()`.

        Returns
        -------
        list[GenevaManifest]
            List of Geneva manifest definitions
        """
        from geneva.manifest.mgr import ManifestConfigManager

        if self._manifest_manager is None:
            self._manifest_manager = ManifestConfigManager(self)
        return self._manifest_manager.list()

    def delete_manifest(self, name: str) -> None:  # noqa: F821
        """
        Delete a Geneva manifest definition.

        Parameters
        ----------
        name: str
            Name of the manifest to delete.
        """
        from geneva.manifest.mgr import ManifestConfigManager

        if self._manifest_manager is None:
            self._manifest_manager = ManifestConfigManager(self)

        self._manifest_manager.delete(name)

    def capture_local_environment(
        self,
        name: str | None = None,
        *,
        skip_site_packages: bool = False,
    ) -> "GenevaManifest":  # noqa: F821
        """Capture and upload the caller's local environment.

        Zips the workspace (and, by default, site-packages)
        and uploads the resulting archives through this connection's
        namespace-vended Uploader before returning. The returned
        :class:`~geneva.manifest.GenevaManifest` carries the uploaded
        zip URIs and is ready to be passed to ``@udf(manifest=...)``.

        Note: the query node deployment must be configured for credential-vending
        via `vend_input_storage_options` configuration

        Typical usage::

            db = geneva.connect(...)
            manifest = db.capture_local_environment(skip_site_packages=True)

            @udf(manifest=manifest)
            def embed(text: str) -> list[float]: ...

        Use :meth:`GenevaManifest.create_pip` for declarative manifests
        when you do not want any local-environment upload to happen.

        Parameters
        ----------
        name: str, optional
            Optional manifest name. If omitted, an auto-generated name
            is assigned.
        skip_site_packages: bool, default False
            If True, capture only the workspace source and rely on the
            worker image's pre-installed dependencies.

        Returns
        -------
        GenevaManifest
            A manifest with ``zips`` populated. No further resolution
            step is required.

        Raises
        ------
        RuntimeError
            If this connection cannot vend an Uploader (e.g. a ``db://``
            connection without ``namespace_client_impl`` configured).
        """
        from geneva.manifest.mgr import build_captured_manifest

        return build_captured_manifest(
            self, name, skip_site_packages=skip_site_packages
        )

    @staticmethod
    def local_ray_context() -> contextlib.AbstractContextManager[None]:
        """Context manager for a local Ray instance.
        This will provision a local Ray instance and return a context manager.
        This is useful for development or small jobs.
        """
        from geneva.runners.ray._mgr import ray_cluster

        return ray_cluster(local=True, log_to_driver=True, logging_level=logging.INFO)

    def context(
        self,
        cluster: str,
        manifest: str | None = None,
        on_exit=None,
        wait_timeout: float | None = None,
        log_to_driver: bool = True,
        logging_level=logging.INFO,
    ) -> contextlib.AbstractContextManager[None]:
        """Context manager for a Geneva Execution Environment.
            This will provision a cluster based on the cluster
            definition and the manifest provided.
            By default, the context manager will delete the cluster on exit.
            This can be configured with the on_exit parameter.
        Parameters
        ----------
        cluster: str
            Name of the persisted cluster definition to use. Required.
            This will raise an exception if the cluster definition was not
            defined via `define_cluster()`.
        manifest: str, optional
            Optional name of the persisted manifest to use. This will
            raise an exception if the manifest definition was not
            defined via `define_manifest()`. If manifest is not provided,
            the local environment will be uploaded.
        on_exit: ExitMode, optional, default ExitMode.DELETE
            Exit mode for the cluster. By default, the cluster waits for all
            running jobs to complete before deleting.
            To retain the cluster when any job fails or the context body
            raises an exception, use `ExitMode.RETAIN_ON_FAILURE`.
            To always retain the cluster, use `ExitMode.RETAIN`.
        wait_timeout: float, optional, default None
            Internal/experimental. Maximum seconds to wait for tracked jobs
            during context exit. Only applies with DELETE or
            RETAIN_ON_FAILURE. None means wait indefinitely. For
            RETAIN_ON_FAILURE, a timeout is treated as a failure and the
            cluster is retained.
        log_to_driver: bool, optional, default True
            Whether to send Ray worker logs to the driver. Defaults to True for
            better visibility in tests and debugging.
        logging_level: int, optional, default logging.INFO
            The logging level for Ray workers. Use logging.DEBUG for detailed logs.
        """
        warnings.warn(
            "Connection.context() is deprecated. Pass cluster= and rely on "
            "the deployment-default manifest, or attach an explicit manifest "
            "via @udf(manifest=...). In remote (db://) mode, db.context() is "
            "scheduled to become internal-only.",
            DeprecationWarning,
            stacklevel=2,
        )

        from geneva.cluster.mgr import ClusterConfigManager
        from geneva.manifest.mgr import ManifestConfigManager
        from geneva.runners.ray._mgr import ray_cluster
        from geneva.runners.ray.raycluster import ExitMode

        if self._cluster_manager is None:
            self._cluster_manager = ClusterConfigManager(self)
        if self._manifest_manager is None:
            self._manifest_manager = ManifestConfigManager(self)

        if cluster is None:
            raise ValueError(
                "cluster name is required. Use conn.context(cluster=...) or "
                "conn.local_ray_context() for a local Ray instance."
            )

        cluster_def = self._cluster_manager.load(cluster)
        if cluster_def is None:
            raise Exception(
                f"cluster definition '{cluster}' not found. "
                f"Create a new cluster with define_cluster()"
            )

        if cluster_def.cluster_type == GenevaClusterType.LOCAL_RAY:
            if manifest is not None:
                raise ValueError(
                    "Manifests are not supported with LOCAL_RAY cluster type"
                )
            return ray_cluster(
                local=True, log_to_driver=log_to_driver, logging_level=logging_level
            )

        ray_env = {
            "RAY_BACKEND_LOG_LEVEL": "info",
            "RAY_LOG_TO_DRIVER": "1",
            "RAY_ENABLE_RECORD_ACTOR_TASK_LOGGING": "0",
            "RAY_RUNTIME_ENV_LOG_TO_DRIVER_ENABLED": "true",
        }
        if self._storage_options:
            account_name = self._storage_options.get(
                "account_name"
            ) or self._storage_options.get("azure_storage_account_name")
            if account_name:
                ray_env["AZURE_STORAGE_ACCOUNT_NAME"] = account_name

        # load the manifest if provided
        manifest_def = None
        if manifest is not None:
            manifest_def = self._manifest_manager.load(manifest)
            if manifest_def is None:
                raise Exception(
                    f"manifest definition '{manifest}' not found. "
                    f"Create a new manifest with define_manifest()"
                )

        uploader = None
        if (
            manifest_def is None
            and cluster_def.cluster_type != GenevaClusterType.LOCAL_RAY
        ):
            self._manifest_manager.get_table()
            uploader = self._default_manifest_uploader()
        uploader_kwargs: dict[str, Any] = (
            {"uploader": uploader} if uploader is not None else {}
        )
        zip_namespace_kwargs: dict[str, Any] = {}
        if (
            manifest_def is not None
            and cluster_def.cluster_type != GenevaClusterType.LOCAL_RAY
            and self._ns_config.namespace_client_impl is not None
        ):
            from geneva.manifest.mgr import MANIFEST_TABLE_NAME

            zip_namespace_kwargs["zip_namespace"] = {
                "impl": self._ns_config.namespace_client_impl,
                "properties": self._ns_config.namespace_client_properties or {},
                "table_id": self.system_namespace + [MANIFEST_TABLE_NAME],
            }

        if cluster_def.cluster_type == GenevaClusterType.EXTERNAL_RAY:
            return ray_cluster(
                addr=cluster_def.ray_address,
                use_portforwarding=False,
                manifest=manifest_def,
                extra_env=ray_env,
                log_to_driver=log_to_driver,
                logging_level=logging_level,
                ray_init_kwargs=cluster_def.ray_init_kwargs,
                **uploader_kwargs,
                **zip_namespace_kwargs,
            )

        use_portforwarding = cluster_def.as_dict()["kuberay"].get(
            "use_portforwarding", True
        )
        rc = cluster_def.to_ray_cluster()
        rc.on_exit = on_exit or ExitMode.DELETE
        if wait_timeout is not None:
            rc.wait_timeout = wait_timeout
        if manifest_def:
            # image explicitly provided in manifest takes precedence over cluster
            if img := manifest_def.head_image:
                _LOG.debug(f"overriding cluster head image from manifest: {img}")
                rc.head_group.image = img
            if img := manifest_def.worker_image:
                _LOG.debug(f"overriding cluster worker image from manifest: {img}")
                for wg in rc.worker_groups:
                    wg.image = img

        return ray_cluster(
            use_portforwarding=use_portforwarding,
            ray_cluster=rc,
            manifest=manifest_def,
            extra_env=ray_env,
            log_to_driver=log_to_driver,
            logging_level=logging_level,
            **uploader_kwargs,
            **zip_namespace_kwargs,
        )

    def is_remote_uri(self) -> bool:
        return self.uri.startswith("db://")

    def is_remote(self) -> bool:
        return self.is_remote_uri()

    def use_remote_dispatch(self) -> bool:
        return self.is_remote_uri() and not self._executor_mode

    def get_job(self, job_id: str) -> "JobRecord":
        """Get a job record by ID.

        Reads from the ``_geneva_jobs`` system table via ``JobStateManager``.
        Works for both native and remote connections.
        """
        results = self._history.get(job_id)
        if not results:
            raise ValueError(f"Job {job_id} not found")
        return results[0]

    def list_jobs(
        self,
        table_name: str | None = None,
        status: str | None = None,
    ) -> "list[JobRecord]":
        """List jobs, optionally filtered by table and/or status.

        Reads from the ``_geneva_jobs`` system table via ``JobStateManager``.
        Works for both native and remote connections.
        """
        return self._history.list_jobs(table_name=table_name, status=status)


# Backward-compatible aliases (previously separate subclasses).
# Keep ``isinstance(conn, DBConnection)`` true for callers that type-check
# against lancedb, without inheriting ``EnforceOverrides`` and the breakage it
# brings. Virtual registration asserts nothing about our method signatures.
#
# ``register`` exists only where ``DBConnection`` is ABC-based. lancedb swaps
# ``EnforceOverrides`` for a no-op stub on Python 3.12+ (see ``lancedb/db.py``),
# leaving a plain class with no ABC machinery -- and, for the same reason, no
# override enforcement, which is why the breakage this change fixes is
# 3.10/3.11-only. There ``isinstance`` was never satisfiable except by real
# inheritance, so there is nothing to preserve and nothing to register.
_register = getattr(DBConnection, "register", None)
if _register is not None:
    _register(Connection)

NativeConnection = Connection
RemoteConnection = Connection


def sql(self, query: str) -> pa.Table:
    """Execute a raw SQL query.

    It uses the Flight SQL engine to execute the query.

    Parameters
    ----------
    query: str
        SQL query to execute

    Returns
    -------
    pyarrow.Table
        Result of the query in a `pyarrow.Table`

    """
    info = self.flight_client.execute(query)
    return self.flight_client.do_get(info.endpoints[0].ticket).read_all()


@attrs.define
class _GenavaConnectionConfig(ConfigBase):
    region: str = attrs.field(default="us-east-1")
    api_key: str | None = attrs.field(default=None)
    host_override: str | None = attrs.field(default=None)
    checkpoint: str | None = attrs.field(default=None)
    system_namespace: list[str] = attrs.field(factory=lambda: [SYSTEM_NAMESPACE])

    @classmethod
    @override
    def name(cls) -> str:
        return "connection"


def _ensure_system_namespace_exists(conn: Connection) -> None:
    """Ensure system_namespace exists, creating it if necessary.

    This is called once at connection time for namespace connections to ensure
    the system namespace is ready before any system tables are created.
    For nested namespaces, creates parent namespaces first.

    Args:
        conn: The Geneva connection

    Raises:
        RuntimeError: If the namespace doesn't exist and cannot be created
    """
    from lance_namespace import CreateNamespaceRequest, DescribeNamespaceRequest

    if not conn.system_namespace or conn._system_namespace_ensured:
        return

    # Remote db:// connections (including those converted to REST namespace)
    # rely on the server to handle namespace creation during table operations.
    # Explicit namespace creation is not reliable across phalanx/server versions
    # and can fail before any useful work begins.
    if conn.is_remote():
        _LOG.info(
            "Deferring system namespace creation for remote connection: %s",
            conn.system_namespace,
        )
        conn._system_namespace_ensured = True
        return

    if conn.namespace_client_impl == "dir":
        _LOG.info(
            "Deferring system namespace creation for directory namespace: %s",
            conn.system_namespace,
        )
        conn._system_namespace_ensured = True
        return

    try:
        # Check if namespace exists
        conn.namespace_client().describe_namespace(
            DescribeNamespaceRequest(id=conn.system_namespace)
        )
        _LOG.info(f"System namespace {conn.system_namespace} exists")
        conn._system_namespace_ensured = True
    except Exception as e:
        # Namespace doesn't exist, try to create it
        if "not found" in str(e).lower():
            try:
                # For nested namespaces, create parents first
                for i in range(1, len(conn.system_namespace) + 1):
                    parent_ns = conn.system_namespace[:i]
                    try:
                        conn.namespace_client().describe_namespace(
                            DescribeNamespaceRequest(id=parent_ns)
                        )
                        _LOG.debug(f"Namespace {parent_ns} already exists")
                    except Exception:
                        _LOG.info(f"Creating namespace {parent_ns}...")
                        conn.namespace_client().create_namespace(
                            CreateNamespaceRequest(id=parent_ns)
                        )
                        _LOG.info(f"Created namespace {parent_ns}")

                _LOG.info(f"System namespace {conn.system_namespace} is ready")
                conn._system_namespace_ensured = True
            except Exception as create_error:
                raise RuntimeError(
                    f"Cannot create system namespace {conn.system_namespace}: "
                    f"{create_error}"
                ) from create_error
        else:
            # Some other error, re-raise
            raise


def connect(
    uri: str | Path | None = None,
    *,
    region: str | None = None,
    api_key: Credential | str | None = None,
    host_override: str | None = None,
    _worker_host_override: str | None = None,
    storage_options: dict[str, str] | None = None,
    checkpoint: str | CheckpointStore | None = None,
    system_namespace: list[str] | None = None,
    namespace_client_impl: str | None = None,
    namespace_client_properties: dict[str, str] | None = None,
    namespace_client_pushdown_operations: list[str] | None = None,
    executor_mode: bool = False,
    **kwargs,
) -> Connection:
    """Create a Geneva Connection to an existing database.

    Examples
    --------
        import geneva
        # Connect to a database in object storage
        conn = geneva.connect("s3://my-storage-bucket/my-database")
        # Connect using directory namespace
        conn = geneva.connect(
            namespace_client_impl="dir", namespace_client_properties={"root": "/path"}
        )
        # Connect using REST namespace
        conn = geneva.connect(
            namespace_client_impl="rest", namespace_client_properties={"uri": f"http://127.0.0.1:1234"}
        )
        conn = geneva.connect(
            uri="db://my_database",
            api_key="my-api-key",
            host_override="https://phalanx.example.com",
        )
        tbl = conn.open_table("youtube_dataset")

    Parameters
    ----------
    uri: geneva URI, or Path, optional
        LanceDB Database URI, or a S3/GCS path.
        If not provided and namespace_client_impl is set, defaults to "namespace://".
    region: str | None
        LanceDB cloud region. Set to `None` on LanceDB Enterprise
    api_key: str | None
        Optional API key for enterprise endpoint
    host_override: str | None
        Optional host URI for enterprise endpoint (used by notebook/client)
    _worker_host_override: str | None
        Internal/experimental. Optional internal host URI for workers. When
        specified, workers will connect to this endpoint instead of host_override.
        This is useful when workers run inside a cluster that has direct access
        to an internal endpoint, while the notebook/client connects via an
        external endpoint.
    system_namespace: list[str] | None
        Namespace for system tables (manifests, clusters, jobs, errors).
        Defaults to config value if not provided.
    namespace_client_impl: str | None
        The namespace implementation to use (e.g., "dir", "rest").
        If provided, connects using namespace instead of local database.
    namespace_client_properties: dict[str, str] | None
        Configuration properties for the namespace implementation.
    namespace_client_pushdown_operations: list[str] | None
        List of operations to push down to the namespace server.
        Supported: "QueryTable", "CreateTable".
        For enterprise connections (db:// + host_override), defaults to both.
    Returns
    -------
    Connection - A LanceDB connection
    """
    if "checkpoint" in kwargs:
        if checkpoint is not None:
            raise TypeError("geneva.connect() got multiple values for checkpoint")
        checkpoint = kwargs.pop("checkpoint")
    removed_upload_kwargs = [
        name for name in ("upload_dir", "initialize_upload_dir") if name in kwargs
    ]
    if removed_upload_kwargs:
        removed = ", ".join(removed_upload_kwargs)
        raise TypeError(
            f"geneva.connect() no longer accepts {removed}. Manifest artifacts "
            "are uploaded under the geneva_manifests table's "
            "_geneva_uploads directory."
        )

    # Whether the caller explicitly passed region=, captured before _pre_connect
    # backfills it from config / the "us-east-1" default.
    explicit_region = region

    (
        api_key,
        host_override,
        region,
        uri,
        system_namespace,
        namespace_client_impl,
        namespace_client_properties,
        namespace_client_pushdown_operations,
    ) = _pre_connect(
        api_key,
        host_override,
        _worker_host_override,
        region,
        uri,
        namespace_client_impl,
        namespace_client_properties,
        system_namespace,
        namespace_client_pushdown_operations,
    )

    if host_override:
        _LOG.info(f"Using host_override: {host_override}")

    # If region set, override AWS_REGION / AWS_DEFAULT_REGION from the environment
    if explicit_region is not None:
        storage_options = dict(storage_options or {})
        storage_options.setdefault("aws_region", explicit_region)

    if storage_options and namespace_client_impl == "dir":
        namespace_props = dict(namespace_client_properties or {})
        namespace_props.update(_directory_namespace_storage_properties(storage_options))
        namespace_client_properties = _RedactedNamespaceProperties(namespace_props)

    checkpoint_store: CheckpointStore | None
    if isinstance(checkpoint, str):
        checkpoint_store = CheckpointStore.from_uri(checkpoint)
    else:
        checkpoint_store = checkpoint

    conn_cls: type[Connection]
    if isinstance(uri, str) and uri.startswith("db://"):
        conn_cls = RemoteConnection
    else:
        conn_cls = NativeConnection

    conn = conn_cls(
        str(uri),
        region=region,
        api_key=api_key,
        host_override=host_override,
        storage_options=storage_options,
        checkpoint_store=checkpoint_store,
        namespace_client_impl=namespace_client_impl,
        namespace_client_properties=namespace_client_properties,
        namespace_client_pushdown_operations=namespace_client_pushdown_operations,
        system_namespace=system_namespace,
        executor_mode=executor_mode,
        **kwargs,
    )

    # Validate and create system namespace for namespace_client_impl connections.
    # For remote db:// connections, defer creation until system tables are used.
    if namespace_client_impl is not None:
        _ensure_system_namespace_exists(conn)

    return conn


def resolve_table_physical_uri(
    table_id: list[str],
    *,
    db_uri: str | None,
    api_key: Credential | str | None = None,
    host_override: str | None = None,
    namespace_client_impl: str | None = None,
    namespace_client_properties: dict[str, str] | None = None,
    use_worker_props: bool = False,
) -> str:
    """Resolve a table reference to the backing physical storage URI."""
    table_name = table_id[-1]
    namespace = table_id[:-1]

    if namespace_client_impl is not None and namespace_client_properties is not None:
        from lance_namespace import DescribeTableRequest

        ns_config = NamespaceConfig(
            namespace_client_impl=namespace_client_impl,
            namespace_client_properties=namespace_client_properties,
        )
        ns_client = ns_config.connect_namespace_client(
            use_worker_props=use_worker_props
        )
        assert ns_client is not None
        response = ns_client.describe_table(DescribeTableRequest(id=table_id))
        if response.location is None:
            raise ValueError(f"Table {table_id} does not have a physical location")
        # TODO(phalanx): Strip trailing '?' that Phalanx may return
        return response.location.rstrip("?")

    if db_uri is not None and db_uri.startswith("db://"):
        remote_db = connect(
            db_uri,
            api_key=api_key,
            host_override=host_override,
            system_namespace=[SYSTEM_NAMESPACE],
            read_consistency_interval=timedelta(0),
        )
        try:
            table = remote_db.open_table(table_name, namespace_path=namespace)
            return table.uri  # pyright: ignore[reportAttributeAccessIssue]
        finally:
            remote_db.close()

    assert db_uri is not None, "db_uri must be set"
    return str(URL(str(db_uri)) / f"{table_name}.lance")


def _pre_connect(
    api_key: Credential | str | None,
    host_override: str | None,
    _worker_host_override: str | None,
    region: str | None,
    uri: str | Path | None,
    namespace_client_impl: str | None,
    namespace_client_properties: dict[str, str] | None,
    system_namespace: list[str] | None,
    namespace_client_pushdown_operations: list[str] | None,
) -> tuple[
    Credential | None,
    str | None,
    str,
    str | Path,
    list[str],
    str | None,
    dict[str, str] | None,
    list[str] | None,
]:
    # load values from config if not provided via arguments
    config = _GenavaConnectionConfig.get()
    region = region or config.region or "us-east-1"
    api_key = api_key or config.api_key
    host_override = host_override or config.host_override
    # Track if system_namespace was explicitly provided (not from config default)
    system_namespace_explicit = system_namespace is not None
    if system_namespace is None:
        system_namespace = config.system_namespace
    uri_was_provided = uri is not None
    # handle local relative paths
    is_local = isinstance(uri, Path) or (
        uri is not None and get_uri_scheme(uri) == "file"
    )
    if is_local and uri:
        if isinstance(uri, str):
            uri = Path(uri)
        uri = uri.expanduser().absolute()
        uri.mkdir(parents=True, exist_ok=True)

    # Default URI for namespace connections
    if uri is None:
        uri = "namespace://"

    # Convert enterprise connection (db:// + host_override) to REST namespace
    if (
        namespace_client_impl is None
        and isinstance(uri, str)
        and uri.startswith("db://")
        and host_override
    ):
        # Extract database name from db://database_name
        database_name = uri[5:].rstrip("/")
        if not database_name:
            raise ValueError(
                "Enterprise connection requires database name in URI (e.g., db://my_database)"
            )

        # Get api_key as string for REST namespace header
        # Credential is a str subclass where __str__ returns "********"
        # Use slicing to get the raw string value
        api_key_str = api_key if isinstance(api_key, str) else None
        if api_key_str is None and isinstance(api_key, Credential):
            api_key_str = api_key[:]  # Slice to get the raw string value

        namespace_client_impl = "rest"
        namespace_client_properties = {"uri": host_override}
        if api_key_str:
            namespace_client_properties["header.x-api-key"] = api_key_str
        namespace_client_properties["header.x-lancedb-database"] = database_name

        # Store _worker_host_override for workers to use instead of host_override
        if _worker_host_override:
            namespace_client_properties[WORKER_URI_KEY] = _worker_host_override
        namespace_client_properties = _RedactedNamespaceProperties(
            namespace_client_properties
        )

        # Enable pushdown operations for enterprise by default
        if namespace_client_pushdown_operations is None:
            namespace_client_pushdown_operations = ["QueryTable", "CreateTable"]

        # Remote connections place system tables under the __system namespace
        # (unless explicitly overridden by user). phalanx's FsCatalog routes
        # this to {db_uri}/__system/{table_name}.lance via
        # namespace_table_location(), matching where geneva_driver resolves
        # system tables via its direct-URI connection.
        if not system_namespace_explicit:
            system_namespace = [SYSTEM_NAMESPACE]

        _LOG.info(
            f"Enterprise connection converted to REST namespace: "
            f"database={database_name}, host={host_override}"
            + (
                f", _worker_host_override={_worker_host_override}"
                if _worker_host_override
                else ""
            )
        )

    if (
        namespace_client_impl is None
        and uri_was_provided
        and not (isinstance(uri, str) and uri.startswith("db://"))
    ):
        namespace_client_impl = "dir"
        namespace_client_properties = {
            "root": str(uri),
            "manifest_enabled": "true",
        }
        if not system_namespace_explicit:
            system_namespace = [SYSTEM_NAMESPACE]
        _LOG.info("Direct storage connection converted to Directory Namespace")

    # Convert api_key to Credential after extracting string for REST namespace
    api_key = Credential(api_key) if isinstance(api_key, str) else api_key

    return (
        api_key,
        host_override,
        region,
        uri,
        system_namespace,
        namespace_client_impl,
        namespace_client_properties,
        namespace_client_pushdown_operations,
    )


def _serialize_source_query_with_identity(
    query: "GenevaQueryBuilder",
) -> str:
    """Serialize the source query JSON with the source-table identity
    embedded as ``source_table`` / ``source_db_uri`` on the
    ``GenevaQuery``.

    ``resolve_mv_source_identity`` reads these back at refresh time as
    the single source of truth for "which table does this MV refresh
    from" (works uniformly for native and namespace-backed MVs).
    """
    qo = query.to_query_object()
    src_tbl = getattr(query, "_table", None)
    if src_tbl is not None:
        qo.source_table = src_tbl.name
        with contextlib.suppress(Exception):
            # Prefer the logical db URI (db://<db>) so refresh resolves the source
            # via the namespace; the physical URI forces a dir listing that fails
            # under scoped credential vending. Fall back for native connections.
            src_conn = getattr(src_tbl, "_conn", None)
            conn_uri = getattr(src_conn, "uri", None) if src_conn is not None else None
            qo.source_db_uri = conn_uri or _get_db_uri(src_tbl.uri)
    return qo.model_dump_json()


def _get_db_uri(tbl_uri: str) -> str:
    """Get the database URI from a table URI.

    For example,
        s3://bucket/path/to/table.lance -> s3://bucket/path/to
        db://path/to/table.lance -> db://path/to
        /tmp/foo/table.lance -> /tmp/foo
        s3+ddb://bucket/path/table.lance?ddbTableName=x -> s3+ddb://bucket/path?ddbTableName=x
    """
    parsed = urlparse(tbl_uri)
    path_parts = parsed.path.rsplit("/", 1)
    db_path = path_parts[0] if len(path_parts) > 1 else ""

    # Handle local paths (no scheme)
    if not parsed.scheme:
        return db_path

    base = f"{parsed.scheme}://{parsed.netloc}{db_path}"
    if parsed.query:
        base = f"{base}?{parsed.query}"
    return base
