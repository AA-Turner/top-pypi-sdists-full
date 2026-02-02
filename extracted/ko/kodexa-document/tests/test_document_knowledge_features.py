"""
Test Document knowledge features methods.
"""

import pytest
from kodexa_document import Document, DocumentKnowledgeFeature


class TestDocumentKnowledgeFeatures:
    """Test document knowledge feature methods."""

    def test_get_empty_knowledge_features(self):
        """Test getting knowledge features from empty document."""
        doc = Document()
        features = doc.get_document_knowledge_features()
        assert features == []
        doc.close()

    def test_set_and_get_knowledge_features_with_dict(self):
        """Test setting and getting knowledge features using dicts (camelCase)."""
        doc = Document()

        features = [
            {
                "knowledgeFeatureRef": "test-feature-1",
                "properties": {"key1": "value1", "count": 42}
            },
            {
                "knowledgeFeatureRef": "test-feature-2",
                "properties": {"enabled": True}
            }
        ]

        doc.set_document_knowledge_features(features)

        retrieved = doc.get_document_knowledge_features()
        assert len(retrieved) == 2

        # Check first feature - use attribute access (Pydantic model)
        assert retrieved[0].knowledge_feature_ref == "test-feature-1"
        assert retrieved[0].properties["key1"] == "value1"
        assert retrieved[0].properties["count"] == 42

        # Check second feature
        assert retrieved[1].knowledge_feature_ref == "test-feature-2"
        assert retrieved[1].properties["enabled"] is True

        doc.close()

    def test_set_and_get_knowledge_features_with_pydantic(self):
        """Test setting and getting knowledge features using Pydantic models."""
        doc = Document()

        features = [
            DocumentKnowledgeFeature(
                knowledge_feature_ref="pydantic-feature",
                properties={"source": "test", "version": "1.0"}
            )
        ]

        doc.set_document_knowledge_features(features)

        retrieved = doc.get_document_knowledge_features()
        assert len(retrieved) == 1
        assert retrieved[0].knowledge_feature_ref == "pydantic-feature"
        assert retrieved[0].properties["source"] == "test"
        assert retrieved[0].properties["version"] == "1.0"

        doc.close()

    def test_overwrite_knowledge_features(self):
        """Test that setting features overwrites existing ones."""
        doc = Document()

        # Set initial features
        doc.set_document_knowledge_features([
            {"knowledgeFeatureRef": "first", "properties": {}}
        ])
        assert len(doc.get_document_knowledge_features()) == 1

        # Overwrite with new features
        doc.set_document_knowledge_features([
            {"knowledgeFeatureRef": "second", "properties": {}},
            {"knowledgeFeatureRef": "third", "properties": {}}
        ])

        retrieved = doc.get_document_knowledge_features()
        assert len(retrieved) == 2
        refs = [f.knowledge_feature_ref for f in retrieved]
        assert "first" not in refs
        assert "second" in refs
        assert "third" in refs

        doc.close()

    def test_clear_knowledge_features(self):
        """Test clearing knowledge features by setting empty list."""
        doc = Document()

        # Set some features
        doc.set_document_knowledge_features([
            {"knowledgeFeatureRef": "to-clear", "properties": {"data": "value"}}
        ])
        assert len(doc.get_document_knowledge_features()) == 1

        # Clear by setting empty list
        doc.set_document_knowledge_features([])
        assert doc.get_document_knowledge_features() == []

        doc.close()

    def test_set_knowledge_features_invalid_type(self):
        """Test that setting non-list raises TypeError."""
        doc = Document()

        with pytest.raises(TypeError):
            doc.set_document_knowledge_features("not a list")

        with pytest.raises(TypeError):
            doc.set_document_knowledge_features({"not": "a list"})

        doc.close()

    def test_set_knowledge_features_invalid_item_type(self):
        """Test that setting list with invalid items raises TypeError."""
        doc = Document()

        with pytest.raises(TypeError):
            doc.set_document_knowledge_features(["not a dict or model"])

        doc.close()

    def test_knowledge_features_persist_after_save_and_reload(self):
        """Test that knowledge features persist through save/reload cycle."""
        import tempfile
        import os

        doc = Document()
        doc.set_document_knowledge_features([
            {
                "knowledgeFeatureRef": "persistent-feature",
                "properties": {"important": "data", "count": 123}
            }
        ])

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
            temp_path = f.name

        try:
            doc.to_kddb(temp_path)
            doc.close()

            # Reload and verify
            doc2 = Document.from_kddb(temp_path)
            retrieved = doc2.get_document_knowledge_features()

            assert len(retrieved) == 1
            assert retrieved[0].knowledge_feature_ref == "persistent-feature"
            assert retrieved[0].properties["important"] == "data"
            assert retrieved[0].properties["count"] == 123

            doc2.close()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
