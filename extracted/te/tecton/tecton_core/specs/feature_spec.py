from dataclasses import dataclass
from typing import Dict
from typing import Optional

from tecton_core.data_types import DataType


@dataclass
class FeatureMetadataSpec:
    name: str
    dtype: DataType
    description: Optional[str]
    tags: Optional[Dict[str, str]]
