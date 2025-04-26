import unittest

from mag_tools.utils.data.list_utils import ListUtils


class TestListUtils(unittest.TestCase):
    def setUp(self):
        # 测试数据
        self.lines = [
            "This is the first line.",
            "A line with the keyword.",
            "Another line with another keyword.",
            "Final line with nothing."
        ]
        self.keyword = "keyword"
        self.keywords = ["first", "keyword", "nothing"]
        
    def test_pick_head(self):
        # 测试数据
        lines = [
            "Line 1",
            "Line 2",
            "Keyword Line",
            "Line 3",
            "Line 4"
        ]
        keyword = "Keyword Line"

        # 期望结果
        expected_result = [
            "Line 1",
            "Line 2"
        ]

        # 执行测试
        result =ListUtils.pick_head(lines, keyword)
        self.assertEqual(result, expected_result)

    def test_split(self):
        # 示例用法
        input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 3
        result = ListUtils.split(input_list, n)
        print(result)  # 输出: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_remove_keyword(self):
        lines = ["apple pie", "banana split", "cherry tart", "crumble apple"]
        expected_result = ["banana split", "cherry tart"]
        self.assertEqual(
            ListUtils.remove_by_keyword(lines, "apple"),
            expected_result
        )

    def test_remove_keyword_at_head(self):
        lines = ["apple pie", "apple crumble", "banana split", "cherry tart"]
        expected_result = ["banana split", "cherry tart"]
        self.assertEqual(
            ListUtils.remove_by_header(lines, "apple"),
            expected_result
        )

    def test_split_by_keyword(self):
        lines = [
            "This is test line 1.",
            "This is test line 2.",
            "Keyword",
            "Another test line 1.",
            "Another test line 2.",
            "Keyword",
            "Final test line 1.",
            "Final test line 2."
        ]
        expected_output_head = [
            ["This is test line 1.",
             "This is test line 2."],
            ["Keyword",
             "Another test line 1.",
             "Another test line 2."],
            ["Keyword",
             "Final test line 1.",
             "Final test line 2."]
        ]
        expected_output_end = [
            ["This is test line 1.",
             "This is test line 2.",
             "Keyword"],
            ["Another test line 1.",
             "Another test line 2.",
             "Keyword"],
            ["Final test line 1.",
             "Final test line 2."]
        ]
        keyword = "Keyword"

        result_head = ListUtils.split_by_keyword(lines, keyword)
        self.assertEqual(result_head, expected_output_head)

        result_end = ListUtils.split_by_keyword(lines, keyword, False)
        self.assertEqual(result_end, expected_output_end)

    def test_split_by_keywords(self):
        lines = [
            "apple",
            "apple is red",
            "apple pie is delicious",
            "banana",
            "banana is yellow",
            "banana split is tasty",
            "cherry",
            "cherry is red",
            "date is brown"
        ]
        keywords = ["apple", "banana", "cherry"]

        expected_output = {
            "apple": [
                "apple",
                "apple is red",
                "apple pie is delicious"
            ],
            "banana": [
                "banana",
                "banana is yellow",
                "banana split is tasty"
            ],
            "cherry": [
                "cherry",
                "cherry is red",
                "date is brown"
            ]
        }
        result = ListUtils.split_by_keywords(lines, keywords)
        self.assertEqual(result, expected_output)

        keyword_map = {"apple": (None, None), "banana": (None, None), "cherry": (None, None)}
        result = ListUtils.split_by_boundary(lines, keyword_map)
        self.assertEqual(result, expected_output)

    def test_split_by_empty_line(self):
        lines = [
            "This is test line 1.",
            "This is test line 2.",
            "",
            "Another test line 1.",
            "Another test line 2.",
            "",
            "Final test line 1.",
            "Final test line 2."
        ]
        expected_output = [
            ["This is test line 1.",
             "This is test line 2."],
            ["Another test line 1.",
             "Another test line 2."],
            ["Final test line 1.",
             "Final test line 2."]
        ]
        result1 = ListUtils.split_by_empty_line(lines)
        self.assertEqual(expected_output, result1)

        result2 = ListUtils.split_by_keyword(lines)
        self.assertEqual(expected_output, result2)

    def test_trim(self):
        # 测试用例 1：起始和结尾都有空行
        lines = [
            "",
            "Line 1",
            "Line 2",
            "",
            "Line 3",
            ""
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 2：只有起始有空行
        lines = [
            "",
            "",
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 3：只有结尾有空行
        lines = [
            "Line 1",
            "Line 2",
            "Line 3",
            "",
            ""
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 4：没有空行
        lines = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 5：全是空行
        lines = [
            "",
            "",
            ""
        ]
        expected_output = []
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

    def test_clear_empty(self):
        # 测试数据
        test_data = [
            "Hello",
            " ",
            [],
            ["World"],
            {},
            {"key": "value"},
            {"another_key": "another_value"},
            set(),
            {"set_value"},
            (),
            ("tuple_value",),
            None
        ]
        # 期望结果
        expected_result = [
            "Hello",
            "World",
            "value",
            "another_value",
            "set_value",
            "tuple_value"
        ]
        # 执行测试
        result = ListUtils.clear_empty(test_data)
        self.assertEqual(result, expected_result)

    def test_pick_line_by_keyword(self):
        # 测试单个关键字匹配的行
        result = ListUtils.pick_line_by_keyword(self.lines, self.keyword)
        self.assertEqual(result, "A line with the keyword.")

    def test_pick_line_by_any_keyword(self):
        # 测试多个关键字的匹配行
        result = ListUtils.pick_line_by_any_keyword(self.lines, self.keywords)
        self.assertEqual(result, "This is the first line.")

    def test_pick_block_include_keyword(self):
        # 测试返回所有包含某关键字的行
        result = ListUtils.pick_block_include_keyword(self.lines, self.keyword)
        self.assertEqual(result, ["A line with the keyword.", "Another line with another keyword."])

    def test_pick_block_include_keywords(self):
        # 测试返回所有包含任意关键字的行
        result = ListUtils.pick_block_include_keywords(self.lines, self.keywords)
        self.assertEqual(result, [
            "This is the first line.",
            "A line with the keyword.",
            "Another line with another keyword.",
            "Final line with nothing."
        ])

    def test_pick_block_by_keyword(self):
        # 测试匹配关键字所在行及后续行的范围
        result = ListUtils.pick_block_by_keyword(self.lines, self.keyword, count=2)
        self.assertEqual(result, [
            "A line with the keyword.",
            "Another line with another keyword."
        ])

        # 测试没有足够行数时的情况
        result = ListUtils.pick_block_by_keyword(self.lines, "nothing", count=2)
        self.assertIsNone(result)

        # 测试关键字不存在时的情况
        result = ListUtils.pick_block_by_keyword(self.lines, "not_found")
        self.assertIsNone(result)

    def test_split_by_boundary(self):
        # 示例用法
        data = """MODELTYPE BlackOil
        FIELD

        GRID
        ##################################################
        DIMENS
         5 2 1
        #GRID END#########################################

        WELL
        ##################################################

        TEMPLATE
        'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /
        WELSPECS
        NAME 'INJE1'
        ''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA  

        NAME 'PROD2'
        ''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA 
        #WELL END#########################################

        PROPS
        ##################################################
        SWOF
        #           Sw         Krw       Krow       Pcow(=Po-Pw)
               0.15174           0     0.99993      257.92

        #PROPS END########################################

        SOLUTION
        ##################################################

        EQUILPAR
        # Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
          9035       3600      9950        0.0         2
        # GOC       GOC_pc
          8800        0.0    
        PBVD
           5000        3600

        #SOLUTION END######################################
        POIL AVG Reg 2 /
        """
        keyword_map = {
            "BASE": (None, None),
            "GRID": (
                "##################################################", "#GRID END#########################################"),
            "WELL": (
                "##################################################", "#WELL END#########################################"),
            "PROPS": (
                "##################################################", "#PROPS END########################################"),
            "SOLUTION": ("##################################################",
                         "#SOLUTION END######################################"),
            "TUNE": (None, None)
        }
        lines = data.splitlines()
        lines.insert(0, "BASE")
        _segments = ListUtils.split_by_boundary(lines, keyword_map)

        for segment_name, segment in _segments.items():
            print(f"Segment: {segment_name}")
            for line in segment:
                print(f"    {line}")
            print()


if __name__ == '__main__':
    unittest.main()