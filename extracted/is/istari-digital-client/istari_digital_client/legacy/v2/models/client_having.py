"""
Backward compatibility re-export for ClientHaving mixin.

.. deprecated:: 9.0.0
    Importing from istari_digital_client.legacy.v2.models.client_having is deprecated.
    Use istari_digital_client.mixin.ClientHaving instead.
"""

import warnings

from istari_digital_client.legacy.mixin import ClientHaving

warnings.warn(
    "istari_digital_client.v2.models.client_having is deprecated. "
    "Use istari_digital_client.mixin.ClientHaving instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ClientHaving"]
