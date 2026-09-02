"""Tests for the ``_filter_shadowed_basename_references()`` helper."""

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import _filter_shadowed_basename_references


def _make_ref(text: str, plan_location: str = "L1") -> Reference:
    return Reference(text=text, kind=ReferenceKind.FILE_PATH, plan_location=plan_location, context_sentence="")


class TestFilterShadowedBasenameReferences:
    def test_path_with_slash_passes_through(self) -> None:
        ref = _make_ref("docs/file.md", "L1")
        assert _filter_shadowed_basename_references("docs/file.md", [ref]) == [ref]

    def test_non_line_location_passes_through(self) -> None:
        ref = _make_ref("file.md", "Summary")
        assert _filter_shadowed_basename_references("file.md", [ref]) == [ref]

    def test_out_of_range_line_number_passes_through(self) -> None:
        ref = _make_ref("file.md", "L99")
        assert _filter_shadowed_basename_references("one line only", [ref]) == [ref]

    def test_drops_basename_shadowed_by_full_path_on_same_line(self) -> None:
        content = "Update `docs/file.md`.\n"
        full_ref = _make_ref("docs/file.md", "L1")
        basename_ref = _make_ref("file.md", "L1")
        result = _filter_shadowed_basename_references(content, [full_ref, basename_ref])
        texts = {r.text for r in result}
        assert "docs/file.md" in texts
        assert "file.md" not in texts

    def test_preserves_unshadowed_basename(self) -> None:
        ref = _make_ref("file.md", "L1")
        result = _filter_shadowed_basename_references("Update file.md.\n", [ref])
        assert result == [ref]

    def test_preserves_standalone_basename_when_full_path_is_not_ancestor(self) -> None:
        content = "Update `docs/ai-pr-loop.yml` and `loop.yml`.\n"
        full_ref = _make_ref("docs/ai-pr-loop.yml", "L1")
        standalone_ref = _make_ref("loop.yml", "L1")
        result = _filter_shadowed_basename_references(content, [full_ref, standalone_ref])
        assert standalone_ref in result

    def test_drops_basename_appearing_only_as_markdown_link_label(self) -> None:
        content = "Write findings to [research.md](docs/research.md).\n"
        full_ref = _make_ref("docs/research.md", "L1")
        basename_ref = _make_ref("research.md", "L1")
        result = _filter_shadowed_basename_references(content, [full_ref, basename_ref])
        texts = {r.text for r in result}
        assert "docs/research.md" in texts
        assert "research.md" not in texts
