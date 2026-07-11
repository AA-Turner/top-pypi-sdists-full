from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingCloud(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_CLOUD_UNSPECIFIED: _ClassVar[BillingCloud]
    BILLING_CLOUD_AWS: _ClassVar[BillingCloud]
    BILLING_CLOUD_GCP: _ClassVar[BillingCloud]
    BILLING_CLOUD_AZURE: _ClassVar[BillingCloud]

BILLING_CLOUD_UNSPECIFIED: BillingCloud
BILLING_CLOUD_AWS: BillingCloud
BILLING_CLOUD_GCP: BillingCloud
BILLING_CLOUD_AZURE: BillingCloud

class MachineRate(_message.Message):
    __slots__ = ("machine_type", "cpus", "memory_gb", "credits_per_hour", "cloud", "machine_family", "gpus")
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CPUS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_GB_FIELD_NUMBER: _ClassVar[int]
    CREDITS_PER_HOUR_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    MACHINE_FAMILY_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    machine_type: str
    cpus: float
    memory_gb: float
    credits_per_hour: float
    cloud: BillingCloud
    machine_family: str
    gpus: float
    def __init__(
        self,
        machine_type: _Optional[str] = ...,
        cpus: _Optional[float] = ...,
        memory_gb: _Optional[float] = ...,
        credits_per_hour: _Optional[float] = ...,
        cloud: _Optional[_Union[BillingCloud, str]] = ...,
        machine_family: _Optional[str] = ...,
        gpus: _Optional[float] = ...,
    ) -> None: ...

class CloudInstanceType(_message.Message):
    __slots__ = (
        "machine_type",
        "cpus",
        "memory_gb",
        "cloud",
        "machine_family",
        "gpus",
        "local_ssd_count",
        "local_ssd_size_gb",
    )
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CPUS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_GB_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    MACHINE_FAMILY_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SSD_COUNT_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SSD_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    machine_type: str
    cpus: float
    memory_gb: float
    cloud: BillingCloud
    machine_family: str
    gpus: float
    local_ssd_count: int
    local_ssd_size_gb: int
    def __init__(
        self,
        machine_type: _Optional[str] = ...,
        cpus: _Optional[float] = ...,
        memory_gb: _Optional[float] = ...,
        cloud: _Optional[_Union[BillingCloud, str]] = ...,
        machine_family: _Optional[str] = ...,
        gpus: _Optional[float] = ...,
        local_ssd_count: _Optional[int] = ...,
        local_ssd_size_gb: _Optional[int] = ...,
    ) -> None: ...
