"""Recording helpers for CUA agents."""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from use_computer.core.sandbox import AsyncSandbox


class RecordingMixin:
    async def start_recording(self: Any, sandbox: AsyncSandbox) -> None:
        try:
            result = await sandbox.recording.start(name="trial")
            self._recording_id = result.id
            self.logger.info(f"Recording started: {self._recording_id}")
        except Exception as e:
            self.logger.warning(f"Failed to start recording: {e}")

    async def stop_recording(self: Any, sandbox: AsyncSandbox) -> None:
        if not self._recording_id:
            return
        await asyncio.sleep(3.0)
        rec_path = self.logs_dir / "recording.mp4"

        try:
            info = await sandbox.recording.stop(self._recording_id)
            self.logger.info(
                f"Recording stopped: id={self._recording_id} "
                f"name={info.name!r} filename={info.filename!r} "
                f"server_size={info.file_size}B "
                f"({info.file_size / (1024 * 1024):.2f} MB)"
            )
            if info.file_size <= 0:
                raise RuntimeError("server recording is empty")

            await asyncio.sleep(2)

            await self._download_recording(sandbox, rec_path)
        except Exception as e:
            self.logger.warning(f"Recording save failed: {type(e).__name__}: {e}")
            try:
                await self._download_recording(sandbox, rec_path)
            except Exception as fallback:
                self.logger.warning(
                    f"Recording fallback download failed: {type(fallback).__name__}: {fallback}"
                )
                self._write_screenshot_recording(
                    rec_path,
                    reason=(
                        f"server recording failed: {type(e).__name__}: {e}; "
                        f"download fallback failed: {type(fallback).__name__}: {fallback}"
                    ),
                )

    async def _download_recording(self: Any, sandbox: AsyncSandbox, rec_path) -> None:
        self.logger.info(f"Downloading recording → {rec_path}")
        t_dl = time.monotonic()
        await sandbox.recording.download(self._recording_id, str(rec_path), timeout=180.0)
        dl_elapsed = time.monotonic() - t_dl
        local_size = rec_path.stat().st_size
        if local_size <= 0:
            raise RuntimeError("downloaded recording is empty")
        self.logger.info(
            f"Recording saved: {rec_path} "
            f"local_size={local_size}B ({local_size / (1024 * 1024):.2f} MB) "
            f"download_elapsed={dl_elapsed:.1f}s"
        )

    def _write_screenshot_recording(self: Any, rec_path: Path, reason: str) -> bool:
        image_dir = self.logs_dir / "images"
        images = sorted(image_dir.glob("*.png")) if image_dir.exists() else []
        if not images:
            self.logger.warning("Screenshot recording fallback skipped: no saved screenshots")
            return False

        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            self.logger.warning("Screenshot recording fallback skipped: ffmpeg not found")
            return False

        try:
            from PIL import Image
        except Exception as e:
            self.logger.warning(f"Screenshot recording fallback skipped: Pillow unavailable: {e}")
            return False

        rec_path.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.monotonic()
        try:
            with Image.open(images[0]) as first:
                width, height = first.size
            width -= width % 2
            height -= height % 2
            if width <= 0 or height <= 0:
                raise RuntimeError(f"invalid screenshot size {width}x{height}")

            with tempfile.TemporaryDirectory(prefix="use-computer-recording-") as tmp:
                tmp_dir = Path(tmp)
                frame_count = 0
                for idx, src in enumerate(images, start=1):
                    with Image.open(src) as img:
                        frame = img.convert("RGB")
                        if frame.size != (width, height):
                            frame = frame.resize((width, height))
                        frame.save(tmp_dir / f"frame{idx:06d}.png")
                    frame_count += 1

                if frame_count == 1:
                    shutil.copyfile(tmp_dir / "frame000001.png", tmp_dir / "frame000002.png")
                    frame_count = 2

                cmd = [
                    ffmpeg,
                    "-y",
                    "-loglevel",
                    "error",
                    "-framerate",
                    "1",
                    "-i",
                    str(tmp_dir / "frame%06d.png"),
                    "-vf",
                    "format=yuv420p",
                    "-movflags",
                    "+faststart",
                    str(rec_path),
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    raise RuntimeError(
                        result.stderr.strip() or f"ffmpeg exited {result.returncode}"
                    )

            local_size = rec_path.stat().st_size
            if local_size <= 0:
                raise RuntimeError("ffmpeg wrote an empty recording")

            meta = {
                "source": "screenshots",
                "reason": reason,
                "frames": len(images),
                "width": width,
                "height": height,
                "file_size": local_size,
                "elapsed_sec": round(time.monotonic() - t0, 3),
            }
            (self.logs_dir / "recording.json").write_text(json.dumps(meta, indent=2))
            self.logger.info(
                f"Screenshot recording fallback saved: {rec_path} "
                f"frames={len(images)} local_size={local_size}B "
                f"({local_size / (1024 * 1024):.2f} MB)"
            )
            return True
        except Exception as e:
            self.logger.warning(f"Screenshot recording fallback failed: {type(e).__name__}: {e}")
            return False
