"""Shared context options for the ``ci run`` CLI commands.

The six ``ci run`` commands all accept the same five context options
(``--project-id`` / ``--project-url`` / ``--pipeline-id`` / ``--mr-iid`` /
``--branch``). Their Typer definitions live here as reusable ``Annotated``
aliases and are collected into :class:`ContextOptions`, so a change to any
option — or the logic that turns them into a :class:`PipelineContext` — is
made in exactly one place instead of being copied across every command.
"""

import sys
from dataclasses import dataclass
from typing import Annotated

import typer

from ...internal.detect_context.detect import Context, DetectArgs, detect
from .gitlab_api import PipelineContext

ProjectIdOption = Annotated[str, typer.Option("--project-id", help="GitLab project ID")]
ProjectUrlOption = Annotated[str, typer.Option("--project-url", help="GitLab project URL")]
PipelineIdOption = Annotated[str, typer.Option("--pipeline-id", help="Pipeline ID")]
MrIidOption = Annotated[str, typer.Option("--mr-iid", help="MR IID")]
BranchOption = Annotated[str, typer.Option("--branch", help="Branch name")]


@dataclass
class ContextOptions:
    """The five context options shared by every ``ci run`` command."""

    project_id: str = ""
    project_url: str = ""
    pipeline_id: str = ""
    mr_iid: str = ""
    branch: str = ""


def _has_ref(ctx: PipelineContext) -> bool:
    """Whether ``ctx`` already names something a pipeline can be found from."""
    return bool(ctx.pipeline_id or ctx.mr_iid or ctx.source_branch)


def _inherit(ctx: PipelineContext, detected: Context) -> None:
    """Complete ``ctx`` from the detected context, in place.

    The branch falls back to the checked-out one (``git_branch``): outside a
    merge request — on ``main``, or on a branch whose MR is merged or not
    opened yet — ``mr_source_branch`` is empty, and taking it as the only
    source of the branch left every command with nothing to resolve.

    Refs are inherited from the local repo only when they belong to the target
    project. A caller naming another project gets the project fields alone:
    an MR IID or branch from here would resolve a pipeline that has nothing to
    do with it.
    """
    other_project = bool(ctx.project_id) and ctx.project_id != detected.project_id
    ctx.project_id = ctx.project_id or detected.project_id
    ctx.project_url = ctx.project_url or detected.project_url
    if other_project:
        return
    ctx.pipeline_id = ctx.pipeline_id or detected.pipeline_id
    ctx.mr_iid = ctx.mr_iid or detected.mr_iid
    ctx.source_branch = ctx.source_branch or detected.mr_source_branch or detected.git_branch
    ctx.sha = ctx.sha or detected.git_sha


def build_context(opts: ContextOptions) -> PipelineContext:
    """Build a :class:`PipelineContext` from CLI options, falling back to detect_context."""
    ctx = PipelineContext(
        project_id=opts.project_id,
        project_url=opts.project_url,
        pipeline_id=opts.pipeline_id,
        mr_iid=opts.mr_iid,
        source_branch=opts.branch,
    )

    if not ctx.project_id or not _has_ref(ctx):
        try:
            detect_args = DetectArgs(
                mr_iid=ctx.mr_iid,
                pipeline_id=ctx.pipeline_id,
            )
            _inherit(ctx, detect(detect_args))
        except Exception as exc:
            print(f"Warning: detect_context failed: {exc}", file=sys.stderr)

    if not ctx.project_id:
        print("ERROR: impossible de detecter le project_id. Utilise --project-id.", file=sys.stderr)
        raise typer.Exit(code=1)

    return ctx
