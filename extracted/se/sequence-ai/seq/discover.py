"""
The class a folder deploys: found by reading the folder's files, never by running them.

In one sentence: `seq deploy [folder]` reads each .py the folder's upload holds (seq.code_bundle's rules: what a
.seqignore leaves out is not looked at) and parses it with `ast` - only a file that names `seq` at all - → a class whose
decorator is @seq.policy, @seq.planner (deployed as a policy is), @seq.benchmark or @seq.adapter, however `seq` was imported (`import seq`, `import seq as s`,
`from seq import policy as p`) - or to which its module applies one by hand (`Model = seq.policy(...)(Model)`), a class
of its own or one it imports by name (`from awomo.policy import Awomo` → `seq.policy(...)(Awomo)`: the one file that
declares a class left as it is) - is a candidate, named by its decorator's name= when that is a plain string and by
the name the file holds the class by else, and imported by the path in the folder of the file that applies it
(policy/OpenWAM/model.py → policy.OpenWAM.model) → one policy or benchmark is the one deployed - an adapter beside it
is not what the folder deploys - and of several, `--name` picks.

WHY by reading: importing every module of a folder to find its classes runs every script it holds, and the class to
deploy is known from its decorator before anything runs.

"""
from __future__ import annotations

import ast
import keyword
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from seq.errors import SeqAuthoringError

KINDS = ("policy", "benchmark", "adapter")


_DEPLOYS_AS = {"policy": "policy", "planner": "policy", "benchmark": "benchmark", "adapter": "adapter"}


@dataclass(frozen=True)
class Found:
    """One decorated class of the folder: its decorator's kind (policy, planner, benchmark or adapter), its name (name=
    or the class name), and where it is."""
    kind: str
    name: str
    module: str
    qualname: str
    path: str
    importable: str | None = None
    name_unreadable: bool = False

    @property
    def ref(self) -> str:
        return f"{self.module}:{self.qualname}" if self.module else f"{self.path}:{self.qualname}"

    @property
    def deploys_as(self) -> str:
        """The kind it is deployed as: a planner's a policy's."""
        return _DEPLOYS_AS[self.kind]


def module_of(path: str) -> tuple[str, str | None]:
    """The module a file of the folder is imported as (`a/b/c.py` → `a.b.c`, `a/b/__init__.py` → `a.b`), and None - or
    "", and why not: a folder or file name that is no Python name."""
    parts = list(PurePosixPath(path).with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    if not parts:
        return "", "the folder's own __init__.py is no module of it"
    bad = [p for p in parts if not p.isidentifier() or keyword.iskeyword(p)]
    if bad:
        return "", f"{bad[0]!r} is no Python name, so it cannot be imported: rename it"
    return ".".join(parts), None


def shown(root: str | Path, path: str) -> str:
    """`path`, a file of the folder at `root`, as the person who ran the command holds it: from where it runs
    (`seq deploy my-x` → my-x/policy.py, `seq deploy` → policy.py), else whole - what they can open or delete as said.
    """
    full = Path(root).resolve() / path
    try:
        return full.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return str(full)


def _names_of_seq(tree: ast.Module) -> tuple[set[str], dict[str, str]]:
    """The names `seq` is bound to in a module, and the decorators imported from it by name ({local name: kind})."""
    modules, kinds = set(), {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules |= {a.asname or a.name for a in node.names if a.name == "seq"}
        elif isinstance(node, ast.ImportFrom) and node.module == "seq" and node.level == 0:
            kinds |= {a.asname or a.name: a.name for a in node.names if a.name in _DEPLOYS_AS}
    return modules, kinds


def _kind_and_name(dec: ast.expr, modules: set[str], kinds: dict[str, str]) -> tuple[str, str | None, bool] | None:
    """(kind, the name= it declares when a plain string else None, whether a name= was given but is not a plain string)
    of a decorator of a class to deploy, else None. A non-plain-string name= (an f-string, a variable) cannot be read
    without running the file, which deploy does not do, so the class is deployed by its class name - and the refusal
    says so when --name then names nothing."""
    call = dec if isinstance(dec, ast.Call) else None
    func = call.func if call else dec
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id in modules \
            and func.attr in _DEPLOYS_AS:
        kind = func.attr
    elif isinstance(func, ast.Name) and func.id in kinds:
        kind = kinds[func.id]
    else:
        return None
    name_kw = next((k for k in (call.keywords if call else ()) if k.arg == "name"), None)
    literal = isinstance(getattr(name_kw, "value", None), ast.Constant) and isinstance(name_kw.value.value, str)
    return kind, (name_kw.value.value if literal else None), name_kw is not None and not literal


def files_of(root: Path) -> list[tuple[Path, str]]:
    """The files of the folder its classes are looked for in: what its upload holds (seq.code_bundle's rules), less each
    large upstream its template names - never uploaded as published, refused when changed - so none of those is read."""
    from seq import code_bundle, source

    upstreams = {f"third_party/{s.name}" for s in source.read_sources(root)}
    return code_bundle._folder_files(root, upstreams)[0]


def find(files: list[tuple[Path, str]]) -> tuple[list[Found], int]:
    """The decorated classes of `files` - (path, path in the folder), what the upload holds - and how many .py were
    read. A file that does not parse is not one: the import of the one chosen says what is wrong with its own."""
    found: list[Found] = []
    read = 0
    for path, rel in sorted(files, key=lambda f: f[1]):
        if not rel.endswith(".py"):
            continue
        read += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "seq" not in text:
            continue
        try:
            tree = ast.parse(text, filename=rel)
        except SyntaxError:
            continue
        modules, kinds = _names_of_seq(tree)
        if not (modules or kinds):
            continue
        module, why = module_of(rel)
        classes = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}


        imported = {a.asname or a.name for node in tree.body
                    if isinstance(node, ast.ImportFrom) and node.module != "seq" for a in node.names if a.name != "*"}
        seen: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for dec in node.decorator_list:
                    got = _kind_and_name(dec, modules, kinds)
                    if got:
                        found.append(Found(got[0], got[1] or node.name, module, node.name, rel, why,
                                           name_unreadable=got[2]))
                        seen.add(node.name)
                        break
                continue




            call = node.value if isinstance(node, (ast.Assign, ast.Expr)) else None
            if not (isinstance(call, ast.Call) and len(call.args) == 1 and not call.keywords
                    and isinstance(call.args[0], ast.Name) and call.args[0].id in (classes | imported) - seen):
                continue
            got = _kind_and_name(call.func, modules, kinds)
            if got:
                target = call.args[0].id
                found.append(Found(got[0], got[1] or target, module, target, rel, why, name_unreadable=got[2]))
                seen.add(target)
    return found, read


def table(found: list[Found]) -> str:
    """The candidates, one a line: kind, name, module:Class."""
    width = max((len(f.name) for f in found), default=4)
    return "\n".join(f"  {f.kind:9}  {f.name:{width}}  {f.ref}" for f in found)


def choose(found: list[Found], name: str | None, folder: str, read: int) -> Found:
    """The class the folder deploys: the one `name` names (name= or the class name), else its only policy or benchmark
    - an adapter beside one is not what it deploys - else its only adapter. Raises SeqAuthoringError, listing them,
    when there is none or no telling which."""
    if not found:
        raise SeqAuthoringError(f"{folder} holds no class decorated @seq.policy, @seq.planner, @seq.benchmark or "
                                f"@seq.adapter (read {read} .py file{'' if read == 1 else 's'} it uploads)")
    if name is not None:
        named = [f for f in found if f.name == name] or [f for f in found if f.qualname == name]
        if len(named) == 1:
            return _importable(named[0], folder)
        if len(found) == 1:
            return _importable(found[0], folder)
        why = "none of them is" if not named else f"{len(named)} of them are"
        note = ("\n(a name= that is not a plain string - an f-string, or a variable - is not read: deploy reads your "
                "files without running them, so a class with one is listed above by its class name. Write its name as "
                "a literal string.)" if not named and any(f.name_unreadable for f in found) else "")
        raise SeqAuthoringError(f"{folder} holds {len(found)} classes to deploy and {why} named {name!r}:\n"
                                f"{table(found)}{note}\npick one with --name")
    runnable = [f for f in found if f.kind != "adapter"]
    pool = runnable or found
    if len(pool) == 1:
        return _importable(pool[0], folder)
    raise SeqAuthoringError(f"{folder} holds {len(pool)} classes to deploy:\n{table(found)}\npick one with --name")


def _importable(found: Found, folder: str) -> Found:
    if found.importable:
        raise SeqAuthoringError(f"{found.name} ({shown(folder, found.path)}): {found.importable}")
    return found
