"""Model downloader with progress bar support.

Downloads GGUF models from the Sage GCS bucket (primary)
with HuggingFace fallback, to ~/.sage/models/.
Auto-registers them in the Sage config.

Performance optimizations:
- Parallel downloads with ThreadPoolExecutor
- Large chunk sizes (1MB) with buffered writes
- Batch config registration to minimize I/O
- HTTP/2 support with connection pooling
"""

from __future__ import annotations

import importlib.util
import io
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable

import httpx

from sage.config import SAGE_DIR, SageConfig, load_config, save_config
from sage.models.catalog import CatalogModel, GCS_BUCKET

# Optimized chunk size: 1MB for better throughput on large files
CHUNK_SIZE = 1024 * 1024  # 1MB (was 256KB)
# Buffer size for writes
WRITE_BUFFER_SIZE = 8 * 1024 * 1024  # 8MB buffer

MODELS_DIR = SAGE_DIR / "models"


def _supports_http2() -> bool:
    """Return True when the optional h2 dependency is installed."""
    return importlib.util.find_spec("h2") is not None


def models_dir() -> Path:
    """Return the models directory, creating it if needed."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    return MODELS_DIR


def model_path(model: CatalogModel) -> Path:
    """Return the expected local path for a catalog model."""
    return models_dir() / model.filename


def is_downloaded(model: CatalogModel) -> bool:
    """Check if a model is already downloaded."""
    p = model_path(model)
    return p.exists() and p.stat().st_size > 0


def _register_model(model: CatalogModel, dest: Path) -> None:
    """Register a downloaded model in the sage config so all commands can find it."""
    cfg = load_config()
    if model.name not in cfg.models:
        cfg.models[model.name] = {"path": str(dest)}
        save_config(cfg)


def download_model(
    model: CatalogModel,
    progress_callback: Callable[[int, int], None] | None = None,
) -> Path:
    """Download a GGUF model to ~/.sage/models/ and register it in config.

    Args:
        model: The catalog model to download.
        progress_callback: Optional callback(downloaded_bytes, total_bytes)
            called periodically during download.

    Returns:
        Path to the downloaded file.

    Raises:
        httpx.HTTPStatusError: If the download fails.
        OSError: If writing to disk fails.
    """
    dest = model_path(model)

    # Support resuming partial downloads
    downloaded = 0
    headers: dict[str, str] = {}
    if dest.exists():
        downloaded = dest.stat().st_size
        headers["Range"] = f"bytes={downloaded}-"

    # Use HTTP/2 for better multiplexing and connection pooling
    with httpx.Client(
        follow_redirects=True,
        timeout=httpx.Timeout(30.0, read=300.0),
        http2=_supports_http2(),
    ) as client:
        with client.stream("GET", model.url, headers=headers) as response:
            # If we get 416 (Range Not Satisfiable), file is complete
            if response.status_code == 416:
                _register_model(model, dest)
                return dest

            # For range requests, expect 206; for full downloads, expect 200
            if response.status_code not in (200, 206):
                response.raise_for_status()

            # If server doesn't support range (returns 200 instead of 206),
            # restart from scratch
            if downloaded > 0 and response.status_code == 200:
                downloaded = 0

            total = None
            content_length = response.headers.get("content-length")
            if content_length:
                total = int(content_length) + downloaded

            mode = "ab" if response.status_code == 206 else "wb"
            # Use buffered writes for better I/O performance
            with open(dest, mode, buffering=WRITE_BUFFER_SIZE) as f:
                for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded, total)

    _register_model(model, dest)
    return dest


def download_models_parallel(
    models: list[CatalogModel],
    max_workers: int = 4,
    progress_callback: Callable[[str, int, int], None] | None = None,
) -> dict[str, Path | Exception]:
    """Download multiple models in parallel.

    Args:
        models: List of catalog models to download.
        max_workers: Maximum concurrent downloads (default 4, recommend 3-6).
        progress_callback: Optional callback(model_name, downloaded_bytes, total_bytes)

    Returns:
        Dict mapping model name to Path (success) or Exception (failure).
    """
    results: dict[str, Path | Exception] = {}

    def download_one(model: CatalogModel) -> tuple[str, Path | Exception]:
        try:
            # Create a model-specific callback if needed
            model_callback = None
            if progress_callback:
                model_callback = lambda d, t: progress_callback(model.name, d, t)
            path = download_model(model, model_callback)
            return (model.name, path)
        except Exception as e:
            return (model.name, e)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_one, m): m.name for m in models}

        for future in as_completed(futures):
            name, result = future.result()
            results[name] = result

    return results


def register_model(model: CatalogModel) -> None:
    """Register a downloaded model in the Sage config so it's available via llama_cpp."""
    cfg = load_config()
    cfg.models[model.name] = {
        "path": str(model_path(model)),
        "provider": "llama_cpp",
    }
    # If the user still has the factory default, switch to local model
    if cfg.default_model == SageConfig.default_model:
        cfg.default_model = f"llama_cpp:{model.name}"
    save_config(cfg)


def register_models_batch(models: list[CatalogModel]) -> None:
    """Register multiple downloaded models in a single config write.

    This is much faster than calling register_model() repeatedly,
    as it only loads/saves the config once.
    """
    if not models:
        return

    cfg = load_config()
    first_model_name = None

    for model in models:
        cfg.models[model.name] = {
            "path": str(model_path(model)),
            "provider": "llama_cpp",
        }
        if first_model_name is None:
            first_model_name = model.name

    # If the user still has the factory default, switch to the first local model
    if cfg.default_model == SageConfig.default_model and first_model_name:
        cfg.default_model = f"llama_cpp:{first_model_name}"

    save_config(cfg)


def unregister_model(name: str) -> None:
    """Remove a model from config and optionally delete the file."""
    cfg = load_config()
    cfg.models.pop(name, None)
    if cfg.default_model == f"llama_cpp:{name}":
        cfg.default_model = SageConfig.default_model
    save_config(cfg)


def unregister_models_batch(names: list[str]) -> None:
    """Remove multiple models from config in a single write.

    This is much faster than calling unregister_model() repeatedly.
    """
    if not names:
        return

    cfg = load_config()
    for name in names:
        cfg.models.pop(name, None)
        if cfg.default_model == f"llama_cpp:{name}":
            cfg.default_model = SageConfig.default_model

    save_config(cfg)


def list_downloaded() -> list[tuple[str, Path]]:
    """Return (model_name, path) for every downloaded GGUF model.

    Combines config-registered models with any .gguf files found directly
    in ~/.sage/models/ so models pulled before registration was added still appear.
    """
    seen: dict[str, Path] = {}

    # Config-registered models
    cfg = load_config()
    for name, entry in cfg.models.items():
        p = Path(entry.get("path", ""))
        if p.is_file() and p.stat().st_size > 0:
            seen[name] = p

    # Disk scan — picks up any .gguf files not yet registered
    if MODELS_DIR.exists():
        for gguf in sorted(MODELS_DIR.glob("*.gguf")):
            if gguf.stat().st_size > 0 and gguf.stem not in seen:
                seen[gguf.stem] = gguf

    return sorted(seen.items(), key=lambda x: x[0].lower())


def list_ollama_pulled_models() -> list[dict[str, Any]]:
    """Return models pulled locally in Ollama (empty if Ollama is not running)."""
    try:
        import httpx

        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=2.0)
        if r.status_code != 200:
            return []
        out: list[dict[str, Any]] = []
        for m in r.json().get("models") or []:
            if not isinstance(m, dict):
                continue
            out.append(
                {
                    "name": m.get("name") or "",
                    "size": m.get("size"),
                    "digest": ((m.get("digest") or "")[:16] if m.get("digest") else ""),
                }
            )
        return out
    except Exception:
        return []


def iter_unregistered_gguf_files() -> list[tuple[str, Path]]:
    """GGUF files under the models dir that exist on disk but are not in config."""
    cfg = load_config()
    registered: set[Path] = set()
    for entry in cfg.models.values():
        raw = entry.get("path", "")
        if raw:
            try:
                registered.add(Path(raw).resolve())
            except OSError:
                pass
    if not MODELS_DIR.exists():
        return []
    extra: list[tuple[str, Path]] = []
    for p in MODELS_DIR.glob("*.gguf"):
        try:
            if not p.is_file() or p.stat().st_size <= 0:
                continue
            rp = p.resolve()
        except OSError:
            continue
        if rp not in registered:
            extra.append((p.stem, p))
    return sorted(extra, key=lambda x: x[0].lower())


def delete_model(name: str) -> bool:
    """Delete a downloaded model file and unregister it."""
    cfg = load_config()
    entry = cfg.models.get(name)
    if entry:
        p = Path(entry.get("path", ""))
        if p.exists():
            p.unlink()
        unregister_model(name)
        return True
    return False
