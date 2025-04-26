from dataclasses import dataclass, field
from typing import Optional

import psutil

from mag_tools.bean.base_data import BaseData
from mag_tools.enums.fs_type import FsType

@dataclass
class DiskPartition(BaseData):
    computer_id: Optional[str] = field(default=None, metadata={"description": "所属计算机的标识"})
    device: Optional[str] = field(default=None, metadata={"description": "设备"})
    fs_type: Optional[FsType] = field(default=None, metadata={"description": "文件系统"})
    mount_point: Optional[str] = field(default=None, metadata={"description": "驱动装载点"})
    opts: Optional[str] = field(default=None, metadata={"description": "挂载选项"})

    @classmethod
    def get_info(cls):
        partition_infos = []

        partitions = psutil.disk_partitions()
        for partition in partitions:
            info = cls(device=partition.device,
                       fs_type=FsType.of_code(partition.fstype),
                       mount_point=partition.mountpoint,
                       opts=partition.opts)
            partition_infos.append(info)

        return partition_infos

if __name__ == '__main__':
    info_ = DiskPartition.get_info()
    print(info_)