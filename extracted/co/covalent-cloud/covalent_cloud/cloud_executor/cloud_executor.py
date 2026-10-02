# Copyright 2023 Agnostiq Inc.

import os
import re
from dataclasses import asdict
from datetime import timedelta
from typing import Dict, Optional, Union

import arrow
from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass

from ..shared.classes.helpers import check_env_is_ready
from ..shared.classes.settings import Settings, settings
from .models.gpu import DEPRECATED_GPUS, GPU_TYPE

executor_plugin_name = "cloud"
unit_multipliers = {"GB": 1024, "MB": 1}
gpu_type_allowed_counts = {
    GPU_TYPE.A100: [1, 2, 4, 8],
    GPU_TYPE.H100: [1, 2, 4, 8],
    GPU_TYPE.V100: [1, 4, 8],
    GPU_TYPE.A10: [1, 4, 8],
    GPU_TYPE.A6000: [1, 2, 4, 8],
    GPU_TYPE.A4000: [1, 2, 4, 8, 10],
    GPU_TYPE.A5000: [1, 2, 4, 8],
    GPU_TYPE.T4: [1, 4],
    GPU_TYPE.L40: [1, 2, 4, 8],
}

EXTRAS_ALLOWED = os.environ.get("COVALENT_CLOUD_EXECUTOR_EXTRAS_ALLOWED", "0") == "1"


@dataclass(config=ConfigDict(extra="allow" if EXTRAS_ALLOWED else "forbid"))
class CloudExecutor:
    """
    CloudExecutor represents a configuration for executing a Covalent workflow on the Covalent Cloud.
    This class allows users to configure the resources (such as the number of CPUs, memory, GPUs, and GPU type) and the software environment for a Covalent workflow that will be executed on the Covalent Cloud. The time limit for the workflow execution can also be set.

    Attributes:

        num_cpus (int, optional): Number of CPUs to be used for the workflow. Defaults to 1.
        cpu_type (str, optional): Model of the CPU to be used for the workflow. Defaults to an empty string.
        memory (int, optional): Amount of memory (in MB) to be used for the workflow. Defaults to 1024.
        num_gpus (int, optional): Number of GPUs to be used for the workflow. Defaults to 0.
        gpu_type (Union[str, cloud_executor.GPU_TYPES], optional): Type of GPU to be used for the workflow. Defaults to an empty string.
        env (str, optional): Name of the software environment to be used for the workflow. Defaults to "default".
        time_limit (Union[int, timedelta], optional): Time limit for the workflow execution, in seconds or as a timedelta. Defaults to 1800s (30 mins). Alternatively can take human readable string in format 'in <number> <unit(s)>'
        provider (str, optional): Name of the provider to target for execution, e.g. 'AWS'. Defaults to None.
        volume_id (int, optional): ID of the volume to be used for the workflow. Defaults to None.
        settings (Settings, optional): Settings object to be used for the workflow. Defaults to the global settings object.
        validate_environment (bool, optional): Whether to validate the environment before dispatching the workflow. Defaults to True.
    Examples:

        .. highlight:: python
        .. code-block:: python

            # create a CloudExecutor with default resource configuration
            # executor = CloudExecutor()

            # create a custom CloudExecutor with specified resources and environment
            # executor = CloudExecutor(
            #     num_cpus=4,
            #     memory=2048,
            #     num_gpus=1,
            #     gpu_type="NVIDIA-Tesla-V100",
            #     env="my_custom_env",
            #     time_limit="in 30 minutes"  # 30 minutes
            # )

            import covalent as ct
            from covalent_cloud import CloudExecutor

            cloud_executor1 = CloudExecutor(num_cpus=1, memory=1024)
            cloud_executor2 = CloudExecutor(num_cpus=2, memory=2048)
            cloud_executor3 = CloudExecutor(num_cpus=1, memory=512)

            # Define manageable tasks as electrons with different cloud executors
            @ct.electron(executor=cloud_executor1)
            def add(x, y):
                return x + y

            @ct.electron(executor=cloud_executor2)
            def multiply(x, y):
                return x * y

            @ct.electron(executor=cloud_executor3)
            def divide(x, y):
                return x / y

            # Define the workflow as a lattice
            @ct.lattice
            def workflow(x, y):
                r1 = add(x, y)
                r2 = [multiply(r1, y) for _ in range(4)]
                r3 = [divide(x, value) for value in r2]
                return r3

            # Import the Covalent Cloud module
            import covalent_cloud as cc

            # Dispatch the workflow to the Covalent Cloud
            dispatch_id = cc.dispatch(workflow)(1, 2)
            result = cc.get_result(dispatch_id, wait=True)
            print(result)

    """

    num_cpus: int = 1
    cpu_type: str = ""
    memory: Union[int, str] = 1024
    num_gpus: int = 0
    gpu_type: Union[str, GPU_TYPE] = ""
    env: str = "default"
    time_limit: Union[int, timedelta, str] = 60 * 30
    provider: Optional[str] = None
    volume_id: Optional[int] = None
    settings: Dict = Field(default_factory=settings.model_dump)
    validate_environment: bool = True

    def __post_init__(self, **kwargs):
        # check if the environment is valid
        if self.validate_environment:
            check_env_is_ready(self.env, Settings.model_validate(self.settings))

        # if gpu type is specified, but num_gpus is not, set num_gpus to 1
        if self.gpu_type and self.num_gpus == 0:
            self.num_gpus = 1

        # check if gpu type and num are consistent
        if (
            os.environ.get("COVALENT_CLOUD_DISABLE_GPU_VALIDATION") is None
            and (self.num_gpus > 0 or self.gpu_type)
            and GPU_TYPE(self.gpu_type) in gpu_type_allowed_counts
            and self.num_gpus not in gpu_type_allowed_counts.get(GPU_TYPE(self.gpu_type), [])
        ):
            raise ValueError(
                f"Invalid number of GPUs for {self.gpu_type}. "
                f"Please choose from: {gpu_type_allowed_counts.get(GPU_TYPE(self.gpu_type))}"
            )

        self.gpu_type = str(self.gpu_type)

        self._extras = {}
        if EXTRAS_ALLOWED:
            for k, v in self.__dict__.items():
                if k not in self.__dataclass_fields__ and k != "_extras":
                    self._extras[k] = v

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

    # Validators:
    @model_validator(mode="after")
    def gpu_type_required(self) -> "CloudExecutor":
        """
        Validator which ensures that GPU type is specified if any GPUs are requested.

        Returns:
            The validated instance

        """
        if self.num_gpus > 0 and not self.gpu_type:
            raise ValueError("GPU type must be specified if num_gpus > 0")

        return self

    @field_validator("num_cpus", "memory", "time_limit")
    @classmethod
    def gt_than_zero(cls, v: int) -> int:
        """
        Validator which ensures that the value is greater than 0.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """
        if v <= 0:
            raise ValueError(f"{v} must be greater than 0")

        return v

    @field_validator("gpu_type")
    @classmethod
    def gpu_types_non_deprecated(cls, v: str) -> str:
        """
        Validator which ensures that the GPU type is not deprecated.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """
        if v and v in DEPRECATED_GPUS:
            raise ValueError(f"GPU type '{v}' is now deprecated.")
        return v

    @field_validator("memory", mode="before")
    @classmethod
    def memory_to_int(cls, v: Union[int, str]) -> int:
        """
        Validator which converts the memory value to an integer.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """
        if isinstance(v, str):
            # grab the number and the unit
            match = re.match(r"(\d+)\s*([A-Za-z]+)", v)
            if match:
                memory_value, unit = match.groups()
            else:
                raise ValueError("Invalid memory string format")

            # convert to MB (int)
            try:
                memory_value = int(memory_value)
                unit = unit.strip()
                v = int(memory_value * unit_multipliers[unit])
            except ValueError as e:
                raise ValueError(f"Invalid memory value: {v}.") from e

        return v

    @field_validator("time_limit", mode="before")
    @classmethod
    def time_limit_to_int_seconds(cls, v: Union[int, timedelta, str]) -> int:
        """
        Validator which converts the time limit value to seconds.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """
        if isinstance(v, timedelta):
            v = v.total_seconds()

        elif isinstance(v, str):
            v = _time_string_total_seconds(v)

        return int(v)

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable dictionary representation of this object.

        Args:
            None

        Returns:
            The JSON-serializable dictionary representation of this object.

        """
        return {
            "type": str(self.__class__),
            "short_name": self.short_name,
            "attributes": asdict(self) | self._extras,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CloudExecutor":
        """
        Create a CloudExecutor object from a dictionary.

        Args:
            data: The dictionary to create the CloudExecutor object from.

        Returns:
            The CloudExecutor object created from the dictionary.

        """
        return cls(**data)


def _time_string_total_seconds(time_limit: str) -> float:
    """Convert a time limit string to seconds.

    Args:
        time_limit: A string specifying the time limit.

    Returns:
        Total seconds in the time limit.

    """
    time_limit = time_limit.strip()

    if not time_limit:
        raise ValueError("Empty time limit string.")

    if "-" in time_limit:  # ad hoc disallow any negatives
        raise ValueError("The '-' character is not allowed in time limit strings.")

    is_human = any(w in time_limit for w in ["hours", "minutes", "seconds"])

    if is_human and re.findall(r"(?:\d+:\d+:\d+\s|\s\d+:\d+:\d+)", time_limit):
        raise ValueError("Mixed time formats are not allowed.")

    now = arrow.utcnow()
    # parse the 'later' point in time
    try:
        if hs_ms_ss := re.match(r"(\d+):(\d+):(\d+)$", time_limit):  # e.g. '05:45:00'
            hs, ms, ss = hs_ms_ss.groups()
            later = now.shift(hours=int(hs), minutes=int(ms), seconds=int(ss))

        else:  # e.g. '5 hours and 45 minutes'
            time_limit = time_limit if time_limit.startswith("in ") else f"in {time_limit}"
            later = now.dehumanize(time_limit)

    except Exception as e:
        raise ValueError(
            f"Invalid time limit string: '{time_limit}'. "
            "Please provide a valid time limit, e.g. '5 hours and 45 minutes' or '05:45:00'."
        ) from e

    # amount of time is the difference between datetimes
    return (later - now).total_seconds()
