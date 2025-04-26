import unittest

from bean.array import Array, ArrayHeader
from mag_tools.format.text_formatter import TextFormatter

from mag_tools.enums.justify_type import JustifyType
from utils.data.list_utils import ListUtils
from utils.data.value_utils import ValueUtils


class TestTextFormat(unittest.TestCase):
    def setUp(self):
        self.format = TextFormatter(
            number_per_line=3,
            justify_type=JustifyType.LEFT,
            at_header='   ',
            decimal_places=3,
            decimal_places_of_zero=3,
            pad_length=None,
            pad_char=' ',
            scientific=False,
            none_default='NA'
        )

    def test_array_1d_to_lines(self):
        text_format = TextFormatter(number_per_line=3, pad_length=0, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_1d = [1, 1, 2, 3, 3, 3]
        expected_output = ['2*1 2   3*3']
        text_format.merge_duplicate = True
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        array_1d = [1.1, 1.1, 2.2, 3.3, 3.3, 3.3]
        expected_output = ['2*1.1 2.2   3*3.3']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        array_1d = [True, True, False, True, True, True]
        expected_output = ['2*True False  3*True']
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        array_1d = ['a', 'a', 'b', 'c', 'c', 'c']
        expected_output = ['a a b', 'c c c']
        text_format.merge_duplicate = False
        result = text_format.array_1d_to_lines(array_1d)
        self.assertEqual(result, expected_output)

    def test_array_2d_to_lines(self):
        text_format = TextFormatter(number_per_line=3, pad_length=0, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_2d = [
            [1, 1, 2],
            [3, 3, 3]
        ]
        expected_output = ['2*1 2   3*3']
        text_format.group_by_layer = False
        text_format.merge_duplicate = True
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        expected_output = ['2*1 2  ','3*3']
        text_format.group_by_layer = True
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试浮点数数组
        array_2d = [
            [1.1, 1.1, 2.2],
            [3.3, 3.3, 3.3]
        ]
        expected_output = ['2*1.1 2.2   3*3.3']
        text_format.group_by_layer = False
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        expected_output = ['2*1.1 2.2  ', '3*3.3']
        text_format.group_by_layer = True
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试布尔值数组
        array_2d = [
            [True, True, False],
            [True, True, True]
        ]
        expected_output = ['2*True False  3*True']
        text_format.group_by_layer = False
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        expected_output = ['2*True False ', '3*True']
        text_format.group_by_layer = True
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        # 测试字符串数组
        array_2d = [
            ['a', 'a', 'b'],
            ['c', 'c', 'c']
        ]
        expected_output = ['a a b', 'c c c']
        text_format.group_by_layer = False
        text_format.merge_duplicate = False
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

        expected_output = ['a a b', 'c c c']
        text_format.group_by_layer = True
        result = text_format.array_2d_to_lines(array_2d)
        self.assertEqual(result, expected_output)

    def test_array_3d_to_lines(self):
        text_format = TextFormatter(number_per_line=4, pad_length=0, justify_type=JustifyType.LEFT)

        # 测试整数数组
        array_3d = [
            [
                [1, 1, 2],
                [2, 3, 3]
            ],
            [
                [4, 4, 5],
                [5, 6, 6]
            ]
        ]
        text_format.group_by_layer = False
        text_format.merge_duplicate = True
        expected_output = ['2*1 2*2 2*3 2*4','2*5 2*6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        text_format.group_by_layer = True
        expected_output = ['2*1 2*2 2*3', '2*4 2*5 2*6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        text_format.merge_duplicate = False
        expected_output = ['1 1 2 2', '3 3', '4 4 5 5', '6 6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试浮点数数组
        array_3d = [
            [
                [1.1, 1.1, 2.2],
                [3.3, 3.3, 3.3]
            ],
            [
                [4.4, 4.4, 5.5],
                [6.6, 6.6, 6.6]
            ]
        ]
        text_format.merge_duplicate = True
        text_format.group_by_layer = False
        expected_output = ['2*1.1 2.2   3*3.3 2*4.4','5.5   3*6.6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        text_format.group_by_layer = True
        expected_output = ['2*1.1 2.2   3*3.3', '2*4.4 5.5   3*6.6']
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试布尔值数组
        array_3d = [
            [
                [True, True, False],
                [True, True, True]
            ],
            [
                [False, False, True],
                [False, False, False]
            ]
        ]
        expected_output = ['2*True  False   3*True  2*False', 'True    3*False']
        text_format.group_by_layer = False
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        expected_output = ['2*True  False   3*True ', '2*False True    3*False']
        text_format.group_by_layer = True
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        # 测试字符串数组
        array_3d = [
            [
                ['a', 'a', 'b'],
                ['c', 'c', 'c']
            ],
            [
                ['d', 'd', 'e'],
                ['f', 'f', 'f']
            ]
        ]
        expected_output = ['a a b c', 'c c d d', 'e f f f']
        text_format.group_by_layer = False
        text_format.merge_duplicate = False
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

        expected_output = ['a a b c', 'c c', 'd d e f', 'f f']
        text_format.group_by_layer = True
        result = text_format.array_3d_to_lines(array_3d)
        self.assertEqual(expected_output, result)

    def test_arrays_to_lines(self):
        str_ = '''
XCOORD       ft          7050          7050          7050          7050          7050          7050
YCOORD       ft          7350          7350          7350          7350          7350          7350
 DEPTH       ft          9110      10378.16      10396.66      10415.66      10450.66      10525.66
 STAGE  integer             0             0             0             0             0             0
OUTLET  integer            -1             0             1             2             3             4    
            '''

        arrays = []
        # 解析数据块，每行为一个数组，由若干数组组成。格式：数组名、单位和数据
        block_lines = ListUtils.trim(str_.splitlines())
        for line in block_lines:
            items = line.split()
            if items[0] in {'XCOORD', 'YCOORD', 'DEPTH'}:
                array_type = 'd'
            else:
                array_type = 'i'

            head = ArrayHeader(array_type=array_type, array_name=items[0], unit_name=items[1])
            data = [ValueUtils.to_value(value, float) if array_type == 'd' else int(value) for value in items[2:]]
            arrays.append(Array(head, data))

        lines = TextFormatter().arrays_to_lines(arrays)
        print('\n'.join(lines))