from typing import  Optional


class BytesUtils:
    """
    字节数组的工具类
    """
    @staticmethod
    def bytes_to_int(ba: bytes) -> int:
        """
        将byte[]转换为int型
        :param ba: 源byte[]
        :return: int型数值
        """
        value = 0
        for b in ba:
            value = (value << 8) | (b & 0xff)
        return value

    @staticmethod
    def bytes_to_string(ba: bytes, encoding: str = 'UTF-8') -> str:
        """
        把一个字节流转换成指定字符集的字符串
        :param ba: byte[] 字节流
        :param encoding: 字符集
        :return: 返回字符串
        """
        try:
            return ba.decode(encoding)
        except UnicodeDecodeError:
            return ba.decode()

    @staticmethod
    def bytes_to_array(ba: bytes) -> Optional[bytes]:
        """
        将byte数组转换为Byte[]
        :param ba: byte数组
        :return: Byte[]
        """
        return None if ba is None else ba

    @staticmethod
    def get_int_from_bytes(ba: bytes, idx: int) -> int:
        if idx + 4 > len(ba):
            return -1
        ba_int = ba[idx:idx + 4]
        return BytesUtils.bytes_to_int(ba_int)

    @staticmethod
    def get_string_from_bytes(ba: bytes, idx: int, length: int) -> str:
        ba_ret = ba[idx:idx + length]
        return BytesUtils.bytes_to_string(ba_ret)

    @staticmethod
    def get_bytes_from_bytes(ba: bytes, idx: int, length: int) -> bytes:
        ba_ret = ba[idx:idx + length]
        return ba_ret

    @staticmethod
    def int_to_bytes(value: int) -> bytes:
        b = bytearray(4)
        for i in range(4):
            b[3 - i] = value & 0xff
            value >>= 8
        return bytes(b)

    @staticmethod
    def string_to_bytes(value: str, encoding: str = 'UTF-8') -> bytes:
        try:
            return value.encode(encoding)
        except UnicodeEncodeError:
            return value.encode()

    @staticmethod
    def length(value: str, encoding: str = 'UTF-8') -> int:
        ba_stream = BytesUtils.string_to_bytes(value, encoding)
        return len(ba_stream) if ba_stream else -1

    @staticmethod
    def set_int_in_bytes(value: int, ba: bytearray, idx: int):
        if idx + 4 > len(ba):
            return
        ba_int = BytesUtils.int_to_bytes(value)
        ba[idx:idx + 4] = ba_int

    @staticmethod
    def set_string_in_bytes(value: str, ba: bytearray, idx: int, encoding: str = 'UTF-8'):
        ba_value = BytesUtils.string_to_bytes(value, encoding)
        if not value or idx + len(ba_value) > len(ba):
            return
        ba[idx:idx + len(ba_value)] = ba_value

    @staticmethod
    def set_bytes_in_bytes(value: bytes, ba: bytearray, idx: int):
        if not value or idx + len(value) > len(ba):
            return
        ba[idx:idx + len(value)] = value

    @staticmethod
    def link_byte_array(buf1: bytes, buf2: bytes) -> bytes:
        return buf1 + buf2

    @staticmethod
    def get_bytes(array: bytes, start: int, length: int) -> bytes:
        if start + length > len(array):
            length = len(array) - start
        return array[start:start + length]

    @staticmethod
    def bytes_to_hex(data: bytes) -> str:
        return ''.join(f'{b:02X}' for b in data)

    @staticmethod
    def hex_to_bytes(hex_str: str) -> Optional[bytes]:
        if not hex_str or len(hex_str) % 2 != 0:
            return None
        return bytes.fromhex(hex_str)

    @staticmethod
    def merge_bytes(vec_data: list[bytes]) -> Optional[bytes]:
        if not vec_data:
            return None
        return b''.join(vec_data)

    @staticmethod
    def split_stream(data: bytes, block_size: int) -> list[bytes]:
        vec_data = [data[i:i + block_size] for i in range(0, len(data), block_size)]
        return vec_data

    @staticmethod
    def trim_bytes(byte_array: bytes) -> Optional[bytes]:
        if byte_array is None:
            return None
        return byte_array.strip(b' ')

    @staticmethod
    def char_to_byte(c: str) -> int:
        return "0123456789ABCDEF".index(c)
