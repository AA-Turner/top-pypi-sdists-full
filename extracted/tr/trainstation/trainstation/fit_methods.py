"""
scikit-learn is an excellent library for training linear models and provides a
large number of useful tools.

This module provides simplified interfaces for vaiours linear model regression
methods. These methods are set up in a way that work out of the box for typical
problems in cluster expansion and force constant potential construction. This
includes slight adjustments scitkit-learn default values.

If you would like more flexibility or extended functionality or ability to
fine-tune parameters that are not included in this interface, it is of course
possible to use scikit-learn directly.
More information about the sklearn linear models can be found at
http://scikit-learn.org/stable/modules/linear_model.html
"""

import numpy as np
import logging
import warnings
from collections import OrderedDict
from sklearn.base import BaseEstimator
from sklearn.linear_model import (
    Lasso,
    LassoCV,
    Ridge,
    OrthogonalMatchingPursuit,
    OrthogonalMatchingPursuitCV,
    RidgeCV,
    ElasticNet,
    ElasticNetCV,
    BayesianRidge,
    ARDRegression,
)
from sklearn.model_selection import ShuffleSplit
from sklearn.feature_selection import RFE, RFECV
from sklearn.preprocessing import StandardScaler
from typing import Any, Dict, List, Union
from .split_bregman import fit_split_bregman


logger = logging.getLogger('trainstation')


def fit(X: np.ndarray,
        y: np.ndarray,
        fit_method: str,
        standardize: bool = True,
        check_condition: bool = True,
        **kwargs) -> Dict[str, Any]:
    """
    Wrapper function for all available fit methods.  The function
    returns parameters and other pertinent information in the form of
    a dictionary.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    fit_method
        method to be used for training; possible choice are
        "least-squares", "lasso", "elasticnet", "bayesian-ridge", "ardr",
        "rfe", "split-bregman"
    standardize : bool
        if True the fit matrix is standardized before fitting
    check_condition : bool
        if True the condition number will be checked
        (this can be sligthly more time consuming for larger
        matrices)
    """

    if fit_method not in available_fit_methods:
        msg = ['Fit method not available']
        msg += ['Please choose one of the following:']
        for key in available_fit_methods:
            msg += [' * ' + key]
        raise ValueError('\n'.join(msg))

    if check_condition and X.shape[0] >= X.shape[1]:
        cond = np.linalg.cond(X)
        if cond > 1e10:
            warnings.warn(f'Warning: Condition number is large, {cond}')

    if standardize:

        # standardize fit matrix, column wise std -> 1.0
        ss = StandardScaler(copy=False, with_mean=False, with_std=True)
        ss.fit_transform(X)  # change in place

        # standardize target values, std(y) -> 1.0
        y_scale = 1.0/np.std(y)
        y_rescaled = y * y_scale

        if fit_method == 'least-squares-with-reg-matrix' and 'reg_matrix' in kwargs:
            # scale regularization matrix
            transf_matrix = 1/ss.scale_*np.eye(X.shape[1])
            kwargs['reg_matrix'] = np.dot(transf_matrix,
                                          np.dot(kwargs['reg_matrix'], transf_matrix))

        # train
        results = fit_methods[fit_method](X, y_rescaled, **kwargs)

        # inverse standardization
        parameters = results['parameters'] / y_scale
        ss.inverse_transform(X)  # change in place
        ss.transform(parameters.reshape(1, -1)).reshape(-1,)
        if fit_method == 'least-squares-with-reg-matrix' and 'reg_matrix' in kwargs:
            transf_matrix_inv = np.linalg.pinv(transf_matrix)
            kwargs['reg_matrix'] = np.dot(transf_matrix_inv,
                                          np.dot(kwargs['reg_matrix'], transf_matrix_inv))
        results['parameters'] = parameters

    else:
        results = fit_methods[fit_method](X, y, **kwargs)
    return results


def _fit_least_squares(X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """
    Returns the least-squares solution `a` to the linear problem
    `Xa=y` in the form of a dictionary with a key named `parameters`.

    This function is a wrapper to the `linalg.lstsq` function in NumPy.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    """
    results = dict()
    results['parameters'] = np.linalg.lstsq(X, y, rcond=-1)[0]
    return results


def _fit_least_squares_with_reg_matrix(X: np.ndarray,
                                       y: np.ndarray,
                                       reg_matrix: np.ndarray = None) -> Dict[str, Any]:
    """
    Returns the regularized least-squares solution `a` to the linear problem
    `Xa=y` with an explicit regularization matrix `L` in the form of a dictionary
    with a key named `parameters`. The solution is found by minimizing

        (y  - Xa)'(y  - Xa) + a'La,

    which yields

        a = (X'X + L)^(-1) X'y.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    reg_matrix
        regularization matrix
    """
    if reg_matrix is None:
        logger.warning('Warning: No regularization matrix specified, consider using OLS')
        reg_matrix = np.zeros((X.shape[1], X.shape[1]))

    XT_X = np.dot(X.T, X)
    XT_y = np.dot(X.T, y)

    results = dict()
    results['parameters'] = np.dot(np.linalg.pinv(XT_X + reg_matrix), XT_y)

    return results


def _fit_lasso(X: np.ndarray, y: np.ndarray,
               alpha: float = None, fit_intercept: bool = False,
               **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by
    using the LASSO method as implemented in scitkit-learn in the form
    of a dictionary with a key named `parameters`.

    LASSO optimizes the following problem::

        (1 / (2 * n_samples)) * ||y - Xw||^2_2 + alpha * ||w||_1

    If `alpha` is `None` this function will call `fit_lassoCV` which attempts
    to find the optimal alpha via sklearn's `LassoCV` class.

    Parameters
    ----------
    X
        fit matrix
    y
        target array
    alpha
        alpha value
    fit_intercept
        center data or not, forwarded to sklearn
    """
    if alpha is None:
        return _fit_lassoCV(X, y, fit_intercept=fit_intercept, **kwargs)
    else:
        lasso = Lasso(alpha=alpha, fit_intercept=fit_intercept, **kwargs)
        lasso.fit(X, y)
        results = dict()
        results['parameters'] = lasso.coef_
        return results


def _fit_lassoCV(X: np.ndarray,
                 y: np.ndarray,
                 alphas: List[float] = None,
                 fit_intercept: bool = False,
                 cv: int = 10,
                 n_jobs: int = -1,
                 **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by
    using the LassoCV method as implemented in scitkit-learn in the
    form of a dictionary with a key named `parameters`.

    The dictionary will also contain the keys `alpha_optimal` (alpha
    value that yields the lowest validation RMSE), `alpha_path` (all
    tested alpha values), and `mse_path` (MSE for validation set for
    each alpha).

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    alphas
        list of alpha values to be evaluated during regularization path
    fit_intercept
        center data or not, forwarded to sklearn
    cv
        how many folds to carry out in cross-validation
    n_jobs
        number of cores to use during the cross validation.
        None means 1 unless in a joblib.parallel_backend context.
        -1 means using all processors.
        See sklearn's glossary for more details.
    """
    if alphas is None:
        alphas = np.logspace(-8, -0.3, 100)

    lassoCV = LassoCV(alphas=alphas, fit_intercept=fit_intercept, cv=cv, n_jobs=n_jobs, **kwargs)
    lassoCV.fit(X, y)
    results = dict()
    results['parameters'] = lassoCV.coef_
    results['alpha_optimal'] = lassoCV.alpha_
    return results


def _fit_adaptive_lasso(X, y, stop_tol=1e-5, n_lasso_iters=30, alpha=None, verbose=False, **kwargs):
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by
    using an adaptive LASSO method.

    Parameters
    ----------
    X
        fit matrix
    y
        target array
    alpha
        alpha value
    stop_tol
        Optimization stops if change in parameters are less than stop_tol between two iterations
    lasso_iter
        number of LASSO fits to carry out
    """

    def update_weights(x):
        return 1 / (2 * np.sqrt(np.abs(x)) + 1e-12)

    # line scan
    if alpha is None:
        return _fit_adaptive_lasso_line_scan(
            X, y, n_lasso_iters=n_lasso_iters, stop_tol=stop_tol, verbose=verbose, **kwargs)

    # adaptive-lasso fit
    n_cols = X.shape[1]
    weights = np.ones(n_cols)
    x = np.zeros(n_cols)

    for it in range(n_lasso_iters):
        X_w = X / weights.reshape(1, -1)
        lasso = Lasso(alpha=alpha, fit_intercept=False, **kwargs)
        lasso.fit(X_w, y)

        x_new = lasso.coef_ / weights
        dx = np.linalg.norm(x_new - x)
        x = x_new
        weights = update_weights(x)

        if verbose:
            print('adaptive-lasso  iter {:3d},  |x|: {:11.8f},  |dx|: {:11.8f},  |dx|/|x|: {:11.8f}'
                  .format(it, np.linalg.norm(x), dx, dx/np.linalg.norm(x)))

        if dx < stop_tol:
            break

    results = dict(parameters=x, weights=weights)
    return results


def _fit_adaptive_lasso_line_scan(X: np.ndarray,
                                  y: np.ndarray,
                                  cv_splits: int = 5,
                                  alphas: List[float] = None,
                                  **kwargs) -> Dict[str, Any]:
    """Adaptive-lasso with line-scan for optimal alpha.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    alphas
        list of alpha values to be evaluated. The optimal
        alpha found will be used in the final fit.
    cv_splits
        how many CV splits to carry out when evaluating each lambda value.
    """
    from .cross_validation import CrossValidationEstimator

    # default lambda values to scan
    if alphas is None:
        alphas = np.logspace(-7, -1, 15)

    # run lin-scan of lambda values
    cv_data = []
    for alpha in alphas:
        cve = CrossValidationEstimator((X, y), fit_method='adaptive-lasso',
                                       validation_method='shuffle-split',
                                       alpha=alpha, test_size=0.1, train_size=0.9,
                                       n_splits=cv_splits, **kwargs)
        cve.validate()
        print('adaptive-lasso   alpha {},  cv-rmse {:11.8f}'.format(alpha, cve.rmse_validation))
        cv_data.append([alpha, cve.rmse_validation])

    # select best lambda
    cv_data = np.array(cv_data)
    optimal_ind = cv_data[:, 1].argmin()
    alpha_optimal = cv_data[optimal_ind, 0]

    # final fit with optimal lambda
    results = _fit_adaptive_lasso(X, y, alpha=alpha_optimal, **kwargs)
    results['alpha_optimal'] = alpha_optimal
    return results


def _fit_ridge(X, y, alpha=None, fit_intercept=False, **kwargs):
    results = dict()
    if alpha is None:
        if 'alphas' not in kwargs:
            kwargs['alphas'] = np.logspace(-6, 3, 100)
        ridge = RidgeCV(fit_intercept=fit_intercept, **kwargs)
        ridge.fit(X, y)
        results['alpha_optimal'] = ridge.alpha_
    else:
        ridge = Ridge(alpha=alpha, fit_intercept=fit_intercept, **kwargs)
        ridge.fit(X, y)
    results['parameters'] = ridge.coef_
    return results


def _fit_bayesian_ridge(X: np.ndarray, y: np.ndarray,
                        fit_intercept: bool = False,
                        **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by using
    Bayesian ridge regression as implemented in scitkit-learn in the
    form of a dictionary with a key named `parameters`.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    fit_intercept
        center data or not, forwarded to sklearn
    """
    brr = BayesianRidge(fit_intercept=fit_intercept, **kwargs)
    brr.fit(X, y)
    results = dict()
    results['parameters'] = brr.coef_
    return results


def _fit_elasticnet(X: np.ndarray, y: np.ndarray,
                    alpha: float = None, fit_intercept: bool = False,
                    **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by using
    the ElasticNet method as implemented in scitkit-learn in the
    form of a dictionary with a key named `parameters`.

    If `alpha` is `None` this function will call the fit_lassoCV which attempts
    to find the optimal alpha via sklearn ElasticNetCV class.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    alpha
        alpha value
    fit_intercept
        center data or not, forwarded to sklearn
    """
    if alpha is None:
        return _fit_elasticnetCV(X, y, fit_intercept=fit_intercept, **kwargs)
    else:
        elasticnet = ElasticNet(alpha=alpha, fit_intercept=fit_intercept, **kwargs)
        elasticnet.fit(X, y)
        results = dict()
        results['parameters'] = elasticnet.coef_
        return results


def _fit_elasticnetCV(X: np.ndarray,
                      y: np.ndarray,
                      alphas: List[float] = None,
                      l1_ratio: Union[float, List[float]] = None,
                      fit_intercept: bool = False,
                      cv: int = 10,
                      n_jobs: int = -1,
                      **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by using
    the ElasticNetCV method as implemented in scitkit-learn in the
    form of a dictionary with a key named `parameters`.

    The dictionary returned by this function will also contain the
    fields `alpha_optimal` (alpha value that yields the lowest
    validation RMSE), `alpha_path` (all tested alpha values),
    `l1_ratio_optmal` (alpha value that yields the lowest validation
    RMSE), `l1_ratio_path` (all tested `l1_ratio` values) `mse_path`
    (MSE for validation set for each alpha and `l1_ratio`)

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    alphas
        list of alpha values to be evaluated during regularization path
    l1_ratio
        l1_ratio values to be evaluated during regularization path
    fit_intercept
        center data or not, forwarded to sklearn
    cv
        how many folds to carry out in cross-validation
    n_jobs
        number of cores to use during the cross validation.
        None means 1 unless in a joblib.parallel_backend context.
        -1 means using all processors.
        See sklearn's glossary for more details.
    """

    if alphas is None:
        alphas = np.logspace(-8, -0.3, 100)
    if l1_ratio is None:
        l1_ratio = [1.0, 0.995, 0.99, 0.98, 0.97, 0.95, 0.925, 0.9, 0.85,
                    0.8, 0.75, 0.65, 0.5, 0.4, 0.25, 0.1]

    elasticnetCV = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratio, cv=cv,
                                fit_intercept=fit_intercept, n_jobs=n_jobs, **kwargs)
    elasticnetCV.fit(X, y)
    results = dict()
    results['parameters'] = elasticnetCV.coef_
    results['alpha_optimal'] = elasticnetCV.alpha_
    results['l1_ratio_optimal'] = elasticnetCV.l1_ratio_
    return results


def _fit_ardr(X: np.ndarray,
              y: np.ndarray,
              threshold_lambda: float = None,
              line_scan: bool = False,
              fit_intercept: bool = False,
              **kwargs) -> Dict[str, Any]:
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by
    using the automatic relevance determination regression (ARDR)
    method as implemented in scitkit-learn in the form of a dictionary
    with a key named `parameters`.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    threshold_lambda
        threshold lambda parameter forwarded to sklearn
    line_scan
        whether or not to perform line-scan in order to find optimal
        threshold-lambda
    fit_intercept
        center data or not, forwarded to sklearn
    """

    if threshold_lambda is not None and line_scan:
        raise ValueError('Specify threshold_lambda or set line_scan=True, not both')

    if threshold_lambda is None:
        threshold_lambda = 1e4

    if line_scan:
        return _fit_ardr_line_scan(X, y, fit_intercept=fit_intercept, **kwargs)
    else:
        ardr = ARDRegression(threshold_lambda=threshold_lambda, fit_intercept=fit_intercept,
                             **kwargs)
        ardr.fit(X, y)
        results = dict()
        results['parameters'] = ardr.coef_
        return results


def _fit_ardr_line_scan(X: np.ndarray,
                        y: np.ndarray,
                        cv_splits: int = 1,
                        threshold_lambdas: List[float] = None,
                        **kwargs) -> Dict[str, Any]:
    """ ARDR with line-scan for optimal threshold-lambda.

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    threshold_lambdas
        list of threshold-lambda values to be evaluated. The optimal
        lambda-value found will be used in the final fit.
    cv_splits
        how many CV splits to carry out when evaluating each lambda value.
    """
    from .cross_validation import CrossValidationEstimator

    # default lambda values to scan
    if threshold_lambdas is None:
        threshold_lambdas = np.logspace(3, 6, 15)

    # run lin-scan of lambda values
    cv_data = []
    for lam in threshold_lambdas:
        cve = CrossValidationEstimator((X, y), fit_method='ardr', validation_method='shuffle-split',
                                       threshold_lambda=lam, test_size=0.1, train_size=0.9,
                                       n_splits=cv_splits, **kwargs)
        cve.validate()
        cv_data.append([lam, cve.rmse_validation])

    # select best lambda
    cv_data = np.array(cv_data)
    optimal_ind = cv_data[:, 1].argmin()
    lambda_optimal = cv_data[optimal_ind, 0]

    # final fit with optimal lambda
    results = _fit_ardr(X, y, threshold_lambda=lambda_optimal, **kwargs)
    results['threshold_lambda_optimal'] = lambda_optimal
    return results


class _Estimator(BaseEstimator):
    """ Estimator class making it possible to use all fit methods
    as estimators in RFE """

    def __init__(self, fit_method, **kwargs):
        if fit_method == 'rfe':
            raise ValueError('recursive infinitum')
        self.fit_method = fit_method
        self.kwargs = kwargs
        self.coef_ = None

    def fit(self, X, y):
        fit_func = fit_methods[self.fit_method]
        results = fit_func(X, y, **self.kwargs)
        self.coef_ = results['parameters']

    def get_params(self, deep=True):
        params = {k: v for k, v in self.kwargs.items()}
        params['fit_method'] = self.fit_method
        return params

    def predict(self, A):
        return np.dot(A, self.coef_)

    def _get_tags(self):
        from sklearn.base import _DEFAULT_TAGS
        return _DEFAULT_TAGS


def _fit_rfe(X: np.ndarray,
             y: np.ndarray,
             n_features: int = None,
             step: Union[int, float] = 0.04,
             estimator: str = 'least-squares',
             final_estimator: str = None,
             estimator_kwargs: dict = {},
             final_estimator_kwargs: dict = {},
             cv_splits: int = 5,
             n_jobs: int = -1,
             **rfe_kwargs):
    """
    Returns the solution `a` to the linear problem `Xa=y` obtained by
    recursive feature elimination (RFE).

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    n_features
        number of features to select, if None sklearn.feature_selection.RFECV
        will be used to determine the optimal number of features
    step
        if given as integer then corresponds to number of parameters to
        eliminate in each iteration. If given as a float then corresponds to
        the fraction of parameters to remove each iteration.
    estimator
        fit method during RFE algorithm
    final_estimator
        fit_method to be used in final fit,
        if None will default to whichever estimator is being used
    cv_splits
        number of 90/10 shuffle-split cv-splits to carry out if finding optimal n_features
    n_jobs
        number of cores to use during the cross validation.
        -1 means using all processors.
    """

    # handle kwargs
    if final_estimator is None:
        final_estimator = estimator
        if len(final_estimator_kwargs) == 0:
            final_estimator_kwargs = estimator_kwargs

    estimator_obj = _Estimator(estimator, **estimator_kwargs)
    if n_features is None:
        if 'scoring' not in rfe_kwargs:
            rfe_kwargs['scoring'] = 'neg_mean_squared_error'
        cv = ShuffleSplit(train_size=0.9, test_size=0.1, n_splits=cv_splits)
        rfe = RFECV(estimator_obj, step=step, cv=cv, n_jobs=n_jobs, **rfe_kwargs)
    else:
        rfe = RFE(estimator_obj, n_features_to_select=n_features, step=step, **rfe_kwargs)

    # Carry out RFE
    rfe.fit(X, y)
    features = rfe.support_
    ranking = rfe.ranking_

    # carry out final fit
    # NOTE/TODO: final fit will not automatically use the same standardize/check_condition as RFE
    n_params = X.shape[1]
    results = fit(X[:, features], y, fit_method=final_estimator, **final_estimator_kwargs)
    params = np.zeros(n_params)
    params[features] = results['parameters']
    results['parameters'] = params

    # finish up
    results['features'] = features
    results['ranking'] = ranking
    return results


def _fit_omp(X: np.ndarray, y: np.ndarray,
             n_nonzero_coefs: int = None, fit_intercept: bool = False,
             cv_splits: int = 5,
             n_jobs: int = -1,
             **kwargs) -> Dict[str, Any]:
    """
    Fitting using Orthogonal Matching Pursuit (OMP) see
    https://scikit-learn.org/stable/modules/linear_model.html#omp

    Parameters
    -----------
    X
        fit matrix
    y
        target array
    n_nonzero_coefs
        number of non-zero parameters to obtain, if None will find the
        optimal number via CV
    cv_splits
        number of cv-splits to carry out if finding optimal n_features
    n_jobs
        number of cores to use during the cross validation.
        -1 means using all processors.
    """

    if n_nonzero_coefs is None:
        n_cols = X.shape[1]
        cv = ShuffleSplit(train_size=0.9, test_size=0.1, n_splits=cv_splits)
        ompcv = OrthogonalMatchingPursuitCV(
            fit_intercept=fit_intercept, max_iter=n_cols, cv=cv, n_jobs=n_jobs, **kwargs)
        ompcv.fit(X, y)
        parameters = ompcv.coef_
    else:
        omp = OrthogonalMatchingPursuit(
            n_nonzero_coefs=n_nonzero_coefs, fit_intercept=fit_intercept, **kwargs)
        omp.fit(X, y)
        parameters = omp.coef_

    results = dict()
    results['parameters'] = parameters
    return results


fit_methods = OrderedDict([
    ('least-squares', _fit_least_squares),
    ('least-squares-with-reg-matrix', _fit_least_squares_with_reg_matrix),
    ('lasso', _fit_lasso),
    ('ridge', _fit_ridge),
    ('omp', _fit_omp),
    ('bayesian-ridge', _fit_bayesian_ridge),
    ('elasticnet', _fit_elasticnet),
    ('split-bregman', fit_split_bregman),
    ('ardr', _fit_ardr),
    ('adaptive-lasso', _fit_adaptive_lasso),
    ('rfe', _fit_rfe),
    ])

available_fit_methods = sorted(fit_methods.keys())
