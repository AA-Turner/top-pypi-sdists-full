import struct
from dataclasses import dataclass, field
from typing import Optional, Union

@dataclass
class ArrayHeader:
    array_type: str = field(metadata={'description': '数据类型，i: 整型；d：双精度'})
    array_name: str = field(metadata={'description': '数组名'})
    unit_name: str = field(metadata={'description': '单位名'})
    max_value: Optional[Union[float, int]] = field(default=None, metadata={'description': '最大值'})
    min_value: Optional[Union[float, int]] = field(default=None, metadata={'description': '最小值'})
    mean_value: Optional[Union[float, int]] = field(default=None, metadata={'description': '均值'})
    time_type: Optional[str] = field(default='d', metadata={'description': '时间类型，d: “YYYYMMDD.x”，t: 浮点时间'})
    dt: Optional[float] = field(default=None, metadata={'description': '日期或时间：类型为d时,整数部分为8位日期，小数部分为0.x天; 为i时，为浮点数时间'})
    reserve: Optional[str] = field(default=None, metadata={'description': "保留"})

    @staticmethod
    def from_bytes(header_bytes):
        dt,array_type,array_name,unit_name,max_value,min_value,mean_value,time_type = struct.unpack(
            '=d1s128s64sddd1s39x', header_bytes)

        return ArrayHeader(dt=dt, array_type=array_type.decode('utf-8'),
                           array_name=array_name.decode('utf-8').strip('\x00'),
                           unit_name=unit_name.decode('utf-8').strip('\x00'),
                           max_value=max_value, min_value=min_value,
                           mean_value=mean_value, time_type=time_type.decode('utf-8'))

    def to_bytes(self):
        return struct.pack(
            '=dB128s64sdddB39x',
            self.dt,
            ord(self.array_type),
            self.array_name.encode('utf-8'),
            self.unit_name.encode('utf-8'),
            self.max_value,
            self.min_value,
            self.mean_value,
            ord(self.time_type)
        )

@dataclass
class Array:
    __header: ArrayHeader = field(metadata={'description': '数组头描述'})
    data: list[Union[float, int]] = field(default_factory=list, metadata={'description': '数据，数组元素为整数或浮点数'})

    @property
    def array_name(self) -> str:
        return self.__header.array_name

    @property
    def array_type(self) -> str:
        return self.__header.array_type

    @property
    def unit_name(self) -> str:
        return self.__header.unit_name

    @property
    def max_value(self) -> Union[float, int]:
        return self.__header.max_value

    @property
    def min_value(self) -> Union[float, int]:
        return self.__header.min_value

    @property
    def mean_value(self) -> Union[float, int]:
        return self.__header.mean_value

    @property
    def time_type(self):
        return self.__header.time_type

    @property
    def time_step(self):
        return self.__header.dt

    @classmethod
    def from_bytes(cls, header: ArrayHeader, array_type: str, array_bytes: bytes):
        data = []
        if array_type == 'd':  # 如果类型为 'd'，则读取 double 数组
            array_format = 'd' * (len(array_bytes) // 8)
            data = struct.unpack(array_format, array_bytes)
        elif array_type == 'i':  # 否则读取 int 数组
            array_format = 'i' * (len(array_bytes) // 4)
            data = struct.unpack(array_format, array_bytes)

        return cls(header, data)

    def to_bytes(self) -> bytes:
        #
        """
        将数组转换为字节数组，包括：数组长度、头信息、数组信息
        :return: byte[]
        """
        # 将头信息转为字节数组
        header_bytes = self.__header.to_bytes()

        # 将数据转换为字节数组
        if self.array_type == 'd':
            array_format = 'd' * len(self.data)
        elif self.array_type == 'i':
            array_format = 'i' * len(self.data)
        else:
            raise ValueError("Unsupported array type")
        array_bytes = struct.pack(array_format, *self.data)

        # 将头信息和数组数据总长度转为字节数组
        total_len = len(array_bytes) + len(header_bytes)
        total_len_bytes = struct.pack('q', total_len)

        return total_len_bytes + header_bytes + array_bytes

    @classmethod
    def load_bin_file(cls, bin_file_path: str) -> list:
        """
        bin_file_path 二进制结果文件
            BIN文件中，多个数组连续排列，所有数组都按同样的二进制格式存储。
            每个数组的第 1 至第 8 字节存储数组长度“len”,不含这8个字节；
            第 8 至第 273 字节存储数组的 header 信息；
            第 274 至第(len+8)字节存储数组本身。
            其中，header信息包括：
                8字节的时间或日期（double格式）
                1字节的数组类型标识
                128字节的数组名
                64字节的的单位名
                8字节的最大值(double)
                8字节的最小值（double）
                8字节的均值
                1字节的时间类型
                39字节保留
        :return: Array[]
        """
        data = []
        with open(bin_file_path, 'rb') as f:
            while True:
                # 读取数组字节长度，包含Header和数组本身的byte数
                len_bytes = f.read(8)
                if not len_bytes:
                    break
                array_len = struct.unpack('Q', len_bytes)[0] - 265

                # 读取 header 信息
                header_bytes = f.read(265)

                # 读取数组本身
                array_bytes = f.read(array_len)

                _header = ArrayHeader.from_bytes(header_bytes)
                _array = cls.from_bytes(_header, _header.array_type, array_bytes)
                data.append(_array)
        return data