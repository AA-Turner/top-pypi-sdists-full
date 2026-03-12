######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21                                                                                #
# Generated on 2026-03-12T01:00:36.693496                                                            #
######################################################################################################

from __future__ import annotations

import typing


def walk(root: str, exclude_hidden: bool = True, file_filter: typing.Callable[[str], bool] | None = None, exclude_tl_dirs: typing.List[str] | None = None) -> typing.Generator[typing.Tuple[str, str], None, None]:
    ...

def suffix_filter(suffixes: typing.List[str]) -> typing.Callable[[str], bool]:
    """
    Returns a filter function that checks if a file ends with any of the given suffixes.
    """
    ...

def with_dir(new_dir):
    ...

