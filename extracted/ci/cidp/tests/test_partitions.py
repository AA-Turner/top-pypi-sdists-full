import boto3
import pytest
from botocore.stub import Stubber

from cidp._partitions import (
    discover_order_from_s3,
    format_path,
    format_spec,
    quote_value,
    validate_partitions,
)


class TestValidatePartitions:
    def test_none_is_ok(self):
        validate_partitions(None)

    def test_nonempty_dict_is_ok(self):
        validate_partitions({"dt": "2026-05-12"})

    def test_empty_dict_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_partitions({})

    def test_none_value_raises(self):
        with pytest.raises(ValueError, match="cannot be None"):
            validate_partitions({"dt": None})


class TestQuoteValue:
    def test_str_simple(self):
        assert quote_value("2026-05-12") == "'2026-05-12'"

    def test_str_with_single_quote_is_doubled(self):
        assert quote_value("a'b") == "'a''b'"

    def test_int(self):
        assert quote_value(42) == "42"

    def test_float(self):
        assert quote_value(1.5) == "1.5"

    def test_bool_true(self):
        assert quote_value(True) == "'true'"

    def test_bool_false(self):
        assert quote_value(False) == "'false'"

    def test_none_rejected(self):
        with pytest.raises(ValueError, match="cannot be None"):
            quote_value(None)

    def test_other_type_rejected(self):
        with pytest.raises(ValueError, match="unsupported"):
            quote_value([1, 2, 3])


class TestFormatSpec:
    def test_single(self):
        assert format_spec([("dt", "2026-05-12")]) == "`dt`='2026-05-12'"

    def test_multi(self):
        assert format_spec([("dt", "2026-05-12"), ("region", "KR")]) == \
               "`dt`='2026-05-12', `region`='KR'"

    def test_mixed_types(self):
        assert format_spec([("dt", "2026-05-12"), ("n", 7)]) == \
               "`dt`='2026-05-12', `n`=7"


class TestFormatPath:
    def test_single(self):
        assert format_path([("dt", "2026-05-12")]) == "dt=2026-05-12"

    def test_multi(self):
        assert format_path([("dt", "2026-05-12"), ("region", "KR")]) == \
               "dt=2026-05-12/region=KR"

    def test_int_value(self):
        assert format_path([("year", 2026)]) == "year=2026"


def _make_s3_stub():
    client = boto3.client("s3", region_name="ap-northeast-2")
    return client, Stubber(client)


class TestDiscoverOrderFromS3:
    def test_single_partition(self):
        client, stub = _make_s3_stub()
        stub.add_response(
            "list_objects_v2",
            {"CommonPrefixes": [{"Prefix": "db/tbl/dt=2026-05-12/"}]},
            {"Bucket": "bkt", "Prefix": "db/tbl/", "Delimiter": "/", "MaxKeys": 1},
        )
        with stub:
            order = discover_order_from_s3(client, "bkt", "db", "tbl", {"dt"})
        assert order == ["dt"]

    def test_two_partitions_in_order(self):
        client, stub = _make_s3_stub()
        stub.add_response(
            "list_objects_v2",
            {"CommonPrefixes": [{"Prefix": "db/tbl/dt=2026-05-12/"}]},
            {"Bucket": "bkt", "Prefix": "db/tbl/", "Delimiter": "/", "MaxKeys": 1},
        )
        stub.add_response(
            "list_objects_v2",
            {"CommonPrefixes": [{"Prefix": "db/tbl/dt=2026-05-12/region=KR/"}]},
            {"Bucket": "bkt", "Prefix": "db/tbl/dt=2026-05-12/",
             "Delimiter": "/", "MaxKeys": 1},
        )
        with stub:
            order = discover_order_from_s3(
                client, "bkt", "db", "tbl", {"dt", "region"}
            )
        assert order == ["dt", "region"]

    def test_keys_mismatch_returns_none(self):
        client, stub = _make_s3_stub()
        stub.add_response(
            "list_objects_v2",
            {"CommonPrefixes": [{"Prefix": "db/tbl/dt=2026-05-12/"}]},
            {"Bucket": "bkt", "Prefix": "db/tbl/", "Delimiter": "/", "MaxKeys": 1},
        )
        with stub:
            order = discover_order_from_s3(
                client, "bkt", "db", "tbl", {"region"}
            )
        assert order is None

    def test_no_partition_dirs_returns_none(self):
        client, stub = _make_s3_stub()
        stub.add_response(
            "list_objects_v2",
            {},
            {"Bucket": "bkt", "Prefix": "db/tbl/", "Delimiter": "/", "MaxKeys": 1},
        )
        with stub:
            order = discover_order_from_s3(client, "bkt", "db", "tbl", {"dt"})
        assert order is None

    def test_non_partition_dir_returns_none(self):
        client, stub = _make_s3_stub()
        stub.add_response(
            "list_objects_v2",
            {"CommonPrefixes": [{"Prefix": "db/tbl/_metadata/"}]},
            {"Bucket": "bkt", "Prefix": "db/tbl/", "Delimiter": "/", "MaxKeys": 1},
        )
        with stub:
            order = discover_order_from_s3(client, "bkt", "db", "tbl", {"dt"})
        assert order is None
