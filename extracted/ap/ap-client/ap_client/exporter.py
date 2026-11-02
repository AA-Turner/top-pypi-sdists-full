"""Export job/group data from Agent Platform to local directories."""

from __future__ import annotations

import concurrent.futures
import json
import logging
import os
import re
import shutil
import sys
import tarfile
import tempfile
import threading
import uuid
from contextlib import nullcontext
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Callable, Optional

import requests

if TYPE_CHECKING:
    from irepo_artifact import ArtifactClient, DownloadResult

from .api import APIClient, APIError

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = "~/.cache/agentplatform"
_DOWNLOAD_TIMEOUT = 300
ProgressCallback = Callable[[int, int, str, str], None]
StageCallback = Callable[[str], None]
ResultCallback = Callable[[str, str, Optional[str]], None]


def _is_share_client(client: APIClient) -> bool:
    return getattr(client, "is_share", False) is True


@dataclass
class ExportSummary:
    """Summary of a group export operation."""

    downloaded: int = 0
    skipped: int = 0
    skipped_job_names: list[str] = field(default_factory=list)


def default_cache_dir() -> Path:
    """Return the export cache root."""
    raw = os.environ.get("AP_CACHE_DIR", DEFAULT_CACHE_DIR)
    return Path(raw).expanduser()


def default_job_export_dir(job_id: str) -> Path:
    """Return the default export path for one job."""
    return default_cache_dir() / "jobs" / job_id


def default_group_export_dir(group_id: str) -> Path:
    """Return the default export path for one group."""
    configured_root = os.environ.get("AP_CACHE_DIR")
    if configured_root:
        return Path(configured_root).expanduser() / "groups" / group_id
    return Path.cwd() / group_id


def export_job(
    client: APIClient,
    job_id: str,
    output_dir: Optional[Path] = None,
    *,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
) -> Path:
    """Export a single job to disk."""
    dest = Path(output_dir) if output_dir else default_job_export_dir(job_id)
    dest.mkdir(parents=True, exist_ok=True)
    _export_job_into_dir(
        client,
        job_id,
        dest,
        timeout=timeout,
        result_callback=result_callback,
        include_logs=include_logs,
        include_events=include_events,
        extract_artifacts=extract_artifacts,
    )
    return dest


@dataclass
class BatchExportSummary(ExportSummary):
    failures: dict[str, str] = field(default_factory=dict)


def export_jobs(
    client: APIClient,
    job_ids: list[str],
    output_dir: Optional[Path] = None,
    *,
    workers: int = 1,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
) -> tuple[Path, BatchExportSummary]:
    """Download through the SDK batch API, then publish each Job independently."""
    root = Path(output_dir) if output_dir else default_cache_dir()
    parent = root.resolve()
    while not parent.exists():
        parent = parent.parent
    summary = BatchExportSummary()
    ids = list(dict.fromkeys(job_ids))
    if _is_share_client(client):
        root.mkdir(parents=True, exist_ok=True)
        for job_id in ids:
            try:
                skipped = _export_job_into_dir(
                    client,
                    job_id,
                    root / "jobs" / job_id,
                    timeout=timeout,
                    result_callback=result_callback,
                    include_logs=include_logs,
                    include_events=include_events,
                    extract_artifacts=extract_artifacts,
                    skip_no_artifact=True,
                )
            except Exception as exc:
                summary.failures[job_id] = str(exc)
            else:
                if skipped is not None:
                    summary.skipped += 1
                    summary.skipped_job_names.append(skipped)
                else:
                    summary.downloaded += 1
        return root, summary
    with tempfile.TemporaryDirectory(prefix=".artifact-export-", dir=parent) as temporary:
        results = _new_artifact_client(client, timeout=timeout).download_many(
            ids,
            output_dir=temporary,
            max_concurrent=workers,
            extract=extract_artifacts,
            overwrite=True,
        )
        for job_id in ids:
            try:
                skipped = _export_job_into_dir(
                    client,
                    job_id,
                    root / "jobs" / job_id,
                    timeout=timeout,
                    result_callback=result_callback,
                    include_logs=include_logs,
                    include_events=include_events,
                    extract_artifacts=extract_artifacts,
                    skip_no_artifact=True,
                    downloaded=results[job_id],
                )
            except Exception as exc:
                summary.failures[job_id] = str(exc)
            else:
                if skipped is not None:
                    summary.skipped += 1
                    summary.skipped_job_names.append(skipped)
                else:
                    summary.downloaded += 1
    return root, summary


def export_group(
    client: APIClient,
    group_id: str,
    output_dir: Optional[Path] = None,
    progress_callback: Optional[ProgressCallback] = None,
    workers: int = 4,
    *,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
    include_files: Optional[list[str]] = None,
    exclude_files: Optional[list[str]] = None,
) -> tuple[Path, ExportSummary]:
    """Export a group and all of its jobs to disk.

    Jobs without artifact URLs are skipped: no directory is created for them.
    Returns (dest_path, ExportSummary) with download/skip statistics.
    """
    include_files = _normalize_file_selectors(include_files)
    exclude_files = _normalize_file_selectors(exclude_files)
    if not extract_artifacts and (include_files or exclude_files):
        raise ValueError("file filters cannot be used when artifact extraction is disabled")
    if _is_share_client(client) and (include_files or exclude_files):
        raise ValueError("file filters are not supported with a share token")

    dest = Path(output_dir) if output_dir else default_group_export_dir(group_id)
    dest.mkdir(parents=True, exist_ok=True)

    group = client.get_group_stats(group_id)
    _write_json(dest / "group.json", group)
    try:
        group_eval = client.get_group_eval(group_id)
        _write_json(dest / "eval.json", group_eval)
        _write_json(dest / "eval_summary.json", group_eval.get("summary", {}))
        task_key = "per_task" if _is_share_client(client) else "results"
        _write_json(dest / "eval_tasks.json", group_eval.get(task_key, []))
    except Exception:
        # Some groups are non-eval workloads, or older servers may not expose eval endpoints.
        pass

    jobs_dir = dest / "jobs"

    workers = max(1, int(workers))
    jobs = _list_group_jobs(client, group_id)
    total = len(jobs)
    done = 0
    done_lock = threading.Lock()
    skipped_jobs: list[str] = []
    downloaded_count = 0

    if progress_callback is not None:
        progress_callback(done, total, "", "listing jobs")

    def _notify(job_id: str, stage: str) -> None:
        if progress_callback is None:
            return
        with done_lock:
            current_done = done
        progress_callback(current_done, total, job_id, stage)

    def _mark_done(job_id: str) -> None:
        nonlocal done
        with done_lock:
            done += 1
            current_done = done
        if progress_callback is not None:
            progress_callback(current_done, total, job_id, "done")

    if workers == 1 or total <= 1:
        for job in jobs:
            job_id = job["job_id"]
            _notify(job_id, "starting")
            result = _export_job_into_dir(
                client,
                job_id,
                jobs_dir / job_id,
                job=None if _is_share_client(client) else job,
                stage_callback=lambda stage, current_job_id=job_id: _notify(current_job_id, stage),
                timeout=timeout,
                result_callback=result_callback,
                include_logs=include_logs,
                include_events=include_events,
                extract_artifacts=extract_artifacts,
                skip_no_artifact=True,
                include_files=include_files,
                exclude_files=exclude_files,
            )
            if result is not None:
                skipped_jobs.append(result)
            else:
                downloaded_count += 1
            _mark_done(job_id)
        return dest, ExportSummary(
            downloaded=downloaded_count,
            skipped=len(skipped_jobs),
            skipped_job_names=skipped_jobs,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(
                _export_job_with_fresh_client,
                client,
                job,
                jobs_dir / job["job_id"],
                lambda stage, current_job_id=job["job_id"]: _notify(current_job_id, stage),
                timeout=timeout,
                result_callback=result_callback,
                include_logs=include_logs,
                include_events=include_events,
                extract_artifacts=extract_artifacts,
                skip_no_artifact=True,
                include_files=include_files,
                exclude_files=exclude_files,
            ): job["job_id"]
            for job in jobs
        }
        for future in concurrent.futures.as_completed(future_map):
            job_id = future_map[future]
            result = future.result()
            if result is not None:
                skipped_jobs.append(result)
            else:
                downloaded_count += 1
            _mark_done(job_id)

    return dest, ExportSummary(
        downloaded=downloaded_count,
        skipped=len(skipped_jobs),
        skipped_job_names=skipped_jobs,
    )


def _list_group_jobs(client: APIClient, group_id: str) -> list[dict]:
    """Fetch all jobs in a group with pagination.

    终止条件（满足任一即停止）：
    1. 当前页返回空列表（没有更多数据）
    2. 当前页返回数据量 < limit（最后一页不满，说明已无更多数据）
    3. total 一致性警告：已获取数远超 total 时记录警告，但不终止循环
    """
    skip = 0
    limit = 200
    jobs: list[dict] = []
    total = None

    while True:
        page = client.list_jobs(group_id=group_id, skip=skip, limit=limit)
        page_jobs = page.get("jobs", [])

        # 第一次请求时获取 total
        if total is None:
            total = page.get("total")  # 如果服务端没有返回 total，则为 None

        # 终止条件1: 当前页为空，说明没有更多数据
        if not page_jobs:
            break

        jobs.extend(page_jobs)

        # 终止条件2: 当前页数据量 < limit，说明已到最后一页
        if len(page_jobs) < limit:
            break

        skip += limit

        # total 一致性警告（仅警告，不终止循环）
        if total is not None and total > 0 and len(jobs) > total:
            logger.warning(
                "Fetched %d jobs exceeds server-reported total=%d, continuing pagination",
                len(jobs),
                total,
            )

    return jobs


def _export_job_with_fresh_client(
    client: APIClient,
    job: dict,
    dest: Path,
    stage_callback: Optional[StageCallback] = None,
    *,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
    skip_no_artifact: bool = False,
    include_files: Optional[list[str]] = None,
    exclude_files: Optional[list[str]] = None,
) -> Optional[str]:
    """Export one job with a dedicated client/session for thread safety."""
    if _is_share_client(client):
        from .share_api import ShareAPIClient

        worker_client = ShareAPIClient(
            client.config, client.share_token, group_id=client.share_group_id
        )
    else:
        worker_client = APIClient(client.config)
    return _export_job_into_dir(
        worker_client,
        job["job_id"],
        dest,
        job=None if _is_share_client(client) else job,
        stage_callback=stage_callback,
        timeout=timeout,
        result_callback=result_callback,
        include_logs=include_logs,
        include_events=include_events,
        extract_artifacts=extract_artifacts,
        skip_no_artifact=skip_no_artifact,
        include_files=include_files,
        exclude_files=exclude_files,
    )


def _export_job_into_dir(
    client: APIClient,
    job_id: str,
    dest: Path,
    job: Optional[dict] = None,
    stage_callback: Optional[StageCallback] = None,
    *,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
    skip_no_artifact: bool = False,
    include_files: Optional[list[str]] = None,
    exclude_files: Optional[list[str]] = None,
    downloaded: Optional[DownloadResult] = None,
) -> Optional[str]:
    """Export SDK-managed artifacts alongside AP metadata.

    Ordinary exports use the SDK for artifacts. Share exports use the share
    endpoint's signed archive URL because the SDK uses authenticated routes.
    """
    if _is_share_client(client):
        return _export_shared_job_into_dir(
            client,
            job_id,
            dest,
            stage_callback=stage_callback,
            timeout=timeout,
            result_callback=result_callback,
            include_logs=include_logs,
            include_events=include_events,
            extract_artifacts=extract_artifacts,
            skip_no_artifact=skip_no_artifact,
        )
    from irepo_artifact import AccessDenied, ArtifactError, ArtifactNotFound

    job_data = job or {}
    current_stage = "job metadata"
    selective = bool(include_files or exclude_files)

    def _set_stage(stage: str) -> None:
        nonlocal current_stage
        current_stage = stage
        if stage_callback is not None:
            stage_callback(stage)

    try:
        _set_stage("job metadata")
        job_data = job or client.get_job(job_id)
        download_stage = (
            "downloading selected artifact files" if selective else "downloading artifact"
        )
        _set_stage(download_stage)
        # Stage on the destination filesystem without creating a skipped Job's
        # directory (or an empty jobs/ directory when every Job is skipped).
        parent = dest.resolve()
        while not parent.exists():
            parent = parent.parent
        context = (
            nullcontext(downloaded.job_dir)
            if downloaded is not None
            else tempfile.TemporaryDirectory(prefix=".artifact-export-", dir=parent)
        )
        with context as temporary:
            staging = Path(temporary)
            error = None
            if downloaded is not None:
                outcome = downloaded
                error = downloaded.error
                if downloaded.status != "success" and error is None:
                    raise RuntimeError(
                        f"SDK download returned {downloaded.status} without an error"
                    )
            else:
                try:
                    outcome = _new_artifact_client(client, timeout=timeout).download(
                        job_id,
                        output_dir=str(staging),
                        include_files=include_files,
                        exclude_files=exclude_files,
                        extract=extract_artifacts and not selective,
                        overwrite=True,
                    )
                except ArtifactError as exc:
                    outcome = error = exc

            # A denied refresh can retain old metadata. Never publish or delete
            # existing export files on an authorization failure.
            if isinstance(error, AccessDenied):
                raise error

            artifact = outcome.artifacts_response
            manifest = outcome.manifest_response
            missing_manifest = (
                isinstance(manifest, dict)
                and "manifest" in manifest
                and manifest["manifest"] is None
            )
            missing_links = (
                isinstance(artifact, dict)
                and artifact.get("url", False) is None
                and not artifact.get("downloads")
            )
            missing = isinstance(error, ArtifactNotFound) and (
                missing_manifest
                if selective
                else missing_links or str(error) == "artifact content not found"
            )
            # SDK 0.1.0 uses ArtifactNotFound for both API and content 404s, and a
            # failed refresh keeps the last metadata. Only its content-missing
            # diagnostic (or an explicit empty response) is safe to skip. Unknown
            # diagnostics fail closed instead of deleting a previous export.
            if missing and skip_no_artifact:
                if not missing_links and not missing_manifest:
                    shutil.rmtree(dest, ignore_errors=True)
                _set_stage("skipped")
                if job_data.get("status") == "Succeeded":
                    logger.warning(
                        "Skipping succeeded job %s (artifact missing — abnormal)", job_id
                    )
                else:
                    logger.info(
                        "Skipping job %s (status=%s, artifact missing)",
                        job_id,
                        job_data.get("status", ""),
                    )
                if result_callback is not None:
                    result_callback(job_id, "skipped", None)
                return job_data.get("job_name") or job_id

            # A missing route or invalid manifest is an API/protocol failure, not
            # evidence of a missing artifact. Do not turn it into a skipped Job.
            valid_manifest = (
                isinstance(manifest, dict)
                and "manifest" in manifest
                and not manifest.get("truncated")
                and (manifest["manifest"] is None or isinstance(manifest["manifest"], list))
            )
            if error is not None and (not valid_manifest if selective else artifact is None):
                raise error

            dest.mkdir(parents=True, exist_ok=True)
            _set_stage("metrics")
            metrics = client.get_job_metrics(job_id)
            _write_json(dest / "job.json", job_data)
            _write_json(dest / "metrics.json", metrics)
            if not selective:
                _write_json(dest / "artifacts.json", artifact)
            elif manifest is not None:
                _write_json(
                    dest / "artifacts.json",
                    {"job_id": job_id, "url": None, "mode": "selected_files"},
                )
                _write_json(dest / "artifacts-manifest.json", manifest)
            if include_events:
                _set_stage("events")
                _write_text(dest / "events.txt", _format_events(client.get_job_events(job_id)))
            if include_logs:
                _set_stage("logs")
                _write_logs(dest / "logs", client, job_id, job_data)

            _set_stage(download_stage)
            if error is not None:
                if (
                    not selective
                    and not missing_links
                    and (not isinstance(error, ArtifactNotFound) or missing)
                ):
                    (dest / "result.tgz").unlink(missing_ok=True)
                if missing:
                    if not missing_links:
                        _warn_missing_artifact(job_id)
                    if result_callback is not None:
                        result_callback(job_id, "skipped", None)
                    return None
                raise error
            # Only AP's output publication remains here. SDK owns filtering,
            # link refresh, transfer and extraction, including empty selections.
            if selective or extract_artifacts:
                _commit_staged_artifacts(
                    staging / "artifacts",
                    dest / "artifacts",
                    archive=None if selective else staging / "result.tgz",
                )
            else:
                (staging / "result.tgz").replace(dest / "result.tgz")
            if result_callback is not None:
                result_callback(job_id, "downloaded", outcome.channel)
    except Exception as exc:
        if result_callback is not None:
            result_callback(job_id, "failed", None)

        if isinstance(exc, AccessDenied):
            if (
                job_data.get("transparency") == "blackbox"
                and job_data.get("can_read_content") is False
                and getattr(exc, "_request_status", None) == 403
            ):
                raise APIError(
                    403,
                    {
                        "code": "blackbox_content_restricted",
                        "message": "Group Reader access is required",
                    },
                    None,
                    None,
                ) from exc
            raise RuntimeError(
                f"Access denied while exporting job {job_id}; check your login/API key and resource permissions."
            ) from exc
        if (
            isinstance(exc, APIError)
            and isinstance(exc.detail, dict)
            and exc.detail.get("code") == "blackbox_content_restricted"
        ):
            raise
        raise RuntimeError(
            f"Failed to export job {job_id} at stage '{current_stage}': {exc}"
        ) from exc
    return None


def _export_shared_job_into_dir(
    client: APIClient,
    job_id: str,
    dest: Path,
    *,
    stage_callback: Optional[StageCallback] = None,
    timeout: float = _DOWNLOAD_TIMEOUT,
    result_callback: Optional[ResultCallback] = None,
    include_logs: bool = False,
    include_events: bool = False,
    extract_artifacts: bool = True,
    skip_no_artifact: bool = False,
) -> Optional[str]:
    """Use the share route's signed archive URL; the SDK uses authenticated routes."""
    stage = "job metadata"

    def set_stage(value: str) -> None:
        nonlocal stage
        stage = value
        if stage_callback is not None:
            stage_callback(value)

    try:
        job = client.get_job(job_id)
        set_stage("artifact metadata")
        artifacts = client.get_job_artifacts([job_id])
        artifact = artifacts[0] if artifacts else {"job_id": job_id, "url": None}
        url = artifact.get("url")
        if not url and skip_no_artifact:
            set_stage("skipped")
            if result_callback is not None:
                result_callback(job_id, "skipped", None)
            return job.get("job_name") or job_id

        parent = dest.resolve()
        while not parent.exists():
            parent = parent.parent
        with tempfile.TemporaryDirectory(prefix=".artifact-share-", dir=parent) as temporary:
            staging = Path(temporary)
            if url:
                set_stage("downloading artifact")
                try:
                    _download_shared_archive(url, staging / "result.tgz", timeout)
                except FileNotFoundError:
                    if skip_no_artifact:
                        _remove_path(dest)
                        set_stage("skipped")
                        if result_callback is not None:
                            result_callback(job_id, "skipped", None)
                        return job.get("job_name") or job_id
                    (dest / "result.tgz").unlink(missing_ok=True)
                    _warn_missing_artifact(job_id)
                    url = None
                if url and extract_artifacts:
                    set_stage("extracting artifact")
                    _extract_shared_archive(staging / "result.tgz", staging / "artifacts")

            dest.mkdir(parents=True, exist_ok=True)
            set_stage("metrics")
            _write_json(dest / "job.json", job)
            _write_json(dest / "metrics.json", client.get_job_metrics(job_id))
            _write_json(dest / "artifacts.json", artifact)
            if include_events:
                set_stage("events")
                _write_text(dest / "events.txt", _format_events(client.get_job_events(job_id)))
            if include_logs:
                set_stage("logs")
                _write_logs(dest / "logs", client, job_id, job)

            if url:
                set_stage("publishing artifact")
                if extract_artifacts:
                    _commit_staged_artifacts(
                        staging / "artifacts", dest / "artifacts", archive=staging / "result.tgz"
                    )
                else:
                    (staging / "result.tgz").replace(dest / "result.tgz")
                if result_callback is not None:
                    result_callback(job_id, "downloaded", None)
            elif result_callback is not None:
                result_callback(job_id, "skipped", None)
    except Exception as exc:
        if result_callback is not None:
            result_callback(job_id, "failed", None)
        raise RuntimeError(f"Failed to export job {job_id} at stage '{stage}': {exc}") from exc
    return None


def _download_shared_archive(url: str, dest: Path, timeout: float) -> None:
    """Stream a signed URL without including it in user-visible errors."""
    try:
        with requests.get(url, stream=True, timeout=(10, timeout)) as response:
            if response.status_code == 404:
                raise FileNotFoundError("shared artifact was not found")
            if response.status_code >= 400:
                raise RuntimeError(f"shared artifact download returned HTTP {response.status_code}")
            with dest.open("wb") as output:
                for chunk in response.iter_content(chunk_size=4 * 1024 * 1024):
                    if chunk:
                        output.write(chunk)
    except requests.RequestException:
        raise RuntimeError("shared artifact download failed") from None


def _extract_shared_archive(archive: Path, artifacts: Path) -> None:
    """Extract an archive inside a fresh staging directory with bounded links."""
    raw = artifacts.parent / "unpacked"
    raw.mkdir()
    try:
        directory_modes: dict[Path, int] = {}
        with tarfile.open(archive, "r:gz") as tar:
            for member in tar:
                name = member.name
                while name.startswith("./"):
                    name = name[2:]
                if name in ("", ".") and member.isdir():
                    continue
                parts = PurePosixPath(name).parts
                if (
                    not name
                    or name.startswith("/")
                    or "\\" in name
                    or "\x00" in name
                    or any(part in {".", ".."} for part in parts)
                    or not (member.isfile() or member.isdir() or member.issym() or member.islnk())
                ):
                    raise ValueError("unsafe shared artifact archive member")
                target = raw / name
                if not target.resolve().is_relative_to(raw.resolve()):
                    raise ValueError("shared artifact archive path escapes destination")
                target.parent.mkdir(parents=True, exist_ok=True)
                if member.isdir():
                    target.mkdir(exist_ok=True)
                    directory_modes[target] = member.mode & 0o777
                elif member.isfile():
                    with tar.extractfile(member) as source, target.open("wb") as output:
                        shutil.copyfileobj(source, output)
                    target.chmod(member.mode & 0o777)
                else:
                    link = member.linkname
                    if (
                        not link
                        or link.startswith("/")
                        or "\\" in link
                        or "\x00" in link
                        or re.match(r"^[A-Za-z]:", link)
                    ):
                        raise ValueError("unsafe shared artifact archive link")
                    link_target = (target.parent if member.issym() else raw) / link
                    if not link_target.resolve().is_relative_to(raw.resolve()):
                        raise ValueError("shared artifact archive link escapes destination")
                    if target.exists() or target.is_symlink():
                        target.unlink()
                    if member.issym():
                        target.symlink_to(link)
                    else:
                        if not link_target.is_file():
                            raise ValueError("shared artifact hard link target is not a file")
                        os.link(link_target.resolve(), target)

        entries = list(raw.iterdir())
        root = (
            entries[0]
            if len(entries) == 1 and entries[0].is_dir() and not entries[0].is_symlink()
            else raw
        )
        output_dir = artifacts / "output"
        output_dir.mkdir(parents=True)
        root_path = root.resolve()
        rewritten_links: dict[Path, str] = {}
        for entry in raw.rglob("*"):
            if not entry.is_symlink():
                continue
            target = entry.resolve()
            if not target.is_relative_to(root_path):
                raise ValueError("shared artifact archive link escapes output")
            final_link = output_dir / entry.relative_to(root)
            final_target = output_dir / target.relative_to(root_path)
            rewritten_links[final_link] = os.path.relpath(final_target, final_link.parent)
        for entry in root.iterdir():
            entry.replace(output_dir / entry.name)
        for link_path, link_target in rewritten_links.items():
            link_path.unlink()
            link_path.symlink_to(link_target)
            if not link_path.resolve().is_relative_to(output_dir.resolve()):
                raise ValueError("shared artifact archive link escapes output")
        # Apply explicit directory modes after all writes and link rewrites so
        # private parents do not prevent extraction of their children.
        for source_dir, mode in sorted(
            directory_modes.items(), key=lambda item: len(item[0].parts), reverse=True
        ):
            final_dir = output_dir / source_dir.relative_to(root)
            if (
                final_dir.is_symlink()
                or not final_dir.is_dir()
                or not final_dir.resolve().is_relative_to(output_dir.resolve())
            ):
                raise ValueError("shared artifact archive directory changed type")
            final_dir.chmod(mode)
    finally:
        shutil.rmtree(raw, ignore_errors=True)


def _normalize_file_selectors(values: Optional[list[str]]) -> Optional[list[str]]:
    selectors: list[str] = []
    for raw in values or []:
        if not isinstance(raw, str):
            raise ValueError("Artifact file selectors must be strings")
        selector = raw.strip()
        while selector.startswith("./"):
            selector = selector[2:]
        selector = selector.rstrip("/")
        _validate_relative_artifact_path(selector, "artifact file selector")
        if selector not in selectors:
            selectors.append(selector)
    return selectors or None


def _validate_relative_artifact_path(path: str, label: str) -> None:
    invalid = (
        not path
        or path.startswith("/")
        or "\\" in path
        or "\x00" in path
        or any(part in {"", ".", ".."} for part in path.split("/"))
        or (len(path) >= 2 and path[0].isalpha() and path[1] == ":")
    )
    if invalid:
        prefix = "Unsafe" if label == "artifact manifest path" else "Invalid"
        raise ValueError(f"{prefix} {label}: {path!r}")


def _new_artifact_client(
    client: APIClient, *, timeout: float = _DOWNLOAD_TIMEOUT
) -> ArtifactClient:
    """Forward AP connection settings through the SDK's public constructor."""
    from irepo_artifact import ArtifactClient

    config = client.config
    endpoint = config.base_url.rstrip("/")
    # Match APIClient._url: configured /api paths and direct localhost/NLB
    # addresses already address the API and must not receive another prefix.
    direct = any(part in endpoint for part in ("/api", "nlb-", "localhost"))
    return ArtifactClient(
        ap_endpoint=endpoint,
        api_key=config.token_key,
        headers=dict(config.headers),
        api_prefix="" if direct else "/api",
        timeout=timeout,
        manifest_wait_timeout=config.artifact_manifest_wait_timeout,
        layout="ap_export",
        verbose=config.verbose,
    )


def _path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def _commit_staged_artifacts(
    staging_dir: Path, artifacts_dir: Path, *, archive: Optional[Path] = None
) -> None:
    """Publish SDK output, restoring the previous export if installation fails."""
    suffix = uuid.uuid4().hex
    artifacts_backup = artifacts_dir.with_name(f".{artifacts_dir.name}.previous-{suffix}")
    archive_path = artifacts_dir.parent / "result.tgz"
    archive_backup = archive_path.with_name(f".{archive_path.name}.previous-{suffix}")
    moved_artifacts = False
    moved_archive = False
    installed = False

    try:
        if _path_exists(artifacts_dir):
            artifacts_dir.replace(artifacts_backup)
            moved_artifacts = True
        if _path_exists(archive_path):
            archive_path.replace(archive_backup)
            moved_archive = True
        staging_dir.replace(artifacts_dir)
        installed = True
        if archive is not None:
            archive.replace(archive_path)
    except Exception:
        if installed and _path_exists(artifacts_dir):
            _remove_path(artifacts_dir)
        if moved_artifacts and _path_exists(artifacts_backup):
            artifacts_backup.replace(artifacts_dir)
        if moved_archive and _path_exists(archive_backup):
            archive_backup.replace(archive_path)
        raise

    for backup in (artifacts_backup, archive_backup):
        if not _path_exists(backup):
            continue
        try:
            _remove_path(backup)
        except OSError as exc:
            logger.warning("Failed to remove selective export backup %s: %s", backup, exc)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_logs(logs_dir: Path, client: APIClient, job_id: str, job_data: dict = None) -> None:
    """Write logs for all containers of a job to separate files in the logs directory."""
    logs_dir.mkdir(parents=True, exist_ok=True)

    # 获取所有容器名称
    job_data = job_data or client.get_job(job_id)
    containers_resp = client.get_job_containers(job_id)
    containers = containers_resp.get("containers", ["main"])  # 默认使用 "main" 容器

    # 为每个容器获取日志并保存到独立的文件
    logs_by_container = {}
    for container in containers:
        try:
            container_logs = client.get_job_logs_complete(job_id, container=container)
            logs_by_container[container] = container_logs
        except Exception as e:
            # 如果某个容器没有日志，记录错误并继续
            print(
                f"[ap export] warning: failed to get logs for container '{container}' in job {job_id}: {e}",
                file=sys.stderr,
            )
            logs_by_container[container] = {"logs": [], "container": container, "job_id": job_id}

    for container, logs_data in logs_by_container.items():
        container_logs_file = logs_dir / f"{_sanitize_name(container)}.log"

        content = logs_data.get("logs", "")
        if isinstance(content, list):
            log_text = "\n".join(_format_log_entry(line) for line in content) + "\n"
        else:
            log_text = str(content or "")

        _write_text(container_logs_file, log_text)


def _format_log_entry(entry) -> str:
    """Format a single log entry to a human-readable line."""
    if isinstance(entry, dict):
        content = entry.get("content", "")
        timestamp = entry.get("timestamp", "")
        if timestamp:
            return f"[{timestamp}] {content}"
        return content
    return str(entry)


def _format_event_item(item) -> str:
    """Format a single event item to a human-readable line."""
    if isinstance(item, dict):
        ts = item.get("last_timestamp") or item.get("timestamp") or ""
        message = item.get("message", "")
        reason = item.get("reason", "")
        prefix = f"[{ts}] " if ts else ""
        body = f"{reason}: {message}" if reason else message
        return f"{prefix}{body}"
    return str(item)


def _format_events(events: dict) -> str:
    if "containers" in events:
        containers = events.get("containers") or {}
    else:
        container = events.get("container") or "default"
        containers = {container: events.get("events", [])}

    lines = []
    for container in sorted(containers):
        values = containers.get(container) or []
        if lines:
            lines.append("")
        lines.append("[{}]".format(container))
        lines.extend(_format_event_item(item) for item in values)
    return "\n".join(lines) + ("\n" if lines else "")


def _warn_missing_artifact(job_id: str) -> None:
    print(
        f"[ap export] warning: artifact missing for job {job_id}; skipping result.tgz download",
        file=sys.stderr,
    )


def _sanitize_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "-" for ch in name)
