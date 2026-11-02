from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class SimArtifactRecorder:
    run_dir: Path
    fps: int = 10
    video_writer: Callable[[Path, np.ndarray, int], None] | None = None
    frames: list[np.ndarray] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def start(self) -> None:
        if self.run_dir.exists():
            if not self.run_dir.is_dir():
                raise NotADirectoryError(f"artifact path is not a directory: {self.run_dir}")
            if any(self.run_dir.iterdir()):
                raise FileExistsError(
                    f"artifact directory is not empty: {self.run_dir}"
                )
        else:
            self.run_dir.mkdir(parents=True, exist_ok=False)
        self.event({"type": "run.started", "time_s": 0.0})

    def frame(
        self,
        frame: Any,
        step: int,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        array = np.ascontiguousarray(np.asarray(frame, dtype=np.uint8))
        self.frames.append(array)
        payload = {
            "type": "sim.frame",
            "frame_index": len(self.frames) - 1,
            "step": int(step),
            **(metadata or {}),
        }
        self.event(payload)

    def buffer(self, payload: dict[str, Any]) -> None:
        self.event({"type": "buffer.health", **payload})

    def policy_timing(self, payload: dict[str, Any]) -> None:
        self.event({"type": "policy.timing", **payload})

    def event(self, payload: dict[str, Any]) -> None:
        self.events.append(dict(payload))

    def finish(self, *, summary: dict[str, Any]) -> None:
        events = [*self.events, {"type": "run.finished", "done": bool(summary.get("done"))}]
        if self.frames:
            frames = np.stack(self.frames)
            if self.video_writer is not None:
                self.video_writer(self.run_dir / "rollout.mp4", frames, self.fps)
            else:
                import imageio.v3 as iio

                iio.imwrite(self.run_dir / "rollout.mp4", frames,
                            plugin="pyav", codec="libx264", fps=self.fps)
        (self.run_dir / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.run_dir / "events.jsonl").write_text(
            "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
            encoding="utf-8",
        )
        self.events = events

    def fail(
        self,
        error: BaseException | str,
        summary: dict[str, Any] | None = None,
    ) -> None:
        error_text = str(error)
        failed_summary = dict(summary or {})
        failed_summary["done"] = False
        failed_summary["error"] = error_text
        events = [*self.events, {"type": "run.failed", "error": error_text}]
        (self.run_dir / "summary.json").write_text(
            json.dumps(failed_summary, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.run_dir / "events.jsonl").write_text(
            "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
            encoding="utf-8",
        )
        self.events = events
