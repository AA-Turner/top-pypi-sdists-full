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

from typing import List, NamedTuple, Sequence, Union
import sys

import attrs

from common import timeit


@attrs.define
class Child:
    value: int
    valor: int
    velar: int


class Data(NamedTuple):
    data: List[Child]


data = {'data': [{'velar': 44, 'valor': 11, 'value': i} for i in range(300000)]}


if sys.argv[1] == '--typedload':
    from typedload import load
    print(timeit(lambda: load(data, Data)))
elif sys.argv[1] == '--pydantic2':
    import pydantic
    ta = pydantic.TypeAdapter(data)
    print(timeit(lambda: ta.validate_python(data)))
elif sys.argv[1] == '--apischema':
    import apischema
    apischema.settings.serialization.check_type = True
    ##### apischema attrs support #####
    prev_default_object_fields = apischema.settings.default_object_fields


    def attrs_fields(cls: type) -> Union[Sequence[apischema.objects.ObjectField], None]:
        if hasattr(cls, "__attrs_attrs__"):
            return [
                apischema.objects.ObjectField(
                    a.name, a.type, required=a.default == attrs.NOTHING, default=a.default
                )
                for a in getattr(cls, "__attrs_attrs__")
            ]
        else:
            return prev_default_object_fields(cls)


    apischema.settings.default_object_fields = attrs_fields
    #####
    print(timeit(lambda: apischema.deserialize(Data, data)))
