import unittest
import numpy as np

from tabpfn_common_utils.regression_pred_result import RegressionPredictResult


class TestRegressionPredResult(unittest.TestCase):
    def setUp(self):
        self.pred_res = {
            "mean": np.array([1, 2, 3]),
            "median": np.array([2, 3, 4]),
            "mode": np.array([3, 4, 5]),
            "quantile_0.25": np.array([4, 5, 6]),
            "quantile_0.75": np.array([5, 6, 7]),
        }

        self.pred_res_serialized_ref = {k: v.tolist() for k, v in self.pred_res.items()}

    def test_serialize_from_numpy(self):
        res = RegressionPredictResult(self.pred_res)
        serialized = RegressionPredictResult.to_basic_representation(res)
        self.assertEqual(serialized, self.pred_res_serialized_ref)

    def test_deserialize_to_numpy(self):
        res = RegressionPredictResult.from_basic_representation(
            self.pred_res_serialized_ref
        )

        for key in res:
            self.assertTrue(np.array_equal(res[key], self.pred_res[key]))

    def test_invalid_input_raises_error(self):
        bad_input = {
            "mean": {"a": 1, "b": 2},
            "median": [2, 3, 4],
            "mode": [3, 4, 5],
            "quantile_0.25": [4, 5, 6],
            "quantile_0.75": [5, 6, 7],
        }
        with self.assertRaises(ValueError):
            RegressionPredictResult(bad_input)
