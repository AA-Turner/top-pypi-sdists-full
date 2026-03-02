import numpy as np
import unittest

from trainstation import CrossValidationEstimator
from trainstation.cross_validation import validation_methods


class TestCrossValidationEstimator(unittest.TestCase):
    """Unittest class for CrossValidationEstimator."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n_rows = 200
        self.n_cols = 50
        self.tol = 1.0 / self.n_rows
        self.float_tol = 1e-10

        # set up dummy linear problem data
        self.A = np.random.normal(0, 1, (self.n_rows, self.n_cols))
        self.x = np.random.normal(0, 5, (self.n_cols, ))
        self.noise = np.random.normal(0, 0.1, (self.n_rows, ))
        self.y = np.dot(self.A, self.x) + self.noise

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_init(self):
        """Tests initializing CrossValidationEstimator."""

        # assert valid cv-method
        with self.assertRaises(ValueError):
            CrossValidationEstimator((self.A, self.y), validation_method='asd')

    def test_set_kwargs(self):
        """Tests set_kwargs."""
        kwargs = dict(value1=1.0, value2=2.0, value3='3')

        # test with k-fold
        for validation_method in validation_methods.keys():
            cve = CrossValidationEstimator((self.A, self.y),
                                           validation_method=validation_method)
            cve._set_kwargs(kwargs)
            self.assertDictEqual(cve._fit_kwargs, kwargs)

    def test_train(self):
        """Tests train."""
        cve = CrossValidationEstimator((self.A, self.y))
        self.assertIsNone(cve.parameters)
        self.assertIsNone(cve.rmse_train_final)
        cve.train()
        self.assertIsNotNone(cve.parameters)
        self.assertIsNotNone(cve.rmse_train_final)

    def test_validate(self):
        """Tests validate."""
        n_splits = 7
        for validation_method in validation_methods:
            cve = CrossValidationEstimator(
                (self.A, self.y), n_splits=n_splits,
                validation_method=validation_method)

            self.assertIsNone(cve.model_splits)
            self.assertIsNone(cve.scatter_data_train)
            self.assertIsNone(cve.scatter_data_validation)
            cve.validate()
            self.assertEqual(len(cve.rmse_validation_splits), n_splits)
            self.assertEqual(len(cve.rmse_validation_splits), n_splits)
            self.assertIsNotNone(cve.scatter_data_train)
            self.assertIsNotNone(cve.scatter_data_validation)

    def test_summary_property(self):
        """Tests summary property."""

        # without having trained
        cve = CrossValidationEstimator((self.A, self.y))
        self.assertIsInstance(cve.summary, dict)

        # with having validated and trained
        cve.validate()
        cve.train()
        self.assertIsInstance(cve.summary, dict)
        self.assertIn('rmse_train', cve.summary.keys())
        self.assertIn('rmse_validation', cve.summary.keys())
        self.assertIn('R2_validation', cve.summary.keys())

    def test_repr(self):
        """Tests repr dunder."""
        cve = CrossValidationEstimator((self.A, self.y))
        self.assertIsInstance(repr(cve), str)

    def test_rmse_properties(self):
        """Tests the rmse properties."""

        # without having run anything
        cve = CrossValidationEstimator((self.A, self.y))
        self.assertIsNone(cve.rmse_train)
        self.assertIsNone(cve.rmse_train_splits)
        self.assertIsNone(cve.rmse_train_final)
        self.assertIsNone(cve.rmse_validation)
        self.assertIsNone(cve.rmse_validation_splits)
        self.assertIsNone(cve.R2_validation)

        # after validation
        cve.validate()
        self.assertIsNotNone(cve.rmse_train)
        self.assertIsNotNone(cve.rmse_train_splits)
        self.assertIsNone(cve.rmse_train_final)
        self.assertIsNotNone(cve.rmse_validation)
        self.assertIsNotNone(cve.rmse_validation_splits)
        self.assertIsNotNone(cve.R2_validation)

        # after training
        cve.train()
        self.assertIsNotNone(cve.rmse_train_splits)
        self.assertIsNotNone(cve.AIC)
        self.assertIsNotNone(cve.BIC)

    def test_split_properties(self):
        """Tests the splits properties."""
        cve = CrossValidationEstimator((self.A, self.y))
        self.assertIsNone(cve.parameters_splits)
        self.assertIsNone(cve.model_splits)
        self.assertIsNone(cve.n_nonzero_parameters_splits)

        cve.validate()
        for p, n in zip(cve.parameters_splits, cve.n_nonzero_parameters_splits):
            self.assertEqual(len(p), self.n_cols)
            self.assertEqual(n, np.count_nonzero(p))

    def test_model_splits(self):
        cve = CrossValidationEstimator((self.A, self.y), fit_method='lasso')
        cve.validate()

        # assert each CV-model has correct attributes, including alpha_optimal from lasso
        for model in cve.model_splits:
            self.assertIsNotNone(model.rmse_train)
            self.assertIsNotNone(model.rmse_test)
            self.assertIsNotNone(model.R2_train)
            self.assertIsNotNone(model.R2_test)
            self.assertIsNotNone(model.AIC)
            self.assertIsNotNone(model.BIC)
            self.assertIsNotNone(model.alpha_optimal)


if __name__ == '__main__':
    unittest.main()
