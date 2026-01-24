# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
from pyanzo import AnzoClient, Quad, QuadStore

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
)


class TestAnzoClientGet(unittest.TestCase):
    graph_uri = "http://cambridgesemantics.com/namedgraph/1"
    md_graph_uri = "http://openanzo.org/metadataGraphs(http%3A%2F%2Fcambridgesemantics.com%2Fnamedgraph%2F1)"  # noqa

    expected_quad = Quad(
        sub='http://cambridgesemantics.com/namedgraph/1/sub',
        pred='http://cambridgesemantics.com/namedgraph/1/pred',
        obj='http://cambridgesemantics.com/namedgraph/1/obj',
        graph='http://cambridgesemantics.com/namedgraph/1'
    )

    expected_quadstore = QuadStore({expected_quad})

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            DOMAIN, PORT, username=USERNAME, password=PASSWORD)

    def test_get(self) -> None:
        result = self.anzo_client.get(self.graph_uri)
        result = result.filter(graph=self.expected_quad.graph)
        self.assertEqual(result, self.expected_quadstore)

    def test_get_with_nonexistent_graph(self) -> None:
        graph_uri = "urn://this/graph/doesnt/exist"
        self.assertRaises(RuntimeError, self.anzo_client.get, graph_uri)

    def test_get_with_metadatagraph(self) -> None:
        result = self.anzo_client.get(
            self.graph_uri, include_metadata_graph=True
        )

        md_graph = result.filter(graph=self.md_graph_uri)
        self.assertTrue(len(md_graph) > 3)

        self.assertNotEqual(result, self.expected_quadstore)

        self.assertEqual(
            result.filter(graph=self.expected_quad.graph),
            self.expected_quadstore
        )
