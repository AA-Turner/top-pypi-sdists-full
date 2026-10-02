"""
Mixins for istari-digital-client models.

This module contains reusable mixins that provide common functionality
across different API versions.
"""

from istari_digital_client.legacy.mixin.client_having import ClientHaving
from istari_digital_client.legacy.mixin.pageable import Pageable
from istari_digital_client.legacy.protocol import PageLike

__all__ = [
    "ClientHaving",
    "Pageable",
    "PageLike",
]
