import pathlib
from typing import Any, Dict, List, Optional, Set, Tuple

from rich.console import Console
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    AttachMachinePoolToCloudRequest,
    CreateMachinePoolRequest,
    CreateMachinePoolResponse,
    DeleteMachinePoolRequest,
    DescribeMachinePoolRequest,
    DescribeMachinePoolResponse,
    DetachMachinePoolFromCloudRequest,
    ListMachinePoolsResponse,
    UpdateMachinePoolRequest,
)
from anyscale.cloud_utils import get_cloud_id_and_name, get_cloud_resource_id_by_name
from anyscale.controllers.base_controller import BaseController


def _machine_types_and_partitions(spec: Any) -> Optional[Dict[str, Set[str]]]:
    """Map each machine-type name in a spec to the set of its partition names.

    Returns None when the spec is not diffable -- it is not a dict or has no
    "machine_types" list -- which signals callers to skip the rename/removal check.
    """
    if not isinstance(spec, dict):
        return None
    machine_types = spec.get("machine_types")
    if not isinstance(machine_types, list):
        return None
    result: Dict[str, Set[str]] = {}
    for machine_type in machine_types:
        if not isinstance(machine_type, dict):
            continue
        name = machine_type.get("machine_type")
        if name is None:
            continue
        partition_names: Set[str] = set()
        partitions = machine_type.get("partitions")
        if isinstance(partitions, list):
            for partition in partitions:
                if isinstance(partition, dict) and partition.get("name") is not None:
                    partition_names.add(partition["name"])
        result[name] = partition_names
    return result


def compute_removed_machine_pool_resources(
    current_spec: Any, new_spec: Any
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Find machine types and partitions present in current_spec but absent from new_spec.

    A machine type or partition name that exists in the current (last-applied) spec
    but not in the new spec is being renamed or removed; the backend applies that as a
    delete-then-create, which terminates the underlying instances. Returns a tuple of
    (removed_machine_type_names, removed (machine_type, partition) pairs). Partitions
    are only reported for machine types that survive the update -- a removed machine
    type already accounts for all of its partitions. Returns ([], []) when the new
    spec is not diffable, so a malformed or non-ANYSCALE_MANAGED spec never raises a
    false "removing everything" warning.
    """
    new_resources = _machine_types_and_partitions(new_spec)
    if new_resources is None:
        return [], []

    current_resources = _machine_types_and_partitions(current_spec)
    if current_resources is None:
        current_resources = {}

    removed_types = sorted(
        name for name in current_resources if name not in new_resources
    )
    removed_partitions: List[Tuple[str, str]] = []
    for machine_type_name, partition_names in current_resources.items():
        if machine_type_name not in new_resources:
            # The whole machine type is gone; its partitions are already covered
            # by the machine-type removal above, so don't double-report them.
            continue
        surviving = new_resources[machine_type_name]
        for partition_name in sorted(partition_names - surviving):
            removed_partitions.append((machine_type_name, partition_name))

    return removed_types, removed_partitions


class MachinePoolController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.console = Console()

    def create_machine_pool(self, machine_pool_name: str,) -> CreateMachinePoolResponse:
        response: CreateMachinePoolResponse = self.api_client.create_machine_pool_api_v2_machine_pools_create_post(
            CreateMachinePoolRequest(machine_pool_name=machine_pool_name,)
        ).result
        return response

    def delete_machine_pool(
        self, machine_pool_name: str,
    ):
        self.api_client.delete_machine_pool_api_v2_machine_pools_delete_post(
            DeleteMachinePoolRequest(machine_pool_name=machine_pool_name)
        )

    def update_machine_pool(self, machine_pool_name: str, spec_file: str):
        path = pathlib.Path(spec_file)
        if not path.exists():
            raise FileNotFoundError(f"File {spec_file} does not exist.")

        if not path.is_file():
            raise ValueError(f"File {spec_file} is not a file.")

        spec = yaml.safe_load(path.read_text())

        self._warn_on_destructive_update(machine_pool_name, spec)

        self.api_client.update_machine_pool_api_v2_machine_pools_update_post(
            UpdateMachinePoolRequest(machine_pool_name=machine_pool_name, spec=spec,)
        )

    def _warn_on_destructive_update(
        self, machine_pool_name: str, new_spec: Any
    ) -> None:
        if _machine_types_and_partitions(new_spec) is None:
            # The new spec has no machine_types list to diff against (e.g. a
            # CUSTOMER_MANAGED or malformed spec); leave validation to the backend.
            return

        current_spec = self._get_current_spec(machine_pool_name)
        removed_types, removed_partitions = compute_removed_machine_pool_resources(
            current_spec, new_spec
        )
        if not removed_types and not removed_partitions:
            return

        lines = ["The following machine pool resources will be removed or renamed:"]
        for machine_type_name in removed_types:
            lines.append(
                f"  - machine type '{machine_type_name}' (and all of its partitions)"
            )
        for machine_type_name, partition_name in removed_partitions:
            lines.append(
                f"  - partition '{partition_name}' in machine type '{machine_type_name}'"
            )
        lines.append(
            "Renaming or removing a machine type or partition is applied as a delete and re-create, so the underlying instances will be terminated and any workloads running on them will be disrupted."
        )
        self.log.warning("\n".join(lines))

    def _get_current_spec(self, machine_pool_name: str) -> Optional[dict]:
        try:
            response = self.list_machine_pools()
            for machine_pool in response.machine_pools:
                if machine_pool.machine_pool_name == machine_pool_name:
                    return machine_pool.spec
            return None
        except Exception:  # noqa: BLE001
            # Fail open: if the current spec can't be read, skip the rename/removal
            # check and let the update proceed (the update call below surfaces any
            # real connectivity or auth error). A transient read failure must not
            # block a legitimate update.
            self.log.warning(
                "Could not read the current machine pool spec; skipping the rename/removal check before updating."
            )
            return None

    def describe_machine_pool(
        self, machine_pool_name: str,
    ) -> DescribeMachinePoolResponse:
        return self.api_client.describe_machine_pool_api_v2_machine_pools_describe_post(
            describe_machine_pool_request=DescribeMachinePoolRequest(
                machine_pool_name=machine_pool_name,
            )
        ).result

    def list_machine_pools(self) -> ListMachinePoolsResponse:
        response = self.api_client.list_machine_pools_api_v2_machine_pools_get().result
        return response

    def format_cloud_and_cloud_resources(
        self, cloud_id: str, cloud_resource_ids: List[str]
    ) -> str:
        # Convert cloud ID and cloud resource IDs to "cloud-name (cloud-resource-name-1, cloud-resource-name-2)".
        _, cloud_name = get_cloud_id_and_name(self.api_client, cloud_id=cloud_id)
        cloud_resource_names = [
            self.api_client.get_cloud_resource_api_v2_clouds_cloud_id_resource_get(
                cloud_id, cloud_resource_id
            ).result.name
            for cloud_resource_id in cloud_resource_ids
        ]
        return f"{cloud_name} ({', '.join(cloud_resource_names)})"

    def attach_machine_pool_to_cloud(
        self,
        machine_pool_name: str,
        cloud_name: str,
        cloud_resource_name: Optional[str] = None,
    ):
        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_name=cloud_name)

        cloud_resource_id = None
        if cloud_resource_name:
            cloud_resource_id = get_cloud_resource_id_by_name(
                cloud_id=cloud_id,
                cloud_resource_name=cloud_resource_name,
                api_client=self.api_client,
            )

        self.api_client.attach_machine_pool_to_cloud_api_v2_machine_pools_attach_post(
            AttachMachinePoolToCloudRequest(
                machine_pool_name=machine_pool_name,
                cloud_id=cloud_id,
                cloud_resource_id=cloud_resource_id,
            )
        )

    def detach_machine_pool_from_cloud(
        self,
        machine_pool_name: str,
        cloud_name: str,
        cloud_resource_name: Optional[str] = None,
    ):
        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_name=cloud_name)

        cloud_resource_id = None
        if cloud_resource_name:
            cloud_resource_id = get_cloud_resource_id_by_name(
                cloud_id=cloud_id,
                cloud_resource_name=cloud_resource_name,
                api_client=self.api_client,
            )

        self.api_client.detach_machine_pool_from_cloud_api_v2_machine_pools_detach_post(
            DetachMachinePoolFromCloudRequest(
                machine_pool_name=machine_pool_name,
                cloud_id=cloud_id,
                cloud_resource_id=cloud_resource_id,
            )
        )
