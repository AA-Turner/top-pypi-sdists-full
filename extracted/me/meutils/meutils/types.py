#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : types
# @Time         : 2023/8/15 12:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from os import PathLike

from meutils.pipe import *

StrPath = Union[str, PathLike]
StrOrPath = Union[str, PathLike]
StrOrCallableStr = Union[str, Callable[..., str]]

FileContent = Union[IO[bytes], bytes, PathLike]
FileTypes = Union[
    # file (or bytes)
    FileContent,
        # (filename, file (or bytes))
    Tuple[Optional[str], FileContent],
        # (filename, file (or bytes), content_type)
    Tuple[Optional[str], FileContent, Optional[str]],
        # (filename, file (or bytes), content_type, headers)
    Tuple[Optional[str], FileContent, Optional[str], Mapping[str, str]],
]
RequestFiles = Union[Mapping[str, FileTypes], Sequence[Tuple[str, FileTypes]]]


def is_list_of_strings(lst):
    return isinstance(lst, List) and all(isinstance(item, str) for item in lst)


def is_list_of_ints(lst):
    return isinstance(lst, List) and all(isinstance(item, int) for item in lst)


