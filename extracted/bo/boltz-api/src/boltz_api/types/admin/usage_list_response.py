# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["UsageListResponse"]


class UsageListResponse(BaseModel):
    end_time: datetime

    quantity: int
    """Aggregated billed quantity for this bucket"""

    start_time: datetime

    application: Optional[
        Literal[
            "structure_and_binding",
            "small_molecule_design",
            "small_molecule_library_screen",
            "protein_design",
            "protein_redesign",
            "protein_library_screen",
            "adme",
        ]
    ] = None

    workspace_id: Optional[str] = None
    """Present when grouped by workspace_id"""
