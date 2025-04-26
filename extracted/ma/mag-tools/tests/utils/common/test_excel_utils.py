import unittest
import pandas as pd
from mag_tools.utils.file.excel_utils import ExcelUtils


class TestExcelUtils(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'A': [None, None, None, None],
            'B': [None, 2, None, 4],
            'C': [None, None, None, None],
            'D': ['apple', 'banana', 'cherry', 'date']
        })

    def test_clear_empty(self):
        df = ExcelUtils.clear_empty(self.df)
        expected_output = pd.DataFrame({
            'B': [None, 2, None, 4],
            'D': ['apple', 'banana', 'cherry', 'date']
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(df, expected_output)

    def test_get_cells_of_row_by_keyword(self):
        result = ExcelUtils.get_cells_of_row_by_keyword(self.df, 3, 'a')
        expected_output = pd.Series(['date'], index=['D'])
        expected_output.name = None  # 确保预期输出没有 name 属性
        pd.testing.assert_series_equal(result, expected_output)

    def test_get_first_cell_of_row_by_keyword(self):
        result = ExcelUtils.get_first_cell_of_row_by_keyword(self.df, 3, 'a')
        self.assertEqual(result, 'date')

    def test_delete_row_with_keyword(self):
        df = ExcelUtils.delete_row_with_keyword(self.df, 3, 'a')
        expected_output = pd.DataFrame({
            'A': [None, None, None],
            'B': [None, 2, None],
            'C': [None, None, None],
            'D': ['apple', 'banana', 'cherry']
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(df, expected_output)

    def test_get_value_from_group(self):
        group = self.df.groupby('D').get_group('banana')
        result = ExcelUtils.get_value_from_group(group, 'B', default_value='default')
        self.assertEqual(2, result)


if __name__ == '__main__':
    unittest.main()
