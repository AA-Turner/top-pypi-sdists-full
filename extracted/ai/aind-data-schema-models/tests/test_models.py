"""Tests classes with fixed Literal values match defaults"""

import unittest

from pydantic import BaseModel

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.species import Species
from aind_data_schema_models.mouse_anatomy import MouseAnatomy, MouseAnatomyModel, MouseEmgMuscles


class LiteralAndDefaultTests(unittest.TestCase):
    """Tests Literals match defaults in several classes"""

    def test_organizations(self):
        """Test Literals match defaults"""

        for organization in Organization.ALL:
            model = organization()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_harp(self):
        """Test Literals match defaults"""

        for harp in HarpDeviceType.ALL:
            model = harp()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_species(self):
        """Test Literals match defaults"""

        for species in Species.ALL:
            model = species()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_mouse_anatomy(self):
        """Test Literals match defaults"""
        structures = [
            "ANATOMICAL_STRUCTURE",
            "FIRST_POLAR_BODY",
            "_1_CELL_STAGE_EMBRYO",
            "SECOND_POLAR_BODY",
            "ZONA_PELLUCIDA",
            "_2_CELL_STAGE_EMBRYO",
        ]

        for structure in structures:
            model = getattr(MouseAnatomy, structure)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_mouse_custom_features(self):
        """Test that the custom __getattribute__ functionality works properly"""
        # ensure that class methods still return properly and don't trigger the custom __getattribute__ functionality
        self.assertIsNotNone(MouseAnatomy.__module__)
        self.assertIsNotNone(MouseAnatomy.__dict__)

        # generate a model from the class
        class TestModel(BaseModel):
            """test class"""

            structure: MouseAnatomyModel = MouseAnatomy.ANATOMICAL_STRUCTURE

        test = TestModel()
        self.assertIsNotNone(test)

        # generate a test model using the emg group
        class TestModel2(BaseModel):
            """test class"""

            structure: MouseAnatomyModel = MouseEmgMuscles.DELTOID

        test = TestModel2()
        self.assertIsNotNone(test)


if __name__ == "__main__":
    unittest.main()
