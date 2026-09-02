import numpy as np
import unittest

from trainstation.model import Model


class TestModel(unittest.TestCase):
    """Unittest class for Optimizer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n_rows = 200
        self.n_cols = 50

        self.parameters = np.random.random(self.n_cols)

        self.A_train = np.random.normal(0, 1, (self.n_rows, self.n_cols))
        self.y_train = np.random.normal(0, 1, (self.n_rows))
        self.y_train_predicted = np.dot(self.A_train, self.parameters)

        self.A_test = np.random.normal(0, 1, (self.n_rows//2, self.n_cols))
        self.y_test = np.random.normal(0, 1, (self.n_rows//2))
        self.y_test_predicted = np.dot(self.A_test, self.parameters)

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_init(self):

        # init with kwargs
        alpha = 0.3
        kwargs = dict(rmse_train=5, rmse_test=4.5, R2_test=-0.12, AIC=100, BIC=-123.3)
        model = Model(parameters=self.parameters, **kwargs, alpha=alpha)
        for key in kwargs.keys():
            self.assertEqual(getattr(model, key), kwargs[key])

        # R2_train is missing from kwargs and hence should be None
        self.assertIsNone(model.R2_train)

        # alpha is not a default kwarg in Model but should still be an attribute
        self.assertEqual(model.alpha, alpha)

        # init from fit data and test reconstruct from to_dict method
        model = Model.from_fit_data(y_train=self.y_train, y_train_predicted=self.y_train_predicted,
                                    parameters=self.parameters,
                                    y_test=self.y_test, y_test_predicted=self.y_test_predicted,
                                    alpha=0.5)
        d = model.to_dict()
        model2 = Model(**d)
        for key in d.keys():
            val1 = getattr(model, key)
            val2 = getattr(model2, key)
            if key == 'parameters':
                np.testing.assert_almost_equal(val1, val2)
            else:
                self.assertEqual(val1, val2)

    def test_to_dict(self):
        model = Model.from_fit_data(y_train=self.y_train, y_train_predicted=self.y_train_predicted,
                                    parameters=self.parameters,
                                    y_test=self.y_test, y_test_predicted=self.y_test_predicted,
                                    alpha=0.5)
        d = model.to_dict()
        self.assertIn('alpha', d)

        for key, val in d.items():
            if key == 'parameters':
                np.testing.assert_almost_equal(self.parameters, val)
            else:
                self.assertEqual(getattr(model, key), val)

    def test_parameters(self):
        p = np.array([1, 2, 3, 4])
        model = Model(parameters=p)

        # parameters are correctly stored
        np.testing.assert_almost_equal(p, model.parameters)

        # parameters is stored as a copy and does not change when p is changed
        p[0] += 1
        self.assertEqual(p[0]-1, model.parameters[0])


if __name__ == '__main__':
    unittest.main()
