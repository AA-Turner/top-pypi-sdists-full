# arpakit

import logging
import os
import shutil
import uuid
from typing import Optional, Union, Iterator

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_str_util import none_if_blank

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class FileStorageInDir:

    def __init__(self, dirpath: str):
        if not isinstance(dirpath, str):
            raise TypeError("not isinstance(dirpath, str)")
        self.dirpath = os.path.abspath(dirpath)
        self._logger = logging.getLogger(self.__class__.__name__)

    def __str__(self) -> str:
        return self.dirpath

    def __repr__(self) -> str:
        return self.dirpath

    def __len__(self) -> int:
        return len(os.listdir(self.dirpath))

    def __iter__(self) -> Iterator[str]:
        self.init()
        for path in self.get_paths():
            yield path

    def init(self):
        if not os.path.exists(self.dirpath):
            os.makedirs(self.dirpath, exist_ok=True)

    def reinit(self):
        if os.path.exists(self.dirpath):
            shutil.rmtree(self.dirpath)
        self.init()

    def get_paths(self) -> list[str]:
        return [os.path.join(self.dirpath, path) for path in os.listdir(self.dirpath)]

    def generate_filepath(
            self,
            *,
            filename: Optional[str] = None,
            file_extension: Optional[str] = None,
            content_to_write: Optional[Union[str, bytes]] = None,
            create: bool = False,
            raise_if_exists: bool = True,
            add_datetime_in_filename: bool = False
    ) -> str:
        self.init()

        filename = none_if_blank(filename)

        if filename is not None:
            if add_datetime_in_filename:
                filename = f"{now_utc_dt().isoformat()}--{filename}"
            if file_extension is not None:
                filename += f".{file_extension}"
        else:
            filename = str(uuid.uuid4())
            if add_datetime_in_filename:
                filename = f"{now_utc_dt().isoformat()}--{filename}"
            if file_extension is not None:
                filename += f".{file_extension}"
            while filename in os.listdir(self.dirpath):
                filename = str(uuid.uuid4())
                if file_extension is not None:
                    filename += f".{file_extension}"

        if raise_if_exists and filename in os.listdir(self.dirpath):
            raise ValueError(f"file ({filename}) already exists")

        filepath = os.path.join(self.dirpath, filename)

        if create is True:
            content_to_write = ""

        if isinstance(content_to_write, str):
            content_to_write = content_to_write.encode()
        if isinstance(content_to_write, bytes):
            with open(filepath, mode="wb") as f:
                f.write(content_to_write)

        return filepath

    def generate_dirpath(
            self, *, dirname: Optional[str] = None, create: bool = True, raise_if_exists: bool = True
    ) -> str:
        self.init()

        if dirname is None:
            dirname = str(uuid.uuid4())
            while dirname in os.listdir(self.dirpath):
                dirname = str(uuid.uuid4())

        if raise_if_exists and dirname in os.listdir(self.dirpath):
            raise ValueError(f"dir ({dirname}) already exists")

        dirpath = os.path.join(self.dirpath, dirname)

        if create:
            os.mkdir(dirpath)

        return dirpath

    def rm_by_filepath(self, filepath: str):
        if os.path.exists(filepath):
            os.remove(filepath)

    def rm_by_filename(self, filename: str):
        filepath = os.path.join(self.dirpath, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    def rm_by_dirpath(self, dirpath: str):
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)

    def rm_by_dirname(self, dirname: str):
        dirpath = os.path.join(self.dirpath, dirname)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)


def __example():
    pass


if __name__ == '__main__':
    __example()
