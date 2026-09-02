"""
This module implements the split-Bregman algorithm described in
T. Goldstein and S. Osher, SIAM J. Imaging Sci. 2, 323 (2009);
doi:10.1137/080725891

This implementation was based on the CSLD code written by Fei Zhou (周非),
Weston Nielson, Yi Xia, and Vidvuds Ozoliņš and makes use of a right
preconditioner for increased efficiency.

The preconditioning algorithm is described in Compressive sensing lattice
dynamics. I. General formalism Fei Zhou (周非), Weston Nielson, Yi Xia,
and Vidvuds Ozoliņš Phys. Rev. B 100, 184308
"""

import numpy as np
import scipy.linalg
import logging
from typing import Dict, Optional, Any, List, Union


logger = logging.getLogger()


def fit_split_bregman(A: np.ndarray,
                      y: np.ndarray,
                      mu: Optional[Union[float, List[float]]] = None,
                      lmbda: float = 3.,
                      n_iters: int = 1000,
                      tol: float = 1e-4,
                      cg_tol: float = 1e-1,
                      cg_n_iters: Optional[int] = None,
                      iprint: Optional[int] = None,
                      cv_splits: int = 5,
                      ) -> Dict[str, Any]:
    r"""
    Determines the solution :math:`\\boldsymbol{x}` to the linear
    problem :math:`\\boldsymbol{A}\\boldsymbol{x}=\\boldsymbol{y}` using
    the split-Bregman algorithm described in T. Goldstein and S. Osher,
    SIAM J. Imaging Sci. 2, 323 (2009); doi:10.1137/080725891.
    The obtained parameters are returned in the form of a
    dictionary with a key named `parameters`.

    In compressive sensing, the solution vector :math:`\boldsymbol{x}` is given
    by

    .. math::

        \boldsymbol{x} =
        \arg\min_{\boldsymbol{x}} \left\Vert\boldsymbol{x}\right\Vert_1
        + \mu \left\Vert\boldsymbol{A}\boldsymbol{x}
                         - \boldsymbol{y}\right\Vert^2_2,

    where :math:`\mu` and :math:`\lambda` are hyperparameters that control the
    sparseness of the solution and the efficiency of the algorithm.

    This implementation was based on the CSLD code written by Fei Zhou (周非),
    Weston Nielson, Yi Xia, and Vidvuds Ozoliņš and makes use of a right
    preconditioner for increased efficiency.

    The preconditioning algorithm is described in Compressive sensing lattice
    dynamics. I. General formalism Fei Zhou (周非), Weston Nielson, Yi Xia,
    and Vidvuds Ozoliņš Phys. Rev. B 100, 184308

    Parameters
    ----------
    A
        fit matrix
    y
        target array
    mu
        sparseness parameter, can be given as a single value, a list of
        values or None. If a list of values is given, cross validation will be
        used to determine the optimal value. If None is given, a default set of
        values will be tested using cross validation.
    lmbda
        weight of additional L2-norm in split-Bregman
    n_iters
        maximal number of split-Bregman iterations
    tol
        convergence criterion iterative minimization
    cg_n_iters
        maximum number of conjugate gradient iterations. If ``None``, a
        reasonable guess will be made based on the number of free parameters
    cg_tol
        relative tolerance for converging the conjugate gradient step.
    iprint
        controls the frequency of logging output. ``iprint=None`` means no
        output; ``iprint = n`` means print the status of the minimization every
        n steps
    cv_splits
        if mu is None or multiple mu's provided, this controls how many CV
        splits to carry out when evaluating each mu value.
    """
    if mu is None:
        mu = np.logspace(2, 6, 5)

    if isinstance(mu, (float, int)):
        results = _split_bregman(A, y, mu, lmbda, n_iters, tol, cg_tol, cg_n_iters, iprint)

    else:
        # multiple mu values given, use CV to select the best one
        from .cross_validation import CrossValidationEstimator

        cv_data = []
        for mu_value in mu:
            cve = CrossValidationEstimator(
                (A, y), fit_method='split-bregman',
                n_splits=cv_splits, mu=mu_value, lmbda=lmbda, n_iters=n_iters,
                tol=tol, cg_tol=cg_tol, cg_n_iters=cg_n_iters, iprint=iprint)
            cve.validate()

            rmse = cve.rmse_validation
            cv_data.append([mu_value, rmse])

            if iprint:
                logger.info("mu: {}, rmse: {:.4f}".format(mu_value, rmse))

        # select best lambda
        cv_data = np.array(cv_data)
        optimal_ind = cv_data[:, 1].argmin()
        mu_optimal = cv_data[optimal_ind, 0]

        # final fit with optimal lambda
        results = _split_bregman(A, y, mu_optimal, lmbda,
                                 n_iters, tol, cg_tol,
                                 cg_n_iters, iprint)
        results['mu_optimal'] = mu_optimal

    return results


def _split_bregman(A: np.ndarray,
                   y: np.ndarray,
                   mu: float,
                   lmbda: float,
                   n_iters: int,
                   tol: float,
                   cg_tol: float,
                   cg_n_iters: int,
                   iprint: Optional[int],
                   ) -> Dict[str, np.ndarray]:
    """
    Determines the solution :math:`\\boldsymbol{x}` to the linear
    problem :math:`\\boldsymbol{A}\\boldsymbol{x}=\\boldsymbol{y}` using
    the split-Bregman algorithm described in T. Goldstein and S. Osher,
    SIAM J. Imaging Sci. 2, 323 (2009); doi:10.1137/080725891.
    The thus obtained parameters are returned in the form of a
    dictionary with a key named `parameters`

    This implementation was based on the CSLD code written by Fei Zhou (周非),
    Weston Nielson, Yi Xia, and Vidvuds Ozoliņš and makes use of a right
    preconditioner for increased efficiency.

    The preconditioning algorithm is described in Compressive sensing lattice
    dynamics. I. General formalism Fei Zhou (周非), Weston Nielson, Yi Xia,
    and Vidvuds Ozoliņš Phys. Rev. B 100, 184308

    Parameters
    ----------
    A
        fit matrix
    y
        target array
    mu
        sparseness parameter
    lmbda
        weight of additional L2-norm in split-Bregman
    n_iters
        maximal number of split-Bregman iterations
    tol
        convergence criterion iterative minimization
    cg_n_iters
        maximum number of conjugate gradient iterations. If ``None``, a
        reasonable guess will be made based on the number of free parameters
    cg_tol
        relative tolerance for converging the conjugate gradient step.
    iprint
        controls the frequency of logging output. ``iprint=None`` means no
        output; ``iprint = n`` means print the status of the minimization every
        n steps
    """

    def _shrink(y: np.ndarray) -> np.ndarray:
        """
        Shrinkage operator as defined in Eq. (11) of the paper by Nelson
        et al., Phys. Rev. B 87, 035125 (2013); doi:10.1103/PhysRevB.87.035125.
        """
        return np.sign(y) * np.maximum(np.abs(y) - 1 / lmbda, 0.0)

    if not cg_n_iters:
        cg_n_iters = int(np.max([10, A.shape[1] / 2.]))

    preconditioner = _get_right_preconditioner(A, 1 / mu, lmbda)

    A = np.dot(A, preconditioner)

    n_cols = A.shape[1]
    d = np.zeros(n_cols)
    b = np.zeros(n_cols)
    x = np.zeros(n_cols)
    dx_norm = 1.

    for k in range(n_iters):
        x_prev = x

        # The next two lines cover equations 18, 21, and 20 in the Nelson paper.
        # except we apply mu to the L2 term instead of the L1 term
        x = _minimize_cg(x, A, y, d, b, mu, lmbda, cg_n_iters, cg_tol * dx_norm)
        d = _shrink(x + b)
        b = b + x - d

        dx_norm = np.linalg.norm(x - x_prev) / np.linalg.norm(x)

        if iprint and (k + 1) % iprint == 1:
            logger.info("Split Bregman it={}, |dU|/|U|={:.6}".format(k + 1,
                                                                     dx_norm))

        if dx_norm <= tol:
            break

    if dx_norm > tol:
        logger.warning("Split Bregman did not converge: |dU|/|U|={:.6} "
                       "Try increasing mu".format(dx_norm))

    fit_results = {'parameters': np.dot(preconditioner, x)}

    return fit_results


def _minimize_cg(x, A, y, d, b, mu, lmbda, n_iters, gtol):
    """
    Minimises the objective function using conjugate gradient.

    The conjugate gradient algorithm is described in S. Boyd and
    L. Vandenberghe, "Convex Optimization" (Cambridge University Press, 2004).

    This implementation was based on the CSLD code written by Fei Zhou (周非),
    Weston Nielson, Yi Xia, and Vidvuds Ozoliņš.

    Parameters
    -----------
    x
        fit matrix
    y
        target array
    mu
        the parameter that adjusts sparseness.
    lmbda
        Split Bregman parameter
    d
        same notation as Nelson, Hart paper
    b
        same notation as Nelson, Hart paper
    n_iters
        maximum number of iterations
    gtol
        gradient tolerance for convergence
    """
    error_vector = np.matmul(A, x) - y
    r = -(mu * np.matmul(A.T, error_vector) - lmbda * (d - b - x))
    p = r
    delta = np.dot(r, r)

    for k in range(n_iters):
        error_vector = np.matmul(A, p)
        rp = mu * np.matmul(A.T, error_vector) + lmbda * p
        alpha = delta / np.dot(p, rp)

        x = x + alpha * p
        r = r - alpha * rp

        delta_prev = delta
        delta = np.dot(r, r)

        if np.sqrt(delta) < gtol:
            break

        beta = delta / delta_prev
        p = beta * p + r

    sdelta = np.sqrt(delta)
    if sdelta > gtol:
        logger.warning("unconverged gradient, CGmin = {:12.6}".format(sdelta))

    return x


def _get_right_preconditioner(A, mu, lmbda):
    """
    Returns the preconditioning matrix.

    Calculates equation 34 of "Compressive sensing lattice dynamics. I. General
    formalism Fei Zhou (周非), Weston Nielson, Yi Xia, and Vidvuds Ozoliņš
    Phys. Rev. B 100, 184308"

    Parameters
    -----------
    A
        fit matrix
    mu
        preconditioner mu parameter.
    lmbda
        preconditioner lmbda value
    """
    ata = np.matmul(A.T, A)
    ata = (ata.T + ata) / 2

    eig_val, eig_vec = scipy.linalg.eigh(ata)
    over_sq_q = 1 / np.sqrt(eig_val + mu * lmbda)
    return np.matmul(eig_vec, np.matmul(np.diag(over_sq_q), eig_vec.T))
