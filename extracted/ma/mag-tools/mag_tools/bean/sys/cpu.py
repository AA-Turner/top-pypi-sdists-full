import re
import subprocess
from dataclasses import dataclass, field
from typing import Optional

import wmi

from mag_tools.bean.base_data import BaseData
from mag_tools.utils.security.digest import Digest
from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.enums.cpu_series import CpuSeries


@dataclass
class Cpu(BaseData):
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    serial_number: Optional[str] = field(default=None, metadata={"description": "序列号"})
    name: Optional[str] = field(default=None, metadata={"description": "名称"})
    cpu_type: Optional[str] = field(default=None, metadata={"description": "CPU类型"})
    cpu_series: Optional[CpuSeries] = field(default=None, metadata={"description": "CPU系列"})
    cores: Optional[int] = field(default=None, metadata={"description": "核心数量（物理核心）:等于性能核心+能效核心"})
    logic_cores: Optional[int] = field(default=None, metadata={"description": "逻辑核心数量"})
    threads: Optional[int] = field(default=None, metadata={"description": "线程数量"})
    base_clock: Optional[float] = field(default=None, metadata={"description": "基础频率（单位：GHz）"})
    boost_clock: Optional[float] = field(default=None, metadata={"description": "最大睿频（单位：GHz）"})
    cache_l2: Optional[int] = field(default=None, metadata={"description": "缓存大小L2（单位：MB）"})
    cache_l3: Optional[int] = field(default=None, metadata={"description": "缓存大小L3（单位：MB）"})
    tdp: Optional[int] = field(default=None, metadata={"description": "热设计功耗（单位：W）"})
    process: Optional[int] = field(default=None, metadata={"description": "制造工艺（单位：nm）"})
    architecture: Optional[str] = field(default=None, metadata={"description": "架构类型"})
    model: Optional[str] = field(default=None, metadata={"description": "型号"})
    min_freq: Optional[str] = field(default=None, metadata={"description": "最小频率"})
    max_freq: Optional[str] = field(default=None, metadata={"description": "最大频率"})

    @property
    def hash(self):
        return Digest.md5(f'{self.serial_number}{self.name}{self.cpu_type}{self.cpu_series}{self.cores}{self.logic_cores}'
                          f'{self.threads}{self.base_clock}{self.boost_clock}{self.cache_l2}{self.cache_l3}{self.tdp}{self.process}'
                          f'{self.architecture}{self.model}{self.min_freq}{self.max_freq}')

    @classmethod
    def get_info(cls):
        """
        获取当前系统的CPU信息，并返回一个Cpu实例
        """
        if OperateSystem.is_windows():
            return cls.__get_from_windows()
        elif OperateSystem.is_linux():
            return cls.__get_from_linux()
        return None

    @classmethod
    def __get_from_windows(cls):
        """
        从 Windows 系统获取 CPU 信息
        """
        c = wmi.WMI()
        cpu_info = c.Win32_Processor()[0]

        cpu_series, model = cls.__parse_brand_raw(cpu_info.Name.strip())

        return cls(
            serial_number=cpu_info.ProcessorId.strip(),
            name=cpu_info.Name.strip(),
            cpu_type=cpu_info.ProcessorType,
            cpu_series=cpu_series,
            base_clock=float(cpu_info.MaxClockSpeed) / 1000,  # 转换为 GHz
            boost_clock=float(cpu_info.MaxClockSpeed) / 1000,  # 转换为 GHz
            cores=cpu_info.NumberOfCores,
            threads=cpu_info.ThreadCount,
            architecture=cpu_info.Architecture,
            cache_l2=cpu_info.L2CacheSize,
            cache_l3=cpu_info.L3CacheSize,
            model=model
        )

    @classmethod
    def __get_from_linux(cls):
        """
        从 Linux 系统获取 CPU 信息
        """
        try:
            result = subprocess.run(["lscpu"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            info = {}
            for line in result.stdout.split("\n"):
                if "Model name:" in line:
                    info["name"] = line.split(":")[1].strip()
                elif "Architecture:" in line:
                    info["architecture"] = line.split(":")[1].strip()
                elif "CPU(s):" in line:
                    info["threads"] = int(line.split(":")[1].strip())
                elif "Core(s) per socket:" in line:
                    info["cores"] = int(line.split(":")[1].strip())
                elif "CPU MHz:" in line:
                    info["base_clock"] = float(line.split(":")[1].strip()) / 1000  # 转换为 GHz
                elif "BogoMIPS:" in line:
                    info["boost_clock"] = float(line.split(":")[1].strip()) / 1000  # 转换为 GHz
                elif "L2 cache:" in line:
                    info["cache_l2"] = int(line.split(":")[1].strip().replace("K", ""))  # 转换为 KB
                elif "L3 cache:" in line:
                    info["cache_l3"] = int(line.split(":")[1].strip().replace("K", ""))  # 转换为 KB
                elif "Vendor ID:" in line:
                    info["cpu_type"] = line.split(":")[1].strip()
                elif "Model:" in line:
                    info["enums"] = line.split(":")[1].strip()

            cpu_series, model = cls.__parse_brand_raw(info.get("name"))

            return cls(
                name=info.get("name"),
                cpu_type=info.get("cpu_type"),
                cpu_series=cpu_series,
                base_clock=info.get("base_clock"),
                boost_clock=info.get("boost_clock"),
                cores=info.get("cores"),
                threads=info.get("threads"),
                architecture=info.get("architecture"),
                cache_l2=info.get("cache_l2"),
                cache_l3=info.get("cache_l3"),
                model=model
            )
        except subprocess.CalledProcessError as e:
            print(f"Error getting CPU information: {e}")
            return cls()

    @classmethod
    def __parse_brand_raw(cls, brand_raw: Optional[str] = None):
        """
        从字符串中提取CPU参数并创建CPUParameters实例
        """
        pattern = r"(?P<generation>\d+th Gen)?\s*(?P<brand>Intel\(R\) Core\(TM\)|AMD Ryzen)\s*(?P<series>i\d|Ryzen \d{3,4}X?)-?(?P<enums>\d+K?)?"

        match = re.match(pattern, brand_raw)
        if match:
            cpu_series = CpuSeries.of_code(match.group('series'))
            model = match.group("enums")
            return cpu_series, model
        return None, None

if __name__ == '__main__':
    cpu = Cpu.get_info()
    print(cpu)
