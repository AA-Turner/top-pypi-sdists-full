from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class SnapshotGpuBackend(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SNAPSHOT_GPU_BACKEND_UNSPECIFIED: _ClassVar[SnapshotGpuBackend]
    SNAPSHOT_GPU_BACKEND_NONE: _ClassVar[SnapshotGpuBackend]
    SNAPSHOT_GPU_BACKEND_NVIDIA_CUDA: _ClassVar[SnapshotGpuBackend]

SNAPSHOT_GPU_BACKEND_UNSPECIFIED: SnapshotGpuBackend
SNAPSHOT_GPU_BACKEND_NONE: SnapshotGpuBackend
SNAPSHOT_GPU_BACKEND_NVIDIA_CUDA: SnapshotGpuBackend

class SnapshotCompatibilityRequirements(_message.Message):
    __slots__ = ("schema_version", "cpu_class", "runtime_class", "machine_type", "gpu_backend", "gpu")
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    CPU_CLASS_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_CLASS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    GPU_BACKEND_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    schema_version: int
    cpu_class: str
    runtime_class: str
    machine_type: SnapshotMachineType
    gpu_backend: SnapshotGpuBackend
    gpu: SnapshotGpuRequirements
    def __init__(
        self,
        schema_version: _Optional[int] = ...,
        cpu_class: _Optional[str] = ...,
        runtime_class: _Optional[str] = ...,
        machine_type: _Optional[_Union[SnapshotMachineType, _Mapping]] = ...,
        gpu_backend: _Optional[_Union[SnapshotGpuBackend, str]] = ...,
        gpu: _Optional[_Union[SnapshotGpuRequirements, _Mapping]] = ...,
    ) -> None: ...

class SnapshotMachineType(_message.Message):
    __slots__ = ("provider", "type")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    provider: str
    type: str
    def __init__(self, provider: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class SnapshotGpuRequirements(_message.Message):
    __slots__ = ("backend_version", "stack_class", "devices", "peer_links")
    BACKEND_VERSION_FIELD_NUMBER: _ClassVar[int]
    STACK_CLASS_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    PEER_LINKS_FIELD_NUMBER: _ClassVar[int]
    backend_version: int
    stack_class: str
    devices: _containers.RepeatedCompositeFieldContainer[SnapshotGpuDeviceRequirement]
    peer_links: _containers.RepeatedCompositeFieldContainer[SnapshotGpuPeerLink]
    def __init__(
        self,
        backend_version: _Optional[int] = ...,
        stack_class: _Optional[str] = ...,
        devices: _Optional[_Iterable[_Union[SnapshotGpuDeviceRequirement, _Mapping]]] = ...,
        peer_links: _Optional[_Iterable[_Union[SnapshotGpuPeerLink, _Mapping]]] = ...,
    ) -> None: ...

class SnapshotGpuDeviceRequirement(_message.Message):
    __slots__ = ("logical_ordinal", "hardware_class")
    LOGICAL_ORDINAL_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_CLASS_FIELD_NUMBER: _ClassVar[int]
    logical_ordinal: int
    hardware_class: str
    def __init__(self, logical_ordinal: _Optional[int] = ..., hardware_class: _Optional[str] = ...) -> None: ...

class SnapshotGpuPeerLink(_message.Message):
    __slots__ = ("source_ordinal", "destination_ordinal", "cuda_peer_access", "interconnect_class")
    SOURCE_ORDINAL_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ORDINAL_FIELD_NUMBER: _ClassVar[int]
    CUDA_PEER_ACCESS_FIELD_NUMBER: _ClassVar[int]
    INTERCONNECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    source_ordinal: int
    destination_ordinal: int
    cuda_peer_access: bool
    interconnect_class: str
    def __init__(
        self,
        source_ordinal: _Optional[int] = ...,
        destination_ordinal: _Optional[int] = ...,
        cuda_peer_access: bool = ...,
        interconnect_class: _Optional[str] = ...,
    ) -> None: ...

class SnapshotCompatibility(_message.Message):
    __slots__ = ("requirements", "gpu_stack", "gpu_devices", "source")
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    GPU_STACK_FIELD_NUMBER: _ClassVar[int]
    GPU_DEVICES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    requirements: SnapshotCompatibilityRequirements
    gpu_stack: SnapshotGpuStackProfile
    gpu_devices: _containers.RepeatedCompositeFieldContainer[SnapshotGpuDevice]
    source: SnapshotCaptureSource
    def __init__(
        self,
        requirements: _Optional[_Union[SnapshotCompatibilityRequirements, _Mapping]] = ...,
        gpu_stack: _Optional[_Union[SnapshotGpuStackProfile, _Mapping]] = ...,
        gpu_devices: _Optional[_Iterable[_Union[SnapshotGpuDevice, _Mapping]]] = ...,
        source: _Optional[_Union[SnapshotCaptureSource, _Mapping]] = ...,
    ) -> None: ...

class SnapshotCaptureSource(_message.Message):
    __slots__ = ("host_id", "machine_id", "boot_id", "inventory_generation")
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    BOOT_ID_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_GENERATION_FIELD_NUMBER: _ClassVar[int]
    host_id: str
    machine_id: str
    boot_id: str
    inventory_generation: str
    def __init__(
        self,
        host_id: _Optional[str] = ...,
        machine_id: _Optional[str] = ...,
        boot_id: _Optional[str] = ...,
        inventory_generation: _Optional[str] = ...,
    ) -> None: ...

class SnapshotHostCapabilities(_message.Message):
    __slots__ = (
        "supported_schema_versions",
        "machine_type",
        "cpu_class",
        "runtime_class",
        "gpu_stack",
        "gpu_devices",
        "peer_links",
        "inventory_generation",
        "gpu_backends",
    )
    SUPPORTED_SCHEMA_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CPU_CLASS_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_CLASS_FIELD_NUMBER: _ClassVar[int]
    GPU_STACK_FIELD_NUMBER: _ClassVar[int]
    GPU_DEVICES_FIELD_NUMBER: _ClassVar[int]
    PEER_LINKS_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_GENERATION_FIELD_NUMBER: _ClassVar[int]
    GPU_BACKENDS_FIELD_NUMBER: _ClassVar[int]
    supported_schema_versions: _containers.RepeatedScalarFieldContainer[int]
    machine_type: SnapshotMachineType
    cpu_class: str
    runtime_class: str
    gpu_stack: SnapshotGpuStackProfile
    gpu_devices: _containers.RepeatedCompositeFieldContainer[SnapshotGpuDevice]
    peer_links: _containers.RepeatedCompositeFieldContainer[SnapshotGpuPeerLink]
    inventory_generation: str
    gpu_backends: _containers.RepeatedCompositeFieldContainer[SnapshotGpuBackendCapability]
    def __init__(
        self,
        supported_schema_versions: _Optional[_Iterable[int]] = ...,
        machine_type: _Optional[_Union[SnapshotMachineType, _Mapping]] = ...,
        cpu_class: _Optional[str] = ...,
        runtime_class: _Optional[str] = ...,
        gpu_stack: _Optional[_Union[SnapshotGpuStackProfile, _Mapping]] = ...,
        gpu_devices: _Optional[_Iterable[_Union[SnapshotGpuDevice, _Mapping]]] = ...,
        peer_links: _Optional[_Iterable[_Union[SnapshotGpuPeerLink, _Mapping]]] = ...,
        inventory_generation: _Optional[str] = ...,
        gpu_backends: _Optional[_Iterable[_Union[SnapshotGpuBackendCapability, _Mapping]]] = ...,
    ) -> None: ...

class SnapshotGpuBackendCapability(_message.Message):
    __slots__ = ("backend", "version", "capture", "restore", "equivalent_device_restore", "multi_gpu")
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_FIELD_NUMBER: _ClassVar[int]
    RESTORE_FIELD_NUMBER: _ClassVar[int]
    EQUIVALENT_DEVICE_RESTORE_FIELD_NUMBER: _ClassVar[int]
    MULTI_GPU_FIELD_NUMBER: _ClassVar[int]
    backend: SnapshotGpuBackend
    version: int
    capture: bool
    restore: bool
    equivalent_device_restore: bool
    multi_gpu: bool
    def __init__(
        self,
        backend: _Optional[_Union[SnapshotGpuBackend, str]] = ...,
        version: _Optional[int] = ...,
        capture: bool = ...,
        restore: bool = ...,
        equivalent_device_restore: bool = ...,
        multi_gpu: bool = ...,
    ) -> None: ...

class SnapshotGpuStackProfile(_message.Message):
    __slots__ = (
        "compatibility_class",
        "kernel_driver_version",
        "kernel_driver_build",
        "kernel_driver_variant",
        "nvproxy_abi",
        "driver_libraries",
        "cuda_checkpoint_sha256",
        "cuda_checkpoint_version",
        "cuda_checkpoint_path",
        "cuda_checkpoint_sequential",
    )
    COMPATIBILITY_CLASS_FIELD_NUMBER: _ClassVar[int]
    KERNEL_DRIVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    KERNEL_DRIVER_BUILD_FIELD_NUMBER: _ClassVar[int]
    KERNEL_DRIVER_VARIANT_FIELD_NUMBER: _ClassVar[int]
    NVPROXY_ABI_FIELD_NUMBER: _ClassVar[int]
    DRIVER_LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    CUDA_CHECKPOINT_SHA256_FIELD_NUMBER: _ClassVar[int]
    CUDA_CHECKPOINT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CUDA_CHECKPOINT_PATH_FIELD_NUMBER: _ClassVar[int]
    CUDA_CHECKPOINT_SEQUENTIAL_FIELD_NUMBER: _ClassVar[int]
    compatibility_class: str
    kernel_driver_version: str
    kernel_driver_build: str
    kernel_driver_variant: str
    nvproxy_abi: str
    driver_libraries: _containers.RepeatedCompositeFieldContainer[SnapshotDriverLibrary]
    cuda_checkpoint_sha256: str
    cuda_checkpoint_version: str
    cuda_checkpoint_path: str
    cuda_checkpoint_sequential: bool
    def __init__(
        self,
        compatibility_class: _Optional[str] = ...,
        kernel_driver_version: _Optional[str] = ...,
        kernel_driver_build: _Optional[str] = ...,
        kernel_driver_variant: _Optional[str] = ...,
        nvproxy_abi: _Optional[str] = ...,
        driver_libraries: _Optional[_Iterable[_Union[SnapshotDriverLibrary, _Mapping]]] = ...,
        cuda_checkpoint_sha256: _Optional[str] = ...,
        cuda_checkpoint_version: _Optional[str] = ...,
        cuda_checkpoint_path: _Optional[str] = ...,
        cuda_checkpoint_sequential: bool = ...,
    ) -> None: ...

class SnapshotDriverLibrary(_message.Message):
    __slots__ = ("container_path", "sha256")
    CONTAINER_PATH_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    container_path: str
    sha256: str
    def __init__(self, container_path: _Optional[str] = ..., sha256: _Optional[str] = ...) -> None: ...

class SnapshotGpuHardwareProfile(_message.Message):
    __slots__ = (
        "compatibility_class",
        "type",
        "model",
        "pci_vendor_id",
        "pci_device_id",
        "pci_subsystem_vendor_id",
        "pci_subsystem_device_id",
        "total_memory_bytes",
        "compute_capability_major",
        "compute_capability_minor",
        "device_mode",
    )
    COMPATIBILITY_CLASS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PCI_VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    PCI_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PCI_SUBSYSTEM_VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    PCI_SUBSYSTEM_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_CAPABILITY_MAJOR_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_CAPABILITY_MINOR_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODE_FIELD_NUMBER: _ClassVar[int]
    compatibility_class: str
    type: str
    model: str
    pci_vendor_id: int
    pci_device_id: int
    pci_subsystem_vendor_id: int
    pci_subsystem_device_id: int
    total_memory_bytes: int
    compute_capability_major: int
    compute_capability_minor: int
    device_mode: str
    def __init__(
        self,
        compatibility_class: _Optional[str] = ...,
        type: _Optional[str] = ...,
        model: _Optional[str] = ...,
        pci_vendor_id: _Optional[int] = ...,
        pci_device_id: _Optional[int] = ...,
        pci_subsystem_vendor_id: _Optional[int] = ...,
        pci_subsystem_device_id: _Optional[int] = ...,
        total_memory_bytes: _Optional[int] = ...,
        compute_capability_major: _Optional[int] = ...,
        compute_capability_minor: _Optional[int] = ...,
        device_mode: _Optional[str] = ...,
    ) -> None: ...

class SnapshotGpuDevice(_message.Message):
    __slots__ = (
        "logical_ordinal",
        "hardware",
        "uuid",
        "minor",
        "pci_bus_address",
        "nvidia_gpu_id",
        "device_instance",
        "subdevice_instance",
    )
    LOGICAL_ORDINAL_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PCI_BUS_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NVIDIA_GPU_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    SUBDEVICE_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    logical_ordinal: int
    hardware: SnapshotGpuHardwareProfile
    uuid: str
    minor: int
    pci_bus_address: str
    nvidia_gpu_id: int
    device_instance: int
    subdevice_instance: int
    def __init__(
        self,
        logical_ordinal: _Optional[int] = ...,
        hardware: _Optional[_Union[SnapshotGpuHardwareProfile, _Mapping]] = ...,
        uuid: _Optional[str] = ...,
        minor: _Optional[int] = ...,
        pci_bus_address: _Optional[str] = ...,
        nvidia_gpu_id: _Optional[int] = ...,
        device_instance: _Optional[int] = ...,
        subdevice_instance: _Optional[int] = ...,
    ) -> None: ...
