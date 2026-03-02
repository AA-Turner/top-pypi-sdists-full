import copy
from typing import Dict

import numpy as np
from sklearn.metrics import r2_score, mean_squared_error


class Model:
    """ Container class for a model that holds the parameter vector,
    default metrics such as the ones listed below, and additional arbitrary
    fit results.

    Attributes
    ----------
    rmse_train : float
        root-mean square-error (RMSE) over training set
    R2_train : float
        R2-score over training set
    rmse_test : float
        root-mean square-error (RMSE) over test set (if available)
    R2_test : float
        R2-score over test set (if available)
    AIC : float
        Akaike information criterion
    BIC : float
        Bayesian information criterion
    parameters
        model parameters
    """

    default_attributes = ['rmse_train', 'rmse_test', 'R2_train', 'R2_test', 'AIC', 'BIC']

    def __init__(self, **kwargs):
        """ Make empty model with just parameters """
        kwargs = copy.deepcopy(kwargs)
        self._parameters = kwargs.pop('parameters', None)

        for att in self.default_attributes:
            val = kwargs.pop(att, None)
            self.__setattr__(att, val)

        self.fit_results = kwargs
        for key, val in self.fit_results.items():
            self.__setattr__(key, val)

    def from_fit_data(y_train: np.ndarray,
                      y_train_predicted: np.ndarray,
                      parameters: np.ndarray,
                      y_test: np.ndarray = None,
                      y_test_predicted: np.ndarray = None,
                      **fit_results):
        """
        Initialize model class fit data and parameters.

        Parameters
        ----------
        y_train
            target values used to train model
        y_train_predicted
            predicted values from model over the training set
        parameters
            obtained parameters
        fit_results
            dict with complementary information results (such as hyper-parameters etc)
        """

        # model metrics
        model_dict = _get_model_metrics(y_train, y_train_predicted, parameters)
        model_dict['parameters'] = parameters
        model_dict.update(fit_results)

        # if test data available
        if y_test is not None:
            if y_test_predicted is None:
                raise ValueError('Specify both y_test and y_test_predicted (or neither)')
            model_dict['rmse_test'] = compute_rmse(y_test, y_test_predicted)
            model_dict['R2_test'] = r2_score(y_test, y_test_predicted)

        # get model object
        model = Model(**model_dict)
        return model

    def to_dict(self) -> dict:
        """Return model parameters as dict."""
        model_dict = dict(parameters=self.parameters)
        for att in self.default_attributes:
            model_dict[att] = getattr(self, att)
        return {**model_dict, **self.fit_results}

    @property
    def parameters(self):
        if self._parameters is None:
            return None
        return self._parameters.copy()

    def __repr__(self):
        return str(self.to_dict())


def _get_model_metrics(y_target: np.ndarray,
                       y_predicted: np.ndarray,
                       parameters: np.ndarray) -> Dict[str, float]:
    """
    Calculates various model metrics including AIC, BIC, RMSE and R2 scores.

    Parameters
    ----------
    y_target
        target values used to train model
    y_predicted
        predicted values from model over the training set
    parameters
        model parameters
    """
    n_samples = len(y_target)
    n_parameters = np.count_nonzero(parameters)

    # evaluate Information Criterias
    mse = mean_squared_error(y_target, y_predicted)
    aic = get_aic(mse, n_samples, n_parameters)
    bic = get_bic(mse, n_samples, n_parameters)

    # r2 and rmse scores
    r2 = r2_score(y_target, y_predicted)
    rmse = compute_rmse(y_target, y_predicted)

    # summarize
    metrics = dict(rmse_train=rmse,
                   R2_train=r2,
                   AIC=aic,
                   BIC=bic)
    return metrics


def compute_rmse(y_target, y_predicted):
    """Calculates the root mean square error.

    Parameters
    ----------
    y_target
        target values
    y_predicted
        predicted values
    """
    return np.sqrt(mean_squared_error(y_target, y_predicted))


def get_aic(mse: float,
            n_samples: int,
            n_parameters: int) -> float:
    """Returns the Akaike information criterion (AIC).

    Parameters
    ----------
    mse
        mean square error
    n_samples
        number of samples
    n_parameters
        number of parameters
    """
    aic = n_samples * np.log(mse) + 2 * n_parameters
    return aic


def get_bic(mse: float,
            n_samples: int,
            n_parameters: int) -> float:
    """Returns the Bayesian information criterion (BIC).

    Parameters
    ----------
    mse
        mean square error
    n_samples
        number of samples
    n_parameters
        number of parameters
    """
    bic = n_samples * np.log(mse) + n_parameters * np.log(n_samples)
    return bic


def estimate_loocv(A: np.ndarray,
                   y_target: np.ndarray,
                   y_predicted: np.ndarray) -> float:
    """Calculates the approximative leave-one-out cross-validation
    (LOO-CV) root mean square error (RMSE).

    Parameters
    ----------
    A
        Matrix in OLS problem y=Ax, needs to be invertible (=linearly independent)
    y_target
        target values
    y_predicted
        predicted values
    """
    n_rows, n_cols = A.shape
    if n_cols > n_rows:
        raise ValueError('Matrix is underdetermined')

    H = A.dot(np.linalg.inv(A.T.dot(A))).dot(A.T)
    e = (y_target - y_predicted) / (1 - np.diag(H))

    return np.linalg.norm(e) / np.sqrt(len(e))
