"""Renaming a project has to change the project.

`ProjectUpdate.alias` existed on the API model, the route passed it through, and
`ProjectService.update_project` dropped it on an `allowed_fields` list that did
not name it. The request was accepted, answered **200**, and changed nothing.

The CLI then printed `update_data` -- what it had *asked for* -- so the discarded
field was reported back as applied. Two layers agreeing to say yes.

**The test that missed it asserted the CLI sends `alias`.** It does, and always
did; that was never the broken half. A check that stops at the boundary it shares
an assumption with cannot see past it, so everything here drives the real route
and reads the row afterwards.
"""

from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.project import Project


def _project(db_engine, org, alias="OLD", name="Renameable"):
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=alias,
            name=name,
            description="d",
        )
        session.add(project)
        session.commit()
        return project.id


def _alias_of(db_engine, project_id):
    with Session(db_engine) as session:
        return session.get(Project, project_id).alias


class TestTheAliasReachesTheRow:
    def test_renaming_actually_renames(self, client, org, auth_headers, db_engine):
        project_id = _project(db_engine, org)

        response = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"alias": "NEW"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json()["alias"] == "NEW"
        assert _alias_of(db_engine, project_id) == "NEW", (
            "the API answered 200 and the row is unchanged -- the exact failure "
            "this module exists for"
        )

    def test_the_response_reports_the_new_alias(
        self, client, org, auth_headers, db_engine
    ):
        """The CLI prints the response now, so a wrong response is a wrong
        message to the person."""
        project_id = _project(db_engine, org, alias="BEFORE")

        body = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"alias": "AFTER"},
            headers=auth_headers,
        ).json()

        assert body["alias"] == "AFTER"

    def test_it_is_normalised_the_same_way_creation_normalises(
        self, client, org, auth_headers, db_engine
    ):
        """An alias reached by rename must be as valid as one reached by create.
        Uppercasing is the stored convention; the lowercased form is what becomes
        the GitHub discovery topic."""
        project_id = _project(db_engine, org)

        client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"alias": "  blast  "},
            headers=auth_headers,
        )

        assert _alias_of(db_engine, project_id) == "BLAST"

    def test_an_alias_already_taken_is_refused(
        self, client, org, auth_headers, db_engine
    ):
        """Two projects in one org cannot share an alias -- it is the ticket
        prefix and the discovery topic, so a collision is two projects claiming
        the same repositories."""
        _project(db_engine, org, alias="TAKEN", name="First")
        project_id = _project(db_engine, org, alias="MINE", name="Second")

        response = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"alias": "TAKEN"},
            headers=auth_headers,
        )

        assert response.status_code >= 400
        assert _alias_of(db_engine, project_id) == "MINE"

    def test_renaming_to_its_own_alias_is_not_a_collision(
        self, client, org, auth_headers, db_engine
    ):
        """A no-op rename, or one that only changes case, must not trip the
        uniqueness check against the project itself."""
        project_id = _project(db_engine, org, alias="SAME")

        response = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"alias": "SAME", "name": "Renamed"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert _alias_of(db_engine, project_id) == "SAME"

    def test_other_fields_still_update(self, client, org, auth_headers, db_engine):
        """The allowed-fields list is what was edited; the rest must be intact."""
        project_id = _project(db_engine, org)

        client.put(
            f"/api/v1/organizations/{org.id}/projects/{project_id}",
            json={"name": "Renamed", "description": "new"},
            headers=auth_headers,
        )

        with Session(db_engine) as session:
            project = session.get(Project, project_id)
            assert (project.name, project.description) == ("Renamed", "new")


class TestNormalisingIsNotIgnoring:
    """The warning must fire on a dropped field and stay quiet on a tidied one.

    Built comparing the two values exactly, and the first real rename showed why
    that is wrong: asking for `blast` and being told `BLAST` is the API doing its
    job, not disregarding the request. A warning that fires every time trains
    people to scroll past it, and the case it exists for goes past with it.
    """

    from src.cli.commands.projects import _server_ignored as _ignored

    @pytest.mark.parametrize(
        "requested,actual",
        [
            ("blast", "BLAST"),  # uppercased, as every alias is
            ("  blast  ", "BLAST"),  # and stripped
            ("BLAST", "BLAST"),  # unchanged
        ],
    )
    def test_a_normalised_value_is_not_a_complaint(self, requested, actual):
        assert not TestNormalisingIsNotIgnoring._ignored(requested, actual)

    @pytest.mark.parametrize(
        "requested,actual",
        [
            ("blast", "BLASTOFF"),  # the real bug: the rename was dropped
            ("Renamed", "Original"),
            ("blast", None),
        ],
    )
    def test_a_disregarded_value_is(self, requested, actual):
        assert TestNormalisingIsNotIgnoring._ignored(requested, actual)

    def test_non_strings_compare_exactly(self):
        """Only strings get case and whitespace forgiveness; a status or a tag
        list that came back different really is different."""
        assert TestNormalisingIsNotIgnoring._ignored(["a"], ["b"])
        assert not TestNormalisingIsNotIgnoring._ignored(["a"], ["a"])


class TestTheCliReportsWhatHappened:
    """Printing the request back is how a silently-dropped field looks applied."""

    @pytest.mark.asyncio
    async def test_a_dropped_field_is_called_out(self):
        import argparse
        from unittest.mock import AsyncMock, MagicMock, patch

        from src.cli.commands.projects import ProjectCommands

        config = MagicMock()
        config.get_current_organization.return_value = "hs"
        config.get_organization_id.return_value = "org-1"
        config.get_current_project_id.return_value = "proj-1"

        response = MagicMock()
        response.status_code = 200
        # The server kept the old alias -- exactly what used to happen.
        response.json.return_value = {"name": "P", "alias": "OLD"}

        client = MagicMock()
        client.put = AsyncMock(return_value=response)
        client.close = AsyncMock()

        printed = []
        args = argparse.Namespace(
            project_id="P",
            name=None,
            alias="NEW",
            description=None,
            goals=None,
            scope_limitations=None,
            priority=None,
            status=None,
            tags=None,
        )

        with (
            patch("src.cli.commands.projects.InnoDayAPIClient", return_value=client),
            patch(
                "src.cli.commands.projects.console.print",
                side_effect=lambda *a, **k: printed.append(str(a[0]) if a else ""),
            ),
        ):
            await ProjectCommands._handle_update(args, config)

        said = " ".join(printed)
        assert "OLD" in said, "the server's answer must be shown"
        assert "asked for" in said, (
            "a field the server did not apply must be called out, not printed "
            "back as though it had been"
        )
