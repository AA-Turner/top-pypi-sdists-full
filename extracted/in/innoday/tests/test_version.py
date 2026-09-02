"""
Tests for src.version -- PATCH is computed from git tags rather than
hardcoded, so CI never needs to commit version.py back to main (that
commit-to-protected-branch was the root cause of version-bump.yml failing
on every merge once branch protection required PRs).
"""

from unittest.mock import MagicMock, patch

import src.version as version_module


class TestComputedPatch:
    def setup_method(self):
        version_module._computed_patch.cache_clear()

    def teardown_method(self):
        version_module._computed_patch.cache_clear()

    def test_counts_matching_tags(self):
        fake_result = MagicMock()
        fake_result.stdout = "v1.2.0-beta\nv1.2.1-beta\nv1.2.2-beta\n"
        with (
            patch("src.version.subprocess.run", return_value=fake_result),
            patch("src.version.VERSION_MAJOR", 1),
            patch("src.version.VERSION_MINOR", 2),
            patch.object(version_module, "_REPO_ROOT") as mock_root,
        ):
            mock_root.__truediv__.return_value.exists.return_value = True
            assert version_module._computed_patch() == 3

    def test_returns_zero_when_no_tags_for_this_minor(self):
        fake_result = MagicMock()
        fake_result.stdout = ""
        with (
            patch("src.version.subprocess.run", return_value=fake_result),
            patch("src.version.VERSION_MAJOR", 1),
            patch("src.version.VERSION_MINOR", 2),
            patch.object(version_module, "_REPO_ROOT") as mock_root,
        ):
            mock_root.__truediv__.return_value.exists.return_value = True
            assert version_module._computed_patch() == 0

    def test_returns_zero_without_git_directory(self):
        with (
            patch("src.version.VERSION_MAJOR", 1),
            patch("src.version.VERSION_MINOR", 2),
            patch.object(version_module, "_REPO_ROOT") as mock_root,
        ):
            mock_root.__truediv__.return_value.exists.return_value = False
            assert version_module._computed_patch() == 0

    def test_returns_zero_on_subprocess_failure(self):
        with (
            patch("src.version.subprocess.run", side_effect=OSError("git not found")),
            patch("src.version.VERSION_MAJOR", 1),
            patch("src.version.VERSION_MINOR", 2),
            patch.object(version_module, "_REPO_ROOT") as mock_root,
        ):
            mock_root.__truediv__.return_value.exists.return_value = True
            assert version_module._computed_patch() == 0


class TestVersionOrdering:
    """The 0.100.0b0-0.112.0b0 PyPI releases outranked the 0.1.x reset line
    under PEP 440 ordering while they were live, which is what
    scripts/verify_pypi_latest.py caught on the 0.1.3-beta release. The
    project owner has since yanked all of them on pypi.org -- yanked
    releases are excluded from PyPI's "latest" resolution, so MINOR reverts
    to 1 here rather than staying inflated to 112. See src/version.py's
    docstring for the full history."""

    def test_major_minor_values(self):
        assert version_module.VERSION_MAJOR == 0
        assert version_module.VERSION_MINOR == 1


class TestComputeVersionFromTags:
    """compute_version_from_tags() is what version-bump.yml actually calls
    (never get_version()) -- must always use live tag count and the exact
    "-beta" suffix spelling, never installed/PEP-440-normalized metadata."""

    def setup_method(self):
        version_module._computed_patch.cache_clear()

    def teardown_method(self):
        version_module._computed_patch.cache_clear()

    def test_ignores_installed_metadata_entirely(self):
        with (
            patch("src.version._installed_version", return_value="9.9.9"),
            patch("src.version._computed_patch", return_value=3),
        ):
            assert version_module.compute_version_from_tags() == "0.1.3-beta"

    def test_uses_beta_suffix_not_pep440_normalized_form(self):
        with patch("src.version._computed_patch", return_value=3):
            result = version_module.compute_version_from_tags()
        assert result.endswith("-beta")
        assert "b0" not in result


class TestGetVersion:
    def setup_method(self):
        version_module._computed_patch.cache_clear()

    def teardown_method(self):
        version_module._computed_patch.cache_clear()

    def test_prefers_installed_metadata_when_present(self):
        # Env override and baked file both absent -> installed metadata wins.
        with (
            patch.dict("os.environ", {}, clear=False),
            patch("src.version._baked_version", return_value=""),
            patch("src.version._installed_version", return_value="0.1.5-beta"),
        ):
            version_module.os.environ.pop(version_module._VERSION_ENV_VAR, None)
            assert version_module.get_version() == "0.1.5-beta"

    def test_falls_back_to_computed_patch_when_not_installed(self):
        with (
            patch("src.version._baked_version", return_value=""),
            patch("src.version._installed_version", return_value=""),
            patch("src.version._computed_patch", return_value=3),
        ):
            version_module.os.environ.pop(version_module._VERSION_ENV_VAR, None)
            assert version_module.get_version() == "0.1.3-beta"

    def test_env_var_overrides_everything(self):
        # The runtime override must win over baked file, installed metadata,
        # and live tag computation.
        with (
            patch.dict("os.environ", {version_module._VERSION_ENV_VAR: "7.8.9-test"}),
            patch("src.version._baked_version", return_value="0.1.99-beta"),
            patch("src.version._installed_version", return_value="0.1.50-beta"),
        ):
            assert version_module.get_version() == "7.8.9-test"

    def test_baked_file_wins_over_installed_and_tags(self):
        # This is the deployed-container case: .innoday_version baked at build
        # time must beat the 0.1.0b0 stub the fallbacks resolve to in-image.
        with (
            patch("src.version._baked_version", return_value="0.1.43-beta"),
            patch("src.version._installed_version", return_value=""),
            patch("src.version._computed_patch", return_value=0),
        ):
            version_module.os.environ.pop(version_module._VERSION_ENV_VAR, None)
            assert version_module.get_version() == "0.1.43-beta"

    def test_display_version_prefixes_with_v(self):
        with patch("src.version.get_version", return_value="0.1.1-beta"):
            assert version_module.get_display_version() == "v0.1.1-beta"


class TestGetVersionInfo:
    def test_parses_full_version_string(self):
        with patch("src.version.get_version", return_value="0.1.3-beta"):
            info = version_module.get_version_info()
        assert info == {
            "major": 0,
            "minor": 1,
            "patch": 3,
            "suffix": "beta",
            "full": "0.1.3-beta",
            "display": "v0.1.3-beta",
        }

    def test_handles_no_suffix(self):
        with patch("src.version.get_version", return_value="1.0.0"):
            info = version_module.get_version_info()
        assert info["suffix"] is None
        assert info["major"] == 1
        assert info["minor"] == 0
        assert info["patch"] == 0
