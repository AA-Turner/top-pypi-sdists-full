"""Credential store failures."""

from __future__ import annotations


class CredentialStoreError(Exception):
    """The secure backend is unavailable or refused an operation."""
