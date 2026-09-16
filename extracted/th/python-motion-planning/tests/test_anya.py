import math

from python_motion_planning.common import Grid, TYPES
from python_motion_planning.path_planner import Anya


def test_anya_empty_map_returns_straight_path():
    map_ = Grid(bounds=[[0, 12], [0, 12]])
    path, info = Anya(map_=map_, start=(1, 2), goal=(10, 9)).plan()

    assert info["success"]
    assert path == [(1, 2), (10, 9)]
    assert math.isclose(info["length"], math.hypot(9, 7))


def test_anya_routes_around_obstacle():
    map_ = Grid(bounds=[[0, 12], [0, 12]])
    map_[5, 2:10] = TYPES.OBSTACLE

    path, info = Anya(map_=map_, start=(2, 5), goal=(9, 5)).plan()

    assert info["success"]
    assert path[0] == (2, 5)
    assert path[-1] == (9, 5)
    assert len(path) > 2
    assert all(isinstance(value, int) for point in path for value in point)
    assert all(not map_.in_collision(path[i - 1], path[i]) for i in range(1, len(path)))


def test_anya_reports_unreachable_goal():
    map_ = Grid(bounds=[[0, 10], [0, 10]])
    map_[5, :] = TYPES.OBSTACLE

    path, info = Anya(map_=map_, start=(2, 5), goal=(8, 5)).plan()

    assert path == []
    assert not info["success"]


def test_anya_respects_strict_collision():
    map_ = Grid(bounds=[[0, 5], [0, 5]])
    map_[1, 0] = TYPES.OBSTACLE

    path, info = Anya(map_=map_, start=(0, 0), goal=(1, 1)).plan()
    assert info["success"]
    assert len(path) > 2
    assert all(not map_.in_collision(path[i - 1], path[i]) for i in range(1, len(path)))

    map_.strict_collision = False
    path, info = Anya(map_=map_, start=(0, 0), goal=(1, 1)).plan()
    assert info["success"]
    assert path == [(0, 0), (1, 1)]


def test_anya_uses_grid_rule_for_double_corner():
    map_ = Grid(bounds=[[0, 3], [0, 3]])
    map_[1, 0] = TYPES.OBSTACLE
    map_[0, 1] = TYPES.OBSTACLE

    path, info = Anya(map_=map_, start=(0, 0), goal=(1, 1)).plan()
    assert path == []
    assert not info["success"]

    map_.strict_collision = False
    path, info = Anya(map_=map_, start=(0, 0), goal=(1, 1)).plan()
    assert info["success"]
    assert path == [(0, 0), (1, 1)]
