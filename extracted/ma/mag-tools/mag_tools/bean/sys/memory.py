import os
from dataclasses import dataclass, field
from typing import Optional

import psutil

from mag_tools.bean.base_data import BaseData
from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.utils.security.digest import Digest


@dataclass
class Memory(BaseData):
    """
    内存参数类
    """
    sn: Optional[str] = field(default=None, metadata={"description": "序号"})
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    total_capacity: Optional[int] = field(default=None, metadata={"description": "总容量（单位：GB）"})
    available_capacity: Optional[int] = field(default=None, metadata={"description": "可用内存（单位：GB）"})
    used_capacity: Optional[int] = field(default=None, metadata={"description": "使用内存（单位：GB）"})
    free_capacity: Optional[int] = field(default=None, metadata={"description": "空闲内存（单位：GB）"})
    cache: Optional[int] = field(default=None, metadata={"description": "缓存大小（单位：GB）"})
    buffer_size: Optional[int] = field(default=None, metadata={"description": "缓冲区大小（单位：GB）"})

    @classmethod
    def get_info(cls):
        """
        获取当前系统的内存信息，并返回一个Memory实例
        """
        # 使用psutil获取内存使用情况
        memory_info = psutil.virtual_memory()

        if OperateSystem.is_windows():
            cache_, buffer_size = cls.__get_from_windows()
        else:
            cache_, buffer_size = cls.__get_from_linux()

        return Memory(
            total_capacity=memory_info.total // (1024 ** 3),  # 将字节转换为GB
            available_capacity=memory_info.available // (1024 ** 3),  # 将字节转换为GB
            used_capacity=memory_info.used // (1024 ** 3),  # 将字节转换为GB
            free_capacity=memory_info.free // (1024 ** 3),  # 将字节转换为GB
            cache=cache_,
            buffer_size=buffer_size
        )

    @property
    def hash(self):
        return Digest.md5(f'{self.total_capacity}')

    @classmethod
    def __get_from_windows(cls):
        cache_, buffer_size = None, None
        try:
            free, total = 0, 0

            result = os.popen('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value').read()
            lines = result.split('\n')
            for line in lines:
                if 'FreePhysicalMemory' in line:
                    free = int(line.split('=')[1].strip())
                if 'TotalVisibleMemorySize' in line:
                    total = int(line.split('=')[1].strip())

            cache_ = (total - free) // 1024  # 缓存大小（MB）
            buffer_size = cache_  # 这是一个近似值
        except (OSError, ValueError):
            pass

        return cache_, buffer_size

    @classmethod
    def __get_from_linux(cls):
        cache_, buffer_size = None, None
        try:
            result = os.popen('free -g').read()
            lines = result.split('\n')
            buffers_line = lines[2].split()

            cache_ = int(buffers_line[5])  # 缓存大小（GB）
            buffer_size = int(buffers_line[4])  # 缓冲区大小（GB）
        except (OSError, ValueError):
            pass

        return cache_, buffer_size

if __name__ == '__main__':
    info_ = Memory.get_info()
    print(info_)