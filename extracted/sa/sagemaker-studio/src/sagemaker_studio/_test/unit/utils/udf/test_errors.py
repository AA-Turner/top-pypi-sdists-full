"""Unit tests for sagemaker_studio.utils.udf.errors."""

from sagemaker_studio.utils.udf.errors import (
    UDFRegistrationError,
    UDFSidecarError,
    UDFUnsupportedError,
    format_sidecar_error,
)


def test_registration_error_is_a_value_error():
    # Notebook users catch ValueError; keep the POC-compatible base class.
    assert issubclass(UDFRegistrationError, ValueError)


def test_unsupported_error_is_not_implemented_error():
    assert issubclass(UDFUnsupportedError, NotImplementedError)


def test_format_sidecar_error_includes_error_and_remote_traceback():
    resp = {
        "ok": False,
        "error": "ValueError: bad return type",
        "traceback": 'Traceback (most recent call last):\n  File "<udf>", line 1\nValueError: bad return type\n',
    }
    err = format_sidecar_error(resp)
    assert isinstance(err, UDFSidecarError)
    text = str(err)
    assert "ValueError: bad return type" in text
    assert "UDF sidecar" in text
    # The remote traceback is indented under a header so it reads as one block
    # in a notebook cell rather than merging into the local traceback.
    assert "Sidecar traceback:" in text
    assert '    File "<udf>", line 1' in text


def test_format_sidecar_error_without_traceback_still_readable():
    err = format_sidecar_error({"ok": False, "error": "boom"})
    assert "boom" in str(err)
    assert "Sidecar traceback:" not in str(err)
