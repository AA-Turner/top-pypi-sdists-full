"""Tests classes in organizations module"""

import unittest

from aind_data_schema_models.organizations import Organization
from typing import get_args


class TestOrganization(unittest.TestCase):
    """Tests methods in Organization class"""

    def test_name_map(self):
        """Tests Organization name_map property"""

        self.assertEqual(Organization.AI, Organization.name_map["Allen Institute"])

    def test_none(self):
        """Tests that empty strings map to None"""

        self.assertEqual(Organization.LIFECANVAS.abbreviation, None)

    def test_from_none(self):
        """Test that you can't get an organization from None"""

        self.assertEqual(Organization.from_abbreviation(None), None)

    def test_groups(self):
        """Test that the organization groups are present"""

        union_types = get_args(Organization.SUBJECT_SOURCES.__origin__)
        self.assertTrue(any(isinstance(Organization.AI, t) for t in union_types))

        union_types = get_args(Organization.RESEARCH_INSTITUTIONS.__origin__)
        self.assertTrue(any(isinstance(Organization.AIBS, t) for t in union_types))


if __name__ == "__main__":
    unittest.main()
