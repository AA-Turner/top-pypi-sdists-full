""" Future get_args and get_origin for python 3.7 """
# Copyright 2021 MosaicML. All Rights Reserved.

# pyright: reportUnusedImport=none

# Future functions from typing for compatibility with python 3.7

import collections.abc
from typing import Any, Generic, _GenericAlias  # type: ignore


def get_args(*_, **__) -> Any:  # type: ignore
    return []


def get_origin(*_, **__) -> Any:  # type: ignore
    return []


try:
    from typing import get_args  # type: ignore pylint: disable=unused-import
except ImportError:
    # From https://github.com/python/cpython/blob/3.8/Lib/typing.py#L1292
    def get_args(tp):  # pylint: disable=function-redefined
        """Get type arguments with all substitutions performed.
        For unions, basic simplifications used by Union constructor are performed.
        Examples::
            get_args(Dict[str, int]) == (str, int)
            get_args(int) == ()
            get_args(Union[int, Union[T, int], str][int]) == (int, str)
            get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])
            get_args(Callable[[], T][int]) == ([], int)
        """
        if isinstance(tp, _GenericAlias) and not tp._special:  # pylint: disable=protected-access
            res = tp.__args__
            if get_origin(tp) is collections.abc.Callable and res[0] is not Ellipsis:
                res = (list(res[:-1]), res[-1])
            # pylint: disable=unreachable
            return res
        return ()  # pylint: enable=unreachable


try:
    from typing import get_origin  # type: ignore
except ImportError:
    # From https://github.com/python/cpython/blob/3.8/Lib/typing.py#L1271
    def get_origin(tp):  # pylint: disable=function-redefined
        """Get the unsubscripted version of a type.
        This supports generic types, Callable, Tuple, Union, Literal, Final and ClassVar.
        Return None for unsupported types. Examples::
            get_origin(Literal[42]) is Literal
            get_origin(int) is None
            get_origin(ClassVar[int]) is ClassVar
            get_origin(Generic) is Generic
            get_origin(Generic[T]) is Generic
            get_origin(Union[T, int]) is Union
            get_origin(List[Tuple[T, T]][int]) == list
        """
        if isinstance(tp, _GenericAlias):
            return tp.__origin__
        if tp is Generic:  # type: ignore
            return Generic  # type: ignore
        return None
