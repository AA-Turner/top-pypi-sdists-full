"""Local model storage without package installation."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import yaml

from dreadnode.core.util import valid_version
from dreadnode.packaging.manifest import ModelManifest
from dreadnode.storage.storage import Storage, hash_file

if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer


_SOURCE_EXCLUDES = {".git", "__pycache__", ".DS_Store"}


def _source_file(rel_path: str, source_dir: Path, *, field_name: str) -> Path:
    candidate = (source_dir / rel_path).resolve()
    source_root = source_dir.resolve()
    if not candidate.is_relative_to(source_root):
        raise ValueError(f"{field_name} path must stay inside {source_dir}: {rel_path}")
    if not candidate.is_file():
        raise FileNotFoundError(f"{field_name} path not found: {rel_path}")
    return candidate


def _default_model_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file():
            continue
        if any(part in _SOURCE_EXCLUDES for part in path.parts):
            continue
        if path.name == "model.yaml":
            continue
        files.append(path)
    return files


def _coerce_string_list(raw: object, *, field_name: str) -> list[str] | None:
    if raw is None:
        return None
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ValueError(f"{field_name} must be a list of strings")
    return [item for item in raw if isinstance(item, str)]


def _infer_framework(files: list[Path]) -> str:
    suffixes = {path.suffix.lower() for path in files}
    if ".safetensors" in suffixes:
        return "safetensors"
    if ".onnx" in suffixes:
        return "onnx"
    if suffixes.intersection({".pt", ".pth", ".bin"}):
        return "pytorch"
    return "safetensors"


def _safe_temp_prefix(name: str) -> str:
    """Build a filesystem-safe prefix for temporary model directories."""
    return name.replace("/", "-").replace(":", "-")


class LocalModel:
    """Model stored in CAS, usable without package installation.

    This class provides a way to work with models stored in the
    Content-Addressable Storage without requiring them to be installed
    as Python packages with entry points.

    Example:
        >>> from dreadnode.models import LocalModel
        >>> from dreadnode.storage import Storage
        >>>
        >>> storage = Storage()
        >>>
        >>> # Save a HuggingFace model to CAS
        >>> from transformers import AutoModelForSequenceClassification
        >>> hf_model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
        >>> local_model = LocalModel.from_hf(hf_model, "my-bert", storage)
        >>>
        >>> # Load and use
        >>> model = local_model.to_hf()
        >>> tokenizer = local_model.tokenizer()
    """

    def __init__(
        self,
        name: str,
        storage: Storage,
        version: str | None = None,
    ):
        """Load a local model by name.

        Args:
            name: Model name.
            storage: Storage instance for CAS access.
            version: Specific version to load. If None, loads latest.
        """
        self.name = name
        self.storage = storage

        if version is None:
            version = storage.latest_version("models", name)
            if version is None:
                raise FileNotFoundError(f"Model not found: {name}")

        self.version = version
        self._manifest: ModelManifest | None = None
        self._model_dir: Path | None = None

    @property
    def manifest(self) -> ModelManifest:
        """Load and cache the manifest."""
        if self._manifest is None:
            content = self.storage.get_manifest("models", self.name, self.version)
            self._manifest = ModelManifest.model_validate_json(content)
        return self._manifest

    @property
    def framework(self) -> str:
        """Model framework (safetensors, pytorch, onnx, etc.)."""
        return self.manifest.framework

    @property
    def task(self) -> str | None:
        """Model task type."""
        return self.manifest.task

    @property
    def architecture(self) -> str | None:
        """Model architecture."""
        return self.manifest.architecture

    @property
    def files(self) -> list[str]:
        """List of artifact file paths."""
        return list(self.manifest.artifacts.keys())

    def _resolve(self, path: str) -> Path:
        """Resolve artifact path to local file."""
        if path not in self.manifest.artifacts:
            raise FileNotFoundError(f"Artifact not in manifest: {path}")

        oid = self.manifest.artifacts[path]
        local_path = self.storage.blob_path(oid)

        if not local_path.exists():
            self.storage.download_blob(oid)

        return local_path

    def model_path(self) -> Path:
        """Get the local path to the model directory.

        Reconstructs the model directory structure from CAS blobs.

        Returns:
            Path to local model directory.
        """
        if self._model_dir is not None and self._model_dir.exists():
            return self._model_dir

        # Create a temp directory to reconstruct model structure
        model_dir = Path(tempfile.mkdtemp(prefix=f"dn_model_{_safe_temp_prefix(self.name)}_"))

        for artifact_path in self.files:
            blob_path = self._resolve(artifact_path)
            dest_path = model_dir / artifact_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            # Copy or link the blob
            shutil.copy2(blob_path, dest_path)

        self._model_dir = model_dir
        return model_dir

    def to_hf(
        self,
        *,
        trust_remote_code: bool = False,
        torch_dtype: Any = None,
        device_map: str | None = None,
        **kwargs: Any,
    ) -> PreTrainedModel:
        """Load as HuggingFace PreTrainedModel.

        Args:
            trust_remote_code: Whether to trust remote code.
            torch_dtype: Torch dtype for model weights.
            device_map: Device map for model parallelism.
            **kwargs: Additional arguments for from_pretrained.

        Returns:
            HuggingFace PreTrainedModel.
        """
        from dreadnode.models.hf import load_model_from_pretrained, require_transformers

        require_transformers()

        model_dir = self.model_path()

        return load_model_from_pretrained(
            model_dir,
            task=self.task,
            trust_remote_code=trust_remote_code,
            torch_dtype=torch_dtype,
            device_map=device_map,
            **kwargs,
        )

    def tokenizer(
        self,
        *,
        trust_remote_code: bool = False,
        **kwargs: Any,
    ) -> PreTrainedTokenizer:
        """Load the associated tokenizer.

        Args:
            trust_remote_code: Whether to trust remote code.
            **kwargs: Additional arguments for from_pretrained.

        Returns:
            HuggingFace PreTrainedTokenizer.
        """
        from dreadnode.models.hf import load_tokenizer_from_pretrained, require_transformers

        require_transformers()

        model_dir = self.model_path()

        return load_tokenizer_from_pretrained(
            model_dir,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

    @classmethod
    def from_hf(
        cls,
        model: PreTrainedModel,
        name: str,
        storage: Storage,
        *,
        tokenizer: PreTrainedTokenizer | None = None,
        format: Literal["safetensors", "pytorch"] = "safetensors",
        task: str | None = None,
        version: str = "0.1.0",
    ) -> LocalModel:
        """Store a HuggingFace model in CAS and return LocalModel.

        Args:
            model: HuggingFace PreTrainedModel to store.
            name: Name for the model.
            storage: Storage instance for CAS access.
            tokenizer: Optional tokenizer to save alongside model.
            format: Save format (safetensors or pytorch).
            task: Task type for manifest.
            version: Version string.

        Returns:
            LocalModel instance for the stored model.

        Example:
            >>> from transformers import AutoModelForCausalLM, AutoTokenizer
            >>> model = AutoModelForCausalLM.from_pretrained("gpt2")
            >>> tokenizer = AutoTokenizer.from_pretrained("gpt2")
            >>> local = LocalModel.from_hf(model, "my-gpt2", storage, tokenizer=tokenizer)
        """
        from dreadnode.models.hf import (
            infer_model_info,
            require_transformers,
            save_model_to_path,
            save_tokenizer_to_path,
        )

        require_transformers()

        artifacts: dict[str, str] = {}

        # Save to temp directory first
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Save model
            save_model_to_path(model, tmp_path, format=format)

            # Save tokenizer if provided
            if tokenizer is not None:
                save_tokenizer_to_path(tokenizer, tmp_path)

            # Hash and store each file in CAS
            for file_path in tmp_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(tmp_path)
                    file_hash = hash_file(file_path)
                    oid = f"sha256:{file_hash}"
                    storage.store_blob(oid, file_path)
                    artifacts[str(rel_path)] = oid

        # Infer model info
        model_info = infer_model_info(model)
        architecture = model_info.get("architecture")

        # Create manifest
        manifest = ModelManifest(
            framework=format,
            task=task,
            architecture=architecture,
            artifacts=artifacts,
        )

        # Store manifest
        manifest_json = manifest.model_dump_json(indent=2)
        storage.store_manifest("models", name, version, manifest_json)

        return cls(name, storage, version)

    @classmethod
    def from_dir(
        cls,
        source_dir: str | Path,
        storage: Storage,
        *,
        name: str | None = None,
        version: str | None = None,
    ) -> LocalModel:
        """Store a model source directory described by model.yaml in CAS."""
        source_dir = Path(source_dir).resolve()
        config_path = source_dir / "model.yaml"
        if not config_path.is_file():
            raise FileNotFoundError(f"model.yaml not found in {source_dir}")

        raw = yaml.safe_load(config_path.read_text())
        if not isinstance(raw, dict):
            raise TypeError("model.yaml must contain a YAML mapping")

        model_name = name or raw.get("name") or source_dir.name
        if not isinstance(model_name, str):
            raise TypeError("model.yaml name must be a string")

        model_version = version or raw.get("version") or "0.1.0"
        if not isinstance(model_version, str):
            raise TypeError("model.yaml version must be a string")
        if not valid_version(model_version):
            raise ValueError(
                f"model.yaml version must use fixed semver (X.Y.Z), got {model_version!r}"
            )

        files = _coerce_string_list(raw.get("files"), field_name="files")
        artifact_paths = (
            [_source_file(path, source_dir, field_name="files") for path in files]
            if files
            else _default_model_files(source_dir)
        )
        if not artifact_paths:
            raise ValueError(f"No model artifacts found in {source_dir}")

        summary = raw.get("summary") or raw.get("description")
        if summary is not None and not isinstance(summary, str):
            raise ValueError("model.yaml summary must be a string")

        framework = raw.get("framework")
        if framework is not None and not isinstance(framework, str):
            raise ValueError("model.yaml framework must be a string")

        task = raw.get("task")
        if task is not None and not isinstance(task, str):
            raise ValueError("model.yaml task must be a string")

        architecture = raw.get("architecture")
        if architecture is not None and not isinstance(architecture, str):
            raise ValueError("model.yaml architecture must be a string")

        artifacts: dict[str, str] = {}
        for artifact_path in artifact_paths:
            rel_path = artifact_path.relative_to(source_dir)
            oid = f"sha256:{hash_file(artifact_path)}"
            storage.store_blob(oid, artifact_path)
            artifacts[str(rel_path)] = oid

        artifacts_json = json.dumps(artifacts, sort_keys=True)
        artifacts_hash = f"sha256:{hashlib.sha256(artifacts_json.encode()).hexdigest()}"

        # Extract catalog metadata from model.yaml
        tags = _coerce_string_list(raw.get("tags"), field_name="tags")
        license_val = raw.get("license")
        if license_val is not None and not isinstance(license_val, str):
            raise ValueError("model.yaml license must be a string")
        pretty_name = raw.get("pretty_name")
        if pretty_name is not None and not isinstance(pretty_name, str):
            raise ValueError("model.yaml pretty_name must be a string")
        language = _coerce_string_list(raw.get("language"), field_name="language")
        task_categories = _coerce_string_list(
            raw.get("task_categories"), field_name="task_categories"
        )
        size_category = raw.get("size_category")
        if size_category is not None and not isinstance(size_category, str):
            raise ValueError("model.yaml size_category must be a string")
        description = raw.get("description")
        if description is not None and not isinstance(description, str):
            raise ValueError("model.yaml description must be a string")
        base_model = raw.get("base_model")
        if base_model is not None and not isinstance(base_model, str):
            raise ValueError("model.yaml base_model must be a string")
        dataset_refs = _coerce_string_list(raw.get("dataset_refs"), field_name="dataset_refs")

        manifest = ModelManifest(
            summary=summary,
            framework=framework or _infer_framework(artifact_paths),
            task=task,
            architecture=architecture,
            artifacts=artifacts,
            artifacts_hash=artifacts_hash,
            tags=tags,
            license=license_val,
            pretty_name=pretty_name,
            language=language,
            task_categories=task_categories,
            size_category=size_category,
            description=description,
            base_model=base_model,
            dataset_refs=dataset_refs,
        )
        storage.store_manifest(
            "models",
            model_name,
            model_version,
            manifest.model_dump_json(indent=2),
        )

        return cls(model_name, storage, model_version)

    def publish(self, version: str | None = None) -> None:
        """Create a DN package for signing and distribution.

        Args:
            version: Version for the package. If None, uses current version.

        Raises:
            NotImplementedError: Package creation not yet implemented.
        """
        raise NotImplementedError(
            "Package publishing is not yet implemented. Use the CLI to create and publish packages."
        )

    def __repr__(self) -> str:
        return f"LocalModel(name={self.name!r}, version={self.version!r}, framework={self.framework!r})"


def load_model(
    path: str | Path,
    *,
    model_name: str | None = None,
    storage: Storage | None = None,
    task: str | None = None,
    format: Literal["safetensors", "pytorch"] = "safetensors",
    version: str | None = None,
    **kwargs: Any,
) -> LocalModel:
    """Load a model from HuggingFace Hub or a local source directory.

    Args:
        path: HuggingFace model path or a local model source directory.
        model_name: Name to store the model as locally. Defaults to the path.
        storage: Storage instance. If None, creates default storage.
        task: Task type for the model.
        format: Storage format (safetensors or pytorch).
        version: Version string for the stored model.
        **kwargs: Additional arguments passed to from_pretrained.

    Returns:
        LocalModel instance with the loaded model.

    Example:
        >>> from dreadnode.models import load_model
        >>>
        >>> # Load and store a HuggingFace model
        >>> model = load_model("bert-base-uncased", task="classification")
        >>> hf_model = model.to_hf()
    """
    source_dir = Path(path).expanduser()

    if storage is None:
        storage = Storage()

    if source_dir.is_dir() and (source_dir / "model.yaml").is_file():
        return LocalModel.from_dir(
            source_dir,
            storage,
            name=model_name,
            version=version,
        )

    from dreadnode.models.hf import (
        load_model_from_pretrained,
        load_tokenizer_from_pretrained,
        require_transformers,
    )

    require_transformers()

    path_str = str(path)

    if model_name is None:
        model_name = path_str.replace("/", "-").replace(":", "-")

    hf_model = load_model_from_pretrained(path_str, task=task, **kwargs)

    try:
        hf_tokenizer = load_tokenizer_from_pretrained(path_str, **kwargs)
    except (ImportError, OSError, RuntimeError, ValueError):
        hf_tokenizer = None

    return LocalModel.from_hf(
        hf_model,
        name=model_name,
        storage=storage,
        tokenizer=hf_tokenizer,
        format=format,
        task=task,
        version=version or "0.1.0",
    )
