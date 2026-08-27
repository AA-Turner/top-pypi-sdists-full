"""
For reference, see the [plate section of the OME-Zarr specification](https://ngff.openmicroscopy.org/0.5/index.html#plate-md).
"""

from ome_zarr_models.common.plate import (
    Acquisition,
    Column,
    PlateBase,
    Row,
    WellInPlate,
)

__all__ = [
    "Acquisition",
    "Column",
    "PlateBase",
    "Row",
    "WellInPlate",
]

# Plate is just PlateBase in v06.
# The version key lives on HCSAttrs (via BaseOMEAttrs).
Plate = PlateBase
