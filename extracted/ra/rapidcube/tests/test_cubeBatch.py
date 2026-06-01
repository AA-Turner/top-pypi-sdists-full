import unittest

import numpy as np

import rapidcube

CubeBatch = rapidcube.CubeBatch
Cube2x2 = rapidcube.Cube2x2
Cube3x3 = rapidcube.Cube3x3

MOVE_INDEX_METHODS = [
    "do_u_move",
    "do_u_prime_move",
    "do_d_move",
    "do_d_prime_move",
    "do_r_move",
    "do_r_prime_move",
    "do_l_move",
    "do_l_prime_move",
    "do_f_move",
    "do_f_prime_move",
    "do_b_move",
    "do_b_prime_move",
]


class TestCubeBatch(unittest.TestCase):
    def test_create_batch_2x2(self):
        batch = CubeBatch(4, 2)
        self.assertEqual(len(batch), 4)
        for i in range(len(batch)):
            self.assertIsInstance(batch[i], Cube2x2)

    def test_create_batch_3x3(self):
        batch = CubeBatch(4, 3)
        self.assertEqual(len(batch), 4)
        for i in range(len(batch)):
            self.assertIsInstance(batch[i], Cube3x3)

    def test_empty_batch(self):
        batch = CubeBatch(0, 2)
        self.assertEqual(len(batch), 0)
        self.assertEqual(list(batch), [])

    def test_invalid_cube_type(self):
        with self.assertRaises(TypeError):
            CubeBatch(5, 4)

    def test_cube_batch_supports_indexing(self):
        batch = CubeBatch(2, 2)

        self.assertIsInstance(batch[0], Cube2x2)
        self.assertIsInstance(batch[1], Cube2x2)

        with self.assertRaises(IndexError):
            _ = batch[2]

        with self.assertRaises(IndexError):
            _ = batch[-3]

        b3 = CubeBatch(2, 3)
        self.assertEqual(len(b3), 2)
        for i in range(2):
            self.assertIsInstance(b3[i], Cube3x3)

    def test_cube_batch_iteration(self):
        batch = CubeBatch(3, 2)
        items = list(batch)
        self.assertEqual(len(items), 3)
        for item in items:
            self.assertIsInstance(item, Cube2x2)

    def test_apply_move_indexes_2x2(self):
        batch = CubeBatch(3, 2)
        move_indexes = np.array([0, 5, 10], dtype=np.uintp)

        batch.apply_move_indexes(move_indexes)

        expected = [Cube2x2(), Cube2x2(), Cube2x2()]
        for cube, move_index in zip(expected, move_indexes):
            getattr(cube, MOVE_INDEX_METHODS[int(move_index)])()

        for i, cube in enumerate(expected):
            self.assertEqual(batch[i].state, cube.state)

    def test_apply_move_indexes_3x3(self):
        batch = CubeBatch(2, 3)
        move_indexes = np.array([1, 8], dtype=np.uintp)

        batch.apply_move_indexes(move_indexes)

        expected = [Cube3x3(), Cube3x3()]
        for cube, move_index in zip(expected, move_indexes):
            getattr(cube, MOVE_INDEX_METHODS[int(move_index)])()

        for i, cube in enumerate(expected):
            self.assertEqual(batch[i].to_binary(), cube.to_binary())

    def test_scramble_length_zero_keeps_solved(self):
        batch = CubeBatch(4, 2)
        scramble_lengths = np.zeros(4, dtype=np.int64)

        batch.scramble(scramble_lengths)

        for i in range(len(batch)):
            self.assertTrue(batch[i].is_solved())

    def test_scramble_length_one_unsolves(self):
        batch = CubeBatch(4, 3)
        scramble_lengths = np.ones(4, dtype=np.int64)

        batch.scramble(scramble_lengths)

        for i in range(len(batch)):
            self.assertFalse(batch[i].is_solved())
