from enum import Enum


class SoftwareTargetOEnum(str, Enum):
    CPU_MICROARCHITECTURE = "cpu_microarchitecture"
    CREATED = "created"
    PACKAGE_NAME = "package_name"
    TARGET_NAME = "target_name"
    TARGET_TYPE = "target_type"
    VALUE_0 = "-cpu_microarchitecture"
    VALUE_1 = "-created"
    VALUE_2 = "-package_name"
    VALUE_3 = "-target_name"
    VALUE_4 = "-target_type"

    def __str__(self) -> str:
        return str(self.value)
