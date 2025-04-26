
from mag_tools.enums.base_enum import BaseEnum


class CpuSeries(BaseEnum):
    INTEL_I3 = ("I3", "Intel Core i3")
    INTEL_I5 = ("I5", "Intel Core i5")
    INTEL_I7 = ("I7", "Intel Core i7")
    INTEL_I9 = ("I9", "Intel Core i9")
    AMD_3 = ("R3", "AMD Ryzen 3")
    AMD_5 = ("R5", "AMD Ryzen 5")
    AMD_7 = ("R7", "AMD Ryzen 7")
    AMD_9 = ("R9", "AMD Ryzen 9")