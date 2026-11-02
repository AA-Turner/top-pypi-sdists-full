from __future__ import annotations

import tomllib
from importlib.metadata import metadata, requires
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_pyproject(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def test_root_package_exposes_openai_extra_and_provider_package() -> None:
    pyproject = load_pyproject(ROOT / "pyproject.toml")

    optional_dependencies = pyproject["project"]["optional-dependencies"]
    assert optional_dependencies["openai"] == ["openai-agents>=0.18.0"]
    assert "openai-agents>=0.18.0" not in pyproject["project"]["dependencies"]

    package_roots = pyproject["tool"]["setuptools"]["packages"]["find"]["where"]
    assert "integrations/openai-agents-runta/src" in package_roots

    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert package_data["agents_runta"] == ["py.typed"]


def test_standalone_openai_provider_uses_supported_dependency_floors() -> None:
    pyproject = load_pyproject(
        ROOT / "integrations/openai-agents-runta/pyproject.toml"
    )

    assert "openai-agents>=0.18.0" in pyproject["project"]["dependencies"]
    assert "runta-sdk>=0.2.0" in pyproject["project"]["dependencies"]


def test_installed_metadata_exposes_openai_extra() -> None:
    package_metadata = metadata("runta-sdk")
    package_requires = requires("runta-sdk") or []

    assert "openai" in (package_metadata.get_all("Provides-Extra") or [])
    assert any(
        requirement == 'openai-agents>=0.18.0; extra == "openai"'
        for requirement in package_requires
    )
