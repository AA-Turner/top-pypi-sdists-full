import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_empty_log_group():
    """Test empty LogGroup."""
    log_group_dict = {"LogItems": [], "LogTags": [], "Topic": "", "Source": ""}

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 0
    assert len(pb_log_group.log_tags) == 0


def test_empty_contents():
    """Test Log with empty Contents list."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": []}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs) == 1
    assert len(pb_log_group.logs[0].contents) == 0


def test_empty_tags():
    """Test LogGroup with empty LogTags list."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [],
        "Topic": "test",
        "Source": "test",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.log_tags) == 0


def test_missing_optional_topic():
    """Test LogGroup without Topic field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [],
        "Source": "test",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert not pb_log_group.HasField("topic")


def test_missing_optional_source():
    """Test LogGroup without Source field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [],
        "Topic": "test",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert not pb_log_group.HasField("source")


def test_missing_optional_time_ns():
    """Test Log without TimeNs field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert not pb_log_group.logs[0].HasField("time_ns")


def test_empty_string_values():
    """Test with empty string values."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [
                    {"Key": "", "Value": ""},
                    {"Key": "empty_value", "Value": ""},
                    {"Key": "", "Value": "empty_key"},
                ],
            }
        ],
        "LogTags": [
            {"Key": "", "Value": ""},
        ],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.logs[0].contents) == 3
    assert pb_log_group.logs[0].contents[0].key == ""
    assert pb_log_group.logs[0].contents[0].value == ""
