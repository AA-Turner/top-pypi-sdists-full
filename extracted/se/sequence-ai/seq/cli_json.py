"""
`seq --json`'s half of a command's output: what the command read, as JSON — `_print_json`, and `_jsonable`, which turns
pydantic models and dataclasses into plain data first. Moved out of seq/cli.py when it reached 1500 lines, so the
command modules (seq/deploy_cli.py, seq/storage_cli.py) print through it without importing the dispatcher.


"""
from __future__ import annotations

import dataclasses
import json
from typing import Any



def _jsonable(v: Any) -> Any:
    if hasattr(v, "model_dump"):
        return v.model_dump(mode="json")
    if dataclasses.is_dataclass(v) and not isinstance(v, type):
        return {f.name: _jsonable(getattr(v, f.name)) for f in dataclasses.fields(v)}
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def _print_json(v: Any) -> None:
    print(json.dumps(_jsonable(v), indent=2, default=str))
