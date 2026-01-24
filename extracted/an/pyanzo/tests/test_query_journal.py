# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
import os
from pyanzo import AnzoClient, QuadStore, Quad

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestAnzoClientQueryJournalBase(unittest.TestCase):
    journal_query1 = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        SELECT ?title
        WHERE {
            GRAPH ?g {
                ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                    dc:title ?title .
            }
            FILTER(?g = <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
        }
    """  # noqa

    journal_query2 = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT ?title
        WHERE {
            GRAPH <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7> {
                ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                    dc:title ?title .
            }
        }
    """  # noqa

    journal_query3 = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT ?title
        WHERE {
            GRAPH ?g {
                ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                    dc:title ?title .
            }
            VALUES (?g) {
                (<http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
            }
        }
    """  # noqa

    journal_query4 = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT ?title
        WHERE {
            ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                dc:title ?title .
            FILTER(?s = <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
        }
    """  # noqa

    journal_queries = [
        journal_query1, journal_query2, journal_query3, journal_query4
    ]

    journal_query_results = [["PyAnzo Graphmart"]]

    journal_query_target_graph_list = [
        "http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7"  # noqa
    ]

    simple_journal_query_file = os.path.join(
        "tests", "test_assets", "simple_journal_query.rq"
    )

    malformed_query_file = os.path.join(
        "tests", "test_assets", "malformed_journal_query.rq"
    )

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def test_journal_query_with_query_string_and_file(self) -> None:
        self.assertRaises(
            ValueError, self.anzo_client.query_journal,
            query_string=self.journal_query1,
            query_file=self.simple_journal_query_file
        )

    def test_journal_query(self) -> None:
        for journal_query in self.journal_queries:
            result = self.anzo_client.query_journal(journal_query)
            self.assertEqual(
                result.as_table_results().as_list(),
                self.journal_query_results
            )

    def test_journal_query_with_graph_specified(self) -> None:
        for journal_query in self.journal_queries:
            result = self.anzo_client.query_journal(
                journal_query,
                named_graphs=self.journal_query_target_graph_list
            )
            self.assertEqual(
                result.as_table_results().as_list(),
                self.journal_query_results
            )

    def test_bad_journal_query(self) -> None:
        query = "SELECT ?title"
        self.assertRaises(RuntimeError, self.anzo_client.query_journal, query)

    def test_simple_journal_query_with_file(self) -> None:
        result = self.anzo_client.query_journal(
            query_file=self.simple_journal_query_file
        )
        self.assertEqual(
            result.as_table_results().as_list(), self.journal_query_results
        )

    def test_journal_query_with_bad_file(self) -> None:
        self.assertRaises(
            RuntimeError, self.anzo_client.query_journal,
            query_file="abc123.123abc"
        )

    def test_malformed_journal_query_with_bad_file(self) -> None:
        self.assertRaises(
            RuntimeError, self.anzo_client.query_journal,
            query_file=self.malformed_query_file
        )


class TestAnzoClientQueryJournalTwoGraphs(unittest.TestCase):
    journal_query_two_graphs = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT ?title
        WHERE {
            GRAPH ?g {
                ?s dc:title ?title .
            }

            VALUES (?g) {
                (<http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
                (<http://csi.com/FileBasedLinkedDataSet/bd05ae950df39757dfbb5a6fbc5c925e>)
            }
        }
        ORDER BY ?title
    """  # noqa

    journal_query_two_graphs_results = [["PyAnzo Dataset"], ["PyAnzo Graphmart"]]  # noqa

    journal_query_two_graphs_list = [
        "http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7",  # noqa
        "http://csi.com/FileBasedLinkedDataSet/bd05ae950df39757dfbb5a6fbc5c925e"  # noqa
    ]

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def test_with_default_graphs(self) -> None:
        result = self.anzo_client.query_journal(
            query_string=self.journal_query_two_graphs
        )
        self.assertEqual(
            result.as_table_results().as_list(),
            self.journal_query_two_graphs_results
        )

    def test_with_two_graphs_specified(self) -> None:
        result = self.anzo_client.query_journal(
            query_string=self.journal_query_two_graphs,
            named_graphs=self.journal_query_two_graphs_list
        )
        self.assertEqual(
            result.as_table_results().as_list(),
            self.journal_query_two_graphs_results
        )

    def test_with_one_graph_specified(self) -> None:
        result = self.anzo_client.query_journal(
            query_string=self.journal_query_two_graphs,
            named_graphs=[self.journal_query_two_graphs_list[0]]
        )
        self.assertNotEqual(
            result.as_table_results().as_list(),
            self.journal_query_two_graphs_results
        )


class TestAnzoClientQueryJournalConstruct(unittest.TestCase):
    query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        CONSTRUCT {
            GRAPH ?g {
                ?s <urn://predicate> ?title .
            }
        }
        WHERE {
            GRAPH ?g {
                ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                    dc:title ?title .
            }
            FILTER(?g = <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
        }
    """  # noqa

    set_of_quads = {
        Quad(
            sub='http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7',  # noqa
            pred='urn://predicate',
            obj='PyAnzo Graphmart',
            graph='http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7',  # noqa
            sub_type="uri",
            obj_type="literal",
        )
    }

    expected_quad_store = QuadStore(set_of_quads)

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def test_construct_query(self) -> None:
        result = self.anzo_client.query_journal(query_string=self.query)
        self.assertEqual(result.as_quad_store(), self.expected_quad_store)
