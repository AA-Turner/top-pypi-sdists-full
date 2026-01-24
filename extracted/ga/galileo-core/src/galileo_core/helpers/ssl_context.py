from os import environ
from ssl import SSLContext, create_default_context
from typing import Optional, Union
from warnings import warn

from galileo_core.helpers.logger import logger


def get_ssl_context(
    ssl_context: Union[SSLContext, bool] = True, logging_extra: Optional[dict] = None
) -> Union[SSLContext, bool]:
    """
    Parse an SSL context.

    We allow for the SSL context to be set in a few different ways:
    1. If the user provides an SSLContext object, we use that.
    2. If the user provides `False`, we disable SSL.
    3. If the user provides `True`, we create a default SSL context.
    4. If the user sets `SSL_CERT_FILE` or `SSL_CERT_DIR`, we use those to create a custom SSL context.

    Inspiration: https://www.python-httpx.org/advanced/ssl/#client-side-certificates
    """
    ssl_cert_file = environ.get("SSL_CERT_FILE")
    ssl_cert_dir = environ.get("SSL_CERT_DIR")
    if ssl_context is False:
        warn("SSL is disabled. This is not recommended for production use.", category=UserWarning)
        logger.debug("SSL validation is disabled.", extra=logging_extra)
    elif ssl_cert_file or ssl_cert_dir:
        logger.debug(
            f"SSL context is set to custom cert file ({ssl_cert_file}) or directory ({ssl_cert_dir}).",
            extra=logging_extra,
        )
        ssl_context = create_default_context(cafile=ssl_cert_file, capath=ssl_cert_dir)
    else:
        logger.debug("SSL context is set to the default context.", extra=logging_extra)
        ssl_context = True
    return ssl_context
