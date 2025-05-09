# Licensed to the LF AI & Data foundation under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, ForwardRef, Optional, Union

from typing_extensions import get_origin
from typing_inspect import get_args, is_typevar, is_union_type


def is_type_tensor(type_: Any) -> bool:
    """Return True if type is a type Tensor or an Optional Tensor type."""
    from docarray.typing.tensor.abstract_tensor import AbstractTensor

    return isinstance(type_, type) and safe_issubclass(type_, AbstractTensor)


def is_tensor_union(type_: Any) -> bool:
    """Return True if type is a Union of type Tensors."""
    is_union = is_union_type(type_)
    if is_union is None:
        return False
    else:
        return is_union and all(
            (is_type_tensor(t) or safe_issubclass(t, type(None)))
            for t in get_args(type_)
        )


def change_cls_name(cls: type, new_name: str, scope: Optional[dict] = None) -> None:
    """Change the name of a class.

    :param cls: the class to change the name of
    :param new_name: the new name
    :param scope: the scope in which the class is defined
    """
    if scope:
        scope[new_name] = cls
    cls.__qualname__ = cls.__qualname__[: -len(cls.__name__)] + new_name
    cls.__name__ = new_name


def safe_issubclass(x: type, a_tuple: type) -> bool:
    """
    This is a modified version of the built-in 'issubclass' function to support non-class input.
    Traditional 'issubclass' calls can result in a crash if the input is non-class type (e.g. list/tuple).

    :param x: A class 'x'
    :param a_tuple: A class, or a tuple of classes.
    :return: A boolean value - 'True' if 'x' is a subclass of 'A_tuple', 'False' otherwise.
             Note that if the origin of 'x' is a list or tuple, the function immediately returns 'False'.
    """
    origin = get_origin(x)
    if origin:  # If x is a generic type like DocList[SomeDoc], get its origin
        x = origin
    if (
        (origin in (list, tuple, dict, set, Union))
        or is_typevar(x)
        or (type(x) == ForwardRef)
        or is_typevar(x)
    ):
        return False

    return isinstance(x, type) and issubclass(x, a_tuple)
