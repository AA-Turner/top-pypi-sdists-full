"""
Test external data functionality matching legacy_python behavior.
"""

import pytest
from kodexa_document import Document


class TestExternalData:
    """Test external data methods."""
    
    def test_external_data(self):
        """Test basic external data functionality."""
        document = Document(inmemory=True)
        
        # Set external data with default key
        document.set_external_data({"cheese": "bar"})
        
        # Get it back
        data = document.get_external_data()
        assert data["cheese"] == "bar"
        
        # Verify not None and keys list
        assert document.get_external_data() is not None
        assert document.get_external_data_keys() == ["default"]
        
        document.close()
    
    def test_external_data_with_custom_key(self):
        """Test external data with custom keys."""
        document = Document(inmemory=True)
        
        # Set data for custom key
        document.set_external_data({"cheese": "foo"}, "new")
        
        # Overwrite the same key
        document.set_external_data({"cheese": "bar"}, "new")
        
        # Verify overwrite worked
        assert document.get_external_data("new")["cheese"] == "bar"
        
        # Default key should be empty (but calling get_external_data creates it)
        assert document.get_external_data() is not None
        assert document.get_external_data() == {}
        
        # Keys include both "new" and "default" (default was created by get_external_data call)
        keys = document.get_external_data_keys()
        assert len(keys) == 2
        assert "new" in keys
        assert "default" in keys  # Created when we called get_external_data() above
        
        document.close()
    
    def test_external_data_nonexistent_key(self):
        """Test getting external data for non-existent key.
        
        Note: get_external_data now initializes an empty entry when the key doesn't exist.
        This is the expected behavior for auto-initialization of external data.
        """
        document = Document(inmemory=True)
        
        # Non-existent key should return empty dict and create the entry
        data = document.get_external_data("nonexistent")
        assert data == {}
        
        # Key is now created (auto-initialization behavior)
        assert document.get_external_data_keys() == ["nonexistent"]
        
        document.close()
    
    def test_external_data_type_validation(self):
        """Test external data type validation."""
        document = Document(inmemory=True)
        
        # Should raise TypeError for non-dict
        with pytest.raises(TypeError, match="external_data must be a dictionary"):
            document.set_external_data("not a dict")
        
        with pytest.raises(TypeError, match="external_data must be a dictionary"):
            document.set_external_data(["not", "a", "dict"])
        
        document.close()
    
    def test_external_data_complex_values(self):
        """Test external data with complex values."""
        document = Document(inmemory=True)
        
        complex_data = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        document.set_external_data(complex_data, "complex")
        retrieved = document.get_external_data("complex")
        
        assert retrieved == complex_data
        
        document.close()
    
    def test_external_data_multiple_keys(self):
        """Test multiple external data keys."""
        document = Document(inmemory=True)
        
        # Set multiple keys
        document.set_external_data({"key1": "value1"}, "first")
        document.set_external_data({"key2": "value2"}, "second") 
        document.set_external_data({"key3": "value3"}, "third")
        
        # Verify all data can be retrieved
        assert document.get_external_data("first")["key1"] == "value1"
        assert document.get_external_data("second")["key2"] == "value2"
        assert document.get_external_data("third")["key3"] == "value3"
        
        # Verify keys list (only keys with data are returned)
        keys = document.get_external_data_keys()
        assert len(keys) == 3  # Only the 3 keys with data
        assert "first" in keys
        assert "second" in keys
        assert "third" in keys
        # "default" key is not included since it has no data
        
        document.close()