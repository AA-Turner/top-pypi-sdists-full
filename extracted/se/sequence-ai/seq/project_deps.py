"""
A project's own dependency files, for `seq deploy`: what the image installs when a policy declares neither image= nor
deps= (or starts its image with seq.Image.from_project) - the files, this machine's versions, what to leave out and
what to add - and the plan the deploy prints before anything is sent. Nothing is resolved here: the platform fits the
files to Linux and the worker's machine when the image builds.

In one sentence: every folder from the entry file's up to the folder deployed is read for dependency files, a folder's lock before what it declares - uv.lock, poetry.lock, pdm.lock,
Pipfile.lock, requirements*.lock or a requirements.txt whose every line pins a version; else pyproject.toml's
dependencies, requirements.txt, setup.cfg / setup.py; a requirements-<name>.txt read as a requirements.txt where a
folder has none and declares nothing else, and of several none until from_project(requirements=) names one, read in
the nearest folder that holds it in place of that folder's other files - and the nearest lock is the one → the local
packages the code imports (loaded when it was imported, or named by an import in its files) that the upload holds in a
folder of their own
(a pyproject.toml or a setup.py), and that it would not import from the uploaded code as it is, are installed with
theirs → declared ranges are held to the versions this machine has (importlib.metadata) → [tool.seq] exclude / extra
and from_project's are laid over → one ImageStepProject, whose every path is a file the upload holds.

WHY the author's versions: a policy that runs here runs with these; a fresh resolve picks versions it never ran with
(OpenWAM's torch>=2.5,<3 resolved to 2.14.1 for Linux) or fails on a package's own metadata (flash-linear-attention
0.2.2 against torch 2.4.1). WHY the platform does the rest: what Linux and a card need - which CUDA a driver takes,
which CUDA extension has a prebuilt wheel, a headless OpenCV - changes with the platform's machines, not with this SDK.

"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from pydantic import ValidationError
from sequence_base.contract import (
    FROZEN_PATH,
    ImageSpec,
    ImageStepProject,
    ImageStepRun,
    ImageStepTemplateFiles,
    Project,
)

from seq.errors import PolicyDefinitionError


_PROJECT_LOCKS = ("uv.lock", "poetry.lock", "pdm.lock")
_PROJECT_FILES = ("pyproject.toml", "setup.py", "setup.cfg")



_NAMED_REQUIREMENTS = re.compile(r"requirements[-_][^/]+\.txt")
_REQUIREMENT = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(\[[^\]]*\])?\s*(.*)$")
_PINNED = re.compile(r"^==\s*[A-Za-z0-9.+!_-]+\s*(;.*)?$")
_PYTHONS = ("3.11", "3.12", "3.13")
_MAX_PINS = 4096
_SHOWN = 6
_COLUMN = 38


def norm(name: str) -> str:
    """A distribution's name as indexes compare them (PEP 503): `Flash_Linear.Attention` is flash-linear-attention."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _name(requirement: str) -> str | None:
    m = _REQUIREMENT.match(requirement)
    return norm(m.group(1)) if m else None


def _dir(path: str) -> str:
    """The folder a path of the upload is in ('' its root)."""
    parent = str(PurePosixPath(path).parent)
    return "" if parent == "." else parent


def _join(folder: str, name: str) -> str:
    return f"{folder}/{name}" if folder else name


def _inside(path: str, folder: str) -> bool:
    return not folder or path == folder or path.startswith(folder + "/")


def _ups(start: str) -> list[str]:
    """`start` and every folder above it, up to the upload's root ('')."""
    out = [start]
    while out[-1]:
        out.append(_dir(out[-1]))
    return out


def _toml(path: Path) -> dict | None:
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
        except ModuleNotFoundError:
            return None
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except (OSError, ValueError):
        return None


def _requirement_lines(path: Path, seen: set[Path] | None = None) -> list[str] | None:
    """A requirements file's requirements, one a line, with those of a file it includes (-r); None when a line installs
    a folder or a VCS checkout, which only the file itself says how to make."""
    seen = seen if seen is not None else set()
    if path in seen or not path.is_file():
        return []
    seen.add(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.split(" #", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^(-r|--requirement)\b", line):
            more = _requirement_lines(path.parent / re.sub(r"^(-r|--requirement)[ =]?", "", line).strip(), seen)
            if more is None:
                return None
            out += more
        elif re.match(r"^(-e|--editable)\b|^[./]|^(git\+|file:)", line):
            return None
        elif not line.startswith("-"):
            out.append(line)
    return out


def _all_pinned(lines: list[str] | None) -> bool:
    if not lines:
        return False
    for line in lines:
        m = _REQUIREMENT.match(line)
        if not m or not _PINNED.match(m.group(3).strip()):
            return False
    return True


def _counted(path: Path) -> int:
    """How many packages a lock names."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    if path.name == "Pipfile.lock":
        try:
            return len(json.loads(text).get("default") or {})
        except ValueError:
            return 0
    if path.name in _PROJECT_LOCKS:
        return len(re.findall(r"^\[\[package\]\]", text, re.M))
    return len(_requirement_lines(path) or [])


def _pyproject_deps(data: dict | None) -> list[str] | None:
    """pyproject.toml's [project].dependencies, None when it declares none (a tool's settings, a poetry project)."""
    deps = ((data or {}).get("project") or {}).get("dependencies")
    return [d for d in deps if isinstance(d, str)] if isinstance(deps, list) and deps else None



@dataclass
class _Level:
    """One folder on the way up with dependency files: its lock, else what it declares."""
    folder: str
    lock: str | None = None
    declared: list[str] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    note: str | None = None
    several: list[str] = field(default_factory=list)


def _level(top: Path, folder: str, files: dict[str, set[str]], kind: str, named: str | None = None) -> _Level | None:
    here = files.get(folder, set())
    where = top / folder if folder else top
    lv = _Level(folder)
    if named in here:


        return _read_requirements(lv, where, here, named, lock=named.endswith(".lock"))
    for lock in _PROJECT_LOCKS:
        if lock in here and "pyproject.toml" in here:
            lv.lock = lock
            return lv
    if "Pipfile.lock" in here:
        lv.lock = "Pipfile.lock"
        return lv
    req_locks = sorted(n for n in here if re.fullmatch(r"requirements[^/]*\.lock", n))
    pick = [n for n in ("requirements.lock", f"requirements-{kind}.lock") if n in req_locks] or \
        (req_locks if len(req_locks) == 1 else [])
    if pick:
        lv.lock = pick[0]
        return lv
    if len(req_locks) > 1:
        lv.note = (f"{', '.join(_join(folder, n) for n in req_locks)}: several locks and none named requirements.lock "
                   f"or requirements-{kind}.lock, so none of them is used")
    txt = "requirements.txt" if "requirements.txt" in here else None
    if txt is None and named is None and not _declares(where, here):
        own = sorted(n for n in here if _NAMED_REQUIREMENTS.fullmatch(n))
        if len(own) > 1:
            lv.several = own
            return lv
        txt = own[0] if own else None
    return _read_requirements(lv, where, here, txt)


def _declares(where: Path, here: set[str]) -> bool:
    """Whether a folder declares its dependencies in a file of the project's own - pyproject.toml's, a setup.cfg or a
    setup.py - beside which a named requirements file (a requirements-dev.txt) is never taken for the project's."""
    return bool(here & {"setup.cfg", "setup.py"}) or (
        "pyproject.toml" in here and bool(_pyproject_deps(_toml(where / "pyproject.toml"))))


def _read_requirements(lv: _Level, where: Path, here: set[str], txt: str | None, *,
                       lock: bool = False) -> _Level | None:
    """A folder's requirements file `txt` read as requirements.txt is - every line pinned, its lock; else what it
    declares beside pyproject.toml's dependencies - or, without one, what the rest of its files declare. `lock`: `txt`
    is a lock as it is (a requirements*.lock)."""
    reqs = _requirement_lines(where / txt) if txt and not lock else []
    if txt and (lock or _all_pinned(reqs)):
        lv.lock = txt
        return lv
    if "pyproject.toml" in here:
        deps = _pyproject_deps(_toml(where / "pyproject.toml"))
        if deps:
            lv.declared.append("pyproject.toml")
            lv.requirements += deps
    if txt:
        lv.declared.append(txt)
        lv.requirements += reqs or []
    if not lv.declared:
        for name in ("setup.cfg", "setup.py"):
            if name in here:
                lv.declared.append(name)
                break
    if not lv.declared and "environment.yml" in here:
        lv.note = (f"{_join(lv.folder, 'environment.yml')} is conda's, which the platform's images do not have: name "
                   "its pip packages in a requirements.txt beside it")
    return lv if lv.declared or lv.note else None



def _installable(top: Path, folder: str, here: set[str]) -> bool:
    """A folder pip could install: a setup.py or setup.cfg, or a pyproject.toml naming a project or a build backend."""
    if "setup.py" in here or "setup.cfg" in here:
        return True
    if "pyproject.toml" not in here:
        return False
    data = _toml((top / folder if folder else top) / "pyproject.toml") or {}
    return bool(data.get("project") or data.get("build-system"))


def _modules_at(folder: str, names: set[str], *, packages_only: bool) -> set[str]:
    """The top-level modules importable from `folder`: a module file or a package, at its root or (a package folder's)
    in src/ - with packages_only, a package has its __init__.py; else any folder of Python files is one (a namespace
    package, as Python imports it)."""
    out: set[str] = set()
    prefix = f"{folder}/" if folder else ""
    for n in names:
        if not n.startswith(prefix) or not n.endswith(".py"):
            continue
        parts = n[len(prefix):].split("/")
        if packages_only and parts[0] == "src" and len(parts) > 1:
            parts = parts[1:]
        if len(parts) == 1:
            if parts[0] not in ("setup.py", "conftest.py", "__init__.py"):
                out.add(parts[0][:-3])
        elif not packages_only or (len(parts) == 2 and parts[1] == "__init__.py"):
            out.add(parts[0])
    return out


def _imports(path: Path) -> set[str]:
    """The top-level modules a Python file imports by name, wherever in it: at its top, in a function, under a try."""
    try:
        tree = ast.parse(path.read_bytes())
    except (SyntaxError, ValueError, OSError):
        return set()
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
            out.add(node.module.split(".")[0])
    return out


def _packages(top: Path, names: set[str], start: str, import_root: str, loaded: list[str], scanned: list[str],
              candidates: list[str]) -> list[str]:
    """The package folders the code imports from: each loaded module's nearest installable folder, and each folder
    holding a module a scanned file imports - never for a module the code imports from the upload as it is. A file of
    a package (one not around `start`) speaks for nothing: its imports are its own pyproject's to declare."""
    chosen: list[str] = []
    scanned = [r for r in scanned if not any(c and _inside(r, c) and not _inside(start, c) for c in candidates)]
    for rel in loaded:
        if _inside(rel, import_root):
            continue
        holder = next((f for f in _ups(_dir(rel)) if f in candidates), None)
        if holder is not None and holder not in chosen:
            chosen.append(holder)
    importable = _modules_at(import_root, names, packages_only=False)
    stdlib = getattr(sys, "stdlib_module_names", frozenset())
    provides = {c: _modules_at(c, names, packages_only=True) for c in candidates}
    for rel in scanned:
        for module in sorted(_imports(top / rel) - importable - set(stdlib)):
            mine = [c for c, mods in provides.items() if module in mods and not _inside(rel, c)]
            mine.sort(key=lambda c: -len(os.path.commonprefix([c + "/", rel])))
            if mine and mine[0] not in chosen:
                chosen.append(mine[0])
    return chosen



def _release(version: str) -> tuple[int, ...]:
    m = re.match(r"^v?(\d+(?:\.\d+)*)", version.strip())
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def fits(spec: str, version: str) -> bool:
    """Whether `version` meets a requirement's version range (">=1.24,<3", "==2.4.1", "~=1.4", "!=1.2.*"), compared by
    release numbers - 2.4.1+cu121 is 2.4.1. A range it cannot read lets the version in."""
    have = _release(version)
    for clause in (c.strip() for c in spec.split(",") if c.strip()):
        m = re.match(r"^(~=|===|==|!=|>=|<=|>|<)\s*v?([0-9]+(?:\.[0-9]+)*)(\.\*)?", clause)
        if not m or not have:
            continue
        op, raw, star = m.groups()
        want = tuple(int(x) for x in raw.split("."))
        n = max(len(have), len(want))
        a, b = have + (0,) * (n - len(have)), want + (0,) * (n - len(want))
        if star:
            ok = (have[:len(want)] == want) == (op == "==")
        elif op == "~=":
            ok = a >= b and have[:len(want) - 1] == want[:-1]
        else:
            ok = {"==": a == b, "===": a == b, "!=": a != b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]
        if not ok:
            return False
    return True


def _spec(requirement: str) -> str:
    m = _REQUIREMENT.match(requirement)
    rest = m.group(3).split(";", 1)[0].strip() if m else ""
    return "" if rest.startswith("@") else rest.strip("()")


def local_versions(requirements: list[str], skip: set[str]) -> tuple[dict[str, str], list[str]]:
    """({name: version} for each requirement this machine has installed within the range the project asks, and each
    package it pulls in, as installed; the requirements it has outside their range, said) - less what `skip` names
    (the local packages, installed from the upload) and anything installed from a URL, a VCS or a folder, whose version
    no index has. One outside its range is not the author's tested version: this machine did not run the project with
    it (an SDK's own numpy 2 beside a project's numpy<2)."""
    from importlib import metadata

    out: dict[str, str] = {}
    outside: list[str] = []
    asked = {n: _spec(r) for r in requirements if (n := _name(r))}
    todo = list(asked)
    seen: set[str] = set()
    while todo and len(out) < _MAX_PINS:
        name = todo.pop(0)
        if name in seen or name in skip:
            continue
        seen.add(name)
        try:
            dist = metadata.distribution(name)
        except metadata.PackageNotFoundError:
            continue
        if dist.read_text("direct_url.json"):
            continue
        version = dist.version or ""
        if name in asked and not fits(asked[name], version):
            outside.append(f"{name} {version} (the project asks {asked[name]})")
            continue
        if re.fullmatch(r"[A-Za-z0-9.+!_-]{1,64}", version):
            out[norm(dist.metadata["Name"] or name)] = version
        for req in dist.requires or []:
            if "extra" not in req.partition(";")[2]:
                todo += [n for n in [_name(req)] if n]
    return out, outside



def _cmp(have: tuple[int, ...], want: tuple[int, ...]) -> int:
    n = max(len(have) + 1, len(want))
    a = have + (99,) * (n - len(have))
    b = want + (0,) * (n - len(want))
    return (a > b) - (a < b)


def allows(spec: str, version: str) -> bool:
    """Whether a requires-python range (">=3.10,<3.13", "~=3.11", "==3.11.*") lets the worker's `version` in."""
    have = tuple(int(x) for x in version.split("."))
    for clause in (c.strip() for c in spec.split(",") if c.strip()):
        m = re.match(r"^(~=|===|==|!=|>=|<=|>|<)\s*v?([0-9]+(?:\.[0-9]+)*)(\.\*)?$", clause)
        if not m:
            continue
        op, raw, star = m.groups()
        want = tuple(int(x) for x in raw.split("."))
        if star:
            ok = (have[:len(want)] == want) == (op == "==")
        elif op == "~=":
            ok = _cmp(have, want) >= 0 and have[:len(want) - 1] == want[:-1]
        elif op in ("==", "===", "!="):
            ok = (have[:len(want)] == want[:len(have)]) == (op != "!=")
        else:
            c = _cmp(have, want)
            ok = {">=": c >= 0, "<=": c <= 0, ">": c > 0, "<": c < 0}[op]
        if not ok:
            return False
    return True


def _python(given: str | None, pinned: str | None, ranges: list[str]) -> tuple[str, str]:
    """The worker's Python and why: as declared → the project's .python-version → the one this machine runs, when the
    worker runs it and the project allows it → the worker's default (3.11), the one most packages build for, when the
    project allows it → the lowest the project allows. Not the newest: torch 2.4 has no build for 3.13."""
    if given:
        return given, "as declared"
    if pinned:
        m = re.search(r"(\d+)\.(\d+)", pinned)
        if m and f"{m.group(1)}.{m.group(2)}" in _PYTHONS:
            return f"{m.group(1)}.{m.group(2)}", ".python-version"
    here = f"{sys.version_info.major}.{sys.version_info.minor}"
    allowed = [v for v in _PYTHONS if all(allows(r, v) for r in ranges)]
    if here in allowed:
        return here, "the Python this machine runs"
    why = (f"this machine's {here} is not one the worker runs" if here not in _PYTHONS
           else f"the project does not allow this machine's {here}")
    if allowed:
        return allowed[0], ("the worker's default" if allowed[0] == _PYTHONS[0] else "the lowest the project allows") + \
            f" - {why}"
    return _PYTHONS[0], "the worker's default (the project's requires-python allows none the worker runs)"



@dataclass
class Found:
    """What `find` read, as the project step names it, and the plan the deploy prints."""
    root: str
    lock: str | None
    declared: list[str]
    packages: list[str]
    pins: dict[str, str]
    exclude: list[str]
    extra: list[str]
    python: str
    lines: list[str] = field(default_factory=list)

    def project(self) -> Project:
        try:

            return Project(root=self.root, lock=self.lock, declared=self.declared,
                           packages=[p or "." for p in self.packages],
                           pins=self.pins, exclude=self.exclude, extra=self.extra)
        except ValidationError as exc:
            raise PolicyDefinitionError(f"the project's dependency files: {exc.errors()[0]['msg']}") from None


def _by_folder(names: set[str]) -> dict[str, set[str]]:
    files: dict[str, set[str]] = {}
    for n in names:
        files.setdefault(_dir(n), set()).add(PurePosixPath(n).name)
    return files


def find(top: Path, names: set[str], start: str, *, import_root: str, loaded: list[str] = (),
         scanned: list[str] = (), kind: str = "policy", exclude: list[str] = (), extra: list[str] = (),
         python: str | None = None, requirements: str | None = None) -> Found | None:
    """The project's dependency files from `start` up to the upload's root, with the local packages the code imports
    and this machine's versions of what they declare - None when the upload holds none. `names` are the upload's
    files, as paths from `top`; `import_root` is where its code imports from, `loaded` the upload's files the code
    loaded when it was imported, `scanned` the files whose imports name the local packages it uses; `requirements` the
    requirements file from_project(requirements=) names, read in the nearest of those folders that holds it. Raises
    PolicyDefinitionError for a named file none holds, and for a folder of several named requirements files that
    declares nothing else, of which none is named."""
    files = _by_folder(set(names))
    ups = _ups(start)
    if requirements is not None and not any(requirements in files.get(f, set()) for f in ups):
        first = start or "the upload's root"
        raise PolicyDefinitionError(
            f'seq.Image.from_project(requirements="{requirements}"): {requirements} is in none of the folders seq '
            f"deploy reads, {first} and those above it up to the folder it uploads")
    levels = [lv for lv in (_level(top, f, files, kind, requirements) for f in ups) if lv]
    several = next((lv for lv in levels if lv.several), None)
    if several is not None:
        raise PolicyDefinitionError(
            f"{', '.join(_join(several.folder, n) for n in several.several)}: several requirements files and no "
            "requirements.txt, pyproject.toml dependencies or setup.py beside them, so which one the project installs "
            f'is yours to say: image=seq.Image.from_project(requirements="{several.several[0]}")')
    candidates = [f for f, here in files.items() if here & set(_PROJECT_FILES) and _installable(top, f, here)]
    packages = _packages(top, set(names), start, import_root, list(loaded), list(scanned), candidates)
    data = {f: _toml((top / f if f else top) / "pyproject.toml") or {}
            for f in dict.fromkeys([*ups, *packages]) if "pyproject.toml" in files.get(f, set())}
    tool = [(d.get("tool") or {}).get("seq") or {} for d in data.values()]
    excluded = list(dict.fromkeys([norm(n) for n in exclude] + [norm(n) for t in tool for n in t.get("exclude") or []
                                                                 if isinstance(n, str)]))
    added = list(dict.fromkeys([*extra, *(r for t in tool for r in t.get("extra") or [] if isinstance(r, str))]))
    name_of = {p: norm(str((data.get(p, {}).get("project") or {}).get("name") or "")) for p in packages}
    packages = [p for p in packages if name_of[p] not in excluded]
    notes = [lv.note for lv in levels if lv.note]
    levels = [lv for lv in levels if lv.lock or lv.declared]
    if not levels and not packages:
        return None


    lock_level = next((lv for lv in levels if lv.lock), None)
    lock = _join(lock_level.folder, lock_level.lock) if lock_level else next(
        (_join(p, lf) for p in packages for lf in _PROJECT_LOCKS
         if lf in files.get(p, set()) and "pyproject.toml" in files.get(p, set())), None)
    lock_folder = _dir(lock) if lock else None
    declared = [_join(lv.folder, d) for lv in levels if not lv.lock
                for d in lv.declared if not (d == "pyproject.toml" and lv.folder in packages)]
    chosen = declared + ([lock] if lock else [])
    root = _common([_dir(p) for p in chosen]) if chosen else ""
    requirements = [r for lv in levels if not lv.lock and lv.folder not in packages for r in lv.requirements]
    for p in packages:
        requirements += _pyproject_deps(data.get(p)) or []
    own = {n for n in name_of.values() if n}
    held, outside = local_versions(requirements, own | set(excluded))
    pins = {n: v for n, v in held.items() if n not in excluded}
    ranges = [str(rp) for d in data.values() if (rp := (d.get("project") or {}).get("requires-python"))]
    pinned = None
    for f in ([lock_folder] if lock_folder is not None else []) + [lv.folder for lv in levels]:
        if ".python-version" in files.get(f, set()):
            text = ((top / f if f else top) / ".python-version").read_text(errors="replace").strip()
            pinned = text.splitlines()[0] if text else None
            break
    version, why = _python(python, pinned, ranges)
    here = f"{sys.version_info.major}.{sys.version_info.minor}"
    if version != here and pins:

        notes.append(f"this machine's versions are not kept: it runs Python {here}, the worker {version}")
        pins, outside = {}, []
    found = Found(root=root, lock=_relative(lock, root) if lock else None,
                  declared=[_relative(d, root) for d in declared], packages=packages, pins=pins, exclude=excluded,
                  extra=added, python=version)
    if outside:
        notes.append(f"not kept, outside the range the project asks: {_shown(outside)}")
    found.lines = _plan(top, found, lock, declared, data, notes, why)
    return found


def _relative(path: str, root: str) -> str:
    return path[len(root) + 1:] if root and path.startswith(root + "/") else path


def _common(folders: list[str]) -> str:
    """The deepest folder of the upload holding every one of `folders`."""
    common: list[str] = []
    for group in zip(*[f.split("/") if f else [] for f in folders]):
        if len(set(group)) != 1:
            break
        common.append(group[0])
    return "/".join(common)


def _shown(items: list[str]) -> str:
    more = len(items) - _SHOWN
    return ", ".join(items[:_SHOWN]) + (f" and {more} more" if more > 0 else "")


def _plan(top: Path, found: Found, lock: str | None, declared: list[str], data: dict, notes: list[str],
          why: str) -> list[str]:
    """What the deploy says about the project's dependencies, a line each: the files, the packages, this machine's
    versions, what is left out and added, the Python."""
    lines = []
    if lock:
        lines.append(f"  {lock:{_COLUMN}} the lock: {_counted(top / lock)} packages at their exact versions")
    for path in declared:
        name = PurePosixPath(path).name
        n = len(_pyproject_deps(_toml(top / path)) or []) if name == "pyproject.toml" else \
            None if name in ("setup.cfg", "setup.py") else len(_requirement_lines(top / path) or [])
        lines.append(f"  {path:{_COLUMN}} " + (f"{n} requirement(s)" if n is not None else "installed as a package"))
    for p in found.packages:
        project = data.get(p, {}).get("project") or {}
        deps = _pyproject_deps(data.get(p))
        held = lock is not None and _dir(lock) == p
        lines.append(f"  {(p or '.') + '/':{_COLUMN}} "
                     + (f"the package {project['name']}" if project.get("name") else "a package") + " the code imports"
                     + (", with what its lock pins" if held else f", with its {len(deps)} requirement(s)" if deps
                        else ", with what it requires"))
    if found.pins:
        lines.append(f"  {'versions kept from this machine':{_COLUMN}} {len(found.pins)}: "
                     + _shown([f"{n} {v}" for n, v in found.pins.items()]))
    if found.exclude:
        lines.append(f"  {'left out':{_COLUMN}} {_shown(found.exclude)}")
    if found.extra:
        lines.append(f"  {'added':{_COLUMN}} {_shown(found.extra)}")
    lines.append(f"  {'Python ' + found.python:{_COLUMN}} {why}")
    lines += [f"  note: {n}" for n in notes]
    lines.append("  the platform fits these to Linux and the worker's machine as the image builds; the build log's "
                 "first lines say how")
    return lines


def mentioned(top: Path, names: set[str], start: str, kind: str = "policy") -> list[str]:
    """The dependency files a project has from `start` up - for a deploy that does not read them, to name them."""
    files = _by_folder(set(names))
    out: list[str] = []
    for f in _ups(start):
        lv = _level(top, f, files, kind)
        if lv and lv.lock:
            out.append(_join(f, lv.lock))
        elif lv:
            out += [_join(f, d) for d in [*lv.declared, *lv.several]]
    return out


def with_project(image: ImageSpec, found: Found, at: int | None) -> ImageSpec:
    """`image` with the project's step: the one from_project began it with, filled, or - `at` None - a policy's
    default image (debian_slim) installing the project."""
    step = ImageStepProject(project=found.project())
    if at is None:
        return ImageSpec(base=image.base, steps=[step], python=found.python)
    steps = list(image.steps)
    steps[at] = step
    return image.model_copy(update={"steps": steps, "python": image.python or found.python})



def _rel(path: Path, folder: Path) -> str | None:
    try:
        rel = path.resolve().relative_to(folder).as_posix()
    except ValueError:
        return None
    return "" if rel == "." else rel


def _where(snap, handler_ref: str, names: set[str]) -> tuple[str, str, list[str], list[str]]:
    """(where the search starts - the entry file's folder -, the import root, the upload's files importing the entry
    loaded, the files whose imports name its local packages - the entry file and those), each a path in the upload.
    What the import loaded is seq.loading.imported_with's; every module this process has, for a class deployed from
    Python."""
    from seq.loading import imported_with

    folder = Path(snap.folder).resolve()
    module = handler_ref.partition(":")[0]
    entry = getattr(sys.modules.get(module), "__file__", None)
    entry_rel = _rel(Path(entry), folder) if entry else None
    start = (_rel(Path(entry).parent, folder) if entry else None) or ""
    with_it = imported_with(module)
    modules = [sys.modules.get(n) for n in with_it] if with_it is not None else list(sys.modules.values())
    loaded = sorted({r for m in modules
                     if (f := getattr(m, "__file__", None)) and (r := _rel(Path(f), folder)) is not None and r in names})
    entry_files = [entry_rel] if entry_rel in names else []
    return start, getattr(snap, "import_root", "") or "", loaded, list(dict.fromkeys(loaded + entry_files))




_FROZEN_FILE = re.compile(re.escape(FROZEN_PATH) + r"/([^\s'\";|&()]+)")


def _frozen_installs(image: ImageSpec) -> set[str]:
    """The files of a template version's frozen copy the image's own steps install: what each run_commands step after
    its template_files step names at FROZEN_PATH, where that step puts the template's files under their own names. None
    for an image without template_files, or before it: no step but a run_commands after it reads them."""
    after, out = False, set()
    for step in image.steps:
        if isinstance(step, ImageStepTemplateFiles):
            after = True
        elif after and isinstance(step, ImageStepRun):
            out |= {m.group(1) for command in step.run_commands for m in _FROZEN_FILE.finditer(command)}
    return out


def _not_read(snap, handler_ref: str, kind: str, declared: str | None, image: ImageSpec) -> list[str]:
    """What a deploy that installs none of the project's dependency files says when the project has some - but for an
    official template's folder, whose image installs its files as their frozen copy and so reads them as that copy.
    
"""
    from seq.code_bundle import bundle_listing

    if snap.folder is None or snap.bundle is None:
        return []
    names = set(bundle_listing(snap.bundle))
    start = _where(snap, handler_ref, names)[0]
    files = mentioned(Path(snap.folder).resolve(), names, start, kind)




    if any(_join(start, name) in names for name in _frozen_installs(image)):
        files = [f for f in files if _dir(f) != start]
    if not files:
        return []
    how = {"image=": "as image= declares", "deps=": "as deps= declares, on debian_slim"}.get(
        declared or "", "as the benchmark declares its image (debian_slim when it declares none)")
    return [f"dependencies  {how}: the project's own files ({_shown(files)}) are not read - start the image with "
            "seq.Image.from_project() to install from them"]


def image_for(image: ImageSpec, snap, *, handler_ref: str, kind: str, declared: str | None) -> ImageSpec:
    """The image a deploy sends, with the project's dependencies where they go - in the step seq.Image.from_project
    began it with, or, for a policy that wrote neither image= nor deps= and whose project has dependency files, on
    debian_slim - and what the deploy says about them, in `snap.deps_lines`. Raises PolicyDefinitionError for a
    from_project image whose files are not uploaded (its module is installed) or that has none."""
    from seq.code_bundle import bundle_listing

    at = next((i for i, s in enumerate(image.steps) if isinstance(s, ImageStepProject)), None)
    if at is None and (kind != "policy" or declared is not None):
        snap.deps_lines = _not_read(snap, handler_ref, kind, declared, image)
        return image
    if snap.folder is None or snap.bundle is None:
        if at is not None:
            raise PolicyDefinitionError(
                "seq.Image.from_project() installs the project's dependency files from what the deploy uploads, and "
                "this module is installed, so nothing is uploaded: deploy the folder of its source")
        return image
    names = set(bundle_listing(snap.bundle))
    start, import_root, loaded, scanned = _where(snap, handler_ref, names)
    given = image.steps[at].project if at is not None else None

    found = find(Path(snap.folder).resolve(), names, start, import_root=import_root, loaded=loaded, scanned=scanned,
                 kind=kind, exclude=list(given.exclude) if given else [], extra=list(given.extra) if given else [],
                 python=image.python if at is not None else None,
                 requirements=given.declared[0] if given and given.declared else None)
    if found is None:
        if at is not None:
            raise PolicyDefinitionError(
                f"seq.Image.from_project(): the upload holds no dependency file in {start or 'its root'} or a folder "
                "above it (a lock, pyproject.toml's dependencies, a requirements file, setup.py), and no package of "
                "the code's own - write them, or declare the image's packages with uv_pip_install()")
        return image
    head = "from seq.Image.from_project():" if at is not None else \
        "from the project's own files (the policy declares no image= and no deps=):"
    snap.deps_lines = [f"dependencies  {head}", *found.lines]
    return with_project(image, found, at)
