# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import copy
import os
import rdflib
import rdflib.compare
import unittest
from pyanzo import AnzoClient, Quad, QuadStore

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
)


class TestQuadStore(unittest.TestCase):
    tmp_filename = "tests/test_assets/tmp.trig"

    trig_filename = "tests/test_assets/sample.trig"
    n3_filename = "tests/test_assets/sample.n3"
    ttl_filename = "tests/test_assets/sample.ttl"
    trix_filename = "tests/test_assets/sample.trix"
    json_ld_filename = "tests/test_assets/sample.json"
    trig_with_bnodes_filename = "tests/test_assets/trig_with_bnodes.trig"

    rdflib_graph = rdflib.ConjunctiveGraph()
    expected_num_statements = 3

    record_dicts = [
        {
            's': 'http://csi.test.com/subject1',
            'p': 'http://csi.test.com/predicate1',
            'o': 'http://csi.test.com/object1',
            'g': 'http://csi.test.com/'
        }, {
            's': 'http://csi.test.com/subject2',
            'p': 'http://csi.test.com/predicate2',
            'o': 'http://csi.test.com/object2',
            'g': 'http://csi.test.com/'
        }, {
            's': 'http://csi.test.com/subject2',
            'p': 'http://csi.test.com/predicate3',
            'o': 7,
            'g': 'http://csi.test.com/graph2'
        }
    ]

    record_dicts_without_graphs = [
        {
            's': 'http://csi.test.com/subject1',
            'p': 'http://csi.test.com/predicate1',
            'o': 'http://csi.test.com/object1'
        }, {
            's': 'http://csi.test.com/subject2',
            'p': 'http://csi.test.com/predicate2',
            'o': 'http://csi.test.com/object2'
        }, {
            's': 'http://csi.test.com/subject2',
            'p': 'http://csi.test.com/predicate3',
            'o': 7
        }
    ]

    quad_set = {
        Quad("http://csi.test.com/subject1",
             "http://csi.test.com/predicate1",
             "http://csi.test.com/object1",
             "http://csi.test.com/"),
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate2",
             "http://csi.test.com/object2",
             "http://csi.test.com/"),
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate3",
             "7",
             "http://csi.test.com/graph2",
             obj_type="literal",
             obj_data_type="http://www.w3.org/2001/XMLSchema#integer"),
    }

    quad_store = QuadStore(copy.deepcopy(quad_set))

    quad_store_without_graphs = QuadStore(
        {
            Quad(q.sub, q.pred, q.obj, None, q.sub_type,
                 q.obj_type, q.obj_data_type)
            for q in quad_set
        }
    )

    def setUp(self) -> None:
        self.rdflib_graph.parse(self.trig_filename, format="trig")

        self.anzo_client = AnzoClient(
            DOMAIN, PORT, username=USERNAME, password=PASSWORD
        )

    def test_from_anzo_json(self) -> None:
        json_one = {"namedGraphUri": "http://csi.test.com/",
                    "subject": {
                        "objectType": "uri",
                        "value": "http://csi.test.com/subject1",
                    },
                    "predicate": "http://csi.test.com/predicate1",
                    "object": {
                        "objectType": "uri",
                        "value": "http://csi.test.com/object1"
                    }
                    }
        json_two = {"namedGraphUri": "http://csi.test.com/",
                    "subject": {
                        "objectType": "uri",
                        "value": "http://csi.test.com/subject2",
                    },
                    "predicate": "http://csi.test.com/predicate2",
                    "object": {
                        "objectType": "uri",
                        "value": "http://csi.test.com/object2"
                    }
                    }

        json_three = {"namedGraphUri": "http://csi.test.com/graph2",
                      "subject": {
                          "objectType": "uri",
                          "value": "http://csi.test.com/subject2",
                      },
                      "predicate": "http://csi.test.com/predicate3",
                      "object": {
                          "dataType": "http://www.w3.org/2001/XMLSchema#integer",
                          "objectType": "literal",
                          "value": "7"
                      }
                      }

        quad_store = QuadStore.from_anzo_json_list(
            [json_one, json_two, json_three]
        )
        self.assertEqual(quad_store, self.quad_store)

    def test_from_anzo_json_error(self) -> None:
        json = {"Penny": 1}
        quad_store = QuadStore()
        self.assertRaises(RuntimeError, quad_store.from_anzo_json_list, json)

    def test_from_rdflib_graph(self) -> None:
        qs = QuadStore.from_rdflib_graph(self.rdflib_graph)
        self.assertEqual(qs, self.quad_store)

        # Test with a non-conjuctive graph
        graph = rdflib.ConjunctiveGraph()
        graph.parse(self.trig_filename, format="trig")
        qs = QuadStore.from_rdflib_graph(self.rdflib_graph)
        self.assertEqual(qs, self.quad_store)

    def test_from_trig_file(self) -> None:
        qs = QuadStore.from_trig_file(self.trig_filename)
        self.assertEqual(qs, self.quad_store)

    def test_to_trig_file(self) -> None:
        self.quad_store.write_to_trig_file(self.tmp_filename)
        qs = QuadStore.from_trig_file(self.tmp_filename)
        self.assertEqual(qs, self.quad_store)
        os.remove(self.tmp_filename)

    def test_from_ttl_file(self) -> None:
        qs = QuadStore.from_file(self.ttl_filename, "ttl")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_ttl_file(self) -> None:
        self.quad_store.write_to_file(self.tmp_filename, "ttl")
        qs = QuadStore.from_file(self.tmp_filename, "ttl")
        self.assertEqual(qs, self.quad_store_without_graphs)
        os.remove(self.tmp_filename)

    def test_from_n3_file(self) -> None:
        qs = QuadStore.from_file(self.n3_filename, "n3")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_n3_file(self) -> None:
        self.quad_store.write_to_file(self.tmp_filename, "n3")
        qs = QuadStore.from_file(self.tmp_filename, "n3")
        self.assertEqual(qs, self.quad_store_without_graphs)
        os.remove(self.tmp_filename)

    def test_from_trix_file(self) -> None:
        qs = QuadStore.from_file(self.trix_filename, "trix")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_trix_file(self) -> None:
        self.quad_store.write_to_file(self.tmp_filename, "trix")
        qs = QuadStore.from_file(self.tmp_filename, "trix")
        self.assertEqual(qs, self.quad_store_without_graphs)
        os.remove(self.tmp_filename)

    def test_from_json_ld_file(self) -> None:
        qs = QuadStore.from_file(self.json_ld_filename, "json-ld")
        self.assertEqual(qs, self.quad_store)

    def test_to_json_ld_file(self) -> None:
        self.quad_store.write_to_file(self.tmp_filename, "json-ld")
        qs = QuadStore.from_file(self.tmp_filename, "json-ld")
        self.assertEqual(qs, self.quad_store)
        os.remove(self.tmp_filename)

    def test_as_rdflib_graph(self) -> None:
        rdflib_graph = self.quad_store.as_rdflib_graph()

        self.assertTrue(
            rdflib.compare.isomorphic(rdflib_graph, self.rdflib_graph)
        )

    def test_as_rdflib_graph_with_bnodes(self) -> None:
        sub = "subject2"
        pred = "http://csi.test.com/predicate3"
        obj = "http://csi.test.com/object3"
        graph = "http://csi.test.com/graph2"

        quad_store = QuadStore({Quad(sub, pred, obj, graph, "bnode", "uri")})
        g = quad_store.as_rdflib_graph()

        expected_g = rdflib.ConjunctiveGraph()
        expected_g.add((
            rdflib.BNode(sub),
            rdflib.URIRef(pred),
            rdflib.URIRef(obj),
            rdflib.URIRef(graph),
        ))

        self.assertTrue(
            rdflib.compare.isomorphic(g, expected_g)
        )

    def test_as_record_dictionaries(self) -> None:
        record_dicts = self.quad_store.as_record_dictionaries()

        self.assertEqual(
            sorted(record_dicts,
                   key=lambda d: (d['s'], d['p'], d['o'], d['g'])),
            sorted(self.record_dicts,
                   key=lambda d: (d['s'], d['p'], d['o'], d['g']))
        )

    def test_as_record_dictionaries_without_graphs(self) -> None:
        record_dicts = self.quad_store_without_graphs.as_record_dictionaries()
        self.assertEqual(
            sorted(record_dicts, key=lambda d: (d['s'], d['p'], d['o'])),
            sorted(self.record_dicts_without_graphs,
                   key=lambda d: (d['s'], d['p'], d['o']))
        )

    def test_quad_store_iterator_correct(self) -> None:
        quad_store = QuadStore(copy.deepcopy(self.quad_set))
        result = [quad for quad in quad_store]
        self.assertEqual(sorted(result), sorted(list(self.quad_set)))

    def test_filtering_by_nothing(self) -> None:
        quad_store = QuadStore(copy.deepcopy(self.quad_set))
        filtered_store = quad_store.filter()
        self.assertEqual(quad_store, filtered_store)

    def test_filtering_by_subject(self) -> None:
        quad_store = QuadStore(copy.deepcopy(self.quad_set))
        result_store = quad_store.filter(
            subject="http://csi.test.com/subject2"
        )

        expected_store = QuadStore({
            Quad("http://csi.test.com/subject2",
                 "http://csi.test.com/predicate3",
                 "7",
                 "http://csi.test.com/graph2",
                 obj_type="literal",
                 obj_data_type="http://www.w3.org/2001/XMLSchema#integer"),
            Quad("http://csi.test.com/subject2",
                 "http://csi.test.com/predicate2",
                 "http://csi.test.com/object2",
                 "http://csi.test.com/")
        })

        self.assertEqual(expected_store, result_store)

    def test_add_basic(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            new = qs.add(quad)
            self.assertTrue(new)
        self.assertEqual(self.quad_store, qs)

    def test_add_repeat(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)

        quad = next(iter(self.quad_set))
        new = qs.add(quad)
        self.assertEqual(self.quad_store, qs)
        self.assertFalse(new)

    def test_remove(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)
        quad = next(iter(self.quad_set))
        removed = qs.remove(quad)
        self.assertEqual(len(qs), len(self.quad_store) - 1)
        self.assertTrue(removed)

    def test_remove_nonexist(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)
        quad = next(iter(self.quad_set))
        qs.remove(quad)
        removed = qs.remove(quad)  # this one should be a no-op, return false
        self.assertEqual(len(qs), len(self.quad_store) - 1)
        self.assertFalse(removed)

    def test_set_basic(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)

        update_quad = Quad("http://csi.test.com/subject1",
                           "http://csi.test.com/predicate1",
                           "http://csi.test.com/object2",
                           "http://csi.test.com/")

        # should upsert existing statement - object1 changes to object2
        upsert = qs.set(update_quad)

        self.assertTrue(upsert)
        self.assertEqual(len(qs), len(self.quad_store))
        # this should be the updated quad
        quad = qs.filter(subject=update_quad.sub, predicate=update_quad.pred,
                         graph=update_quad.graph).quads.pop()
        self.assertEqual(quad.obj, "http://csi.test.com/object2")

    def test_set_multiple_previous(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)

        add_quad = Quad("http://csi.test.com/subject1",
                        "http://csi.test.com/predicate1",
                        "http://csi.test.com/object2",
                        "http://csi.test.com/")
        qs.add(add_quad)  # add a new statement
        # qs should be 1 greater than base quad_store because we added a quad
        self.assertEqual(len(qs), len(self.quad_store) + 1)

        update_quad = Quad("http://csi.test.com/subject1",
                           "http://csi.test.com/predicate1",
                           "http://csi.test.com/object3",
                           "http://csi.test.com/")
        upsert = qs.set(update_quad)

        self.assertTrue(upsert)
        # should now be same size as original because we've reset the statement
        self.assertEqual(len(qs), len(self.quad_store))

        # this should be the updated quad
        quad = qs.filter(subject=update_quad.sub, predicate=update_quad.pred,
                         graph=update_quad.graph).quads.pop()
        self.assertEqual(quad.obj, "http://csi.test.com/object3")

    def test_set_none_previous(self) -> None:
        qs = QuadStore()
        for quad in self.quad_set:
            qs.add(quad)

        update_quad = Quad("http://csi.test.com/subject1",
                           "http://csi.test.com/predicate4",
                           "http://csi.test.com/object4",
                           "http://csi.test.com/")
        # should insert a new statement
        upsert = qs.set(update_quad)

        self.assertFalse(upsert)
        self.assertEqual(len(qs), len(self.quad_store) + 1)
        # this should be the new quad
        quad = qs.filter(subject=update_quad.sub, predicate=update_quad.pred,
                         graph=update_quad.graph).quads.pop()
        self.assertEqual(quad.obj, "http://csi.test.com/object4")

    def test_trig_with_bnodes(self):
        qs = QuadStore.from_trig_file(self.trig_with_bnodes_filename)
        g = qs.as_rdflib_graph()

        rdflib_graph = rdflib.ConjunctiveGraph()
        rdflib_graph.parse(self.trig_with_bnodes_filename, format="trig")
        self.assertTrue(
            rdflib.compare.isomorphic(rdflib_graph, qs.as_rdflib_graph())
        )

    def test_to_trig_string(self) -> None:
        s = self.quad_store.to_trig_string()
        qs = QuadStore.from_trig_string(s)
        self.assertEqual(qs, self.quad_store)

    def test_to_trig_string2(self) -> None:
        s = self.quad_store.to_string("trig")
        qs = QuadStore.from_string(s, "trig")
        self.assertEqual(qs, self.quad_store)

    def test_to_from_json_ld_string(self) -> None:
        s = self.quad_store.to_string("json-ld")
        qs = QuadStore.from_string(s, "json-ld")
        self.assertEqual(qs, self.quad_store)

    def test_to_from_ttl_string(self) -> None:
        s = self.quad_store.to_string("ttl")
        qs = QuadStore.from_string(s, "ttl")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_from_n3_string(self) -> None:
        s = self.quad_store.to_string("n3")
        qs = QuadStore.from_string(s, "n3")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_from_trix_string(self) -> None:
        s = self.quad_store.to_string("trix")
        qs = QuadStore.from_string(s, "trix")
        self.assertEqual(qs, self.quad_store_without_graphs)

    def test_to_string_bad_format(self) -> None:
        self.assertRaises(
            Exception, self.quad_store.to_string, "foo"
        )

    def test_form_string_bad_format(self) -> None:
        s = self.quad_store.to_string("trig")

        self.assertRaises(
            Exception, QuadStore.from_string, s, "ttl"
        )

        self.assertRaises(
            Exception, QuadStore.from_string, s, "foo"
        )

        self.assertRaises(
            Exception, QuadStore.from_string, s, ""
        )
