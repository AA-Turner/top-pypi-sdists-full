import numpy as np

from ase.utils import deprecated


def asetransport_deprecated(func):
    return deprecated(
        'The ase.transport package is deprecated in ase-3.30.0 '
        'and will be removed in a future version.  If you use any '
        'features in ase.transport, and believe that they are worth '
        'conserving, please open an issue on the ASE issue tracker.'
    )(func)


class GreenFunction:
    """Equilibrium retarded Green function."""

    @asetransport_deprecated
    def __init__(self, H, S=None, selfenergies=None, eta=1e-4):
        if selfenergies is None:
            selfenergies = []
        self.H = H
        self.S = S
        self.selfenergies = selfenergies
        self.eta = eta
        self.energy = None
        self.Ginv = np.empty(H.shape, complex)

    def retarded(self, energy, inverse=False):
        """Get retarded Green function at specified energy.

        If 'inverse' is True, the inverse Green function is returned (faster).
        """
        if energy != self.energy:
            self.energy = energy
            z = energy + self.eta * 1.0j

            if self.S is None:
                self.Ginv[:] = 0.0
                self.Ginv.flat[:: len(self.S) + 1] = z
            else:
                self.Ginv[:] = z
                self.Ginv *= self.S
            self.Ginv -= self.H

            for selfenergy in self.selfenergies:
                self.Ginv -= selfenergy.retarded(energy)

        if inverse:
            return self.Ginv
        else:
            return np.linalg.inv(self.Ginv)

    def calculate(self, energy, sigma):
        """XXX is this really needed"""
        ginv = energy * self.S - self.H - sigma
        return np.linalg.inv(ginv)

    def apply_retarded(self, energy, X):
        """Apply retarded Green function to X.

        Returns the matrix product G^r(e) . X
        """
        return np.linalg.solve(self.retarded(energy, inverse=True), X)

    def dos(self, energy):
        """Total density of states -1/pi Im(Tr(GS))"""
        if self.S is None:
            return -self.retarded(energy).imag.trace() / np.pi
        else:
            GS = self.apply_retarded(energy, self.S)
            return -GS.imag.trace() / np.pi

    def pdos(self, energy):
        """Projected density of states -1/pi Im(SGS/S)"""
        if self.S is None:
            return -self.retarded(energy).imag.diagonal() / np.pi
        else:
            S = self.S
            SGS = np.dot(S, self.apply_retarded(energy, S))
            return -(SGS.diagonal() / S.diagonal()).imag / np.pi
