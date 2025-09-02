"""Geometry models."""

from __future__ import annotations


class Geometry:
    """Represents a geometry."""


class Point(Geometry):
    """Represents a point."""

    def __init__(self, latitude: float, longitude: float):
        """Initialise point."""
        self._latitude: float = latitude
        self._longitude: float = longitude

    def __repr__(self):
        """Return string representation of this point."""
        return f"<{self.__class__.__name__}(latitude={self.latitude}, longitude={self.longitude})>"

    def __hash__(self) -> int:
        """Return unique hash of this geometry."""
        return hash((self.latitude, self.longitude))

    def __eq__(self, other: object) -> bool:
        """Return if this object is equal to other object."""
        return (
            self.__class__ == other.__class__
            and self.latitude == other.latitude
            and self.longitude == other.longitude
        )

    @property
    def latitude(self) -> float | None:
        """Return the latitude of this point."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return the longitude of this point."""
        return self._longitude


class Polygon(Geometry):
    """Represents a polygon."""

    def __init__(self, points: list[Point]):
        """Initialise polygon."""
        self._points: list[Point] = points

    def __repr__(self):
        """Return string representation of this polygon."""
        return f"<{self.__class__.__name__}(centroid={self.centroid})>"

    def __hash__(self) -> int:
        """Return unique hash of this geometry."""
        return hash(self.points)

    def __eq__(self, other: object) -> bool:
        """Return if this object is equal to other object."""
        return self.__class__ == other.__class__ and self.points == other.points

    @property
    def points(self) -> list[Point] | None:
        """Return the points of this polygon."""
        return self._points

    @property
    def edges(self) -> list[tuple[Point, Point]]:
        """Return all edges of this polygon."""
        edges: list[tuple[Point, Point]] = []
        for i in range(1, len(self.points)):
            previous = self.points[i - 1]
            current = self.points[i]
            edges.append((previous, current))
        return edges

    @property
    def centroid(self) -> Point:
        """Find the polygon's centroid as a best approximation."""
        longitudes_list: list[float] = [point.longitude for point in self.points]
        latitudes_list: list[float] = [point.latitude for point in self.points]
        number_of_points: int = len(self.points)
        longitude: float = sum(longitudes_list) / number_of_points
        latitude: float = sum(latitudes_list) / number_of_points
        return Point(latitude, longitude)

    def is_inside(self, point: Point | None) -> bool:
        """Check if the provided point is inside this polygon."""
        if point:
            crossings: int = 0
            for edge in self.edges:
                if Polygon._ray_crosses_segment(point, edge):
                    crossings += 1
            return crossings % 2 == 1
        return False

    @staticmethod
    def _ray_crosses_segment(point: Point, edge: tuple[Point, Point]):
        """Use ray-casting algorithm to check provided point and edge."""
        a, b = edge
        px = point.longitude
        py = point.latitude
        ax = a.longitude
        ay = a.latitude
        bx = b.longitude
        by = b.latitude
        if ay > by:
            ax = b.longitude
            ay = b.latitude
            bx = a.longitude
            by = a.latitude
        # Alter longitude to cater for 180 degree crossings.
        if px < 0:
            px += 360.0
        if ax < 0:
            ax += 360.0
        if bx < 0:
            bx += 360.0

        if py in (ay, by):
            py += 0.00000001
        if (py > by or py < ay) or (px > max(ax, bx)):
            return False
        if px < min(ax, bx):
            return True

        red = ((by - ay) / (bx - ax)) if (ax != bx) else float("inf")
        blue = ((py - ay) / (px - ax)) if (ax != px) else float("inf")
        return blue >= red


class BoundingBox(Geometry):
    """Represents a bounding box (bbox)."""

    # <!--gdacs: bbox format = lonmin lonmax latmin latmax -->
    # <gdacs:bbox> 164.5652 172.5652 -24.9041 -16.9041 </gdacs:bbox>

    def __init__(self, bottom_left: Point, top_right: Point):
        """Initialise bounding box."""
        self._bottom_left: Point = bottom_left
        self._top_right: Point = top_right

    def __repr__(self):
        """Return string representation of this bounding box."""
        return f"<{self.__class__.__name__}(bottom_left={self._bottom_left}, top_right={self._top_right})>"

    def __hash__(self) -> int:
        """Return unique hash of this geometry."""
        return hash((self.bottom_left, self.top_right))

    def __eq__(self, other: object) -> bool:
        """Return if this object is equal to other object."""
        return (
            self.__class__ == other.__class__
            and self.bottom_left == other.bottom_left
            and self.top_right == other.top_right
        )

    @property
    def bottom_left(self) -> Point:
        """Return bottom left point."""
        return self._bottom_left

    @property
    def top_right(self) -> Point:
        """Return top right point."""
        return self._top_right

    @property
    def centroid(self) -> Point:
        """Find the bounding box's centroid as a best approximation."""
        transposed_top_right_longitude: float = self._top_right.longitude
        if self._bottom_left.longitude > self._top_right.longitude:
            # bounding box spans across 180 degree longitude
            transposed_top_right_longitude = self._top_right.longitude + 360
        longitude: float = (
            self._bottom_left.longitude + transposed_top_right_longitude
        ) / 2
        latitude: float = (self._bottom_left.latitude + self._top_right.latitude) / 2
        return Point(latitude, longitude)

    def is_inside(self, point: Point) -> bool:
        """Check if the provided point is inside this bounding box."""
        if point:
            transposed_point_longitude: float = point.longitude
            transposed_top_right_longitude = self._top_right.longitude
            if self._bottom_left.longitude > self._top_right.longitude:
                # bounding box spans across 180 degree longitude
                transposed_top_right_longitude = self._top_right.longitude + 360
                if point.longitude < 0:
                    transposed_point_longitude += 360
            return (
                self._bottom_left.latitude <= point.latitude <= self._top_right.latitude
            ) and (
                self._bottom_left.longitude
                <= transposed_point_longitude
                <= transposed_top_right_longitude
            )
        return False
