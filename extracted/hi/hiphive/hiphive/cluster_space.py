"""
Contains the ClusterSpace object central to hiPhive
"""

import numpy as np
import tarfile

from ase.data import chemical_symbols
from collections import OrderedDict
from copy import deepcopy

from .core.cluster_space_builder import build_cluster_space
from .core.atoms import Atoms
from .core.orbits import Orbit
from .cluster_space_data import ClusterSpaceData
from .input_output.logging_tools import logger
from .input_output.read_write_files import (add_items_to_tarfile_pickle,
                                            add_items_to_tarfile_custom,
                                            add_list_to_tarfile_custom,
                                            read_items_pickle,
                                            read_list_custom)
from .cutoffs import Cutoffs, CutoffMaximumBody, BaseClusterFilter

from .config import Config
logger = logger.getChild('ClusterSpace')


class ClusterSpace:
    """Primitive object for handling clusters and force constants of a structure.

    Parameters
    ----------
    prototype_structure : ase.Atoms
        prototype structure; spglib will be used to find a suitable cell based
        on this structure unless the cell is already a primitive cell.
    cutoffs : list or Cutoffs
        cutoff radii for different orders starting with second order
    cluster_filter : ClusterFilter
        accepts a subclass of hiphive.filters.BaseClusterFilter to further
        control which orbits to include.
    config : Config object
        a configuration object that holds information on how the cluster space
        should be built, e.g., values for tolerances and specifications
        regarding the handling of acoustic sum rules; if ``config`` is
        not given then the keyword arguments that follow below can be
        used for configuration.
    acoustic_sum_rules : bool
        If True the aucostic sum rules will be enforced by constraining the
        parameters.
    symprec : float
        numerical precision that will be used for analyzing the symmetry (this
        parameter will be forwarded to
        `spglib <https://phonopy.github.io/spglib/>`_)
    length_scale : float
        This will be used as a normalization constant for the eigentensors

    Examples
    --------

    To instantiate a :class:`ClusterSpace` object one has to specify a
    prototype structure and cutoff radii for each cluster order that
    should be included.  For example the following snippet will set up
    a :class:`ClusterSpace` object for a body-centered-cubic (BCC)
    structure including second order terms up to a distance of 5 A and
    third order terms up to a distance of 4 A.

    >>> from ase.build import bulk
    >>> from hiphive import ClusterSpace
    >>> prim = bulk('W')
    >>> cs = ClusterSpace(prim, [5.0, 4.0])

    """
    # TODO: This class probably needs some more documentation

    def __init__(self, prototype_structure, cutoffs, config=None,
                 cluster_filter=None, **kwargs):

        if not all(prototype_structure.pbc):
            raise ValueError('prototype_structure must have pbc.')

        if isinstance(cutoffs, Cutoffs):
            self._cutoffs = cutoffs
        elif isinstance(cutoffs, list):
            self._cutoffs = CutoffMaximumBody(cutoffs, len(cutoffs) + 1)
        else:
            raise TypeError('cutoffs must be a list or a Cutoffs object')

        if config is None:
            config = Config(**kwargs)
        else:
            if not isinstance(config, Config):
                raise TypeError('config kw must be of type {}'.format(Config))
            if len(kwargs) > 0:
                raise ValueError('use either Config or kwargs, not both')
        self._config = config

        if cluster_filter is None:
            self._cluster_filter = BaseClusterFilter()
        else:
            self._cluster_filter = cluster_filter

        self._atom_list = None
        self._cluster_list = None
        self._symmetry_dataset = None
        self._permutations = None
        self._prim = None
        self._orbits = None

        self._constraint_vectors = None
        # TODO: How to handle the constraint matrices? Should they even be
        # stored?
        self._constraint_matrices = None
        # Is this the best way or should the prim be instantiated separately?

        build_cluster_space(self, prototype_structure)
        self.summary = ClusterSpaceData(self)

    # TODO: Should everything here be properties? deepcopy/ref etc.?
    @property
    def n_dofs(self):
        """int : number of free parameters in the model

        If the sum rules are not enforced the number of DOFs is the same as
        the total number of eigentensors in all orbits.
        """
        return self._get_n_dofs()

    @property
    def cutoffs(self):
        """ Cutoffs : cutoffs used for constructing the cluster space """
        return deepcopy(self._cutoffs)

    @property
    def symprec(self):
        """ float : symprec value used when constructing the cluster space """
        return self._config['symprec']

    @property
    def acoustic_sum_rules(self):
        """ bool : True if acoustic sum rules are enforced """
        return self._config['acoustic_sum_rules']

    @property
    def length_scale(self):
        """ float : normalization constant of the force constants """
        return self._config['length_scale']

    @property
    def primitive_structure(self):
        """ ase.Atoms : structure of the lattice """
        return self._prim.copy()

    @property
    def spacegroup(self):
        """ str : space group of the lattice structure obtained from spglib """
        return f'{self._symmetry_dataset.international} ({self._symmetry_dataset.number})'

    @property
    def wyckoff_sites(self):
        """ list : wyckoff sites in the primitive cell """
        return self._symmetry_dataset.equivalent_atoms

    @property
    def rotation_matrices(self):
        """ list(numpy.ndarray) : symmetry elements (`3x3` matrices)
        representing rotations """
        return self._symmetry_dataset.rotations.copy()

    @property
    def translation_vectors(self):
        """ list(numpy.ndarray) : symmetry elements representing
        translations """
        # TODO: bug incoming!
        return (self._symmetry_dataset.translations % 1).copy()

    @property
    def permutations(self):
        """ list(numpy.ndarray) : lookup for permutation references """
        return deepcopy(self._permutations)

    @property
    def atom_list(self):
        """ BiMap : atoms inside the cutoff relative to the of the center cell
        """
        return self._atom_list

    @property
    def cluster_list(self):
        """ BiMap : clusters possible within the cutoff """
        return self._cluster_list

    @property
    def orbits(self):  # TODO: add __getitem__ method
        """ list(Orbit) : orbits associated with the lattice structure. """
        return self._orbits

    @property
    def orbit_data(self):
        """ list(dict) : detailed information for each orbit, e.g., cluster
        radius and atom types.
        """
        data = []
        p = 0
        for orbit_index, orbit in enumerate(self.orbits):
            d = {}
            d['index'] = orbit_index
            d['order'] = orbit.order
            d['radius'] = orbit.radius
            d['maximum_distance'] = orbit.maximum_distance
            d['n_clusters'] = len(orbit.orientation_families)
            d['eigentensors'] = orbit.eigentensors
            d['n_parameters'] = len(d['eigentensors'])

            types, wyckoff_sites = [], []
            for atom_index in self.cluster_list[orbit.prototype_index]:
                atom = self.atom_list[atom_index]
                types.append(self.primitive_structure.numbers[atom.site])
                wyckoff_sites.append(self.wyckoff_sites[atom.site])
            d['prototype_cluster'] = self.cluster_list[orbit.prototype_index]
            d['prototype_atom_types'] = tuple(types)
            d['prototype_wyckoff_sites'] = tuple(wyckoff_sites)

            d['geometrical_order'] = len(set(d['prototype_cluster']))
            d['parameter_indices'] = np.arange(p, p + len(orbit.eigentensors))

            p += len(orbit.eigentensors)
            data.append(d)

        return data

    def get_parameter_indices(self, order):
        """
        Returns a list of the parameter indices associated with the requested
        order.

        Parameters
        ----------
        order : int
            order for which to return the parameter indices

        Returns
        -------
        list(int)
            list of parameter indices associated with the requested order

        Raises
        ------
        ValueError
            if the order is not included in the cluster space
         """
        order = int(order)
        if order not in self.cutoffs.orders:
            raise ValueError('Order must be in {}'.format(self.cutoffs.orders))
        min_param = 0
        max_param = 0
        for orbit in self.orbits:
            if orbit.order < order:
                min_param += len(orbit.eigentensors)
                max_param = min_param
            elif orbit.order == order:
                max_param += len(orbit.eigentensors)
            else:
                break
        rows, cols = self._cvs.nonzero()
        parameters = set()
        for r, c in zip(rows, cols):
            if min_param <= r < max_param:
                parameters.add(c)
        for r, c in zip(rows, cols):
            if c in parameters:
                assert min_param <= r < max_param, 'The internals are broken!'

        return sorted(parameters)

    def get_n_dofs_by_order(self, order):
        """ Returns number of degrees of freedom for the given order.

        Parameters
        ----------
        order : int
            order for which to return the number of dofs

        Returns
        -------
        int
            number of degrees of freedom
        """
        return len(self.get_parameter_indices(order=order))

    def _get_n_dofs(self):
        """ Returns the number of degrees of freedom. """
        return self._cvs.shape[1]

    def _map_parameters(self, parameters):
        """ Maps irreducible parameters to the real parameters associated with
        the eigentensors.
        """
        if len(parameters) != self.n_dofs:
            raise ValueError('Invalid number of parameters, please provide {} '
                             'parameters'.format(self.n_dofs))
        return self._cvs.dot(parameters)

    def print_tables(self):
        """ Prints information concerning the underlying cluster space to stdout,including,
        e.g., the number of cluster, orbits, and parameters by order and number of bodies. """
        self.summary.print_tables()

    def print_orbits(self):
        """ Prints a list of all orbits. """
        orbits = self.orbit_data

        def str_orbit(index, orbit):
            elements = ' '.join(chemical_symbols[n] for n in
                                orbit['prototype_atom_types'])
            fields = OrderedDict([
                ('index',        '{:^3}'.format(index)),
                ('order',        '{:^3}'.format(orbit['order'])),
                ('elements',     '{:^18}'.format(elements)),
                ('radius',       '{:^8.4f}'.format(orbit['radius'])),
                ('prototype',    '{:^18}'.format(str(orbit['prototype_cluster']))),
                ('clusters',     '{:^4}'.format(orbit['n_clusters'])),
                ('parameters',   '{:^3}'.format(len(orbit['eigentensors']))),
                ])

            s = []
            for name, value in fields.items():
                n = max(len(name), len(value))
                if index < 0:
                    s += ['{s:^{n}}'.format(s=name, n=n)]
                else:
                    s += ['{s:^{n}}'.format(s=value, n=n)]
            return ' | '.join(s)

        # table header
        width = max(len(str_orbit(-1, orbits[-1])), len(str_orbit(0, orbits[-1])))
        print(' List of Orbits '.center(width, '='))
        print(str_orbit(-1, orbits[0]))
        print(''.center(width, '-'))

        # table body
        for i, orbit in enumerate(orbits):
            print(str_orbit(i, orbit))
        print(''.center(width, '='))

    def __str__(self):

        def str_order(order, header=False):
            formats = {'order':        '{:2}',
                       'n_orbits':   '{:5}',
                       'n_clusters': '{:5}'}
            s = []
            for name, value in order.items():
                str_repr = formats[name].format(value)
                n = max(len(name), len(str_repr))
                if header:
                    s += ['{s:^{n}}'.format(s=name, n=n)]
                else:
                    s += ['{s:^{n}}'.format(s=str_repr, n=n)]
            return ' | '.join(s)

        # collect data
        orbits = self.orbit_data
        orders = self.cutoffs.orders

        order_data = {o: dict(order=o, n_orbits=0, n_clusters=0) for o in orders}
        for orbit in orbits:
            o = orbit['order']
            order_data[o]['n_orbits'] += 1
            order_data[o]['n_clusters'] += orbit['n_clusters']

        # prototype with max order to find column width
        max_order = max(orders)
        prototype = order_data[max_order]
        n = max(len(str_order(prototype)), 54)

        # basic information
        s = []
        s.append(' Cluster Space '.center(n, '='))
        data = [('Spacegroup',               self.spacegroup),
                ('symprec',                  self.symprec),
                ('Sum rules',                self.acoustic_sum_rules),
                ('Length scale',             self.length_scale),
                ('Cutoffs',                  self.cutoffs),
                ('Cell',                     self.primitive_structure.cell),
                ('Basis',                    self.primitive_structure.basis),
                ('Numbers',                  self.primitive_structure.numbers),
                ('Total number of orbits',   len(orbits)),
                ('Total number of clusters',
                 sum([order_data[order]['n_clusters'] for order in orders])),
                ('Total number of parameters', self._get_n_dofs()
                 )]
        for field, value in data:
            if str(value).count('\n') > 1:
                s.append('{:26} :\n{}'.format(field, value))
            else:
                s.append('{:26} : {}'.format(field, value))

        # table header
        s.append(''.center(n, '-'))
        s.append(str_order(prototype, header=True))
        s.append(''.center(n, '-'))
        for order in orders:
            s.append(str_order(order_data[order]).rstrip())
        s.append(''.center(n, '='))
        return '\n'.join(s)

    def __repr__(self):
        s = 'ClusterSpace({!r}, {!r}, {!r})'
        return s.format(self.primitive_structure, self.cutoffs, self._config)

    def copy(self):
        return deepcopy(self)

    def write(self, fileobj):
        """ Writes cluster space to file.

        The instance is saved into a custom format based on tar-files. The
        resulting file will be a valid tar file and can be browsed by by a tar
        reader. The included objects are themself either pickles, npz or other
        tars.

        Parameters
        ----------
        fileobj : str or file-like object
            If the input is a string a tar archive will be created in the
            current directory. Otherwise the input must be a valid file
            like object.
        """
        # Create a tar archive
        if isinstance(fileobj, str):
            tar_file = tarfile.open(name=fileobj, mode='w')
        else:
            tar_file = tarfile.open(fileobj=fileobj, mode='w')

        # Attributes in pickle format
        pickle_attributes = ['_config',
                             '_symmetry_dataset', '_permutations',
                             '_atom_list', '_cluster_list']
        items_pickle = dict()
        for attribute in pickle_attributes:
            items_pickle[attribute] = self.__getattribute__(attribute)
        add_items_to_tarfile_pickle(tar_file, items_pickle, 'attributes')

        # Constraint matrices and vectors in hdf5 format
        items = dict(cvs=self._cvs)
        add_items_to_tarfile_pickle(tar_file, items, 'constraint_vectors')

        # Cutoffs and prim with their builtin write/read functions
        items_custom = {'_cutoffs': self._cutoffs, '_prim': self._prim}
        add_items_to_tarfile_custom(tar_file, items_custom)

        # Orbits
        add_list_to_tarfile_custom(tar_file, self._orbits, 'orbits')
        add_list_to_tarfile_custom(tar_file, self._dropped_orbits,
                                   'dropped_orbits')

        # Done!
        tar_file.close()

    def read(f):
        """ Reads a cluster space from file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)
        """

        # Instantiate empty cs obj.
        cs = ClusterSpace.__new__(ClusterSpace)

        # Load from file on disk or file-like
        if type(f) is str:
            tar_file = tarfile.open(mode='r', name=f)
        else:
            tar_file = tarfile.open(mode='r', fileobj=f)

        # Attributes
        attributes = read_items_pickle(tar_file, 'attributes')
        for name, value in attributes.items():
            cs.__setattr__(name, value)

        # Load the constraint matrices into their dict
        items = read_items_pickle(tar_file, 'constraint_vectors')
        cs._cvs = items['cvs']

        # Cutoffs and prim via custom save funcs
        fileobj = tar_file.extractfile('_cutoffs')
        cs._cutoffs = Cutoffs.read(fileobj)

        fileobj = tar_file.extractfile('_prim')
        cs._prim = Atoms.read(fileobj)

        # Orbits are stored in a separate archive
        cs._orbits = read_list_custom(tar_file, 'orbits', Orbit.read)
        cs._dropped_orbits = read_list_custom(
            tar_file, 'dropped_orbits', Orbit.read)

        tar_file.close()

        # create summary object based on CS
        cs.summary = ClusterSpaceData(cs)

        # Done!
        return cs
