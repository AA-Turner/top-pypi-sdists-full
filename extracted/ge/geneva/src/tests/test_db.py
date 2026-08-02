# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
from pathlib import Path
from unittest.mock import MagicMock, patch

import lancedb
import pyarrow as pa
import pytest
from lance_namespace import DescribeTableRequest
from lance_namespace.errors import TableNotFoundError

from geneva import connect
from geneva.db import (
    WORKER_URI_KEY,
    Connection,
    NamespaceConfig,
    _as_namespace_client_properties,
    _ensure_system_namespace_exists,
    has_stable_row_ids,
    resolve_table_physical_uri,
)
from geneva.debug.error_store import GENEVA_ERRORS_TABLE_NAME, ErrorStore
from geneva.jobs.jobs import GENEVA_JOBS_TABLE_NAME
from geneva.manifest.mgr import MANIFEST_TABLE_NAME, ManifestConfigManager
from geneva.table import TableReference


def test_connect(tmp_path: Path) -> None:
    db = connect(tmp_path)
    assert db.namespace_client_impl == "dir"
    assert db.namespace_client_properties == {
        "root": str(tmp_path),
        "manifest_enabled": "true",
    }
    assert db.system_namespace == ["__system"]

    # Use lancedb to verify the results are the same
    ldb = lancedb.connect(tmp_path)

    # Create a Table with integer columns
    tbl = pa.Table.from_pydict({"a": [1, 2, 3], "b": [4, 5, 6]})
    db.create_table("table1", tbl)
    ldb_tbls = db.table_names()
    assert "table1" in ldb_tbls
    db.open_table("table1")

    db_tbls = db.table_names()
    assert db_tbls == ldb_tbls

    # Use lancedb to read the data back
    ldb_tbl = ldb.open_table("table1")
    assert ldb_tbl.to_arrow() == tbl
    db.drop_table("table1")


def test_local_directory_namespace_preserves_stable_row_ids(tmp_path: Path) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "stable_table",
        pa.table({"value": [1, 2, 3]}),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    assert has_stable_row_ids(list(table.to_lance().get_fragments()))
    response = db.namespace_client().describe_table(
        DescribeTableRequest(id=["stable_table"])
    )
    assert response.location is not None


def test_local_directory_namespace_checkpoint_store_uses_ckp_subdir(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    table = db.create_table("checkpointed", pa.table({"value": [1]}))
    store = table.get_reference().open_checkpoint_store()
    assert list(store.list_keys()) == []
    batch = pa.record_batch([pa.array([42])], names=["value"])

    store["frag"] = batch

    assert "frag" in store
    assert list(store.list_keys()) == ["frag"]
    assert store["frag"].to_pydict() == {"value": [42]}
    assert (tmp_path / "checkpointed.lance" / "_ckp" / "frag.lance").exists()
    assert not (tmp_path / "checkpointed.lance" / "frag.lance").exists()

    store.delete("frag")
    assert "frag" not in store


def test_connect_non_existent(tmp_path: Path) -> None:
    db = connect(tmp_path)
    with pytest.raises(TableNotFoundError, match="Table not found"):
        db.open_table("non_existent")


def test_error_store_from_system_table_ref_stays_in_single_system_db(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    db.create_table("table1", pa.Table.from_pydict({"a": [1]}))

    system_ref = (
        db.open_table("table1")
        .get_reference()
        .as_system_table(GENEVA_ERRORS_TABLE_NAME)
    )
    reopened = system_ref.open_db()
    store = ErrorStore(reopened)
    location = (
        store.db.namespace_client()
        .describe_table(DescribeTableRequest(id=["__system", GENEVA_ERRORS_TABLE_NAME]))
        .location
    )

    assert store.db.system_namespace == ["__system"]
    assert location is not None
    assert location.endswith("__system$geneva_errors")
    assert "/__system/__system/" not in location


def test_error_store_nests_under_system_db_named_system(tmp_path: Path) -> None:
    db_path = tmp_path / "__system"
    db = connect(db_path)
    db.create_table("table1", pa.Table.from_pydict({"a": [1]}))

    system_ref = (
        db.open_table("table1")
        .get_reference()
        .as_system_table(GENEVA_ERRORS_TABLE_NAME)
    )
    reopened = system_ref.open_db()
    store = ErrorStore(reopened)
    location = (
        store.db.namespace_client()
        .describe_table(DescribeTableRequest(id=["__system", GENEVA_ERRORS_TABLE_NAME]))
        .location
    )

    assert store.db.system_namespace == ["__system"]
    assert location is not None
    assert location.endswith("__system$geneva_errors")


class TestConnectRemote:
    """Tests for connect() with remote db:// URI (Phalanx server)."""

    def test_connect_remote_uri_uses_host_override(self) -> None:
        """Test that db:// URI with host_override is converted to REST namespace."""
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.internal:8080",
        )

        # Verify enterprise connection was converted to REST namespace
        assert db.namespace_client_impl == "rest"
        assert db.namespace_client_properties is not None
        assert db.namespace_client_properties["uri"] == "https://phalanx.internal:8080"
        assert db.namespace_client_properties["header.x-api-key"] == "test-api-key"
        assert (
            db.namespace_client_properties["header.x-lancedb-database"] == "my_database"
        )

        # Verify pushdown operations are enabled by default
        assert db.namespace_client_pushdown_operations == ["QueryTable", "CreateTable"]

        # Trigger the lazy connection and verify namespace connection is used
        _ = db._connect
        assert db._namespace_connection is not None

    def test_connect_remote_stores_connection_params(self) -> None:
        """Test that remote connection parameters are stored on Connection object."""
        db = connect(
            uri="db://test_db",
            api_key="my-api-key",
            host_override="https://phalanx.example.com",
            region="us-west-2",
        )

        assert db.uri == "db://test_db"
        assert db._host_override == "https://phalanx.example.com"
        assert db._region == "us-west-2"
        # api_key is wrapped in Credential
        assert db._api_key is not None

    def test_connect_remote_system_namespace_preserved(self) -> None:
        """Remote connections should preserve configured system_namespace."""
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
            system_namespace=["prod", "system"],
        )

        assert db.system_namespace == ["prod", "system"]

    def test_connect_remote_system_namespace_defaults_to_system(self) -> None:
        """Remote connections should default system tables to __system namespace.

        This ensures the client's _geneva_jobs path matches where
        geneva_driver writes via its direct-URI connection, preventing
        the client from polling a stale/wrong jobs table.
        """
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

        # Remote connections use __system namespace so phalanx's
        # FsCatalog.namespace_table_location() routes to
        # {db_uri}/__system/{table}.lance — same path as the driver.
        assert db.system_namespace == ["__system"]

    def test_connect_local_vs_remote_differentiation(self, tmp_path: Path) -> None:
        """Test that local and remote URIs are handled differently."""
        # Local connection
        local_db = connect(tmp_path)
        assert not local_db.uri.startswith("db://")

        # Remote connection
        remote_db = connect(
            uri="db://remote_db",
            api_key="key",
            host_override="https://phalanx.example.com",
        )
        assert remote_db.uri == "db://remote_db"

    def test_connect_remote_flight_client_creation(self) -> None:
        """Test that flight_client is properly configured for remote connections."""
        pytest.importorskip("flightsql")
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com:8080",
        )

        # Access flight_client to trigger creation
        with patch("flightsql.FlightSQLClient") as mock_flight:
            mock_flight.return_value = MagicMock()
            _ = db.flight_client

            # Verify FlightSQLClient was created with correct host
            mock_flight.assert_called_once()
            call_kwargs = mock_flight.call_args.kwargs
            assert call_kwargs.get("host") == "phalanx.example.com"


def test_connect_remote_does_not_probe_system_tables_for_upload_dir() -> None:
    """Remote connect should not touch system tables just to infer upload_dir."""
    with (
        patch("geneva.db.Uploader.get", side_effect=ValueError("unset")),
        patch("geneva.db.lancedb.connect") as mock_lancedb_connect,
    ):
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

    assert db.uri == "db://test_db"
    mock_lancedb_connect.assert_not_called()


def test_connect_namespace_does_not_probe_system_tables_for_upload_dir(
    tmp_path: Path,
) -> None:
    """Namespace connect should not create/open system tables just for upload_dir."""
    with (
        patch("geneva.db.Uploader.get", side_effect=ValueError("unset")),
        patch(
            "geneva.manifest.mgr.ManifestConfigManager",
            side_effect=AssertionError("should not probe manifest table"),
        ),
    ):
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": str(tmp_path)},
        )

    assert db.namespace_client_impl == "dir"


def test_ensure_system_namespace_exists_directory_namespace_defers_namespace_creation(
    tmp_path: Path,
) -> None:
    db = Connection(
        str(tmp_path),
        namespace_client_impl="dir",
        namespace_client_properties={"root": str(tmp_path)},
        system_namespace=["__system"],
    )

    with patch.object(
        db,
        "namespace_client",
        side_effect=AssertionError("directory namespace should not be probed"),
    ):
        _ensure_system_namespace_exists(db)

    assert db.system_namespace == ["__system"]
    assert db._system_namespace_ensured is True


def test_ensure_system_namespace_exists_remote_defers_namespace_creation() -> None:
    db = connect(
        uri="db://test_db",
        api_key="test-key",
        host_override="https://phalanx.example.com",
        system_namespace=["__system"],
    )

    _ensure_system_namespace_exists(db)

    # Remote connections defer namespace creation
    assert db._system_namespace_ensured is True


def test_ensure_system_namespace_exists_remote_defers_with_default_namespace() -> None:
    db = connect(
        uri="db://test_db",
        api_key="test-key",
        host_override="https://phalanx.example.com",
    )

    _ensure_system_namespace_exists(db)

    # Remote connections defer namespace creation (phalanx handles it)
    assert db.system_namespace == ["__system"]
    assert db._system_namespace_ensured is True


REMOTE_NAMESPACE_LOCATION_ERROR = (
    "Invalid input, Location must be provided when namespace is not empty"
)


def test_remote_system_tables_do_not_fallback_to_root_namespace() -> None:
    with (
        patch("geneva.utils.schema.alter_or_create_table") as mock_alter_or_create,
    ):
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
            system_namespace=["__system"],
        )
        mock_alter_or_create.side_effect = RuntimeError(REMOTE_NAMESPACE_LOCATION_ERROR)

        with pytest.raises(RuntimeError, match="Location must be provided"):
            ManifestConfigManager(db)

    assert db.system_namespace == ["__system"]
    assert mock_alter_or_create.call_count == 1
    assert mock_alter_or_create.call_args.kwargs["namespace_path"] == ["__system"]


def test_table_reference_open_db_preserves_remote_system_namespace() -> None:
    """Reopened remote refs should keep their explicit system namespace."""
    with patch("geneva.table.connect") as mock_connect:
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
            system_namespace=["prod", "system"],
        )

        ref.open_db()

    assert mock_connect.call_args.kwargs["system_namespace"] == ["prod", "system"]


def test_table_reference_open_db_preserves_remote_credentials() -> None:
    with patch("geneva.table.connect") as mock_connect:
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

        ref.open_db()

    assert mock_connect.call_args.kwargs["api_key"] == "test-key"
    assert mock_connect.call_args.kwargs["host_override"] == (
        "https://phalanx.example.com"
    )
    assert "initialize_upload_dir" not in mock_connect.call_args.kwargs


def test_table_reference_open_db_does_not_probe_upload_dir(tmp_path: Path) -> None:
    with (
        patch("geneva.db.Uploader.get", side_effect=ValueError("unset")),
        patch(
            "geneva.manifest.mgr.ManifestConfigManager",
            side_effect=AssertionError("should not probe manifest table"),
        ),
    ):
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri=str(tmp_path),
        )

        ref.open_db()


@pytest.mark.asyncio
async def test_table_reference_open_system_db_async_preserves_remote_credentials() -> (
    None
):
    with (
        patch("geneva.db.namespace_connect") as mock_namespace_connect,
        patch("geneva.table.AsyncLanceNamespaceDBConnection") as mock_async_conn,
    ):
        mock_namespace_connect.return_value = MagicMock()
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

        await ref.open_system_db_async()

    assert mock_namespace_connect.call_args.args[0] == "rest"
    assert mock_namespace_connect.call_args.args[1]["header.x-api-key"] == "test-key"
    assert mock_async_conn.call_count == 1


def test_table_reference_checkpoint_store_uses_remote_table_location() -> None:
    with (
        patch("geneva.table.resolve_table_physical_uri") as mock_resolve_uri,
        patch("geneva.checkpoint.FlatLanceCheckpointStore") as mock_checkpoint_store,
    ):
        mock_resolve_uri.return_value = "s3://bucket/db/tbl.lance"
        # ``open_checkpoint_store`` reads ``DEFAULT_TABLE_SUBDIR`` off the
        # selected store class; preserve the real value through the mock so
        # the path under assertion stays stable (and exercises the per-class
        # subdir wiring from GEN-536).
        mock_checkpoint_store.DEFAULT_TABLE_SUBDIR = "_ckp"

        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

        ref.open_checkpoint_store()

    assert mock_resolve_uri.call_args.kwargs["db_uri"] is None
    assert mock_resolve_uri.call_args.kwargs["namespace_client_impl"] == "rest"
    assert (
        mock_resolve_uri.call_args.kwargs["namespace_client_properties"][
            "header.x-api-key"
        ]
        == "test-key"
    )
    assert mock_checkpoint_store.call_args.args[0] == "s3://bucket/db/tbl.lance/_ckp"


def test_table_reference_open_db_preserves_checkpoint_store(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1]}))

    conn = tbl.get_reference().open_db()

    assert conn._checkpoint_store is not None
    assert conn._checkpoint_store.uri().endswith("/tbl.lance/_ckp")


def test_table_reference_open_db_preserves_explicit_empty_remote_system_namespace() -> (
    None
):
    """Explicit root namespace should not be rewritten to __system."""
    with patch("geneva.table.connect") as mock_connect:
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            db_uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
            system_namespace=[],
        )

        ref.open_db()

    assert ref.system_namespace == []
    assert mock_connect.call_args.kwargs["system_namespace"] == []


@pytest.mark.slow
def test_colocated_system_table_ref_reuses_physical_db_root() -> None:
    with patch("geneva.table.connect") as mock_connect:
        ref = TableReference(
            table_id=["tbl"],
            version=None,
            namespace_client_impl="dir",
            namespace_client_properties={"root": "s3://bucket/db"},
            system_namespace=[],
            co_located_system_tables=True,
        )

        ref.as_system_table(GENEVA_JOBS_TABLE_NAME).open_db()

    assert mock_connect.call_args.kwargs["namespace_client_impl"] == "dir"
    assert mock_connect.call_args.kwargs["namespace_client_properties"] == {
        "root": "s3://bucket/db"
    }
    assert mock_connect.call_args.kwargs["system_namespace"] == []


class TestConnectConfig:
    """Tests for connect() configuration loading."""

    def test_connect_loads_config_defaults(self, tmp_path: Path) -> None:
        """Test that connect() loads defaults from config."""
        db = connect(tmp_path)
        # Default region should be set
        assert db._region == "us-east-1"

    def test_connect_explicit_params_override_config(self, tmp_path: Path) -> None:
        """Test that explicit parameters override config defaults."""
        db = connect(tmp_path, region="eu-west-1")
        assert db._region == "eu-west-1"


class TestUploadDirRemoval:
    """Tests for removed connection-level upload_dir configuration."""

    def test_connect_rejects_upload_dir(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError, match="no longer accepts upload_dir"):
            connect(
                tmp_path,
                upload_dir="s3://my-upload-bucket/manifests",
            )

    def test_remote_connection_rejects_upload_dir(self) -> None:
        with pytest.raises(TypeError, match="no longer accepts upload_dir"):
            connect(
                uri="db://my_database",
                api_key="test-api-key",
                host_override="https://phalanx.example.com",
                upload_dir="gs://enterprise-upload-bucket/manifests",
            )

    def test_connect_rejects_initialize_upload_dir(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError, match="no longer accepts initialize_upload_dir"):
            connect(tmp_path, initialize_upload_dir=False)

    def test_connection_state_omits_upload_dir_and_ignores_legacy_state(
        self, tmp_path: Path
    ) -> None:
        db = connect(tmp_path)
        state = db.__getstate__()
        assert "upload_dir" not in state

        state["upload_dir"] = "s3://legacy-upload-bucket/manifests"
        new_db = connect(tmp_path / "other")
        new_db.__setstate__(state)
        assert not hasattr(new_db, "_upload_dir")

    def test_namespace_connection_serialization(self, tmp_path: Path) -> None:
        """Namespace connection state should survive a pickle-style round trip."""
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": str(tmp_path)},
            system_namespace=["prod", "system"],
        )

        state = db.__getstate__()
        assert state["namespace_client_impl"] == "dir"
        assert state["namespace_client_properties"] == {"root": str(tmp_path)}

        new_db = connect(tmp_path / "other")
        new_db.__setstate__(state)
        assert new_db.namespace_client_impl == "dir"
        assert new_db.namespace_client_properties == {"root": str(tmp_path)}
        assert new_db.system_namespace == ["prod", "system"]

    def test_define_manifest_uses_manifest_table_context(self, tmp_path: Path) -> None:
        db = connect(tmp_path)

        # Mock the Uploader to capture how it's instantiated
        with patch("geneva.db.Uploader") as mock_uploader_class:
            mock_uploader = MagicMock()
            mock_uploader_class.return_value = mock_uploader

            # Mock upload_local_env to avoid actual file operations
            with patch("geneva.db.upload_local_env") as mock_upload:
                mock_upload.return_value.__enter__ = MagicMock(return_value=[])
                mock_upload.return_value.__exit__ = MagicMock(return_value=None)

                # Mock the manifest manager
                with patch.object(db, "_manifest_manager") as mock_mgr:
                    mock_mgr.get_table.return_value = MagicMock()
                    db._manifest_manager = mock_mgr

                    # Create a minimal manifest
                    from geneva.manifest.mgr import GenevaManifest

                    manifest = GenevaManifest(name="test_manifest")

                    db.define_manifest("test_manifest", manifest)

                    mock_uploader_class.assert_called_once_with(
                        namespace_config=db._ns_config,
                        table_id=["__system", MANIFEST_TABLE_NAME],
                    )


@pytest.mark.parametrize(
    ("tbl_uri", "expected"),
    [
        # Simple bucket
        ("s3://bucket/table.lance", "s3://bucket"),
        # Bucket with path
        (
            "s3://bucket/path/table.lance",
            "s3://bucket/path",
        ),
        # local
        (
            "/foo/bar/table.lance",
            "/foo/bar",
        ),
        # GCS bucket
        ("gs://gcs-bucket/foo/table.lance", "gs://gcs-bucket/foo"),
        # Remote URI
        ("db://foo/table.lance", "db://foo"),
        # S3+DDB with query params
        (
            "s3+ddb://bucket/path/table.lance?ddbTableName=external-manifest",
            "s3+ddb://bucket/path?ddbTableName=external-manifest",
        ),
        # S3+DDB nested path with query params
        (
            "s3+ddb://bucket/path/to/table.lance?ddbTableName=my-table",
            "s3+ddb://bucket/path/to?ddbTableName=my-table",
        ),
    ],
)
def test_get_db_uri_from_table(tbl_uri, expected) -> None:
    from geneva.db import _get_db_uri

    result = _get_db_uri(tbl_uri)
    assert result == expected


def test_uploader_rejects_db_uri() -> None:
    from geneva.packager.uploader import Uploader

    with pytest.raises(TypeError, match="db_uri"):
        Uploader(db_uri="s3://bucket/path", table_id=["my_table"])


class TestWorkerHostOverride:
    """Tests for worker_host_override parameter (internal endpoint for Ray workers)."""

    def test_connect_with_worker_host_override_stores_in_properties(self) -> None:
        """Test that worker_host_override is stored in namespace_client_properties."""
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.external:8080",
            _worker_host_override="https://phalanx.internal:8080",
        )

        assert db.namespace_client_impl == "rest"
        assert db.namespace_client_properties is not None
        assert db.namespace_client_properties["uri"] == "https://phalanx.external:8080"
        assert (
            db.namespace_client_properties[WORKER_URI_KEY]
            == "https://phalanx.internal:8080"
        )

    def test_connect_without_worker_host_override_no_worker_uri(self) -> None:
        """Test that worker_uri is not set when worker_host_override is not provided."""
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.external:8080",
        )

        assert db.namespace_client_properties is not None
        assert WORKER_URI_KEY not in db.namespace_client_properties

    def test_get_worker_properties_transforms_uri(self) -> None:
        """Test that worker_uri transforms uri for workers."""
        ns = NamespaceConfig(
            namespace_client_properties={
                "uri": "https://external.endpoint.com",
                WORKER_URI_KEY: "https://internal.endpoint.com",
                "header.x-api-key": "my-key",
                "header.x-lancedb-database": "test_db",
            }
        )

        worker_props = ns.get_worker_properties()

        assert worker_props is not None
        assert worker_props["uri"] == "https://internal.endpoint.com"
        assert WORKER_URI_KEY not in worker_props
        assert worker_props["header.x-api-key"] == "my-key"
        assert worker_props["header.x-lancedb-database"] == "test_db"

    def test_get_worker_properties_returns_original_without_worker_uri(
        self,
    ) -> None:
        """Test that original properties are returned when no worker_uri is set."""
        props = {
            "uri": "https://external.endpoint.com",
            "header.x-api-key": "my-key",
        }
        ns = NamespaceConfig(namespace_client_properties=props)

        worker_props = ns.get_worker_properties()

        # Should return the same dict (not a copy) when no transformation needed
        assert worker_props is props

    def test_get_worker_properties_handles_none(self) -> None:
        """Test that None input returns None."""
        ns = NamespaceConfig()
        assert ns.get_worker_properties() is None

    def test_table_reference_open_db_uses_worker_host_override(self) -> None:
        """Test that TableReference.open_db() uses worker_uri when available."""
        with patch("geneva.table.connect") as mock_connect:
            ref = TableReference(
                table_id=["tbl"],
                version=None,
                db_uri="db://test_db",
                api_key="test-key",
                host_override="https://phalanx.external:8080",
                namespace_client_impl="rest",
                namespace_client_properties={
                    "uri": "https://phalanx.external:8080",
                    WORKER_URI_KEY: "https://phalanx.internal:8080",
                    "header.x-api-key": "test-key",
                    "header.x-lancedb-database": "test_db",
                },
            )

            ref.open_db()

            # Verify connect was called with transformed properties
            call_kwargs = mock_connect.call_args.kwargs
            passed_props = call_kwargs["namespace_client_properties"]
            assert passed_props["uri"] == "https://phalanx.internal:8080"
            assert WORKER_URI_KEY not in passed_props

    def test_table_reference_connect_namespace_defaults_to_external_endpoint(
        self,
    ) -> None:
        """Test that TableReference.connect_namespace() uses external uri by default."""
        with patch("geneva.db.namespace_connect") as mock_ns_connect:
            ref = TableReference(
                table_id=["tbl"],
                version=None,
                db_uri="db://test_db",
                namespace_client_impl="rest",
                namespace_client_properties={
                    "uri": "https://phalanx.external:8080",
                    WORKER_URI_KEY: "https://phalanx.internal:8080",
                    "header.x-api-key": "test-key",
                },
            )

            ref.connect_namespace()

            call_args = mock_ns_connect.call_args
            passed_props = call_args[0][1]
            assert passed_props["uri"] == "https://phalanx.external:8080"
            assert WORKER_URI_KEY in passed_props

    def test_table_reference_connect_namespace_uses_worker_host_override(self) -> None:
        """Test that TableReference.connect_namespace() can use worker_uri."""
        with patch("geneva.db.namespace_connect") as mock_ns_connect:
            ref = TableReference(
                table_id=["tbl"],
                version=None,
                db_uri="db://test_db",
                namespace_client_impl="rest",
                namespace_client_properties={
                    "uri": "https://phalanx.external:8080",
                    WORKER_URI_KEY: "https://phalanx.internal:8080",
                    "header.x-api-key": "test-key",
                },
            )

            ref.connect_namespace(use_worker_props=True)

            call_args = mock_ns_connect.call_args
            passed_props = call_args[0][1]
            assert passed_props["uri"] == "https://phalanx.internal:8080"
            assert WORKER_URI_KEY not in passed_props

    def test_resolve_table_physical_uri_can_use_worker_host_override(self) -> None:
        """Worker checkpoint fallback should describe tables through worker_uri."""
        with patch("geneva.db.namespace_connect") as mock_ns_connect:
            namespace = MagicMock()
            namespace.describe_table.return_value.location = "s3://bucket/tbl.lance"
            mock_ns_connect.return_value = namespace

            location = resolve_table_physical_uri(
                ["tbl"],
                db_uri=None,
                namespace_client_impl="rest",
                namespace_client_properties={
                    "uri": "https://phalanx.external:8080",
                    WORKER_URI_KEY: "https://phalanx.internal:8080",
                    "header.x-api-key": "test-key",
                },
                use_worker_props=True,
            )

            assert location == "s3://bucket/tbl.lance"
            passed_props = mock_ns_connect.call_args.args[1]
            assert passed_props["uri"] == "https://phalanx.internal:8080"
            assert WORKER_URI_KEY not in passed_props

    def test_open_checkpoint_store_forwards_worker_props_to_uri_fallback(
        self,
    ) -> None:
        """Worker checkpoint fallback should resolve physical uri through worker_uri."""
        with (
            patch("geneva.db.namespace_connect", return_value=MagicMock()),
            patch("geneva.table.resolve_table_physical_uri") as mock_resolve_uri,
            patch("geneva.checkpoint.FlatLanceCheckpointStore") as mock_store,
        ):
            mock_resolve_uri.return_value = "s3://bucket/tbl.lance"
            ref = TableReference(
                table_id=["tbl"],
                version=None,
                namespace_client_impl="rest",
                namespace_client_properties={
                    "uri": "https://phalanx.external:8080",
                    WORKER_URI_KEY: "https://phalanx.internal:8080",
                    "header.x-api-key": "test-key",
                },
                storage_options={"account_name": "acct"},
            )

            ref.open_checkpoint_store(use_worker_props=True)

            assert mock_resolve_uri.call_args.kwargs["use_worker_props"] is True
            store_kwargs = mock_store.call_args.kwargs
            assert store_kwargs["namespace_client_impl"] == "rest"
            assert (
                store_kwargs["namespace_client_properties"]["uri"]
                == "https://phalanx.internal:8080"
            )
            assert WORKER_URI_KEY not in store_kwargs["namespace_client_properties"]
            assert store_kwargs["storage_options"] == {"account_name": "acct"}

    def test_connection_uses_external_endpoint_not_worker_uri(self) -> None:
        """Test that Connection (notebook side) uses external endpoint.

        db:// connections set namespace_client_properties with the
        external host_override URI for worker-side namespace access.
        """
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.external:8080",
            _worker_host_override="https://phalanx.internal:8080",
        )

        props = db.namespace_client_properties
        assert props is not None
        assert props["uri"] == "https://phalanx.external:8080"
        assert props[WORKER_URI_KEY] == "https://phalanx.internal:8080"

    def test_table_reference_preserves_worker_uri_in_properties(self) -> None:
        """Test that TableReference preserves worker_uri for later transformation.

        When a Table creates a TableReference, the worker_uri should be preserved
        in namespace_client_properties so workers can use it.
        """
        with patch("geneva.db.namespace_connect") as mock_ns_connect:
            mock_ns_connect.return_value = MagicMock()

            db = connect(
                uri="db://my_database",
                api_key="test-api-key",
                host_override="https://phalanx.external:8080",
                _worker_host_override="https://phalanx.internal:8080",
            )

            # Verify the connection stores both URIs
            assert db.namespace_client_properties is not None
            assert (
                db.namespace_client_properties["uri"] == "https://phalanx.external:8080"
            )
            assert (
                db.namespace_client_properties[WORKER_URI_KEY]
                == "https://phalanx.internal:8080"
            )

    def test_worker_properties_transformation_is_idempotent(self) -> None:
        """Test that transforming properties multiple times is safe.

        Once worker_uri is transformed to uri, subsequent transformations
        should be no-ops (return the same dict).
        """
        ns = NamespaceConfig(
            namespace_client_properties={
                "uri": "https://external.endpoint.com",
                WORKER_URI_KEY: "https://internal.endpoint.com",
                "header.x-api-key": "my-key",
            }
        )

        # First transformation
        worker_props = ns.get_worker_properties()
        assert worker_props is not None
        assert worker_props["uri"] == "https://internal.endpoint.com"
        assert WORKER_URI_KEY not in worker_props

        # Second transformation (should return same dict, no worker_uri to transform)
        ns2 = NamespaceConfig(namespace_client_properties=worker_props)
        worker_props_2 = ns2.get_worker_properties()
        assert worker_props_2 is worker_props  # Same object returned

    def test_worker_properties_does_not_mutate_original(self) -> None:
        """Test that get_worker_properties doesn't mutate original."""
        original_props = {
            "uri": "https://external.endpoint.com",
            WORKER_URI_KEY: "https://internal.endpoint.com",
            "header.x-api-key": "my-key",
        }
        original_uri = original_props["uri"]
        original_worker_uri = original_props[WORKER_URI_KEY]

        ns = NamespaceConfig(namespace_client_properties=original_props)
        worker_props = ns.get_worker_properties()

        # Original should be unchanged
        assert original_props["uri"] == original_uri
        assert original_props[WORKER_URI_KEY] == original_worker_uri
        assert WORKER_URI_KEY in original_props

        # Transformed should be different
        assert worker_props is not None
        assert worker_props["uri"] == original_worker_uri
        assert WORKER_URI_KEY not in worker_props

    def test_worker_host_override_supports_fqdn_with_trailing_dot(self) -> None:
        """Test that worker_host_override supports FQDN with trailing dot.

        Kubernetes internal DNS names often use trailing dots to indicate
        fully qualified domain names (e.g., "phalanx.namespace.svc.cluster.local.").
        """
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.external:8080",
            _worker_host_override="http://phalanx.geneva.svc.cluster.local.:8080",
        )

        assert db.namespace_client_properties is not None
        assert (
            db.namespace_client_properties[WORKER_URI_KEY]
            == "http://phalanx.geneva.svc.cluster.local.:8080"
        )

        # Verify transformation preserves the trailing dot
        ns = db._ns_config
        worker_props = ns.get_worker_properties()
        assert worker_props is not None
        assert worker_props["uri"] == "http://phalanx.geneva.svc.cluster.local.:8080"


class TestStorageOptionsPropagation:
    """Tests for storage_options propagation through TableReference."""

    def test_create_table_inherits_connection_storage_options(
        self, tmp_path: Path
    ) -> None:
        """db.create_table() without an explicit storage_options must fall back
        to Connection._storage_options. Regression for the customer's Azure
        backfill: NativeTable._ltbl reopens with storage_options=None and dies
        on cloud URIs ("no Azure account name in URI") when the create-table
        call site doesn't thread the Connection-level options.
        """
        db = connect(
            str(tmp_path),
            storage_options={"account_name": "myaccount", "account_key": "mykey"},
        )

        tbl = db.create_table("test", [{"id": 1}])

        assert tbl._storage_options is not None
        assert tbl._storage_options.get("account_name") == "myaccount"
        assert tbl._storage_options.get("account_key") == "mykey"

    def test_create_table_explicit_storage_options_wins(self, tmp_path: Path) -> None:
        """Explicit storage_options on create_table takes precedence over the
        Connection-level options.
        """
        db = connect(
            str(tmp_path),
            storage_options={"account_name": "from-conn"},
        )

        tbl = db.create_table(
            "test",
            [{"id": 1}],
            storage_options={"account_name": "from-call"},
        )

        assert tbl._storage_options == {"account_name": "from-call"}

    def test_get_reference_merges_connection_and_latest_storage_options(
        self, tmp_path: Path
    ) -> None:
        """Test that get_reference() merges connection storage_options with latest."""
        db = connect(
            str(tmp_path),
            storage_options={"account_name": "myaccount", "account_key": "mykey"},
        )
        db.create_table("test", [{"id": 1}])
        tbl = db.open_table("test")

        ref = tbl.get_reference()

        # Should have connection's storage_options (latest_storage_options returns None
        # for local tables, so only connection options are present)
        assert ref.storage_options is not None
        assert ref.storage_options.get("account_name") == "myaccount"
        assert ref.storage_options.get("account_key") == "mykey"

    def test_get_reference_without_storage_options(self, tmp_path: Path) -> None:
        """Test that get_reference() works without storage_options."""
        db = connect(str(tmp_path))
        db.create_table("test", [{"id": 1}])
        tbl = db.open_table("test")

        ref = tbl.get_reference()

        # Should be None when no storage_options provided
        assert ref.storage_options is None

    def test_as_system_table_propagates_storage_options(self) -> None:
        """Test that as_system_table() propagates storage_options."""
        ref = TableReference(
            table_id=["my_table"],
            version=None,
            db_uri="az://mycontainer/path",
            storage_options={"account_name": "myaccount", "account_key": "secret"},
        )

        system_ref = ref.as_system_table("_geneva_jobs")

        assert system_ref.storage_options is not None
        assert system_ref.storage_options["account_name"] == "myaccount"
        assert system_ref.storage_options["account_key"] == "secret"

    def test_open_db_passes_storage_options_for_cloud_uri(self) -> None:
        """Test that open_db() passes storage_options for cloud storage URIs."""
        with patch("geneva.table.connect") as mock_connect:
            ref = TableReference(
                table_id=["my_table"],
                version=None,
                db_uri="az://mycontainer/path",
                storage_options={"account_name": "myaccount", "account_key": "secret"},
            )

            ref.open_db()

            call_kwargs = mock_connect.call_args.kwargs
            assert call_kwargs["storage_options"] == {
                "account_name": "myaccount",
                "account_key": "secret",
            }

    def test_open_db_forwards_storage_options_for_db_uri(self) -> None:
        """Explicit storage_options reach the worker Connection for db:// refs."""
        with patch("geneva.table.connect") as mock_connect:
            ref = TableReference(
                table_id=["my_table"],
                version=None,
                db_uri="db://my_database",
                api_key="test-key",
                host_override="https://phalanx.external:8080",
                storage_options={"account_name": "myaccount"},
            )

            ref.open_db()

            call_kwargs = mock_connect.call_args.kwargs
            assert call_kwargs["storage_options"] == {"account_name": "myaccount"}

    def test_open_db_omits_storage_options_when_none_for_db_uri(self) -> None:
        """No storage_options supplied -> None is forwarded, not synthesized."""
        with patch("geneva.table.connect") as mock_connect:
            ref = TableReference(
                table_id=["my_table"],
                version=None,
                db_uri="db://my_database",
                api_key="test-key",
                host_override="https://phalanx.external:8080",
            )

            ref.open_db()

            assert mock_connect.call_args.kwargs["storage_options"] is None

    @pytest.mark.asyncio
    async def test_open_db_async_passes_storage_options(self) -> None:
        """Direct storage refs pass storage options to directory namespace."""
        with (
            patch("geneva.db.namespace_connect") as mock_namespace_connect,
            patch("geneva.table.AsyncLanceNamespaceDBConnection") as mock_async_conn,
        ):
            mock_namespace_connect.return_value = MagicMock()
            mock_async_conn.return_value = MagicMock()

            ref = TableReference(
                table_id=["my_table"],
                version=None,
                db_uri="s3://mybucket/path",
                storage_options={
                    "aws_access_key_id": "AKID",
                    "aws_secret_access_key": "secret",
                },
            )

            await ref.open_db_async()

            assert mock_namespace_connect.call_args.args[0] == "dir"
            assert mock_namespace_connect.call_args.args[1] == {
                "root": "s3://mybucket/path",
                "storage.aws_access_key_id": "AKID",
                "storage.aws_secret_access_key": "secret",
            }
            mock_async_conn.assert_called_once()

    @pytest.mark.asyncio
    async def test_open_system_db_async_passes_storage_options(self) -> None:
        """System async direct storage refs use directory namespace credentials."""
        with (
            patch("geneva.db.namespace_connect") as mock_namespace_connect,
            patch("geneva.table.AsyncLanceNamespaceDBConnection") as mock_async_conn,
        ):
            mock_namespace_connect.return_value = MagicMock()
            mock_async_conn.return_value = MagicMock()

            ref = TableReference(
                table_id=["my_table"],
                version=None,
                db_uri="gs://mybucket/path",
                storage_options={"google_service_account_key": "key"},
            )

            await ref.open_system_db_async()

            assert mock_namespace_connect.call_args.args[0] == "dir"
            assert mock_namespace_connect.call_args.args[1] == {
                "root": "gs://mybucket/path",
                "storage.google_service_account_key": "key",
            }
            mock_async_conn.assert_called_once()

    def test_storage_options_not_in_repr(self) -> None:
        """Test that storage_options values are redacted in repr."""
        ref = TableReference(
            table_id=["my_table"],
            version=None,
            db_uri="az://mycontainer/path",
            storage_options={"account_name": "myaccount", "account_key": "supersecret"},
        )

        repr_str = repr(ref)

        # Values must never appear in repr
        assert "supersecret" not in repr_str
        assert "myaccount" not in repr_str
        # Keys are shown for debugging, but values are redacted
        assert "[REDACTED]" in repr_str


class TestOpenLanceDatasetCloudWarning:
    """Verify open_lance_dataset warns on cloud URIs without storage_options.

    Catches data-flow bugs where credentials exist on a Connection but a
    chain of intermediary objects fails to thread them into the open. The
    AST guard and required-kwarg signature only check syntactic presence
    of storage_options=; this runtime check fires when the value is None
    on a scheme that needs credentials.
    """

    @pytest.mark.parametrize(
        "uri",
        [
            "az://mycontainer/path/table.lance",
            "abfs://container@account.dfs.core.windows.net/path",
            "s3://mybucket/path/table.lance",
            "s3+ddb://mybucket/path?ddbTableName=x",
            "gs://mybucket/path/table.lance",
            "gcs://mybucket/path/table.lance",
        ],
    )
    def test_warns_on_cloud_uri_with_no_storage_options(
        self, uri: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        from geneva.db import open_lance_dataset

        with (
            patch("lance.dataset") as mock_lance,
            caplog.at_level("WARNING", logger="geneva.db"),
        ):
            open_lance_dataset(uri, storage_options=None)

        assert mock_lance.called
        msgs = [rec.message for rec in caplog.records]
        assert any("no storage_options" in m and uri in m for m in msgs), (
            f"expected warning mentioning {uri}, got: {msgs}"
        )

    def test_no_warning_when_storage_options_present(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        from geneva.db import open_lance_dataset

        with (
            patch("lance.dataset") as mock_lance,
            caplog.at_level("WARNING", logger="geneva.db"),
        ):
            open_lance_dataset(
                "az://mycontainer/path/table.lance",
                storage_options={"account_name": "foo"},
            )

        assert mock_lance.called
        assert not any("no storage_options" in rec.message for rec in caplog.records)

    def test_no_warning_for_local_path(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        from geneva.db import open_lance_dataset

        with (
            patch("lance.dataset") as mock_lance,
            caplog.at_level("WARNING", logger="geneva.db"),
        ):
            open_lance_dataset(str(tmp_path / "t.lance"), storage_options=None)

        assert mock_lance.called
        assert not any("no storage_options" in rec.message for rec in caplog.records)

    def test_no_warning_when_namespace_client_present(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        from geneva.db import open_lance_dataset

        mock_ns_client = MagicMock()
        with (
            patch("lance.dataset") as mock_lance,
            caplog.at_level("WARNING", logger="geneva.db"),
        ):
            open_lance_dataset(
                "az://mycontainer/path/table.lance",
                storage_options=None,
                namespace_client=mock_ns_client,
                table_id=["my_table"],
            )

        assert mock_lance.called
        assert not any("no storage_options" in rec.message for rec in caplog.records)

    def test_namespace_table_not_found_does_not_fallback_to_uri(self) -> None:
        from geneva.db import open_lance_dataset

        mock_ns_client = MagicMock()
        with patch("lance.dataset") as mock_lance:
            mock_lance.side_effect = RuntimeError("table not found")

            with pytest.raises(RuntimeError, match="table not found"):
                open_lance_dataset(
                    "s3://bucket/path/table.lance",
                    namespace_client=mock_ns_client,
                    table_id=["missing"],
                    storage_options={"aws_region": "us-east-1"},
                )

        assert mock_lance.call_count == 1

    def test_rest_namespace_table_not_found_does_not_fallback_to_uri(self) -> None:
        from geneva.db import open_lance_dataset

        with patch("lance.dataset") as mock_lance:
            mock_lance.side_effect = RuntimeError("table not found")

            with pytest.raises(RuntimeError, match="table not found"):
                open_lance_dataset(
                    "s3://bucket/path/table.lance",
                    namespace_config=NamespaceConfig(
                        namespace_client_impl="rest",
                        namespace_client_properties={"uri": "https://example.com"},
                    ),
                    table_id=["missing"],
                    storage_options={"aws_region": "us-east-1"},
                )

        assert mock_lance.call_count == 1

    def test_namespace_type_error_falls_back_to_uri_for_compatibility(self) -> None:
        from geneva.db import open_lance_dataset

        sentinel = object()
        mock_ns_client = MagicMock()
        with patch("lance.dataset") as mock_lance:
            mock_lance.side_effect = [
                TypeError("unexpected keyword argument 'namespace_client'"),
                sentinel,
            ]

            result = open_lance_dataset(
                "s3://bucket/path/table.lance",
                namespace_client=mock_ns_client,
                table_id=["tbl"],
                storage_options={"aws_region": "us-east-1"},
            )

        assert result is sentinel
        assert mock_lance.call_count == 2
        assert mock_lance.call_args.args == ("s3://bucket/path/table.lance",)
        assert mock_lance.call_args.kwargs["storage_options"] == {
            "aws_region": "us-east-1"
        }

    def test_directory_namespace_credentials_redacted_in_repr(
        self, tmp_path: Path
    ) -> None:
        """Namespace credentials should not leak in reprs."""
        db = connect(
            tmp_path,
            storage_options={
                "aws_access_key_id": "access",
                "aws_secret_access_key": "supersecret",
                "endpoint": "http://example.com",
            },
        )
        ref = TableReference(
            table_id=["my_table"],
            version=None,
            db_uri=str(tmp_path),
            namespace_client_impl=db.namespace_client_impl,
            namespace_client_properties=db.namespace_client_properties,
            storage_options={
                "aws_access_key_id": "access",
                "aws_secret_access_key": "supersecret",
            },
        )

        assert db.namespace_client_properties is not None
        assert (
            db.namespace_client_properties["storage.aws_secret_access_key"]
            == "supersecret"
        )

        namespace_repr = repr(db.namespace_client_properties)
        ref_repr = repr(ref)

        assert "supersecret" not in namespace_repr
        assert "supersecret" not in ref_repr
        assert "storage.endpoint" in namespace_repr

        rest_properties = _as_namespace_client_properties(
            {
                "uri": "https://example.com",
                "header.x-api-key": "restsecret",
                "header.x-lancedb-database": "db",
            }
        )
        assert rest_properties is not None
        rest_repr = repr(rest_properties)
        assert "restsecret" not in rest_repr
        assert "header.x-api-key" in rest_repr

        explicit_conn = Connection(
            "namespace://",
            namespace_client_impl="rest",
            namespace_client_properties={
                "uri": "https://example.com",
                "header.x-api-key": "explicitsecret",
            },
            system_namespace=[],
        )
        assert "explicitsecret" not in repr(explicit_conn.namespace_client_properties)


# ---------------------------------------------------------------------------
# System namespace alignment: client ↔ driver
#
# These tests ensure that enterprise (db://) clients and direct-URI clients
# (like geneva_driver) resolve _geneva_jobs to the same physical path.
# Regression guard for the bug where the client used namespace=[] (root)
# while the driver used __system, causing RemoteJob.result() to time out
# polling a different table than the one the driver was updating.
# ---------------------------------------------------------------------------


class TestSystemNamespaceAlignment:
    """Verify that the client and driver agree on system table locations."""

    def test_remote_defaults_to_system_namespace(self) -> None:
        """db:// + host_override should default to ['__system']."""
        db = connect(
            uri="db://mydb",
            api_key="key",
            host_override="https://phalanx.example.com",
        )
        assert db.system_namespace == ["__system"]

    def test_remote_explicit_override_is_preserved(self) -> None:
        """Explicit system_namespace should not be overwritten."""
        db = connect(
            uri="db://mydb",
            api_key="key",
            host_override="https://phalanx.example.com",
            system_namespace=["custom"],
        )
        assert db.system_namespace == ["custom"]

    def test_remote_explicit_empty_is_preserved(self) -> None:
        """Explicitly passing [] should NOT be rewritten to ['__system']."""
        db = connect(
            uri="db://mydb",
            api_key="key",
            host_override="https://phalanx.example.com",
            system_namespace=[],
        )
        assert db.system_namespace == []

    def test_direct_uri_uses_directory_namespace(self, tmp_path: Path) -> None:
        """Direct-URI connections are normalized to directory namespace."""
        db = connect(str(tmp_path))
        assert db.namespace_client_impl == "dir"
        assert db.namespace_client_properties == {
            "root": str(tmp_path),
            "manifest_enabled": "true",
        }
        assert db.system_namespace == ["__system"]
        assert str(db.uri) == str(tmp_path)

    def test_namespace_connection_defaults_to_system(self, tmp_path: Path) -> None:
        """Namespace connections (non-remote) should default to ['__system']."""
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": str(tmp_path)},
        )
        assert db.system_namespace == ["__system"]

    def test_client_driver_path_alignment(self, tmp_path: Path) -> None:
        """Local and enterprise clients should use the same system namespace."""
        driver_db = connect(str(tmp_path))
        client_db = connect(
            uri="db://test",
            api_key="key",
            host_override="https://phalanx.example.com",
        )

        assert driver_db.system_namespace == ["__system"]
        assert client_db.system_namespace == ["__system"]

    def test_directory_namespace_root_stable_create_duplicate_raises(
        self,
        tmp_path: Path,
    ) -> None:
        db = connect(str(tmp_path))
        storage_options = {"new_table_enable_stable_row_ids": "true"}

        db.create_table(
            "stable_duplicate",
            data=pa.table({"value": [1]}),
            storage_options=storage_options,
        )

        with pytest.raises(Exception, match="already exists"):
            db.create_table(
                "stable_duplicate",
                data=pa.table({"value": [2]}),
                storage_options=storage_options,
            )


class TestAddColumnsRefreshesLtbl:
    """Regression: add_columns must make new columns visible via schema/count_rows."""

    def test_schema_visible_after_add_columns(self, tmp_path: Path) -> None:
        """After add_columns, the new column must be visible via schema/count_rows."""
        import pyarrow as pa

        from geneva import udf

        @udf(data_type=pa.int64())
        def double_val(val: int) -> int:
            return val * 2

        db = connect(str(tmp_path))
        tbl = db.create_table("t", data=pa.table({"val": [1, 2, 3]}))

        tbl.add_columns({"doubled": double_val})
        assert "doubled" in tbl.schema.names
        assert tbl.count_rows("`doubled` IS NULL") == 3  # not yet backfilled


class TestConnectionSplit:
    """connect() always returns Connection (aliases are equivalent)."""

    def test_local_uri_returns_connection(self, tmp_path: Path) -> None:
        from geneva.db import Connection, NativeConnection, RemoteConnection

        db = connect(str(tmp_path))
        assert isinstance(db, Connection)
        # Aliases are the same type now
        assert isinstance(db, NativeConnection)
        assert isinstance(db, RemoteConnection)

    def test_db_uri_returns_connection(self) -> None:
        from geneva.db import Connection

        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.internal:8080",
        )
        assert isinstance(db, Connection)
        assert db.is_remote_uri()

    def test_table_returned_for_connection(self, tmp_path: Path) -> None:
        from geneva.table import NativeTable, Table

        db = connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": [1, 2]}))
        assert isinstance(tbl, Table)
        assert isinstance(tbl, NativeTable)

    def test_open_table_returns_table(self, tmp_path: Path) -> None:
        from geneva.table import Table

        db = connect(str(tmp_path))
        db.create_table("t2", pa.table({"a": [1, 2]}))
        tbl = db.open_table("t2")
        assert isinstance(tbl, Table)


class TestRemoteConnectionRouting:
    """V2 routing is now driven by ``Connection.routes_through_v2()``,
    derived from the URI and the ``executor_mode`` flag passed at connect
    time. No env-var feature flag."""

    def test_remote_connection_introspection(self) -> None:
        db = connect(
            uri="db://my_db",
            api_key="x",
            host_override="https://phalanx.internal",
        )

        assert db.uri == "db://my_db"
        assert db.is_remote_uri()
        assert db.use_remote_dispatch()

    def test_executor_mode_disables_v2_routing(self) -> None:
        db = connect(
            uri="db://my_db",
            api_key="x",
            host_override="https://phalanx.internal",
            executor_mode=True,
        )

        assert db.is_remote_uri()
        assert not db.use_remote_dispatch()

    def test_native_connection_never_routes_through_v2(self, tmp_path) -> None:
        db = connect(str(tmp_path))
        assert not db.is_remote_uri()
        assert not db.use_remote_dispatch()
