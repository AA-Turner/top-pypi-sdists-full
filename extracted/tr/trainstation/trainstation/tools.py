"""
Collection of tools for managing and analyzing linear models.

Todo
-----
Consider what functionality we actually want here

"""

import numpy as np


class ScatterData:
    """ Container class for holding data like target and predict values

    sd = ScatterData(y_target, y_predicted)
    plt.plot(sd.target, sd.predicted, 'o')
    """

    def __init__(self, target=None, predicted=None):
        if target is None:
            target = []
        if predicted is None:
            predicted = []
        self._target = list(target)
        self._predicted = list(predicted)

    @property
    def target(self):
        return np.array(self._target)

    @property
    def predicted(self):
        return np.array(self._predicted)

    def __add__(self, other):
        target = self._target + other._target
        predicted = self._predicted + other._predicted
        return ScatterData(target, predicted)

    def __eq__(self, ot):
        return np.allclose(self.target, ot.target) and np.allclose(self.predicted, ot.predicted)

    def to_dict(self) -> dict:
        return {'target': self.target.tolist(), 'predicted': self.predicted.tolist()}

    def from_dict(dct: dict):
        return ScatterData(target=dct['target'], predicted=dct['predicted'])


def compute_correlation_matrix(A: np.ndarray) -> np.ndarray:
    """
    Returns the correlation matrix for the rows in the fit matrix.

    Notes
    -----
    Naive implementation.

    Parameters
    ----------
    A
        fit matrix
    """
    N = A.shape[0]
    C = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            norm = np.linalg.norm(A[i, :]) * np.linalg.norm(A[j, :])
            c_ij = np.dot(A[i, :], A[j, :]) / norm
            C[i, j] = c_ij
            C[j, i] = c_ij
    return C
