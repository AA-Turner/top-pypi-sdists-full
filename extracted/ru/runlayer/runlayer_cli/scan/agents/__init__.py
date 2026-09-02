"""Static agent-detection engine.

Discovers AI-agent frameworks at rest on the filesystem by combining dependency
manifests with source-code signatures. Deterministic, fully explainable, and
standard-library only so it fits the frozen ``aiwatch`` bundle with no extra
dependencies.

The package is intentionally light at import time (no eager submodule imports)
so it stays cheap to pull into the scan path. Import the concrete modules
(``discover``, ``manifests``, ``registry``, ``detect``, ``report``) directly.
"""
