"""the destination scope a store belongs to (workspace, project, account)."""

from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib
import json
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class Scope:
    backend: str
    customer_id: str
    workspace_id: str
    project_id: str | None = None

    @property
    def key(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()[:24]

    @classmethod
    def resolve(
        cls, client, project: str | None = None, *, workspace_id: str | None = None,
    ) -> Scope:
        """Authenticate and resolve IDs before any completion or resume shortcut.

        A saved job supplies its approved workspace explicitly so a later default
        selection or CLI context change cannot redirect an import already queued.
        """
        from ....commands.ref_syntax import resolve

        identity = client.me()
        tenant = identity.get("customer_id")
        parsed = urlsplit(client.settings.base_url)
        if not tenant or not parsed.hostname or parsed.username or parsed.password:
            raise CoverageError("Cannot establish an authenticated backend and tenant.")
        backend = urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                               parsed.path.rstrip("/"), "", ""))
        selected = None
        if project:
            selected = client.get_project(resolve(client, "project", project).id)
            if selected.get("customer_id") != tenant:
                raise CoverageError("The selected project is outside the authenticated tenant.")
            if not selected.get("workspace_id"):
                raise CoverageError("The selected project has no verified workspace.")
            if workspace_id and str(selected["workspace_id"]) != str(workspace_id):
                raise CoverageError("The selected project moved from this import's approved workspace.")
        workspace = (
            selected["workspace_id"] if selected
            else workspace_id or client.settings.workspace
        )
        if workspace:
            row = client.get_workspace(str(workspace))
            if row.get("customer_id") != tenant:
                raise CoverageError("The selected workspace is outside the authenticated tenant.")
        else:
            workspace = _default_workspace(client.list_workspaces(), identity)["id"]
        return cls(backend, str(tenant), str(workspace),
                   str(selected["id"]) if selected else None)


def _default_workspace(rows: list[dict], identity: dict) -> dict:
    """The import's workspace when neither the import nor this computer names one.

    Only a team's ONLY workspace is chosen for it: with several, the folder
    import stops and says how to pick this computer's (the setup wizard asks;
    `probe workspace use` changes it) -- the same rule the server applies to an
    unaddressed project create, and for the same reason: a guess (the oldest,
    the newest one you made) filed work under the wrong person.
    """
    candidates = [row for row in rows
                  if row.get("customer_id") == identity["customer_id"] and row.get("id")]
    if not candidates:
        raise CoverageError(
            "No workspace is available for this account. "
            "Create a workspace in the dashboard, then retry the folder import."
        )
    if len(candidates) == 1:
        return candidates[0]
    raise CoverageError(
        "This team has several workspaces and this computer has none set. "
        "Pick one with `probe workspace use <slug>` (see `probe workspace list`), then retry."
    )
from probe.cli.imports.folder.coverage.coverage import CoverageError  # noqa: E402 -- pieces need each other; the front door loads this one first
