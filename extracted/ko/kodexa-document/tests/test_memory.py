"""
Test memory management and cleanup.
"""

import gc
import weakref
import pytest
from kodexa_document import Document


class TestMemoryManagement:
    """Test memory management and cleanup."""
    
    def test_finalizer_cleanup(self):
        """Test that finalizer cleans up when document is garbage collected."""
        doc = Document()
        uuid = doc.uuid
        
        # Create weak reference to track when object is deleted
        ref = weakref.ref(doc)
        
        # Delete the document without closing
        del doc
        gc.collect()
        
        # Object should be cleaned up
        assert ref() is None
    
    def test_explicit_close_detaches_finalizer(self):
        """Test that explicit close detaches the finalizer."""
        doc = Document()
        
        # Explicitly close
        doc.close()
        
        # Delete - finalizer should not run since we already closed
        del doc
        gc.collect()
        
        # No errors should occur
    
    def test_multiple_documents(self):
        """Test creating and cleaning up multiple documents."""
        docs = []
        uuids = []
        
        # Create multiple documents
        for i in range(10):
            doc = Document(metadata={"index": i})
            docs.append(doc)
            uuids.append(doc.uuid)
        
        # All should have unique UUIDs
        assert len(set(uuids)) == 10
        
        # Close all
        for doc in docs:
            doc.close()
    
    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up."""
        uuid = None
        
        with Document() as doc:
            uuid = doc.uuid
            assert uuid is not None
        
        # After context, document should be closed
        # Creating a new document should work fine
        with Document() as doc2:
            uuid2 = doc2.uuid
            assert uuid2 != uuid