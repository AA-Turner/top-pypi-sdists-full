from typing import ClassVar, Literal, Union, cast

from shortuuid import uuid

from .._util.instances import get_instances, track_instance

SELECTION_PREFIX = "selection_"


class Selection(str):
    """Selection that can be filtered by inputs and other selections.

    Selection types include:

    - `Selection.intersect()` for intersecting clauses (logical "and")
    - `Selection.union()` for unionone clauses (logical "or")
    - `Selection.single()` for a single clause only
    - `Selection.crossfilter()` for a cross-filtered intersection
    """

    _id: str
    _select: Literal["crossfilter", "intersect", "single", "union"]
    _cross: bool | None
    _empty: bool | None
    _include: Union["Selection", list["Selection"] | None]

    @classmethod
    def intersect(
        cls,
        cross: bool = False,
        empty: bool = False,
        include: Union["Selection", list["Selection"]] | None = None,
    ) -> "Selection":
        """Create a new Selection instance with an intersect (conjunction) resolution strategy.

        Args:
            cross: Boolean flag indicating cross-filtered resolution. If true, selection clauses will not be applied to the clients they are associated with.
            empty:  Boolean flag indicating if a lack of clauses should correspond to an empty selection with no records. This setting determines the default selection state.
            include: Upstream selections whose clauses should be included as part of the new selection. Any clauses published to upstream selections will be relayed to the new selection.
        """
        return Selection("intersect", cross=cross, empty=empty, include=include)

    @classmethod
    def union(
        cls,
        cross: bool = False,
        empty: bool = False,
        include: Union["Selection", list["Selection"]] | None = None,
    ) -> "Selection":
        """Create a new Selection instance with a union (disjunction) resolution strategy.

        Args:
            cross: Boolean flag indicating cross-filtered resolution. If true, selection clauses will not be applied to the clients they are associated with.
            empty: Boolean flag indicating if a lack of clauses should correspond to an empty selection with no records. This setting determines the default selection state.
            include: Upstream selections whose clauses should be included as part of the new selection. Any clauses published to upstream selections will be relayed to the new selection.
        """
        return Selection("union", cross=cross, empty=empty, include=include)

    @classmethod
    def single(
        cls,
        cross: bool = False,
        empty: bool = False,
        include: Union["Selection", list["Selection"]] | None = None,
    ) -> "Selection":
        """Create a new Selection instance with a singular resolution strategy that keeps only the most recent selection clause.

        Args:
            cross: Boolean flag indicating cross-filtered resolution. If true, selection clauses will not be applied to the clients they are associated with.
            empty: Boolean flag indicating if a lack of clauses should correspond to an empty selection with no records. This setting determines the default selection state.
            include: Upstream selections whose clauses should be included as part of the new selection. Any clauses published to upstream selections will be relayed to the new selection.
        """
        return Selection("single", cross=cross, empty=empty, include=include)

    @classmethod
    def crossfilter(
        cls,
        empty: bool = False,
        include: Union["Selection", list["Selection"]] | None = None,
    ) -> "Selection":
        """Create a new Selection instance with a cross-filtered intersect resolution strategy.

        Args:
            empty: Boolean flag indicating if a lack of clauses should correspond to an empty selection with no records. This setting determines the default selection state.
            include: Upstream selections whose clauses should be included as part of the new selection. Any clauses published to upstream selections will be relayed to the new selection.
        """
        return Selection("crossfilter", cross=True, empty=empty, include=include)

    def __new__(
        cls,
        select: Literal["crossfilter", "intersect", "single", "union"],
        *,
        cross: bool | None = None,
        empty: bool | None = None,
        unique: str | None = None,
        include: Union["Selection", list["Selection"] | None] = None,
    ) -> "Selection":
        # assign a unique id
        id = f"{SELECTION_PREFIX}{unique or uuid()}"

        # create the string instance
        instance = super().__new__(cls, f"${id}")

        # bind instance vars
        instance._id = id
        instance._select = select
        instance._cross = cross
        instance._empty = empty
        instance._include = include

        # track and return instance
        track_instance("selection", instance)
        return instance

    @property
    def id(self) -> str:
        return self._id

    @property
    def select(self) -> Literal["crossfilter", "intersect", "single", "union"]:
        return self._select

    @property
    def cross(self) -> bool | None:
        return self._cross

    @property
    def empty(self) -> bool | None:
        return self._empty

    @property
    def include(self) -> Union["Selection", list["Selection"] | None]:
        return self._include

    def __repr__(self) -> str:
        # start with selection
        repr = f"Selection(select={self.select}"

        # include non-default cross
        if (self.cross is True and self.select != "crossfilter") or (
            self.cross is False and self.select == "crossfilter"
        ):
            repr = f"{repr},cross={self.cross}"

        # include empty if specified
        if self.empty is not None:
            repr = f"{repr},empty={self.empty}"

        if self._include is not None:
            include = (
                self._include if isinstance(self._include, list) else [self._include]
            )
            repr = f"{repr},selection={','.join(include)}"

        # close out and return
        return f"{repr})"

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Selection"]] = []

    @classmethod
    def _get_all(cls) -> list["Selection"]:
        """Get all selections."""
        return cast(list["Selection"], get_instances("selection"))
