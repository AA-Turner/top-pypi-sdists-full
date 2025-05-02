import unittest
from pyanzo import AnzoClient, QuadStore, Quad

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestAnzoClientUpdateJournal(unittest.TestCase):
    graph_uri = "urn://graph1"

    wipe_graph_query = """
        DELETE { GRAPH ?g { ?s ?p ?o } }
        WHERE { GRAPH ?g { ?s ?p ?o } FILTER(?g=<{GRAPH}>) }
    """.replace("{GRAPH}", graph_uri)


    seed_graph_query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        INSERT DATA {
            GRAPH <{GRAPH}> {
                <urn://sub> <urn://pred> <urn://obj1> .
                <urn://sub> <urn://pred> <urn://obj2> .
            }
        }
    """.replace("{GRAPH}", graph_uri)  # noqa

    insert_delete_query_with_graph = """
        DELETE {
            graph ?g {
                <urn://sub> <urn://pred> ?o .
            }
        }
        INSERT {
            graph ?g {
                <urn://sub> <urn://pred> <urn://obj3>
            }
        }
        WHERE {
            graph ?g {
                <urn://sub> <urn://pred> ?o .
                FILTER(?o = <urn://obj2>)
            }
        }
    """

    insert_delete_query_without_graph = """
        DELETE {
            graph <{GRAPH}> {
                <urn://sub> <urn://pred> ?o .
            }
        }
        INSERT {
            graph <{GRAPH}> {
                <urn://sub> <urn://pred> <urn://obj3>
            }
        }
        WHERE {
            <urn://sub> <urn://pred> ?o .
            FILTER(?o = <urn://obj2>)
        }
    """.replace("{GRAPH}", graph_uri)

    insert_without_insert_graph = """
        DELETE {
            graph <{GRAPH}> {
                <urn://sub> <urn://pred> ?o .
            }
        }
        INSERT {
            <urn://sub> <urn://pred> <urn://obj3>
        }
        WHERE {
            <urn://sub> <urn://pred> ?o .
            FILTER(?o = <urn://obj2>)
        }
    """.replace("{GRAPH}", graph_uri)

    insert_without_delete_graph = """
        DELETE {
            <urn://sub> <urn://pred> ?o .
        }
        INSERT {
            graph <{GRAPH}> {
                <urn://sub> <urn://pred> <urn://obj3>
            }
        }
        WHERE {
            <urn://sub> <urn://pred> ?o .
            FILTER(?o = <urn://obj2>)
        }
    """.replace("{GRAPH}", graph_uri)

    quad1 = Quad("urn://sub", "urn://pred", "urn://obj1", graph_uri)
    quad2 = Quad("urn://sub", "urn://pred", "urn://obj2", graph_uri)
    quad3 = Quad("urn://sub", "urn://pred", "urn://obj3", graph_uri)

    quadstore12 = QuadStore({quad1, quad2})  # contains quads 1 and 2
    quadstore13 = QuadStore({quad1, quad3})  # contains quads 1 and 3

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def wipe_graph(self) -> None:
        self.anzo_client.update_journal(self.wipe_graph_query)

    def seed_graph(self) -> None:
        self.wipe_graph()
        self.anzo_client.update_journal(self.seed_graph_query)

        graph = self.anzo_client.get(self.graph_uri).filter(
            graph=self.graph_uri
        )
        self.assertEqual(graph, self.quadstore12)

    def test_insert_data(self) -> None:
        self.wipe_graph()
        self.anzo_client.update_journal(self.seed_graph_query)
        quadstore = self.anzo_client.get(self.graph_uri).filter(
            graph=self.graph_uri
        )
        self.assertEqual(quadstore, self.quadstore12)

    def test_insert_delete_with_graph(self) -> None:
        self.seed_graph()
        self.anzo_client.update_journal(self.insert_delete_query_with_graph)
        graph = self.anzo_client.get(self.graph_uri).filter(
            graph=self.graph_uri
        )
        self.assertEqual(graph, self.quadstore13)

    def test_insert_delete_without_graph(self) -> None:
        self.seed_graph()
        self.anzo_client.update_journal(self.insert_delete_query_without_graph)
        graph = self.anzo_client.get(self.graph_uri).filter(
            graph=self.graph_uri
            )
        self.assertEqual(graph, self.quadstore13)

    def test_insert_without_insert_graph(self) -> None:
        self.seed_graph()
        self.assertRaises(
            RuntimeError,
            self.anzo_client.update_journal,
            self.insert_without_insert_graph
        )

    def test_insert_without_delete_graph(self) -> None:
        self.seed_graph()
        self.assertRaises(
            RuntimeError,
            self.anzo_client.update_journal,
            self.insert_without_delete_graph
        )

