"""Harbor inside TRL (`trl/experimental/harbor/`, RL plan §6.6): a rollout whose environment is a `HarborEnv` is keyed
by the Harbor task as the Harbor connector keys it (`local:<folder>`, its content digest in the scenario) and graded by
Harbor's verifier, so it reads beside a `harbor run --plugin probe` eval of that folder by key and digest. TRL runs no
Harbor `Trial`, so there is nothing for the plugin to merge with: this adapter writes the sample alone. Line refs are
`huggingface/trl@4ae4d34a86f3` and `harbor-framework/harbor@9c7a39b991d7`."""

from __future__ import annotations

import functools
import hashlib
from pathlib import Path
from typing import Any

#: The base class every TRL Harbor harness subclasses (`trl/experimental/harbor/_env.py:42`).
HARBOR_ENV_CLASS = "HarborEnv"
HARBOR_ENV_MODULE = "trl.experimental.harbor"
#: Harbor's default verifier (`verifier/factory.py:89-99`) and the connector's version for it, the digest of its
#: empty kwargs (`connectors/harbor/samples`: `DEFAULT_VERIFIER`, `make_digest({})`; a test keeps them equal).
HARBOR_VERIFIER = "harbor.verifier.verifier:Verifier"
HARBOR_VERIFIER_VERSION = "sha256:" + hashlib.sha256(b"{}").hexdigest()


def is_harbor_env(environment: Any) -> bool:
    """Whether ``environment`` is a TRL `HarborEnv` (any harness), told by its class chain, never by importing TRL."""
    return any(
        cls.__name__ == HARBOR_ENV_CLASS and cls.__module__.startswith(HARBOR_ENV_MODULE)
        for cls in type(environment).__mro__
    )


def read_harbor_task(environment: Any) -> dict:
    """The task facts a reset Harbor environment holds (`_env.py:101-120`: `self._task = Task(task_dir=...)`). The key is
    Harbor's local task id, `local:<folder name>` (`models/task/id.py:43-49`, the connector's `build_task_key`); the
    digest is the one Harbor's lock records for a local task (`models/job/lock.py:618-623`); and the sandbox backend."""
    facts: dict[str, Any] = {"scorer": True}
    task = getattr(environment, "_task", None)
    task_dir = _get_task_dir(task)
    name = task_dir.name if task_dir is not None else getattr(task, "name", None)
    if isinstance(name, str) and name:
        facts["task_key"] = f"local:{name}"[:512]
    digest = get_task_digest(str(task_dir)) if task_dir is not None else None
    if digest:
        facts["task_digest"] = digest
    kind = getattr(environment, "_environment_type", None)
    if isinstance(kind, str) and kind:
        facts["environment_type"] = kind[:256]
    return facts


def make_harbor_scorer() -> dict:
    """`HarborEnv._verify` runs a default `VerifierConfig()` (`_env.py:174-196`): Harbor's own verifier with no kwargs,
    named and versioned as the Harbor connector names it."""
    return {"name": HARBOR_VERIFIER, "kind": "verifier", "version": HARBOR_VERIFIER_VERSION}


@functools.lru_cache(maxsize=1024)
def get_task_digest(task_dir: str) -> str | None:
    """`sha256:` + Harbor's content hash of a task folder (`publisher/packager.py:88-100`), once per folder. None
    where Harbor is not importable (a TRL Harbor env always has it) or the folder cannot be hashed."""
    try:
        from harbor.publisher.packager import Packager

        content_hash, _ = Packager.compute_content_hash(Path(task_dir))
    except Exception:  # noqa: BLE001 -- the digest is a scenario value, never a reason to lose the sample
        return None
    return content_hash if str(content_hash).startswith("sha256:") else f"sha256:{content_hash}"


def _get_task_dir(task: Any) -> Path | None:
    """`Task.task_dir` (`models/task/task.py:270-272`)."""
    try:
        found = getattr(task, "task_dir", None)
    except Exception:  # noqa: BLE001 -- a property on a half-built task
        return None
    return Path(found) if isinstance(found, (str, Path)) and str(found) else None
