import re
import subprocess
from dataclasses import dataclass, field
from typing import Optional

import wmi

from mag_tools.bean.base_data import BaseData
from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.enums.memory_type import MemoryType
from mag_tools.utils.security.digest import Digest


@dataclass
class MemoryModule(BaseData):
    sn: Optional[str] = field(default=None, metadata={"description": "序号"})
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机资源标识"})
    serial_number: Optional[str] = field(default=None, metadata={"description": "序列号"})
    memory_type: Optional[MemoryType] = field(default=None, metadata={"description": "内存类型"})
    capacity: Optional[int] = field(default=None, metadata={"description": "容量 (GB)"})
    speed: Optional[int] = field(default=None, metadata={"description": "频率 (MHz)"})
    voltage: Optional[float] = field(default=None, metadata={"description": "电压 (mV)"})
    form_factor: Optional[str] = field(default=None, metadata={"description": "形态"})
    part_number: Optional[str] = field(default=None, metadata={"description": "零件编号"})
    manufacturer: Optional[str] = field(default=None, metadata={"description": "生产厂商"})
    latency: Optional[int] = field(default=None, metadata={"description": "延迟 (CL)"})
    bank_label: Optional[int] = field(default=None, metadata={"description": "插槽位置标签"})
    device_locator: Optional[int] = field(default=None, metadata={"description": "内存所在位置"})
    data_width: Optional[int] = field(default=None, metadata={"description": "数据宽度，以位为单位"})
    tag: Optional[str] = field(default=None, metadata={"description": "标签"})

    @property
    def hash(self):
        return Digest.md5(f'{self.serial_number}{self.memory_type}{self.capacity}{self.speed}{self.voltage}{self.latency}{self.manufacturer}')

    @classmethod
    def get_info(cls):
        if OperateSystem.is_windows():
            return cls.__get_from_windows()
        else:
            return cls.__get_from_linux()

    def __str__(self):
        """
        返回内存条的字符串表示
        """
        return f"MemoryModule(memory_type='{self.memory_type}', capacity={self.capacity} MB, frequency={self.speed} MHz, voltage={self.voltage} V, latency={self.latency} CL, form_factor='{self.form_factor}', serial_number='{self.serial_number}')"

    @classmethod
    def __get_from_windows(cls):
        modules = []
        c = wmi.WMI()
        for memory in c.Win32_PhysicalMemory():
            modules.append(cls(serial_number=memory.SerialNumber,
                               memory_type=MemoryType.of_code(memory.MemoryType),
                               capacity=int(memory.Capacity) // (1024 ** 3),  # 将字节转换为GB
                               speed=memory.Speed,
                               voltage=memory.ConfiguredVoltage,
                               form_factor=memory.FormFactor,
                               part_number=memory.PartNumber,
                               bank_label=memory.BankLabel,
                               device_locator=memory.DeviceLocator,
                               data_width=memory.DataWidth,
                                tag=memory.Tag
                               ))

        return modules

    @classmethod
    def __get_from_linux(cls):
        """
        获取当前系统的所有内存条信息，并返回一个包含多个Memory实例的列表
        """
        result = subprocess.run(['sudo', 'dmidecode', '--type', 'memory'], stdout=subprocess.PIPE)
        output = result.stdout.decode()

        modules = []
        for section in output.split('\n\n'):
            memory_type = capacity = frequency = voltage = form_factor = serial_number = None

            for line in section.split('\n'):
                if 'Type:' in line and 'Type Detail:' not in line:
                    memory_type = line.split(':')[-1].strip()
                elif 'Size:' in line and 'No Module Installed' not in line:
                    capacity = int(re.findall(r'\d+', line.split(':')[-1].strip())[0])
                elif 'Speed:' in line:
                    frequency = int(re.findall(r'\d+', line.split(':')[-1].strip())[0])
                elif 'Voltage:' in line:
                    voltage = float(re.findall(r'\d+\.\d+', line.split(':')[-1].strip())[0])
                elif 'Form Factor:' in line:
                    form_factor = line.split(':')[-1].strip()
                elif 'Serial Number:' in line:
                    serial_number = line.split(':')[-1].strip()

            if memory_type and capacity:
                modules.append(MemoryModule(memory_type=memory_type, capacity=capacity, speed=frequency, voltage=voltage,
                                            form_factor=form_factor, serial_number=serial_number))

        return modules

# 示例调用
if __name__ == "__main__":
    modules_ = MemoryModule.get_info()
    for module in modules_:
        print(module)
