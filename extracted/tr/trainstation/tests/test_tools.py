import numpy as np
import unittest

from trainstation.tools import compute_correlation_matrix, ScatterData
from trainstation.model import estimate_loocv


class TestFittingTools(unittest.TestCase):
    """Unittest class for tools module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_compute_correlation_matrix(self):
        """Tests compute_correlation_matrix."""

        v0 = np.array([1, 1, 1])
        v1 = np.array([1, 1, -2])
        v2 = np.array([-1, -1, -1])

        A = np.array([v0, v1, v2])
        n_rows = len(A)
        C = compute_correlation_matrix(A)

        # check that correlation matrix is symmetric
        for i in range(n_rows):
            for j in range(n_rows):
                self.assertAlmostEqual(C[i][j], C[j][i])

        # check diagonal elements are zero
        for i in range(n_rows):
            self.assertAlmostEqual(C[i][i], 0)

        # check v0-v1 and v1-v2 correlations are zero
        self.assertAlmostEqual(C[0][1], 0)
        self.assertAlmostEqual(C[2][1], 0)

        # check v0-v2 correlation is minus one
        self.assertAlmostEqual(C[0][2], -1)

    def test_estimate_loocv(self):
        A = np.arange(5000).reshape(100, 50) % 101
        y_target = np.arange(100, 200)
        y_predicted = np.arange(100, 200) + np.arange(-50, 50)/100
        loocv = estimate_loocv(A, y_target, y_predicted)
        loocv_target = 472.45040152319416
        self.assertAlmostEqual(loocv, loocv_target)

    def test_ScatterData(self):
        """ Test the scatterData class """

        # setup
        target1 = [1, 2, 3]
        target2 = [10, 20, 30]
        predicted1 = [4, 5, 6]
        predicted2 = [40, 50, 60]
        sd1 = ScatterData(target1, predicted1)
        sd2 = ScatterData(target2, predicted2)

        # check data is correct
        np.testing.assert_almost_equal(sd1.target, target1)
        np.testing.assert_almost_equal(sd1.predicted, predicted1)
        np.testing.assert_almost_equal(sd2.target, target2)
        np.testing.assert_almost_equal(sd2.predicted, predicted2)

        # check add methods work

        sd3 = sd1 + sd2
        np.testing.assert_almost_equal(sd3.target, target1+target2)
        np.testing.assert_almost_equal(sd3.predicted, predicted1+predicted2)


if __name__ == '__main__':
    unittest.main()
