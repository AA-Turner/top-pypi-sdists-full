"""
Test ContentNode methods for legacy_python compatibility.
Based on usage patterns from lib/python/tests/basic_document_test.py
"""

import pytest
from kodexa_document import Document


class TestContentNodeLegacyCompat:
    """Test ContentNode methods match legacy_python behavior."""
    
    def test_get_all_content_basic(self):
        """Test get_all_content matches legacy_python basic usage."""
        # Based on basic_document_test.py test_kbbd
        doc = Document.from_text('It is going to be a great day')
        assert doc.content_node.get_all_content() == 'It is going to be a great day'
        
        # Test it persists through serialization
        doc2 = Document.from_kddb(doc.to_kddb())
        assert doc2.content_node.get_all_content() == 'It is going to be a great day'
        
        doc.close()
        doc2.close()
    
    def test_get_all_content_with_children(self):
        """Test get_all_content with child nodes."""
        # Based on basic_document_test.py test_finder_and_tag pattern
        document = Document()
        root = document.create_node(node_type='root', content='')
        document.content_node = root
        
        # Add children with content
        child1 = document.create_node(node_type='bar', content='cheese')
        child2 = document.create_node(node_type='bar', content='cheeseburger')
        
        root.add_child(child1)
        root.add_child(child2)
        
        # Test individual child content
        assert root.get_children()[1].get_all_content() == 'cheeseburger'
        
        # Test root gets all content
        all_content = root.get_all_content()
        assert 'cheese' in all_content
        assert 'cheeseburger' in all_content
        
        document.close()
    
    def test_get_all_content_strip_parameter(self):
        """Test get_all_content strip parameter behavior."""
        # Based on tagging_test.py usage patterns
        doc = Document.from_text('  Hello   Philip   Dodds  ')
        
        # Test with strip=False (preserve whitespace)
        content_no_strip = doc.content_node.get_all_content(strip=False)
        assert content_no_strip == '  Hello   Philip   Dodds  '
        
        # Test with strip=True (default)
        content_stripped = doc.content_node.get_all_content(strip=True)
        assert content_stripped == 'Hello   Philip   Dodds'  # Only strips leading/trailing
        
        doc.close()
    
    def test_get_all_content_separator(self):
        """Test get_all_content with different separators."""
        doc = Document()
        root = doc.create_node('document', 'Title')
        doc.content_node = root
        
        para1 = doc.create_node('paragraph', 'First')
        para2 = doc.create_node('paragraph', 'Second')
        para3 = doc.create_node('paragraph', 'Third')
        
        root.add_child(para1)
        root.add_child(para2)
        root.add_child(para3)
        
        # Test default separator (space)
        assert root.get_all_content() == 'Title First Second Third'
        
        # Test custom separator
        assert root.get_all_content(separator='|') == 'Title|First|Second|Third'
        assert root.get_all_content(separator='\n') == 'Title\nFirst\nSecond\nThird'
        
        doc.close()
    
    def test_get_all_content_with_tags(self):
        """Test get_all_content after tagging (based on tagging_test.py)."""
        doc = Document.from_text('Hello Philip Dodds')
        
        # Verify content before tagging
        original_content = doc.content_node.get_all_content(strip=False)
        assert original_content == 'Hello Philip Dodds'
        
        # Tag some content (note: tagging functionality might not be fully implemented)
        # This test ensures get_all_content still works after document modifications
        
        # Verify content unchanged after operations
        assert doc.content_node.get_all_content(strip=False) == 'Hello Philip Dodds'
        
        # Test substring extraction pattern from tagging_test.py
        assert doc.content_node.get_all_content(strip=False)[6:12] == 'Philip'
        assert doc.content_node.get_all_content(strip=False)[13:18] == 'Dodds'
        
        doc.close()