# -*- coding: utf-8 -*-

import typing
from dataclasses import dataclass
from pprint import pprint

from serpyco import Serializer


@dataclass
class Point(object):
    x: float
    y: float


serializer = Serializer(Point)

pprint(serializer.json_schema())
o: Point = serializer.load({"x": 3.14, "y": 1.5})
pprint(o)
try:
    serializer.load({"x": 3.14, "y": "wrong"})
except Exception as ex:
    pprint(ex)

om: typing.List[Point] = serializer.load(
    [{"x": 1, "y": 2}, {"x": 2, "y": 3}], many=True
)
pprint(om)

d: typing.Dict[str, typing.Any] = serializer.dump(Point(x=3.14, y=1.5))
pprint(d)

dm: typing.List[typing.Dict[str, typing.Any]] = serializer.dump(
    [Point(x=1, y=2), Point(x=2, y=3)], many=True
)
pprint(dm)

try:
    serializer.dump(Point(x=3.14, y="wrong"), validate=True)
except Exception as ex:
    pprint(ex)
