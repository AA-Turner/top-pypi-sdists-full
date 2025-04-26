# Copyright (C) 2022 Martin Fischer <martin@push-f.com>
# Copyright (C) 2023-2024 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

from typing import Set, TypeVar, Type, Any, Optional, Dict, List, Tuple, Callable, _SpecialForm

from .dataloader import Loader
from .datadumper import Dumper

# Load and dump take **kwargs for backwards-compatibility.
# This interface file intentionally omits **kwargs so that
# typos can be caught by static type checkers.
# If you want to extend Loader or Dumper in a type-safe manner
# you should subclass them (instead of using **kwargs).

__all__ = [
    'dataloader',
    'load',
    'datadumper',
    'dump',
    'typechecks',
]

T = TypeVar('T')

def load(
    value: Any,
    type_: Type[T] | _SpecialForm,
    basictypes: Set[Type[Any]] = ...,
    basiccast: bool = ...,
    failonextra: bool = ...,
    raiseconditionerrors: bool = ...,
    frefs: Optional[Dict[str, Type[Any]]] = ...,
    dictequivalence: bool = ...,
    mangle_key: str = ...,
    uniondebugconflict: bool = ...,
    strconstructed: Set[Type[Any]] = ...,
    handlers: List[
        Tuple[Callable[[Any], bool], Callable[[Loader, Any, Type[Any]], Any]]
    ] = ...,
    pep563: bool = ...,
) -> T: ...

def dump(
    value: Any,
    hidedefault: bool = ...,
    isodates: bool = ...,
    raiseconditionerrors: bool = ...,
    mangle_key: str = ...,
    handlers: List[Tuple[Callable[[Any], bool], Callable[['Dumper', Any, Any], Any]|Callable[['Dumper', Any], Any]]] = ...,
    strconstructed: Set[Type[Any]] = ...,
) -> Any: ...
