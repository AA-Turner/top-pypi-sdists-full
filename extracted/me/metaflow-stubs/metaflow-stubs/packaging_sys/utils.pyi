######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39                                                                                #
# Generated on 2026-09-02T21:19:46.735804                                                            #
######################################################################################################

from __future__ import annotations

import typing


def walk(root: str, exclude_hidden: bool = True, file_filter: typing.Union[typing.Callable[[str], bool], None] = None, exclude_tl_dirs: typing.Union[typing.List[str], None] = None) -> typing.Generator[typing.Tuple[str, str], None, None]:
    ...

def suffix_filter(suffixes: typing.List[str]) -> typing.Callable[[str], bool]:
    """
    Returns a filter function that checks if a file ends with any of the given suffixes.
    """
    ...

def with_dir(new_dir):
    ...

