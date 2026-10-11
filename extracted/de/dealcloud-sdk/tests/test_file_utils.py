"""Tests for file utility functions."""

import pytest
import pandas as pd
from pathlib import Path

from dealcloud_sdk.utils.file_utils import (
    detect_encoding,
    is_supported_file,
    should_skip_file,
    read_csv,
    read_excel,
    read_file,
    get_data_files,
    SUPPORTED_CSV_EXTENSIONS,
    SUPPORTED_EXCEL_EXTENSIONS,
    ALL_SUPPORTED_EXTENSIONS,
)


class TestDetectEncoding:
    """Tests for detect_encoding function."""
    
    def test_detects_utf8(self, tmp_path):
        """Test detection of UTF-8 encoding."""
        filepath = tmp_path / "utf8.csv"
        filepath.write_text("name,value\ntest,123\n", encoding='utf-8')
        
        result = detect_encoding(filepath)
        
        assert result == 'utf-8'
    
    def test_detects_latin1(self, tmp_path):
        """Test detection of Latin-1 encoding."""
        filepath = tmp_path / "latin1.csv"
        # Use Latin-1 specific character
        filepath.write_bytes(b"name,value\ncaf\xe9,123\n")
        
        result = detect_encoding(filepath)
        
        # Should find a working encoding
        assert result in ['latin-1', 'cp1252', 'utf-8']
    
    def test_fallback_to_utf8_on_unreadable(self, tmp_path):
        """Test fallback to utf-8 when all encodings fail."""
        from unittest.mock import patch
        
        filepath = tmp_path / "unreadable.csv"
        filepath.write_text("test data", encoding='utf-8')
        
        # Mock open to always raise UnicodeDecodeError
        def mock_open_always_fail(*args, **kwargs):
            raise UnicodeDecodeError("test", b"", 0, 1, "mocked error")
        
        with patch('builtins.open', side_effect=mock_open_always_fail):
            result = detect_encoding(filepath)
        
        # Should return utf-8 as fallback
        assert result == 'utf-8'


class TestIsSupportedFile:
    """Tests for is_supported_file function."""
    
    def test_csv_is_supported(self):
        """Test that CSV files are supported."""
        assert is_supported_file("data.csv") is True
        assert is_supported_file("data.CSV") is True
    
    def test_excel_is_supported(self):
        """Test that Excel files are supported."""
        assert is_supported_file("data.xlsx") is True
        assert is_supported_file("data.xls") is True
        assert is_supported_file("data.xlsm") is True
    
    def test_txt_is_supported(self):
        """Test that TXT files are supported."""
        assert is_supported_file("data.txt") is True
        assert is_supported_file("data.tsv") is True
    
    def test_unsupported_extensions(self):
        """Test that unsupported extensions return False."""
        assert is_supported_file("data.pdf") is False
        assert is_supported_file("data.docx") is False
        assert is_supported_file("data.json") is False
    
    def test_path_object(self):
        """Test with Path object."""
        assert is_supported_file(Path("data.xlsx")) is True


class TestShouldSkipFile:
    """Tests for should_skip_file function."""
    
    def test_skips_hidden_files(self):
        """Test that hidden files are skipped."""
        assert should_skip_file(".hidden.csv") is True
        assert should_skip_file("visible.csv") is False
    
    def test_skips_temp_excel_files(self):
        """Test that temporary Excel files are skipped."""
        assert should_skip_file("~$document.xlsx") is True
    
    def test_skips_ds_store(self):
        """Test that .DS_Store is skipped."""
        assert should_skip_file(".DS_Store") is True
    
    def test_skips_zip_files(self):
        """Test that zip files are skipped."""
        assert should_skip_file("archive.zip") is True
        assert should_skip_file("archive.ZIP") is True
    
    def test_normal_files_not_skipped(self):
        """Test that normal files are not skipped."""
        assert should_skip_file("data.csv") is False
        assert should_skip_file("report.xlsx") is False


class TestReadCsv:
    """Tests for read_csv function."""
    
    def test_read_utf8_csv(self, tmp_path):
        """Test reading UTF-8 CSV."""
        filepath = tmp_path / "test.csv"
        filepath.write_text("name,value\nAlice,100\nBob,200\n")
        
        df = read_csv(filepath)
        
        assert len(df) == 2
        assert list(df.columns) == ["name", "value"]
    
    def test_read_csv_with_explicit_encoding(self, tmp_path):
        """Test reading CSV with explicit encoding."""
        filepath = tmp_path / "test.csv"
        filepath.write_text("name,value\nTest,123\n", encoding='utf-8')
        
        df = read_csv(filepath, encoding='utf-8')
        
        assert len(df) == 1
    
    def test_read_csv_with_delimiter(self, tmp_path):
        """Test reading CSV with custom delimiter."""
        filepath = tmp_path / "test.csv"
        filepath.write_text("name;value\nAlice;100\n")
        
        df = read_csv(filepath, delimiter=";")
        
        assert list(df.columns) == ["name", "value"]
    
    def test_read_csv_unicode_error_fallback(self, tmp_path):
        """Test CSV reading with UnicodeError fallback."""
        from unittest.mock import patch, MagicMock
        
        filepath = tmp_path / "test.csv"
        filepath.write_text("name,value\nTest,123\n", encoding='utf-8')
        
        # Mock read_csv to raise UnicodeError on first call, succeed on second
        call_count = [0]
        mock_df = pd.DataFrame({"name": ["Test"], "value": [123]})
        
        def mock_read_csv(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise UnicodeError("Test encoding error")
            return mock_df
        
        with patch('dealcloud_sdk.utils.file_utils.pd.read_csv', side_effect=mock_read_csv):
            # This should trigger the UnicodeError and fall back
            df = read_csv(filepath, encoding='latin-1')
        
        # Should have called twice (once failed, once succeeded)
        assert call_count[0] == 2
        assert len(df) >= 1


class TestReadExcel:
    """Tests for read_excel function."""
    
    def test_read_xlsx(self, tmp_path):
        """Test reading XLSX file."""
        filepath = tmp_path / "test.xlsx"
        df_original = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        df_original.to_excel(filepath, index=False, engine='openpyxl')
        
        df = read_excel(filepath)
        
        assert len(df) == 2
        assert list(df.columns) == ["A", "B"]
    
    def test_read_specific_sheet(self, tmp_path):
        """Test reading a specific sheet by name."""
        filepath = tmp_path / "test.xlsx"
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            pd.DataFrame({"A": [1]}).to_excel(writer, sheet_name="First", index=False)
            pd.DataFrame({"B": [2]}).to_excel(writer, sheet_name="Second", index=False)
        
        df = read_excel(filepath, sheet_name="Second")
        
        assert list(df.columns) == ["B"]
    
    def test_read_sheet_by_index(self, tmp_path):
        """Test reading sheet by index."""
        filepath = tmp_path / "test.xlsx"
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            pd.DataFrame({"A": [1]}).to_excel(writer, sheet_name="First", index=False)
            pd.DataFrame({"B": [2]}).to_excel(writer, sheet_name="Second", index=False)
        
        df = read_excel(filepath, sheet_name=1)
        
        assert list(df.columns) == ["B"]
    
    def test_read_xlsm(self, tmp_path):
        """Test reading XLSM file (macro-enabled)."""
        filepath = tmp_path / "test.xlsm"
        df_original = pd.DataFrame({"A": [1, 2]})
        df_original.to_excel(filepath, index=False, engine='openpyxl')
        
        df = read_excel(filepath)
        
        assert len(df) == 2
        assert list(df.columns) == ["A"]
    
    def test_read_xls_format(self, tmp_path):
        """Test reading XLS format (mocked)."""
        from unittest.mock import ANY, patch

        filepath = tmp_path / "test.xls"
        filepath.write_bytes(b"dummy")  # Create file

        mock_df = pd.DataFrame({"A": [1, 2]})
        with patch('dealcloud_sdk.utils.file_utils.pd.read_excel', return_value=mock_df) as mock_read:
            df = read_excel(filepath)
            mock_read.assert_called_once_with(ANY, engine='xlrd', sheet_name=0)
        
        assert len(df) == 2
    
    def test_read_ods_format(self, tmp_path):
        """Test reading ODS format (mocked)."""
        from unittest.mock import ANY, patch

        filepath = tmp_path / "test.ods"
        filepath.write_bytes(b"dummy")

        mock_df = pd.DataFrame({"A": [1]})
        with patch('dealcloud_sdk.utils.file_utils.pd.read_excel', return_value=mock_df) as mock_read:
            df = read_excel(filepath)
            mock_read.assert_called_once_with(ANY, engine='odf', sheet_name=0)
        
        assert len(df) == 1
    
    def test_read_unknown_extension_auto_detect(self, tmp_path):
        """Test reading unknown extension with auto-detection."""
        filepath = tmp_path / "test.xlsx"
        df_original = pd.DataFrame({"A": [1]})
        df_original.to_excel(filepath, index=False, engine='openpyxl')
        
        # Rename to unknown extension
        unknown_path = tmp_path / "test.data"
        filepath.rename(unknown_path)
        
        df = read_excel(unknown_path)
        assert len(df) == 1
    
    def test_read_unknown_extension_fallback_to_openpyxl(self, tmp_path):
        """Test unknown extension falls back to openpyxl on auto-detect failure."""
        from unittest.mock import patch
        
        filepath = tmp_path / "test.xlsx"
        df_original = pd.DataFrame({"A": [1]})
        df_original.to_excel(filepath, index=False, engine='openpyxl')
        
        unknown_path = tmp_path / "test.data"
        filepath.rename(unknown_path)
        
        mock_df = pd.DataFrame({"A": [1]})
        call_count = [0]
        
        def mock_read_excel(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1 and 'engine' not in kwargs:
                raise ValueError("Cannot auto-detect")
            return mock_df
        
        with patch('dealcloud_sdk.utils.file_utils.pd.read_excel', side_effect=mock_read_excel):
            df = read_excel(unknown_path)
        
        assert len(df) == 1
    
    def test_read_corrupted_file_raises(self, tmp_path):
        """Test reading corrupted file raises ValueError."""
        filepath = tmp_path / "corrupted.xlsx"
        filepath.write_bytes(b"not an excel file")
        
        with pytest.raises(ValueError, match="Unsupported file format or corrupted"):
            read_excel(filepath)


class TestReadFile:
    """Tests for read_file function."""
    
    def test_read_csv_file(self, tmp_path):
        """Test reading CSV via read_file."""
        filepath = tmp_path / "data.csv"
        filepath.write_text("col1,col2\na,b\n")
        
        df = read_file(filepath)
        
        assert list(df.columns) == ["col1", "col2"]
    
    def test_read_excel_file(self, tmp_path):
        """Test reading Excel via read_file."""
        filepath = tmp_path / "data.xlsx"
        pd.DataFrame({"A": [1]}).to_excel(filepath, index=False, engine='openpyxl')
        
        df = read_file(filepath)
        
        assert list(df.columns) == ["A"]
    
    def test_read_hidden_file_raises(self, tmp_path):
        """Test that reading hidden file raises error."""
        filepath = tmp_path / ".hidden.csv"
        filepath.write_text("a,b\n1,2\n")
        
        with pytest.raises(ValueError, match="Skipping hidden"):
            read_file(filepath)
    
    def test_read_unsupported_raises(self, tmp_path):
        """Test that unsupported format raises error."""
        filepath = tmp_path / "data.json"
        filepath.write_text('{"a": 1}')
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            read_file(filepath)
    
    def test_read_tsv_file(self, tmp_path):
        """Test reading TSV file."""
        filepath = tmp_path / "data.tsv"
        filepath.write_text("col1\tcol2\na\tb\n")
        
        df = read_file(filepath)
        
        # Default CSV reader should handle this
        assert len(df) >= 1


class TestGetDataFiles:
    """Tests for get_data_files function."""
    
    def test_finds_csv_files(self, tmp_path):
        """Test finding CSV files in directory."""
        (tmp_path / "data1.csv").write_text("a,b\n1,2\n")
        (tmp_path / "data2.csv").write_text("c,d\n3,4\n")
        
        files = get_data_files(tmp_path)
        
        assert len(files) == 2
        assert all(f.suffix == ".csv" for f in files)
    
    def test_finds_excel_files(self, tmp_path):
        """Test finding Excel files in directory."""
        pd.DataFrame({"A": [1]}).to_excel(tmp_path / "data.xlsx", index=False)
        
        files = get_data_files(tmp_path)
        
        assert len(files) == 1
        assert files[0].suffix == ".xlsx"
    
    def test_excludes_hidden_files(self, tmp_path):
        """Test that hidden files are excluded."""
        (tmp_path / "visible.csv").write_text("a,b\n1,2\n")
        (tmp_path / ".hidden.csv").write_text("a,b\n1,2\n")
        
        files = get_data_files(tmp_path)
        
        assert len(files) == 1
        assert files[0].name == "visible.csv"
    
    def test_recursive_search(self, tmp_path):
        """Test recursive file search."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root.csv").write_text("a\n1\n")
        (subdir / "nested.csv").write_text("b\n2\n")
        
        files = get_data_files(tmp_path, recursive=True)
        
        assert len(files) == 2
    
    def test_non_recursive_search(self, tmp_path):
        """Test non-recursive file search."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root.csv").write_text("a\n1\n")
        (subdir / "nested.csv").write_text("b\n2\n")
        
        files = get_data_files(tmp_path, recursive=False)
        
        assert len(files) == 1
        assert files[0].name == "root.csv"


class TestConstants:
    """Tests for module constants."""
    
    def test_csv_extensions(self):
        """Test SUPPORTED_CSV_EXTENSIONS."""
        assert '.csv' in SUPPORTED_CSV_EXTENSIONS
        assert '.tsv' in SUPPORTED_CSV_EXTENSIONS
        assert '.txt' in SUPPORTED_CSV_EXTENSIONS
    
    def test_excel_extensions(self):
        """Test SUPPORTED_EXCEL_EXTENSIONS."""
        assert '.xlsx' in SUPPORTED_EXCEL_EXTENSIONS
        assert '.xls' in SUPPORTED_EXCEL_EXTENSIONS
        assert '.xlsm' in SUPPORTED_EXCEL_EXTENSIONS
    
    def test_all_extensions(self):
        """Test ALL_SUPPORTED_EXTENSIONS combines both."""
        assert set(SUPPORTED_CSV_EXTENSIONS).issubset(set(ALL_SUPPORTED_EXTENSIONS))
        assert set(SUPPORTED_EXCEL_EXTENSIONS).issubset(set(ALL_SUPPORTED_EXTENSIONS))


class TestFileUtilities:
    """Tests for file utility functions (main module exports)."""

    def test_file_utils_exported(self):
        """File utilities are exported from main module."""
        from dealcloud_sdk import (
            detect_encoding,
            is_supported_file,
            should_skip_file,
            read_csv,
            read_excel,
            read_file,
            get_data_files,
        )
        assert detect_encoding is not None
        assert is_supported_file is not None
        assert should_skip_file is not None
        assert read_csv is not None
        assert read_excel is not None
        assert read_file is not None
        assert get_data_files is not None

    def test_is_supported_file_via_main(self):
        """is_supported_file correctly identifies supported formats (via main module)."""
        from dealcloud_sdk import is_supported_file

        assert is_supported_file("data.csv") is True
        assert is_supported_file("data.xlsx") is True
        assert is_supported_file("data.xls") is True
        assert is_supported_file("data.txt") is True
        assert is_supported_file("data.json") is False

    def test_should_skip_file_via_main(self):
        """should_skip_file correctly identifies files to skip (via main module)."""
        from dealcloud_sdk import should_skip_file

        assert should_skip_file(".hidden") is True
        assert should_skip_file("~$temp.xlsx") is True
        assert should_skip_file(".DS_Store") is True
        assert should_skip_file("data.zip") is True
        assert should_skip_file("normal.csv") is False
        assert should_skip_file("data.xlsx") is False

    def test_extension_constants_exported(self):
        """File extension constants are available from main module."""
        from dealcloud_sdk import (
            SUPPORTED_CSV_EXTENSIONS,
            SUPPORTED_EXCEL_EXTENSIONS,
            ALL_SUPPORTED_EXTENSIONS,
        )

        assert ".csv" in SUPPORTED_CSV_EXTENSIONS
        assert ".xlsx" in SUPPORTED_EXCEL_EXTENSIONS
        assert len(ALL_SUPPORTED_EXTENSIONS) > 0


try:
    import polars as pl

    _POLARS = True
except ImportError:
    _POLARS = False


@pytest.mark.skipif(not _POLARS, reason="Polars not installed")
class TestFileUtilsPolarsOutput:
    """read_csv / read_file with output='polars'."""

    def test_read_csv_polars(self, tmp_path):
        filepath = tmp_path / "t.csv"
        filepath.write_text("a,b\n1,2\n", encoding="utf-8")
        result = read_csv(filepath, output="polars")
        assert isinstance(result, pl.DataFrame)
        assert result.columns == ["a", "b"]
        assert result.rows() == [(1, 2)]

    def test_read_file_polars_csv(self, tmp_path):
        filepath = tmp_path / "t.csv"
        filepath.write_text("x,y\n3,4\n", encoding="utf-8")
        result = read_file(filepath, output="polars")
        assert isinstance(result, pl.DataFrame)
        assert result["x"].to_list() == [3]

