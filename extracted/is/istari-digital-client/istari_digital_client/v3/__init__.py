"""
Backward compatibility shim for istari_digital_client.v3.

The canonical v3 package lives in istari_digital_client.legacy.v3.
This module provides backward compatibility for imports like:
    from istari_digital_client.v3.models import ResourceTypeDto
"""

import sys

# Import the actual v3 package from old location
from istari_digital_client.legacy import v3 as _v3

# Re-export everything from old.v3
from istari_digital_client.legacy.v3 import *

# Set up module aliases so subpackage imports work
# e.g., from istari_digital_client.v3.models import Foo
sys.modules["istari_digital_client.v3.api"] = sys.modules[
    "istari_digital_client.legacy.v3.api"
]
sys.modules["istari_digital_client.v3.models"] = sys.modules[
    "istari_digital_client.legacy.v3.models"
]

# Import subpackages to make them accessible as attributes
from istari_digital_client.legacy.v3 import api, models  # noqa: F401

__all__ = list(getattr(_v3, "__all__", []))
