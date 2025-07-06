"""Test generator class"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import pandas as pd
from aind_data_schema_models._generators.generator import generate_code, check_black_version, load_data
import os


TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = TEST_DIR / ".." / "src/aind_data_schema_models"


class TestGenerateCode(unittest.TestCase):
    """Test generate_code"""

    @patch("builtins.open", new_callable=mock_open, read_data="template content")
    @patch("pandas.read_csv")
    @patch("subprocess.run")
    @patch("jinja2.Environment.from_string")
    def test_generate_code(self, mock_from_string, mock_subprocess_run, mock_read_csv, mock_open):
        """Test the generate_code function"""
        # Mock the CSV data to be used
        mock_data = pd.DataFrame({"column": ["value"]})
        mock_read_csv.return_value = mock_data

        # Mock Jinja2 template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered code"
        mock_from_string.return_value = mock_template

        # Define the paths that will be used in the function
        data_type = "test_data"
        output_path = Path("root/test_data.py")

        # Run the function with isort and black enabled
        generate_code(data_type, root_path="root", isort=True, black=True)

        # Check if the CSV file was read correctly
        mock_read_csv.assert_called_once_with(Path(f"root/_generators/models/{data_type}.csv"))

        # Check if the template was read correctly
        mock_open.assert_any_call(Path(f"root/_generators/templates/{data_type}.txt"))

        # Ensure the template rendering was called with the correct context
        mock_template.render.assert_called_once_with(data=mock_data)

        # Check if the output file was written with the rendered code
        mock_open().write.assert_called_once_with("rendered code")

        # Ensure isort and black were called
        mock_subprocess_run.assert_any_call(["isort", str(output_path)])
        mock_subprocess_run.assert_any_call(["black", str(output_path)])

    @patch("subprocess.run")
    @patch("jinja2.Environment.from_string")
    @patch("pandas.read_csv")
    @patch("builtins.open", new_callable=mock_open, read_data="template content")
    def test_generate_code_without_isort_black(self, mock_open, mock_read_csv, mock_from_string, mock_subprocess_run):
        """Test the generate_code function without running isort/black"""
        # Mock the CSV data
        mock_read_csv.return_value = pd.DataFrame({"column": ["value"]})

        # Mock Jinja2 template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered code"
        mock_from_string.return_value = mock_template

        # Run the function without isort and black
        generate_code("test_data", root_path="root", isort=False, black=False)

        # Ensure that neither isort nor black was called
        mock_subprocess_run.assert_not_called()

    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_generate_code_missing_data_file(self, mock_read_csv):
        """Test that the function crashes if a file is missing"""
        with self.assertRaises(FileNotFoundError):
            generate_code("missing_data", root_path=ROOT_DIR)

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("pandas.read_csv")
    def test_generate_code_missing_template_file(self, mock_read_csv, mock_open):
        """Test that the function crashes if a file is missing"""
        # Mock the CSV data to be used
        mock_read_csv.return_value = pd.DataFrame({"column": ["value"]})

        # Run the function expecting a FileNotFoundError due to missing template file
        with self.assertRaises(FileNotFoundError):
            generate_code("missing_template", root_path=ROOT_DIR)

    def test_check_black_version_too_old(self):
        """Test check_black_version when black version is too old"""
        with patch("black.__version__", "24.0.0"):
            with self.assertRaises(AssertionError) as context:
                check_black_version()

            self.assertIn("Please upgrade the black package to version 25.0.0 or later.", str(context.exception))

    def test_check_black_version_valid(self):
        """Test check_black_version when black version is valid"""
        with patch("black.__version__", "25.0.0"):
            check_black_version()

    @patch("pandas.read_csv")
    def test_load_data(self, mock_read_csv):
        """Test load_data function"""
        # Mock the CSV data
        mock_data = pd.DataFrame({"name": ["value1", "value2"], "column": ["value1", "value2"]})
        mock_read_csv.return_value = mock_data

        # Call the function
        data = load_data("test_data", root_path="root")

        # Check if the CSV file was read correctly
        mock_read_csv.assert_called_once_with(Path("root/_generators/models/test_data.csv"))

        # Check if the data was returned correctly
        pd.testing.assert_frame_equal(data, mock_data)

    @patch("pandas.read_csv")
    def test_load_data_with_sorting(self, mock_read_csv):
        """Test load_data function with sorting"""
        # Mock the CSV data
        mock_data = pd.DataFrame({"name": ["value2", "value1"], "column": ["value2", "value1"]})
        sorted_data = mock_data.sort_values("name")
        mock_read_csv.return_value = mock_data

        # Call the function
        data = load_data("test_data", root_path="root")

        # Check if the CSV file was read correctly
        mock_read_csv.assert_called_once_with(Path("root/_generators/models/test_data.csv"))

        # Check if the data was sorted correctly
        pd.testing.assert_frame_equal(data, sorted_data)

    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_load_data_missing_file(self, mock_read_csv):
        """Test load_data function when the file is missing"""
        with self.assertRaises(FileNotFoundError):
            load_data("missing_data", root_path="root")


if __name__ == "__main__":
    unittest.main()
