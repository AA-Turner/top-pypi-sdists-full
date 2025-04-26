import subprocess
import wmi
from dataclasses import dataclass, field
from typing import Optional

from mag_tools.bean.base_data import BaseData
from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.utils.security.digest import Digest


@dataclass
class Motherboard(BaseData):
    computer_id: Optional[str] = field(default=None, metadata={"description": "所属计算机的标识"})
    manufacturer: Optional[str] = field(default=None, metadata={"description": "主板制造商"})
    product: Optional[str] = field(default=None, metadata={"description": "主板产品型号"})
    serial_number: Optional[str] = field(default=None, metadata={"description": "主板序列号"})
    version: Optional[str] = field(default=None, metadata={"description": "主板版本"})

    @property
    def hash(self):
        return Digest.md5(f'{self.serial_number}{self.manufacturer}{self.product}{self.version}')

    @classmethod
    def get_info(cls):
        """
        获取主板信息，根据操作系统选择相应的方法
        """
        if OperateSystem.is_windows():
            return cls.__get_from_windows()
        elif OperateSystem.is_linux():
            return cls.__get_from_linux()

    @classmethod
    def __get_from_windows(cls):
        """
        从 Windows 系统获取主板信息
        """
        c = wmi.WMI()
        motherboard_info = c.Win32_BaseBoard()[0]
        return cls(
            manufacturer=motherboard_info.Manufacturer,
            product=motherboard_info.Product,
            serial_number=motherboard_info.SerialNumber,
            version=motherboard_info.Version
        )

    @classmethod
    def __get_from_linux(cls):
        """
        从 Linux 系统获取主板信息
        """
        try:
            result = subprocess.run(["sudo", "dmidecode", "-t", "baseboard"], capture_output=True, text=True, check=True)
            lines = result.stdout.split("\n")
            info = {}
            for line in lines:
                if line.startswith("\tManufacturer:"):
                    info["manufacturer"] = line.split(":")[1].strip()
                elif line.startswith("\tProduct Name:"):
                    info["product"] = line.split(":")[1].strip()
                elif line.startswith("\tSerial Number:"):
                    info["serial_number"] = line.split(":")[1].strip()
                elif line.startswith("\tVersion:"):
                    info["version"] = line.split(":")[1].strip()
            return cls(
                manufacturer=info.get("manufacturer"),
                product=info.get("product"),
                serial_number=info.get("serial_number"),
                version=info.get("version")
            )
        except subprocess.CalledProcessError as e:
            print(f"Error getting motherboard information: {e}")
            return cls()

if __name__ == '__main__':
    info_ = Motherboard.get_info()
    print(info_)