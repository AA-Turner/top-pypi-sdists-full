import unittest
from io import BytesIO

import numpy as np
import pandas as pd

from tabpfn_common_utils.utils import (
    serialize_to_csv_formatted_bytes,
    assert_y_pred_proba_is_valid,
    shape_of,
)


class TestDataSerialization(unittest.TestCase):
    def test_serialize_numpy_array_to_csv_formatted_bytes(self):
        test_data = np.array([[1, 2, 3], [4, 5, 6]])
        test_pd_data = pd.DataFrame(test_data, columns=pd.Index(["0", "1", "2"]))
        csv_bytes = serialize_to_csv_formatted_bytes(test_data)
        data_recovered = pd.read_csv(BytesIO(csv_bytes), delimiter=",")
        pd.testing.assert_frame_equal(test_pd_data, data_recovered)

    def test_serialize_pandas_dataframe_to_csv_formatted_bytes(self):
        test_data = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]], columns=pd.Index(["a", "b", "c"])
        )
        csv_bytes = serialize_to_csv_formatted_bytes(test_data)
        data_recovered = pd.read_csv(BytesIO(csv_bytes), delimiter=",")
        pd.testing.assert_frame_equal(test_data, data_recovered)


class TestAssertYPredProbaIsValid(unittest.TestCase):
    x_test = pd.DataFrame([[1, 2, 3], [4, 5, 6]])

    def test_valid_y_pred_proba_assert_true(self):
        y_pred = np.array([[0.1, 0.2, 0.7], [0.3, 0.4, 0.3]])
        assert_y_pred_proba_is_valid(self.x_test, y_pred)

    def test_invalid_shape_assert_false(self):
        y_pred = np.array([1, 2, 3])
        with self.assertRaises(AssertionError):
            assert_y_pred_proba_is_valid(self.x_test, y_pred)

    def test_invalid_value_assert_false(self):
        y_pred = np.array([[0.1, 0.2, 0.6], [0.3, 0.4, 0.3]])
        with self.assertRaises(AssertionError):
            assert_y_pred_proba_is_valid(self.x_test, y_pred)


class TestShapeOf(unittest.TestCase):
    """Test cases for the shape_of function."""

    def test_numpy_2d_array(self):
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(shape_of(arr), (2, 3))

    def test_numpy_1d_array(self):
        arr = np.array([1, 2, 3, 4])
        self.assertEqual(shape_of(arr), (4, 1))

    def test_numpy_scalar(self):
        scalar = np.array(42)
        self.assertEqual(shape_of(scalar), (1, 1))

    def test_numpy_empty_array(self):
        arr = np.array([])
        self.assertEqual(shape_of(arr), (0, 1))

    def test_pandas_dataframe(self):
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(shape_of(df), (2, 3))

    def test_pandas_series(self):
        series = pd.Series([1, 2, 3, 4])
        self.assertEqual(shape_of(series), (4, 1))

    def test_pandas_empty_dataframe(self):
        df = pd.DataFrame()
        self.assertEqual(shape_of(df), (0, 0))

    def test_list_2d(self):
        lst = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(shape_of(lst), (2, 3))

    def test_list_1d(self):
        lst = [1, 2, 3, 4]
        self.assertEqual(shape_of(lst), (4, 1))

    def test_tuple_2d(self):
        tup = ((1, 2, 3), (4, 5, 6))
        self.assertEqual(shape_of(tup), (2, 3))

    def test_tuple_1d(self):
        tup = (1, 2, 3, 4)
        self.assertEqual(shape_of(tup), (4, 1))

    def test_empty_list(self):
        lst = []
        self.assertEqual(shape_of(lst), (0, 0))

    def test_nested_empty_list(self):
        lst = [[]]
        self.assertEqual(shape_of(lst), (1, 0))

    def test_irregular_nested_list(self):
        lst = [[1, 2], [3, 4, 5], [6]]
        # Should return (3, 2) based on first element length
        self.assertEqual(shape_of(lst), (3, 2))

    def test_single_element_list(self):
        lst = [42]
        self.assertEqual(shape_of(lst), (1, 1))

    def test_set_input(self):
        self.assertEqual(shape_of({1, 2, 3}), (0, 0))

    def test_generator_input(self):
        gen = (x for x in range(3))
        self.assertEqual(shape_of(gen), (0, 0))

    def test_range_input(self):
        rng = range(5)
        self.assertEqual(shape_of(rng), (5, 1))

    def test_1d_array_edge_case(self):
        # This tests the condition where shape[1] > 1 would exclude arrays like (100, 1)
        # These should be treated as having 1 column, not 0 columns
        arr_1d = np.array([1, 2, 3, 4, 5])  # shape (5,)
        self.assertEqual(shape_of(arr_1d), (5, 1))

        # Test with larger 1D array
        arr_large_1d = np.array(range(100))  # shape (100,)
        self.assertEqual(shape_of(arr_large_1d), (100, 1))

        # Test pandas Series (which should also be treated as 1 column)
        series = pd.Series([1, 2, 3, 4, 5])
        self.assertEqual(shape_of(series), (5, 1))

        # Test 1D list
        lst_1d = [1, 2, 3, 4, 5]
        self.assertEqual(shape_of(lst_1d), (5, 1))
