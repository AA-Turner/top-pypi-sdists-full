"""Model registry with versioning, resume downloads, deduplication, and local import.

All model sources must be from GitHub (github.com, raw.githubusercontent.com,
objects.githubusercontent.com). No external AI hosting platforms allowed.
"""

import hashlib
import json
import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .config import settings
from .schemas import (
    DownloadModelReq,
    ImportModelReq,
    ModelRecord,
    ModelVersion,
)

logger = logging.getLogger("ai-platform.registry")

# ONLY GitHub sources — no HuggingFace or other platforms
ALLOWED_HOSTS = {
    "github.com",
    "raw.githubusercontent.com",
    "objects.githubusercontent.com",
}


class ModelRegistry:
    def __init__(self) -> None:
        settings.ensure_dirs()
        self.registry_path = settings.config_dir / "registry.json"
        if not self.registry_path.exists():
            self.registry_path.write_text("{}", encoding="utf-8")

    # ── Read / write helpers ───────────────────────────────────

    def _load_raw(self) -> dict:
        try:
            return json.loads(self.registry_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Corrupt registry.json, resetting: %s", e)
            self.registry_path.write_text("{}", encoding="utf-8")
            return {}

    def _save_raw(self, data: dict) -> None:
        """
        P1-10: Atomic write with file locking to prevent corruption.

        Writes to a temporary file first, then atomically renames.
        """
        import tempfile
        import fcntl

        content = json.dumps(data, indent=2)

        # Write to temp file in same directory (ensures same filesystem for atomic rename)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=self.registry_path.parent,
            prefix=".registry_",
            suffix=".tmp"
        )

        try:
            # Lock the temp file
            fcntl.flock(temp_fd, fcntl.LOCK_EX)

            # Write content
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(content)

            # Atomic rename
            os.rename(temp_path, self.registry_path)

        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    # ── Public API ─────────────────────────────────────────────

    def list_models(self) -> list[ModelRecord]:
        raw = self._load_raw()
        return [ModelRecord(**v) for v in raw.values()]

    def get_model(self, model_id: str) -> ModelRecord:
        raw = self._load_raw()
        if model_id not in raw:
            raise KeyError(f"Unknown model: {model_id}")
        return ModelRecord(**raw[model_id])

    def list_versions(self, model_id: str) -> list[ModelVersion]:
        return self.get_model(model_id).versions

    def set_active_version(self, model_id: str, version: int) -> ModelRecord:
        raw = self._load_raw()
        if model_id not in raw:
            raise KeyError(f"Unknown model: {model_id}")
        record = ModelRecord(**raw[model_id])
        if not any(v.version == version for v in record.versions):
            raise KeyError(f"Version {version} not found for {model_id}")
        record.active_version = version
        raw[model_id] = record.model_dump()
        self._save_raw(raw)
        logger.info("Switched %s to version %d", model_id, version)
        return record

    def has_hash(self, model_id: str, sha256: str) -> bool:
        """Check if a SHA256 hash already exists for this model (deduplication)."""
        try:
            record = self.get_model(model_id)
            return sha256.lower() in record.all_hashes()
        except KeyError:
            return False

    def has_tag(self, model_id: str, tag: str) -> bool:
        """Check if a version tag already exists for this model."""
        try:
            record = self.get_model(model_id)
            return tag in record.all_tags()
        except KeyError:
            return False

    # ── Download with versioning, resume, and dedup ────────────

    def download_and_register(self, req: DownloadModelReq) -> ModelRecord:
        self._validate_source(req.source_url)

        # Dedup by version tag
        if req.version_tag and self.has_tag(req.model_id, req.version_tag):
            logger.info(
                "Skipping %s tag %s — already registered",
                req.model_id,
                req.version_tag,
            )
            return self.get_model(req.model_id)

        raw = self._load_raw()
        existing = ModelRecord(**raw[req.model_id]) if req.model_id in raw else None
        next_version = (existing.latest_version_number() + 1) if existing else 1

        filename = req.filename or self._infer_filename(
            req.source_url, req.model_id, req.runtime
        )
        version_dir = settings.models_dir / req.model_id / f"v{next_version}"
        version_dir.mkdir(parents=True, exist_ok=True)
        target = version_dir / filename

        self._download_file(req.source_url, target)

        computed_hash = self._sha256(target)

        # Verify checksum if provided
        if req.sha256 and computed_hash.lower() != req.sha256.lower():
            target.unlink(missing_ok=True)
            raise ValueError("Checksum mismatch — download removed")

        # Dedup by SHA256: if file is identical to an existing version, skip
        if existing and computed_hash.lower() in existing.all_hashes():
            target.unlink(missing_ok=True)
            try:
                version_dir.rmdir()
            except OSError:
                pass
            logger.info(
                "Skipping %s — SHA256 %s matches existing version",
                req.model_id,
                computed_hash[:12],
            )
            return ModelRecord(**raw[req.model_id])

        file_size = target.stat().st_size / (1024**3)

        # Extract source repo from URL
        source_repo = self._extract_source_repo(req.source_url)

        version = ModelVersion(
            version=next_version,
            version_tag=req.version_tag,
            file_path=str(target.resolve()),
            source_url=req.source_url,
            sha256=computed_hash,
            size_gb=req.size_gb or round(file_size, 2),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        if existing:
            existing.versions.append(version)
            existing.active_version = next_version
            if req.license:
                existing.license = req.license
            if req.format:
                existing.format = req.format
            if source_repo:
                existing.source_repo = source_repo
            raw[req.model_id] = existing.model_dump()
        else:
            record = ModelRecord(
                model_id=req.model_id,
                runtime=req.runtime,
                license=req.license,
                format=req.format or self._detect_format(filename),
                source_repo=source_repo,
                active_version=next_version,
                versions=[version],
            )
            raw[req.model_id] = record.model_dump()

        self._save_raw(raw)
        logger.info("Registered %s v%d (tag: %s)", req.model_id, next_version, req.version_tag or "none")
        return ModelRecord(**raw[req.model_id])

    # ── Local import ───────────────────────────────────────────

    def import_local(self, req: ImportModelReq) -> ModelRecord:
        source = Path(req.local_path)
        if not source.exists():
            raise FileNotFoundError(f"Path does not exist: {req.local_path}")

        self._validate_local_model(source, req.runtime)

        raw = self._load_raw()
        existing = ModelRecord(**raw[req.model_id]) if req.model_id in raw else None
        next_version = (existing.latest_version_number() + 1) if existing else 1

        version_dir = settings.models_dir / req.model_id / f"v{next_version}"
        version_dir.mkdir(parents=True, exist_ok=True)

        if source.is_dir():
            target = version_dir
            shutil.copytree(source, target, dirs_exist_ok=True)
            file_path = str(target.resolve())
            file_hash = None
        else:
            target = version_dir / source.name
            shutil.copy2(source, target)
            file_path = str(target.resolve())
            file_hash = self._sha256(target)

            # Dedup by SHA256
            if existing and file_hash.lower() in existing.all_hashes():
                target.unlink(missing_ok=True)
                try:
                    version_dir.rmdir()
                except OSError:
                    pass
                logger.info("Skipping import — identical file already registered for %s", req.model_id)
                return ModelRecord(**raw[req.model_id])

        version = ModelVersion(
            version=next_version,
            file_path=file_path,
            local_import=True,
            sha256=file_hash,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        detected_format = req.format or self._detect_format(source.name)

        if existing:
            existing.versions.append(version)
            existing.active_version = next_version
            raw[req.model_id] = existing.model_dump()
        else:
            record = ModelRecord(
                model_id=req.model_id,
                runtime=req.runtime,
                license=req.license,
                format=detected_format,
                active_version=next_version,
                versions=[version],
            )
            raw[req.model_id] = record.model_dump()

        self._save_raw(raw)
        logger.info("Imported local model %s v%d from %s", req.model_id, next_version, req.local_path)
        return ModelRecord(**raw[req.model_id])

    # ── Internal helpers ───────────────────────────────────────

    def _validate_source(self, source_url: str) -> None:
        parsed = urlparse(source_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only http/https sources are allowed")
        host = parsed.netloc.lower()
        if host not in ALLOWED_HOSTS:
            raise ValueError(
                f"Host '{host}' is not allowed. "
                f"Only GitHub sources are permitted: {ALLOWED_HOSTS}"
            )

    def _validate_local_model(self, path: Path, runtime: str) -> None:
        if path.is_file():
            suffix = path.suffix.lower().lstrip(".")
            if runtime == "llama_cpp" and suffix != "gguf":
                raise ValueError(f"llama_cpp requires .gguf files, got .{suffix}")
            if runtime == "onnx" and suffix != "onnx":
                raise ValueError(f"onnx runtime requires .onnx files, got .{suffix}")
        elif path.is_dir():
            files = list(path.iterdir())
            if not files:
                raise ValueError("Model directory is empty")
            has_weights = any(
                f.suffix.lower() in {".safetensors", ".bin", ".gguf", ".onnx"}
                for f in files
            )
            if not has_weights:
                raise ValueError("No recognized model weight files in directory")

    def _download_file(self, url: str, target: Path) -> None:
        """Download with resume support via HTTP Range headers."""
        existing_size = target.stat().st_size if target.exists() else 0
        headers = {}
        if existing_size > 0:
            headers["Range"] = f"bytes={existing_size}-"
            logger.info("Resuming download from byte %d", existing_size)

        with httpx.stream(
            "GET", url, headers=headers, follow_redirects=True, timeout=300
        ) as response:
            if response.status_code == 416:
                logger.info("File already fully downloaded")
                return
            response.raise_for_status()

            mode = "ab" if response.status_code == 206 else "wb"
            total = response.headers.get("content-length")
            downloaded = existing_size if mode == "ab" else 0

            with target.open(mode) as output:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            pct = downloaded / int(total) * 100
                            logger.debug("Download progress: %.1f%%", pct)

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _infer_filename(self, url: str, model_id: str, runtime: str) -> str:
        parsed = urlparse(url)
        name = Path(parsed.path).name
        if name and "." in name:
            return name
        ext_map = {"llama_cpp": ".gguf", "onnx": ".onnx"}
        suffix = ext_map.get(runtime, ".safetensors")
        return f"{model_id}{suffix}"

    def _detect_format(self, filename: str) -> str:
        suffix = Path(filename).suffix.lower().lstrip(".")
        mapping = {
            "gguf": "gguf",
            "safetensors": "safetensors",
            "onnx": "onnx",
            "bin": "pytorch",
            "pt": "pytorch",
        }
        return mapping.get(suffix, "unknown")

    def _extract_source_repo(self, url: str) -> str | None:
        """Extract 'owner/repo' from a GitHub URL."""
        parsed = urlparse(url)
        if "github" not in parsed.netloc.lower():
            return None
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
        return None
