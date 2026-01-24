# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest

from pyanzo import (
    AnzoClient, ALL_NAMED_GRAPHS_URI
)

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestAnzoClientQueryLds(unittest.TestCase):
    ontology_lds_uri = "http://openanzo.org/catEntry(%5Bhttp%3A%2F%2Fcambridgesemantics.com%2Fregistries%2FOntologies%5D%40%5Bhttp%3A%2F%2Fopenanzo.org%2Fdatasource%2FsystemDatasource%5D)"  # noqa

    pyanzo_ontology_uri = "http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource"  # noqa
    resources_in_pyanzo_ontology = [
        ["http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person"],  # noqa
        ["http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Age"],  # noqa
        ["http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City"],  # noqa
        ["http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Name"]  # noqa
     ]

    pyanzo_ont_query_string = f"""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT distinct ?resource WHERE {{
            GRAPH <{pyanzo_ontology_uri}> {{
                ?resource a ?type .
                VALUES (?type) {{
                    (owl:Class)
                    (owl:DatatypeProperty)
                    (owl:FunctionalProperty)
                }}
            }}
        }}
        ORDER BY ?resource
        LIMIT 20
    """  # noqa

    # This query is designed to make sure that when (a) no named graphs are
    # specifed and (b) there's no GRAPH ?g part of the where then the query
    # query will still reach the ontology graphs.
    pyanzo_ont_query_string_without_graph2 = f"""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT distinct ?resource WHERE {{
            ?resource a owl:Class .
            ?resource rdfs:label "Person" .
        }}
        ORDER BY ?resource
        LIMIT 20
    """  # noqa

    person_resources = [
        ['http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person'],
        ['http://s.opencalais.com/1/type/em/e/Person'],
        ['http://xmlns.com/foaf/0.1/Person']
    ]


    system_table_lds = "http://openanzo.org/catEntry(%5Bhttp%3A%2F%2Fcambridgesemantics.com%2Fontologies%2F2009%2F05%2FLinkedData%23AnzoXray%5D%40%5Bhttp%3A%2F%2Fcambridgesemantics.com%2Fdatasource%2FSystemTables%5D)"  # noqa

    gmart_query = """
        PREFIX gms: <http://cambridgesemantics.com/ontologies/GraphmartStatus#>
        SELECT ?status WHERE {
            ?obj gms:status ?status .
            FILTER(?obj=<http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
        }
        LIMIT 100
    """  # noqa

    gmart_query_res = [
        ['http://openanzo.org/ontologies/2008/07/System#Online']
    ]

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def test_bad_query(self) -> None:
        query_string = "SELECT * WHER { ?s ?p ?o . } LIMIT 10"

        self.assertRaises(
            RuntimeError, self.anzo_client.query_lds,
            self.ontology_lds_uri, query_string=query_string
        )

    def test_empty_query(self) -> None:
        query_string = ""
        self.assertRaises(
            ValueError, self.anzo_client.query_lds,
            self.ontology_lds_uri, query_string=query_string
        )

    def test_bad_lds_uri(self) -> None:
        # make bad by dropping the last two characters of the
        # ontology lds uri
        bad_lds_uri = self.ontology_lds_uri[:-2]

        self.assertRaises(
            RuntimeError, self.anzo_client.query_lds,
            bad_lds_uri, query_string=self.pyanzo_ont_query_string
        )

    def test_empty_lds_uri(self) -> None:
        empty_lds_uri = ""

        self.assertRaises(
            RuntimeError, self.anzo_client.query_lds,
            empty_lds_uri, query_string=self.pyanzo_ont_query_string
        )

    def test_simple_lds_query(self) -> None:
        result = self.anzo_client.query_lds(
            self.ontology_lds_uri, query_string=self.pyanzo_ont_query_string
        )

        self.assertEqual(result.as_table_results().as_list(),
                         self.resources_in_pyanzo_ontology)

    def test_query_without_named_graph_specified(self) -> None:
        # test query is designed to make sure that when (a) no named graphs are
        # specifed in the query and (b) there's no GRAPH ?g part of the where
        # then the query query will still reach the ontology graphs.

        result = self.anzo_client.query_lds(
            self.ontology_lds_uri,
            query_string=self.pyanzo_ont_query_string_without_graph2
        )

        self.assertEqual(
            result.as_table_results().as_list(), self.person_resources
        )

    def test_query_system_tables_with_all_graphs(self) -> None:
        # When querying the system tables, all named graphs should be included
        res = self.anzo_client.query_lds(
            self.system_table_lds, self.gmart_query,
            named_graphs=[ALL_NAMED_GRAPHS_URI]
        )
        res_list = res.as_table_results().as_list()
        self.assertEqual(res_list, self.gmart_query_res)
