"""
The ``utilities`` module contains various support functions and classes.
"""
import sympy
import numpy as np
from scipy.sparse import coo_matrix
from collections import defaultdict
from ..input_output.logging_tools import Progress
from ase import Atoms
from typing import Tuple

__all__ = ['Progress']


def ase_atoms_to_spglib_tuple(structure: Atoms) -> Tuple:
    """
    Returns a tuple of three components: cell metric, atomic positions, and
    atomic species of the input ASE Atoms object.
    """
    return (structure.cell, structure.get_scaled_positions(), structure.get_atomic_numbers())


class SparseMatrix(sympy.SparseMatrix):

    def rref_sparse(self, simplify=False):
        """ A sparse row reduce algorithm mimicing the dense version """

        def multiply_and_add_row(row1, factor, row2):
            """ does row1 += factor * row2 when rows are represented by dicts
            """
            keys_to_delete = []
            for k, v in row2.items():
                row1[k] += factor * v
                if row1[k] == 0:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del row1[k]

        # The matrix is represented as a list of dicts where each dict is a row
        M = defaultdict(lambda: defaultdict(lambda: 0))

        # Init our special representation. This is possible due to defaultdict
        for r, c, v in self.row_list():
            M[r][c] = v
        M = list(M.values())

        # The pivot elements is stored as tuples as (row, col)
        pivots = []
        r, c = 0, 0  # current row and col of possible pivot
        nRows, nCols = len(M), self.shape[1]
        while r < nRows and c < nCols:
            row = M[r]
            # check if proposed pivot i zero. if so swap this row with a row
            # below which has non zero element at that col
            if c not in row:
                for r2 in range(r + 1, nRows):
                    row2 = M[r2]
                    if c in row2:  # This row has element in the current col
                        M[r], M[r2] = row2, row  # swap the rows
                        row = row2
                        break
                else:  # The pivot and all elements below are zero.
                    c += 1  # goto next column but stay on row
                    continue
            pivots.append((r, c))
            # Normalize row
            row_c = row[c]
            for k in row:
                row[k] /= row_c
            # Start elimination
            r2 = r + 1
            while r2 < nRows:
                row2 = M[r2]
                if c not in row2:
                    r2 += 1
                    continue
                multiply_and_add_row(row2, -row2[c], row)
                if len(row2) == 0:
                    nRows -= 1
                    del M[r2]
                    continue
                r2 += 1
            r += 1
            c += 1

        # Eliminate elements above pivots
        for (r, p) in pivots:
            row_p = M[r]
            for i in range(r):
                row = M[i]
                if p in row:
                    multiply_and_add_row(row, -row[p], row_p)

        # Create the new rrefd matrix
        M2 = SparseMatrix(*self.shape, 0)
        for i, d in enumerate(M):
            for j, v in d.items():
                M2[i, j] = v

        pivots = tuple(p[1] for p in pivots)

        return M2, pivots

    def nullspace(self, simplify=False):
        """ This is a slightly patched version which also uses the sparse rref
            and is faster due to up-front creation of empty SparseMatrix
            vectors instead of conversion of the finished vectors
        """
        if (max(*self.shape) < 10):  # If matrix small use the dense version
            reduced, pivots = self.rref(simplify=simplify)
        else:
            reduced, pivots = self.rref_sparse(simplify=simplify)

        free_vars = [i for i in range(self.cols) if i not in pivots]

        basis = []
        for free_var in free_vars:
            # for each free variable, we will set it to 1 and all others
            # to 0.  Then, we will use back substitution to solve the system

            # initialize each vector as an empty SparseMatrix
            vec = self._new(self.cols, 1, 0)
            vec[free_var] = 1
            for piv_row, piv_col in enumerate(pivots):
                vec[piv_col] -= reduced[piv_row, free_var]
            basis.append(vec)

        return basis

    def to_array(self):
        """ Cast SparseMatrix instance to numpy array """
        row, col, data = [], [], []
        for r, c, v in self.row_list():
            row.append(r)
            col.append(c)
            data.append(np.float64(v))
        M = coo_matrix((data, (row, col)), shape=self.shape)
        return M.toarray()


class BiMap:
    """Simple list like structure with fast dict-lookup

    The structure can append objects and supports some simple list interfaces.
    The lookup is fast since an internal dict stores the indices.
    """
    def __init__(self):
        self._list = list()
        self._dict = dict()

    def __contains__(self, value):
        return value in self._dict

    def __getitem__(self, index):
        return self._list[index]

    def append(self, value):
        """bm.append(hashable) -> None -- append hashable object to end"""
        self._dict[value] = len(self._list)
        self._list.append(value)

    def __len__(self):
        return len(self._list)

    def index(self, value):
        """bm.index(values) -> integer -- return index of value
        Raises ValueError if the values is not present.
        """
        try:
            return self._dict[value]
        except KeyError:
            raise ValueError('{} is not in list'.format(value))

    def copy(self):
        """bm.copy() -> BiMap -- a shallow copy of bm"""
        tbm = BiMap()
        tbm._list = self._list.copy()
        tbm._dict = self._dict.copy()
        return tbm
