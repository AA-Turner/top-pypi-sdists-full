"""Find the packages a System requires, from a script inside a checkout or a platform job.

Everything here reads ``.istari-deps/dependencies.lock.json`` and nothing else: no network,
no login. A checkout made by someone who may not open every package the System requires has no
lock; there ``locate`` finds a package by its only folder. The lock maps each package name to the folder it means at System level
(``locate``), with exceptions for package folders whose own requirement names another folder
(``within``). So a script inside a package that keeps ``fasteners/bolt`` at 1.2.1 finds
``bolt/1.2.1``, while every other script finds ``bolt/1.x``::

    from istari_digital_client import deps

    bolt = deps.locate("fasteners/bolt")        # answers for the file that calls it
    spec = bolt / "spec.json"
    print(deps.version(bolt))                   # "1.2.2"
"""

from __future__ import annotations

import inspect
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

from istari_digital_client._package_names import split_package_name

__all__ = ["NotRequiredError", "here", "locate", "root", "version"]

DEPS_FOLDER = ".istari-deps"
LOCK_PATH = f"{DEPS_FOLDER}/dependencies.lock.json"
ROOT_VARIABLE = "ISTARI_SYSTEM_ROOT"

PathLike = str | os.PathLike[str]


class NotRequiredError(LookupError):
    """The System's lock has no package by that name, or no folder at that path."""


def root(*, from_: PathLike | None = None) -> Path:
    """Return the System root: ``$ISTARI_SYSTEM_ROOT``, else the nearest folder holding ``.istari-deps/``.

    The search starts from ``from_``, by default the file that called, and then from the
    current directory. Raises FileNotFoundError when neither is inside a System checkout.
    """
    configured = os.environ.get(ROOT_VARIABLE)
    if configured:
        return Path(configured).resolve()
    starts = [Path(from_) if from_ is not None else _caller(), Path.cwd()]
    for start in starts:
        if start is None:
            continue
        start = start.resolve()
        for folder in [start, *start.parents]:
            if (folder / DEPS_FOLDER).is_dir():
                return folder
    raise FileNotFoundError(
        f"no {DEPS_FOLDER} folder above {starts[0] or Path.cwd()}; run inside a System "
        f"checkout or set {ROOT_VARIABLE}"
    )


def locate(
    name: str, *, within: PathLike | None = None, from_: PathLike | None = None
) -> Path:
    """Return the folder package ``name`` (``library/package``) means for whoever asks.

    The asker is ``within`` (a package folder, or the name of a package the System
    requires), else the package folder containing the file ``from_``, else the package
    folder containing the file that called. A package folder whose own requirement of
    ``name`` points elsewhere gets that folder; everyone else gets the System's. Raises
    NotRequiredError naming the package when the lock does not have it.
    """
    if within is not None and from_ is not None:
        raise ValueError("give within or from_, not both")
    asker = Path(from_) if from_ is not None else _caller()
    system = root(from_=asker)
    if not (system / LOCK_PATH).is_file():
        return _only_folder(system, name)
    lock = _read_lock(system)
    if within is not None:
        folder: str | None = _asking_folder(system, lock, within)
    else:
        folder = _package_folder(system, lock, asker) if asker else None
    return system / _located(system, lock, name, folder)


def here() -> Path:
    """Return the package folder containing the calling file, or the System root outside one."""
    caller = _caller() or Path.cwd()
    system = root(from_=caller)
    folder = _package_folder(system, _read_lock(system), caller)
    return system / folder if folder else system


def version(path_or_name: PathLike) -> str:
    """Return the version a package folder holds, given its path, a path inside it, or a package name.

    A name is located as :func:`locate` would for the calling file. A relative path is taken
    from the System root, as the lock writes paths.
    """
    system = root(from_=_caller())
    lock = _read_lock(system)
    if isinstance(path_or_name, str) and path_or_name in lock.get("locate", {}):
        path_or_name = locate(path_or_name)
    folder = _package_folder(system, lock, Path(path_or_name))
    for package in lock.get("packages", []):
        if package["folder"] == folder:
            return str(package["version"])
    raise NotRequiredError(
        f"{path_or_name} is not a package folder of the System at {system}"
    )


def _located(system: Path, lock: dict[str, Any], name: str, asker: str | None) -> str:
    """Return the folder ``name`` means for the package folder ``asker`` (None: the System)."""
    located: dict[str, str] = lock.get("locate", {})
    if name not in located:
        raise NotRequiredError(
            f"{name} is not required by the System at {system}; add it to dependencies.yaml"
        )
    exceptions: dict[str, str] = lock.get("within", {}).get(asker, {}) if asker else {}
    return exceptions.get(name, located[name])


def _only_folder(system: Path, name: str) -> Path:
    """Return the one folder of package ``name`` in a checkout without a lock."""
    library, package_key = split_package_name(name)
    package = system / DEPS_FOLDER / library / package_key
    folders = (
        sorted(path for path in package.iterdir() if path.is_dir())
        if package.is_dir()
        else []
    )
    if len(folders) == 1:
        return folders[0]
    if not folders:
        raise NotRequiredError(f"{name} is not in the checkout at {system}")
    raise NotRequiredError(
        f"{name} has {len(folders)} folders in {system} and this checkout has no {LOCK_PATH} "
        "to tell them apart; open one by its path"
    )


def _asking_folder(system: Path, lock: dict[str, Any], within: PathLike) -> str:
    """Return the package folder ``within`` names: a package folder path, or a required package's name."""
    text = str(within)
    folder = lock.get("locate", {}).get(text) or _package_folder(
        system, lock, Path(text)
    )
    if folder is None:
        raise NotRequiredError(
            f"{text} is not a package folder or package of the System at {system}"
        )
    return folder


def _package_folder(system: Path, lock: dict[str, Any], path: Path) -> str | None:
    """Return the lock's package folder that is or contains ``path`` (relative to the System root), or None."""
    try:
        relative = PurePosixPath(
            (system / path).resolve().relative_to(system).as_posix()
        )
    except ValueError:
        return None
    for package in lock.get("packages", []):
        folder = PurePosixPath(package["folder"])
        if relative == folder or folder in relative.parents:
            return str(folder)
    return None


def _read_lock(system: Path) -> dict[str, Any]:
    path = system / LOCK_PATH
    try:
        lock: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"no {LOCK_PATH} in {system}; check out the branch with its packages "
            "(it is left out for a reader who may not open every package)"
        ) from None
    return lock


def _caller() -> Path | None:
    """Return the file of the nearest caller outside this module, or None from an interactive prompt."""
    frame = inspect.currentframe()
    while frame is not None and frame.f_globals.get("__name__") == __name__:
        frame = frame.f_back
    if frame is None or frame.f_code.co_filename.startswith("<"):
        return None
    return Path(frame.f_code.co_filename)
