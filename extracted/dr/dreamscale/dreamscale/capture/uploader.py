"""Latency-aware background uploader for local LeRobot v3.0 episode spools.

Uploads finalized local episode bundles into Dreamscale's appendable dataset
ingest API (R2 presigned PUTs or customer BYOB S3) completely off the live
inference link:

- While live policy inference is active (``set_inference_active(True)``), upload
  streams throttle chunk writes below spare uplink headroom (default 256 KiB/s)
  so real-time QUIC/WSS observations never queue behind bulk episode video.
- During idle gaps between episodes (``set_inference_active(False)``), uploads
  burst at full link speed.
- Retries idempotently on ``client_episode_id`` after network drops or restarts
  without creating duplicate episodes.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.parse
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from dreamscale.capture.spool import EpisodeSummary, SpoolEpisode, _atomic_write_json

DEFAULT_ACTIVE_BYTES_PER_SEC = 256 * 1024  # 256 KiB/s while inference is active
DEFAULT_CHUNK_BYTES = 64 * 1024
INITIAL_BACKOFF_S = 2.0
MAX_BACKOFF_S = 60.0


def default_spool_root() -> Path:
    from dreamscale.config import dreamscale_home

    return dreamscale_home() / "spools"


def _iter_throttled_file(
    path: Path,
    *,
    inference_active: threading.Event,
    stop_event: threading.Event,
    active_bytes_per_sec: int,
    idle_bytes_per_sec: int | None,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Iterator[bytes]:
    """Stream file bytes, clamping throughput whenever live inference is active."""
    with path.open("rb") as fh:
        while True:
            if stop_event.is_set():
                raise InterruptedError("uploader stopped")
            t0 = time.monotonic()
            chunk = fh.read(chunk_bytes)
            if not chunk:
                break
            yield chunk
            limit = active_bytes_per_sec if inference_active.is_set() else idle_bytes_per_sec
            if limit and limit > 0:
                min_s = len(chunk) / float(limit)
                elapsed = time.monotonic() - t0
                if min_s > elapsed:
                    sleep_fn(min_s - elapsed)


@dataclass(frozen=True)
class UploadOutcome:
    client_episode_id: str
    episode_id: str
    dataset_ref: str
    qc_status: str | None
    storage_backend: str
    files_uploaded: int


class SpoolUploader:
    """Crash-safe, latency-aware background worker draining ``spool_root``."""

    def __init__(
        self,
        spool_root: Path,
        *,
        api_url: str,
        api_key: str,
        active_bytes_per_sec: int = DEFAULT_ACTIVE_BYTES_PER_SEC,
        idle_bytes_per_sec: int | None = None,
        timeout_s: float = 60.0,
        http_client: httpx.Client | None = None,
        s3_uploader: Callable[[dict[str, Any], str, Path], None] | None = None,
        on_uploaded: Callable[[UploadOutcome], None] | None = None,
        on_error: Callable[[str, Exception], None] | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.spool_root = Path(spool_root).expanduser().resolve()
        self.spool_root.mkdir(parents=True, exist_ok=True)
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.active_bytes_per_sec = max(16 * 1024, int(active_bytes_per_sec))
        self.idle_bytes_per_sec = idle_bytes_per_sec
        self.timeout_s = float(timeout_s)
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=self.timeout_s)
        self._s3_uploader = s3_uploader or self._upload_customer_s3
        self._on_uploaded = on_uploaded
        self._on_error = on_error
        self._sleep_fn = sleep_fn

        self._inference_active = threading.Event()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._retry_after: dict[str, tuple[float, float]] = {}  # ep_id -> (next_ts, backoff_s)
        self._thread: threading.Thread | None = None

    def set_inference_active(self, active: bool) -> None:
        """Toggle latency-aware throttling (clamped while True, burst when False)."""
        if active:
            self._inference_active.set()
        else:
            self._inference_active.clear()
            self._wake.set()

    def start(self) -> None:
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                return
            self._stop.clear()
            self._thread = threading.Thread(
                target=self._run_loop,
                name="dreamscale-spool-uploader",
                daemon=True,
            )
            self._thread.start()
        self._wake.set()

    def notify(self) -> None:
        """Wake the uploader immediately after a new episode is finalized."""
        self._wake.set()

    def stop(self, *, drain_timeout_s: float = 0.0) -> None:
        """Stop the background uploader, optionally waiting up to ``drain_timeout_s``."""
        if drain_timeout_s > 0:
            self.wait_until_idle(timeout_s=drain_timeout_s)
        self._stop.set()
        self._wake.set()
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=5.0)
        if self._owns_client:
            self._client.close()

    def pending_manifests(self) -> list[Path]:
        if not self.spool_root.exists():
            return []
        found: list[Path] = []
        for child in sorted(self.spool_root.iterdir()):
            manifest = child / "episode.json"
            if not manifest.is_file():
                continue
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 - ignore corrupt/partial manifests
                continue
            if data.get("status") in ("ready", "uploading") and data.get("dataset_ref"):
                found.append(manifest)
        return found

    def wait_until_idle(self, *, timeout_s: float = 30.0) -> bool:
        """Wait until all currently ready manifests are uploaded or timeout expires."""
        self._wake.set()
        deadline = time.monotonic() + max(0.1, timeout_s)
        while time.monotonic() < deadline:
            if not self.pending_manifests():
                return True
            self._sleep_fn(0.1)
        return not self.pending_manifests()

    def _run_loop(self) -> None:
        while not self._stop.is_set():
            did_work = self.drain_once()
            if self._stop.is_set():
                break
            if did_work:
                continue
            wait_s = self._next_wait_s()
            self._wake.wait(timeout=wait_s)
            self._wake.clear()

    def _next_wait_s(self) -> float:
        now = time.monotonic()
        soonest = 5.0
        for next_ts, _ in list(self._retry_after.values()):
            soonest = min(soonest, max(0.1, next_ts - now))
        return soonest

    def drain_once(self) -> bool:
        """Attempt one pass over pending local episodes; returns True if any succeeded."""
        progressed = False
        now = time.monotonic()
        for manifest_path in self.pending_manifests():
            if self._stop.is_set():
                break
            ep_dir = manifest_path.parent
            key = ep_dir.name
            retry = self._retry_after.get(key)
            if retry is not None and now < retry[0]:
                continue
            try:
                outcome = self.upload_episode(manifest_path)
            except InterruptedError:
                break
            except Exception as exc:  # noqa: BLE001
                prev_backoff = retry[1] if retry is not None else INITIAL_BACKOFF_S / 2
                backoff = min(MAX_BACKOFF_S, max(INITIAL_BACKOFF_S, prev_backoff * 2))
                self._retry_after[key] = (time.monotonic() + backoff, backoff)
                if self._on_error is not None:
                    self._on_error(key, exc)
            else:
                self._retry_after.pop(key, None)
                progressed = True
                if self._on_uploaded is not None:
                    self._on_uploaded(outcome)
        return progressed

    def upload_episode(self, manifest_path: Path) -> UploadOutcome:
        """Synchronously upload one finalized local episode manifest (idempotent)."""
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        dataset_ref = str(manifest.get("dataset_ref") or "").strip()
        if not dataset_ref:
            raise ValueError(f"Episode manifest {manifest_path} has no dataset_ref")
        files = [str(f) for f in manifest.get("files") or []]
        if not files:
            raise ValueError(f"Episode manifest {manifest_path} has no files to upload")

        ep_dir = manifest_path.parent
        missing = [name for name in files if not (ep_dir / name).is_file()]
        if missing:
            raise FileNotFoundError(f"Missing local spool files {missing} in {ep_dir}")

        manifest["status"] = "uploading"
        _atomic_write_json(manifest_path, manifest)

        quoted_ref = urllib.parse.quote(dataset_ref, safe="/")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        start_body: dict[str, Any] = {
            "client_episode_id": manifest["client_episode_id"],
            "files": files,
            "bytes": int(manifest.get("bytes") or 0),
            "frame_count": int(manifest.get("frame_count") or 0),
            "fps": manifest.get("fps"),
            "duration_seconds": manifest.get("duration_seconds"),
            "source_kind": manifest.get("source_kind") or "autonomous",
            "policy_id": manifest.get("policy_id"),
            "policy_version": manifest.get("policy_version"),
            "deployment_id": manifest.get("deployment_id"),
            "session_id": manifest.get("session_id"),
            "robot_id": manifest.get("robot_id"),
            "task": manifest.get("task") or "",
            "takeover_count": int(manifest.get("takeover_count") or 0),
            "takeover_frames": int(manifest.get("takeover_frames") or 0),
            "outcome": manifest.get("outcome"),
            "metadata": manifest.get("metadata") or {},
            "recorded_at": manifest.get("recorded_at"),
        }
        start_resp = self._client.post(
            f"{self.api_url}/v1/datasets/{quoted_ref}/episodes/upload",
            json={k: v for k, v in start_body.items() if v is not None},
            headers=headers,
        )
        start_resp.raise_for_status()
        start_payload = start_resp.json()
        episode_id = str(start_payload["episode"]["id"])
        backend = str(start_payload.get("storage_backend") or "r2")
        spool_prefix = str(start_payload.get("spool_prefix") or "").rstrip("/")

        uploaded_count = 0
        if backend == "r2":
            upload_urls: dict[str, str] = start_payload.get("upload_urls") or {}
            for name in files:
                url = upload_urls.get(name)
                if not url:
                    raise RuntimeError(f"Control plane did not return upload URL for '{name}'")
                file_path = ep_dir / name
                size = file_path.stat().st_size
                content_type = (
                    "video/mp4" if name.endswith(".mp4") else "application/octet-stream"
                )
                stream = _iter_throttled_file(
                    file_path,
                    inference_active=self._inference_active,
                    stop_event=self._stop,
                    active_bytes_per_sec=self.active_bytes_per_sec,
                    idle_bytes_per_sec=self.idle_bytes_per_sec,
                    sleep_fn=self._sleep_fn,
                )
                put_resp = self._client.put(
                    url,
                    content=stream,
                    headers={
                        "Content-Type": content_type,
                        "Content-Length": str(size),
                    },
                )
                put_resp.raise_for_status()
                uploaded_count += 1
        elif backend == "customer_s3":
            ext = start_payload.get("external_storage") or {}
            for name in files:
                file_path = ep_dir / name
                key = f"{spool_prefix}/{name}" if spool_prefix else name
                self._s3_uploader(ext, key, file_path)
                uploaded_count += 1
        else:
            raise RuntimeError(f"Unsupported episode storage_backend '{backend}'")

        complete_body: dict[str, Any] = {
            "readable": manifest.get("writer_error") is None,
            "unreadable_reason": manifest.get("writer_error"),
            "bytes": int(manifest.get("bytes") or 0),
            "frame_count": int(manifest.get("frame_count") or 0),
            "fps": manifest.get("fps"),
            "duration_seconds": manifest.get("duration_seconds"),
            "state_dim": manifest.get("state_dim"),
            "action_dim": manifest.get("action_dim"),
            "cameras": manifest.get("cameras") or [],
            "has_nonfinite": bool(manifest.get("has_nonfinite")),
            "zero_motion": bool(manifest.get("zero_motion")),
            "dropped_frame_ratio": manifest.get("dropped_frame_ratio"),
            "takeover_count": int(manifest.get("takeover_count") or 0),
            "takeover_frames": int(manifest.get("takeover_frames") or 0),
            "outcome": manifest.get("outcome"),
        }
        complete_resp = self._client.post(
            f"{self.api_url}/v1/datasets/{quoted_ref}/episodes/{urllib.parse.quote(episode_id)}/complete",
            json={k: v for k, v in complete_body.items() if v is not None},
            headers=headers,
        )
        complete_resp.raise_for_status()
        complete_payload = complete_resp.json()
        ep_row = complete_payload.get("episode") or {}
        qc_status = ep_row.get("qc_status")

        manifest["status"] = "uploaded"
        manifest["episode_id"] = episode_id
        manifest["qc_status"] = qc_status
        manifest["uploaded_at"] = datetime.now(UTC).isoformat()
        _atomic_write_json(manifest_path, manifest)

        if not manifest.get("keep_local", False):
            for name in files:
                try:
                    (ep_dir / name).unlink(missing_ok=True)
                except OSError:
                    pass

        return UploadOutcome(
            client_episode_id=str(manifest["client_episode_id"]),
            episode_id=episode_id,
            dataset_ref=dataset_ref,
            qc_status=qc_status,
            storage_backend=backend,
            files_uploaded=uploaded_count,
        )

    @staticmethod
    def _upload_customer_s3(ext: dict[str, Any], key: str, file_path: Path) -> None:
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError(
                "Uploading to customer S3 requires boto3 (`pip install boto3`) "
                "using your local AWS credentials."
            ) from exc
        bucket = str(ext.get("bucket") or "").strip()
        if not bucket:
            raise RuntimeError("Customer S3 external_storage metadata is missing 'bucket'")
        kwargs: dict[str, Any] = {}
        if ext.get("region"):
            kwargs["region_name"] = str(ext["region"])
        if ext.get("endpoint"):
            kwargs["endpoint_url"] = str(ext["endpoint"])
        client = boto3.client("s3", **kwargs)
        client.upload_file(str(file_path), bucket, key)


class CaptureManager:
    """High-level coordinator uniting local ``SpoolEpisode`` capture and ``SpoolUploader``.

    Designed for both ``AttendedTaskRunner`` (autonomous + takeover runs) and standalone
    cold-start demo collection (``dreamscale record``).
    """

    def __init__(
        self,
        *,
        spool_root: Path | None = None,
        dataset_ref: str | None = None,
        api_url: str | None = None,
        api_key: str | None = None,
        keep_local: bool = False,
        active_bytes_per_sec: int = DEFAULT_ACTIVE_BYTES_PER_SEC,
        idle_bytes_per_sec: int | None = None,
        print_fn: Callable[[str], None] | None = None,
        uploader: SpoolUploader | None = None,
    ) -> None:
        self.spool_root = Path(spool_root or default_spool_root()).expanduser().resolve()
        self.spool_root.mkdir(parents=True, exist_ok=True)
        self.dataset_ref = dataset_ref
        self.keep_local = bool(keep_local)
        self.print_fn = print_fn

        if uploader is not None:
            self.uploader: SpoolUploader | None = uploader
        elif api_url and api_key:
            self.uploader = SpoolUploader(
                self.spool_root,
                api_url=api_url,
                api_key=api_key,
                active_bytes_per_sec=active_bytes_per_sec,
                idle_bytes_per_sec=idle_bytes_per_sec,
                on_uploaded=self._report_uploaded,
            )
        else:
            self.uploader = None
        self._started = False

    def _report_uploaded(self, outcome: UploadOutcome) -> None:
        if self.print_fn is not None:
            qc = f" (QC: {outcome.qc_status})" if outcome.qc_status else ""
            self.print_fn(
                f"Uploaded episode {outcome.client_episode_id} -> {outcome.dataset_ref}{qc}."
            )

    def bind_dataset(self, dataset_ref: str | None) -> None:
        if dataset_ref and not self.dataset_ref:
            self.dataset_ref = dataset_ref

    def set_inference_active(self, active: bool) -> None:
        if self.uploader is not None:
            self.uploader.set_inference_active(active)

    def start_episode(
        self,
        *,
        task: str = "",
        fps: float = 30.0,
        policy_id: str | None = None,
        policy_version: int | None = None,
        deployment_id: str | None = None,
        session_id: str | None = None,
        robot_id: str | None = None,
        default_source_kind: str = "autonomous",
        metadata: dict[str, Any] | None = None,
    ) -> SpoolEpisode:
        if self.uploader is not None and not self._started:
            self.uploader.start()
            self._started = True
        return SpoolEpisode(
            self.spool_root,
            dataset_ref=self.dataset_ref,
            policy_id=policy_id,
            policy_version=policy_version,
            deployment_id=deployment_id,
            session_id=session_id,
            robot_id=robot_id,
            task=task,
            fps=fps,
            default_source_kind=default_source_kind,
            keep_local=self.keep_local,
            metadata=metadata,
        )

    def finish_episode(
        self,
        episode: SpoolEpisode,
        *,
        outcome: str | None = None,
    ) -> EpisodeSummary:
        summary = episode.finish(outcome=outcome, dataset_ref=self.dataset_ref)
        if summary.status == "ready" and self.uploader is not None:
            if not self._started:
                self.uploader.start()
                self._started = True
            self.uploader.notify()
        return summary

    def close(self, *, drain_timeout_s: float = 10.0) -> None:
        if self.uploader is not None:
            self.uploader.stop(drain_timeout_s=drain_timeout_s)
