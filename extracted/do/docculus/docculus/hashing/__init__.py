r"""Contain hashing utilities."""

from __future__ import annotations

__all__ = [
    "DocumentHasher",
    "hash_document",
    "hash_document_to_uuid",
    "hash_documents",
    "register_document_hasher",
]

from docculus.hashing.functions import hash_document, hash_documents
from docculus.hashing.hasher import DocumentHasher, register_document_hasher
from docculus.hashing.uuid import hash_document_to_uuid
