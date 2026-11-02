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


def _fnv1a_step(hash_value: int, units: bytes) -> int:
    """One FNV-1a pass over little-endian UTF-16 code units, mod 2**32."""
    h = hash_value
    for i in range(0, len(units), 2):
        h = ((h ^ (units[i] | (units[i + 1] << 8))) * _FNV_PRIME) & _MASK32
    return h


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
        # surrogatepass: JS strings legally hold lone surrogates (e.g. from
        # slicing a pair); a strict encode would raise where JS hashes fine.
        units = chunk.encode("utf-16-le", "surrogatepass")
        self._a = _fnv1a_step(self._a, units)
        self._b = _fnv1a_step(self._b, units)
        self._length += len(units) // 2

    def current(self) -> str:
        """Fingerprint of everything pushed so far."""
        return f"{_to_base36(self._length)}-{_to_base36(self._a)}{_to_base36(self._b)}"


def fingerprint_text(source: str) -> str:
    """Fingerprint a complete region source string (TS ``fingerprintText``)."""
    hasher = Fingerprinter()
    hasher.push(source)
    return hasher.current()
