from collections.abc import Sequence
from typing import Literal, Self


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int): ...
    def __add__(self, other: Self) -> Self: ...
    def __radd__(self, other: Self) -> Self: ...
    def __sub__(self, other: Self) -> Self: ...
    def __rsub__(self, other: Self) -> Self: ...
    def midpoint(self, other: Self) -> Self: ...


class BoundingBox:
    top: int
    right: int
    bottom: int
    left: int
    center: Point
    top_right: Point
    top_center: Point
    top_left: Point
    center_left: Point
    center_right: Point
    bottom_right: Point
    bottom_center: Point
    bottom_left: Point

    def __init__(self, top: int, right: int, bottom: int, left: int): ...
    def __add__(self, other: Point | Self) -> Self: ...
    def __contains__(self, other: Point | Self) -> bool: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @staticmethod
    def wrap(objs: Sequence[PixelGroup | Pixel | TextPath | Box]) -> Self: ...
    def duplicate_shifted(self, position: Point | tuple[int, int]) -> Self: ...


class PixelGroup:
    pixels: list[Pixel]
    position: Point
    style: Style
    weight: int

    def __init__(
        self,
        pixels: list[Pixel],
        position: Point | tuple[int, int] | None = None,
        style: str | None = None,
        weight: int | None = None,
    ): ...
    def __getitem__(self, index: int) -> Pixel: ...
    def __setitem__(self, index: int, pixel: Pixel) -> None: ...
    @property
    def bbox(self) -> BoundingBox: ...
    def duplicate(self, position: Point | tuple[int, int] | None = None) -> Self: ...
    def duplicate_shifted(self, position: Point | tuple[int, int]) -> Self: ...


class Pixel:
    character: str
    position: Point
    style: Style
    weight: int

    def __init__(
        self,
        character: str,
        position: Point | tuple[int, int] | None = None,
        style: str | None = None,
        *,
        weight: int | None = None,
    ): ...
    def duplicate(self, position: Point | tuple[int, int] | None = None) -> Self: ...
    def duplicate_shifted(self, position: Point | tuple[int, int]) -> Self: ...


class Style:
    def __init__(self, style: str): ...
    def __add__(self, other: str | Self) -> Self: ...
    def __call__(self, text: str) -> str: ...
    @property
    def effects(self) -> set[str]: ...
    @property
    def fg(self) -> str: ...
    def bg(self) -> str: ...


def render(objs: Sequence[PixelGroup | Pixel | TextPath | Box], default_style: str | None = None) -> str: ...
def duplicate_shifted(
    objs: Sequence[PixelGroup | Pixel | TextPath | Box], delta: Point | tuple[int, int]
) -> list[PixelGroup | Pixel | TextPath | Box]: ...


class TextPath:
    position: Point
    style: Style
    line_style: Literal['light', 'heavy', 'double']
    weight: int | None
    start_direction: Literal['up', 'right', 'down', 'left'] | None
    end_direction: Literal['up', 'right', 'down', 'left'] | None

    def __init__(
        self,
        start: Point | tuple[int, int],
        end: Point | tuple[int, int],
        position: Point | tuple[int, int] | None = None,
        style: str | None = None,
        *,
        line_style: Literal['light', 'heavy', 'double'] = 'light',
        weight: int | None = None,
        start_direction: Literal['up', 'right', 'down', 'left'] | None = None,
        end_direction: Literal['up', 'right', 'down', 'left'] | None = None,
        bend_penalty: int = 1,
        environment: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
        barriers: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
        paths: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
        bbox: BoundingBox | tuple[int, int, int, int] | None = None,
    ) -> Self: ...
    @property
    def cost(self) -> int: ...
    @property
    def bbox(self) -> BoundingBox: ...
    def duplicate(self, position: Point | tuple[int, int] | None = None) -> Self: ...
    def duplicate_shifted(self, position: Point | tuple[int, int]) -> Self: ...


def multipath(
    starts: Sequence[Point | tuple[int, int]],
    ends: Sequence[Point | tuple[int, int]],
    position: Point | tuple[int, int] | None = None,
    style: str | None = None,
    *,
    line_style: Literal['light', 'heavy', 'double'] = 'light',
    weight: int | None = None,
    start_directions: Sequence[Literal['up', 'right', 'down', 'left'] | None] | None = None,
    end_directions: Sequence[Literal['up', 'right', 'down', 'left'] | None] | None = None,
    bend_penalty: int = 1,
    environment: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
    barriers: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
    paths: Sequence[PixelGroup | Pixel | TextPath | Box] | None = None,
    bbox: BoundingBox | tuple[int, int, int, int] | None = None,
    optimize: bool = False,
) -> list[TextPath]: ...


def arrow(fmt: str) -> str: ...
def text(
    text: str, position: Point | tuple[int, int] | None = None, style: str | None = None, weight: int | None = None
) -> str: ...


class Box:
    text: str
    position: Point
    width: int
    height: int
    style: Style
    border_style: Style
    line_style: Literal['light', 'heavy', 'double'] | None
    weight: int | None
    padding: tuple[int, int, int, int] | None
    padding_style: Style
    align: Literal['top', 'center', 'bottom']
    justify: Literal['right', 'center', 'left']
    truncate_string: str | None
    transparent: bool
    transparent_padding: bool

    def __init__(
        self,
        text: str = '',
        position: Point | tuple[int, int] | None = None,
        width: int = 0,
        height: int = 0,
        style: str | None = None,
        *,
        border_style: str | None = None,
        line_style: Literal['light', 'heavy', 'double'] | None = 'light',
        weight: int | None = 1,
        padding: tuple[int, int, int, int] | None = None,
        padding_style: str | None = None,
        align: Literal['top', 'center', 'bottom'] = 'top',
        justify: Literal['right', 'center', 'left'] = 'left',
        truncate_string: str | None = None,
        transparent: bool = False,
        transparent_padding: bool = False,
    ) -> Self: ...
    @property
    def bbox(self) -> BoundingBox: ...
    @property
    def text_bbox(self) -> BoundingBox: ...
    def duplicate(self, position: Point | tuple[int, int] | None = None) -> Self: ...
    def duplicate_shifted(self, position: Point | tuple[int, int]) -> Self: ...


__all__ = [
    'BoundingBox',
    'Box',
    'Pixel',
    'PixelGroup',
    'Point',
    'Style',
    'TextPath',
    'arrow',
    'duplicate_shifted',
    'multipath',
    'render',
    'text',
]
