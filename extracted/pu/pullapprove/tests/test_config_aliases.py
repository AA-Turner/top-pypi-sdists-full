from pathlib import Path

import pytest
from pullapprove.config import ConfigModel, ConfigModels


@pytest.mark.parametrize(
    ("config_data", "expected"),
    [
        (
            {
                "aliases": {
                    "team": ["alice", "bob"],
                    "qa": ["carol"],
                    "extras": ["bob", "dave"],
                },
                "scopes": [
                    {
                        "name": "all",
                        "paths": ["*"],
                        "authors": ["$team", "carol", "$extras", "frank"],
                        "reviewers": ["$qa", "$team", "carol"],
                        "alternates": ["$extras", "grace", "$qa"],
                        "cc": ["$team", "$team", "eve"],
                        "labels": ["$qa", "bug", "bug"],
                    }
                ],
                "large_scale_change": {
                    "reviewers": ["$team", "hank", "$extras"],
                    "labels": ["$qa", "$qa", "feature"],
                },
            },
            {
                "authors": ["alice", "bob", "carol", "dave", "frank"],
                "reviewers": ["carol", "alice", "bob"],
                "alternates": ["bob", "dave", "grace", "carol"],
                "cc": ["alice", "bob", "eve"],
                "labels": ["carol", "bug"],
                "lsc_reviewers": ["alice", "bob", "hank", "dave"],
                "lsc_labels": ["carol", "feature"],
            },
        )
    ],
)
def test_alias_expansion(config_data, expected):
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    assert scope.authors == expected["authors"]
    assert scope.reviewers == expected["reviewers"]
    assert scope.alternates == expected["alternates"]
    assert scope.cc == expected["cc"]
    assert scope.labels == expected["labels"]

    lsc = compiled.large_scale_change
    assert lsc is not None
    assert lsc.reviewers == expected["lsc_reviewers"]
    assert lsc.labels == expected["lsc_labels"]


def test_nested_aliases():
    """Test that aliases can reference other aliases."""
    config_data = {
        "aliases": {
            "backend": ["alice", "bob"],
            "frontend": ["carol", "dave"],
            "qa": ["eve"],
            "all_devs": ["$backend", "$frontend"],
            "everyone": ["$all_devs", "$qa", "frank"],
            "leads": ["alice", "carol"],
            "all_leads": ["$leads", "george"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$everyone"],
                "alternates": ["$all_leads"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    # everyone = all_devs + qa + frank = backend + frontend + qa + frank
    assert scope.reviewers == ["alice", "bob", "carol", "dave", "eve", "frank"]
    # all_leads = leads + george
    assert scope.alternates == ["alice", "carol", "george"]


def test_circular_alias_detection():
    """Test that circular references in aliases raise an error."""
    config_data = {
        "aliases": {
            "a": ["$b", "alice"],
            "b": ["$c", "bob"],
            "c": ["$a", "carol"],  # Creates a cycle: a -> b -> c -> a
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$a"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(
        ValueError, match="Circular reference detected in aliases: a -> b -> c -> a"
    ):
        config.compiled_config(Path("CODEREVIEW.toml"), configs)


def test_self_referencing_alias():
    """Test that self-referencing aliases are detected."""
    config_data = {
        "aliases": {
            "self": ["$self", "alice"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$self"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

    with pytest.raises(
        ValueError, match="Circular reference detected in aliases: self -> self"
    ):
        config.compiled_config(Path("CODEREVIEW.toml"), configs)


def test_deeply_nested_aliases():
    """Test multiple levels of alias nesting."""
    config_data = {
        "aliases": {
            "level1": ["alice"],
            "level2": ["$level1", "bob"],
            "level3": ["$level2", "carol"],
            "level4": ["$level3", "dave"],
            "level5": ["$level4", "eve"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$level5"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    assert scope.reviewers == ["alice", "bob", "carol", "dave", "eve"]


def test_mixed_nested_aliases():
    """Test aliases with mix of direct users and other aliases."""
    config_data = {
        "aliases": {
            "core": ["alice", "bob"],
            "extended": ["$core", "carol", "dave"],
            "all": ["$extended", "eve", "$core"],  # Includes duplicates
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$all", "alice"],  # More duplicates
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    # Should deduplicate while preserving order
    assert scope.reviewers == ["alice", "bob", "carol", "dave", "eve"]


def test_negated_alias_expansion():
    """Test that negated aliases like '!$team' expand to ['!alice', '!bob']."""
    config_data = {
        "aliases": {
            "verify_team": ["kasperhj", "xephyz", "HaayanchandravatSr"],
        },
        "scopes": [
            {
                "name": "Not Verify Team",
                "paths": ["**"],
                "authors": ["!$verify_team"],
                "reviewers": ["$verify_team"],
            },
            {
                "name": "Verify Team",
                "paths": ["**"],
                "authors": ["$verify_team"],
                "reviewers": ["$verify_team"],
            },
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    # The negated alias should expand to individual negated entries
    scope_not_team = compiled.scopes[0]
    assert scope_not_team.authors == [
        "!kasperhj",
        "!xephyz",
        "!HaayanchandravatSr",
    ]

    # Non-negated alias should expand normally
    scope_team = compiled.scopes[1]
    assert scope_team.authors == ["kasperhj", "xephyz", "HaayanchandravatSr"]

    # matches_author should work correctly with expanded negated aliases
    assert scope_not_team.matches_author("someoneelse") is True
    assert scope_not_team.matches_author("kasperhj") is False
    assert scope_not_team.matches_author("xephyz") is False

    assert scope_team.matches_author("kasperhj") is True
    assert scope_team.matches_author("someoneelse") is False


def test_negated_nested_alias_expansion():
    """Test that negated aliases work with nested aliases."""
    config_data = {
        "aliases": {
            "core": ["alice", "bob"],
            "all_devs": ["$core", "carol"],
        },
        "scopes": [
            {
                "name": "external",
                "paths": ["**"],
                "authors": ["!$all_devs"],
                "reviewers": ["$core"],
            }
        ],
    }

    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)

    scope = compiled.scopes[0]
    assert scope.authors == ["!alice", "!bob", "!carol"]
    assert scope.matches_author("external_user") is True
    assert scope.matches_author("alice") is False
    assert scope.matches_author("carol") is False


def test_circular_alias_across_extends():
    """Test that circular references across extended configs are detected."""
    # Base config with alias 'a' that references 'b'
    base_config_data = {
        "template": True,
        "aliases": {
            "a": ["$b", "alice"],
        },
    }

    # Extended config that defines 'b' referencing 'a' (creating a cycle)
    extended_config_data = {
        "extends": ["CODEREVIEW.base.toml"],
        "aliases": {
            "b": ["$a", "bob"],
        },
        "scopes": [
            {
                "name": "all",
                "paths": ["*"],
                "reviewers": ["$a"],
            }
        ],
    }

    base_config = ConfigModel.from_data(base_config_data, Path("CODEREVIEW.base.toml"))
    extended_config = ConfigModel.from_data(
        extended_config_data, Path("CODEREVIEW.toml")
    )

    configs = ConfigModels.from_config_models(
        {
            "CODEREVIEW.base.toml": base_config,
            "CODEREVIEW.toml": extended_config,
        }
    )

    with pytest.raises(
        ValueError, match="Circular reference detected in aliases: a -> b -> a"
    ):
        extended_config.compiled_config(Path("CODEREVIEW.toml"), configs)


def test_large_scale_change_reviewers_expand_through_processing_path():
    """The large-scale-change section must get aliases expanded (and extends
    merged) the same way scopes do.

    This mirrors a real config where ``$backend`` is defined in an extended
    template and used in the main config's ``[large-scale-change]`` reviewers.
    The processing path goes through ``filter_for_pullrequest`` (which returns
    the compiled set) and then ``get_default_large_scale_change``, so the alias
    must still resolve to usernames there.
    """
    teams_template_data = {
        "template": True,
        "aliases": {
            "backend": ["mozerov", "lundemann", "hua-dit-alkistis"],
        },
    }
    main_config_data = {
        "extends": ["CODEREVIEW-TEAMS.toml"],
        "large_scale_change": {
            "reviewers": ["$backend"],
            "labels": ["large-change"],
        },
        "scopes": [
            {"name": "all", "paths": ["*"], "reviewers": ["$backend"]},
        ],
    }

    configs = ConfigModels.from_config_models(
        {
            "CODEREVIEW-TEAMS.toml": ConfigModel.from_data(
                teams_template_data, Path("CODEREVIEW-TEAMS.toml")
            ),
            "CODEREVIEW.toml": ConfigModel.from_data(
                main_config_data, Path("CODEREVIEW.toml")
            ),
        }
    )

    filtered = configs.compiled().filter_for_pullrequest(author_username="someone")

    lsc = filtered.get_default_large_scale_change()
    assert lsc.reviewers == ["mozerov", "lundemann", "hua-dit-alkistis"]
    assert lsc.labels == ["large-change"]


def test_compiled_does_not_compile_templates_standalone():
    """A template scope may reference an alias the *consumer* defines. compiled()
    must resolve each non-template config in its own chain (where the alias
    resolves) and never compile a template standalone (where it would raise
    ``Unknown alias``)."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-TEAMS.toml"],
                "aliases": {"team": ["alice", "bob"]},
                "scopes": [],
            },
            "CODEREVIEW-TEAMS.toml": {
                "template": True,
                "scopes": [
                    {"name": "shared", "paths": ["**/*"], "reviewers": ["$team"]}
                ],
            },
        }
    )

    # Must not raise (the template is never compiled on its own).
    consumer = configs.compiled()["CODEREVIEW.toml"]
    assert [s.name for s in consumer.scopes] == ["shared"]
    assert consumer.scopes[0].reviewers == ["alice", "bob"]


def test_circular_extends_detected():
    """A -> B -> A must raise a clear error, not blow the stack."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {"extends": ["CODEREVIEW-OTHER.toml"], "scopes": []},
            "CODEREVIEW-OTHER.toml": {"extends": ["CODEREVIEW.toml"], "scopes": []},
        }
    )

    with pytest.raises(
        ValueError,
        match="Circular reference detected in extends: "
        "CODEREVIEW.toml -> CODEREVIEW-OTHER.toml -> CODEREVIEW.toml",
    ):
        configs["CODEREVIEW.toml"].compiled_config(Path("CODEREVIEW.toml"), configs)


def test_self_extends_detected():
    """A config that extends itself is a cycle too."""
    configs = ConfigModels.from_configs_data(
        {"CODEREVIEW.toml": {"extends": ["CODEREVIEW.toml"], "scopes": []}}
    )

    with pytest.raises(ValueError, match="Circular reference detected in extends"):
        configs["CODEREVIEW.toml"].compiled_config(Path("CODEREVIEW.toml"), configs)


# --- M1: flatten-then-expand-once (transitive inheritance + alias scoping) ---
# (diamond-is-not-a-cycle is covered by test_diamond_shared_ancestor_merged_once,
# which exercises the same 3-level diamond and also asserts the merged result.)


def test_transitive_extends_inherits_grandparent():
    """A extends B extends C — A must inherit C's scopes, aliases, and LSC."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-B.toml"],
                "scopes": [{"name": "a", "paths": ["a/**"], "reviewers": ["ann"]}],
            },
            "CODEREVIEW-B.toml": {
                "template": True,
                "extends": ["CODEREVIEW-C.toml"],
                "scopes": [{"name": "b", "paths": ["b/**"], "reviewers": ["bob"]}],
            },
            "CODEREVIEW-C.toml": {
                "template": True,
                "aliases": {"grand": ["carol"]},
                "scopes": [{"name": "c", "paths": ["c/**"], "reviewers": ["$grand"]}],
                "large_scale_change": {"reviewers": ["$grand"]},
            },
        }
    )

    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )

    scope_names = [s.name for s in compiled.scopes]
    assert scope_names == ["c", "b", "a"]  # grandparent..parent..child order
    # grandparent alias resolves in the grandparent scope it came from
    assert compiled.scopes[0].reviewers == ["carol"]
    assert compiled.large_scale_change is not None
    assert compiled.large_scale_change.reviewers == ["carol"]


def test_alias_defined_in_child_resolves_in_parent_scope():
    """A template scope can reference an alias the consuming config provides —
    expansion happens after the whole chain is merged."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-TEAMS.toml"],
                "aliases": {"team": ["alice", "bob"]},
                "scopes": [],
            },
            "CODEREVIEW-TEAMS.toml": {
                "template": True,
                "scopes": [
                    {"name": "shared", "paths": ["**/*"], "reviewers": ["$team"]}
                ],
            },
        }
    )

    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["alice", "bob"]


def test_diamond_shared_ancestor_merged_once():
    """A extends [B, C], both extend D (which has a scope). D's scope must
    appear exactly once — no duplicate-name error from double inclusion."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-B.toml", "CODEREVIEW-C.toml"],
                "scopes": [],
            },
            "CODEREVIEW-B.toml": {"template": True, "extends": ["CODEREVIEW-D.toml"]},
            "CODEREVIEW-C.toml": {"template": True, "extends": ["CODEREVIEW-D.toml"]},
            "CODEREVIEW-D.toml": {
                "template": True,
                "scopes": [{"name": "d", "paths": ["**/*"], "reviewers": ["dee"]}],
            },
        }
    )

    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )
    assert [s.name for s in compiled.scopes] == ["d"]


# --- M2: extends path resolution (relative, /, bare) ---


def test_extends_relative_parent_path():
    """`../CODEREVIEW.toml` from a subdir resolves to the parent directory."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {"aliases": {"root": ["alice"]}, "scopes": []},
            "app/CODEREVIEW.toml": {
                "extends": ["../CODEREVIEW.toml"],
                "scopes": [{"name": "s", "paths": ["**/*"], "reviewers": ["$root"]}],
            },
        }
    )
    compiled = configs["app/CODEREVIEW.toml"].compiled_config(
        Path("app/CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["alice"]


def test_extends_repo_absolute_path():
    """`/CODEREVIEW.toml` resolves to the repo root from any depth."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {"aliases": {"root": ["alice"]}, "scopes": []},
            "a/b/CODEREVIEW.toml": {
                "extends": ["/CODEREVIEW.toml"],
                "scopes": [{"name": "s", "paths": ["**/*"], "reviewers": ["$root"]}],
            },
        }
    )
    compiled = configs["a/b/CODEREVIEW.toml"].compiled_config(
        Path("a/b/CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["alice"]


def test_extends_bare_name_relative_to_dir():
    """A bare filename resolves relative to the extending file's directory."""
    configs = ConfigModels.from_configs_data(
        {
            "sub/CODEREVIEW.base.toml": {"template": True, "aliases": {"t": ["bob"]}},
            "sub/CODEREVIEW.toml": {
                "extends": ["CODEREVIEW.base.toml"],
                "scopes": [{"name": "s", "paths": ["**/*"], "reviewers": ["$t"]}],
            },
        }
    )
    compiled = configs["sub/CODEREVIEW.toml"].compiled_config(
        Path("sub/CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["bob"]


def test_extends_escape_above_root_errors():
    configs = ConfigModels.from_configs_data(
        {"app/CODEREVIEW.toml": {"extends": ["../../CODEREVIEW.toml"], "scopes": []}}
    )
    with pytest.raises(ValueError, match="above the repo root"):
        configs["app/CODEREVIEW.toml"].compiled_config(
            Path("app/CODEREVIEW.toml"), configs
        )


def test_extends_missing_target_names_resolved_path():
    configs = ConfigModels.from_configs_data(
        {"app/CODEREVIEW.toml": {"extends": ["../CODEREVIEW.toml"], "scopes": []}}
    )
    with pytest.raises(ValueError, match="resolved to 'CODEREVIEW.toml'"):
        configs["app/CODEREVIEW.toml"].compiled_config(
            Path("app/CODEREVIEW.toml"), configs
        )


# --- M3: undefined alias -> error ---


def test_undefined_alias_errors():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {"name": "s", "paths": ["*"], "reviewers": ["$typo", "real"]}
                ]
            }
        }
    )
    with pytest.raises(ValueError, match=r"Unknown alias: \$typo"):
        configs["CODEREVIEW.toml"].compiled_config(Path("CODEREVIEW.toml"), configs)


def test_undefined_negated_alias_errors():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [{"name": "s", "paths": ["*"], "authors": ["!$typo"]}]
            }
        }
    )
    with pytest.raises(ValueError, match=r"Unknown alias: !\$typo"):
        configs["CODEREVIEW.toml"].compiled_config(Path("CODEREVIEW.toml"), configs)


def test_alias_defined_in_chain_does_not_error():
    """An alias defined anywhere in the extends chain resolves — no false error."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-BASE.toml"],
                "scopes": [{"name": "s", "paths": ["*"], "reviewers": ["$shared"]}],
            },
            "CODEREVIEW-BASE.toml": {
                "template": True,
                "aliases": {"shared": ["alice"]},
            },
        }
    )
    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["alice"]


# --- M4: duplicate scope name across extends -> error ---


def test_duplicate_scope_name_across_extends_errors():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["CODEREVIEW-BASE.toml"],
                "scopes": [{"name": "dup", "paths": ["a/**"], "reviewers": ["alice"]}],
            },
            "CODEREVIEW-BASE.toml": {
                "template": True,
                "scopes": [{"name": "dup", "paths": ["b/**"], "reviewers": ["bob"]}],
            },
        }
    )
    with pytest.raises(ValueError, match="Duplicate scope name: dup"):
        configs["CODEREVIEW.toml"].compiled_config(Path("CODEREVIEW.toml"), configs)


# --- M5: config-relative scope paths (template path-relativity) ---


def test_root_config_paths_unchanged():
    """A root config (dir '') anchors at the repo root — paths are unchanged."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [{"name": "s", "paths": ["src/**/*"], "reviewers": ["a"]}]
            }
        }
    )
    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].paths == ["src/**/*"]


def test_subdir_config_paths_anchored_at_its_dir():
    """A subdir config's scope paths anchor at the config's own directory."""
    configs = ConfigModels.from_configs_data(
        {
            "app/CODEREVIEW.toml": {
                "scopes": [{"name": "s", "paths": ["src/**/*"], "reviewers": ["a"]}]
            }
        }
    )
    compiled = configs["app/CODEREVIEW.toml"].compiled_config(
        Path("app/CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].paths == ["app/src/**/*"]
    assert compiled.scopes[0].matches_path(Path("app/src/foo.py"))
    assert not compiled.scopes[0].matches_path(Path("src/foo.py"))


def test_template_scope_paths_anchored_at_consumer():
    """A template's scope paths anchor at the consuming config's directory —
    the same template yields different anchors for different consumers."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW-TEMPLATE.toml": {
                "template": True,
                "scopes": [{"name": "s", "paths": ["src/**/*"], "reviewers": ["a"]}],
            },
            "app/CODEREVIEW.toml": {
                "extends": ["/CODEREVIEW-TEMPLATE.toml"],
                "scopes": [],
            },
            "lib/CODEREVIEW.toml": {
                "extends": ["/CODEREVIEW-TEMPLATE.toml"],
                "scopes": [],
            },
        }
    )
    app_c = configs["app/CODEREVIEW.toml"].compiled_config(
        Path("app/CODEREVIEW.toml"), configs
    )
    lib_c = configs["lib/CODEREVIEW.toml"].compiled_config(
        Path("lib/CODEREVIEW.toml"), configs
    )
    assert app_c.scopes[0].paths == ["app/src/**/*"]
    assert lib_c.scopes[0].paths == ["lib/src/**/*"]


def test_nontemplate_parent_scopes_anchored_at_parent_dir():
    """A non-template parent's scopes stay anchored at the parent's directory,
    even when a deeper child extends it; the child's own scopes anchor at the
    child's directory."""
    configs = ConfigModels.from_configs_data(
        {
            "app/CODEREVIEW.toml": {
                "scopes": [{"name": "p", "paths": ["src/**"], "reviewers": ["a"]}]
            },
            "app/web/CODEREVIEW.toml": {
                "extends": ["../CODEREVIEW.toml"],
                "scopes": [{"name": "c", "paths": ["ui/**"], "reviewers": ["b"]}],
            },
        }
    )
    compiled = configs["app/web/CODEREVIEW.toml"].compiled_config(
        Path("app/web/CODEREVIEW.toml"), configs
    )
    by_name = {s.name: s for s in compiled.scopes}
    assert by_name["p"].paths == ["app/src/**"]
    assert by_name["c"].paths == ["app/web/ui/**"]


def test_anchor_path_absolute_and_negation():
    """A leading `/` is repo-root-absolute; a leading `!` negation is preserved."""
    configs = ConfigModels.from_configs_data(
        {
            "app/CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "s",
                        "paths": ["/shared/**", "!build/**", "src/**"],
                        "reviewers": ["a"],
                    }
                ]
            }
        }
    )
    compiled = configs["app/CODEREVIEW.toml"].compiled_config(
        Path("app/CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].paths == ["shared/**", "!app/build/**", "app/src/**"]


def test_multiple_parents_last_alias_wins():
    """With `extends: [A, B]`, a later parent's alias wins on key collision."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "extends": ["/CODEREVIEW-A.toml", "/CODEREVIEW-B.toml"],
                "scopes": [{"name": "s", "paths": ["*"], "reviewers": ["$team"]}],
            },
            "CODEREVIEW-A.toml": {"template": True, "aliases": {"team": ["alice"]}},
            "CODEREVIEW-B.toml": {"template": True, "aliases": {"team": ["bob"]}},
        }
    )
    compiled = configs["CODEREVIEW.toml"].compiled_config(
        Path("CODEREVIEW.toml"), configs
    )
    assert compiled.scopes[0].reviewers == ["bob"]


def test_standalone_template_with_scopes_compiles():
    """A template compiled on its own (via the direct ``compiled_config`` API)
    has untagged scopes — paths stay unanchored and the model builds cleanly
    (the transient anchor tag must not leak into the model)."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW-TEMPLATE.toml": {
                "template": True,
                "scopes": [{"name": "s", "paths": ["src/**"], "reviewers": ["a"]}],
            }
        }
    )
    compiled = configs["CODEREVIEW-TEMPLATE.toml"].compiled_config(
        Path("CODEREVIEW-TEMPLATE.toml"), configs
    )
    assert compiled.scopes[0].paths == ["src/**"]
