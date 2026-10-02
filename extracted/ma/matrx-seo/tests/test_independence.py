import ast
import tomllib
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[1]

#: Repo-root modules. None of these exist in a fresh `pip install matrx-seo`,
#: so an import of one is a package that only works inside this monorepo.
FORBIDDEN_HOST_MODULES = {"aidream", "api_management", "research", "workflows"}


def _declared_matrx_siblings() -> set[str]:
    data = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text())
    project = data["project"]
    requirements = list(project.get("dependencies", []))
    for extra in project.get("optional-dependencies", {}).values():
        requirements.extend(extra)
    names = set()
    for requirement in requirements:
        name = requirement.split(">")[0].split("<")[0].split("=")[0].split("[")[0].strip()
        if name.startswith("matrx-"):
            names.add(name.replace("-", "_"))
    return names


def _imported_top_modules() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for path in (PACKAGE_ROOT / "matrx_seo").rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module.split(".")[0]]
            else:
                continue
            for name in names:
                found.append((f"{path}:{node.lineno}", name))
    return found


def test_package_has_no_host_imports() -> None:
    """The package may never reach into the HOST.

    A DECLARED matrx-* sibling is a different thing and is allowed by the
    package doctrine — `matrx-scraper` is a hard dependency because it owns the
    ONE Brave transport every caller in the platform shares. What is forbidden
    is `aidream` and any other repo-root module: those do not exist in a fresh
    `pip install matrx-seo`, so importing one turns the package into a module
    of the app wearing a package costume.
    """
    violations = [
        f"{where}:{name}"
        for where, name in _imported_top_modules()
        if name in FORBIDDEN_HOST_MODULES
    ]
    assert violations == []


def test_every_matrx_sibling_import_is_declared() -> None:
    """An UNDECLARED sibling import resolves here and ImportErrors on a fresh
    install — the failure mode a boundary test exists to make impossible."""
    declared = _declared_matrx_siblings() | {"matrx_seo"}
    violations = [
        f"{where}:{name}"
        for where, name in _imported_top_modules()
        if name.startswith("matrx_") and name not in declared
    ]
    assert violations == [], f"undeclared sibling imports (declared: {sorted(declared)})"


def test_standalone_app_constructs_without_host() -> None:
    from matrx_seo.standalone import create_app

    app = create_app()
    routes = {getattr(route, "path", None) for route in app.routes}
    assert "/collections" in routes
