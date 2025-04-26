from typing import Union

from ..extensions import UnknownType
from ..models.batch_worklist_items_list import BatchWorklistItemsList
from ..models.container_worklist_items_list import ContainerWorklistItemsList
from ..models.entity_worklist_items_list import EntityWorklistItemsList
from ..models.plate_worklist_items_list import PlateWorklistItemsList

WorklistItemsPaginatedList = Union[
    ContainerWorklistItemsList,
    EntityWorklistItemsList,
    PlateWorklistItemsList,
    BatchWorklistItemsList,
    UnknownType,
]
