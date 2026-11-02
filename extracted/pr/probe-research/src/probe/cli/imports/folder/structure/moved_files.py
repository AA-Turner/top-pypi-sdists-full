"""move delivered files to their run or experiment, and find files imported before the folder's plan named any."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from probe.cli.imports.folder.structure.resolution import Level, REVIEWED_KEY, STRUCTURE_VERSION, reviewed_version
#: Moves in flight at once while filing files into their runs.
FILE_WORKERS = 4


#: A move the server refused for good: the artifact or its target is gone (404),
#: a file identical to it is already there (409), or the move is not one the
#: server allows from where the file now is -- a person filed it elsewhere (422).
FINAL_MOVE_STATUSES = (404, 409, 422)


def file_delivered(coverage, client, *, report=None) -> dict:
    """Move every delivered file not yet at its run or experiment there.

    The artifact keeps its id and its bytes; only where it is filed changes. A
    file whose upload has not landed waits for the next pass; a changed file's
    new upload (a new artifact) is filed again. A move the server refuses for
    good is recorded and not retried.
    """
    pending = coverage.unfiled()
    if not pending:
        return {"files_filed": 0, "files_filing_failed": 0}
    filed, failed = file_moves(client, pending)
    for path, artifact_id, target_id in filed:
        coverage.filed(path, target_id, artifact_id)
    for path, artifact_id, error, final in failed:
        if final:
            coverage.filing_refused(path, artifact_id, error)
        else:
            # It may have moved part of the way (up to its project, then the
            # step down failed): where it sits is unknown, so the next pass
            # sends its move again whatever it was last filed as.
            coverage.filing_unknown(path)
    if report is not None:
        if filed:
            report.add(f"{len(filed):,} file(s) filed into their runs and experiments "
                       "(no bytes re-sent).")
        if failed:
            report.add(f"{len(failed):,} file(s) could not be filed into their run or experiment; "
                       "they stay at their project (a refused move is not retried):",
                       *[f"  {path}: {error}" for path, _, error, _ in failed[:3]])
    return {"files_filed": len(filed), "files_filing_failed": len(failed)}


def _landed(row: dict | None, level: str, target_id: str) -> bool:
    """Did a move's answer put the artifact at (level, target)? Both storage
    shapes: an experiment's file reads `project_id = E` until R6, or
    `experiment_id = E` beside its project."""
    if not isinstance(row, dict):
        return True  # an answer without a body: nothing says otherwise
    if level == Level.RUN.value:
        return str(row.get("run_id")) == str(target_id)
    if level == Level.EXPERIMENT.value:
        return row.get("run_id") is None and target_id in (
            str(row.get("experiment_id")), str(row.get("project_id")))
    return (row.get("run_id") is None and not row.get("experiment_id")
            and str(row.get("project_id") or target_id) == str(target_id))


def file_moves(client, moves) -> tuple[list[tuple[str, str, str]], list[tuple[str, str, str, bool]]]:
    """Move artifacts to their run, experiment or project. Data in, no store.

    `moves` are `(path, artifact id, level, target id)`. Returns the moves made,
    `(path, artifact id, target id)`, and the ones refused,
    `(path, artifact id, error, final)`: `final` when the server refused for
    good (`FINAL_MOVE_STATUSES`), so the caller does not offer it again.

    The server moves a file only along its own chain: up to an ancestor, or
    down into its own subtree; run to run is refused (422). A file a re-plan
    takes from one run (or experiment) to another goes up to its project
    first, then down to its target. A move counts only where the server's
    answer says the file landed.
    """
    from .....sdk import errors

    def move(item):
        path, artifact_id, level, target_id = item
        try:
            try:
                row = client.move_artifact(artifact_id, level=level, target_id=target_id)
            except errors.RosError as exc:
                if exc.status != 422 or level == Level.PROJECT.value:
                    raise
                # Not in the target's subtree: up to the project, then down.
                client.move_artifact(artifact_id, level=Level.PROJECT.value)
                row = client.move_artifact(artifact_id, level=level, target_id=target_id)
            if not _landed(row, level, target_id):
                # The server put it somewhere else (a person moved its run,
                # say): asking again would land it there again.
                return item, f"the server filed it elsewhere ({level} {target_id} asked)", True
            return item, None, False
        except Exception as exc:  # noqa: BLE001 - recorded per file
            final = isinstance(exc, errors.RosError) and exc.status in FINAL_MOVE_STATUSES
            return item, str(exc)[:300], final

    filed: list[tuple[str, str, str]] = []
    failed: list[tuple[str, str, str, bool]] = []
    with ThreadPoolExecutor(max_workers=FILE_WORKERS) as pool:
        for (path, artifact_id, _, target_id), error, final in pool.map(move, list(moves)):
            if error is None:
                filed.append((path, artifact_id, target_id))
            else:
                failed.append((path, artifact_id, error, final))
    return filed, failed


def restructure_candidates(coverage, *, version: int = STRUCTURE_VERSION) -> dict[str, str]:
    """Files imported before this folder's plan named experiments and runs.

    path -> project slug, for delivered (or referenced) files with a project.
    Empty once a plan has been made, or declined, under `version` or later.
    """
    if reviewed_version(coverage.meta(REVIEWED_KEY)) >= version:
        return {}
    report = coverage.report()
    done = set(report["delivered"]) | set(report["references"])
    return {row["path"]: row["project_slug"] for row in coverage.rows()
            if row["path"] in done and row["project_id"] and row["project_slug"]}
