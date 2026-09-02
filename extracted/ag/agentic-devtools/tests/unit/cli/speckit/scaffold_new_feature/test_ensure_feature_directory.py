"""Tests for ``ensure_feature_directory``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import ensure_feature_directory


def test_ensure_feature_directory_uses_template_when_present(tmp_path: Path) -> None:
    template_path = tmp_path / ".specify" / "presets" / "agdt-templates" / "templates" / "spec-template.md"
    template_path.parent.mkdir(parents=True)
    template_path.write_text("# Template\n", encoding="utf-8")
    feature_dir, spec_file = ensure_feature_directory(tmp_path, "7", "Feature seven")
    assert feature_dir == tmp_path / "specs" / "7-feature-seven"
    assert spec_file.read_text(encoding="utf-8") == "# Template\n"


def test_ensure_feature_directory_falls_back_to_empty_spec_when_no_template(tmp_path: Path) -> None:
    _feature_dir, spec_file = ensure_feature_directory(tmp_path, "8", "Feature eight")
    assert spec_file.read_text(encoding="utf-8") == ""


def test_ensure_feature_directory_ignores_template_resolving_outside_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    template_path = tmp_path / ".specify" / "presets" / "agdt-templates" / "templates" / "spec-template.md"
    template_path.parent.mkdir(parents=True)
    template_path.write_text("# Should not copy\n", encoding="utf-8")
    real_resolve = Path.resolve

    def _fake_resolve(self: Path, *args, **kwargs) -> Path:
        if self == template_path:
            return tmp_path.parent / "outside-spec-template.md"
        return real_resolve(self, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", _fake_resolve)
    _feature_dir, spec_file = ensure_feature_directory(tmp_path, "8", "Feature eight")
    assert spec_file.read_text(encoding="utf-8") == ""


def test_ensure_feature_directory_supports_nested_parent_without_description(tmp_path: Path) -> None:
    parent_dir = tmp_path / "specs" / "1-parent"
    parent_dir.mkdir(parents=True)
    feature_dir, _spec_file = ensure_feature_directory(
        tmp_path,
        "2",
        "Feature two",
        parent_dir=parent_dir,
        use_description_in_name=False,
    )
    assert feature_dir == parent_dir / "2"


def test_ensure_feature_directory_rejects_path_outside_repo(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-repo"
    with pytest.raises(ValueError, match="outside the repository root"):
        ensure_feature_directory(tmp_path, "outside", "Evil Feature", parent_dir=outside)


def test_ensure_feature_directory_rejects_symlinked_target(tmp_path: Path) -> None:
    specs_dir = tmp_path / "specs"
    specs_dir.mkdir(parents=True)
    # Symlink within the repo root — should still be rejected
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature.Path.is_symlink", return_value=True):
        with pytest.raises(ValueError, match="symlinked or non-directory target"):
            ensure_feature_directory(tmp_path, "evil-link", "Evil Feature", use_description_in_name=False)


def test_ensure_feature_directory_rejects_symlinked_spec_file(tmp_path: Path) -> None:
    feature_dir = tmp_path / "specs" / "7-feature-seven"
    feature_dir.mkdir(parents=True)
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature.Path.is_symlink", side_effect=[False, True]):
        with pytest.raises(ValueError, match="Refusing to seed symlinked spec.md"):
            ensure_feature_directory(tmp_path, "7", "Feature seven")


def test_ensure_feature_directory_rejects_non_file_spec_path(tmp_path: Path) -> None:
    feature_dir = tmp_path / "specs" / "7-feature-seven"
    spec_path = feature_dir / "spec.md"
    spec_path.mkdir(parents=True)
    with pytest.raises(ValueError, match="Refusing to seed non-file spec.md"):
        ensure_feature_directory(tmp_path, "7", "Feature seven")


def test_ensure_feature_directory_preserves_existing_spec_content(tmp_path: Path) -> None:
    # Intentional compatibility exception: unlike the legacy bash flow, existing spec.md
    # is preserved rather than overwritten, to protect developer-authored content.
    template_path = tmp_path / ".specify" / "presets" / "agdt-templates" / "templates" / "spec-template.md"
    template_path.parent.mkdir(parents=True)
    template_path.write_text("# Template\n", encoding="utf-8")
    feature_dir = tmp_path / "specs" / "7-feature-seven"
    feature_dir.mkdir(parents=True)
    (feature_dir / "spec.md").write_text("# Developer content\n", encoding="utf-8")

    _feature_dir, spec_file = ensure_feature_directory(tmp_path, "7", "Feature seven")

    assert spec_file.read_text(encoding="utf-8") == "# Developer content\n"
