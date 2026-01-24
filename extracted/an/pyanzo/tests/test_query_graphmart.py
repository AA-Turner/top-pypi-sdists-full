# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
import time
import os

from pyanzo import (
    AnzoClient,
    QueryResult,
    QuadStore,
    Quad,
    TYPE_PRED,
)

from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestAnzoClientQueryGraphmart(unittest.TestCase):
    # Paramterized values for the tests. This value is overwritten by the
    # values in the decorator

    graphmart = GRAPHMART

    # A simple select query used for testing core functionality in the tests
    select_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    select_query_results_first_layer = [
        ["Cambridge"],
        ["Somerville"],
        ["Watertown"],
    ]

    select_query_results_second_layer = [
        ["Boston"],
        ["Medford"],
    ]

    select_query_results = [
        ["Boston"],
        ["Cambridge"],
        ["Medford"],
        ["Somerville"],
        ["Watertown"],
    ]

    construct_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        CONSTRUCT {
            ?s a data:Person .
        } WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 1
    """  # noqa

    construct_query_results = QuadStore({
        Quad(
            "http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0",
            TYPE_PRED,
            "http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person",  # noqa
            ""
        )
    })

    layer_one_uri = "http://cambridgesemantics.com/Layer/dd29f470d8d44dad8e6cf9ce3b6322fd"  # noqa
    layer_two_uri = "http://cambridgesemantics.com/Layer/d2bb3f418d7942d8a85fdedad608ccb3"  # noqa

    # TODO: WHY ISNT THIS USED ANYWHERE?
    # A slightly more complicated query,
    # useful for checking behavior of unbound variables
    select_query_with_optional = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city ?height WHERE {
          ?s a data:Person ;
               data:Person_Name ?name ;
               data:Person_City ?city ;
               data:Person_Age ?age .

          # person height is not a property and
          # will be unbound by design (for testing)
          OPTIONAL { ?s  data:Person_Height  ?height }

        } ORDER BY ?city LIMIT 5
     """  # noqa

    # TODO: is this not used anywhere??
    # The expected result of self.select_query_with_optional
    select_query_with_optional_results = QueryResult("""{
        "head": {"vars": ["city", "height"]},
        "results": {
            "bindings": [
                {"city": {"type": "literal", "value": "Boston"}},
                {"city": {"type": "literal", "value": "Cambridge"}},
                {"city": {"type": "literal", "value": "Medford"}},
                {"city": {"type": "literal", "value": "Somerville"}},
                {"city": {"type": "literal", "value": "Watertown"}}
            ]
        }
    }""")

    # Test with query files
    select_query_file = os.path.join(
        "tests", "test_assets", "simple_graphmart_query.rq"
    )

    malformed_query_file = os.path.join(
        "tests", "test_assets", "malformed_graphmart_query.rq"
    )

    # The test docstrings are convenient when looking at the code, but
    # they make the verbose testing view look cluttered. This function
    # removes comments/descriptions from the verbose test view.
    def shortDescription(self) -> str:
        return None

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )

    @unittest.skip("Requires Anzo improvement to pass")
    def test_with_ask_query_true(self) -> None:
        query = "ASK WHERE { ?s ?p ?o }"
        result = self.anzo_client.query_graphmart(
            self.graphmart, query
        )

        self.assertEqual(
            result.as_table_results().as_list(), ["true"]
        )

    @unittest.skip("Requires Anzo improvement to pass")
    def test_with_ask_query_false(self) -> None:
        query = "ASK WHERE { <urn://doesnt/exist> ?p ?o }"
        result = self.anzo_client.query_graphmart(
            self.graphmart, query
        )

        self.assertEqual(
            result.as_table_results().as_list(), ["false"]
        )

    def test_malformed_graphmart_query_with_file(self) -> None:
        self.assertRaises(
            RuntimeError, self.anzo_client.query_graphmart, self.graphmart,
            query_file=self.malformed_query_file
        )

    def test_bad_graphmart_query_with_file(self) -> None:
        self.assertRaises(
            RuntimeError, self.anzo_client.query_graphmart,
            self.graphmart, query_file="abcqwerty.qwerty"
        )

    def test_malformed_graphmart_query(self) -> None:
        bad_query = "SE"
        self.assertRaises(
            RuntimeError, self.anzo_client.query_graphmart,
            self.graphmart, query_string=bad_query
        )

    def test_empty_graphmart_query_string(self) -> None:
        self.assertRaises(
            ValueError, self.anzo_client.query_graphmart,
            self.graphmart, query_string=""
        )

    def test_empty_graphmart(self) -> None:
        self.assertRaises(
            ValueError, self.anzo_client.query_graphmart,
            "", query_string=self.select_query
        )

    def test_graphmart_with_no_query(self) -> None:
        self.assertRaises(
            ValueError, self.anzo_client.query_graphmart, self.graphmart
        )

    def test_bad_graphmart_in_graphmart_query(self) -> None:
        bad_graphmart = "qwerty"
        self.assertRaises(
            RuntimeError, self.anzo_client.query_graphmart,
            bad_graphmart, self.select_query_file
        )

    def test_basic_query(self) -> None:
        result = self.anzo_client.query_graphmart(
            self.graphmart,
            query_string=self.select_query
        )

        self.assertEqual(
            result.as_table_results().as_list(), self.select_query_results
        )

    def test_basic_construct_query(self) -> None:
        result = self.anzo_client.query_graphmart(
            self.graphmart, self.construct_query
        )

        self.assertEqual(
            result.as_quad_store(), self.construct_query_results
        )

    def test_construct_query_with_no_results(self) -> None:
        query = "CONSTRUCT { ?s a <urn://type> } WHERE { ?s a <urn://not/a/type> } LIMIT 1"  # noqa
        result = self.anzo_client.query_graphmart(
            self.graphmart, query
        )

        self.assertEqual(
            result.as_quad_store(), QuadStore()
        )

    def test_with_first_layer_specified(self) -> None:
        result = self.anzo_client.query_graphmart(
            self.graphmart,
            query_string=self.select_query,
            data_layers=[self.layer_one_uri]
        )

        self.assertEqual(
            result.as_table_results().as_list(),
            self.select_query_results_first_layer
        )

    def test_with_first_second_specified(self) -> None:
        result = self.anzo_client.query_graphmart(
            self.graphmart,
            query_string=self.select_query,
            data_layers=[self.layer_two_uri]
        )

        self.assertEqual(
            result.as_table_results().as_list(),
            self.select_query_results_second_layer
        )

    def test_with_both_layers_specified(self) -> None:
        result = self.anzo_client.query_graphmart(
            self.graphmart,
            query_string=self.select_query,
            data_layers=[self.layer_one_uri, self.layer_two_uri]
        )

        self.assertEqual(
            result.as_table_results().as_list(), self.select_query_results
        )

    def test_with_cache_skipped(self) -> None:
        try:
            self.anzo_client.query_graphmart(self.graphmart,
                                             query_string=self.select_query,
                                             skip_cache=True)
        except RuntimeError:
            self.fail("Cache Skipping Not Implemented")

    def test_timeout(self) -> None:
        ac = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT,
            timeout_seconds=0.00001
        )

        self.assertRaises(
            TimeoutError, ac.query_graphmart,
            self.graphmart, query_string=self.select_query
        )
