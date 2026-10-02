# Copyright 2024 Agnostiq Inc.

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from covalent_cloud import CloudExecutor

from .models.gpu import GPU_TYPE

executor_plugin_name = "oci_cloud"


@dataclass(config=ConfigDict(extra="forbid"))
class OCICloudExecutor(CloudExecutor):
    """
    OCICloudExecutor is used to target BYOC infrastructure on OCI.
    """

    shape: str = "VM.Standard1.1"

    def __post_init__(self):
        """
        Post initialization method for the OCICloudExecutor.
        """
        super().__post_init__()

        num_units = int(self.shape.split(".")[-1])

        if "GPU" in self.shape:
            self.num_gpus = num_units
            self.gpu_type = str(GPU_TYPE.REMOTELY_SET)
        else:
            self.num_cpus = num_units

    @property
    def short_name(self) -> str:
        """
        Property which returns the short name
        of the executor used by Covalent for identification.

        Args:
            None

        Returns:
            The short name of the executor

        """
        return executor_plugin_name
