#!/usr/bin/env python


from provide_dir import version
from datetime import date
from pathlib import Path
from typing import Callable
from typing import Optional


__author__ = "Sven Siegmund"
__author_email__ = "sven.siegmund@gmail.com"
__maintainer__ = __author__
__maintainer_email__ = __author_email__
__release_date__ = date(year=2022, month=4, day=13)
__version__ = version.version
__repository__ = "https://github.com/Nagidal/provide_dir"


def core_provide_dir(directory: Path) -> bool:
    """
    Checks if `directory` already exists.
    If not, it will try to create one.
    Returns True if at least one directory had to be created
    Raises FileExistsError if the path or a subpath of it
        already exists as a file.
    """
    created_something = False
    if directory.exists() and directory.is_dir():
        pass
    else:
        while True:
            try:
                directory.mkdir()
                created_something = True
                break
            except FileNotFoundError:
                _ = provide_dir(directory.parent)
                continue
            except FileExistsError:
                raise
    return created_something


def provide_dir(path: Path, sink: Optional[Callable[[str], None]] = None) -> None:
    """
    A wrapper for `_provide_dir` which outputs information
    into the sink (usually some sort of logger, or print (partial) function)
    """
    was_created = core_provide_dir(path)
    try:
        if was_created:
            if sink:
                sink(f"{str(path)} was created")
        else:
            if sink:
                sink(f"{str(path)} already exists")
    except FileExistsError:
        # This means that the parent path to the file cannot
        # be created because a part of it already exists
        # as a file
        raise
