"""
Tests for FindDirection and Traverse enums for legacy_python compatibility.
"""
import pytest
from kodexa_document import FindDirection, Traverse


class TestFindDirection:
    """Test FindDirection enum"""
    
    def test_enum_values(self):
        """Test that enum values match legacy_python"""
        assert FindDirection.CHILDREN.value == 1
        assert FindDirection.PARENT.value == 2
    
    def test_enum_members(self):
        """Test that all expected members exist"""
        members = [m.name for m in FindDirection]
        assert "CHILDREN" in members
        assert "PARENT" in members
        assert len(members) == 2
    
    def test_enum_comparison(self):
        """Test enum comparison"""
        assert FindDirection.CHILDREN == FindDirection.CHILDREN
        assert FindDirection.CHILDREN != FindDirection.PARENT
    
    def test_enum_by_value(self):
        """Test accessing enum by value"""
        assert FindDirection(1) == FindDirection.CHILDREN
        assert FindDirection(2) == FindDirection.PARENT
    
    def test_invalid_value(self):
        """Test that invalid values raise error"""
        with pytest.raises(ValueError):
            FindDirection(0)
        with pytest.raises(ValueError):
            FindDirection(3)


class TestTraverse:
    """Test Traverse enum - values must match legacy Python (1-indexed)"""

    def test_enum_values(self):
        """Test that enum values match legacy Python (1-indexed)"""
        assert Traverse.SIBLING.value == 1
        assert Traverse.CHILDREN.value == 2
        assert Traverse.PARENT.value == 3
        assert Traverse.ALL.value == 4

    def test_enum_members(self):
        """Test that all expected members exist"""
        members = [m.name for m in Traverse]
        assert "SIBLING" in members
        assert "CHILDREN" in members
        assert "PARENT" in members
        assert "ALL" in members
        assert len(members) == 4

    def test_enum_comparison(self):
        """Test enum comparison"""
        assert Traverse.SIBLING == Traverse.SIBLING
        assert Traverse.CHILDREN != Traverse.PARENT
        assert Traverse.ALL != Traverse.SIBLING

    def test_enum_by_value(self):
        """Test accessing enum by value (1-indexed like legacy)"""
        assert Traverse(1) == Traverse.SIBLING
        assert Traverse(2) == Traverse.CHILDREN
        assert Traverse(3) == Traverse.PARENT
        assert Traverse(4) == Traverse.ALL

    def test_invalid_value(self):
        """Test that invalid values raise error (0 and 5 are invalid)"""
        with pytest.raises(ValueError):
            Traverse(0)
        with pytest.raises(ValueError):
            Traverse(5)
    
    def test_enum_usage_compatibility(self):
        """Test that enums can be used as expected in legacy code patterns"""
        # This simulates how legacy code might use the enum
        traverse_type = Traverse.SIBLING
        
        # Check that we can compare with enum members
        if traverse_type == Traverse.SIBLING:
            assert True
        else:
            assert False, "Should have matched SIBLING"
        
        # Check that we can use in a dict (common pattern)
        options = {
            "traverse": Traverse.CHILDREN,
            "direction": FindDirection.PARENT
        }
        assert options["traverse"] == Traverse.CHILDREN
        assert options["direction"] == FindDirection.PARENT


class TestEnumInteroperability:
    """Test that the enums work together as expected"""
    
    def test_combined_usage(self):
        """Test using both enums together"""
        # Common pattern in legacy code
        direction = FindDirection.CHILDREN
        traverse = Traverse.ALL
        
        # Simulate a function that might use both
        def process_options(dir_opt, trav_opt):
            if dir_opt == FindDirection.CHILDREN and trav_opt == Traverse.ALL:
                return "process_all_children"
            elif dir_opt == FindDirection.PARENT and trav_opt == Traverse.SIBLING:
                return "process_parent_siblings"
            return "other"
        
        result = process_options(direction, traverse)
        assert result == "process_all_children"
        
        result = process_options(FindDirection.PARENT, Traverse.SIBLING)
        assert result == "process_parent_siblings"
    
    def test_enum_string_representation(self):
        """Test string representation of enums"""
        # Check that string representation is predictable
        assert "CHILDREN" in str(FindDirection.CHILDREN)
        assert "PARENT" in str(FindDirection.PARENT)
        assert "SIBLING" in str(Traverse.SIBLING)
        assert "ALL" in str(Traverse.ALL)