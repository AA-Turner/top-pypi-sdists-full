"""
BaseOptimizer serves as base for all optimizers.
"""

import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from .fit_methods import available_fit_methods
from .model import Model
from .oi import _write_summary_json


logger = logging.getLogger('trainstation')


class BaseOptimizer(ABC):
    r"""BaseOptimizer class.

    Serves as base class for all Optimizers solving the linear
    :math:`\boldsymbol{X}\boldsymbol{a} = \boldsymbol{y}` problem.

    Parameters
    ----------
    fit_data : tuple(numpy.ndarray, numpy.ndarray)
        the first element of the tuple represents the `NxM`-dimensional
        fit matrix `A` whereas the second element represents the
        vector of `N`-dimensional target values `y`; here `N` (=rows of
        `A`, elements of `y`) equals the number of target values and
        `M` (=columns of `A`) equals the number of parameters
    fit_method : str
        method to be used for training; possible choice are
        "ardr", "bayesian-ridge", "elasticnet", "lasso", "least-squares",
        "omp", "rfe", "ridge", "split-bregman"
    standardize : bool
        if True the fit matrix and target values are standardized before fitting,
        meaning columns in the fit matrix and th target values are rescaled to
        have a standard deviation of 1.0.
    check_condition : bool
        if True the condition number will be checked
        (this can be sligthly more time consuming for larger
        matrices)
    seed : int
        seed for pseudo random number generator
    """

    def __init__(self,
                 fit_data: Tuple[np.ndarray, np.ndarray],
                 fit_method: str,
                 standardize: bool = True,
                 check_condition: bool = True,
                 seed: int = 42):
        """
        Attributes
        ----------
        _A : numpy.ndarray
            fit matrix (N, M)
        _y : numpy.ndarray
            target values (N)
        """

        if fit_method not in available_fit_methods:
            raise ValueError(f'Unknown fit_method: {fit_method}')

        if fit_data is None:
            raise TypeError('Invalid fit data; Fit data can not be None')
        if fit_data[0].shape[0] != fit_data[1].shape[0]:
            raise ValueError('Invalid fit data; shapes of fit matrix'
                             ' and target vector do not match')
        if len(fit_data[0].shape) != 2:
            raise ValueError('Invalid fit matrix; must have two dimensions')

        self._A, self._y = fit_data
        self._n_rows = self._A.shape[0]
        self._n_cols = self._A.shape[1]
        self._fit_method = fit_method
        self._standarize = standardize
        self._check_condition = check_condition
        self._seed = seed
        self.model = Model()

        # warn if under-determined
        if self._n_cols > self._n_rows:
            logger.warning('Warning: The linear problem is underdetermined')

    def get_contributions(self, A: np.ndarray) -> np.ndarray:
        """
        Returns the average contribution for each row of `A`
        to the predicted values from each element of the parameter vector.

        Parameters
        ----------
        A
            fit matrix where `N` (=rows of `A`, elements of `y`) equals the
            number of target values and `M` (=columns of `A`) equals the number
            of parameters
        """
        return np.mean(np.abs(np.multiply(A, self.parameters)), axis=0)

    @abstractmethod
    def train(self) -> None:
        pass

    @property
    def summary(self) -> Dict[str, Any]:
        """ Comprehensive information about the optimizer """
        target_values_std = np.std(self._y)

        model_dict = self.model.to_dict()
        info = dict()  # type: Dict[str, Any]
        info['seed'] = self.seed
        info['fit_method'] = self.fit_method
        info['standardize'] = self.standardize
        info['n_target_values'] = self.n_target_values
        info['n_parameters'] = self.n_parameters
        info['n_nonzero_parameters'] = self.n_nonzero_parameters
        info['parameters_norm'] = self.parameters_norm
        info['target_values_std'] = target_values_std
        return {**info, **model_dict}

    def write_summary(self, fname: str) -> None:
        """ Writes summary dict to file. """
        _write_summary_json(fname, self.summary)

    def __str__(self) -> str:
        info = self.summary
        width = 54
        s = []
        s.append(' {} '.format(self.__class__.__name__).center(width, '='))
        for key in info.keys():
            value = info[key]
            if isinstance(value, (str, int, np.integer)):
                s.append(f'{key:30} : {value}')
            elif isinstance(value, (float, np.floating)):
                s.append(f'{key:30} : {value:.7g}')
        s.append(''.center(width, '='))
        return '\n'.join(s)

    def __repr__(self) -> str:
        return f'BaseOptimizer((A, y), {self.fit_method}, {self.seed}'

    @property
    def fit_method(self) -> str:
        """ Fit method """
        return self._fit_method

    @property
    def parameters(self) -> np.ndarray:
        """ Copy of parameter vector """
        return self.model.parameters

    @property
    def parameters_norm(self) -> float:
        """ Norm of the parameter vector """
        if self.parameters is None:
            return None
        else:
            return np.linalg.norm(self.parameters)

    @property
    def n_nonzero_parameters(self) -> int:
        """ Number of non-zero parameters """
        if self.parameters is None:
            return None
        else:
            return np.count_nonzero(self.parameters)

    @property
    def n_target_values(self) -> int:
        """ Number of target values (=rows in `A` matrix) """
        return self._n_rows

    @property
    def n_parameters(self) -> int:
        """ Number of parameters (=columns in `A` matrix) """
        return self._n_cols

    @property
    def standardize(self) -> bool:
        """ If True standardize the fit matrix before fitting """
        return self._standarize

    @property
    def seed(self) -> int:
        """ Seed used to initialize pseudo random number generator """
        return self._seed
