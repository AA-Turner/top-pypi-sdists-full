from dataclasses import dataclass, field
import platform
from typing import Optional

from mag_tools.bean.base_data import BaseData


@dataclass
class OperateSystem(BaseData):
    """
    操作系统信息类
    """
    computer_id: Optional[str] = field(default=None, metadata={"description": "所属计算机的标识"})
    name: Optional[str] = field(default=None, metadata={"description": "名称"})
    version: Optional[str] = field(default=None, metadata={"description": "版本"})
    architecture: Optional[str] = field(default=None, metadata={"description": "架构"})

    @classmethod
    def get_info(cls):
        """
        获取操作系统的信息，并返回一个OperateSystem实例
        """
        os_name = platform.system()
        os_version = platform.version()
        os_architecture = platform.machine()
        return cls(name=os_name, version=os_version, architecture=os_architecture)

    @classmethod
    def is_windows(cls):
        return platform.system() == 'Windows'

    @classmethod
    def is_linux(cls):
        return platform.system() == 'Linux'

    # def __str__(self):
    #     """
    #     返回操作系统信息的字符串表示
    #     """
    #     return f"Operating System: {self.name}, Version: {self.version}, Architecture: {self.architecture}"

# 示例用法
if __name__ == '__main__':
    os_info = OperateSystem.get_info()
    print(os_info)
