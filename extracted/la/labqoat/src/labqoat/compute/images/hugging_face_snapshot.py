"""Pinned public model downloads retained in immutable worker image layers."""

import re
import shlex
from typing import ClassVar

from labqoat.compute.images.image_validation import ImageValidation


class HuggingFaceSnapshot:
    """Render an explicit build-time download without importing model libraries on the client."""

    cache: ClassVar[str] = "/opt/labqoat-models/huggingface"

    @classmethod
    def command(cls, repository: str, revision: str, patterns: tuple[str, ...]) -> str:
        """Require immutable revisions and quote all authored values as data for the builder."""
        if re.fullmatch(r"[\w.-]+(?:/[\w.-]+)?", repository, flags=re.ASCII) is None:
            raise ValueError("Model repository must be a Hugging Face repository ID")
        if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            raise ValueError("Model revision must be an immutable 40-character commit SHA")
        if len(patterns) > 128:
            raise ValueError("Model snapshots allow at most 128 file patterns")
        selected = [ImageValidation.text(pattern) for pattern in patterns]
        options = {
            "repo_id": repository,
            "revision": revision,
            "cache_dir": cls.cache,
            "allow_patterns": selected or None,
            "token": False,
        }
        script = f"from huggingface_hub import snapshot_download; snapshot_download(**{options!r})"
        return "python -c " + shlex.quote(script)
