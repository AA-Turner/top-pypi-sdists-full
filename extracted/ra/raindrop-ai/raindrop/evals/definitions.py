"""Definition helpers; manifests stay identical to the JavaScript and UI JSON."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import (
    EvalDataset,
    EvalProgram,
    EvalSuite,
    EvalSuiteManifest,
    LocalEvaluator,
    ReplayRow,
)


def define_dataset(dataset: dict[str, Any] | None = None, **kwargs: Any) -> EvalDataset:
    raw = dict(dataset or {}, **kwargs)
    rows = [
        ReplayRow.model_validate(
            {**row, "id": row["id"].strip(), "name": row.get("name", row["id"].strip())}
        )
        if isinstance(row, dict)
        else row
        for row in raw.pop("rows")
    ]
    if not rows or len({row.id for row in rows}) != len(rows):
        raise ValueError("Datasets require nonempty rows with unique ids")
    version = (
        raw.pop("version", None)
        or hashlib.sha256(
            json.dumps(
                [
                    {
                        "id": row.id,
                        "name": row.name,
                        "input": row.input,
                        "output": row.output,
                        "properties": dict(sorted(row.properties.items())),
                    }
                    for row in rows
                ],
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ).encode()
        ).hexdigest()
    )
    for key in ("id", "name"):
        raw[key] = raw[key].strip()
        if not raw[key]:
            raise ValueError(f"Dataset {key} cannot be empty")
    return EvalDataset(**raw, rows=rows, version=version)


def define_local_evaluator(
    evaluator: dict[str, Any] | None = None, **kwargs: Any
) -> LocalEvaluator:
    return LocalEvaluator.model_validate(dict(evaluator or {}, **kwargs))


def define_evaluator_program(
    program: dict[str, Any] | None = None, **kwargs: Any
) -> EvalProgram:
    return EvalProgram.model_validate(dict(program or {}, **kwargs))


def define_eval_suite(
    definition: EvalSuiteManifest | dict[str, Any] | None = None,
    *,
    run: Any = None,
    agent: Any = None,
    **kwargs: Any,
) -> EvalSuite:
    raw = (
        definition.wire()
        if isinstance(definition, EvalSuiteManifest)
        else dict(definition or {})
    )
    if run is not None:
        raw["run"] = run
    if agent is not None:
        raw["agent"] = agent
    raw.update(kwargs)
    # Optional manifest settings default in the runner rather than serializing nulls.
    return EvalSuite.model_validate(raw)


def is_eval_dataset(value: Any) -> bool:
    return isinstance(value, EvalDataset)


def is_eval_suite_definition(value: Any) -> bool:
    return isinstance(value, EvalSuite)


def is_published_eval_suite(value: EvalSuite) -> bool:
    return (
        isinstance(value.dataset, str)
        and value.dataset_version_id is not None
        and all(
            not isinstance(e.evaluator, str)
            and (
                not isinstance(e.evaluator, EvalProgram)
                or e.evaluator.expected is not None
            )
            for e in value.evaluators
        )
    )
