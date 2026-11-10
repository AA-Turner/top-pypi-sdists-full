"""
`seq policy data export` — field data from a deployment's real robots, for fine-tuning.

In one sentence: its capture setting (`seq policy set <name> capture=on`, seq/settings_cli.py) has its workers keep
every episode whole - each step's observation as the robot sent it, frames and all, each act's answer, and what the
policy kept in episode.state at its end → robots label how an episode went with `policy.label(success=...)` →
`seq policy data export <name> --format lerobot --out DIR` downloads the kept files through the platform and writes a
LeRobot v3.0 dataset: a frame for every step a robot observed (policy.observe) - its marked items (sequence_ai.Video,
Depth, Tactile) decoded as the worker decoded them, each camera frame an image `observation.images.<key>`, every other
number an array `observation.<key>`, the key as the robot sent it less an "observation" of its own in front and with
"/" made "." - with the action its act's answer gives that step; the policy's declared hz as the dataset's fps (its
robots' own pace beside it, observed_fps); each episode's instruction - the first a robot sent under instruction, task,
prompt or language_instruction, else under a key that holds one of those words - as its task, and its label as
`next.success` on its last frame.

WHY a frame a step: the worker keeps every observation a robot posts
, so the dataset has every frame the robot saw, not only those it asked for actions at. An act's answer is placed
among the steps by its `step` - the observations before it: the answer to an act after step k's observation gives step
k its first row, step k + 1 its second, and so on; a step past the answer's last row keeps that row, and a step before
the first answer is given that answer's first row. `--format jsonl` keeps every captured field as it was sent.


A deleted deployment's captured data stays its owner's, a dataset of its own named `capture:<name>-<id8>`
(`seq volume ls`): `seq policy data export capture:<name>-<id8>` reads it the same way, with no deployment behind it.

"""
from __future__ import annotations

import base64
import json
import os
import re
from collections import defaultdict
from typing import Any

from seq import safe_path, storage_note
from seq.deployments_cli import _call
from seq.errors import MissingPackage, raise_for, unreachable
from sequence_ai._core.direct_observe import PROMPT_KEYS
from sequence_ai._core.names import file_path, segment
from sequence_ai.errors import InvalidRequest, NotFound
from seq._account import auth_headers, credential




LEROBOT_VERSION = "v3.0"
_CHUNK = 1000


_DATA_FILE_MB = 100

_QUANTILES = ((0.01, "q01"), (0.10, "q10"), (0.50, "q50"), (0.90, "q90"), (0.99, "q99"))

_STAT_FRAMES = 100

_TASKS_PANDAS = {"index_columns": ["task"], "column_indexes": [{"name": None, "field_name": None,
                 "pandas_type": "unicode", "numpy_type": "object", "metadata": {"encoding": "UTF-8"}}],
                 "columns": [{"name": "task_index", "field_name": "task_index", "pandas_type": "int64",
                              "numpy_type": "int64", "metadata": None},
                             {"name": "task", "field_name": "task", "pandas_type": "unicode", "numpy_type": "object",
                              "metadata": None}],
                 "attributes": {}, "creator": {"library": "pyarrow", "version": "14.0.0"}, "pandas_version": "2.0.0"}




_DATASET = re.compile(r"capture:[A-Za-z0-9][A-Za-z0-9._-]{0,72}")


def _files(name: str) -> str:
    """Where `name`'s captured files are listed: a dataset's own, else its deployment's."""
    if not name.startswith("capture:"):
        return f"/v1/deployments/{segment(name)}/capture/files"
    if not _DATASET.fullmatch(name):
        raise InvalidRequest(f"{name!r} is not a dataset: `seq volume ls` lists yours (capture:<name>-<id8>)")
    return f"/v1/volumes/{name}/files"


def _download(name: str, path: str, base_url: str | None) -> bytes:
    import httpx

    from seq._gateway import DEFAULT_BASE_URL

    base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    key = credential(None, base)
    from seq._http import RetryReads

    try:
        with httpx.Client(headers=auth_headers(key), timeout=120, transport=RetryReads()) as client:
            r = client.get(f"{base}{_files(name)}/{file_path(path)}")
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    raise_for(r)
    return r.content


def _listing(name: str, base_url: str | None) -> list[dict]:
    return _listed(name, base_url)[0]


def _listed(name: str, base_url: str | None) -> tuple[list[dict], float | None]:
    """`name`'s captured files, and the hz its policy declares where the platform says it beside them (a deployment's
    listing; a dataset's says none)."""
    try:
        got = _call("GET", _files(name), base_url)
        hz = got.get("hz")
        return got["files"], (float(hz) if isinstance(hz, (int, float)) and not isinstance(hz, bool) and hz > 0
                              else None)
    except NotFound as exc:

        if not name.startswith("capture:") and not exc.hint:
            exc.hint = (f"a deleted deployment's captured data is kept as a dataset: `seq volume ls` lists it as "
                        f"capture:{name}-<id8>, which `seq policy data export` reads")
        raise


def load(name: str, base_url: str | None = None, *, fetch=None,
         listing: list[dict] | None = None) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """Every captured sample of the deployment grouped by episode (in time order), and every episode's label - what
    is under ckpt/ left out: the states saved as its episodes ran, a standby's to read back by (each episode's
    state.json, its keys' objects, each a value as it is, and its record's chunks), none of them a record."""
    fetch = fetch or (lambda path: _download(name, path, base_url))
    files = listing if listing is not None else _listing(name, base_url)
    episodes: dict[str, list[dict]] = defaultdict(list)
    labels: dict[str, dict] = {}
    for f in files:
        path = f["path"]
        if path.startswith("ckpt/"):
            continue
        data = fetch(path)
        if path.startswith("labels/") and path.endswith(".json"):
            label = json.loads(data)
            labels[label.get("episode_id") or path[len("labels/"):-len(".json")]] = label
            continue
        for line in data.splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get("kind") == "label":


                    labels.setdefault(row.get("episode_id"), {k: row.get(k) for k in
                                                              ("episode_id", "success", "notes")})
                    continue
                episodes[row.get("episode_id") or f"rid-{row.get('rid')}"].append(row)
    for rows in episodes.values():
        rows.sort(key=lambda r: r.get("ts") or 0)
    return dict(episodes), labels


def _capturing(name: str, base_url: str | None) -> bool:
    """Whether the deployment's capture switch is on; False when it cannot be read: an export's words, never its failure."""
    try:
        rows = _call("GET", f"/v1/deployments/{segment(name)}/settings", base_url).get("settings") or []
    except Exception:
        return False
    return any(r.get("key") == "capture" and r.get("value") == "on" for r in rows)


def _why_none(name: str, base_url: str | None) -> str:
    """What an export of a deployment says when it holds no episode. An account at its storage limit first: its capture
    being on, or its robot a teleop one, keeps nothing then, and nothing else says so to whoever looks here. What it
    cannot tell is why these episodes are missing, so it says how the account stands now.
    
"""
    full = storage_note.full_now(base_url)
    if full:
        return f"{name}: no episodes: {full}"
    if _capturing(name, base_url):
        return f"{name}: nothing captured yet: capture is on, and no robot has run an episode since"
    return f"{name}: nothing captured yet (`seq policy set {name} capture=on`)"


def export(name: str, out: str, *, fmt: str = "lerobot", base_url: str | None = None, echo=print,
           fetch=None, listing: list[dict] | None = None, hz: float | None = None) -> dict:
    """`seq policy data export`: the kept files as they are (jsonl), or a LeRobot dataset of them at the policy's
    declared hz - `hz`, else what the platform's listing says. `listing` and `fetch` stand in for the platform."""


    live = listing is None and not name.startswith("capture:")
    if listing is None and fmt != "jsonl":
        listing, said_hz = _listed(name, base_url)
        hz = hz or said_hz
    if fmt == "jsonl":
        files = listing if listing is not None else _listing(name, base_url)
        fetch = fetch or (lambda path: _download(name, path, base_url))


        dests = [(f, safe_path.under(out, f["path"])) for f in files]
        for f, dest in dests:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(fetch(f["path"]))
        echo(f"wrote {len(files)} file(s) to {out}")
        if live:

            kept = any(not f["path"].startswith("labels/") for f in files)
            said = storage_note.full_now(base_url) if kept else _why_none(name, base_url)
            if said:
                echo(said)
        return {"files": len(files)}
    episodes, labels = load(name, base_url, fetch=fetch, listing=listing)
    if not episodes:
        echo(f"{name}: no episodes in this dataset" if name.startswith("capture:") else
             _why_none(name, base_url) if live else f"{name}: nothing captured yet (`seq policy set {name} capture=on`)")
        return {"episodes": 0, "frames": 0}
    summary = write_steps(episodes, labels, out, hz=hz)
    echo(f"wrote a LeRobot {LEROBOT_VERSION} dataset to {out}: {summary['episodes']} episode(s), "
         f"{summary['frames']} frame(s), {summary['labelled']} labelled")
    if summary.get("fps_from") == "observed":

        echo(f"its fps, {summary['fps']:g}, is the pace its robots observed at: the platform did not say its policy's hz")
    full = storage_note.full_now(base_url) if live else None
    if full:
        echo(full)
    return summary


def _parquet():
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        raise MissingPackage("the LeRobot export writes parquet, which needs pyarrow",
                             hint="pip install 'sequence-ai[data]'") from None
    return pa, pq


def _arrow_type(pa, feature: dict):
    """A feature's column as LeRobot's own writer types it: an image a struct of its bytes, a vector a list of its
    length, a 2-D array a list of lists (datasets' Array2D), a single number a value."""
    shape = list(feature.get("shape") or [1])
    if feature["dtype"] == "image":
        return pa.struct([("bytes", pa.binary()), ("path", pa.string())])
    value = {"float32": pa.float32(), "int64": pa.int64(), "bool": pa.bool_()}[feature["dtype"]]
    if shape == [1]:
        return value
    return pa.list_(value, shape[0]) if len(shape) == 1 else pa.list_(pa.list_(value))


def _hf_feature(feature: dict) -> dict:
    """The feature as datasets names it, in the data files' own metadata, for a reader that takes it from there."""
    shape = list(feature.get("shape") or [1])
    if feature["dtype"] == "image":
        return {"_type": "Image"}
    if shape == [1]:
        return {"dtype": feature["dtype"], "_type": "Value"}
    if len(shape) == 1:
        return {"feature": {"dtype": feature["dtype"], "_type": "Value"}, "length": shape[0], "_type": "List"}
    return {"shape": shape, "dtype": feature["dtype"], "_type": f"Array{len(shape)}D"}


def _stat_array(values: list, feature: dict):
    """A feature's values over an episode as one array its stats are taken of - an image's pixels in 0-1, from frames
    spread over the episode, a channel last - or None when it holds none."""
    import numpy as np

    if feature["dtype"] == "image":
        import io

        from PIL import Image

        kept = [v["bytes"] for v in values if isinstance(v, dict) and v.get("bytes")]
        if not kept:
            return None
        pick = np.linspace(0, len(kept) - 1, min(len(kept), _STAT_FRAMES)).round().astype(int)
        frames = [np.asarray(Image.open(io.BytesIO(kept[i])).convert("RGB")) for i in sorted(set(pick.tolist()))]
        return np.stack(frames).reshape(-1, 3).astype(np.float64) / 255.0
    kept = [v for v in values if v is not None]
    if not kept:
        return None
    a = np.asarray(kept, dtype=np.float64)
    return a.reshape(len(kept), -1) if a.ndim == 1 else a.reshape(-1, a.shape[-1])


def _stats(a, feature: dict, frames: int) -> dict:
    """min, max, mean, std, count and quantiles of `a`, a value a column (its last axis) - an image's as (3, 1, 1)."""
    import numpy as np

    shape = (3, 1, 1) if feature["dtype"] == "image" else (a.shape[-1],)
    got = {"min": a.min(0), "max": a.max(0), "mean": a.mean(0), "std": a.std(0),
           **{name: np.quantile(a, q, axis=0) for q, name in _QUANTILES}}
    return {**{k: v.reshape(shape).tolist() for k, v in got.items()}, "count": [int(frames)]}


def _write_v30(out: str, episodes: list[tuple[dict, dict]], features: dict, tasks: dict[str, int], fps: float,
               robot_type: str, extra: dict | None = None) -> None:
    """The episodes - each (its columns, its meta) - as a LeRobot v3.0 dataset: their frames in data/chunk-NNN/file-NNN
    .parquet, whole episodes a file; meta/episodes/... a row an episode (where its frames are, its tasks, length and
    stats, with what the platform knows of it - its id, label and operators - beside them); meta/tasks.parquet;
    meta/stats.json over every frame; meta/info.json. `extra`, what LeRobot has no field for, goes in meta/capture.json.
    As LeRobot 0.6.1's own writer lays a dataset out (LeRobotDataset.create, save_episode, finalize)."""
    import numpy as np

    pa, pq = _parquet()
    names = list(features)
    schema = pa.schema([pa.field(n, _arrow_type(pa, features[n])) for n in names],
                       metadata={"huggingface": json.dumps({"info": {"features": {
                           n: _hf_feature(features[n]) for n in names}}})})
    rows: dict[str, list] = defaultdict(list)
    every: dict[str, list] = defaultdict(list)
    pending, size, file_index, start = [], 0, 0, 0

    def flush() -> None:
        nonlocal pending, size, file_index
        if not pending:
            return
        chunk = os.path.join(out, "data", f"chunk-{file_index // _CHUNK:03d}")
        os.makedirs(chunk, exist_ok=True)
        table = pa.Table.from_batches([b for t in pending for b in t.to_batches()], schema=schema)
        pq.write_table(table, os.path.join(chunk, f"file-{file_index % _CHUNK:03d}.parquet"))
        pending, size, file_index = [], 0, file_index + 1

    for cols, meta in episodes:
        length = len(cols["index"])
        arrays = []
        for n in names:
            values = cols.get(n) or [None] * length
            if features[n]["dtype"] != "image" and list(features[n].get("shape") or [1]) == [1]:
                values = [v[0] if isinstance(v, list) and len(v) == 1 else v for v in values]
            arrays.append(pa.array(values, type=schema.field(n).type))
        table = pa.Table.from_arrays(arrays, schema=schema)
        if pending and size + table.nbytes > _DATA_FILE_MB * 2 ** 20:
            flush()
        pending.append(table)
        size += table.nbytes
        rows["episode_index"].append(meta["episode_index"])
        rows["tasks"].append(meta["tasks"])
        rows["length"].append(length)
        rows["data/chunk_index"].append(file_index // _CHUNK)
        rows["data/file_index"].append(file_index % _CHUNK)
        rows["dataset_from_index"].append(start)
        rows["dataset_to_index"].append(start + length)
        start += length
        for n in names:
            a = _stat_array(cols.get(n) or [], features[n])
            if a is None:
                continue
            every[n].append(a)
            for stat, value in _stats(a, features[n], length).items():
                rows[f"stats/{n}/{stat}"].append(value)
        rows["meta/episodes/chunk_index"].append(0)
        rows["meta/episodes/file_index"].append(0)
        for key in ("episode_id", "success", "notes", "operators"):
            rows[key].append(meta.get(key))
    flush()
    total = start
    os.makedirs(os.path.join(out, "meta", "episodes", "chunk-000"), exist_ok=True)
    pq.write_table(pa.table(dict(rows)), os.path.join(out, "meta", "episodes", "chunk-000", "file-000.parquet"))
    order = sorted(tasks.items(), key=lambda kv: kv[1])
    task_table = pa.table({"task_index": pa.array([i for _, i in order], pa.int64()),
                           "task": pa.array([t for t, _ in order], pa.string())})
    pq.write_table(task_table.replace_schema_metadata({"pandas": json.dumps(_TASKS_PANDAS)}),
                   os.path.join(out, "meta", "tasks.parquet"))
    stats = {n: _stats(np.concatenate(arrays), features[n], total) for n, arrays in every.items()}
    with open(os.path.join(out, "meta", "stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    info = {"codebase_version": LEROBOT_VERSION, "robot_type": robot_type, "total_episodes": len(episodes),
            "total_frames": total, "total_tasks": len(tasks), "chunks_size": _CHUNK,
            "data_files_size_in_mb": _DATA_FILE_MB, "video_files_size_in_mb": 200, "fps": fps,
            "splits": {"train": f"0:{len(episodes)}"},
            "data_path": "data/chunk-{chunk_index:03d}/file-{file_index:03d}.parquet", "video_path": None,
            "features": features}
    with open(os.path.join(out, "meta", "info.json"), "w") as f:
        json.dump(info, f, indent=2)
    if extra:
        with open(os.path.join(out, "meta", "capture.json"), "w") as f:
            json.dump(extra, f, indent=2)





_TASK_KEYS = PROMPT_KEYS
_TASK_WORDS = ("instruction", "task", "prompt")
_ACTION_KEYS = ("actions", "action", "rows", "chunk")




_DRIVER_CODE = {"model": 0, "human": 1, "stopped": 2}


def write_steps(episodes: dict[str, list[dict]], labels: dict[str, dict], out: str, *,
                hz: float | None = None) -> dict:
    """The episodes kept a step at a time (the worker's "observe" and "act" lines) as a LeRobot v3.0 dataset: a frame
    for every step observed, each once, in step order - and, in meta/episode_states.jsonl, what each policy kept in
    episode.state at its episode's end (the worker's "state" line), as it was captured: an array or bytes in the tagged
    form JSON carries them in.
    Its fps is `hz`, the policy's declared rate, with the pace its robots observed at beside it (observed_fps): that
    pace was the fps, 2.4 for a policy of hz 10 whose robot observed every 0.4 s - in meta/capture.json, a field
    LeRobot's info has none of."""
    import numpy as np

    _parquet()
    built = []
    states: dict[str, dict] = {}
    for episode_id, rows in episodes.items():
        for r in rows:
            if r.get("kind") == "state":
                states[episode_id] = r
        observed = sorted({r["step"]: r for r in rows if r.get("kind") == "observe" and isinstance(r.get("step"), int)
                           }.items())
        streams, frames = None, []
        for step, r in observed:
            value = _untagged(r.get("observation"))
            if _holds_mark(value):
                marked = _marked()
                streams = streams or marked.Streams()
                value = marked.decode(value, streams)
            frames.append((step, float(r.get("ts") or 0.0), value, r))
        answers = []
        for r in sorted((r for r in rows if r.get("kind") == "act"), key=lambda r: (r.get("step") or 0, r.get("ts") or 0)):
            got = _rows_of(_untagged(r.get("outputs")))
            if got:
                answers.append((max(int(r.get("step") or 0) - 1, 0), got))
        task = _task([_untagged(r.get("inputs")) for r in rows if r.get("kind") == "act" and "inputs" in r],
                     [fr[2] for fr in frames])
        if frames:
            built.append((episode_id, frames, answers, task))
    leaves: dict[str, tuple[str, list]] = {}
    for _, frames, _, _ in built:
        for _, _, value, _ in frames:
            for name, kind, shape in _leaves(value):
                leaves.setdefault(name, (kind, shape))
    named = _feature_names(leaves)



    in_state = [] if "observation.state" in named.values() else sorted(
        (n for n, (kind, shape) in leaves.items() if kind != "image" and len(shape or []) <= 1), key=named.get)
    state_names = _state_names(in_state, leaves, named)
    action_dim = next((len(rows[0]) for _, _, answers, _ in built for _, rows in answers), 0)
    tasks: dict[str, int] = {}
    index = total = labelled = 0
    meta_episodes, meta_states, fps_seen, written = [], [], [], []
    for e, (episode_id, frames, answers, task) in enumerate(sorted(built, key=lambda b: b[1][0][1])):
        task_index = tasks.setdefault(task, len(tasks))
        label = labels.get(episode_id)
        labelled += label is not None
        t0 = frames[0][1]
        if len(frames) > 1 and frames[-1][1] > t0:
            fps_seen.append((len(frames) - 1) / (frames[-1][1] - t0))
        cols: dict[str, list] = defaultdict(list)
        ops: set[str] = set()
        for i, (step, ts, value, rec) in enumerate(frames):
            got = dict((name, leaf) for name, leaf in _leaf_values(value))
            for name, (kind, _) in leaves.items():
                v = got.get(name)
                if kind == "image":
                    cols[named[name]].append({"bytes": _png(v) if v is not None else None, "path": None})
                else:
                    cols[named[name]].append(np.atleast_1d(np.asarray(v, dtype=np.float32)).tolist()
                                             if v is not None else None)
            if in_state:
                parts = [got.get(n) for n in in_state]
                cols["observation.state"].append(
                    None if any(v is None for v in parts) else
                    np.concatenate([np.atleast_1d(np.asarray(v, dtype=np.float32)).ravel() for v in parts]).tolist())
            cols["action"].append(_action_at(step, answers))
            cols["timestamp"].append(float(ts - t0))
            cols["frame_index"].append(i)
            cols["episode_index"].append(e)
            cols["index"].append(index)
            cols["task_index"].append(task_index)
            last = i == len(frames) - 1
            cols["next.done"].append(last)
            cols["next.success"].append(bool(last and label and label.get("success")))


            cols["driver"].append(_DRIVER_CODE.get(str(rec.get("driver") or "model"), 0))
            op = rec.get("operator")
            if op:
                ops.add(str(op))
            index += 1
        total += len(frames)
        meta_episodes.append({"episode_index": e, "tasks": [task], "length": len(frames), "episode_id": episode_id,
                              **({"operators": sorted(ops)} if ops else {}),
                              **({"success": bool(label.get("success")), "notes": label.get("notes") or ""}
                                 if label else {})})
        written.append((cols, meta_episodes[-1]))
        if episode_id in states:
            kept = states[episode_id]
            meta_states.append({"episode_index": e, "episode_id": episode_id, "state": kept.get("state"),
                                "skipped": kept.get("skipped") or []})
    features: dict[str, Any] = {
        **({"observation.state": {"dtype": "float32", "shape": [len(state_names)], "names": state_names}}
           if in_state else {}),
        **{named[n]: ({"dtype": "image", "shape": shape, "names": ["height", "width", "channel"]} if k == "image"
                      else {"dtype": "float32", "shape": shape or [1], "names": None})
           for n, (k, shape) in leaves.items()},
        "action": {"dtype": "float32", "shape": [action_dim], "names": None},
        "timestamp": {"dtype": "float32", "shape": [1], "names": None},
        "frame_index": {"dtype": "int64", "shape": [1], "names": None},
        "episode_index": {"dtype": "int64", "shape": [1], "names": None},
        "index": {"dtype": "int64", "shape": [1], "names": None},
        "task_index": {"dtype": "int64", "shape": [1], "names": None},
        "next.done": {"dtype": "bool", "shape": [1], "names": None},
        "next.success": {"dtype": "bool", "shape": [1], "names": None},


        "driver": {"dtype": "int64", "shape": [1], "names": ["model", "human", "stopped"]},
    }

    observed = round(sum(fps_seen) / len(fps_seen), 1) if fps_seen else None
    fps = float(hz) if hz else (observed or 10.0)
    _write_v30(out, written, features, tasks, fps, "unknown",
               extra={"observed_fps": observed} if observed is not None else None)
    if meta_states:
        with open(os.path.join(out, "meta", "episode_states.jsonl"), "w") as f:
            f.writelines(json.dumps(m) + "\n" for m in meta_states)
    return {"episodes": len(meta_episodes), "frames": total, "labelled": labelled, "states": len(meta_states),
            "fps": fps, "fps_from": "declared" if hz else "observed" if observed is not None else "default"}


def _state_names(in_state: list, leaves: dict, named: dict) -> list[str]:
    """observation.state's names, a number each: a column's own name for a number, `<name>.<i>` for a vector's."""
    out = []
    for n in in_state:
        base, size = named[n][len("observation."):], (leaves[n][1] or [1])[0]
        out += [base] if size <= 1 else [f"{base}.{i}" for i in range(size)]
    return out


def _marked():
    """sequence_base's decoders of the observation format, which the worker used on the same items."""
    try:
        from sequence_base.codec import marked

        import av
        import zstandard
    except ImportError as exc:
        raise MissingPackage(f"this dataset's steps hold Video, Depth or Tactile items, and decoding them needs "
                             f"what is missing here ({exc.name})", hint="pip install -U 'sequence-ai[data]'") from None
    return marked


def _untagged(value: Any) -> Any:
    """A kept line's value as the robot sent it: {"__ndarray__", "dtype", "shape"} an array again, {"__bytes__"} bytes
    (the worker's capture writes them so, JSON carrying neither)."""
    if isinstance(value, dict):
        if "__ndarray__" in value:
            import numpy as np

            raw = base64.b64decode(value["__ndarray__"])
            return np.frombuffer(raw, np.dtype(value["dtype"])).reshape(value.get("shape") or [-1]).copy()
        if "__bytes__" in value:
            return base64.b64decode(value["__bytes__"])
        return {k: _untagged(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_untagged(v) for v in value]
    return value


def _holds_mark(value: Any) -> bool:
    if isinstance(value, dict):
        return value.get("__seq__") in ("video", "depth", "tactile") or any(_holds_mark(v) for v in value.values())
    if isinstance(value, list):
        return any(_holds_mark(v) for v in value)
    return False


def _leaf_values(value: Any, prefix: str = ""):
    """(name, value) for each item of an observation a dataset has a column for: nested keys joined by dots."""
    import numpy as np

    if isinstance(value, dict):
        for k, v in value.items():
            yield from _leaf_values(v, f"{prefix}{k}" if not prefix else f"{prefix}.{k}")
        return
    if isinstance(value, np.ndarray):
        if value.dtype.kind in "uifb":
            yield prefix, value
        return
    if isinstance(value, list):
        if value and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value):
            yield prefix, value
        else:
            for i, v in enumerate(value):
                yield from _leaf_values(v, f"{prefix}.{i}" if prefix else str(i))
        return
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        yield prefix, [value]


def _leaves(value: Any):
    """(name, kind, shape) for each column `value` gives: an RGB frame an image, any other number an array."""
    import numpy as np

    for name, v in _leaf_values(value):
        a = np.asarray(v)
        if a.dtype == np.uint8 and a.ndim == 3 and a.shape[2] == 3:
            yield name, "image", list(a.shape)
        else:
            yield name, "array", list(a.shape)


def _png(frame: Any) -> bytes:
    import io

    import numpy as np
    from PIL import Image

    a = np.asarray(frame)
    if a.dtype != np.uint8 or a.ndim != 3:
        return b""
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, format="PNG")
    return buf.getvalue()


def _rows_of(outputs: Any) -> list[list[float]] | None:
    """The rows of an act function's answer: an array of rows, one row, or the one of those a map holds - its actions,
    action, rows or chunk, or its only array. None for an answer that is no rows of numbers."""
    import numpy as np

    if isinstance(outputs, dict):
        for key in _ACTION_KEYS:
            if key in outputs:
                return _rows_of(outputs[key])
        arrays = [v for v in outputs.values() if _rows_of(v)]
        return _rows_of(arrays[0]) if len(arrays) == 1 else None
    if outputs is None or isinstance(outputs, (str, bytes)):
        return None
    try:
        a = np.asarray(outputs, dtype=np.float64)
    except (TypeError, ValueError):
        return None
    if a.ndim == 1 and a.size:
        return [a.tolist()]
    if a.ndim == 2 and a.size:
        return a.tolist()
    return None


def _action_at(step: int, answers: list) -> list:
    """The action an episode's answers give `step` (the module's rule): the newest answer that starts at or before it,
    its row for the step - its last past its end - or, before the first answer, that answer's first row."""
    if not answers:
        return []
    start, rows = answers[0]
    for s, r in answers:
        if s > step:
            break
        start, rows = s, r
    return [float(v) for v in rows[min(max(step - start, 0), len(rows) - 1)]]


def _task(inputs: list, observations: list) -> str:
    """An episode's instruction: what an act carried as a sentence alone; else the first non-empty string under a key
    named instruction, task, prompt or language_instruction, at any depth - as its acts carried it, then as its steps
    observed it; else under a key that holds one of those words; "unspecified" where none did. Before, a key had to be
    named so exactly, at the top.
"""
    for value in inputs:
        if isinstance(value, str) and value.strip():
            return value.strip()
    said = [_said(v) for v in [*inputs, *observations]]
    for named, _ in said:
        if named:
            return named
    for _, worded in said:
        if worded:
            return worded
    return "unspecified"


def _said(value: Any) -> tuple[str | None, str | None]:
    """The first non-empty string `value` holds under a key named as an instruction is (_TASK_KEYS), and the first under
    a key holding one of _TASK_WORDS - each key read by its last part, "/" and "." apart."""
    named = worded = None
    if not isinstance(value, dict):
        return named, worded
    for key, v in value.items():
        last = re.split(r"[./]", str(key))[-1].lower()
        if isinstance(v, str) and v.strip():
            if named is None and last in _TASK_KEYS:
                named = v.strip()
            if worded is None and any(w in last for w in _TASK_WORDS):
                worded = v.strip()
        elif isinstance(v, dict):
            inner_named, inner_worded = _said(v)
            named, worded = named or inner_named, worded or inner_worded
    return named, worded


def _feature_names(leaves: dict) -> dict:
    """Each leaf's column as LeRobot names them: a camera frame `observation.images.<key>`, any other array
    `observation.<key>` - its key as the robot sent it, nested keys joined by ".", with "/" made "." and an
    "observation" of its own in front left out. A key written as a template's, "observation/exterior_image_1_left",
    came out `observation.images.observation/exterior_image_1_left`; it is `observation.images.exterior_image_1_left`.
    Two that would come out the same keep their keys whole, then a number.

"""
    out: dict[str, str] = {}
    taken: set[str] = set()
    for name, (kind, _) in leaves.items():
        parts = [p for p in re.split(r"[./]", name) if p] or [name]
        trimmed = parts[1:] if len(parts) > 1 and parts[0].lower() == "observation" else parts
        head = "observation.images." if kind == "image" else "observation."
        column = head + ".".join(trimmed)
        if column in taken:
            column = head + ".".join(parts)
        n = 2
        while column in taken:
            column, n = f"{head}{'.'.join(parts)}_{n}", n + 1
        taken.add(column)
        out[name] = column
    return out
