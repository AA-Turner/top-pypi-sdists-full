from __future__ import annotations

import heapq
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import Literal, Union, override

from rich.text import Text


class BorderType(Enum):
    """
    Enum representing available Unicode border styles.

    Members
    -------
    LIGHT : str
        Light single-line borders (e.g., '─', '│').
    HEAVY : str
        Heavy single-line borders (e.g., '━', '┃').
    DOUBLE : str
        Double-line borders (e.g., '═', '║').
    """

    LIGHT = "light"
    HEAVY = "heavy"
    DOUBLE = "double"


BORDER_CHARS = {
    BorderType.LIGHT: {
        "hor": "─",
        "ver": "│",
        "dl": "┐",
        "dr": "┌",
        "ul": "┘",
        "ur": "└",
        "t": "┴",
        "b": "┬",
        "l": "┤",
        "r": "├",
        "x": "┼",
    },
    BorderType.HEAVY: {
        "hor": "━",
        "ver": "┃",
        "dl": "┓",
        "dr": "┏",
        "ul": "┛",
        "ur": "┗",
        "t": "┻",
        "b": "┳",
        "l": "┫",
        "r": "┣",
        "x": "╋",
    },
    BorderType.DOUBLE: {
        "hor": "═",
        "ver": "║",
        "dl": "╗",
        "dr": "╔",
        "ul": "╝",
        "ur": "╚",
        "t": "╩",
        "b": "╦",
        "l": "╣",
        "r": "╠",
        "x": "╬",
    },
}


@dataclass
class StyledChar:
    char: str
    style: str
    x: int
    y: int


@dataclass(frozen=True)
class Left:
    """
    A horizontal segment representing movement to the left.

    Parameters
    ----------
    length : int
        Number of characters in the segment.
    """

    length: int


@dataclass(frozen=True)
class Right:
    """
    A horizontal segment representing movement to the right.

    Parameters
    ----------
    length : int
        Number of characters in the segment.
    """

    length: int


@dataclass(frozen=True)
class Up:
    """
    A vertical segment representing movement upward.

    Parameters
    ----------
    length : int
        Number of characters in the segment.
    """

    length: int


@dataclass(frozen=True)
class Down:
    """
    A vertical segment representing movement downward.

    Parameters
    ----------
    length : int
        Number of characters in the segment.
    """

    length: int


Segment = Union[Left, Right, Up, Down]


class AbstractTextObject(ABC):
    """
    Abstract base class for text objects composed of styled characters.

    Parameters
    ----------
    penalty_group : str or None, optional
        An optional identifier used to group objects for pathfinding
        cost penalization or merging purposes.

    Attributes
    ----------
    chars : list of StyledChar
        The list of characters and their styles/positions that compose the object.
    height : int
        Height of the object in character rows.
    width : int
        Width of the object in character columns.
    """

    def __init__(self, *, penalty_group: str | None = None):
        self.penalty_group = penalty_group

    @property
    @abstractmethod
    def chars(self) -> list[StyledChar]:
        """List of all styled characters in the object."""

    @property
    @abstractmethod
    def height(self) -> int:
        """Height of the object in character rows."""

    @property
    @abstractmethod
    def width(self) -> int:
        """Width of the object in character columns."""


class TextObject(AbstractTextObject):
    """
    A mutable text object composed of styled characters placed on a 2D grid.

    This class provides methods for building and manipulating 2D terminal layouts
    from strings or directional path segments. It also supports merging intersecting
    lines using Unicode box-drawing characters and rendering via Rich.

    Attributes
    ----------
    chars : list of StyledChar
        The list of styled characters in the object.
    width : int
        The width of the bounding box around all characters.
    height : int
        The height of the bounding box around all characters.
    penalty_group : str or None
        Optional group identifier used for layout cost sharing or merging behavior.
    """

    def __init__(
        self, chars: list[StyledChar] | None = None, *, penalty_group: str | None = None
    ):
        """
        Initialize a `TextObject` with an optional character list and penalty group.

        Parameters
        ----------
        chars : list of StyledChar or None, optional
            Initial list of styled characters. If None, starts empty.
        penalty_group : str or None, optional
            Optional identifier used for layout merging or pathfinding penalties.
        """
        self._chars: list[StyledChar] = chars or []
        super().__init__(penalty_group=penalty_group)

    @property
    @override
    def chars(self) -> list[StyledChar]:
        return self._chars

    def with_penalty_group(self, group: str) -> TextObject:
        """
        Assign a penalty group to this object and return self.

        Parameters
        ----------
        group : str
            Group identifier used during layout merging or pathfinding.

        Returns
        -------
        TextObject
            This instance, for method chaining.
        """
        self.penalty_group = group
        return self

    @classmethod
    def from_string(
        cls, text: str, *, style: str = "", transparent: bool = False
    ) -> TextObject:
        """
        Create a `TextObject` from a multi-line string.

        Parameters
        ----------
        text : str
            The input text to convert to styled characters.
        style : str, optional
            Rich style to apply to all characters.
        transparent : bool, optional
            If True, space characters will be omitted from the object.

        Returns
        -------
        TextObject
            A new text object containing the rendered characters.
        """
        obj = cls()
        lines = text.splitlines()
        max_width = max(len(line) for line in lines)

        for y, line in enumerate(lines):
            padded = line.ljust(max_width)
            for x, char in enumerate(padded):
                if transparent and char == " ":
                    continue
                obj.add_char(char, x, y, style=style)
        return obj

    @classmethod
    def from_path(  # noqa: PLR0912
        cls,
        segments: list[Segment],
        *,
        border_type: BorderType = BorderType.LIGHT,
        style: str = "",
        start_char: str | None = None,
        start_style: str | None = None,
        end_char: str | None = None,
        end_style: str | None = None,
    ) -> TextObject:
        """
        Create a `TextObject` from a series of directional segments.

        Parameters
        ----------
        segments : list of Segment
            Sequence of directional movements (Left, Right, Up, Down).
        border_type : BorderType, optional
            The type of border characters to use for path junctions.
        style : str, optional
            Style to apply to the path.
        start_char : str, optional
            Optional character to place at the start of the path.
        start_style : str, optional
            Optional style for the start character.
        end_char : str, optional
            Optional character to place at the end of the path.
        end_style : str, optional
            Optional style for the end character.

        Returns
        -------
        TextObject
            A new text object representing the path.
        """
        obj = cls()
        x = y = 0
        visited: list[tuple[int, int]] = []

        for seg in segments:
            if isinstance(seg, Left):
                for _ in range(seg.length):
                    visited.append((x, y))
                    x -= 1
            elif isinstance(seg, Right):
                for _ in range(seg.length):
                    visited.append((x, y))
                    x += 1
            elif isinstance(seg, Up):
                for _ in range(seg.length):
                    visited.append((x, y))
                    y -= 1
            elif isinstance(seg, Down):
                for _ in range(seg.length):
                    visited.append((x, y))
                    y += 1
        visited.append((x, y))

        for i, (x, y) in enumerate(visited):
            if i == 0 and start_char:
                obj.add_char(start_char, x, y, style=start_style or style)
            elif i == len(visited) - 1 and end_char:
                obj.add_char(end_char, x, y, style=end_style or style)
            else:
                obj.add_char("?", x, y, style=style)

        obj.merge_path_intersections(border_type)
        return obj

    def merge_path_intersections(self, border_type: BorderType):
        """
        Replace ambiguous path characters with the correct box-drawing characters
        based on neighboring path directions.

        Parameters
        ----------
        border_type : BorderType
            Border character set to use for detecting paths and joining intersections.
        """
        chars = BORDER_CHARS[border_type]
        path_map: dict[tuple[int, int], set[str]] = {}

        for c in self.chars:
            if c.char in chars.values() or c.char == "?":
                x, y = c.x, c.y
                for dx, dy, direction in [
                    (-1, 0, "left"),
                    (1, 0, "right"),
                    (0, -1, "up"),
                    (0, 1, "down"),
                ]:
                    if any((c2.x, c2.y) == (x + dx, y + dy) for c2 in self.chars):
                        path_map.setdefault((x, y), set()).add(direction)

        conn_map = {
            frozenset(["left"]): chars["hor"],
            frozenset(["right"]): chars["hor"],
            frozenset(["left", "right"]): chars["hor"],
            frozenset(["up"]): chars["ver"],
            frozenset(["down"]): chars["ver"],
            frozenset(["up", "down"]): chars["ver"],
            frozenset(["down", "right"]): chars["dr"],
            frozenset(["down", "left"]): chars["dl"],
            frozenset(["up", "right"]): chars["ur"],
            frozenset(["up", "left"]): chars["ul"],
            frozenset(["left", "right", "up"]): chars["t"],
            frozenset(["left", "right", "down"]): chars["b"],
            frozenset(["up", "down", "right"]): chars["r"],
            frozenset(["up", "down", "left"]): chars["l"],
            frozenset(["up", "down", "left", "right"]): chars["x"],
        }

        new_chars = []
        seen = {(c.x, c.y): c for c in self.chars}
        for (x, y), dirs in path_map.items():
            new_char = conn_map.get(frozenset(dirs), chars["x"])
            style = seen.get((x, y), StyledChar("", "", x, y)).style
            new_chars.append(StyledChar(new_char, style, x, y))

        self._chars = [c for c in self.chars if (c.x, c.y) not in path_map] + new_chars

    @property
    @override
    def width(self) -> int:
        if not self.chars:
            return 0
        return max(c.x for c in self.chars) - min(c.x for c in self.chars) + 1

    @property
    @override
    def height(self) -> int:
        if not self.chars:
            return 0
        return max(c.y for c in self.chars) - min(c.y for c in self.chars) + 1

    def add_char(self, char: str, x: int, y: int, *, style: str = ""):
        """
        Add a styled character at a specific location.

        Parameters
        ----------
        char : str
            Character to draw.
        x : int
            Horizontal coordinate.
        y : int
            Vertical coordinate.
        style : str, optional
            Rich style string for the character.
        """
        self.chars.append(StyledChar(char, style, x, y))

    def __rich__(self) -> Text:
        """
        Generate a `rich.Text` object representing this text object.

        Returns
        -------
        Text
            A styled Rich Text object suitable for printing in the terminal.
        """
        if not self.chars:
            return Text("")
        min_x = min(c.x for c in self.chars)
        min_y = min(c.y for c in self.chars)
        shifted = [
            StyledChar(c.char, c.style, c.x - min_x, c.y - min_y) for c in self.chars
        ]
        width = max(c.x for c in shifted) + 1
        height = max(c.y for c in shifted) + 1
        grid = [[Text(" ") for _ in range(width)] for _ in range(height)]
        for c in shifted:
            grid[c.y][c.x] = Text(c.char, style=c.style)
        return Text("\n").join(Text().join(row) for row in grid)


class TextPanel(AbstractTextObject):
    """
    A composite text container that can position multiple `AbstractTextObject` instances
    on a shared coordinate plane.

    TextPanels are useful for assembling multiple graphical elements into a single
    renderable layout. They also support routing paths between objects using A* pathfinding.

    Attributes
    ----------
    objects : list of tuple[AbstractTextObject, int, int]
        List of contained objects and their (x, y) offsets.
    chars : list of StyledChar
        All characters across all contained objects, with positions offset.
    width : int
        Width of the bounding box around all characters.
    height : int
        Height of the bounding box around all characters.
    """

    def __init__(
        self,
        objects: list[tuple[AbstractTextObject, int, int] | AbstractTextObject]
        | None = None,
        *,
        penalty_group: str | None = None,
    ):
        """
        Initialize a `TextPanel` with optional pre-positioned objects and a penalty group.

        Parameters
        ----------
        objects : list of tuple[AbstractTextObject, int, int] or AbstractTextObject, optional
            List of `(object, x_offset, y_offset)` tuples to populate the panel initially.
            List elements can also be plain AbstractTextObject objects, in which case the
            offsets will be `(0, 0)`. If None, starts empty.
        penalty_group : str or None, optional
            Optional group label for use in pathfinding cost calculations.
        """
        if objects is not None:
            self.objects: list[tuple[AbstractTextObject, int, int]] = []
            for obj in objects:
                if isinstance(obj, AbstractTextObject):
                    self.objects.append((obj, 0, 0))
                else:
                    self.objects.append(obj)
        else:
            self.objects = []
        super().__init__(penalty_group=penalty_group)

    def add_object(self, obj: AbstractTextObject, x_offset: int = 0, y_offset: int = 0):
        """
        Add a sub-object to the panel at a specific offset.

        Parameters
        ----------
        obj : AbstractTextObject
            The object to insert into the panel.
        x_offset : int, default = 0
            Horizontal position offset for the object.
        y_offset : int, default = 0
            Vertical position offset for the object.
        """
        self.objects.append((obj, x_offset, y_offset))

    @property
    @override
    def chars(self) -> list[StyledChar]:
        all_chars = []
        for obj, dx, dy in self.objects:
            all_chars.extend(
                [StyledChar(c.char, c.style, c.x + dx, c.y + dy) for c in obj.chars]
            )
        return all_chars

    @property
    @override
    def width(self) -> int:
        if not self.objects:
            return 0
        all_x = [c.x + dx for obj, dx, _ in self.objects for c in obj.chars]
        return max(all_x) - min(all_x) + 1 if all_x else 0

    @property
    @override
    def height(self) -> int:
        if not self.objects:
            return 0
        all_y = [c.y + dy for obj, _, dy in self.objects for c in obj.chars]
        return max(all_y) - min(all_y) + 1 if all_y else 0

    def __rich__(self) -> Text:
        """
        Generate a Rich renderable for the full panel.

        Returns
        -------
        Text
            Rendered representation as a Rich `Text` block.
        """
        all_chars = []
        for obj, dx, dy in self.objects:
            all_chars.extend(
                [StyledChar(c.char, c.style, c.x + dx, c.y + dy) for c in obj.chars]
            )
        if not all_chars:
            return Text("")
        min_x = min(c.x for c in all_chars)
        min_y = min(c.y for c in all_chars)
        shifted = [
            StyledChar(c.char, c.style, c.x - min_x, c.y - min_y) for c in all_chars
        ]
        width = max(c.x for c in shifted) + 1
        height = max(c.y for c in shifted) + 1
        grid = [[Text(" ") for _ in range(width)] for _ in range(height)]
        for c in shifted:
            grid[c.y][c.x] = Text(c.char, style=c.style)
        return Text("\n").join(Text().join(row) for row in grid)

    def find_path(  # noqa: PLR0912, PLR0915
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        *,
        bend_penalty: int = 1,
        group_penalties: dict[str, int] | None = None,
    ) -> tuple[list[Segment], int, int, int]:
        """
        Use A* search to find a path between two coordinates, avoiding existing content.

        Parameters
        ----------
        start : tuple[int, int]
            Starting coordinate (x, y).
        end : tuple[int, int]
            Target coordinate (x, y).
        bend_penalty : int, optional
            Penalty for changing direction in the path.
        group_penalties : dict of str to int, optional
            Per-penalty-group cost override.

        Returns
        -------
        segments : list of Segment
            The directional steps to reach the target.
        x0 : int
            Absolute x-coordinate of the path start.
        y0 : int
            Absolute y-coordinate of the path start.
        total_cost : int
            Total cost of the found path.

        Raises
        ------
        RuntimeError
            If no valid path is found.
        """
        owner_map: dict[tuple[int, int], AbstractTextObject] = {}
        for obj, dx, dy in self.objects:
            for c in obj.chars:
                pos = (c.x + dx, c.y + dy)
                owner_map[pos] = obj

        def cost(
            pos: tuple[int, int],
            prev_dir: tuple[int, int] | None = None,
            new_dir: tuple[int, int] | None = None,
        ):
            group = (
                (owner_map[pos].penalty_group if pos in owner_map else None)
                if pos in owner_map
                else None
            )
            base = 1
            if group_penalties and group in group_penalties:
                base = group_penalties[group]
            bend = bend_penalty if prev_dir != new_dir else 0
            return base + bend

        frontier = [(0, start, (0, 0))]
        came_from = {start: ((0, 0), (0, 0))}
        cost_so_far = {start: 0}

        while frontier:
            _, current, prev_dir = heapq.heappop(frontier)
            if current == end:
                break
            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (x + dx, y + dy)
                direction = (dx, dy)
                new_cost = cost_so_far[current] + cost(next_pos, prev_dir, direction)
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = (
                        new_cost + abs(end[0] - next_pos[0]) + abs(end[1] - next_pos[1])
                    )
                    heapq.heappush(frontier, (priority, next_pos, direction))
                    came_from[next_pos] = (current, direction)

        path = []
        cur = end
        while cur != start:
            path.append(cur)
            cur = came_from.get(cur, (None,))[0]
            if cur is None:
                msg = "No valid path found"
                raise RuntimeError(msg)
        path.append(start)
        path.reverse()

        segments = []
        i = 0
        while i < len(path) - 1:
            x0, y0 = path[i]
            x1, y1 = path[i + 1]
            dx, dy = x1 - x0, y1 - y0
            count = 1
            while i + count < len(path):
                x2, y2 = path[i + count]
                if (x2 - x1, y2 - y1) != (dx, dy):
                    break
                count += 1
                x1, y1 = x2, y2
            if dx == 1:
                segments.append(Right(count))
            elif dx == -1:
                segments.append(Left(count))
            elif dy == 1:
                segments.append(Down(count))
            elif dy == -1:
                segments.append(Up(count))
            i += count

        x0, y0 = path[0]
        return segments, x0, y0, cost_so_far[end]

    def connect(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        *,
        border_type: BorderType = BorderType.LIGHT,
        style: str = "",
        start_char: str | None = None,
        start_style: str | None = None,
        end_char: str | None = None,
        end_style: str | None = None,
        bend_penalty: int = 1,
        group_penalties: dict[str, int] | None = None,
    ) -> TextObject:
        """
        Find a path between two points and return a `TextObject` with it drawn.

        Parameters
        ----------
        start, end : tuple[int, int]
            Start and end coordinates of the connection.
        border_type : BorderType, optional
            Type of border characters to use.
        style : str, optional
            Style for the entire path.
        start_char : str, optional
            Optional character at the path's start.
        start_style : str, optional
            Style for the start character.
        end_char : str, optional
            Optional character at the path's end.
        end_style : str, optional
            Style for the end character.
        bend_penalty : int, optional
            Cost added for each bend in the path.
        group_penalties : dict of str to int, optional
            Per-penalty-group cost override.

        Returns
        -------
        TextObject
            A `TextObject` representing the path.

        Raises
        ------
        RuntimeError
            If no valid path is found.
        """
        segments, x0, y0, _ = self.find_path(
            start, end, bend_penalty=bend_penalty, group_penalties=group_penalties
        )
        obj = TextObject.from_path(
            segments,
            border_type=border_type,
            style=style,
            start_char=start_char,
            start_style=start_style,
            end_char=end_char,
            end_style=end_style,
        )
        for c in obj.chars:
            c.x += x0
            c.y += y0
        return obj

    def connect_many(
        self,
        starts: list[tuple[int, int]],
        ends: list[tuple[int, int]],
        border_type: BorderType = BorderType.LIGHT,
        style: str = "",
        start_char: str | None = None,
        start_style: str | None = None,
        end_char: str | None = None,
        end_style: str | None = None,
        bend_penalty: int = 1,
        merge_penalty: int = 0,
        group_penalties: dict[str, int] | None = None,
        merge_penalty_group: str = "_mergepath",
        optimize_ordering: bool = False,
    ) -> TextObject:
        """
        Connect multiple point pairs with minimal cost using merged paths.

        Tries all permutations of connection order and chooses the one with
        the lowest total routing cost, encouraging path reuse.

        Parameters
        ----------
        starts, ends : list of tuple[int, int]
            Lists of start and end coordinates. Must be the same length.
        border_type : BorderType, optional
            Type of border characters to use.
        style : str, optional
            Style to apply to all paths.
        start_char : str, optional
            Character to draw at each start point.
        start_style : str, optional
            Style for the start character.
        end_char : str, optional
            Character to draw at each end point.
        end_style : str, optional
            Style for the end character.
        bend_penalty : int, optional
            Penalty added for direction changes.
        merge_penalty : int, optional
            Penalty added for moving along existing merged path.
        group_penalties : dict of str to int, optional
            Per-penalty-group cost override.
        merge_penalty_group : str, optional
            Group name assigned to paths to encourage path merging.
        optimize_ordering : bool, optional
            If true, the order of each set of start and end points
            will be permuted to optimize the path cost.

        Returns
        -------
        TextObject
            A merged `TextObject` with all connections drawn.

        Raises
        ------
        ValueError
            If `starts` and `ends` have unequal lengths.
        RuntimeError
            If no valid set of paths could be found.
        """
        if len(starts) != len(ends):
            msg = "'starts' and 'ends' must have the same length"
            raise ValueError(msg)
        best_obj = None
        min_total_cost = float("inf")
        path_pairs = list(zip(starts, ends))

        if optimize_ordering:
            orderings = list(permutations(path_pairs))
        else:
            orderings = [path_pairs]

        for ordering in orderings:
            temp_panel = TextPanel()
            temp_panel.objects = list(self.objects)
            paths = []
            total_cost = 0

            for s, e in ordering:
                segments, x0, y0, cost = temp_panel.find_path(
                    s,
                    e,
                    bend_penalty=bend_penalty,
                    group_penalties={
                        **(group_penalties or {}),
                        merge_penalty_group: merge_penalty,
                    },
                )
                total_cost += cost

                path_obj = TextObject.from_path(
                    segments,
                    border_type=border_type,
                    style=style,
                    start_char=start_char,
                    start_style=start_style,
                    end_char=end_char,
                    end_style=end_style,
                )
                for c in path_obj.chars:
                    c.x += x0
                    c.y += y0
                path_obj.penalty_group = merge_penalty_group
                temp_panel.add_object(path_obj)
                paths.append(path_obj)

            if total_cost < min_total_cost:
                min_total_cost = total_cost
                best_obj = TextObject()
                for p in paths:
                    best_obj.chars.extend(p.chars)
                best_obj.merge_path_intersections(border_type)

        if best_obj is None:
            msg = "No best valid path found"
            raise RuntimeError(msg)
        return best_obj


class TextBox(TextObject):
    """
    A styled Unicode box that wraps a `TextObject` with a border and padding.

    The content is centered within the box with optional padding and styled border
    characters. The resulting object is fully compatible with the `TextObject` API.

    Parameters
    ----------
    content : TextObject
        The inner content to be displayed inside the box.
    border_style : str, optional
        Rich style string applied to the border characters.
    border_type : BorderType, optional
        Type of box-drawing border to use (e.g., light, heavy, double).
    padding : tuple[int, int, int, int], optional
        Amount of padding around the content in the order (top, right, bottom, left).
    transparent_padding : bool, optional
        If True, spaces in the padding are not rendered.
    penalty_group : str or None, optional
        Optional group name used during pathfinding to influence cost.

    Notes
    -----
    The border adds 2 extra characters of width and height beyond the
    inner content plus padding.
    """

    def __init__(
        self,
        content: TextObject,
        *,
        border_style: str = "",
        border_type: BorderType = BorderType.LIGHT,
        padding: tuple[int, int, int, int] = (0, 1, 0, 1),
        transparent_padding: bool = False,
        penalty_group: str | None = None,
    ):
        super().__init__(penalty_group=penalty_group)

        top_pad, right_pad, bottom_pad, left_pad = padding
        content_min_x = min((c.x for c in content.chars), default=0)
        content_min_y = min((c.y for c in content.chars), default=0)

        for c in content.chars:
            self.add_char(
                c.char,
                c.x - content_min_x + 1 + left_pad,
                c.y - content_min_y + 1 + top_pad,
                style=c.style,
            )

        inner_width = content.width + left_pad + right_pad
        inner_height = content.height + top_pad + bottom_pad
        box_width = inner_width + 2
        box_height = inner_height + 2

        chars = BORDER_CHARS[border_type]

        for x in range(1, box_width - 1):
            self.add_char(chars["hor"], x, 0, style=border_style)
            self.add_char(chars["hor"], x, box_height - 1, style=border_style)
            if not transparent_padding and 0 < x < box_width - 1:
                for p in range(top_pad):
                    self.add_char(" ", x, p + 1, style=border_style)
                for p in range(bottom_pad):
                    self.add_char(" ", x, box_height - 1 - (p + 1), style=border_style)
        for y in range(1, box_height - 1):
            self.add_char(chars["ver"], 0, y, style=border_style)
            self.add_char(chars["ver"], box_width - 1, y, style=border_style)
            if not transparent_padding and 0 < y < box_height - 1:
                for p in range(left_pad):
                    self.add_char(" ", p + 1, y, style=border_style)
                for p in range(right_pad):
                    self.add_char(" ", box_width - 1 - (p + 1), y, style=border_style)

        self.add_char(chars["dr"], 0, 0, style=border_style)
        self.add_char(chars["dl"], box_width - 1, 0, style=border_style)
        self.add_char(chars["ur"], 0, box_height - 1, style=border_style)
        self.add_char(chars["ul"], box_width - 1, box_height - 1, style=border_style)

    @classmethod
    def from_string(
        cls,
        text: str,
        *,
        border_style: str = "",
        style: str = "",
        border_type: BorderType = BorderType.LIGHT,
        padding: tuple[int, int, int, int] = (0, 1, 0, 1),
        justify: Literal["left", "center", "right"] = "center",
        transparent: bool = False,
    ) -> TextBox:
        """
        Create a `TextBox` from a multiline string with justification and padding.

        Parameters
        ----------
        text : str
            The input string to wrap in a styled box.
        border_style : str, optional
            Rich style string applied to the border characters.
        style : str, optional
            Style to apply to the inner text content.
        border_type : BorderType, optional
            Box-drawing style to use for the border.
        padding : tuple[int, int, int, int], optional
            Padding around the content in (top, right, bottom, left) order.
        justify : {'left', 'center', 'right'}, optional
            Alignment of text lines within the content area.
        transparent : bool, optional
            If True, spaces in the content string are not rendered.

        Returns
        -------
        TextBox
            A styled box containing the given text.
        """
        lines = text.splitlines()
        max_line_length = max((len(line) for line in lines), default=0)
        aligned_lines = []

        for line in lines:
            if justify == "left":
                text = line.ljust(max_line_length)
            elif justify == "center":
                text = line.center(max_line_length)
            else:
                text = line.rjust(max_line_length)
            aligned_lines.append(text)

        padded_lines = aligned_lines or [""]
        text_obj = TextObject.from_string(
            "\n".join(padded_lines), style=style, transparent=transparent
        )

        return cls(
            text_obj,
            border_style=border_style,
            border_type=border_type,
            padding=padding,
        )


__all__ = [
    "AbstractTextObject",
    "BorderType",
    "Down",
    "Left",
    "Right",
    "StyledChar",
    "TextBox",
    "TextObject",
    "TextPanel",
    "Up",
]
