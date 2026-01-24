from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from pycarlo.common import get_logger
from pycarlo.features.metadata.base_allow_block_list import BaseAllowBlockList, FilterRule

logger = get_logger(__name__)


@dataclass
class AssetAllowBlockList(BaseAllowBlockList[FilterRule], DataClassJsonMixin):
    # JSON deserialization fails without this ugly override
    rules: Optional[List[FilterRule]] = field(default_factory=list)

    asset_type: Optional[str] = None

    def __post_init__(self):
        # We can't remove the default value because of properties with defaults in the parent class.
        if not self.asset_type:
            raise ValueError("asset_type is required")
