r"""Contain document loaders."""

from __future__ import annotations

__all__ = ["DocumentListLoader", "DocumentStoreLoader", "resolve_document_loader"]

from zenpyre.document_loaders.document_store import DocumentStoreLoader
from zenpyre.document_loaders.resolve import resolve_document_loader
from zenpyre.document_loaders.sequence import DocumentListLoader
