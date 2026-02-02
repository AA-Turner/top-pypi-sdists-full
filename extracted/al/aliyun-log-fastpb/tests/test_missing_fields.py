"""
Test handling of missing LogItems and LogTags fields.

These fields should be treated as empty arrays when not present.
"""

import pytest
import aliyun_log_fastpb

try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_missing_log_items():
    """Test LogGroup without LogItems field - should default to empty array."""
    log_group_dict = {
        "LogTags": [{"Key": "tag1", "Value": "value1"}],
        "Topic": "test-topic",
        "Source": "test-source",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 0
    assert len(pb_log_group.log_tags) == 1
    assert pb_log_group.topic == "test-topic"
    assert pb_log_group.source == "test-source"


def test_missing_log_tags():
    """Test LogGroup without LogTags field - should default to empty array."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [{"Key": "test", "Value": "data"}],
            }
        ],
        "Topic": "test-topic",
        "Source": "test-source",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 1
    assert len(pb_log_group.log_tags) == 0
    assert pb_log_group.topic == "test-topic"
    assert pb_log_group.source == "test-source"


def test_missing_both_log_items_and_log_tags():
    """Test LogGroup without both LogItems and LogTags fields."""
    log_group_dict = {
        "Topic": "test-topic",
        "Source": "test-source",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 0
    assert len(pb_log_group.log_tags) == 0
    assert pb_log_group.topic == "test-topic"
    assert pb_log_group.source == "test-source"


def test_missing_all_optional_fields():
    """Test LogGroup with only empty dict - should produce minimal valid protobuf."""
    log_group_dict = {}

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 0
    assert len(pb_log_group.log_tags) == 0
    assert not pb_log_group.HasField("topic")
    assert not pb_log_group.HasField("source")


def test_missing_log_items_raw():
    """Test LogGroupRaw without LogItems field."""
    log_group_dict = {
        "LogTags": [{"Key": "tag1", "Value": "value1"}],
        "Topic": "test-topic",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_dict)

    pb_log_group = logs_pb2.LogGroupRaw()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 0
    assert len(pb_log_group.log_tags) == 1


def test_missing_log_tags_raw():
    """Test LogGroupRaw without LogTags field."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 2000,
                "Contents": [{"Key": "binary", "Value": b"data"}],
            }
        ],
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_dict)

    pb_log_group = logs_pb2.LogGroupRaw()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 1
    assert len(pb_log_group.log_tags) == 0


def test_mixed_missing_fields():
    """Test various combinations of missing and present fields."""
    test_cases = [
        {"LogItems": []},
        {"LogTags": []},
        {"Topic": "test"},
        {"Source": "test"},
        {"LogItems": [], "Topic": "test"},
        {"LogTags": [], "Source": "test"},
    ]

    for log_group_dict in test_cases:
        rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

        pb_log_group = logs_pb2.LogGroup()
        pb_log_group.ParseFromString(rust_bytes)

        # Should succeed without errors
        assert pb_log_group is not None
