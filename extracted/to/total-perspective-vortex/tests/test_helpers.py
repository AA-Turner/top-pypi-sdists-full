"""Unit tests module for the helper functions"""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tpv.commands.test import mock_galaxy
from tpv.core.helpers import get_dataset_attributes, weighted_random_sampling


class TestHelpers(unittest.TestCase):
    """Tests for helper functions"""

    def test_get_dataset_attributes(self):
        """Test that the function returns a dictionary with the correct attributes"""
        job = mock_galaxy.Job()
        job.add_input_dataset(
            mock_galaxy.DatasetAssociation(
                "test",
                mock_galaxy.Dataset("test.txt", file_size=7 * 1024**3, object_store_id="files1"),
            )
        )
        dataset_attributes = get_dataset_attributes(job.input_datasets)
        expected_result = {0: {"object_store_id": "files1", "size": 7 * 1024**3}}
        self.assertEqual(dataset_attributes, expected_result)

    def test_weighted_random_sampling_without_weights_uses_unweighted_sampling(self):
        """When no destination defines params.weight, use unweighted random sampling."""
        destinations = [
            SimpleNamespace(id="dest_a", params={}),
            SimpleNamespace(id="dest_b", params=None),
            SimpleNamespace(id="dest_c", params={"foo": "bar"}),
        ]
        sampled_destinations = [destinations[2], destinations[0], destinations[1]]

        with patch("tpv.core.helpers.random.sample", return_value=sampled_destinations) as sample_mock:
            with patch("tpv.core.helpers.random.choices") as choices_mock:
                result = weighted_random_sampling(destinations)

        self.assertEqual(result, sampled_destinations)
        sample_mock.assert_called_once_with(destinations, k=3)
        choices_mock.assert_not_called()

    def test_weighted_random_sampling_with_weights_uses_weighted_choices(self):
        """When any destination defines params.weight, use weighted random choices."""
        destinations = [
            SimpleNamespace(id="dest_a", params={"weight": 5}),
            SimpleNamespace(id="dest_b", params={}),
            SimpleNamespace(id="dest_c", params=None),
        ]
        sampled_destinations = [destinations[0], destinations[0], destinations[2]]

        with patch("tpv.core.helpers.random.choices", return_value=sampled_destinations) as choices_mock:
            with patch("tpv.core.helpers.random.sample") as sample_mock:
                result = weighted_random_sampling(destinations)

        self.assertEqual(result, sampled_destinations)
        choices_mock.assert_called_once_with(destinations, weights=[5, 1, 1], k=3)
        sample_mock.assert_not_called()
