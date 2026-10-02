"""Partial inspection permits bytes with a warning, never a readable finding."""

import io
import struct
import zipfile

import pytest

from probe.sdk.secret_gate import CredentialBlocked, ScanPolicy, checked_upload, inspect_bytes


def mixed_archive(*, clear_member=b"ordinary text"):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("encrypted.bin", b"unavailable encrypted payload")
        archive.writestr("visible.txt", clear_member)
    raw = bytearray(output.getvalue())
    # Declare the first member encrypted in both ZIP headers. Its contents are
    # deliberately never decrypted; the second member remains independently readable.
    for signature, offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        start = raw.index(signature) + offset
        flags = struct.unpack_from("<H", raw, start)[0]
        struct.pack_into("<H", raw, start, flags | 1)
    return bytes(raw)


@pytest.mark.parametrize(
    "raw", [b"\xff\x00\x80", b"PK\x03\x04broken", b"\x1f\x8bbroken", mixed_archive()]
)
def test_uninspectable_format_returns_loud_warning_without_changing_bytes(raw):
    result = inspect_bytes(raw)
    assert result is not None
    assert result.fully_inspected is False
    assert result.warnings
    assert "cannot confirm" in result.warning_message.lower()


def test_supported_text_has_no_incomplete_inspection_warning():
    result = inspect_bytes(b"learning_rate=0.003\n")
    assert result is not None and result.fully_inspected is True
    assert result.warning_message is None


def test_frozen_opaque_bytes_are_not_rescanned_on_this_machine(tmp_path):
    """The client no longer inspects binary content: it cannot rewrite it, and
    the server inspects every upload in full and returns its own warning (see
    tests/test_transport_inspection_warnings.py). Frozen bytes pass unchanged."""
    import warnings

    source = tmp_path / "checkpoint.bin"
    raw = b"\xff\x00\x80"
    source.write_bytes(raw)
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with checked_upload(source) as frozen:
            from pathlib import Path

            assert Path(frozen).read_bytes() == raw
    assert source.read_bytes() == raw


@pytest.mark.parametrize(
    "raw",
    [
        b"\xff\x00\x80\npassword=FabricatedPasswordForInspection123!\n",
        mixed_archive(clear_member=b"password=FabricatedPasswordForInspection123!\n"),
        b"PK\x03\x04broken\npassword=FabricatedPasswordForInspection123!\n",
    ],
)
def test_format_uncertainty_does_not_hide_readable_credentials(raw):
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(raw).has_findings


def test_explicit_strict_format_policy_still_refuses_opaque_and_encrypted():
    for raw in (b"\xff\x00\x80", mixed_archive()):
        with pytest.raises(CredentialBlocked):
            inspect_bytes(raw, scan_policy=ScanPolicy(allow_opaque=False))
