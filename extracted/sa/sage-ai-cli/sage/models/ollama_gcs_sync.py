"""Ollama → GCS sync: pull a model locally, extract the GGUF blob, upload to GCS.

Ollama stores weights internally as GGUF blobs at:
  ~/.ollama/models/blobs/sha256-<hash>

The manifest at:
  ~/.ollama/models/manifests/registry.ollama.ai/library/<name>/<tag>

points to the model layer (mediaType application/vnd.ollama.image.model).
That blob IS the GGUF file — no conversion needed.

Workflow:
  1. ollama pull <model>            (if not already local)
  2. Parse manifest → find model blob
  3. Copy blob to ~/.sage/models/<name>.gguf
  4. Upload to gs://sage-ai-models/gguf/<name>.gguf
  5. Update gs://sage-ai-models/catalog.json
  6. ollama rm <model>              (optional)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable

OLLAMA_HOME = Path(os.environ.get("OLLAMA_HOME", Path.home() / ".ollama"))
OLLAMA_MODELS = Path(os.environ.get("OLLAMA_MODELS", OLLAMA_HOME / "models"))
OLLAMA_MANIFESTS = OLLAMA_MODELS / "manifests"
OLLAMA_BLOBS = OLLAMA_MODELS / "blobs"

DEFAULT_BUCKET = "sage-ai-models"
GCS_GGUF_PREFIX = "gguf"


class SyncError(RuntimeError):
    pass


# ── Ollama helpers ────────────────────────────────────────────────────────────

def _is_ollama_running() -> bool:
    try:
        import httpx
        with httpx.Client(timeout=2) as c:
            return c.get("http://localhost:11434/api/version").is_success
    except Exception:
        return False


def _ollama_pull(model_name: str, log: Callable[[str], None] = print) -> None:
    log(f"  ollama pull {model_name}…")
    result = subprocess.run(
        ["ollama", "pull", model_name],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        raise SyncError(f"ollama pull {model_name} failed (exit {result.returncode})")


def _ollama_rm(model_name: str, log: Callable[[str], None] = print) -> None:
    log(f"  ollama rm {model_name}…")
    subprocess.run(["ollama", "rm", model_name], capture_output=True, text=True)


def _find_manifest(model_name: str) -> Path | None:
    """Locate the Ollama manifest file for a model name like 'qwen3:8b'."""
    name_part, _, tag = model_name.partition(":")
    if not tag:
        tag = "latest"
    # Try library namespace first, then full path
    for namespace in ("library",):
        candidate = (
            OLLAMA_MANIFESTS
            / "registry.ollama.ai"
            / namespace
            / name_part
            / tag
        )
        if candidate.exists():
            return candidate
    # Fallback: glob search
    for p in OLLAMA_MANIFESTS.rglob(f"*/{name_part}/{tag}"):
        if p.is_file():
            return p
    return None


def _extract_model_blob(manifest_path: Path) -> tuple[Path | None, str | None]:
    """Return the GGUF blob path and short digest referenced by the manifest's model layer."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None, None

    for layer in manifest.get("layers", []):
        media_type = layer.get("mediaType", "")
        # The weights layer is application/vnd.ollama.image.model
        if "image.model" in media_type or media_type.endswith(".model"):
            digest: str = layer.get("digest", "")
            if not digest:
                continue
            blob_name = digest.replace(":", "-")
            blob_path = OLLAMA_BLOBS / blob_name
            if blob_path.exists():
                short_hash = digest.split(":")[-1][:8] if ":" in digest else digest[:8]
                return blob_path, short_hash
    return None, None


def _gguf_filename(model_name: str) -> str:
    """Turn 'qwen3:8b' into 'qwen3-8b.gguf'."""
    return model_name.replace(":", "-").replace("/", "_") + ".gguf"


# ── GCS helpers ───────────────────────────────────────────────────────────────

def _gsutil(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gsutil", *args],
        capture_output=True,
        text=True,
    )


def _gcs_exists(uri: str) -> bool:
    return _gsutil("-q", "stat", uri).returncode == 0


def _gcs_upload(local: Path, uri: str, log: Callable[[str], None] = print) -> None:
    log(f"  Uploading {local.name} → {uri}…")
    r = _gsutil(
        "-o", "GSUtil:parallel_composite_upload_threshold=150T",
        "cp", str(local), uri,
    )
    if r.returncode != 0:
        raise SyncError(f"gsutil upload failed:\n{r.stderr or r.stdout}")


def _gcs_catalog_add(model_name: str, filename: str, size_gb: float, bucket: str, short_hash: str) -> None:
    """Fetch catalog.json from GCS, add/update the entry, re-upload."""
    catalog_uri = f"gs://{bucket}/catalog.json"
    import tempfile, time as _time

    tmp_dir = Path(tempfile.mkdtemp())
    local_catalog = tmp_dir / "catalog.json"

    # Download existing catalog (ignore failure — may not exist yet)
    _gsutil("cp", catalog_uri, str(local_catalog))

    if local_catalog.exists():
        try:
            data = json.loads(local_catalog.read_text(encoding="utf-8"))
        except Exception:
            data = {"version": 1, "models": []}
    else:
        data = {"version": 1, "models": []}

    name = model_name.replace(":", "-").replace("/", "_") + f"-{short_hash}"
    display = name.replace("-", " ").replace("_", " ").title()
    url = f"https://storage.googleapis.com/{bucket}/{GCS_GGUF_PREFIX}/{filename}"

    entry = {
        "name": name,
        "display_name": display,
        "filename": filename,
        "url": url,
        "size_gb": round(size_gb, 2),
        "params": "",
        "family": name.split("-")[0].title(),
        "description": f"Synced from Ollama: {model_name}",
        "backend": "gguf",
        "tags": [],
        "category": "general",
        "default": False,
    }

    models = data.get("models", [])
    for i, m in enumerate(models):
        if m.get("name") == name:
            models[i] = entry
            break
    else:
        models.append(entry)

    data["models"] = models
    data["updated_at"] = _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime())
    data["model_count"] = len(models)

    local_catalog.write_text(json.dumps(data, indent=2), encoding="utf-8")

    r = _gsutil(
        "-h", "Content-Type:application/json",
        "-h", "Cache-Control:public, max-age=3600",
        "cp", str(local_catalog), catalog_uri,
    )
    _gsutil("acl", "ch", "-u", "AllUsers:R", catalog_uri)

    shutil.rmtree(tmp_dir, ignore_errors=True)


# ── Main sync entry point ─────────────────────────────────────────────────────

def sync_model(
    model_name: str,
    *,
    bucket: str = DEFAULT_BUCKET,
    pull_if_missing: bool = True,
    delete_after_upload: bool = False,
    skip_if_exists: bool = True,
    log: Callable[[str], None] = print,
) -> dict:
    """Pull an Ollama model locally, extract its GGUF blob, upload to GCS.

    Returns a dict with keys: model, uploaded, skipped, deleted_local.
    """
    gguf_name = _gguf_filename(model_name)
    gcs_uri = f"gs://{bucket}/{GCS_GGUF_PREFIX}/{gguf_name}"

    if skip_if_exists and _gcs_exists(gcs_uri):
        log(f"  {model_name} already in GCS — skipping")
        return {"model": model_name, "uploaded": False, "skipped": True, "deleted_local": False}

    # Step 1: Ensure model is pulled locally
    manifest_path = _find_manifest(model_name)
    if manifest_path is None:
        if not pull_if_missing:
            raise SyncError(f"{model_name} is not pulled locally. Run: ollama pull {model_name}")
        if not _is_ollama_running():
            raise SyncError("Ollama is not running. Start it with: ollama serve")
        _ollama_pull(model_name, log=log)
        manifest_path = _find_manifest(model_name)
        if manifest_path is None:
            raise SyncError(f"Manifest not found after pulling {model_name}")

    # Step 2: Extract GGUF blob
    blob_path, short_hash = _extract_model_blob(manifest_path)
    if blob_path is None or short_hash is None:
        raise SyncError(f"Could not locate model blob for {model_name}. Is it a GGUF model?")

    size_gb = blob_path.stat().st_size / (1024 ** 3)
    log(f"  Found GGUF blob: {blob_path.name} ({size_gb:.1f} GB) Hash: {short_hash}")

    gguf_name = _gguf_filename(model_name).replace(".gguf", f"-{short_hash}.gguf")
    gcs_uri = f"gs://{bucket}/{GCS_GGUF_PREFIX}/{gguf_name}"

    if skip_if_exists and _gcs_exists(gcs_uri):
        log(f"  {model_name} already in GCS — skipping")
        return {"model": model_name, "uploaded": False, "skipped": True, "deleted_local": False}

    # Step 3: Copy blob with friendly name to a temp location for upload
    import tempfile
    tmp_dir = Path(tempfile.mkdtemp())
    gguf_copy = tmp_dir / gguf_name
    try:
        log(f"  Copying blob → {gguf_name}…")
        shutil.copy2(str(blob_path), str(gguf_copy))

        # Step 4: Upload to GCS
        _gcs_upload(gguf_copy, gcs_uri, log=log)

        # Step 5: Update catalog.json in GCS
        log("  Updating catalog.json in GCS…")
        _gcs_catalog_add(model_name, gguf_name, size_gb, bucket, short_hash)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Step 6: Optionally delete local Ollama model
    deleted = False
    if delete_after_upload:
        _ollama_rm(model_name, log=log)
        deleted = True

    log(f"  ✓ {model_name} synced to GCS")
    return {"model": model_name, "uploaded": True, "skipped": False, "deleted_local": deleted}


def list_local_ollama_models() -> list[str]:
    """Return all model names currently pulled in local Ollama."""
    try:
        import httpx
        with httpx.Client(timeout=5) as c:
            resp = c.get("http://localhost:11434/api/tags")
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        return []


def sync_all(
    *,
    bucket: str = DEFAULT_BUCKET,
    delete_after_upload: bool = False,
    skip_if_exists: bool = True,
    log: Callable[[str], None] = print,
) -> list[dict]:
    """Sync every locally pulled Ollama model to GCS."""
    models = list_local_ollama_models()
    if not models:
        log("No local Ollama models found.")
        return []
    log(f"Found {len(models)} local Ollama model(s): {', '.join(models)}")
    results = []
    for m in models:
        try:
            r = sync_model(
                m,
                bucket=bucket,
                pull_if_missing=False,
                delete_after_upload=delete_after_upload,
                skip_if_exists=skip_if_exists,
                log=log,
            )
            results.append(r)
        except SyncError as e:
            log(f"  ✗ {m}: {e}")
            results.append({"model": m, "uploaded": False, "skipped": False, "error": str(e)})
    return results
