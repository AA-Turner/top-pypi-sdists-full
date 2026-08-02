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

import unittest

import dimod
import networkx as nx

import dwave.graphs


class TestMinVertexColor(unittest.TestCase):
    def test_5path(self):
        G = nx.path_graph(5)
        coloring = dwave.graphs.min_vertex_coloring(G, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))
        self.assertEqual(len(set(coloring.values())), 2)  # bipartite

    def test_odd_cycle_graph(self):
        """Graph that is an odd circle"""
        G = nx.cycle_graph(5)
        coloring = dwave.graphs.min_vertex_coloring(G, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))

    def test_disconnected_graph(self):
        """One edge and one disconnected node"""
        G = nx.path_graph(2)
        G.add_node(3)

        coloring = dwave.graphs.min_vertex_coloring(G, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))

    def test_disconnected_cycle_graph(self):
        G = nx.complete_graph(3)  # odd 3-cycle
        G.add_node(4)  # floating node
        coloring = dwave.graphs.min_vertex_coloring(G, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))


class TestVertexColor(unittest.TestCase):
    def test_4cycle(self):
        G = nx.cycle_graph('abcd')

        coloring = dwave.graphs.vertex_coloring(G, 2, dimod.ExactSolver())

        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))

    def test_4cycle_with_chord(self):
        G = nx.cycle_graph(4)
        G.add_edge(0, 2)

        # need 3 colors in this case
        coloring = dwave.graphs.vertex_coloring(G, 3, dimod.ExactSolver())

        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))

    def test_5cycle(self):
        G = nx.cycle_graph(5)
        coloring = dwave.graphs.vertex_coloring(G, 3, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))

    def test_disconnected_cycle_graph(self):
        G = nx.complete_graph(3)  # odd 3-cycle
        G.add_node(4)  # floating node
        coloring = dwave.graphs.vertex_coloring(G, 3, dimod.ExactSolver())
        self.assertTrue(dwave.graphs.is_vertex_coloring(G, coloring))
