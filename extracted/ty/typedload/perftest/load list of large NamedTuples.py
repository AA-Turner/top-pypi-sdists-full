# typedload
# Copyright (C) 2021-2024 Salvo "LtWorf" Tomaselli
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

from typing import List, NamedTuple
import sys

from common import timeit, raised



class Child(NamedTuple):
    a: int = 1
    b: int = 1
    c: int = 1
    d: int = 1
    e: int = 1
    f: int = 1
    g: int = 1
    h: int = 1
    j: int = 1
    k: int = 1
    l: int = 1
    m: int = 1
    n: int = 1
    o: int = 1


class Data(NamedTuple):
    data: List[Child]


if sys.argv[1] == '--typedload':
    from typedload import load
    f = lambda: load(data, Data)
elif sys.argv[1] == '--jsons':
    from jsons import load
    f = lambda: load(data, Data)
elif sys.argv[1] == '--pydantic2':
    import pydantic
    class ChildPy(pydantic.BaseModel):
        value: int
    class DataPy(pydantic.BaseModel):
        data: List[ChildPy]
    f = lambda: DataPy(**data)
elif sys.argv[1] == '--apischema':
    import apischema
    apischema.settings.serialization.check_type = True
    f = lambda: apischema.deserialize(Data, data)
elif sys.argv[1] == '--dataclass_json':
    from dataclasses import dataclass
    from dataclasses_json import dataclass_json

    @dataclass_json
    @dataclass
    class Child:
        value: int
    @dataclass_json
    @dataclass
    class Data:
        data: List[Child]
    f = lambda: Data.from_dict(data)

data = {'data': [{} for i in range(30)]}
assert f().data[1].a == 1

data = {'data': [{'a': 'qwe'} for i in range(30)]}
assert raised(f)

data = {'data': [{} for i in range(900000)]}
print(timeit(f))

