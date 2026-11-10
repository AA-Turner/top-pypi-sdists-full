from enum import Enum


class InstanceMetricsEnum(str, Enum):
    VM_CPU_TIME = "vm.cpu.time"
    VM_CPU_UTILIZATION = "vm.cpu.utilization"
    VM_DISK_IO = "vm.disk.io"
    VM_DISK_OPERATIONS = "vm.disk.operations"
    VM_MEMORY_UTILIZATION = "vm.memory.utilization"
    VM_NETWORK_IO = "vm.network.io"
    VOLUME_IO = "volume.io"
    VOLUME_OPERATIONS = "volume.operations"

    def __str__(self) -> str:
        return str(self.value)
