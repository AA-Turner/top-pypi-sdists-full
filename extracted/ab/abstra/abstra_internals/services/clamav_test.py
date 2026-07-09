from pathlib import Path
from unittest import mock

from abstra_internals.services.clamav import (
    MAX_SCAN_BYTES,
    ClamAVScanner,
    ScanEngine,
    ScanVerdict,
)

EICAR = rb"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
PE_EXECUTABLE = b"MZ\x90\x00\x03\x00\x00\x00more-bytes-here"
CLEAN_PDF = b"%PDF-1.4\n%clean content here"


def _scanner(enabled=True):
    return ClamAVScanner(host="clamd.test", port=3310, enabled=enabled)


class TestScanDisabled:
    def test_disabled_skips_without_touching_clamd(self):
        s = _scanner(enabled=False)
        with mock.patch.object(s, "_clamd_instream") as m:
            result = s.scan_bytes(PE_EXECUTABLE, filename="x.exe")
        m.assert_not_called()
        assert result.verdict is ScanVerdict.SKIPPED
        assert result.engine is ScanEngine.NONE
        assert not result.is_infected

    def test_empty_data_skips(self):
        result = _scanner().scan_bytes(b"", filename="empty.bin")
        assert result.verdict is ScanVerdict.SKIPPED


class TestClamdPath:
    def test_clean_verdict(self):
        s = _scanner()
        with mock.patch.object(s, "_clamd_instream", return_value=(False, None)):
            result = s.scan_bytes(CLEAN_PDF, filename="invoice.pdf")
        assert result.verdict is ScanVerdict.CLEAN
        assert result.engine is ScanEngine.CLAMD
        assert not result.is_infected

    def test_infected_verdict_carries_signature_and_message(self):
        s = _scanner()
        with mock.patch.object(
            s, "_clamd_instream", return_value=(True, "Eicar-Test-Signature")
        ):
            result = s.scan_bytes(EICAR, filename="invoice.pdf")
        assert result.is_infected
        assert result.engine is ScanEngine.CLAMD
        assert result.signature == "Eicar-Test-Signature"
        assert result.message is not None
        assert "invoice.pdf" in result.message
        assert "Eicar-Test-Signature" in result.message


class TestFailOpenFallback:
    def test_clamd_unreachable_clean_file_allowed(self):
        s = _scanner()
        with mock.patch.object(
            s, "_clamd_instream", side_effect=ConnectionError("refused")
        ):
            result = s.scan_bytes(CLEAN_PDF, filename="invoice.pdf")
        # fail-open: clean file allowed, but via the degraded magic-byte engine
        assert result.verdict is ScanVerdict.CLEAN
        assert result.engine is ScanEngine.HEURISTIC

    def test_clamd_unreachable_executable_still_blocked(self):
        s = _scanner()
        with mock.patch.object(
            s, "_clamd_instream", side_effect=TimeoutError("timed out")
        ):
            result = s.scan_bytes(PE_EXECUTABLE, filename="invoice.pdf")
        # even with clamd down, a renamed executable is caught by magic-byte
        assert result.is_infected
        assert result.engine is ScanEngine.HEURISTIC
        assert result.signature == "HEURISTIC.Executable"

    def test_oversized_payload_uses_magic_byte_only(self):
        s = _scanner()
        big_clean = b"%PDF-1.4" + b"\x00" * (MAX_SCAN_BYTES + 1)
        with mock.patch.object(s, "_clamd_instream") as m:
            result = s.scan_bytes(big_clean, filename="huge.pdf")
        m.assert_not_called()  # never streamed to clamd
        assert result.verdict is ScanVerdict.CLEAN
        assert result.engine is ScanEngine.HEURISTIC

    def test_oversized_executable_blocked_without_clamd(self):
        s = _scanner()
        big_exe = PE_EXECUTABLE + b"\x00" * (MAX_SCAN_BYTES + 1)
        with mock.patch.object(s, "_clamd_instream") as m:
            result = s.scan_bytes(big_exe, filename="huge.bin")
        m.assert_not_called()
        assert result.is_infected
        assert result.engine is ScanEngine.HEURISTIC


class TestMagicByteSignatures:
    def test_elf_blocked(self):
        s = _scanner()
        with mock.patch.object(s, "_clamd_instream", side_effect=ConnectionError()):
            result = s.scan_bytes(b"\x7fELFrest", filename="x.bin")
        assert result.is_infected

    def test_shebang_blocked(self):
        s = _scanner()
        with mock.patch.object(s, "_clamd_instream", side_effect=ConnectionError()):
            result = s.scan_bytes(b"#!/bin/sh\nrm -rf /", filename="x.txt")
        assert result.is_infected


class TestScanFile:
    def test_scan_file_reads_and_scans(self, tmp_path: Path):
        f = tmp_path / "invoice.pdf"
        f.write_bytes(EICAR)
        s = _scanner()
        with mock.patch.object(
            s, "_clamd_instream", return_value=(True, "Eicar-Test-Signature")
        ):
            result = s.scan_file(f)
        assert result.is_infected
        assert result.signature == "Eicar-Test-Signature"

    def test_disabled_scan_file_never_reads(self, tmp_path: Path):
        f = tmp_path / "invoice.pdf"
        f.write_bytes(EICAR)
        s = _scanner(enabled=False)
        with mock.patch.object(Path, "read_bytes") as read:
            result = s.scan_file(f)
        read.assert_not_called()
        assert result.verdict is ScanVerdict.SKIPPED
        assert result.engine is ScanEngine.NONE

    def test_oversized_file_reads_head_only_not_whole_file(self, tmp_path: Path):
        # Regression: a large download must not be pulled whole into RAM. The
        # oversized branch stats the file and reads only the head, never read_bytes.
        f = tmp_path / "huge.bin"
        f.write_bytes(PE_EXECUTABLE + b"\x00" * (MAX_SCAN_BYTES + 1))
        s = _scanner()
        with (
            mock.patch.object(Path, "read_bytes") as read,
            mock.patch.object(s, "_clamd_instream") as clamd,
        ):
            result = s.scan_file(f)
        read.assert_not_called()  # whole file never loaded
        clamd.assert_not_called()  # too big to stream to clamd
        assert result.is_infected  # caught by head-only suspicious-byte check
        assert result.engine is ScanEngine.HEURISTIC

    def test_oversized_clean_file_allowed_via_head_check(self, tmp_path: Path):
        f = tmp_path / "huge.pdf"
        f.write_bytes(b"%PDF-1.4" + b"\x00" * (MAX_SCAN_BYTES + 1))
        s = _scanner()
        result = s.scan_file(f)
        assert result.verdict is ScanVerdict.CLEAN
        assert result.engine is ScanEngine.HEURISTIC

    def test_read_error_fails_open_as_skipped(self, tmp_path: Path):
        f = tmp_path / "invoice.pdf"
        f.write_bytes(CLEAN_PDF)
        s = _scanner()
        with mock.patch.object(Path, "read_bytes", side_effect=MemoryError("boom")):
            result = s.scan_file(f)
        # a read failure must never escape into the download flow
        assert result.verdict is ScanVerdict.SKIPPED
        assert result.engine is ScanEngine.NONE

    def test_missing_file_fails_open_as_skipped(self, tmp_path: Path):
        s = _scanner()
        result = s.scan_file(tmp_path / "does-not-exist.pdf")
        assert result.verdict is ScanVerdict.SKIPPED
        assert result.engine is ScanEngine.NONE
