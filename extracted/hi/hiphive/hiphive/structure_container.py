"""
This module provides functionality for storing structures and their fit
matrices together with target forces and displacements
"""

import tarfile
import numpy as np
from collections import OrderedDict
from ase.calculators.singlepoint import SinglePointCalculator

from .input_output.read_write_files import (add_items_to_tarfile_hdf5,
                                            add_items_to_tarfile_pickle,
                                            add_items_to_tarfile_custom,
                                            add_list_to_tarfile_custom,
                                            read_items_hdf5,
                                            read_items_pickle,
                                            read_list_custom)

from .cluster_space import ClusterSpace
from .force_constant_model import ForceConstantModel
from .input_output.logging_tools import logger
logger = logger.getChild('structure_container')


class StructureContainer:
    """
    This class serves as a container for structures as well as associated
    fit properties and fit matrices.

    Parameters
    -----------
    cs : ClusterSpace
        cluster space that is the basis for the container
    fit_structure_list : list(FitStructure)
         structures to be added to the container
    """

    def __init__(self, cs, fit_structure_list=None):
        """
        Attributes
        -----------
        _cs : ClusterSpace
            cluster space that is the basis for the container
        _structure_list : list(FitStructure)
            structures to add to container
        _previous_fcm : ForceConstantModel
            FCM object used for last fit matrix calculation; check will be
            carried out to decide if this FCM can be used for a new structure
            or not, which often enables a considerable speed-up
        """
        self._cs = cs.copy()
        self._previous_fcm = None

        # Add atoms from atoms_list
        self._structure_list = []
        if fit_structure_list is not None:
            for fit_structure in fit_structure_list:
                if not isinstance(fit_structure, FitStructure):
                    raise TypeError('Can only add FitStructures')
                self._structure_list.append(fit_structure)

    def __len__(self):
        return len(self._structure_list)

    def __getitem__(self, ind):
        return self._structure_list[ind]

    @property
    def data_shape(self):
        """ tuple : tuple of integers representing the shape of the fit data
        matrix """
        n_cols = self._cs.n_dofs
        n_rows = sum(len(fs) * 3 for fs in self)
        if n_rows == 0:
            return None
        return n_rows, n_cols

    @property
    def cluster_space(self):
        """ ClusterSpace : copy of the cluster space the structure
        container is based on"""
        return self._cs.copy()

    @staticmethod
    def read(fileobj, read_structures=True):
        """Restore a StructureContainer object from file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)
        read_structures : bool
            if True the structures will be read; if False only the cluster
            space will be read
        """
        if isinstance(fileobj, str):
            tar_file = tarfile.open(mode='r', name=fileobj)
        else:
            tar_file = tarfile.open(mode='r', fileobj=fileobj)

        # Read clusterspace
        f = tar_file.extractfile('cluster_space')
        cs = ClusterSpace.read(f)

        # Read fitstructures
        fit_structure_list = None
        if read_structures:
            fit_structure_list = read_list_custom(tar_file, 'fit_structure', FitStructure.read)

        # setup StructureContainer
        sc = StructureContainer(cs, fit_structure_list)

        # Read previous FCM if it exists
        if 'previous_fcm' in tar_file.getnames():
            f = tar_file.extractfile('previous_fcm')
            fcm = ForceConstantModel.read(f)
            sc._previous_fcm = fcm

        return sc

    def write(self, f):
        """Write a StructureContainer instance to a file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """

        if isinstance(f, str):
            tar_file = tarfile.open(mode='w', name=f)
        else:
            tar_file = tarfile.open(mode='w', fileobj=f)

        # save cs and previous_fcm (if it exists)
        custom_items = dict(cluster_space=self._cs)
        if self._previous_fcm is not None:
            custom_items['previous_fcm'] = self._previous_fcm
        add_items_to_tarfile_custom(tar_file, custom_items)

        # save fit structures
        add_list_to_tarfile_custom(tar_file, self._structure_list, 'fit_structure')

        tar_file.close()

    def add_structure(self, atoms, **meta_data):
        """Add a structure to the container.

        Note that custom information about the atoms object may not be
        stored inside, for example an ASE
        :class:`SinglePointCalculator` will not be kept.

        Parameters
        ----------
        atoms : ase.Atoms
            the structure to be added; the Atoms object must contain
            supplementary per-atom arrays with displacements and forces
        meta_data : dict
            dict with meta_data about the atoms
        """

        atoms_copy = atoms.copy()

        # atoms object must contain displacements
        if 'displacements' not in atoms_copy.arrays.keys():
            raise ValueError('Atoms must have displacements array')

        # atoms object must contain forces
        if 'forces' not in atoms_copy.arrays.keys():
            if isinstance(atoms.calc, SinglePointCalculator):
                atoms_copy.new_array('forces', atoms.get_forces())
            else:
                raise ValueError('Atoms must have forces')

        # check if an identical atoms object already exists in the container
        for i, structure in enumerate(self._structure_list):
            if are_configurations_equal(atoms_copy, structure.atoms):
                raise ValueError('Atoms is identical to structure {}'.format(i))

        logger.debug('Adding structure')
        M = self._compute_fit_matrix(atoms)
        structure = FitStructure(atoms_copy, M, **meta_data)
        self._structure_list.append(structure)

    def delete_all_structures(self):
        """ Remove all current structures in StructureContainer. """
        self._structure_list = []

    def get_fit_data(self, structures=None):
        """Return fit data for structures. The fit matrices and target forces
        for the structures are stacked into NumPy arrays.

        Parameters
        ----------
        structures: list, tuple
            list of integers corresponding to structure indices. Defaults to
            None and in that case returns all fit data available.

        Returns
        -------
        numpy.ndarray, numpy.ndarray
            stacked fit matrices, stacked target forces for the structures
        """
        if structures is None:
            structures = range(len(self))

        M_list, f_list = [], []
        for i in structures:
            M_list.append(self._structure_list[i].fit_matrix)
            f_list.append(self._structure_list[i].forces.flatten())

        if len(M_list) == 0:
            return None
        return np.vstack(M_list), np.hstack(f_list)

    def __str__(self):
        if len(self._structure_list) > 0:
            return self._get_str_structure_list()
        else:
            return 'Empty StructureContainer'

    def __repr__(self):
        return 'StructureContainer({!r}, {!r})'.format(
            self._cs, self._structure_list)

    def _get_str_structure_list(self):
        """ Return formatted string of the structure list """
        def str_structure(index, structure):
            fields = OrderedDict([
                ('index',     '{:^4}'.format(index)),
                ('num-atoms', '{:^5}'.format(len(structure))),
                ('avg-disp',  '{:7.4f}'
                 .format(np.mean([np.linalg.norm(d) for d in
                                  structure.displacements]))),
                ('avg-force', '{:7.4f}'
                 .format(np.mean([np.linalg.norm(f) for f in
                                  structure.forces]))),
                ('max-force', '{:7.4f}'
                 .format(np.max([np.linalg.norm(f) for f in
                                 structure.forces])))])
            s = []
            for name, value in fields.items():
                n = max(len(name), len(value))
                if index < 0:
                    s += ['{s:^{n}}'.format(s=name, n=n)]
                else:
                    s += ['{s:^{n}}'.format(s=value, n=n)]
            return ' | '.join(s)

        # table width
        dummy = self._structure_list[0]
        n = len(str_structure(-1, dummy))

        # table header
        s = []
        s.append(' Structure Container '.center(n, '='))
        s += ['{:22} : {}'.format('Total number of structures', len(self))]
        _, target_forces = self.get_fit_data()
        s += ['{:22} : {}'.format('Number of force components', len(target_forces))]
        s.append(''.center(n, '-'))
        s.append(str_structure(-1, dummy))
        s.append(''.center(n, '-'))

        # table body
        for i, structure in enumerate(self._structure_list):
            s.append(str_structure(i, structure))
        s.append(''.center(n, '='))
        return '\n'.join(s)

    def _compute_fit_matrix(self, atoms):
        """ Compute fit matrix for a single atoms object """
        logger.debug('Computing fit matrix')
        if atoms != getattr(self._previous_fcm, 'atoms', None):
            logger.debug('  Building new FCM object')
            self._previous_fcm = ForceConstantModel(atoms, self._cs)
        else:
            logger.debug('  Reusing old FCM object')
        return self._previous_fcm.get_fit_matrix(atoms.get_array('displacements'))


class FitStructure:
    """This class holds a structure with displacements and forces as well as
    the fit matrix.

    Parameters
    ----------
    atoms : ase.Atoms
        supercell structure
    fit_matrix : numpy.ndarray
        fit matrix, `N, M` array with `N = 3 * len(atoms)`
    meta_data : dict
        any meta data that needs to be stored in the FitStructure
    """

    def __init__(self, atoms, fit_matrix, **meta_data):
        if 3 * len(atoms) != fit_matrix.shape[0]:
            raise ValueError('fit matrix not compatible with atoms')
        self._atoms = atoms
        self._fit_matrix = fit_matrix
        self.meta_data = meta_data

    @property
    def fit_matrix(self):
        """ numpy.ndarray : the fit matrix """
        return self._fit_matrix

    @property
    def atoms(self):
        """ ase.Atoms : supercell structure """
        return self._atoms.copy()

    @property
    def forces(self):
        """ numpy.ndarray : forces """
        return self._atoms.get_array('forces')

    @property
    def displacements(self):
        """ numpy.ndarray : atomic displacements """
        return self._atoms.get_array('displacements')

    def __getattr__(self, key):
        """ Accesses meta_data if possible and returns value. """
        if key not in self.meta_data.keys():
            return super().__getattribute__(key)
        return self.meta_data[key]

    def __len__(self):
        return len(self._atoms)

    def __str__(self):
        s = []
        s.append(' FitStructure '.center(65, '='))
        s.append('Formula: {}'.format(self.atoms.get_chemical_formula()))
        s.append(('Cell:' + '\n   [{:9.5f} {:9.5f} {:9.5f}]'*3).format(
            *self.atoms.cell[0], *self.atoms.cell[1], *self.atoms.cell[2]))
        s.append('Atoms (positions, displacements, forces):')
        for atom, disp, force in zip(self.atoms, self.displacements, self.forces):
            array_fmt = '[ {:9.5f} {:9.5f} {:9.5f} ]'
            row_str = '{:3d} {}'.format(atom.index, atom.symbol)
            row_str += array_fmt.format(*atom.position)
            row_str += array_fmt.format(*disp)
            row_str += array_fmt.format(*force)
            s.append(row_str)
        return '\n'.join(s)

    def __repr__(self):
        return 'FitStructure({!r}, ..., {!r})'.format(self.atoms, self.meta_data)

    def write(self, fileobj):
        """ Write the instance to file.

        Parameters
        ----------
        fileobj : str or file object
            name of input file (str) or stream to write to (file object)
        """
        if isinstance(fileobj, str):
            tar_file = tarfile.open(name=fileobj, mode='w')
        else:
            tar_file = tarfile.open(fileobj=fileobj, mode='w')

        items_pickle = dict(atoms=self._atoms, meta_data=self.meta_data)
        items_hdf5 = dict(fit_matrix=self.fit_matrix)

        add_items_to_tarfile_pickle(tar_file, items_pickle, 'items.pickle')
        add_items_to_tarfile_hdf5(tar_file, items_hdf5, 'fit_matrix.hdf5')

        tar_file.close()

    @staticmethod
    def read(fileobj, read_fit_matrix=True):
        """ Read a OrientationFamily instance from a file.

        Parameters
        ----------
        fileobj : str or file object
            name of input file (str) or stream to read from (file object)
        read_fit_matrix : bool
            whether or not to read the fit_matrix
        Returns
        -------
        FitStructure instance
        """
        if isinstance(fileobj, str):
            tar_file = tarfile.open(mode='r', name=fileobj)
        else:
            tar_file = tarfile.open(mode='r', fileobj=fileobj)

        items = read_items_pickle(tar_file, 'items.pickle')
        fit_matrix = read_items_hdf5(tar_file, 'fit_matrix.hdf5')['fit_matrix']

        return FitStructure(items['atoms'], fit_matrix, **items['meta_data'])


def are_configurations_equal(atoms1, atoms2, tol=1e-10):
    """ Compare if two configurations are equal within some tolerance. This
    includes checking all available arrays in the two atoms objects.

    Parameters
    ----------
    atoms1 : ase.Atoms
    atoms2 : ase.Atoms

    Returns
    -------
    bool
        True if atoms are equal, False otherwise
    """

    # pbc
    if not all(atoms1.pbc == atoms2.pbc):
        return False

    # cell
    if not np.allclose(atoms1.cell, atoms2.cell, atol=tol, rtol=0.0):
        return False

    # arrays
    if not len(atoms1.arrays.keys()) == len(atoms2.arrays.keys()):
        return False
    for key, array1 in atoms1.arrays.items():
        if key not in atoms2.arrays.keys():
            return False
        if not np.allclose(array1, atoms2.arrays[key], atol=tol, rtol=0.0):
            return False

    # passed all test, atoms must be equal
    return True
