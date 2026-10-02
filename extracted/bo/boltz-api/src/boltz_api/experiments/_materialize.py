from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from ._errors import ExperimentError
from .._client import Boltz
from ._progress import ProgressSink

SUPPORTED_ARCHIVE_SUFFIXES = (".tar.gz", ".tgz", ".tar", ".zip")


def prediction_paths(run_dir: Path, archive_url: str) -> tuple[Path, Path]:
    suffix = archive_suffix_from_url(archive_url)
    return run_dir / "outputs" / f"archive{suffix}", run_dir / "outputs" / "files"


def pipeline_paths(run_dir: Path, result_id: str, archive_url: str) -> tuple[Path, Path]:
    suffix = archive_suffix_from_url(archive_url)
    return run_dir / "results" / result_id / f"archive{suffix}", run_dir / "results" / result_id / "files"


def archive_suffix_from_url(url: str) -> str:
    name = Path(urlparse(url).path).name
    lower_name = name.lower()
    for suffix in SUPPORTED_ARCHIVE_SUFFIXES:
        if lower_name.endswith(suffix):
            return suffix
    raise ExperimentError(f"Archive URL does not include a supported file suffix: {url}")


def is_materialized(archive_path: Path, extracted_dir: Path) -> bool:
    return archive_path.exists() and extracted_dir.is_dir()


def materialize_archive(
    *,
    client: Boltz,
    archive_url: str,
    archive_path: Path,
    extracted_dir: Path,
    sink: ProgressSink,
) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    if not archive_path.exists():
        sink.info(f"Downloading archive to {archive_path}")
        _download_archive(client=client, url=archive_url, destination=archive_path)

    if extracted_dir.is_dir():
        return

    sink.info(f"Extracting archive to {extracted_dir}")
    _extract_archive(archive_path=archive_path, destination=extracted_dir)


def prefix_prediction_structure_file(*, run_dir: Path, prediction_id: str) -> None:
    _prefix_structure_artifact_file(extracted_dir=run_dir / "outputs" / "files", artifact_id=prediction_id)


def prefix_pipeline_result_structure_file(*, result_dir: Path, result_id: str) -> None:
    _prefix_structure_artifact_file(extracted_dir=result_dir / "files", artifact_id=result_id)


def _prefix_structure_artifact_file(*, extracted_dir: Path, artifact_id: str) -> None:
    if not extracted_dir.is_dir():
        return

    structure_path = _find_structure_artifact(extracted_dir=extracted_dir, result_id=artifact_id)
    if structure_path is None:
        return

    prefixed_name = prefixed_structure_artifact_name(result_id=artifact_id, structure_path=structure_path)
    if structure_path.name == prefixed_name:
        return

    prefixed_path = structure_path.with_name(prefixed_name)
    if prefixed_path.exists():
        return

    structure_path.replace(prefixed_path)


def preferred_structure_artifact_paths(result_id: str) -> tuple[str, ...]:
    return (
        f"result/{_prefixed_structure_artifact_name_with_suffix(result_id=result_id, suffix='.cif')}",
        _prefixed_structure_artifact_name_with_suffix(result_id=result_id, suffix=".cif"),
        f"result/{_prefixed_structure_artifact_name_with_suffix(result_id=result_id, suffix='.pdb')}",
        _prefixed_structure_artifact_name_with_suffix(result_id=result_id, suffix=".pdb"),
        "result/predicted_structure.cif",
        "predicted_structure.cif",
    )


def prefixed_structure_artifact_name(*, result_id: str, structure_path: Path) -> str:
    suffix = structure_path.suffix.lower()
    if suffix != ".pdb":
        suffix = ".cif"
    return _prefixed_structure_artifact_name_with_suffix(result_id=result_id, suffix=suffix)


def _prefixed_structure_artifact_name_with_suffix(*, result_id: str, suffix: str) -> str:
    return f"{result_id}_predicted{suffix}"


def _find_structure_artifact(*, extracted_dir: Path, result_id: str) -> Path | None:
    for preferred_path in preferred_structure_artifact_paths(result_id):
        candidate = extracted_dir / preferred_path
        if candidate.is_file():
            return candidate

    matches = sorted(path for path in extracted_dir.rglob("*") if path.is_file() and _matches_structure_artifact(path))
    return matches[0] if matches else None


def _matches_structure_artifact(path: Path) -> bool:
    basename = path.name.lower()
    return basename == "predicted_structure.cif" or basename.endswith(".cif") or basename.endswith(".pdb")


def _download_archive(*, client: Boltz, url: str, destination: Path) -> None:
    tmp_path = destination.with_name(f"{destination.name}.part")
    if tmp_path.exists():
        tmp_path.unlink()

    with client._client.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        with tmp_path.open("wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

    tmp_path.replace(destination)


def _extract_archive(*, archive_path: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)

    base_dir = destination.parent
    base_dir.mkdir(parents=True, exist_ok=True)
    temp_dir_path = Path(tempfile.mkdtemp(prefix=f"{destination.name}.tmp-", dir=str(base_dir)))
    try:
        shutil.unpack_archive(str(archive_path), str(temp_dir_path))
        temp_dir_path.replace(destination)
    except Exception as exc:
        shutil.rmtree(temp_dir_path, ignore_errors=True)
        if isinstance(exc, shutil.ReadError):
            raise ExperimentError(f"Unsupported archive format for {archive_path}") from exc
        raise
