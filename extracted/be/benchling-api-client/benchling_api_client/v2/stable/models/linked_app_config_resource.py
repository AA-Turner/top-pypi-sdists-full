from typing import Union

from ..extensions import UnknownType
from ..models.inaccessible_resource import InaccessibleResource
from ..models.linked_app_config_resource_summary import LinkedAppConfigResourceSummary

LinkedAppConfigResource = Union[LinkedAppConfigResourceSummary, InaccessibleResource, UnknownType]
