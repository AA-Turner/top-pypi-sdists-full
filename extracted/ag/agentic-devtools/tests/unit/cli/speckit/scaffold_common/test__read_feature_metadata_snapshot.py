"""Tests for ``_read_feature_metadata_snapshot``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_common import FeatureResolutionError, _read_feature_metadata_snapshot

_METADATA_PATH = Path(".specify") / "feature.json"


class TestReadFeatureMetadataSnapshot:
    """_read_feature_metadata_snapshot reads both fields from a single JSON parse."""

    def test_returns_both_fields_when_present(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "042-my-feature", "branch_name": "42-add-login"}', encoding="utf-8")
        feature_directory, branch_name = _read_feature_metadata_snapshot(tmp_path)
        assert feature_directory == "042-my-feature"
        assert branch_name == "42-add-login"

    def test_returns_none_branch_when_field_missing(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "042-my-feature"}', encoding="utf-8")
        feature_directory, branch_name = _read_feature_metadata_snapshot(tmp_path)
        assert feature_directory == "042-my-feature"
        assert branch_name is None

    def test_returns_none_none_when_file_absent(self, tmp_path: Path) -> None:
        assert _read_feature_metadata_snapshot(tmp_path) == (None, None)

    def test_raises_when_feature_directory_path_is_a_directory(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.mkdir()  # directory instead of file
        with pytest.raises(FeatureResolutionError, match="exists but is not a regular file"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_raises_on_invalid_json(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text("not json", encoding="utf-8")
        with pytest.raises(FeatureResolutionError, match="invalid JSON"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_raises_when_root_is_not_dict(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text("[1, 2, 3]", encoding="utf-8")
        with pytest.raises(FeatureResolutionError, match="JSON object"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_raises_when_feature_directory_is_blank(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "   "}', encoding="utf-8")
        with pytest.raises(FeatureResolutionError, match="invalid 'feature_directory'"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_raises_when_feature_directory_is_null(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": null}', encoding="utf-8")
        with pytest.raises(FeatureResolutionError, match="invalid 'feature_directory'"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_returns_none_feature_directory_when_key_missing(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"branch_name": "42-add-login"}', encoding="utf-8")
        feature_directory, branch_name = _read_feature_metadata_snapshot(tmp_path)
        assert feature_directory is None
        assert branch_name == "42-add-login"

    def test_branch_name_none_when_blank(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "042-my-feature", "branch_name": "  "}', encoding="utf-8")
        feature_directory, branch_name = _read_feature_metadata_snapshot(tmp_path)
        assert feature_directory == "042-my-feature"
        assert branch_name is None

    def test_strips_whitespace_from_both_fields(self, tmp_path: Path) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "  042-x  ", "branch_name": "  42-login  "}', encoding="utf-8")
        feature_directory, branch_name = _read_feature_metadata_snapshot(tmp_path)
        assert feature_directory == "042-x"
        assert branch_name == "42-login"

    def test_raises_on_oserror(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "042-x"}', encoding="utf-8")

        def _raise(self, *args, **kwargs):
            raise OSError("permission denied")

        monkeypatch.setattr(Path, "read_text", _raise)
        with pytest.raises(FeatureResolutionError, match="Cannot read"):
            _read_feature_metadata_snapshot(tmp_path)

    def test_raises_on_unicode_decode_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        meta = tmp_path / _METADATA_PATH
        meta.parent.mkdir(parents=True)
        meta.write_text('{"feature_directory": "042-x"}', encoding="utf-8")

        def _raise(self, *args, **kwargs):
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid byte")

        monkeypatch.setattr(Path, "read_text", _raise)
        with pytest.raises(FeatureResolutionError, match="Cannot read"):
            _read_feature_metadata_snapshot(tmp_path)
