from dataclasses import dataclass, field
from typing import Optional

import wmi

from mag_tools.bean.base_data import BaseData
from mag_tools.enums.media_type import MediaType
from mag_tools.utils.security.digest import Digest


@dataclass
class Disk(BaseData):
    """
    磁盘参数类
    """
    computer_id: Optional[str] = field(default=None, metadata={"description": "所属计算机的标识"})
    serial_number: Optional[str] = field(default=None, metadata={"description": "序列号"})
    model: Optional[str] = field(default=None, metadata={"description": "型号"})
    media_type: Optional[str] = field(default=None, metadata={"description": "介质类型"})
    manufacturer: Optional[str] = field(default=None, metadata={"description": "制造商"})
    capacity: Optional[int] = field(default=None, metadata={"description": "总容量，单位为G"})
    caption: Optional[str] = field(default=None, metadata={"description": "描述"})
    device_id: Optional[str] = field(default=None, metadata={"description": "磁盘的设备标识符"})
    partitions: Optional[int] = field(default=None, metadata={"description": "分区数"})
    interface_type: Optional[str] = field(default=None, metadata={"description": "接口类型"})
    firmware_revision: Optional[str] = field(default=None, metadata={"description": "固件版本"})
    status: Optional[str] = field(default=None, metadata={"description": "状态"})
    sectors_per_track: Optional[int] = field(default=None, metadata={"description": "每磁道的扇区数"})
    total_tracks: Optional[int] = field(default=None, metadata={"description": "磁盘总磁道数"})
    bytes_per_sector: Optional[int] = field(default=None, metadata={"description": "每扇区的字节数"})
    tracks_per_cylinder: Optional[int] = field(default=None, metadata={"description": "每柱面的磁道数"})

    @property
    def hash(self):
        return Digest.md5(f'{self.serial_number}{self.media_type}{self.model}{self.manufacturer}{self.capacity}')

    @classmethod
    def get_info(cls):
        physical_disks = []
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            info = cls(serial_number=disk.DeviceID,
                       media_type=MediaType.of_code(disk.MediaType),
                       model=disk.Model,
                       capacity=int(disk.Size) // 1000**3,
                       manufacturer=disk.Manufacturer,
                       caption=disk.Caption,
                       device_id=disk.DeviceID,
                       partitions=disk.Partitions,
                       interface_type=disk.InterfaceType,
                       firmware_revision=disk.FirmwareRevision,
                       status=disk.Status,
                       sectors_per_track=disk.SectorsPerTrack,
                       total_tracks=disk.TotalTracks,
                       bytes_per_sector=disk.BytesPerSector,
                       tracks_per_cylinder=disk.TracksPerCylinder)

            if "SSD" in disk.Model or "Solid State" in disk.Model:
                info.media_type = MediaType.SSD

            physical_disks.append(info)

        return physical_disks

    @classmethod
    def __parse(cls, model):
        items = model.split()
        manufacturer = items[0] if len(items) > 0 else None
        dick_type = MediaType.of_code(items[1]) if len(items) > 1 else None

        return manufacturer, dick_type

if __name__ == '__main__':
    disk_ = Disk.get_info()
    print(disk_)