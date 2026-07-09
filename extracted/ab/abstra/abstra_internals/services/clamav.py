import enum
import socket
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

from abstra_internals import environment
from abstra_internals.logger import AbstraLogger

MAX_SCAN_BYTES: int = 100 * 1024 * 1024
CLAMD_CONNECT_TIMEOUT_SECONDS: float = 10
SCAN_TIMEOUT_SECONDS: float = 90
STREAM_CHUNK_BYTES: int = 64 * 1024
SUSPICIOUS_HEAD_BYTES: int = 8
SUSPICIOUS_BYTES: Tuple[bytes, ...] = (
    b"MZ",  # DOS/PE executable (.exe, .dll, .scr)
    b"\x7fELF",  # Linux/Unix ELF binary
    b"\xfe\xed\xfa\xce",  # Mach-O 32-bit
    b"\xfe\xed\xfa\xcf",  # Mach-O 64-bit
    b"\xcf\xfa\xed\xfe",  # Mach-O 64-bit little-endian
    b"\xca\xfe\xba\xbe",  # Mach-O universal binary / Java .class
    b"#!",  # shebang script (#!/bin/sh, #!/usr/bin/env python, ...)
)


class ScanVerdict(enum.Enum):
    """Outcome of a scan."""

    CLEAN = "clean"
    INFECTED = "infected"
    SKIPPED = "skipped"


class ScanEngine(enum.Enum):
    """Which check produced the verdict."""

    NONE = "none"
    CLAMD = "clamd"
    HEURISTIC = "heuristic"


@dataclass(frozen=True)
class ScanResult:
    verdict: ScanVerdict
    engine: ScanEngine
    signature: Optional[str] = None
    message: Optional[str] = None

    @property
    def is_infected(self) -> bool:
        return self.verdict is ScanVerdict.INFECTED


class ClamAVScanner:
    """Streams bytes to clamd and returns a :class:`ScanResult`.

    Stateless aside from connection config; safe to share a single instance
    (the underlying clamd client opens a fresh connection per scan).
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        enabled: Optional[bool] = None,
    ):
        self.host = host if host is not None else environment.CLAMD_HOST
        self.port = port if port is not None else environment.CLAMD_PORT
        self.enabled = environment.CLAMAV_SCAN_ENABLED if enabled is None else enabled

    def scan_bytes(self, data: bytes, *, filename: str) -> ScanResult:
        """Scan in-memory ``data`` and return a :class:`ScanResult`.

        Returns ``SKIPPED`` when disabled or empty. Falls back to a suspicious-byte
        check on any clamd failure or an oversized payload.
        """
        if not self.enabled:
            return ScanResult(ScanVerdict.SKIPPED, ScanEngine.NONE)
        if not data:
            return ScanResult(ScanVerdict.SKIPPED, ScanEngine.NONE)
        if len(data) > MAX_SCAN_BYTES:
            AbstraLogger.warning(
                "clamav: payload too large for clamd; suspicious-byte check only",
                {"filename": filename, "size": len(data), "limit": MAX_SCAN_BYTES},
            )
            return self._suspicious_byte_check(data, filename)

        try:
            found, signature = self._clamd_instream(data)
        except Exception as e:  # connection refused, timeout, protocol error, ...
            AbstraLogger.warning(
                "clamav: scan failed; falling back to suspicious-byte check",
                {"filename": filename, "error": str(e)},
            )
            return self._suspicious_byte_check(data, filename)

        if found:
            AbstraLogger.warning(
                "clamav: file flagged; blocking",
                {"filename": filename, "signature": signature},
            )
            return ScanResult(
                ScanVerdict.INFECTED,
                ScanEngine.CLAMD,
                signature=signature,
                message=(
                    f"Download blocked: '{filename}' was flagged as malicious "
                    f"({signature}). The file was not saved."
                ),
            )
        return ScanResult(ScanVerdict.CLEAN, ScanEngine.CLAMD)

    def scan_file(self, path: Union[str, Path]) -> ScanResult:
        """Scan a file already written to disk"""
        p = Path(path)
        if not self.enabled:
            return ScanResult(ScanVerdict.SKIPPED, ScanEngine.NONE)
        try:
            size = p.stat().st_size
            if size > MAX_SCAN_BYTES:
                AbstraLogger.warning(
                    "clamav: file too large for clamd; suspicious-byte check only",
                    {"filename": p.name, "size": size, "limit": MAX_SCAN_BYTES},
                )
                with p.open("rb") as f:
                    head = f.read(SUSPICIOUS_HEAD_BYTES)
                return self._suspicious_byte_check(head, p.name)
            data = p.read_bytes()
        except Exception as e:
            AbstraLogger.warning(
                "clamav: could not read file for scanning; skipping",
                {"filename": p.name, "error": str(e)},
            )
            return ScanResult(ScanVerdict.SKIPPED, ScanEngine.NONE)
        return self.scan_bytes(data, filename=p.name)

    def _clamd_instream(self, data: bytes) -> Tuple[bool, Optional[str]]:
        """Return ``(found, signature)`` from a clamd ``INSTREAM`` scan.

        Speaks the clamd wire protocol directly over a stdlib socket (no
        third-party client): send ``zINSTREAM\\0``, then the payload as
        length-prefixed chunks, then a zero-length terminator; read the
        null-terminated reply. Raises on connection/timeout/protocol errors so
        :meth:`scan_bytes` can fall back to the suspicious-byte check.
        """
        with socket.create_connection(
            (self.host, self.port), timeout=CLAMD_CONNECT_TIMEOUT_SECONDS
        ) as sock:
            sock.settimeout(SCAN_TIMEOUT_SECONDS)
            sock.sendall(b"zINSTREAM\0")
            view = memoryview(data)
            for start in range(0, len(data), STREAM_CHUNK_BYTES):
                chunk = view[start : start + STREAM_CHUNK_BYTES]
                sock.sendall(struct.pack("!L", len(chunk)) + chunk)
            sock.sendall(struct.pack("!L", 0))  # zero-length chunk = end of stream

            reply = b""
            while b"\0" not in reply:
                part = sock.recv(4096)
                if not part:
                    break
                reply += part

        # Replies: "stream: OK", "stream: <Signature> FOUND", "stream: <msg> ERROR"
        text = reply.decode("utf-8", "replace").strip().strip("\0").strip()
        if text.endswith("FOUND"):
            signature = text[: -len("FOUND")].split(":", 1)[-1].strip()
            return True, signature
        if text.endswith("OK"):
            return False, None
        raise RuntimeError(f"unexpected clamd reply: {text!r}")

    def _suspicious_byte_check(self, data: bytes, filename: str) -> ScanResult:
        """Block obvious executables/scripts by leading suspicious bytes (fail-open)."""
        head = data[:8]
        for sig in SUSPICIOUS_BYTES:
            if head.startswith(sig):
                AbstraLogger.warning(
                    "clamav: matched executable signature; blocking",
                    {"filename": filename, "signature": repr(sig)},
                )
                return ScanResult(
                    ScanVerdict.INFECTED,
                    ScanEngine.HEURISTIC,
                    signature="HEURISTIC.Executable",
                    message=(
                        f"Download blocked: '{filename}' appears to be an "
                        "executable, which is not allowed. The file was not saved."
                    ),
                )
        return ScanResult(ScanVerdict.CLEAN, ScanEngine.HEURISTIC)


default_scanner = ClamAVScanner()
