from __future__ import annotations

import io
import re
import json
import shutil
import tarfile
import zipfile
from types import SimpleNamespace
from typing import Any, Literal, cast
from pathlib import Path
from datetime import datetime, timezone
from collections.abc import Callable

import httpx
import pytest

from boltz_api import Boltz
from boltz_api.experiments import (
    Bond,
    Protein,
    EmptyMsa,
    CustomMsa,
    LigandCcd,
    MsaFormat,
    URLSource,
    BoltzModel,
    LigandAtom,
    PolymerAtom,
    LigandSmiles,
    ModelOptions,
    PolymerContact,
    CcdModification,
    ExperimentError,
    PredictionStatus,
    ContactConstraint,
    SmallMoleculeTarget,
    LigandProteinBinding,
    SmallMoleculeTargetBond,
    SmallMoleculeTargetConstraint,
    ExperimentFingerprintMismatchError,
    ExperimentUnsupportedOperationError,
)
from boltz_api.experiments._state import RunMetadata, load_metadata, save_metadata
from boltz_api.experiments.inputs import Protein as InputsProtein
from boltz_api.experiments._results import write_pipeline_result_metadata
from boltz_api.experiments._addressing import generate_name, deterministic_name
from boltz_api.experiments._materialize import archive_suffix_from_url

NOW = datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc)
PipelineRunType = Literal[
    "protein_design",
    "protein_library_screen",
    "small_molecule_design",
    "small_molecule_library_screen",
]
HappyPathRunner = Callable[[Boltz, pytest.MonkeyPatch, Path, Any], Path]
PipelineStarter = Callable[[Boltz, Path], Path]
PipelineResourceGetter = Callable[[Boltz], Any]


def _iso_now() -> str:
    return NOW.isoformat()


def _make_archive_bytes(files: dict[str, bytes] | None = None) -> bytes:
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w:gz") as archive:
        for name, content in (files or {"result.txt": b"hello"}).items():
            info = tarfile.TarInfo(name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
    return data.getvalue()


def _make_zip_archive_bytes(files: dict[str, bytes] | None = None) -> bytes:
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode="w") as archive:
        for name, content in (files or {"result.txt": b"hello"}).items():
            archive.writestr(name, content)
    return data.getvalue()


def _prediction_response(
    *,
    run_id: str,
    status: str,
    archive_url: str | None = None,
    workspace_id: str = "ws_123",
    error_code: str | None = None,
) -> SimpleNamespace:
    output = None
    if archive_url is not None:
        output = SimpleNamespace(
            archive=SimpleNamespace(url=archive_url, url_expires_at=NOW),
            best_sample=SimpleNamespace(
                metrics={"complex_plddt": 0.5},
                structure=SimpleNamespace(url=archive_url.replace(".tar.gz", ".cif"), url_expires_at=NOW),
            ),
        )
    return SimpleNamespace(
        id=run_id,
        status=status,
        workspace_id=workspace_id,
        started_at=NOW,
        completed_at=NOW if status in {"succeeded", "failed"} else None,
        stopped_at=None,
        error=SimpleNamespace(code=error_code) if error_code is not None else None,
        output=output,
    )


def _adme_response(
    *,
    run_id: str,
    status: str,
    output: dict[str, Any] | None = None,
    workspace_id: str = "ws_123",
    error_code: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=run_id,
        status=status,
        workspace_id=workspace_id,
        started_at=NOW,
        completed_at=NOW if status in {"succeeded", "failed"} else None,
        stopped_at=None,
        error=SimpleNamespace(code=error_code) if error_code is not None else None,
        output=output,
    )


def _pipeline_response(
    *,
    run_id: str,
    status: str,
    latest_result_id: str | None = None,
    workspace_id: str = "ws_123",
    error_code: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=run_id,
        status=status,
        workspace_id=workspace_id,
        started_at=NOW,
        completed_at=NOW if status in {"succeeded", "failed", "stopped"} else None,
        stopped_at=NOW if status == "stopped" else None,
        error=SimpleNamespace(code=error_code) if error_code is not None else None,
        progress=SimpleNamespace(latest_result_id=latest_result_id),
    )


def _pipeline_result(result_id: str, archive_url: str, **fields: Any) -> SimpleNamespace:
    data = dict(
        id=result_id,
        artifacts=SimpleNamespace(archive=SimpleNamespace(url=archive_url)),
    )
    data.update(fields)
    return SimpleNamespace(**data)


def _page(*results: SimpleNamespace) -> SimpleNamespace:
    last_id = results[-1].id if results else None
    return SimpleNamespace(data=list(results), last_id=last_id)


def _read_metadata(run_dir: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((run_dir / ".boltz-run.json").read_text(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        cast(dict[str, Any], json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _assert_no_download_urls(value: Any) -> None:
    if isinstance(value, dict):
        data = cast(dict[str, Any], value)
        assert "url" not in data
        assert "url_expires_at" not in data
        for item in data.values():
            _assert_no_download_urls(item)
    elif isinstance(value, list):
        for item in cast(list[Any], value):
            _assert_no_download_urls(item)


def _pipeline_result_fields(run_type: PipelineRunType, result_id: str) -> dict[str, Any]:
    metrics = {"binding_confidence": 0.91 if result_id == "res_1" else 0.82}
    protein_entities = [
        {
            "chain_ids": ["A"],
            "modifications": [],
            "type": "protein",
            "value": "ACDE" if result_id == "res_1" else "FGHI",
        }
    ]

    fields: dict[str, Any] = {
        "created_at": NOW,
        "metrics": metrics,
    }
    if run_type == "protein_design":
        fields["entities"] = protein_entities
    elif run_type == "protein_library_screen":
        fields.update(
            {
                "entities": protein_entities,
                "external_id": "prot001" if result_id == "res_1" else "prot002",
                "warnings": [{"code": "low_confidence", "message": "Review interface"}],
            }
        )
    elif run_type == "small_molecule_design":
        fields["smiles"] = "CCO" if result_id == "res_1" else "CCN"
    else:
        fields.update(
            {
                "external_id": "mol001" if result_id == "res_1" else "mol002",
                "smiles": "CCO" if result_id == "res_1" else "CCN",
                "warnings": [{"code": "low_confidence", "message": "Review pose"}],
            }
        )
    return fields


def _expected_pipeline_metadata(run_type: PipelineRunType, result_id: str) -> dict[str, Any]:
    metadata = _pipeline_result_fields(run_type, result_id)
    metadata["created_at"] = _iso_now()
    return {"id": result_id, **metadata}


def _assert_pipeline_result_metadata(run_dir: Path, run_type: PipelineRunType) -> None:
    index_entries = _read_jsonl(run_dir / "results" / "index.jsonl")
    assert [entry["id"] for entry in index_entries] == ["res_1", "res_2"]

    for result_id in ("res_1", "res_2"):
        expected = _expected_pipeline_metadata(run_type, result_id)
        result_dir = run_dir / "results" / result_id

        assert _read_json(result_dir / "metadata.json") == expected

        manifest_entry = index_entries[0 if result_id == "res_1" else 1]
        assert manifest_entry == {
            **expected,
            "paths": {
                "archive": f"results/{result_id}/archive.tar.gz",
                "files": f"results/{result_id}/files",
                "metrics": f"results/{result_id}/files/result/metrics.json",
                "structure": f"results/{result_id}/files/result/{result_id}_predicted.cif",
                "pae": f"results/{result_id}/files/result/pae.npz",
            },
        }
        assert "artifacts" not in manifest_entry
        for local_path in manifest_entry["paths"].values():
            assert (run_dir / local_path).exists()


def test_pipeline_manifest_tracks_files_dir_and_structure_fallbacks(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "manifest"
    result_dir = run_dir / "results" / "res_pdb"
    archive_path = result_dir / "archive.zip"
    extracted_dir = result_dir / "files"
    structure_path = extracted_dir / "ranked" / "model.pdb"
    metrics_path = extracted_dir / "metrics.json"
    pae_path = extracted_dir / "pae.npz"

    archive_path.parent.mkdir(parents=True)
    archive_path.write_bytes(_make_zip_archive_bytes())
    structure_path.parent.mkdir(parents=True)
    structure_path.write_text("ATOM\n", encoding="utf-8")
    metrics_path.write_text("{}", encoding="utf-8")
    pae_path.write_bytes(b"npz")

    write_pipeline_result_metadata(
        run_dir=run_dir,
        result=_pipeline_result("res_pdb", "https://files.example.com/res_pdb.zip", score=0.9),
    )

    manifest = _read_jsonl(run_dir / "results" / "index.jsonl")
    assert manifest == [
        {
            "id": "res_pdb",
            "score": 0.9,
            "paths": {
                "archive": "results/res_pdb/archive.zip",
                "files": "results/res_pdb/files",
                "metrics": "results/res_pdb/files/metrics.json",
                "structure": "results/res_pdb/files/ranked/model.pdb",
                "pae": "results/res_pdb/files/pae.npz",
            },
        }
    ]


def test_archive_suffixes_match_download_results_cli() -> None:
    assert archive_suffix_from_url("https://files.example.com/result.tar.gz?sig=1") == ".tar.gz"
    assert archive_suffix_from_url("https://files.example.com/result.tgz") == ".tgz"
    assert archive_suffix_from_url("https://files.example.com/result.tar") == ".tar"
    assert archive_suffix_from_url("https://files.example.com/result.zip") == ".zip"

    with pytest.raises(ExperimentError, match="supported file suffix"):
        archive_suffix_from_url("https://files.example.com/result.gz")


def _prediction_response_json(
    *,
    run_id: str,
    status: str,
    workspace_id: str = "ws_123",
    archive_url: str | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] | None = None
    if archive_url is not None:
        output = {
            "all_sample_results": [],
            "best_sample": {
                "metrics": {
                    "complex_plddt": 0.5,
                    "complex_iptm": 0.5,
                    "complex_pde": 1.0,
                    "complex_ptm": 0.5,
                },
                "structure": {
                    "url": archive_url.replace(".tar.gz", ".cif"),
                    "url_expires_at": _iso_now(),
                },
            },
            "archive": {"url": archive_url, "url_expires_at": _iso_now()},
        }

    return {
        "id": run_id,
        "completed_at": _iso_now() if status in {"succeeded", "failed"} else None,
        "created_at": _iso_now(),
        "data_deleted_at": None,
        "error": None,
        "expires_at": None,
        "input": None,
        "livemode": False,
        "model": "boltz-2.1",
        "output": output,
        "started_at": _iso_now(),
        "status": status,
        "version": "test-version",
        "workspace_id": workspace_id,
        "idempotency_key": "idem_test",
    }


def _protein_design_run_json(
    *,
    run_id: str,
    status: str,
    latest_result_id: str | None = None,
    workspace_id: str = "ws_123",
) -> dict[str, Any]:
    return {
        "id": run_id,
        "completed_at": _iso_now() if status in {"succeeded", "failed", "stopped"} else None,
        "created_at": _iso_now(),
        "data_deleted_at": None,
        "engine": "boltzprot",
        "engine_version": "1.0",
        "error": None,
        "input": None,
        "livemode": False,
        "pipeline": "boltzprot",
        "pipeline_version": "1.0",
        "progress": {
            "num_proteins_generated": 1 if latest_result_id is not None else 0,
            "total_proteins_to_generate": 1,
            "latest_result_id": latest_result_id,
        },
        "started_at": _iso_now(),
        "status": status,
        "stopped_at": _iso_now() if status == "stopped" else None,
        "workspace_id": workspace_id,
        "idempotency_key": "idem_test",
    }


def _protein_design_result_json(result_id: str, archive_url: str) -> dict[str, Any]:
    return {
        "id": result_id,
        "artifacts": {
            "archive": {"url": archive_url, "url_expires_at": _iso_now()},
        },
        "created_at": _iso_now(),
        "entities": [
            {
                "chain_ids": ["A"],
                "modifications": [],
                "type": "protein",
                "value": "ACDE",
            }
        ],
        "metrics": {
            "binding_confidence": 0.9,
            "helix_fraction": 0.1,
            "iptm": 0.8,
            "loop_fraction": 0.2,
            "min_interaction_pae": 1.0,
            "sheet_fraction": 0.3,
            "structure_confidence": 0.95,
        },
        "warnings": [],
    }


def _small_molecule_design_run_json(
    *,
    run_id: str,
    status: str,
    latest_result_id: str | None = None,
    workspace_id: str = "ws_123",
) -> dict[str, Any]:
    return {
        "id": run_id,
        "completed_at": _iso_now() if status in {"succeeded", "failed", "stopped"} else None,
        "created_at": _iso_now(),
        "data_deleted_at": None,
        "engine": "boltzmol",
        "engine_version": "1.0",
        "error": None,
        "input": None,
        "livemode": False,
        "pipeline": "boltzmol",
        "pipeline_version": "1.0",
        "progress": {
            "num_molecules_generated": 1 if latest_result_id is not None else 0,
            "total_molecules_to_generate": 1,
            "latest_result_id": latest_result_id,
        },
        "started_at": _iso_now(),
        "status": status,
        "stopped_at": _iso_now() if status == "stopped" else None,
        "workspace_id": workspace_id,
        "idempotency_key": "idem_test",
    }


def _small_molecule_library_screen_run_json(
    *,
    run_id: str,
    status: str,
    latest_result_id: str | None = None,
    workspace_id: str = "ws_123",
) -> dict[str, Any]:
    return {
        "id": run_id,
        "completed_at": _iso_now() if status in {"succeeded", "failed", "stopped"} else None,
        "created_at": _iso_now(),
        "data_deleted_at": None,
        "engine": "boltzmol",
        "engine_version": "1.0",
        "error": None,
        "input": None,
        "livemode": False,
        "pipeline": "boltzmol",
        "pipeline_version": "1.0",
        "progress": {
            "num_molecules_failed": 0,
            "num_molecules_screened": 1 if latest_result_id is not None else 0,
            "total_molecules_to_screen": 1,
            "latest_result_id": latest_result_id,
            "rejection_summary": None,
        },
        "started_at": _iso_now(),
        "status": status,
        "stopped_at": _iso_now() if status == "stopped" else None,
        "workspace_id": workspace_id,
        "idempotency_key": "idem_test",
    }


def _protein_no_template_binder_spec() -> Any:
    return {"type": "no_template", "entities": []}


def _protein_no_template_target() -> Any:
    return {"type": "no_template", "entities": []}


def _small_molecule_target() -> Any:
    return {"entities": []}


def _structure_template_binder_spec(structure: Any) -> Any:
    return {
        "type": "structure_template",
        "modality": "peptide",
        "chain_selection": {},
        "structure": structure,
    }


def _structure_template_target(structure: Any) -> Any:
    return {
        "type": "structure_template",
        "chain_selection": {},
        "structure": structure,
    }


def _base64_cif_source(data: str = "ZGF0YQ==") -> dict[str, str]:
    return {
        "type": "base64",
        "media_type": "chemical/x-cif",
        "data": data,
    }


def _prediction_start_stub(run_id: str, *, status: str = "running") -> Any:
    def start(**_kwargs: Any) -> SimpleNamespace:
        del _kwargs
        return _prediction_response(run_id=run_id, status=status)

    return start


def _prediction_retrieve_stub(run_id: str, *, status: str, archive_url: str | None = None) -> Any:
    def retrieve(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        del _args, _kwargs
        return _prediction_response(run_id=run_id, status=status, archive_url=archive_url)

    return retrieve


def _pipeline_start_stub(
    run_id: str,
    *,
    status: str = "running",
    latest_result_id: str | None = None,
) -> Any:
    def start(**_kwargs: Any) -> SimpleNamespace:
        del _kwargs
        return _pipeline_response(run_id=run_id, status=status, latest_result_id=latest_result_id)

    return start


def _pipeline_retrieve_stub(
    run_id: str,
    *,
    status: str,
    latest_result_id: str | None = None,
) -> Any:
    def retrieve(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        del _args, _kwargs
        return _pipeline_response(run_id=run_id, status=status, latest_result_id=latest_result_id)

    return retrieve


def _pipeline_stop_stub(stop_calls: dict[str, int], *, status: str = "stopped") -> Any:
    def stop(run_id: str) -> SimpleNamespace:
        stop_calls["count"] += 1
        return _pipeline_response(run_id=run_id, status=status)

    return stop


def _run_prediction_case(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    return _run_prediction_happy_path(
        client=client,
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        respx_mock=respx_mock,
    )


def _run_protein_design_happy_path(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    return _run_pipeline_happy_path(
        client=client,
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        respx_mock=respx_mock,
        run_type="protein_design",
    )


def _run_protein_library_screen_happy_path(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    return _run_pipeline_happy_path(
        client=client,
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        respx_mock=respx_mock,
        run_type="protein_library_screen",
    )


def _run_small_molecule_design_happy_path(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    return _run_pipeline_happy_path(
        client=client,
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        respx_mock=respx_mock,
        run_type="small_molecule_design",
    )


def _run_small_molecule_library_screen_happy_path(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    return _run_pipeline_happy_path(
        client=client,
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        respx_mock=respx_mock,
        run_type="small_molecule_library_screen",
    )


def _start_protein_design_for_stop(client: Boltz, tmp_path: Path) -> Path:
    return client.experiments.start_protein_design(
        binder_specification=_protein_no_template_binder_spec(),
        num_proteins=1,
        target=_protein_no_template_target(),
        root_dir=tmp_path / "runs",
        name="stop-protein-design",
        quiet=True,
    )


def _start_protein_library_screen_for_stop(client: Boltz, tmp_path: Path) -> Path:
    return client.experiments.start_protein_library_screen(
        proteins=[],
        target=_protein_no_template_target(),
        root_dir=tmp_path / "runs",
        name="stop-protein-screen",
        quiet=True,
    )


def _start_small_molecule_design_for_stop(client: Boltz, tmp_path: Path) -> Path:
    return client.experiments.start_small_molecule_design(
        num_molecules=1,
        target=_small_molecule_target(),
        root_dir=tmp_path / "runs",
        name="stop-small-design",
        quiet=True,
    )


def _start_small_molecule_library_screen_for_stop(client: Boltz, tmp_path: Path) -> Path:
    return client.experiments.start_small_molecule_library_screen(
        molecules=[],
        target=_small_molecule_target(),
        root_dir=tmp_path / "runs",
        name="stop-small-screen",
        quiet=True,
    )


HAPPY_PATH_RUNNERS: list[tuple[str, HappyPathRunner]] = [
    ("prediction", _run_prediction_case),
    ("protein_design", _run_protein_design_happy_path),
    ("protein_library_screen", _run_protein_library_screen_happy_path),
    ("small_molecule_design", _run_small_molecule_design_happy_path),
    ("small_molecule_library_screen", _run_small_molecule_library_screen_happy_path),
]

PIPELINE_STARTERS: list[tuple[PipelineRunType, PipelineStarter]] = [
    ("protein_design", _start_protein_design_for_stop),
    ("protein_library_screen", _start_protein_library_screen_for_stop),
    ("small_molecule_design", _start_small_molecule_design_for_stop),
    ("small_molecule_library_screen", _start_small_molecule_library_screen_for_stop),
]

PIPELINE_RESOURCE_RUNNERS: list[tuple[PipelineRunType, PipelineResourceGetter, dict[str, Any]]] = [
    (
        "protein_design",
        lambda client: client.protein.design,
        {
            "binder_specification": _protein_no_template_binder_spec(),
            "num_proteins": 2,
            "target": _protein_no_template_target(),
        },
    ),
    (
        "protein_library_screen",
        lambda client: client.protein.library_screen,
        {
            "proteins": [],
            "target": _protein_no_template_target(),
        },
    ),
    (
        "small_molecule_design",
        lambda client: client.small_molecule.design,
        {
            "num_molecules": 2,
            "target": _small_molecule_target(),
            "chemical_space": "enamine_real",
        },
    ),
    (
        "small_molecule_library_screen",
        lambda client: client.small_molecule.library_screen,
        {
            "molecules": [],
            "target": _small_molecule_target(),
        },
    ),
]


def _has_resource_run(resource: object) -> bool:
    return callable(getattr(resource, "run", None))


def _run_resource(resource: object, **kwargs: Any) -> Path:
    return cast(Any, resource).run(**kwargs)


@pytest.mark.respx
def test_experiments_namespace_attaches_without_breaking_generated_usage(client: Boltz) -> None:
    assert client.experiments is client.experiments
    assert callable(client.experiments.start_structure_and_binding)
    assert callable(client.experiments.run_structure_and_binding)
    assert callable(client.experiments.predict_structure_and_binding)
    assert Protein is InputsProtein
    assert str(BoltzModel.BOLTZ_2_1) == "boltz-2.1"
    assert PredictionStatus.SUCCEEDED == "succeeded"
    assert EmptyMsa().to_dict() == {"type": "empty"}
    assert client.cli is client.cli
    assert client.auth is client.auth
    assert client.predictions.structure_and_binding is client.predictions.structure_and_binding
    assert client.protein.design is client.protein.design
    assert _has_resource_run(client.predictions.structure_and_binding)
    assert _has_resource_run(client.predictions.adme)
    assert _has_resource_run(client.protein.design)
    assert _has_resource_run(client.protein.library_screen)
    assert _has_resource_run(client.small_molecule.design)
    assert _has_resource_run(client.small_molecule.library_screen)


def test_resource_run_methods_are_marked_for_reference_generation(client: Boltz) -> None:
    assert getattr(client.predictions.structure_and_binding.run, "__boltz_api_custom_method__", False) is True
    assert getattr(client.predictions.adme.run, "__boltz_api_custom_method__", False) is True
    assert getattr(client.protein.design.run, "__boltz_api_custom_method__", False) is True
    assert getattr(client.protein.library_screen.run, "__boltz_api_custom_method__", False) is True
    assert getattr(client.small_molecule.design.run, "__boltz_api_custom_method__", False) is True
    assert getattr(client.small_molecule.library_screen.run, "__boltz_api_custom_method__", False) is True


@pytest.mark.respx
def test_structure_and_binding_resource_run_uses_start_input(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url = "https://files.example.com/resource-prediction.tar.gz"
    archive_bytes = _make_archive_bytes({"prediction.txt": b"prediction"})
    start_kwargs: dict[str, Any] = {}

    def start(**kwargs: Any) -> SimpleNamespace:
        start_kwargs.update(kwargs)
        return _prediction_response(run_id="pred_resource", status="running")

    monkeypatch.setattr(client.predictions.structure_and_binding, "start", start)
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "retrieve",
        _prediction_retrieve_stub("pred_resource", status="succeeded", archive_url=archive_url),
    )
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    input_payload = cast(
        Any,
        {
            "entities": [
                {
                    "chain_ids": ["A"],
                    "type": "protein",
                    "value": "MKTIIALSYIFCLVFA",
                }
            ],
            "num_samples": 3,
            "templates": [
                {
                    "format": "cif",
                    "source": {"type": "url", "url": "https://files.example.com/template.cif"},
                    "chain_id": "A",
                    "template_id": "A",
                }
            ],
        },
    )

    run_dir = _run_resource(
        client.predictions.structure_and_binding,
        model="boltz-2.1",
        input=input_payload,
        root_dir=tmp_path / "runs",
        name="resource-prediction",
        workspace_id="ws_123",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    assert start_kwargs["input"] == input_payload
    assert start_kwargs["model"] == "boltz-2.1"
    assert start_kwargs["workspace_id"] == "ws_123"
    assert isinstance(start_kwargs["idempotency_key"], str)
    assert run_dir == tmp_path / "runs" / "resource-prediction"
    assert (run_dir / "outputs" / "archive.tar.gz").exists()


def test_adme_resource_run_waits_and_writes_inline_output(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start_kwargs: dict[str, Any] = {}
    output = {
        "molecules": [
            {
                "id": "mol_1",
                "external_id": "aspirin",
                "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
                "status": "succeeded",
                "adme": {
                    "lipophilicity": 0.1,
                    "permeability": 0.2,
                    "solubility": "high-confidence",
                },
                "error": None,
            }
        ]
    }

    def start(**kwargs: Any) -> SimpleNamespace:
        start_kwargs.update(kwargs)
        return _adme_response(run_id="adme_pred_resource", status="running")

    def retrieve(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        del _args, _kwargs
        return _adme_response(run_id="adme_pred_resource", status="succeeded", output=output)

    monkeypatch.setattr(client.predictions.adme, "start", start)
    monkeypatch.setattr(client.predictions.adme, "retrieve", retrieve)

    input_payload = cast(
        Any,
        {
            "molecules": [
                {
                    "id": "aspirin",
                    "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
                }
            ]
        },
    )

    run_dir = _run_resource(
        client.predictions.adme,
        model="adme-v1",
        input=input_payload,
        root_dir=tmp_path / "runs",
        name="resource-adme",
        workspace_id="ws_123",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    assert start_kwargs["input"] == input_payload
    assert start_kwargs["model"] == "adme-v1"
    assert start_kwargs["workspace_id"] == "ws_123"
    assert isinstance(start_kwargs["idempotency_key"], str)
    assert run_dir == tmp_path / "runs" / "resource-adme"
    assert _read_json(run_dir / "run.json")["output"] == output
    assert not (run_dir / "outputs").exists()


@pytest.mark.parametrize(("run_type", "resource_getter", "kwargs"), PIPELINE_RESOURCE_RUNNERS)
def test_pipeline_resource_run_methods_wait_and_write_metadata(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    run_type: PipelineRunType,
    resource_getter: PipelineResourceGetter,
    kwargs: dict[str, Any],
) -> None:
    resource = resource_getter(client)
    run_id = f"{run_type}_resource_id"
    start_kwargs: dict[str, Any] = {}

    def start(**start_call_kwargs: Any) -> SimpleNamespace:
        start_kwargs.update(start_call_kwargs)
        return _pipeline_response(run_id=run_id, status="running", latest_result_id="res_1")

    def list_results(*_args: Any, **list_kwargs: Any) -> Any:
        if list_kwargs.get("after_id") is not None:
            return _page()
        return _page(
            _pipeline_result(
                "res_1",
                f"https://files.example.com/{run_type}_resource_1.tar.gz",
                **_pipeline_result_fields(run_type, "res_1"),
            )
        )

    monkeypatch.setattr(resource, "start", start)
    monkeypatch.setattr(
        resource,
        "retrieve",
        _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_1"),
    )
    monkeypatch.setattr(resource, "list_results", list_results)

    run_dir = _run_resource(
        resource,
        root_dir=tmp_path / "runs",
        name=f"{run_type}-resource",
        workspace_id="ws_123",
        download_mode="metadata_only",
        quiet=True,
        poll_interval_seconds=0.0,
        **kwargs,
    )

    assert start_kwargs["workspace_id"] == "ws_123"
    assert isinstance(start_kwargs["idempotency_key"], str)
    assert run_dir == tmp_path / "runs" / f"{run_type}-resource"
    assert _read_json(run_dir / "run.json")["id"] == run_id
    assert _read_jsonl(run_dir / "results" / "index.jsonl")[0]["id"] == "res_1"


def test_generated_run_names_include_entropy_suffix() -> None:
    generated = generate_name()
    assert re.fullmatch(r"[a-z]+-[a-z]+-[a-z]+-[0-9a-f]{6}", generated)


@pytest.mark.respx
@pytest.mark.parametrize(
    ("label", "runner"),
    HAPPY_PATH_RUNNERS,
)
def test_run_happy_path_for_all_flows(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
    label: str,
    runner: HappyPathRunner,
) -> None:
    del label
    run_dir = runner(client, monkeypatch, tmp_path, respx_mock)
    metadata = _read_metadata(run_dir)
    assert run_dir.is_absolute()
    assert metadata["pending"] is None


@pytest.mark.respx
def test_start_structure_and_binding_returns_absolute_path_without_waiting(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start_calls: list[dict[str, Any]] = []

    def fake_start(*, input: Any, model: str, idempotency_key: str, workspace_id: str | None = None) -> Any:
        start_calls.append(
            {
                "input": input,
                "model": model,
                "idempotency_key": idempotency_key,
                "workspace_id": workspace_id,
            }
        )
        return _prediction_response(run_id="pred_1", status="running")

    def unexpected_retrieve(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("start_structure_and_binding() must not wait")

    monkeypatch.setattr(client.predictions.structure_and_binding, "start", fake_start)
    monkeypatch.setattr(client.predictions.structure_and_binding, "retrieve", unexpected_retrieve)

    run_dir = client.experiments.start_structure_and_binding(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="pred-start-only",
        quiet=True,
    )

    assert run_dir.is_absolute()
    assert start_calls
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == "pred_1"
    assert run_json["status"] == "running"
    assert not (run_dir / "outputs").exists()


@pytest.mark.respx
def test_generated_prediction_start_omits_absent_optional_fields(
    client: Boltz,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    requests: list[dict[str, Any]] = []

    def start_handler(request: httpx.Request) -> httpx.Response:
        requests.append(
            {
                "json": json.loads(request.content.decode("utf-8")),
                "query": dict(request.url.params),
            }
        )
        return httpx.Response(200, json=_prediction_response_json(run_id="pred_real", status="running"))

    respx_mock.post("/compute/v1/predictions/structure-and-binding").mock(side_effect=start_handler)

    run_dir = client.experiments.start_prediction(
        entities=[
            {
                "chain_ids": ["A"],
                "modifications": [],
                "type": "protein",
                "value": "ACDE",
            }
        ],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="prediction-real-start",
        quiet=True,
    )

    assert run_dir.is_absolute()
    assert requests == [
        {
            "json": {
                "input": {
                    "entities": [
                        {
                            "chain_ids": ["A"],
                            "modifications": [],
                            "type": "protein",
                            "value": "ACDE",
                        }
                    ]
                },
                "model": "boltz-2.1",
                "idempotency_key": requests[0]["json"]["idempotency_key"],
            },
            "query": {},
        }
    ]
    assert "workspace_id" not in requests[0]["json"]
    assert "binding" not in requests[0]["json"]["input"]
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == "pred_real"
    assert run_json["status"] == "running"


@pytest.mark.respx
def test_structure_and_binding_typed_inputs_serialize_to_generated_payload(
    client: Boltz,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    requests: list[dict[str, Any]] = []

    def start_handler(request: httpx.Request) -> httpx.Response:
        requests.append(json.loads(request.content.decode("utf-8")))
        return httpx.Response(200, json=_prediction_response_json(run_id="pred_typed", status="running"))

    respx_mock.post("/compute/v1/predictions/structure-and-binding").mock(side_effect=start_handler)

    run_dir = client.experiments.start_structure_and_binding(
        entities=[
            Protein(
                value="ACDE",
                chain_ids=["A"],
                modifications=[CcdModification(residue_index=1, value="MSE")],
                msa=CustomMsa(format=MsaFormat.A3M, source=URLSource("https://files.example.com/protein.a3m")),
            ),
            LigandSmiles(value="CCO", chain_ids=["B"]),
            LigandCcd(value="ATP", chain_ids=["C"]),
        ],
        model=BoltzModel.BOLTZ_2_1,
        binding=LigandProteinBinding(binder_chain_id="B"),
        bonds=[Bond(atom1=PolymerAtom(chain_id="A", residue_index=0, atom_name="CA"), atom2=LigandAtom("C", "C1"))],
        constraints=[
            ContactConstraint(
                token1=PolymerContact(chain_id="A", residue_index=0),
                token2={"type": "ligand_contact", "chain_id": "C", "atom_name": "C1"},
                max_distance_angstrom=5.0,
                force=True,
            )
        ],
        model_options=ModelOptions(recycling_steps=2, sampling_steps=50),
        num_samples=2,
        root_dir=tmp_path / "runs",
        name="typed-prediction-start",
        quiet=True,
    )

    assert run_dir.is_absolute()
    assert requests == [
        {
            "input": {
                "entities": [
                    {
                        "chain_ids": ["A"],
                        "modifications": [{"residue_index": 1, "type": "ccd", "value": "MSE"}],
                        "msa": {
                            "format": "a3m",
                            "source": {"type": "url", "url": "https://files.example.com/protein.a3m"},
                            "type": "custom",
                        },
                        "type": "protein",
                        "value": "ACDE",
                    },
                    {"chain_ids": ["B"], "type": "ligand_smiles", "value": "CCO"},
                    {"chain_ids": ["C"], "type": "ligand_ccd", "value": "ATP"},
                ],
                "binding": {"binder_chain_id": "B", "type": "ligand_protein_binding"},
                "bonds": [
                    {
                        "atom1": {"atom_name": "CA", "chain_id": "A", "residue_index": 0, "type": "polymer_atom"},
                        "atom2": {"atom_name": "C1", "chain_id": "C", "type": "ligand_atom"},
                    }
                ],
                "constraints": [
                    {
                        "force": True,
                        "max_distance_angstrom": 5.0,
                        "token1": {"chain_id": "A", "residue_index": 0, "type": "polymer_contact"},
                        "token2": {"atom_name": "C1", "chain_id": "C", "type": "ligand_contact"},
                        "type": "contact",
                    }
                ],
                "model_options": {"recycling_steps": 2, "sampling_steps": 50},
                "num_samples": 2,
            },
            "model": "boltz-2.1",
            "idempotency_key": requests[0]["idempotency_key"],
        }
    ]
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == "pred_typed"


@pytest.mark.respx
@pytest.mark.parametrize("run_type", ["small_molecule_design", "small_molecule_library_screen"])
def test_small_molecule_targets_forward_constraints_and_bonds(
    client: Boltz,
    tmp_path: Path,
    respx_mock: Any,
    run_type: str,
) -> None:
    requests: list[dict[str, Any]] = []
    bond: SmallMoleculeTargetBond = {
        "atom1": {
            "type": "polymer_atom",
            "chain_id": "A",
            "residue_index": 0,
            "atom_name": "CA",
        },
        "atom2": {
            "type": "polymer_atom",
            "chain_id": "A",
            "residue_index": 1,
            "atom_name": "CB",
        },
    }
    constraint: SmallMoleculeTargetConstraint = {
        "type": "contact",
        "token1": {
            "type": "polymer_contact",
            "chain_id": "A",
            "residue_index": 0,
        },
        "token2": {
            "type": "polymer_contact",
            "chain_id": "A",
            "residue_index": 1,
        },
        "max_distance_angstrom": 6.0,
        "force": True,
    }
    target: SmallMoleculeTarget = {
        "entities": [
            {
                "chain_ids": ["A"],
                "modifications": [],
                "type": "protein",
                "value": "ACDE",
            }
        ],
        "pocket_residues": {"A": [1, 2]},
        "reference_ligands": ["CCO"],
        "bonds": [bond],
        "constraints": [constraint],
    }

    def start_handler(request: httpx.Request) -> httpx.Response:
        requests.append(json.loads(request.content.decode("utf-8")))
        if run_type == "small_molecule_design":
            return httpx.Response(200, json=_small_molecule_design_run_json(run_id="sm_design_1", status="running"))
        return httpx.Response(
            200,
            json=_small_molecule_library_screen_run_json(run_id="sm_screen_1", status="running"),
        )

    if run_type == "small_molecule_design":
        respx_mock.post("/compute/v1/small-molecule/design").mock(side_effect=start_handler)
        run_dir = client.experiments.start_small_molecule_design(
            num_molecules=1,
            target=target,
            root_dir=tmp_path / "runs",
            name="small-molecule-target-constraints",
            quiet=True,
        )
    else:
        respx_mock.post("/compute/v1/small-molecule/library-screen").mock(side_effect=start_handler)
        run_dir = client.experiments.start_small_molecule_library_screen(
            molecules=[{"smiles": "CCO", "id": "mol-1"}],
            target=target,
            root_dir=tmp_path / "runs",
            name="small-molecule-target-constraints",
            quiet=True,
        )

    assert run_dir.is_absolute()
    assert requests[0]["target"]["bonds"] == [bond]
    assert requests[0]["target"]["constraints"] == [constraint]
    run_json = _read_json(run_dir / "run.json")
    assert run_json["status"] == "running"
    assert run_json["id"] == ("sm_design_1" if run_type == "small_molecule_design" else "sm_screen_1")


@pytest.mark.respx
def test_generated_pipeline_methods_omit_absent_optional_query_fields(
    client: Boltz,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url = "https://files.example.com/real-design.tar.gz"
    archive_bytes = _make_archive_bytes({"result.txt": b"real"})
    start_bodies: list[dict[str, Any]] = []
    retrieve_queries: list[dict[str, str]] = []
    list_queries: list[dict[str, str]] = []

    def start_handler(request: httpx.Request) -> httpx.Response:
        start_bodies.append(json.loads(request.content.decode("utf-8")))
        return httpx.Response(
            200,
            json=_protein_design_run_json(run_id="design_real", status="running", latest_result_id="res_1"),
        )

    def retrieve_handler(request: httpx.Request) -> httpx.Response:
        retrieve_queries.append(dict(request.url.params))
        return httpx.Response(
            200,
            json=_protein_design_run_json(run_id="design_real", status="succeeded", latest_result_id="res_1"),
        )

    def list_handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        list_queries.append(params)
        if params.get("after_id") == "res_1":
            return httpx.Response(200, json={"data": [], "first_id": None, "last_id": None, "has_more": False})
        return httpx.Response(
            200,
            json={
                "data": [_protein_design_result_json("res_1", archive_url)],
                "first_id": "res_1",
                "last_id": "res_1",
                "has_more": False,
            },
        )

    respx_mock.post("/compute/v1/protein/design").mock(side_effect=start_handler)
    respx_mock.get("/compute/v1/protein/design/design_real").mock(side_effect=retrieve_handler)
    respx_mock.get("/compute/v1/protein/design/design_real/results").mock(side_effect=list_handler)
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    run_dir = client.experiments.start_protein_design(
        binder_specification=_protein_no_template_binder_spec(),
        num_proteins=1,
        target=_protein_no_template_target(),
        root_dir=tmp_path / "runs",
        name="design-real-transport",
        quiet=True,
    )
    client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    assert "workspace_id" not in start_bodies[0]
    assert retrieve_queries == [{"workspace_id": "ws_123"}]
    assert list_queries[0] == {"limit": "20", "workspace_id": "ws_123"}
    assert list_queries[1] == {"limit": "20", "workspace_id": "ws_123"}
    assert list_queries[2] == {"after_id": "res_1", "limit": "20", "workspace_id": "ws_123"}
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == "design_real"
    assert run_json["status"] == "succeeded"


@pytest.mark.respx
def test_download_results_default_run_dir_uses_deterministic_remote_id_name(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url = "https://files.example.com/prediction.tar.gz"
    archive_bytes = _make_archive_bytes({"nested/output.txt": b"done"})
    retrieve_calls = {"count": 0}

    def fake_retrieve(run_id: str, *, workspace_id: str | None = None) -> Any:
        del workspace_id
        retrieve_calls["count"] += 1
        return _prediction_response(run_id=run_id, status="succeeded", archive_url=archive_url)

    monkeypatch.setattr(client.predictions.structure_and_binding, "retrieve", fake_retrieve)
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    first_run_dir = client.experiments.download_results(
        id="pred_123",
        root_dir=tmp_path / "runs",
        quiet=True,
        poll_interval_seconds=0.0,
    )
    second_run_dir = client.experiments.download_results(
        id="pred_123",
        root_dir=tmp_path / "runs",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    assert first_run_dir == second_run_dir
    assert first_run_dir == tmp_path / "runs" / deterministic_name("pred_123")
    assert first_run_dir.name == "clear-pocket-screens-a8d3cc"
    assert retrieve_calls["count"] == 2
    assert (first_run_dir / "outputs" / "files" / "nested" / "output.txt").is_file()


@pytest.mark.respx
def test_download_results_metadata_only_skips_pipeline_artifacts(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    run_id = "prot_des_123"
    archive_url_1 = "https://files.example.com/res_1.tar.gz"
    archive_url_2 = "https://files.example.com/res_2.tar.gz"

    def retrieve(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        del _args, _kwargs
        return _pipeline_response(run_id=run_id, status="succeeded", latest_result_id="res_2")

    monkeypatch.setattr(client.protein.design, "retrieve", retrieve)

    def list_results(
        run_id: str,
        after_id: str | None = None,
        limit: int | None = None,
        workspace_id: str | None = None,
    ) -> Any:
        del run_id, limit, workspace_id
        if after_id is None:
            return _page(
                _pipeline_result("res_1", archive_url_1),
                _pipeline_result("res_2", archive_url_2),
            )
        return _page()

    monkeypatch.setattr(client.protein.design, "list_results", list_results)

    def unexpected_stream(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("metadata_only must not download artifacts")

    monkeypatch.setattr(client._client, "stream", unexpected_stream)

    run_dir = client.experiments.download_results(
        id=run_id,
        root_dir=tmp_path / "runs",
        download_mode="metadata_only",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    metadata = _read_metadata(run_dir)
    manifest = _read_jsonl(run_dir / "results" / "index.jsonl")

    assert metadata["download_mode"] == "metadata_only"
    assert not (run_dir / "results" / "res_1").exists()
    assert [entry["id"] for entry in manifest] == ["res_1", "res_2"]
    assert "paths" not in manifest[0]

    resumed_run_dir = client.experiments.download_results(
        id=run_id,
        root_dir=tmp_path / "runs",
        quiet=True,
        poll_interval_seconds=0.0,
    )
    assert resumed_run_dir == run_dir
    assert _read_jsonl(run_dir / "results" / "index.jsonl") == manifest


@pytest.mark.respx
def test_pipeline_result_manifest_is_append_only_when_resuming(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    run_id = "prot_des_append"
    run_dir = tmp_path / "runs" / "append-only"
    run_dir.mkdir(parents=True)
    metadata = RunMetadata.create(
        name=run_dir.name,
        run_type="protein_design",
        download_mode="metadata_only",
        request_fingerprint="test",
        idempotency_key="download_test",
    )
    metadata.remote.run_id = run_id
    metadata.remote.status = "running"
    metadata.remote.workspace_id = "ws_123"
    metadata.cursor_after_id = "res_1"
    save_metadata(
        run_dir,
        metadata,
    )
    manifest_path = run_dir / "results" / "index.jsonl"
    manifest_path.parent.mkdir(parents=True)
    existing_manifest = '{"note":"keep formatting","id":"res_1"}\n'
    manifest_path.write_text(existing_manifest, encoding="utf-8")

    def retrieve(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        del _args, _kwargs
        return _pipeline_response(run_id=run_id, status="succeeded", latest_result_id="res_2")

    monkeypatch.setattr(client.protein.design, "retrieve", retrieve)

    def list_results(
        run_id: str,
        after_id: str | None = None,
        limit: int | None = None,
        workspace_id: str | None = None,
    ) -> Any:
        del run_id, limit, workspace_id
        if after_id == "res_1":
            return _page(_pipeline_result("res_2", "https://files.example.com/res_2.tar.gz"))
        return _page()

    monkeypatch.setattr(client.protein.design, "list_results", list_results)

    client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    updated_manifest = manifest_path.read_text(encoding="utf-8")
    assert updated_manifest.startswith(existing_manifest)
    assert _read_jsonl(manifest_path) == [
        {"note": "keep formatting", "id": "res_1"},
        {"id": "res_2"},
    ]


@pytest.mark.respx
def test_prediction_retries_submission_with_same_idempotency_key(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    idempotency_keys: list[str] = []
    attempts = {"count": 0}

    def flaky_start(*, input: Any, model: str, idempotency_key: str, workspace_id: str | None = None) -> Any:
        del input, model, workspace_id
        idempotency_keys.append(idempotency_key)
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("connection lost before confirmation")
        return _prediction_response(run_id="pred_retry", status="running")

    monkeypatch.setattr(client.predictions.structure_and_binding, "start", flaky_start)

    with pytest.raises(RuntimeError, match="connection lost"):
        client.experiments.start_prediction(
            entities=[],
            model="boltz-2.1",
            root_dir=tmp_path / "runs",
            name="retry-me",
            quiet=True,
        )

    run_dir = client.experiments.start_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="retry-me",
        quiet=True,
    )

    assert run_dir.name == "retry-me"
    assert len(idempotency_keys) == 2
    assert idempotency_keys[0] == idempotency_keys[1]


@pytest.mark.respx
def test_prediction_wait_and_download_by_name_recovers_missing_extraction_dir(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url = "https://files.example.com/prediction.tar.gz"
    archive_bytes = _make_archive_bytes({"nested/output.txt": b"done"})
    retrieve_calls = {"count": 0}

    def fake_start(*, input: Any, model: str, idempotency_key: str, workspace_id: str | None = None) -> Any:
        del input, model, idempotency_key, workspace_id
        return _prediction_response(run_id="pred_resume", status="running")

    def fake_retrieve(run_id: str, *, workspace_id: str | None = None) -> Any:
        del run_id, workspace_id
        retrieve_calls["count"] += 1
        return _prediction_response(run_id="pred_resume", status="succeeded", archive_url=archive_url)

    monkeypatch.setattr(client.predictions.structure_and_binding, "start", fake_start)
    monkeypatch.setattr(client.predictions.structure_and_binding, "retrieve", fake_retrieve)
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    run_dir = client.experiments.run_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="resume-prediction",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    extracted_dir = run_dir / "outputs" / "files"
    assert extracted_dir.is_dir()
    shutil.rmtree(extracted_dir)

    client.experiments.wait_and_download(
        name="resume-prediction",
        root_dir=tmp_path / "runs",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    assert extracted_dir.is_dir()
    assert retrieve_calls["count"] >= 2


def test_metadata_loader_rejects_missing_required_top_level_key(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_missing_key"),
    )

    run_dir = client.experiments.start_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="missing-metadata-key",
        quiet=True,
    )

    metadata_path = run_dir / ".boltz-run.json"
    metadata = _read_metadata(run_dir)
    del metadata["remote"]
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ExperimentError, match=r"Invalid run metadata\.remote: .*required"):
        load_metadata(run_dir)


def test_metadata_loader_accepts_and_preserves_unexpected_top_level_key(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_extra_key"),
    )

    run_dir = client.experiments.start_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="extra-metadata-key",
        quiet=True,
    )

    metadata_path = run_dir / ".boltz-run.json"
    metadata = _read_metadata(run_dir)
    metadata["unexpected"] = True
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    loaded_metadata = load_metadata(run_dir)
    save_metadata(run_dir, loaded_metadata)

    assert _read_metadata(run_dir)["unexpected"] is True


@pytest.mark.respx
def test_pipeline_restart_with_pending_page_continues_successfully(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url_1 = "https://files.example.com/res_1.tar.gz"
    archive_url_2 = "https://files.example.com/res_2.tar.gz"
    archive_bytes = _make_archive_bytes()
    run_id = "pipe_resume"

    monkeypatch.setattr(
        client.protein.design,
        "start",
        _pipeline_start_stub(run_id=run_id, latest_result_id="res_2"),
    )
    monkeypatch.setattr(
        client.protein.design,
        "retrieve",
        _pipeline_retrieve_stub(run_id=run_id, status="running", latest_result_id="res_2"),
    )

    def fake_list_results(
        run_id: str, after_id: str | None = None, limit: int | None = None, workspace_id: str | None = None
    ) -> Any:
        del run_id, limit, workspace_id
        if after_id is None:
            return _page(
                _pipeline_result("res_1", archive_url_1),
                _pipeline_result("res_2", archive_url_2),
            )
        return _page()

    monkeypatch.setattr(client.protein.design, "list_results", fake_list_results)

    calls = {"archive_2": 0}
    respx_mock.get(archive_url_1).mock(return_value=httpx.Response(200, content=archive_bytes))

    def archive_2_handler(request: httpx.Request) -> httpx.Response:
        del request
        calls["archive_2"] += 1
        if calls["archive_2"] == 1:
            return httpx.Response(500)
        return httpx.Response(200, content=archive_bytes)

    respx_mock.get(archive_url_2).mock(side_effect=archive_2_handler)

    run_dir = client.experiments.start_protein_design(
        binder_specification=_protein_no_template_binder_spec(),
        num_proteins=2,
        target=_protein_no_template_target(),
        root_dir=tmp_path / "runs",
        name="pipe-restart",
        quiet=True,
    )

    with pytest.raises(httpx.HTTPStatusError):
        client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    metadata = _read_metadata(run_dir)
    assert metadata["pending"]["result_ids"] == ["res_2"]

    monkeypatch.setattr(
        client.protein.design,
        "retrieve",
        _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_2"),
    )
    client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    assert (run_dir / "results" / "res_1" / "files").is_dir()
    assert (run_dir / "results" / "res_2" / "files").is_dir()
    assert _read_metadata(run_dir)["pending"] is None


def test_prediction_download_recovers_from_partial_temp_file(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    archive_url = "https://files.example.com/prediction.tar.gz"
    archive_bytes = _make_archive_bytes()

    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_part"),
    )
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "retrieve",
        _prediction_retrieve_stub("pred_part", status="succeeded", archive_url=archive_url),
    )

    class _BrokenResponse:
        def __enter__(self) -> "_BrokenResponse":
            return self

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            return None

        def raise_for_status(self) -> None:
            return None

        def iter_bytes(self) -> Any:
            yield b"partial"
            raise RuntimeError("stream interrupted")

    class _GoodResponse:
        def __enter__(self) -> "_GoodResponse":
            return self

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            return None

        def raise_for_status(self) -> None:
            return None

        def iter_bytes(self) -> Any:
            yield archive_bytes

    run_dir = client.experiments.start_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="partial-prediction",
        quiet=True,
    )

    def broken_stream(*_args: Any, **_kwargs: Any) -> _BrokenResponse:
        del _args, _kwargs
        return _BrokenResponse()

    monkeypatch.setattr(client._client, "stream", broken_stream)
    with pytest.raises(RuntimeError, match="stream interrupted"):
        client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    archive_path = run_dir / "outputs" / "archive.tar.gz"
    assert not archive_path.exists()
    assert archive_path.with_name("archive.tar.gz.part").exists()

    def good_stream(*_args: Any, **_kwargs: Any) -> _GoodResponse:
        del _args, _kwargs
        return _GoodResponse()

    monkeypatch.setattr(client._client, "stream", good_stream)
    client.experiments.wait_and_download(run_dir=run_dir, quiet=True, poll_interval_seconds=0.0)

    assert archive_path.exists()
    assert not archive_path.with_name("archive.tar.gz.part").exists()
    assert (run_dir / "outputs" / "files").is_dir()


@pytest.mark.respx
def test_request_fingerprint_mismatch_fails_clearly(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_fingerprint"),
    )

    client.experiments.start_prediction(
        entities=[{"type": "protein", "chain_ids": ["A"], "modifications": [], "value": "AAAA"}],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="same-name",
        quiet=True,
    )

    with pytest.raises(ExperimentFingerprintMismatchError):
        client.experiments.start_prediction(
            entities=[{"type": "protein", "chain_ids": ["A"], "modifications": [], "value": "BBBB"}],
            model="boltz-2.1",
            root_dir=tmp_path / "runs",
            name="same-name",
            quiet=True,
        )


@pytest.mark.respx
def test_local_cif_paths_are_normalized_to_inline_base64(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    target_path = tmp_path / "target.cif"
    binder_path = tmp_path / "binder.cif"
    target_path.write_text("data_target", encoding="utf-8")
    binder_path.write_text("data_binder", encoding="utf-8")

    captured: dict[str, Any] = {}

    def fake_start(
        *,
        binder_specification: Any,
        num_proteins: int,
        target: Any,
        idempotency_key: str,
        workspace_id: str | None = None,
    ) -> Any:
        del num_proteins, idempotency_key, workspace_id
        captured["binder_specification"] = binder_specification
        captured["target"] = target
        return _pipeline_response(run_id="design_1", status="running")

    monkeypatch.setattr(client.protein.design, "start", fake_start)

    client.experiments.start_protein_design(
        binder_specification=_structure_template_binder_spec(binder_path),
        num_proteins=4,
        target=_structure_template_target(target_path),
        root_dir=tmp_path / "runs",
        name="normalize-cif",
        quiet=True,
    )

    assert captured["binder_specification"]["structure"]["type"] == "base64"
    assert captured["target"]["structure"]["type"] == "base64"
    assert captured["binder_specification"]["structure"]["media_type"] == "chemical/x-cif"
    assert captured["target"]["structure"]["media_type"] == "chemical/x-cif"


@pytest.mark.respx
def test_explicit_base64_structure_sources_pass_through_for_protein_design(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    binder_source = _base64_cif_source("YmluZGVy")
    target_source = _base64_cif_source("dGFyZ2V0")

    captured: dict[str, Any] = {}

    def fake_start(
        *,
        binder_specification: Any,
        num_proteins: int,
        target: Any,
        idempotency_key: str,
        workspace_id: str | None = None,
    ) -> Any:
        del num_proteins, idempotency_key, workspace_id
        captured["binder_specification"] = binder_specification
        captured["target"] = target
        return _pipeline_response(run_id="design_base64", status="running")

    monkeypatch.setattr(client.protein.design, "start", fake_start)
    binder_input: Any = _structure_template_binder_spec(binder_source)
    target_input: Any = _structure_template_target(target_source)

    client.experiments.start_protein_design(
        binder_specification=binder_input,
        num_proteins=4,
        target=target_input,
        root_dir=tmp_path / "runs",
        name="base64-design",
        quiet=True,
    )

    assert captured["binder_specification"]["structure"] == binder_source
    assert captured["target"]["structure"] == target_source


@pytest.mark.respx
def test_explicit_base64_structure_sources_require_cif_media_type(
    client: Boltz,
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="chemical/x-cif"):
        client.experiments.start_protein_design(
            binder_specification=_structure_template_binder_spec(
                {
                    "type": "base64",
                    "media_type": "application/octet-stream",
                    "data": "YmluZGVy",
                }
            ),
            num_proteins=4,
            target=_protein_no_template_target(),
            root_dir=tmp_path / "runs",
            name="invalid-base64-media-type",
            quiet=True,
        )


@pytest.mark.respx
def test_protein_library_screen_target_supports_cif_paths_and_base64(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    target_path = tmp_path / "screen-target.cif"
    target_path.write_text("data_target", encoding="utf-8")
    base64_source = _base64_cif_source("c2NyZWVu")

    captured: list[Any] = []

    def fake_start(
        *,
        proteins: Any,
        target: Any,
        idempotency_key: str,
        workspace_id: str | None = None,
    ) -> Any:
        del proteins, idempotency_key, workspace_id
        captured.append(target)
        return _pipeline_response(run_id="screen_1", status="running")

    monkeypatch.setattr(client.protein.library_screen, "start", fake_start)
    path_target_input: Any = _structure_template_target(target_path)
    base64_target_input: Any = _structure_template_target(base64_source)

    client.experiments.start_protein_library_screen(
        proteins=[],
        target=path_target_input,
        root_dir=tmp_path / "runs",
        name="screen-path",
        quiet=True,
    )
    client.experiments.start_protein_library_screen(
        proteins=[],
        target=base64_target_input,
        root_dir=tmp_path / "runs",
        name="screen-base64",
        quiet=True,
    )

    assert captured[0]["structure"]["type"] == "base64"
    assert captured[0]["structure"]["media_type"] == "chemical/x-cif"
    assert captured[1]["structure"] == base64_source


@pytest.mark.respx
def test_local_cif_file_content_changes_trigger_fingerprint_mismatch(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    target_path = tmp_path / "target.cif"
    binder_path = tmp_path / "binder.cif"
    target_path.write_text("target_v1", encoding="utf-8")
    binder_path.write_text("binder_v1", encoding="utf-8")

    monkeypatch.setattr(client.protein.design, "start", _pipeline_start_stub(run_id="design_fp"))

    client.experiments.start_protein_design(
        binder_specification=_structure_template_binder_spec(binder_path),
        num_proteins=4,
        target=_structure_template_target(target_path),
        root_dir=tmp_path / "runs",
        name="file-fingerprint",
        quiet=True,
    )

    binder_path.write_text("binder_v2", encoding="utf-8")

    with pytest.raises(ExperimentFingerprintMismatchError):
        client.experiments.start_protein_design(
            binder_specification=_structure_template_binder_spec(binder_path),
            num_proteins=4,
            target=_structure_template_target(target_path),
            root_dir=tmp_path / "runs",
            name="file-fingerprint",
            quiet=True,
        )


@pytest.mark.respx
def test_local_pdb_paths_are_rejected(client: Boltz, tmp_path: Path) -> None:
    pdb_path = tmp_path / "target.pdb"
    pdb_path.write_text("ATOM", encoding="utf-8")

    with pytest.raises(ExperimentError, match="PDB"):
        client.experiments.start_protein_design(
            binder_specification=_protein_no_template_binder_spec(),
            num_proteins=1,
            target=_structure_template_target(pdb_path),
            root_dir=tmp_path / "runs",
            name="reject-pdb",
            quiet=True,
        )


@pytest.mark.respx
@pytest.mark.parametrize(
    ("run_type", "starter"),
    PIPELINE_STARTERS,
)
def test_stop_supported_for_pipelines(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    run_type: PipelineRunType,
    starter: PipelineStarter,
) -> None:
    stop_calls = {"count": 0}
    run_id = f"{run_type}_id"

    if run_type == "protein_design":
        monkeypatch.setattr(client.protein.design, "start", _pipeline_start_stub(run_id=run_id))
        monkeypatch.setattr(client.protein.design, "stop", _pipeline_stop_stub(stop_calls))
    elif run_type == "protein_library_screen":
        monkeypatch.setattr(client.protein.library_screen, "start", _pipeline_start_stub(run_id=run_id))
        monkeypatch.setattr(client.protein.library_screen, "stop", _pipeline_stop_stub(stop_calls))
    elif run_type == "small_molecule_design":
        monkeypatch.setattr(client.small_molecule.design, "start", _pipeline_start_stub(run_id=run_id))
        monkeypatch.setattr(client.small_molecule.design, "stop", _pipeline_stop_stub(stop_calls))
    else:
        monkeypatch.setattr(client.small_molecule.library_screen, "start", _pipeline_start_stub(run_id=run_id))
        monkeypatch.setattr(client.small_molecule.library_screen, "stop", _pipeline_stop_stub(stop_calls))

    run_dir = starter(client, tmp_path)
    client.experiments.stop(run_dir=run_dir, quiet=True)

    assert stop_calls["count"] == 1
    assert _read_metadata(run_dir)["remote"]["status"] == "stopped"


@pytest.mark.respx
def test_stop_rejected_for_prediction(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_stop"),
    )
    run_dir = client.experiments.start_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="stop-prediction",
        quiet=True,
    )

    with pytest.raises(ExperimentUnsupportedOperationError):
        client.experiments.stop(run_dir=run_dir, quiet=True)


@pytest.mark.respx
def test_metadata_remains_bounded_after_many_pipeline_results(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> None:
    archive_url = "https://files.example.com/shared.tar.gz"
    archive_bytes = _make_archive_bytes()
    pages = {
        None: _page(*[_pipeline_result(f"res_{index:02d}", archive_url) for index in range(1, 21)]),
        "res_20": _page(*[_pipeline_result(f"res_{index:02d}", archive_url) for index in range(21, 41)]),
        "res_40": _page(*[_pipeline_result(f"res_{index:02d}", archive_url) for index in range(41, 46)]),
        "res_45": _page(),
    }

    monkeypatch.setattr(
        client.small_molecule.library_screen,
        "start",
        _pipeline_start_stub(run_id="many_results", status="succeeded", latest_result_id="res_45"),
    )
    monkeypatch.setattr(
        client.small_molecule.library_screen,
        "retrieve",
        _pipeline_retrieve_stub(run_id="many_results", status="succeeded", latest_result_id="res_45"),
    )

    def many_results_list(
        screen_id: str,
        after_id: str | None = None,
        limit: int | None = None,
        workspace_id: str | None = None,
    ) -> Any:
        del screen_id, limit, workspace_id
        return pages[after_id]

    monkeypatch.setattr(client.small_molecule.library_screen, "list_results", many_results_list)
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    run_dir = client.experiments.run_small_molecule_library_screen(
        molecules=[],
        target={"entities": []},
        root_dir=tmp_path / "runs",
        name="many-results",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    metadata_text = (run_dir / ".boltz-run.json").read_text(encoding="utf-8")
    assert len(metadata_text) < 2048
    assert '"result_ids"' not in metadata_text
    assert '"res_01"' not in metadata_text


@pytest.mark.respx
def test_progress_output_can_be_suppressed(
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
    capsys: pytest.CaptureFixture[str],
) -> None:
    archive_url = "https://files.example.com/progress.tar.gz"
    archive_bytes = _make_archive_bytes()

    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_progress"),
    )
    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "retrieve",
        _prediction_retrieve_stub("pred_progress", status="succeeded", archive_url=archive_url),
    )
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    client.experiments.run_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="progress-visible",
        quiet=False,
        poll_interval_seconds=0.0,
    )
    visible_output = capsys.readouterr().out
    assert "Prediction run ID" in visible_output

    client.experiments.run_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="progress-hidden",
        quiet=True,
        poll_interval_seconds=0.0,
    )
    assert capsys.readouterr().out == ""


def _run_prediction_happy_path(
    *,
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
) -> Path:
    archive_url = "https://files.example.com/prediction.tar.gz"
    archive_bytes = _make_archive_bytes(
        {
            "prediction.txt": b"prediction",
            "result/predicted_structure.cif": b"data_prediction\n",
        }
    )
    retrieve_calls = {"count": 0}

    monkeypatch.setattr(
        client.predictions.structure_and_binding,
        "start",
        _prediction_start_stub("pred_happy"),
    )

    def fake_retrieve(run_id: str, *, workspace_id: str | None = None) -> Any:
        del run_id, workspace_id
        retrieve_calls["count"] += 1
        if retrieve_calls["count"] == 1:
            return _prediction_response(run_id="pred_happy", status="running")
        return _prediction_response(run_id="pred_happy", status="succeeded", archive_url=archive_url)

    monkeypatch.setattr(client.predictions.structure_and_binding, "retrieve", fake_retrieve)
    respx_mock.get(archive_url).mock(return_value=httpx.Response(200, content=archive_bytes))

    run_dir = client.experiments.run_prediction(
        entities=[],
        model="boltz-2.1",
        root_dir=tmp_path / "runs",
        name="prediction-happy",
        workspace_id="ws_123",
        quiet=True,
        poll_interval_seconds=0.0,
    )

    assert (run_dir / "outputs" / "archive.tar.gz").exists()
    assert (run_dir / "outputs" / "files").is_dir()
    assert (run_dir / "outputs" / "files" / "result" / "pred_happy_predicted.cif").exists()
    assert not (run_dir / "outputs" / "files" / "result" / "predicted_structure.cif").exists()
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == "pred_happy"
    assert run_json["status"] == "succeeded"
    assert run_json["output"]["best_sample"]["metrics"] == {"complex_plddt": 0.5}
    _assert_no_download_urls(run_json)
    return run_dir


def _run_pipeline_happy_path(
    *,
    client: Boltz,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    respx_mock: Any,
    run_type: PipelineRunType,
) -> Path:
    archive_url_1 = f"https://files.example.com/{run_type}_1.tar.gz"
    archive_url_2 = f"https://files.example.com/{run_type}_2.tar.gz"
    archive_bytes = _make_archive_bytes(
        {
            "result/metrics.json": b'{"binding_confidence":0.9}',
            "result/predicted_structure.cif": b"data_prediction\n",
            "result/pae.npz": b"npz",
        }
    )
    run_id = f"{run_type}_id"

    def list_results(
        run_id: str, after_id: str | None = None, limit: int | None = None, workspace_id: str | None = None
    ) -> Any:
        del run_id, limit, workspace_id
        if after_id is None:
            return _page(
                _pipeline_result("res_1", archive_url_1, **_pipeline_result_fields(run_type, "res_1")),
                _pipeline_result("res_2", archive_url_2, **_pipeline_result_fields(run_type, "res_2")),
            )
        return _page()

    run_method: Any
    if run_type == "protein_design":
        monkeypatch.setattr(
            client.protein.design, "start", _pipeline_start_stub(run_id=run_id, latest_result_id="res_2")
        )
        monkeypatch.setattr(
            client.protein.design,
            "retrieve",
            _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_2"),
        )
        monkeypatch.setattr(client.protein.design, "list_results", list_results)
        run_method = client.experiments.run_protein_design
        kwargs: dict[str, Any] = {
            "binder_specification": _protein_no_template_binder_spec(),
            "num_proteins": 2,
            "target": _protein_no_template_target(),
        }
    elif run_type == "protein_library_screen":
        monkeypatch.setattr(
            client.protein.library_screen,
            "start",
            _pipeline_start_stub(run_id=run_id, latest_result_id="res_2"),
        )
        monkeypatch.setattr(
            client.protein.library_screen,
            "retrieve",
            _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_2"),
        )
        monkeypatch.setattr(client.protein.library_screen, "list_results", list_results)
        run_method = client.experiments.run_protein_library_screen
        kwargs = {
            "proteins": [],
            "target": _protein_no_template_target(),
        }
    elif run_type == "small_molecule_design":
        monkeypatch.setattr(
            client.small_molecule.design,
            "start",
            _pipeline_start_stub(run_id=run_id, latest_result_id="res_2"),
        )
        monkeypatch.setattr(
            client.small_molecule.design,
            "retrieve",
            _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_2"),
        )
        monkeypatch.setattr(client.small_molecule.design, "list_results", list_results)
        run_method = client.experiments.run_small_molecule_design
        kwargs = {"num_molecules": 2, "target": _small_molecule_target()}
    else:
        monkeypatch.setattr(
            client.small_molecule.library_screen,
            "start",
            _pipeline_start_stub(run_id=run_id, latest_result_id="res_2"),
        )
        monkeypatch.setattr(
            client.small_molecule.library_screen,
            "retrieve",
            _pipeline_retrieve_stub(run_id=run_id, status="succeeded", latest_result_id="res_2"),
        )
        monkeypatch.setattr(client.small_molecule.library_screen, "list_results", list_results)
        run_method = client.experiments.run_small_molecule_library_screen
        kwargs = {"molecules": [], "target": _small_molecule_target()}

    respx_mock.get(archive_url_1).mock(return_value=httpx.Response(200, content=archive_bytes))
    respx_mock.get(archive_url_2).mock(return_value=httpx.Response(200, content=archive_bytes))

    run_dir = cast(
        Path,
        run_method(
            root_dir=tmp_path / "runs",
            name=f"{run_type}-happy",
            workspace_id="ws_123",
            quiet=True,
            poll_interval_seconds=0.0,
            **kwargs,
        ),
    )

    assert (run_dir / "results" / "res_1" / "archive.tar.gz").exists()
    assert (run_dir / "results" / "res_1" / "files").is_dir()
    assert (run_dir / "results" / "res_1" / "files" / "result" / "res_1_predicted.cif").exists()
    assert not (run_dir / "results" / "res_1" / "files" / "result" / "predicted_structure.cif").exists()
    assert (run_dir / "results" / "res_2" / "archive.tar.gz").exists()
    assert (run_dir / "results" / "res_2" / "files").is_dir()
    assert (run_dir / "results" / "res_2" / "files" / "result" / "res_2_predicted.cif").exists()
    run_json = _read_json(run_dir / "run.json")
    assert run_json["id"] == run_id
    assert run_json["status"] == "succeeded"
    _assert_pipeline_result_metadata(run_dir, run_type)
    return run_dir
