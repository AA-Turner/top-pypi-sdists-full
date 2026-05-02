from abc import ABC
import glob
from pathlib import Path, PurePath
from ..abstract import AbstractEvent


class FileBase(AbstractEvent, ABC):
    def __init__(self, *args, **kwargs):
        self._filenames: list[PurePath] = []
        super(FileBase, self).__init__(*args, **kwargs)

    def start(self):
        if hasattr(self, "directory"):
            d = self.mask_replacement(
                self.directory  # pylint: disable=E0203
            )  # pylint: disable=access-member-before-definition
            p = Path(d)  # pylint: disable=E0203
            if p.exists() and p.is_dir():
                self.directory = p
            else:
                self._logger.error(f"Path doesn't exists: {self.directory}")
        if hasattr(self, "destination"):
            d = self.mask_replacement(
                self.destination  # pylint: disable=E0203
            )  # pylint: disable=access-member-before-definition
            p = Path(d)  # pylint: disable=E0203
            if p.exists() and p.is_dir():
                self.destination = p
            else:
                if hasattr(self, "create_destination"):
                    self.destination.mkdir(parents=True, exist_ok=True)
                else:
                    self._logger.error(
                        f"Destination Path doesn't exists: {self.directory}"
                    )
        if hasattr(self, "filename"):
            if isinstance(self.filename, list):
                for file in self.filename:
                    fname = self.mask_replacement(file)
                    self._filenames.append(self.directory.joinpath(fname))
            elif isinstance(self.filename, PurePath):
                self._filenames.append(self.filename)
            elif isinstance(self.filename, str):
                if "*" in self.filename:
                    path = self.directory.joinpath(self.filename)
                    listing = glob.glob(str(path))  # TODO using glob from pathlib
                    for fname in listing:
                        self._filenames.append(Path(fname))
                else:
                    fname = self.mask_replacement(self.filename)
                    self._filenames.append(self.directory.joinpath(fname))
