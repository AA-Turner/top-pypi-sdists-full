"""HTTP helpers shared by capability implementations.

Builds the SSL context used by capabilities that make outbound HTTP calls, such
as the builtin web tools.
"""

import os
import ssl
from functools import lru_cache

import certifi
import structlog

logger = structlog.get_logger()


@lru_cache(maxsize=1)
def build_ssl_context() -> ssl.SSLContext:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_cert_file = os.getenv("SSL_CERT_FILE")
    ssl_cert_dir = os.getenv("SSL_CERT_DIR")
    if not ssl_cert_file and not ssl_cert_dir:
        return ssl_context

    try:
        ssl_context.load_verify_locations(cafile=ssl_cert_file, capath=ssl_cert_dir)
    except (OSError, ssl.SSLError):
        logger.warning(
            "Failed to load custom SSL certificates",
            ssl_cert_file=ssl_cert_file,
            ssl_cert_dir=ssl_cert_dir,
        )

    return ssl_context
