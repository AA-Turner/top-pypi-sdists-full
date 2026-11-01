"""WorkspacesResource (client.workspaces, typed reads) and WorkspacesMixin, Client's methods:
workspaces, the computer workspace, access groups (twins: app/workspaces, app/access_groups)."""

from __future__ import annotations
import builtins
from ....generated.models import AccessGroupOut, BestPickOut, WorkspaceOut, WorkspaceWriters
from ..resource import Resource
import sys
import uuid

from ... import errors


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

    def _hand_over_workspace(self) -> str | None:
        """Pin the caller's legacy saved default (0354) on this computer, once.

        Only for a computer with no workspace set, and only when the server still
        marks one of the caller's workspaces `is_default` that they may write.
        Saves it as this context's pin -- what `probe workspace use` writes --
        and says so on stderr. Once per computer: the context remembers it ran
        (`config.WORKSPACE_HANDOVER`, also set by `probe workspace use --clear`,
        so an explicit clear is never undone). Returns the id, or None when there
        is nothing to hand over (the caller then raises `WorkspaceRequired`).
        """
        if self.settings.workspace:
            return None
        from probe.sdk.settings.settings import WORKSPACE_HANDOVER, ConfigUnreadable, load_context, save_context

        try:
            saved = load_context()
        except ConfigUnreadable:
            saved = {}
        pinned = (saved.get("workspace") or {}).get("id") if isinstance(saved.get("workspace"), dict) else None
        if pinned:
            # Set since this process read its settings (the setup wizard, `probe
            # workspace use` in another shell): that choice wins over the legacy one.
            self.settings.workspace = str(pinned)
            return self.workspace_id_for(str(pinned))
        if saved.get(WORKSPACE_HANDOVER):
            return None
        try:
            mine = next(
                (
                    w for w in self.list_workspaces()
                    if w.get("is_default") is True and w.get("writable") is not False
                ),
                None,
            )
        except errors.RosError:
            return None
        if mine is None:
            return None
        try:
            save_context(
                {"workspace": {"id": str(mine["id"]), "project": None}, WORKSPACE_HANDOVER: True}
            )
        except (OSError, ConfigUnreadable):
            pass  # a read-only or unreadable config still gets this one request filed
        self.settings.workspace = str(mine["id"])
        print(
            f"probe: this computer's work now goes into {mine.get('name')!r} "
            "(change it with `probe workspace use <slug>`)",
            file=sys.stderr,
        )
        return str(mine["id"])

    def create_workspace(self, slug: str, name: str | None = None) -> dict:
        """POST /v1/workspaces — a workspace any team member may use or rename.

        Pass ``workspace_id`` to :meth:`create_project`, or select it in the CLI
        with ``probe workspace use <slug>``. Without a workspace, the server uses
        this computer's workspace (``probe workspace use``, ``PROBE_WORKSPACE``);
        with none set, the server files into the team's only workspace and
        refuses (``WorkspaceRequired``) when there are several.

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
