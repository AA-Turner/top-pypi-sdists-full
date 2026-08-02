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
import parameterized

import dwave.graphs


@parameterized.parameterized_class(
    'graph',
    [[nx.Graph()],
     [nx.path_graph(10)],
     [nx.complete_graph(4)],
     [nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5)])],
     [nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5)])],
     [nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)])],
     [nx.Graph({0: [], 1: [6], 2: [5], 3: [4], 4: [3], 2: [5], 6: [1]})]
     # [nx.Graph([(0, 3), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 7),
     #            (2, 4), (2, 6), (3, 6), (3, 7), (4, 7), (6, 7)])],  # slow
     ]
    )
class TestMatching(unittest.TestCase):
    def test_maximal_matching(self):
        matching = dwave.graphs.algorithms.maximal_matching(
            self.graph, dimod.ExactSolver())
        self.assertTrue(nx.is_maximal_matching(self.graph, matching))

    def test_min_maximal_matching(self):
        matching = dwave.graphs.algorithms.min_maximal_matching(
            self.graph, dimod.ExactSolver())
        self.assertTrue(nx.is_maximal_matching(self.graph, matching))
