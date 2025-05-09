"""
Implementation of :mod:`pytools.expression` and subpackages.
"""

from __future__ import annotations

import logging
from abc import ABCMeta
from collections.abc import MutableMapping
from typing import Any, Generic, TypeVar
from weakref import WeakValueDictionary

from ...api import AllTracker, inheritdoc
from ...meta import SingletonMeta
from ..base import AtomicExpression

log = logging.getLogger(__name__)


#
# Exported names
#

__all__ = [
    "Lit",
    "Id",
    "Epsilon",
]

#
# Type variables
#

T_Literal = TypeVar("T_Literal", bool, int, float, complex, str, bytes)


#
# Ensure all symbols introduced below are included in __all__
#

__tracker = AllTracker(globals())


#
# Class definitions
#


@inheritdoc(match="[see superclass]")
class Lit(AtomicExpression[T_Literal], Generic[T_Literal]):
    """
    A literal value (usually a number or string).
    """

    def __init__(self, value: T_Literal) -> None:
        """
        :param value: the literal value represented by this expression
        """
        super().__init__()
        self._value: T_Literal = value

    @property
    def value_(self) -> T_Literal:
        """[see superclass]"""
        return self._value

    @property
    def text_(self) -> str:
        """[see superclass]"""
        return repr(self.value_)


class _IdentifierMeta(ABCMeta):
    _identifiers: MutableMapping[str, Id] = WeakValueDictionary()

    def __getattr__(self, name: str) -> Id:
        if name.startswith("_") or name.endswith("_") or name == "Id":
            # we do not allow creating identifiers with leading or trailing underscores
            # we also disallow "Id" to avoid a compatibility issue with sphinx
            raise AttributeError(name)

        identifier = _IdentifierMeta._identifiers.get(name, None)
        if identifier is None:
            _IdentifierMeta._identifiers[name] = identifier = Id(name)

        return identifier


@inheritdoc(match="[see superclass]")
class Id(AtomicExpression[str], metaclass=_IdentifierMeta):
    """
    An identifier.

    Identifiers can be created either by

    - class instantiation: ``Id("x")``
    - attribute access: ``Id.x``

    The attribute access method will return the identical :class:`Id` instance
    for subsequent access to an attribute of the same name (stored internally using a
    weak reference dictionary).
    Creating identifiers using attribute access requires attribute names that do not
    start or end with an underscore character (``_``), otherwise an
    :class:`AttributeError` is raised.
    For compatibility reasons, attribute access does not work for the ``Id`` name.
    Evaluating ``Id.Id`` will raise an :class:`AttributeError`.
    """

    # the name of this identifier
    _name: str

    def __init__(self, name: Any) -> None:
        """
        :param name: the name of the identifier
        """
        super().__init__()
        if not isinstance(name, str):
            name = getattr(name, "__name__", None)
            if not name:
                raise TypeError(
                    "arg name must be a string, or must have attribute __name__"
                )
        self._name = name

    @property
    def value_(self) -> str:
        """[see superclass]"""
        return self._name

    @property
    def text_(self) -> str:
        """[see superclass]"""
        return self._name


class _EpsilonMeta(SingletonMeta, ABCMeta):
    pass


@inheritdoc(match="[see superclass]")
class Epsilon(AtomicExpression[None], metaclass=_EpsilonMeta):
    """
    A singleton class representing the empty expression.
    """

    @property
    def value_(self) -> None:
        """[see superclass]"""
        return None

    @property
    def text_(self) -> str:
        """[see superclass]"""
        return ""


__tracker.validate()
