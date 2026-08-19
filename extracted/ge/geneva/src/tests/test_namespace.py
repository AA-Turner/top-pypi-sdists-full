# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import copy
import shutil
import tempfile
from unittest.mock import MagicMock

import lancedb
import pyarrow as pa
import pytest

import geneva.table as geneva_table
from geneva.db import connect
from geneva.manifest.mgr import GenevaManifest
from geneva.table import TableReference


class TestNamespaceConnection:
    """Test namespace-based LanceDB connection."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_connect_namespace_dir(self) -> None:
        """Test connecting to Geneva through DirectoryNamespace."""
        # Connect using DirectoryNamespace
        props = {"root": self.temp_dir}
        db = lancedb.connect_namespace("dir", props)

        # Should be a LanceNamespaceDBConnection
        assert isinstance(db, lancedb.LanceNamespaceDBConnection)

        # Initially no tables
        assert len(list(db.table_names())) == 0

        # connect through geneva
        db = connect(namespace_client_impl="dir", namespace_client_properties=props)
        assert len(list(db.table_names())) == 0

        assert db.namespace_client_impl == "dir"
        assert db.namespace_client_properties == props
        assert len(list(db.table_names())) == 0
        assert isinstance(db._namespace_connection, lancedb.LanceNamespaceDBConnection)

    def test_open_table_through_namespace(self) -> None:
        """Test opening an existing table through namespace."""
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

        # Create a table with schema
        schema = pa.schema(
            [
                pa.field("id", pa.int64()),
                pa.field("vector", pa.list_(pa.float32(), 2)),
            ]
        )
        db.create_table("test_table", schema=schema)

        # Open the table
        table = db.open_table("test_table")
        assert table is not None
        assert table.name == "test_table"

        # Verify empty table with correct schema
        result = table.to_pandas()
        assert len(result) == 0
        assert list(result.columns) == ["id", "vector"]

        assert len(db.list_manifests()) == 0

    def test_open_table_namespace_path_alias(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """open_table should honor namespace_path for namespace-backed dbs."""
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

        namespace = ["workspace"]
        captured: dict[str, list[str]] = {}

        class DummyTable:
            def __init__(
                self, *_: object, namespace: list[str] | None = None, **__: object
            ) -> None:
                captured["namespace"] = namespace or []

        # open_table instantiates NativeTable for native-mode connections.
        monkeypatch.setattr(geneva_table, "NativeTable", DummyTable)

        table = db.open_table("ns_table", namespace_path=namespace)
        assert isinstance(table, DummyTable)
        assert captured["namespace"] == namespace

    def test_table_reference(self) -> None:
        props = {"root": self.temp_dir}
        ref = TableReference(
            table_id=["test_table"],
            version=None,
            db_uri=None,
            namespace_client_impl="dir",
            namespace_client_properties=props,
        )

        db = ref.open_db()

        assert db.namespace_client_impl == "dir"
        assert db.namespace_client_properties == props
        assert len(list(db.table_names())) == 0
        assert isinstance(db._namespace_connection, lancedb.LanceNamespaceDBConnection)
        assert ref.table_id == ["test_table"]
        assert ref.table_name == "test_table"

    @pytest.mark.slow
    def test_manifest_crud_with_namespace(self) -> None:
        """Test manifest CRUD operations with namespace connection."""
        # Create mock uploader to avoid actual file uploads
        mock_uploader = MagicMock()
        mock_uploader.upload_dir = "/mock/upload/dir"
        mock_uploader._file_exists.return_value = False
        mock_uploader.upload.side_effect = lambda path: f"mock://{path.name}"

        # Connect using namespace
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

        # Verify manifest table will be created in the configured namespace
        assert db.namespace_client_impl == "dir"
        assert db.system_namespace == ["__system"]  # Default system namespace

        # Create a manifest
        manifest_def = GenevaManifest(
            name="test-ns-manifest",
            local_zip_output_dir=self.temp_dir,
            skip_site_packages=False,
            delete_local_zips=False,
            pip=["numpy", "pandas"],
            py_modules=["pyarrow"],
        )

        # Test CREATE: define manifest
        db.define_manifest("test-ns-manifest", manifest_def, uploader=mock_uploader)

        # Verify upload was called
        upload_count = mock_uploader.upload.call_count
        assert upload_count >= 1, "files should have been uploaded"

        # Test READ: list manifests
        manifests = db.list_manifests()
        assert len(manifests) == 1, "should have exactly one manifest"
        m = manifests[0]
        _assert_manifest_eq(m.as_dict(), manifest_def.as_dict())
        assert m.name == "test-ns-manifest"
        assert m.pip == ["numpy", "pandas"]
        assert m.py_modules == ["pyarrow"]

        # Test UPDATE: update manifest and verify checksum changes
        manifest_def.skip_site_packages = True
        db.define_manifest("test-ns-manifest", manifest_def, uploader=mock_uploader)

        manifests = db.list_manifests()
        assert len(manifests) == 1, "should still have exactly one manifest"
        m1 = manifests[0].as_dict()
        m2 = manifest_def.as_dict()
        assert m1["checksum"] != m2["checksum"], "checksum should change after update"
        _assert_manifest_eq(m1, m2)
        assert mock_uploader.upload.call_count >= upload_count, (
            "more files should be uploaded"
        )

        # Test DELETE: delete manifest
        db.delete_manifest("test-ns-manifest")
        assert db.list_manifests() == [], "manifest should be deleted"

    @pytest.mark.slow
    def test_manifest_custom_namespace_config(self) -> None:
        """Test manifest with custom system namespace configuration."""
        mock_uploader = MagicMock()
        mock_uploader.upload_dir = "/mock/upload/dir"
        mock_uploader._file_exists.return_value = False
        mock_uploader.upload.side_effect = lambda path: f"mock://{path.name}"

        # Connect with custom system namespace
        db = connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
            system_namespace=["custom", "namespace"],
        )

        # Verify custom configuration
        assert db.system_namespace == ["custom", "namespace"]

        # Create and verify manifest works with custom config
        manifest_def = GenevaManifest(
            name="custom-manifest",
            local_zip_output_dir=self.temp_dir,
            skip_site_packages=True,
            delete_local_zips=False,
            pip=["requests"],
        )

        db.define_manifest("custom-manifest", manifest_def, uploader=mock_uploader)

        # Verify manifest was created
        manifests = db.list_manifests()
        assert len(manifests) == 1
        assert manifests[0].name == "custom-manifest"
        assert manifests[0].pip == ["requests"]

        # Clean up
        db.delete_manifest("custom-manifest")
        assert db.list_manifests() == []


def _assert_manifest_eq(m1: dict, m2: dict) -> None:
    """Assert two manifest dicts are equal, excluding transient fields."""
    m1 = copy.deepcopy(m1)
    m2 = copy.deepcopy(m2)
    # exclude transient fields from comparison
    for f in {"checksum", "zips", "created_at", "created_by"}:
        if f in m1:
            del m1[f]
        if f in m2:
            del m2[f]
    assert m1 == m2, "manifests should match"


def test_backfill_namespace_client_sends_min_read_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remote backfill attaches ``x-lancedb-min-read-version`` (= the client's
    current table version) so a query node under weak read consistency refreshes
    to a snapshot that includes a just-added column, instead of failing backfill
    validation with ``Column '<name>' not found``.
    """
    import types

    import lance_namespace

    captured: dict = {}

    def fake_connect(impl: str, props: dict) -> str:
        captured["impl"] = impl
        captured["props"] = dict(props)
        return "header-client"

    monkeypatch.setattr(lance_namespace, "connect", fake_connect)

    base_props = {
        "uri": "http://localhost:10024",
        "header.x-api-key": "secret",
        "header.x-lancedb-database": "mydb",
    }
    conn = types.SimpleNamespace(
        namespace_client_impl="rest",
        namespace_client_properties=base_props,
        namespace_client=lambda: "shared-client",
    )
    fake_self = types.SimpleNamespace(_conn=conn, version=12)

    ns = geneva_table.Table._min_read_version_namespace_client(fake_self)

    assert ns == "header-client"
    assert captured["impl"] == "rest"
    # the monotonic read floor is attached...
    assert captured["props"]["header.x-lancedb-min-read-version"] == "12"
    # ...without dropping the existing auth/db headers or the uri
    assert captured["props"]["header.x-api-key"] == "secret"
    assert captured["props"]["header.x-lancedb-database"] == "mydb"
    assert captured["props"]["uri"] == "http://localhost:10024"
    assert captured["props"]["header.user-agent"].startswith("Geneva-Python-Client/")
    # the caller's props are copied, not mutated in place
    assert "header.x-lancedb-min-read-version" not in base_props


@pytest.mark.parametrize(
    ("impl", "props"),
    [
        (None, None),
        # A local "dir" namespace has non-None impl/props but no query-node
        # cache, so it must still fall back to the shared, mockable client —
        # otherwise unit tests that patch ``namespace_client()`` are bypassed.
        ("dir", {"root": "namespace-root", "manifest_enabled": "true"}),
    ],
)
def test_backfill_namespace_client_falls_back_for_non_rest(
    impl: "str | None",
    props: "dict | None",
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only REST namespaces get the header client; every other impl falls back
    to the connection's default (mockable) client rather than building one.
    """
    import types

    import lance_namespace

    monkeypatch.setattr(
        lance_namespace,
        "connect",
        lambda *a, **k: pytest.fail("should not build a fresh client for non-rest"),
    )
    conn = types.SimpleNamespace(
        namespace_client_impl=impl,
        namespace_client_properties=props,
        namespace_client=lambda: "default-client",
    )
    fake_self = types.SimpleNamespace(_conn=conn, version=7)

    ns = geneva_table.Table._min_read_version_namespace_client(fake_self)
    assert ns == "default-client"
