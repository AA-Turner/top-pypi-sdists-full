"""Settings for string-method TS searches (FSM and GSM)."""

from typing import Literal

from pydantic import BaseModel

from .interpolation import Interpolation


class StringMethodSettings(BaseModel):
    """
    Settings for a string-method TS search.

    :param settings_type: search-settings discriminator; fixed to "string_method"
    :param freeze: freeze nodes as they are added to the string (true=FSM, false=GSM; default True)
    :param interpolation_method: method to use for interpolation between nodes (default GEODESIC)
    """

    settings_type: Literal["string_method"] = "string_method"
    freeze: bool = True
    interpolation_method: Interpolation = Interpolation.GEODESIC


class FSMSettings(StringMethodSettings):
    """
    Settings for the Freezing String Method (FSM) TS search.

    Retained for backwards compatibility; equivalent to `StringMethodSettings(freeze=True)`.
    Deprecated

    :param settings_type: inherited search-settings discriminator; fixed to "string_method"
    :param interpolation_method: inherited interpolation method between nodes (default GEODESIC)
    :param freeze: always True for FSM
    """

    freeze: Literal[True] = True
