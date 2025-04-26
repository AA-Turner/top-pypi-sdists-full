# -*- coding: utf-8 -*-

import typing as T

from .sentinel import NOTHING

def resolve_kwargs(
    _mapper: T.Optional[T.Dict[str, str]] = None,
    **kwargs,
) -> dict:
    if _mapper is None:  # pragma: no cover
        _mapper = dict()
    return {
        _mapper.get(key, key): value
        for key, value in kwargs.items()
        if value is not NOTHING
    }
