"""``pysae-ai-tools glab issue-close-release`` — close every ticket shipped in a release.

Reads the annotated **release tag** message via the GitLab API (the changelog
section the release pipeline wrote into it), extracts every referenced ticket —
the release project's own ``(#1234)`` **and** cross-project refs like
``(op#1722)`` — then closes each one and strips its workflow/board labels so it
leaves the kanban board.

Source of truth is the tag, not a working copy: one API call per project, no
clone. Dry-run by default; pass ``--apply`` to actually close.
"""

import json
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated

import typer

from ...common.glab.runner import glab_api, run_glab
from ...common.group import resolve_group
from ...common.project_config import resolve_project_path
from ...common.references.gitlab_labels import BoardLabel
from ..workflow_transition import _get_project_id
from .core import IssueRef, parse_issue_refs

# Every kanban board column label — removed wholesale on close so a shipped
# ticket no longer shows up in any board column.
_BOARD_LABELS_CSV: str = ",".join(str(b) for b in BoardLabel)


def _encode(project: str) -> str:
    """URL-encode a project path so ``pysae/op`` works as a GitLab ``:id``."""
    return project.replace("/", "%2F")


def _tag_message(project: str, tag: str) -> str | None:
    """Return the annotated tag's message (+ release notes) for ``tag``.

    ``None`` when the tag does not exist. The message holds the changelog
    section; the optional ``release.description`` is appended for robustness.
    """
    data = glab_api(f"projects/{_encode(project)}/repository/tags/{_encode(tag)}")
    if not isinstance(data, dict):
        return None
    parts = [str(data.get("message", "") or "")]
    release = data.get("release")
    if isinstance(release, dict):
        parts.append(str(release.get("description", "") or ""))
    return "\n".join(parts)


def _close_and_strip(project: str, iid: int) -> bool:
    """Close issue ``iid`` and remove every board column label in one PUT."""
    return run_glab(
        "api",
        "-X",
        "PUT",
        f"projects/{_encode(project)}/issues/{iid}",
        "-f",
        "state_event=close",
        "-f",
        f"remove_labels={_BOARD_LABELS_CSV}",
    ).ok


def _target_project(ref: IssueRef, own_project: str, group: str) -> str:
    """Project an issue ref lives in: its cross-project path, or the release's own.

    ``parse_issue_refs`` stays I/O-free, so it can only prefix the group: a ref to a
    project nested in a subgroup (``infra-cluster#129``) comes out as ``<group>/infra-cluster``,
    which does not exist. Resolving here is what makes those refs closable.
    """
    if ref.project_path is None:
        return own_project
    return resolve_project_path(ref.project_path, group)


def main(
    tag: Annotated[str, typer.Argument(help="Release tag whose referenced tickets are closed (e.g. v1.4.0).")],
    project: Annotated[
        str | None,
        typer.Option(
            "--project",
            help="Release project (path or id). Defaults to the current repo via detect_context.",
        ),
    ] = None,
    apply: Annotated[bool, typer.Option("--apply", help="Actually close (default: dry-run plan only).")] = False,
    workers: Annotated[int, typer.Option("--workers", help="Concurrent close calls.")] = 8,
) -> None:
    """Close every ticket referenced in a release tag and take it off the board.

    The tag message (written by the release pipeline) is the single source of
    truth: same-project ``(#1234)`` and cross-project ``(op#1722)`` refs are both
    closed. Cross-project refs are namespaced under the ``pysae`` group.
    """
    own_project = project or _get_project_id()
    if not own_project:
        print(json.dumps({"error": "could not resolve the release project (pass --project)"}))
        raise typer.Exit(1)

    message = _tag_message(own_project, tag)
    if message is None:
        print(json.dumps({"error": f"tag '{tag}' not found in project '{own_project}'"}))
        raise typer.Exit(1)

    # De-duplicate by (resolved project, iid) — a ticket referenced twice closes once.
    seen: set[tuple[str, int]] = set()
    tickets: list[dict[str, object]] = []
    group = resolve_group()
    for ref in parse_issue_refs(message, group):
        target = _target_project(ref, own_project, group)
        key = (target, ref.iid)
        if key in seen:
            continue
        seen.add(key)
        tickets.append(
            {
                "project": target,
                "iid": ref.iid,
                "scope": "cross" if ref.project_path is not None else "own",
                "action": "close+strip-board-labels",
            }
        )

    if apply and tickets:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            results = pool.map(
                lambda t: _close_and_strip(str(t["project"]), int(t["iid"])),
                tickets,
            )
            for ticket, ok in zip(tickets, results, strict=True):
                ticket["result"] = "closed" if ok else "error:close-failed"

    print(
        json.dumps(
            {
                "tag": tag,
                "project": own_project,
                "applied": apply,
                "tickets_found": len(tickets),
                "tickets": tickets,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    typer.run(main)
