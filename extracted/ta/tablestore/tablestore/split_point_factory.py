# -*- coding: utf8 -*-
"""
内部分区点生成工具类

用于生成预分区建表时的分区点，仅供内部使用。
"""

from tablestore.error import OTSClientError


class SplitPointFactory:
    """
    内部分区点生成工具类
    
    提供静态方法用于生成数字类型和十六进制字符串类型的分区点。
    所有方法均为内部方法（下划线前缀），不对外暴露。
    """
    
    _DEFAULT_MAX_LENGTH = 8
    
    @staticmethod
    def _get_digit(point_count, begin, end):
        """
        生成数字类型的分区点
        
        :param point_count: 分区点数量，必须大于0
        :param begin: 范围起始值（包含）
        :param end: 范围结束值（包含）
        :return: 分区点列表（整数列表）
        
        例如：_get_digit(3, 0, 999) 返回 [250, 500, 750]
        """
        if point_count <= 0:
            raise OTSClientError("The number of point_count must be greater than 0.")
        
        # end + 1 因为区间是左闭右开的
        end_exclusive = end + 1
        range_size = (end_exclusive - begin) / (point_count + 1)
        
        if range_size < 1:
            max_points = end - begin
            raise OTSClientError(
                "When you try to set the split points for the interval [{}, {}], "
                "you can set up to {} split points, currently {}.".format(
                    begin, end, max_points, point_count
                )
            )
        
        points = []
        point = begin
        for i in range(point_count):
            point += range_size
            points.append(int(point))
        
        return points
    
    @staticmethod
    def _get_hex_value(point_count, point_length):
        """
        生成十六进制字符串分区点的基础方法
        
        :param point_count: 分区点数量，必须大于0
        :param point_length: 十六进制字符串长度，必须大于0
        :return: 十六进制字符串列表
        """
        if point_count <= 0 or point_length <= 0:
            raise OTSClientError(
                "The number of point_count and point_length must be greater than 0."
            )
        
        # 计算范围：0 到 16^point_length - 1
        end_value = (1 << (4 * point_length)) - 1  # 16^point_length - 1
        begin_value = 0
        
        # 每个分区的大小
        range_size = (end_value - begin_value + 1) // (point_count + 1)
        
        if range_size == 0:
            max_points = (1 << (4 * point_length)) - 1
            raise OTSClientError(
                "When the length of hex string is {}, you can set up to {} split points, "
                "currently {}.".format(point_length, max_points, point_count)
            )
        
        points = []
        for i in range(point_count):
            # 计算分区点位置
            point_value = (end_value - begin_value + 1) * (i + 1) // (point_count + 1)
            # 格式化为十六进制字符串，补零到指定长度
            hex_str = format(point_value, 'x').zfill(point_length)
            points.append(hex_str)
        
        return points
    
    @staticmethod
    def _get_lower_hex_string(point_count, point_length):
        """
        生成小写十六进制字符串分区点
        
        :param point_count: 分区点数量
        :param point_length: 十六进制字符串长度
        :return: 小写十六进制字符串列表
        
        例如：_get_lower_hex_string(3, 8) 返回 ['40000000', '80000000', 'c0000000']
        """
        return SplitPointFactory._get_hex_value(point_count, point_length)
    
    @staticmethod
    def _get_upper_hex_string(point_count, point_length):
        """
        生成大写十六进制字符串分区点
        
        :param point_count: 分区点数量
        :param point_length: 十六进制字符串长度
        :return: 大写十六进制字符串列表
        
        例如：_get_upper_hex_string(3, 8) 返回 ['40000000', '80000000', 'C0000000']
        """
        hex_points = SplitPointFactory._get_hex_value(point_count, point_length)
        return [p.upper() for p in hex_points]
    
    @staticmethod
    def _get_binary(point_count, byte_length):
        """
        生成二进制分区点，在完整字节范围内均匀分布
        
        :param point_count: 分区点数量，必须大于0
        :param byte_length: 每个分区点的字节长度，范围 1-1024
        :return: 二进制分区点列表（bytes 列表），严格递增
        :raises OTSClientError: 参数非法时抛出
        
        例如：_get_binary(3, 4) 返回 [b'\x40\x00\x00\x00', b'\x80\x00\x00\x00', b'\xc0\x00\x00\x00']
        """
        # 参数校验
        if point_count <= 0:
            raise OTSClientError("The number of point_count must be greater than 0.")
        if byte_length <= 0:
            raise OTSClientError("byte_length must be greater than 0.")
        if byte_length > 1024:
            raise OTSClientError("byte_length must not exceed 1024 bytes.")
        
        # 计算最大值：byte_length 字节能表示的最大无符号整数
        # 例如：4字节 = 0xFFFFFFFF = 4294967295
        max_value = (1 << (byte_length * 8)) - 1
        
        # 计算步长：将范围分成 point_count+1 等份
        # 例如：3个分区点，分4份，步长 = 总范围 / 4
        step = (max_value + 1) // (point_count + 1)
        if step == 0:
            raise OTSClientError(
                "When byte_length is {}, you can set up to {} split points, "
                "currently {}.".format(byte_length, max_value, point_count)
            )
        
        # 生成分区点：位于每个分段边界处
        split_points = []
        for i in range(1, point_count + 1):
            value = i * step
            # 转换为指定长度的字节数组，大端序
            bytes_value = value.to_bytes(byte_length, byteorder='big')
            split_points.append(bytes_value)
        
        return split_points
