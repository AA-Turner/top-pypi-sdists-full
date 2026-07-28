"""Regression guard: `ydf` and `treeple` were removed from geocif.

Both are compiled backends with no aarch64 wheels (ydf uses Bazel and cannot build
on ARM at all), so they blocked pixi/PyPI installs on Linux ARM hosts (e.g. AWS
Graviton / terrahub). They were dropped from `[project.dependencies]`, and their
model branches in `ml/trainers.py` ('oblique' → treeple, 'ydf', 'desreg' → ydf)
now raise a clear error instead of importing the missing package.

These are pure static checks (no imports/network) so they run anywhere.
"""

import pathlib
import re
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _dependency_names():
    data = tomllib.load(open(ROOT / "pyproject.toml", "rb"))
    names = []
    for dep in data["project"]["dependencies"]:
        m = re.match(r"^\s*([A-Za-z0-9._-]+)", dep)
        if m:
            names.append(m.group(1).lower())
    return names


def test_ydf_treeple_not_in_dependencies():
    names = _dependency_names()
    assert "ydf" not in names, "ydf must stay out of [project.dependencies] (no aarch64 wheel)"
    assert "treeple" not in names, "treeple must stay out of [project.dependencies] (no aarch64 wheel)"


def test_trainers_no_live_imports_of_removed_packages():
    src = (ROOT / "geocif" / "ml" / "trainers.py").read_text(encoding="utf-8")
    assert "import ydf" not in src, "ml/trainers.py must not import ydf"
    assert "from treeple" not in src, "ml/trainers.py must not import treeple"


def test_trainers_removed_model_branches_raise():
    src = (ROOT / "geocif" / "ml" / "trainers.py").read_text(encoding="utf-8")
    # each removed-model branch must be present AND followed by a raise mentioning removal
    for model in ("oblique", "ydf", "desreg"):
        m = re.search(rf'model_name == "{model}":\s*\n\s*raise (ValueError|ImportError)', src)
        assert m, f"the '{model}' branch in ml/trainers.py must raise immediately"
    assert "was removed from geocif" in src or "removed from geocif" in src
