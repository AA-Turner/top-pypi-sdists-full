"""Package-installed SDK source and its locked dependencies for managed worker images."""

import tomllib
from pathlib import Path

import labqoat

from labqoat.compute.context_files import ContextFiles
from labqoat.compute.images.input_tree import InputTree


class RuntimeBundle:
    """Capture the installed SDK independently of the submitting repository layout."""

    @staticmethod
    def source() -> InputTree:
        """Snapshot executable SDK modules and package resources, excluding bytecode and caches."""
        root = Path(labqoat.__file__).parent
        files = ContextFiles.directory(root, ("compute/images/runtime_metadata",))
        tree = InputTree.capture({f"labqoat/{name}": path for name, path in files.items()}, root=root)
        return InputTree(tuple(sorted((*tree.entries, *RuntimeBundle._distribution()))))

    @staticmethod
    def metadata() -> InputTree:
        """Capture locked dependencies with stable readme metadata independent of documentation edits."""
        source = RuntimeBundle._project()
        metadata = InputTree.capture({name: source / name for name in ("pyproject.toml", "uv.lock")}, root=source)
        return InputTree((("README.md", b"", 0o644), *metadata.entries))

    @staticmethod
    def _project() -> Path:
        """Prefer metadata packaged with an installed SDK over an editable checkout's project files."""
        root = Path(labqoat.__file__).parent
        packaged = root / "compute" / "images" / "runtime_metadata"
        return packaged if packaged.is_dir() else root.parent.parent

    @staticmethod
    def _distribution() -> tuple[tuple[str, bytes, int], ...]:
        """Give the source-only worker SDK the distribution metadata importlib.metadata expects."""
        pyproject = RuntimeBundle._project() / "pyproject.toml"
        if not pyproject.is_file():
            return ()
        project = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]
        name, version = project["name"], project["version"]
        metadata = f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n".encode()
        return ((f"{name}-{version}.dist-info/METADATA", metadata, 0o644),)
