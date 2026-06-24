import unittest

from abstra_internals.controllers.workflow_layout import Box, find_free_position


def _overlaps(a, b):
    return (
        a.x < b.x + b.width
        and a.x + a.width > b.x
        and a.y < b.y + b.height
        and a.y + a.height > b.y
    )


class TestFindFreePosition(unittest.TestCase):
    def test_empty_returns_origin(self):
        self.assertEqual(find_free_position([]), (0, 0))

    def test_single_existing_does_not_overlap_it(self):
        existing = [Box(0, 0)]
        x, y = find_free_position(existing)
        self.assertFalse(_overlaps(Box(x, y), existing[0]))

    def test_new_stage_cascades_below_existing(self):
        x, y = find_free_position([Box(0, 0)])
        self.assertEqual(x, 0)
        self.assertGreater(y, 0)

    def test_result_avoids_all_existing(self):
        existing = [Box(0, 0), Box(280, 0), Box(0, 130)]
        x, y = find_free_position(existing)
        for box in existing:
            self.assertFalse(_overlaps(Box(x, y), box))

    def test_respects_arbitrary_non_grid_positions(self):
        existing = [Box(37, 11), Box(900, 640)]
        x, y = find_free_position(existing)
        for box in existing:
            self.assertFalse(_overlaps(Box(x, y), box))

    def test_avoids_large_custom_sized_box(self):
        existing = [Box(0, 0, 5000, 5000)]
        x, y = find_free_position(existing)
        self.assertFalse(_overlaps(Box(x, y), existing[0]))

    def test_deterministic(self):
        existing = [Box(0, 0), Box(280, 0)]
        self.assertEqual(find_free_position(existing), find_free_position(existing))


if __name__ == "__main__":
    unittest.main()
