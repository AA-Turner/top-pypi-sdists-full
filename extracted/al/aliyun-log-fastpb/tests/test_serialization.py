"""
Comprehensive tests for aliyun-log-fastpb serialization.

Tests verify correctness by comparing output with Google's protobuf library.
"""

import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_simple_log_group():
    """Test simple LogGroup with one log entry."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1234567890,
                "Contents": [
                    {"Key": "level", "Value": "INFO"},
                    {"Key": "message", "Value": "Hello World"},
                ],
            }
        ],
        "LogTags": [{"Key": "host", "Value": "server1"}],
        "Topic": "test-topic",
        "Source": "test-source",
    }

    # Serialize with Rust
    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    # Verify with protobuf
    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.topic == "test-topic"
    assert pb_log_group.source == "test-source"
    assert len(pb_log_group.logs) == 1
    assert pb_log_group.logs[0].time == 1234567890
    assert len(pb_log_group.logs[0].contents) == 2
    assert pb_log_group.logs[0].contents[0].key == "level"
    assert pb_log_group.logs[0].contents[0].value == "INFO"
    assert len(pb_log_group.log_tags) == 1
    assert pb_log_group.log_tags[0].key == "host"


def test_log_with_time_ns():
    """Test Log with TimeNs field."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1234567890,
                "TimeNs": 123456789,
                "Contents": [{"Key": "key1", "Value": "value1"}],
            }
        ],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.logs[0].time == 1234567890
    assert pb_log_group.logs[0].time_ns == 123456789


def test_multiple_logs():
    """Test LogGroup with multiple log entries."""
    log_group_dict = {
        "LogItems": [
            {"Time": 1000, "Contents": [{"Key": "id", "Value": "1"}]},
            {"Time": 2000, "Contents": [{"Key": "id", "Value": "2"}]},
            {"Time": 3000, "Contents": [{"Key": "id", "Value": "3"}]},
        ],
        "LogTags": [],
        "Topic": "multi-log",
        "Source": "test",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 3
    assert pb_log_group.logs[0].time == 1000
    assert pb_log_group.logs[1].time == 2000
    assert pb_log_group.logs[2].time == 3000


def test_multiple_contents():
    """Test Log with multiple content entries."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [
                    {"Key": "field1", "Value": "value1"},
                    {"Key": "field2", "Value": "value2"},
                    {"Key": "field3", "Value": "value3"},
                    {"Key": "field4", "Value": "value4"},
                    {"Key": "field5", "Value": "value5"},
                ],
            }
        ],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs[0].contents) == 5
    for i in range(5):
        assert pb_log_group.logs[0].contents[i].key == f"field{i+1}"
        assert pb_log_group.logs[0].contents[i].value == f"value{i+1}"


def test_multiple_tags():
    """Test LogGroup with multiple tags."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [
            {"Key": "tag1", "Value": "value1"},
            {"Key": "tag2", "Value": "value2"},
            {"Key": "tag3", "Value": "value3"},
        ],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.log_tags) == 3
    for i in range(3):
        assert pb_log_group.log_tags[i].key == f"tag{i+1}"
        assert pb_log_group.log_tags[i].value == f"value{i+1}"


def test_string_consistency():
    """Verify string values produce consistent results."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1234567890,
                "Contents": [{"Key": "test", "Value": "hello world"}],
            }
        ],
        "LogTags": [{"Key": "env", "Value": "test"}],
        "Topic": "test-topic",
        "Source": "test-source",
    }

    # Serialize with both functions
    log_group_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)
    log_group_raw_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_dict)

    # Parse with protobuf
    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(log_group_bytes)

    pb_log_group_raw = logs_pb2.LogGroupRaw()
    pb_log_group_raw.ParseFromString(log_group_raw_bytes)

    # Verify metadata fields are the same
    assert pb_log_group.topic == pb_log_group_raw.topic
    assert pb_log_group.source == pb_log_group_raw.source
    assert len(pb_log_group.logs) == len(pb_log_group_raw.logs)
    assert len(pb_log_group.log_tags) == len(pb_log_group_raw.log_tags)

    # Verify content values (string vs bytes)
    assert pb_log_group.logs[0].contents[0].value == pb_log_group_raw.logs[0].contents[
        0
    ].value.decode("utf-8")
