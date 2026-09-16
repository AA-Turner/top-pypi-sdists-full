"""Repository-shared tree binding and locking primitives."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

_fcntl: Any = None
try:
    import fcntl as _fcntl_module
except ImportError:  # pragma: no cover - exercised only on Windows
    pass
else:
    _fcntl = _fcntl_module

_REGISTRY_NAME = "epic-tree-bindings.json"
_LOCK_DIR = "epic-tree-locks"


def _git_common_dir() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("Unable to determine the Git common directory")
    common = Path(result.stdout.strip())
    return common.resolve() if common.is_absolute() else (Path.cwd() / common).resolve()


def _shared_dir() -> Path:
    return _git_common_dir().parent / ".agdt" / "create-epic"


def _registry_path() -> Path:
    return _shared_dir() / _REGISTRY_NAME


@contextmanager
def _registry_lock(registry: Path) -> Iterator[None]:
    lock_path = registry.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+", encoding="utf-8")
    try:
        if _fcntl is not None:  # pragma: no branch
            _fcntl.flock(handle.fileno(), _fcntl.LOCK_EX)
        yield
    finally:
        if _fcntl is not None:  # pragma: no branch
            _fcntl.flock(handle.fileno(), _fcntl.LOCK_UN)
        handle.close()


def _definition_key(path: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return path.relative_to(Path(result.stdout.strip()).resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def _read_registry(path: Path) -> dict:
    if not path.exists():
        return {"schemaVersion": "1.0", "bindings": {}}
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("Corrupt epic-tree binding registry")
    if document.get("schemaVersion") != "1.0" or not isinstance(document.get("bindings"), dict):
        raise ValueError("Corrupt epic-tree binding registry")
    seen: set[str] = set()
    for key, binding in document["bindings"].items():
        if (
            not isinstance(binding, dict)
            or binding.get("path") != key
            or binding.get("status") not in {"pending", "confirmed"}
            or not isinstance(binding.get("treeId"), str)
        ):
            raise ValueError("Corrupt epic-tree binding registry entry")
        try:
            uuid.UUID(binding["treeId"])
        except (ValueError, AttributeError):
            raise ValueError("Corrupt epic-tree binding registry treeId") from None
        if binding["treeId"] in seen:
            raise ValueError("Duplicate treeId in epic-tree binding registry")
        seen.add(binding["treeId"])
    return document


def _atomic_write(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    except Exception:
        try:
            os.unlink(name)
        except OSError:
            pass
        raise


def reserve_binding(
    definition_path: Path | str,
    *,
    tree_id: str | None = None,
    registry_path: Path | str | None = None,
) -> dict[str, str]:
    """Reserve a pending UUID binding for a canonical definition path."""
    path = Path(definition_path).resolve()
    key = _definition_key(path)
    registry = Path(registry_path) if registry_path is not None else _registry_path()
    with _registry_lock(registry):
        document = _read_registry(registry)
        existing = document["bindings"].get(key)
        if existing is not None:
            if tree_id is not None and existing["treeId"] != tree_id:
                raise ValueError(f"Definition path is already bound to treeId {existing['treeId']}")
            return dict(existing)
        selected = tree_id or str(uuid.uuid4())
        try:
            uuid.UUID(selected)
        except (ValueError, AttributeError):
            raise ValueError("tree_id must be a UUID") from None
        if any(item["treeId"] == selected for item in document["bindings"].values()):
            raise ValueError(f"treeId {selected} is already bound to another definition")
        binding = {"status": "pending", "treeId": selected, "path": key}
        document["bindings"][key] = binding
        _atomic_write(registry, document)
        return binding


def promote_binding(
    definition_path: Path | str,
    *,
    tree_id: str | None = None,
    registry_path: Path | str | None = None,
) -> dict[str, str]:
    """Promote a pending binding to a confirmed binding atomically."""
    path = Path(definition_path).resolve()
    registry = Path(registry_path) if registry_path is not None else _registry_path()
    key = _definition_key(path)
    with _registry_lock(registry):
        document = _read_registry(registry)
        binding = document["bindings"].get(key)
        if binding is None:
            raise ValueError(f"No binding reservation exists for {path}")
        if tree_id is not None and binding["treeId"] != tree_id:
            raise ValueError("treeId does not match the existing binding")
        binding = {**binding, "status": "confirmed"}
        document["bindings"][key] = binding
        _atomic_write(registry, document)
        return binding


def get_tree_lock_path(tree_id: str, *, common_dir: Path | str | None = None) -> Path:
    """Return the repository-shared lock path for a UUID tree identity."""
    normalized = str(uuid.UUID(str(tree_id)))
    common = Path(common_dir).resolve() if common_dir is not None else _git_common_dir()
    return common.parent / ".agdt" / _LOCK_DIR / f"{normalized}.lock"


@contextmanager
def acquire_tree_lock(tree_id: str, *, common_dir: Path | str | None = None) -> Iterator[Path]:
    """Acquire one non-blocking exclusive tree lock and release it on exit."""
    path = get_tree_lock_path(tree_id, common_dir=common_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+", encoding="utf-8")
    try:
        if _fcntl is None:  # pragma: no cover - Windows fallback
            import msvcrt  # type: ignore[import-not-found]

            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)  # type: ignore[attr-defined]
            except OSError as exc:
                raise RuntimeError(f"Tree lock is already held: {path}") from exc
        else:
            try:
                _fcntl.flock(handle.fileno(), _fcntl.LOCK_EX | _fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError(f"Tree lock is already held: {path}") from exc
        yield path
    finally:
        if _fcntl is not None:  # pragma: no branch
            _fcntl.flock(handle.fileno(), _fcntl.LOCK_UN)
        handle.close()
