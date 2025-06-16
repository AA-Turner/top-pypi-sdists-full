import shutil
from pathlib import Path
from typing import Iterator


class BuildCleaner:
    """Removes "dist", "build" and "*.egg-info" directories if they did not
    exist when the object was created."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir.absolute()
        self._build_existed = self.build_dir.exists()
        self._distr_existed = self.distr_dir.exists()
        self._eggs_existed = list(self.egg_infos)

    @property
    def build_dir(self) -> Path:
        return self.project_dir / "build"

    @property
    def distr_dir(self) -> Path:
        return self.project_dir / "distr"

    @property
    def egg_infos(self) -> Iterator[Path]:
        return self.project_dir.glob('*.egg-info')

    def cleanup(self):

        def remove(p: Path):
            shutil.rmtree(p, ignore_errors=True)

        if not self._build_existed:
            remove(self.build_dir)
        if not self._distr_existed:
            remove(self.distr_dir)

        for egg in self.egg_infos:
            if egg not in self._eggs_existed:
                remove(egg)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()