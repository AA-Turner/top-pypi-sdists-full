
from mag_tools.enums.base_enum import BaseEnum


class MediaType(BaseEnum):
    """
    磁盘类型枚举类
    """
    SSD = ("Solid state disk", "固态硬盘")
    HDD = ("Fixed hard disk media", "机械硬盘")
    REMOVABLE = ("Removable media", "可移动硬盘和U盘")
    OPTICAL = ("Optical disk", "光盘")
    UNKNOWN = ("Unknown", "未知")
