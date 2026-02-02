"""
Test note functionality for document-level annotations.
"""

import pytest
from kodexa_document import Document, NoteInput, NoteType


class TestNoteAccessor:
    """Test note accessor methods."""

    def test_create_and_get_note(self):
        """Test creating and retrieving a note."""
        document = Document(inmemory=True)

        # Create a note
        note_input = NoteInput(content="This is a test note")
        note = document.notes.create(note_input)

        assert note is not None, "Should return the created note"
        assert note["id"] > 0, "Should have a valid ID"
        assert note["content"] == "This is a test note"
        assert note["noteType"] == "TEXT"

        document.close()

    def test_create_note_with_all_fields(self):
        """Test creating a note with all optional fields."""
        document = Document(inmemory=True)

        note_input = NoteInput(
            content="Full note content",
            title="My Note Title",
            note_type=NoteType.markdown,
            properties={"key": "value", "number": 42}
        )
        note = document.notes.create(note_input)

        assert note is not None
        assert note["content"] == "Full note content"
        assert note["title"] == "My Note Title"
        assert note["noteType"] == "MARKDOWN"
        assert note["properties"]["key"] == "value"
        assert note["properties"]["number"] == 42

        document.close()

    def test_get_all_notes(self):
        """Test getting all notes in a document."""
        document = Document(inmemory=True)

        # Initially empty
        notes = document.notes.get_all()
        assert notes == []

        # Create multiple notes
        document.notes.create(NoteInput(content="Note 1"))
        document.notes.create(NoteInput(content="Note 2"))
        document.notes.create(NoteInput(content="Note 3"))

        # Get all
        notes = document.notes.get_all()
        assert len(notes) == 3

        contents = [n["content"] for n in notes]
        assert "Note 1" in contents
        assert "Note 2" in contents
        assert "Note 3" in contents

        document.close()

    def test_update_note(self):
        """Test updating an existing note."""
        document = Document(inmemory=True)

        # Create a note
        note = document.notes.create(NoteInput(content="Original content"))
        note_id = note["id"]

        # Update it
        result = document.notes.update(
            note_id,
            NoteInput(content="Updated content", note_type=NoteType.markdown)
        )
        assert result is True

        # Verify the update
        notes = document.notes.get_all()
        updated_note = next(n for n in notes if n["id"] == note_id)
        assert updated_note["content"] == "Updated content"
        assert updated_note["noteType"] == "MARKDOWN"

        document.close()

    def test_delete_note(self):
        """Test deleting a note."""
        document = Document(inmemory=True)

        # Create a note
        note = document.notes.create(NoteInput(content="Delete me"))
        note_id = note["id"]

        # Verify it exists
        notes = document.notes.get_all()
        assert len(notes) == 1

        # Delete it
        result = document.notes.delete(note_id)
        assert result is True

        # Verify it's gone
        notes = document.notes.get_all()
        assert len(notes) == 0

        document.close()

    def test_note_types(self):
        """Test different note types."""
        document = Document(inmemory=True)

        # Test TEXT (default)
        note_text = document.notes.create(NoteInput(content="Plain text"))
        assert note_text["noteType"] == "TEXT"

        # Test MARKDOWN
        note_md = document.notes.create(NoteInput(content="# Markdown", note_type=NoteType.markdown))
        assert note_md["noteType"] == "MARKDOWN"

        # Test HTML
        note_html = document.notes.create(NoteInput(content="<p>HTML</p>", note_type=NoteType.html))
        assert note_html["noteType"] == "HTML"

        document.close()

    def test_note_with_unicode_content(self):
        """Test notes with Unicode content."""
        document = Document(inmemory=True)

        unicode_contents = [
            "Hello World",
            "Cafe with an accent",
            "Japanese text",
            "Russian text",
            "Emojis",
        ]

        for content in unicode_contents:
            note = document.notes.create(NoteInput(content=content))
            assert note is not None
            assert note["content"] == content

        document.close()

    def test_note_with_long_content(self):
        """Test notes with long content."""
        document = Document(inmemory=True)

        # Create a long note (10KB)
        long_content = "x" * 10240
        note = document.notes.create(NoteInput(content=long_content))

        assert note is not None
        assert note["content"] == long_content
        assert len(note["content"]) == 10240

        document.close()

    def test_multiple_notes_crud(self):
        """Test CRUD operations with multiple notes."""
        document = Document(inmemory=True)

        # Create 5 notes
        created_ids = []
        for i in range(5):
            note = document.notes.create(NoteInput(content=f"Note {i}"))
            created_ids.append(note["id"])

        # Verify all exist
        assert len(document.notes.get_all()) == 5

        # Update one
        document.notes.update(created_ids[2], NoteInput(content="Updated Note 2"))

        # Delete one
        document.notes.delete(created_ids[0])

        # Verify state
        notes = document.notes.get_all()
        assert len(notes) == 4

        # Verify the update
        updated = next(n for n in notes if n["id"] == created_ids[2])
        assert updated["content"] == "Updated Note 2"

        # Verify the delete
        ids = [n["id"] for n in notes]
        assert created_ids[0] not in ids

        document.close()

    def test_empty_notes_list(self):
        """Test operations on empty notes list."""
        document = Document(inmemory=True)

        # All operations should work on empty list
        notes = document.notes.get_all()
        assert notes == []

        document.close()

    def test_note_properties(self):
        """Test notes with complex properties."""
        document = Document(inmemory=True)

        props = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {"a": 1, "b": 2}
        }

        note = document.notes.create(NoteInput(content="Test", properties=props))

        assert note is not None
        assert note["properties"]["string"] == "value"
        assert note["properties"]["number"] == 42
        assert note["properties"]["float"] == 3.14
        assert note["properties"]["boolean"] is True
        assert note["properties"]["array"] == [1, 2, 3]
        assert note["properties"]["nested"]["a"] == 1

        document.close()

    def test_get_note_by_uuid(self):
        """Test getting a note by UUID."""
        document = Document(inmemory=True)

        # Create a note with a specific UUID
        note = document.notes.create(NoteInput(
            content="Test note",
            uuid="test-uuid-12345"
        ))

        # Get by UUID
        fetched = document.notes.get_by_uuid("test-uuid-12345")
        assert fetched is not None
        assert fetched["id"] == note["id"]
        assert fetched["content"] == "Test note"

        # Non-existent UUID returns None
        missing = document.notes.get_by_uuid("non-existent-uuid")
        assert missing is None

        document.close()

    def test_get_notes_by_type(self):
        """Test getting notes by type."""
        document = Document(inmemory=True)

        # Create notes of different types
        document.notes.create(NoteInput(content="Text 1", note_type=NoteType.text))
        document.notes.create(NoteInput(content="Text 2", note_type=NoteType.text))
        document.notes.create(NoteInput(content="Markdown 1", note_type=NoteType.markdown))
        document.notes.create(NoteInput(content="HTML 1", note_type=NoteType.html))

        # Get by type
        text_notes = document.notes.get_by_type("TEXT")
        assert len(text_notes) == 2

        markdown_notes = document.notes.get_by_type("MARKDOWN")
        assert len(markdown_notes) == 1
        assert markdown_notes[0]["content"] == "Markdown 1"

        html_notes = document.notes.get_by_type("HTML")
        assert len(html_notes) == 1
        assert html_notes[0]["content"] == "HTML 1"

        document.close()

    def test_get_notes_by_group_uuid(self):
        """Test getting notes by group UUID."""
        document = Document(inmemory=True)

        # Create notes in different groups
        document.notes.create(NoteInput(content="Group1 Note1", group_uuid="group-1"))
        document.notes.create(NoteInput(content="Group1 Note2", group_uuid="group-1"))
        document.notes.create(NoteInput(content="Group2 Note1", group_uuid="group-2"))
        document.notes.create(NoteInput(content="No Group"))

        # Get by group UUID
        group1_notes = document.notes.get_by_group_uuid("group-1")
        assert len(group1_notes) == 2
        contents = [n["content"] for n in group1_notes]
        assert "Group1 Note1" in contents
        assert "Group1 Note2" in contents

        group2_notes = document.notes.get_by_group_uuid("group-2")
        assert len(group2_notes) == 1
        assert group2_notes[0]["content"] == "Group2 Note1"

        # Non-existent group returns empty list
        empty_group = document.notes.get_by_group_uuid("non-existent-group")
        assert empty_group == []

        document.close()

    def test_get_root_notes(self):
        """Test getting root notes (notes without a parent)."""
        document = Document(inmemory=True)

        # Create root notes (no parent)
        root1 = document.notes.create(NoteInput(content="Root 1"))
        root2 = document.notes.create(NoteInput(content="Root 2"))

        # Create child notes
        document.notes.create(NoteInput(content="Child 1", parent_note_id=root1["id"]))
        document.notes.create(NoteInput(content="Child 2", parent_note_id=root1["id"]))
        document.notes.create(NoteInput(content="Child 3", parent_note_id=root2["id"]))

        # Get root notes
        root_notes = document.notes.get_root_notes()
        assert len(root_notes) == 2
        contents = [n["content"] for n in root_notes]
        assert "Root 1" in contents
        assert "Root 2" in contents

        document.close()

    def test_get_child_notes(self):
        """Test getting child notes of a parent note."""
        document = Document(inmemory=True)

        # Create parent and child notes
        parent = document.notes.create(NoteInput(content="Parent"))
        child1 = document.notes.create(NoteInput(content="Child 1", parent_note_id=parent["id"]))
        child2 = document.notes.create(NoteInput(content="Child 2", parent_note_id=parent["id"]))

        # Create another parent with different children
        parent2 = document.notes.create(NoteInput(content="Parent 2"))
        document.notes.create(NoteInput(content="Child 3", parent_note_id=parent2["id"]))

        # Get children of first parent
        children = document.notes.get_child_notes(parent["id"])
        assert len(children) == 2
        contents = [n["content"] for n in children]
        assert "Child 1" in contents
        assert "Child 2" in contents

        # Get children of second parent
        children2 = document.notes.get_child_notes(parent2["id"])
        assert len(children2) == 1
        assert children2[0]["content"] == "Child 3"

        # Non-existent parent returns empty list
        no_children = document.notes.get_child_notes(99999)
        assert no_children == []

        document.close()

    def test_note_hierarchy(self):
        """Test full hierarchy operations with notes."""
        document = Document(inmemory=True)

        # Create a hierarchy: grandparent -> parent -> children
        grandparent = document.notes.create(NoteInput(content="Grandparent"))
        parent = document.notes.create(NoteInput(content="Parent", parent_note_id=grandparent["id"]))
        child1 = document.notes.create(NoteInput(content="Child 1", parent_note_id=parent["id"]))
        child2 = document.notes.create(NoteInput(content="Child 2", parent_note_id=parent["id"]))

        # Only grandparent should be a root note
        roots = document.notes.get_root_notes()
        assert len(roots) == 1
        assert roots[0]["id"] == grandparent["id"]

        # Grandparent should have parent as child
        gp_children = document.notes.get_child_notes(grandparent["id"])
        assert len(gp_children) == 1
        assert gp_children[0]["id"] == parent["id"]

        # Parent should have child1 and child2 as children
        p_children = document.notes.get_child_notes(parent["id"])
        assert len(p_children) == 2

        document.close()
