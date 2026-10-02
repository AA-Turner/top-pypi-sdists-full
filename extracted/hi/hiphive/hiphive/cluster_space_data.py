from typing import Any, Dict, List
import numpy as np
from .input_output.pretty_table_prints import print_table
from pandas import DataFrame


class ClusterSpaceData:

    """Container class that holds information concerning a cluster space, including,
    e.g., the number of cluster, orbits, and parameters by order and number of bodies.

    Parameters
    ----------
    cs : ClusterSpace
        cluster space
    """

    def __init__(self, cs) -> None:
        self.max_nbody = cs.cutoffs.max_nbody
        self.max_order = cs.cutoffs.max_order

        # collect cutoff matrix
        self._cutoff_matrix = cs.cutoffs.cutoff_matrix

        # collect cluster, orbit, eigentensor counts
        self._cluster_counts = np.zeros((self.max_nbody, self.max_order - 1), dtype=int)
        self._orbit_counts = np.zeros((self.max_nbody, self.max_order - 1), dtype=int)
        self._eigentensor_counts = np.zeros((self.max_nbody, self.max_order - 1), dtype=int)
        for orbit in cs.orbits:
            proto_cluster = cs.cluster_list[orbit.prototype_index]
            order = len(proto_cluster)
            nbody = len(set(proto_cluster))
            self._cluster_counts[nbody-1, order-2] += len(orbit.orientation_families)
            self._orbit_counts[nbody-1, order-2] += 1
            self._eigentensor_counts[nbody-1, order-2] += len(orbit.eigentensors)

        # collect number of parameters after sum rule constraint
        self.ndofs_by_order = {o: cs.get_n_dofs_by_order(o) for o in cs.cutoffs.orders}

    def print_tables(self) -> None:
        """ Prints information concerning the underlying cluster space to stdout, including,
        e.g., the number of cluster, orbits, and parameters by order and number of bodies. """

        # print table data
        print('Cutoff Matrix')
        print_table(self._cutoff_matrix_padded)
        print('\nCluster counts')
        print_table(self._cluster_counts, include_sum=True)
        print('\nOrbit counts')
        print_table(self._orbit_counts, include_sum=True)
        print('\nEigentensor counts')
        print_table(self._eigentensor_counts, include_sum=True)

    @property
    def _cutoff_matrix_padded(self) -> np.array:
        """ Padded cutoff matrix with None for nbody=1 terms """
        return np.vstack(([[None] * (self.max_order - 1)], self._cutoff_matrix))

    def to_list(self) -> List[Dict[str, Any]]:
        """ Returns cluster space data in the form of a list of dicts. """
        records = []
        for order in range(2, self.max_order+1):
            for nbody in range(1, self.max_nbody+1):
                if nbody > order:
                    continue
                row = dict(order=order, nbody=nbody)
                row['cutoff'] = self._cutoff_matrix_padded[nbody-1, order-2]
                row['cluster_counts'] = self._cluster_counts[nbody-1, order-2]
                row['orbit_counts'] = self._orbit_counts[nbody-1, order-2]
                row['eigentensor_counts'] = self._eigentensor_counts[nbody-1, order-2]
                records.append(row)
        return records

    def to_dataframe(self) -> DataFrame:
        """ Returns cluster space data in the form of a pandas DataFrame. """
        return DataFrame.from_dict(self.to_list())

    def __str__(self) -> str:
        s = f'Cutoff matrix: \n {self._cutoff_matrix}\n'
        s += f'Cluster counts: \n{self._cluster_counts}\n'
        s += f'Orbit counts: \n{self._orbit_counts}\n'
        s += f'Eigentensor counts: \n{self._eigentensor_counts}\n'
        s += f'Degrees of freedoms: \n{self.ndofs_by_order}\n'
        return s

    def __repr__(self) -> str:
        return str(self)
