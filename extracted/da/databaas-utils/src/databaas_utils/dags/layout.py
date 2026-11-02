"""Where a target lives in the DAG bucket, and what describes it there.

The layout and `_databaas_target.json` are what the platform's
``DataBaasS3DagBundle`` and ``databaas_target`` read, and match what the
per-repo CI workflows wrote before this command existed.
"""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from databaas_utils.dags.gitinfo import GitInfo
from databaas_utils.errors import ConfigurationError

TARGET_FILE = "_databaas_target.json"
MAX_SLUG = 40
# Every key the command writes or deletes must match this, so a bad bundle
# name or slug can never reach outside its own target.
PREFIX_PATTERN = re.compile(r"^dags/(dev/[^/]+|prod)/[^/]+/$")


def dev_slug(branch: str) -> str:
    """The dev key for `branch`: lower-case, hyphenated, at most ~47 characters.

    Longer branches are cut to 40 characters plus a 6-character hash of the
    full name, so two long branches with a common start stay distinct.

    Raises:
        ConfigurationError: If nothing usable is left of `branch`.
    """
    slug = re.sub(r"[^a-z0-9-]", "-", branch.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if len(slug) > MAX_SLUG:
        suffix = hashlib.sha1(branch.encode()).hexdigest()[:6]
        slug = slug[:MAX_SLUG].rstrip("-") + "-" + suffix
    if not slug:
        raise ConfigurationError(f"branch {branch!r} gives an empty dev key")
    return slug


def target_prefix(bundle: str, dev_key: str | None) -> str:
    """``dags/prod/<bundle>/``, or ``dags/dev/<dev_key>/<bundle>/`` for a dev key.

    Raises:
        ConfigurationError: If the result falls outside the DAG layout.
    """
    prefix = f"dags/dev/{dev_key}/{bundle}/" if dev_key else f"dags/prod/{bundle}/"
    if not PREFIX_PATTERN.fullmatch(prefix):
        raise ConfigurationError(f"{prefix!r} does not match the dags/ layout")
    return prefix


def target_document(
    *,
    bundle: str,
    dev_key: str | None,
    git: GitInfo,
    now: datetime | None = None,
) -> dict[str, Any]:
    """The `_databaas_target.json` for a deploy."""
    when = (now or datetime.now(UTC)).astimezone(UTC)
    return {
        "mode": "development" if dev_key else "production",
        "dev_key": dev_key or "",
        "bundle": bundle,
        "repo": git.repo,
        "ref": git.ref,
        "commit": git.commit,
        "run_url": git.run_url,
        "deployed_at": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
