"""
What `seq eval replay`'s page asks for, and where each comes from: an eval's, from the gateway with the CLI's own key
(GatewaySource); a file `seq eval report --replays` saved, from the disk alone (FileSource).

Each answers the player's requests as bytes - report and details as the gateway's JSON, an episode's replay, a scene
by its sha256, a recording, what the policy was sent, the cameras the benchmark's observation carries - and raises
Missing for one there is none of.
"""
from __future__ import annotations

import json
import os
import pathlib
import re

from seq._replay_player.read import header
from sequence_ai._core.names import segment

SHA = re.compile(r"[0-9a-f]{64}")


class Missing(Exception):
    """What the page asked for is not there."""


class GatewaySource:
    """An eval's, as the console's page reads it - the same routes - through the CLI's client."""

    def __init__(self, client, eval_id: str) -> None:
        self.client = client
        self.eval_id = eval_id
        self._path = f"/v1/eval/{segment(eval_id)}"
        self._details: dict | None = None

    def _bytes(self, path: str, timeout: float = 120.0) -> bytes:
        return self.client._get("GET", path, timeout=timeout).content

    def report(self) -> bytes:
        return self._bytes(self._path, 60.0)

    def details(self) -> bytes:
        body = self._bytes(f"{self._path}/details")
        self._details = json.loads(body)
        return body

    def replay(self, ep: int) -> bytes:
        return self.client.replay(self.eval_id, int(ep))

    def scene(self, sha: str) -> bytes:
        return self.client.scene(self.eval_id, sha)

    def video(self, ep: int) -> bytes:
        return self._bytes(f"{self._path}/videos/{int(ep)}.mp4")

    def record(self, ep: int) -> bytes:
        return self._bytes(f"{self._path}/episodes/{int(ep)}/record")

    def cameras(self) -> bytes:
        details = self._details if self._details is not None else json.loads(self.details())
        bench = (details.get("manifest") or {}).get("benchmark")
        if not bench:
            raise Missing("the eval names no benchmark")
        return self._bytes(f"/v1/benchmarks/{segment(str(bench))}/io", 60.0)


class FileSource:
    """One episode's .seqreplay on the disk, with its scene where `seq eval report --replays` puts it (scenes/<sha>.glb
    beside the file): an eval of that one episode, nothing fetched."""

    def __init__(self, path: str | os.PathLike) -> None:
        self.path = pathlib.Path(path)
        self.data = self.path.read_bytes()
        head = header(self.data)
        self.episode = head.get("episode") if isinstance(head.get("episode"), dict) else {}
        named = re.search(r"-(\d+)\.seqreplay$", self.path.name)
        given = self.episode.get("index")
        self.index = int(given) if isinstance(given, int) and given >= 0 else int(named.group(1)) if named else 0
        scene = head.get("scene") if isinstance(head.get("scene"), dict) else {}
        sha = str(scene.get("sha256") or "")
        self.sha = sha if SHA.fullmatch(sha) else None
        self.scene_path = next((p for p in (self.path.parent / "scenes" / f"{self.sha}.glb",
                                            self.path.parent / f"{self.sha}.glb") if p.is_file()), None) \
            if self.sha else None
        self.frames = head.get("frames")

    def report(self) -> bytes:
        return json.dumps({"eval_id": self.path.stem, "status": "completed", "metrics": {}}).encode()

    def details(self) -> bytes:
        ep = self.episode
        return json.dumps({
            "episodes": [{"index": self.index, "task": ep.get("task") or "", "seed": ep.get("seed"),
                          "steps": ep.get("steps"), "replay": True, "scene_sha256": self.sha,
                          "scene_bytes": self.scene_path.stat().st_size if self.scene_path else None,

                          **({"success": ep["success"]} if isinstance(ep.get("success"), bool) else {})}],
            "episodes_total": 1, "manifest": {}, "replay": {"state": "done"},
        }).encode()

    def replay(self, ep: int) -> bytes:
        return self.data

    def scene(self, sha: str) -> bytes:
        if sha != self.sha or self.scene_path is None:
            raise Missing(f"no scene {sha[:12]} beside {self.path.name} (scenes/<sha256>.glb, as `seq eval report "
                          "--replays` saves it)")
        return self.scene_path.read_bytes()

    def video(self, ep: int) -> bytes:
        raise Missing("a file has no recording")

    def record(self, ep: int) -> bytes:
        raise Missing("a file has no recording")

    def cameras(self) -> bytes:
        raise Missing("a file names no benchmark")
