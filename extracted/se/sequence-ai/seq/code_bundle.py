"""
Pack a deployment's source into the deploy body's `code` bundle.

In one sentence: `seq deploy [folder]` uploads that folder, whole - the class to deploy found in it by reading its
files (seq.discover) and imported from it, so the folder is the module's import root - less what its rules leave out
(version control and caches anywhere; a virtualenv or a build's output at the folder's root; a .env file, unless a
.seqignore takes it back; what each folder's .seqignore names; a template's large upstream while it is as published,
which the image installs from its official package), each of which the deploy names → that snapshot is the version's
code, nothing kept from an earlier version → a module the class imported that the upload leaves behind is refused →
the deploy prints how many files, how large, and their hash (seq.source.files_sha256), which the platform keeps beside
the version.

WHY a folder: one argument decided both which class to deploy and which code to upload - "so when you deploy, you deploy
a py file, and then it uploads the entire thing. That is not very intuitive. Why couldn't we just deploy a folder"
. WHY the whole folder: a helper, a config or
third_party/ left behind ran the version the author did not see. WHY nothing is
left out unsaid: `build/` and `env/` were dropped wherever they were, a vendored package's own `build/` with them (worker
8, 10-13). An add_local_file / add_local_dir path inside the folder is the folder's own copy (its add_local step names it
there); one outside it ships under `_seq_local/<n>/`.

The tar is deterministic (sorted entries, zeroed mtime/owner) so the same source gives the same sha256 and the platform
can reuse a build. A module installed in site-packages ships nothing: the image is expected to install it.
"""
from __future__ import annotations

import ast
import gzip
import importlib
import importlib.machinery
import importlib.util
import io
import os
import re
import subprocess
import sys
import sysconfig
import tarfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from sequence_base.constants.serving import MAX_SOURCE_TREE_BYTES
from sequence_base.contract import MAX_CODE_BUNDLE_BYTES, CodeBundle

from seq import source
from seq.errors import PolicyDefinitionError



_ROOT_SKIP_DIRS = frozenset({".venv", "venv", "env", "build", "dist", "node_modules"})
_ROOT_SKIP_SUFFIXES = (".egg-info",)





SOURCE_CONTEXT_DIR = "build-context"
IGNORE_FILE = ".seqignore"


_MAX_RAW_BYTES = MAX_SOURCE_TREE_BYTES
_WHY_SKIPPED = {".git": "version control", ".hg": "version control", ".svn": "version control"}


_ENV_WHY = "a .env file: secrets go through `seq secret`; a .seqignore line !.env uploads it"


@dataclass
class Snapshot:
    """What a deploy uploads: the bundle, and what to say about it."""
    bundle: CodeBundle | None
    entry: str
    folder: Path | None
    files: int = 0
    raw_bytes: int = 0
    tree_sha256: str | None = None
    left_out: list[tuple[str, str]] = field(default_factory=list)
    sources: list[source.SourceState] = field(default_factory=list)
    src_map: dict[str, str] = field(default_factory=dict)
    deps_lines: list[str] = field(default_factory=list)


def _installed_roots() -> list[Path]:
    import site

    paths = sysconfig.get_paths()
    found = {paths.get("purelib"), paths.get("platlib"), paths.get("stdlib"), site.getusersitepackages(),
             *getattr(site, "getsitepackages", list)()}
    return [Path(p).resolve() for p in found if p]


def _is_installed(path: Path) -> bool:
    p = path.resolve()
    return any(p == root or root in p.parents for root in _installed_roots())


def _walk(root: Path, arc_prefix: str, left_out: list[tuple[str, str]] | None = None) -> list[tuple[Path, str]]:
    """Every file of a declared directory or a package, as (path, archive name), in a stable order: version control,
    caches and links left out (and named in `left_out`), everything else as it is."""
    out: list[tuple[Path, str]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        keep = []
        for d in sorted(dirnames):
            arc = (Path(arc_prefix) / rel / d).as_posix()
            link = os.path.islink(os.path.join(dirpath, d))
            if link or source.skipped(d, True):
                if left_out is not None:
                    left_out.append((arc + "/", "a symbolic link" if link else _why(d, True)))
                continue
            keep.append(d)
        dirnames[:] = keep
        for name in sorted(filenames):
            full = Path(dirpath) / name
            arc = (Path(arc_prefix) / rel / name).as_posix()
            if full.is_symlink() or source.skipped(name, False) or not full.is_file():
                if left_out is not None:
                    left_out.append((arc, _why(name, False) if not full.is_symlink() else "a symbolic link"))
                continue
            out.append((full, arc))
    return out


def _why(name: str, is_dir: bool) -> str:
    """Why seq.source leaves a file or directory of this name out of every tree."""
    if name in _WHY_SKIPPED:
        return _WHY_SKIPPED[name]
    if is_dir:
        return "a cache"
    return "the Finder's folder notes" if name == ".DS_Store" else "compiled bytecode"


def _module_root(module_name: str) -> tuple[Path, list[tuple[Path, str]], str] | None:
    """(the import root, the entry module's own files, the entry file's path in the bundle) for the handler's
    module, or None when it is installed (the image provides it)."""
    top_name = module_name.split(".", 1)[0]
    top = sys.modules.get(top_name) or importlib.import_module(top_name)
    pkg_paths = list(getattr(top, "__path__", []) or [])
    if pkg_paths:
        pkg = Path(pkg_paths[0])
        if _is_installed(pkg):
            return None
        mod = sys.modules.get(module_name) or importlib.import_module(module_name)
        entry = Path(getattr(mod, "__file__", "") or pkg / "__init__.py")
        root = pkg.resolve().parent
        return root, _walk(pkg, top_name), entry.resolve().relative_to(root).as_posix()
    file = getattr(top, "__file__", None)
    if not file:
        raise PolicyDefinitionError(f"cannot locate the source of module {top_name!r} to ship with the deploy")
    path = Path(file)
    if _is_installed(path):
        return None
    return path.resolve().parent, [(path, path.name)], path.name



def _glob(pattern: str) -> str:
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append(r"(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(r".*")
            i += 2
        elif pattern[i] == "*":
            out.append(r"[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append(r"[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return "".join(out)


def ignore_rules(folder: Path) -> list[tuple[re.Pattern, bool, bool, str]]:
    """The folder's .seqignore, as (pattern, directories only, takes back, the line): gitignore's form - a path from the
    folder (`third_party/openpi/docs`, `/notes.txt`) or a name at any depth below it (`data`, `*.bin`); a trailing / for
    directories only; * and ? within a name, ** across directories; # comments; `!` takes back what a line before it -
    or a parent folder's .seqignore - left out, though nothing inside a folder left out whole, as in git."""
    path = Path(folder) / IGNORE_FILE
    if not path.is_file():
        return []
    rules = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line == "!":
            continue
        back = line.startswith("!")
        body = line[1:] if back else line
        dir_only = body.endswith("/")
        pattern = body.rstrip("/")
        anchored = pattern.startswith("/") or "/" in pattern
        regex = ("^" if anchored else r"^(?:.*/)?") + _glob(pattern.lstrip("/")) + "$"
        rules.append((re.compile(regex), dir_only, back, line))
    return rules


def _decided(rel: str, is_dir: bool, layers: list[tuple[str, list]], why: str | None = None) -> str | None:
    """Why `rel` - a path from the folder's top - is left out, or None when it is kept: `why` before any rule (a .env
    file's), then every .seqignore above it, the top's first (`layers`: (its folder, its rules)), the last line to match
    deciding - a line leaves out, a `!` line takes back."""
    for folder, rules in layers:
        if folder and not rel.startswith(folder + "/"):
            continue
        sub = rel[len(folder) + 1:] if folder else rel
        for regex, dir_only, back, line in rules:
            if (is_dir or not dir_only) and regex.match(sub):
                why = None if back else f"{folder + '/' if folder else ''}{IGNORE_FILE}: {line}"
    return why


def _is_env(name: str) -> bool:
    return name == ".env" or name.startswith(".env.")



def _folder_files(root: Path, official: set[str]) -> tuple[list[tuple[Path, str]], list[tuple[str, str]]]:
    """Every file of the folder the snapshot keeps, as (path, path in the folder), and what it leaves out, with why."""
    files: list[tuple[Path, str]] = []
    left: list[tuple[str, str]] = []
    layers_of: dict[str, list[tuple[str, list]]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath).relative_to(root).as_posix()
        here = "" if here == "." else here
        own = ignore_rules(Path(dirpath))
        layers = (layers_of[here.rpartition("/")[0]] if here else []) + ([(here, own)] if own else [])
        layers_of[here] = layers
        keep = []
        for d in sorted(dirnames):
            rel = f"{here}/{d}" if here else d
            why = None
            if os.path.islink(os.path.join(dirpath, d)):
                why = "a symbolic link"
            elif rel in official:
                why = "installed from its official package, as published"
            elif source.skipped(d, True):
                why = _why(d, True)
            elif not here and (d in _ROOT_SKIP_DIRS or d.endswith(_ROOT_SKIP_SUFFIXES)):
                why = "a virtualenv or build output at the folder's root"
            elif not here and d == SOURCE_CONTEXT_DIR:
                why = "a version's build context, as its source download writes it - not its code"
            else:
                why = _decided(rel, True, layers)
            if why:
                left.append((rel + "/", why))
            else:
                keep.append(d)
        dirnames[:] = keep
        for name in sorted(filenames):
            rel = f"{here}/{name}" if here else name
            full = Path(dirpath) / name
            why = None
            if full.is_symlink():
                why = "a symbolic link"
            elif not full.is_file():
                why = "not a regular file"
            elif source.skipped(name, False):
                why = _why(name, False)
            elif name in _WHY_SKIPPED:
                why = _WHY_SKIPPED[name]
            else:
                why = _decided(rel, False, layers, _ENV_WHY if _is_env(name) else None)
            if why:
                left.append((rel, why))
            else:
                files.append((full, rel))
    return files, left


def _inside(path: Path, root: Path) -> str | None:
    """`path`'s place in the folder, or None when it is outside it."""
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return None


def pack(handler_ref: str, *, local_files: tuple[tuple[str, str], ...] = (), python_sources: tuple[str, ...] = ()
         ) -> Snapshot:
    """The snapshot `seq deploy` uploads for `handler_ref`: the folder it was imported from, whole (seq.loading
    load_folder puts the folder first on sys.path, so the module's import root is the folder), with what the image
    declared (`local_files`: (path in the bundle, local path) from add_local_file / add_local_dir; `python_sources`:
    modules from add_local_python_source). Raises PolicyDefinitionError for what cannot be uploaded as asked: a declared
    path that is not here or that the folder's rules leave out, a changed large upstream, a module the class imported
    that the upload leaves behind, a snapshot past the size limit."""
    module_name = handler_ref.partition(":")[0]
    found = _module_root(module_name)
    if found is None:
        declared = _python_sources(python_sources) + _declared(local_files, None, [])
        bundle = _pack(declared, f"the files declared for {handler_ref!r}", _ENTRY_ADVICE) if declared else None
        return _summed(Snapshot(bundle, entry="", folder=None), declared)
    folder, _, entry = found
    states = source.check_sources(folder)
    if (refusal := source.changed_refusal(states, folder)) is not None:
        raise PolicyDefinitionError(refusal)
    snap = Snapshot(None, entry=entry, folder=folder, sources=states)
    official = {s.path for s in states if s.state == "as published"}
    files, snap.left_out = _folder_files(folder, official)
    held = {rel for _, rel in files}
    for src, local in local_files:
        rel = _inside(Path(local), folder)
        if rel is None or not Path(local).exists():
            continue
        if rel in official:
            raise PolicyDefinitionError(f"add_local_dir({rel!r}): {rel} is installed from its official package "
                                        "(third_party/SOURCES.json), so the deploy does not upload it")
        if rel == ".":
            pass
        elif Path(local).is_dir() and not any(r.startswith(rel + "/") for r in held) or \
                Path(local).is_file() and rel not in held:
            why = next((w for p, w in snap.left_out if p.rstrip("/") == rel or rel.startswith(p)), "left out")
            raise PolicyDefinitionError(f"add_local({rel!r}) names what the upload leaves out ({why}): take it out "
                                        f"of {IGNORE_FILE}, or declare another path")
        snap.src_map[src] = rel
    local_files = tuple((src, local) for src, local in local_files if src not in snap.src_map)
    files += _python_sources(python_sources)
    files += _declared(local_files, folder, snap.left_out)
    seen: set[str] = set()
    files = [f for f in files if not (f[1] in seen or seen.add(f[1]))]
    if not files:
        return snap
    _check_imports(module_name, folder, {rel for _, rel in files}, snap.left_out, python_sources)
    what = f"the folder {_shown(folder)}"
    advice = _folder_advice(files, snap, folder)
    _check_raw(files, what, advice)
    snap.bundle = _pack(files, what, advice)
    return _summed(snap, files)


_ENTRY_ADVICE = "Keep checkpoints and data out of the module's directory (use weights= or a volume)."

_OWN_PACKAGES = frozenset({"seq", "sequence_ai", "sequence_base"})


def _named_in(files: list[Path]) -> set[str]:
    """Every module an absolute import statement of `files` names, read and never run: each dotted prefix of `import
    a.b`, and of `from a.b import c` the module and what it takes from it (a submodule or a name)."""
    names: set[str] = set()
    for path in files:
        try:
            tree = ast.parse(path.read_bytes(), filename=str(path))
        except (OSError, SyntaxError, ValueError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                full = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
                full = [node.module, *(f"{node.module}.{alias.name}" for alias in node.names if alias.name != "*")]
            else:
                continue
            for dotted in full:
                parts = dotted.split(".")
                names.update(".".join(parts[:i]) for i in range(1, len(parts) + 1))
    return names


def _check_imports(module_name: str, top: Path, kept: set[str], left_out: list[tuple[str, str]],
                   shipped: tuple[str, ...] = ()) -> None:
    """Refuse an upload that leaves behind a module the entry imported here - one from outside the folder (a folder
    the author put on sys.path, a package installed from a checkout of their own) or one the folder's rules leave out:
    the worker could not import it. Only the modules first loaded while the entry module was (seq.loading.imported_with)
    count; the SDK's own and what is installed in site-packages (the image installs those) never do. One from outside
    the folder counts only when the folder's own code names it in an import statement (_named_in, over the folder's
    files that ran): what a library loads or makes as it is imported is that library's, and the worker's copy of the
    library loads or makes its own - multiprocessing names this program's main module __mp_main__ (the `seq` script),
    an older torch writes _remote_module_non_scriptable into the system's temporary directory and imports it.
    """
    from seq.loading import imported_with

    loaded = imported_with(module_name) or ()

    ran = []
    for name in loaded:
        file = getattr(sys.modules.get(name), "__file__", None)
        if file and os.path.isfile(file) and _inside(Path(file), top) is not None:
            ran.append(Path(file))
    named = _named_in(ran)
    shipped_tops = {s.split(".", 1)[0] for s in shipped}
    missing = []
    for name in loaded:
        if name.split(".", 1)[0] in _OWN_PACKAGES or name.split(".", 1)[0] in shipped_tops:
            continue
        file = getattr(sys.modules.get(name), "__file__", None)
        if not file or not os.path.isfile(file) or _is_installed(Path(file)):
            continue
        rel = _inside(Path(file), top)
        if rel is None:
            if name not in named:
                continue
            missing.append(f"{name} ({Path(file).resolve()}: outside the folder)")
        elif rel not in kept:
            why = next((w for p, w in left_out if p.rstrip("/") == rel or rel.startswith(p)), "left out")
            missing.append(f"{name} ({rel}: {why})")
    if missing:
        raise PolicyDefinitionError(
            f"the entry imports {len(missing)} module{'s' if len(missing) > 1 else ''} the upload of {_shown(top)} "
            f"leaves behind, so the deployment could not import {'them' if len(missing) > 1 else 'it'}: "
            f"{'; '.join(missing[:6])}{' and more' if len(missing) > 6 else ''}. Deploy a folder that holds "
            f"{'them' if len(missing) > 1 else 'it'}, take {'them' if len(missing) > 1 else 'it'} back with a ! line in "
            f"the {IGNORE_FILE}, ship {'them' if len(missing) > 1 else 'it'} with seq.Image.add_local_python_source, or "
            f"install {'them' if len(missing) > 1 else 'it'} in the image.")


def _dir_sizes(files: list[tuple[Path, str]]) -> dict[str, int]:
    """Each directory of the snapshot (a path from its top) and how many bytes it holds, all the way down."""
    sizes: dict[str, int] = {}
    for path, arc in files:
        size = path.stat().st_size
        parts = arc.split("/")
        for i in range(1, len(parts)):
            key = "/".join(parts[:i])
            sizes[key] = sizes.get(key, 0) + size
    return sizes


def _gitignored(top: Path) -> list[str]:
    """The folders the folder's .gitignore ignores (as paths from its top), for the advice alone; [] where git cannot
    say."""
    try:
        done = subprocess.run(["git", "-C", str(top), "ls-files", "-z", "--others", "--ignored", "--exclude-standard",
                               "--directory"], capture_output=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return []
    return [p.rstrip("/") for p in done.stdout.decode(errors="replace").split("\0") if p.endswith("/")] \
        if done.returncode == 0 else []


def _mib(n: float) -> str:
    """A size as the docs and the limits say it, in MiB: the 64 MiB ceiling read "67 MB" in decimal megabytes.
    {worker 7's std3 list B5}"""
    return f"{n / 2 ** 20:.1f} MiB"


def _folder_advice(files: list[tuple[Path, str]], snap: Snapshot, top: Path) -> str:
    """What to leave out of a folder past the limit: where most of it is not the entry's own - the lines for the
    folder's .seqignore that keep only the entry's branch of that folder - what its .gitignore ignores too (a folder in a
    git repository), and --dry-run's listing."""
    sizes, total = _dir_sizes(files), sum(p.stat().st_size for p, _ in files)
    parts = [p for p in PurePosixPath(snap.entry).parent.parts if p not in ("", ".")]
    lines = ""
    for depth in range(len(parts) - 1, -1, -1):
        folder, branch = "/".join(parts[:depth]), "/".join(parts[:depth + 1])
        held = sizes.get(folder, total) if folder else total
        if held - sizes.get(branch, 0) >= total / 2:
            here = f"{folder}/" if folder else "the folder's top"
            lines = (f" {here} holds {_mib(held)}, the entry's {branch}/ {_mib(sizes.get(branch, 0))} of "
                     f"it: the lines \"{folder + '/' if folder else '/'}*\" and \"!{'' if folder else '/'}{branch}/\" "
                     "keep only the entry's.")
            break
    ignored = sorted(((d, sizes[d]) for d in _gitignored(top) if d in sizes), key=lambda x: -x[1])[:3]
    git = (" Its .gitignore ignores " + ", ".join(f"{d}/ {_mib(n)}" for d, n in ignored) + " too.") \
        if ignored else ""
    return (f"Leave out what the deployment does not read in a {IGNORE_FILE} at {_shown(top)}, one path or pattern a "
            f"line (data/, *.bin).{lines}{git} Weights go through weights= or a volume.")


def _python_sources(names: tuple[str, ...]) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for name in names:
        try:
            files.extend(_source_files(name) or [])
        except ModuleNotFoundError:
            raise PolicyDefinitionError(f"add_local_python_source({name!r}): there is no module {name!r} here to "
                                        "ship - nothing on this machine's import path (sys.path) has that name") from None
    return files


def _source_files(name: str) -> list[tuple[Path, str]] | None:
    """What add_local_python_source(`name`) ships - a module's one file, or the whole package a dotted name is in -
    found where `import name` would find it by the import system's finders, never by running it: what it imports need
    only be in the image. None when it is installed (the image provides it). Raises ModuleNotFoundError when nothing on
    this machine's import path has that name.
"""
    top_name, *rest = name.split(".")
    spec = importlib.util.find_spec(top_name)
    if spec is None:
        raise ModuleNotFoundError(name)
    if spec.submodule_search_locations is not None:
        where = list(spec.submodule_search_locations)
        pkg = Path(where[0])
        if _is_installed(pkg):
            return None
        for part in rest:
            sub = importlib.machinery.PathFinder.find_spec(part, where)
            if sub is None:
                raise ModuleNotFoundError(name)
            where = list(sub.submodule_search_locations or [])
        return _walk(pkg, top_name)
    if rest:
        raise ModuleNotFoundError(name)
    if spec.origin == "frozen":
        return None
    if not spec.origin or not os.path.isfile(spec.origin):
        raise PolicyDefinitionError(f"cannot locate the source of module {top_name!r} to ship with the deploy")
    path = Path(spec.origin)
    return None if _is_installed(path) else [(path, path.name)]


def _declared(local_files: tuple[tuple[str, str], ...], root: Path | None,
              left_out: list[tuple[str, str]]) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for src, local in local_files:
        local_path = Path(local)
        if not local_path.exists():
            raise PolicyDefinitionError(f"add_local_file / add_local_dir: {local} does not exist here, so it cannot be "
                                        "shipped with the deploy")
        files.extend(_walk(local_path, src, left_out) if local_path.is_dir() else [(local_path, src)])
    return files


def _shown(root: Path) -> str:
    try:
        rel = os.path.relpath(root)
    except ValueError:
        return str(root)
    return "./" if rel == "." else (rel if rel.startswith("..") else f"./{rel}")


def _largest(files: list[tuple[Path, str]], n: int = 5) -> str:
    """The largest paths of a snapshot, a directory summed: third_party/<upstream>/ apart, anything else by its first
    part."""
    sums: dict[str, int] = {}
    for path, arc in files:
        parts = arc.split("/")
        key = "/".join(parts[:2]) + "/" if parts[0] == "third_party" and len(parts) > 2 else \
            (parts[0] + "/" if len(parts) > 1 else parts[0])
        sums[key] = sums.get(key, 0) + path.stat().st_size
    top = sorted(sums.items(), key=lambda kv: -kv[1])[:n]
    return ", ".join(f"{k} {_mib(v)}" for k, v in top)


def _check_raw(files: list[tuple[Path, str]], what: str, advice: str) -> None:
    total = sum(p.stat().st_size for p, _ in files)
    if total > _MAX_RAW_BYTES:
        raise PolicyDefinitionError(f"{what} is {_mib(total)} — too large to upload with a deploy (limit "
                                    f"{_MAX_RAW_BYTES / 2 ** 20:.0f} MiB, {MAX_CODE_BUNDLE_BYTES / 2 ** 20:.0f} MiB once "
                                    f"compressed). Its largest: {_largest(files)}. {advice}")


def _summed(snap: Snapshot, files: list[tuple[Path, str]]) -> Snapshot:
    snap.files = len(files)
    snap.raw_bytes = sum(p.stat().st_size for p, _ in files)
    snap.tree_sha256 = source.files_sha256((arc, p.stat().st_size, source.file_sha256(p)) for p, arc in files) \
        if files else None
    return snap


def with_sources(image, src_map: dict[str, str]):
    """`image` (an ImageSpec) with each add_local step whose path the folder holds pointing at the folder's copy."""
    if not src_map or image is None:
        return image
    steps = []
    for step in image.steps:
        add = getattr(step, "add_local", None)
        if add is not None and add.src in src_map:
            step = step.model_copy(update={"add_local": add.model_copy(update={"src": src_map[add.src]})})
        steps.append(step)
    return image.model_copy(update={"steps": steps})




_CONTEXT_SKIP_DIRS = frozenset({".git", ".hg", ".svn", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache",
                                ".ruff_cache", ".ipynb_checkpoints"})


def pack_dir(root: str | Path) -> CodeBundle:
    """A Dockerfile's build context: every file under `root` as the bundle the build unpacks for its COPY / ADD.
    """
    root = Path(root)
    files: list[tuple[Path, str]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)

        dirnames[:] = sorted(d for d in dirnames
                             if d not in _CONTEXT_SKIP_DIRS and not (rel == Path(".") and d == SOURCE_CONTEXT_DIR))
        for name in sorted(filenames):
            full = Path(dirpath) / name
            if full.is_symlink() or not full.is_file():
                continue
            files.append((full, str(rel / name)))
    total = sum(p.stat().st_size for p, _ in files)
    if total > _MAX_RAW_BYTES:
        raise PolicyDefinitionError(
            f"the build context {str(root)!r} is {_mib(total)} — too large to ship with a deploy. Narrow "
            "it to what the Dockerfile copies (weights go through weights= or a volume).")
    return _pack(files, f"the build context {str(root)!r}", "Narrow it to what the Dockerfile copies.")


def _pack(files: list[tuple[Path, str]], what: str, advice: str) -> CodeBundle:
    """A deterministic gzip'd tar of `files` (sorted entries, zeroed metadata), within the bundle size limit."""
    buf = io.BytesIO()

    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for path, arcname in sorted(files, key=lambda f: f[1]):
                info = tarfile.TarInfo(arcname)
                info.size = path.stat().st_size
                info.mode = 0o644
                info.mtime = 0
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                with path.open("rb") as fh:
                    tar.addfile(info, fh)
    raw = buf.getvalue()
    if len(raw) > MAX_CODE_BUNDLE_BYTES:
        raise PolicyDefinitionError(
            f"{what} is {_mib(len(raw))} compressed (limit {MAX_CODE_BUNDLE_BYTES / 2 ** 20:.0f} MiB). Its largest: "
            f"{_largest(files)}. {advice}")
    return CodeBundle.from_bytes(raw)


def bundle_listing(bundle: CodeBundle) -> list[str]:
    """The archive's file names — for the human-readable deploy echo."""
    with tarfile.open(fileobj=io.BytesIO(bundle.raw()), mode="r:gz") as tar:
        return [m.name for m in tar.getmembers() if m.isfile()]
