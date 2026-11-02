"""name an entity on the command line and resolve it: slug and run ref arguments, workspace/project/container ids through the shared reads, and the ref-shape check before a write is queued."""

from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ...sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer
from ...sdk.settings.settings import resolve
from . import ref_syntax as refs
from ...shared.reads import reads


#: Characters that mean a run ref was never going to resolve, whatever the
#: server thinks. Kept deliberately tiny.
_IMPOSSIBLE_IN_A_REF = frozenset({"/", "\\", " ", "\t", "\n"})


def _check_ref_shape(ref: str) -> None:
    """Fail a ref that CANNOT be valid, before it is queued.

    Queued writes exit 0 -- the op is on disk, and whether the server accepts it
    is not known for minutes. That is the intended trade, but it turns a typo
    from an instant non-zero exit into a dead letter nobody is watching. This
    buys back the obvious half of that for free: no network, no round trip, just
    the shapes a run ref can never have.

    Deliberately NOT a slug or UUID validator. Run refs are ids OR server-minted
    petnames (refs.py:49), the petname grammar belongs to the server, and a
    client-side guess at it would reject valid refs the day the server widens it
    -- a much worse failure than the one this prevents. Anything that could
    plausibly resolve is passed straight through.
    """
    if not ref or not ref.strip():
        raise typer.BadParameter("run ref is empty")
    if ref.startswith("-"):
        # The classic: an option typo'd or mis-ordered so the flag itself landed
        # on the positional. Queued, this becomes a 422 minutes later.
        raise typer.BadParameter(
            f"{ref!r} looks like an option, not a run ref — check the argument order"
        )
    if "=" in ref:
        # The run argument is missing, so the first key=value took its place:
        # `probe log $RUN loss=0.5 acc=0.9` with $RUN empty, which the shell
        # drops from the command line. Bucket, 2026-10-27: queued, it was a 404
        # and a dead letter. No run ref has an `=`: uuids have none and the
        # server refuses one in a run slug (`RunSlug`, app/core/slugs.py).
        raise typer.BadParameter(
            f"{ref!r} looks like key=value, not a run ref — the run argument is "
            "missing (is the variable holding the run ref empty?)"
        )
    if any(character in _IMPOSSIBLE_IN_A_REF for character in ref):
        raise typer.BadParameter(
            f"{ref!r} is not a run ref (it contains a path separator or whitespace)"
        )


def _api(client: Any, *, pretty: bool = False) -> "reads.Api":
    """This command's Probe for the shared read bodies (`probe.shared.reads.reads`): its
    client, this process's environment and settings. `pretty`: JSON laid out for
    a terminal (a command that prints passes `sys.stdout.isatty()`)."""
    return reads.Api(
        client=client,
        resolve=resolve,
        env=os.environ,
        pretty=pretty,
        base_url=_conn.base_url,
        # Late-bound: the active project as this module resolves it (a test may stand one in).
        ambient_project=lambda explicit, **kw: _ambient_project(explicit, **kw),
    )


def _resolve_workspace(client: Client | None, explicit: str | None) -> str | None:
    """Explicit flag -> PROBE_WORKSPACE -> context, resolved to an id.

    Same provenance rule as :func:`_ambient_project`: an EXPLICIT ref is typed by
    a person, so a bare one is a slug; the ambient value was written by
    ``workspace use`` and is an id. Getting that backwards is how an explicit
    ``--workspace <something>`` would silently address a different workspace.

    ``client`` may be None where the caller has none open and only needs the
    ambient value passed through untouched.
    """
    merged = resolve(workspace=explicit).workspace
    if explicit is None:
        # Ambient: `workspace use` stores the id; PROBE_WORKSPACE may be an id or
        # a slug -- the same rule the SDK applies (`Client.workspace_id_for`).
        if client is not None:
            return client.workspace_id_for(merged)
        return _bare_id(merged)
    if client is None:  # pragma: no cover - every caller with an explicit ref has one
        return explicit
    return _ref(client, "workspace", explicit).id


def _bare_id(ref: str | None) -> str | None:
    """Strip an `id:` prefix for the API, which takes the uuid itself."""
    if ref is None:
        return None
    bare, _ = refs.split_selector(ref)
    return bare


def _ref(client: Client, kind: str, ref: str) -> refs.Ref:
    """Resolve a ref, reporting both failure modes as CLI errors
    (`reads.resolve_ref`, with this process's active project and limit)."""
    return _api(client).ref(kind, ref)


#: The project a resolved experiment ref is filed under (`reads.filed_under`).
_filed_under = reads.filed_under


def _ambient_project(explicit: str | None, **kw) -> str | None:
    """The project ref to use, canonicalising ONLY the ambient one
    (`reads.ambient_project`, through this process's settings)."""
    return reads.ambient_project(resolve, explicit, **kw)


def _project_id(client: Client, ref: str) -> str:
    """A project SLUG (or ``id:<uuid>``) -> the id every route wants.

    Every ``/v1/projects/{project_id}`` route types the path param as a UUID, so a
    slug reaches the server as a 422 about UUID parsing rather than a lookup, and
    the translation has to happen client-side. Slugs are the handle people
    actually remember, so they are what a bare ref means -- see
    :mod:`probe.cli.commands.ref_syntax` for why that is a rule and not a preference.
    """
    return _ref(client, "project", ref).id


def _project_slug(client: Client, ref: str | None) -> str | None:
    """The inverse of :func:`_project_id`, for the slug-resolving paths (`reads.project_slug`)."""
    return reads.project_slug(_api(client), ref)

#: Runs read either way on purpose -- see refs.resolve_run.
RUN_REF_HELP = "run slug or id (they cannot collide)"


def slug_ref(kind: str) -> Any:
    """The positional ref for a slug-addressed kind (project, experiment)."""
    return typer.Argument(..., help=f"{kind} slug (or id:<uuid>)")


def run_ref() -> Any:
    return typer.Argument(..., help=RUN_REF_HELP)
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
