"""The `unless` scope field: producer-pinned string refs."""

import pytest
from pullapprove.config import ConfigModel, ConfigModels
from pydantic import ValidationError


def _config(scope_extra=None):
    scope = {"name": "api", "paths": ["api/**"], "reviewers": ["bob"], "require": 1}
    scope.update(scope_extra or {})
    return ConfigModel.from_data({"scopes": [scope]}, "CODEREVIEW.toml")


# --- ref format ---------------------------------------------------------------


def test_a_ref_is_producer_slash_name():
    config = _config({"unless": ["acme-review/no-functional-change"]})
    assert config.scopes[0].unless == ["acme-review/no-functional-change"]
    assert config.scopes[0].unless_refs() == [("acme-review", "no-functional-change")]


def test_refs_split_on_the_first_slash():
    """App slugs cannot contain a `/`, check names can -- everything after the
    first slash is the name."""
    config = _config({"unless": ["ci-app/build / test"]})
    assert config.scopes[0].unless_refs() == [("ci-app", "build / test")]


def test_the_producer_is_lowercased_the_name_is_not():
    config = _config({"unless": ["Acme-Review/No-Functional-Change"]})
    assert config.scopes[0].unless_refs() == [("acme-review", "No-Functional-Change")]


def test_a_bare_name_is_a_compile_error():
    """A check name without its producer is worthless -- any workflow with
    `checks: write` can post any name -- so it's rejected by syntax, not
    trusted by default."""
    with pytest.raises(ValidationError, match="must be 'producer/check-name'"):
        _config({"unless": ["no-functional-change"]})


def test_an_empty_producer_is_a_compile_error():
    with pytest.raises(ValidationError, match="must be 'producer/check-name'"):
        _config({"unless": ["/no-functional-change"]})


def test_an_empty_name_is_a_compile_error():
    with pytest.raises(ValidationError, match="must be 'producer/check-name'"):
        _config({"unless": ["acme-review/"]})


def test_referencing_pullapprove_itself_is_a_compile_error():
    """To most users PullApprove *is* "the check" on their PRs. It never
    creates these checks, it only reads them -- and waiting on our own status
    would deadlock politely."""
    with pytest.raises(ValidationError, match="PullApprove never creates checks"):
        _config({"unless": ["pullapprove/approved"]})


# --- bots never sit in rosters ------------------------------------------------


def test_a_bot_in_reviewers_is_a_compile_error():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "api",
                        "paths": ["api/**"],
                        "reviewers": ["bob", "review-bot[bot]"],
                    }
                ]
            }
        }
    )
    with pytest.raises(ValueError, match="is a bot and cannot be listed"):
        configs.compiled()


def test_a_bot_in_alternates_or_cc_is_a_compile_error():
    for field in ("alternates", "cc"):
        configs = ConfigModels.from_configs_data(
            {
                "CODEREVIEW.toml": {
                    "scopes": [
                        {
                            "name": "api",
                            "paths": ["api/**"],
                            "reviewers": ["bob"],
                            field: ["review-bot[bot]"],
                        }
                    ]
                }
            }
        )
        with pytest.raises(ValueError, match="is a bot and cannot be listed"):
            configs.compiled()


def test_a_bot_smuggled_through_an_alias_is_still_rejected():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "aliases": {"team": ["bob", "review-bot[bot]"]},
                "scopes": [
                    {"name": "api", "paths": ["api/**"], "reviewers": ["$team"]}
                ],
            }
        }
    )
    with pytest.raises(ValueError, match="is a bot and cannot be listed"):
        configs.compiled()


def test_a_bot_author_is_fine():
    """Agents as subjects: routing bot-authored PRs with `authors` never
    needed a declaration and still works."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "bot-prs",
                        "paths": ["**"],
                        "authors": ["dependabot[bot]"],
                        "reviewers": ["bob"],
                    }
                ]
            }
        }
    )
    compiled = configs.compiled()
    assert compiled["CODEREVIEW.toml"].scopes[0].authors == ["dependabot[bot]"]


# --- declared_check_names (the webhook/fetch index) ---------------------------


def test_declared_check_names_is_the_union_across_configs():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "api",
                        "paths": ["api/**"],
                        "unless": ["acme-review/no-functional-change"],
                    }
                ]
            },
            "docs/CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "docs",
                        "paths": ["**"],
                        "unless": [
                            "acme-review/no-functional-change",
                            "ci-app/docs-only",
                        ],
                    }
                ]
            },
        }
    )
    assert configs.declared_check_names() == {
        "no-functional-change",
        "docs-only",
    }


def test_declared_check_names_is_empty_without_unless():
    configs = ConfigModels.from_configs_data(
        {"CODEREVIEW.toml": {"scopes": [{"name": "all", "paths": ["**"]}]}}
    )
    assert configs.declared_check_names() == set()


def test_an_unconsumed_templates_checks_are_not_indexed():
    """A template nothing extends never participates in matching, so its
    `unless` refs must not make every pull request fetch (or error on) its
    checks. The consumed case is covered by test_unless_survives_extends."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.template.toml": {
                "template": True,
                "scopes": [
                    {
                        "name": "api",
                        "paths": ["api/**"],
                        "reviewers": ["bob"],
                        "require": 1,
                        "unless": ["acme-review/no-functional-change"],
                    }
                ],
            },
            "CODEREVIEW.toml": {"scopes": [{"name": "all", "paths": ["**"]}]},
        }
    )
    assert configs.declared_check_names() == set()


# --- extends ------------------------------------------------------------------


def test_unless_survives_extends():
    """A template's scope keeps its `unless` when consumed -- the ref is part
    of the scope, not a separate table to merge."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.template.toml": {
                "template": True,
                "scopes": [
                    {
                        "name": "api",
                        "paths": ["api/**"],
                        "reviewers": ["bob"],
                        "require": 1,
                        "unless": ["acme-review/no-functional-change"],
                    }
                ],
            },
            "CODEREVIEW.toml": {"extends": ["CODEREVIEW.template.toml"]},
        }
    )
    compiled = configs.compiled()
    scope = compiled["CODEREVIEW.toml"].scopes[0]
    assert scope.unless == ["acme-review/no-functional-change"]
    assert configs.declared_check_names() == {"no-functional-change"}
