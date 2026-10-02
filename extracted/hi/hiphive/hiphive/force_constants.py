"""
This module provides functionality for storing and handling of force constants.
"""

import numpy as np
import tarfile

from abc import ABC, abstractmethod
from itertools import product
from string import ascii_lowercase, ascii_uppercase
from typing import List, Tuple

from scipy.linalg import eig
from ase import Atoms, units

from .input_output import shengBTE as shengBTEIO
from .input_output import phonopy as phonopyIO
from .input_output.read_write_files import add_items_to_tarfile_pickle, read_items_pickle, \
    add_ase_atoms_to_tarfile, read_ase_atoms_from_tarfile
from .input_output import gpumd as gpumdIO


class ForceConstants(ABC):
    """ Base class for force constants """

    def __init__(self, supercell: Atoms):
        if not all(supercell.pbc):
            raise ValueError('configuration must have periodic boundary conditions')
        self._supercell = supercell.copy()

    @abstractmethod
    def __getitem__(self):
        pass

    @property
    def n_atoms(self) -> int:
        """ number of atoms """
        return len(self.supercell)

    @property
    def supercell(self) -> Atoms:
        """ supercell associated with force constants """
        return self._supercell.copy()

    @property
    def clusters(self) -> list:
        """ sorted list of clusters """
        return sorted(self._fc_dict.keys(), key=lambda c: (len(c), c))

    def __len__(self) -> int:
        """ int : number of clusters (or force constants) """
        return len(self._fc_dict)

    def __add__(self, fcs_other) -> None:
        """ ForceConstants : addition of two force constants """
        if not isinstance(fcs_other, type(self)):
            raise ValueError('ForceConstants objects are of different types')

        # if they have overlapping orders, raise
        if any(order in self.orders for order in fcs_other.orders):
            raise ValueError('ForceConstants objects share at least one order')

        # check that they share the same supercell
        if self.supercell != fcs_other.supercell:
            raise ValueError('supercells do not match')

        # add force constants
        fc_merged = {**self._fc_dict, **fcs_other._fc_dict}
        return self.__class__(fc_merged, self.supercell)

    def get_fc_dict(self, order: int = None) -> dict:
        """ Returns force constant dictionary for one specific order.

        The returned dict may be sparse or may be dense depending on the
        underlying force constants.

        Parameters
        ----------
        order
            force constants returned for this order

        Returns
        -------
        dictionary with keys corresponding to clusters and values to
        respective force constant
        """
        if order is None:
            return self._fc_dict

        if order not in self.orders:
            raise ValueError('Order {} not in ForceConstants'.format(order))

        fc_order = {}
        for c, fc in self._fc_dict.items():
            if len(c) == order:
                fc_order[c] = fc
        return fc_order

    def get_fc_array(self, order: int, format: str = 'phonopy') -> np.ndarray:
        """ Returns force constants in array format for specified order.

        Parameters
        ----------
        order
            force constants for this order will be returned
        format
            specify which format (shape) the NumPy array should have,
            possible values are `phonopy` and `ase`

        Returns
        -------
        NumPy array with shape `(N,)*order + (3,)*order` where `N` is
        the number of atoms
        """
        if order not in self.orders:
            raise ValueError('Order not in orders')
        if format not in ['ase', 'phonopy']:
            raise ValueError('Format must be either ase or phonopy')

        # generate fc array for phonopy format
        fc_array = np.zeros((self.n_atoms, ) * order + (3, ) * order)
        for cluster in product(range(self.n_atoms), repeat=order):
            fc_array[cluster] = self[cluster]

        if format == 'ase':
            if order != 2:
                raise ValueError('ASE format works only for order 2')
            return fc_array.transpose([0, 2, 1, 3]).reshape(
                self.n_atoms * 3, self.n_atoms * 3)
        else:
            return fc_array

    def compute_gamma_frequencies(self) -> np.ndarray:
        """ Returns the Gamma frequencies in THz using the second-order force
        constants. """
        fc2_array = self.get_fc_array(order=2)
        masses = self.supercell.get_masses()
        return _compute_gamma_frequencies(fc2_array, masses)

    def assert_acoustic_sum_rules(self, order: int = None, tol: float = 1e-6):
        """ Asserts that force constants obey acoustic sum rules.

        Parameters
        ----------
        order
            specifies which order to check, if None all are checked
        tol
            numeric tolerance for checking sum rules

        Raises
        ------
        AssertionError
            if acoustic sum rules are violated
        """

        # set up orders
        if order is None:
            orders = self.orders
        else:
            if order not in self.orders:
                raise ValueError('Order not available in FCS')
            orders = [order]

        atomic_indices = range(self.n_atoms)
        for order in orders:
            assert_msg = 'Acoustic sum rule for order {} violated for atom'
            assert_msg += ' {}' * (order - 1) + ' x'
            for ijk in product(atomic_indices, repeat=order-1):
                fc_sum_ijk = np.zeros((3, )*order)
                for m in atomic_indices:
                    cluster = ijk + (m, )
                    fc_sum_ijk += self[cluster]
                assert np.linalg.norm(fc_sum_ijk) < tol, assert_msg.format(order, *ijk)

    def print_force_constant(self, cluster: Tuple[int]) -> None:
        """
        Prints force constants for a cluster in a nice format.

        Parameters
        ----------
        cluster
            sites belonging to the cluster
        """
        print(self._repr_fc(cluster))

    def __eq__(self, other):

        # check supercells are the same
        if not len(self.supercell) == len(other.supercell):
            return False
        if not np.allclose(self.supercell.positions, other.supercell.positions):
            return False
        if not np.allclose(self.supercell.cell, other.supercell.cell):
            return False
        if not all(self.supercell.numbers == other.supercell.numbers):
            return False

        # check orders and clusters are the same
        if self.orders != other.orders:
            return False
        if self.clusters != other.clusters:
            return False

        # check force constants
        for c in self.clusters:
            if not np.allclose(self[c], other[c]):
                return False
        return True

    def __str__(self) -> str:
        s = []
        s.append(' ForceConstants '.center(54, '='))
        s.append('Orders: {}'.format(self.orders))
        s.append('Atoms: {}'.format(self.supercell))
        s.append('')
        if len(self) > 10:
            for c in self.clusters[:3]:
                s.append(self._repr_fc(c)+'\n')
            s.append('...\n')
            for c in self.clusters[-3:]:
                s.append(self._repr_fc(c)+'\n')
        else:
            for c in self.clusters:
                s.append(self._repr_fc(c)+'\n')
        return '\n'.join(s)

    def __repr__(self) -> str:
        fc_dict_str = '{{{}: {}, ..., {}: {}}}'.format(
            self.clusters[0], self[self.clusters[0]].round(5),
            self.clusters[-1], self[self.clusters[-1]].round(5))
        return ('ForceConstants(fc_dict={}, atoms={!r})'
                .format(fc_dict_str, self.supercell))

    def _repr_fc(self, cluster: Tuple[int],
                 precision: float = 5, suppress: bool = True) -> str:
        """
        Representation for single cluster and its force constant.

        Parameters
        ----------
        cluster
            tuple of ints indicating the sites belonging to the cluster
        """
        s = []
        s.append('Cluster: {}'.format(cluster))
        for atom_index in cluster:
            s.append(str(self.supercell[atom_index]))
        s.append('Force constant:')
        s.append(np.array_str(self[cluster], precision=precision,
                 suppress_small=suppress))
        return '\n'.join(s)

    def _sanity_check_dict(self, fc_dict: dict) -> None:
        """ Checks that all indices in clusters are between 0 and number of
        atoms. """
        # Use flat numpy array for fast check
        cluster_indices = np.concatenate([cluster for cluster in fc_dict.keys()])
        if not np.all((0 <= cluster_indices) & (cluster_indices < self.n_atoms)):
            # If the check failed, do slower list processing to find the erring cluster
            for cluster in fc_dict.keys():
                if not all(0 <= i < self.n_atoms for i in cluster):
                    raise ValueError('Cluster {} not in supercell'.format(cluster))

    @classmethod
    def from_arrays(cls, supercell: Atoms,
                    fc2_array: np.ndarray = None, fc3_array: np.ndarray = None):
        """ Constructs FCs from numpy arrays.

        One or both of fc2_array and fc3_array must not be None

        Parameters
        ----------
        supercell
            supercell structure
        fc2_array
            second-order force constant in phonopy format, i.e. must have shape (N, N, 3, 3)
        fc3_array
            third-order force constant in phonopy format, i.e. must have shape (N, N, N, 3, 3, 3)
        """
        if fc2_array is None and fc3_array is None:
            raise ValueError('Please provide force constant arrays.')

        n_atoms = len(supercell)
        if fc2_array is None:
            fc2_dict = dict()
        else:
            if fc2_array.shape != (n_atoms, n_atoms, 3, 3):
                raise ValueError('fc2 array has wrong shape')
            fc2_dict = array_to_dense_dict(fc2_array)

        if fc3_array is None:
            fc3_dict = dict()
        else:
            if fc3_array.shape != (n_atoms, n_atoms, n_atoms, 3, 3, 3):
                raise ValueError('fc2 array has wrong shape')
            fc3_dict = array_to_dense_dict(fc3_array)

        fc_dict = {**fc2_dict, **fc3_dict}
        return cls.from_dense_dict(fc_dict, supercell)

    @classmethod
    def from_sparse_dict(cls, fc_dict: dict, supercell: Atoms):
        """ Assumes label symmetries, meaning only one cluster for each
        permuation should be included

        Parameters
        ----------
        fc_dict
            keys corresponding to clusters and values to the force constants
        supercell
            atomic configuration
        """
        return SortedForceConstants(fc_dict, supercell=supercell)

    @classmethod
    def from_dense_dict(cls, fc_dict: dict, supercell: Atoms):
        """ All permutations of clusters that are not zero must be listed,
        if label symmetries are fullfilled will return a SortedForceConstants

        Parameters
        ----------
        fc_dict
            keys corresponding to clusters and values to the force constants
        supercell
            atomic configuration
        """
        if check_label_symmetries(fc_dict):
            fc_sparse_dict = dense_dict_to_sparse_dict(fc_dict)
            return SortedForceConstants(fc_sparse_dict, supercell=supercell)
        else:
            return RawForceConstants(fc_dict, supercell=supercell)

    @classmethod
    def read_phonopy(cls, supercell: Atoms, fname: str, format: str = None):
        """ Reads force constants from a phonopy calculation.

        Parameters
        ----------
        supercell
            supercell structure (`SPOSCAR`)
        fname
            name of second-order force constant file
        format
            format for second-order force constants;
            possible values: "text", "hdf5"
        """
        fc2_array = phonopyIO.read_phonopy_fc2(fname, format=format)
        return cls.from_arrays(supercell, fc2_array)

    @classmethod
    def read_phono3py(cls, supercell: Atoms, fname: str):
        """ Reads force constants from a phono3py calculation.

        Parameters
        ----------
        supercell
            supercell structure (`SPOSCAR`)
        fname
            name of third-order force constant file
        """
        fc3_array = phonopyIO.read_phonopy_fc3(fname)
        return cls.from_arrays(supercell, fc3_array=fc3_array)

    @classmethod
    def read_shengBTE(cls, supercell: Atoms, fname: str, prim: Atoms, symprec=1e-5):
        """ Reads third order force constants from a shengBTE calculation.

        shengBTE force constants will be mapped onto a supercell.

        Parameters
        ----------
        supercell
            supercell structure
        fname
            name of third-order force constant file
        prim
            primitive configuration (must be equivalent to structure used in
            the shengBTE calculation)
        symprec
            structural symmetry tolerance
        """
        fcs = shengBTEIO.read_shengBTE_fc3(fname, prim, supercell, symprec)
        return fcs

    @classmethod
    def read(cls, fname: str):
        """ Reads ForceConstants from file.

        Parameters
        ----------
        fname
            name of file from which to read
        """
        tar_file = tarfile.open(mode='r', name=fname)
        items = read_items_pickle(tar_file, 'fc_dict')
        fc_dict = items['fc_dict']
        fcs_type = items['fcs_type']
        supercell = read_ase_atoms_from_tarfile(tar_file, 'supercell')
        tar_file.close()
        if fcs_type == 'SortedForceConstants':
            return SortedForceConstants(fc_dict, supercell)
        elif fcs_type == 'RawForceConstants':
            return RawForceConstants(fc_dict, supercell)
        else:
            raise ValueError('FCS type not recongnized')

    def write(self, fname: str) -> None:
        """ Writes entire ForceConstants object to file.

        Parameters
        ----------
        fname
            name of file to which to write
        """
        tar_file = tarfile.open(name=fname, mode='w')
        items_pickle = dict(fc_dict=self._fc_dict, fcs_type=self.__class__.__name__)
        add_items_to_tarfile_pickle(tar_file, items_pickle, 'fc_dict')
        add_ase_atoms_to_tarfile(tar_file, self.supercell, 'supercell')
        tar_file.close()

    def write_to_phonopy(self, fname: str, format: str = None) -> None:
        """
        Writes force constants in phonopy format.

        Parameters
        ----------
        fname
            name of file to which to write second-order force constant
        format
            format for second-order force constants;
             possible values: "text", "hdf5"
        """
        phonopyIO.write_phonopy_fc2(fname, self, format=format)

    def write_to_phono3py(self, fname: str) -> None:
        """
        Writes force constants in phono3py format.

        Parameters
        ----------
        fname
            name of file to which to write third-order force constant
        """
        phonopyIO.write_phonopy_fc3(fname, self)

    def write_to_shengBTE(self, fname: str, prim: Atoms, **kwargs) -> None:
        """
        Writes third order force constants in shengBTE format.

        Parameters
        ----------
        fname
            name of file to which to write third-order force constant
        prim
            primitive configuration (must be equivalent to structure used in
            the shengBTE calculation)
        """
        shengBTEIO.write_shengBTE_fc3(fname, self, prim, **kwargs)


class SortedForceConstants(ForceConstants):
    """ Force constants with label symmetries.

    Parameters
    ----------
    fc_dict : dict
        keys corresponding to clusters and values to the force constants,
        should only contain sorted clusters
    supercell : ase.Atoms
    """

    def __init__(self, fc_dict: dict, supercell: Atoms) -> None:
        super().__init__(supercell)
        self._sanity_check_dict(fc_dict)
        self._fc_dict = fc_dict
        self._orders = sorted(set(len(c) for c in self._fc_dict.keys()))

    def __getitem__(self, cluster: Tuple[int]):
        sorted_cluster = tuple(sorted(cluster))

        # cluster not in fcs
        if sorted_cluster not in self._fc_dict.keys():
            return np.zeros((3,)*len(cluster))

        # return fc for the unsorted cluster
        inv_perm = np.argsort(np.argsort(cluster))
        return self._fc_dict[sorted_cluster].transpose(inv_perm)

    @property
    def orders(self) -> List[int]:
        """ orders for which force constants exist """
        return self._orders.copy()

    def _sanity_check_dict(self, fc_dict: dict) -> None:
        super()._sanity_check_dict(fc_dict)

        # also check clusters are sorted
        for cluster in fc_dict.keys():
            if cluster != tuple(sorted(cluster)):
                raise ValueError('Found unsorted cluster {}'.format(cluster))

    def write_to_GPUMD(self, fname_fc, fname_clusters, order, tol=1e-10):
        """
        Writes force constants of the specified order in GPUMD format.

        Parameters
        ----------
        fname_fc : str
            name of file which contains the lookup force constants
        fname_clusters : str
            name of file which contains the clusters and the fc lookup index
        order : int
            force constants for this order will be written to file
        tol : float
            if the norm of a force constant is less than tol then it is not written.
            if two force-constants are within tol; they are considered equal.
        """
        gpumdIO.write_fcs_gpumd(fname_fc, fname_clusters, self, order, tol)


class RawForceConstants(ForceConstants):
    """ Force constants without label symmetries.

    Parameters
    ----------
    fc_dict : dict
        keys corresponding to clusters and values to the force constants,
        should contain all clusters with nonzero force constants
    supercell : ase.Atoms
    """

    def __init__(self, fc_dict: dict, supercell: Atoms) -> None:
        super().__init__(supercell)
        self._sanity_check_dict(fc_dict)
        self._fc_dict = fc_dict
        self._orders = sorted(set(len(c) for c in self._fc_dict.keys()))

    def __getitem__(self, cluster: Tuple[int]):
        if cluster not in self._fc_dict.keys():
            return np.zeros((3,)*len(cluster))
        return self._fc_dict[cluster]

    @property
    def orders(self) -> List[int]:
        """ orders for which force constants exist """
        return self._orders.copy()


# ====================== #
#     HELPER FUNCTIONS   #
# ====================== #


def array_to_dense_dict(fc_array: np.ndarray, fc_tol: float = 1e-10) -> dict:
    """ Constructs a dense dict from an fc array in phonopy format.

    Force constants with norm smaller than fc_tol will be considered zero and
    therefore not included in the fc_dict.

    Parameters
    ----------
    fc_array
        force constant array in phonopy format
    fc_tol
        tolerance for considering force constants zero or not
    """

    # sanity check
    n_atoms = fc_array.shape[0]
    order = int(len(fc_array.shape) / 2)
    if fc_array.shape != (n_atoms, ) * order + (3, ) * order:
        raise ValueError('fc array has bad shape')

    # construct dense dict
    fc_dict = dict()
    for cluster in product(range(n_atoms), repeat=order):
        fc = fc_array[cluster]
        if np.linalg.norm(fc) > fc_tol:
            fc_dict[cluster] = fc
    return fc_dict


def check_label_symmetries(fc_dict: dict) -> bool:
    """ Checks label symmetries for dense fc dict.

    TODO
    ----
    tol, which one to use etc

    Parameters
    ----------
    fc_dict
        keys corresponding to clusters and values to the force constants
    """
    for cluster, fc in fc_dict.items():
        inv_perm = np.argsort(np.argsort(cluster))
        sorted_cluster = tuple(sorted(cluster))
        if sorted_cluster not in fc_dict:
            return False
        if not np.allclose(fc, fc_dict[sorted_cluster].transpose(inv_perm)):
            return False
    return True


def dense_dict_to_sparse_dict(fc_dict: dict) -> dict:
    """ Converts dense dict to sparse dict.

    This does not check if label symmetry is True, but rather will just keep
    the sorted clusters and their force constants.

    Parameters
    ----------
    fc_dict
        keys corresponding to clusters and values to the force constants
    """
    fc_dict_sparse = dict()
    for cluster, fc in fc_dict.items():
        if cluster == tuple(sorted(cluster)):
            fc_dict_sparse[cluster] = fc
    return fc_dict_sparse


def symbolize_force_constant(fc: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    """Carries out a symbolic symmetrization of a force constant tensor.

    Parameters
    ----------
    fc
        force constant tensor
    tol
        tolerance used to decide whether two elements are identical

    Returns
    -------
    symbolic representation of force constant matrix
    """
    fc_int = np.round(fc / tol).astype(int)
    fc_chars = np.empty(fc_int.shape, dtype=object).flatten()
    all_chars = ascii_lowercase + ascii_uppercase
    lookup_chars = {}
    for i, val in enumerate(fc_int.flatten()):
        if val == 0:
            fc_chars[i] = 0
        elif val in lookup_chars.keys():
            fc_chars[i] = lookup_chars[val]
        elif -val in lookup_chars.keys():
            fc_chars[i] = '-{:}'.format(lookup_chars[-val])
        else:
            lookup_chars[val] = all_chars[len(lookup_chars.keys())]
            fc_chars[i] = lookup_chars[val]
    return fc_chars.reshape(fc_int.shape)


def _compute_gamma_frequencies(fc2: np.ndarray, masses: List[float]) -> np.ndarray:
    """ Computes Gamma frequencies using second-order force constants.
    Assumes fc2 is in units of eV/A2.

    Parameters
    ----------
    fc2
        second-order force constants in phonopy format
    masses
        mass of each atom

    Returns
    -------
    Gamma frequencies in THz
    """

    n_atoms = fc2.shape[0]
    if len(masses) != n_atoms:
        raise ValueError('Length of masses not compatible with fc2')
    mass_matrix = np.sqrt(np.outer(masses, masses))

    # divide with mass matrix
    fc2_tmp = np.zeros((n_atoms, n_atoms, 3, 3))
    for pair in product(range(n_atoms), repeat=2):
        fc2_tmp[pair] = fc2[pair] / mass_matrix[pair]

    # reshape into matrix and solve eigenvalues
    fc2_tmp = fc2_tmp.transpose([0, 2, 1, 3]).reshape(n_atoms * 3, n_atoms * 3)
    eigen_vals, _ = eig(fc2_tmp)
    eigen_vals *= 1e20 / units.J * units.kg  # [1/s**2]
    eigen_vals.sort()

    # if negative eigenval, set frequency to negative
    gamma_frequencies = []
    for val in eigen_vals.real:
        if val >= 0:
            gamma_frequencies.append(np.sqrt(val))
        else:
            gamma_frequencies.append(-np.sqrt(np.abs(val)))

    # Sort and convert to THz
    gamma_frequencies = np.array(gamma_frequencies) / 1e12 / (2 * np.pi)
    gamma_frequencies.sort()
    return gamma_frequencies
