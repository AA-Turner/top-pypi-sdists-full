from __future__ import annotations
from typing import Union

from ..expressions import BooleanExpression, NumberExpression, StringExpression

Ostr = Union[str, None]
Obool = Union[bool, None]
Oint = Union[int, None]
StringLike = Union[str, StringExpression]
BoolLike = Union[bool, BooleanExpression]
IntLike = Union[int, NumberExpression]
Ostrlike = Union[StringLike, None]
Oboolstr = Union[BooleanExpression, str, None]
Oboollike = Union[BoolLike, None]
Ointlike = Union[IntLike, None]
StringOrBoolLike = Union[StringLike, BoolLike]

__all__ = [
    'Ostr',
    'Obool',
    'Oint',
    'StringLike',
    'BoolLike',
    'IntLike',
    'Ostrlike',
    'Oboolstr',
    'Oboollike',
    'Ointlike',
    'StringOrBoolLike',
]
