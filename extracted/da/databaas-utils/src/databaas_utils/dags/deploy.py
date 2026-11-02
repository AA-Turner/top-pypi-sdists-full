"""Deploy and destroy DAG targets in the environment's DAG bucket."""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from databaas_utils.dags import s3
from databaas_utils.dags.config import DagsConfig, Target
from databaas_utils.dags.files import collect_files
from databaas_utils.dags.gitinfo import GitInfo, collect
from databaas_utils.dags.layout import (
    TARGET_FILE,
    dev_slug,
    target_document,
    target_prefix,
)
from databaas_utils.dags.namespacing import namespace_packages
from databaas_utils.errors import ConfigurationError


@dataclass(frozen=True)
class ResolvedTarget:
    """A configured target and the prefix it deploys to.

    Attributes:
        target: The entry from `databaas.yml`.
        dev_key: The dev slug; empty for production.
        prefix: ``dags/prod/<bundle>/`` or ``dags/dev/<dev_key>/<bundle>/``.
    """

    target: Target
    dev_key: str
    prefix: str


@dataclass(frozen=True)
class DeployResult:
    """What a deploy did, or would do with ``dry_run``."""

    resolved: ResolvedTarget
    url: str
    uploaded: tuple[str, ...]
    unchanged: tuple[str, ...]
    deleted: tuple[str, ...]
    renamed: dict[str, str] = field(default_factory=dict)
    dry_run: bool = False


def resolve_target(
    config: DagsConfig,
    target_name: str | None,
    *,
    dev_key: str | None = None,
    git: GitInfo | None = None,
) -> ResolvedTarget:
    """Pick the target and work out its prefix.

    A development target's dev key is `dev_key`, else the current branch
    (``GITHUB_HEAD_REF``, ``BITBUCKET_BRANCH``, ... or git), as a slug.

    Raises:
        ConfigurationError: If `dev_key` is given for production, or a
            development target has no branch to be named after.
    """
    target = config.target(target_name)
    if target.production:
        if dev_key:
            raise ConfigurationError("--dev-key only applies to a development target")
        return ResolvedTarget(target, "", target_prefix(config.name, None))
    branch = dev_key or (git or collect(config.root)).ref
    if not branch:
        raise ConfigurationError(
            "no branch to name the dev deploy after (detached HEAD?) — pass --dev-key"
        )
    key = dev_slug(branch)
    return ResolvedTarget(target, key, target_prefix(config.name, key))


def stage(
    config: DagsConfig,
    resolved: ResolvedTarget,
    into: Path,
    *,
    git: GitInfo,
    now: datetime | None = None,
) -> dict[str, str]:
    """Copy ``artifacts.dags`` into `into` as it will be deployed.

    A dev target's top-level packages are namespaced, and the target's
    `_databaas_target.json` is written.

    Returns:
        The renamed top-level modules, old name to new.

    Raises:
        NamespacingError: If a dev target's renaming leaves the tree broken.
    """
    for relative, path in collect_files(config.source, (TARGET_FILE,)).items():
        destination = into / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    renamed = namespace_packages(into, resolved.dev_key) if resolved.dev_key else {}
    document = target_document(
        bundle=config.name, dev_key=resolved.dev_key, git=git, now=now
    )
    (into / TARGET_FILE).write_text(json.dumps(document, indent=2) + "\n")
    return renamed


def deploy(
    config: DagsConfig,
    target_name: str | None,
    bucket: s3.DagBucket,
    *,
    dev_key: str | None = None,
    dry_run: bool = False,
    git: GitInfo | None = None,
    client: Any = None,
    now: datetime | None = None,
    log: Callable[[str], None] = lambda _: None,
) -> DeployResult:
    """Make the target's prefix hold exactly the ``artifacts.dags`` tree.

    The tree is staged in a temporary directory: a dev deploy namespaces its
    top-level packages there and `_databaas_target.json` is written there, so
    the checkout is never changed. ``_databaas_target.json`` is uploaded
    first, then changed files; files no longer in the tree are deleted last.

    Raises:
        ConfigurationError: On a bad target or dev key.
        NamespacingError: If a dev deploy's renaming leaves the tree broken.
    """
    provenance = git or collect(config.root)
    resolved = resolve_target(config, target_name, dev_key=dev_key, git=provenance)
    s3_client = client or bucket.client()
    with tempfile.TemporaryDirectory(prefix="databaas-dags-") as staging:
        renamed = stage(config, resolved, Path(staging), git=provenance, now=now)
        files = collect_files(Path(staging))
        remote = {
            obj.key: obj
            for obj in s3.list_objects(s3_client, bucket.bucket, resolved.prefix)
        }
        plan = s3.plan_sync(files, remote, resolved.prefix)
        if not dry_run:
            target_key = resolved.prefix + TARGET_FILE
            ordered = sorted(plan.upload, key=lambda key: key != target_key)
            for key in ordered:
                log(f"upload {key}")
                s3.upload(
                    s3_client,
                    bucket.bucket,
                    key,
                    files[key.removeprefix(resolved.prefix)],
                )
            if plan.delete:
                log(f"delete {len(plan.delete)} stale object(s)")
                s3.delete(s3_client, bucket.bucket, plan.delete, resolved.prefix)
    return DeployResult(
        resolved=resolved,
        url=f"s3://{bucket.bucket}/{resolved.prefix}",
        uploaded=plan.upload,
        unchanged=plan.unchanged,
        deleted=plan.delete,
        renamed=renamed,
        dry_run=dry_run,
    )


def destroy(
    config: DagsConfig,
    target_name: str | None,
    bucket: s3.DagBucket,
    *,
    dev_key: str | None = None,
    force: bool = False,
    git: GitInfo | None = None,
    client: Any = None,
) -> tuple[ResolvedTarget, int]:
    """Delete everything under the target's prefix. Nothing there is not an error.

    Returns:
        The target and how many objects were deleted.

    Raises:
        ConfigurationError: For production without `force`, or a bad target.
    """
    resolved = resolve_target(config, target_name, dev_key=dev_key, git=git)
    if resolved.target.production and not force:
        raise ConfigurationError(
            f"refusing to destroy production target {resolved.target.name!r} "
            "without --force"
        )
    s3_client = client or bucket.client()
    keys = tuple(
        obj.key for obj in s3.list_objects(s3_client, bucket.bucket, resolved.prefix)
    )
    if keys:
        s3.delete(s3_client, bucket.bucket, keys, resolved.prefix)
    return resolved, len(keys)
