import boto3
import pytest
from botocore.stub import Stubber

from cidp import spark as spark_mod


@pytest.fixture
def stub_env(monkeypatch):
    """Wire download_table to a stubbed boto3 S3 client and bypass Spark."""
    monkeypatch.setattr(spark_mod, "_get_or_create_spark",
                        lambda s=None: object())
    monkeypatch.setattr(
        spark_mod, "_get_table_location",
        lambda spark, db, tbl: f"s3a://my-bucket/{db}/{tbl}/",
    )

    s3 = boto3.client("s3", region_name="ap-northeast-2")
    stubber = Stubber(s3)
    monkeypatch.setattr(spark_mod.boto3, "client", lambda **kw: s3)

    downloads = []

    def fake_download_file(bucket, key, dest):
        downloads.append((bucket, key, dest))
        open(dest, "w").close()

    s3.download_file = fake_download_file
    return s3, stubber, downloads


class TestDownloadTableExistenceCheck:
    def test_succeeds_without_directory_marker(self, tmp_path, stub_env):
        """Hadoop S3A's default marker policy is 'delete' — tables written
        by Spark typically have no zero-byte marker at the prefix. The
        existence check must accept these as valid."""
        s3, stubber, downloads = stub_env
        listing = {"Contents": [
            {"Key": "db/tbl/part-00000.parquet", "Size": 100},
        ]}
        stubber.add_response("list_objects_v2", listing,
                             {"Bucket": "my-bucket", "Prefix": "db/tbl/"})
        stubber.add_response("list_objects_v2", listing,
                             {"Bucket": "my-bucket", "Prefix": "db/tbl/"})
        stubber.activate()

        output = tmp_path / "out"
        spark_mod.download_table("db", "tbl", str(output))

        assert downloads == [(
            "my-bucket",
            "db/tbl/part-00000.parquet",
            f"{output}/part-00000.parquet",
        )]

    def test_succeeds_with_marker_and_data(self, tmp_path, stub_env):
        """Legacy data with both marker and parquet files still works."""
        s3, stubber, downloads = stub_env
        listing = {"Contents": [
            {"Key": "db/tbl/", "Size": 0},
            {"Key": "db/tbl/part-00000.parquet", "Size": 100},
        ]}
        stubber.add_response("list_objects_v2", listing,
                             {"Bucket": "my-bucket", "Prefix": "db/tbl/"})
        stubber.add_response("list_objects_v2", listing,
                             {"Bucket": "my-bucket", "Prefix": "db/tbl/"})
        stubber.activate()

        output = tmp_path / "out"
        spark_mod.download_table("db", "tbl", str(output))

        assert downloads == [(
            "my-bucket",
            "db/tbl/part-00000.parquet",
            f"{output}/part-00000.parquet",
        )]

    def test_raises_when_prefix_empty(self, tmp_path, stub_env):
        """An empty listing means the table/partition is missing."""
        s3, stubber, _ = stub_env
        stubber.add_response("list_objects_v2", {},
                             {"Bucket": "my-bucket", "Prefix": "db/tbl/"})
        stubber.activate()

        with pytest.raises(FileNotFoundError, match="not found"):
            spark_mod.download_table("db", "tbl", str(tmp_path / "out"))

    def test_raises_when_only_marker_present(self, tmp_path, stub_env):
        """An 'empty directory' (marker but no data files) still fails."""
        s3, stubber, _ = stub_env
        stubber.add_response(
            "list_objects_v2",
            {"Contents": [{"Key": "db/tbl/", "Size": 0}]},
            {"Bucket": "my-bucket", "Prefix": "db/tbl/"},
        )
        stubber.activate()

        with pytest.raises(FileNotFoundError, match="not found"):
            spark_mod.download_table("db", "tbl", str(tmp_path / "out"))
