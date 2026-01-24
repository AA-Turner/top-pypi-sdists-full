from dataclasses import dataclass
from enum import Enum, auto

from foliar import Pretty, pretty_print


class EnumA(Enum):
    PEACE = auto()
    PLANE = auto()
    SUGAR = auto()


@dataclass
class SubExampleA:
    alter: float | EnumA
    bases: dict[str, int]
    civil: tuple[bool, type]


@dataclass
class ExampleA:
    rival: str
    anger: int
    jimmy: list[SubExampleA]


example_a = ExampleA(
    rival="example",
    anger=42,
    jimmy=[
        SubExampleA(
            alter=3.14,
            bases={"one": 1, "two": 2},
            civil=(True, str),
        ),
        SubExampleA(
            alter=EnumA.SUGAR,
            bases={"three": 3, "four": 4},
            civil=(False, int),
        ),
    ],
)

# Create a Pretty instance. Use an instance over the functions for repeated use.
pretty = Pretty(indent=2)
pretty.print(example_a)

# Or, use the functions directly as a one-off.
pretty_print(example_a, indent=2)
