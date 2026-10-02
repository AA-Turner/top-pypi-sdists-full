"""Settings for band-method TS searches (NEB)."""

from typing import Literal

from pydantic import BaseModel

from .interpolation import Interpolation


class NEBSettings(BaseModel):
    """
    Settings for a nudged elastic band (NEB) TS search.

    :param interpolation_method: method to use for interpolation between nodes
    """

    settings_type: Literal["neb"] = "neb"
    interpolation_method: Interpolation = Interpolation.GEODESIC
