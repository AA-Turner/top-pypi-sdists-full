"""Test mouse anatomy class methods"""

import unittest

from unittest.mock import patch
from aind_data_schema_models.mouse_anatomy import search_emapa_exact_match, get_emapa_id
from aind_data_schema_models.mouse_anatomy import MouseAnatomy, MouseAnatomyModel, Registry


class MouseAnatomyTests(unittest.TestCase):
    """Tests mouse anatomy"""

    @patch("aind_data_schema_models.mouse_anatomy.requests.get")
    def test_search_emapa_exact_match(self, mock_get):
        """Test search_emapa_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_emapa_exact_match("Test Label")
        expected = [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]
        self.assertEqual(result, expected)

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_emapa_exact_match("Test Label")

    @patch("aind_data_schema_models.mouse_anatomy.requests.get")
    def test_get_emapa_id(self, mock_get):
        """Test get_emapa_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_emapa_id("Test Label")
        expected = "12345"
        self.assertEqual(result, expected)

    @patch("aind_data_schema_models.mouse_anatomy.requests.get")
    def test_get_emapa_id_no_match(self, mock_get):
        """Test get_emapa_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_emapa_id("Nonexistent Label")
        self.assertIsNone(result)


class MouseAnatomyMetaTests(unittest.TestCase):
    """Tests MouseAnatomyMeta class"""

    @patch("aind_data_schema_models.mouse_anatomy.get_emapa_id")
    def test_getattribute_existing_attribute(self, mock_get_emapa_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_emapa_id.return_value = "12345"
        result = MouseAnatomy.ANATOMICAL_STRUCTURE
        expected = MouseAnatomyModel(
            name="Anatomical structure",
            registry=Registry.EMAPA,
            registry_identifier="12345",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)

    @patch("aind_data_schema_models.mouse_anatomy.get_emapa_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_emapa_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_emapa_id.return_value = None
        with self.assertRaises(AttributeError):
            MouseAnatomy.NONEXISTENT_ATTRIBUTE

        # this is a real attribute, but we're faking that it doesn't exist in the registry
        with self.assertRaises(ValueError):
            MouseAnatomy.ABDOMEN

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = MouseAnatomy.__name__
        expected = "MouseAnatomy"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
