"""Auto-download metadata files via Pooch when missing locally."""

import logging
import os
from pathlib import Path

import pooch

logger = logging.getLogger(__name__)

_SENTINEL = "boundary_files"  # Subdirectory that must exist if metadata is populated


def ensure_metadata(parser):
    """Download and extract metadata.zip if dir_metadata is not populated.

    Reads [POOCH] url from config, or GEOCIF_METADATA_URL env var.
    If neither is set, does nothing (preserves current manual-setup behavior).
    """
    metadata_root = Path(parser.get("PATHS", "dir_metadata"))

    # Already populated — nothing to do
    if (metadata_root / _SENTINEL).is_dir():
        return

    # Determine URL
    url = os.environ.get("GEOCIF_METADATA_URL")
    if parser.has_section("POOCH"):
        if not parser.getboolean("POOCH", "enabled", fallback=True):
            return
        url = parser.get("POOCH", "url", fallback=url)

    if not url:
        logger.debug("Pooch not configured — skipping metadata download.")
        return

    logger.info(f"Downloading metadata from {url} ...")
    metadata_root.mkdir(parents=True, exist_ok=True)

    pooch.retrieve(
        url=url,
        known_hash=None,
        fname="metadata.zip",
        path=str(metadata_root),
        processor=pooch.Unzip(extract_dir=str(metadata_root)),
    )
    logger.info(f"Metadata extracted to {metadata_root}")
