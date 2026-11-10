from pathlib import Path

import pytest
from pullapprove.config import (
    LARGE_SCALE_CHANGE_SCOPE_NAME,
    CompiledConfigModels,
    ConfigModel,
    ConfigModels,
    LargeScaleChangeModel,
    ScopeModel,
    scope_line_range,
)
from pullapprove.matches import match_diff
from pydantic import ValidationError


def test_empty_configs():
    configs = ConfigModels.from_configs_data({"CODEREVIEW.toml": {}})
    assert bool(configs)
    assert "CODEREVIEW.toml" in configs
    assert not configs["CODEREVIEW.toml"].template


def test_angular_diff(snapshot):
    cfg = ConfigModel.from_filesystem(Path(__file__).parent / "config.toml")
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": cfg})
    diff = (Path(__file__).parent / "test.diff").read_text()
    diff_results = match_diff(configs.compiled(), diff)
    assert not diff_results.config_paths_modified
    assert (
        diff_results.additions == 2975
    )  # Expected number of additions (matches diffstat)
    assert (
        diff_results.deletions == 8512
    )  # Expected number of deletions (matches diffstat)
    assert snapshot("angular.json") == diff_results.matches.model_dump()


def test_matched_scopes_come_back_in_declaration_order():
    """Scope order is a property of the config, not of the diff. Here the
    first changed file matches only `broad`, but `specific` is declared first
    and must come first. Consumers that walk scopes in sequence depend on
    this: review requesting counts what earlier scopes asked for."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {"name": "specific", "paths": ["z/**"], "reviewers": ["alice"]},
                    {
                        "name": "broad",
                        "paths": ["**"],
                        "reviewers": ["bob"],
                        "ownership": "append",
                    },
                ]
            }
        }
    )
    diff = (
        "diff --git a/a.py b/a.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+print('a')\n"
        "diff --git a/z/z.py b/z/z.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+print('z')\n"
    )

    diff_results = match_diff(configs.compiled(), diff)

    assert list(diff_results.matches.scopes) == ["specific", "broad"]


def test_a_duplicate_scope_name_in_another_config_does_not_reorder_the_root():
    """Declaration position belongs to the scope object, not to its name. A
    second config declaring the same name must not move the root config's
    scope."""
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {"name": "specific", "paths": ["z/**"], "reviewers": ["alice"]},
                    {
                        "name": "broad",
                        "paths": ["**"],
                        "reviewers": ["bob"],
                        "ownership": "append",
                    },
                ]
            },
            "nested/CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "unrelated",
                        "paths": ["**"],
                        "reviewers": ["cam"],
                        "ownership": "append",
                    },
                    {"name": "specific", "paths": ["**"], "reviewers": ["dee"]},
                ]
            },
        }
    )
    diff = (
        "diff --git a/a.py b/a.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+print('a')\n"
        "diff --git a/z/z.py b/z/z.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+print('z')\n"
    )

    diff_results = match_diff(configs.compiled(), diff)

    assert list(diff_results.matches.scopes) == ["specific", "broad"]


class TestReviewersForRequireValidation:
    """Test the validate_reviewers_for_require model validator."""

    def test_empty_reviewers_with_require_raises(self):
        """Empty reviewers with require > 0 should raise ValidationError."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": [],
                    "require": 1,
                }
            ]
        }
        with pytest.raises(
            ValidationError,
            match="has require=1 but only 0 reviewers/alternates specified",
        ):
            ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))

    def test_insufficient_reviewers_raises(self):
        """Fewer reviewers than require should raise ValidationError."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["alice"],
                    "require": 2,
                }
            ]
        }
        with pytest.raises(
            ValidationError,
            match="has require=2 but only 1 reviewers/alternates specified",
        ):
            ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))

    def test_alternates_count_toward_total(self):
        """Alternates should count toward the reviewer total."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["alice"],
                    "alternates": ["bob"],
                    "require": 2,
                }
            ]
        }
        # Should not raise - 1 reviewer + 1 alternate = 2, which meets require=2
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 2

    def test_wildcard_skips_validation(self):
        """Wildcard in reviewers should skip validation."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["*"],
                    "require": 5,
                }
            ]
        }
        # Should not raise - wildcard means anyone can review
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 5

    def test_wildcard_in_alternates_skips_validation(self):
        """Wildcard in alternates must not raise at raw parse — compiled
        configs stored inside old processing results re-parse through
        ScopeModel, so the rejection happens at compile time instead
        (see TestWildcardOnlyInReviewers)."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": [],
                    "alternates": ["*"],
                    "require": 5,
                }
            ]
        }
        # Should not raise - wildcard in alternates
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 5

    def test_alias_skips_validation(self):
        """Unexpanded aliases should skip validation (will validate after expansion)."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["$team"],
                    "require": 5,
                }
            ]
        }
        # Should not raise - alias not yet expanded
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 5

    def test_alias_in_alternates_skips_validation(self):
        """Unexpanded aliases in alternates should skip validation."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": [],
                    "alternates": ["$team"],
                    "require": 5,
                }
            ]
        }
        # Should not raise - alias not yet expanded
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 5

    def test_zero_require_passes(self):
        """require=0 with no reviewers should pass."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": [],
                    "require": 0,
                }
            ]
        }
        # Should not raise - require=0 means no approvals needed
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 0

    def test_valid_config_passes(self):
        """Valid config with enough reviewers should pass."""
        config_data = {
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["alice", "bob", "carol"],
                    "require": 2,
                }
            ]
        }
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        assert config.scopes[0].require == 2

    def test_validation_after_alias_expansion(self):
        """Validation should catch issues after aliases are expanded."""
        config_data = {
            "aliases": {
                "small_team": ["alice"],
            },
            "scopes": [
                {
                    "name": "test",
                    "paths": ["*"],
                    "reviewers": ["$small_team"],
                    "require": 3,
                }
            ],
        }
        # Initial parse should pass (alias not expanded)
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

        # After compilation (alias expansion), should raise
        with pytest.raises(
            ValidationError,
            match="has require=3 but only 1 reviewers/alternates specified",
        ):
            config.compiled_config(Path("CODEREVIEW.toml"), configs)


def _compile_root_config(config_data):
    """Compile a lone root CODEREVIEW.toml."""
    config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
    configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})
    return config.compiled_config(Path("CODEREVIEW.toml"), configs)


class TestNegativeValues:
    """Negative require/request/author_value are invalid. These are
    compile-time checks (like the wildcard checks) so that compiled configs
    stored inside old processing results keep parsing."""

    def _scope_config(self, **scope_fields):
        scope = {"name": "test", "paths": ["*"], **scope_fields}
        return {"scopes": [scope]}

    def test_negative_values_still_parse(self):
        """Raw parse must accept negative values — compiled configs with
        them were storable inside old processing results and must reload."""
        config = ConfigModel.from_data(
            self._scope_config(
                reviewers=["alice"], require=-1, request=-5, author_value=-1
            ),
            Path("CODEREVIEW.toml"),
        )
        assert config.scopes[0].require == -1

    def test_negative_require_raises_at_compile(self):
        with pytest.raises(ValueError, match="require cannot be negative"):
            _compile_root_config(self._scope_config(reviewers=["alice"], require=-1))

    def test_negative_request_raises_at_compile(self):
        with pytest.raises(ValueError, match="request cannot be negative"):
            _compile_root_config(self._scope_config(reviewers=["alice"], request=-2))

    def test_negative_author_value_raises_at_compile(self):
        with pytest.raises(ValueError, match="author_value cannot be negative"):
            _compile_root_config(
                self._scope_config(reviewers=["alice"], author_value=-1)
            )

    def test_lsc_negative_require_raises_at_compile(self):
        with pytest.raises(ValueError, match="require cannot be negative"):
            _compile_root_config(
                {"large_scale_change": {"reviewers": ["alice"], "require": -1}}
            )

    def test_lsc_negative_request_raises_at_compile(self):
        with pytest.raises(ValueError, match="request cannot be negative"):
            _compile_root_config(
                {"large_scale_change": {"reviewers": ["alice"], "request": -1}}
            )


class TestGlobalRequire:
    """A global scope with require = 0 is rejected at compile time."""

    def _scope_config(self, **scope_fields):
        scope = {"name": "leads", "paths": ["**/*"], "reviewers": ["lead"]}
        return {"scopes": [{**scope, **scope_fields}]}

    def test_global_require_zero_still_parses(self):
        config = ConfigModel.from_data(
            self._scope_config(ownership="global", require=0),
            Path("CODEREVIEW.toml"),
        )
        assert config.scopes[0].require == 0

    def test_global_require_zero_raises_at_compile(self):
        with pytest.raises(ValueError, match="global scopes need require >= 1"):
            _compile_root_config(self._scope_config(ownership="global", require=0))

    def test_global_with_require_omitted_raises_at_compile(self):
        """require defaults to 0, so leaving it out is the same mistake."""
        with pytest.raises(ValueError, match="global scopes need require >= 1"):
            _compile_root_config(self._scope_config(ownership="global"))

    def test_global_require_zero_in_a_template_raises(self):
        """The reported case: the global scope lives in an extended template."""
        configs = ConfigModels.from_configs_data(
            {
                "CODEREVIEW.toml": {"extends": ["/codereview/CODEREVIEW.base.toml"]},
                "codereview/CODEREVIEW.base.toml": {
                    "template": True,
                    **self._scope_config(ownership="global", require=0),
                },
            }
        )
        with pytest.raises(ValueError, match="Scope 'leads': global scopes"):
            configs.compiled()

    def test_global_require_one_compiles(self):
        """The intended "can approve anything, isn't auto-requested" shape."""
        compiled = _compile_root_config(
            self._scope_config(ownership="global", require=1)
        )
        assert compiled.scopes[0].require == 1
        assert compiled.scopes[0].request == 0

    @pytest.mark.parametrize("ownership", ["", "append"])
    def test_require_zero_is_still_fine_without_global(self, ownership):
        """Default and append scopes with require = 0 are how exemptions,
        labels, and FYI requests are written."""
        compiled = _compile_root_config(
            self._scope_config(ownership=ownership, require=0, request=1)
        )
        assert compiled.scopes[0].require == 0


class TestCountsToward:
    """counts_toward decides whose review the scope counts -- the one
    membership rule the engine and the request batcher both read."""

    def _scope(self, **fields):
        config = ConfigModel.from_data(
            {"scopes": [{"name": "test", "paths": ["*"], **fields}]},
            Path("CODEREVIEW.toml"),
        )
        return config.scopes[0]

    def test_reviewers_and_alternates_both_count(self):
        scope = self._scope(reviewers=["alice"], alternates=["bob"])
        assert scope.counts_toward("alice")
        assert scope.counts_toward("bob")
        assert not scope.counts_toward("carol")

    def test_matching_is_case_insensitive(self):
        scope = self._scope(reviewers=["Alice"], alternates=["BOB"])
        assert scope.counts_toward("aLiCe")
        assert scope.counts_toward("bob")

    def test_a_wildcard_in_reviewers_counts_everybody(self):
        scope = self._scope(reviewers=["*"])
        assert scope.counts_toward("anybody")

    def test_a_wildcard_alternate_does_not_count_everybody(self):
        """ "Anyone may approve" is a statement about `reviewers`, not about
        its backups, and the engine's point counting reads it that way."""
        scope = self._scope(reviewers=["alice"], alternates=["*"])
        assert scope.counts_toward("alice")
        assert not scope.counts_toward("carol")


class TestUnsolvableReason:
    """unsolvable_reason explains why a scope/LSC can never pass for a PR
    author; author_points feeds the max-possible math."""

    def _scope(self, **fields):
        config = ConfigModel.from_data(
            {"scopes": [{"name": "test", "paths": ["*"], **fields}]},
            Path("CODEREVIEW.toml"),
        )
        return config.scopes[0]

    def test_author_points_requires_listing(self):
        scope = self._scope(reviewers=["alice"], author_value=2)
        assert scope.author_points("Alice") == 2
        assert scope.author_points("someone") == 0

    def test_author_points_count_alternates(self):
        scope = self._scope(reviewers=["bob"], alternates=["alice"], author_value=1)
        assert scope.author_points("Alice") == 1

    def test_author_points_ignore_wildcard(self):
        scope = self._scope(reviewers=["*"], author_value=1)
        assert scope.author_points("alice") == 0

    def test_author_value_makes_alternate_author_solvable(self):
        scope = self._scope(
            reviewers=["bob"], alternates=["alice"], require=2, author_value=1
        )
        assert scope.unsolvable_reason("alice") is None

    def test_author_only_reviewer_is_unsolvable(self):
        scope = self._scope(reviewers=["alice"], require=1)
        assert scope.unsolvable_reason("alice") is not None
        assert scope.unsolvable_reason("someone") is None

    def test_author_value_makes_author_only_solvable(self):
        scope = self._scope(reviewers=["alice"], require=1, author_value=1)
        assert scope.unsolvable_reason("alice") is None

    def test_wildcard_is_always_solvable(self):
        scope = self._scope(reviewers=["*"], require=5)
        assert scope.unsolvable_reason("alice") is None


class TestWildcardOnlyInReviewers:
    """The "*" wildcard is only supported in `reviewers` — everywhere else it
    is matched as a literal username and silently does nothing (`alternates`:
    scope pends forever; `authors`: scope never applies; `cc`: nobody is
    notified). Compilation rejects it."""

    @pytest.mark.parametrize("field", ["authors", "alternates", "cc"])
    def test_wildcard_raises_at_compile(self, field):
        config_data = {
            "scopes": [
                {
                    "name": "all",
                    "paths": ["*"],
                    "reviewers": ["alice"],
                    field: ["*"],
                    "require": 1,
                }
            ],
        }
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

        with pytest.raises(
            ValueError,
            match=f"Scope 'all': \"\\*\" is not supported in {field}",
        ):
            config.compiled_config(Path("CODEREVIEW.toml"), configs)

    def test_wildcard_in_alternates_via_alias_raises_at_compile(self):
        config_data = {
            "aliases": {
                "anyone": ["*"],
            },
            "scopes": [
                {
                    "name": "all",
                    "paths": ["*"],
                    "alternates": ["$anyone"],
                    "require": 1,
                }
            ],
        }
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

        with pytest.raises(
            ValueError,
            match='"\\*" is not supported in alternates — add it to reviewers',
        ):
            config.compiled_config(Path("CODEREVIEW.toml"), configs)

    def test_wildcard_in_reviewers_with_other_fields_compiles(self):
        config_data = {
            "scopes": [
                {
                    "name": "all",
                    "paths": ["*"],
                    "reviewers": ["*"],
                    "alternates": ["bob"],
                    "authors": ["carol", "!dave"],
                    "cc": ["erin"],
                    "require": 1,
                }
            ],
        }
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

        compiled = config.compiled_config(Path("CODEREVIEW.toml"), configs)
        assert compiled.scopes[0].reviewers == ["*"]
        assert compiled.scopes[0].alternates == ["bob"]
        assert compiled.scopes[0].authors == ["carol", "!dave"]
        assert compiled.scopes[0].cc == ["erin"]


class TestLargeScaleChangeAsScope:
    """A large-scale change is reviewed as one scope covering every path."""

    def test_fields_carry_over(self):
        lsc = LargeScaleChangeModel(
            reviewers=["alice", "bob", "carol"],
            alternates=["dave"],
            require=2,
            request=1,
            labels=["big-change"],
        )

        scope = lsc.as_scope()

        assert scope.name == LARGE_SCALE_CHANGE_SCOPE_NAME
        assert scope.reviewers == ["alice", "bob", "carol"]
        assert scope.alternates == ["dave"]
        assert scope.require == 2
        assert scope.request == 1
        assert scope.labels == ["big-change"]
        assert scope.matches_path(Path("any/where/at/all.py"))

    def test_no_reviewers_is_a_config_error(self):
        with pytest.raises(ValueError, match="no reviewers defined"):
            LargeScaleChangeModel().as_scope()

    def test_alternates_alone_are_enough(self):
        """Same as a scope: alternates can approve, they just aren't asked."""
        scope = LargeScaleChangeModel(alternates=["alice"]).as_scope()
        assert scope.alternates == ["alice"]

    def test_require_beyond_the_roster_is_a_config_error(self):
        lsc = LargeScaleChangeModel(reviewers=["alice"], require=2)
        with pytest.raises(
            ValueError, match="require=2 but only 1 reviewers/alternates"
        ):
            lsc.as_scope()

    def test_wildcard_in_alternates_raises_at_compile(self):
        config_data = {
            "large_scale_change": {"reviewers": ["alice"], "alternates": ["*"]},
        }
        config = ConfigModel.from_data(config_data, Path("CODEREVIEW.toml"))
        configs = ConfigModels.from_config_models({"CODEREVIEW.toml": config})

        with pytest.raises(
            ValueError,
            match='large_scale_change: "\\*" is not supported in alternates',
        ):
            config.compiled_config(Path("CODEREVIEW.toml"), configs)


class TestReviewedForRemoved:
    """`reviewed_for` was removed entirely; it must now be rejected (scope
    models forbid extra keys)."""

    def test_reviewed_for_is_rejected(self):
        with pytest.raises(ValidationError, match="reviewed_for"):
            ConfigModel.from_data(
                {
                    "scopes": [
                        {
                            "name": "test",
                            "paths": ["*"],
                            "reviewers": ["alice"],
                            "reviewed_for": "required",
                        }
                    ]
                },
                Path("CODEREVIEW.toml"),
            )

    def test_checklist_still_passes(self):
        config = ConfigModel.from_data(
            {
                "scopes": [
                    {
                        "name": "test",
                        "paths": ["*"],
                        "reviewers": ["alice"],
                        "checklist": {"items": [{"label": "I reviewed the code"}]},
                    }
                ]
            },
            Path("CODEREVIEW.toml"),
        )
        assert config.scopes[0].checklist is not None


class TestMatchesAuthor:
    """Test the ScopeModel.matches_author() method."""

    def _scope(self, authors):
        return ScopeModel(name="test", paths=["*"], authors=authors)

    def test_no_authors_matches_anyone(self):
        scope = self._scope([])
        assert scope.matches_author("alice") is True

    def test_positive_author_matches(self):
        scope = self._scope(["alice", "bob"])
        assert scope.matches_author("alice") is True
        assert scope.matches_author("bob") is True

    def test_positive_author_excludes_unlisted(self):
        scope = self._scope(["alice", "bob"])
        assert scope.matches_author("carol") is False

    def test_negated_author_excludes_that_user(self):
        scope = self._scope(["!dependabot"])
        assert scope.matches_author("dependabot") is False

    def test_negated_author_matches_everyone_else(self):
        scope = self._scope(["!dependabot"])
        assert scope.matches_author("alice") is True
        assert scope.matches_author("bob") is True

    def test_mixed_positive_and_negated(self):
        scope = self._scope(["alice", "!dependabot"])
        assert scope.matches_author("alice") is True
        assert scope.matches_author("dependabot") is False
        assert scope.matches_author("bob") is False

    def test_case_insensitive_matching(self):
        scope = self._scope(["Alice", "!Dependabot"])
        assert scope.matches_author("alice") is True
        assert scope.matches_author("ALICE") is True
        assert scope.matches_author("dependabot") is False
        assert scope.matches_author("DEPENDABOT") is False


class TestBranchesRemoved:
    """`branches` was removed entirely; it must now be rejected wherever it
    appears (config models forbid extra keys)."""

    def test_config_level_branches_is_rejected(self):
        with pytest.raises(ValidationError, match="branches"):
            ConfigModel.from_data(
                {"branches": ["main"], "scopes": []}, Path("CODEREVIEW.toml")
            )

    def test_scope_level_branches_is_rejected(self):
        with pytest.raises(ValidationError, match="branches"):
            ConfigModel.from_data(
                {"scopes": [{"name": "s", "paths": ["*"], "branches": ["main"]}]},
                Path("CODEREVIEW.toml"),
            )


class TestCompileFilterSeparation:
    """PR-independent compilation vs PR-dependent filtering.

    `compiled()` resolves extends/aliases/paths once (no PR involved);
    `filter_for_pullrequest()` is a lightweight overlay that only drops
    author-disabled scopes from the already-compiled set.
    """

    def test_compiled_resolves_each_config(self):
        configs = ConfigModels.from_configs_data(
            {
                "app/CODEREVIEW.toml": {
                    "aliases": {"team": ["alice", "bob"]},
                    "scopes": [
                        {
                            "name": "s",
                            "paths": ["src/**"],
                            "reviewers": ["$team"],
                        }
                    ],
                }
            }
        )
        compiled = configs.compiled()
        scope = compiled["app/CODEREVIEW.toml"].scopes[0]
        # aliases expanded and paths anchored at the config's own directory
        assert scope.reviewers == ["alice", "bob"]
        assert scope.paths == ["app/src/**"]

    def test_compiled_returns_immutable_type_anchored_once(self):
        """compiled() returns a distinct CompiledConfigModels with paths anchored
        exactly once. The type has no compiled()/add_config, so the
        non-idempotent anchoring can never double-apply by construction."""
        configs = ConfigModels.from_configs_data(
            {
                "app/CODEREVIEW.toml": {
                    "scopes": [{"name": "s", "paths": ["src/**"], "reviewers": ["a"]}]
                }
            }
        )
        compiled = configs.compiled()
        assert isinstance(compiled, CompiledConfigModels)
        assert compiled["app/CODEREVIEW.toml"].scopes[0].paths == ["app/src/**"]
        # The compiled type cannot be recompiled or mutated → no double-anchor.
        assert not hasattr(compiled, "compiled")
        assert not hasattr(compiled, "add_config")

    def test_compiled_drops_extends_and_aliases(self):
        """The compiled/effective config is self-contained — its extends and
        aliases are already merged/expanded away."""
        configs = ConfigModels.from_configs_data(
            {
                "CODEREVIEW.toml": {
                    "extends": ["CODEREVIEW-BASE.toml"],
                    "scopes": [{"name": "s", "paths": ["*"], "reviewers": ["$team"]}],
                },
                "CODEREVIEW-BASE.toml": {
                    "template": True,
                    "aliases": {"team": ["alice"]},
                },
            }
        )
        compiled = configs.compiled()["CODEREVIEW.toml"]
        assert compiled.extends == []
        assert compiled.aliases == {}
        assert compiled.scopes[0].reviewers == ["alice"]

    def test_closest_config_returns_compiled_skips_templates(self):
        """closest_config selects the nearest non-template config and returns
        its already-compiled form (no recompile)."""
        configs = ConfigModels.from_configs_data(
            {
                "CODEREVIEW-TEMPLATE.toml": {
                    "template": True,
                    "scopes": [{"name": "t", "paths": ["**/*"], "reviewers": ["x"]}],
                },
                "app/CODEREVIEW.toml": {
                    "aliases": {"team": ["alice"]},
                    "scopes": [
                        {"name": "s", "paths": ["src/**"], "reviewers": ["$team"]}
                    ],
                },
            }
        )
        compiled = configs.compiled()
        config = compiled.closest_config(Path("app/src/foo.py"))
        assert [s.name for s in config.scopes] == ["s"]
        assert config.scopes[0].reviewers == ["alice"]
        assert config.scopes[0].paths == ["app/src/**"]

    def test_closest_config_no_config_raises(self):
        configs = ConfigModels.from_configs_data(
            {"app/CODEREVIEW.toml": {"scopes": []}}
        )
        with pytest.raises(ValueError, match="No config found"):
            configs.compiled().closest_config(Path("other/foo.py"))

    def test_compiled_propagates_value_error(self):
        """compiled() surfaces config errors as ValueError (not ValidationError)
        — the proposed-config validation in the processor relies on catching it."""
        configs = ConfigModels.from_configs_data(
            {
                "CODEREVIEW.toml": {
                    "scopes": [{"name": "s", "paths": ["*"], "reviewers": ["$typo"]}]
                }
            }
        )
        with pytest.raises(ValueError, match=r"Unknown alias: \$typo"):
            configs.compiled()

    def test_filter_returns_compiled_overlay(self):
        """filter_for_pullrequest overlays on a compiled set: aliases expanded,
        paths anchored, author-disabled scopes dropped, result still compiled."""
        configs = ConfigModels.from_configs_data(
            {
                "app/CODEREVIEW.toml": {
                    "aliases": {"team": ["alice"]},
                    "scopes": [
                        {
                            "name": "alice-only",
                            "paths": ["src/**"],
                            "authors": ["alice"],
                            "reviewers": ["$team"],
                        },
                        {
                            "name": "always",
                            "paths": ["src/**"],
                            "reviewers": ["$team"],
                        },
                    ],
                }
            }
        )
        filtered = configs.compiled().filter_for_pullrequest(author_username="dev")
        assert isinstance(filtered, CompiledConfigModels)
        # author-disabled scope dropped; survivor is compiled
        scopes = filtered["app/CODEREVIEW.toml"].scopes
        assert [s.name for s in scopes] == ["always"]
        assert scopes[0].reviewers == ["alice"]
        assert scopes[0].paths == ["app/src/**"]


def scope_toml(name):
    return f'[[scopes]]\nname = "{name}"\npaths = ["**"]\n'


class TestDeclaringConfigPath:
    def test_a_scope_inherited_through_extends(self):
        configs = ConfigModels.from_contents(
            {
                "shared/CODEREVIEW-team.toml": "template = true\n" + scope_toml("team"),
                "api/CODEREVIEW.toml": 'extends = ["../shared/CODEREVIEW-team.toml"]\n'
                + scope_toml("api"),
            }
        )
        assert (
            configs.declaring_config_path(
                config_path="api/CODEREVIEW.toml", scope_name="team"
            )
            == "shared/CODEREVIEW-team.toml"
        )
        assert (
            configs.declaring_config_path(
                config_path="api/CODEREVIEW.toml", scope_name="api"
            )
            == "api/CODEREVIEW.toml"
        )

    def test_a_scope_outside_the_chain(self):
        configs = ConfigModels.from_contents(
            {
                "CODEREVIEW.toml": scope_toml("root"),
                "api/CODEREVIEW.toml": scope_toml("api"),
            }
        )
        assert (
            configs.declaring_config_path(
                config_path="CODEREVIEW.toml", scope_name="api"
            )
            is None
        )


TEAM_TEMPLATE = """template = true

[[scopes]]
name = "first"
paths = ["**"]

# The team's scope
[[scopes]]
name = "team"
paths = ["**"]

[[scopes.checklist.items]]
label = "Tested it"

[[scopes]]
name = "last"
paths = ["**"]
"""


def test_scope_line_range_covers_the_table_and_its_sub_tables():
    # A blank line or comment leading into the next table isn't part of this
    # one; a scope's own sub-tables are.
    assert scope_line_range(content=TEAM_TEMPLATE, scope_name="first") == (3, 5)
    assert scope_line_range(content=TEAM_TEMPLATE, scope_name="team") == (8, 13)
    assert scope_line_range(content=TEAM_TEMPLATE, scope_name="last") == (15, 17)
    assert scope_line_range(content=TEAM_TEMPLATE, scope_name="missing") is None


def test_scope_line_range_skips_lines_inside_multi_line_strings():
    content = """[[scopes]]
name = "docs"
paths = ["**"]
instructions = \"\"\"
[Guidelines](https://example.com) first.
[x] Checked the links
\"\"\"

[[scopes]]
name = "after"
paths = ["**"]
"""
    assert scope_line_range(content=content, scope_name="docs") == (1, 7)
    assert scope_line_range(content=content, scope_name="after") == (9, 11)


def test_scope_line_range_ignores_delimiters_in_comments_and_single_line_strings():
    content = """# Write instructions with \"\"\" strings
[[scopes]]
name = "a"
description = "don'''t"
paths = ["**"]

[[scopes]]
name = "b"
paths = ["**"]
instructions = \"\"\"
An escaped \\\"\"\" doesn't close it
\"\"\"
"""
    assert scope_line_range(content=content, scope_name="a") == (2, 5)
    assert scope_line_range(content=content, scope_name="b") == (7, 12)


def test_scope_line_range_allows_tabs_and_quotes_in_headers():
    content = '[[\tscopes\t]]\nname = "a"\npaths = ["**"]\n\n[["scopes".checklist.items]]\nlabel = "x"\n'
    assert scope_line_range(content=content, scope_name="a") == (1, 6)


def test_scope_line_range_allows_spaces_inside_header_brackets():
    content = """[[ scopes ]]
name = "team"
paths = ["**"]

[[ scopes.checklist.items ]]
label = "Tested it"
"""
    assert scope_line_range(content=content, scope_name="team") == (1, 6)


def test_scope_line_range_counts_only_newlines_as_line_breaks():
    content = '# A comment\u2028[x] with a line separator\n[[scopes]]\nname = "team"\npaths = ["**"]\n'
    assert scope_line_range(content=content, scope_name="team") == (2, 4)
