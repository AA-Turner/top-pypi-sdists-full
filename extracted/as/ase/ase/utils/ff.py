from collections.abc import Sequence

import numpy as np
from numpy import linalg
from numpy.typing import NDArray

from ase import Atoms, units

# Three variables extracted from what used to be endless repetitions below.
Ax = np.array(
    [
        [1, 0, 0, -1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, -1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 1],
    ]
)
Bx = np.array([[1, 0, 0, -1, 0, 0], [0, 1, 0, 0, -1, 0], [0, 0, 1, 0, 0, -1]])
Mx = Bx


class Morse:
    """Morse potential between two atoms.

    Parameters
    ----------
    atomi, atomj : int
        Indices of the two atoms.
    D : float
        Dissociation energy.
    alpha : float
        Parameter controlling the width of the potential.
    r0 : float
        Equilibrium bond length.
    """

    def __init__(self, atomi, atomj, D, alpha, r0):
        self.atomi = atomi
        self.atomj = atomj
        self.D = D
        self.alpha = alpha
        self.r0 = r0
        self.r = None


class Bond:
    """Harmonic bond-stretching potential between two atoms.

    Parameters
    ----------
    atomi, atomj : int
        Indices of the two atoms.
    k : float
        Bond force constant.
    b0 : float
        Equilibrium bond length.
    alpha : sequence of float or None
        Parameters for distance-dependent scaling of the Hessian.
    rref : sequence of float or None
        Reference bond lengths for distance-dependent scaling.
    """

    def __init__(self, atomi, atomj, k, b0, alpha=None, rref=None):
        self.atomi = atomi
        self.atomj = atomj
        self.k = k
        self.b0 = b0
        self.alpha = alpha
        self.rref = rref
        self.b = None


class Angle:
    """Harmonic angle-bending potential involving three atoms.

    Parameters
    ----------
    atomi, atomj, atomk : int
        Indices of the three atoms, with atomj as the central atom.
    k : float
        Angle force constant.
    a0 : float
        Equilibrium bond angle in radians.
    cos : bool
        If True, use the difference in cosines instead of angles.
    alpha : sequence of float or None
        Parameters for distance-dependent scaling of the Hessian.
    rref : sequence of float or None
        Reference bond lengths for distance-dependent scaling.
    """

    def __init__(
        self, atomi, atomj, atomk, k, a0, cos=False, alpha=None, rref=None
    ):
        self.atomi = atomi
        self.atomj = atomj
        self.atomk = atomk
        self.k = k
        self.a0 = a0
        self.cos = cos
        self.alpha = alpha
        self.rref = rref
        self.a = None


class Dihedral:
    """Dihedral potential involving four atoms.

    The potential is harmonic if `n` is None and `d0` is specified,
    periodic if both are specified, and planar if `d0` is None.

    Parameters
    ----------
    atomi, atomj, atomk, atoml : int
        Indices of the four atoms defining the dihedral angle.
    k : float
        Force constant or potential amplitude.
    d0 : float or None
        Equilibrium dihedral angle or phase offset, in radians.
    n : int or None
        Periodicity of the torsional potential.
    """

    def __init__(
        self,
        atomi,
        atomj,
        atomk,
        atoml,
        k,
        d0=None,
        n=None,
        alpha=None,
        rref=None,
    ):
        self.atomi = atomi
        self.atomj = atomj
        self.atomk = atomk
        self.atoml = atoml
        self.k = k
        self.d0 = d0
        self.n = n
        self.alpha = alpha
        self.rref = rref
        self.d = None


class VdW:
    """Van der Waals potential between two atoms.

    Parameters
    ----------
    atomi, atomj : int
        Indices of the two atoms.
    Aij : float
        Coefficient of the repulsive r^-12 term.
    Bij : float
        Coefficient of the attractive r^-6 term.
    """

    def __init__(
        self,
        atomi,
        atomj,
        epsilonij=None,
        sigmaij=None,
        rminij=None,
        Aij=None,
        Bij=None,
        epsiloni=None,
        epsilonj=None,
        sigmai=None,
        sigmaj=None,
        rmini=None,
        rminj=None,
        scale=1.0,
    ):
        self.atomi = atomi
        self.atomj = atomj
        if epsilonij is not None:
            if sigmaij is not None:
                self.Aij = scale * 4.0 * epsilonij * sigmaij**12
                self.Bij = scale * 4.0 * epsilonij * sigmaij**6
            elif rminij is not None:
                self.Aij = scale * epsilonij * rminij**12
                self.Bij = scale * 2.0 * epsilonij * rminij**6
            else:
                raise NotImplementedError(
                    'not implemented combinationof vdW parameters.'
                )
        elif Aij is not None and Bij is not None:
            self.Aij = scale * Aij
            self.Bij = scale * Bij
        elif epsiloni is not None and epsilonj is not None:
            if sigmai is not None and sigmaj is not None:
                self.Aij = (
                    scale
                    * 4.0
                    * np.sqrt(epsiloni * epsilonj)
                    * ((sigmai + sigmaj) / 2.0) ** 12
                )
                self.Bij = (
                    scale
                    * 4.0
                    * np.sqrt(epsiloni * epsilonj)
                    * ((sigmai + sigmaj) / 2.0) ** 6
                )
            elif rmini is not None and rminj is not None:
                self.Aij = (
                    scale
                    * np.sqrt(epsiloni * epsilonj)
                    * ((rmini + rminj) / 2.0) ** 12
                )
                self.Bij = (
                    scale
                    * 2.0
                    * np.sqrt(epsiloni * epsilonj)
                    * ((rmini + rminj) / 2.0) ** 6
                )
        else:
            raise NotImplementedError(
                'not implemented combinationof vdW parameters.'
            )
        self.r = None


class Coulomb:
    """Coulomb potential between two point charges.

    Parameters
    ----------
    atomi, atomj : int
        Indices of the two atoms.
    chargeij : float or None
        Product of the two charges.
    chargei, chargej : float or None
        Individual atomic charges, used if `chargeij` is None.
    scale : float
        Scaling factor for the Coulomb interaction.
    """

    def __init__(
        self, atomi, atomj, chargeij=None, chargei=None, chargej=None, scale=1.0
    ):
        self.atomi = atomi
        self.atomj = atomj
        if chargeij is not None:
            self.chargeij = (
                scale
                * chargeij
                * 8.9875517873681764e9
                * units.m
                * units.J
                / units.C
                / units.C
            )
        elif chargei is not None and chargej is not None:
            self.chargeij = (
                scale
                * chargei
                * chargej
                * 8.9875517873681764e9
                * units.m
                * units.J
                / units.C
                / units.C
            )
        else:
            raise NotImplementedError(
                'not implemented combinationof Coulomb parameters.'
            )
        self.r = None


def get_morse_potential_eta(
    atoms: Atoms,
    morse: Morse,
) -> float:
    i = morse.atomi
    j = morse.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)

    if dij > morse.r0:
        exp = np.exp(-morse.alpha * (dij - morse.r0))
        eta = 1.0 - (1.0 - exp) ** 2
    else:
        eta = 1.0

    return eta


def get_morse_potential_value(
    atoms: Atoms,
    morse: Morse,
) -> tuple[int, int, float]:
    i = morse.atomi
    j = morse.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)

    exp = np.exp(-morse.alpha * (dij - morse.r0))

    v = morse.D * (1.0 - exp) ** 2

    morse.r = dij

    return i, j, v


def get_morse_potential_gradient(
    atoms: Atoms,
    morse: Morse,
) -> tuple[int, int, NDArray[np.floating]]:
    i = morse.atomi
    j = morse.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    exp = np.exp(-morse.alpha * (dij - morse.r0))

    gr = 2.0 * morse.D * morse.alpha * exp * (1.0 - exp) * eij

    gx = np.dot(Mx.T, gr)

    morse.r = dij

    return i, j, gx


def get_morse_potential_hessian(
    atoms: Atoms,
    morse: Morse,
    spectral: bool = False,
) -> tuple[int, int, NDArray[np.floating]]:
    i = morse.atomi
    j = morse.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij

    exp = np.exp(-morse.alpha * (dij - morse.r0))

    Hr = (
        2.0
        * morse.D
        * morse.alpha
        * exp
        * (morse.alpha * (2.0 * exp - 1.0) * Pij + (1.0 - exp) / dij * Qij)
    )

    Hx = np.dot(Mx.T, np.dot(Hr, Mx))

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    morse.r = dij

    return i, j, Hx


def get_morse_potential_reduced_hessian(
    atoms: Atoms,
    morse: Morse,
) -> tuple[int, int, NDArray[np.floating]]:
    """Calculate the reduced Hessian of a Morse potential.

    Only the bond-stretching contribution is retained, and the absolute value
    of the curvature is used to obtain a positive-semidefinite Hessian.
    """
    i = morse.atomi
    j = morse.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)

    exp = np.exp(-morse.alpha * (dij - morse.r0))

    Hr = np.abs(2.0 * morse.D * morse.alpha**2 * exp * (2.0 * exp - 1.0)) * Pij

    Hx = np.dot(Mx.T, np.dot(Hr, Mx))

    morse.r = dij

    return i, j, Hx


def get_bond_potential_value(
    atoms: Atoms,
    bond: Bond,
) -> tuple[int, int, float]:
    i = bond.atomi
    j = bond.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)

    v = 0.5 * bond.k * (dij - bond.b0) ** 2

    bond.b = dij

    return i, j, v


def get_bond_potential_gradient(
    atoms: Atoms,
    bond: Bond,
) -> tuple[int, int, NDArray[np.floating]]:
    i = bond.atomi
    j = bond.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    gr = bond.k * (dij - bond.b0) * eij

    gx = np.dot(Bx.T, gr)

    bond.b = dij

    return i, j, gx


def get_bond_potential_hessian(
    atoms: Atoms,
    bond: Bond,
    morses: Sequence[Morse] | None = None,
    spectral: bool = False,
) -> tuple[int, int, NDArray[np.floating]]:
    i = bond.atomi
    j = bond.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij

    Hr = bond.k * Pij + bond.k * (dij - bond.b0) / dij * Qij

    if bond.alpha is not None:
        Hr *= np.exp(bond.alpha[0] * (bond.rref[0] ** 2 - dij**2))

    if morses is not None:
        for m in range(len(morses)):
            if morses[m].atomi == i or morses[m].atomi == j:
                Hr *= get_morse_potential_eta(atoms, morses[m])
            elif morses[m].atomj == i or morses[m].atomj == j:
                Hr *= get_morse_potential_eta(atoms, morses[m])

    Hx = np.dot(Bx.T, np.dot(Hr, Bx))

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    bond.b = dij

    return i, j, Hx


def get_bond_potential_reduced_hessian(
    atoms: Atoms,
    bond: Bond,
    morses: Sequence[Morse] | None = None,
) -> tuple[int, int, NDArray[np.floating]]:
    """Calculate the reduced Hessian of a harmonic bond potential.

    Only the bond-stretching contribution is retained, neglecting
    the transverse contributions to the Hessian.

    The Hessian is optionally scaled by distance-dependent factors
    and Morse-potential-based bond-breaking factors.
    """
    i = bond.atomi
    j = bond.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)

    Hr = bond.k * Pij

    if bond.alpha is not None:
        Hr *= np.exp(bond.alpha[0] * (bond.rref[0] ** 2 - dij**2))

    if morses is not None:
        for m in range(len(morses)):
            if morses[m].atomi == i or morses[m].atomi == j:
                Hr *= get_morse_potential_eta(atoms, morses[m])
            elif morses[m].atomj == i or morses[m].atomj == j:
                Hr *= get_morse_potential_eta(atoms, morses[m])

    Hx = np.dot(Bx.T, np.dot(Hr, Bx))

    bond.b = dij

    return i, j, Hx


def get_angle_potential_value(
    atoms: Atoms,
    angle: Angle,
) -> tuple[int, int, int, float]:

    i = angle.atomi
    j = angle.atomj
    k = angle.atomk

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    ekj = rkj / dkj
    eijekj = np.dot(eij, ekj)
    if np.abs(eijekj) > 1.0:
        eijekj = np.sign(eijekj)

    a = np.arccos(eijekj)

    if angle.cos:
        da = np.cos(a) - np.cos(angle.a0)
    else:
        da = a - angle.a0
        da = da - np.around(da / np.pi) * np.pi

    v = 0.5 * angle.k * da**2

    angle.a = a

    return i, j, k, v


def get_angle_potential_gradient(
    atoms: Atoms,
    angle: Angle,
) -> tuple[int, int, int, NDArray[np.floating]]:
    i = angle.atomi
    j = angle.atomj
    k = angle.atomk

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    ekj = rkj / dkj
    eijekj = np.dot(eij, ekj)
    if np.abs(eijekj) > 1.0:
        eijekj = np.sign(eijekj)

    a = np.arccos(eijekj)
    if angle.cos:
        da = np.cos(a) - np.cos(angle.a0)
    else:
        da = a - angle.a0
        da = da - np.around(da / np.pi) * np.pi
        sina = np.sin(a)

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij
    Pkj = np.tensordot(ekj, ekj, axes=0)
    Qkj = np.eye(3) - Pkj

    gr = np.zeros(6)
    if angle.cos:
        gr[0:3] = angle.k * da / dij * np.dot(Qij, ekj)
        gr[3:6] = angle.k * da / dkj * np.dot(Qkj, eij)
    elif np.abs(sina) > 0.001:
        gr[0:3] = -angle.k * da / sina / dij * np.dot(Qij, ekj)
        gr[3:6] = -angle.k * da / sina / dkj * np.dot(Qkj, eij)

    gx = np.dot(Ax.T, gr)

    angle.a = a

    return i, j, k, gx


def get_angle_potential_hessian(
    atoms: Atoms,
    angle: Angle,
    morses: Sequence[Morse] | None = None,
    spectral: bool = False,
) -> tuple[int, int, int, NDArray[np.floating]]:
    i = angle.atomi
    j = angle.atomj
    k = angle.atomk

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    dij2 = dij * dij
    eij = rij / dij
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    dkj2 = dkj * dkj
    ekj = rkj / dkj
    dijdkj = dij * dkj
    eijekj = np.dot(eij, ekj)
    if np.abs(eijekj) > 1.0:
        eijekj = np.sign(eijekj)

    a = np.arccos(eijekj)
    if angle.cos:
        da = np.cos(a) - np.cos(angle.a0)
        cosa0 = np.cos(angle.a0)
    else:
        da = a - angle.a0
        da = da - np.around(da / np.pi) * np.pi
    sina = np.sin(a)
    cosa = np.cos(a)
    ctga = cosa / sina

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij
    Pkj = np.tensordot(ekj, ekj, axes=0)
    Qkj = np.eye(3) - Pkj
    Pik = np.tensordot(eij, ekj, axes=0)
    Pki = np.tensordot(ekj, eij, axes=0)
    P = np.eye(3) * eijekj

    QijPkjQij = np.dot(Qij, np.dot(Pkj, Qij))
    QijPkiQkj = np.dot(Qij, np.dot(Pki, Qkj))
    QkjPijQkj = np.dot(Qkj, np.dot(Pij, Qkj))

    Hr = np.zeros((6, 6))
    if angle.cos and np.abs(sina) > 0.001:
        factor = 1.0 - 2.0 * cosa * cosa + cosa * cosa0
        Hr[0:3, 0:3] = (
            angle.k
            * (
                factor * QijPkjQij / sina
                - sina
                * da
                * (
                    -ctga * QijPkjQij / sina
                    + np.dot(Qij, Pki)
                    - np.dot(Pij, Pki) * 2.0
                    + (Pik + P)
                )
            )
            / sina
            / dij2
        )
        Hr[0:3, 3:6] = (
            angle.k
            * (
                factor * QijPkiQkj / sina
                - sina * da * (-ctga * QijPkiQkj / sina - np.dot(Qij, Qkj))
            )
            / sina
            / dijdkj
        )
        Hr[3:6, 0:3] = Hr[0:3, 3:6].T
        Hr[3:6, 3:6] = (
            angle.k
            * (
                factor * QkjPijQkj / sina
                - sina
                * da
                * (
                    -ctga * QkjPijQkj / sina
                    + np.dot(Qkj, Pik)
                    - np.dot(Pkj, Pik) * 2.0
                    + (Pki + P)
                )
            )
            / sina
            / dkj2
        )
    elif np.abs(sina) > 0.001:
        Hr[0:3, 0:3] = (
            angle.k
            * (
                QijPkjQij / sina
                + da
                * (
                    -ctga * QijPkjQij / sina
                    + np.dot(Qij, Pki)
                    - np.dot(Pij, Pki) * 2.0
                    + (Pik + P)
                )
            )
            / sina
            / dij2
        )
        Hr[0:3, 3:6] = (
            angle.k
            * (
                QijPkiQkj / sina
                + da * (-ctga * QijPkiQkj / sina - np.dot(Qij, Qkj))
            )
            / sina
            / dijdkj
        )
        Hr[3:6, 0:3] = Hr[0:3, 3:6].T
        Hr[3:6, 3:6] = (
            angle.k
            * (
                QkjPijQkj / sina
                + da
                * (
                    -ctga * QkjPijQkj / sina
                    + np.dot(Qkj, Pik)
                    - np.dot(Pkj, Pik) * 2.0
                    + (Pki + P)
                )
            )
            / sina
            / dkj2
        )

    if angle.alpha is not None:
        Hr *= np.exp(angle.alpha[0] * (angle.rref[0] ** 2 - dij**2)) * np.exp(
            angle.alpha[1] * (angle.rref[1] ** 2 - dkj**2)
        )

    if morses is not None:
        for m in range(len(morses)):
            if (
                morses[m].atomi == i
                or morses[m].atomi == j
                or morses[m].atomi == k
            ):
                Hr *= get_morse_potential_eta(atoms, morses[m])
            elif (
                morses[m].atomj == i
                or morses[m].atomj == j
                or morses[m].atomj == k
            ):
                Hr *= get_morse_potential_eta(atoms, morses[m])

    Hx = np.dot(Ax.T, np.dot(Hr, Ax))

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    angle.a = a

    return i, j, k, Hx


def get_angle_potential_reduced_hessian(
    atoms: Atoms,
    angle: Angle,
    morses: Sequence[Morse] | None = None,
) -> tuple[int, int, int, NDArray[np.floating]]:
    """Calculate the reduced Hessian of an angle potential.

    Only the angle-bending contribution is retained.

    The absolute value of the angular curvature is used to obtain
    a positive-semidefinite Hessian.

    The Hessian is optionally scaled by distance-dependent factors
    and Morse-potential-based bond-breaking factors.
    """
    i = angle.atomi
    j = angle.atomj
    k = angle.atomk

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    dij2 = dij * dij
    eij = rij / dij
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    dkj2 = dkj * dkj
    ekj = rkj / dkj
    dijdkj = dij * dkj
    eijekj = np.dot(eij, ekj)
    if np.abs(eijekj) > 1.0:
        eijekj = np.sign(eijekj)

    a = np.arccos(eijekj)
    sina = np.sin(a)
    sina2 = sina * sina

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij
    Pkj = np.tensordot(ekj, ekj, axes=0)
    Qkj = np.eye(3) - Pkj
    Pki = np.tensordot(ekj, eij, axes=0)

    Hr = np.zeros((6, 6))
    if np.abs(sina) > 0.001:
        Hr[0:3, 0:3] = np.dot(Qij, np.dot(Pkj, Qij)) / dij2
        Hr[0:3, 3:6] = np.dot(Qij, np.dot(Pki, Qkj)) / dijdkj
        Hr[3:6, 0:3] = Hr[0:3, 3:6].T
        Hr[3:6, 3:6] = np.dot(Qkj, np.dot(Pij, Qkj)) / dkj2

    if angle.cos and np.abs(sina) > 0.001:
        cosa = np.cos(a)
        cosa0 = np.cos(angle.a0)
        factor = np.abs(1.0 - 2.0 * cosa * cosa + cosa * cosa0)
        Hr = Hr * factor * angle.k / sina2
    elif np.abs(sina) > 0.001:
        Hr = Hr * angle.k / sina2

    if angle.alpha is not None:
        Hr *= np.exp(angle.alpha[0] * (angle.rref[0] ** 2 - dij**2)) * np.exp(
            angle.alpha[1] * (angle.rref[1] ** 2 - dkj**2)
        )

    if morses is not None:
        for m in range(len(morses)):
            if (
                morses[m].atomi == i
                or morses[m].atomi == j
                or morses[m].atomi == k
            ):
                Hr *= get_morse_potential_eta(atoms, morses[m])
            elif (
                morses[m].atomj == i
                or morses[m].atomj == j
                or morses[m].atomj == k
            ):
                Hr *= get_morse_potential_eta(atoms, morses[m])

    Hx = np.dot(Ax.T, np.dot(Hr, Ax))

    angle.a = a

    return i, j, k, Hx


def get_dihedral_potential_value(
    atoms: Atoms,
    dihedral: Dihedral,
) -> tuple[int, int, int, int, float]:
    i = dihedral.atomi
    j = dihedral.atomj
    k = dihedral.atomk
    l = dihedral.atoml

    rij = rel_pos_pbc(atoms, i, j)
    rkj = rel_pos_pbc(atoms, k, j)
    rkl = rel_pos_pbc(atoms, k, l)

    rmj = np.cross(rij, rkj)
    dmj = linalg.norm(rmj)
    emj = rmj / dmj
    rnk = np.cross(rkj, rkl)
    dnk = linalg.norm(rnk)
    enk = rnk / dnk
    emjenk = np.dot(emj, enk)
    if np.abs(emjenk) > 1.0:
        emjenk = np.sign(emjenk)

    d = np.sign(np.dot(rkj, np.cross(rmj, rnk))) * np.arccos(emjenk)

    if dihedral.d0 is None:
        v = 0.5 * dihedral.k * (1.0 - np.cos(2.0 * d))
    else:
        dd = d - dihedral.d0
        dd = dd - np.around(dd / np.pi / 2.0) * np.pi * 2.0
        if dihedral.n is None:
            v = 0.5 * dihedral.k * dd**2
        else:
            v = dihedral.k * (1.0 + np.cos(dihedral.n * d - dihedral.d0))

    dihedral.d = d

    return i, j, k, l, v


def get_dihedral_potential_gradient(
    atoms: Atoms,
    dihedral: Dihedral,
) -> tuple[int, int, int, int, NDArray[np.floating]]:
    i = dihedral.atomi
    j = dihedral.atomj
    k = dihedral.atomk
    l = dihedral.atoml

    rij = rel_pos_pbc(atoms, i, j)
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    dkj2 = dkj * dkj
    rkl = rel_pos_pbc(atoms, k, l)

    rijrkj = np.dot(rij, rkj)
    rkjrkl = np.dot(rkj, rkl)

    rmj = np.cross(rij, rkj)
    dmj = linalg.norm(rmj)
    dmj2 = dmj * dmj
    emj = rmj / dmj
    rnk = np.cross(rkj, rkl)
    dnk = linalg.norm(rnk)
    dnk2 = dnk * dnk
    enk = rnk / dnk
    emjenk = np.dot(emj, enk)
    if np.abs(emjenk) > 1.0:
        emjenk = np.sign(emjenk)

    dddri = dkj / dmj2 * rmj
    dddrl = -dkj / dnk2 * rnk

    gx = np.zeros(12)

    gx[0:3] = dddri
    gx[3:6] = (rijrkj / dkj2 - 1.0) * dddri - rkjrkl / dkj2 * dddrl
    gx[6:9] = (rkjrkl / dkj2 - 1.0) * dddrl - rijrkj / dkj2 * dddri
    gx[9:12] = dddrl

    d = np.sign(np.dot(rkj, np.cross(rmj, rnk))) * np.arccos(emjenk)

    if dihedral.d0 is None:
        gx *= dihedral.k * np.sin(2.0 * d)
    else:
        dd = d - dihedral.d0
        dd = dd - np.around(dd / np.pi / 2.0) * np.pi * 2.0
        if dihedral.n is None:
            gx *= dihedral.k * dd
        else:
            gx *= (
                -dihedral.k * dihedral.n * np.sin(dihedral.n * d - dihedral.d0)
            )

    dihedral.d = d

    return i, j, k, l, gx


def get_dihedral_potential_hessian(
    atoms: Atoms,
    dihedral: Dihedral,
    morses: Sequence[Morse] | None = None,
    spectral: bool = False,
) -> tuple[int, int, int, int, NDArray[np.floating]]:
    eps = 0.000001

    i, j, k, l, g = get_dihedral_potential_gradient(atoms, dihedral)

    Hx = np.zeros((12, 12))

    dihedral_eps = Dihedral(
        dihedral.atomi,
        dihedral.atomj,
        dihedral.atomk,
        dihedral.atoml,
        dihedral.k,
        dihedral.d0,
        dihedral.n,
    )
    indx = [
        3 * i,
        3 * i + 1,
        3 * i + 2,
        3 * j,
        3 * j + 1,
        3 * j + 2,
        3 * k,
        3 * k + 1,
        3 * k + 2,
        3 * l,
        3 * l + 1,
        3 * l + 2,
    ]
    for x in range(12):
        a = atoms.copy()
        positions = np.reshape(a.get_positions(), -1)
        positions[indx[x]] += eps
        a.set_positions(np.reshape(positions, (len(a), 3)))
        i, j, k, l, geps = get_dihedral_potential_gradient(a, dihedral_eps)
        for y in range(12):
            Hx[x, y] += 0.5 * (geps[y] - g[y]) / eps
            Hx[y, x] += 0.5 * (geps[y] - g[y]) / eps

    if dihedral.alpha is not None:
        rij = rel_pos_pbc(atoms, i, j)
        dij = linalg.norm(rij)
        rkj = rel_pos_pbc(atoms, k, j)
        dkj = linalg.norm(rkj)
        rkl = rel_pos_pbc(atoms, k, l)
        dkl = linalg.norm(rkl)
        Hx *= (
            np.exp(dihedral.alpha[0] * (dihedral.rref[0] ** 2 - dij**2))
            * np.exp(dihedral.alpha[1] * (dihedral.rref[1] ** 2 - dkj**2))
            * np.exp(dihedral.alpha[2] * (dihedral.rref[2] ** 2 - dkl**2))
        )

    if morses is not None:
        for m in range(len(morses)):
            if (
                morses[m].atomi == i
                or morses[m].atomi == j
                or morses[m].atomi == k
                or morses[m].atomi == l
            ):
                Hx *= get_morse_potential_eta(atoms, morses[m])
            elif (
                morses[m].atomj == i
                or morses[m].atomj == j
                or morses[m].atomj == k
                or morses[m].atomj == l
            ):
                Hx *= get_morse_potential_eta(atoms, morses[m])

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    return i, j, k, l, Hx


def get_dihedral_potential_reduced_hessian(
    atoms: Atoms,
    dihedral: Dihedral,
    morses: Sequence[Morse] | None = None,
) -> tuple[int, int, int, int, NDArray[np.floating]]:
    """Calculate the reduced Hessian of a dihedral potential.

    Only the torsional contribution is retained.

    The absolute value of the torsional curvature is used to obtain
    a positive-semidefinite Hessian.

    The Hessian is optionally scaled by distance-dependent factors
    and Morse-potential-based bond-breaking factors.
    """
    i = dihedral.atomi
    j = dihedral.atomj
    k = dihedral.atomk
    l = dihedral.atoml

    rij = rel_pos_pbc(atoms, i, j)
    rkj = rel_pos_pbc(atoms, k, j)
    dkj = linalg.norm(rkj)
    dkj2 = dkj * dkj
    rkl = rel_pos_pbc(atoms, k, l)

    rijrkj = np.dot(rij, rkj)
    rkjrkl = np.dot(rkj, rkl)

    rmj = np.cross(rij, rkj)
    dmj = linalg.norm(rmj)
    dmj2 = dmj * dmj
    emj = rmj / dmj
    rnk = np.cross(rkj, rkl)
    dnk = linalg.norm(rnk)
    dnk2 = dnk * dnk
    enk = rnk / dnk
    emjenk = np.dot(emj, enk)
    if np.abs(emjenk) > 1.0:
        emjenk = np.sign(emjenk)

    d = np.sign(np.dot(rkj, np.cross(rmj, rnk))) * np.arccos(emjenk)

    dddri = dkj / dmj2 * rmj
    dddrl = -dkj / dnk2 * rnk

    gx = np.zeros(12)

    gx[0:3] = dddri
    gx[3:6] = (rijrkj / dkj2 - 1.0) * dddri - rkjrkl / dkj2 * dddrl
    gx[6:9] = (rkjrkl / dkj2 - 1.0) * dddrl - rijrkj / dkj2 * dddri
    gx[9:12] = dddrl

    if dihedral.d0 is None:
        Hx = np.abs(2.0 * dihedral.k * np.cos(2.0 * d)) * np.tensordot(
            gx, gx, axes=0
        )
    if dihedral.n is None:
        Hx = dihedral.k * np.tensordot(gx, gx, axes=0)
    else:
        Hx = np.abs(
            -dihedral.k * dihedral.n**2 * np.cos(dihedral.n * d - dihedral.d0)
        ) * np.tensordot(gx, gx, axes=0)

    if dihedral.alpha is not None:
        rij = rel_pos_pbc(atoms, i, j)
        dij = linalg.norm(rij)
        rkj = rel_pos_pbc(atoms, k, j)
        dkj = linalg.norm(rkj)
        rkl = rel_pos_pbc(atoms, k, l)
        dkl = linalg.norm(rkl)
        Hx *= (
            np.exp(dihedral.alpha[0] * (dihedral.rref[0] ** 2 - dij**2))
            * np.exp(dihedral.alpha[1] * (dihedral.rref[1] ** 2 - dkj**2))
            * np.exp(dihedral.alpha[2] * (dihedral.rref[2] ** 2 - dkl**2))
        )

    if morses is not None:
        for m in range(len(morses)):
            if (
                morses[m].atomi == i
                or morses[m].atomi == j
                or morses[m].atomi == k
                or morses[m].atomi == l
            ):
                Hx *= get_morse_potential_eta(atoms, morses[m])
            elif (
                morses[m].atomj == i
                or morses[m].atomj == j
                or morses[m].atomj == k
                or morses[m].atomj == l
            ):
                Hx *= get_morse_potential_eta(atoms, morses[m])

    dihedral.d = d

    return i, j, k, l, Hx


def get_vdw_potential_value(
    atoms: Atoms,
    vdw: VdW,
) -> tuple[int, int, float]:
    i = vdw.atomi
    j = vdw.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)

    v = vdw.Aij / dij**12 - vdw.Bij / dij**6

    vdw.r = dij

    return i, j, v


def get_vdw_potential_gradient(
    atoms: Atoms,
    vdw: VdW,
) -> tuple[int, int, NDArray[np.floating]]:
    i = vdw.atomi
    j = vdw.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    gr = (-12.0 * vdw.Aij / dij**13 + 6.0 * vdw.Bij / dij**7) * eij

    gx = np.dot(Bx.T, gr)

    vdw.r = dij

    return i, j, gx


def get_vdw_potential_hessian(
    atoms: Atoms,
    vdw: VdW,
    spectral: bool = False,
) -> tuple[int, int, NDArray[np.floating]]:
    i = vdw.atomi
    j = vdw.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij

    Hr = (156.0 * vdw.Aij / dij**14 - 42.0 * vdw.Bij / dij**8) * Pij + (
        -12.0 * vdw.Aij / dij**13 + 6.0 * vdw.Bij / dij**7
    ) / dij * Qij

    Hx = np.dot(Bx.T, np.dot(Hr, Bx))

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    vdw.r = dij

    return i, j, Hx


def get_coulomb_potential_value(
    atoms: Atoms,
    coulomb: Coulomb,
) -> tuple[int, int, float]:
    i = coulomb.atomi
    j = coulomb.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)

    v = coulomb.chargeij / dij

    coulomb.r = dij

    return i, j, v


def get_coulomb_potential_gradient(
    atoms: Atoms,
    coulomb: Coulomb,
) -> tuple[int, int, NDArray[np.floating]]:
    i = coulomb.atomi
    j = coulomb.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    gr = -coulomb.chargeij / dij / dij * eij

    gx = np.dot(Bx.T, gr)

    coulomb.r = dij

    return i, j, gx


def get_coulomb_potential_hessian(
    atoms: Atoms,
    coulomb: Coulomb,
    spectral: bool = False,
) -> tuple[int, int, NDArray[np.floating]]:
    i = coulomb.atomi
    j = coulomb.atomj

    rij = rel_pos_pbc(atoms, i, j)
    dij = linalg.norm(rij)
    eij = rij / dij

    Pij = np.tensordot(eij, eij, axes=0)
    Qij = np.eye(3) - Pij

    Hr = (2.0 * coulomb.chargeij / dij**3) * Pij + (
        -coulomb.chargeij / dij / dij
    ) / dij * Qij

    Hx = np.dot(Bx.T, np.dot(Hr, Bx))

    if spectral:
        eigvals, eigvecs = linalg.eigh(Hx)
        D = np.diag(np.abs(eigvals))
        U = eigvecs
        Hx = np.dot(U, np.dot(D, np.transpose(U)))

    coulomb.r = dij

    return i, j, Hx


def rel_pos_pbc(atoms: Atoms, i: int, j: int) -> NDArray[np.floating]:
    """
    Return difference between two atomic positions,
    correcting for jumps across PBC
    """
    d = atoms.get_positions()[i, :] - atoms.get_positions()[j, :]
    g = linalg.inv(atoms.get_cell().T)
    f = np.floor(np.dot(g, d.T) + 0.5)
    d -= np.dot(atoms.get_cell().T, f).T
    return d
