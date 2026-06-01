import unittest

import rapidcube

Cube3x3 = rapidcube.Cube3x3


MOVE_PAIRS = [
    ("do_u_move", "do_u_prime_move"),
    ("do_d_move", "do_d_prime_move"),
    ("do_r_move", "do_r_prime_move"),
    ("do_l_move", "do_l_prime_move"),
    ("do_f_move", "do_f_prime_move"),
    ("do_b_move", "do_b_prime_move"),
]


def _identity_corners() -> int:
    corners = 0
    for i in range(8):
        corners |= i << (i * 5)
    return corners


def _identity_edges() -> int:
    edges = 0
    for i in range(12):
        edges |= i << (i * 5)
    return edges


class TestCube3x3(unittest.TestCase):
    def test_new_cube_has_identity_piece_state(self):
        cube = Cube3x3()

        self.assertEqual(cube.get_corners(), [(i, 0) for i in range(8)])
        self.assertEqual(cube.get_edges(), [(i, 0) for i in range(12)])

    def test_binary_methods_are_consistent_and_64_bit(self):
        cube = Cube3x3()

        corners_bits = cube.to_binary_corners()
        edges_bits = cube.to_binary_edges()
        pair = cube.to_binary()

        self.assertEqual(len(corners_bits), 64)
        self.assertEqual(len(edges_bits), 64)
        self.assertTrue(set(corners_bits).issubset({"0", "1"}))
        self.assertTrue(set(edges_bits).issubset({"0", "1"}))

        self.assertEqual(pair, (corners_bits, edges_bits))
        self.assertEqual(int(corners_bits, 2), _identity_corners())
        self.assertEqual(int(edges_bits, 2), _identity_edges())

    def test_get_corners_returns_two_dimensional_integer_array(self):
        cube = Cube3x3()

        corners = cube.get_corners()

        self.assertIsInstance(corners, list)
        self.assertEqual(len(corners), 8)
        self.assertEqual(corners, [(i, 0) for i in range(8)])

        for row in corners:
            self.assertIsInstance(row, tuple)
            self.assertEqual(len(row), 2)
            self.assertTrue(all(isinstance(value, int) for value in row))

    def test_get_edges_returns_two_dimensional_integer_array(self):
        cube = Cube3x3()

        edges = cube.get_edges()

        self.assertIsInstance(edges, list)
        self.assertEqual(len(edges), 12)
        self.assertEqual(edges, [(i, 0) for i in range(12)])

        for row in edges:
            self.assertIsInstance(row, tuple)
            self.assertEqual(len(row), 2)
            self.assertTrue(all(isinstance(value, int) for value in row))

    def test_is_solved_tracks_state_changes(self):
        cube = Cube3x3()

        self.assertTrue(cube.is_solved())

        cube.do_f_move()
        self.assertFalse(cube.is_solved())

        cube.do_f_prime_move()
        self.assertTrue(cube.is_solved())

    def test_move_followed_by_inverse_restores_state(self):
        for move, inv in MOVE_PAIRS:
            with self.subTest(move=move, inv=inv):
                cube = Cube3x3()
                before = cube.to_binary()

                getattr(cube, move)()
                getattr(cube, inv)()

                self.assertEqual(cube.to_binary(), before)

    def test_four_quarter_turns_restore_state(self):
        for move, _ in MOVE_PAIRS:
            with self.subTest(move=move):
                cube = Cube3x3()
                before = cube.to_binary()

                for _ in range(4):
                    getattr(cube, move)()

                self.assertEqual(cube.to_binary(), before)

    def test_do_moves_matches_explicit_execution_and_ignores_unknown_tokens(self):
        parsed = Cube3x3()
        explicit = Cube3x3()

        parsed.do_moves("U R2 F! INVALID_TOKEN B' D2")

        explicit.do_u_move()
        explicit.do_r_move()
        explicit.do_r_move()
        explicit.do_f_prime_move()
        explicit.do_b_prime_move()
        explicit.do_d_move()
        explicit.do_d_move()

        self.assertEqual(parsed.to_binary(), explicit.to_binary())

    def test_get_next_states_returns_qtm_successors(self):
        cubes = [Cube3x3(), Cube3x3()]

        states = rapidcube.get_next_states(cubes)

        self.assertEqual(states.shape, (len(cubes) * 12, 54))
        self.assertTrue(hasattr(states, "dtype"))

    def test_str_returns_multiline_colored_net(self):
        cube = Cube3x3()
        text = str(cube)

        self.assertIsInstance(text, str)
        self.assertIn("\x1b[", text)
        self.assertEqual(len(text.splitlines()), 9)


if __name__ == "__main__":
    unittest.main()
