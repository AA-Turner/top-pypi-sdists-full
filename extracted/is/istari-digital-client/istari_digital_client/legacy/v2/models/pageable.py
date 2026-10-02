"""
Backward compatibility re-export for pagination mixins.

.. deprecated:: 9.0.0
    Importing from istari_digital_client.legacy.v2.models.pageable is deprecated.
    Use istari_digital_client.mixin for Pageable,
    or istari_digital_client.protocol for PageLike.
"""

import warnings

from istari_digital_client.legacy.mixin import Pageable
from istari_digital_client.legacy.protocol import PageLike

warnings.warn(
    "istari_digital_client.v2.models.pageable is deprecated. "
    "Use istari_digital_client.mixin for Pageable "
    "or istari_digital_client.protocol for PageLike.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["Pageable", "PageLike"]
