from pathlib import Path

from fluidattacks_core.filesystem import (
    _detect_languages_in_dir,
    _optimize_exclusions,
    find_projects,
)
from fluidattacks_core.filesystem.defaults import Language


def test_optimize_exclusions() -> None:
    optimize = _optimize_exclusions

    assert optimize(["a", "a/b", "c"]) == ["a", "c"]
    assert optimize(["a/b", "a", "a/b/c"]) == ["a"]


def test_detect_languages() -> None:
    langs = _detect_languages_in_dir(["pyproject.toml"])
    assert Language.Python in langs

    langs = _detect_languages_in_dir(["package.json"])
    assert Language.JavaScript in langs

    langs = _detect_languages_in_dir(["pyproject.toml", "package.json"])
    assert {Language.Python, Language.JavaScript}.issubset(langs)


def test_find_projects_basic(tmp_path: Path) -> None:
    # Structure:
    # tmp/
    # ├── sub_py/pyproject.toml
    # └── sub_js/package.json
    sub_py = tmp_path / "sub_py"
    sub_py.mkdir()
    (sub_py / "pyproject.toml").write_text("[tool.poetry]\nname = 'demo'\n")

    sub_js = tmp_path / "sub_js"
    sub_js.mkdir()
    (sub_js / "package.json").write_text("{}")

    projects = find_projects(tmp_path)

    # first element → root directory
    root_path, root_lang, root_exclusions = projects[0]
    assert root_path == tmp_path
    assert root_lang == "root"
    assert sorted(root_exclusions) == sorted(["sub_py", "sub_js"])

    # sub-project Python
    py_entry = next(p for p in projects if p[0] == sub_py)
    assert py_entry[1] == Language.Python.value
    assert py_entry[2] == []

    # sub-project JavaScript
    js_entry = next(p for p in projects if p[0] == sub_js)
    assert js_entry[1] == Language.JavaScript.value
    assert js_entry[2] == []
