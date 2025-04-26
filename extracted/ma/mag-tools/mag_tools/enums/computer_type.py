from mag_tools.enums.base_enum import BaseEnum


class ComputerType(BaseEnum):
    """
    计算机类型枚举类
    """
    DESKTOP = ("Desktop", "台式计算机")
    LAPTOP = ("Laptop", "笔记本电脑")
    SERVER = ("Server", "服务器")
    WORKSTATION = ("Workstation", "工作站")
    TABLET = ("Tablet", "平板电脑")