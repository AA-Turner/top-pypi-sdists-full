import hashlib
import json
import re
from novita_sandbox.core.exceptions import InvalidImageReferenceException


def normalize_oci_image(image: str) -> str:
    if not isinstance(image, str):
        raise InvalidImageReferenceException("OCI image reference must be a string")
    value = image.strip()
    if not value:
        raise InvalidImageReferenceException("OCI image reference cannot be empty")
    if any(ch.isspace() for ch in value) or value.startswith(('/', ':')):
        raise InvalidImageReferenceException(f"Invalid OCI image reference: {image!r}")
    slash, colon = value.rfind("/"), value.rfind(":")
    return value if "@" in value or colon > slash else f"{value}:latest"


def oci_fingerprint(image: str, build: dict) -> str:
    content = {
        "schema_version": 1,
        "image": normalize_oci_image(image),
        "build": {
            key: build.get(key)
            for key in ("cmd", "ready_cmd", "patch_cmd", "cpu_count", "memory_mb", "skip_cache", "no_cache", "tags")
            if build.get(key) is not None
        },
    }
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:12]


def oci_slug(image: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_oci_image(image).lower()).strip("-")[:32]
