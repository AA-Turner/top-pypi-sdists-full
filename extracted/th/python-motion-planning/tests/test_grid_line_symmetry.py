import itertools
import unittest

import numpy as np

from python_motion_planning.common import Grid, TYPES


class GridLineSymmetryTest(unittest.TestCase):
    def test_half_cell_ties(self):
        for dim in (2, 3, 4):
            grid = Grid(bounds=[[0, 13]] * dim)
            start = (6,) * dim
            for delta in itertools.product(range(-3, 4), repeat=dim):
                end = tuple(a + b for a, b in zip(start, delta))
                path = grid.line_of_sight(start, end)
                self.assertEqual(path, grid.line_of_sight(end, start)[::-1])
                self.assertEqual(path[0], start)
                self.assertEqual(path[-1], end)
                # Independent rational reference: ties follow the increasing
                # primary-axis traversal, including when requested in reverse.
                axis = max(range(dim), key=lambda d: abs(delta[d]))
                a, b = (start, end) if delta[axis] >= 0 else (end, start)
                steps = abs(delta[axis])
                expected = [a]
                for i in range(1, steps + 1):
                    expected.append(tuple(
                        a[d] + (1 if b[d] >= a[d] else -1)
                        * ((2 * i * abs(b[d] - a[d]) + steps - 1) // (2 * steps))
                        for d in range(dim)
                    ))
                if delta[axis] < 0:
                    expected.reverse()
                self.assertEqual(path, expected)

    def test_inflated_corner_regression(self):
        grid = Grid(bounds=[[0, 51], [0, 31]])
        grid.fill_boundary_with_obstacles()
        grid[10:21, 15] = TYPES.OBSTACLE
        grid[20, :15] = TYPES.OBSTACLE
        grid[30, 15:] = TYPES.OBSTACLE
        grid[40, :16] = TYPES.OBSTACLE
        grid.inflate_obstacles(radius=3)
        a, b = (27, 12), (31, 11)
        self.assertEqual(grid[30, 12], TYPES.INFLATION)
        self.assertTrue(grid.in_collision(a, b))
        self.assertTrue(grid.in_collision(b, a))
        grid.strict_collision = False
        self.assertFalse(grid.in_collision(a, b))
        self.assertFalse(grid.in_collision(b, a))
        grid.strict_collision = True
        grid[30, 12] = TYPES.FREE
        self.assertFalse(grid.in_collision(a, b))
        self.assertFalse(grid.in_collision(b, a))

    def test_random_collision_matches_steps(self):
        rng = np.random.default_rng(0)
        for dim in (2, 3, 4):
            shape = (9,) * dim
            data = np.zeros(shape, dtype=np.int8)
            values = rng.random(shape)
            data[values < 0.08] = TYPES.OBSTACLE
            data[(values >= 0.08) & (values < 0.16)] = TYPES.INFLATION
            grid = Grid(bounds=[[0, 9]] * dim, type_map=data)
            for strict in (False, True):
                grid.strict_collision = strict
                for _ in range(500):
                    a = tuple(int(x) for x in rng.integers(0, 9, dim))
                    b = tuple(int(x) for x in rng.integers(0, 9, dim))
                    path = grid.line_of_sight(a, b)
                    expected = not grid.is_expandable(a) or any(
                        not grid.is_expandable(v, u)
                        for u, v in zip(path, path[1:])
                    )
                    actual = grid.in_collision(a, b)
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual, grid.in_collision(b, a))


if __name__ == '__main__':
    unittest.main()
