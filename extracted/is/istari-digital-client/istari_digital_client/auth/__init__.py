"""
Backward compatibility shim for istari_digital_client.auth.

The canonical auth package lives in istari_digital_client.legacy.auth.
This module provides backward compatibility for imports like:
    from istari_digital_client.auth import exchange_pat
    from istari_digital_client.auth.identity_service import validate_credentials_file
"""

import sys

# Import the actual auth package from old location
from istari_digital_client.legacy import auth as _auth

# Re-export everything from old.auth
from istari_digital_client.legacy.auth import *

# Set up module aliases so submodule imports work
# e.g., from istari_digital_client.auth.identity_service import RetryPolicy
sys.modules["istari_digital_client.auth.identity_service"] = sys.modules[
    "istari_digital_client.legacy.auth.identity_service"
]
sys.modules["istari_digital_client.auth.key_exchange"] = sys.modules[
    "istari_digital_client.legacy.auth.key_exchange"
]
sys.modules["istari_digital_client.auth.key_registration"] = sys.modules[
    "istari_digital_client.legacy.auth.key_registration"
]
sys.modules["istari_digital_client.auth.keys"] = sys.modules[
    "istari_digital_client.legacy.auth.keys"
]

# Import submodules to make them accessible as attributes
from istari_digital_client.legacy.auth import (  # noqa: F401
    identity_service,
    key_exchange,
    key_registration,
    keys,
)

__all__ = list(getattr(_auth, "__all__", []))
