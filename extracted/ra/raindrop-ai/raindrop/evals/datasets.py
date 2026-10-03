from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any
from urllib.parse import quote
from uuid import UUID, uuid4

import rfc8785

from .client import EvalClient
from .models import DatasetManifest, DatasetRow, EvalDataset, EvalProgram, EvalSuite


def dataset_version_fingerprint(rows: list[dict[str, Any] | DatasetRow]) -> str:
    cases = []
    ids = set()
    if not 1 <= len(rows) <= 1000:
        raise ValueError("Datasets require between 1 and 1000 rows")
    for raw in rows:
        row = raw if isinstance(raw, DatasetRow) else DatasetRow.model_validate(raw)
        if row.id in ids:
            raise ValueError(f"Duplicate row id {row.id}")
        ids.add(row.id)
        # Missing output and null output are distinct in the version fingerprint.
        value = row.model_dump(mode="json", by_alias=True, exclude_unset=True)
        value.pop("referenceTraceSha256", None)
        if value.get("referenceTrace"):
            snapshot = copy.deepcopy(value["referenceTrace"])
            snapshot["spans"].sort(
                key=lambda span: (int(span["start_unix_ns"]), span["span_id"])
            )
            value["referenceTrace"] = snapshot
        cases.append(value)
    return hashlib.sha256(rfc8785.dumps(cases)).hexdigest()


async def publish_eval_dataset(
    client: EvalClient,
    *,
    slug: str,
    name: str,
    rows: list[dict[str, Any] | DatasetRow],
    expected_current_version_id: str | None = None,
    query_url: str | None = None,
) -> DatasetManifest:
    slug = slug.strip()
    if (
        not slug
        or len(slug) > 64
        or re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) is None
    ):
        raise ValueError("Invalid dataset slug")
    name = name.strip()
    if not 1 <= len(name) <= 100:
        raise ValueError("Dataset name must be from 1 to 100 characters")
    if expected_current_version_id:
        UUID(expected_current_version_id)
    fingerprint = dataset_version_fingerprint(rows)
    cases = [
        row.model_dump(mode="json", by_alias=True, exclude_unset=True)
        if isinstance(row, DatasetRow)
        else DatasetRow.model_validate(row).model_dump(
            mode="json", by_alias=True, exclude_unset=True
        )
        for row in rows
    ]
    for case in cases:
        if (
            "referenceTrace" in case
            and len(json.dumps(case["referenceTrace"], ensure_ascii=False).encode())
            > 1024 * 1024
        ):
            raise ValueError("Reference trace exceeds 1 MiB")
    body = {
        "name": name,
        "requestKey": str(uuid4()),
        "expectedCurrentVersionId": expected_current_version_id,
        "fingerprint": fingerprint,
        "cases": cases,
    }
    if len(json.dumps(body, ensure_ascii=False).encode()) > 4 * 1024 * 1024:
        raise ValueError("Dataset upload exceeds 4 MiB")
    response = DatasetManifest.from_wire(
        await client.request(
            "PUT",
            f"/v1/eval-datasets/{quote(slug, safe='')}",
            body=body,
            query_url=query_url,
            retries=2,
        )
    )
    if response.dataset.slug != slug or response.version.fingerprint != fingerprint:
        raise ValueError("Dataset publication returned a mismatched identity")
    return response


async def read_eval_dataset(
    client: EvalClient,
    dataset: str,
    *,
    version_id: str | UUID | None = None,
    query_url: str | None = None,
) -> DatasetManifest:
    dataset = dataset.strip()
    ref = quote(dataset, safe="")
    if not ref:
        raise ValueError("Dataset reference cannot be empty")
    path = f"/v1/eval-datasets/{ref}"
    if version_id:
        version_id = UUID(str(version_id))
        path += f"/versions/{version_id}"
    manifest = DatasetManifest.from_wire(
        await client.request("GET", path, query_url=query_url)
    )
    if dataset not in (manifest.dataset.slug, str(manifest.dataset.id)):
        raise ValueError("Dataset response returned a different dataset")
    if version_id and manifest.version.id != version_id:
        raise ValueError("Dataset response returned a different version")
    return manifest


async def read_eval_manifest(
    client: EvalClient, dataset: str, *, query_url: str | None = None
) -> dict[str, Any]:
    result = await client.request(
        "GET",
        "/v1/replays/manifest?dataset=" + quote(dataset, safe=""),
        query_url=query_url,
    )
    return {
        "datasetId": result["dataset_id"],
        **(
            {"datasetVersionId": result["dataset_version_id"]}
            if result.get("dataset_version_id") is not None
            else {}
        ),
        "fingerprint": result["fingerprint"],
        "cases": result["rows"],
    }


async def read_evaluator(
    client: EvalClient, slug: str, *, query_url: str | None = None
) -> EvalProgram:
    data = (
        await client.request(
            "GET", f"/v1/evals/{quote(slug, safe='')}", query_url=query_url
        )
    )["data"]
    if data["slug"] != slug:
        raise ValueError("Evaluator response returned a different slug")
    return EvalProgram(
        slug=data["slug"],
        name=data["name"],
        output=data["outputType"],
        execution_mode=data["kind"],
        source=data["programSource"],
        description=data.get("description"),
        intent=data["intent"],
        rules=data["rules"],
        expected={"evalId": data["id"], "programVersion": data["programVersion"]},
    )


async def publish_eval_suite(
    client: EvalClient,
    definition: EvalSuite,
    *,
    query_url: str | None = None,
    expected_current_dataset_version_id: str | None = None,
) -> EvalSuite:
    from .models import Evaluator, validate_threshold

    # Validate before writing supporting resources. Source authorship uses MCP/UI.
    for entry in definition.evaluators:
        if (
            isinstance(entry.evaluator, EvalProgram)
            and entry.evaluator.expected is None
        ):
            raise ValueError(
                "Create hosted evaluator source in Raindrop and reference its slug"
            )
    entries = []
    for entry in definition.evaluators:
        evaluator = (
            await read_evaluator(client, entry.evaluator, query_url=query_url)
            if isinstance(entry.evaluator, str)
            else entry.evaluator
        )
        validate_threshold(evaluator.output, entry.threshold)
        entries.append(Evaluator(evaluator=evaluator, threshold=entry.threshold))
    if isinstance(definition.dataset, EvalDataset):
        rows = [
            r.model_dump(mode="json", by_alias=True) for r in definition.dataset.rows
        ]
        for row in rows:
            if row["output"] is None:
                del row["output"]
        manifest = await publish_eval_dataset(
            client,
            slug=definition.dataset.id,
            name=definition.dataset.name,
            rows=rows,
            query_url=query_url,
            expected_current_version_id=expected_current_dataset_version_id,
        )
    else:
        manifest = await read_eval_dataset(
            client,
            definition.dataset,
            version_id=definition.dataset_version_id,
            query_url=query_url,
        )
    return definition.model_copy(
        update={
            "dataset": manifest.dataset.slug,
            "dataset_version_id": manifest.version.id,
            "evaluators": entries,
        }
    )


async def list_evaluators(client: EvalClient, *, query_url: str | None = None) -> Any:
    return await client.request("GET", "/v1/evals", query_url=query_url)
