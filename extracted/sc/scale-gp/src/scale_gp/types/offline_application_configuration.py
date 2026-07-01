# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["OfflineApplicationConfiguration"]


class OfflineApplicationConfiguration(BaseModel):
    metadata: Optional[Dict[str, object]] = None
    """User defined metadata about the application"""
