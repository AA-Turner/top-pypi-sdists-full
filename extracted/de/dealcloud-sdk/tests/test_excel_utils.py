"""Tests for Excel utility functions."""

import pytest
import pandas as pd
from pathlib import Path

from dealcloud_sdk.utils.excel_utils import (
    sanitize_sheet_name,
    sanitize_cell_value,
    sanitize_dataframe,
    export_to_excel,
    export_with_formatting,
    create_data_validation_dropdown,
    read_excel_sheets,
    append_to_excel,
    ILLEGAL_CHARACTERS_RE,
    INVALID_SHEET_NAME_CHARS,
    MAX_SHEET_NAME_LENGTH,
)


class TestSanitizeSheetName:
    """Tests for sanitize_sheet_name function."""
    
    def test_removes_invalid_characters(self):
        """Test that invalid characters are removed."""
        assert sanitize_sheet_name("Data: Q1/Q2 [2024]") == "Data Q1Q2 2024"
    
    def test_truncates_to_max_length(self):
        """Test truncation to max length."""
        long_name = "A" * 50
        result = sanitize_sheet_name(long_name)
        assert len(result) == MAX_SHEET_NAME_LENGTH
    
    def test_custom_max_length(self):
        """Test custom max length."""
        result = sanitize_sheet_name("Hello World Test", max_length=10)
        assert len(result) == 10
    
    def test_normal_name_unchanged(self):
        """Test that normal names are unchanged."""
        assert sanitize_sheet_name("Data") == "Data"


class TestSanitizeCellValue:
    """Tests for sanitize_cell_value function."""
    
    def test_removes_control_characters(self):
        """Test removal of control characters."""
        value = "Hello\x00World\x01Test"
        result = sanitize_cell_value(value)
        assert "\x00" not in result
        assert "\x01" not in result
    
    def test_non_string_unchanged(self):
        """Test that non-strings are unchanged."""
        assert sanitize_cell_value(123) == 123
        assert sanitize_cell_value(None) is None
        assert sanitize_cell_value(3.14) == 3.14
    
    def test_normal_string_unchanged(self):
        """Test that normal strings are unchanged."""
        assert sanitize_cell_value("Hello World") == "Hello World"


class TestSanitizeDataframe:
    """Tests for sanitize_dataframe function."""
    
    def test_sanitizes_all_strings(self):
        """Test that all string values are sanitized."""
        df = pd.DataFrame({
            "A": ["Hello\x00", "World"],
            "B": [1, 2],
        })
        result = sanitize_dataframe(df)
        assert "\x00" not in result["A"].iloc[0]
    
    def test_preserves_non_strings(self):
        """Test that non-string values are preserved."""
        df = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [1.1, 2.2, 3.3],
        })
        result = sanitize_dataframe(df)
        assert list(result["A"]) == [1, 2, 3]


class TestExportToExcel:
    """Tests for export_to_excel function."""
    
    def test_export_single_dataframe(self, tmp_path):
        """Test exporting a single DataFrame."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
        output_path = tmp_path / "test.xlsx"
        
        result = export_to_excel(df, output_path)
        
        assert result == output_path
        assert output_path.exists()
    
    def test_export_multiple_sheets(self, tmp_path):
        """Test exporting multiple sheets."""
        data = {
            "Sheet1": pd.DataFrame({"A": [1, 2]}),
            "Sheet2": pd.DataFrame({"B": [3, 4]}),
        }
        output_path = tmp_path / "multi.xlsx"
        
        result = export_to_excel(data, output_path)
        
        assert result == output_path
        assert output_path.exists()
        
        # Verify both sheets exist
        sheets = read_excel_sheets(output_path)
        assert "Sheet1" in sheets
        assert "Sheet2" in sheets
    
    def test_export_with_sanitization(self, tmp_path):
        """Test that data is sanitized by default."""
        df = pd.DataFrame({"A": ["Hello\x00", "World"]})
        output_path = tmp_path / "sanitized.xlsx"
        
        export_to_excel(df, output_path)
        
        # Read back and verify sanitization
        result = pd.read_excel(output_path, engine='openpyxl')
        assert "\x00" not in result["A"].iloc[0]
    
    def test_export_without_sanitization(self, tmp_path):
        """Test export with sanitize=False."""
        df = pd.DataFrame({"A": ["Hello", "World"]})
        output_path = tmp_path / "no_sanitize.xlsx"
        
        result = export_to_excel(df, output_path, sanitize=False)
        
        assert result == output_path
        assert output_path.exists()


class TestExportWithFormatting:
    """Tests for export_with_formatting function."""
    
    def test_basic_export(self, tmp_path):
        """Test basic formatted export."""
        df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
        output_path = tmp_path / "formatted.xlsx"
        
        result = export_with_formatting(df, output_path)
        
        assert result == output_path
        assert output_path.exists()
    
    def test_export_with_column_widths(self, tmp_path):
        """Test export with column widths."""
        df = pd.DataFrame({"Name": ["Alice"], "Description": ["Long text"]})
        output_path = tmp_path / "widths.xlsx"
        
        result = export_with_formatting(
            df, output_path,
            column_widths={"Name": 30, "Description": 50}
        )
        
        assert result == output_path
    
    def test_export_with_column_index_widths(self, tmp_path):
        """Test export with column index widths."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        output_path = tmp_path / "index_widths.xlsx"
        
        result = export_with_formatting(
            df, output_path,
            column_widths={0: 20, 1: 30}
        )
        
        assert result == output_path
    
    def test_export_with_header_style(self, tmp_path):
        """Test export with header styling."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        output_path = tmp_path / "styled.xlsx"
        
        result = export_with_formatting(
            df, output_path,
            header_style={
                'bold': True,
                'fill_color': 'CCCCCC',
                'alignment': {'horizontal': 'center'}
            }
        )
        
        assert result == output_path

    def test_export_header_style_fill_color_only(self, tmp_path):
        df = pd.DataFrame({"A": [1]})
        output_path = tmp_path / "fill_only.xlsx"
        result = export_with_formatting(
            df, output_path, header_style={"fill_color": "FF0000"}
        )
        assert result == output_path

    def test_export_header_style_alignment_only(self, tmp_path):
        df = pd.DataFrame({"A": [1]})
        output_path = tmp_path / "align_only.xlsx"
        result = export_with_formatting(
            df,
            output_path,
            header_style={"alignment": {"horizontal": "center"}},
        )
        assert result == output_path

    def test_export_header_style_bold_only(self, tmp_path):
        df = pd.DataFrame({"A": [1]})
        output_path = tmp_path / "bold_only.xlsx"
        result = export_with_formatting(df, output_path, header_style={"bold": False})
        assert result == output_path
    
    def test_export_without_freeze_panes(self, tmp_path):
        """Test export without freeze panes."""
        df = pd.DataFrame({"A": [1]})
        output_path = tmp_path / "no_freeze.xlsx"
        
        result = export_with_formatting(df, output_path, freeze_panes=None)
        
        assert result == output_path
    
    def test_export_with_column_widths_and_index(self, tmp_path):
        """Test export with column widths when index=True."""
        df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
        output_path = tmp_path / "widths_indexed.xlsx"
        
        # With index=True, column indices shift by 1
        result = export_with_formatting(
            df, output_path,
            column_widths={"Name": 30, "Age": 20},
            index=True
        )
        
        assert result == output_path
        assert output_path.exists()
    
    def test_export_with_column_widths_string_not_in_columns(self, tmp_path):
        """Test export with column width for non-existent column."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        output_path = tmp_path / "widths_missing.xlsx"
        
        # Providing a column name that doesn't exist - should not crash
        result = export_with_formatting(
            df, output_path,
            column_widths={"A": 30, "NonExistent": 20}
        )
        
        assert result == output_path


class TestReadExcelSheets:
    """Tests for read_excel_sheets function."""
    
    def test_read_all_sheets(self, tmp_path):
        """Test reading all sheets from a workbook."""
        # Create file with multiple sheets
        output_path = tmp_path / "multi.xlsx"
        data = {
            "First": pd.DataFrame({"A": [1, 2]}),
            "Second": pd.DataFrame({"B": [3, 4]}),
        }
        export_to_excel(data, output_path)
        
        # Read all sheets
        result = read_excel_sheets(output_path)
        
        assert "First" in result
        assert "Second" in result
        assert len(result["First"]) == 2
        assert len(result["Second"]) == 2


class TestAppendToExcel:
    """Tests for append_to_excel function."""
    
    def test_append_rows(self, tmp_path):
        """Test appending rows to existing file."""
        # Create initial file
        output_path = tmp_path / "append.xlsx"
        initial = pd.DataFrame({"A": [1, 2], "B": ["a", "b"]})
        export_to_excel(initial, output_path)
        
        # Append new rows
        new_rows = pd.DataFrame({"A": [3, 4], "B": ["c", "d"]})
        result = append_to_excel(new_rows, output_path)
        
        assert result == output_path
        
        # Verify rows were added
        final = pd.read_excel(output_path, engine='openpyxl')
        assert len(final) == 4
    
    def test_append_without_sanitization(self, tmp_path):
        """Test appending rows without sanitization."""
        output_path = tmp_path / "append_no_sanitize.xlsx"
        initial = pd.DataFrame({"A": [1, 2]})
        export_to_excel(initial, output_path)
        
        new_rows = pd.DataFrame({"A": [3, 4]})
        result = append_to_excel(new_rows, output_path, sanitize=False)
        
        assert result == output_path
        final = pd.read_excel(output_path, engine='openpyxl')
        assert len(final) == 4


class TestCreateDataValidationDropdown:
    """Tests for create_data_validation_dropdown function."""
    
    def test_add_dropdown_by_column_letter(self, tmp_path):
        """Test adding dropdown by column letter."""
        output_path = tmp_path / "dropdown.xlsx"
        df = pd.DataFrame({"Status": ["Active", "Pending"], "Name": ["Alice", "Bob"]})
        export_to_excel(df, output_path)
        
        create_data_validation_dropdown(
            output_path,
            "Sheet1",
            "A",  # Column letter
            ["Active", "Inactive", "Pending"]
        )
        
        # File should still be valid
        result = pd.read_excel(output_path, engine='openpyxl')
        assert len(result) == 2
    
    def test_add_dropdown_by_column_index(self, tmp_path):
        """Test adding dropdown by column index."""
        output_path = tmp_path / "dropdown_idx.xlsx"
        df = pd.DataFrame({"Status": ["Active"], "Name": ["Alice"]})
        export_to_excel(df, output_path)
        
        create_data_validation_dropdown(
            output_path,
            "Sheet1",
            1,  # Column index
            ["Active", "Inactive"]
        )
        
        result = pd.read_excel(output_path, engine='openpyxl')
        assert len(result) == 1
    
    def test_add_dropdown_by_column_name(self, tmp_path):
        """Test adding dropdown by column header name."""
        output_path = tmp_path / "dropdown_name.xlsx"
        df = pd.DataFrame({"Status": ["Active"], "Name": ["Alice"]})
        export_to_excel(df, output_path)
        
        create_data_validation_dropdown(
            output_path,
            "Sheet1",
            "Status",  # Column header name
            ["Active", "Inactive", "Pending"]
        )
        
        result = pd.read_excel(output_path, engine='openpyxl')
        assert len(result) == 1
    
    def test_dropdown_with_custom_end_row(self, tmp_path):
        """Test adding dropdown with specific end row."""
        output_path = tmp_path / "dropdown_endrow.xlsx"
        df = pd.DataFrame({"Status": ["A", "B", "C", "D", "E"]})
        export_to_excel(df, output_path)
        
        create_data_validation_dropdown(
            output_path,
            "Sheet1",
            "A",
            ["X", "Y", "Z"],
            start_row=2,
            end_row=4
        )
        
        result = pd.read_excel(output_path, engine='openpyxl')
        assert len(result) == 5
    
    def test_dropdown_column_not_found_raises(self, tmp_path):
        """Test that invalid column name raises ValueError."""
        output_path = tmp_path / "dropdown_error.xlsx"
        df = pd.DataFrame({"Status": ["Active"]})
        export_to_excel(df, output_path)
        
        with pytest.raises(ValueError, match="Column 'NonExistent' not found"):
            create_data_validation_dropdown(
                output_path,
                "Sheet1",
                "NonExistent",
                ["A", "B"]
            )
    
    def test_dropdown_lowercase_column_letter(self, tmp_path):
        """Test adding dropdown with lowercase column letter."""
        output_path = tmp_path / "dropdown_lower.xlsx"
        df = pd.DataFrame({"A": [1], "B": [2]})
        export_to_excel(df, output_path)
        
        create_data_validation_dropdown(
            output_path,
            "Sheet1",
            "b",  # lowercase
            ["X", "Y"]
        )
        
        result = pd.read_excel(output_path, engine='openpyxl')
        assert len(result) == 1


class TestConstants:
    """Tests for module constants."""
    
    def test_max_sheet_name_length(self):
        """Test MAX_SHEET_NAME_LENGTH is 31 (Excel limit)."""
        assert MAX_SHEET_NAME_LENGTH == 31
    
    def test_illegal_characters_regex_matches_control_chars(self):
        """Test that regex matches control characters."""
        import re
        assert re.search(ILLEGAL_CHARACTERS_RE, "\x00")
        assert re.search(ILLEGAL_CHARACTERS_RE, "\x01")
    
    def test_invalid_sheet_chars_regex_matches_special(self):
        """Test that sheet name regex matches special chars."""
        import re
        assert re.search(INVALID_SHEET_NAME_CHARS, "\\")
        assert re.search(INVALID_SHEET_NAME_CHARS, "*")
        assert re.search(INVALID_SHEET_NAME_CHARS, "?")
        assert re.search(INVALID_SHEET_NAME_CHARS, ":")
        assert re.search(INVALID_SHEET_NAME_CHARS, "/")
        assert re.search(INVALID_SHEET_NAME_CHARS, "[")
        assert re.search(INVALID_SHEET_NAME_CHARS, "]")


class TestExcelUtilities:
    """Tests for Excel export utilities (main module exports)."""

    def test_excel_utils_exported(self):
        """Excel utilities are exported from main module."""
        from dealcloud_sdk import (
            sanitize_sheet_name,
            sanitize_cell_value,
            sanitize_dataframe,
            export_to_excel,
            export_with_formatting,
            read_excel_sheets,
            append_to_excel,
        )
        assert sanitize_sheet_name is not None
        assert sanitize_cell_value is not None
        assert sanitize_dataframe is not None
        assert export_to_excel is not None
        assert export_with_formatting is not None
        assert read_excel_sheets is not None
        assert append_to_excel is not None

    def test_sanitize_sheet_name_via_main(self):
        """sanitize_sheet_name removes illegal characters (via main module)."""
        from dealcloud_sdk import sanitize_sheet_name

        assert sanitize_sheet_name("Data: Q1/Q2") == "Data Q1Q2"
        assert sanitize_sheet_name("Test[1]") == "Test1"
        long_name = "A" * 50
        assert len(sanitize_sheet_name(long_name)) == 31

    def test_sanitize_cell_value_via_main(self):
        """sanitize_cell_value removes control characters (via main module)."""
        from dealcloud_sdk import sanitize_cell_value

        assert sanitize_cell_value("test\x00value") == "testvalue"
        assert sanitize_cell_value("normal text") == "normal text"
        assert sanitize_cell_value(123) == 123
        assert sanitize_cell_value(None) is None

    def test_sanitize_dataframe_via_main(self):
        """sanitize_dataframe cleans all string values (via main module)."""
        from dealcloud_sdk import sanitize_dataframe

        df = pd.DataFrame({
            "A": ["test\x00", "normal"],
            "B": [1, 2],
        })
        clean = sanitize_dataframe(df)
        assert clean["A"][0] == "test"
        assert clean["B"][0] == 1

    def test_illegal_chars_constants_exported(self):
        """Illegal character regex constants are available from main module."""
        from dealcloud_sdk import ILLEGAL_CHARACTERS_RE, INVALID_SHEET_NAME_CHARS

        assert ILLEGAL_CHARACTERS_RE is not None
        assert INVALID_SHEET_NAME_CHARS is not None


try:
    import polars as pl

    _POLARS = True
except ImportError:
    _POLARS = False


@pytest.mark.skipif(not _POLARS, reason="Polars not installed")
class TestExcelUtilsPolarsInput:
    """export_to_excel accepts Polars DataFrames (converted via to_pandas)."""

    def test_export_to_excel_polars_single(self, tmp_path):
        path = tmp_path / "out.xlsx"
        df = pl.DataFrame({"a": [1], "b": ["x"]})
        export_to_excel(df, path)
        sheets = read_excel_sheets(path)
        assert "Sheet1" in sheets
        assert list(sheets["Sheet1"]["a"]) == [1]

    def test_export_to_excel_polars_multi_sheet(self, tmp_path):
        path = tmp_path / "out.xlsx"
        export_to_excel(
            {"S1": pl.DataFrame({"x": [1]}), "S2": pl.DataFrame({"y": [2]})},
            path,
        )
        sheets = read_excel_sheets(path)
        assert len(sheets) == 2

