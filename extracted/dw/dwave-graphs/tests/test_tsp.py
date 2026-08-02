# Copyright 2018 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import itertools
import unittest

import dimod
import networkx as nx

from dwave.graphs import is_hamiltonian_path, traveling_salesperson


# adapted from future networkx version (nx.path_weight(...))
def path_weight(G, path):
    '''Return the total cost of a cycle in G specified by path.'''
    cost = 0
    for node, nbr in nx.utils.pairwise(path):
        cost += G[node][nbr]['weight']
    # add back to the starting point
    cost += G[path[-1]][path[0]]['weight']
    return cost


class TestIsHamiltonCycle(unittest.TestCase):
    def test_empty(self):
        G = nx.Graph()

        self.assertTrue(is_hamiltonian_path(G, []))

    def test_K1(self):
        G = nx.complete_graph(1)

        self.assertTrue(is_hamiltonian_path(G, [0]))
        self.assertFalse(is_hamiltonian_path(G, []))

    def test_K2(self):
        G = nx.complete_graph(2)

        self.assertTrue(is_hamiltonian_path(G, [0, 1]))
        self.assertTrue(is_hamiltonian_path(G, [1, 0]))
        self.assertFalse(is_hamiltonian_path(G, [0]))
        self.assertFalse(is_hamiltonian_path(G, [1]))
        self.assertFalse(is_hamiltonian_path(G, []))

    def test_K3(self):
        G = nx.complete_graph(3)

        self.assertTrue(is_hamiltonian_path(G, [0, 1, 2]))
        self.assertTrue(is_hamiltonian_path(G, [1, 0, 2]))
        self.assertFalse(is_hamiltonian_path(G, [0, 1]))
        self.assertFalse(is_hamiltonian_path(G, [0]))
        self.assertFalse(is_hamiltonian_path(G, [1]))
        self.assertFalse(is_hamiltonian_path(G, []))


class TestTSP(unittest.TestCase):
    def test_TSP_basic(self):
        """Runs the function on some small and simple graphs, just to make
        sure it works in basic functionality.
        """
        G = nx.complete_graph(4)
        for u, v in G.edges():
            G[u][v]['weight'] = 1
        route = traveling_salesperson(G, dimod.ExactSolver())
        self.assertTrue(is_hamiltonian_path(G, route))

        G = nx.complete_graph(4)
        for u, v in G.edges():
            G[u][v]['weight'] = u+v
        route = traveling_salesperson(G, dimod.ExactSolver(), lagrange=10.0)
        self.assertTrue(is_hamiltonian_path(G, route))

    def test_dimod_vs_list(self):
        G = nx.complete_graph(4)
        for u, v in G.edges():
            G[u][v]['weight'] = 1

        route = traveling_salesperson(G, dimod.ExactSolver())
        route = traveling_salesperson(G, dimod.SimulatedAnnealingSampler())

    def test_weighted_complete_graph(self):
        G = nx.Graph()
        G.add_weighted_edges_from({(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 2, 3),
                                   (1, 3, 4), (2, 3, 5)})
        route = traveling_salesperson(G, dimod.ExactSolver(), lagrange=10)

        self.assertEqual(len(route), len(G))

    def test_start(self):
        G = nx.Graph()
        G.add_weighted_edges_from((u, v, .5)
                                  for u, v in itertools.combinations(range(3), 2))

        route = traveling_salesperson(G, dimod.ExactSolver(), start=1)

        self.assertEqual(route[0], 1)

    def test_weighted_complete_digraph(self):
        G = nx.DiGraph()
        G.add_weighted_edges_from([
            (0, 1, 2),
            (1, 0, 1),
            (0, 2, 2),
            (2, 0, 2),
            (0, 3, 1),
            (3, 0, 2),
            (1, 2, 2),
            (2, 1, 1),
            (1, 3, 2),
            (3, 1, 2),
            (2, 3, 2),
            (3, 2, 1),
        ])

        route = traveling_salesperson(G, dimod.ExactSolver(), start=1)

        self.assertEqual(len(route), len(G))
        self.assertListEqual(route, [1, 0, 3, 2])

        cost = path_weight(G, route)

        self.assertEqual(cost, 4)
