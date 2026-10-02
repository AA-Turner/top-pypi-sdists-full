"""Folder imports resolve shared workspaces and keep queued destinations pinned."""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from probe.cli.backfill_coverage import CoverageError, Scope
from probe.sdk.errors import NotFoundError


def workspace(ident, *, creator=None, created="2026-09-01T00:00:00Z", **fields):
    return {
        "id": ident, "customer_id": "tenant", "kind": "team",
        "owner_user_id": None, "created_by": creator, "created_at": created,
        **fields,
    }


class Client:
    def __init__(self, *rows, selected=None, user_id="me"):
        self.rows = list(rows)
        self.settings = SimpleNamespace(base_url="https://probe.test", workspace=selected)
        self.identity = {"customer_id": "tenant", "user_id": user_id}
        self.projects = {}

    def me(self):
        return self.identity

    def list_workspaces(self):
        return list(self.rows)

    def get_workspace(self, ident):
        return next((row for row in self.rows if row["id"] == ident), None) or self._missing()

    def get_project(self, ident):
        return self.projects[ident]

    @staticmethod
    def _missing():
        raise NotFoundError("workspace not found")


def test_single_shared_workspace_works_without_personal_metadata():
    client = Client(workspace("only", creator="user:teammate"))
    assert Scope.resolve(client).workspace_id == "only"
    assert client.settings.workspace is None, "the default must not overwrite CLI context"


def test_multiple_workspaces_use_newest_recorded_creator_not_order_kind_or_owner():
    client = Client(
        workspace("z-new-mine", creator="user:me", created="2026-09-11T00:00:00Z"),
        workspace("a-old-mine", creator="user:me", created="2026-09-01T00:00:00Z"),
        workspace("other", creator="user:teammate", created="2026-09-12T00:00:00Z"),
        workspace("legacy", kind="personal", owner_user_id="me",
                  created="2026-09-13T00:00:00Z"),
    )
    assert Scope.resolve(client).workspace_id == "z-new-mine"
    client.rows.reverse()
    assert Scope.resolve(client).workspace_id == "z-new-mine"


def test_creation_dates_compare_instants_and_break_ties_by_id():
    client = Client(
        workspace("looks-later", creator="user:me", created="2026-09-12T12:00:00+08:00"),
        workspace("a", creator="user:me", created="2026-09-12T05:00:00Z"),
        workspace("z", creator="user:me", created=datetime(2026, 9, 12, 5, tzinfo=timezone.utc)),
    )
    assert Scope.resolve(client).workspace_id == "z"


@pytest.mark.parametrize("user_id", ["me", None])
def test_no_recorded_creator_uses_server_oldest_default(user_id):
    client = Client(
        workspace("new", creator="user:None", created="2026-09-12T00:00:00Z"),
        workspace("old", creator="user:teammate", created="2026-09-01T00:00:00Z"),
        workspace("legacy", kind="personal", owner_user_id="me",
                  created="2026-09-13T00:00:00Z"),
        user_id=user_id,
    )
    assert Scope.resolve(client).workspace_id == "old"


def test_fallback_never_selects_another_tenant():
    client = Client(
        workspace("mine"),
        workspace("foreign", customer_id="other", creator="user:me",
                  created="2026-09-13T00:00:00Z"),
    )
    assert Scope.resolve(client).workspace_id == "mine"


@pytest.mark.parametrize("rows", [[], [workspace("foreign", customer_id="other")]])
def test_missing_workspace_has_actionable_local_destination_error(rows):
    with pytest.raises(CoverageError, match="No workspace.*Create a workspace"):
        Scope.resolve(Client(*rows))


def test_invalid_creation_date_requires_explicit_destination():
    client = Client(workspace("one", created="not-a-date"), workspace("two"))
    with pytest.raises(CoverageError, match="creation date.*Select a workspace"):
        Scope.resolve(client)


def test_explicit_workspace_remains_authoritative():
    client = Client(
        workspace("selected"),
        workspace("new", creator="user:me", created="2026-09-12T00:00:00Z"),
        selected="selected",
    )
    assert Scope.resolve(client).workspace_id == "selected"


def test_deleted_explicit_workspace_is_not_silently_replaced():
    with pytest.raises(NotFoundError, match="workspace not found"):
        Scope.resolve(Client(workspace("other"), selected="deleted"))


def test_explicit_workspace_is_validated_in_tenant():
    client = Client(workspace("foreign", customer_id="other"), selected="foreign")
    with pytest.raises(CoverageError, match="outside the authenticated tenant"):
        Scope.resolve(client)


def test_saved_workspace_survives_new_workspaces_and_context_changes():
    client = Client(workspace("first", creator="user:me"))
    approved = Scope.resolve(client)
    client.rows.append(workspace("second", creator="user:me", created="2026-09-12T00:00:00Z"))
    assert Scope.resolve(client).workspace_id == "second"
    client.settings.workspace = "second"
    assert Scope.resolve(client, workspace_id=approved.workspace_id) == approved


def test_saved_workspace_is_still_validated_in_tenant():
    client = Client(workspace("foreign", customer_id="other"), workspace("current"))
    with pytest.raises(CoverageError, match="outside the authenticated tenant"):
        Scope.resolve(client, workspace_id="foreign")


def test_explicit_project_wins_over_configured_and_default_workspace():
    client = Client(workspace("project-workspace"), workspace("configured"), selected="configured")
    client.projects["p"] = {"id": "p", "customer_id": "tenant", "workspace_id": "project-workspace"}
    assert Scope.resolve(client, "id:p") == Scope("https://probe.test", "tenant", "project-workspace", "p")


def test_project_moving_after_approval_requires_new_approval():
    client = Client(workspace("old"), workspace("new"))
    client.projects["p"] = {"id": "p", "customer_id": "tenant", "workspace_id": "new"}
    with pytest.raises(CoverageError, match="project moved"):
        Scope.resolve(client, "id:p", workspace_id="old")


def test_project_pin_uses_the_approved_workspace_even_when_context_changes():
    client = Client(workspace("approved"), workspace("configured"), selected="configured")
    client.projects["p"] = {"id": "p", "customer_id": "tenant", "workspace_id": "approved"}
    assert Scope.resolve(client, "id:p", workspace_id="approved").workspace_id == "approved"


def test_foreign_project_cannot_reuse_an_in_tenant_workspace():
    client = Client(workspace("current"))
    client.projects["p"] = {"id": "p", "customer_id": "other", "workspace_id": "current"}
    with pytest.raises(CoverageError, match="selected project is outside"):
        Scope.resolve(client, "id:p")
