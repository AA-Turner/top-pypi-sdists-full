"""Interpolation methods for generating initial paths between end nodes."""

from ..base import LowercaseStrEnum


class Interpolation(LowercaseStrEnum):
    """Methods for interpolating the initial path between end nodes."""

    CARTESIAN = "cartesian"
    LINEAR_SYNCHRONOUS_TRANSIT = "linear_synchronous_transit"
    REDUNDANT_INTERNAL_COORDINATES = "redundant_internal_coordinates"
    GEODESIC = "geodesic"
    IDPP = "idpp"
