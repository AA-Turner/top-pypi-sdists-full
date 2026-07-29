from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from anyscale._private.models import ModelBase


@dataclass(frozen=True)
class MachinePool(ModelBase):
    """A machine pool in an Anyscale organization."""

    machine_pool_name: str = field(metadata={"docstring": "Name of the machine pool."})

    def _validate_machine_pool_name(self, machine_pool_name: str):
        if not isinstance(machine_pool_name, str):
            raise TypeError("'machine_pool_name' must be a string.")

    machine_pool_id: str = field(
        metadata={"docstring": "Unique identifier for the machine pool."}
    )

    def _validate_machine_pool_id(self, machine_pool_id: str):
        if not isinstance(machine_pool_id, str):
            raise TypeError("'machine_pool_id' must be a string.")

    cloud_ids: Optional[List[str]] = field(
        metadata={"docstring": "IDs of the clouds the machine pool is attached to."}
    )

    def _validate_cloud_ids(self, cloud_ids: Optional[List[str]]):
        if cloud_ids is not None and not isinstance(cloud_ids, list):
            raise TypeError("'cloud_ids' must be a list or None.")

    spec: Optional[Dict[str, Any]] = field(
        metadata={"docstring": "Specification of the machine pool."}
    )

    def _validate_spec(self, spec: Optional[Dict[str, Any]]):
        if spec is not None and not isinstance(spec, dict):
            raise TypeError("'spec' must be a dict or None.")
