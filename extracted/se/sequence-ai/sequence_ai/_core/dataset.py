"""
A robot's steps as a dataset: LeRobot v3.0, or every field kept as it was (JSON lines). What `seq data export` writes
from recordings of your own - a teleop robot's Record (teleop_record.py), `seq robot record`'s files - and what
sequence-cloud's `seq policy data export` writes from what it downloads of a deployment's.

In one sentence: each recording's items, read in order (sequence_ai.read_record) → episodes_of: by episode, each
observation an "observe" row and each act's answer - a person's chunk the robot played, or its policy's - an "act" row
placed by its step, each label its episode's → write_steps: a frame for every step observed, its marked items (Video,
Depth, Tactile) decoded as the worker decodes them, each camera frame an image `observation.images.<key>`, every other
number an array `observation.<key>`, the action its act's answer gives that step, who drove it (`driver`), each episode's
instruction its task and its label `next.success` on its last frame → _write_v30: as LeRobot's own writer lays a
dataset out.
WHY open: the robot's data is the robot's owner's, and turning it into a dataset needs nothing of the platform's.


"""
from __future__ import annotations

import base64
import glob
import json
import os
import re
from collections import defaultdict
from typing import Any, Iterable

from sequence_ai._core.direct_observe import PROMPT_KEYS
from sequence_ai.errors import InvalidRequest, MissingPackage




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
        answers, human = [], []
        for r in sorted((r for r in rows if r.get("kind") == "act"), key=lambda r: (r.get("step") or 0, r.get("ts") or 0)):
            outputs = _untagged(r.get("outputs"))
            got = _rows_of(outputs)
            if got:
                answers.append((max(int(r.get("step") or 0) - 1, 0), got))
            if isinstance(outputs, dict) and isinstance(outputs.get("inputs"), dict):
                human.append((max(int(r.get("step") or 0) - 1, 0), _human_pose(outputs["inputs"])))
        task = _task([_untagged(r.get("inputs")) for r in rows if r.get("kind") == "act" and "inputs" in r],
                     [fr[2] for fr in frames])
        if frames:
            built.append((episode_id, frames, answers, task, human))
    leaves: dict[str, tuple[str, list]] = {}
    for _, frames, _, _, _ in built:
        for _, _, value, _ in frames:
            for name, kind, shape in _leaves(value):
                leaves.setdefault(name, (kind, shape))
    named = _feature_names(leaves)



    in_state = [] if "observation.state" in named.values() else sorted(
        (n for n, (kind, shape) in leaves.items() if kind != "image" and len(shape or []) <= 1), key=named.get)
    state_names = _state_names(in_state, leaves, named)
    action_dim = next((len(rows[0]) for _, _, answers, _, _ in built for _, rows in answers), 0)
    with_human = any(human for *_, human in built)
    tasks: dict[str, int] = {}
    index = total = labelled = 0
    meta_episodes, meta_states, fps_seen, written = [], [], [], []
    for e, (episode_id, frames, answers, task, human) in enumerate(sorted(built, key=lambda b: b[1][0][1])):
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
            if with_human:
                cols["human_pose"].append(_human_at(step, human))
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


        **({"human_pose": {"dtype": "float32", "shape": [len(HUMAN_POSE_NAMES)], "names": list(HUMAN_POSE_NAMES)}}
           if with_human else {}),
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
    """The observation format's decoders the worker used on the same items: the codec observe() encodes with
    (marked_observe._codec, the one way this package reaches sequence_base), with PyAV and zstandard beside it."""
    from sequence_ai._core.marked_observe import _codec

    try:
        marked = _codec()
        import av
        if not _zstd_here():
            raise ImportError("no zstd here", name="zstandard")
    except (ImportError, MissingPackage) as exc:
        raise MissingPackage(f"this dataset's steps hold Video, Depth or Tactile items, and decoding them needs "
                             f"what is missing here ({getattr(exc, 'name', None) or exc})",
                             hint="pip install -U sequence-ai, on Python 3.10 or later") from None
    return marked


def _zstd_here() -> bool:
    """Whether this machine has zstd for an item's bytes: Python 3.14's compression.zstd, else zstandard installed - the
    robot's posts' own (compress._codec)."""
    from sequence_ai._core.compress import _codec as _posts

    return _posts()[0] == "zstd"


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





HUMAN_POSE_NAMES = (*(f"head.{a}" for a in ("x", "y", "z", "qx", "qy", "qz", "qw")),
                    *(f"{side}.{a}" for side in ("left", "right")
                      for a in ("tracked", "x", "y", "z", "qx", "qy", "qz", "qw", "trigger", "squeeze")))


def _pose_row(pose: Any) -> list[float]:
    pose = pose if isinstance(pose, dict) else {}
    p, q = list(pose.get("p") or (0.0, 0.0, 0.0))[:3], list(pose.get("q") or (0.0, 0.0, 0.0, 1.0))[:4]
    try:
        return [float(v) for v in (*p, *q)]
    except (TypeError, ValueError):
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def _human_pose(inputs: dict) -> list[float]:
    """`inputs` (a console's, as sequence_ai.retarget reads them) as HUMAN_POSE_NAMES' row."""
    row = _pose_row(inputs.get("head"))
    for side in ("left", "right"):
        s = inputs.get(side)
        if not isinstance(s, dict) or s.get("tracked") is False or "p" not in s:
            row += [0.0] * 10
            continue
        try:
            pressed = [float(s.get("trigger") or 0.0), float(s.get("squeeze") or 0.0)]
        except (TypeError, ValueError):
            pressed = [0.0, 0.0]
        row += [1.0, *_pose_row(s), *pressed]
    return row


def _human_at(step: int, human: list) -> list:
    """The person's inputs that held at `step`: the newest at or before it, the first before any."""
    if not human:
        return [0.0] * len(HUMAN_POSE_NAMES)
    row = human[0][1]
    for s, r in human:
        if s > step:
            break
        row = r
    return row


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




def _row_of(kind: str, episode: str, step: Any, at: Any, item: dict, **value: Any) -> dict:
    """One of write_steps' rows, as a worker's capture writes it: its kind, episode, step and time, and who drove."""
    return {"kind": kind, "episode_id": episode, "step": step, "ts": at, **value,
            **({"driver": item["driver"]} if item.get("driver") else {}),
            **({"operator": item["operator"]} if item.get("operator") else {})}


def episodes_of(items: Iterable[dict]) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """A recording's items (sequence_ai.read_record) as write_steps takes them - by episode, in time order - with each
    episode's label. A teleop robot's Record writes each observation as it was made ("observe") and each chunk of a
    person's it played ("step", did "played"); `seq robot record` writes each act ("step") with the observations sent
    since the one before it, and an episode's end with those after its last act. A chunk never played is no step the
    robot took, and a gap or a change of who drives no row."""
    episodes: dict[str, list[dict]] = defaultdict(list)
    labels: dict[str, dict] = {}
    for item in items:
        kind, episode = item.get("kind"), item.get("episode")
        if not isinstance(episode, str) or not episode:
            continue
        at = item.get("at")
        if kind == "label":
            labels[episode] = {"episode_id": episode, "success": bool(item.get("success")),
                               "notes": item.get("notes") or ""}
        elif kind == "observe":
            episodes[episode].append(_row_of("observe", episode, item.get("step"), at, item,
                                             observation=item.get("observation")))
        elif kind in ("step", "end"):
            for pair in item.get("observations") or ():
                if isinstance(pair, (list, tuple)) and len(pair) == 2:
                    episodes[episode].append(_row_of("observe", episode, pair[0], at, item, observation=pair[1]))
            if kind == "step" and item.get("did", "played") == "played" and item.get("action") is not None:
                episodes[episode].append(_row_of("act", episode, item.get("step"), at, item,
                                                 outputs=item.get("action")))
        elif kind == "executed" and item.get("action") is not None:


            episodes[episode].append(_row_of("act", episode, item.get("step"), at, item,
                                             outputs={"actions": [item.get("action")]}))
    for rows in episodes.values():
        rows.sort(key=lambda r: (r.get("ts") or 0.0, r["kind"] != "observe"))
    return dict(episodes), labels


def recordings(paths: Iterable[str]) -> list[str]:
    """Each recording a path names: a file as it is, a folder's *.msgpack files in name order - which a robot names by
    its name and when it began (teleop_record: <robot>-<when>.msgpack)."""
    out: list[str] = []
    for path in paths:
        if os.path.isdir(path):
            out += sorted(glob.glob(os.path.join(path, "*.msgpack")))
        elif os.path.isfile(path):
            out.append(path)
        else:
            raise InvalidRequest(f"{path}: no such file or folder")
    if not out:
        raise InvalidRequest(f"no recording in {', '.join(paths)}: a recording is a .msgpack file a robot's Record or "
                             "`seq robot record` wrote")
    return out


def export(paths: Iterable[str], out: str, *, fmt: str = "lerobot", fps: float | None = None, echo: Any = None) -> dict:
    """`seq data export`: the recordings `paths` name as a LeRobot v3.0 dataset in `out`, at `fps` - unset, the pace
    its robots observed at - or (fmt "jsonl") every item of each as a line of JSON, its arrays and bytes in the tagged
    form JSON carries them in (_tagged), a file a recording."""
    from sequence_ai._core import recorder

    echo = echo or print
    files = recordings(list(paths))
    if fmt == "jsonl":
        os.makedirs(out, exist_ok=True)
        lines = 0
        for path in files:
            dest = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".jsonl")
            with open(dest, "w") as f:
                for item in recorder.read(path):
                    f.write(json.dumps(_tagged(item)) + "\n")
                    lines += 1
        echo(f"wrote {len(files)} file(s), {lines} line(s), to {out}")
        return {"files": len(files), "lines": lines}
    if fmt != "lerobot":
        raise InvalidRequest(f"--format is lerobot or jsonl, not {fmt!r}")
    items: list[dict] = []
    for path in files:
        items.extend(recorder.read(path))
    episodes, labels = episodes_of(items)
    if not episodes:
        echo(f"no episodes in {len(files)} recording(s): no observation was recorded")
        return {"episodes": 0, "frames": 0}
    summary = write_steps(episodes, labels, out, hz=fps)
    echo(f"wrote a LeRobot {LEROBOT_VERSION} dataset to {out}: {summary['episodes']} episode(s), "
         f"{summary['frames']} frame(s), {summary['labelled']} labelled, at {summary['fps']:g} fps"
         + (" - the pace its robots observed at" if summary.get("fps_from") == "observed" else ""))
    return summary


def _tagged(value: Any) -> Any:
    """A recording's value as JSON carries it: an array {"__ndarray__", "dtype", "shape"}, bytes {"__bytes__"} -
    _untagged's forms, which a worker's capture writes."""
    import numpy as np

    if isinstance(value, dict):
        return {str(k): _tagged(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_tagged(v) for v in value]
    if isinstance(value, np.ndarray):
        return {"__ndarray__": base64.b64encode(np.ascontiguousarray(value).tobytes()).decode(),
                "dtype": value.dtype.str, "shape": list(value.shape)}
    if isinstance(value, (bytes, bytearray, memoryview)):
        return {"__bytes__": base64.b64encode(bytes(value)).decode()}
    if isinstance(value, np.generic):
        return value.item()
    return value
