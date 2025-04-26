from typing import Union

from ..extensions import UnknownType
from ..models.batch import Batch
from ..models.container import Container
from ..models.generic_entity import GenericEntity
from ..models.plate import Plate

WorklistItem = Union[Batch, Container, GenericEntity, Plate, UnknownType]
