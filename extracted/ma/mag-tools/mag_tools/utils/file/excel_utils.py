from typing import Any

import pandas as pd


class ExcelUtils:
    @staticmethod
    def clear_empty(df: pd.DataFrame) -> pd.DataFrame:
        """
        清除前面的空白行和左边的空白列
        :param df: Excel文件句柄
        :return: 清除空白行和列后的DataFrame
        """
        df = df.dropna(how='all').reset_index(drop=True)
        df = df.dropna(axis=1, how='all')
        return df

    @staticmethod
    def get_cells_of_row_by_keyword(df: pd.DataFrame, row: int, keyword: str) -> pd.Series:
        """
        获取指定行中匹配关键词的单元格的内容
        :param df: Excel文件句柄
        :param row: 行数
        :param keyword: 内容所包含的关键词
        :return: 指定单元格的内容，返回匹配的所有单元格内容
        """
        row_data = df.iloc[row]
        result = row_data[row_data.astype(str).str.contains(keyword, na=False)]
        result.name = None  # 确保返回的 Series 没有 name 属性
        return result

    @staticmethod
    def get_first_cell_of_row_by_keyword(df: pd.DataFrame, row: int, keyword: str) -> Any:
        """
        获取指定行中匹配关键词的首个单元格的内容
        :param df: Excel文件句柄
        :param row: 行数
        :param keyword: 内容所包含的关键词
        :return: 指定单元格的内容，返回匹配的第一个单元格内容
        """
        matching_columns = ExcelUtils.get_cells_of_row_by_keyword(df, row, keyword)
        return matching_columns.iloc[0] if not matching_columns.empty else None

    @staticmethod
    def delete_row_with_keyword(df: pd.DataFrame, row: int, keyword: str) -> pd.DataFrame:
        """
        删除包含指定关键词的行
        :param df: Excel文件句柄
        :param row: 行数
        :param keyword: 内容所包含的关键词
        :return: 删除指定行后的DataFrame
        """
        if row < len(df) and df.iloc[row].astype(str).str.contains(keyword, na=False).any():
            df = df.drop(index=row).reset_index(drop=True)
        return df

    @staticmethod
    def get_value_from_group(group: pd.DataFrame, column_name: str, default_value: Any = None) -> Any:
        """
        从分组中获取指定列的值
        :param group: 分组后的DataFrame
        :param column_name: 列名
        :param default_value: 默认值
        :return: 指定列的值
        """
        value = default_value
        if column_name in group.columns:
            value_groups = group[column_name].dropna().unique()
            if len(value_groups) > 0:
                value = value_groups[0]
        return value
