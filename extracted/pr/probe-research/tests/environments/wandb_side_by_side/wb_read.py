"""Read an offline W&B run's transaction log (``run-<id>.wandb``) with no
account and no network: the history rows, the exit record, config keys.

    wb_read.py <offline-run-dir>

wandb >= 0.19 no longer ships a Python reader, so this walks the file's
LevelDB-style log format (7-byte header, 32 KiB blocks, FULL / FIRST /
MIDDLE / LAST chunks) and decodes each record with wandb's own protobufs.
"""

from __future__ import annotations

import glob
import json
import os
import struct
import sys

import envchild
from wandb.proto import wandb_internal_pb2 as pb

BLOCK = 32 * 1024


def records(path: str):
    data = open(path, "rb").read()
    if data[:4] != b":W&B":
        raise SystemExit(f"{path}: not a W&B transaction log")
    pos, buf = 7, b""
    while pos + 7 <= len(data):
        left = BLOCK - (pos % BLOCK)
        if left < 7:
            pos += left
            continue
        _crc, length, kind = struct.unpack("<IHB", data[pos : pos + 7])
        pos += 7
        if kind == 0 and length == 0:  # block padding
            pos += left - 7
            continue
        chunk = data[pos : pos + length]
        pos += length
        if kind == 1:
            yield chunk
        elif kind == 2:
            buf = chunk
        elif kind == 3:
            buf += chunk
        elif kind == 4:
            yield buf + chunk
            buf = b""


def main(run_dir: str) -> None:
    (log,) = glob.glob(os.path.join(run_dir, "run-*.wandb"))
    history, exit_codes, config_keys, kinds = [], [], set(), {}
    for raw in records(log):
        rec = pb.Record()
        rec.ParseFromString(raw)
        kind = rec.WhichOneof("record_type")
        kinds[kind] = kinds.get(kind, 0) + 1
        if kind == "history":
            row = {}
            for item in rec.history.item:
                key = item.key or "/".join(item.nested_key)
                row[key] = json.loads(item.value_json)
            history.append(row)
        elif kind == "exit":
            exit_codes.append(rec.exit.exit_code)
        elif kind == "config":
            for item in rec.config.update:
                config_keys.add(item.key or "/".join(item.nested_key))
    envchild.result(
        "wbread", history=history, exit_codes=exit_codes,
        config_keys=sorted(config_keys), kinds=kinds,
    )


if __name__ == "__main__":
    main(sys.argv[1])
