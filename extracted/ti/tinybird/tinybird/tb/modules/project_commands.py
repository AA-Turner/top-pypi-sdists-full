import re
import tarfile
from pathlib import Path
from typing import Optional

import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project


@cli.group(hidden=True)
@click.pass_context
def project(ctx: click.Context) -> None:
    """Project commands."""


@project.command(name="archive")
@click.option("-o", "--output", type=click.Path(), default=None, help="Output file path")
@click.pass_context
def project_archive(ctx: click.Context, output: Optional[str]) -> None:
    """Create a tar.gz archive of all datafiles for support purposes."""
    project_obj: Project = ctx.ensure_object(dict)["project"]
    config = ctx.ensure_object(dict)["config"]

    all_files = project_obj.get_project_files() + project_obj.get_vendored_files()

    if not all_files:
        click.echo(FeedbackManager.warning(message="No datafiles found in the project"))
        return

    if output:
        output_path = Path(output)
        if not output_path.is_absolute():
            output_path = Path(project_obj.folder) / output_path
    else:
        workspace_name = config.get("name", "") or project_obj.workspace_name or "workspace"
        workspace_name = re.sub(r"[^a-zA-Z0-9_-]", "_", workspace_name)
        output_filename = f"{workspace_name}_datafiles.tar.gz"
        output_path = Path(project_obj.folder) / output_filename

    if output_path.exists() and not click.confirm(f"{output_path} already exists. Overwrite?"):
        click.echo("Aborted.")
        return

    with tarfile.open(output_path, "w:gz") as tar:
        for f in all_files:
            rel_path = Path(f).relative_to(project_obj.path)
            tar.add(f, arcname=str(rel_path))
            click.echo(f"a {rel_path}")

    click.echo(FeedbackManager.success(message=f"Created {output_path}"))
