from typing import Union

from ..extensions import UnknownType
from ..models.batch import Batch
from ..models.inaccessible_resource import InaccessibleResource

BatchOrInaccessibleResource = Union[Batch, InaccessibleResource, UnknownType]
