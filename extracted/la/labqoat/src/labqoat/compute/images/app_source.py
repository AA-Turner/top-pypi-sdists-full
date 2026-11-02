"""Automatic capture of importable App modules, their sibling Python sources and small files beside them."""

from pathlib import Path
from typing import ClassVar

from labqoat.compute.context_files import ContextFiles
from labqoat.compute.images.declared_image import DeclaredImage
from labqoat.compute.images.input_tree import InputTree


class AppSource:
    """Capture registered modules under their import paths and reject overlapping roots.

    Beside the Python sources, files up to ``FILE_BYTES`` each travel too, in path order until ``TOTAL_BYTES`` or
    ``FILES``, so configuration, prompts and small data next to the code are where the code expects them. The rest
    is left out and named before launch; ``Image.add_local_dir`` adds it explicitly.
    """

    FILE_BYTES: ClassVar[int] = 1024 * 1024
    TOTAL_BYTES: ClassVar[int] = 16 * 1024 * 1024
    FILES: ClassVar[int] = 1000

    @classmethod
    def capture(cls, declarations: tuple[DeclaredImage, ...]) -> InputTree:
        """Include sibling modules and small files once, without private configuration or caches."""
        files: dict[str, Path] = {}
        for declaration in declarations:
            cls._include(files, declaration)
        return InputTree.capture(files)

    @staticmethod
    def root(source: Path, module: str) -> Path:
        """The directory a module is imported from: its file's parent, raised once per package level."""
        root = source.absolute().parent
        depth = len(module.split(".")) - 1 + (source.name == "__init__.py")
        for _index in range(depth):
            root = root.parent
        return root

    @classmethod
    def data(cls, root: Path) -> tuple[dict[str, Path], list[str]]:
        """The non-Python files that travel with the code, and the names of those left out by size."""
        kept: dict[str, Path] = {}
        left_out: list[str] = []
        total = 0
        for name, path in sorted(ContextFiles.directory(root, ("**/*.py",)).items()):
            size = path.stat().st_size
            if size > cls.FILE_BYTES or total + size > cls.TOTAL_BYTES or len(kept) >= cls.FILES:
                left_out.append(name)
                continue
            kept[name] = path
            total += size
        return kept, left_out

    @classmethod
    def _include(cls, files: dict[str, Path], declaration: DeclaredImage) -> None:
        """Locate a module's import root from its lexical filename and declared module name."""
        root = cls.root(declaration.source, declaration.module)
        selected = ContextFiles.directory(root, ("**", "!**/*.py"))
        if declaration.source.absolute() not in selected.values():
            raise ValueError("The authored function source is not a regular captured Python file")
        selected.update(cls.data(root)[0])
        for name, path in selected.items():
            if name in files and files[name] != path:
                raise ValueError(f"Conflicting App import path: {name}")
            files[name] = path
