"""Minimal mesh log scanner and voxel viewer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import matplotlib.pyplot as plt

def scan(log_path: str) -> List[Dict[str, Any]]:
    """Return list of DATA payloads from a mesh log file."""
    entries: List[Dict[str, Any]] = []
    path = Path(log_path)
    if not path.exists():
        return entries
    for line in path.read_text().splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("event_type") == "DATA" and isinstance(
            obj.get("payload"), dict
        ):
            entries.append(obj["payload"])
    return entries

def render_voxels(voxels: List[Dict[str, Any]]) -> None:
    """Render voxels using matplotlib."""
    if not voxels:
        return
    xs = np.array([v.get("pace", 0) for v in voxels])
    ys = np.array([v.get("rate", 0) for v in voxels])
    zs = np.arange(len(voxels))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs)
    ax.set_xlabel("pace")
    ax.set_ylabel("rate")
    ax.set_zlabel("index")
    plt.show()

def summarize(voxels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return simple stats from the voxel list."""
    if not voxels:
        return {"voxels": 0}
    pace = np.array([v.get("pace", 0.0) for v in voxels], dtype=float)
    rate = np.array([v.get("rate", 0.0) for v in voxels], dtype=float)
    return {
        "voxels": len(voxels),
        "pace": {
            "min": float(pace.min()),
            "max": float(pace.max()),
            "avg": float(pace.mean()),
        },
        "rate": {
            "min": float(rate.min()),
            "max": float(rate.max()),
            "avg": float(rate.mean()),
        },
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="TSAL Meshkeeper")
    parser.add_argument("log", nargs="?", default="data/mesh_log.jsonl")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--dump", metavar="PATH", help="write raw voxels to file")
    args = parser.parse_args()
    voxels = scan(args.log)
    if args.dump:
        Path(args.dump).write_text(json.dumps(voxels))
        return
    if args.render:
        render_voxels(voxels)
    else:
        print(json.dumps(summarize(voxels)))

if __name__ == "__main__":
    main()
