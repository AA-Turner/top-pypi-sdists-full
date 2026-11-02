from pullapprove.results_migrations import (
    ResultsMigrator,
    migrate_agent_result_states,
)


def test_drops_branches_from_old_results():
    """Old stored results carry removed fields: config-level `branches`,
    scope-level `branches` (in both configs and scope results), and the
    PullRequest `base_branch`/`head_branch`. The migrations must strip all of
    them so the result re-parses under the models' `extra="forbid"`."""
    data = {
        "version": 1,
        "pullrequest": {
            "base_branch": {"name": "main"},
            "head_branch": {"name": "feature"},
            "reviewers": [],
        },
        "config_results": {
            "CODEREVIEW.toml": {
                "config": {
                    "branches": ["main"],
                    "scopes": [
                        {
                            "name": "all",
                            "paths": ["*"],
                            "branches": ["main"],
                            "reviewers": ["alice"],
                        }
                    ],
                }
            }
        },
        "scope_results": {
            "all": {"scope": {"name": "all", "paths": ["*"], "branches": ["main"]}}
        },
    }

    migrated = ResultsMigrator.migrate(data)

    assert "base_branch" not in migrated["pullrequest"]
    assert "head_branch" not in migrated["pullrequest"]
    config = migrated["config_results"]["CODEREVIEW.toml"]["config"]
    assert "branches" not in config
    assert "branches" not in config["scopes"][0]
    assert "branches" not in migrated["scope_results"]["all"]["scope"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_drops_reviewed_for_from_old_results():
    """The scope-level `reviewed_for` setting was removed. Old stored scopes
    that set it (in both configs and scope results) must be stripped so the
    result re-parses under the scope model's `extra="forbid"`."""
    data = {
        "version": 1,
        "config_results": {
            "CODEREVIEW.toml": {
                "config": {
                    "scopes": [
                        {
                            "name": "all",
                            "paths": ["*"],
                            "reviewed_for": "required",
                            "reviewers": ["alice"],
                        }
                    ],
                }
            }
        },
        "scope_results": {
            "all": {"scope": {"name": "all", "paths": ["*"], "reviewed_for": "ignored"}}
        },
    }

    migrated = ResultsMigrator.migrate(data)

    config = migrated["config_results"]["CODEREVIEW.toml"]["config"]
    assert "reviewed_for" not in config["scopes"][0]
    assert "reviewed_for" not in migrated["scope_results"]["all"]["scope"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_unwraps_review_results():
    """The ReviewResult wrapper was removed; review_results now maps host_id ->
    Review directly. Old stored {"review": {...}} wrappers (carrying the dropped
    matched_scopes) must be unwrapped to the bare review so they re-parse."""
    data = {
        "version": 1,
        "review_results": {
            "r1": {
                "review": {"host_id": "r1", "body": "x"},
                "matched_scopes": ["docs"],
            },
        },
    }

    migrated = ResultsMigrator.migrate(data)

    assert migrated["review_results"]["r1"] == {"host_id": "r1", "body": "x"}
    assert migrated["version"] == ResultsMigrator.current_version()


def test_drops_path_and_code_reviews():
    """PathResult.reviews / CodeResult.reviews were removed; old stored path and
    code results that carried them must be stripped so they re-parse under the
    models' `extra="forbid"`."""
    data = {
        "version": 1,
        "path_results": {
            "a.py": {"path": {}, "status": "pending", "reviews": ["r1"]},
        },
        "code_results": {
            "h1": {"code": {}, "status": "pending", "reviews": ["r1"]},
        },
    }

    migrated = ResultsMigrator.migrate(data)

    assert "reviews" not in migrated["path_results"]["a.py"]
    assert "reviews" not in migrated["code_results"]["h1"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_migrate_is_safe_when_config_results_absent():
    migrated = ResultsMigrator.migrate({"version": 1})
    assert migrated["version"] == ResultsMigrator.current_version()


def test_requested_placeholder_reviews_become_requested_flag():
    """Review requests used to be synthetic PENDING reviews with host_id
    "requested:<id>". They become `requested: true` on the reviewer, and the
    synthetic entries are stripped from review_results and review id lists."""
    placeholder = {
        "host_id": "requested:3",
        "host_url": "https://example.com/pull/1",
        "body": "",
        "state": "PENDING",
        "submitted_at": "2024-01-01T00:00:00",
        "user": {"host_id": "3", "username": "carol", "avatar_url": ""},
    }
    real_review = {
        "host_id": "r1",
        "host_url": "https://example.com/r/1",
        "body": "LGTM",
        "state": "APPROVED",
        "submitted_at": "2024-01-01T00:00:00Z",
        "user": {"host_id": "2", "username": "bob", "avatar_url": ""},
    }
    data = {
        "version": 7,
        "pullrequest": {
            "reviewers": [
                {"reviews": [real_review], "user": real_review["user"]},
                {"reviews": [placeholder], "user": placeholder["user"]},
            ],
        },
        "review_results": {"r1": real_review, "requested:3": placeholder},
        "scope_results": {
            "all": {
                "scope": {"name": "all", "paths": ["*"]},
                "reviews": ["r1", "requested:3"],
            }
        },
    }

    migrated = ResultsMigrator.migrate(data)

    bob, carol = migrated["pullrequest"]["reviewers"]
    assert bob["reviews"] == [real_review]
    assert "requested" not in bob
    assert carol["reviews"] == []
    assert carol["requested"] is True
    assert list(migrated["review_results"]) == ["r1"]
    assert migrated["scope_results"]["all"]["reviews"] == ["r1"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_migrate_drop_agents():
    """v8 -> v9: results stored while a config declared `[[agents]]` carry an
    `agents` list at the top level and inside stored config dumps. Both must
    strip, or the tombstone validator (ConfigModel) and the results model's
    extra="forbid" make old rows -- including merged PRs that never reprocess
    -- unrenderable."""
    data = {
        "version": 8,
        "agents": [{"username": "claude", "answer": "REPORTED"}],
        "config_results": {
            "CODEREVIEW.toml": {
                "config": {
                    "agents": [{"account": "claude[bot]"}],
                    "scopes": [{"name": "all", "paths": ["*"]}],
                }
            }
        },
    }

    migrated = ResultsMigrator.migrate(data)

    assert "agents" not in migrated
    assert "agents" not in migrated["config_results"]["CODEREVIEW.toml"]["config"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_migrate_agent_result_states():
    """v9 -> v10: the one "pending" agent state split into queued/running/
    disputed. AgentResult forbids extra keys, so the `in_flight`/`unstarted`
    flags that used to carry that distinction have to go — but they are what
    says which of the three each stored "pending" was, so each one migrates to
    the state its flags described. A dispute stored neither flag (both
    defaulted False), and turning it into "running" would relabel a settled
    dispute as a review still going — on a merged pull request, forever."""
    data = {
        "version": 9,
        "agent_results": {
            "claude": {"state": "pending", "in_flight": True, "unstarted": True},
            "gemini": {"state": "pending", "in_flight": True},
            "audit": {"state": "pending", "findings_summary": "1 disputed"},
            "codex": {"state": "blocking", "findings_summary": "1 blocking"},
        },
    }

    # The step on its own: the gate this rewrote is gone again a version
    # later (see test_migrate_drop_agent_results), so a full migrate would
    # strip what this asserts on.
    migrated = migrate_agent_result_states(data)

    assert migrated["agent_results"]["claude"] == {"state": "queued"}
    assert migrated["agent_results"]["gemini"] == {"state": "running"}
    assert migrated["agent_results"]["audit"] == {
        "state": "disputed",
        "findings_summary": "1 disputed",
    }
    assert migrated["agent_results"]["codex"] == {
        "state": "blocking",
        "findings_summary": "1 blocking",
    }


def test_migrate_drop_agent_results():
    """v10 -> v11: the agent gate left with the hosted agent reviews. Results
    stored while it ran carry an `agent_results` receipt, and config dumps an
    `agents` list; both models forbid extra keys, so both must strip for old
    rows -- merged pull requests that never reprocess -- to keep rendering."""
    data = {
        "version": 10,
        "agent_results": {"codex": {"state": "approved"}},
        "config_results": {
            "CODEREVIEW.toml": {
                "config": {
                    "agents": [{"name": "codex", "preset": "codex-review"}],
                    "scopes": [{"name": "all", "paths": ["*"]}],
                }
            }
        },
    }

    migrated = ResultsMigrator.migrate(data)

    assert "agent_results" not in migrated
    assert "agents" not in migrated["config_results"]["CODEREVIEW.toml"]["config"]
    assert migrated["version"] == ResultsMigrator.current_version()


def test_migrate_drop_removal_kind_flags():
    """v11 -> v12: the who-removed-it flags left with the single removal rule.
    Results stored while they existed carry them on reviewers, and Reviewer
    forbids extra keys, so they must strip. `removed` itself is kept."""
    data = {
        "version": 11,
        "pullrequest": {
            "reviewers": [
                {"user": {"host_id": "1"}, "removed": True, "removed_by_self": True},
                {"user": {"host_id": "2"}, "removed": True, "removed_by_bot": True},
                {"user": {"host_id": "3"}},
            ]
        },
    }

    migrated = ResultsMigrator.migrate(data)

    reviewers = migrated["pullrequest"]["reviewers"]
    assert [r.get("removed") for r in reviewers] == [True, True, None]
    assert not any("removed_by_self" in r or "removed_by_bot" in r for r in reviewers)
    assert migrated["version"] == ResultsMigrator.current_version()


def test_migrate_drop_large_scale_change_results():
    """v12 -> v13: a large-scale change is now a scope in `scope_results`.
    The old block must strip, or the results model's extra="forbid" makes old
    rows unrenderable. Nothing else is touched."""
    data = {
        "version": 12,
        "status": "PENDING",
        "large_scale_change_results": {
            "large_scale_change": {"reviewers": ["alice"], "require": 1},
            "status": "PENDING",
            "points": 0,
            "points_pending": 0,
            "reviews": [],
        },
        "scope_results": {},
    }

    migrated = ResultsMigrator.migrate(data)

    assert "large_scale_change_results" not in migrated
    assert migrated["status"] == "PENDING"
    assert migrated["scope_results"] == {}
    assert migrated["version"] == ResultsMigrator.current_version()


def test_a_persons_request_flag_becomes_who_asked():
    """A scope's people said `requested: true`; they now say who asked. A
    stored result can't know, so every standing request reads as a
    person's ("host"), and someone not requested gets no key at all."""
    data = {
        "version": 13,
        "scope_results": {
            "app": {
                "scope": {"name": "app", "paths": ["*"]},
                "people": [
                    {"username": "bob", "on_pullrequest": True, "requested": True},
                    {"username": "carol", "on_pullrequest": True},
                    {"username": "dana"},
                ],
            }
        },
    }

    migrated = ResultsMigrator.migrate(data)

    bob, carol, dana = migrated["scope_results"]["app"]["people"]
    assert bob == {"username": "bob", "on_pullrequest": True, "requested_by": "host"}
    assert carol == {"username": "carol", "on_pullrequest": True}
    assert dana == {"username": "dana"}
    assert migrated["version"] == ResultsMigrator.current_version()
