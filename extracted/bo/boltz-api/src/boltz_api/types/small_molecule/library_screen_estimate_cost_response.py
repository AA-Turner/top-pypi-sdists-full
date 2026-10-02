# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LibraryScreenEstimateCostResponse", "Breakdown"]


class Breakdown(BaseModel):
    """Cost breakdown for the billed application."""

    application: Literal[
        "structure_and_binding",
        "small_molecule_design",
        "small_molecule_library_screen",
        "protein_design",
        "protein_redesign",
        "protein_library_screen",
        "adme",
    ]

    cost_per_unit_usd: str
    """
    Estimated cost per displayed unit as a decimal string, rounded up to 4 decimal
    places. This may include token-size multipliers or generation overhead;
    estimated_cost_usd is the authoritative total.
    """

    num_units: int
    """Number of billable units in the estimate.

    The unit depends on the endpoint: samples for structure-and-binding, molecules
    for ADME, and requested proteins or molecules for design/screen endpoints.
    """


class LibraryScreenEstimateCostResponse(BaseModel):
    """
    Estimate response with monetary values encoded as decimal strings to preserve precision.
    """

    breakdown: Breakdown
    """Cost breakdown for the billed application."""

    disclaimer: str

    estimated_cost_usd: str
    """Estimated total cost as a decimal string"""
