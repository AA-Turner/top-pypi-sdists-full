from mag_tools.enums.base_enum import BaseEnum


class ClientType(BaseEnum):
    IPHONE = ("IPhone", "苹果IPhone客户端")
    IPAD = ("IPad", "苹果IPAD客户端")
    ANDROID = ("Android", "安卓客户端")
    WEB = ("Web", "浏览器客户端")
    WINDOWS = ("Windows", "Windows客户端")
    MACOS = ("Macos", "苹果Mac客户端")
    APPLICATION = ("Application", "应用系统客户端")