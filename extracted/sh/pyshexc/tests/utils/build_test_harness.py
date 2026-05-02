import pytest
import sys
from typing import Callable, Generator, Any

import os
import requests


class ValidationTestConfig:
    repo_url: str = None
    file_suffix: str = None  # file suffix (e.g. ".shex")
    start_at: str | None = ""  # Start at or after this
    skip: dict[str, str] = dict()  # Filename / reason arra
    validation_function: Callable[[str], bool] = None
    single_file: bool = False  # True means process exactly one file

    @staticmethod
    def enumerate_http_files(url) -> Generator[tuple[str, str], Any, None]:
        resp = requests.get(url)
        if resp.ok:
            for f in resp.json():
                yield f['name'], f['download_url']
        else:
            print("Error {}: {}".format(resp.status_code, resp.reason), file=sys.stderr)

    @staticmethod
    def enumerate_directory(dir_) -> Generator[tuple[str, str], Any, None]:
        for fname in os.listdir(dir_):
            fpath = os.path.join(dir_, fname)
            if os.path.isfile(fpath):
                yield fname, fpath

    @classmethod
    def get_files(cls):
        if ':' in cls.repo_url:
            return cls.enumerate_http_files(cls.repo_url)
        return cls.enumerate_directory(cls.repo_url)

    @classmethod
    def build_test_harness(cls):
        started = not bool(cls.start_at)
        cases = []
        files = (cls.enumerate_http_files(cls.repo_url) if ':' in cls.repo_url
                 else cls.enumerate_directory(cls.repo_url))
        for fname, fpath in files:
            if fname.endswith(cls.file_suffix):
                if started or fname.startswith(cls.start_at):
                    if fname not in cls.skip:
                        started = True
                        cases.append(pytest.param(fpath, id=fname.rsplit('.', 1)[0]))
                        if cls.single_file:
                            break
                    else:
                        print(f"***** Skipped: {fname} - {cls.skip[fname]}")
        return cases
