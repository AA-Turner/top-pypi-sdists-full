"""
This module introduces the ForceConstantPotential object which acts as the
finalized force constant model.
"""

import pickle
import tarfile
import numpy as np

from collections import Counter
from typing import Any, Dict, List
from .core.atoms import Atoms
from .force_constant_model import ForceConstantModel
from .core.orbits import Orbit
from .core.orbits import OrientationFamily
from .core.tensors import rotation_to_cart_coord, rotate_tensor
from .input_output.read_write_files import (add_items_to_tarfile_pickle,
                                            add_items_to_tarfile_custom,
                                            add_list_to_tarfile_custom,
                                            read_items_pickle,
                                            read_list_custom)
from .input_output.logging_tools import logger


logger = logger.getChild('ForceConstantPotential')


class ForceConstantPotential:
    """ A finalized force constant model. Can produce force constants for any
    structure compatible with the structure for which the model was set up.

    Parameters
    ----------
    cs : ClusterSpace
        The cluster space the model is based upon
    parameters : numpy.ndarray
        The fitted paramteres
    metadata : dict
        metadata dictionary, will be pickled when object is written to file
    """

    def __init__(self, cs, parameters, metadata=None):

        self._prim = cs.primitive_structure.copy()
        self.cluster_list = cs.cluster_list.copy()
        self.atom_list = cs.atom_list.copy()
        self.orbits = []
        self.spacegroup = cs.spacegroup
        self._config = cs._config
        self.cs_summary = cs.summary

        # add metadata
        if metadata is None:
            metadata = dict()
        self._metadata = metadata
        self._add_default_metadata()

        # Extract the eigentensors from the cluster space and use the paramters
        # to construct the finalized force constants
        parameters = cs._map_parameters(parameters)
        p = 0
        for orb in cs.orbits:
            new_orbit = Orbit()
            fc = np.zeros(orb.eigentensors[0].shape)
            for et, a in zip(orb.eigentensors, parameters[p:]):
                fc += et * a
            new_orbit.force_constant = fc
            new_orbit.order = orb.order
            new_orbit.radius = orb.radius
            new_orbit.maximum_distance = orb.maximum_distance
            for of in orb.orientation_families:
                new_of = OrientationFamily()
                new_of.cluster_indices = of.cluster_indices.copy()
                sym_ind = of.symmetry_index
                R = rotation_to_cart_coord(cs.rotation_matrices[sym_ind],
                                           self.primitive_structure.cell)
                fc = rotate_tensor(new_orbit.force_constant, R.T)
                perm = cs.permutations[of.permutation_indices[0]]
                new_of.force_constant = fc.transpose(perm)
                new_orbit.orientation_families.append(new_of)
            self.orbits.append(new_orbit)
            p += len(orb.eigentensors)

    @property
    def symprec(self):
        return self._config['symprec']

    def write(self, filename):
        """ Writes a ForceConstantPotential to file.

        Parameters
        ----------
        filename : str
            name of file to write ForceConstantPotential to
        """

        # Create a tar archive
        if isinstance(filename, str):
            tar_file = tarfile.open(name=filename, mode='w')
        else:
            raise ValueError('filename must be str')

        # objects with custom write
        add_list_to_tarfile_custom(tar_file, self.orbits, 'orbits')

        # prim with its builtin write/read functions. Note prim is a hiphive.core.Atoms object
        items_custom = {'_prim': self._prim}
        add_items_to_tarfile_custom(tar_file, items_custom)

        # Attributes in pickle format
        pickle_attributes = ['_config', '_metadata', 'spacegroup', 'atom_list',
                             'cluster_list', 'cs_summary']
        items_pickle = dict()
        for attribute in pickle_attributes:
            items_pickle[attribute] = self.__getattribute__(attribute)
        add_items_to_tarfile_pickle(tar_file, items_pickle, 'attributes')

        # Done!
        tar_file.close()

    @staticmethod
    def read(filename):
        """ Reads a ForceConstantPotentialfrom file.

        Parameters
        ----------
        filename : str
            name of input file to load ForceConstantPotential from

        Returns
        -------
        ForceConstantPotential
            the original object as stored in the file
        """

        # Try usage of old read format, Remove in hiphive 1.0
        try:
            old_fcp = ForceConstantPotential._read_old(filename)
            logger.warning('This fcp was written with a version <1.0. Please rewrite it.')
            return old_fcp
        except Exception:
            pass

        # Instantiate empty cs obj.
        fcp = ForceConstantPotential.__new__(ForceConstantPotential)

        # Load from file on disk
        if type(filename) is str:
            tar_file = tarfile.open(mode='r', name=filename)
        else:
            raise ValueError('filename must be str')

        # Attributes with custom read
        fileobj = tar_file.extractfile('_prim')
        fcp._prim = Atoms.read(fileobj)

        fcp.orbits = read_list_custom(tar_file, 'orbits', Orbit.read)

        # Attributes
        attributes = read_items_pickle(tar_file, 'attributes')
        for name, value in attributes.items():
            fcp.__setattr__(name, value)

        # Done!
        tar_file.close()
        return fcp

    # TODO: Remove?
    def _write_old(self, f):
        """Writes a force constant potential to file using old format.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """
        if isinstance(f, str):
            with open(f, 'wb') as fobj:
                pickle.dump(self, fobj)
        else:
            try:
                pickle.dump(self, f)
            except Exception:
                raise Exception('Failed writing to file.')

    @staticmethod
    def _read_old(f):
        """Reads a force constant potential from file in old format.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)

        Returns
        -------
        ForceConstantPotential
            the original object as stored in the file
        """
        if isinstance(f, str):
            with open(f, 'rb') as fobj:

                # This allows for reading FCPs with ASE-3.17 and 3.18
                fcp = pickle.load(fobj)
                _prim = fcp._prim

                if hasattr(_prim, '_cell'):  # 3.17
                    cell = _prim._cell
                else:                       # 3.18
                    cell = _prim.cell[:]

                # assume PBC True (as it has to be True in hiphive)
                pbc = [True, True, True]

                new_prim = Atoms(
                    symbols=_prim.symbols, positions=_prim.positions, cell=cell, pbc=pbc)
                fcp._prim = new_prim
                return fcp
        else:
            return pickle.load(f)

    @property
    def metadata(self):
        """ dict : metadata associated with force constant potential """
        return self._metadata

    @property
    def primitive_structure(self):
        """ ase.Atoms : atomic structure """
        return self._prim.copy()

    @property
    def orbit_data(self) -> List[Dict[str, Any]]:
        """list of dictionaries containing detailed information for each
        orbit, e.g. cluster radius and force constant
        """
        data = []
        for orbit_index, orbit in enumerate(self.orbits):
            d = {}
            d['index'] = orbit_index
            d['order'] = orbit.order
            d['radius'] = orbit.radius
            d['maximum_distance'] = orbit.maximum_distance
            d['n_clusters'] = len(orbit.orientation_families)

            types = []
            for atom_ind in self.cluster_list[orbit.prototype_index]:
                types.append(self.primitive_structure.numbers[
                    self.atom_list[atom_ind].site])
            d['prototype_cluster'] = self.cluster_list[orbit.prototype_index]
            d['prototype_atom_types'] = types

            d['geometrical_order'] = len(set(d['prototype_cluster']))
            d['force_constant'] = orbit.force_constant
            d['force_constant_norm'] = np.linalg.norm(orbit.force_constant)
            data.append(d)
        return data

    def print_tables(self):
        """ Prints information concerning the underlying cluster space to stdout,including,
        e.g., the number of cluster, orbits, and parameters by order and number of bodies. """
        self.cs_summary.print_tables()

    def get_force_constants(self, atoms):
        """ Return the force constants of a compatible structure.

        Parameters
        ----------
        atoms : ase.Atoms
            input structure

        Returns
        -------
        ForceConstants
            force constants
        """
        return ForceConstantModel(atoms, self).get_force_constants()

    def __str__(self):
        orbits = self.orbit_data
        orbit_counts = Counter([orbit['order'] for orbit in orbits])
        cluster_counts = Counter()
        for orbit in orbits:
            cluster_counts[orbit['order']] += orbit['n_clusters']

        n = 54
        s = []
        s.append(' ForceConstantPotential '.center(n, '='))
        s.append(f'Spacegroup {self.spacegroup}')
        s.append(f'Cell:\n{self.primitive_structure.cell}')
        s.append(f'Basis:\n{self.primitive_structure.basis}')
        s.append(f'Numbers: {self.primitive_structure.numbers}')

        s.append(f'Cutoff matrix:\n{self.cs_summary._cutoff_matrix}')

        for order in sorted(orbit_counts.keys()):
            n_dofs = self.cs_summary.ndofs_by_order[order]
            s.append(f'Order {order}, #orbits {orbit_counts[order]}, #cluster '
                     f'{cluster_counts[order]}, #parameters {n_dofs}')
        s.append(f'Total number of orbits: {len(orbits)}')
        s.append(f'total number of clusters: {sum(cluster_counts.values())}')
        s.append(f'total number of parameters: {sum(self.cs_summary.ndofs_by_order.values())}')
        s.append(''.center(n, '='))
        return '\n'.join(s)

    def __repr__(self):
        return 'ForceConstantPotential(ClusterSpace({!r}, ...), [...])'.format(
            self.primitive_structure)

    def _add_default_metadata(self):
        """Adds default metadata to metadata dict."""
        import getpass
        import socket
        from datetime import datetime
        from . import __version__ as hiphive_version

        self._metadata['date_created'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self._metadata['username'] = getpass.getuser()
        self._metadata['hostname'] = socket.gethostname()
        self._metadata['hiphive_version'] = hiphive_version
