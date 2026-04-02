"""
Handling of Hermite Normal Form and Smith Normal Form matrices
"""

import numpy as np


class HermiteNormalForm(object):
    """
    Hermite Normal Form matrix.
    """

    def __init__(self, H: np.ndarray, rotations: np.ndarray,
                 translations: np.ndarray, basis_shifts: np.ndarray):
        self.H = H
        self.snf = SmithNormalForm(H)
        self.transformations = []
        self.compute_transformations(rotations, translations, basis_shifts)

    def compute_transformations(self, rotations: np.ndarray,
                                translations: np.ndarray,
                                basis_shifts: np.ndarray,
                                tolerance: float = 1e-3) -> None:
        """
        Save transformations (based on rotations) that turns the supercell
        into an equivalent supercell. Precompute these transformations,
        consisting of permutation as well as translation and basis shift, for
        later use.

        Parameters
        ----------
        rotations
            list of (rotational) symmetry operations
        translations
            list of translations that go together with the rotational operations
        basis_shifts
            corresponding to d_Nd in HarFor09
        tolerance
            tolerance applied when checking that matrices are all integers
        """

        for R, T, basis_shift in zip(rotations, translations,
                                     basis_shifts):
            check = np.dot(np.dot(np.linalg.inv(self.H), R), self.H)
            check = check - np.round(check)
            if (abs(check) < tolerance).all():
                LRL = np.dot(self.snf.L, np.dot(R, np.linalg.inv(self.snf.L)))

                # Should be an integer matrix
                assert (abs(LRL - np.round(LRL)) < tolerance).all()
                LRL = np.round(LRL).astype(np.int64)
                LT = np.dot(T, self.snf.L.T)
                self.transformations.append([LRL, LT, basis_shift])


def yield_hermite_normal_forms(det: int, pbc: list[bool]) -> np.ndarray:
    """
    Yield all Hermite Normal Form matrices with determinant det.

    Parameters
    ----------
    det
        Target determinant of HNFs
    pbc
        Periodic boundary conditions of the primitive structure

    Yields
    ------
    3x3 HNF matrix
    """
    # 1D
    if sum(pbc) == 1:
        hnf = np.eye(3, dtype=int)
        for i, bc in enumerate(pbc):
            if bc:
                hnf[i, i] = det
                break
        yield hnf

    # 2D
    elif sum(pbc) == 2:
        for a in range(1, det + 1):
            if det % a == 0:
                c = det // a
                for b in range(0, c):
                    if not pbc[0]:
                        hnf = [[1, 0, 0],
                               [0, a, 0],
                               [0, b, c]]
                    elif not pbc[1]:
                        hnf = [[a, 0, 0],
                               [0, 1, 0],
                               [b, 0, c]]
                    else:
                        hnf = [[a, 0, 0],
                               [b, c, 0],
                               [0, 0, 1]]
                    yield np.array(hnf)

    # 3D
    else:
        for a in range(1, det + 1):
            if det % a == 0:
                for c in range(1, det // a + 1):
                    if det // a % c == 0:
                        f = det // (a * c)
                        for b in range(0, c):
                            for d in range(0, f):
                                for e in range(0, f):
                                    hnf = [[a, 0, 0],
                                           [b, c, 0],
                                           [d, e, f]]
                                    yield np.array(hnf)


def yield_reduced_hnfs(ncells: int, symmetries: dict,
                       pbc: list[bool], tolerance: float = 1e-3) -> HermiteNormalForm:
    """
    For a fixed determinant N (i.e., a number of atoms N), yield all
    Hermite Normal Forms (HNF) that are inequivalent under symmetry
    operations of the parent lattice.'

    Parameters
    ----------
    ncells
        Determinant of the HNF.
    symmetries
        Symmetry operations of the parent lattice.
    pbc
        Periodic boundary conditions of the primitive structure
    tolerance
        tolerance applied when checking that matrices are all integers

    Yields
    ------
    HermiteNormalForm object, each one symmetrically distinct from the others
    """
    rotations = symmetries['rotations']
    translations = symmetries['translations']
    basis_shifts = symmetries['basis_shifts']
    hnfs = []

    for hnf in yield_hermite_normal_forms(ncells, pbc):

        # Throw away HNF:s that yield equivalent supercells
        hnf_inv = np.linalg.inv(hnf)
        duplicate = False
        for R in rotations:
            HR = np.dot(hnf_inv, R)
            for hnf_previous in hnfs:
                check = np.dot(HR, hnf_previous.H)
                check = check - np.round(check)
                if (abs(check) < tolerance).all():
                    duplicate = True
                    break
            if duplicate:
                break
        if duplicate:
            continue

        # If it's not a duplicate, save the hnf
        # and the supercell so that it can be compared to
        hnf = HermiteNormalForm(hnf, rotations, translations, basis_shifts)
        hnfs.append(hnf)
        yield hnf


class SmithNormalForm(object):
    """
    Smith Normal Form matrix.
    """

    def __init__(self, H: np.ndarray):
        self.compute_snf(H)
        self.S = tuple([self.S_matrix[i, i] for i in range(3)])
        self.ncells = self.S[0] * self.S[1] * self.S[2]
        self.group_order = None
        self.hnfs = []

        # Help list for permuting labelings
        blocks = [self.ncells // self.S[0]]
        for i in range(1, 3):
            blocks.append(blocks[-1] // self.S[i])
        self.blocks = blocks

    def compute_snf(self, H: np.ndarray) -> None:
        """
        Compute Smith Normal Form for 3x3 matrix. Note that H = L*S*R.

        Parameters
        ----------
        H
            3x3 matrix
        """
        A = H.copy()
        L = np.eye(3, dtype=int)
        R = np.eye(3, dtype=int)
        while True:
            # Clear upper row and leftmost column in such
            # a way that greatest common denominator ends
            # up in A[0, 0], in a standard Smith Normal Form way
            # (Euclidean algorithm for finding greatest common divisor)
            while sorted(A[0])[1] != 0 or sorted(A[:, 0])[1] != 0:
                A, R = _gcd_reduce_row(A, R, 0)
                A, L = _gcd_reduce_row(A.T, L.T, 0)
                A, L = A.T, L.T

            # Do the same thing for lower 2x2 matrix
            while sorted(A[1, 1:])[0] != 0 or sorted(A[1:, 1])[0] != 0:
                A, R = _gcd_reduce_row(A, R, 1)
                A, L = _gcd_reduce_row(A.T, L.T, 1)
                A, L = A.T, L.T

            # If last diagonal entry is negative,
            # make it positive
            if A[2, 2] < 0:
                A[2, 2] = -A[2, 2]
                L[2] = -L[2]

            # Check that the diagonal entry i,i divides
            # diagonal entry i+1, i+1. Otherwise,
            # add row i+1 to i and start over.
            if A[2, 2] % A[1, 1] != 0:
                A[1] = A[1] + A[2]
                L[1] = L[1] + L[2]
            elif A[1, 1] % A[0, 0] != 0:
                A[0] = A[0] + A[1]
                L[0] = L[0] + L[1]
            else:
                break
        assert (abs(np.dot(np.dot(L, H), R) - A) < 1e-5).all()
        self.S_matrix = A
        self.L = L

    def add_hnf(self, hnf: HermiteNormalForm) -> None:
        """Add HNF to SNF.

        Paramaters
        ----------
        hnf
            HermiteNormalForm object
        """
        self.hnfs.append(hnf)

    def set_group_order(self) -> None:
        """
        Set group representation of an SNF matrix (the G matrix in HarFor08).
        """
        group_order = []
        for i in range(self.S[0]):
            for j in range(self.S[1]):
                for k in range(self.S[2]):
                    group_order.append([i, j, k])
        self.group_order = group_order


def _gcd_reduce_row(A: np.ndarray, R: np.ndarray, i: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Use column operations to make A[i, i] the greatest common
    denominator of the elements in row i and the other elements
    zero.

    Parameters
    ----------
    A
        Matrix whose row is to be cleared.
    R
        Matrix that should be subject to the same operations.
    i
        Index of row to be treated.

    Returns
    -------
    A
        Treated matrix A.
    R
        Matrix that has been subject to the same operations.
    """
    for j in range(i, 3):
        if A[i, j] < 0:
            A[:, j] = -1 * A[:, j]
            R[:, j] = -1 * R[:, j]
    while np.sort(A[i, i:])[1 - i] > 0:
        max_index = np.argmax(A[i, i:]) + i
        min_index = np.argmin(A[i, i:]) + i
        if max_index == min_index:
            max_index += 1
        if A[i, min_index] == 0 and i == 0:
            if np.sort(A[i])[1] > 0:
                min_index += 1
                min_index = min_index % 3
                if min_index == max_index:
                    min_index += 1
                    min_index = min_index % 3
            if A[i, min_index] == A[i, max_index]:
                tmp = min_index
                min_index = max_index
                max_index = tmp
        A[:, max_index] = A[:, max_index] - A[:, min_index]
        R[:, max_index] = R[:, max_index] - R[:, min_index]
    max_index = np.argmax(A[i])
    return A, R


def get_unique_snfs(hnfs: list[HermiteNormalForm]) -> list[SmithNormalForm]:
    """
    For a list of Hermite Normal Forms, obtain the set of unique Smith Normal
    Forms.

    Parameters
    ----------
    hnfs
        List of HermiteNormalForm objects.

    Returns
    -------
        The unique Smith Normal Form matrices in a list.
    """
    snfs = []
    for hnf in hnfs:
        # Check whether the snf is new or already encountered
        snf = hnf.snf
        snf_is_new = True
        for snf_comp in snfs:
            if snf_comp.S == snf.S:
                snf_is_new = False
                snf_comp.add_hnf(hnf)
                break
        if snf_is_new:
            snf.set_group_order()
            snf.add_hnf(hnf)
            snfs.append(snf)
    return snfs
