"""Content-IR envelope fingerprint — byte-exact parity with the TypeScript twin.

This is the idempotence key for ``metadata.__ir`` envelopes: the frontend only
reuses a server-built ``CanonicalBlockIR`` when this fingerprint of the block's
exact ``render_block.content`` string matches its own — any divergence silently
degrades to a client re-parse (matrx-frontend
``/Users/armanisadeghi/code/common-docs/systems/architecture/content-ir/FEATURE.md``). Algorithm: two
independent FNV-1a 32-bit passes (seeds ``0x811c9dc5`` / ``0x01000193``, prime
``16777619``) over the string's UTF-16 code units — JS ``charCodeAt`` semantics,
so astral chars hash as TWO surrogate units and lone surrogates are legal input
— formatted ``"{length}-{a}{b}"`` in lowercase base-36, where ``length`` is the
UTF-16 code-unit count. TS twin: matrx-frontend
``features/content-ir/core/fingerprint.ts``. Shared vectors (must stay
byte-identical with the frontend copy): matrx-ai
``tests/fixtures/fingerprint_vectors.json`` ↔ matrx-frontend
``features/content-ir/__tests__/fingerprint-vectors.json`` (parity test:
matrx-ai ``tests/test_fingerprint_parity.py``). Never change this module
without regenerating BOTH vector twins from the TS implementation.

Canonical home is matrx-graph (this file) so BOTH Python envelope producers —
the chat-side ``matrx_ai.processing.blocks.envelope`` and the workflow-side
``matrx_graph.content_ir.envelope`` — share one implementation; matrx-ai
re-exports it under its historical import path.
"""

from __future__ import annotations

import asyncio
import sys
from array import array

_SEED_A: int = 0x811C9DC5
_SEED_B: int = 0x01000193
_FNV_PRIME: int = 16777619
_MASK32: int = 0xFFFFFFFF
_BASE36_DIGITS: str = "0123456789abcdefghijklmnopqrstuvwxyz"


def _to_base36(value: int) -> str:
    """Lowercase base-36, matching JS ``Number.prototype.toString(36)``."""
    if value == 0:
        return "0"
    digits: list[str] = []
    while value:
        value, rem = divmod(value, 36)
        digits.append(_BASE36_DIGITS[rem])
    return "".join(reversed(digits))


def _code_units(chunk: str) -> array[int]:
    """The string's UTF-16 code units (JS ``charCodeAt`` semantics) as unsigned shorts.

    surrogatepass: JS strings legally hold lone surrogates (e.g. from slicing a
    pair); a strict encode would raise where JS hashes fine."""
    units = array("H")
    units.frombytes(chunk.encode("utf-16-le", "surrogatepass"))
    if sys.byteorder == "big":
        units.byteswap()
    return units


def _fnv1a_both(a: int, b: int, units: array[int]) -> tuple[int, int]:
    """Both FNV-1a 32-bit passes in ONE loop over the code units, mod 2**32.

    One loop instead of two, over machine shorts instead of byte pairs: the same
    numbers ~2x faster. Still pure Python — a large value is hashed off the event
    loop by the caller (``fingerprint_text_off_loop``)."""
    prime = _FNV_PRIME
    mask = _MASK32
    for u in units:
        a = ((a ^ u) * prime) & mask
        b = ((b ^ u) * prime) & mask
    return a, b


class Fingerprinter:
    """Incremental form: pushing chunks equals one-shot over the concatenation.

    Chunk boundaries may split surrogate pairs — hashing is strictly per
    UTF-16 code unit, so the result is boundary-independent, exactly like the
    TS ``createFingerprinter``.
    """

    __slots__ = ("_a", "_b", "_length")

    def __init__(self) -> None:
        self._a: int = _SEED_A
        self._b: int = _SEED_B
        self._length: int = 0

    def push(self, chunk: str) -> None:
        units = _code_units(chunk)
        self._a, self._b = _fnv1a_both(self._a, self._b, units)
        self._length += len(units)

    def current(self) -> str:
        """Fingerprint of everything pushed so far."""
        return f"{_to_base36(self._length)}-{_to_base36(self._a)}{_to_base36(self._b)}"


def fingerprint_text(source: str) -> str:
    """Fingerprint a complete region source string (TS ``fingerprintText``)."""
    hasher = Fingerprinter()
    hasher.push(source)
    return hasher.current()


# Above this many UTF-16 code units a fingerprint is computed in a worker thread:
# ~0.25 s per million units on a laptop, several times that on a busy server, and on
# the event loop it froze every other run (458 s of stalls in 7 days, PF-WF 2026-11-02).
# A performance line, not a behaviour: the result is identical either way.
OFF_LOOP_MIN_UNITS: int = 64 * 1024


async def fingerprint_text_off_loop(source: str) -> str:
    """``fingerprint_text`` that never holds the event loop for a large string.

    Byte-identical to ``fingerprint_text``; a string over ``OFF_LOOP_MIN_UNITS`` is hashed
    in a worker thread (the loop gets the GIL every switch interval, so other runs keep
    moving). ``len(source)`` under-counts astral characters, which only moves the line."""
    if len(source) < OFF_LOOP_MIN_UNITS:
        return fingerprint_text(source)
    return await asyncio.to_thread(fingerprint_text, source)
