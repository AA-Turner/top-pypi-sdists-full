import pickle
import numpy as np
from ase.neighborlist import NeighborList
from hiphive.input_output.pretty_table_prints import table_array_to_string


class Cutoffs:
    """ This class maintains information about the cutoff configuration,
    i.e. which clusters will be included (="inside cutoff"). It also
    encapsulates functionality that is used e.g., during cluster space
    construction.

    Here, `n-body` refers to number of atoms in a cluster. For example
    the cluster (0011) is a two-body cluster of fourth order and the
    cluster (123) is a three-body cluster of third order.

    Parameters
    ----------
    cutoff_matrix : numpy.ndarray
        the matrix element `ij` provides to the cutoff for order `j+2`
        and nbody `i+2`; elements with `i>j` will be ignored
    """

    def __init__(self, cutoff_matrix):

        self._cutoff_matrix = np.array(cutoff_matrix, dtype=float)

        if len(self._cutoff_matrix.shape) != 2:
            raise ValueError('Please specify cutoff matrix as a 2D array')
        for i, row in enumerate(self._cutoff_matrix):
            if np.any(row[i:] < 0):
                raise ValueError('Negative number as cutoff')
            row[:i] = np.nan
        self._cutoff_matrix = self._cutoff_matrix[:(self.max_nbody-1), :(self.max_order-1)]

    @property
    def cutoff_matrix(self):
        """ numpy.ndarray : copy of cutoff matrix """
        return self._cutoff_matrix.copy()

    @property
    def orders(self):
        """ list(int) : allowed orders """
        return list(range(2, self.max_order + 1))

    @property
    def nbodies(self):
        """ list(int) : allowed bodies """
        return list(range(2, self.max_nbody + 1))

    def get_cutoff(self, order, nbody):
        """
        Returns cutoff for a given body and order.

        Parameters
        ----------
        order : int
        nbody : int

        Raises
        ------
        ValueError
            if order is not in orders
        ValueError
            if nbody is not in nbodies
        ValueError
            if nbody is larger than order

        Returns
        -------
        float
        """
        if order not in self.orders:
            raise ValueError('order not in orders')
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        if nbody > order:
            raise ValueError('nbody can not be larger than order')
        return self._cutoff_matrix[nbody - 2, order - 2]

    @property
    def max_cutoff(self):
        """ float : maximum cutoff """
        max_cutoff = 0
        for i, row in enumerate(self._cutoff_matrix):
            max_cutoff = max(max_cutoff, np.max(row[i:]))
        return max_cutoff

    @property
    def max_nbody(self):
        """ int : maximum body """
        nbody = 1
        for i, row in enumerate(self._cutoff_matrix):
            if np.any(row[i:]):
                nbody = i + 2
        return nbody

    @property
    def max_order(self):
        """ int : maximum order """
        order = None
        for col in range(self._cutoff_matrix.shape[1]):
            if np.any(self._cutoff_matrix[:col + 1, col]):
                order = col + 2
        return order

    def max_nbody_cutoff(self, nbody):
        """ Return maximum cutoff for a given body. """
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        return np.max(self._cutoff_matrix[nbody - 2, max(0, nbody - 2):])

    def max_nbody_order(self, nbody):
        """ Returns maximum order for a given body """
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        row = self._cutoff_matrix[nbody - 2]
        max_order = None
        for order, cutoff in enumerate(row[nbody-2:], start=nbody):
            if cutoff:
                max_order = order
        return max_order

    def write(self, fileobj):
        """ Writes instance to file.

        Parameters
        ----------
        fileobj : file-like object
            file-like object to which the cutoffs will be written to
        """
        pickle.dump(self._cutoff_matrix, fileobj)

    def read(fileobj):
        """ Reads an instance from file.

        Parameters
        ----------
        fileobj : file-like object
            input file to read from
        """
        data = pickle.load(fileobj)
        return Cutoffs(data)

    def to_filename_tag(self):
        """ Simple function turning cutoffs into a string to be used in e.g.
        filenames. """
        s = []
        for i, c in enumerate(self._cutoff_matrix.tolist(), start=2):
            s.append('{}body-{}'.format(i, '_'.join(map(str, c))))
        return '_'.join(s)

    def __str__(self):
        cutoff_matrix = self._cutoff_matrix.copy()
        cutoff_matrix = np.vstack(([[None] * len(self.orders)], cutoff_matrix))
        s = table_array_to_string(cutoff_matrix)

        width = max(len(c) for c in s.split('\n'))
        header = ' Cutoffs '.center(width, '=') + '\n'
        bottom = '\n' + ''.center(width, '=')
        s = header + s + bottom
        return s

    def __repr__(self):
        return 'Cutoffs({!r})'.format(self._cutoff_matrix)


class CutoffMaximumBody(Cutoffs):
    """ Specify cutoff-list plus maximum body

    Usefull when creating e.g. 6th order expansions but with only 3-body
    interactions.

    Parameters
    ----------
    cutoff_list : list
        list of cutoffs for order 2, 3, etc. Must be in decresing order
    max_nbody : int
        No clusters containing more than max_nbody atoms will be generated
    """

    def __init__(self, cutoff_list, max_nbody):
        cutoff_matrix = np.zeros((max_nbody - 1, len(cutoff_list)))
        for order, cutoff in enumerate(cutoff_list, start=2):
            cutoff_matrix[:, order - 2] = cutoff
        super().__init__(cutoff_matrix)


def is_cutoff_allowed(atoms, cutoff):
    """ Checks if atoms is compatible with cutoff

    Parameters
    ----------
    atoms : ase.Atoms
        structure used for checking compatibility with cutoff
    cutoff : float
        cutoff to be tested

    Returns
    -------
    bool
        True if cutoff compatible with atoms object, else False
    """
    nbrlist = NeighborList(cutoffs=[cutoff / 2] * len(atoms), skin=0,
                           self_interaction=False, bothways=True)
    nbrlist.update(atoms)

    for i in range(len(atoms)):
        neighbors, _ = nbrlist.get_neighbors(i)
        if i in neighbors:
            return False
        if len(neighbors) != len(set(neighbors)):
            return False
    return True


def estimate_maximum_cutoff(atoms, max_iter=11):
    """ Estimates the maximum possible cutoff given the atoms object

    Parameters
    ----------
    atoms : ase.Atoms
        structure used for checking compatibility with cutoff
    max_iter : int
        number of iterations in binary search
    """

    # First upper boundary of cutoff
    upper_cutoff = min(np.linalg.norm(atoms.cell, axis=1))

    # generate all possible offsets given upper_cutoff
    nbrlist = NeighborList(cutoffs=[upper_cutoff / 2] * len(atoms), skin=0,
                           self_interaction=False, bothways=True)
    nbrlist.update(atoms)
    all_offsets = []
    for i in range(len(atoms)):
        _, offsets = nbrlist.get_neighbors(i)
        all_offsets.extend([tuple(offset) for offset in offsets])

    # find lower boundary and new upper boundary
    unique_offsets = set(all_offsets)
    unique_offsets.discard((0, 0, 0))
    upper = min(np.linalg.norm(np.dot(offset, atoms.cell))
                for offset in unique_offsets)
    lower = upper / 2.0

    # run binary search between the upper and lower bounds
    for _ in range(max_iter):
        cutoff = (upper + lower) / 2
        if is_cutoff_allowed(atoms, cutoff):
            lower = cutoff
        else:
            upper = cutoff
    return lower


class BaseClusterFilter:
    """Base cluster filter class.

    This filter simply accepts all proposed clusters.  A proper
    subclass must implement the same methods.
    """
    def setup(self, atoms):
        """ The filter is passed the environment of the primitive cell.

        Parameters
        ----------
        atoms : ase.Atoms
            non-pbc primitive cell plus neighboring atoms
        """
        self._atoms = atoms

    def __call__(self, cluster):
        """ Returns True or False when a cluster is proposed.

        Parameters
        ----------
        cluster : tuple(int)
            indices of proposed cluster referenced to the internal
            atoms object
        """
        return True
