"""
This module provides the :class:`ClusterSpace` class.
"""

import os
import copy
import itertools
import pickle
import tarfile
import tempfile
from collections.abc import Iterable
from math import log10, floor

import numpy as np
import spglib

from _icet import ClusterSpace as _ClusterSpace
from _icet import _ClusterExpansionCalculator
from ase import Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
from icet.core.orbit_list import OrbitList
from icet.core.structure import structure_to_arrays
from icet.core.sublattices import Sublattices
from icet.tools.geometry import (ase_atoms_to_spglib_cell,
                                 call_spglib,
                                 get_occupied_primitive_structure)
from pandas import DataFrame


class ClusterSpace(_ClusterSpace):
    """This class provides functionality for generating and maintaining
    cluster spaces.

    Note
    ----
    In :program:`icet` all :class:`Atoms <ase.Atoms>` objects must have
    periodic boundary conditions. When constructing cluster expansions
    for surfaces and nanoparticles it is therefore recommended to
    surround the structure with vacuum and use periodic boundary
    conditions. This can be achieved by using :func:`Atoms.center <ase.Atoms.center>`.

    Parameters
    ----------
    structure
        Atomic structure.
    cutoffs
        Cutoff radii per order that define the cluster space.

        Cutoffs are specified in units of Ångstrom and refer to the
        longest distance between two atoms in the cluster. The first
        element refers to pairs, the second to triplets, the third
        to quadruplets, and so on. :attr:`cutoffs=[7.0, 4.5]` thus implies
        that all pairs distanced 7 Å or less will be included,
        as well as all triplets among which the longest distance is no
        longer than 4.5 Å.
    chemical_symbols
        List of chemical symbols, each of which must map to an element
        of the periodic table.

        If a list of chemical symbols is provided, all sites on the
        lattice will have the same allowed occupations as the input
        list.

        If a list of list of chemical symbols is provided then the
        outer list must be the same length as the :attr:`structure` object and
        :attr:`chemical_symbols[i]` will correspond to the allowed species
        on lattice site ``i``.
    symprec
        Tolerance imposed when analyzing the symmetry using spglib.
    position_tolerance
        Tolerance applied when comparing positions in Cartesian coordinates.

    Examples
    --------
    The following snippets illustrate several common situations::

        >>> from ase.build import bulk
        >>> from ase.io import read
        >>> from icet import ClusterSpace

        >>> # AgPd alloy with pairs up to 7.0 A and triplets up to 4.5 A
        >>> prim = bulk('Ag')
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 4.5],
        ...                   chemical_symbols=[['Ag', 'Pd']])
        >>> print(cs)

        >>> # (Mg,Zn)O alloy on rocksalt lattice with pairs up to 8.0 A
        >>> prim = bulk('MgO', crystalstructure='rocksalt', a=6.0)
        >>> cs = ClusterSpace(structure=prim, cutoffs=[8.0],
        ...                   chemical_symbols=[['Mg', 'Zn'], ['O']])
        >>> print(cs)

        >>> # (Ga,Al)(As,Sb) alloy with pairs, triplets, and quadruplets
        >>> prim = bulk('GaAs', crystalstructure='zincblende', a=6.5)
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 6.0, 5.0],
        ...                   chemical_symbols=[['Ga', 'Al'], ['As', 'Sb']])
        >>> print(cs)

        >>> # PdCuAu alloy with pairs and triplets
        >>> prim = bulk('Pd')
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 5.0],
        ...                   chemical_symbols=[['Au', 'Cu', 'Pd']])
        >>> print(cs)

    """

    def __init__(self,
                 structure: Atoms,
                 cutoffs: list[float],
                 chemical_symbols: list[str] | list[list[str]],
                 symprec: float = 1e-5,
                 position_tolerance: float | None = None) -> None:

        if not isinstance(structure, Atoms):
            raise TypeError('Input configuration must be an ASE Atoms object'
                            f', not type {type(structure)}.')
        if not all(structure.pbc):
            raise ValueError('Input structure must be periodic.')
        if symprec <= 0:
            raise ValueError('symprec must be a positive number.')

        self._config = {'symprec': symprec}
        self._cutoffs = cutoffs.copy()
        self._input_structure = structure.copy()
        self._input_chemical_symbols = copy.deepcopy(chemical_symbols)
        chemical_symbols = self._get_chemical_symbols()

        self._pruning_history: list[tuple] = []

        # set up primitive
        occupied_primitive, primitive_chemical_symbols = get_occupied_primitive_structure(
            self._input_structure, chemical_symbols, symprec=self.symprec)
        self._primitive_chemical_symbols = primitive_chemical_symbols
        assert len(occupied_primitive) == len(primitive_chemical_symbols)

        # derived tolerances
        if position_tolerance is None:
            self._config['position_tolerance'] = symprec
        else:
            if position_tolerance <= 0:
                raise ValueError('position_tolerance must be a positive number')
            self._config['position_tolerance'] = position_tolerance
        effective_box_size = abs(np.linalg.det(occupied_primitive.cell)) ** (1 / 3)
        tol = self.position_tolerance / effective_box_size
        tol = min(tol, self._config['position_tolerance'] / 5)
        self._config['fractional_position_tolerance'] = round(tol, -int(floor(log10(abs(tol)))))

        # set up orbit list
        orbit_list = OrbitList(
            structure=occupied_primitive,
            cutoffs=self._cutoffs,
            chemical_symbols=self._primitive_chemical_symbols,
            symprec=self.symprec,
            position_tolerance=self.position_tolerance,
            fractional_position_tolerance=self.fractional_position_tolerance)
        self._orbit_list = orbit_list.without_inactive_orbits()

        # call (base) C++ constructor
        _ClusterSpace.__init__(self, orbit_list=self._orbit_list)

    def _get_chemical_symbols(self):
        """ Returns chemical symbols using input structure and
        chemical symbols. Carries out multiple sanity checks. """

        # set up chemical symbols as list[list[str]]
        if all(isinstance(i, str) for i in self._input_chemical_symbols):
            chemical_symbols = [self._input_chemical_symbols] * len(self._input_structure)
        # also accept tuples and other iterables but not, e.g., list[list, str]
        # (need to check for str explicitly here because str is an Iterable)
        elif not all(isinstance(i, Iterable) and not isinstance(i, str)
                     for i in self._input_chemical_symbols):
            raise TypeError('chemical_symbols must be list[str] or list[list[str]], not {}'.format(
                type(self._input_chemical_symbols)))
        elif len(self._input_chemical_symbols) != len(self._input_structure):
            msg = 'chemical_symbols must have same length as structure. '
            msg += 'len(chemical_symbols) = {}, len(structure)= {}'.format(
                len(self._input_chemical_symbols), len(self._input_structure))
            raise ValueError(msg)
        else:
            chemical_symbols = copy.deepcopy(self._input_chemical_symbols)

        for i, symbols in enumerate(chemical_symbols):
            if len(symbols) != len(set(symbols)):
                raise ValueError(
                    'Found duplicates of allowed chemical symbols on site {}.'
                    ' allowed species on  site {}= {}'.format(i, i, symbols))

        if len([tuple(sorted(s)) for s in chemical_symbols if len(s) > 1]) == 0:
            raise ValueError('No active sites found')

        return chemical_symbols

    def _get_chemical_symbol_representation(self):
        """Returns a str version of the chemical symbols that is
        easier on the eyes.
        """
        sublattices = self.get_sublattices(self.primitive_structure)
        nice_str = []
        for sublattice in sublattices.active_sublattices:
            sublattice_symbol = sublattice.symbol
            nice_str.append('{} (sublattice {})'.format(
                list(sublattice.chemical_symbols), sublattice_symbol))
        return ', '.join(nice_str)

    def _get_string_representation(self,
                                   print_threshold: int | None = None,
                                   print_minimum: int = 10) -> str:
        """
        String representation of the cluster space that provides an overview of
        the orbits (order, radius, multiplicity etc) that constitute the space.

        Parameters
        ----------
        print_threshold
            if the number of orbits exceeds this number print dots
        print_minimum
            number of lines printed from the top and the bottom of the orbit
            list if `print_threshold` is exceeded

        Returns
        -------
        multi-line string
            string representation of the cluster space.
        """

        def repr_orbit(orbit, header=False):
            formats = {'order': '{:2}',
                       'radius': '{:8.4f}',
                       'multiplicity': '{:4}',
                       'index': '{:4}',
                       'orbit_index': '{:4}',
                       'multicomponent_vector': '{:}',
                       'sublattices': '{:}'}
            s = []
            for name, value in orbit.items():
                if name == 'sublattices':
                    str_repr = formats[name].format('-'.join(value))
                else:
                    str_repr = formats[name].format(value)
                n = max(len(name), len(str_repr))
                if header:
                    s += ['{s:^{n}}'.format(s=name, n=n)]
                else:
                    s += ['{s:^{n}}'.format(s=str_repr, n=n)]
            return ' | '.join(s)

        # basic information
        # (use largest orbit to obtain maximum line length)
        prototype_orbit = self.as_list[-1]
        width = len(repr_orbit(prototype_orbit))
        s = []
        s += ['{s:=^{n}}'.format(s=' Cluster Space ', n=width)]
        s += [' {:38} : {}'.format('space group', self.space_group)]
        s += [' {:38} : {}'
              .format('chemical species', self._get_chemical_symbol_representation())]
        s += [' {:38} : {}'.format('cutoffs',
                                   ' '.join(['{:.4f}'.format(c) for c in self.cutoffs]))]
        s += [' {:38} : {}'.format('total number of parameters', len(self))]
        t = ['{}= {}'.format(k, c)
             for k, c in self.number_of_orbits_by_order.items()]
        s += [' {:38} : {}'.format('number of parameters by order', '  '.join(t))]
        for key, value in sorted(self._config.items()):
            s += [' {:38} : {}'.format(key, value)]

        # table header
        s += [''.center(width, '-')]
        s += [repr_orbit(prototype_orbit, header=True)]
        s += [''.center(width, '-')]

        # table body
        index = 0
        orbit_list_info = self.as_list
        while index < len(orbit_list_info):
            if (print_threshold is not None and
                    len(self) > print_threshold and
                    index >= print_minimum and
                    index <= len(self) - print_minimum):
                index = len(self) - print_minimum
                s += [' ...']
            s += [repr_orbit(orbit_list_info[index])]
            index += 1
        s += [''.center(width, '=')]

        return '\n'.join(s)

    def __str__(self) -> str:
        """ String representation. """
        return self._get_string_representation(print_threshold=50)

    def _repr_html_(self) -> str:
        """ HTML representation. Used, e.g., in jupyter notebooks. """
        s = ['<h4>Cluster Space</h4>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>']
        s += ['<tbody>']
        s += [f'<tr><td style="text-align: left;">Space group</td><td>{self.space_group}</td></tr>']
        for sl in self.get_sublattices(self.primitive_structure).active_sublattices:
            s += [f'<tr><td style="text-align: left;">Sublattice {sl.symbol}</td>'
                  f'<td>{sl.chemical_symbols}</td></tr>']
        s += [f'<tr><td style="text-align: left;">Cutoffs</td><td>{self.cutoffs}</td></tr>']
        s += ['<tr><td style="text-align: left;">Total number of parameters</td>'
              f'<td>{len(self)}</td></tr>']
        for k, n in self.number_of_orbits_by_order.items():
            s += [f'<tr><td style="text-align: left;">Number of parameters of order {k}</td>'
                  f'<td>{n}</td></tr>']
        for key, value in sorted(self._config.items()):
            s += [f'<tr><td style="text-align: left;">{key}</td><td>{value}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)

    def __repr__(self) -> str:
        """ Representation. """
        s = type(self).__name__ + '('
        s += f'structure={self.primitive_structure.__repr__()}'
        s += f', cutoffs={self._cutoffs.__repr__()}'
        s += f', chemical_symbols={self._input_chemical_symbols.__repr__()}'
        s += f', position_tolerance={self._config["position_tolerance"]}'
        s += ')'
        return s

    def __getitem__(self, ind: int):
        return self.as_list[ind]

    @property
    def symprec(self) -> float:
        """ Tolerance imposed when analyzing the symmetry using spglib. """
        return self._config['symprec']

    @property
    def position_tolerance(self) -> float:
        """ Tolerance applied when comparing positions in Cartesian coordinates. """
        return self._config['position_tolerance']

    @property
    def fractional_position_tolerance(self) -> float:
        """ Tolerance applied when comparing positions in fractional coordinates. """
        return self._config['fractional_position_tolerance']

    @property
    def space_group(self) -> str:
        """ Space group of the primitive structure in international notion (via spglib). """
        structure_as_tuple = ase_atoms_to_spglib_cell(self.primitive_structure)
        return call_spglib(spglib.get_spacegroup, structure_as_tuple,
                           symprec=self._config['symprec'])

    @property
    def as_list(self) -> list[dict]:
        """Representation of cluster space as list with information regarding
        order, radius, multiplicity etc.
        """
        data = []
        zerolet = dict(
            index=0,
            order=0,
            radius=0,
            multiplicity=1,
            orbit_index=-1,
            multicomponent_vector='.',
            sublattices='.',
        )
        data.append(zerolet)

        sublattices = self.get_sublattices(self.primitive_structure)
        index = 0
        for orbit_index in range(len(self.orbit_list)):
            orbit = self.orbit_list.get_orbit(orbit_index)
            representative_cluster = orbit.representative_cluster
            orbit_sublattices = [
                sublattices[sublattices.get_sublattice_index_from_site_index(ls.index)].symbol
                for ls in representative_cluster.lattice_sites]
            for cv_element in orbit.cluster_vector_elements:
                index += 1
                data.append(dict(
                    index=index,
                    order=representative_cluster.order,
                    radius=representative_cluster.radius,
                    multiplicity=cv_element['multiplicity'],
                    orbit_index=orbit_index,
                    multicomponent_vector=cv_element['multicomponent_vector'],
                    sublattices=orbit_sublattices
                ))
        return data

    def to_dataframe(self) -> DataFrame:
        """ Returns a representation of the cluster space as a DataFrame. """
        df = DataFrame.from_dict(self.as_list)
        del df['index']
        return df

    @property
    def number_of_orbits_by_order(self) -> dict:
        """ Number of orbits by order in the form of a dictionary
        where keys and values represent order and number of orbits,
        respectively.
        """
        count_orbits: dict[int, int] = {}
        for orbit in self.as_list:
            k = orbit['order']
            count_orbits[k] = count_orbits.get(k, 0) + 1
        return dict(sorted(count_orbits.items()))

    def get_cluster_vector(self, structure: Atoms) -> np.ndarray:
        """
        Returns the cluster vector for a structure.

        The cluster vector is evaluated through the per-orbit evaluation
        tables of a calculator built for this structure, which is the single
        path by which cluster vectors are computed. Building those tables
        costs far less than enumerating the clusters of the supercell, so the
        calculator pays for itself already on the first evaluation.

        Parameters
        ----------
        structure
            Atomic configuration.
        """
        if not isinstance(structure, Atoms):
            raise TypeError('Input structure must be an ASE Atoms object')

        try:
            cv = self._build_calculator(structure).get_cluster_vector()
        except Exception as e:
            self.assert_structure_compatibility(structure)
            raise Exception(str(e))
        return cv

    def _get_cluster_vector_from_supercell_orbit_list(self, structure: Atoms) -> np.ndarray:
        """
        Returns the cluster vector for a structure, obtained by building a
        full supercell orbit list and counting the clusters it stores.

        This is the reference oracle against which the evaluation tables that
        :func:`get_cluster_vector` uses are checked. It is reachable for
        equivalence testing and is not used in production, being both slower
        and heavier in memory than the tables for every supercell size.

        Parameters
        ----------
        structure
            Atomic configuration.
        """
        if not isinstance(structure, Atoms):
            raise TypeError('Input structure must be an ASE Atoms object')

        try:
            cv = _ClusterSpace.get_cluster_vector_from_supercell_orbit_list(
                self,
                **structure_to_arrays(structure),
                fractional_position_tolerance=self.fractional_position_tolerance)
        except Exception as e:
            self.assert_structure_compatibility(structure)
            raise Exception(str(e))
        return cv

    def get_coordinates_of_representative_cluster(self, orbit_index: int) -> list[tuple[float]]:
        """
        Returns the positions of the sites in the representative cluster of the selected orbit.

        Parameters
        ----------
        orbit_index
            Index of the orbit for which to return the positions of the sites.
        """
        # Raise exception if chosen orbit index not in current list of orbit indices
        if orbit_index not in range(len(self._orbit_list)):
            raise ValueError('The input orbit index is not in the list of possible values.')
        return self._orbit_list.get_orbit(orbit_index).representative_cluster.positions

    def _set_orbit_list(self, orbit_list) -> None:
        """
        Bases this cluster space on the given orbit list.

        Orbit lists are immutable, so an edit produces a new one and this
        function is how it takes effect. Any calculator built from this cluster
        space earlier holds the previous orbit list and keeps evaluating the
        model it was built with.

        The attribute is assigned only once the C++ base has accepted the orbit
        list, so that a rejected orbit list leaves the two sides describing the
        same model rather than disagreeing.

        Parameters
        ----------
        orbit_list
            The orbit list this cluster space is to be based on.
        """
        _ClusterSpace._set_orbit_list(self, orbit_list=orbit_list)
        self._orbit_list = orbit_list

    def _remove_orbits(self, indices: list[int]) -> None:
        """
        Removes orbits.

        Parameters
        ----------
        indices
            Indices to all orbits to be removed.
        """
        size_before = len(self._orbit_list)
        self._set_orbit_list(self._orbit_list.without_orbits(sorted(indices)))
        size_after = len(self._orbit_list)
        assert size_before - len(indices) == size_after

    def prune_orbit_list(self, indices: list[int]) -> None:
        """
        Prunes the internal orbit list and maintains the history.

        Parameters
        ----------
        indices
            Indices to all orbits to be removed.
        """
        self._remove_orbits(indices)
        # A copy, since the history is what a later copy or write replays and
        # the caller remains free to reuse the container it passed in.
        self._pruning_history.append(('prune', copy.deepcopy(indices)))

    @property
    def primitive_structure(self) -> Atoms:
        """ Primitive structure on which cluster space is based. """
        structure = self._orbit_list.primitive_structure
        # Decorate with the "real" symbols (instead of H, He, Li etc)
        for atom, symbols in zip(structure, self._primitive_chemical_symbols):
            atom.symbol = min(symbols)
        return structure

    @property
    def chemical_symbols(self) -> list[list[str]]:
        """ Species identified by their chemical symbols. """
        return self._primitive_chemical_symbols.copy()

    @property
    def cutoffs(self) -> list[float]:
        """
        Cutoffs for different n-body clusters. The cutoff radius (in
        Ångstroms) defines the largest interatomic distance in a
        cluster.
        """
        return self._cutoffs

    @property
    def orbit_list(self):
        """ Orbit list that defines the cluster in the cluster space. """
        return self._orbit_list

    def get_possible_orbit_occupations(self, orbit_index: int) -> list[list[str]]:
        """ Returns possible occupations of the orbit.

        Parameters
        ----------
        orbit_index
            Index of orbit of interest.
        """
        # get_orbit copies the one orbit asked for, where the orbits property
        # copies all of them.
        # Both hand out copies, so the orbit list cannot be changed through
        # what they return.
        # A negative index counts from the end, as it does for a list, which
        # the binding does not accept since it takes an unsigned index.
        if orbit_index < 0:
            orbit_index += len(self.orbit_list)
        orbit = self.orbit_list.get_orbit(orbit_index)
        indices = [ls.index for ls in orbit.representative_cluster.lattice_sites]
        allowed_species = [self.chemical_symbols[index] for index in indices]
        return list(itertools.product(*allowed_species))

    def get_sublattices(self, structure: Atoms) -> Sublattices:
        """ Returns the sublattices of the input structure.

        Parameters
        ----------
        structure
            Atomic structure the sublattices are based on.
        """
        sl = Sublattices(self.chemical_symbols,
                         self.primitive_structure,
                         structure,
                         fractional_position_tolerance=self.fractional_position_tolerance)
        return sl

    def assert_structure_compatibility(self, structure: Atoms, vol_tol: float = 1e-5) -> None:
        """ Raises error if structure is not compatible with this cluster space.

        Parameters
        ----------
        structure
            Structure to check for compatibility with cluster space.
        vol_tol
            Tolerance imposed when comparing volumes.
        """
        # check volume
        vol1 = self.primitive_structure.get_volume() / len(self.primitive_structure)
        vol2 = structure.get_volume() / len(structure)
        if abs(vol1 - vol2) > vol_tol:
            raise ValueError(f'Volume per atom of structure ({vol1}) does not match the volume of'
                             f' the primitive structure ({vol2}; vol_tol= {vol_tol}).')

        # check occupations
        sublattices = self.get_sublattices(structure)
        sublattices.assert_occupation_is_allowed(structure.get_chemical_symbols())

        # check pbc
        if not all(structure.pbc):
            raise ValueError('Input structure must be periodic.')

    def merge_orbits(self,
                     equivalent_orbits: dict[int, list[int]],
                     ignore_permutations: bool = False) -> None:
        """ Combines several orbits into one. This allows one to make custom
        cluster spaces by manually declaring the clusters in two or more
        orbits to be equivalent. This is a powerful approach for simplifying
        the cluster spaces of low-dimensional structures such as
        surfaces or nanoparticles.

        The procedure works in principle for any number of components. Note,
        however, that in the case of more than two components the outcome of
        the merging procedure inherits the treatment of the multi-component
        vectors of the orbit chosen as the representative one.

        Parameters
        ----------
        equivalent_orbits
            The keys of this dictionary denote the indices of the orbit into
            which to merge. The values are the indices of the orbits that are
            supposed to be merged into the orbit denoted by the key.
        ignore_permutations
            If ``True`` orbits will be merged even if their multi-component
            vectors and/or site permutations differ. While the object will
            still be functional, the cluster space may not be properly spanned
            by the resulting cluster vectors.
            Orbits whose sites allow different species are rejected whatever
            this is set to. The merged orbit reads all of its clusters through
            the multi-component vectors of the orbit they are merged into, and
            those address the point functions of the species allowed on its
            sites.

        Note
        ----
        The orbit index should not be confused with the index shown when
        printing the cluster space.

        Examples
        --------
        The following snippet illustrates the use of this method to create a
        cluster space for a (111) FCC surface, in which only the singlets for
        the first and second layer are distinct as well as the in-plane pair
        interaction in the topmost layer. All other singlets and pairs are
        respectively merged into one orbit. After merging there aree only 3
        singlets and 2 pairs left with correspondingly higher multiplicities.

            >>> from icet import ClusterSpace
            >>> from ase.build import fcc111
            >>>
            >>> # Create primitive surface unit cell
            >>> structure = fcc111('Au', size=(1, 1, 8),
            ...                    a=4.1, vacuum=10, periodic=True)
            >>>
            >>> # Set up initial cluster space
            >>> cs = ClusterSpace(structure=structure,
            ...                   cutoffs=[3.8], chemical_symbols=['Au', 'Ag'])
            >>>
            >>> # At this point, one can inspect the orbits in the cluster space
            >>> # by printing the ClusterSpace object and accessing the individial
            >>> # orbits. There will be 4 singlets and 8 pairs.
            >>>
            >>> # Merge singlets for the third and fourth layers as well as all
            >>> # pairs except for the one corresponding to the in-plane
            >>> # interaction in the topmost surface layer.
            >>> cs.merge_orbits({2: [3], 4: [6, 7, 8, 9, 10, 11]})
        """

        orbits_already_merged = []
        for k1, orbit_indices in equivalent_orbits.items():
            orbit1 = self.orbit_list.get_orbit(k1)

            for k2 in orbit_indices:

                # sanity checks
                if k1 == k2:
                    raise ValueError(f'Cannot merge orbit {k1} with itself.')
                if k2 in orbits_already_merged:
                    raise ValueError(f'Orbit {k2} cannot be merged into orbit {k1}'
                                     ' since it was already merged with another orbit.')
                orbit2 = self.orbit_list.get_orbit(k2)
                if orbit1.order != orbit2.order:
                    raise ValueError(f'The order of orbit {k1} ({orbit1.order}) does not'
                                     f' match the order of orbit {k2} ({orbit2.order}).')

                if not ignore_permutations:
                    elements1 = orbit1.cluster_vector_elements
                    elements2 = orbit2.cluster_vector_elements
                    for element1, element2 in zip(elements1, elements2):
                        # compare site permutations
                        permutations1 = element1['site_permutations']
                        permutations2 = element2['site_permutations']
                        if len(permutations1) != len(permutations2) or \
                                not np.allclose(np.array(permutations1), np.array(permutations2)):
                            raise ValueError(f'Orbit {k1} and orbit {k2} have different '
                                             'site permutations.')

                        # compare multi-component vectors (maybe this is redundant because
                        # site permutations always differ if multi-component vectors differ?)
                        if not np.allclose(element1['multicomponent_vector'],
                                           element2['multicomponent_vector']):
                            raise ValueError(f'Orbit {k1} and orbit {k2} have different '
                                             'multi-component vectors.')

                    # The comparison above covers the elements the two orbits
                    # have in common. Orbits that agree there but describe
                    # different numbers of elements are still different, and
                    # merging them gives the clusters of one of them the
                    # multi-component vectors of the other. Two orbits of the
                    # same order differ in this way when they sit on
                    # sublattices with different numbers of allowed species.
                    if len(elements1) != len(elements2):
                        raise ValueError(f'Orbit {k1} and orbit {k2} describe different numbers'
                                         f' of cluster vector elements ({len(elements1)} and'
                                         f' {len(elements2)}).')

                orbits_already_merged.append(k2)

        # Merging and removing the merged-away orbits is a single operation on
        # the orbit list, so the cluster space never refers to an orbit list in
        # which the two have come apart.
        self._set_orbit_list(self._orbit_list.with_merged_orbits(equivalent_orbits))

        # update merge/prune history, once the merge has gone through, so that
        # a rejected merge leaves no entry for a later copy or write to replay.
        # A deep copy, since the history is what a later copy or write replays
        # and the caller remains free to reuse the container it passed in; the
        # lists inside the dictionary have to be copied too, not just the
        # dictionary itself.
        self._pruning_history.append(('merge', copy.deepcopy(equivalent_orbits)))

    def is_supercell_self_interacting(self, structure: Atoms) -> bool:
        """
        Checks whether a structure has self-interactions via periodic
        boundary conditions.
        Returns ``True`` if the structure contains self-interactions via periodic
        boundary conditions, otherwise ``False``.

        The answer describes the geometry of the supercell, so the species on
        its sites do not enter it and need not be ones this cluster space
        defines.
        The supercell does have to be commensurate with the primitive
        structure.

        Parameters
        ----------
        structure
            Structure to be tested.
        """
        return self._build_temporary_calculator(structure).is_self_interacting

    def are_local_cluster_vectors_additive(self, structure: Atoms) -> bool:
        """
        Checks whether the local cluster vectors of a supercell add up to its
        cluster vector.

        Local cluster vectors, as returned by
        :func:`ClusterExpansionCalculator.cpp_calc.get_local_cluster_vector
        <mchammer.calculators.ClusterExpansionCalculator>`, are an additive
        decomposition of the cluster vector: summed over all sites of the
        supercell they reproduce it.

        This holds unless a cluster contains the same site more than once
        through periodic images, which happens when the supercell is small
        enough for a cluster to reach a periodic image of one of its own sites.
        Such a cluster is counted with a weight of :math:`1/n` instead of once
        per site, where :math:`n` is the number of occurrences, and the sums
        fall short by the difference.

        Returns ``True`` if no cluster contains a repeated site, in which case
        the decomposition holds, otherwise ``False``.

        Note that this is a weaker requirement than the absence of
        self-interaction as tested by :func:`is_supercell_self_interacting`.
        A supercell can be self-interacting and still admit the decomposition.

        The answer describes the geometry of the supercell, so the species on
        its sites do not enter it and need not be ones this cluster space
        defines.
        The supercell does have to be commensurate with the primitive
        structure.

        Parameters
        ----------
        structure
            Structure to be tested.
        """
        return self._build_temporary_calculator(structure).are_local_cluster_vectors_additive

    def _build_temporary_calculator(self, structure: Atoms) -> _ClusterExpansionCalculator:
        """
        Returns a calculator for the given supercell, used to answer the
        setup-time questions above.
        The evaluation tables of a calculator determine both answers as a
        byproduct of their construction, and building them costs far less
        than the full supercell orbit list that answering from the orbit
        list would require.

        Both questions are about the geometry of the supercell, so the
        structure is decorated with species this cluster space defines before
        the calculator is built.
        A calculator validates the occupations it is constructed with, and the
        caller is entitled to ask either question about a supercell it has not
        decided how to decorate yet.

        Parameters
        ----------
        structure
            Supercell commensurate with the primitive structure of this
            cluster space.
        """
        decorated = structure.copy()
        try:
            sublattices = self.get_sublattices(decorated)
        except Exception:
            # Deciding the sublattices maps every position onto the primitive
            # cell, which fails for a supercell that is not commensurate with
            # it.
            # The structure is passed on as it is in that case, so that the
            # calculator reports why the supercell cannot be used rather than
            # this step reporting that a position could not be matched.
            sublattices = None
        if sublattices is not None:
            atomic_numbers = decorated.get_atomic_numbers()
            for sublattice in sublattices:
                atomic_numbers[sublattice.indices] = sublattice.atomic_numbers[0]
            decorated.set_atomic_numbers(atomic_numbers)

        return self._build_calculator(decorated)

    def _build_calculator(self, structure: Atoms) -> _ClusterExpansionCalculator:
        """
        Returns a calculator for the given supercell as it is occupied.

        This is the one place a calculator is built from a cluster space, and
        the evaluation tables it constructs are how cluster vectors are
        computed.

        Parameters
        ----------
        structure
            Supercell commensurate with the primitive structure of this
            cluster space, occupied by species this cluster space defines.
        """
        return _ClusterExpansionCalculator(
            cluster_space=self,
            **structure_to_arrays(structure),
            fractional_position_tolerance=self.fractional_position_tolerance)

    def get_multiplicities(self) -> list[int]:
        """
        Get multiplicities for each cluster space element as a list.
        """
        return [elem['multiplicity'] for elem in self.as_list]

    def write(self, filename: str) -> None:
        """
        Saves cluster space to a file.

        Parameters
        ---------
        filename
            Name of file to which to write.
        """

        with tarfile.open(name=filename, mode='w') as tar_file:

            # write items
            items = dict(cutoffs=self._cutoffs,
                         chemical_symbols=self._input_chemical_symbols,
                         pruning_history=self._pruning_history,
                         symprec=self.symprec,
                         position_tolerance=self.position_tolerance)
            temp_file = tempfile.TemporaryFile()
            pickle.dump(items, temp_file)
            temp_file.seek(0)
            tar_info = tar_file.gettarinfo(arcname='items', fileobj=temp_file)
            tar_file.addfile(tar_info, temp_file)
            temp_file.close()

            # write structure
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.close()
            ase_write(temp_file.name, self._input_structure, format='json')
            with open(temp_file.name, 'rb') as tt:
                tar_info = tar_file.gettarinfo(arcname='atoms', fileobj=tt)
                tar_file.addfile(tar_info, tt)
            os.remove(temp_file.name)

    @staticmethod
    def read(filename: str) -> 'ClusterSpace':
        """
        Reads cluster space from file and returns :attr:`ClusterSpace` object.

        Parameters
        ---------
        filename
            Name of file from which to read cluster space.
        """
        if isinstance(filename, str):
            tar_file = tarfile.open(mode='r', name=filename)
        else:
            tar_file = tarfile.open(mode='r', fileobj=filename)

        # read items
        items = pickle.load(tar_file.extractfile('items'))

        # read structure
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(tar_file.extractfile('atoms').read())
        temp_file.close()
        structure = ase_read(temp_file.name, format='json')
        os.remove(temp_file.name)

        tar_file.close()

        # ensure backward compatibility
        if 'symprec' not in items:  # pragma: no cover
            items['symprec'] = 1e-5
        if 'position_tolerance' not in items:  # pragma: no cover
            items['position_tolerance'] = items['symprec']

        cs = ClusterSpace(structure=structure,
                          cutoffs=items['cutoffs'],
                          chemical_symbols=items['chemical_symbols'],
                          symprec=items['symprec'],
                          position_tolerance=items['position_tolerance'])
        if len(items['pruning_history']) > 0:
            if isinstance(items['pruning_history'][0], tuple):
                for key, value in items['pruning_history']:
                    if key == 'prune':
                        cs.prune_orbit_list(value)
                    elif key == 'merge':
                        # Permutations are ignored here because a recorded merge
                        # was accepted once already, so a difference in them is
                        # not a reason to refuse it now.
                        # The checks that do not depend on this setting still
                        # apply, so a recorded merge of orbits whose sites allow
                        # different species is refused, as it is anywhere else.
                        cs.merge_orbits(value, ignore_permutations=True)
            else:  # for backwards compatibility
                for value in items['pruning_history']:
                    cs.prune_orbit_list(value)

        return cs

    def copy(self):
        """
        Returns copy of :class:`ClusterSpace` instance.

        The copy shares the orbit list with this cluster space, which is
        possible because orbit lists are immutable and because pruning or
        merging replaces the orbit list of a cluster space rather than changing
        it. Editing either cluster space therefore leaves the other as it was,
        and the copy costs no symmetry analysis and no orbit list construction.
        """
        cs_copy = ClusterSpace.__new__(ClusterSpace)

        cs_copy._config = self._config.copy()
        cs_copy._cutoffs = self._cutoffs.copy()
        cs_copy._input_structure = self._input_structure.copy()
        cs_copy._input_chemical_symbols = copy.deepcopy(self._input_chemical_symbols)
        cs_copy._primitive_chemical_symbols = copy.deepcopy(self._primitive_chemical_symbols)
        cs_copy._pruning_history = copy.deepcopy(self._pruning_history)

        cs_copy._orbit_list = self._orbit_list
        _ClusterSpace.__init__(cs_copy, orbit_list=self._orbit_list)
        return cs_copy
