"""Settings for string-method TS searches (FSM and GSM)."""

from typing import Literal

from pydantic import BaseModel

from .interpolation import Interpolation


class StringMethodSettings(BaseModel):
    """Settings for a string-method TS search.

    Attributes:
        settings_type: search-settings discriminator; fixed to "string_method"
        freeze: freeze nodes as they are added to the string (true=FSM, false=GSM; default True)
        interpolation_method: method to use for interpolation between nodes (default GEODESIC)
    """

    settings_type: Literal["string_method"] = "string_method"
    freeze: bool = True
    interpolation_method: Interpolation = Interpolation.GEODESIC


class FSMSettings(StringMethodSettings):
    """Settings for the Freezing String Method (FSM) TS search.

    Retained for backwards compatibility; equivalent to `StringMethodSettings(freeze=True)`.
    Deprecated

    Attributes:
        settings_type: inherited search-settings discriminator; fixed to "string_method"
        interpolation_method: inherited interpolation method between nodes (default GEODESIC)
        freeze: always True for FSM
    """

    freeze: Literal[True] = True
