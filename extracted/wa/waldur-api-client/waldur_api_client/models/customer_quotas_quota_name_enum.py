from enum import Enum


class CustomerQuotasQuotaNameEnum(str, Enum):
    ESTIMATED_PRICE = "estimated_price"
    NC_RESOURCE_COUNT = "nc_resource_count"
    OS_CPU_COUNT = "os_cpu_count"
    OS_RAM_SIZE = "os_ram_size"
    OS_STORAGE_SIZE = "os_storage_size"
    VPC_CPU_COUNT = "vpc_cpu_count"
    VPC_FLOATING_IP_COUNT = "vpc_floating_ip_count"
    VPC_INSTANCE_COUNT = "vpc_instance_count"
    VPC_RAM_SIZE = "vpc_ram_size"
    VPC_STORAGE_SIZE = "vpc_storage_size"

    def __str__(self) -> str:
        return str(self.value)
