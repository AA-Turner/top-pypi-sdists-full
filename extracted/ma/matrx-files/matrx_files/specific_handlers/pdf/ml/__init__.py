"""Pluggable layout providers — Docling, MinerU, PaddleOCR (Phase 7).

Each provider implements the ``LayoutProvider`` Protocol so the host can
inject its preferred backend at startup via ``register_layout_provider``.
"""
