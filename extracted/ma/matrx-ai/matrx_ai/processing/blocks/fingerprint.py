"""Content-IR envelope fingerprint — canonical implementation in matrx-graph.

The FNV-1a double hash moved to ``matrx_graph.content_ir.fingerprint`` so the
workflow scheduler's envelope producer can share it (matrx-ai depends on
matrx-graph, never the reverse). This module keeps the established matrx-ai
import path; the algorithm, its TS-twin parity contract, and the shared
vector fixtures (``tests/fixtures/fingerprint_vectors.json`` ↔ matrx-frontend
``features/content-ir/__tests__/fingerprint-vectors.json``, enforced by
``tests/test_fingerprint_parity.py``) are documented at the implementation.
"""

from __future__ import annotations

from matrx_graph.content_ir.fingerprint import Fingerprinter, fingerprint_text

__all__ = ["Fingerprinter", "fingerprint_text"]
