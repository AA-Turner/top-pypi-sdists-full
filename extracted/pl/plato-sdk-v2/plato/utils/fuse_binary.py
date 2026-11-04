"""Resolution of the plato-fuse binary on the local machine.

Shared by the world-side lazy mount path (``plato.worlds.lazy_dvc``) and the
direct agent-VM fuse transport (``plato.transports.fuse``). Lives in
``plato.utils`` so transports can use it without importing ``plato.worlds``
(which would cycle back through ``plato.agents.mounts``).
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

PLATO_FUSE_S3_BUCKET = "plato-public-static"
PLATO_FUSE_S3_KEY = "plato-fuse"
PLATO_FUSE_INSTALL_PATH = "/usr/local/bin/plato-fuse"

# Idempotent fuse3 userspace-tools install, shared by the chronos dev/test
# runners (world VM) and the direct agent-VM fuse transport.
ENSURE_FUSE3_COMMAND = (
    "dpkg -s fuse3 > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq fuse3) > /dev/null 2>&1"
)


async def ensure_plato_fuse() -> tuple[str, str]:
    """Return ``(path, source)`` for the local plato-fuse binary.

    Resolution order: ``PLATO_FUSE_BINARY`` env override -> PATH -> download
    from the public S3 bucket. ``source`` is one of ``"override"``, ``"path"``,
    or ``"s3-download"`` so callers can log where the binary came from.
    """
    override = os.environ.get("PLATO_FUSE_BINARY")
    if override:
        override_path = Path(override)
        if override_path.is_file():
            logger.debug("Using PLATO_FUSE_BINARY override: %s", override_path)
            return str(override_path), "override"
        raise RuntimeError(f"PLATO_FUSE_BINARY does not exist: {override}")

    binary = shutil.which("plato-fuse")
    if binary:
        logger.debug("Using plato-fuse from PATH: %s", binary)
        return binary, "path"

    logger.debug(
        "plato-fuse not found on PATH, downloading from s3://%s/%s",
        PLATO_FUSE_S3_BUCKET,
        PLATO_FUSE_S3_KEY,
    )

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "cp",
        f"s3://{PLATO_FUSE_S3_BUCKET}/{PLATO_FUSE_S3_KEY}",
        PLATO_FUSE_INSTALL_PATH,
        "--no-sign-request",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to download plato-fuse from S3: {stderr.decode().strip()}")

    os.chmod(PLATO_FUSE_INSTALL_PATH, 0o755)
    logger.debug("Installed plato-fuse to %s", PLATO_FUSE_INSTALL_PATH)
    return PLATO_FUSE_INSTALL_PATH, "s3-download"
