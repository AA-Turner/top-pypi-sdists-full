from mag_tools.enums.base_enum import BaseEnum


class UsbType(BaseEnum):
    STORAGE = ("Storage", "存储设备")
    HUB = ("Hub", "集线器")
    COMPOSITE = ("Composite", "复合设备")
    KEY = ("Key", "加密狗")
    OTHER = ("Other", "其他设备")
