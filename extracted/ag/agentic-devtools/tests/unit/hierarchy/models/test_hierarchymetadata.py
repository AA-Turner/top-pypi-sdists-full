"""Tests for HierarchyMetadata dataclass."""

from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestHierarchyMetadata:
    """Tests for HierarchyMetadata construction and serialization."""

    def test_default_construction(self) -> None:
        meta = HierarchyMetadata(level=HierarchyLevel.EPIC)
        assert meta.level == HierarchyLevel.EPIC
        assert meta.parent is None
        assert meta.children == []
        assert meta.informational_children == []

    def test_full_construction(self) -> None:
        children = [
            ChildInfo(number=101, title="Feature A"),
            ChildInfo(number=102, title="Feature B"),
        ]
        info_children = [ChildInfo(number=201, title="Deep child")]
        meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=children,
            informational_children=info_children,
        )
        assert meta.level == HierarchyLevel.FEATURE
        assert meta.parent == 100
        assert len(meta.children) == 2
        assert len(meta.informational_children) == 1

    def test_to_dict(self) -> None:
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildInfo(number=101, title="Feature A")],
        )
        d = meta.to_dict()
        assert d["level"] == "epic"
        assert d["parent"] is None
        assert len(d["children"]) == 1
        assert d["children"][0]["number"] == 101
        assert d["children"][0]["title"] == "Feature A"
        assert d["informational_children"] == []

    def test_standalone_metadata(self) -> None:
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        assert meta.level == HierarchyLevel.STANDALONE
        assert meta.parent is None
        assert meta.children == []
