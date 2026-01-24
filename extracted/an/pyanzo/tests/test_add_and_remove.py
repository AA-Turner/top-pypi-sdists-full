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


class TestAnzoClientAddAndRemove(unittest.TestCase):
    named_graph_uri = "http://cambridgesemantics.com/namedgraph/addremove"
    non_existent_named_graph_uri = "http://cambridgesemantics.com/namedgraph/doesntexist"  # noqa

    quad1 = Quad(
        sub="http://cambridgesemantics.com/namedgraph/addremove/sub1",
        pred="http://cambridgesemantics.com/namedgraph/addremove/pred2",
        obj="http://cambridgesemantics.com/namedgraph/addremove/obj1",
        graph=named_graph_uri
    )

    quad2 = Quad(
        sub="http://cambridgesemantics.com/namedgraph/addremove/sub1",
        pred="http://cambridgesemantics.com/namedgraph/addremove/pred2",
        obj="http://cambridgesemantics.com/namedgraph/addremove/obj2",
        graph=named_graph_uri
    )

    quad3 = Quad(
        sub="http://cambridgesemantics.com/namedgraph/addremove/sub1",
        pred="http://cambridgesemantics.com/namedgraph/addremove/pred3",
        obj="http://cambridgesemantics.com/namedgraph/addremove/obj2",
        graph=named_graph_uri
    )

    non_existent_quad = Quad(
        sub="http://cambridgesemantics.com/namedgraph/addremove/sub1",
        pred="http://cambridgesemantics.com/namedgraph/addremove/pred2",
        obj="http://cambridgesemantics.com/namedgraph/addremove/obj1",
        graph=non_existent_named_graph_uri
    )

    sample_prefix = "http://csi.test.com/"

    sample_quad1 = Quad(
        sub=f"{sample_prefix}subject1",
        pred=f"{sample_prefix}predicate1",
        obj=f"{sample_prefix}object1",
        graph=sample_prefix)

    sample_quad2 = Quad(
        sub=f"{sample_prefix}subject2",
        pred=f"{sample_prefix}predicate2",
        obj=f"{sample_prefix}object2",
        graph=sample_prefix)

    sample_graph1 = QuadStore(set([sample_quad1, sample_quad2]))

    sample_graph2 = QuadStore(set([Quad(
        sub=f"{sample_prefix}subject2",
        pred=f"{sample_prefix}predicate3",
        obj="7",
        graph=f"{sample_prefix}graph2",
        obj_type="literal",
        obj_data_type="http://www.w3.org/2001/XMLSchema#integer")]))

    @classmethod
    def wipe_graph(cls) -> None:
        ac = AnzoClient(DOMAIN, PORT, username=USERNAME, password=PASSWORD)
        query = f"""
            DELETE {{ GRAPH ?g {{ ?s ?p ?o }} }}
            WHERE {{
                GRAPH ?g {{ ?s ?p ?o }}
                FILTER(?g=?graph)
                VALUES(?graph)
                {{(<{cls.named_graph_uri}>)
                  (<{cls.sample_prefix}>)
                  (<{cls.sample_prefix}graph2>)
                  }}
            }}
        """
        ac.update_journal(query)

    @classmethod
    def setUpClass(cls) -> None:
        cls.wipe_graph()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.wipe_graph()

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            DOMAIN, PORT, username=USERNAME, password=PASSWORD
        )

    def test_add_and_remove(self) -> None:
        self.anzo_client.add(quad_store=QuadStore({self.quad1}))
        self.assertEqual(
            QuadStore({self.quad1}),
            self.anzo_client.get(self.named_graph_uri)
        )

        self.anzo_client.add(quad_store=QuadStore({self.quad2, self.quad3}))

        self.assertEqual(
            QuadStore({self.quad1, self.quad2, self.quad3}),
            self.anzo_client.get(self.named_graph_uri)
        )

        self.anzo_client.remove(QuadStore({self.quad1}))
        self.assertEqual(
            QuadStore({self.quad2, self.quad3}),
            self.anzo_client.get(self.named_graph_uri)
        )

        self.anzo_client.remove(QuadStore({self.quad2, self.quad3}))
        self.assertEqual(
            QuadStore({}),
            self.anzo_client.get(self.named_graph_uri)
        )

    def test_add_from_file(self) -> None:

        self.anzo_client.add(trig_filename="tests/test_assets/sample.trig")
        self.assertEqual(self.sample_graph1,
                         self.anzo_client.get(self.sample_prefix))

        self.assertEqual(self.sample_graph2,
                         self.anzo_client.get(f"{self.sample_prefix}graph2"))

    def test_remove_from_file(self) -> None:

        self.anzo_client.add(quad_store=self.sample_graph1)
        self.anzo_client.add(quad_store=self.sample_graph2)

        self.assertNotEqual(
            QuadStore({}),
            self.anzo_client.get(self.sample_prefix))

        self.assertNotEqual(
            QuadStore({}),
            self.anzo_client.get(f"{self.sample_prefix}graph2"))

        self.anzo_client.remove(trig_filename="tests/test_assets/sample.trig")

        self.assertEqual(
            QuadStore({}),
            self.anzo_client.get(self.sample_prefix))

        self.assertEqual(
            QuadStore({}),
            self.anzo_client.get(f"{self.sample_prefix}graph2"))

    def test_add_and_remove_too_many_inputs(self) -> None:
        trig = "tests/test_assets/sample.trig"
        self.assertRaises(ValueError,
                          self.anzo_client.add,
                          quad_store=self.sample_graph1,
                          trig_filename=trig)

        self.assertRaises(ValueError,
                          self.anzo_client.remove,
                          quad_store=self.sample_graph1,
                          trig_filename=trig)

    def test_add_and_remove_too_few_inputs(self) -> None:
        self.assertRaises(ValueError,
                          self.anzo_client.add)

        self.assertRaises(ValueError,
                          self.anzo_client.remove)

    def test_removing_non_existent_quad(self) -> None:
        self.anzo_client.remove(QuadStore({self.non_existent_quad}))
