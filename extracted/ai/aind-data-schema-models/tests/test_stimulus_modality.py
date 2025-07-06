"""Tests classes in stimulus_modality module"""

import unittest

from aind_data_schema_models.stimulus_modality import StimulusModality


class TestStimulusModality(unittest.TestCase):
    """Tests methods in StimulusModality class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(StimulusModality.NO_STIMULUS, StimulusModality("No stimulus"))


if __name__ == "__main__":
    unittest.main()
