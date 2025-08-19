"""
compression_handler.py
──────────────────────
Detect wrapper & format from *content* (magic bytes), peek inside wrappers,
and decompress to memory or local temp‑files.

Design notes
------------
* SRP (Single‑responsibility): each helper (_Detector, _Inflater, _S3TempWriter)
  owns one job.
* OCP (Open/Closed): adding a new wrapper means implementing another
  _Inflater subclass – no edits in high‑level code.
* No filename parsing – 100 % content‑based.
"""

from __future__ import annotations

import gzip
import io
import os
import tempfile
import zipfile
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple

import boto3
import snappy

try:
    import zstandard as zstd  # type: ignore
except ImportError:  # pragma: no cover
    zstd = None  # we’ll guard every use with “if zstd is not None”
from mypy_boto3_s3 import S3Client


# ───────────────────────── Enums ──────────────────────────
class FileFormat(Enum):
    JSON = "json"
    CSV = "csv"
    TSV = "tsv"
    PARQUET = "parquet"
    ORC = "orc"
    AVRO = "avro"
    UNKNOWN = "unknown"

    @property
    def extension(self) -> str:
        return f".{self.value}" if self != FileFormat.UNKNOWN else ""

    def __str__(self) -> str:
        return self.extension


class CompressionWrapper(Enum):
    GZ = "gz"
    SNAPPY = "snappy"
    ZIP = "zip"
    ZST = "zst"
    NONE = "none"

    @property
    def extension(self) -> str:
        return f".{self.value}" if self != CompressionWrapper.NONE else ""

    def __str__(self) -> str:
        return self.extension


# ───────────────────────── Value Object ──────────────────────────


class FileTypeMetadata:
    """Immutable description of the (wrapper, format) pair."""

    __slots__ = ("wrapper", "format")

    def __init__(
        self,
        wrapper: CompressionWrapper,
        format: FileFormat,
    ):
        self.wrapper: CompressionWrapper = wrapper
        self.format: FileFormat = format

    # nice for debugging / logging
    def __repr__(self) -> tuple[str, FileTypeMetadata]:  # type: ignore
        return f"FileTypeMetadata(wrapper={self.wrapper}, " f"format={self.format})"  # type: ignore


# ───────────────────────── Detection helpers ──────────────────────────


class _Detector:
    """Pure functions for wrapper / format sniffing."""

    _ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
    _PEEK_LIMIT = 64 * 1024  # 64 KiB

    # ----- wrapper ----------------------------------------------------
    @staticmethod
    def wrapper_of(data: bytes) -> CompressionWrapper:
        if data.startswith(b"\x1f\x8b"):
            return CompressionWrapper.GZ
        if data.startswith(b"PK\x03\x04"):
            return CompressionWrapper.ZIP
        if data.startswith(b"\xff\x06\x00\x00sNaPpY"):
            return CompressionWrapper.SNAPPY
        if data.startswith(_Detector._ZSTD_MAGIC):
            return CompressionWrapper.ZST

        # heuristic snappy probe
        try:
            snappy.decompress(data)
            return CompressionWrapper.SNAPPY
        except Exception:
            return CompressionWrapper.NONE

    # ----- format -----------------------------------------------------
    @staticmethod
    def format_of(data: bytes) -> FileFormat:
        """Detect the (internal) file format from *plain* bytes."""
        if data.startswith(b"PAR1"):
            return FileFormat.PARQUET
        if b"ORC" in data[-16:]:
            return FileFormat.ORC
        if data.startswith(b"Obj"):
            return FileFormat.AVRO
        if data.strip().startswith((b"{", b"[")):
            return FileFormat.JSON
        if b"," in data[:1024]:
            return FileFormat.CSV
        if b"\t" in data[:1024]:
            return FileFormat.TSV
        return FileFormat.UNKNOWN

    # ----- light peek inside wrapper ----------------------------------
    @staticmethod
    def _peek_inner_bytes(wrapper: CompressionWrapper, raw: bytes) -> bytes:  # ≤64 KiB
        if wrapper == CompressionWrapper.GZ:
            try:
                return gzip.GzipFile(fileobj=io.BytesIO(raw)).read(
                    _Detector._PEEK_LIMIT
                )
            except Exception:
                return b""

        if wrapper == CompressionWrapper.SNAPPY:
            # snappy-python has no “max_len”, so decompress then slice
            try:
                import snappy

                return snappy.decompress(raw)[: _Detector._PEEK_LIMIT]  # type: ignore
            except Exception:
                return b""
        if wrapper == CompressionWrapper.ZIP:
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                namelist = zf.namelist()
                if not namelist:
                    return b""
                with zf.open(namelist[0]) as zmem:
                    return zmem.read(_Detector._PEEK_LIMIT)
        if wrapper == CompressionWrapper.ZST and zstd is not None:
            try:
                # Decompress just the first ≤64 KiB so the detector can sniff it
                return zstd.ZstdDecompressor().decompress(
                    raw, max_output_size=_Detector._PEEK_LIMIT
                )
            except Exception:  # corrupted or truncated
                return b""

        # ZST and NONE are not peeked (zstd library optional)
        return b""


# ───────────────────────── Inflaters (Strategy) ──────────────────────────


class _Inflater(ABC):
    """Strategy interface for a compression wrapper."""

    @abstractmethod
    def decompress(self, raw: bytes) -> bytes: ...


class _GzipInflater(_Inflater):
    def decompress(self, raw: bytes) -> bytes:
        return gzip.decompress(raw)


class _SnappyInflater(_Inflater):
    def decompress(self, raw: bytes) -> bytes:
        return snappy.decompress(raw)  # type: ignore


class _ZipInflater(_Inflater):
    def decompress(self, raw: bytes) -> bytes:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            names = zf.namelist()
            if not names:
                raise IndexError("empty archive")
            if len(names) != 1:
                raise zipfile.BadZipFile(
                    "multi‑file archive not supported; got " + ", ".join(names)
                )
            return zf.read(names[0])


class _ZstdInflater(_Inflater):
    def decompress(self, raw: bytes) -> bytes:
        if zstd is None:  # should never happen in tests
            raise RuntimeError("zstandard library not installed")
        return zstd.decompress(raw)  # type: ignore[arg-type]


# Wrapper → strategy lookup
_INFLATERS: dict[CompressionWrapper, _Inflater] = {
    CompressionWrapper.GZ: _GzipInflater(),
    CompressionWrapper.SNAPPY: _SnappyInflater(),
    CompressionWrapper.ZIP: _ZipInflater(),
}

if zstd is not None:  # register only when the library is present
    _INFLATERS[CompressionWrapper.ZST] = _ZstdInflater()
# ───────────────────────── Facade (public API) ──────────────────────────


class CompressionHandler:
    """
    Light‑weight façade around the detector + inflaters.

    ➜ Only *forwards* to helpers so we keep a clean SOLID design **and**
      preserve the historical class‑level API relied on by tests.
    """

    # ---------------- constants expected by tests -----------------
    _ZSTD_MAGIC = _Detector._ZSTD_MAGIC
    SUPPORTED_FILE_TYPES = {f.value for f in FileFormat if f is not FileFormat.UNKNOWN}
    COMPRESSION_EXTENSIONS = {
        w.value for w in CompressionWrapper if w is not CompressionWrapper.NONE
    }

    # ---------------- proxy helpers (names kept for b/c) ----------
    detect_compression_by_magic_bytes = staticmethod(_Detector.wrapper_of)
    detect_format_by_magic_bytes = staticmethod(_Detector.format_of)

    # ---------------- high‑level helpers --------------------------
    @staticmethod
    def get_file_type_metadata(raw_bytes: bytes) -> FileTypeMetadata:
        wrapper = _Detector.wrapper_of(raw_bytes)

        # Small peek inside wrapper (if any) to decide real format
        inner_head = (
            _Detector._peek_inner_bytes(wrapper, raw_bytes)
            if wrapper is not CompressionWrapper.NONE
            else raw_bytes
        )
        fmt = _Detector.format_of(inner_head)

        return FileTypeMetadata(wrapper, fmt)

    # ------------------------------------------------------------------
    @staticmethod
    def decompress(
        raw_bytes: bytes, wrapper: CompressionWrapper
    ) -> Tuple[io.BytesIO, FileFormat]:
        """
        Decompress *raw_bytes* according to *wrapper* (or auto‑detect if
        `wrapper` is `.none`).

        Returns a **memory** buffer + detected internal format.
        """
        # auto‑detect if caller passed “NONE”
        actual_wrapper = (
            _Detector.wrapper_of(raw_bytes)
            if wrapper is CompressionWrapper.NONE
            else wrapper
        )

        if actual_wrapper not in _INFLATERS:
            raise ValueError(f"Unsupported compression wrapper: {wrapper.value}")

        data = _INFLATERS[actual_wrapper].decompress(raw_bytes)
        if not isinstance(data, bytes):
            data = data.encode()  # for snappy < 1.1 returning `str`

        return io.BytesIO(data), _Detector.format_of(data)

    # ------------------------------------------------------------------
    def decompress_s3_file_to_local(  # noqa: C901 – a bit long but straightforward
        self,
        bucket: str,
        key: str,
        *,
        s3_client: Optional[S3Client] = None,
        tmpdir: str | None = None,
        compression_wrapper: Optional[CompressionWrapper] = None,
        file_buff: bytes | None = None,
    ) -> Tuple[str, FileTypeMetadata]:
        """
        Download *bucket/key*, (optionally) decompress, write to tmp‑file,
        return local path.

        Added keyword parameters allow callers that already fetched the bytes
        (schema detection) to skip a second network hop.
        """
        s3 = s3_client or boto3.client("s3")
        raw = (
            file_buff
            if file_buff is not None
            else s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        )

        wrapper_hint = (
            compression_wrapper
            if compression_wrapper is not None
            else _Detector.wrapper_of(raw)
        )

        # Create a safe prefix that preserves the original key path
        # Replace path separators with underscores to make it filesystem-safe
        safe_key = key.replace("/", "_").replace("\\", "_")
        prefix = safe_key

        if wrapper_hint is CompressionWrapper.NONE:
            suffix = os.path.splitext(key)[1] or ".bin"
            with tempfile.NamedTemporaryFile(
                delete=False, prefix=prefix, suffix=suffix, dir=tmpdir
            ) as tmp:
                tmp.write(raw)
                path = tmp.name
            fmt = _Detector.format_of(raw)
            meta = FileTypeMetadata(wrapper_hint, fmt)
            return path, meta

        byte_io, int_fmt = self.decompress(raw, wrapper_hint)
        suffix = int_fmt.extension or ".bin"

        with tempfile.NamedTemporaryFile(
            delete=False, prefix=prefix, suffix=suffix, dir=tmpdir
        ) as tmp:
            tmp.write(byte_io.read())
            path = tmp.name
        meta = FileTypeMetadata(CompressionWrapper.NONE, int_fmt)
        return path, meta
