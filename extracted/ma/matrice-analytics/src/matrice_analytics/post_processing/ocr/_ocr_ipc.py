"""Wire protocol shared by the OCR subprocess worker and its client.

The OCR onnxruntime session must run in a separate interpreter on Jetson Thor
because CuPy (parent process) needs ``numpy >= 2`` while ``onnxruntime-gpu``
(the Jetson/NGC wheel) needs ``numpy < 2`` -- the two cannot coexist in one
interpreter. The parent talks to the worker over the worker's stdin/stdout
using the length-prefixed framing defined here.

Design notes:

* Stdlib + numpy only. The worker imports this module by file-path (it lives
  next to ``_ocr_subprocess_worker.py``), so it must NOT pull in any
  ``matrice_analytics`` package machinery.
* Raw image / confidence bytes travel alongside a tiny JSON header rather than
  being JSON/base64 encoded -- this avoids ~33% bloat and keeps the transfer
  numpy-version agnostic (raw IEEE bytes decode identically under numpy 1.x and
  2.x via ``np.frombuffer``).

Frame layout (all integers big-endian)::

    [4 bytes frame-length L][L bytes body]
    body = [1 byte tag][tag-specific bytes]

    tag 'C' (control):  body[1:] = UTF-8 JSON
    tag 'Q' (request):  body[1:] = [4 bytes header-len HL][HL bytes JSON][raw payload]
    tag 'R' (response): body[1:] = [4 bytes header-len HL][HL bytes JSON][raw payload]
"""

from __future__ import annotations

import json
import struct
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence

import numpy as np

# Message tags (single bytes).
TAG_CONTROL = b"C"
TAG_REQUEST = b"Q"
TAG_RESPONSE = b"R"


def normalize_run_result(result):
    """Normalize ``LicensePlateRecognizer.run(return_confidence=True)`` output to
    ``(texts, confs)`` across upstream versions.

    Two upstream return shapes exist and we must support both so a routine
    ``pip install`` of a newer ``fast_plate_ocr`` never breaks OCR again:

    * ``<= 1.0.x`` returns a ``(texts, confs)`` tuple where ``confs`` is an
      ``(N, num_chars)`` ndarray of per-character probabilities.
    * ``>= 1.1.0`` returns ``list[PlatePrediction]`` where each item exposes
      ``.plate`` (str) and ``.char_probs`` (ndarray | None).

    Returns ``(texts: list[str], confs: np.ndarray | None)``. ``confs`` is the
    stacked ``(N, num_chars)`` array when every prediction carries probabilities,
    else ``None``.
    """
    # Old tuple API.
    if isinstance(result, tuple) and len(result) == 2:
        texts, confs = result
        return list(texts), confs
    if isinstance(result, list):
        # New PlatePrediction-list API (duck-typed: avoid importing fast_plate_ocr
        # here so this module stays dependency-light for the worker).
        if result and hasattr(result[0], "plate"):
            texts = [str(getattr(p, "plate", "") or "") for p in result]
            probs = [getattr(p, "char_probs", None) for p in result]
            confs = None
            if probs and all(p is not None for p in probs):
                try:
                    confs = np.stack([np.asarray(p) for p in probs])
                except Exception:
                    confs = None
            return texts, confs
        # Plain list of strings (return_confidence=False).
        return [str(x) for x in result], None
    # Scalar / unknown.
    return [str(result)], None


# Control message types (the ``type`` field of a 'C' frame).
CTRL_READY = "ready"
CTRL_ERROR = "error"
CTRL_PONG = "pong"

_U32 = struct.Struct(">I")


class Frame(NamedTuple):
    """A decoded protocol frame."""

    tag: bytes
    header: Dict[str, Any]
    payload: bytes


# ---------------------------------------------------------------------------
# Low-level framing
# ---------------------------------------------------------------------------
def _frame(body: bytes) -> bytes:
    """Prefix ``body`` with its 4-byte big-endian length."""
    return _U32.pack(len(body)) + body


def read_frame(read_exact: Callable[[int], bytes]) -> Frame:
    """Read and decode one frame using ``read_exact(n) -> bytes``.

    ``read_exact`` must return exactly ``n`` bytes or raise ``EOFError`` /
    ``TimeoutError`` (the worker uses a blocking reader, the client a
    deadline-aware one).
    """
    length = _U32.unpack(read_exact(4))[0]
    body = read_exact(length)
    tag = body[0:1]
    rest = body[1:]
    if tag == TAG_CONTROL:
        return Frame(tag, json.loads(rest.decode("utf-8")), b"")
    if tag in (TAG_REQUEST, TAG_RESPONSE):
        header_len = _U32.unpack(rest[0:4])[0]
        header = json.loads(rest[4 : 4 + header_len].decode("utf-8"))
        return Frame(tag, header, rest[4 + header_len :])
    raise ValueError(f"Unknown OCR IPC frame tag: {tag!r}")


def read_exact_from_stream(stream, n: int) -> bytes:
    """Blocking ``read_exact`` for a binary stream (used by the worker)."""
    buf = bytearray()
    while len(buf) < n:
        chunk = stream.read(n - len(buf))
        if not chunk:
            raise EOFError("OCR IPC stream closed")
        buf += chunk
    return bytes(buf)


def write_frame(stream, frame_bytes: bytes) -> None:
    """Write a packed frame to a binary stream and flush."""
    stream.write(frame_bytes)
    stream.flush()


# ---------------------------------------------------------------------------
# Packers
# ---------------------------------------------------------------------------
def pack_control(obj: Dict[str, Any]) -> bytes:
    return _frame(TAG_CONTROL + json.dumps(obj).encode("utf-8"))


def _pack_with_payload(tag: bytes, header: Dict[str, Any], payload: bytes) -> bytes:
    header_bytes = json.dumps(header).encode("utf-8")
    return _frame(tag + _U32.pack(len(header_bytes)) + header_bytes + payload)


def pack_request(
    request_id: int,
    array: Optional[np.ndarray],
    return_confidence: bool = True,
    op: str = "run",
) -> bytes:
    """Pack a ``run`` (with image) or ``ping`` (no image) request."""
    if op == "run":
        arr = np.ascontiguousarray(array)
        header = {
            "request_id": request_id,
            "op": "run",
            "dtype": arr.dtype.str,
            "shape": list(arr.shape),
            "return_confidence": bool(return_confidence),
        }
        return _pack_with_payload(TAG_REQUEST, header, arr.tobytes())
    return _pack_with_payload(TAG_REQUEST, {"request_id": request_id, "op": op}, b"")


def pack_batch_request(
    request_id: int,
    arrays: "Sequence[np.ndarray]",
    return_confidence: bool = True,
) -> bytes:
    """Pack a ``run_batch`` request: several crops in one round trip.

    Crops from one frame have different shapes, so they cannot be stacked into a
    single array -- ``np.asarray`` on a ragged list raises. Instead each crop is
    made contiguous and its bytes concatenated, with a per-crop shape in the
    header; :func:`decode_request_arrays` slices them back apart. One dtype is
    used for all of them, taken from the first crop, because they come from the
    same decoded frame.

    This exists so the OCR model sees one call for N crops. It does not change
    what the model is given: each crop still arrives as its own array, so
    preprocessing stays inside the recognizer and read quality is unaffected.
    """
    contiguous = [np.ascontiguousarray(a) for a in arrays]
    if not contiguous:
        raise ValueError("pack_batch_request needs at least one array")
    header = {
        "request_id": request_id,
        "op": "run_batch",
        "dtype": contiguous[0].dtype.str,
        "shapes": [list(a.shape) for a in contiguous],
        "return_confidence": bool(return_confidence),
    }
    return _pack_with_payload(TAG_REQUEST, header, b"".join(a.tobytes() for a in contiguous))


def pack_response_ok(request_id: int, texts: list, confs: Optional[np.ndarray]) -> bytes:
    header: Dict[str, Any] = {
        "request_id": request_id,
        "status": "ok",
        "texts": list(texts),
    }
    if confs is None:
        header["confs_shape"] = None
        return _pack_with_payload(TAG_RESPONSE, header, b"")
    confs_arr = np.ascontiguousarray(confs)
    header["confs_dtype"] = confs_arr.dtype.str
    header["confs_shape"] = list(confs_arr.shape)
    return _pack_with_payload(TAG_RESPONSE, header, confs_arr.tobytes())


def pack_response_error(request_id: int, error: str) -> bytes:
    return _pack_with_payload(
        TAG_RESPONSE,
        {"request_id": request_id, "status": "error", "error": str(error)},
        b"",
    )


# ---------------------------------------------------------------------------
# Decoders for the raw payloads
# ---------------------------------------------------------------------------
def decode_request_array(frame: Frame) -> np.ndarray:
    """Reconstruct the image array from a 'run' request frame."""
    return np.frombuffer(frame.payload, dtype=np.dtype(frame.header["dtype"])).reshape(frame.header["shape"])


def decode_request_arrays(frame: Frame) -> "List[np.ndarray]":
    """Reconstruct the crop list from a 'run_batch' request frame.

    The inverse of :func:`pack_batch_request`: walk the per-crop shapes, slicing
    the concatenated payload at each crop's byte length.
    """
    dtype = np.dtype(frame.header["dtype"])
    payload = frame.payload
    arrays: "List[np.ndarray]" = []
    offset = 0
    for shape in frame.header["shapes"]:
        count = 1
        for dim in shape:
            count *= int(dim)
        nbytes = count * dtype.itemsize
        arrays.append(np.frombuffer(payload, dtype=dtype, count=count, offset=offset).reshape(shape))
        offset += nbytes
    if offset != len(payload):
        raise ValueError(f"run_batch payload is {len(payload)} bytes but its shapes describe {offset}")
    return arrays


def decode_response_confs(frame: Frame) -> Optional[np.ndarray]:
    """Reconstruct the confidence array from a response frame (or None)."""
    if frame.header.get("confs_shape") is None:
        return None
    return np.frombuffer(frame.payload, dtype=np.dtype(frame.header["confs_dtype"])).reshape(
        frame.header["confs_shape"]
    )
