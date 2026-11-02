"""Someone in both `reviewers` and `alternates`: the more specific mention
decides whether they're requested."""

from pathlib import Path

from pullapprove.config import ConfigModel, ConfigModels, ScopeModel

TEAMS = {
    "acme/backend": ["alice", "bob", "carol"],
    "acme/backend-owners": ["alice"],
    "acme/managers": ["bob"],
}


def compile_config(
    config_data: dict[str, object], *, teams: dict[str, list[str]] | None
) -> ConfigModel:
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    return config.compiled_config(Path("CODEREVIEW.toml"), configs, teams=teams)


def compile_scope(
    scope: dict[str, object],
    *,
    aliases: dict[str, list[str]] | None = None,
    teams: dict[str, list[str]] | None = TEAMS,
) -> ScopeModel:
    config_data = {
        "aliases": aliases or {},
        "scopes": [{"name": "all", "paths": ["*"], **scope}],
    }
    return compile_config(config_data, teams=teams).scopes[0]


def test_username_in_alternates_beats_team_in_reviewers() -> None:
    """A team member you list as an alternate by name is never requested,
    still counts, and still fills a `require` slot."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend"], "alternates": ["bob"], "require": 3}
    )

    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["bob"]
    assert scope.counts_toward("bob")


def test_alias_in_alternates_beats_team_in_reviewers() -> None:
    """A reusable never-request alias works against any team."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend"], "alternates": ["$never_request"]},
        aliases={"never_request": ["bob", "carol"]},
    )

    assert scope.reviewers == ["alice"]
    assert scope.alternates == ["bob", "carol"]


def test_username_in_reviewers_beats_alias_in_alternates() -> None:
    """The named owner is requested even though the backup pool includes them."""
    scope = compile_scope(
        {"reviewers": ["alice"], "alternates": ["$backend"]},
        aliases={"backend": ["alice", "bob", "carol"]},
    )

    assert scope.reviewers == ["alice"]
    assert scope.alternates == ["alice", "bob", "carol"]


def test_username_in_alternates_beats_alias_in_reviewers() -> None:
    scope = compile_scope(
        {"reviewers": ["$backend"], "alternates": ["bob"]},
        aliases={"backend": ["alice", "bob", "carol"]},
    )

    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["bob"]


def test_team_in_both_is_a_tie() -> None:
    """A team in alternates is a backup pool; the owners team is still asked."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend-owners"], "alternates": ["@acme/backend"]}
    )

    assert scope.reviewers == ["alice"]
    assert scope.alternates == ["alice", "bob", "carol"]


def test_alias_in_both_is_a_tie() -> None:
    scope = compile_scope(
        {"reviewers": ["$owners"], "alternates": ["$backend"]},
        aliases={"owners": ["alice"], "backend": ["alice", "bob", "carol"]},
    )

    assert scope.reviewers == ["alice"]
    assert scope.alternates == ["alice", "bob", "carol"]


def test_same_username_in_both_is_a_tie() -> None:
    scope = compile_scope({"reviewers": ["alice", "bob"], "alternates": ["bob"]})

    assert scope.reviewers == ["alice", "bob"]
    assert scope.alternates == ["bob"]


def test_team_inside_alias_is_still_a_team() -> None:
    """Wrapping a team in an alias doesn't make its members more specific."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend"], "alternates": ["$leads"]},
        aliases={"leads": ["@acme/managers"]},
    )
    assert scope.reviewers == ["alice", "bob", "carol"]
    assert scope.alternates == ["bob"]

    scope = compile_scope(
        {"reviewers": ["$everyone"], "alternates": ["bob"]},
        aliases={"everyone": ["@acme/backend"]},
    )
    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["bob"]


def test_most_specific_mention_in_a_list_wins() -> None:
    """Writing bob into reviewers by name keeps him requested even though a
    team puts him there too and an alias lists him as an alternate."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend", "bob"], "alternates": ["$never_request"]},
        aliases={"never_request": ["bob"]},
    )

    assert scope.reviewers == ["alice", "bob", "carol"]
    assert scope.alternates == ["bob"]


def test_negation_is_not_a_mention() -> None:
    scope = compile_scope(
        {"reviewers": ["@acme/backend", "!bob"], "alternates": ["bob"]}
    )

    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["bob"]


def test_negated_alternate_stays_a_reviewer() -> None:
    """Subtracting bob from the alternates pool takes him out of that list
    only; the alias still outranks the team for everyone left in it."""
    scope = compile_scope(
        {"reviewers": ["@acme/backend"], "alternates": ["$pool", "!bob"]},
        aliases={"pool": ["alice", "bob", "carol"]},
    )

    assert scope.reviewers == ["bob"]
    assert scope.alternates == ["alice", "carol"]
    assert scope.counts_toward("bob")


def test_case_insensitive() -> None:
    scope = compile_scope({"reviewers": ["@acme/backend"], "alternates": ["Bob"]})

    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["Bob"]


def test_wildcard_reviewers_are_untouched() -> None:
    scope = compile_scope({"reviewers": ["*", "alice"], "alternates": ["bob"]})

    assert scope.reviewers == ["*", "alice"]
    assert scope.alternates == ["bob"]


def test_offline_compile_leaves_unexpanded_team_refs_alone() -> None:
    scope = compile_scope(
        {"reviewers": ["@acme/backend"], "alternates": ["bob"]}, teams=None
    )

    assert scope.reviewers == ["@acme/backend"]
    assert scope.alternates == ["bob"]


def test_offline_compile_resolves_aliases_without_teams() -> None:
    scope = compile_scope(
        {"reviewers": ["$backend"], "alternates": ["bob"]},
        aliases={"backend": ["alice", "bob", "carol"]},
        teams=None,
    )

    assert scope.reviewers == ["alice", "carol"]
    assert scope.alternates == ["bob"]


def test_large_scale_change_follows_the_same_rule() -> None:
    compiled = compile_config(
        {
            "large_scale_change": {
                "reviewers": ["@acme/backend"],
                "alternates": ["bob"],
            },
            "scopes": [{"name": "all", "paths": ["*"], "reviewers": ["alice"]}],
        },
        teams=TEAMS,
    )

    assert compiled.large_scale_change is not None
    assert compiled.large_scale_change.reviewers == ["alice", "carol"]
    assert compiled.large_scale_change.alternates == ["bob"]
