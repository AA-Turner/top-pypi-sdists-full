# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
import os
import json
import copy
import parameterized


from pyanzo import (
    AnzoClient,
    AnzoRequestBuilder,
    AnzoRequest,
    Quad,
    QueryResult,
    QuadStore,
    TableResult,
    semantic_type_to_python_object,
)

from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    EMPTY_AUTH_TOKEN,
    USERNAME,
    PASSWORD,
    PATH
)


class TestAnzoClientGetGraph(unittest.TestCase):
    graphmart = GRAPHMART

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(DOMAIN, PORT, USERNAME, PASSWORD)

    # TODO: add a test that checks the output more carefully.
    # These graphs were just so big that I didn"t want to paste
    # the expected values.
    @unittest.skip("Not implemented yet")
    def test_simple_get_graphmart(self) -> None:
        res = self.anzo_client.get_graph(self.graphmart)
        self.assertEqual(res[0]["namedGraphUri"], self.graphmart)


class TestQueryResult(unittest.TestCase):
    """
    TODO: the names of the methods in this need to be updated. They're based
    on querying anzo/graphmarts but anzo/graphmart is never actually queried.
    """

    graphmart = GRAPHMART

    # This is the basis of the query result
    # simple_select_query = """
    # PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>  # noqa
    #
    # SELECT ?city WHERE {
    #     ?s a data:Person ;
    #         data:Person_City ?city .
    # } ORDER BY ?city LIMIT 5"""

    # We construct the result manually to avoid confounding errors
    # TODO: rename based on conventions
    QueryResult_simple_select_query = QueryResult("""{
        "head": {"vars": ["city"]},
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

    # Results
    simple_select_graphmart_query_results_list = [
        ["Boston"], ["Cambridge"], ["Medford"], ["Somerville"], ["Watertown"]
    ]

    simple_select_graphmart_query_results_dict = [
        {"city": "Boston"},
        {"city": "Cambridge"},
        {"city": "Medford"},
        {"city": "Somerville"},
        {"city": "Watertown"}
    ]

    # This is the basis of the query
    # query_with_optional = """
    #     PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>  # noqa
    #
    #     SELECT ?city ?height WHERE {
    #       ?s a data:Person ;
    #            data:Person_Name ?name ;
    #            data:Person_City ?city ;
    #            data:Person_Age ?age .
    #
    #       # person height is not a property and
    #       # will be unbound by design (for testing)
    #       OPTIONAL { ?s  data:Person_Height  ?height }
    #
    #     } ORDER BY ?city LIMIT 5
    #  """

    # We construct the result manually to avoid confounding errors
    QueryResult_query_with_optional = QueryResult("""{
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

    graphmart_query_with_optional_results_list = [
        ["Boston", ""], ["Cambridge", ""], ["Medford", ""],
        ["Somerville", ""], ["Watertown", ""]
    ]

    graphmart_query_with_optional_results_dict = [
        {"city": "Boston", "height": ""},
        {"city": "Cambridge", "height": ""},
        {"city": "Medford", "height": ""},
        {"city": "Somerville", "height": ""},
        {"city": "Watertown", "height": ""},
    ]

    # Templated verions of the queries to allow for different
    # SELECT vars and LIMITs
    simple_select_query_template = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT {} WHERE {{
            ?s a data:Person ;
                data:Person_City ?city .
        }} ORDER BY ?city LIMIT {}"""  # noqa

    query_with_ints = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?name ?age WHERE {{
            ?s a data:Person ;
                data:Person_Name ?name ;
                data:Person_Age ?age2 .
                BIND(DOUBLE(?age2) as ?age)
        }} ORDER BY ?age
    """  # noqa

    record_dicts_with_ints = [
        {'name': 'Alice', 'age': 30.0},
        {'name': 'Bob', 'age': 33.0},
        {'name': 'Carlos', 'age': 50.0},
        {'name': 'Diego', 'age': 60.0},
        {'name': 'Eve', 'age': 70.0}
    ]

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(domain=DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)

    # The test docstrings are convenient when looking at the code, but
    # they make the verbose testing view look cluttered. This function
    # removes comments/descriptions from the verbose test view.
    def shortDescription(self) -> None:
        return None

    @parameterized.parameterized.expand([
        ("SELECT_CITY", QueryResult_simple_select_query),
        ("SELECT_CITY_HEIGHT", QueryResult_query_with_optional),
    ])
    def test_graphmart_query_sublist_equal_length(self,
                                                  test_name: str,
                                                  query_result: QueryResult
                                                  ) -> None:
        """Test that each sublist/solution is the same length"""

        result = query_result.as_table_results()

        self.assertTrue(
            all(
                len(solution) == len(result.as_list()[-1])
                for solution in result.as_list()
            )
        )

    @parameterized.parameterized.expand([
        ("SELECT_CITY", QueryResult_simple_select_query),
        ("SELECT_CITY_HEIGHT", QueryResult_query_with_optional),
    ])
    def test_graphmart_query_dict_values_equal_length(self,
                                                      test_name: str,
                                                      query_result: QueryResult
                                                      ) -> None:
        """Test that each sublist/solution is the same length"""

        result = query_result.as_table_results()

        self.assertTrue(
            all(len(solution.values()) == len(result.as_record_dictionaries()[-1].values())  # noqa
                for solution in result.as_record_dictionaries())
        )

    # This will create two versions of this test
    #   1) test_graphmart_query_result_length_0_LIST
    #   2) test_graphmart_query_result_length_1_DICT
    # The name comes from the first value of each tuple
    # The values of the tuple are passed to the test as parameters
    # ("LIST", QueryResult.as_list) becomes
    #   test_graphmart_query_result_length(self, "LIST", QueryResult.as_list)
    @parameterized.parameterized.expand([
        ("LIST",
         TableResult.as_list,
         simple_select_graphmart_query_results_list),
        ("DICT",
         TableResult.as_record_dictionaries,
         simple_select_graphmart_query_results_dict),

        # Need to convert iter to list in order to compare results
        ("LIST_ITER", lambda x: list(TableResult.as_list_iter(x)),
            simple_select_graphmart_query_results_list)
    ])
    def test_simple_graphmart_query(self,
                                    test_name,
                                    query_result_method,
                                    expected) -> None:
        """Test a simple query returns the correct results for each
        query result method
        """
        result = self.QueryResult_simple_select_query.as_table_results()
        self.assertEqual(query_result_method(result), expected)

    @parameterized.parameterized.expand([
        ("LIST",
         TableResult.as_list,
         graphmart_query_with_optional_results_list),
        ("DICT",
         TableResult.as_record_dictionaries,
         graphmart_query_with_optional_results_dict),

        # Need to convert iter to list in order to compare results
        ("LIST_ITER", lambda x: list(TableResult.as_list_iter(x)),
            graphmart_query_with_optional_results_list)
    ])
    def test_graphmart_optional_query(self,
                                      test_name,
                                      query_result_method,
                                      expected) -> None:
        """Test a query that contains optional bindings, unbound values should
           be marked as empty string"""
        result = self.QueryResult_query_with_optional.as_table_results()

        self.assertEqual(query_result_method(result), expected)

    def test_simple_graphmart_query_internal_iter(self) -> None:
        """Test __iter__ of query result, the query result itself
           should be iterable"""
        result = self.QueryResult_simple_select_query.as_table_results()
        self.assertTrue(
            all(self.simple_select_graphmart_query_results_list[i] == solution
                for i, solution in enumerate(result))
        )

        self.assertEqual(
            list(result),
            self.simple_select_graphmart_query_results_list,
        )

    def test_simple_construct_query(self) -> None:
        """Test to ensure that simple construct queries do not error."""
        anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT)
        query = """
        PREFIX pyanzo:<http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>
        CONSTRUCT {
            ?s a pyanzo:Person  .
        }
        WHERE {
        ?s a pyanzo:Person .
        }""" # noqa
        graphmart = GRAPHMART
        expectation_uris = set(
            ['http://csi.com/Person/0c391c0f-340d-4f08-9fa6-13a1793c35cb',
             'http://csi.com/Person/a153b0aa-5583-40ff-8710-f94c8a25df3d',
             'http://csi.com/Person/c2ee95a3-d5b1-40d8-8243-9c7d541853f7',
             'http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711',
             'http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0'
             ])
        results = anzo_client.query_graphmart(graphmart, query_string=query)
        quad_store = results.as_quad_store()
        person_uris = set()
        for quad in quad_store:
            person_uris.add(quad.sub)
        self.assertEqual(expectation_uris, person_uris)

    def test_record_dicts(self) -> None:
        res = self.anzo_client.query_graphmart(
            self.graphmart,
            self.query_with_ints
        )

        rd = res.as_table_results().as_record_dictionaries()
        self.assertEqual(rd, self.record_dicts_with_ints)

class TestAnzoRequestBuilder(unittest.TestCase):
    domain = DOMAIN
    path = PATH
    auth_token = EMPTY_AUTH_TOKEN
    username = USERNAME
    password = PASSWORD
    port = PORT
    graphmart = GRAPHMART

    query_string = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
    query_file = simple_select_query_file = os.path.join(
        "tests", "test_assets", "simple_graphmart_query.rq"
    )

    def test_missing_url_postfix(self) -> None:
        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        self.assertRaises(ValueError, arb.build)

    def test_missing_url(self) -> None:
        arb = AnzoRequestBuilder()
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_query_string(self.query_string)
        self.assertRaises(ValueError, arb.build)

    def test_missing_auth(self) -> None:
        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_query_string(self.query_string)
        self.assertRaises(ValueError, arb.build)


class TestAnzoRequest(unittest.TestCase):
    domain = DOMAIN 
    port = PORT
    auth_token = EMPTY_AUTH_TOKEN
    username = USERNAME
    password = PASSWORD
    graphmart = GRAPHMART
    timeout_seconds = 120  # two minutes

    query_string = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
    query_file = simple_select_query_file = os.path.join(
        "tests", "test_assets", "simple_graphmart_query.rq"
    )

    url = f"https://{domain}:{port}/sparql"
    payload = {
        "query": query_string,
        "format": "json"
    }
    headers = {}

    query_json_results = {
        "head": {
            "vars": ["p", "s", "o"]
        },
        "results": {
            "bindings": []
        }
    }

    def test_good_request(self) -> None:
        req = AnzoRequest(
            self.url,
            self.auth_token,
            self.username,
            self.password,
            self.headers,
            self.payload,
            self.timeout_seconds)
        res = req.execute_request()
        self.assertEqual(json.loads(res), self.query_json_results)

    def test_bad_host(self) -> None:
        bad_host = self.domain + self.domain
        bad_url = f"http://{bad_host}:{self.port}/sparql"
        req = AnzoRequest(bad_url,
                          self.username,
                          self.password,
                          self.auth_token,
                          self.headers,
                          self.payload,
                          self.timeout_seconds)
        self.assertRaises(RuntimeError, req.execute_request)

    def test_bad_port(self) -> None:
        bad_port = "8088"
        self.assertNotEqual(self.port, bad_port)

        bad_url = f"http://{self.url}:{bad_port}/sparql"
        req = AnzoRequest(bad_url,
                          self.username,
                          self.password,
                          self.auth_token,
                          self.headers,
                          self.payload,
                          self.timeout_seconds)
        self.assertRaises(RuntimeError, req.execute_request)

    def test_bad_username(self) -> None:
        bad_username = self.username + self.username

        req = AnzoRequest(self.url,
                          bad_username,
                          self.password,
                          self.auth_token,
                          self.headers,
                          self.payload,
                          self.timeout_seconds)
        self.assertRaises(RuntimeError, req.execute_request)

    def test_bad_password(self) -> None:
        bad_password = self.password + self.password

        req = AnzoRequest(self.url,
                          self.username,
                          bad_password,
                          self.auth_token,
                          self.headers,
                          self.payload,
                          self.timeout_seconds)
        self.assertRaises(RuntimeError, req.execute_request)


class TestSemanticTypeToPythonObject(unittest.TestCase):
    def test_unknown_type(self) -> None:
        val = "test"
        res = semantic_type_to_python_object(
            val, "http://www.w3.org/2001/XMLSchema#unknowntype"
        )
        self.assertEqual(val, res)

    def test_string(self) -> None:
        val = "test"
        res = semantic_type_to_python_object(val, "")
        self.assertEqual(val, res)

    def test_int(self) -> None:
        five_string = "5"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#int"
        )
        self.assertEqual(five, 5)

    def test_long(self) -> None:
        five_string = "5"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#long"
        )
        self.assertEqual(five, 5)

    def test_integer(self) -> None:
        five_string = "5"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#integer"
        )
        self.assertEqual(five, 5)

    def test_float(self) -> None:
        five_string = "5.0"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#float"
        )
        self.assertEqual(five, 5.0)

    def test_double(self) -> None:
        five_string = "5.0"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#double"
        )
        self.assertEqual(five, 5.0)

    def test_decimal(self) -> None:
        five_string = "5.0"
        five = semantic_type_to_python_object(
            five_string, "http://www.w3.org/2001/XMLSchema#decimal"
        )
        self.assertEqual(five, 5.0)

