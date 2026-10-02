"""
Backward compatibility shim for istari_digital_client.v2.

The canonical v2 package lives in istari_digital_client.legacy.v2.
This module provides backward compatibility for imports like:
    from istari_digital_client.v2.models import Job
"""

import sys

# Import the actual v2 package from old location
from istari_digital_client.legacy import v2 as _v2

# Re-export everything from old.v2
from istari_digital_client.legacy.v2 import *

# Set up module aliases so subpackage imports work
# e.g., from istari_digital_client.v2.models import Foo
sys.modules["istari_digital_client.v2.api"] = sys.modules[
    "istari_digital_client.legacy.v2.api"
]
sys.modules["istari_digital_client.v2.models"] = sys.modules[
    "istari_digital_client.legacy.v2.models"
]

# Import subpackages to make them accessible as attributes
from istari_digital_client.legacy.v2 import api, models  # noqa: F401

__all__ = list(getattr(_v2, "__all__", []))
