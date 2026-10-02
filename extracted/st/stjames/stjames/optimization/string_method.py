"""Settings for string-method TS searches (FSM and GSM)."""

from typing import Literal

from pydantic import BaseModel

from .interpolation import Interpolation


class StringMethodSettings(BaseModel):
    """
    Settings for a string-method TS search.

    :param freeze: freeze nodes as they are added to the string (true=FSM, false=GSM)
    :param interpolation_method: method to use for interpolation between nodes
    """

    settings_type: Literal["string_method"] = "string_method"
    freeze: bool = True
    interpolation_method: Interpolation = Interpolation.GEODESIC


class FSMSettings(StringMethodSettings):
    """
    Settings for the Freezing String Method (FSM) TS search.

    Retained for backwards compatibility; equivalent to `StringMethodSettings(freeze=True)`.
    Deprecated

    :param freeze: always True for FSM
    """

    freeze: Literal[True] = True
