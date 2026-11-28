from __future__ import annotations

import logging

import pytest
from hatchling.metadata.plugin.interface import MetadataHookInterface

from hatchling_autoextras_hook.hooks import (
    AutoExtrasMetadataHook,
    _dependencies,
    _normalize,
    _read_warn_only,
    hatch_register_metadata_hook,
)

WARN_ONLY_ENV = "HATCHLING_AUTOEXTRAS_WARN_ONLY"


@pytest.fixture(autouse=True)
def _unset_warn_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the tests independent of the environment of the caller."""
    monkeypatch.delenv(WARN_ONLY_ENV, raising=False)


def test_plugin_name() -> None:
    """Test that the plugin name is correct."""
    assert AutoExtrasMetadataHook.PLUGIN_NAME == "autoextras"


@pytest.mark.parametrize("extra_name", [None, 1, ["all"]])
def test_invalid_extra_name_type(extra_name: object) -> None:
    with pytest.raises(TypeError, match=r"'extra-name' in .* must be a string"):
        AutoExtrasMetadataHook("test", {"extra-name": extra_name})


@pytest.mark.parametrize(
    "extra_name",
    ["", " ", "\t\n", " all ", "a b", "-a", "a-", "_a", "a_", ".a", "a.", "é", "all\n"],
)
def test_invalid_extra_name_value(extra_name: str) -> None:
    with pytest.raises(ValueError, match=r"'extra-name' in .* must be a valid extra name"):
        AutoExtrasMetadataHook("test", {"extra-name": extra_name})


@pytest.mark.parametrize(
    "extra_name", ["all", "full", "my_extra", "my-extra", "a.b", "a", "A1", "9"]
)
def test_valid_extra_name(extra_name: str) -> None:
    hook = AutoExtrasMetadataHook("test", {"extra-name": extra_name})
    assert hook.config["extra-name"] == extra_name


@pytest.mark.parametrize("exclude", ["dev", ("dev",), {"dev"}, None, 1])
def test_invalid_exclude_type(exclude: object) -> None:
    with pytest.raises(TypeError, match=r"'exclude' in .* must be a list of extra names"):
        AutoExtrasMetadataHook("test", {"exclude": exclude})


@pytest.mark.parametrize("overwrite", ["true", 1, 0, None])
def test_invalid_overwrite_type(overwrite: object) -> None:
    with pytest.raises(TypeError, match=r"'overwrite' in .* must be a boolean"):
        AutoExtrasMetadataHook("test", {"overwrite": overwrite})


def test_default_config() -> None:
    hook = AutoExtrasMetadataHook("test", {})
    assert hook.config == {"extra-name": "all", "exclude": [], "overwrite": False}


def test_config_overrides_defaults() -> None:
    hook = AutoExtrasMetadataHook(
        "test", {"extra-name": "full", "exclude": ["dev"], "overwrite": True}
    )
    assert hook.config == {"extra-name": "full", "exclude": ["dev"], "overwrite": True}


def test_update_default_extra_name() -> None:
    """Test that the default extra name is 'all'."""
    hook = AutoExtrasMetadataHook("test", {})
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=4.0"],
        }
    }
    hook.update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["black>=22.0", "pytest>=7.0", "sphinx>=4.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=4.0"],
        }
    }


def test_update_custom_extra_name() -> None:
    """Test that a custom extra name can be configured."""
    hook = AutoExtrasMetadataHook("test", {"extra-name": "complete"})
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=4.0"],
        }
    }
    hook.update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "complete": ["black>=22.0", "pytest>=7.0", "sphinx>=4.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=4.0"],
        }
    }


def test_update_with_no_optional_dependencies() -> None:
    """Test that update does nothing when there are no optional
    dependencies."""
    metadata = {}
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {"optional-dependencies": {"all": []}}


def test_update_with_empty_optional_dependencies() -> None:
    """Test that update does nothing when optional dependencies is
    empty."""
    metadata = {"optional-dependencies": {}}
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {"optional-dependencies": {"all": []}}


def test_update_with_single_extra() -> None:
    """Test that update creates 'all' extra with dependencies from one
    extra."""
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["black>=22.0", "pytest>=7.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
        }
    }


def test_update_with_multiple_extras() -> None:
    """Test that update creates 'all' extra combining all extras."""
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=5.0", "sphinx-rtd-theme>=1.0"],
            "typing": ["mypy>=1.0"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": [
                "black>=22.0",
                "mypy>=1.0",
                "pytest>=7.0",
                "sphinx-rtd-theme>=1.0",
                "sphinx>=5.0",
            ],
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=5.0", "sphinx-rtd-theme>=1.0"],
            "typing": ["mypy>=1.0"],
        }
    }


def test_update_with_duplicate_dependencies() -> None:
    """Test that update handles duplicate dependencies across extras."""
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
            "test": ["pytest>=7.0", "coverage>=6.0"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["black>=22.0", "coverage>=6.0", "pytest>=7.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
            "test": ["pytest>=7.0", "coverage>=6.0"],
        }
    }


def test_update_sorts_dependencies() -> None:
    """Test that dependencies in 'all' extra are sorted."""
    metadata = {
        "optional-dependencies": {
            "dev": ["zzz-package", "aaa-package", "mmm-package"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["aaa-package", "mmm-package", "zzz-package"],
            "dev": ["zzz-package", "aaa-package", "mmm-package"],
        }
    }


def test_update_does_not_overwrite_all() -> None:
    """Test that update raises an error if 'all' extra already
    exists."""
    metadata = {
        "optional-dependencies": {
            "all": ["old-dependency"],
            "dev": ["pytest>=7.0", "black>=22.0"],
        }
    }
    hook = AutoExtrasMetadataHook(root="test", config={})
    with pytest.raises(ValueError, match=r"Cannot create the 'all' extra: 'all' already exists"):
        hook.update(metadata)


def test_update_overwrite_all() -> None:
    """Test that update replaces an existing 'all' extra when overwrite
    is True."""
    metadata = {
        "optional-dependencies": {
            "all": ["old-dependency"],
            "dev": ["pytest>=7.0", "black>=22.0"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={"overwrite": True}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["black>=22.0", "pytest>=7.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
        }
    }


def test_update_with_exclude() -> None:
    """Test that update excludes some extras."""
    metadata = {
        "optional-dependencies": {
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=5.0", "sphinx-rtd-theme>=1.0"],
            "typing": ["mypy>=1.0"],
        }
    }
    AutoExtrasMetadataHook(root="test", config={"exclude": ["dev"]}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "all": ["mypy>=1.0", "sphinx-rtd-theme>=1.0", "sphinx>=5.0"],
            "dev": ["pytest>=7.0", "black>=22.0"],
            "docs": ["sphinx>=5.0", "sphinx-rtd-theme>=1.0"],
            "typing": ["mypy>=1.0"],
        }
    }


def test_hatch_register_metadata_hook_returns_a_class() -> None:
    """The plugin registration function returns a class."""
    assert isinstance(hatch_register_metadata_hook(), type)


def test_hatch_register_metadata_hook_returns_correct_class() -> None:
    """The plugin registration function returns the hook class."""
    assert hatch_register_metadata_hook() is AutoExtrasMetadataHook


def test_hatch_register_metadata_hook_returns_a_hook_interface() -> None:
    """The class returned by the plugin registration function is a
    hatchling metadata hook."""
    assert issubclass(hatch_register_metadata_hook(), MetadataHookInterface)


def test_update_strips_whitespace() -> None:
    metadata = {"optional-dependencies": {"dev": ["  pytest>=7.0 ", "pytest>=7.0"]}}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata["optional-dependencies"]["all"] == ["pytest>=7.0"]


def test_update_exclude_all_extras() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["dev", "docs"]}).update(metadata)
    assert metadata["optional-dependencies"]["all"] == []


def test_update_overwrite_with_exclude() -> None:
    metadata = {"optional-dependencies": {"all": ["old"], "dev": ["pytest"], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True, "exclude": ["dev"]}).update(metadata)
    assert metadata["optional-dependencies"]["all"] == ["sphinx"]


def test_update_does_not_overwrite_custom_extra() -> None:
    metadata = {"optional-dependencies": {"complete": ["old"], "dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"extra-name": "complete"})
    with pytest.raises(
        ValueError, match=r"Cannot create the 'complete' extra: 'complete' already exists"
    ):
        hook.update(metadata)


def test_update_does_not_overwrite_custom_extra_suggests_overwrite() -> None:
    metadata = {"optional-dependencies": {"complete": ["old"], "dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"extra-name": "complete"})
    with pytest.raises(ValueError, match=r"overwrite = true"):
        hook.update(metadata)


def test_update_does_not_overwrite_custom_extra_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"complete": ["old"], "dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"extra-name": "complete"})
    with pytest.raises(ValueError, match=r"already exists"):
        hook.update(metadata)
    assert metadata == {"optional-dependencies": {"complete": ["old"], "dev": ["pytest"]}}


def test_update_all_exists_when_custom_extra_name() -> None:
    """An existing 'all' extra is treated as a regular extra when the
    extra name differs."""
    metadata = {"optional-dependencies": {"all": ["numpy"], "dev": ["pytest"]}}
    AutoExtrasMetadataHook("test", {"extra-name": "complete"}).update(metadata)
    assert metadata["optional-dependencies"]["complete"] == ["numpy", "pytest"]


def test_update_does_not_modify_source_extras() -> None:
    dev = ["pytest", "black"]
    metadata = {"optional-dependencies": {"dev": dev}}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert dev == ["pytest", "black"]


def test_update_preserves_other_metadata() -> None:
    metadata = {"name": "pkg", "optional-dependencies": {"dev": ["pytest"]}}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata["name"] == "pkg"


def test_update_is_idempotent_with_overwrite() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"overwrite": True})
    hook.update(metadata)
    first = {k: list(v) for k, v in metadata["optional-dependencies"].items()}
    hook.update(metadata)
    assert metadata["optional-dependencies"] == first


def test_update_sorts_as_strings() -> None:
    metadata = {"optional-dependencies": {"dev": ["sphinx>=5", "sphinx-rtd", "Zed", "alpha"]}}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "dev": ["sphinx>=5", "sphinx-rtd", "Zed", "alpha"],
            "all": ["Zed", "alpha", "sphinx-rtd", "sphinx>=5"],
        }
    }


@pytest.mark.parametrize("warn_only", ["0", "1"])
def test_update_output_is_the_same_in_strict_and_warn_only_modes(
    monkeypatch: pytest.MonkeyPatch, warn_only: str
) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, warn_only)
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["docs"]}).update(metadata)
    assert metadata == {
        "optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"], "all": ["pytest"]}
    }


def test_update_logs_debug(caplog: pytest.LogCaptureFixture) -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with caplog.at_level(logging.DEBUG, logger="hatchling_autoextras_hook.hooks"):
        AutoExtrasMetadataHook("test", {}).update(metadata)
    assert "Created 'all' with 1 dependencies from 1 extras" in caplog.text


@pytest.mark.parametrize("exclude", [[1], ["dev", None]])
def test_invalid_exclude_item_type(exclude: object) -> None:
    with pytest.raises(TypeError, match=r"'exclude' in .* must be a list of extra names"):
        AutoExtrasMetadataHook("test", {"exclude": exclude})


@pytest.mark.parametrize("deps", ["pytest", ("pytest",), None, 1])
def test_update_invalid_extra_dependencies(deps: object) -> None:
    metadata = {"optional-dependencies": {"dev": deps}}
    with pytest.raises(TypeError, match=r"Dependencies of extra 'dev' must be a list"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


@pytest.mark.parametrize("optional", [["pytest"], "pytest", 1])
def test_update_invalid_optional_dependencies(optional: object) -> None:
    with pytest.raises(TypeError, match=r"'optional-dependencies' must be a table"):
        AutoExtrasMetadataHook("test", {}).update({"optional-dependencies": optional})


def test_update_failure_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": "sphinx"}}
    with pytest.raises(TypeError, match=r"must be a list of strings"):
        AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata == {"optional-dependencies": {"dev": ["pytest"], "docs": "sphinx"}}


def test_update_logs_overwrite(caplog: pytest.LogCaptureFixture) -> None:
    metadata = {"optional-dependencies": {"all": ["old"], "dev": ["pytest"]}}
    with caplog.at_level(logging.DEBUG, logger="hatchling_autoextras_hook.hooks"):
        AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert "Overwriting existing 'all' extra" in caplog.text


#########################################
#     Tests for the unknown options     #
#########################################


def test_unknown_option_raises() -> None:
    with pytest.raises(ValueError, match=r"Unknown option\(s\) in .*: \['excludes'\]"):
        AutoExtrasMetadataHook("test", {"excludes": ["dev"]})


def test_unknown_option_message_lists_valid_options() -> None:
    with pytest.raises(
        ValueError, match=r"Valid options: \['exclude', 'extra-name', 'overwrite'\]"
    ):
        AutoExtrasMetadataHook("test", {"excludes": ["dev"]})


def test_old_option_name_group_name_is_unknown() -> None:
    with pytest.raises(
        ValueError,
        match=r"Unknown option\(s\) in .*: \['group-name'\]\. "
        r"Valid options: \['exclude', 'extra-name', 'overwrite'\]",
    ):
        AutoExtrasMetadataHook("test", {"group-name": "complete"})


def test_unknown_options_are_reported_sorted() -> None:
    with pytest.raises(ValueError, match=r"Unknown option\(s\) in .*: \['alpha', 'zeta'\]"):
        AutoExtrasMetadataHook("test", {"zeta": 1, "alpha": 2})


def test_unknown_option_with_valid_options_raises() -> None:
    with pytest.raises(ValueError, match=r"Unknown option\(s\) in .*: \['typo'\]"):
        AutoExtrasMetadataHook("test", {"extra-name": "full", "typo": True})


def test_unknown_option_warn_only_warns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.warns(UserWarning, match=r"Unknown option\(s\) in .*: \['excludes'\]"):
        AutoExtrasMetadataHook("test", {"excludes": ["dev"]})


def test_unknown_option_warn_only_is_dropped_from_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.warns(UserWarning, match=r"Unknown option"):
        hook = AutoExtrasMetadataHook("test", {"excludes": ["dev"], "extra-name": "full"})
    assert hook.config == {"extra-name": "full", "exclude": [], "overwrite": False}


def test_unknown_option_warn_only_ignores_the_option(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"]}}
    with pytest.warns(UserWarning, match=r"Unknown option"):
        hook = AutoExtrasMetadataHook("test", {"excludes": ["dev"]})
    hook.update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "dev": ["pytest"],
            "docs": ["sphinx"],
            "all": ["pytest", "sphinx"],
        }
    }


def test_warn_only_does_not_downgrade_invalid_extra_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.raises(ValueError, match=r"'extra-name' in .* must be a valid extra name"):
        AutoExtrasMetadataHook("test", {"extra-name": ""})


def test_warn_only_does_not_downgrade_invalid_exclude(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.raises(TypeError, match=r"'exclude' in .* must be a list of extra names"):
        AutoExtrasMetadataHook("test", {"exclude": "dev"})


def test_warn_only_does_not_downgrade_invalid_overwrite(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.raises(TypeError, match=r"'overwrite' in .* must be a boolean"):
        AutoExtrasMetadataHook("test", {"overwrite": "true"})


def test_default_config_is_not_shared_between_hooks() -> None:
    hook1 = AutoExtrasMetadataHook("test", {})
    hook1.config["exclude"].append("dev")
    assert AutoExtrasMetadataHook("test", {}).config["exclude"] == []


###############################
#     Tests for _report       #
###############################


def test_report_raises_by_default() -> None:
    hook = AutoExtrasMetadataHook("test", {})
    with pytest.raises(ValueError, match=r"something is wrong"):
        hook._report("something is wrong")


def test_report_warns_in_warn_only_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    hook = AutoExtrasMetadataHook("test", {})
    with pytest.warns(UserWarning, match=r"something is wrong"):
        hook._report("something is wrong")


#####################################
#     Tests for _read_warn_only     #
#####################################


@pytest.mark.parametrize("value", ["1", "true", "TRUE", "True", "yes", "YES", "on", "On", " 1 "])
def test_read_warn_only_enabled(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, value)
    assert _read_warn_only() is True


@pytest.mark.parametrize("value", ["0", "false", "FALSE", "no", "NO", "off", "Off", "", "  "])
def test_read_warn_only_disabled(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, value)
    assert _read_warn_only() is False


def test_read_warn_only_unset() -> None:
    assert _read_warn_only() is False


@pytest.mark.parametrize("value", ["maybe", "2", "enabled", "y"])
def test_read_warn_only_invalid(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, value)
    with pytest.raises(ValueError, match=r"HATCHLING_AUTOEXTRAS_WARN_ONLY"):
        _read_warn_only()


def test_init_invalid_warn_only_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "maybe")
    with pytest.raises(ValueError, match=r"Invalid value 'maybe'"):
        AutoExtrasMetadataHook("test", {})


##############################
#     Tests for _normalize   #
##############################


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Dev_Extra", "dev-extra"),
        ("dev.extra", "dev-extra"),
        ("a..b", "a-b"),
        ("A-_-B", "a-b"),
        ("dev", "dev"),
        ("dev-extra", "dev-extra"),
        ("", ""),
    ],
)
def test_normalize(name: str, expected: str) -> None:
    assert _normalize(name) == expected


def test_normalize_is_idempotent() -> None:
    assert _normalize(_normalize("A_.b")) == "a-b"


#######################################
#     Tests for the normalized names  #
#######################################


@pytest.mark.parametrize("exclude", [["ALL"], ["All"], ["all"]])
def test_exclude_generated_extra_raises(exclude: list[str]) -> None:
    with pytest.raises(
        ValueError, match=r"'exclude' in .* must not contain the generated extra 'all'"
    ):
        AutoExtrasMetadataHook("test", {"exclude": exclude})


def test_exclude_generated_extra_other_spelling_raises() -> None:
    with pytest.raises(ValueError, match=r"'exclude' in .* must not contain the generated extra"):
        AutoExtrasMetadataHook("test", {"extra-name": "my_extra", "exclude": ["My.Extra"]})


def test_update_exclude_is_case_insensitive() -> None:
    metadata = {"optional-dependencies": {"a": ["x"], "b": ["y"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["A"]}).update(metadata)
    assert metadata == {"optional-dependencies": {"a": ["x"], "b": ["y"], "all": ["y"]}}


def test_update_exclude_matches_other_separator() -> None:
    metadata = {"optional-dependencies": {"B_c": ["x"], "d": ["y"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["B.c"]}).update(metadata)
    assert metadata == {"optional-dependencies": {"B_c": ["x"], "d": ["y"], "all": ["y"]}}


def test_update_conflict_is_case_insensitive() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"Cannot create the 'all' extra: 'All' already exists"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_conflict_failure_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"already exists"):
        AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata == {"optional-dependencies": {"All": ["old"], "dev": ["pytest"]}}


def test_update_conflict_with_other_separator() -> None:
    metadata = {"optional-dependencies": {"my.extra": ["old"], "dev": ["pytest"]}}
    with pytest.raises(
        ValueError, match=r"Cannot create the 'my_extra' extra: 'my.extra' already exists"
    ):
        AutoExtrasMetadataHook("test", {"extra-name": "my_extra"}).update(metadata)


def test_update_overwrite_replaces_existing_spelling() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert metadata == {"optional-dependencies": {"dev": ["pytest"], "all": ["pytest"]}}


def test_update_overwrite_logs_existing_spelling(caplog: pytest.LogCaptureFixture) -> None:
    metadata = {"optional-dependencies": {"ALL": ["old"], "dev": ["pytest"]}}
    with caplog.at_level(logging.DEBUG, logger="hatchling_autoextras_hook.hooks"):
        AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert "Overwriting existing 'ALL' extra" in caplog.text


def test_update_custom_extra_name_with_exclude() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"], "aws": ["boto3"]}}
    AutoExtrasMetadataHook("test", {"extra-name": "full", "exclude": ["DEV", "docs"]}).update(
        metadata
    )
    assert metadata == {
        "optional-dependencies": {
            "dev": ["pytest"],
            "docs": ["sphinx"],
            "aws": ["boto3"],
            "full": ["boto3"],
        }
    }


###############################
#     Tests for _dependencies #
###############################


def test_dependencies_strips_items() -> None:
    assert _dependencies("dev", ["  pytest>=7.0 ", "black"]) == ["pytest>=7.0", "black"]


def test_dependencies_empty_list() -> None:
    assert _dependencies("dev", []) == []


def test_dependencies_keeps_duplicates() -> None:
    assert _dependencies("dev", ["pytest", " pytest"]) == ["pytest", "pytest"]


@pytest.mark.parametrize("value", ["pytest", ("pytest",), None, 1, {"pytest"}])
def test_dependencies_not_a_list_raises(value: object) -> None:
    with pytest.raises(TypeError, match=r"Dependencies of extra 'dev' must be a list of strings"):
        _dependencies("dev", value)


@pytest.mark.parametrize("item", [1, None, 1.5, ["pytest"], b"pytest"])
def test_dependencies_non_string_item_raises(item: object) -> None:
    with pytest.raises(TypeError, match=r"Dependency #2 of extra 'dev' must be a string"):
        _dependencies("dev", ["pytest", item])


@pytest.mark.parametrize("item", ["", " ", "\t\n"])
def test_dependencies_blank_item_raises(item: str) -> None:
    with pytest.raises(ValueError, match=r"Dependency #2 of extra 'dev' must not be blank"):
        _dependencies("dev", ["pytest", item])


def test_dependencies_error_names_the_extra() -> None:
    with pytest.raises(TypeError, match=r"Dependency #1 of extra 'my-extra'"):
        _dependencies("my-extra", [1])


###################################
#     Tests for strict extras     #
###################################


def test_update_non_string_dependency_raises() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest", 1, None, "black"]}}
    with pytest.raises(TypeError, match=r"Dependency #2 of extra 'dev' must be a string"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_blank_dependency_raises() -> None:
    metadata = {"optional-dependencies": {"dev": ["", "  ", "pytest"]}}
    with pytest.raises(ValueError, match=r"Dependency #1 of extra 'dev' must not be blank"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_invalid_dependency_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx", " "]}}
    with pytest.raises(ValueError, match=r"must not be blank"):
        AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata == {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx", " "]}}


def test_update_invalid_dependency_with_overwrite_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": [1]}}
    with pytest.raises(TypeError, match=r"must be a string"):
        AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert metadata == {"optional-dependencies": {"All": ["old"], "dev": [1]}}


def test_update_invalid_excluded_extra_is_not_inspected() -> None:
    metadata = {"optional-dependencies": {"dev": [1, " "], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["dev"]}).update(metadata)
    assert metadata == {
        "optional-dependencies": {"dev": [1, " "], "docs": ["sphinx"], "all": ["sphinx"]}
    }


def test_update_invalid_generated_extra_is_not_inspected() -> None:
    metadata = {"optional-dependencies": {"all": [1, " "], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert metadata == {"optional-dependencies": {"all": ["sphinx"], "docs": ["sphinx"]}}


def test_update_exclude_unmatched_raises() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"match no extra: \['missing'\]"):
        AutoExtrasMetadataHook("test", {"exclude": ["missing"]}).update(metadata)


def test_update_exclude_unmatched_are_listed_sorted() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"match no extra: \['a', 'z'\]"):
        AutoExtrasMetadataHook("test", {"exclude": ["z", "dev", "a"]}).update(metadata)


def test_update_exclude_unmatched_leaves_metadata_unchanged() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"match no extra"):
        AutoExtrasMetadataHook("test", {"exclude": ["tset"]}).update(metadata)
    assert metadata == {"optional-dependencies": {"dev": ["pytest"]}}


def test_update_exclude_without_optional_dependencies_raises() -> None:
    with pytest.raises(ValueError, match=r"match no extra: \['dev'\]"):
        AutoExtrasMetadataHook("test", {"exclude": ["dev"]}).update({})


def test_update_exclude_matches_extra_with_other_spelling() -> None:
    metadata = {"optional-dependencies": {"Dev_Extra": ["pytest"], "docs": ["sphinx"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["dev.extra"]}).update(metadata)
    assert metadata["optional-dependencies"]["all"] == ["sphinx"]


def test_update_exclude_unmatched_warn_only_warns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"exclude": ["missing"]})
    with pytest.warns(UserWarning, match=r"match no extra: \['missing'\]"):
        hook.update(metadata)


def test_update_exclude_unmatched_warn_only_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"]}}
    hook = AutoExtrasMetadataHook("test", {"exclude": ["docs", "missing"]})
    with pytest.warns(UserWarning, match=r"match no extra"):
        hook.update(metadata)
    assert metadata == {
        "optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"], "all": ["pytest"]}
    }


def test_update_warn_only_does_not_downgrade_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"all": ["old"]}}
    with pytest.raises(ValueError, match=r"already exists"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_warn_only_does_not_downgrade_invalid_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": "pytest"}}
    with pytest.raises(TypeError, match=r"must be a list of strings"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_warn_only_does_not_downgrade_invalid_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": [1]}}
    with pytest.raises(TypeError, match=r"must be a string"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


@pytest.mark.parametrize(
    "extras",
    [
        {"dev": ["pytest", "black"], "docs": ["sphinx"]},
        {"docs": ["sphinx"], "dev": ["black", "pytest"]},
    ],
)
def test_update_result_does_not_depend_on_the_order_of_the_extras(extras: dict) -> None:
    metadata = {"optional-dependencies": extras}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert metadata["optional-dependencies"]["all"] == ["black", "pytest", "sphinx"]


def test_update_whole_output_with_every_option() -> None:
    metadata = {
        "name": "pkg",
        "optional-dependencies": {
            "Full": ["old"],
            "dev": ["pytest", " black "],
            "test": ["pytest", "coverage"],
            "docs": ["sphinx"],
        },
    }
    hook = AutoExtrasMetadataHook(
        "test", {"extra-name": "full", "exclude": ["DOCS"], "overwrite": True}
    )
    hook.update(metadata)
    assert metadata == {
        "name": "pkg",
        "optional-dependencies": {
            "dev": ["pytest", " black "],
            "test": ["pytest", "coverage"],
            "docs": ["sphinx"],
            "full": ["black", "coverage", "pytest"],
        },
    }


def test_update_hook_can_be_reused() -> None:
    hook = AutoExtrasMetadataHook("test", {})
    metadata1 = {"optional-dependencies": {"dev": ["pytest"]}}
    metadata2 = {"optional-dependencies": {"docs": ["sphinx"]}}
    hook.update(metadata1)
    hook.update(metadata2)
    assert metadata2 == {"optional-dependencies": {"docs": ["sphinx"], "all": ["sphinx"]}}


def test_update_second_call_without_overwrite_raises() -> None:
    hook = AutoExtrasMetadataHook("test", {})
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    hook.update(metadata)
    with pytest.raises(ValueError, match=r"already exists"):
        hook.update(metadata)


def test_update_does_not_use_the_previous_content_of_the_generated_extra() -> None:
    metadata = {"optional-dependencies": {"all": ["old"], "dev": ["pytest"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert "old" not in metadata["optional-dependencies"]["all"]


def test_update_logs_debug_lists_the_extras(caplog: pytest.LogCaptureFixture) -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx"]}}
    with caplog.at_level(logging.DEBUG, logger="hatchling_autoextras_hook.hooks"):
        AutoExtrasMetadataHook("test", {"exclude": ["docs"]}).update(metadata)
    assert "Created 'all' with 1 dependencies from 1 extras: ['dev']" in caplog.text


def test_update_logs_overwrite_only_with_overwrite(caplog: pytest.LogCaptureFixture) -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with caplog.at_level(logging.DEBUG, logger="hatchling_autoextras_hook.hooks"):
        AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert "Overwriting" not in caplog.text


def test_update_conflict_message_lists_existing_extras() -> None:
    metadata = {"optional-dependencies": {"all": ["old"], "dev": ["pytest"]}}
    with pytest.raises(ValueError, match=r"Existing extras: \['all', 'dev'\]"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


def test_update_conflict_message_suggests_the_options() -> None:
    metadata = {"optional-dependencies": {"all": ["old"]}}
    with pytest.raises(ValueError, match=r"set 'overwrite = true'"):
        AutoExtrasMetadataHook("test", {}).update(metadata)


##############################################
#     Tests for the position of the extra    #
##############################################


def test_update_overwrite_other_spelling_appends_the_extra_last() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"], "z": ["zip"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert list(metadata["optional-dependencies"].items()) == [
        ("dev", ["pytest"]),
        ("z", ["zip"]),
        ("all", ["pytest", "zip"]),
    ]


def test_update_overwrite_same_spelling_appends_the_extra_last() -> None:
    metadata = {"optional-dependencies": {"all": ["old"], "dev": ["pytest"], "z": ["zip"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True}).update(metadata)
    assert list(metadata["optional-dependencies"].items()) == [
        ("dev", ["pytest"]),
        ("z", ["zip"]),
        ("all", ["pytest", "zip"]),
    ]


def test_update_overwrite_other_spelling_uses_the_configured_spelling() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"]}}
    AutoExtrasMetadataHook("test", {"overwrite": True, "extra-name": "all"}).update(metadata)
    assert list(metadata["optional-dependencies"]) == ["dev", "all"]


@pytest.mark.parametrize(
    ("extras", "expected"),
    [
        pytest.param(
            {"dev": ["pytest"], "docs": ["sphinx"]},
            [("dev", ["pytest"]), ("docs", ["sphinx"]), ("all", ["pytest", "sphinx"])],
            id="sorted",
        ),
        pytest.param(
            {"docs": ["sphinx"], "dev": ["pytest"]},
            [("docs", ["sphinx"]), ("dev", ["pytest"]), ("all", ["pytest", "sphinx"])],
            id="reversed",
        ),
        pytest.param(
            {"z": ["zip"], "a": ["abc"], "m": ["mod"]},
            [("z", ["zip"]), ("a", ["abc"]), ("m", ["mod"]), ("all", ["abc", "mod", "zip"])],
            id="unsorted",
        ),
    ],
)
def test_update_appends_the_extra_last_and_keeps_the_order_of_the_others(
    extras: dict[str, list[str]], expected: list[tuple[str, list[str]]]
) -> None:
    metadata = {"optional-dependencies": extras}
    AutoExtrasMetadataHook("test", {}).update(metadata)
    assert list(metadata["optional-dependencies"].items()) == expected


##############################################
#     Tests for the table in the messages    #
##############################################

TABLE = r"\[tool\.hatch\.metadata\.hooks\.autoextras\]"


@pytest.mark.parametrize(
    "config",
    [
        pytest.param({"excludes": ["dev"]}, id="unknown option"),
        pytest.param({"extra-name": 1}, id="extra-name type"),
        pytest.param({"extra-name": "a b"}, id="extra-name value"),
        pytest.param({"exclude": "dev"}, id="exclude type"),
        pytest.param({"exclude": ["all"]}, id="exclude generated extra"),
        pytest.param({"overwrite": "yes"}, id="overwrite type"),
    ],
)
def test_configuration_error_names_the_table(config: dict[str, object]) -> None:
    with pytest.raises((TypeError, ValueError), match=TABLE):
        AutoExtrasMetadataHook("test", config)


def test_unmatched_exclude_error_names_the_table() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    with pytest.raises(ValueError, match=TABLE):
        AutoExtrasMetadataHook("test", {"exclude": ["tset"]}).update(metadata)


def test_unknown_option_warning_names_the_table(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    with pytest.warns(UserWarning, match=TABLE):
        AutoExtrasMetadataHook("test", {"excludes": ["dev"]})


def test_unmatched_exclude_warning_names_the_table(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(WARN_ONLY_ENV, "1")
    metadata = {"optional-dependencies": {"dev": ["pytest"]}}
    hook = AutoExtrasMetadataHook("test", {"exclude": ["tset"]})
    with pytest.warns(UserWarning, match=TABLE):
        hook.update(metadata)


#############################################
#     Tests for the validated attributes    #
#############################################


def test_update_does_not_read_the_config_after_init() -> None:
    metadata = {"optional-dependencies": {"All": ["old"], "dev": ["pytest"], "docs": ["sphinx"]}}
    hook = AutoExtrasMetadataHook(
        "test", {"extra-name": "Full_Extra", "exclude": ["DEV"], "overwrite": True}
    )
    hook.config.clear()
    hook.update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "All": ["old"],
            "dev": ["pytest"],
            "docs": ["sphinx"],
            "Full_Extra": ["old", "sphinx"],
        }
    }


def test_update_self_reference_of_an_excluded_extra_is_copied() -> None:
    metadata = {"optional-dependencies": {"dev": ["pytest"], "docs": ["sphinx", "pkg[dev]"]}}
    AutoExtrasMetadataHook("test", {"exclude": ["dev"]}).update(metadata)
    assert metadata == {
        "optional-dependencies": {
            "dev": ["pytest"],
            "docs": ["sphinx", "pkg[dev]"],
            "all": ["pkg[dev]", "sphinx"],
        }
    }
