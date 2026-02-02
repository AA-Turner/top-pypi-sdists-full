import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_many_logs():
    """Test LogGroup with many log entries."""
    num_logs = 1000
    log_items = []
    for i in range(num_logs):
        log_items.append(
            {"Time": 1000 + i, "Contents": [{"Key": f"log_id", "Value": str(i)}]}
        )

    log_group_dict = {
        "LogItems": log_items,
        "LogTags": [],
        "Topic": "large-test",
        "Source": "test",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == num_logs
    assert pb_log_group.logs[0].time == 1000
    assert pb_log_group.logs[-1].time == 1000 + num_logs - 1


def test_many_contents_per_log():
    """Test Log with many content entries."""
    num_contents = 100
    contents = []
    for i in range(num_contents):
        contents.append(
            {"Key": f"field_{i:03d}", "Value": f"value_{i:03d}_" + "x" * 100}
        )

    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": contents}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs[0].contents) == num_contents


def test_many_tags():
    """Test LogGroup with many tags."""
    num_tags = 100
    tags = []
    for i in range(num_tags):
        tags.append({"Key": f"tag_{i:03d}", "Value": f"value_{i:03d}"})

    log_group_dict = {"LogItems": [], "LogTags": tags, "Topic": "", "Source": ""}

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.log_tags) == num_tags


def test_long_strings():
    """Test with very long string values."""
    long_string = "x" * 10000

    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [{"Key": "long_value", "Value": long_string}],
            }
        ],
        "LogTags": [],
        "Topic": long_string,
        "Source": long_string,
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.logs[0].contents[0].value == long_string
    assert pb_log_group.topic == long_string
    assert pb_log_group.source == long_string


def test_realistic_scenario():
    """Test realistic logging scenario with 1000 logs."""
    # 1000 logs, 5 tags, 15 fields per log
    log_items = []
    for i in range(1000):
        contents = []
        for j in range(15):
            key = f"field_{j:02d}"
            value = f"value_{i}_{j}_" + "x" * 42  # Average ~50 chars
            contents.append({"Key": key, "Value": value})

        log_items.append(
            {
                "Time": 1600000000 + i,
                "TimeNs": (i * 1000000) % 1000000000,
                "Contents": contents,
            }
        )

    tags = []
    for i in range(5):
        tags.append({"Key": f"tag_{i}", "Value": f"tag_value_{i}"})

    log_group_dict = {
        "LogItems": log_items,
        "LogTags": tags,
        "Topic": "production",
        "Source": "app-server-001",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 1000
    assert len(pb_log_group.log_tags) == 5
    assert len(pb_log_group.logs[0].contents) == 15
    assert pb_log_group.topic == "production"
