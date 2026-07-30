from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field

from acryl_datahub_cloud.periodic_analytics.bundled_config import read_config_yaml

BUNDLED_USAGE_OPERATIONS_FILE = "usage_operations.yaml"
DEFAULT_COST_UNITS_FALLBACK = 1
_USAGE_OPERATIONS_KEY = "usage_operations"


class UsageOperationConfig(BaseModel):
    # GMS's usage_operations.yaml carries fields (description, request_apis,
    # activity_class, graphql) that billing-sync derivation doesn't need —
    # tolerate and ignore them rather than mirroring the whole taxonomy here.
    model_config = ConfigDict(extra="ignore")

    ingestion_endpoint: bool = False
    default_cost_units: int = DEFAULT_COST_UNITS_FALLBACK


class UsageOperationsConfig(BaseModel):
    operations: Dict[str, UsageOperationConfig] = Field(default_factory=dict)

    def is_known(self, usage_operation: str) -> bool:
        return usage_operation in self.operations

    def is_ingestion_endpoint(self, usage_operation: str) -> bool:
        op = self.operations.get(usage_operation)
        return op.ingestion_endpoint if op is not None else False

    def default_cost_units(self, usage_operation: str) -> int:
        op = self.operations.get(usage_operation)
        return op.default_cost_units if op is not None else DEFAULT_COST_UNITS_FALLBACK


def _read_yaml(text: str) -> UsageOperationsConfig:
    raw = yaml.safe_load(text) or {}
    operations = raw.get(_USAGE_OPERATIONS_KEY, {})
    return UsageOperationsConfig(
        operations={
            name: UsageOperationConfig.model_validate(fields)
            for name, fields in operations.items()
        }
    )


def load_usage_operations(path: Optional[str] = None) -> UsageOperationsConfig:
    if path:
        return _read_yaml(Path(path).read_text())
    return _read_yaml(read_config_yaml(BUNDLED_USAGE_OPERATIONS_FILE))
