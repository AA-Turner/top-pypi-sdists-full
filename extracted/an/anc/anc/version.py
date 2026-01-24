import toml
from pathlib import Path

def get_version():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    pyproject_content = toml.load(pyproject_path)
    return pyproject_content["tool"]["poetry"]["version"]

__version__ = get_version()
