"""Upload geocif outputs to HuggingFace Hub.

Uploads the SQLite database and agmet PNGs to a private HuggingFace dataset
repo, and maintains a manifest.json tracking all available databases.
"""

import ast
import json
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from geocif import __version__

logger = logging.getLogger(__name__)


def upload_to_hf(parser):
    """Upload DB + agmet PNGs to HuggingFace Hub and update manifest.

    Reads config values:
        [ML] hf_repo_id: HuggingFace dataset repo (e.g., "ritvik/geocif-data")
        [DEFAULT] db: database filename
        [PATHS] dir_output: base output directory
        [DEFAULT] project_name: project name (default "geocif")
    """
    try:
        from huggingface_hub import HfApi, hf_hub_download
    except ImportError:
        logger.error("huggingface_hub not installed. Run: pip install huggingface_hub")
        return

    repo_id = parser.get("ML", "hf_repo_id", fallback="ritvik/geocif-data")
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    db_name = parser.get("DEFAULT", "db")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name

    db_path = dir_output / "ml" / "db" / db_name
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        return

    api = HfApi()

    # Ensure repo exists (create if not)
    try:
        api.create_repo(repo_id, repo_type="dataset", private=True, exist_ok=True)
    except Exception as e:
        logger.warning("Could not create/verify HF repo: %s", e)

    # ── Upload DB ───────────────────────────────────────────────────────
    hf_db_path = f"db/{db_name}"
    logger.info("Uploading DB to HF: %s -> %s/%s", db_path, repo_id, hf_db_path)
    try:
        api.upload_file(
            path_or_fileobj=str(db_path),
            path_in_repo=hf_db_path,
            repo_id=repo_id,
            repo_type="dataset",
        )
    except Exception as e:
        logger.error("Failed to upload DB: %s", e)
        return

    # ── Upload agmet PNGs ───────────────────────────────────────────────
    agmet_dir = dir_output / "agmet"
    if agmet_dir.exists() and any(agmet_dir.rglob("*.png")):
        logger.info("Uploading agmet PNGs from %s", agmet_dir)
        try:
            api.upload_folder(
                folder_path=str(agmet_dir),
                path_in_repo="agmet",
                repo_id=repo_id,
                repo_type="dataset",
                allow_patterns="**/*.png",
            )
        except Exception as e:
            logger.warning("Failed to upload agmet PNGs: %s", e)
    else:
        logger.info("No agmet PNGs found at %s — skipping", agmet_dir)

    # ── Upload GeoJSON shapefiles ───────────────────────────────────────
    geojson_dir = dir_output / "shapefiles"
    if geojson_dir.exists() and any(geojson_dir.glob("*.geojson")):
        logger.info("Uploading GeoJSON files from %s", geojson_dir)
        try:
            api.upload_folder(
                folder_path=str(geojson_dir),
                path_in_repo="shapefiles",
                repo_id=repo_id,
                repo_type="dataset",
                allow_patterns="*.geojson",
            )
        except Exception as e:
            logger.warning("Failed to upload GeoJSON files: %s", e)

    # ── Update manifest.json ────────────────────────────────────────────
    manifest = _download_manifest(api, repo_id)
    entry = _build_manifest_entry(parser, db_name)
    manifest["databases"] = [
        e for e in manifest.get("databases", []) if e["filename"] != hf_db_path
    ]
    manifest["databases"].append(entry)
    manifest["databases"].sort(key=lambda e: e.get("generated_at", ""))

    _upload_manifest(api, repo_id, manifest)
    logger.info("HuggingFace sync complete: %s", repo_id)


def _download_manifest(api, repo_id):
    """Download existing manifest.json or return empty dict."""
    try:
        from huggingface_hub import hf_hub_download
        path = hf_hub_download(
            repo_id=repo_id,
            filename="manifest.json",
            repo_type="dataset",
        )
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {"databases": []}


def _build_manifest_entry(parser, db_name):
    """Build a manifest entry dict for the current run."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    crops = list({
        parser.get(c, "crops", fallback="maize") for c in countries
    })

    return {
        "filename": f"db/{db_name}",
        "countries": countries,
        "crops": crops,
        "forecast_year": int(parser.get("DEFAULT", "forecast_year", fallback="2026")),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "geocif_version": __version__,
    }


def _upload_manifest(api, repo_id, manifest):
    """Upload updated manifest.json to HF."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(manifest, f, indent=2)
        tmp_path = f.name

    try:
        api.upload_file(
            path_or_fileobj=tmp_path,
            path_in_repo="manifest.json",
            repo_id=repo_id,
            repo_type="dataset",
        )
    except Exception as e:
        logger.error("Failed to upload manifest.json: %s", e)
    finally:
        Path(tmp_path).unlink(missing_ok=True)
