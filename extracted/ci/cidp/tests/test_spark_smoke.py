"""Local-Spark smoke test. Skipped if pyspark is not installed or local Spark
cannot start. Requires a JDK on PATH and pyspark[sql]. This is not a
substitute for production tests against the real S3+Glue stack, but
exercises the write/ADD/verify/ANALYZE path end to end.
"""
import pytest

pyspark = pytest.importorskip("pyspark")
from pyspark.sql import SparkSession

from cidp import _partitions
from cidp.spark import write_table


@pytest.fixture(scope="module")
def spark(tmp_path_factory):
    warehouse = tmp_path_factory.mktemp("warehouse")
    s = (
        SparkSession.builder
        .master("local[1]")
        .appName("cidp-smoke")
        .config("spark.sql.warehouse.dir", str(warehouse))
        .config("spark.sql.catalogImplementation", "hive")
        .getOrCreate()
    )
    yield s
    s.stop()


def _make_df(spark, rows):
    return spark.createDataFrame(rows)


@pytest.fixture(autouse=True)
def _smoke_db(spark, request):
    # Skip database creation for tests that don't need Spark (e.g., pure unit tests)
    if request.cls and request.cls.__name__ in ("TestParseS3aUri", "TestGetOrCreateSpark"):
        return
    spark.sql("CREATE DATABASE IF NOT EXISTS smoke_db")


class TestAddVerifyAnalyzeRoundTrip:
    def test_single_partition(self, spark):
        rows = [
            {"id": 1, "dt": "2026-05-12"},
            {"id": 2, "dt": "2026-05-12"},
        ]
        df = _make_df(spark, rows)
        write_table(df, "smoke_db", "single_p",
                    partitions={"dt": "2026-05-12"})

        parts = {r[0] for r in spark.sql(
            "SHOW PARTITIONS smoke_db.single_p"
        ).collect()}
        assert "dt=2026-05-12" in parts

    def test_multi_partition_with_reorder(self, spark):
        rows = [
            {"id": 1, "dt": "2026-05-12", "region": "KR"},
            {"id": 2, "dt": "2026-05-12", "region": "KR"},
        ]
        df = _make_df(spark, rows)

        # First call: defines DDL with (dt, region) order from input dict.
        write_table(df, "smoke_db", "multi_p",
                    partitions={"dt": "2026-05-12", "region": "KR"})

        # Second call with the input dict order swapped: must auto-reorder
        # to match existing DDL.
        df2 = _make_df(spark, [
            {"id": 3, "dt": "2026-05-13", "region": "JP"},
        ])
        write_table(df2, "smoke_db", "multi_p",
                    partitions={"region": "JP", "dt": "2026-05-13"})

        parts = {r[0] for r in spark.sql(
            "SHOW PARTITIONS smoke_db.multi_p"
        ).collect()}
        assert "dt=2026-05-12/region=KR" in parts
        assert "dt=2026-05-13/region=JP" in parts

    def test_add_partition_idempotent(self, spark):
        rows = [{"id": 1, "dt": "2026-05-12"}]
        df = _make_df(spark, rows)
        write_table(df, "smoke_db", "idempotent_p",
                    partitions={"dt": "2026-05-12"})

        ordered = [("dt", "2026-05-12")]
        _partitions.add_partition(spark, "smoke_db", "idempotent_p", ordered)
        _partitions.add_partition(spark, "smoke_db", "idempotent_p", ordered)
        _partitions.verify_registered(spark, "smoke_db", "idempotent_p", ordered)

    def test_validate_partitions_rejects_keys_mismatch(self, spark):
        df = _make_df(spark, [{"id": 1, "dt": "x", "region": "y"}])
        # Seed the table so the mismatch check exercises the existing-DDL path.
        write_table(df, "smoke_db", "mismatch_p",
                    partitions={"dt": "x", "region": "y"})

        with pytest.raises(ValueError, match="partition keys mismatch"):
            write_table(df, "smoke_db", "mismatch_p",
                        partitions={"dt": "x"})  # missing region


from cidp.spark import _parse_s3a_uri


class TestParseS3aUri:
    def test_s3a_with_key(self):
        assert _parse_s3a_uri("s3a://bucket/db/tbl/") == ("bucket", "db/tbl/")

    def test_s3a_without_trailing_slash(self):
        assert _parse_s3a_uri("s3a://bucket/db/tbl") == ("bucket", "db/tbl/")

    def test_s3_scheme(self):
        assert _parse_s3a_uri("s3://b/k/") == ("b", "k/")

    def test_bucket_only(self):
        assert _parse_s3a_uri("s3a://bucket") == ("bucket", "/")

    def test_rejects_hdfs(self):
        import pytest
        with pytest.raises(ValueError, match="unsupported location scheme"):
            _parse_s3a_uri("hdfs://nn/path")

    def test_rejects_local(self):
        import pytest
        with pytest.raises(ValueError, match="unsupported location scheme"):
            _parse_s3a_uri("/tmp/path")


class TestGetOrCreateSpark:
    def test_returns_passed_arg(self):
        from cidp.spark import _get_or_create_spark
        sentinel = object()
        assert _get_or_create_spark(sentinel) is sentinel

    def test_returns_active_session_when_present(self, spark):
        from cidp.spark import _get_or_create_spark
        # The `spark` fixture sets an active SparkSession for this module.
        assert _get_or_create_spark(None) is spark

    def test_builds_new_when_no_active(self, monkeypatch):
        from cidp.spark import _get_or_create_spark
        from cidp import spark as spark_mod

        monkeypatch.setattr(
            spark_mod.SparkSession, "getActiveSession", staticmethod(lambda: None)
        )

        built = object()

        class FakeBuilder:
            def __init__(self):
                pass
            def getOrCreate(self):
                return built

        monkeypatch.setattr(spark_mod, "SparkSessionBuilder", FakeBuilder)

        assert _get_or_create_spark(None) is built


from cidp.spark import _get_table_location


class TestGetTableLocation:
    def test_returns_table_location_uri(self, spark, tmp_path):
        loc = f"file://{tmp_path}/explicit_loc_tbl"
        spark.sql("DROP TABLE IF EXISTS smoke_db.explicit_loc_tbl")
        spark.sql(
            "CREATE TABLE smoke_db.explicit_loc_tbl (id INT) "
            f"USING parquet LOCATION '{loc}'"
        )
        result = _get_table_location(spark, "smoke_db", "explicit_loc_tbl")
        # Spark may strip a trailing slash; compare normalized.
        assert result.rstrip("/") == loc.rstrip("/")

    def test_raises_when_no_location_row(self, spark, monkeypatch):
        import pytest
        from cidp import spark as spark_mod

        class FakeSqlResult:
            def collect(self):
                return []

        class FakeSpark:
            def sql(self, q):
                return FakeSqlResult()

        with pytest.raises(RuntimeError, match="could not find Location"):
            spark_mod._get_table_location(FakeSpark(), "db", "tbl")


from cidp.spark import _get_partition_location


class TestGetPartitionLocation:
    def test_returns_partition_location_uri(self, spark):
        # Seed a partitioned table via write_table (already tested).
        rows = [{"id": 1, "dt": "2026-05-12"}]
        df = spark.createDataFrame(rows)
        write_table(df, "smoke_db", "part_loc_tbl",
                    partitions={"dt": "2026-05-12"})

        ordered = [("dt", "2026-05-12")]
        loc = _get_partition_location(
            spark, "smoke_db", "part_loc_tbl", ordered,
        )
        assert loc.rstrip("/").endswith("dt=2026-05-12")
        # Must be a URI scheme (file:// in this local fixture) or an
        # absolute path Spark returns.
        assert "://" in loc or loc.startswith("/")


from cidp.spark import upload_table


class TestUploadTableSessionResolution:
    def test_uses_passed_spark(self, spark):
        # Smoke: passing spark= still works, no ValueError.
        rows = [{"id": 1, "dt": "2026-05-12"}]
        upload_table(rows, "smoke_db", "upload_sess_tbl",
                     partitions={"dt": "2026-05-12"}, spark=spark)
        n = spark.sql(
            "SELECT count(*) FROM smoke_db.upload_sess_tbl"
        ).collect()[0][0]
        assert n == 1

    def test_falls_back_to_active_session(self, spark):
        # `spark` fixture has an active session; passing spark=None should
        # resolve to it and succeed (was: ValueError before this change).
        rows = [{"id": 2, "dt": "2026-05-12"}]
        upload_table(rows, "smoke_db", "upload_fallback_tbl",
                     partitions={"dt": "2026-05-12"})
        n = spark.sql(
            "SELECT count(*) FROM smoke_db.upload_fallback_tbl"
        ).collect()[0][0]
        assert n == 1


from unittest.mock import MagicMock
from cidp.spark import download_table


class TestDownloadTableMetastorePaths:
    def _mock_s3_client(self, location_prefix):
        """Build a MagicMock s3 client that reports a single object at
        '<prefix>data.parquet' plus the zero-byte directory marker.
        """
        client = MagicMock()
        client.list_objects_v2.return_value = {
            "Contents": [
                {"Key": location_prefix, "Size": 0},
                {"Key": f"{location_prefix}data.parquet", "Size": 100},
            ]
        }
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"Contents": [
                {"Key": location_prefix, "Size": 0},
                {"Key": f"{location_prefix}data.parquet", "Size": 100},
            ]}
        ]
        client.get_paginator.return_value = paginator
        return client

    def test_non_partitioned_uses_metastore_bucket(self, spark, tmp_path,
                                                  monkeypatch):
        # Create a table whose LOCATION points to a custom s3a:// URI in a
        # NON-default bucket. The table has no real data — only the
        # metastore entry matters for path resolution.
        spark.sql("DROP TABLE IF EXISTS smoke_db.dl_meta_tbl")
        spark.sql(
            "CREATE TABLE smoke_db.dl_meta_tbl (id INT) USING parquet "
            "LOCATION 's3a://other-bucket/custom/path/dl_meta_tbl'"
        )

        client = self._mock_s3_client("custom/path/dl_meta_tbl/")
        monkeypatch.setattr("cidp.spark.boto3.client", lambda **kw: client)

        out = tmp_path / "out"
        download_table("smoke_db", "dl_meta_tbl", str(out), spark=spark)

        # Assert the listing/marker check hit the metastore-derived bucket.
        call = client.list_objects_v2.call_args
        assert call.kwargs["Bucket"] == "other-bucket"
        assert call.kwargs["Prefix"] == "custom/path/dl_meta_tbl/"

        # Assert download_file uses the metastore-derived bucket too.
        dlc = client.download_file.call_args
        assert dlc.args[0] == "other-bucket"

    def test_partitioned_uses_partition_location(self, spark, tmp_path,
                                                 monkeypatch):
        # Seed a real partitioned table (uses local filesystem warehouse).
        # Then patch _get_table_location and _get_partition_location to
        # return s3a:// URIs so we can observe the download routing without
        # needing a real S3 backend.
        rows = [{"id": 1, "dt": "2026-05-12"}]
        df = spark.createDataFrame(rows)
        write_table(df, "smoke_db", "dl_part_tbl",
                    partitions={"dt": "2026-05-12"})

        from cidp import spark as spark_mod
        monkeypatch.setattr(
            spark_mod, "_get_table_location",
            lambda s, d, t: "s3a://other-bucket/p/dl_part_tbl",
        )
        monkeypatch.setattr(
            spark_mod, "_get_partition_location",
            lambda s, d, t, ordered:
                "s3a://other-bucket/p/dl_part_tbl/dt=2026-05-12",
        )

        client = self._mock_s3_client("p/dl_part_tbl/dt=2026-05-12/")
        monkeypatch.setattr("cidp.spark.boto3.client", lambda **kw: client)

        out = tmp_path / "out_part"
        download_table("smoke_db", "dl_part_tbl", str(out),
                       partitions={"dt": "2026-05-12"}, spark=spark)

        call = client.list_objects_v2.call_args
        assert call.kwargs["Bucket"] == "other-bucket"
        assert call.kwargs["Prefix"] == "p/dl_part_tbl/dt=2026-05-12/"
