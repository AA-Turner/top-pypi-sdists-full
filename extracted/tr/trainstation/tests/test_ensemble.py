import numpy as np
import unittest
from trainstation import EnsembleOptimizer


class TestEnsemble(unittest.TestCase):
    """Unittest class for EnsembleOptimizer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n_rows = 200
        self.n_cols = 50

        # set up dummy linear problem data
        self.A = np.random.normal(0, 1, (self.n_rows, self.n_cols))
        self.x = np.random.normal(0, 5, (self.n_cols, ))
        self.noise = np.random.normal(0, 0.1, (self.n_rows, ))
        self.y = np.dot(self.A, self.x) + self.noise

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_init(self):
        """Tests init."""

        # specify train size via integer
        train_size = int(0.7*self.n_rows)
        EnsembleOptimizer((self.A, self.y), train_size=train_size)

        # specify train size as fraction
        train_size = 0.7
        EnsembleOptimizer((self.A, self.y), train_size=train_size)

        # raise otherwise
        train_size = '50'
        with self.assertRaises(TypeError):
            EnsembleOptimizer((self.A, self.y), train_size=train_size)

    def test_train(self):
        """Tests training of ensemble models."""

        size = 11
        eopt = EnsembleOptimizer((self.A, self.y), ensemble_size=size)

        self.assertIsNone(eopt._train_set_splits)
        self.assertIsNone(eopt._test_set_splits)
        self.assertIsNone(eopt.model_splits)
        self.assertIsNone(eopt.parameters)

        eopt.train()

        # check parameters
        self.assertEqual(len(eopt.model_splits), size)
        self.assertEqual(len(eopt.parameters), self.n_cols)
        self.assertEqual(len(eopt.parameters_std), self.n_cols)
        self.assertEqual(eopt.parameters_splits.shape, (size, self.n_cols))

        # check train and test set splits
        self.assertIsNotNone(eopt._train_set_splits)
        self.assertEqual(len(eopt._train_set_splits), size)

        self.assertIsNotNone(eopt._test_set_splits)
        self.assertEqual(len(eopt._test_set_splits), size)

        # check rmse properties
        self.assertIsNotNone(eopt.rmse_train)
        self.assertEqual(len(eopt.rmse_train_splits), size)
        self.assertIsNotNone(eopt.rmse_test)
        self.assertEqual(len(eopt.rmse_test_splits), size)

    def test_error_matrix(self):
        """Tests error_matrix property."""
        ensemble_size = 50
        eopt = EnsembleOptimizer((self.A, self.y), ensemble_size=ensemble_size)
        eopt.train()
        error_matrix = eopt.error_matrix
        self.assertEqual(error_matrix.shape, (self.n_rows, ensemble_size))

    def test_predict(self):
        """Tests predict."""
        ensemble_size = 50
        eopt = EnsembleOptimizer((self.A, self.y), ensemble_size=ensemble_size)
        eopt.train()

        # test correct output from predict
        predictions = eopt.predict(self.A)
        self.assertEqual(predictions.shape, (self.n_rows,))

        # test correct output from matrix predict with return_std
        predictions, stds = eopt.predict(self.A, return_std=True)
        self.assertSequenceEqual(predictions.shape, (self.n_rows,))
        self.assertSequenceEqual(stds.shape, (self.n_rows,))

        # test correct output from row predict with return_std
        predictions, stds = eopt.predict(self.A[0], return_std=True)
        self.assertIsInstance(predictions, float)
        self.assertIsInstance(stds, float)

    def test_summary_property(self):
        """Tests summary property."""

        # without having trained
        eopt = EnsembleOptimizer((self.A, self.y))
        self.assertIsInstance(eopt.summary, dict)

        # with having trained
        eopt.train()
        self.assertIsInstance(eopt.summary, dict)
        self.assertIn('rmse_train', eopt.summary.keys())
        self.assertIn('rmse_test', eopt.summary.keys())
        self.assertIn('parameters_std', eopt.summary.keys())

    def test_repr(self):
        """Tests repr dunder."""
        opt = EnsembleOptimizer((self.A, self.y))
        self.assertIsInstance(repr(opt), str)


if __name__ == '__main__':
    unittest.main()
