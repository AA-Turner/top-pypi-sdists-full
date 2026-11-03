"""WorkspacesResource (client.workspaces, typed reads) and WorkspacesMixin, Client's methods:
workspaces, the computer workspace, access groups
(twins: app/projects/workspaces, app/accounts/access_groups)."""

from __future__ import annotations
import builtins
from collections.abc import Iterable
from ....generated.models import AccessGroupOut, BestPickOut, WorkspaceOut, WorkspaceWriters
from ..resource import Resource
import sys
import uuid

from ... import errors


def get_home_row(rows: Iterable[dict]) -> dict | None:
    """The caller's home workspace among listed `rows`, or None.

    The server marks it (`is_default`) only while the caller may still write it;
    `writable` also guards a stale mark from an older server."""
    return next(
        (r for r in rows if r.get("is_default") is True and r.get("writable") is not False),
        None,
    )


def _load_context_or_empty() -> dict:
    from probe.sdk.settings.settings import ConfigUnreadable, load_context

    try:
        return load_context()
    except ConfigUnreadable:
        return {}


def _get_pin_ref(context: dict) -> str | None:
    """This context's saved pin (an id, maybe `id:`-prefixed), or None."""
    anchor = context.get("workspace")
    ref = anchor.get("id") if isinstance(anchor, dict) else None
    return str(ref) if ref else None


class WorkspacesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- workspaces ---------------------------------------------------------
    def list_workspaces(self) -> list[dict]:
        """Every workspace in the team, as an unpaginated list in server order.

        The server sorts alphabetically, equally for every team member.
        """
        return self.transport.get("/v1/workspaces")

    def get_workspace(self, workspace_id: str) -> dict:
        return self.transport.get(f"/v1/workspaces/{workspace_id}")

    def computer_workspace_id(self) -> str | None:
        """The workspace this computer files new projects into, as an id, or None.

        From `Settings.workspace`: PROBE_WORKSPACE, else the context's pin (the
        setup wizard's choice; `probe workspace use` changes it). An id
        (bare or `id:<uuid>`) is used as is; anything else is a workspace SLUG
        and is looked up, so `PROBE_WORKSPACE=engineering` works. An unknown
        slug raises rather than falling through to the server's rule.
        """
        return self.workspace_id_for(self.settings.workspace)

    def workspace_id_for(self, ref: str | None) -> str | None:
        """A workspace ref -- an id (bare or `id:<uuid>`) or a slug (bare or
        `slug:<slug>`) -- as an id. Only a slug costs a request."""
        if not ref:
            return None
        if ref.startswith("slug:"):
            bare = ref[5:]
        else:
            bare = ref[3:] if ref.startswith("id:") else ref
            try:
                return str(uuid.UUID(bare))
            except ValueError:
                pass
        for row in self.list_workspaces():
            if row.get("slug") == bare:
                return str(row["id"])
        raise errors.ValidationError(
            f"workspace {bare!r} is not a workspace on this team: see `probe workspace list`"
        )

    def save_home_workspace(self, workspace_id: str) -> dict:
        """PUT /v1/workspaces/{id}/default: make it your home workspace on this team.

        Your home is per person: a computer with no workspace set falls back to it.
        This computer's workspace (`probe workspace use`) is separate and unchanged.
        Only a workspace you may write (`home_eligible`) can be a home (403 else).
        """
        return self.transport.put(f"/v1/workspaces/{workspace_id}/default", None)

    def _pin_home_workspace(self) -> str | None:
        """Pin the caller's home workspace on this computer; its id, or None when none.

        For a computer with no workspace set (no `workspace=`, PROBE_WORKSPACE or pin).
        Every time it is needed, not once: only `probe workspace use --clear` stops it
        (`is_workspace_cleared`, which honours the legacy flag too). Saves it as this
        context's pin -- what `probe workspace use` writes -- and says so on stderr; a
        job signed in as another account than the stored login uses it for itself only.
        None makes the caller raise `WorkspaceRequired`.
        """
        if self.settings.workspace:
            return None
        from probe.sdk.settings.settings import ConfigUnreadable, WorkspaceSource, is_workspace_cleared, save_context

        saved = _load_context_or_empty()
        if _get_pin_ref(saved) or is_workspace_cleared(saved):
            return self._adopt_pin(_get_pin_ref(saved))
        try:
            home = get_home_row(self.list_workspaces())
        except errors.RosError:
            return None
        if home is None:
            return None
        saved = _load_context_or_empty()  # again: a pick or clear made during the list wins
        if _get_pin_ref(saved) or is_workspace_cleared(saved):
            return self._adopt_pin(_get_pin_ref(saved))
        home_id, name = str(home["id"]), home.get("name")
        self.settings.workspace = home_id
        if not self._can_change_pin(saved):
            print(f"probe: filing into your home workspace {name!r}; this computer's workspace "
                  "belongs to the account signed in here", file=sys.stderr)
            return home_id
        try:
            save_context({"workspace": {"id": home_id, "project": None}})
        except (OSError, ConfigUnreadable):
            pass  # a read-only or unreadable config still gets this one request filed
        self.settings.workspace_source = WorkspaceSource.PIN
        print(f"probe: this computer's work now goes into your home workspace {name!r} "
              "(change it with `probe workspace use <slug>`)", file=sys.stderr)
        return home_id

    def _adopt_pin(self, ref: str | None) -> str | None:
        """Use this computer's pin, set since this process read its settings (another shell's
        pick wins over the home); None when the context was cleared instead."""
        from probe.sdk.settings.settings import WorkspaceSource

        if not ref:
            return None
        self.settings.workspace, self.settings.workspace_source = ref, WorkspaceSource.PIN
        return self.workspace_id_for(ref)

    def _can_change_pin(self, context: dict) -> bool:
        """Whether this client may change this computer's pin: the context stores no login,
        or this client signs in with it. A job of another account on a shared box
        (`PROBE_TOKEN`) never moves the stored login's pin."""
        from probe.sdk.settings.settings import TOKEN_KEY

        stored = context.get(TOKEN_KEY)
        return not stored or stored == self.settings.token

    def _drop_dead_pin(self, workspace_id: str) -> bool:
        """Forget this computer's pin naming `workspace_id`, which the server no longer has;
        whether the create may go again through the home rule. Only a pin of this client's
        own login (`WorkspaceSource.PIN`), never `workspace=`, PROBE_WORKSPACE or a limit."""
        from probe.sdk.settings.settings import (
            WORKSPACE_CLEAR_RESET,
            ConfigUnreadable,
            WorkspaceSource,
            save_context,
        )
        from probe.sdk.settings.workspace_limit import LIMIT_KEY

        if self.settings.workspace_source is not WorkspaceSource.PIN or self.settings.workspace_limit is not None:
            return False
        saved = _load_context_or_empty()
        anchor = saved.get("workspace")
        if not self._can_change_pin(saved) or (isinstance(anchor, dict) and anchor.get(LIMIT_KEY) is True):
            return False  # another account's pin, or a limit's (`probe workspace limit` changes it)
        ref = _get_pin_ref(saved) or ""
        if (ref[3:] if ref.startswith("id:") else ref) == workspace_id:
            try:
                # The pin was the latest choice, so an older clear goes with it.
                save_context({"workspace": None, **WORKSPACE_CLEAR_RESET})
            except (OSError, ConfigUnreadable):
                return False
        # Else a sibling process (a sweep's other runs) already moved it on: the home rule adopts that.
        self.settings.workspace = self.settings.workspace_source = None
        return True

    def create_workspace(self, slug: str, name: str | None = None) -> dict:
        """POST /v1/workspaces — a workspace any team member may use or rename.

        Pass ``workspace_id`` to :meth:`create_project`, or select it in the CLI
        with ``probe workspace use <slug>``. Without a workspace, the server uses
        this computer's workspace (``probe workspace use``, ``PROBE_WORKSPACE``);
        with none set, the server files into the team's only workspace, and when
        there are several the client pins your home workspace (``WorkspaceRequired``
        when you have none). The first workspace you create becomes your home.

        A taken slug is a 409 carrying the existing id and a free suggestion, never a
        silent hand-back of somebody else's row.
        """
        body: dict = {"slug": slug}
        if name is not None:
            body["name"] = name
        return self.transport.post("/v1/workspaces", body)

    def rename_workspace(self, workspace_id: str, name: str) -> dict:
        """PATCH /v1/workspaces/{id}. Any team member may rename any workspace.

        ``name`` is the only editable field; the slug stays unchanged.
        """
        return self.transport.patch(f"/v1/workspaces/{workspace_id}", {"name": name})

    def delete_workspace(self, workspace_id: str) -> None:
        """DELETE /v1/workspaces/{id}. Any workspace, only while empty.

        Projects, files, or an integration targeting it cause a 409. Move work out
        and disconnect integrations first. If none remain, the next write without
        a workspace creates a Default workspace.
        """
        self.transport.delete(f"/v1/workspaces/{workspace_id}")

    # -- write permissions (0214) -------------------------------------------
    #
    # THE INTERIM ADMIN SURFACE. The dashboard half of this feature ships in a
    # later change, so until then these methods (and the `probe access-group` /
    # `probe workspace writers` commands over them) are the only way to say who
    # may edit a workspace. Every mutation is owner/admin-only server-side.
    #
    # None of this touches READS: a restricted workspace stays fully visible to
    # every team member, which is the product decision, not an omission.

    def list_access_groups(self) -> list[dict]:
        """Every named group in the team, with its member user ids.

        Names and emails come from the team roster, not from here -- a group
        stores ids so a rename or an email change cannot strand a grant.
        """
        return self.transport.get("/v1/access-groups")

    def create_access_group(self, name: str) -> dict:
        """POST /v1/access-groups. The slug is derived from the name.

        NOT `groups`: that word already means a RUN group (a sweep) everywhere
        else in this client.
        """
        return self.transport.post("/v1/access-groups", {"name": name})

    def rename_access_group(self, group_id: str, name: str) -> dict:
        return self.transport.patch(f"/v1/access-groups/{group_id}", {"name": name})

    def delete_access_group(self, group_id: str) -> None:
        """Deleting a group drops it from every writer list it guards.

        That can only NARROW access: a restricted workspace left with no writers
        is writable by nobody, never by everybody.
        """
        self.transport.delete(f"/v1/access-groups/{group_id}")

    def add_access_group_member(self, group_id: str, user_id: str) -> None:
        """Idempotent. A user may belong to several groups."""
        self.transport.put(f"/v1/access-groups/{group_id}/members/{user_id}", None)

    def remove_access_group_member(self, group_id: str, user_id: str) -> None:
        """Idempotent."""
        self.transport.delete(f"/v1/access-groups/{group_id}/members/{user_id}")

    def get_workspace_writers(self, workspace_id: str) -> dict:
        """`{mode, users, groups}` — who may EDIT this workspace.

        Readable by every member: a permission nobody can see is a save that
        mysteriously fails.
        """
        return self.transport.get(f"/v1/workspaces/{workspace_id}/writers")

    def set_workspace_writers(
        self,
        workspace_id: str,
        *,
        mode: str,
        users: list[str] | None = None,
        groups: list[str] | None = None,
    ) -> dict:
        """Replace the WHOLE write state (mode + both lists) in one call.

        Whole-state rather than add/remove because "restrict this to the lab" as
        three requests can interleave with another admin's three and commit a
        state neither asked for. The server takes a row lock for the same reason.

        `mode='open'` restores the default: every team member may edit.
        """
        return self.transport.put(
            f"/v1/workspaces/{workspace_id}/writers",
            {"mode": mode, "users": users or [], "groups": groups or []},
        )


class WorkspacesResource(Resource):
    """`client.workspaces`: typed workspace, access-group and best-pick reads."""

    __slots__ = ()

    def get(self, workspace_id: str) -> WorkspaceOut:
        """`Client.get_workspace` as a `WorkspaceOut`."""
        return self._to_model(WorkspaceOut, self._client.get_workspace(workspace_id))

    def list(self) -> builtins.list[WorkspaceOut]:
        """`Client.list_workspaces` as `WorkspaceOut`s."""
        return self._to_models(WorkspaceOut, self._client.list_workspaces())

    def list_access_groups(self) -> builtins.list[AccessGroupOut]:
        """`Client.list_access_groups` as `AccessGroupOut`s."""
        return self._to_models(AccessGroupOut, self._client.list_access_groups())

    def get_writers(self, workspace_id: str) -> WorkspaceWriters:
        """`Client.get_workspace_writers` as a `WorkspaceWriters`."""
        return self._to_model(WorkspaceWriters, self._client.get_workspace_writers(workspace_id))

    def get_best(self, workspace_id: str, *, history: int | None = None) -> BestPickOut:
        """`Client.get_workspace_best` as a `BestPickOut`."""
        return self._to_model(
            BestPickOut,
            self._client.get_workspace_best(workspace_id, history=history),
        )
