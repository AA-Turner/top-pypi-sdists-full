from typing import  Union

import numpy as np

from mag_tools.utils.data.value_utils import ValueUtils


class ArrayUtils:
    """
    数组工具类，在数值计算中通常采用np.ndarray
    """
    @staticmethod
    def text_to_array_1d(text: str, data_type: type) -> np.ndarray:
        """
        从一行文本中获取数值数组[]
        :param text: 文本，由 "数值" 或 "数值个数*数值"构成
        :param data_type: 数据类型
        :return: 数值数组
        """
        data = []

        for part in text.split():
            if '*' in part:
                count, value = part.split('*')
                data.extend([ValueUtils.to_value(value, data_type)] * int(count))
            else:
                data.append(ValueUtils.to_value(part, data_type))

        return np.array(data, dtype=data_type)

    @staticmethod
    def lines_to_array_1d(lines: list[str], data_type: type) -> np.ndarray:
        """
        从多行文本中获取数值数组[]
        :param lines: 文本段，每行由 "数值" 或 "数值个数*数值"构成
        :param data_type: 数据类型
        :return: 数值数组
        """
        array_1d = []
        for line in lines:
            array_1d.extend(ArrayUtils.text_to_array_1d(line, data_type).tolist())
        return np.array(array_1d, dtype=data_type)

    @staticmethod
    def lines_to_array_2d(lines: list[str], nx: int, ny: int, data_type: type) -> np.ndarray:
        """
        从文本块获取数值列表
        :param lines: 文本块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        :param nx: 行数
        :param ny: 列数
        :param data_type: 数据类型
        :return: Values
        """
        array_1d = ArrayUtils.lines_to_array_1d(lines, data_type)

        if len(array_1d) != nx * ny:
            raise ValueError(
                f"Data length mismatch: Expected {nx}*{ny}, but got {len(array_1d)}."
            )
        return array_1d.reshape((nx, ny))

    @staticmethod
    def lines_to_array_3d(block_lines: list[str], nx: int, ny: int, nz: int, data_type: type) -> np.ndarray:
        """
        从文本块获取数值列表
        :param block_lines: 文本块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        :param nx: 层数
        :param ny: 行数
        :param nz: 列数
        :param data_type: 数据类型
        :return: Values
        """
        array_1d = ArrayUtils.lines_to_array_1d(block_lines, data_type)
        return array_1d.reshape((nx, ny, nz))

    @staticmethod
    def assign_array_2d(array2: np.ndarray, i1: int, i2: int, j1: int, j2: int, value: Union[int, float]):
        """
        给数组指定区域的元素赋值
        :param array2: 二维数组
        :param i1: 起始行数
        :param i2: 结束行数
        :param j1: 起始列数
        :param j2: 结束列数
        :param value: 数值
        """
        rows, cols = array2.shape

        if i1 < 0 or j1 < 0 or i2 >= rows or j2 >= cols or i1 > i2 or j1 > j2:
            raise IndexError("Index out of range for the provided 2D array dimensions.")

        array2[i1:i2 + 1, j1:j2 + 1] = value
        return array2

    @staticmethod
    def multiply_array_2d(array2: np.ndarray, i1: int, i2: int, j1: int, j2: int, factor: Union[int, float]):
        """
        给数组指定区域的元素乘以系数
        :param array2: 二维数组
        :param i1: 起始行数
        :param i2: 结束行数
        :param j1: 起始列数
        :param j2: 结束列数
        :param factor: 系数
        """
        rows, cols = array2.shape
        if i1 < 0 or j1 < 0 or i2 >= rows or j2 >= cols or i1 > i2 or j1 > j2:
            raise IndexError("Index out of range for the provided 2D array dimensions.")

        array2[i1:i2 + 1, j1:j2 + 1] *= factor
        return array2

    @staticmethod
    def add_array_2d(array2: np.ndarray, i1: int, i2: int, j1: int, j2: int, value: Union[int, float]):
        """
        给数组指定区域的元素增加数值
        :param array2: 二维数组
        :param i1: 起始行数
        :param i2: 结束行数
        :param j1: 起始列数
        :param j2: 结束列数
        :param value: 数值
        """
        rows, cols = array2.shape
        if i1 < 0 or j1 < 0 or i2 >= rows or j2 >= cols or i1 > i2 or j1 > j2:
            raise IndexError("Index out of range for the provided 2D array dimensions.")

        array2[i1:i2 + 1, j1:j2 + 1] += value
        return array2

    @staticmethod
    def assign_array_3d(array3: np.ndarray, i1: int, i2: int, j1: int, j2: int, k1: int, k2: int, value: Union[float, int]):
        """
        给数组指定区域的元素赋值
        :param array3: 三维数组
        :param i1: 起始层数
        :param i2: 结束层数
        :param j1: 起始行数
        :param j2: 结束行数
        :param k1: 起始列数
        :param k2: 结束列数
        :param value: 数值
        """
        layers, rows, cols = array3.shape
        if i1 < 0 or j1 < 0 or k1 < 0 or i2 >= layers or j2 >= rows or k2 >= cols or i1 > i2 or j1 > j2 or k1 > k2:
            raise IndexError("Index out of range for the provided 3D array dimensions.")

        array3[i1:i2 + 1, j1:j2 + 1, k1:k2 + 1] = value
        return array3

    @staticmethod
    def multiply_array_3d(array3: np.ndarray, i1: int, i2: int, j1: int, j2: int, k1: int, k2: int, factor: Union[int, float]):
        """
        给数组指定区域的元素乘以系数
        :param array3: 三维数组
        :param i1: 起始层数
        :param i2: 结束层数
        :param j1: 起始行数
        :param j2: 结束行数
        :param k1: 起始列数
        :param k2: 结束列数
        :param factor: 系数
        """
        layers, rows, cols = array3.shape
        if i1 < 0 or j1 < 0 or k1 < 0 or i2 >= layers or j2 >= rows or k2 >= cols or i1 > i2 or j1 > j2 or k1 > k2:
            raise IndexError("Index out of range for the provided 3D array dimensions.")

        array3[i1:i2 + 1, j1:j2 + 1, k1:k2 + 1] *= factor
        return array3

    @staticmethod
    def add_array_3d(array3: np.ndarray, i1: int, i2: int, j1: int, j2: int, k1: int, k2: int, value: Union[float,int]):
        """
        给数组指定区域的元素增加数值
        :param array3: 三维数组
        :param i1: 起始层数
        :param i2: 结束层数
        :param j1: 起始行数
        :param j2: 结束行数
        :param k1: 起始列数
        :param k2: 结束列数
        :param value: 数值
        """
        layers, rows, cols = array3.shape
        if i1 < 0 or j1 < 0 or k1 < 0 or i2 >= layers or j2 >= rows or k2 >= cols or i1 > i2 or j1 > j2 or k1 > k2:
            raise IndexError("Index out of range for the provided 3D array dimensions.")

        array3[i1:i2 + 1, j1:j2 + 1, k1:k2 + 1] += value
        return array3

    @staticmethod
    def copy_array_3d(source_array: np.ndarray, target_array: np.ndarray, i1: int, i2: int, j1: int, j2: int, k1: int, k2: int):
        """
        复制源数组指定区域到目标数组
        :param source_array: 源数组
        :param target_array: 目标数组
        :param i1: 起始层数
        :param i2: 结束层数
        :param j1: 起始行数
        :param j2: 结束行数
        :param k1: 起始列数
        :param k2: 结束列数
        """

        src_layers, src_rows, src_cols = source_array.shape
        tgt_layers, tgt_rows, tgt_cols = target_array.shape

        # 检查索引是否超出源数组的范围
        if i1 < 0 or j1 < 0 or k1 < 0 or i2 >= src_layers or j2 >= src_rows or k2 >= src_cols:
            raise IndexError(
                f"Source array index out of range: i1={i1}, i2={i2}, j1={j1}, j2={j2}, k1={k1}, k2={k2}, source_shape={source_array.shape}"
            )

        # 检查索引是否超出目标数组的范围
        if i1 < 0 or j1 < 0 or k1 < 0 or i2 >= tgt_layers or j2 >= tgt_rows or k2 >= tgt_cols:
            raise IndexError(
                f"Target array index out of range: i1={i1}, i2={i2}, j1={j1}, j2={j2}, k1={k1}, k2={k2}, target_shape={target_array.shape}"
            )

        # 检查索引逻辑是否合理 (例如 i1 > i2)
        if i1 > i2 or j1 > j2 or k1 > k2:
            raise ValueError(
                f"Invalid indices: i1={i1}, i2={i2}, j1={j1}, j2={j2}, k1={k1}, k2={k2}. Start index must not be greater than end index."
            )

        target_array[i1:i2 + 1, j1:j2 + 1, k1:k2 + 1] = source_array[i1:i2 + 1, j1:j2 + 1, k1:k2 + 1]
        return target_array

    @staticmethod
    def array_1d_to_text(array_: np.ndarray) -> str:
        """
        将一维数值数组转换为文本,相邻的重复数据采用 m*A的方法
        """
        if not isinstance(array_, np.ndarray) or array_.ndim != 1:
            raise ValueError("输入必须是一维 numpy 数组")

        line, count, prev = [], 1, array_[0]
        for current in array_[1:]:
            if current == prev:
                count += 1
            else:
                line.append(f"{count}*{prev}" if count > 1 else str(prev))
                count, prev = 1, current
        line.append(f"{count}*{prev}" if count > 1 else str(prev))  # 最后一个元素
        return " ".join(line)

    @staticmethod
    def array_2d_to_text(array: np.ndarray) -> str:
        """
        将二维数组转换为文本,相邻的重复数据采用 m*A的方法
        :param array: 二维数组
        :return: 文本
        """
        if not isinstance(array, np.ndarray) or array.ndim != 2:
            raise ValueError("输入必须是二维 numpy 数组")

        return ArrayUtils.array_1d_to_text(array.flatten())

    @staticmethod
    def array_2d_to_lines(array: np.ndarray) -> list[str]:
        """
        将二维数组转换为文本块,相邻的重复数据采用 m*A的方法
        :param array: 二维数组
        :return: 文本块，每行对应一个字符串
        """
        if not isinstance(array, np.ndarray) or array.ndim != 2:
            raise ValueError("输入必须是二维 numpy 数组")

        lines = []
        for row in array:
            lines.append(ArrayUtils.array_1d_to_text(row))

        return lines

    @staticmethod
    def array_3d_to_blocks(array: np.ndarray) -> list[str]:
        """
        将三维数组转换为每层对应的行列表,相邻的重复数据采用 m*A的方法
        :param array: 三维数组
        :return: 每层对应的 str
        """
        if not isinstance(array, np.ndarray) or array.ndim != 3:
            raise ValueError("输入必须是三维 numpy 数组")

        all_layers = []  # 用于存储所有层

        for layer in array:  # 遍历每一层
            layer_text = ArrayUtils.array_2d_to_text(layer)
            all_layers.append(layer_text)  # 将当前层添加到所有层

        return all_layers

    @staticmethod
    def array_3d_to_lines(array: np.ndarray) -> list[str]:
        """
        将三维数组转换为每层对应的行列表,相邻的重复数据采用 m*A的方法
        :param array: 三维数组
        :return: 每层对应的 list[str]
        """
        if not isinstance(array, np.ndarray) or array.ndim != 3:
            raise ValueError("输入必须是三维 numpy 数组")

        all_layers = []  # 用于存储所有层

        for layer in array:  # 遍历每一层
            layer_lines = ArrayUtils.array_2d_to_lines(layer)
            all_layers.extend(layer_lines)  # 将当前层添加到所有层

        return all_layers