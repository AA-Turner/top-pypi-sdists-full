"""
Optimizer with cross validation score
"""

import numpy as np
from sklearn.model_selection import KFold, ShuffleSplit
from typing import Any, Dict, Tuple
from .base_optimizer import BaseOptimizer
from .optimizer import Optimizer
from .tools import ScatterData


validation_methods = {
    'k-fold': KFold,
    'shuffle-split': ShuffleSplit,
}


class CrossValidationEstimator(BaseOptimizer):
    r"""
    This class provides an optimizer with cross validation for solving the
    linear :math:`\boldsymbol{A}\boldsymbol{x} = \boldsymbol{y}` problem.
    Cross-validation (CV) scores are calculated by splitting the
    available reference data in multiple different ways.  It also produces
    the finalized model (using the full input data) for which the CV score
    is an estimation of its performance.

    Warning
    -------
    Repeatedly setting up a :class:`CrossValidationEstimator` and training
    *without* changing the seed for the random number generator will yield
    identical or correlated results, to avoid this please specify a different
    seed when setting up multiple :class:`CrossValidationEstimator` instances.

    Parameters
    ----------
    fit_data : tuple(numpy.ndarray, numpy.ndarray)
        the first element of the tuple represents the fit matrix `A`
        (`N, M` array) while the second element represents the vector
        of target values `y` (`N` array); here `N` (=rows of `A`,
        elements of `y`) equals the number of target values and `M`
        (=columns of `A`) equals the number of parameters
    fit_method : str
        method to be used for training; possible choice are
        "ardr", "bayesian-ridge", "elasticnet", "lasso", "least-squares",
        "omp", "rfe", "ridge", "split-bregman"
    standardize : bool
        if True the fit matrix and target values are standardized before fitting,
        meaning columns in the fit matrix and th target values are rescaled to
        have a standard deviation of 1.0.
    validation_method : str
        method to use for cross-validation; possible choices are
        "shuffle-split", "k-fold"
    n_splits : int
        number of times the fit data set will be split for the cross-validation
    check_condition : bool
        if True the condition number will be checked
        (this can be sligthly more time consuming for larger
        matrices)
    seed : int
        seed for pseudo random number generator

    Attributes
    ----------
    scatter_data_train : ScatterData
        contains target and predicted values from each individual
        traininig set in the cross-validation split
    scatter_data_validation : ScatterData
        contains target and predicted values from each individual
        validation set in the cross-validation split
    """

    def __init__(self,
                 fit_data: Tuple[np.ndarray, np.ndarray],
                 fit_method: str = 'least-squares',
                 standardize: bool = True,
                 validation_method: str = 'k-fold',
                 n_splits: int = 10,
                 check_condition: bool = True,
                 seed: int = 42,
                 **kwargs) -> None:

        super().__init__(fit_data, fit_method, standardize, check_condition, seed)

        if validation_method not in validation_methods.keys():
            msg = ['Validation method not available']
            msg += ['Please choose one of the following:']
            for key in validation_methods:
                msg += [' * ' + key]
            raise ValueError('\n'.join(msg))
        self._validation_method = validation_method
        self._n_splits = n_splits
        self._set_kwargs(kwargs)

        # data set splitting object
        self._splitter = validation_methods[validation_method](
            n_splits=self.n_splits, random_state=seed, **self._split_kwargs)

        self.scatter_data_train = None
        self.scatter_data_validation = None
        self.model_splits = None

    def train(self) -> None:
        """ Constructs the final model using all input data available. """
        opt = Optimizer((self._A, self._y), self.fit_method,
                        standardize=self.standardize,
                        train_size=1.0,
                        check_condition=self._check_condition,
                        **self._fit_kwargs)
        opt.train()
        self.model = opt.model

    def validate(self) -> None:
        """ Runs validation. """
        self.scatter_data_train = ScatterData()
        self.scatter_data_validation = ScatterData()
        self.model_splits = []
        for train_set, test_set in self._splitter.split(self._A):
            opt = Optimizer((self._A, self._y), self.fit_method,
                            standardize=self.standardize,
                            train_set=train_set,
                            test_set=test_set,
                            check_condition=self._check_condition,
                            **self._fit_kwargs)
            opt.train()
            self.model_splits.append(opt.model)

            self.scatter_data_train += opt.scatter_data_train
            self.scatter_data_validation += opt.scatter_data_test

    def _set_kwargs(self, kwargs: dict) -> None:
        """
        Sets up fit_kwargs and split_kwargs.
        Different split methods need different keywords.
        """
        self._fit_kwargs = {}
        self._split_kwargs = {}

        if self.validation_method == 'k-fold':
            self._split_kwargs['shuffle'] = True  # default True
            for key, val in kwargs.items():
                if key in ['shuffle']:
                    self._split_kwargs[key] = val
                else:
                    self._fit_kwargs[key] = val
        elif self.validation_method == 'shuffle-split':
            for key, val in kwargs.items():
                if key in ['test_size', 'train_size']:
                    self._split_kwargs[key] = val
                else:
                    self._fit_kwargs[key] = val

    @property
    def summary(self) -> Dict[str, Any]:
        """ Comprehensive information about the optimizer """

        info = super().summary

        # add model metrics
        info = {**info, **self.model.to_dict()}

        # Add class specific data
        info['validation_method'] = self.validation_method
        info['n_splits'] = self.n_splits
        info['rmse_train'] = self.rmse_train
        info['rmse_train_final'] = self.rmse_train_final
        info['rmse_train_splits'] = self.rmse_train_splits
        info['rmse_validation'] = self.rmse_validation
        info['R2_validation'] = self.R2_validation
        info['rmse_validation_splits'] = self.rmse_validation_splits
        info['scatter_data_train'] = self.scatter_data_train
        info['scatter_data_validation'] = self.scatter_data_validation

        # add kwargs used for fitting and splitting
        info = {**info, **self._fit_kwargs, **self._split_kwargs}
        return info

    def __repr__(self) -> str:
        kwargs = dict()
        kwargs['fit_method'] = self.fit_method
        kwargs['validation_method'] = self.validation_method
        kwargs['n_splits'] = self.n_splits
        kwargs['seed'] = self.seed
        kwargs = {**kwargs, **self._fit_kwargs, **self._split_kwargs}
        return 'CrossValidationEstimator((A, y), {})'.format(
            ', '.join('{}={}'.format(*kwarg) for kwarg in kwargs.items()))

    @property
    def validation_method(self) -> str:
        """ Validation method name """
        return self._validation_method

    @property
    def n_splits(self) -> int:
        """ Number of splits (folds) used for cross-validation """
        return self._n_splits

    @property
    def parameters_splits(self) -> np.ndarray:
        """ All parameters obtained during cross-validation """
        if self.model_splits is None:
            return None
        else:
            return np.array([model.parameters for model in self.model_splits])

    @property
    def n_nonzero_parameters_splits(self) -> np.ndarray:
        """ Number of non-zero parameters for each split """
        if self.model_splits is None:
            return None
        else:
            return np.array([np.count_nonzero(p) for p in self.parameters_splits])

    @property
    def rmse_train_final(self) -> float:
        """ Root mean squared error when using the full set of input data """
        if self.model is None:
            return None
        else:
            return self.model.rmse_train

    @property
    def rmse_train(self) -> float:
        """ Average root mean squared training error obtained during cross-validation """
        if self.model_splits is None:
            return None
        else:
            return np.mean(self.rmse_train_splits)

    @property
    def rmse_train_splits(self) -> np.ndarray:
        """ Root mean squared training errors obtained during cross-validation """
        if self.model_splits is None:
            return None
        else:
            return np.array([model.rmse_train for model in self.model_splits])

    @property
    def rmse_validation(self) -> float:
        """ Average root mean squared cross-validation error """
        if self.model_splits is None:
            return None
        else:
            return np.mean(self.rmse_validation_splits)

    @property
    def R2_validation(self) -> float:
        """ Average R2 score for validation sets """
        if self.model_splits is None:
            return None
        else:
            return np.mean([model.R2_test for model in self.model_splits])

    @property
    def rmse_validation_splits(self) -> np.ndarray:
        """ Root mean squared validation errors obtained during cross-validation """
        if self.model_splits is None:
            return None
        else:
            return np.array([model.rmse_test for model in self.model_splits])

    @property
    def AIC(self) -> float:
        """ Akaike information criterion (AIC) for the model """
        return self.model.AIC

    @property
    def BIC(self) -> float:
        """ Bayesian information criterion (BIC) for the model """
        return self.model.BIC
