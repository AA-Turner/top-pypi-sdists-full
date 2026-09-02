"""
Tests for InnoDayVersionStore and the `innoday release`/`hotfix` proxy.

The store is exercised against a mocked InnoDayAPIClient (mirroring
test_releases_cli.py's mock style) -- the store's own logic is:
  * derive last_released_version = max released version, next_version = its
    minor bump;
  * bootstrap to v0.1.0 when there are no released rows;
  * record a release as a create-or-update call with status=released and the
    changelog wrapped as {"repos": [...]}.

The CLI proxy test mocks blastoff's Release.run so no real GitHub tagging
happens -- it asserts the store is injected and the version is passed through.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import blastoff.stores
import pytest

from src.integrations.innoday_version_store import (
    BOOTSTRAP_VERSION,
    InnoDayVersionStore,
)


def _response(status_code, json_body=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else {}
    resp.text = text
    return resp


def _api_serving(rows):
    """A mock API client that honours the ``status`` query param.

    `load_org_config` makes two calls now -- one for the released rows, one for
    the in-progress row -- so a mock with a single `return_value` would answer
    both with the same body and quietly make the two indistinguishable. Routing
    on the param is also what the real endpoint does (`list_releases` filters on
    `ReleaseStatus`), so the fake and the thing it stands in for agree.
    """

    async def get(_endpoint, params=None):
        wanted = (params or {}).get("status")
        served = [r for r in rows if not wanted or r.get("status") == wanted]
        return _response(200, served)

    api = MagicMock()
    api.get = AsyncMock(side_effect=get)
    return api


def _store(api_client):
    return InnoDayVersionStore(
        api_client=api_client,
        org_id="org-1",
        project_id="proj-1",
        github_org="havilandsoftware",
        topics=["pixelfuel"],
        prerelease="beta",
    )


class TestSubclass:
    def test_is_versionstore_subclass(self):
        assert issubclass(InnoDayVersionStore, blastoff.stores.VersionStore)


class TestLoadOrgConfig:
    def test_max_released_and_minor_bump(self):
        api = _api_serving(
            [
                {"version": "v1.2.0", "status": "released"},
                {"version": "v1.3.0", "status": "released"},
                {"version": "v1.1.0", "status": "released"},
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.last_released_version == "v1.3.0"
        assert org.next_version == "v1.4.0"  # minor bump of the max released
        assert org.organization == "havilandsoftware"
        assert org.label == "pixelfuel"
        # **Deliberately not asserted any more.** `OrgConfig` used to carry
        # `innoday_org_id`/`innoday_project_id`, and this store filled them in.
        # Nothing ever read them -- not here, not in blastoff -- so they were a
        # release engine's config schema naming one particular consumer, for no
        # behaviour. They are being removed from blastoff, and this store has to
        # stop supplying them first or the constructor call breaks on upgrade.
        assert org.prerelease == "beta"

        # Confirm it asked for each slice by status, scoped to the project.
        asked = {call.kwargs["params"]["status"] for call in api.get.call_args_list}
        assert asked == {"released", "in_progress"}
        assert all(
            call.kwargs["params"]["project_id"] == "proj-1"
            for call in api.get.call_args_list
        )

    def test_ignores_unparseable_versions(self):
        api = _api_serving(
            [
                {"version": "not-a-version", "status": "released"},
                {"version": "v2.0.0", "status": "released"},
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.last_released_version == "v2.0.0"
        assert org.next_version == "v2.1.0"

    def test_bootstrap_when_no_releases(self):
        api = _api_serving([])

        org = _store(api).load_org_config("pf")

        assert org.last_released_version is None
        assert org.next_version == BOOTSTRAP_VERSION == "v0.1.0"

    def test_missing_project_raises_filenotfound(self):
        api = MagicMock()
        store = InnoDayVersionStore(
            api_client=api,
            org_id="org-1",
            project_id="",  # unresolved project
            github_org="havilandsoftware",
            topics=["pixelfuel"],
        )
        with pytest.raises(FileNotFoundError):
            store.load_org_config("pf")


class TestRecordRelease:
    def test_records_released_status_and_wraps_changelog(self):
        api = MagicMock()
        api.post = AsyncMock(
            return_value=_response(201, {"version": "v1.4.0", "status": "released"})
        )

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf",
            organization="havilandsoftware",
            topics=["pixelfuel"],
            next_version="v1.4.0",
        )
        changelog = [
            {"repo": "app", "prs": [{"number": 1, "title": "Fix", "author": "x"}]}
        ]

        _store(api).record_release(
            org, "v1.4.0", summary="Ship it", changelog=changelog
        )

        api.post.assert_called_once()
        endpoint, kwargs = api.post.call_args
        assert endpoint[0] == "/organizations/org-1/releases"
        body = kwargs["json"]
        assert body["version"] == "v1.4.0"
        assert body["project_id"] == "proj-1"
        assert body["status"] == "released"
        assert body["released_at"]  # defaulted to now
        assert body["summary"] == "Ship it"
        # blastoff list-of-repos wrapped into InnoDay's dict column.
        assert body["changelog"] == {"repos": changelog}

    def test_uses_explicit_released_at(self):
        api = MagicMock()
        api.post = AsyncMock(return_value=_response(201, {}))

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf", organization="o", topics=["l"], next_version="v1.0.0"
        )
        _store(api).record_release(org, "v1.0.0", released_at="2026-07-21T00:00:00Z")

        body = api.post.call_args[1]["json"]
        assert body["released_at"] == "2026-07-21T00:00:00Z"

    def test_idempotent_conflict_falls_back_to_patch(self):
        api = MagicMock()
        api.post = AsyncMock(return_value=_response(409))
        api.get = AsyncMock(
            return_value=_response(200, {"id": "rel-1", "version": "v1.4.0"})
        )
        api.patch = AsyncMock(
            return_value=_response(200, {"version": "v1.4.0", "status": "released"})
        )

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf", organization="o", topics=["l"], next_version="v1.4.0"
        )
        # Should not raise -- re-running an already-recorded release updates it.
        _store(api).record_release(org, "v1.4.0")

        api.patch.assert_called_once()
        endpoint = api.patch.call_args[0][0]
        assert endpoint == "/organizations/org-1/releases/rel-1"
        # project_id is stripped from the PATCH body (can't be re-set).
        assert "project_id" not in api.patch.call_args[1]["json"]

    def test_server_error_raises(self):
        api = MagicMock()
        api.post = AsyncMock(return_value=_response(500, text="boom"))

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf", organization="o", topics=["l"], next_version="v1.0.0"
        )
        with pytest.raises(RuntimeError):
            _store(api).record_release(org, "v1.0.0")


class TestChangelogRoundTrip:
    """The writer's output, read by the reader that actually renders it.

    **This is the test whose absence let the two disagree.** Each side had its
    own tests and both passed: the store's asserted `{"repos": [...]}`, and the
    Releases tab's fed a bare list -- while its "malformed" case fed a dict,
    which is exactly what production writes. So the tab would have shown
    "0 repos · 0 PRs" for every release the engine ever recorded, and no test
    could have said so, because none of them ran the writer into the reader.

    Latent rather than observed: no release row carries a changelog yet (179
    rows in dev, all `null`), because recording has been failing upstream. This
    pins the seam before the first one lands, not after.
    """

    @staticmethod
    def _recorded_changelog(changelog):
        """The `changelog` value the store actually puts on the wire."""
        api = MagicMock()
        api.post = AsyncMock(return_value=_response(201, {}))

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf",
            organization="havilandsoftware",
            topics=["pixelfuel"],
            next_version="v1.4.0",
        )
        _store(api).record_release(org, "v1.4.0", changelog=changelog)
        return api.post.call_args.kwargs["json"]["changelog"]

    def test_the_tab_counts_what_the_store_recorded(self):
        from src.routers.webui.data import _changelog_totals

        # blastoff's own shape, straight out of `changelog_api.build_changelog`.
        blastoff_changelog = [
            {
                "repo": "innoday",
                "prs": [
                    {"number": 660, "title": "a", "author": "havkarl"},
                    {"number": 655, "title": "b", "author": "havkarl"},
                ],
            },
            {"repo": "innoday-blastoff", "prs": [{"number": 12, "title": "c"}]},
        ]

        stored = self._recorded_changelog(blastoff_changelog)

        assert _changelog_totals(stored) == (2, 3)

    def test_a_bare_list_still_counts(self):
        """A row written straight through the ORM, as the fixtures do."""
        from src.routers.webui.data import _changelog_totals

        assert _changelog_totals([{"repo": "innoday", "prs": [{"number": 1}]}]) == (
            1,
            1,
        )

    @pytest.mark.parametrize(
        "value",
        [None, "v1.0.0", 7, {}, {"repo": "innoday"}, {"repos": "innoday"}, [1, 2]],
    )
    def test_anything_else_counts_as_nothing(self, value):
        """Never a 500 on the one page that shows what shipped.

        `{"repo": ...}` (singular) is in here deliberately: it is a dict, so the
        unwrap above finds no `repos` key and must fall through to zero rather
        than raise.
        """
        from src.routers.webui.data import _changelog_totals

        assert _changelog_totals(value) == (0, 0)


class TestSaveOrgConfigNoOp:
    def test_save_org_config_touches_no_api(self):
        api = MagicMock()
        api.post = AsyncMock()
        api.patch = AsyncMock()
        api.put = AsyncMock()

        from blastoff.version_manager import OrgConfig

        org = OrgConfig(
            alias="pf", organization="o", topics=["l"], next_version="v1.0.0"
        )
        _store(api).save_org_config(org)  # no-op

        api.post.assert_not_called()
        api.patch.assert_not_called()
        api.put.assert_not_called()


class TestReleaseProxyCLI:
    """`innoday blastoff` drives the engine with a **brief**, not an alias.

    The GitHub account and topics used to come from a `release_configs` block in
    project.yml, keyed by an alias passed as `-c`. InnoDay already knows both --
    it computes them for `innoday init` -- so the copy in the file was one answer
    stored twice, matched case-sensitively (`pf` never matched project `PF`), and
    held up by a "there is only one entry" fallback.
    """

    def _args(self, **overrides):
        import argparse

        defaults = dict(
            hotfix=False,
            dry_run=True,  # tests never tag; the confirm path has its own class
            assume_yes=False,
            topics=None,
            repo=None,
            commit=None,
            org_id="org-1",
            project_id="proj-1",
            token=None,
            github_org=None,
            summary=None,
            commits=False,
            as_json=False,
            generate_summary=False,
            dir=None,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    def _config(self):
        config = MagicMock()
        config.get_current_organization.return_value = "hs"
        config.get_organization_id.return_value = "org-1"
        config.get_current_project_id.return_value = "proj-1"
        return config

    def _store(self):
        store = MagicMock()
        store.load_org_config.return_value = SimpleNamespace(
            next_version="v1.4.0",
            last_released_version="v1.3.0",
            last_released="2026-07-01T00:00:00Z",
            topics=["pf", "pixelfuel"],
        )
        store.ticket_picture.return_value = None
        return store

    def _drive(self, args=None, store=None, content=None):
        """Run `_drive_release`, returning (argv, brief) handed to the engine.

        `_fetch_content` is stubbed rather than mocked at the HTTP layer: it is
        the seam the release now depends on, and every test here is about what
        reaches the engine, not about how the content was obtained. Pass
        `content` to exercise the assembled path.
        """
        import asyncio
        import json as _json

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        captured = {}

        def fake_invoke(app_cls, argv, st, stdin=None, confirm=None):
            captured["argv"] = argv
            captured["brief"] = _json.loads(stdin) if stdin else None
            captured["confirm"] = confirm
            return 0

        async def fake_content(*a, **k):
            return content

        with (
            patch.object(
                ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
            ),
            patch.object(
                ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
            ),
        ):
            asyncio.run(
                ReleaseProxyCommands._drive_release(
                    args or self._args(),
                    store or self._store(),
                    "pf",
                    "havilandsoftware",
                    ["pf", "pixelfuel"],
                    MagicMock(),
                    "org-1",
                    "proj-1",
                )
            )
        return captured

    def test_the_engine_is_handed_a_brief_not_an_alias(self):
        captured = self._drive()
        assert captured["argv"][:2] == ["--brief", "-"]
        assert "-c" not in captured["argv"], "the alias lookup is gone"

    def test_the_brief_carries_what_the_lookup_used_to_supply(self):
        brief = self._drive()["brief"]
        assert brief["github_org"] == "havilandsoftware"
        assert brief["topics"] == ["pf", "pixelfuel"]
        assert brief["version"] == "v1.4.0"
        assert brief["previous_version"] == "v1.3.0"

    def test_all_topics_travel_not_just_the_first(self):
        """The divergence this closes: InnoDay found repos by every topic while
        blastoff was told only one, so a `pf`-only repo joined the project and
        was left out of its release."""
        assert self._drive()["brief"]["topics"] == ["pf", "pixelfuel"]

    def test_ticket_counts_ride_along_when_known(self):
        store = self._store()
        store.ticket_picture.return_value = (4, 4)
        brief = self._drive(store=store)["brief"]
        assert (brief["ticket_count"], brief["open_ticket_count"]) == (4, 4)

    def test_unknown_ticket_counts_are_absent_not_zero(self):
        """ "We could not ask" is not "there are none"; the report shows only
        the second."""
        brief = self._drive()["brief"]
        assert "ticket_count" not in brief

    def test_a_release_that_cannot_read_tickets_still_runs(self):
        """A release must not fail because a count would not load."""
        store = self._store()
        store.ticket_picture.side_effect = RuntimeError("boom")
        assert self._drive(store=store)["brief"]["version"] == "v1.4.0"


class TestTheStoreCutsThePipelinesVersion:
    """The version blastoff tags and the version the page shows are one row.

    They were not, and nothing reconciled them. `load_org_config` derived the tag
    from ``max(released).bump_minor()`` while querying only ``status="released"``
    -- the upcoming rows were invisible to it. A project that had shipped v1.8.0
    and carried a planned v2.0.0 showed v2.0.0 on screen and tagged v1.9.0, then
    left v2.0.0 dangling because nothing revisited it.
    """

    def test_the_in_progress_release_is_what_gets_cut(self):
        api = _api_serving(
            [
                {"version": "v1.8.0", "status": "released"},
                {"version": "v2.0.0", "status": "in_progress"},
                {"version": "v2.1.0", "status": "planned"},
            ]
        )

        org = _store(api).load_org_config("pf")

        # Not v1.9.0, which is what a minor bump of the high-water mark gives.
        assert org.next_version == "v2.0.0"
        assert org.last_released_version == "v1.8.0"

    def test_a_project_with_no_pipeline_still_falls_back_to_a_minor_bump(self):
        """The old derivation is the fallback, not a dead branch: a project whose
        pipeline has not been established yet must still be releasable."""
        api = _api_serving([{"version": "v1.8.0", "status": "released"}])

        assert _store(api).load_org_config("pf").next_version == "v1.9.0"

    def test_a_non_semver_in_progress_tag_is_cut_as_written(self):
        """Someone deliberately planned `rancher-FINAL`. It cannot be bumped or
        compared, but cutting the version the project says it is cutting is
        right -- guessing a semver instead would tag something nobody asked for."""
        api = _api_serving(
            [
                {"version": "v1.8.0", "status": "released"},
                {"version": "rancher-FINAL", "status": "in_progress"},
            ]
        )

        assert _store(api).load_org_config("pf").next_version == "rancher-FINAL"

    @pytest.mark.parametrize(
        "rows",
        [
            # Nothing at all -- the pipeline bootstraps.
            [],
            # Shipped, with a pipeline already open above it.
            [
                {"version": "v1.8.0", "status": "released"},
                {"version": "v1.9.0", "status": "in_progress"},
                {"version": "v1.10.0", "status": "planned"},
            ],
            # The case that used to diverge: an upcoming version well above the
            # minor bump the store would otherwise have computed.
            [
                {"version": "v1.8.0", "status": "released"},
                {"version": "v2.0.0", "status": "in_progress"},
            ],
            # Shipped, with no pipeline open yet.
            [{"version": "v1.8.0", "status": "released"}],
            # A stale IN_PROGRESS below the high-water mark -- BPAI's original
            # bug, which used to make the page name a version four releases old.
            [
                {"version": "v1.4.0", "status": "in_progress"},
                {"version": "v1.8.0", "status": "released"},
            ],
        ],
    )
    def test_the_page_and_the_command_name_the_same_version(self, rows):
        """**This is the defect, stated as a test.**

        For one project state, what `next_release` puts on the dashboard and the
        Releases tab must equal what `load_org_config` hands blastoff to tag.

        The invariant is applied first, exactly as the release router and
        repository sync apply it -- that is what production guarantees, and it is
        the thing that makes the two agree. A project with no pipeline has
        nothing to show and nothing to compare; a project with one always does,
        which is the second assertion here.
        """
        from src.domain.release import Release, ReleaseStatus
        from src.services.release_planning import ensure_pipeline, next_release

        model_rows = [
            Release(
                organization_id="org-1",
                project_id="proj-1",
                version=row["version"],
                status=ReleaseStatus(row["status"]),
            )
            for row in rows
        ]
        for version, status in ensure_pipeline(model_rows):
            model_rows.append(
                Release(
                    organization_id="org-1",
                    project_id="proj-1",
                    version=version,
                    status=status,
                )
            )

        upcoming = next_release(model_rows)
        assert upcoming is not None, "a maintained pipeline always has a next"

        served = [{"version": r.version, "status": r.status.value} for r in model_rows]
        cut_by_blastoff = (
            _store(_api_serving(served)).load_org_config("pf").next_version
        )

        assert upcoming.version == cut_by_blastoff


class TestTheDryRunSaysWhatWorkIsPlannedIn:
    """**The half of the report blastoff structurally cannot provide.**

    The engine decides what is in a release from GitHub merge dates and has no
    idea tickets exist, so a preview could say which pull requests were in and
    nothing at all about the work planned into it -- while shipping used to close
    every ticket carrying the version.

    Returned rather than printed: it belongs on the report's header line beside
    the repo and PR counts. A separate sentence above the header was the second
    of the two headers that change removed.
    """

    @staticmethod
    def _store_seeing(rows):
        api = MagicMock()
        api.get = AsyncMock(return_value=_response(200, rows))
        return _store(api)

    def test_it_reports_planned_and_unfinished(self):
        store = self._store_seeing(
            [{"version": "v1.4.0", "ticket_count": 7, "open_ticket_count": 2}]
        )
        assert store.ticket_picture("v1.4.0") == (7, 2)

    def test_an_unknown_version_is_unknown_not_zero(self):
        """`None`, never `(0, 0)`.

        "We could not ask" and "nothing is planned in" are different answers, and
        printing the second for the first is the preview lying quietly -- which is
        the exact failure this whole change exists to remove.
        """
        store = self._store_seeing(
            [{"version": "v9.9.9", "ticket_count": 3, "open_ticket_count": 1}]
        )
        assert store.ticket_picture("v1.4.0") is None

    def test_a_row_without_counts_is_unknown(self):
        store = self._store_seeing([{"version": "v1.4.0"}])
        assert store.ticket_picture("v1.4.0") is None

    def test_a_failing_api_never_blocks_a_release(self):
        api = MagicMock()
        api.get = AsyncMock(side_effect=RuntimeError("boom"))
        assert _store(api).ticket_picture("v1.4.0") is None

    def test_the_proxy_swallows_a_store_that_raises(self):
        """Belt and braces: the store guards itself, and so does the caller."""
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        store = MagicMock()
        store.ticket_picture.side_effect = RuntimeError("boom")
        assert ReleaseProxyCommands._ticket_picture(store, "v1.4.0") is None

    def test_a_store_without_the_method_is_fine(self):
        """An older store, or a stub. Absence is not an error."""
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        assert (
            ReleaseProxyCommands._ticket_picture(MagicMock(spec=[]), "v1.4.0") is None
        )


class TestBlastoffArgvSurvivesTheRealParser:
    """`_invoke_blastoff` hands argv to plumbum, so plumbum has to accept it.

    Every other test here stubs `Release.run`, which is the whole reason this
    broke unnoticed: stubbing `run` skips plumbum's argument parsing entirely, so
    `assert "-c" in argv` passed while the real command failed on every
    invocation. These tests stub `main` instead -- the method plumbum calls
    *after* parsing -- so the parser runs for real.
    """

    def _store(self):
        store = MagicMock(spec=["load_org_config"])
        return store

    def test_the_switches_parse(self):
        from blastoff.release import Release

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        seen = {}

        # `(self)` exactly, matching the real `Release.main`. plumbum derives the
        # allowed positional count from this signature, so a `*args` stub would
        # cheerfully swallow the stray positional and hide the very failure
        # these tests exist to catch -- as it did on the first attempt.
        def fake_main(self):
            seen["topic"] = getattr(self, "_topic", None)
            return 0

        with patch.object(Release, "main", fake_main):
            code = ReleaseProxyCommands._invoke_blastoff(
                Release, ["-c", "pf", "-o", "havilandsoftware"], self._store()
            )

        assert code == 0, (
            "plumbum rejected the argv. If argv[0] is a switch it is consumed as "
            "the program name and the value behind it becomes a positional: "
            "\"Expected at most 0 positional arguments, got ['pf']\""
        )
        assert seen["topic"] == "pf"

    def test_a_missing_program_name_is_what_breaks_it(self):
        """Pinning the failure mode itself, so the fix cannot be quietly undone.

        plumbum's `Application.run` does `inst = cls(argv.pop(0))` -- argv has the
        same shape as `sys.argv`, executable included.
        """
        from blastoff.release import Release

        def fake_main(self):
            return 0

        with patch.object(Release, "main", fake_main):
            _inst, retcode = Release.run(
                ["-c", "pf", "-o", "havilandsoftware"], exit=False
            )

        assert retcode != 0, (
            "plumbum accepted a switch as argv[0]; if this ever passes, the "
            "program-name prepend in _invoke_blastoff is no longer needed"
        )


class TestTheReportFlagsReachTheEngine:
    """**A flag the engine has and the proxy does not is silently unreachable.**

    This parser owns the command line, so argparse rejects an undeclared flag
    before blastoff is ever entered. That is how #663 happened: blastoff 0.5.0
    made summary generation opt-in behind `--generate-summary`, the proxy
    forwarded neither that nor `--json`, and upgrading the engine left
    `innoday release` producing no summary at all.
    """

    def _argv_for(self, **flags):
        return TestReleaseProxyCLI()._drive(TestReleaseProxyCLI()._args(**flags))[
            "argv"
        ]

    def test_each_flag_is_forwarded(self):
        assert "--json" in self._argv_for(as_json=True)
        assert "--generate-summary" in self._argv_for(generate_summary=True)
        assert "--commits" in self._argv_for(commits=True)

    def test_the_removed_flags_are_not_forwarded(self):
        """**`--prs` and `--pr-list` no longer exist in the engine.**

        They read as the same flag and acted on opposite sets, and in a dry run
        the first did nothing at all. Both sections are now always shown. This
        test used to assert they were forwarded; forwarding them today is an
        unknown-argument error one layer down.
        """
        argv = self._argv_for(commits=True, as_json=True, generate_summary=True)
        assert "--prs" not in argv
        assert "--pr-list" not in argv

    def test_none_are_forwarded_unasked(self):
        """`--generate-summary` especially: billed, and it deadlocks when run
        from inside a Claude Code session."""
        argv = self._argv_for()
        for flag in ("--json", "--generate-summary", "--commits"):
            assert flag not in argv

    def test_the_engine_accepts_the_argv_the_proxy_actually_builds(self):
        """Declared here is not the same as accepted there -- and the argv under
        test must be **the proxy's own**, not one hand-written to match it.

        Written the obvious way first, with a literal list, and a mutation caught
        it: misspelling the flag the proxy appends left it green, because the two
        halves were joined only by the same string being typed twice.

        `main` is stubbed rather than `run`, because stubbing `run` skips
        plumbum's parsing entirely -- which is how a broken argv once passed its
        tests and failed on every real invocation.
        """
        from blastoff.release import Release

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        argv = self._argv_for(commits=True, as_json=True, generate_summary=True)
        seen = {}

        def fake_main(self):
            seen["json"] = getattr(self, "_json", None)
            seen["commits"] = getattr(self, "_commits", None)
            seen["gen"] = getattr(self, "_generate_summary_flag", None)
            seen["brief"] = getattr(self, "_brief", None)
            return 0

        with patch.object(Release, "main", fake_main):
            code = ReleaseProxyCommands._invoke_blastoff(
                Release,
                argv,
                MagicMock(spec=["load_org_config"]),
                stdin="{}",
            )

        assert code == 0, "blastoff rejected a flag the proxy forwards"
        assert seen["json"] and seen["commits"] and seen["gen"]
        assert seen["brief"] == "-", "the brief must arrive on stdin"


class TestTheInjectionDoesNotLeak:
    """`version_store` and `confirm` are class attributes on a shared engine.

    Left set, they leak into the next invocation in the same process -- which is
    every MCP tool call, and any test after this one. The store half was already
    pinned; `confirm` is new and leaks the same way, only worse: a stale hook
    would make a later *preview* tag things.
    """

    def test_both_are_restored_afterwards(self):
        from blastoff.release import Release

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        before_store = Release.version_store
        before_confirm = Release.confirm

        with patch.object(Release, "main", lambda self: 0):
            ReleaseProxyCommands._invoke_blastoff(
                Release,
                ["--brief", "-"],
                MagicMock(spec=["load_org_config"]),
                stdin="{}",
                confirm=lambda version, repos: True,
            )

        assert Release.version_store is before_store
        assert Release.confirm is before_confirm

    def test_they_are_restored_even_when_the_engine_raises(self):
        from blastoff.release import Release

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        before_store, before_confirm = Release.version_store, Release.confirm

        def boom(self):
            raise RuntimeError("blastoff exploded")

        with patch.object(Release, "main", boom):
            ReleaseProxyCommands._invoke_blastoff(
                Release,
                ["--brief", "-"],
                MagicMock(),
                stdin="{}",
                confirm=lambda **k: True,
            )

        assert Release.version_store is before_store
        assert Release.confirm is before_confirm


class TestJsonOutputIsOneDocument:
    """A caller passing `--json` parses stdout. Anything else printed there
    makes the whole thing unparseable.

    The proxy used to print its own "Releasing …" line above the engine's
    report, and had to suppress it under `--json`. It now prints **nothing** --
    the engine's header is the only one -- so there is no longer anything to
    suppress. Pinned because the temptation to add a friendly line back is
    permanent, and CI is where that failure surfaces (no `claude` binary there,
    green on four developer machines and red on the runner).
    """

    def test_the_proxy_prints_nothing_of_its_own(self):
        import asyncio

        from src.cli.commands.release_proxy import ReleaseProxyCommands

        cli = TestReleaseProxyCLI()

        async def no_content(*a, **k):
            return None

        with patch("src.cli.commands.release_proxy.console") as console:
            with (
                patch.object(
                    ReleaseProxyCommands,
                    "_invoke_blastoff",
                    staticmethod(lambda *a, **k: 0),
                ),
                patch.object(
                    ReleaseProxyCommands, "_fetch_content", staticmethod(no_content)
                ),
            ):
                asyncio.run(
                    ReleaseProxyCommands._drive_release(
                        cli._args(as_json=True, dry_run=False),
                        cli._store(),
                        "pf",
                        "havilandsoftware",
                        ["pf"],
                        MagicMock(),
                        "org-1",
                        "proj-1",
                    )
                )
        console.print.assert_not_called()


def _async_returning(value):
    """A stand-in for a coroutine function that just returns `value`.

    `_drive_release` became async when the release started being assembled
    server-side; a plain lambda here yields an int the caller then tries to
    await.
    """

    async def _stub(*a, **k):
        return value

    return _stub


class TestTheApprovalPoint:
    """One run previews *and* ships, and a run that cannot ask refuses to tag."""

    def _args(self, **over):
        return TestReleaseProxyCLI()._args(**over)

    def _confirmer(self, **over):
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        return ReleaseProxyCommands._confirmer(self._args(**over))

    def test_dry_run_never_tags(self):
        assert self._confirmer(dry_run=True) is None

    def test_json_implies_dry_run(self, monkeypatch):
        """A caller parsing one document is not going to answer a prompt, and a
        prompt would land in the middle of its stdout.

        **With a terminal attached**, deliberately. Written without it first and
        a mutation caught it: pytest's stdin is not a tty, so removing the
        `as_json` check left the test green — it was passing on the
        cannot-ask branch, not the one it names.
        """
        import io
        import sys

        stream = io.StringIO("y\n")
        stream.isatty = lambda: True
        monkeypatch.setattr(sys, "stdin", stream)

        assert self._confirmer(dry_run=False, as_json=True, do_release=True) is None
        # …and the same run without --json does get asked, so the terminal is
        # genuinely present and it is `as_json` doing the work.
        assert callable(self._confirmer(dry_run=False, as_json=False, do_release=True))

    def test_yes_skips_the_asking_not_the_reporting(self):
        assert self._confirmer(dry_run=False, assume_yes=True) is True

    def test_a_bare_run_reports_and_stops(self, monkeypatch):
        """`innoday blastoff` with no flags must not offer to tag.

        The two mistakes do not cost the same. A preview nobody wanted costs a
        scroll; a tag nobody wanted is written to every repository in the
        project and cannot be taken back -- innoday's own patch number is the
        *count* of its version tags, so deleting one to undo a slip silently
        stops every future publish while CI stays green.

        Before this, somebody typing the command to see what a release contained
        was one keystroke from tagging, and the keystroke was the answer to a
        question they had not asked for.
        """
        import io
        import sys

        stream = io.StringIO("y\n")
        stream.isatty = lambda: True
        monkeypatch.setattr(sys, "stdin", stream)

        assert self._confirmer(dry_run=False) is None

    def test_release_is_what_asks(self, monkeypatch):
        """…and the same run with the flag does get asked, so it is `--release`
        doing the work and not the missing terminal."""
        import io
        import sys

        stream = io.StringIO("y\n")
        stream.isatty = lambda: True
        monkeypatch.setattr(sys, "stdin", stream)

        assert callable(self._confirmer(dry_run=False, do_release=True))

    def test_yes_carries_the_intent_on_its_own(self):
        """`--yes` means "do not ask me", which only says anything about a run
        that is going to tag. Requiring `--release` beside it would break every
        script already passing it and buy nothing -- there is no reading of
        `--yes` that wants a report."""
        assert self._confirmer(dry_run=False, assume_yes=True) is True

    def test_the_hint_fires_only_when_somebody_needs_it(self):
        """`--dry-run` asked for a report and does not need telling it got one.
        A bare run did not, and a report that stops without saying how to
        proceed reads as a failure."""
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        stopped = ReleaseProxyCommands._stopped_at_the_report
        assert stopped(self._args(dry_run=False)) is True
        assert stopped(self._args(dry_run=True)) is False
        assert stopped(self._args(dry_run=False, do_release=True)) is False
        assert stopped(self._args(dry_run=False, assume_yes=True)) is False

    def test_a_run_that_cannot_ask_refuses_to_tag(self, monkeypatch):
        """cron, CI, a pipe. Treating an unanswerable prompt as approval would
        tag every repository because nobody was there to say no."""
        import sys

        monkeypatch.setattr(sys, "stdin", SimpleNamespace(isatty=lambda: False))
        assert self._confirmer(dry_run=False) is None

    def test_a_terminal_gets_asked(self, monkeypatch):
        import io
        import sys

        stream = io.StringIO("y\n")
        stream.isatty = lambda: True
        monkeypatch.setattr(sys, "stdin", stream)

        ask = self._confirmer(dry_run=False, do_release=True)
        assert callable(ask)
        assert ask(version="v1.0.0", repos=["a"]) is True

    def test_only_yes_means_yes(self, monkeypatch):
        import io
        import sys

        for answer, expected in (("y", True), ("YES", True), ("", False), ("n", False)):
            stream = io.StringIO(answer + "\n")
            stream.isatty = lambda: True
            monkeypatch.setattr(sys, "stdin", stream)
            ask = self._confirmer(dry_run=False, do_release=True)
            assert ask(version="v1.0.0", repos=["a"]) is expected, answer

    def test_the_prompt_reads_the_terminal_not_the_brief(self, monkeypatch):
        """**The subtle one.** The brief is handed to blastoff on stdin, so by
        the time the hook runs `sys.stdin` is a spent buffer holding that JSON.
        `input()` would read the brief back as the answer, or hit EOF. The hook
        captures the real terminal before the swap.
        """
        import io
        import sys

        terminal = io.StringIO("y\n")
        terminal.isatty = lambda: True
        monkeypatch.setattr(sys, "stdin", terminal)
        ask = self._confirmer(dry_run=False, do_release=True)

        # …now the brief replaces stdin, exactly as _invoke_blastoff does.
        monkeypatch.setattr(sys, "stdin", io.StringIO('{"github_org": "x"}'))
        assert ask(version="v1.0.0", repos=["a"]) is True


class TestScopeBelongsToHotfix:
    """`--repo`/`--commit` narrow a hotfix. A release is never partial."""

    def _check(self, hotfix, **over):
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        return ReleaseProxyCommands._check_scope(
            TestReleaseProxyCLI()._args(**over), hotfix
        )

    def test_a_release_refuses_repo(self):
        message = self._check(False, repo="innoday")
        assert message and "--repo is only for a hotfix" in message
        # It should say what would go wrong, not just "no".
        assert "counting the same work twice" in message

    def test_a_release_refuses_commit(self):
        assert self._check(False, repo="innoday", commit="abc1234")

    def test_a_hotfix_allows_both(self):
        assert self._check(True, repo="innoday", commit="abc1234") is None

    def test_a_hotfix_with_neither_covers_the_project(self):
        assert self._check(True) is None

    def test_commit_needs_repo_even_on_a_hotfix(self):
        """A commit belongs to one repository; a hotfix may span several."""
        message = self._check(True, commit="abc1234")
        assert message and "--commit needs --repo" in message


class TestTheApiClientIsClosedBeforeTheLoopIs:
    """The proxy's teardown has to *await* the close, not schedule it.

    It used to branch on whether an event loop was running and, when one was,
    `ensure_future(api_client.close())`. A loop is always running here -- the CLI
    dispatcher awaits these entry points -- so it always took that branch,
    returned immediately, and the loop closed before the task ran:

        ✗ Error: Event loop is closed

    A line meant only to release a connection failed the whole command.
    """

    def _args(self):
        args = MagicMock()
        for name in ("repo", "commit", "summary", "token", "org", "topics"):
            setattr(args, name, None)
        for name in ("hotfix", "assume_yes", "as_json", "prs", "commits"):
            setattr(args, name, False)
        args.dry_run = True
        return args

    @pytest.mark.asyncio
    async def test_close_is_awaited_within_the_running_loop(self):
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        resolved = ("pf", "havilandsoftware", ["pf", "pixelfuel"])
        closed = {"awaited": False}

        async def fake_close():
            closed["awaited"] = True

        with (
            patch(
                "src.cli.commands.release_proxy._resolve_release_target",
                AsyncMock(return_value=resolved),
            ),
            patch("src.cli.commands.release_proxy.InnoDayAPIClient") as MockClient,
            patch(
                "src.cli.commands.release_proxy._build_store",
                return_value=MagicMock(spec=["load_org_config"]),
            ),
            patch.object(
                ReleaseProxyCommands,
                "_drive_release",
                staticmethod(_async_returning(0)),
            ),
        ):
            MockClient.return_value.close = fake_close
            code = await ReleaseProxyCommands.execute_release(self._args(), MagicMock())

        assert code == 0
        # Ran to completion *before* execute_release returned. A scheduled task
        # would still be pending here, and the loop would close without it.
        assert closed["awaited"], (
            "the client close did not run inside the command; if it is scheduled "
            "rather than run to completion, the loop closes first and the "
            "command fails with 'Event loop is closed'"
        )

    @pytest.mark.asyncio
    async def test_the_close_runs_even_when_blastoff_fails(self):
        """It is in a `finally`, and a failed release must not also leak a
        connection."""
        from src.cli.commands.release_proxy import ReleaseProxyCommands

        resolved = ("pf", "havilandsoftware", ["pf", "pixelfuel"])
        closed = {"awaited": False}

        async def fake_close():
            closed["awaited"] = True

        def boom(*_a, **_k):
            raise RuntimeError("blastoff exploded")

        with (
            patch(
                "src.cli.commands.release_proxy._resolve_release_target",
                AsyncMock(return_value=resolved),
            ),
            patch("src.cli.commands.release_proxy.InnoDayAPIClient") as MockClient,
            patch(
                "src.cli.commands.release_proxy._build_store",
                return_value=MagicMock(spec=["load_org_config"]),
            ),
            patch.object(ReleaseProxyCommands, "_drive_release", staticmethod(boom)),
        ):
            MockClient.return_value.close = fake_close
            with pytest.raises(RuntimeError):
                await ReleaseProxyCommands.execute_release(self._args(), MagicMock())

        assert closed["awaited"]


class TestEveryRequestSharesOneLoop:
    """Two requests in one command must not each get a throwaway loop.

    `httpx.AsyncClient` pools connections, so a connection opened under one loop
    and reused under the next raises `RuntimeError: Event loop is closed` from
    *inside a request*. Nothing hit it while `load_org_config` made a single
    request; it began failing the moment the pipeline work added the IN_PROGRESS
    lookup beside the released one.
    """

    def test_sequential_calls_run_on_the_same_loop(self):
        import asyncio

        from src.integrations.innoday_version_store import _run_sync

        async def which_loop():
            return id(asyncio.get_running_loop())

        first = _run_sync(which_loop())
        second = _run_sync(which_loop())
        assert first == second, (
            "each call got its own loop; the client's pooled connections belong "
            "to the first one and the second request will fail on them"
        )

    def test_the_loop_outlives_a_call_rather_than_being_closed(self):

        from src.integrations.innoday_version_store import _run_sync, _StoreLoop

        async def noop():
            return None

        _run_sync(noop())
        assert _StoreLoop._loop is not None and not _StoreLoop._loop.is_closed()

    def test_load_org_config_makes_two_requests_and_survives_both(self):
        """The regression, at the level it actually happened: two listings in one
        `load_org_config`, through one client."""
        api = _api_serving([{"version": "v1.8.0", "status": "released"}])

        org = _store(api).load_org_config("pf")

        statuses = sorted(
            call.kwargs["params"]["status"] for call in api.get.call_args_list
        )
        assert statuses == ["in_progress", "released"]
        # Both requests completed. Before the shared loop, the second raised
        # "Event loop is closed" on a connection pooled under the first's loop.
        assert org.next_version == "v1.9.0"


class TestLastReleasedTimestamp:
    """``last_released`` is what bounds blastoff's changelog window.

    It was hardcoded None, and blastoff read no other boundary, so
    ``list_merged_pull_requests_since(None)`` returned every merged PR the org
    had ever had — a dry run reported the whole history as one release's
    contents. Supplying the timestamp is half the fix; blastoff's own git-tag
    fallback is the other half, and covers every project this half cannot.
    """

    def test_released_at_of_the_max_released_row_is_supplied(self):
        api = _api_serving(
            [
                {
                    "version": "v1.2.0",
                    "status": "released",
                    "released_at": "2026-06-01T00:00:00Z",
                },
                {
                    "version": "v1.3.0",
                    "status": "released",
                    "released_at": "2026-07-14T10:00:00Z",
                },
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.last_released == "2026-07-14T10:00:00Z"

    def test_the_timestamp_comes_from_the_max_version_not_the_last_row(self):
        """Paired with the version, so the boundary can't come from a different
        release than the base version does."""
        api = _api_serving(
            [
                {
                    "version": "v1.3.0",
                    "status": "released",
                    "released_at": "2026-07-14T10:00:00Z",
                },
                {
                    "version": "v1.1.0",
                    "status": "released",
                    "released_at": "2026-08-01T00:00:00Z",
                },  # later row, lower version
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.last_released_version == "v1.3.0"
        assert org.last_released == "2026-07-14T10:00:00Z"

    def test_a_released_row_without_a_timestamp_yields_none(self):
        """released_at is nullable, so the version can exist without it. None is
        the honest answer — blastoff then falls back to the git tag."""
        api = _api_serving([{"version": "v1.3.0", "status": "released"}])

        org = _store(api).load_org_config("pf")

        assert org.last_released_version == "v1.3.0"
        assert org.last_released is None

    def test_no_released_rows_yields_none(self):
        """The common case for a project that has never shipped through InnoDay
        — on 2026-08-11, every project except PF. blastoff's git-tag fallback is
        the entire fix for these."""
        api = _api_serving([{"version": "v2.0.0", "status": "in_progress"}])

        org = _store(api).load_org_config("pf")

        assert org.last_released is None
        assert org.next_version == "v2.0.0"

    def test_an_unparseable_version_does_not_donate_its_timestamp(self):
        api = _api_serving(
            [
                {
                    "version": "rancher-FINAL",
                    "status": "released",
                    "released_at": "2026-08-09T00:00:00Z",
                },
                {
                    "version": "v1.0.0",
                    "status": "released",
                    "released_at": "2026-07-01T00:00:00Z",
                },
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.last_released_version == "v1.0.0"
        assert org.last_released == "2026-07-01T00:00:00Z"


class TestTwoSlotPipelineUnchanged:
    """Regression guard for #528: the version blastoff cuts must stay slot 1.

    The changelog-window fix touches the same method, and the failure mode it
    risks reintroducing is silent — the page names one version, the command tags
    another. `last_released_version` also has to keep meaning "max released",
    because hotfix uses it as its base.
    """

    def test_the_in_progress_slot_is_still_what_gets_cut(self):
        api = _api_serving(
            [
                {
                    "version": "v1.8.0",
                    "status": "released",
                    "released_at": "2026-07-14T10:00:00Z",
                },
                {"version": "v2.0.0", "status": "in_progress"},
            ]
        )

        org = _store(api).load_org_config("pf")

        # Slot 1, not a minor bump of the max released (which would be v1.9.0).
        assert org.next_version == "v2.0.0"
        # ...and the hotfix base is still the max released.
        assert org.last_released_version == "v1.8.0"
        # ...and the window starts at that release, not at the one being cut.
        assert org.last_released == "2026-07-14T10:00:00Z"

    def test_supplying_the_timestamp_did_not_change_the_fallback_bump(self):
        api = _api_serving(
            [
                {
                    "version": "v1.8.0",
                    "status": "released",
                    "released_at": "2026-07-14T10:00:00Z",
                }
            ]
        )

        org = _store(api).load_org_config("pf")

        assert org.next_version == "v1.9.0"


class TestTheProjectIsResolvedFromInnoDay:
    """The GitHub account and topics come from InnoDay, not from a file.

    They used to be read out of a `release_configs` block in project.yml --
    values InnoDay already computes for `innoday init`. Two copies of one
    answer, keyed by an alias matched byte-for-byte, held up by a "there is only
    one entry" fallback.
    """

    def _client(self, status=200, body=None):
        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        client.get = AsyncMock(return_value=_response(status, body or {}))
        return client

    async def _resolve(self, client):
        from src.cli.commands import release_proxy

        with patch.object(release_proxy, "InnoDayAPIClient", return_value=client):
            return await release_proxy._resolve_release_target(
                MagicMock(), "org-1", "proj-1"
            )

    @pytest.mark.asyncio
    async def test_it_asks_innoday_and_gets_all_the_topics(self):
        client = self._client(
            body={
                "org": {"alias": "hs", "github_org": "havilandsoftware"},
                "project": {"alias": "PF"},
                "github_topic": "pf,pixelfuel",
            }
        )
        assert await self._resolve(client) == (
            "PF",
            "havilandsoftware",
            ["pf", "pixelfuel"],
        )

    @pytest.mark.asyncio
    async def test_it_reuses_the_endpoint_init_already_trusts(self):
        """Not a new endpoint — `/onboarding/resolve` returns exactly these
        fields and is what `innoday init` already believes."""
        client = self._client(
            body={
                "org": {"github_org": "o"},
                "project": {"alias": "P"},
                "github_topic": "t",
            }
        )
        await self._resolve(client)
        assert client.get.call_args[0][0] == "/api/v1/onboarding/resolve"

    @pytest.mark.asyncio
    async def test_no_github_account_is_explained_not_guessed(self):
        client = self._client(
            body={
                "org": {"alias": "hs"},
                "project": {"alias": "PF"},
                "github_topic": "pf",
            }
        )
        assert await self._resolve(client) is None

    @pytest.mark.asyncio
    async def test_an_api_failure_says_what_innoday_said(self):
        client = self._client(status=404, body={"detail": "no such project"})
        assert await self._resolve(client) is None


class TestTheCommandIsCalledBlastoff:
    def test_blastoff_is_registered_with_release_and_hotfix_as_aliases(self):
        from src.cli.main import create_parser

        parser = create_parser()
        actions = [
            a
            for a in parser._actions
            if getattr(a, "choices", None) and "blastoff" in a.choices
        ]
        assert actions, "`innoday blastoff` is not registered"
        choices = actions[0].choices
        # The old names stay: `release` is what people have typed for months and
        # `hotfix` is the short form worth keeping on its own merits.
        assert "release" in choices and "hotfix" in choices

    def test_the_alias_lookup_flag_is_gone(self):
        """`-c` was a key into a file block. The project comes from the cwd."""
        from src.cli.main import create_parser

        parser = create_parser()
        sub = [
            a
            for a in parser._actions
            if getattr(a, "choices", None) and "blastoff" in a.choices
        ][0]
        flags = {
            opt
            for action in sub.choices["blastoff"]._actions
            for opt in action.option_strings
        }
        assert "-c" not in flags and "--topic" not in flags
        for expected in ("--hotfix", "--dry-run", "--yes", "--topics", "--commit"):
            assert expected in flags, expected


class TestTheStoreCarriesEveryTopic:
    """The store builds the OrgConfig blastoff reads, and must not drop topics.

    `TestReleaseProxyCLI` mocks the store out, so a mutation collapsing the list
    here survived it. This drives the real store.
    """

    def test_every_topic_reaches_the_org_config(self):
        api = _api_serving([{"version": "v1.2.0", "status": "released"}])
        store = InnoDayVersionStore(
            api_client=api,
            org_id="org-1",
            project_id="proj-1",
            github_org="havilandsoftware",
            topics=["pf", "pixelfuel"],
        )
        assert store.load_org_config("pf").topics == ["pf", "pixelfuel"]

    def test_a_comma_separated_string_still_works(self):
        """An older caller, or a hand-typed override."""
        api = _api_serving([{"version": "v1.2.0", "status": "released"}])
        store = InnoDayVersionStore(
            api_client=api,
            org_id="org-1",
            project_id="proj-1",
            github_org="o",
            topics="pf, pixelfuel",
        )
        assert store.load_org_config("pf").topics == ["pf", "pixelfuel"]
