import dataclasses
import functools
import operator
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from ..settings import settings

EDIT_SNIPPET_PREFIX = "## DCA edit snippet:"


@dataclasses.dataclass(frozen=True)
class Snippet:
    path: Path
    name: str
    description: str
    code: str
    base_path: Path


def get_shared_project_paths():
    return [os.environ[k] for k in os.environ.keys() if re.search(r"^DOMINO_.+_WORKING_DIR$", k)]


def get_shared_dataset_paths():
    datasets_dir = Path(settings.domino_datasets_dir)
    if not datasets_dir.exists():
        return []
    local_dir = Path(f"{settings.domino_datasets_dir}/local")
    return [str(p) for p in datasets_dir.glob("*") if p.is_dir() and p != local_dir]


def get_shared_git_paths():
    path = settings.domino_repos_dir or settings.domino_imported_code_dir
    if not path:
        return []
    return [str(p) for p in Path(path).glob("*") if p.is_dir() and (p / "snippets").is_dir()]


def get_prefix_paths():
    return [str(p) for p in settings.domino_snippet_builtin_dir.glob("*") if p.is_dir()]


def read_snippets(sub: Path, data: str, base_path: Path) -> List[Snippet]:
    return [Snippet(Path(*sub.parts[:-1]), sub.parts[-1], "", data, base_path)]


def read_snippet_file(sub: Path, file: Path, base_path: Path) -> List[Snippet]:
    with open(file, "r") as f:
        content = f.read()

    return read_snippets(sub, content, base_path)


def flatten(nested_list: List):
    return functools.reduce(operator.iconcat, nested_list, [])


def find_snippets_in_path(path: Path) -> List[Snippet]:
    files = path.glob("**/*.py")
    base_path = path
    return flatten([read_snippet_file(file.relative_to(path), file, base_path) for file in files])


def snippet_directory(directory: Path):
    # directories under $prefix/share/domino-code-assist/snippets/<name> will not need a suffix
    if settings.domino_snippet_builtin_dir in directory.parents:
        return directory
    # all other directories will need the "snippets" suffix
    return Path(directory) / "snippets"


def find_snippets(paths: List[str]) -> List[Snippet]:
    paths_ = [snippet_directory(Path(p)) for p in paths]
    paths_ = [p for p in paths_ if p.is_dir()]
    return flatten([find_snippets_in_path(path) for path in paths_])


def snippet_list_to_map(snippets: List[Snippet]):
    snippet_map: Dict[str, Any] = {}

    for snippet in snippets:
        sub_map = snippet_map
        for part in snippet.path.parts:
            if part not in sub_map:
                sub_map[part] = {}
            sub_map = sub_map[part]
        sub_map[snippet.name] = snippet

    return snippet_map


def make_get_items(snippet_map):
    def get_items(path: List[Dict]):
        sub_map = snippet_map
        for part in path[1:]:
            sub_map = sub_map[part["id"]]

        # sort by leaf first, then by name case-insensitive alphabetically
        sorted_items = sorted(sub_map.items(), key=lambda t: ("a" if isinstance(t[1], Snippet) else "b") + t[0].lower())

        return [
            {
                "label": re.sub(".py$", "", k),
                "id": k,
                "leaf": isinstance(v, Snippet),
                "icon": "mdi-card-text-outline" if isinstance(v, Snippet) else "mdi-folder-outline",
            }
            for k, v in sorted_items
        ]

    return get_items


def make_get_content(snippet_map):
    def get_content(path: List[Dict]):
        sub_map = snippet_map
        for part in path[1:]:
            sub_map = sub_map[part["id"]]

        return sub_map

    return get_content


def get_writable_paths():
    git_paths = get_shared_git_paths()

    def is_writable(path):
        return 0 == subprocess.run(["git", "push", "--dry-run", "--force", "--no-verify"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode

    return [{"path": str(p), "writable": is_writable(p)} for p in git_paths] + [{"path": str(settings.domino_working_dir), "writable": True}]


def adjust_path(snippet_map, path: List[Dict]):
    if not path:
        return path
    new_path = path[:1]
    sub_map = snippet_map
    try:
        for part in path[1:]:
            sub_map = sub_map[part["id"]]
            new_path.append(part)
    except KeyError:
        return new_path
    return path


def make_fns():

    snippets = find_snippets(
        [
            *get_shared_project_paths(),
            *get_shared_dataset_paths(),
            *get_shared_git_paths(),
            *get_prefix_paths(),
            settings.domino_working_dir,
        ]
    )

    snippet_map = snippet_list_to_map(snippets)
    return len(snippets), make_get_items(snippet_map), make_get_content(snippet_map), functools.partial(adjust_path, snippet_map)


def save_snippet(code: str):
    if code.startswith(EDIT_SNIPPET_PREFIX):
        marker, rest = code.split("\n", 1)
        path = Path(marker.split(EDIT_SNIPPET_PREFIX)[-1].strip())
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(rest)
