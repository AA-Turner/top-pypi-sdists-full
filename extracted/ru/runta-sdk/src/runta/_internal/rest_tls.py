"""Certifi-backed TLS resumption for async REST connections."""

import ssl

import certifi

from .tls_resumption import _TLSResumption


class _RestTLS(_TLSResumption):
    def __init__(self) -> None:
        super().__init__(lambda: ssl.create_default_context(cafile=certifi.where()))
