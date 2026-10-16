"""Publish Miles' full dashboard through Probe's ordinary artifact upload door.

Only the training host reads its trusted native dumps. Hosted readers receive
inert JSON, including the exact token diagnostics produced by Miles' reader.
The background worker never raises into the training loop. Its local cursor is
advanced only after a synchronous, confirmed upload, so failed exports retry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import os
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
PREFIX = "miles-dashboard/"
STREAMS = (
    "metrics",
    "phases",
    "topology",
    "gpu_util",
    "engine_series",
    "trajectories",
    "gpu_processes",
    "data_buffer",
)
CHUNK_BYTES = 2 * 1024 * 1024
SHARD_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 16 * 1024 * 1024


def _safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe(item) for item in value]
    return value


def _json_bytes(value) -> bytes:
    return json.dumps(
        _safe(value), separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def _source_stamp(root: Path, step: int, evaluation: bool) -> str:
    stem = f"eval_{step}" if evaluation else str(step)
    paths = [root / "rollout_data" / f"{stem}.pt", root / "trajectory" / f"{stem}.jsonl"]
    if not evaluation:
        paths.extend(sorted((root / "train_data").glob(f"{step}_*.pt")))
    records = [
        (str(path.relative_to(root)), path.stat().st_size, path.stat().st_mtime_ns)
        for path in paths
        if path.is_file()
    ]
    return hashlib.sha256(_json_bytes(records)).hexdigest()[:20]


class DashboardPublisher:
    """Incremental publisher; reusable by the worker and offline repair command."""

    def __init__(self, run: Any, dump_dir: Path, state_dir: Path):
        self.run = run
        self.root = Path(dump_dir)
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._reader = None

    def _upload(
        self, name: str, raw: bytes, *, info: dict | None = None, step: int | None = None
    ) -> None:
        if len(raw) > MAX_FILE_BYTES:
            raise ValueError(f"dashboard shard {name} exceeds 16 MiB")
        digest = hashlib.sha256(raw).hexdigest()
        path = self.state_dir / (digest + (".jsonl" if name.endswith(".jsonl") else ".json"))
        path.write_bytes(raw)
        try:
            result = self.run.log_artifact(
                name,
                path=str(path),
                kind="miles_dashboard",
                content_type="application/x-ndjson"
                if name.endswith(".jsonl")
                else "application/json",
                step_index=step,
                meta={"rl_dashboard": info or {}},
                strict=True,
                sync=True,
            )
            # Exclusions and the upload inspection gate can refuse an upload
            # without throwing. A path reference is not remotely readable.
            if result is None or (
                result.get("is_reference")
                if isinstance(result, dict)
                else getattr(result, "is_reference", False)
            ):
                raise RuntimeError(f"dashboard artifact was not uploaded: {name}")
        finally:
            path.unlink(missing_ok=True)

    def sync_once(self) -> None:
        from probe.integrations.miles import _file_lock, _read_json, _write_json_atomic

        with _file_lock(self.state_dir / ".publish.lock"):
            state_path = self.state_dir / "state.json"
            state = _read_json(state_path) if state_path.is_file() else {"files": {}, "steps": {}}
            self._streams(state, lambda: _write_json_atomic(state_path, state))
            self._rollouts(state, lambda: _write_json_atomic(state_path, state))
            self._meta()

    def _streams(self, state: dict, commit) -> None:
        dashboard = self.root / "dashboard"
        for stream in STREAMS:
            paths = [dashboard / f"{stream}.jsonl", *sorted((dashboard / stream).glob("*.jsonl"))]
            for path in paths:
                if not path.is_file():
                    continue
                source = str(path.relative_to(dashboard))
                entry = state["files"].get(source, {"offset": 0, "epoch": 0})
                if path.stat().st_size < entry["offset"]:
                    entry = {"offset": 0, "epoch": entry["epoch"] + 1}
                with path.open("rb") as handle:
                    handle.seek(entry["offset"])
                    while True:
                        raw = handle.read(CHUNK_BYTES)
                        if not raw:
                            break
                        boundary = raw.rfind(b"\n")
                        if boundary < 0:
                            # Leave a partial tail for the next pass. Never
                            # advance over a producer's unfinished JSON line.
                            if len(raw) == CHUNK_BYTES:
                                raise ValueError(f"dashboard record exceeds 2 MiB in {source}")
                            break
                        raw = raw[: boundary + 1]
                        end = entry["offset"] + len(raw)
                        records = [json.loads(line) for line in raw.splitlines()]
                        times = [
                            float(record[key])
                            for record in records
                            for key in ("ts", "t0", "t1")
                            if isinstance(record.get(key), (int, float)) and record[key] >= 0
                        ]
                        source_id = hashlib.sha256(source.encode()).hexdigest()[:16]
                        # Zero-padded offsets preserve stream order when the
                        # hosted engine concatenates immutable segments.
                        name = f"{PREFIX}streams/{stream}/{source_id}-{entry['epoch']:04d}-{entry['offset']:020d}.jsonl"
                        self._upload(
                            name,
                            raw,
                            info={
                                "stream": stream,
                                "source": source,
                                "offset": entry["offset"],
                                "t0": min(times) if times else None,
                                "t1": None
                                if any(record.get("t1") == -1 for record in records)
                                else (max(times) if times else None),
                            },
                        )
                        entry = {**entry, "offset": end}
                        state["files"][source] = entry
                        commit()
                        handle.seek(end)

    def _rollouts(self, state: dict, commit) -> None:
        if not (self.root / "rollout_data").is_dir():
            return
        from miles.dashboard.dump_reader import DumpReader

        self._reader = DumpReader(
            self.root, cache_dir=self.state_dir / "reader-cache", tensor_lru=1
        )
        ids = self._reader.rollout_ids()
        for evaluation, steps in ((False, ids.train), (True, ids.eval)):
            for step in steps:
                key = f"{'eval' if evaluation else 'train'}:{step}"
                signature = _source_stamp(self.root, step, evaluation)
                if state["steps"].get(key) == signature:
                    continue
                document = self._step(step, evaluation, signature)
                if _source_stamp(self.root, step, evaluation) != signature:
                    continue  # the training side finished another shard meanwhile
                name = f"{PREFIX}rollouts/{'eval' if evaluation else 'train'}/{step}/summary.json"
                self._upload(
                    name,
                    _json_bytes(document),
                    step=step,
                    info={
                        "type": "summary",
                        "step": step,
                        "evaluation": evaluation,
                        "aggregates": document["aggregates"],
                    },
                )
                state["steps"][key] = signature
                commit()

    def _step(self, step: int, evaluation: bool, signature: str) -> dict:
        rows = self._reader.summary(step, evaluation=evaluation).to_dicts()
        groups = self._reader.groups(step, evaluation=evaluation).to_dicts()
        files = {}
        shard = {}
        size = 0
        shard_index = 0

        def flush():
            nonlocal shard, size, shard_index
            if not shard:
                return
            name = f"{PREFIX}rollouts/{'eval' if evaluation else 'train'}/{step}/samples-{signature}-{shard_index}.json"
            self._upload(name, _json_bytes({"schema_version": 1, "samples": shard}), step=step)
            for sample_key in shard:
                files[sample_key] = name
            shard_index += 1
            shard, size = {}, 0

        for row in rows:
            index, occurrence = int(row["sample_index"]), int(row.get("sample_occurrence", 0))
            sample = {"messages": None, "tokens": None}
            try:
                sample["messages"] = self._reader.trajectory_messages(
                    step, index, sample_occurrence=occurrence, evaluation=evaluation
                )
            except (FileNotFoundError, KeyError):
                pass  # no conversation is a supported native Miles state
            sample["tokens"] = self._reader.tokens(
                step, index, sample_occurrence=occurrence, evaluation=evaluation
            )
            encoded_size = len(_json_bytes(sample))
            if encoded_size > MAX_FILE_BYTES - 1024:
                raise ValueError(
                    f"token diagnostics for sample {index} exceed the export shard limit"
                )
            if size + encoded_size > SHARD_BYTES:
                flush()
            shard[f"{index}:{occurrence}"] = sample
            size += encoded_size
        flush()
        # The metadata index carries native aggregate values, so a scalar
        # chart never downloads every step's sample or token files.
        frame = self._reader.summary(step, evaluation=evaluation)
        group_frame = self._reader.groups(step, evaluation=evaluation)
        aggregates = dict(
            rollout_id=step,
            n_samples=frame.height,
            reward_mean=frame["raw_reward"].mean(),
            reward_std=frame["raw_reward"].std(),
            response_length_mean=frame["response_length"].mean(),
            truncated_frac=frame["truncated"].cast(float).mean(),
            zero_std_group_frac=group_frame["zero_std"].cast(float).mean(),
            mean_abs_lp_diff=frame["mean_abs_lp_diff"].mean(),
            mean_entropy=frame["mean_entropy"].mean(),
            mixed_version_frac=frame["mixed_version"].cast(float).mean(),
        )
        return {
            "schema_version": 1,
            "rows": rows,
            "groups": groups,
            "sample_files": files,
            "aggregates": _safe(aggregates),
        }

    def _meta(self) -> None:
        path = self.root / "dashboard" / "meta.json"
        if not path.is_file():
            return
        # Query the native store for its authoritative global time bounds;
        # high-rate partitions are still read lazily by the hosted engine.
        from miles.dashboard.store import MetricStore

        store = MetricStore.load(self.root / "dashboard")
        catalog = self.root / "dashboard" / "lane_catalog.json"
        document = {
            "schema_version": 1,
            "has_tokenizer": (self.root / "tokenizer").is_dir(),
            "meta": json.loads(path.read_text()),
            "lane_catalog": json.loads(catalog.read_text()) if catalog.is_file() else None,
            "time_range": store.time_range(),
        }
        raw = _json_bytes(document)
        stamp_path = self.state_dir / "meta.sha256"
        digest = hashlib.sha256(raw).hexdigest()
        if stamp_path.is_file() and stamp_path.read_text() == digest:
            return
        self._upload(PREFIX + "meta.json", raw)
        stamp_path.write_text(digest)


class DashboardCapture:
    def __init__(
        self,
        *,
        run_id: str,
        dump_dir: Path,
        state_dir: Path,
        base_url: str | None,
        interval: float = 15,
    ):
        self.run_id, self.dump_dir, self.state_dir = run_id, dump_dir, state_dir
        self.base_url, self.interval = base_url, max(5, interval)
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._loop, name="probe-miles-dashboard", daemon=True
        )

    def start(self):
        self._thread.start()

    def close(self, timeout: float = 5):
        self._stop.set()
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def _loop(self):
        from probe.sdk import Client, Run

        client = None
        publisher = None
        try:
            while True:
                try:
                    if publisher is None:
                        if client is not None:
                            client.close()
                        client = Client(
                            base_url=self.base_url,
                            token=os.environ.get("PROBE_TOKEN"),
                            fail_open=False,
                        )
                        run = Run(client, client.get_run(self.run_id))
                        publisher = DashboardPublisher(run, self.dump_dir, self.state_dir)
                    publisher.sync_once()
                except Exception:
                    logger.warning(
                        "Miles dashboard export is pending; local source data and cursors are retained for retry",
                        exc_info=True,
                    )
                if self._stop.wait(self.interval):
                    try:
                        if publisher is not None:
                            publisher.sync_once()
                    except Exception:
                        logger.warning(
                            "Final Miles dashboard export is pending; rerun the dashboard repair command to publish retained dumps",
                            exc_info=True,
                        )
                    break
        finally:
            if client is not None:
                client.close()


def start_capture(args, run_id: str, queue_dir: Path) -> DashboardCapture | None:
    dump_dir = getattr(args, "dump_details", None)
    if not dump_dir or not getattr(args, "probe_dashboard", True):
        return None
    capture = DashboardCapture(
        run_id=run_id,
        dump_dir=Path(dump_dir),
        state_dir=queue_dir / "dashboard-export",
        base_url=getattr(args, "probe_base_url", None),
        interval=getattr(args, "probe_dashboard_interval_sec", 15),
    )
    capture.start()
    return capture


def main():
    parser = argparse.ArgumentParser(
        description="Publish or repair a Miles dashboard export for an existing Probe run."
    )
    parser.add_argument("--run", required=True)
    parser.add_argument("--dump-details", required=True)
    parser.add_argument("--base-url")
    parser.add_argument("--follow", action="store_true")
    args = parser.parse_args()
    from probe.sdk import Client, Run

    with Client(base_url=args.base_url, fail_open=False) as client:
        run = Run(client, client.get_run(args.run))
        publisher = DashboardPublisher(
            run, Path(args.dump_details), Path(args.dump_details) / ".probe-dashboard-export"
        )
        while True:
            publisher.sync_once()
            if not args.follow:
                break
            threading.Event().wait(15)


if __name__ == "__main__":
    main()
