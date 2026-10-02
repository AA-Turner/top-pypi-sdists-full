"""
This module provides the ConvexHull class.
"""

from typing import TYPE_CHECKING

import numpy as np
from collections.abc import Sized
from scipy.spatial import ConvexHull as ConvexHullSciPy
from scipy.spatial import Delaunay
from scipy.spatial import QhullError

if TYPE_CHECKING:
    # Imported for the annotations only.  `icet.core.cluster_space` imports
    # `icet.tools.geometry`, so importing it here at run time would close a
    # cycle through `icet.tools`.
    from ase import Atoms
    from icet.core.cluster_space import ClusterSpace

# Facets whose normal has a vertical component smaller than this are treated as
# vertical, i.e., as side walls of the hull rather than as part of the lower
# hull.  The value is dimensionless because Qhull normalizes the facet normals
# to unit length.
_VERTICAL_FACET_TOLERANCE = 1e-10

# Tolerance used when testing whether a target concentration lies inside the
# region spanned by the input concentrations.  Concentrations are of order one,
# so an absolute tolerance is appropriate.
_INSIDE_TOLERANCE = 1e-9

# A species whose concentration varies by less than this across the input is
# taken to be held fixed.
_CONSTANT_CONCENTRATION_TOLERANCE = 1e-12

# A barycentric coordinate may fall below zero by this much and the point still
# counts as lying inside the simplex.  Anything more negative means that the
# point lies in a different simplex of the same face.
_BARYCENTRIC_TOLERANCE = 1e-10

# How closely the barycentric coordinates have to reproduce a concentration for
# the simplex to describe it.  Concentrations are of order one, so an absolute
# tolerance is appropriate.
_REPRODUCTION_TOLERANCE = 1e-9

# A face whose plane comes this close to the largest value taken at a target
# is treated as supporting the hull there as well.  The value is relative to
# the range of the energies.
_PLANE_TIE_TOLERANCE = 1e-9

# How well one chemical potential per species has to reproduce the differences
# that are resolved by sublattice for the two to describe the same face.  The
# value is relative to the size of those differences.
_POTENTIAL_RESIDUAL_TOLERANCE = 1e-8


class ConvexHull:
    """This class provides functionality for extracting the convex hull
    of the (free) energy of mixing. It is based on the `convex hull
    calculator in SciPy
    <http://docs.scipy.org/doc/scipy-dev/reference/\
generated/scipy.spatial.ConvexHull.html>`_.

    Only the lower part of the hull is retained, i.e., the part that minimizes
    rather than maximizes the energy. It is obtained directly from the facets
    of the hull, namely those whose outward normal points downward along the
    energy axis.

    Parameters
    ----------
    concentrations
        Concentrations for each structure listed as ``[[c1, c2], [c1, c2],
        ...]``; for binaries, in which case there is only one independent
        concentration, the format ``[c1, c2, c3, ...]`` works as well.
    energies
        Energy (or energy of mixing) for each structure.

    Attributes
    ----------
    concentrations : np.ndarray
        Concentrations of the structures on the convex hull.
    energies : np.ndarray
        Energies of the structures on the convex hull.
    dimensions : int
        Number of independent concentrations needed to specify a point in
        concentration space (1 for binaries, 2 for ternaries and so on).
    structures : list[int]
        Indices of structures that constitute the convex hull (indices are
        defined by the order of their concentrations and energies are fed when
        initializing the :class:`ConvexHull` object).

    Examples
    --------
    A :class:`ConvexHull` object is easily initialized by providing lists of
    concentrations and energies::

        >>> data = {'concentration': [0,    0.2,  0.2,  0.3,  0.4,  0.5,  0.8,  1.0],
        ...         'mixing_energy': [0.1, -0.2, -0.1, -0.2,  0.2, -0.4, -0.2, -0.1]}
        >>> hull = ConvexHull(data['concentration'], data['mixing_energy'])

    Now one can for example access the points along the convex hull directly::

        >>> for c, e in zip(hull.concentrations, hull.energies):
        ...     print(c, e)
        0.0 0.1
        0.2 -0.2
        0.5 -0.4
        1.0 -0.1

    or plot the convex hull along with the original data using e.g., matplotlib::

        >>> import matplotlib.pyplot as plt
        >>> plt.scatter(data['concentration'], data['mixing_energy'], color='darkred')
        >>> plt.plot(hull.concentrations, hull.energies)
        >>> plt.show(block=False)

    It is also possible to extract structures at or close to the convex hull::

        >>> low_energy_structures = hull.extract_low_energy_structures(
        ...     data['concentration'], data['mixing_energy'],
        ...     energy_tolerance=0.005)

    A complete example can be found in the :ref:`basic tutorial
    <tutorial_enumerate_structures>`.
    """

    def __init__(self,
                 concentrations: list[float] | list[list[float]],
                 energies: list[float]) -> None:
        if len(concentrations) != len(energies):
            raise ValueError('concentrations and energies must have the same length')

        self._input_concentrations = _as_concentration_array(concentrations)
        self._input_energies = np.asarray(energies, dtype=float)
        self.dimensions = self._input_concentrations.shape[1]

        _validate_input(self._input_concentrations, self._input_energies, self.dimensions)

        # The lower hull is unchanged by a shift of the energy axis and by a
        # positive scaling of it.  Both are applied here, because Qhull works
        # on the coordinates as they are given: energies that share a large
        # offset differ from one another only in their trailing digits, and
        # dividing by the range without removing the offset first would
        # magnify it.  Energies that are all equal carry no scale of their own
        # and keep a scale of one.
        self._energy_offset = float(np.mean(self._input_energies))
        self._energy_scale = float(np.ptp(self._input_energies)) or 1.0
        self._scaled_energies = (self._input_energies - self._energy_offset) / self._energy_scale

        # Region of concentration space that is spanned by the input, used to
        # decide whether a target concentration lies inside the hull.
        self._domain_equations = _concentration_domain_equations(self._input_concentrations)

        # If the energies are an affine function of the concentrations, the
        # points lie on a single hyperplane rather than on a hull with an
        # interior, which Qhull cannot handle.  The hull is then that
        # hyperplane.
        points = np.column_stack((self._input_concentrations, self._scaled_energies))
        self._planar = _affine_rank(points) <= self.dimensions
        if self._planar:
            self._simplices = self._triangulate_domain()
            equations = np.tile(self._fit_plane(), (len(self._simplices), 1))
        else:
            self._simplices, equations = self._compute_lower_hull(points)

        # Qhull triangulates a facet that has more than `dimensions + 1`
        # vertices, so one face of the hull can arrive as several simplices
        # that share a plane.  Such a face is a single region of coexistence
        # and has to be treated as one.
        self._face_equations, self._face_simplices, self._face_vertices = \
            _group_coplanar_simplices(self._simplices, equations)

        structures = self._collect_hull_structures()
        self.concentrations = self._input_concentrations[structures]
        if self.dimensions == 1:
            # With a single independent concentration the points form a line
            # and it is more useful to have them sorted along it.
            order = np.argsort(self.concentrations[:, 0], kind='stable')
            structures = structures[order]
            self.concentrations = self.concentrations[order, 0]
        self.energies = self._input_energies[structures]
        self.structures = [int(s) for s in structures]

        # Set by `from_sublattice_concentrations`, which knows what each
        # independent concentration refers to.
        self._concentration_labels = None
        self._dependent_species = None
        # The concentrations of an array are taken to refer to all sites, so a
        # change of one site changes them by 1/N.
        self._site_fractions = np.ones(self.dimensions)

    @property
    def concentration_labels(self) -> list[tuple[str, str]] | None:
        """The species that each independent concentration refers to, as
        ``(sublattice symbol, chemical symbol)`` pairs in the order of the
        columns of :attr:`concentrations`, of the target concentrations of the
        various methods, and of the columns returned by
        :func:`get_chemical_potentials`.

        This is ``None`` unless the object was created with
        :func:`from_sublattice_concentrations`.
        """
        if self._concentration_labels is None:
            return None
        return list(self._concentration_labels)

    @classmethod
    def from_sublattice_concentrations(
            cls,
            concentrations: list[dict],
            energies: list[float],
            site_fractions: dict[str, float] | None = None,
            cluster_space: 'ClusterSpace | None' = None) -> 'ConvexHull':
        """Constructs a convex hull from concentrations that are resolved by
        sublattice.

        Parameters
        ----------
        concentrations
            One entry per structure, in the form used throughout icet, namely
            ``{'A': {'Ag': 0.3, 'Pd': 0.7}, 'B': {'H': 0.2, 'X': 0.8}}``, where
            the keys of the outer dictionary are the symbols of the sublattices
            of a :class:`ClusterSpace <icet.ClusterSpace>` and the
            concentrations sum to one on each sublattice. If there is only one
            sublattice the outer dictionary can be omitted, as in ``{'Ag': 0.3,
            'Pd': 0.7}``. Such concentrations are conveniently obtained with
            :func:`get_sublattice_concentrations`.
        energies
            Energy (or energy of mixing) for each structure.
        site_fractions
            Fraction of the sites of the lattice that each sublattice occupies,
            as in ``{'A': 0.5, 'B': 0.5}``, conveniently obtained with
            :func:`get_sublattice_site_fractions`. This is needed by
            :func:`get_chemical_potentials` and by
            :func:`get_species_chemical_potentials`, which cannot recover it
            from the concentrations. The geometry of the hull, including
            :func:`get_facet_gradients` and :func:`get_decomposition`, does not
            use it.
        cluster_space
            Cluster space that the structures belong to. When it is given, the
            concentrations are checked against it, so that a sublattice which
            allows more than one species and is left out is reported here
            instead of through a missing chemical potential during a
            simulation.

        Returns
        -------
        A convex hull over the independent concentrations that the supplied
        sublattices define.

        Notes
        -----
        A species whose concentration is the same in every structure carries
        no information and is left out, as is a sublattice all of whose species
        are. Of the species that remain on a sublattice, the alphabetically
        last is dropped, since the others determine it. The concentrations that
        result are ordered by sublattice symbol and then by chemical symbol,
        and :attr:`concentration_labels` records that order.

        A ternary cluster space fed with data along one binary edge therefore
        gives concentrations for two species, not three, and a hull built while
        one sublattice is held fixed gives none for that sublattice.

        All structures must share the same underlying lattice, so that the
        number of sites of each sublattice stands in the same ratio in all of
        them. This holds for structures that belong to one cluster space, and
        it is what makes the concentration of a mixture of phases the average
        of their concentrations on every sublattice at once.

        Every sublattice that allows more than one species has to appear in the
        concentrations, at a fixed composition if it does not vary.
        A sublattice that is left out is neither described by the hull nor
        visible to it, and a simulation that samples it looks up a chemical
        potential that was never formed.
        :func:`get_sublattice_concentrations` covers every sublattice on its
        own, and passing ``cluster_space`` here checks it for concentrations
        that were assembled by hand.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> concentrations = [{'A': {'Ag': 1.0, 'Pd': 0.0}, 'B': {'H': 0.0, 'X': 1.0}},
        ...                   {'A': {'Ag': 0.0, 'Pd': 1.0}, 'B': {'H': 0.0, 'X': 1.0}},
        ...                   {'A': {'Ag': 0.5, 'Pd': 0.5}, 'B': {'H': 0.0, 'X': 1.0}},
        ...                   {'A': {'Ag': 0.5, 'Pd': 0.5}, 'B': {'H': 1.0, 'X': 0.0}}]
        >>> hull = ConvexHull.from_sublattice_concentrations(
        ...     concentrations, [0.0, 0.0, -0.1, 0.3])
        >>> hull.concentration_labels
        [('A', 'Ag'), ('B', 'H')]
        """
        array, labels, dependent, allowed = _sublattice_concentrations_to_array(concentrations)
        if cluster_space is not None:
            _check_every_active_sublattice_is_present(allowed, cluster_space)
        hull = cls(array, energies)
        hull._concentration_labels = labels
        hull._dependent_species = dependent
        if site_fractions is None:
            # Without them the chemical potentials cannot be formed, which
            # `get_chemical_potentials` reports when it is called.
            hull._site_fractions = None
        else:
            missing = {sublattice for sublattice, _ in labels} - set(site_fractions)
            if missing:
                raise ValueError(f'site_fractions is missing the sublattice(s) '
                                 f'{sorted(missing)}')
            hull._site_fractions = np.array([site_fractions[sublattice]
                                             for sublattice, _ in labels], dtype=float)
            if not ((hull._site_fractions > 0) & (hull._site_fractions <= 1)).all():
                raise ValueError('The site fractions must lie between zero and one')
            # A sum below one is ordinary, since a sublattice that carries no
            # concentration need not appear. A sum above one describes no
            # lattice and would rescale the chemical potentials silently.
            total = sum(site_fractions.values())
            if total > 1 + 1e-9:
                raise ValueError(
                    f'The site fractions sum to {total}, which is more than the sites of the '
                    'lattice. They give the fraction of all the sites that each sublattice '
                    'occupies, so they cannot sum to more than one.')
        return hull

    def _triangulate_domain(self) -> np.ndarray:
        """Returns a triangulation of the region of concentration space spanned
        by the input, as indices into the input.

        This is used when the points lie on a single hyperplane, in which case
        the hull has no facets of its own and the coexistence regions are
        instead set by the shape of the concentration domain.
        """
        concentrations = self._input_concentrations
        if self.dimensions == 1:
            vertices = np.array([int(np.argmin(concentrations[:, 0])),
                                 int(np.argmax(concentrations[:, 0]))])
            return vertices.reshape(1, 2)
        vertices = np.unique(ConvexHullSciPy(concentrations).vertices)
        return vertices[Delaunay(concentrations[vertices]).simplices]

    def _fit_plane(self) -> np.ndarray:
        """Returns the equation of the hyperplane that the points lie on, in
        the same convention as :func:`_compute_lower_hull_equations` but
        without a normalized normal.

        The energies are an affine function of the concentrations here, so a
        least squares fit reproduces them exactly.
        """
        design = np.column_stack((self._input_concentrations,
                                  np.ones(len(self._input_concentrations))))
        coefficients = np.linalg.lstsq(design, self._scaled_energies, rcond=None)[0]
        # E = w . c + b  is  w . c - E + b = 0, and the vertical component -1
        # is negative, which marks it as part of the lower hull.
        return np.append(np.append(coefficients[:-1], -1.0), coefficients[-1])

    def _compute_lower_hull(self, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Returns the simplices and the hyperplane equations of the facets
        that make up the lower convex hull.

        Each equation is ``[a_1, ..., a_d, b, offset]`` and describes the plane
        ``a . c + b * E + offset = 0`` with an outward pointing unit normal, so
        that ``b < 0`` identifies a facet of the lower hull. The energies enter
        in scaled form, see :func:`_evaluate_equations`.
        """
        try:
            hull = ConvexHullSciPy(points)
        except QhullError as error:
            raise ValueError(
                'Failed to construct the convex hull of the provided concentrations and '
                'energies. This usually means that the points are degenerate, for example '
                'because several of them coincide. The underlying error was:\n'
                f'{error}') from error

        lower = hull.equations[:, -2] < -_VERTICAL_FACET_TOLERANCE
        if not lower.any():
            raise ValueError('The convex hull has no lower facets, which means that the '
                             'provided points are degenerate.')
        return hull.simplices[lower], hull.equations[lower]

    def _collect_hull_structures(self) -> np.ndarray:
        """Returns the indices of the input structures that lie on the lower
        convex hull, in ascending order."""
        return np.unique(self._simplices)

    def __str__(self) -> str:
        width = 40
        s = []
        s += ['{s:=^{n}}'.format(s=' Convex Hull ', n=width)]
        s += [' {:24} : {}'.format('dimensions', self.dimensions)]
        s += [' {:24} : {}'.format('number of points', len(self.concentrations))]
        s += [' {:24} : {}'.format('smallest concentration', np.min(self.concentrations))]
        s += [' {:24} : {}'.format('largest concentration', np.max(self.concentrations))]
        s += [''.center(width, '=')]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        """ HTML representation. Used, e.g., in jupyter notebooks. """
        s = ['<h4>Convex Hull</h4>']
        s += ['<table border="1" class="dataframe">']
        s += ['<tbody>']
        s += [f'<tr><td style="text-align: left;">Dimensions</td><td>{self.dimensions}</td></tr>']
        s += ['<tr><td style="text-align: left;">Number of points</td>'
              f'<td>{len(self.concentrations)}</td></tr>']
        s += ['<tr><td style="text-align: left;">Smallest concentration</td>'
              f'<td>{np.min(self.concentrations)}</td></tr>']
        s += ['<tr><td style="text-align: left;">Largest concentration</td>'
              f'<td>{np.max(self.concentrations)}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)

    def _prepare_targets(self,
                         target_concentrations: list[float] | list[list[float]],
                         ) -> np.ndarray:
        """Returns the target concentrations as an array of shape
        ``(n_targets, dimensions)``."""
        if len(target_concentrations) == 0:
            return np.empty((0, self.dimensions))
        if self.dimensions > 1 and isinstance(target_concentrations[0], Sized):
            if len(target_concentrations[0]) != self.dimensions:
                raise ValueError(
                    f'Expected {self.dimensions} independent concentrations per point but '
                    f'got {len(target_concentrations[0])}')
        targets = _as_concentration_array(target_concentrations)
        if targets.shape[1] != self.dimensions:
            raise ValueError(
                f'Expected {self.dimensions} independent concentrations per point but '
                f'got {targets.shape[1]}')
        return targets

    def _evaluate_equations(self, targets: np.ndarray) -> np.ndarray:
        """Returns the energy of every face of the lower hull, extended to a
        full hyperplane, at every target concentration.

        The result has shape ``(n_targets, n_faces)``. Since the hull is
        convex its value at a point is the largest value taken by any of these
        planes.
        """
        normals = self._face_equations[:, :-2]
        vertical = self._face_equations[:, -2]
        offsets = self._face_equations[:, -1]
        scaled = -(targets @ normals.T + offsets) / vertical
        return scaled * self._energy_scale + self._energy_offset

    def _outside_domain(self, targets: np.ndarray) -> np.ndarray:
        """Returns a boolean mask that is ``True`` for every target
        concentration outside the region spanned by the input
        concentrations.

        A target that is not finite lies nowhere and counts as outside, which
        keeps it out of the search for a simplex that contains it.
        """
        normals = self._domain_equations[:, :-1]
        offsets = self._domain_equations[:, -1]
        with np.errstate(invalid='ignore'):
            outside = ((targets @ normals.T + offsets) > _INSIDE_TOLERANCE).any(axis=1)
        return outside | ~np.isfinite(targets).all(axis=1)

    def get_energy_at_convex_hull(self,
                                  target_concentrations: list[float] | list[list[float]],
                                  ) -> np.ndarray:
        """Returns the energy of the convex hull at specified concentrations.
        If any concentration is outside the allowed range, NaN is
        returned.

        Parameters
        ----------
        target_concentrations
            Concentrations at target points.

            If there is one independent concentration, a list of
            floats is sufficient. Otherwise, the concentrations ought
            to be provided as a list of lists, such as ``[[0.1, 0.2],
            [0.3, 0.1], ...]``.

        Returns
        -------
        The energy of the convex hull at each target concentration, and NaN
        where the concentration lies outside the sampled range.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.get_energy_at_convex_hull([0.25, 0.75])
        array([-0.5, -0.5])
        """
        return self._energy_at(self._prepare_targets(target_concentrations))

    def _energy_at(self, targets: np.ndarray) -> np.ndarray:
        """Returns the energy of the convex hull at prepared target
        concentrations, with NaN outside the sampled range."""
        energies = self._evaluate_equations(targets).max(axis=1)
        energies[self._outside_domain(targets)] = np.nan
        return energies

    def get_energy_above_convex_hull(self,
                                     concentrations: list[float] | list[list[float]],
                                     energies: list[float]) -> np.ndarray:
        """Returns the energy of each structure relative to the convex hull,
        commonly referred to as the energy above the hull. The value is zero
        for structures on the hull and positive otherwise. If a concentration
        lies outside the allowed range, NaN is returned.

        Parameters
        ----------
        concentrations
            Concentrations of the structures.

            If there is one independent concentration, a list of
            floats is sufficient. Otherwise, the concentrations must
            be provided as a list of lists, such as ``[[0.1, 0.2],
            [0.3, 0.1], ...]``.
        energies
            Energies of the structures.

        Returns
        -------
        The energy of each structure relative to the convex hull, and NaN
        where the concentration lies outside the sampled range.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.get_energy_above_convex_hull([0.25, 0.5], [0.0, -1.0])
        array([0.5, 0. ])
        """
        energies = np.asarray(energies, dtype=float)
        targets = self._prepare_targets(concentrations)
        if len(targets) != len(energies):
            raise ValueError('concentrations and energies must have the same length')
        return energies - self._energy_at(targets)

    def is_on_convex_hull(self,
                          concentrations: list[float] | list[list[float]],
                          energies: list[float],
                          energy_tolerance: float = 1e-6) -> np.ndarray:
        """Returns a boolean array that is ``True`` for every structure that
        lies on the convex hull, which is convenient for filtering a table of
        results.

        A structure whose energy lies below the hull is not on it, and the
        result is ``False``. That situation means that the hull was constructed
        without that structure and no longer describes the system. Use
        :func:`extract_low_energy_structures` to collect the structures that
        are at or below the hull, which is what a search for new ground states
        needs.

        Parameters
        ----------
        concentrations
            Concentrations of the structures.

            If there is one independent concentration, a list of
            floats is sufficient. Otherwise, the concentrations must
            be provided as a list of lists, such as ``[[0.1, 0.2],
            [0.3, 0.1], ...]``.
        energies
            Energies of the structures.
        energy_tolerance
            Consider a structure to be on the hull if its energy is at most
            this far above it.

        Returns
        -------
        A boolean for each structure that is ``True`` where it lies on the
        convex hull.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.is_on_convex_hull([0.25, 0.5], [0.0, -1.0])
        array([False,  True])
        """
        above = self.get_energy_above_convex_hull(concentrations, energies)
        with np.errstate(invalid='ignore'):
            return np.abs(above) <= energy_tolerance

    def get_decomposition(self,
                          target_concentrations: list[float] | list[list[float]],
                          ) -> list[dict]:
        """Returns the decomposition of each target concentration into the
        structures on the convex hull.

        At every concentration the hull is spanned by one of its facets. The
        structures that define this facet are the phases that a sample of the
        given overall concentration separates into, and the barycentric
        coordinates of the concentration within the facet are the fractions in
        which they occur.

        Parameters
        ----------
        target_concentrations
            Concentrations at target points.

            If there is one independent concentration, a list of
            floats is sufficient. Otherwise, the concentrations ought
            to be provided as a list of lists, such as ``[[0.1, 0.2],
            [0.3, 0.1], ...]``.

        Returns
        -------
        One dictionary per target concentration with the keys ``structures``,
        holding the indices of the structures the concentration decomposes
        into, ``fractions``, holding the fraction of each of them, and
        ``energy``, holding the resulting energy. For a concentration outside
        the allowed range, and for one that is not a number, the lists are
        empty and the energy is NaN.

        The fractions reproduce the target concentration. Right at the rim of
        the sampled range a target can be accepted as lying inside while
        falling outside every simplex by a small amount, in which case the
        fractions describe the closest concentration that is inside.

        A structure can carry a fraction of zero, which happens for a target on
        the boundary between two simplices of one face. The structures reported
        are therefore those of a simplex that contains the target, and which
        simplex that is depends on the order of the input.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> decomposition = hull.get_decomposition([0.25])
        >>> decomposition[0]['structures']
        [0, 1]
        >>> [round(f, 6) for f in decomposition[0]['fractions']]
        [0.5, 0.5]
        >>> round(decomposition[0]['energy'], 6)
        -0.5
        """
        targets = self._prepare_targets(target_concentrations)
        plane_energies = self._evaluate_equations(targets)
        hull_energies = plane_energies.max(axis=1)
        outside = self._outside_domain(targets)

        decompositions = []
        for target, planes, energy, is_outside in zip(targets, plane_energies,
                                                      hull_energies, outside):
            if is_outside:
                decompositions.append({'structures': [], 'fractions': [], 'energy': np.nan})
                continue
            structures, fractions = self._decompose_at(planes, energy, target)
            decompositions.append({'structures': [int(s) for s in structures],
                                   'fractions': [float(f) for f in fractions],
                                   'energy': float(energy)})
        return decompositions

    def _decompose_at(self,
                      planes: np.ndarray,
                      energy: float,
                      target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Returns the structures and fractions that a target concentration
        decomposes into.

        The hull is supported at the target by the face whose plane takes the
        largest value. That face is spanned by one or more simplices and the
        target lies in one of them, which is the one to report, since the
        barycentric coordinates with respect to any other simplex of the same
        face reproduce a different concentration.

        Every face whose plane comes within a tolerance of the largest value is
        searched rather than only the face that attains it. Faces that support
        the hull at the same point hold the same plane and are one face, so
        this costs nothing in the ordinary case, and it keeps the result
        correct even where two faces meet.
        """
        candidates = np.flatnonzero(planes >= energy - _PLANE_TIE_TOLERANCE * self._energy_scale)
        best_structures = best_fractions = None
        smallest_violation = np.inf
        for face in candidates:
            for simplex in self._face_simplices[face]:
                structures = np.sort(simplex)
                vertices = self._input_concentrations[structures]
                fractions = _barycentric_coordinates(vertices, target)
                # A simplex of a face can be degenerate in concentration space
                # even though its vertices are vertices of the face, and the
                # coordinates of a point then solve no system at all. They can
                # still come out positive, so whether they reproduce the point
                # is what decides here.
                if not np.allclose(fractions @ vertices, target, atol=_REPRODUCTION_TOLERANCE):
                    continue
                violation = -min(fractions.min(), 0.0)
                if violation <= _BARYCENTRIC_TOLERANCE:
                    return structures, _normalized(fractions)
                if violation < smallest_violation:
                    smallest_violation = violation
                    best_structures, best_fractions = structures, fractions
        if best_structures is None:
            # No simplex both reproduces the target and holds it, which a
            # target on the rim of the hull can reach through rounding. The
            # closest one that reproduces the target is then the best there is.
            for face in candidates:
                for simplex in self._face_simplices[face]:
                    structures = np.sort(simplex)
                    vertices = self._input_concentrations[structures]
                    fractions = _barycentric_coordinates(vertices, target)
                    deviation = float(np.abs(fractions @ vertices - target).max())
                    if deviation < smallest_violation:
                        smallest_violation = deviation
                        best_structures, best_fractions = structures, fractions
        return best_structures, _normalized(best_fractions)

    def get_facets(self) -> list[list[int]]:
        """Returns the faces of the lower convex hull, each as the list of
        indices of the structures that span it.

        In a binary these are the tie lines, in a ternary the three-phase
        triangles, and so on. Together they enumerate the coexistence regions
        of the system.

        A face can have more vertices than ``dimensions + 1``, in which case
        the structures on it are degenerate in energy over the whole face.
        :func:`get_decomposition` still reports ``dimensions + 1`` of them,
        since a given concentration separates into that many phases.

        Returns
        -------
        The indices of the structures that span each face of the lower convex
        hull, one list per face.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.get_facets()
        [[0, 1], [1, 2]]
        """
        return [[int(vertex) for vertex in vertices] for vertices in self._face_vertices]

    def get_facet_gradients(self) -> np.ndarray:
        """Returns the gradient of the energy along each face of the lower
        convex hull as an array of shape ``(n_faces, dimensions)``.

        Entry :math:`i` of a row is :math:`\\partial e/\\partial c_i`, the
        derivative of the energy with respect to the :math:`i`-th independent
        concentration along that face. The rows are ordered as the faces
        returned by :func:`get_facets`.

        This is a property of the geometry of the hull alone. See
        :func:`get_chemical_potentials` for the related quantity that a
        semi-grand canonical simulation takes, which differs by the fraction of
        the sites that the concentration refers to.

        Returns
        -------
        The gradient of the energy along each face, of shape
        ``(n_faces, dimensions)``.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.get_facet_gradients()
        array([[-2.],
               [ 2.]])
        """
        return (-self._face_equations[:, :-2] / self._face_equations[:, -2, None]
                * self._energy_scale)

    def get_chemical_potentials(self) -> np.ndarray:
        """Returns the chemical potentials at which the structures on each face
        of the lower convex hull coexist, as an array of shape ``(n_faces,
        dimensions)``.

        Entry :math:`i` of a row is the difference between the chemical
        potential of the species that the :math:`i`-th concentration counts and
        that of the species of the same sublattice whose concentration is fixed
        by the others. The rows are ordered as the faces returned by
        :func:`get_facets`.

        These differences are resolved by sublattice. A simulation in the
        semi-grand canonical ensemble takes one chemical potential per species
        instead, which :func:`get_species_chemical_potentials` assembles from
        them. The two carry the same information only when no species occurs on
        more than one sublattice.

        A concentration counts the species of one sublattice relative to the
        sites of that sublattice, while the energy of a cluster expansion is
        given per site of the whole lattice. Changing the occupation of a
        single site therefore changes the concentration by :math:`1/N_s` rather
        than by :math:`1/N`, and the chemical potential is the gradient of
        :func:`get_facet_gradients` divided by the fraction of the sites that
        the sublattice occupies.

        For a hull that was built from an array of concentrations that fraction
        is taken to be one, i.e., the concentrations are assumed to refer to
        all sites. For a hull built with
        :func:`from_sublattice_concentrations` the fractions have to be
        supplied there, since they cannot be recovered from the concentrations.

        Returns
        -------
        The chemical potential differences of each face, of shape
        ``(n_faces, dimensions)``.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> hull = ConvexHull([0.0, 0.5, 1.0], [0.0, -1.0, 0.0])
        >>> hull.get_chemical_potentials()
        array([[-2.],
               [ 2.]])
        """
        if self._site_fractions is None:
            raise ValueError(
                'The chemical potentials require the fraction of the sites that each '
                'sublattice occupies, which cannot be recovered from the concentrations. '
                'Pass site_fractions to from_sublattice_concentrations, using '
                'get_sublattice_site_fractions to obtain them, or use get_facet_gradients '
                'for the gradient of the energy along each face.')
        return self.get_facet_gradients() / self._site_fractions

    def get_species_chemical_potentials(self, strict: bool = True) -> list[dict[str, float] | None]:
        """Returns the chemical potential of each species at which the
        structures on each face of the lower convex hull coexist, as one
        dictionary per face in the order of :func:`get_facets`.

        This is the ``chemical_potentials`` argument of
        :class:`SemiGrandCanonicalEnsemble
        <mchammer.ensembles.SemiGrandCanonicalEnsemble>`. Setting it to the
        values of a face makes the structures on that face degenerate, so that
        the simulation sits at the corresponding phase boundary. Only
        differences between species that share a sublattice matter, since those
        are the exchanges a simulation makes, and the species that comes first
        alphabetically is given a value of zero. A difference between species of
        different sublattices is whatever the solution happened to give and
        carries no meaning.

        A chemical potential belongs to a species and not to a sublattice,
        while :func:`get_chemical_potentials` gives one difference per
        concentration and therefore per sublattice. When a species occurs on
        more than one sublattice those differences can constrain the same pair
        of species twice, and there is then no set of chemical potentials that
        satisfies all of them at once. Such a face is not a state that a
        semi-grand canonical simulation can reach, whatever chemical potentials
        are chosen, and this method raises rather than return values that do
        not describe it.

        The result covers the species whose concentration varies across the
        structures the hull was built from, and only those. A species held at
        one composition throughout, and every species of a sublattice held that
        way, carry no information for the hull to report and are absent from
        the dictionary.

        A simulation therefore has to leave them where the hull assumed them.
        :class:`SemiGrandCanonicalEnsemble
        <mchammer.ensembles.SemiGrandCanonicalEnsemble>` holds a whole
        sublattice fixed through its ``sublattice_probabilities`` argument, and
        :class:`HybridEnsemble <mchammer.ensembles.HybridEnsemble>` holds
        individual species fixed through the ``allowed_symbols`` of a
        semi-grand canonical step. A simulation that samples a species the
        dictionary does not name changes a composition the hull took as given,
        and no longer sits at the phase boundary it reports.

        Parameters
        ----------
        strict
            Raise for a face that no set of chemical potentials describes. When
            it is ``False`` such a face yields ``None`` in its place and the
            remaining faces are returned as usual.

        Returns
        -------
        The chemical potential of each species at which the structures on each
        face coexist, as one dictionary per face in the order of
        :func:`get_facets`, with ``None`` for a face that no set of chemical
        potentials describes when ``strict`` is ``False``.

        Raises
        ------
        ValueError
            If the hull was not built from concentrations that are resolved by
            sublattice, if the site fractions were not supplied, or if a face
            cannot be described by one chemical potential per species while
            ``strict`` is ``True``.

        Examples
        --------
        >>> from icet.tools import ConvexHull
        >>> concentrations = [{'A': {'Ag': 1.0, 'Pd': 0.0}},
        ...                   {'A': {'Ag': 0.0, 'Pd': 1.0}},
        ...                   {'A': {'Ag': 0.5, 'Pd': 0.5}}]
        >>> hull = ConvexHull.from_sublattice_concentrations(
        ...     concentrations, [0.0, 0.0, -1.0], site_fractions={'A': 1.0})
        >>> [{k: round(v, 6) for k, v in mu.items()}
        ...  for mu in hull.get_species_chemical_potentials()]
        [{'Ag': 0.0, 'Pd': -2.0}, {'Ag': 0.0, 'Pd': 2.0}]
        """
        if self._concentration_labels is None:
            raise ValueError(
                'The chemical potential of a species requires the species to be known, which '
                'is the case only for a hull built with from_sublattice_concentrations. Use '
                'get_chemical_potentials for a hull built from an array of concentrations.')

        species = sorted({symbol for _, symbol in self._concentration_labels}
                         | set(self._dependent_species.values()))
        position = {symbol: index for index, symbol in enumerate(species)}
        matrix = np.zeros((len(self._concentration_labels), len(species)))
        for row, (sublattice, symbol) in enumerate(self._concentration_labels):
            matrix[row, position[symbol]] += 1.0
            matrix[row, position[self._dependent_species[sublattice]]] -= 1.0

        potentials = []
        for face, differences in zip(self.get_facets(), self.get_chemical_potentials()):
            solution = np.linalg.lstsq(matrix, differences, rcond=None)[0]
            residual = float(np.abs(matrix @ solution - differences).max())
            # The tolerance follows the size of the differences themselves, so
            # that it neither accepts an inconsistency that is large compared
            # with them nor refuses a face whose differences are small.
            if residual > _POTENTIAL_RESIDUAL_TOLERANCE * float(np.abs(differences).max()):
                if not strict:
                    potentials.append(None)
                    continue
                raise ValueError(
                    f'The face spanned by the structures {face} cannot be described by one '
                    'chemical potential per species. Its differences '
                    f'{ {f"{s}-{self._dependent_species[sl]}": round(float(d), 6) for (sl, s), d in zip(self._concentration_labels, differences)} } '  # noqa
                    'constrain the same species through more than one sublattice and do not '
                    'agree. No semi-grand canonical simulation reaches this face, whatever '
                    'chemical potentials are chosen. Use get_chemical_potentials for the '
                    'differences that are resolved by sublattice.')
            solution = solution - solution[0]
            potentials.append({symbol: float(value) for symbol, value in zip(species, solution)})
        return potentials

    def extract_low_energy_structures(self,
                                      concentrations: list[float] | list[list[float]],
                                      energies: list[float],
                                      energy_tolerance: float) -> list[int]:
        """Returns the indices of energies that lie within a certain
        tolerance of the convex hull.

        Parameters
        ----------
        concentrations
            Concentrations of candidate structures.

            If there is one independent concentration, a list of
            floats is sufficient. Otherwise, the concentrations must
            be provided as a list of lists, such as ``[[0.1, 0.2],
            [0.3, 0.1], ...]``.
        energies
            Energies of candidate structures.
        energy_tolerance
            Include structures with an energy that is at most this far
            from the convex hull.

        Returns
        -------
        The indices of the structures that lie within the tolerance of the
        convex hull.
        """
        # Convert to numpy arrays, can be necessary if, for example,
        # they are Pandas Series with "gaps"
        concentrations = np.array(concentrations)
        energies = np.array(energies)

        n_points = len(concentrations)
        if len(energies) != n_points:
            raise ValueError('concentrations and energies must have '
                             'the same length')

        # Calculate energy at convex hull for specified concentrations
        hull_energies = self.get_energy_at_convex_hull(concentrations)

        # Extract those that are close enough
        close_to_hull = [i for i in range(n_points)
                         if energies[i] <= hull_energies[i] + energy_tolerance]

        return close_to_hull


def get_sublattice_concentrations(structures: list['Atoms'],
                                  cluster_space: 'ClusterSpace') -> list[dict]:
    """Returns the concentrations of each structure resolved by sublattice, in
    the form expected by
    :func:`ConvexHull.from_sublattice_concentrations
    <icet.tools.convex_hull.ConvexHull.from_sublattice_concentrations>`.

    Parameters
    ----------
    structures
        Atomic configurations, each of which must be a supercell of the
        primitive structure of the cluster space.
    cluster_space
        Cluster space that defines the sublattices and the species allowed on
        them.

    Returns
    -------
    One dictionary per structure of the form ``{'A': {'Ag': 0.3, 'Pd': 0.7},
    'B': {'H': 0.2, 'X': 0.8}}``. Every species that the cluster space allows
    on a sublattice appears, including those that the structure does not
    contain.

    Examples
    --------
    >>> from ase.build import bulk
    >>> from icet import ClusterSpace
    >>> from icet.tools import get_sublattice_concentrations
    >>> primitive_structure = bulk('Ag', 'fcc', a=4.0)
    >>> cluster_space = ClusterSpace(primitive_structure, [4.0], ['Ag', 'Pd'])
    >>> structure = primitive_structure.repeat(2)
    >>> structure.symbols[:4] = 'Pd'
    >>> get_sublattice_concentrations([structure], cluster_space)
    [{'A': {'Ag': 0.5, 'Pd': 0.5}}]
    """
    concentrations = []
    for structure in structures:
        symbols = structure.get_chemical_symbols()
        entry = {}
        for sublattice in cluster_space.get_sublattices(structure):
            indices = sublattice.indices
            if len(indices) == 0:
                raise ValueError(
                    f'Sublattice {sublattice.symbol} has no sites in one of the structures, '
                    'so its concentration is undefined')
            occupation = [symbols[index] for index in indices]
            entry[sublattice.symbol] = {species: occupation.count(species) / len(indices)
                                        for species in sublattice.chemical_symbols}
        concentrations.append(entry)
    return concentrations


def get_sublattice_site_fractions(structure: 'Atoms',
                                  cluster_space: 'ClusterSpace') -> dict[str, float]:
    """Returns the fraction of the sites of the lattice that each sublattice
    occupies, in the form expected by
    :func:`ConvexHull.from_sublattice_concentrations
    <icet.tools.convex_hull.ConvexHull.from_sublattice_concentrations>`.

    A concentration counts the species of one sublattice relative to the sites
    of that sublattice, while the energy of a cluster expansion is given per
    site of the whole lattice. These fractions relate the two and are what
    turns the gradient of the energy along a face of the hull into a chemical
    potential.

    Parameters
    ----------
    structure
        Atomic configuration, which must be a supercell of the primitive
        structure of the cluster space. The fractions are a property of the
        lattice rather than of the occupation, so any such supercell will do.
    cluster_space
        Cluster space that defines the sublattices.

    Returns
    -------
    The fraction of the sites that each sublattice occupies, keyed by the
    symbol of the sublattice.

    Examples
    --------
    >>> from ase.build import bulk
    >>> from icet import ClusterSpace
    >>> from icet.tools import get_sublattice_site_fractions
    >>> primitive_structure = bulk('NaCl', 'rocksalt', a=5.6)
    >>> cluster_space = ClusterSpace(primitive_structure, [6.0],
    ...                              [['Na', 'K'], ['Cl', 'X']])
    >>> get_sublattice_site_fractions(primitive_structure, cluster_space)
    {'A': 0.5, 'B': 0.5}
    """
    n_sites = len(structure)
    return {sublattice.symbol: len(sublattice.indices) / n_sites
            for sublattice in cluster_space.get_sublattices(structure)}


def _check_every_active_sublattice_is_present(allowed: dict[str, tuple[str, ...]],
                                              cluster_space: 'ClusterSpace') -> None:
    """Checks that the supplied concentrations cover every sublattice of the
    cluster space that allows more than one species.

    A sublattice that is left out is neither constrained by the hull nor
    visible to it, so a simulation that samples it looks up a chemical
    potential that was never formed.
    """
    primitive_structure = cluster_space.primitive_structure
    missing = {}
    for sublattice in cluster_space.get_sublattices(primitive_structure):
        if len(sublattice.chemical_symbols) < 2:
            continue
        if sublattice.symbol not in allowed:
            missing[sublattice.symbol] = list(sublattice.chemical_symbols)
            continue
        supplied = set(allowed[sublattice.symbol])
        expected = set(sublattice.chemical_symbols)
        if supplied != expected:
            raise ValueError(
                f'The concentrations give the species {sorted(supplied)} on sublattice '
                f'{sublattice.symbol}, while the cluster space allows {sorted(expected)} '
                'there. Every species of the sublattice has to appear, and no other.')
    if missing:
        raise ValueError(
            f'The concentrations leave out the sublattice(s) {missing}, which the cluster '
            'space allows more than one species on. A sublattice that is left out is neither '
            'described by the hull nor visible to it, and a simulation that samples it looks '
            'up a chemical potential that was never formed. Give every such sublattice a '
            'concentration, at a fixed composition if it does not vary, which '
            'get_sublattice_concentrations does on its own.')


def _sublattice_concentrations_to_array(
        concentrations: list[dict],
        ) -> tuple[np.ndarray, list[tuple[str, str]], dict[str, str], dict[str, tuple[str, ...]]]:
    """Returns the independent concentrations of a set of sublattice resolved
    concentrations as an array, together with the species that the columns
    refer to, the species of each sublattice whose concentration is fixed by
    the others, and the species that every supplied sublattice allows."""
    if len(concentrations) == 0:
        raise ValueError('concentrations must not be empty')

    entries = [_as_sublattice_dictionary(entry, index)
               for index, entry in enumerate(concentrations)]

    reference = {sublattice: tuple(sorted(species))
                 for sublattice, species in entries[0].items()}
    for index, entry in enumerate(entries):
        found = {sublattice: tuple(sorted(species)) for sublattice, species in entry.items()}
        if found != reference:
            raise ValueError(
                'All structures must have the same sublattices and the same species on them, '
                f'but structure {index} has {found} while structure 0 has {reference}')

    if all(len(species) < 2 for species in reference.values()):
        raise ValueError('At least one sublattice must allow more than one species, '
                         'otherwise there is no concentration to construct a hull over')

    # Check every value that was supplied, including the ones that are dropped
    # below.  A value that is not a number would otherwise make the sum over a
    # sublattice NaN, which compares false against the tolerance and would let
    # it pass unnoticed.
    for index, entry in enumerate(entries):
        for sublattice, species in entry.items():
            for symbol, value in species.items():
                # A value that is not a number at all reaches `isfinite` as an
                # object it cannot handle, so its type is settled first.
                if not isinstance(value, (int, float, np.integer, np.floating)) \
                        or isinstance(value, bool):
                    raise ValueError(
                        f'The concentration of {symbol} on sublattice {sublattice} of '
                        f'structure {index} is {value!r}, but concentrations must be numbers')
                if not np.isfinite(value):
                    raise ValueError(
                        f'The concentration of {symbol} on sublattice {sublattice} of '
                        f'structure {index} is {value}, but concentrations must be finite')
                if not -1e-9 <= value <= 1 + 1e-9:
                    raise ValueError(
                        f'The concentration of {symbol} on sublattice {sublattice} of '
                        f'structure {index} is {value}, but concentrations must lie between '
                        'zero and one')
            total = sum(species.values())
            if abs(total - 1.0) > 1e-5:
                raise ValueError(
                    f'Concentrations must sum to one on each sublattice, but they sum to '
                    f'{total} on sublattice {sublattice} of structure {index}')

    # A species whose concentration is the same in every structure adds no
    # dimension to the hull.  This is the normal situation when one sublattice
    # is held fixed while another is varied, so such species are dropped rather
    # than rejected.  The result is visible in the labels that are returned.
    #
    # Which species varies has to be settled before the dependent species is
    # chosen, because the concentrations of the varying species of a sublattice
    # sum to a constant of their own.  Choosing the dependent species first
    # would leave a set that is linearly dependent whenever the fixed species
    # happens to be the one that sorts last.
    labels = []
    dependent = {}
    for sublattice in sorted(reference):
        varying = [symbol for symbol in reference[sublattice]
                   if np.ptp([entry[sublattice][symbol] for entry in entries])
                   > _CONSTANT_CONCENTRATION_TOLERANCE]
        # The concentrations of a sublattice sum to one, so either none of its
        # species varies or at least two of them do, and dropping the last of
        # the varying ones always leaves at least one.
        if varying:
            dependent[sublattice] = varying[-1]
        labels.extend((sublattice, symbol) for symbol in varying[:-1])
    if len(labels) == 0:
        raise ValueError('The concentrations are the same in every structure, so they do not '
                         'span a hull')

    array = np.array([[entry[sublattice][symbol] for sublattice, symbol in labels]
                      for entry in entries], dtype=float)

    if _affine_rank(array) < array.shape[1]:
        raise ValueError(
            f'The concentrations of {labels} are not independent of one another, so they do '
            'not span a hull of that many dimensions. This happens when the composition of '
            'one sublattice is determined by that of another, in which case only one of them '
            'should be provided.')

    return array, labels, dependent, dict(reference)


def _as_sublattice_dictionary(entry: dict, index: int) -> dict:
    """Returns one set of concentrations as a dictionary of sublattices,
    accepting the shorthand that omits the sublattice when there is only
    one."""
    if not isinstance(entry, dict) or len(entry) == 0:
        raise ValueError(f'Concentrations of structure {index} must be a non-empty dictionary '
                         f'but are {entry!r}')
    if all(isinstance(value, dict) for value in entry.values()):
        return entry
    if any(isinstance(value, dict) for value in entry.values()):
        raise ValueError(
            f'Concentrations of structure {index} mix the form that specifies a sublattice '
            'with the form that does not')
    return {'A': entry}


def _group_coplanar_simplices(simplices: np.ndarray,
                              equations: np.ndarray,
                              ) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
    """Groups the simplices of the lower hull by the plane that supports them
    and returns, for each face, its equation, its simplices, and the indices of
    the structures that span it.

    Qhull triangulates a facet with more than ``dimensions + 1`` vertices, so
    one face arrives as several simplices with the same equation. Such a face
    is one region of coexistence, and reporting the triangulation instead would
    invent boundaries that carry no physical meaning.

    The simplices that Qhull splits one facet into carry the equation of that
    facet unchanged, so the grouping compares the equations exactly. Comparing
    them within a tolerance would group facets that are merely close, which
    are distinct faces of the hull. Rounding to a fixed number of decimals
    would do the same, and would decide the question by where the values fall
    relative to the rounding grid.
    """
    # Adding zero turns a negative zero into a zero, which compares equal but
    # does not sort together.
    keys = equations + 0.0
    _, inverse = np.unique(keys, axis=0, return_inverse=True)
    inverse = np.asarray(inverse).ravel()

    # Collect the members of each group in one pass over the sorted labels,
    # rather than scanning all simplices once per group.
    order = np.argsort(inverse, kind='stable')
    boundaries = np.flatnonzero(np.diff(inverse[order])) + 1

    faces = []
    for members in np.split(order, boundaries):
        vertices = np.unique(simplices[members])
        faces.append((tuple(int(v) for v in vertices), equations[members[0]], simplices[members],
                      vertices))
    # Order the faces by the structures that span them, so that the faces and
    # the quantities derived from them have a reproducible order.
    faces.sort(key=lambda face: face[0])

    face_equations = np.array([face[1] for face in faces])
    face_simplices = [face[2] for face in faces]
    face_vertices = [face[3] for face in faces]
    return face_equations, face_simplices, face_vertices


def _as_concentration_array(concentrations) -> np.ndarray:
    """Returns the concentrations as an array of shape ``(n_points,
    n_independent_concentrations)``, accepting the flat format that is
    convenient for binaries."""
    array = np.asarray(concentrations, dtype=float)
    if array.ndim == 1:
        return array.reshape(-1, 1)
    if array.ndim == 2:
        return array
    raise ValueError('concentrations must be one- or two-dimensional but have '
                     f'{array.ndim} dimensions')


def _validate_input(concentrations: np.ndarray,
                    energies: np.ndarray,
                    dimensions: int) -> None:
    """Checks that the input can support a convex hull of the expected
    dimensionality and raises an informative error otherwise."""
    if not np.isfinite(concentrations).all():
        raise ValueError('concentrations must all be finite')
    if not np.isfinite(energies).all():
        raise ValueError('energies must all be finite')

    if len(concentrations) < dimensions + 1:
        raise ValueError(
            f'At least {dimensions + 1} structures are needed to construct a convex hull '
            f'with {dimensions} independent concentrations but only {len(concentrations)} '
            'were provided')

    rank = _affine_rank(concentrations)
    if rank < dimensions:
        raise ValueError(
            f'The concentrations span {rank} dimension(s) but {dimensions} independent '
            f'concentrations were provided. Describe the system with {rank} independent '
            'concentration(s) instead, for example by dropping a concentration that is not '
            'varied or by using a coordinate along the section that is sampled.')


def _affine_rank(points: np.ndarray, tolerance: float = 1e-10) -> int:
    """Returns the dimensionality of the affine subspace spanned by the given
    points."""
    if len(points) < 2:
        return 0
    centered = points - points.mean(axis=0)
    scale = np.abs(centered).max()
    if scale == 0.0:
        return 0
    return int(np.linalg.matrix_rank(centered / scale, tol=tolerance))


def _concentration_domain_equations(concentrations: np.ndarray) -> np.ndarray:
    """Returns the inequalities that describe the region of concentration space
    spanned by the given concentrations.

    Each row is ``[a_1, ..., a_d, offset]`` and a point lies inside the region
    if ``a . c + offset <= 0`` for every row.
    """
    if concentrations.shape[1] == 1:
        # Qhull cannot handle one-dimensional input, so the interval is
        # constructed directly.
        lower = concentrations[:, 0].min()
        upper = concentrations[:, 0].max()
        return np.array([[-1.0, lower], [1.0, -upper]])
    return ConvexHullSciPy(concentrations).equations


def _normalized(fractions: np.ndarray) -> np.ndarray:
    """Returns the fractions with the negative ones removed and the rest
    scaled to sum to one.

    A coordinate slightly below zero is a consequence of finite precision and
    carries no physical meaning.
    """
    clipped = np.clip(fractions, 0.0, None)
    return clipped / clipped.sum()


def _barycentric_coordinates(vertices: np.ndarray, point: np.ndarray) -> np.ndarray:
    """Returns the barycentric coordinates of a point with respect to the given
    vertices, i.e., the coefficients that sum to one and reproduce the point as
    a linear combination of the vertices.

    The coordinates are returned as they are. A negative coordinate means that
    the point lies outside the simplex, which the caller uses to find the
    simplex that contains it, so it must not be clipped away here.
    """
    matrix = np.vstack((vertices.T, np.ones(len(vertices))))
    right_hand_side = np.append(point, 1.0)
    if matrix.shape[0] == matrix.shape[1]:
        try:
            coordinates = np.linalg.solve(matrix, right_hand_side)
        except np.linalg.LinAlgError:
            # Qhull can return a simplex whose vertices are degenerate, in
            # which case the coordinates are not unique and any solution that
            # reproduces the point will do.
            coordinates = np.linalg.lstsq(matrix, right_hand_side, rcond=None)[0]
    else:
        coordinates = np.linalg.lstsq(matrix, right_hand_side, rcond=None)[0]
    return coordinates
