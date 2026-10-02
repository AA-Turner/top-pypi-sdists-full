"""Readable plaintext remains subject to inspection after container corruption."""

import gzip
import io
import struct
import zipfile
import zlib

import pytest

from probe.sdk.secret_gate import CredentialBlocked, ScanPolicy, inspect_bytes

SECRET = b"password=FabricatedOnlyAuditPassword27!\n"


def broken_gzip(body):
    return gzip.compress(body) + b"\x1f\x8bbroken"


def bad_crc_gzip(body):
    raw = bytearray(gzip.compress(body))
    raw[-8] ^= 1
    return bytes(raw)


def bad_crc_zip(body, compression=zipfile.ZIP_DEFLATED, *, later=None):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=compression) as archive:
        archive.writestr("readable.txt", body)
        if later is not None:
            archive.writestr("later.txt", later)
    raw = bytearray(output.getvalue())
    start = raw.index(b"PK\x01\x02")
    crc = struct.unpack_from("<I", raw, start + 16)[0]
    struct.pack_into("<I", raw, start + 16, crc ^ 1)
    return bytes(raw)


@pytest.mark.parametrize("wrap", [broken_gzip, bad_crc_gzip, bad_crc_zip])
@pytest.mark.parametrize("prefix", [b"", b"ordinary text\n" * 6000], ids=["short", "long"])
def test_recovered_plaintext_secret_blocks_even_after_container_failure(wrap, prefix):
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(wrap(prefix + SECRET)).has_findings


@pytest.mark.parametrize(
    "compression", [zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED, zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA]
)
def test_zip_integrity_failure_does_not_hide_supported_plaintext(compression):
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(bad_crc_zip(SECRET, compression)).has_findings


@pytest.mark.parametrize("wrap", [broken_gzip, bad_crc_gzip, bad_crc_zip])
def test_benign_recovered_content_allows_with_warning(wrap):
    result = inspect_bytes(wrap(b"ordinary harmless notes\n"))
    assert not result.fully_inspected and result.warning_message


def test_zip_recovery_continues_to_later_readable_members():
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(bad_crc_zip(b"ordinary harmless notes\n", later=SECRET)).has_findings


@pytest.mark.parametrize("wrap", [broken_gzip, bad_crc_zip])
def test_recovery_cannot_waive_expansion_limit(wrap):
    with pytest.raises(CredentialBlocked, match="inspection limit"):
        inspect_bytes(wrap(b"a" * 4096), scan_policy=ScanPolicy(max_bytes=512))


def test_zip_recovery_enforces_actual_expansion_despite_false_declared_size():
    raw = bytearray(bad_crc_zip(b"a" * 4096))
    start = raw.index(b"PK\x01\x02")
    struct.pack_into("<I", raw, start + 24, 1)
    with pytest.raises(CredentialBlocked, match="inspection limit"):
        inspect_bytes(bytes(raw), scan_policy=ScanPolicy(max_bytes=512))


def test_zip_false_size_and_matching_prefix_crc_cannot_hide_readable_suffix():
    prefix = b"ordinary harmless notes\n"
    raw = bytearray(bad_crc_zip(prefix + SECRET))
    crc = zlib.crc32(prefix)
    local = raw.index(b"PK\x03\x04")
    central = raw.index(b"PK\x01\x02")
    struct.pack_into("<I", raw, local + 14, crc)
    struct.pack_into("<I", raw, local + 22, len(prefix))
    struct.pack_into("<I", raw, central + 16, crc)
    struct.pack_into("<I", raw, central + 24, len(prefix))
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(bytes(raw)).has_findings


@pytest.mark.parametrize("wrap", [broken_gzip, bad_crc_zip])
def test_recovered_plaintext_scanner_exception_still_blocks(monkeypatch, wrap):
    from probe.sdk import secret_gate

    scan = secret_gate.scan

    def fail_on_plaintext(text):
        if text == "ordinary harmless notes\n":
            raise RuntimeError("synthetic scanner failure")
        return scan(text)

    monkeypatch.setattr(secret_gate, "scan", fail_on_plaintext)
    with pytest.raises(CredentialBlocked, match="inspection failed"):
        inspect_bytes(wrap(b"ordinary harmless notes\n"))
