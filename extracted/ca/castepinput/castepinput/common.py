"""
Module for some shared things
"""
from math import sin, cos, pi, sqrt

from monty.json import MSONable
import numpy as np

# pylint: disable=invalid-name


class FormatError(RuntimeError):
    pass


class Block(MSONable, list):
    """
    A class for blocks in CASTEP inputs files stored as a list of strings
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert all(isinstance(s, str) for s in self)

    def as_dict(self):
        d = {"@module": self.__class__.__module__, "@class": self.__class__.__name__}
        d["strings"] = list(self)
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(d["strings"])

    def compact(self, inplace=False):
        """
        Remove any blank lines
        """
        f = [s.strip() for s in self if s]
        if inplace:
            del self[:]
            self.extend(f)
            return self
        return f


def cell_abcs_to_vec(abcs):
    """
    Convert fractional cell format to vectors.
    The result a vector is along [1, 0, 0] and the normal of a,b plane
    is along [0, 0, 1] direction.

    :param abcs: a list of [a, b, c, alpha, beta, gamma]
    """

    a, b, c, alpha, beta, gamma = abcs

    # In case of orthorhobic cell - avoid rounding errors
    e = 2 * np.spacing(90, dtype=np.float64)

    if abs(abs(alpha) - 90) < e:
        cos_alpha = 0.0
    else:
        cos_alpha = cos(alpha * pi / 180)

    if abs(abs(beta) - 90) < e:
        cos_beta = 0.0
    else:
        cos_beta = cos(beta * pi / 180)

    if abs(gamma - 90) < e:
        cos_gamma = 0.0
        sin_gamma = 1.0
    elif abs(gamma + 90) < e:
        cos_gamma = 0.0
        sin_gamma = -1.0
    else:
        cos_gamma = cos(gamma * pi / 180)
        sin_gamma = sin(gamma * pi / 180)

    va = a * np.array([1, 0, 0])
    vb = b * np.array([cos_gamma, sin_gamma, 0])
    cx = cos_beta
    cy = (cos_alpha - cos_beta * cos_gamma) / sin_gamma
    cz = sqrt(1.0 - cx * cx - cy * cy)
    vc = c * np.array([cx, cy, cz])

    cell = np.vstack([va, vb, vc])
    return cell
