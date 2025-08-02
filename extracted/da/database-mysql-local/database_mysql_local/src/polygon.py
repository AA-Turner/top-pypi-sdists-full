# from .point import Point
from database_infrastructure_local.point import Point
# from .to_sql_interface import ToSQLInterface
from database_infrastructure_local.to_sql_interface import ToSQLInterface


class Polygon(ToSQLInterface):
    def __init__(self, points: list[Point]):
        if len(points) < 3:
            raise ValueError("A polygon must have at least 3 points.")
        self.points = points

    def to_sql(self):
        # the first point as the last point to ensure the polygon is closed.
        points_sql = ", ".join([f"{point.longitude} {point.latitude}" for point in self.points] + [
            f"{self.points[0].longitude} {self.points[0].latitude}"])
        return f"ST_PolygonFromText('POLYGON(({points_sql}))')"

    @staticmethod
    def create_select_stmt(column_name: str):
        return f"ST_AsText({column_name})"

    def __eq__(self, other_polygon):
        if isinstance(other_polygon, Polygon):
            return self.points == other_polygon.points
        return False

    @classmethod
    def from_text(cls, polygon_text):

        # Example input: 'POLYGON((10.1 10.1,10.2 10.2,10.3 10.3,10.1 10.1))'
        # Remove the outer parentheses
        inner_text = polygon_text.replace('POLYGON((', '').replace('))', '')

        # Splitting the inner text into pairs and
        # converting them to Point instances
        pairs = inner_text.split(',')
        # Converting each pair to a Point instance, Exclude the last pair
        points = [Point(float(pair.split()[0]), float(pair.split()[1])) for pair in pairs[:-1]]
        return cls(points)
