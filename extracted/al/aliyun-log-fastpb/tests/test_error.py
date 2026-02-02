import pytest
import sys
import os

import aliyun_log_fastpb

# Import generated protobuf classes for verification
try:
    from . import logs_pb2
except ImportError:
    import logs_pb2


def test_log_items_not_list():
    """Test error when LogItems is not a list."""
    log_group_dict = {
        "LogItems": "not a list",
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="LogItems must be a list"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_log_tags_not_list():
    """Test error when LogTags is not a list."""
    log_group_dict = {
        "LogItems": [],
        "LogTags": "not a list",
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="LogTags must be a list"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_log_not_dict():
    """Test error when Log item is not a dict."""
    log_group_dict = {
        "LogItems": ["not a dict"],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Log must be a dict"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_log_missing_time():
    """Test error when Log is missing Time field."""
    log_group_dict = {
        "LogItems": [{"Contents": [{"Key": "test", "Value": "data"}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="Log missing 'Time' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_log_missing_contents():
    """Test error when Log is missing Contents field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="Log missing 'Contents' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_contents_not_list():
    """Test error when Contents is not a list."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": "not a list"}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Contents must be a list"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_content_not_dict():
    """Test error when Content item is not a dict."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": ["not a dict"]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Content must be a dict"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_content_missing_key():
    """Test error when Content is missing Key field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Value": "data"}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="LogContent missing 'Key' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_content_missing_value():
    """Test error when Content is missing Value field."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test"}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="LogContent missing 'Value' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_tag_not_dict():
    """Test error when Tag item is not a dict."""
    log_group_dict = {
        "LogItems": [],
        "LogTags": ["not a dict"],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="LogTag must be a dict"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_tag_missing_key():
    """Test error when Tag is missing Key field."""
    log_group_dict = {
        "LogItems": [],
        "LogTags": [{"Value": "data"}],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="LogTag missing 'Key' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_tag_missing_value():
    """Test error when Tag is missing Value field."""
    log_group_dict = {
        "LogItems": [],
        "LogTags": [{"Key": "test"}],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(ValueError, match="LogTag missing 'Value' field"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_time_type():
    """Test error when Time is wrong type."""
    log_group_dict = {
        "LogItems": [{"Time": "not a number", "Contents": []}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Value must be an unsigned integer"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_time_ns_type():
    """Test error when TimeNs is wrong type."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "TimeNs": "not a number", "Contents": []}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Value must be an unsigned integer"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_topic_type():
    """Test error when Topic is wrong type."""
    log_group_dict = {"LogItems": [], "LogTags": [], "Topic": 123, "Source": ""}

    with pytest.raises(TypeError, match="Value must be a string"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_source_type():
    """Test error when Source is wrong type."""
    log_group_dict = {"LogItems": [], "LogTags": [], "Topic": "", "Source": 123}

    with pytest.raises(TypeError, match="Value must be a string"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_content_key_type():
    """Test error when Content Key is wrong type."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": 123, "Value": "data"}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Value must be a string"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_invalid_content_value_type():
    """Test error when Content Value is wrong type."""
    log_group_dict = {
        "LogItems": [{"Time": 1000, "Contents": [{"Key": "test", "Value": 123}]}],
        "LogTags": [],
        "Topic": "",
        "Source": "",
    }

    with pytest.raises(TypeError, match="Value must be a string"):
        aliyun_log_fastpb.serialize_log_group(log_group_dict)


def test_not_dict_input():
    """Test error when input is not a dict."""
    with pytest.raises(Exception):  # Will raise some exception
        aliyun_log_fastpb.serialize_log_group("not a dict")


def test_none_input():
    """Test error when input is None."""
    with pytest.raises(Exception):  # Will raise some exception
        aliyun_log_fastpb.serialize_log_group(None)
