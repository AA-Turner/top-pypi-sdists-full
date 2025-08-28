######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.095991                                                            #
######################################################################################################

from __future__ import annotations

import typing


def walk_without_cycles(top_root: str, exclude_dirs: typing.Optional[typing.List[str]] = None) -> typing.Generator[typing.Tuple[str, typing.List[str]], None, None]:
    ...

def walk(root: str, exclude_hidden: bool = True, file_filter: typing.Optional[typing.Callable[[str], bool]] = None, exclude_tl_dirs: typing.Optional[typing.List[str]] = None) -> typing.Generator[typing.Tuple[str, str], None, None]:
    ...

def suffix_filter(suffixes: typing.List[str]) -> typing.Callable[[str], bool]:
    """
    Returns a filter function that checks if a file ends with any of the given suffixes.
    """
    ...

def with_dir(new_dir):
    ...

