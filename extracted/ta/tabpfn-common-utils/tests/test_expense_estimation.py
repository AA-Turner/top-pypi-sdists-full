import unittest
from tabpfn_common_utils.expense_estimation import (
    estimate_duration,
    VERTEX_GPU_FACTOR,
)


class TestExpenseEstimation(unittest.TestCase):
    def test_estimate_duration_classification(self):
        # Test basic classification case
        duration = estimate_duration(
            num_rows=100, num_features=10, task="classification"
        )
        self.assertGreater(duration, 0)
        self.assertIsInstance(duration, float)

    def test_estimate_duration_regression(self):
        # Test basic regression case
        duration = estimate_duration(num_rows=100, num_features=10, task="regression")
        self.assertGreater(duration, 0)
        self.assertIsInstance(duration, float)

        # Regression should take longer than classification with same parameters
        # due to higher default n_estimators (8 vs 4)
        classification_duration = estimate_duration(
            num_rows=100, num_features=10, task="classification"
        )
        self.assertGreater(duration, classification_duration)

    def test_scaling_with_rows_and_features(self):
        # Test scaling with number of rows
        small_dataset = estimate_duration(
            num_rows=100, num_features=10, task="classification"
        )

        large_dataset = estimate_duration(
            num_rows=1000, num_features=10, task="classification"
        )

        self.assertGreater(large_dataset, small_dataset)

        # Test scaling with number of features
        more_features = estimate_duration(
            num_rows=100, num_features=50, task="classification"
        )

        self.assertGreater(more_features, small_dataset)

    def test_custom_duration_factor(self):
        # Test with custom duration factor
        base_duration = estimate_duration(
            num_rows=100, num_features=10, task="classification"
        )

        doubled_factor = estimate_duration(
            num_rows=100,
            num_features=10,
            task="classification",
            duration_factor=VERTEX_GPU_FACTOR * 2,
        )

        self.assertAlmostEqual(doubled_factor, base_duration * 2, delta=0.1)

    def test_latency_offset(self):
        # Test with latency offset
        base_duration = estimate_duration(
            num_rows=100, num_features=10, task="classification"
        )

        with_offset = estimate_duration(
            num_rows=100, num_features=10, task="classification", latency_offset=1.5
        )

        self.assertAlmostEqual(with_offset, base_duration + 1.5, delta=0.001)
