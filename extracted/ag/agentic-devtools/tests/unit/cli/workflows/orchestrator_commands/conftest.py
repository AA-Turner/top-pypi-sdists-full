from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def emulate_unprivileged_symlinks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Emulate symlinks only when Windows denies them for lack of privileges."""
    simulated_symlinks: dict[Path, Path] = {}
    original_symlink_to = Path.symlink_to
    original_is_symlink = Path.is_symlink
    original_resolve = Path.resolve

    def symlink_to(path: Path, target: Path, *, target_is_directory: bool = False) -> None:
        try:
            original_symlink_to(path, target, target_is_directory=target_is_directory)
        except OSError as error:
            if getattr(error, "winerror", None) != 1314:
                raise
            simulated_symlinks[path] = target
            if target_is_directory:
                path.mkdir()
            else:
                path.touch()

    def is_symlink(path: Path) -> bool:
        return path in simulated_symlinks or original_is_symlink(path)

    def resolve(path: Path, *, strict: bool = False) -> Path:
        for link, target in simulated_symlinks.items():
            try:
                relative_path = path.relative_to(link)
            except ValueError:
                continue
            return original_resolve(target / relative_path, strict=strict)
        return original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "symlink_to", symlink_to)
    monkeypatch.setattr(Path, "is_symlink", is_symlink)
    monkeypatch.setattr(Path, "resolve", resolve)
