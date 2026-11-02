from pathlib import Path

import pytest
from pullapprove.config import ConfigModel, ConfigModels


def test_team_minus_person_in_reviewers():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios", "!bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].reviewers == ["alice", "carol"]


def test_team_minus_person_via_alias():
    config_data = {
        "aliases": {
            "ios_minus_bob": ["@acme/ios", "!bob"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$ios_minus_bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].reviewers == ["alice", "carol"]


def test_case_insensitive_subtraction():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios", "!Bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].reviewers == ["alice", "carol"]


def test_subtraction_in_alternates():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["dave"],
                "alternates": ["@acme/ios", "!bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].alternates == ["alice", "carol"]


def test_subtraction_in_cc():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["dave"],
                "cc": ["@acme/ios", "!bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].cc == ["alice", "carol"]


def test_subtraction_in_large_scale_change_reviewers():
    config_data = {
        "large_scale_change": {
            "reviewers": ["@acme/ios", "!bob"],
        },
        "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["dave"]}],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.large_scale_change is not None
    assert compiled.large_scale_change.reviewers == ["alice", "carol"]


def test_authors_negation_not_subtracted():
    """authors is a match-time predicate — team expansion still happens, but
    "!bob" survives as its own entry instead of removing "bob" from the list."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "authors": ["@acme/ios", "!bob"],
                "reviewers": ["dave"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios": ["alice", "bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.scopes[0].authors == ["alice", "bob", "carol", "!bob"]


def test_wildcard_plus_negation_in_reviewers_raises():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["*", "!bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(ValueError, match='cannot be combined with "\\*"'):
        config.compiled_config(Path("CODEREVIEW.toml"), configs)


def test_roster_subtracted_to_empty_with_require_errors():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["bob", "!bob"],
                "require": 1,
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(ValueError, match="has require=1"):
        config.compiled_config(Path("CODEREVIEW.toml"), configs)


def test_offline_unexpanded_team_ref_negation_left_untouched():
    """With teams=None (offline/CLI compile), an unexpanded "!@org/team" ref
    means the field isn't fully resolved yet — subtraction is skipped and the
    ref passes through unchanged, same as team expansion itself does."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["alice", "!@acme/ios"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    assert compiled.scopes[0].reviewers == ["alice", "!@acme/ios"]


def test_plain_negation_without_teams_still_subtracts():
    """No team refs at all (teams=None too) — the list is already fully
    resolved, so subtraction still applies."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["alice", "bob", "!bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    assert compiled.scopes[0].reviewers == ["alice"]


def test_wildcard_plus_negated_team_ref_raises_offline_and_online():
    """The wildcard+negation error is a check on the written form, so an
    offline compile (teams=None) rejects it exactly like the server will --
    a `pullapprove check` that passes locally can't then error in
    production."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["*", "!@acme/ios"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(ValueError, match='cannot be combined with "\\*"'):
        config.compiled_config(Path("CODEREVIEW.toml"), configs)

    with pytest.raises(ValueError, match='cannot be combined with "\\*"'):
        config.compiled_config(
            Path("CODEREVIEW.toml"), configs, teams={"acme/ios": ["alice"]}
        )
