"""which entity an artifact hangs on: exactly one anchor from the flags, project/experiment anchors named by slug."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer
from ....sdk.artifact.anchors import Anchor
from .. import ref_syntax as refs


#: Anchors whose ref has a slug spelling. Runs anchor by id or petname and are
#: resolved server-side; workspaces and the Shared folder have ids only.
_SLUG_ANCHORS = {
    Anchor.PROJECT: "project",
    Anchor.EXPERIMENT: "experiment",
    Anchor.WORKSPACE: "workspace",
}


def _anchor_id_for(client: Client, anchor: Anchor, anchor_id: str | None) -> str | None:
    """Let a project or experiment anchor be named by SLUG, not only by id.

    Every ``/v1/{kind}/{id}`` route types the path param as a UUID, so a slug
    reaches the server as a 422 about UUID parsing. That is survivable for a
    human who can look the id up once; it is not survivable for an agent filing a
    few thousand artifacts, which would have to thread a uuid through every
    command and only has to get it wrong once.

    Slugs are the handle people actually remember -- the same reason
    :func:`_project_id` exists for the project verbs. Experiments were left out
    of this originally, which made ``--project my-slug`` work and ``--experiment
    my-slug`` 422 on the same command line.

    ADDITIVE, never a new gate. An id passes straight through, and so does
    anything that does not resolve: this route already answers a bad anchor with
    a 422, and turning that into a local hard error would reject values that
    were previously fine (an id this caller cannot enumerate). The exact
    ``?slug=`` lookup is used rather than listing, so it is one request and
    correct past 200 rows.
    """
    kind = _SLUG_ANCHORS.get(anchor)
    if kind is None or not anchor_id:
        return anchor_id
    # verify=False: an `id:` ref does not need a round trip to confirm it exists
    # -- it IS the id, and returns without touching the network. That keeps the
    # agent path (thousands of artifacts) at one request for a slug, none for an id.
    #
    # This used to swallow every error and pass the raw ref through, on a
    # "never a gate" rationale that slug-default invalidates: the route types its
    # path param as a UUID, so passing a bare UUID through is not a no-op -- the
    # SERVER reads it as an id and files the upload against whichever project owns
    # it. That is the misresolution this whole grammar exists to end, so a failed
    # lookup is now an error instead of a silent redirect.
    if kind == "workspace":
        # Its own resolver: the listing is complete (unpaginated by contract), so
        # there is no server-side ?slug= to ask for and none is needed.
        return refs.resolve_workspace(client, anchor_id).id
    return refs.resolve(client, kind, anchor_id, verify=False).id


def _pick_anchor(
    *,
    run: str | None,
    project: str | None,
    experiment: str | None,
    workspace: str | None,
    shared: bool,
) -> tuple[Anchor, str | None]:
    """Resolve exactly one anchor from the flags, or fail loudly.

    An artifact hangs off exactly one thing (the DB CHECKs it), so two anchors is a
    mistake worth stopping for rather than silently picking a winner.
    """
    chosen = [
        (Anchor.PROJECT, project),
        (Anchor.EXPERIMENT, experiment),
        (Anchor.WORKSPACE, workspace),
    ]
    given = [(a, v) for a, v in chosen if v is not None]
    if shared:
        given.append((Anchor.SHARED, None))
    if run is not None:
        given.append((Anchor.RUN, run))
    if len(given) > 1:
        names = ", ".join(f"--{a.value}" if a is not Anchor.RUN else "RUN" for a, _ in given)
        raise typer.BadParameter(f"an artifact anchors to exactly one thing; got {names}")
    if not given:
        raise typer.BadParameter(
            "needs an anchor: a RUN argument, or --project/--experiment/--workspace/--shared"
        )
    return given[0]


class _AnchorFailure:
    """A cached anchor-resolution failure.

    Cached for the same reason a success is: a manifest naming one bad project
    slug on every row would otherwise pay one failing round trip per row -- the
    exact cost this command exists to remove, incurred on the error path where
    nobody is measuring it.
    """

    def __init__(self, message: str) -> None:
        self.message = message
