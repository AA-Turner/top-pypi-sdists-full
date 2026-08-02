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

from ...internal.detect_context.detect import DetectArgs, detect
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


def build_context(opts: ContextOptions) -> PipelineContext:
    """Build a :class:`PipelineContext` from CLI options, falling back to detect_context."""
    ctx = PipelineContext(
        project_id=opts.project_id,
        project_url=opts.project_url,
        pipeline_id=opts.pipeline_id,
        mr_iid=opts.mr_iid,
        source_branch=opts.branch,
    )

    if not ctx.project_id:
        # Fall back to detect_context
        try:
            detect_args = DetectArgs(
                mr_iid=ctx.mr_iid,
                pipeline_id=ctx.pipeline_id,
            )
            detected = detect(detect_args)
            ctx.project_id = ctx.project_id or detected.project_id
            ctx.project_url = ctx.project_url or detected.project_url
            ctx.pipeline_id = ctx.pipeline_id or detected.pipeline_id
            ctx.mr_iid = ctx.mr_iid or detected.mr_iid
            ctx.source_branch = ctx.source_branch or detected.mr_source_branch
        except Exception as exc:
            print(f"Warning: detect_context failed: {exc}", file=sys.stderr)

    if not ctx.project_id:
        print("ERROR: impossible de detecter le project_id. Utilise --project-id.", file=sys.stderr)
        raise typer.Exit(code=1)

    return ctx
