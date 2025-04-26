import unittest

import numpy as np

from mag_tools.utils.data.array_utils import ArrayUtils


class TestArrayUtils(unittest.TestCase):
    def test_text_to_array_1d(self):
        # 测试整数数组
        text = "1 2 3 4*2"
        expected_output = [1, 2, 3, 2, 2, 2, 2]
        result = ArrayUtils.text_to_array_1d(text, int).tolist()
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        text = "1.1 2.2 3.3 2*4.4"
        expected_output = [1.1, 2.2, 3.3, 4.4, 4.4]
        result = ArrayUtils.text_to_array_1d(text, float).tolist()
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        text = "true false 2*true"
        expected_output = [True, False, True, True]
        result = ArrayUtils.text_to_array_1d(text, bool).tolist()
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        text = "a b c 2*d"
        expected_output = ["a", "b", "c", "d", "d"]
        result = ArrayUtils.text_to_array_1d(text, str).tolist()
        self.assertEqual(result, expected_output)

        # 测试字符型数组
        text = "1 2.2 true 2*a"
        expected_output = ["1", "2.2", "true", "a", "a"]
        result = ArrayUtils.text_to_array_1d(text, str).tolist()
        self.assertEqual(result, expected_output)

    def test_lines_to_array_1d(self):
        # 测试整数数组
        lines = [
            "1 2 3",
            "4 5 6",
            "7 8 9"
        ]
        expected_output = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = ArrayUtils.lines_to_array_1d(lines, int).tolist()
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        lines = [
            "1.1 2.2 3.3",
            "4.4 5.5 6.6",
            "7.7 8.8 9.9"
        ]
        expected_output = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]
        result = ArrayUtils.lines_to_array_1d(lines, float).tolist()
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        lines = [
            "true false true",
            "false true false"
        ]
        expected_output = [True, False, True, False, True, False]
        result = ArrayUtils.lines_to_array_1d(lines, bool).tolist()
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        lines = [
            "a b c",
            "d e f",
            "g h i"
        ]
        expected_output = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        result = ArrayUtils.lines_to_array_1d(lines, str).tolist()
        self.assertEqual(result, expected_output)

        # 测试混合类型数组
        lines = [
            "1 2.2 true",
            "2*a"
        ]
        expected_output = ['1', '2.2', 'true', 'a', 'a']
        result = ArrayUtils.lines_to_array_1d(lines, str).tolist()
        self.assertEqual(expected_output, result)

    def test_lines_to_array_2d(self):
        # 测试整数数组
        lines = [
            "1 2 3",
            "4 5 6",
            "7 8 9"
        ]
        nx, ny = 3, 3
        expected_output = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        result = ArrayUtils.lines_to_array_2d(lines, nx, ny, int).tolist()
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        lines = [
            "1.1 2.2 3.3",
            "4.4 5.5 6.6",
            "7.7 8.8 9.9"
        ]
        nx, ny = 3, 3
        expected_output = [
            [1.1, 2.2, 3.3],
            [4.4, 5.5, 6.6],
            [7.7, 8.8, 9.9]
        ]
        result = ArrayUtils.lines_to_array_2d(lines, nx, ny, float).tolist()
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        lines = [
            "true false true",
            "false true false"
        ]
        nx, ny = 2, 3
        expected_output = [
            [True, False, True],
            [False, True, False]
        ]
        result = ArrayUtils.lines_to_array_2d(lines, nx, ny, bool).tolist()
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        lines = [
            "a b c",
            "d e f",
            "g h i"
        ]
        nx, ny = 3, 3
        expected_output = [
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"]
        ]
        result = ArrayUtils.lines_to_array_2d(lines, nx, ny, str).tolist()
        self.assertEqual(result, expected_output)

        # 测试混合类型数组
        lines = [
            "1 2.2 true",
            "2*a none"
        ]
        nx, ny = 2, 3
        expected_output = [
            ["1", "2.2", "true"],
            ["a", "a", 'none']  # 由于混合类型，最后一个值可能为 None
        ]
        result = ArrayUtils.lines_to_array_2d(lines, nx, ny, str).tolist()
        self.assertEqual(result, expected_output)

    def test_lines_to_array_3d(self):
        # 测试整数数组
        block_lines = [
            "1 2 3",
            "4 5 6",
            "7 8 9",
            "10 11 12",
            "13 14 15",
            "16 17 18"
        ]
        nx, ny, nz = 2, 3, 3
        expected_output = [
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ],
            [
                [10, 11, 12],
                [13, 14, 15],
                [16, 17, 18]
            ]
        ]
        result = ArrayUtils.lines_to_array_3d(block_lines, nx, ny, nz, int).tolist()
        self.assertEqual(expected_output, result)

        # 测试浮点数数组
        block_lines = [
            "1.1 2.2 3.3",
            "4.4 5.5 6.6",
            "7.7 8.8 9.9",
            "10.1 11.2 12.3",
            "13.4 14.5 15.6",
            "16.7 17.8 18.9"
        ]
        nx, ny, nz = 2, 3, 3
        expected_output = [
            [
                [1.1, 2.2, 3.3],
                [4.4, 5.5, 6.6],
                [7.7, 8.8, 9.9]
            ],
            [
                [10.1, 11.2, 12.3],
                [13.4, 14.5, 15.6],
                [16.7, 17.8, 18.9]
            ]
        ]
        result = ArrayUtils.lines_to_array_3d(block_lines, nx, ny, nz, float).tolist()
        self.assertEqual(expected_output, result)

        # 测试布尔值数组
        block_lines = [
            "true false true",
            "false true false",
            "true true false",
            "false false true",
            "true false true",
            "false true false"
        ]
        nx, ny, nz = 2, 3, 3
        expected_output = [
            [
                [True, False, True],
                [False, True, False],
                [True, True, False]
            ],
            [
                [False, False, True],
                [True, False, True],
                [False, True, False]
            ]
        ]
        result = ArrayUtils.lines_to_array_3d(block_lines, nx, ny, nz, bool).tolist()
        self.assertEqual(expected_output, result)

        # 测试字符串数组
        block_lines = [
            "a b c",
            "d e f",
            "g h i",
            "j k l",
            "m n o",
            "p q r"
        ]
        nx, ny, nz = 2, 3, 3
        expected_output = [
            [
                ["a", "b", "c"],
                ["d", "e", "f"],
                ["g", "h", "i"]
            ],
            [
                ["j", "k", "l"],
                ["m", "n", "o"],
                ["p", "q", "r"]
            ]
        ]
        result = ArrayUtils.lines_to_array_3d(block_lines, nx, ny, nz, str).tolist()
        self.assertEqual(expected_output, result)

    def test_assign_array_2d(self):
        array2d = np.zeros((5, 5))
        ArrayUtils.assign_array_2d(array2d, 1, 3, 1, 3, 10).tolist()
        expected = np.array([[0, 0, 0, 0, 0],
                              [0, 10, 10, 10, 0],
                              [0, 10, 10, 10, 0],
                              [0, 10, 10, 10, 0],
                              [0, 0, 0, 0, 0]])
        np.testing.assert_array_equal(array2d, expected)

    def test_multiply_array_2d(self):
        array2d = np.ones((5, 5))
        ArrayUtils.multiply_array_2d(array2d, 1, 3, 1, 3, 2).tolist()
        expected = np.array([[1, 1, 1, 1, 1],
                              [1, 2, 2, 2, 1],
                              [1, 2, 2, 2, 1],
                              [1, 2, 2, 2, 1],
                              [1, 1, 1, 1, 1]])
        np.testing.assert_array_equal(array2d, expected)

    def test_add_array_2d(self):
        array2d = np.ones((5, 5))
        ArrayUtils.add_array_2d(array2d, 1, 3, 1, 3, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                              [1, 6, 6, 6, 1],
                              [1, 6, 6, 6, 1],
                              [1, 6, 6, 6, 1],
                              [1, 1, 1, 1, 1]])
        np.testing.assert_array_equal(array2d, expected)

    def test_assign_array_3d(self):
        array3d = np.zeros((4, 4, 4))
        ArrayUtils.assign_array_3d(array3d, 1, 2, 1, 2, 1, 2, 10)
        expected = np.zeros((4, 4, 4))
        expected[1:3, 1:3, 1:3] = 10
        np.testing.assert_array_equal(array3d, expected)

    def test_multiply_array_3d(self):
        array3d = np.ones((4, 4, 4))
        ArrayUtils.multiply_array_3d(array3d, 1, 2, 1, 2, 1, 2, 3)
        expected = np.ones((4, 4, 4))
        expected[1:3, 1:3, 1:3] *= 3
        np.testing.assert_array_equal(array3d, expected)

    def test_add_array_3d(self):
        array3d = np.ones((4, 4, 4))
        ArrayUtils.add_array_3d(array3d, 1, 2, 1, 2, 1, 2, 5)
        expected = np.ones((4, 4, 4))
        expected[1:3, 1:3, 1:3] += 5
        np.testing.assert_array_equal(array3d, expected)

    def test_copy_array_3d(self):
        source_array = np.arange(64).reshape((4, 4, 4))
        target_array = np.zeros((4, 4, 4))
        ArrayUtils.copy_array_3d(source_array, target_array, 1, 2, 1, 2, 1, 2)
        expected = np.zeros((4, 4, 4))
        expected[1:3, 1:3, 1:3] = source_array[1:3, 1:3, 1:3]
        np.testing.assert_array_equal(target_array, expected)

    def test_array_1d_to_text(self):
        array = np.array([1.0, 1.0, 2, 2, 2, 3])
        text = ArrayUtils.array_1d_to_text(array)
        print(text)  # 输出: "2*1 3*2 1*3"

    def test_array_2d_to_lines(self):
        # 示例二维数组
        array = np.array([
            [1, 1, 2, 2, 2],
            [3, 4, 4, 5, 5],
            [6, 6, 6, 6, 6]
        ])

        # 转换为文本块
        lines = ArrayUtils.array_2d_to_lines(array)
        print("\n".join(lines))  # 输出每行文本

    def test_array_2d_to_text(self):
        # 示例二维数组
        array = np.array([
            [1, 1, 2, 2, 2],
            [3, 4, 4, 5, 5],
            [6, 6, 6, 6, 6]
        ])

        # 转换为文本块
        text = ArrayUtils.array_2d_to_text(array)
        print(text)  # 输出每行文本

    def test_array_3d_to_lines(self):
        # 示例三维数组
        array = np.array([
            [
                [1, 1, 2, 2],
                [3, 3, 4, 5]
            ],
            [
                [6, 6, 6, 7],
                [8, 9, 9, 9]
            ]
        ])

        # 转换为文本块
        lines = ArrayUtils.array_3d_to_lines(array)
        print("\n".join(lines))  # 打印每行

    def test_array_3d_to_blocks(self):
        # 示例三维数组
        array = np.array([
            [
                [1, 1, 2, 2],
                [2, 3, 3, 5]
            ],
            [
                [6, 6, 6, 7],
                [8, 9, 9, 9]
            ]
        ])

        # 转换为文本块
        lines = ArrayUtils.array_3d_to_blocks(array)
        print("\n".join(lines))  # 打印每行

if __name__ == '__main__':
    unittest.main()




