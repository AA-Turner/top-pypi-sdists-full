r"""Contain validation functions for docculus."""

from __future__ import annotations

__all__ = ["DocumentConsistencyError", "validate_document_consistency"]

from docculus.validation.consistency import (
    DocumentConsistencyError,
    validate_document_consistency,
)
