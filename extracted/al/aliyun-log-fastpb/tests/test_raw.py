import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_simple_log_group_raw():
    """Test LogGroupRaw with string values."""
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

    rust_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_dict)

    pb_log_group = logs_pb2.LogGroupRaw()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.topic == "test-topic"
    assert pb_log_group.source == "test-source"
    assert len(pb_log_group.logs) == 1
    assert pb_log_group.logs[0].time == 1234567890


def test_log_group_raw_with_bytes():
    """Test LogGroupRaw with actual binary data."""
    binary_data = b"\x00\x01\x02\xff\xfe\xfd"
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [{"Key": "binary_field", "Value": binary_data}],
            }
        ],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group_raw(log_group_dict)

    pb_log_group = logs_pb2.LogGroupRaw()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.logs[0].contents[0].key == "binary_field"
    assert pb_log_group.logs[0].contents[0].value == binary_data
