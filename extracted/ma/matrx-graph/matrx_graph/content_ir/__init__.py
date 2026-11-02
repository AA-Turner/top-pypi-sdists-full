"""Content IR primitives shared by every Python envelope producer.

The engine-side home of the pure, dependency-free pieces of the Content IR
envelope contract (matrx-frontend
``/Users/armanisadeghi/code/common-docs/systems/architecture/content-ir/FEATURE.md``):

- ``fingerprint`` — the FNV-1a double hash (TS-twin parity, vector-pinned).
- ``envelope`` — canonical ``CanonicalBlockIR`` assembly for the workflow
  scheduler's verified node outputs, plus the
  shared wire constants (``IR_VERSION`` / ``IR_ENVELOPE_KEY`` / ``KIND_KEY``).

matrx-ai's chat-side producer (``matrx_ai.processing.blocks.envelope``,
engine ``py-block-detector``) consumes these same primitives — matrx-ai
depends on matrx-graph, never the reverse.
"""
