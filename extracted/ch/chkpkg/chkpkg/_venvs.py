# SPDX-FileCopyrightText: (c) 2021 Arteom iG (rtmigo.github.io)
# SPDX-License-Identifier: MIT

import os
import venv
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union, Optional


class VenvPaths:
    def __init__(self, venv_dir: Union[Path, str]):
        self.venv_dir = Path(venv_dir)

    @staticmethod
    def _find(*args: Path) -> Path:
        for p in args:
            if p.exists():
                return p
        raise FileNotFoundError

    @property
    def executable(self):
        return self._find(self.venv_dir / 'bin' / 'python',
                          self.venv_dir / 'Scripts' / 'python.exe')

    @property
    def windows_cmdexe_activate(self):
        # https://docs.python.org/3/library/venv.html
        return self._find(self.venv_dir / 'Scripts' / 'activate.bat')

    @property
    def posix_bash_activate(self):
        # https://docs.python.org/3/library/venv.html
        return self._find(self.venv_dir / 'bin' / 'activate')


class TempVenv:
    """Creates virtual environment in a temporary directory.
    Removes the directory and the environment when `cleanup` is called.
    Can be used as context manager:

    with TempVenv() as python_exe:
        run([python_exe, '-m', 'module'])
    """

    def __init__(self):
        self._temp_dir: Optional[TemporaryDirectory] = None
        self._executable = None

    @property
    def venv_dir_str(self) -> str:
        if self._temp_dir is None:
            raise Exception("No temp dir name. Did you call __enter__?")
        return self._temp_dir.name

    @property
    def paths(self) -> VenvPaths:
        if self._temp_dir is None:
            raise Exception("No temp dir name. Did you call __enter__?")
        return VenvPaths(self._temp_dir.name)

    def create(self):
        self._temp_dir = TemporaryDirectory()
        assert os.path.exists(self.venv_dir_str)
        assert os.path.isdir(self.venv_dir_str)
        print(f"Initializing venv in {self.venv_dir_str}")
        venv.create(env_dir=self.venv_dir_str, with_pip=True, clear=True)

    def cleanup(self):
        print(f"Removing temp venv dir {self._temp_dir.name}")
        self._temp_dir.cleanup()

    def __enter__(self) -> str:
        self.create()
        return str(self.paths.executable)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
