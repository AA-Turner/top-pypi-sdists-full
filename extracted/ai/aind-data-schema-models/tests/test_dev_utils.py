"""Dev utils tests"""

import unittest
from unittest.mock import patch, MagicMock
from aind_data_schema_models._generators.dev_utils import to_class_name, to_class_name_underscored, update_harp_types


class TestDevUtils(unittest.TestCase):
    """Tests for dev_utils module"""

    def test_to_class_name(self):
        """Test to class name method"""

        # Regular cases
        self.assertEqual(to_class_name("Smart SPIM"), "Smart_Spim")
        self.assertEqual(to_class_name("SmartSPIM"), "Smartspim")
        self.assertEqual(to_class_name("single-plane-ophys"), "Single_Plane_Ophys")

        # Edge cases
        self.assertEqual(to_class_name("a-b-c"), "A_B_C")  # Hyphenated
        self.assertEqual(to_class_name("_Already-Underscored"), "_Already_Underscored")

        # Check that non-alphanumeric characters are replaced with _
        self.assertEqual(to_class_name("123test"), "_123Test")  # Replace number with _
        self.assertEqual(to_class_name("#a"), "_A")  # Replace alphanumeric with _
        self.assertEqual(to_class_name("1Smart 2Spim"), "_1Smart_2Spim")  # Replace alphanumeric with _

        # Empty string
        self.assertEqual(to_class_name(""), "")

    def test_to_class_name_underscored(self):
        """Test to class name underscored method"""

        # Regular cases
        self.assertEqual(to_class_name_underscored("Smart SPIM"), "_Smart_Spim")
        self.assertEqual(to_class_name_underscored("SmartSPIM"), "_Smartspim")
        self.assertEqual(to_class_name_underscored("single-plane-ophys"), "_Single_Plane_Ophys")

        # Edge cases
        self.assertEqual(to_class_name_underscored("123test"), "_123Test")  # Starts with a number
        self.assertEqual(to_class_name_underscored("a-b-c"), "_A_B_C")  # Hyphenated
        self.assertEqual(to_class_name_underscored("_Already-Underscored"), "__Already_Underscored")
        self.assertEqual(to_class_name_underscored("#a"), "__A")  # Strip non-alphanumeric characters
        self.assertEqual(to_class_name_underscored("1Smart 2Spim"), "_1Smart_2Spim")  # Replace alphanumeric with _

        # Empty string
        self.assertEqual(to_class_name_underscored(""), "_")  # Should still return an underscore

    @patch("aind_data_schema_models._generators.dev_utils.requests.get")
    @patch("aind_data_schema_models._generators.dev_utils.pd.DataFrame.to_csv")
    def test_update_harp_types_success(self, mock_to_csv, mock_get):
        """Test successful execution of update_harp_types function"""

        # Mock YAML content
        mock_yaml_content = """
devices:
  1234:
    name: "Test Device 1"
    description: "A test device"
  5678:
    name: "Test Device 2"
    description: "Another test device"
"""

        # Setup mock response
        mock_response = MagicMock()
        mock_response.content.decode.return_value = mock_yaml_content
        mock_get.return_value = mock_response

        # Call the function
        result = update_harp_types()

        # Verify HTTP request was made correctly
        mock_get.assert_called_once_with(
            "https://raw.githubusercontent.com/harp-tech/whoami/refs/heads/main/whoami.yml",
            allow_redirects=True,
            timeout=5,
        )

        # Verify CSV file was saved
        mock_to_csv.assert_called_once()
        call_args = mock_to_csv.call_args
        self.assertTrue(str(call_args[0][0]).endswith("harp_types.csv"))
        self.assertEqual(call_args[1]["index"], False)

        # Verify function returns None (as it doesn't have a return statement)
        self.assertIsNone(result)

    @patch("aind_data_schema_models._generators.dev_utils.requests.get")
    @patch("aind_data_schema_models._generators.dev_utils.pd.DataFrame.to_csv")
    def test_update_harp_types_custom_url(self, mock_to_csv, mock_get):
        """Test update_harp_types with custom URL"""

        # Mock YAML content
        mock_yaml_content = """
devices:
  9999:
    name: "Custom Device"
    description: "A custom device"
"""

        # Setup mock response
        mock_response = MagicMock()
        mock_response.content.decode.return_value = mock_yaml_content
        mock_get.return_value = mock_response

        custom_url = "https://example.com/custom.yml"

        # Call the function with custom URL
        result = update_harp_types(url=custom_url)

        # Verify HTTP request was made to custom URL
        mock_get.assert_called_once_with(custom_url, allow_redirects=True, timeout=5)

        # Verify function returns None
        self.assertIsNone(result)

        # Verify CSV was saved
        mock_to_csv.assert_called_once()

    @patch("aind_data_schema_models._generators.dev_utils.requests.get")
    @patch("aind_data_schema_models._generators.dev_utils.pd.DataFrame.to_csv")
    def test_update_harp_types_empty_devices(self, mock_to_csv, mock_get):
        """Test update_harp_types with empty devices list"""

        # Mock YAML content with no devices
        mock_yaml_content = """
devices: {}
"""

        # Setup mock response
        mock_response = MagicMock()
        mock_response.content.decode.return_value = mock_yaml_content
        mock_get.return_value = mock_response

        # Call the function
        result = update_harp_types()

        # Verify function returns None
        self.assertIsNone(result)

        # Verify CSV was still saved (even if empty)
        mock_to_csv.assert_called_once()

    @patch("aind_data_schema_models._generators.dev_utils.requests.get")
    @patch("aind_data_schema_models._generators.dev_utils.pd.DataFrame.to_csv")
    @patch("aind_data_schema_models._generators.dev_utils.pd.DataFrame")
    def test_update_harp_types_numeric_whoami(self, mock_dataframe, mock_to_csv, mock_get):
        """Test update_harp_types ensures whoami is converted to string"""

        # Mock YAML content with numeric whoami
        mock_yaml_content = """
devices:
  12345:
    name: "Numeric Device"
    description: "Device with numeric whoami"
"""

        # Setup mock response
        mock_response = MagicMock()
        mock_response.content.decode.return_value = mock_yaml_content
        mock_get.return_value = mock_response

        # Setup mock DataFrame to capture the data passed to it
        mock_df_instance = MagicMock()
        mock_dataframe.return_value = mock_df_instance

        # Call the function
        result = update_harp_types()

        # Verify function returns None
        self.assertIsNone(result)

        # Verify DataFrame was created with correct data structure
        mock_dataframe.assert_called_once()
        call_args = mock_dataframe.call_args[0][0]  # Get the data passed to DataFrame

        # Verify the data structure and that whoami is converted to string
        self.assertEqual(len(call_args), 1)
        self.assertEqual(call_args[0]["name"], "Numeric Device")
        self.assertEqual(call_args[0]["whoami"], "12345")
        self.assertIsInstance(call_args[0]["whoami"], str)


if __name__ == "__main__":
    unittest.main()
