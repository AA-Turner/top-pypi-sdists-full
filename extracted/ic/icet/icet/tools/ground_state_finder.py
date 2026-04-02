from math import inf
import numpy as np

from ase import Atoms
from ase.data import chemical_symbols as periodic_table
from .. import ClusterExpansion
from ..core.local_orbit_list_generator import LocalOrbitListGenerator
from ..core.structure import Structure
from .variable_transformation import transform_parameters
from ..input_output.logging_tools import logger

try:
    import highspy
    from highspy.highs import highs_cons
    highspy_loaded = True
except ImportError:
    from types import SimpleNamespace
    from unittest.mock import MagicMock
    # For typing purposes
    highspy = SimpleNamespace(Highs=None, HighsModelStatus=None)
    highs_cons = MagicMock()
    highspy_loaded = False


class GroundStateFinder:
    """
    This class provides functionality for determining the ground states
    using a binary cluster expansion. This is efficiently achieved through the
    use of mixed integer programming (MIP) as developed by Larsen *et al.* in
    `Phys. Rev. Lett. 120, 256101 (2018)
    <https://doi.org/10.1103/PhysRevLett.120.256101>`_.

    This class relies on the `HiGHS package <https://www.highs.dev/>`_.

    Note
    ----
    The current implementation only works for binary systems.


    Parameters
    ----------
    cluster_expansion
        Cluster expansion for which to find ground states.
    structure
        Atomic configuration.

    Example
    -------
    The following snippet illustrates how to determine the ground state for a
    Au-Ag alloy. Here, the parameters of the cluster
    expansion are set to emulate a simple Ising model in order to obtain an
    example that can be run without modification. In practice, one should of
    course use a proper cluster expansion::

        >>> from ase.build import bulk
        >>> from icet import ClusterExpansion, ClusterSpace

        >>> # prepare cluster expansion
        >>> # the setup emulates a second nearest-neighbor (NN) Ising model
        >>> # (zerolet and singlet parameters are zero; only first and second
        >>> # neighbor pairs are included)
        >>> prim = bulk('Au')
        >>> chemical_symbols = ['Ag', 'Au']
        >>> cs = ClusterSpace(prim, cutoffs=[4.3], chemical_symbols=chemical_symbols)
        >>> ce = ClusterExpansion(cs, [0, 0, 0.1, -0.02])

        >>> # prepare initial configuration
        >>> structure = prim.repeat(3)

        >>> # set up the ground state finder and calculate the ground state energy
        >>> gsf = GroundStateFinder(ce, structure)
        >>> ground_state = gsf.get_ground_state({'Ag': 5})
        >>> print('Ground state energy:', ce.predict(ground_state))
    """

    def __init__(self,
                 cluster_expansion: ClusterExpansion,
                 structure: Atoms) -> None:
        if not highspy_loaded:
            raise ImportError('HiGHS (https://www.highs.dev/) is required in order to use the'
                              ' ground state finder.')
        # Check that there is only one active sublattice
        self._cluster_expansion = cluster_expansion
        self._fractional_position_tolerance = cluster_expansion.fractional_position_tolerance
        self.structure = structure
        cluster_space = self._cluster_expansion.get_cluster_space_copy()
        primitive_structure = cluster_space.primitive_structure
        self._active_sublattices = cluster_space.get_sublattices(structure).active_sublattices

        # Check that there are no more than two allowed species
        active_species = [set(subl.chemical_symbols) for subl in self._active_sublattices]
        if any(len(species) > 2 for species in active_species):
            raise NotImplementedError('Currently, systems with more than two allowed species on '
                                      'any sublattice are not supported.')

        # Check that there are no merged orbits
        if any(['merge' in elem for elem in cluster_space._pruning_history]):
            raise NotImplementedError('Currently, systems with merged orbits are not supported.')

        self._active_species = active_species

        # Define cluster functions for elements
        self._reverse_id_maps = []
        for species in active_species:
            for species_map in cluster_space.species_maps:
                symbols = [periodic_table[n] for n in species_map]
                if set(symbols) == species:
                    reverse_id_map = {1 - species_map[n]: periodic_table[n] for n in species_map}
                    self._reverse_id_maps.append(reverse_id_map)
                    break
        self._count_symbols = [reverse_id_map[1] for reverse_id_map in self._reverse_id_maps]

        # Generate full orbit list
        self._orbit_list = cluster_space.orbit_list
        lolg = LocalOrbitListGenerator(
            orbit_list=self._orbit_list,
            structure=Structure.from_atoms(primitive_structure),
            fractional_position_tolerance=self._fractional_position_tolerance)
        self._full_orbit_list = lolg.generate_full_orbit_list()

        # Transform the parameters
        binary_parameters = transform_parameters(primitive_structure,
                                                 self._full_orbit_list,
                                                 self._cluster_expansion.parameters)
        self._transformed_parameters = binary_parameters

        # Build model
        self._model = self._build_model(structure)

        # Properties that are defined when searching for a ground state
        self._optimization_status = None

    def _build_model(self,
                     structure: Atoms) -> highspy.Highs:
        """
        Build a HiGHS model based on the provided structure.

        Parameters
        ----------
        structure
            Atomic configuration.
        """

        # Create cluster maps
        self._create_cluster_maps(structure)

        # Initiate MIP model
        model = highspy.Highs()

        # Spin variables (remapped) for all atoms in the structure
        xs = {i: model.addBinary(name=f'atom_{i}')
              for subl in self._active_sublattices for i in subl.indices}
        ys = [model.addBinary(name=f'cluster_{i}')
              for i in range(len(self._cluster_to_orbit_map))]

        # Connect cluster variables to spin variables with cluster constraints
        # TODO: don't create cluster constraints for singlets
        constraint_count = 0
        for i, cluster in enumerate(self._cluster_to_sites_map):
            orbit = self._cluster_to_orbit_map[i]
            parameter = self._transformed_parameters[orbit + 1]
            assert parameter != 0

            if len(cluster) < 2 or parameter < 0:  # no "downwards" pressure
                for atom in cluster:
                    model.addConstr(ys[i] <= xs[atom], f'Decoration -> cluster {constraint_count}')
                    constraint_count = constraint_count + 1

            if len(cluster) < 2 or parameter > 0:  # no "upwards" pressure
                model.addConstr(
                    ys[i] >= 1 - len(cluster) + highspy.highs.qsum(xs[atom] for atom in cluster),
                    'Decoration -> cluster {}'.format(constraint_count))
                constraint_count = constraint_count + 1

        for sym, subl in zip(self._count_symbols, self._active_sublattices):
            # Create slack variable
            slack = model.addIntegral(lb=0, ub=len(subl.indices), name=f'slackvar_{sym}')

            # Add slack constraint
            model.addConstr(slack <= -1, f'{sym} slack')

            # Set species constraint

            model.addConstr(
                highspy.highs.qsum([xs[i] for i in subl.indices]) + slack == -1, f'{sym} count')

        # Add an objective function to the 'model'
        model.setObjective(highspy.highs.qsum(self._get_total_energy(ys)),
                           highspy.ObjSense.kMinimize)

        # Update the model so that variables and constraints can be queried
        return model

    def _create_cluster_maps(self, structure: Atoms) -> None:
        """
        Create maps that include information regarding which sites and orbits
        are associated with each cluster as well as the number of clusters per
        orbit.

        Parameters
        ----------
        structure
            Atomic configuration.
        """
        # Generate full orbit list
        lolg = LocalOrbitListGenerator(
            orbit_list=self._orbit_list,
            structure=Structure.from_atoms(structure),
            fractional_position_tolerance=self._fractional_position_tolerance)
        full_orbit_list = lolg.generate_full_orbit_list()

        # Create maps of site indices and orbits for all clusters
        cluster_to_sites_map = []
        cluster_to_orbit_map = []
        for orb_index in range(len(full_orbit_list)):

            clusters = full_orbit_list.get_orbit(orb_index).clusters

            # Determine the sites and the orbit associated with each cluster
            for cluster in clusters:

                # Do not include clusters for which the parameter is 0
                parameter = self._transformed_parameters[orb_index + 1]
                if parameter == 0:
                    continue

                # Add the the list of sites and the orbit to the respective cluster maps
                cluster_sites = [site.index for site in cluster.lattice_sites]
                cluster_to_sites_map.append(cluster_sites)
                cluster_to_orbit_map.append(orb_index)

        # calculate the number of clusters per orbit
        nclusters_per_orbit = [cluster_to_orbit_map.count(i) for i in
                               range(cluster_to_orbit_map[-1] + 1)]
        nclusters_per_orbit = [1] + nclusters_per_orbit

        self._cluster_to_sites_map = cluster_to_sites_map
        self._cluster_to_orbit_map = cluster_to_orbit_map
        self._nclusters_per_orbit = nclusters_per_orbit

    def _get_total_energy(self, cluster_instance_activities: list[int]) -> list[float]:
        r"""
        Calculates the total energy using the expression based on binary variables.

        .. math::

            H({\boldsymbol x}, {\boldsymbol E})=E_0+
            \sum\limits_j\sum\limits_{{\boldsymbol c}
            \in{\boldsymbol C}_j}E_jy_{{\boldsymbol c}},

        where (:math:`y_{{\boldsymbol c}}=
        \prod\limits_{i\in{\boldsymbol c}}x_i`).

        Parameters
        ----------
        cluster_instance_activities
            list of cluster instance activities, (:math:`y_{{\boldsymbol c}}`)
        """

        E = [0.0 for _ in self._transformed_parameters]
        for i in range(len(cluster_instance_activities)):
            orbit = self._cluster_to_orbit_map[i]
            E[orbit + 1] = E[orbit + 1] + cluster_instance_activities[i]
        E[0] = 1

        E = [0.0 if np.isclose(self._transformed_parameters[orbit], 0.0) else
             E[orbit] * (self._transformed_parameters[orbit] / self._nclusters_per_orbit[orbit])
             for orbit in range(len(self._transformed_parameters))]
        return E

    def _change_constraint_bounds(self, name, lower_bound=None, upper_bound=None) -> None:
        r"""
        Changes the lower (:math:`b_l`) and upper bound (:math:`b_u`) of the specified
        constraint (:math:`b_l\leq\sum\limits_ic_ix_i\leq b_u`). Note that both should be set to
        the same value to represent an equality (:math:`\leq\sum\limits_ic_ix_i=b_l=b_u`).

        Parameters
        ----------
        name
            Name of constraint (key in the :attr:`self.constraints` dictionary).
        lower_bound
            New lower bound for the constraint.
        upper_bound
            New upper bound for the constraint.
        """
        if lower_bound is None and upper_bound is None:
            raise ValueError('Specify at least one bound.')

        cons = self.constraints[name]
        expr = cons.expr()
        if lower_bound is None:
            lower_bound = expr.bounds[0]
        elif np.isneginf(lower_bound):
            lower_bound = -self._model.inf
        if upper_bound is None:
            upper_bound = expr.bounds[1]
        elif np.isposinf(upper_bound):
            upper_bound = self._model.inf
        expr.bounds = (lower_bound, upper_bound)
        self._model.removeConstr(cons)
        self._model.addConstr(expr, name)

    def get_ground_state(self,
                         species_count: dict[str, int] = None,
                         max_seconds: float = inf,
                         threads: int = 0) -> Atoms:
        """Finds the ground state for a given structure and species count. If
        :attr:`species_count` is not provided when initializing the
        instance of this class the first species in the list of
        chemical symbols for the active sublattice will be used.

        Parameters
        ----------
        species_count
            Dictionary with count for one of the species on each active
            sublattice. If no count is provided for a sublattice, the
            concentration is allowed to vary.
        max_seconds
            Maximum runtime in seconds.
        threads
            Number of threads to be used when solving the problem, given that a
            positive integer has been provided. If set to :math:`0` the solver default
            configuration is used while :math:`-1` corresponds to all available
            processing cores.

        """
        if species_count is None:
            species_count = {}

        # Check that the species_count is consistent with the cluster space
        all_active_species = set.union(*self._active_species)
        for symbol in species_count:
            if symbol not in all_active_species:
                raise ValueError('The species {} is not present on any of the active sublattices'
                                 ' ({})'.format(symbol, self._active_species))

        # Solve model using the HiGHS MIP solver
        model = self._model

        # Update the species counts
        for i, species in enumerate(self._active_species):
            count_symbol = self._count_symbols[i]
            max_count = len(self._active_sublattices[i].indices)

            symbols_to_add = set.intersection(set(species_count), set(species))
            if len(symbols_to_add) > 1:
                raise ValueError('Provide counts for at most one of the species on each active '
                                 'sublattice ({}), not {}!'.format(self._active_species,
                                                                   list(species_count)))
            elif len(symbols_to_add) == 1:
                sym = symbols_to_add.pop()
                count = species_count[sym]
                if count < 0 or count > max_count:
                    raise ValueError('The count for species {} ({}) must be a positive integer and'
                                     ' cannot exceed the number of sites on the active sublattice '
                                     '({})'.format(sym, count, max_count))
                if sym == count_symbol:
                    xcount = count
                else:
                    xcount = max_count - count

                max_slack = 0
            else:
                xcount = max_slack = max_count

            self._change_constraint_bounds(f'{count_symbol} count', xcount, xcount)
            self._change_constraint_bounds(f'{count_symbol} slack', upper_bound=max_slack)

        # Set the time limit and number of threads
        model.setOptionValue('threads', threads)
        model.setOptionValue('time_limit', max_seconds)

        # Optimize the model
        model.run()
        self._optimization_status = model.getModelStatus()

        # The status of the solution is printed to the screen
        if model.modelStatusToString(self._optimization_status) != 'Optimal':
            if model.modelStatusToString(self._optimization_status) == 'ObjectiveTarget':
                logger.info('Target value for the model objective has been reached.')
            else:
                raise Exception('Optimization failed ({0})'.format(
                    model.modelStatusToString(self._optimization_status)))

        # Each of the variables is printed with it's resolved optimum value
        values = list(model.getSolution().col_value)
        gs = self.structure.copy()

        active_index_to_sublattice_map = {i: j for j, subl in enumerate(self._active_sublattices)
                                          for i in subl.indices}
        for v in model.getVariables():
            if 'atom' in v.name:
                index = int(v.name.split('_')[-1])
                sublattice_index = active_index_to_sublattice_map[index]
                gs[index].symbol = self._reverse_id_maps[sublattice_index][np.rint(values[v.index])]

        # Assert that the solution agrees with the prediction
        prediction = self._cluster_expansion.predict(gs)
        assert abs(model.getInfo().objective_function_value - prediction) < 1e-6
        return gs

    @property
    def optimization_status(self) -> highspy.HighsModelStatus:
        """ Optimization status. """
        return self._optimization_status

    @property
    def model(self) -> highspy.Highs:
        """ HiGHS model. """
        return self._model

    @property
    def constraints(self) -> dict[str, highs_cons]:
        """ Dictionary with highs_cons objects and the names as keys. """
        return {cons.name: cons for cons in self._model.getConstrs()}
