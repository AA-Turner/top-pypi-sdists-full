from collections import defaultdict
from typing import Annotated

from pydantic import AfterValidator, Field

from ome_zarr_models.base import BaseAttrs
from ome_zarr_models.common.validation import (
    WellPathCharsConstraint,
    unique_items_validator,
    validate_zarr_node_name,
)

__all__ = ["WellImage", "WellMeta"]


class WellImage(BaseAttrs):
    """
    A single image within a well.

    The ``path`` constraint was relaxed from alphanumeric to alphanumeric +
    ``.-_`` in NGFF 0.6 (see https://github.com/ome/ngff-spec/pull/71).
    """

    path: Annotated[
        str, WellPathCharsConstraint, AfterValidator(validate_zarr_node_name)
    ]
    acquisition: int | None = Field(
        None, description="A unique identifier within the context of the plate"
    )


# ponytail: No version here—lives on WellAttrs via BaseOMEAttrs in v06
class WellMeta(BaseAttrs):
    """
    Metadata for a single well.
    """

    images: Annotated[list[WellImage], AfterValidator(unique_items_validator)] = Field(
        ..., description="Images within a well"
    )

    def get_acquisition_paths(self) -> dict[int, list[str]]:
        """
        Get mapping from acquisition indices to corresponding paths.
        """
        acquisition_dict: dict[int, list[str]] = defaultdict(list)
        for image in self.images:
            if image.acquisition is None:
                raise ValueError(
                    "Cannot get acquisition paths for Zarr files without "
                    "'acquisition' metadata at the well level"
                )
            acquisition_dict[image.acquisition].append(image.path)
        return dict(acquisition_dict)
