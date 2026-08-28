"""Analytics flow routing: decide whether an app runs the new AnalyticsEngine.

``PostProcessor`` calls :func:`resolve_manifest_for_app` with the deployment's
``app_name``. A non-None return is the bare manifest name to run through the new
:class:`~matrice_analytics.analytics.engine.AnalyticsEngine`; ``None`` keeps the
app on the legacy post-processing use-case flow.

Resolution is dynamic — a manifest dropped into ``analytics/config/`` becomes
routable with no code change here. Eligibility is currently scoped to
VOLUME, INCIDENT, QUALITY, and SAFETY analytics:

- categories must be a subset of {VOLUME, INCIDENT, QUALITY, SAFETY}
- no ``volume.counter`` section (abline/polygon counters need per-camera
  zone geometry, which the inference pipeline does not wire yet — e.g. footfall)
- not in the deny-list (license_plate_recognition: the new engine takes no
  frame bytes, so routing LPR to it would silently drop OCR plate text)

Override with ``MATRICE_ANALYTICS_FLOW``:
- ``auto`` (default): manifest match + the eligibility checks above
- ``old``: always legacy
- ``new``: route to a matching manifest even if eligibility scoping would
  exclude it (still requires the manifest to exist and parse)
"""

import logging
import os
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

FLOW_ENV_VAR = "MATRICE_ANALYTICS_FLOW"

# Apps whose manifest exists but must stay on the legacy flow.
NEW_FLOW_DENYLIST = {"license_plate_recognition"}

# Harness-only manifests that share a production app name — keep legacy until cutover.
NEW_FLOW_HARNESS_DENYLIST = {
    "car_damage_detection",
    "ppe_detection",
    "ppe_compliance_new",
    "bottle_defect_detection",
}

# Eligibility scope for auto mode.
ALLOWED_CATEGORIES = {"VOLUME", "INCIDENT", "QUALITY", "SAFETY"}

_CONFIG_DIR = Path(__file__).parent / "config"

# Cache of {normalized app.name -> manifest stem} built from the config-dir scan.
_app_name_index: Optional[Dict[str, str]] = None


def _normalize(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def _load_manifest_yaml(path: Path) -> Optional[dict]:
    try:
        import yaml
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or "app" not in data or "categories" not in data:
            logger.warning("Analytics manifest %s is malformed (missing app/categories)", path)
            return None
        return data
    except Exception as e:
        logger.warning("Analytics manifest %s failed to parse: %s", path, e)
        return None


def _build_app_name_index() -> Dict[str, str]:
    """Map normalized manifest ``app.name`` display names to manifest stems."""
    global _app_name_index
    if _app_name_index is not None:
        return _app_name_index
    index: Dict[str, str] = {}
    try:
        for yaml_path in sorted(_CONFIG_DIR.glob("*.yaml")):
            data = _load_manifest_yaml(yaml_path)
            if not data:
                continue
            display_name = (data.get("app") or {}).get("name", "")
            if display_name:
                index[_normalize(str(display_name))] = yaml_path.stem
    except OSError as e:
        logger.warning("Failed to scan analytics manifests in %s: %s", _CONFIG_DIR, e)
    _app_name_index = index
    return index


def load_manifest_index_to_category(manifest_name: str) -> Optional[Dict[int, str]]:
    """Return ``index_to_category`` from a bundled manifest, if present."""
    from .engine_session import normalize_index_to_category

    path = _CONFIG_DIR / f"{manifest_name}.yaml"
    if not path.is_file():
        return None
    data = _load_manifest_yaml(path)
    if not data:
        return None
    raw = data.get("index_to_category")
    if not raw:
        return None
    return normalize_index_to_category(raw) or None


def _is_eligible(manifest_name: str, manifest: dict) -> bool:
    """Auto-mode eligibility: allowed categories, no geometry, not denied."""
    if manifest_name in NEW_FLOW_DENYLIST:
        logger.info(
            "Analytics manifest '%s' is deny-listed for the new flow "
            "(requires capabilities the new engine lacks)", manifest_name
        )
        return False
    if manifest_name in NEW_FLOW_HARNESS_DENYLIST:
        logger.info(
            "Analytics manifest '%s' is a harness manifest sharing a legacy "
            "app name — staying on legacy flow (use the *_new manifest for prod)",
            manifest_name,
        )
        return False
    categories = {str(c).upper() for c in (manifest.get("categories") or [])}
    if not categories or not categories.issubset(ALLOWED_CATEGORIES):
        logger.info(
            "Analytics manifest '%s' categories %s outside supported scope %s",
            manifest_name, sorted(categories), sorted(ALLOWED_CATEGORIES)
        )
        return False
    volume_section = manifest.get("volume") or {}
    if isinstance(volume_section, dict) and volume_section.get("counter"):
        logger.info(
            "Analytics manifest '%s' uses a geometry counter (zone geometry "
            "not wired yet) — staying on legacy flow", manifest_name
        )
        return False
    return True


def resolve_manifest_for_app(app_name: Optional[str]) -> Optional[str]:
    """Return the new-flow manifest name for ``app_name``, or None for legacy.

    A non-None return is a bare manifest name guaranteed to exist under
    ``analytics/config/`` and loadable by ``AnalyticsEngine(manifest_name)``.
    """
    mode = os.environ.get(FLOW_ENV_VAR, "auto").strip().lower() or "auto"
    if mode == "old":
        logger.info("Analytics flow for app '%s': LEGACY (forced via %s=old)",
                    app_name, FLOW_ENV_VAR)
        return None

    if not app_name:
        return None

    if not _CONFIG_DIR.is_dir():
        logger.warning("Analytics config dir missing (%s) — using legacy flow", _CONFIG_DIR)
        return None

    norm = _normalize(app_name)
    manifest_name = (
        norm if (_CONFIG_DIR / f"{norm}.yaml").exists()
        else _build_app_name_index().get(norm)
    )

    if manifest_name is None:
        logger.info("Analytics flow for app '%s': LEGACY (no manifest match)", app_name)
        return None

    manifest = _load_manifest_yaml(_CONFIG_DIR / f"{manifest_name}.yaml")
    if manifest is None:
        logger.warning("Analytics flow for app '%s': LEGACY (manifest '%s' invalid)",
                       app_name, manifest_name)
        return None

    if mode != "new" and not _is_eligible(manifest_name, manifest):
        logger.info("Analytics flow for app '%s': LEGACY (manifest '%s' not eligible)",
                    app_name, manifest_name)
        return None

    logger.info("Analytics flow for app '%s': NEW (manifest=%s)", app_name, manifest_name)
    return manifest_name
