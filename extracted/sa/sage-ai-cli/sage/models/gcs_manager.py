from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class PullResult:
    ok: bool
    message: str = ""
    model_name: str = ""


@dataclass(frozen=True)
class ConversionResult:
    ok: bool
    message: str = ""
    input_path: str = ""
    output_path: str = ""


@dataclass(frozen=True)
class UploadResult:
    ok: bool
    message: str = ""
    bucket: str = ""
    object_name: str = ""


@dataclass(frozen=True)
class GCSModel:
    name: str
    display_name: str
    filename: str
    url: str
    size_gb: float | None = None
    params: str | None = None
    family: str | None = None
    description: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    checksum: str | None = None
    uploaded_at: str | None = None
    source: str | None = None


class OllamaClient:
    def pull(self, model_name: str) -> PullResult:
        if not model_name.strip():
            return PullResult(ok=False, message="missing model name", model_name=model_name)
        return PullResult(ok=True, message="ok", model_name=model_name)


class GCSModelManager:
    def __init__(self, bucket_name: str, credentials_path: str | None = None, models_dir: str | Path | None = None):
        self._bucket_name = bucket_name
        self._credentials_path = credentials_path
        self._models_dir = Path(models_dir) if models_dir is not None else (Path.home() / ".sage" / "models")
        self._models_dir.mkdir(parents=True, exist_ok=True)

        try:
            from google.cloud import storage  # type: ignore
        except Exception as exc:
            raise RuntimeError("google-cloud-storage is required for GCSModelManager") from exc

        if credentials_path:
            self._client = storage.Client.from_service_account_json(credentials_path)
        else:
            self._client = storage.Client()
        self._bucket = self._client.bucket(bucket_name)

    def _public_url(self, blob_name: str) -> str:
        return f"https://storage.googleapis.com/{self._bucket_name}/{blob_name}"

    def _iter_blobs(self) -> Iterable[Any]:
        return self._bucket.list_blobs()

    def list_gcs_models(self) -> list[GCSModel]:
        models: list[GCSModel] = []
        for blob in self._iter_blobs():
            name = getattr(blob, "name", "")
            if not isinstance(name, str) or not name:
                continue
            if not name.lower().endswith(".gguf"):
                continue
            size_bytes = getattr(blob, "size", None)
            size_gb = (float(size_bytes) / (1024**3)) if isinstance(size_bytes, (int, float)) else None
            updated = getattr(blob, "updated", None)
            uploaded_at = None
            if isinstance(updated, datetime):
                uploaded_at = updated.isoformat(timespec="seconds")
            models.append(
                GCSModel(
                    name=Path(name).stem,
                    display_name=Path(name).stem,
                    filename=name,
                    url=self._public_url(name),
                    size_gb=size_gb,
                    uploaded_at=uploaded_at,
                    source="gcs",
                )
            )
        return sorted(models, key=lambda m: m.name)

    def get_model_info(self, model_name: str) -> GCSModel | None:
        model_name = model_name.strip()
        if not model_name:
            return None
        candidates = self.list_gcs_models()
        for m in candidates:
            if m.name == model_name:
                return m
        return None

    def download_from_gcs(self, model_name: str) -> Path | None:
        info = self.get_model_info(model_name)
        if not info:
            return None
        dest = self._models_dir / Path(info.filename).name
        blob = self._bucket.blob(info.filename)
        blob.download_to_filename(str(dest))
        return dest

    def delete_from_gcs(self, filename: str) -> bool:
        filename = filename.strip()
        if not filename:
            return False
        blob = self._bucket.blob(filename)
        blob.delete()
        return True

