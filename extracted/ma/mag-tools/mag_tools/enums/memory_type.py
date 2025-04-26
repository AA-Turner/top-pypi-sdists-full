from mag_tools.enums.base_enum import BaseEnum

class MemoryType(BaseEnum):
    DDR = (20, "DDR Memory")
    DDR2 = (21, "DDR2 Memory")
    DDR3 = (24, "DDR3 Memory")
    DDR4 = (26, "DDR4 Memory")
    DDR5 = (31, "DDR5 Memory")
    LPDDR = (27, "Low Power DDR Memory")
    LPDDR2 = (28, "Low Power DDR2 Memory")
    LPDDR3 = (29, "Low Power DDR3 Memory")
    LPDDR4 = (30, "Low Power DDR4 Memory")
    LPDDR5 = (32, "Low Power DDR5 Memory")
    UNKNOWN = (0, "Unknown Memory")