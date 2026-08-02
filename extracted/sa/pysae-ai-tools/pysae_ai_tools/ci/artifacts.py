"""CLI entry point: pysae-ai-tools ci artifacts <command>.

Inspect and download a CI job's artifacts via the glab API.

Commands:
    list <job>                 List the artifact files a job exposes
    download <job> --path P    Download one file from the artifacts archive
    download <job> --archive   Download (and unzip) the whole archive

Examples:
    pysae-ai-tools ci artifacts list 987654
    pysae-ai-tools ci artifacts download 987654 --path coverage/coverage.xml
    pysae-ai-tools ci artifacts download 987654 --archive --dest /tmp/art
"""

import json
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Annotated, Any

import typer

from .common.glab import glab_api, resolve_target, run_glab_bytes

app = typer.Typer(help="Inspect and download CI job artifacts")


@dataclass
class ArtifactEntry:
    """One artifact file produced by a job (archive, metadata, junit, …)."""

    file_type: str
    filename: str
    size: int
    file_format: str = ""


def parse_artifacts(job: dict[str, Any]) -> list[ArtifactEntry]:
    """Extract the artifact entries from a job metadata payload (pure)."""
    entries: list[ArtifactEntry] = []
    for art in job.get("artifacts", []) or []:
        entries.append(
            ArtifactEntry(
                file_type=str(art.get("file_type", "") or ""),
                filename=str(art.get("filename", "") or ""),
                size=int(art.get("size", 0) or 0),
                file_format=str(art.get("file_format", "") or ""),
            )
        )
    return entries


def _resolve_job(job: str, project_id: str, job_id: str) -> tuple[str, str]:
    """Resolve (project_id, job_id), falling back to detect_context."""
    refs = [job] if job else []
    target = resolve_target(project_id=project_id, job_id=job_id or job, refs=refs)
    if not target.project_id or not target.job_id:
        print(
            "Could not resolve project_id / job_id. Pass a job URL or --project-id/--job-id.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    return target.project_id, target.job_id


@app.command("list")
def list_artifacts(
    job: Annotated[str, typer.Argument(help="Job id or URL (defaults to detected context)")] = "",
    project_id: Annotated[str, typer.Option("--project-id", help="GitLab project id")] = "",
    job_id: Annotated[str, typer.Option("--job-id", help="Job id (overrides positional)")] = "",
    as_json: Annotated[bool, typer.Option("--json", help="Emit structured JSON")] = False,
) -> None:
    """List the artifact files a job exposes (type, name, size, expiry)."""
    pid, jid = _resolve_job(job, project_id, job_id)
    data = glab_api(f"projects/{pid}/jobs/{jid}")
    if data is None:
        raise typer.Exit(1)

    entries = parse_artifacts(data)
    expire_at = data.get("artifacts_expire_at") or ""

    if as_json:
        print(
            json.dumps(
                {"job_id": jid, "artifacts_expire_at": expire_at, "artifacts": [asdict(e) for e in entries]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if not entries:
        print("This job exposes no artifacts.")
        return
    print(f"Artifacts for job {jid}" + (f" (expire at {expire_at})" if expire_at else ""))
    for entry in entries:
        size_kb = entry.size / 1024
        fmt = f", {entry.file_format}" if entry.file_format else ""
        print(f"  - {entry.file_type:10s} {entry.filename}  ({size_kb:.1f} KiB{fmt})")


@app.command("download")
def download_artifact(
    job: Annotated[str, typer.Argument(help="Job id or URL (defaults to detected context)")] = "",
    path: Annotated[str, typer.Option("--path", help="Single artifact file path inside the archive")] = "",
    archive: Annotated[bool, typer.Option("--archive", help="Download the whole artifacts archive (zip)")] = False,
    dest: Annotated[str, typer.Option("--dest", help="Destination dir for --archive (unzipped here)")] = "",
    output: Annotated[str, typer.Option("--output", help="Write a single file to this path instead of stdout")] = "",
    project_id: Annotated[str, typer.Option("--project-id", help="GitLab project id")] = "",
    job_id: Annotated[str, typer.Option("--job-id", help="Job id (overrides positional)")] = "",
) -> None:
    """Download one artifact file (--path) or the whole archive (--archive)."""
    if archive == bool(path):
        print("Pass exactly one of --path <file> or --archive.", file=sys.stderr)
        raise typer.Exit(1)

    pid, jid = _resolve_job(job, project_id, job_id)

    if path:
        content = run_glab_bytes("api", f"projects/{pid}/jobs/{jid}/artifacts/{path}")
        if content is None:
            print(f"Could not download '{path}' from job {jid}.", file=sys.stderr)
            raise typer.Exit(1)
        if output:
            Path(output).write_bytes(content)
            print(f"Wrote {len(content)} bytes to {output}", file=sys.stderr)
        else:
            sys.stdout.write(content.decode("utf-8", errors="replace"))
        return

    # Whole archive
    content = run_glab_bytes("api", f"projects/{pid}/jobs/{jid}/artifacts")
    if content is None:
        print(f"Could not download the artifacts archive from job {jid}.", file=sys.stderr)
        raise typer.Exit(1)
    dest_dir = Path(dest) if dest else Path(f"artifacts-{jid}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / f"artifacts-{jid}.zip"
    zip_path.write_bytes(content)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
        zip_path.unlink()
        print(f"Extracted artifacts to {dest_dir}", file=sys.stderr)
    except zipfile.BadZipFile:
        print(f"Downloaded archive is not a valid zip; kept raw at {zip_path}", file=sys.stderr)
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
