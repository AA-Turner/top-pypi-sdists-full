from enum import Enum


class SoftwareTargetOEnum(str, Enum):
    CPU_FAMILY = "cpu_family"
    CPU_MICROARCHITECTURE = "cpu_microarchitecture"
    CREATED = "created"
    PACKAGE_NAME = "package_name"
    TARGET_NAME = "target_name"
    TARGET_TYPE = "target_type"
    VALUE_0 = "-cpu_family"
    VALUE_1 = "-cpu_microarchitecture"
    VALUE_2 = "-created"
    VALUE_3 = "-package_name"
    VALUE_4 = "-target_name"
    VALUE_5 = "-target_type"

    def __str__(self) -> str:
        return str(self.value)
