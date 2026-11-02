from pathlib import Path

import pytest
from pullapprove.config import ConfigModel, ConfigModels


def test_team_expansion_in_each_user_field():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "authors": ["@acme/ios-devs"],
                "reviewers": ["@acme/ios-devs"],
                "alternates": ["@acme/ios-devs"],
                "cc": ["@acme/ios-devs"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.authors == ["alice", "bob"]
    assert scope.reviewers == ["alice", "bob"]
    assert scope.alternates == ["alice", "bob"]
    assert scope.cc == ["alice", "bob"]


def test_team_expansion_in_large_scale_change_reviewers_and_alternates():
    config_data = {
        "large_scale_change": {
            "reviewers": ["@acme/ios-devs"],
            "alternates": ["@acme/migrators", "!bob"],
        },
        "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["alice"]}],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"], "acme/migrators": ["bob", "carol"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    assert compiled.large_scale_change is not None
    assert compiled.large_scale_change.reviewers == ["alice", "bob"]
    assert compiled.large_scale_change.alternates == ["carol"]


def test_team_ref_stays_literal_in_paths_code_labels():
    """A leading `@` in paths/code/labels is a literal string (e.g. npm-style
    scoped package paths), never a team reference — even when a teams mapping
    is provided."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["@acme/ios-devs/**"],
                "code": [],
                "labels": ["@acme/ios-devs"],
                "reviewers": ["alice"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.paths == ["@acme/ios-devs/**"]
    assert scope.labels == ["@acme/ios-devs"]


def test_negated_team_ref_expansion():
    config_data = {
        "scopes": [
            {
                "name": "external",
                "paths": ["**"],
                "authors": ["!@acme/ios-devs"],
                "reviewers": ["alice"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.authors == ["!alice", "!bob"]
    assert scope.matches_author("carol") is True
    assert scope.matches_author("alice") is False


def test_matches_author_refuses_a_team_it_cant_see_into():
    """Offline (teams=None) a team ref stays as written, and comparing a
    username to it would quietly exclude or include the wrong people."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "external",
                        "paths": ["**"],
                        "authors": ["!@acme/ios-devs"],
                    }
                ]
            }
        }
    )

    with pytest.raises(ValueError, match="@acme/ios-devs"):
        configs.compiled().filter_for_pullrequest(author_username="alice")


def test_alias_containing_team_ref_expands_in_user_field():
    config_data = {
        "aliases": {
            "release": ["@acme/ios-devs", "sarah"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$release"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.reviewers == ["alice", "bob", "sarah"]


def test_alias_containing_team_ref_passes_through_literally_in_paths():
    """An alias used in a non-user field (paths) does not expand team refs
    within it — the `@...` string it carries just passes through."""
    config_data = {
        "aliases": {
            "weird": ["@acme/ios-devs"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["$weird"],
                "reviewers": ["alice"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.paths == ["@acme/ios-devs"]


def test_mixed_list_username_alias_team_wildcard():
    config_data = {
        "aliases": {
            "qa": ["carol"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["dave", "$qa", "@acme/ios-devs", "*"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    teams = {"acme/ios-devs": ["alice", "bob"]}
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)

    scope = compiled.scopes[0]
    assert scope.reviewers == ["dave", "carol", "alice", "bob", "*"]


def test_teams_none_passes_through_unexpanded():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios-devs", "alice"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    # No teams= at all -> default None -> no error, refs left unresolved.
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    assert scope.reviewers == ["@acme/ios-devs", "alice"]


def test_empty_teams_dict_raises_for_unknown_ref():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios-devs"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(ValueError, match=r"Unknown team: @acme/ios-devs"):
        config.compiled_config(Path("CODEREVIEW.toml"), configs, teams={})


def test_empty_team_expands_to_nothing():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios-devs", "alice"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(
        Path("CODEREVIEW.toml"), configs, teams={"acme/ios-devs": []}
    )

    assert compiled.scopes[0].reviewers == ["alice"]


def test_case_insensitive_team_lookup():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@Acme/IOS-Devs"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(
        Path("CODEREVIEW.toml"),
        configs,
        teams={"acme/ios-devs": ["alice", "bob"]},
    )

    assert compiled.scopes[0].reviewers == ["alice", "bob"]


def test_teams_dict_keys_normalized_regardless_of_caller_casing():
    """The `teams` mapping itself may use any casing for its keys — not just
    the ref's own casing — and still resolve."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["@acme/ios-devs"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(
        Path("CODEREVIEW.toml"),
        configs,
        teams={"Acme/iOS-Devs": ["alice", "bob"]},
    )

    assert compiled.scopes[0].reviewers == ["alice", "bob"]


def test_dedup_across_team_and_explicit_username():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["alice", "@acme/ios-devs", "bob"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(
        Path("CODEREVIEW.toml"),
        configs,
        teams={"acme/ios-devs": ["alice", "bob"]},
    )

    assert compiled.scopes[0].reviewers == ["alice", "bob"]


def test_team_ref_through_extends_chain():
    """A team ref defined in a template's scope resolves using the teams
    mapping passed to the consuming config's compile — mirrors how alias
    resolution works through `extends`."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW-TEAMS.toml": {
                "template": True,
                "scopes": [
                    {
                        "name": "shared",
                        "paths": ["**/*"],
                        "reviewers": ["@acme/ios-devs"],
                    }
                ],
            },
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-TEAMS.toml"],
                "scopes": [],
            },
        }
    )

    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"),
        configs,
        teams={"acme/ios-devs": ["alice", "bob"]},
    )
    assert compiled.scopes[0].reviewers == ["alice", "bob"]


@pytest.mark.parametrize("bad_ref", ["@justorg", "@/x", "!@justorg"])
def test_malformed_team_ref_raises_validation_error(bad_ref):
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": [bad_ref],
            }
        ],
    }
    with pytest.raises(ValueError, match="team references need the 'org/team' form"):
        ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))


def test_malformed_team_ref_in_large_scale_change_raises():
    config_data = {
        "large_scale_change": {"reviewers": ["@justorg"]},
        "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["alice"]}],
    }
    with pytest.raises(ValueError, match="team references need the 'org/team' form"):
        ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))


def test_email_address_in_reviewers_raises_with_email_message():
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["alice@company.com"],
            }
        ],
    }
    with pytest.raises(ValueError, match="email addresses are not supported here"):
        ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))


def test_bot_username_with_brackets_still_allowed_in_cc():
    """`dependabot[bot]`-style usernames have no "@" in them, so the closed
    grammar check doesn't touch them."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["alice"],
                "cc": ["dependabot[bot]"],
            }
        ],
    }
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    assert config.scopes[0].cc == ["dependabot[bot]"]


def test_negated_team_ref_skips_require_validation_before_compile():
    """A negated, unexpanded team ref (`!@org/team`) must skip the
    require-vs-reviewer-count check just like a positive team ref does — it
    can't be counted until it's resolved at compile time."""
    config_data = {
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["!@acme/blocked"],
                "require": 2,
            }
        ],
    }
    # Must not raise - the ref hasn't been expanded yet.
    ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))


def test_configs_compiled_threads_teams_through():
    """`ConfigModels.compiled(teams=...)` reaches each config's expansion."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {"name": "all", "paths": ["*"], "reviewers": ["@acme/ios-devs"]}
                ]
            }
        }
    )
    compiled = configs.compiled(teams={"acme/ios-devs": ["alice", "bob"]})
    assert compiled["CODEREVIEW.toml"].scopes[0].reviewers == ["alice", "bob"]


def test_cli_match_and_coverage_work_with_unexpanded_team_refs(tmp_path, monkeypatch):
    """`match` and `coverage` compile without a teams mapping and never read
    user-list fields, so a config containing team refs should work exactly as
    it does with a config containing aliases."""
    from click.testing import CliRunner
    from pullapprove.cli import cli

    monkeypatch.chdir(tmp_path)

    (tmp_path / "CODEREVIEW.toml").write_text(
        '[[scopes]]\nname = "all"\npaths = ["**/*"]\nreviewers = ["@acme/ios-devs"]\n'
    )
    (tmp_path / "file.py").write_text("print('hi')\n")

    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=t@example.com",
            "-c",
            "user.name=t",
            "commit",
            "-m",
            "x",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    runner = CliRunner()

    match_result = runner.invoke(cli, ["match"])
    assert match_result.exit_code == 0, match_result.output

    coverage_result = runner.invoke(cli, ["coverage"])
    assert coverage_result.exit_code == 0, coverage_result.output


def test_team_refs_collects_direct_refs():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["*"],
                        "reviewers": ["@acme/ios-devs"],
                        "cc": ["@acme/android-devs"],
                    }
                ],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs", "acme/android-devs"}


def test_team_refs_collects_ref_via_alias():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"release": ["@acme/ios-devs", "sarah"]},
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["$release"]}],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_includes_negated_ref():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["*"],
                        "authors": ["!@acme/ios-devs"],
                        "reviewers": ["alice"],
                    }
                ],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_dedups_case_insensitively_and_includes_large_scale_change():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "large_scale_change": {"reviewers": ["@Acme/IOS-Devs"]},
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["*"],
                        "reviewers": ["@acme/ios-devs"],
                    }
                ],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_includes_large_scale_change_alternates():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "large_scale_change": {
                    "reviewers": ["alice"],
                    "alternates": ["@acme/migrators"],
                },
            }
        }
    )
    assert configs.team_refs() == {"acme/migrators"}


def test_team_refs_empty_when_none_referenced():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {"name": "all", "paths": ["*"], "reviewers": ["alice", "$qa"]}
                ],
                "aliases": {"qa": ["bob"]},
            }
        }
    )
    assert configs.team_refs() == set()


def test_team_refs_ignores_alias_only_used_in_paths():
    """An alias holding an npm-style scoped path pattern is only referenced
    from `paths` (never team-expanded there), so its `@org/team`-shaped
    value must not be collected — compiling this config never expands it."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"scoped": ["@vendor/pkg/**"]},
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["$scoped"],
                        "reviewers": ["alice"],
                    }
                ],
            }
        }
    )
    assert configs.team_refs() == set()


def test_team_refs_ignores_alias_no_field_references():
    """An alias defined but never referenced by any field (user-list or
    otherwise) must not contribute its team ref — nothing would expand it."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"unused": ["@otherorg/team"]},
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["alice"]}],
            }
        }
    )
    assert configs.team_refs() == set()


def test_team_refs_collects_refs_in_every_user_field():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["*"],
                        "authors": ["@acme/authors"],
                        "reviewers": ["@acme/reviewers"],
                        "alternates": ["@acme/alternates"],
                        "cc": ["@acme/cc"],
                    }
                ],
            }
        }
    )
    assert configs.team_refs() == {
        "acme/authors",
        "acme/reviewers",
        "acme/alternates",
        "acme/cc",
    }


def test_team_refs_collects_ref_via_nested_alias():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {
                    "outer": ["$inner"],
                    "inner": ["@acme/ios-devs"],
                },
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["$outer"]}],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_collects_ref_via_negated_alias():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"release": ["@acme/ios-devs"]},
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["!$release"]}],
            }
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_collects_ref_from_alias_defined_in_extended_template():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW-TEAMS.toml": {
                "template": True,
                "aliases": {"release": ["@acme/ios-devs"]},
                "scopes": [],
            },
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-TEAMS.toml"],
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["$release"]}],
            },
        }
    )
    assert configs.team_refs() == {"acme/ios-devs"}


def test_team_refs_alias_cycle_does_not_hang():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {
                    "a": ["$b"],
                    "b": ["$a"],
                },
                "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["$a"]}],
            }
        }
    )
    assert configs.team_refs() == set()


def test_team_refs_same_alias_name_different_teams_per_config():
    """Two configs defining the same alias name with different teams must
    both be collected — resolution is scoped per config, like compilation,
    so a shadowed definition can't be dropped."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"devs": ["@acme/team-a"]},
                "scopes": [{"name": "a", "paths": ["a/*"], "reviewers": ["$devs"]}],
            },
            "sub/CODEREVIEW.toml": {
                "aliases": {"devs": ["@acme/team-b"]},
                "scopes": [{"name": "b", "paths": ["b/*"], "reviewers": ["$devs"]}],
            },
        }
    )
    assert configs.team_refs() == {"acme/team-a", "acme/team-b"}


def test_team_refs_same_alias_name_path_use_in_other_config_not_collected():
    """A same-name alias holding a path pattern in another config must not
    leak into collection — each config's alias map is walked separately."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"devs": ["@acme/ios"]},
                "scopes": [{"name": "a", "paths": ["a/*"], "reviewers": ["$devs"]}],
            },
            "sub/CODEREVIEW.toml": {
                "aliases": {"devs": ["@vendor/pkg/**"]},
                "scopes": [{"name": "b", "paths": ["$devs"], "reviewers": ["alice"]}],
            },
        }
    )
    assert configs.team_refs() == {"acme/ios"}


def test_cli_check_catches_compile_errors(tmp_path, monkeypatch):
    """`check` compiles the set offline, so config errors that would
    otherwise only surface in production (unknown aliases, wildcard +
    negated team ref) fail the command."""
    from click.testing import CliRunner
    from pullapprove.cli import cli

    monkeypatch.chdir(tmp_path)
    (tmp_path / "CODEREVIEW.toml").write_text(
        '[[scopes]]\nname = "all"\npaths = ["**/*"]\nreviewers = ["*", "!@acme/ios"]\n'
    )

    result = CliRunner().invoke(cli, ["check"])
    assert result.exit_code != 0
    assert "cannot be combined" in result.output


def test_cli_check_passes_unexpanded_team_refs(tmp_path, monkeypatch):
    """A valid config with team refs passes `check` -- offline compilation
    leaves the refs unexpanded rather than erroring on them."""
    from click.testing import CliRunner
    from pullapprove.cli import cli

    monkeypatch.chdir(tmp_path)
    (tmp_path / "CODEREVIEW.toml").write_text(
        '[[scopes]]\nname = "all"\npaths = ["**/*"]\nreviewers = ["@acme/ios"]\n'
    )

    result = CliRunner().invoke(cli, ["check"])
    assert result.exit_code == 0, result.output
