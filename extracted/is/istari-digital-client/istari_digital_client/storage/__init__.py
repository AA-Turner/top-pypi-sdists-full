"""
Backward compatibility shim for istari_digital_client.storage.

The canonical storage package lives in istari_digital_client.legacy.storage.
This module provides backward compatibility for imports like:
    from istari_digital_client.storage.api import StorageApi
"""

import sys

# Import the actual storage package from old location
from istari_digital_client.legacy import storage as _storage

# Re-export everything from old.storage
from istari_digital_client.legacy.storage import *

# Set up module aliases so subpackage imports work
sys.modules["istari_digital_client.storage.api"] = sys.modules[
    "istari_digital_client.legacy.storage.api"
]

# Import subpackages to make them accessible as attributes
from istari_digital_client.legacy.storage import api  # noqa: F401

__all__ = list(getattr(_storage, "__all__", []))
