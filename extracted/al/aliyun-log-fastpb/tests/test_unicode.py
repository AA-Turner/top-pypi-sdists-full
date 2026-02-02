import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_unicode_content():
    """Test Unicode characters in content."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [
                    {"Key": "中文键", "Value": "中文值"},
                    {"Key": "emoji", "Value": "🚀🎉💻"},
                    {"Key": "mixed", "Value": "Hello 世界 🌍"},
                ],
            }
        ],
        "LogTags": [],
        "Topic": "Unicode测试",
        "Source": "テスト",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert pb_log_group.topic == "Unicode测试"
    assert pb_log_group.source == "テスト"
    assert pb_log_group.logs[0].contents[0].key == "中文键"
    assert pb_log_group.logs[0].contents[0].value == "中文值"
    assert pb_log_group.logs[0].contents[1].value == "🚀🎉💻"


def test_unicode_tags():
    """Test Unicode characters in tags."""
    log_group_dict = {
        "LogItems": [],
        "LogTags": [
            {"Key": "地域", "Value": "北京"},
            {"Key": "환경", "Value": "프로덕션"},
            {"Key": "סביבה", "Value": "ייצור"},
        ],
        "Topic": "",
        "Source": "",
    }

    rust_bytes = aliyun_log_fastpb.serialize_log_group(log_group_dict)

    pb_log_group = logs_pb2.LogGroup()
    pb_log_group.ParseFromString(rust_bytes)

    assert len(pb_log_group.log_tags) == 3
    assert pb_log_group.log_tags[0].key == "地域"
    assert pb_log_group.log_tags[0].value == "北京"


def test_special_characters():
    """Test special characters and escapes."""
    log_group_dict = {
        "LogItems": [
            {
                "Time": 1000,
                "Contents": [
                    {"Key": "newline", "Value": "line1\nline2\nline3"},
                    {"Key": "tab", "Value": "col1\tcol2\tcol3"},
                    {"Key": "quote", "Value": 'He said "Hello"'},
                    {"Key": "backslash", "Value": "path\\to\\file"},
                    {"Key": "null", "Value": "null\x00char"},
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

    contents = pb_log_group.logs[0].contents
    assert contents[0].value == "line1\nline2\nline3"
    assert contents[1].value == "col1\tcol2\tcol3"
    assert contents[2].value == 'He said "Hello"'
    assert contents[3].value == "path\\to\\file"
