from typing import Union, Optional
from pathlib import Path, PurePath
from .abstract import AbstractStore
from ..exceptions import StoreError
from ...exceptions import FileNotFound


class FileStore(AbstractStore):
    """
    FileStore: Saving files in local filesystem.
    """

    def __init__(
        self, path: Union[str, PurePath], prefix: str, *args, **kwargs
    ) -> None:
        if isinstance(path, str):
            path = Path(path)
        if path.exists() and path.is_dir():
            self.path: PurePath = path
        else:
            raise StoreError(
                f"FileStore: directory doesn't exists: {path}"
            )
        self._prefix: str = prefix
        super().__init__(*args, **kwargs)

    def default_directory(self, directory: str):
        return self.path.joinpath(self._program, self._prefix, directory)

    def get_directory(self, directory: str, program: Optional[str] = None):
        if not program:
            program = self._program
        if isinstance(directory, PurePath):
            _dir = directory
        if ":" in directory:
            # relative directory to Storage:
            _dir = self.path.joinpath(
                program, self._prefix, directory.rsplit(":", 1)[1]
            )
        elif ".." in directory:
            # relative directory to base directory:
            _dir = self.path.joinpath(directory)
        else:
            _dir = Path(directory)
            # If not relative, try to use as is:
            if not _dir.is_absolute() or not _dir.exists():
                # Try to use instead base directory:
                _dir = self.path.joinpath(
                    program,
                    self._prefix,
                    directory
                )
            elif not _dir.exists():
                _dir = Path(directory).resolve()
        if _dir.exists() and _dir.is_dir():
            self.logger.debug(
                f"Directory: {_dir}"
            )
            return _dir
        else:
            self.logger.error(
                f"Path doesn't exists: {_dir}"
            )
            raise FileNotFound(
                f"Path doesn't exists: {_dir}"
            )
