import pathlib
from typing import Optional

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
from anyscale.cloud_utils import get_cloud_id_and_name
from anyscale.controllers.base_controller import BaseController


class MachinePoolController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.console = Console()

    def create_machine_pool(
        self,
        machine_pool_name: str,
        enable_rootless_dataplane_config: Optional[bool] = False,
    ) -> CreateMachinePoolResponse:
        response: CreateMachinePoolResponse = self.api_client.create_machine_pool_api_v2_machine_pools_create_post(
            CreateMachinePoolRequest(
                machine_pool_name=machine_pool_name,
                enable_rootless_dataplane_config=enable_rootless_dataplane_config,
            )
        ).result
        return response

    def delete_machine_pool(
        self, machine_pool_name: str,
    ):
        self.api_client.delete_machine_pool_api_v2_machine_pools_delete_post(
            DeleteMachinePoolRequest(machine_pool_name=machine_pool_name)
        )

    def update_machine_pool(
        self, machine_pool_name: str, spec_file: str,
    ):
        path = pathlib.Path(spec_file)
        if not path.exists():
            raise FileNotFoundError(f"File {spec_file} does not exist.")

        if not path.is_file():
            raise ValueError(f"File {spec_file} is not a file.")

        spec = yaml.safe_load(path.read_text())

        self.api_client.update_machine_pool_api_v2_machine_pools_update_post(
            UpdateMachinePoolRequest(machine_pool_name=machine_pool_name, spec=spec,)
        )

    def describe_machine_pool(
        self, machine_pool_name: str,
    ) -> DescribeMachinePoolResponse:
        return self.api_client.describe_machine_pool_api_v2_machine_pools_describe_post(
            describe_machine_pool_request=DescribeMachinePoolRequest(
                machine_pool_name=machine_pool_name,
            )
        ).result

    def list_machine_pools(self,) -> ListMachinePoolsResponse:
        response = self.api_client.list_machine_pools_api_v2_machine_pools_get().result
        return response

    def attach_machine_pool_to_cloud(self, machine_pool_name: str, cloud: str):
        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_name=cloud)
        self.api_client.attach_machine_pool_to_cloud_api_v2_machine_pools_attach_post(
            AttachMachinePoolToCloudRequest(
                machine_pool_name=machine_pool_name, cloud_id=cloud_id
            )
        )

    def detach_machine_pool_from_cloud(self, machine_pool_name: str, cloud: str):
        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_name=cloud)
        self.api_client.detach_machine_pool_from_cloud_api_v2_machine_pools_detach_post(
            DetachMachinePoolFromCloudRequest(
                machine_pool_name=machine_pool_name, cloud_id=cloud_id
            )
        )
