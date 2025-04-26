from typing import Union

from ..extensions import UnknownType
from ..models.inaccessible_resource import InaccessibleResource
from ..models.well import Well

WellOrInaccessibleResource = Union[Well, InaccessibleResource, UnknownType]
