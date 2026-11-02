"""Pluggable cloud OCR providers — Mistral, Azure Read, AWS Textract, Google Document AI (Phase 7).

Each provider implements the ``OcrProvider`` Protocol so the host can register
its preferred backend at startup via ``register_ocr_provider``.
"""
