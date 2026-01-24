# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
from pyanzo import AnzoClient, QuadStore, Quad
from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestAnzoClientExecuteSemanticService(unittest.TestCase):
    reload_graphmart_service_uri = "http://cambridgesemantics.com/semanticServices/gqe#reloadGraphmart"  # noqa

    graphmart = GRAPHMART

    reload_graphmart_request = QuadStore({
        Quad("http://openanzo.org/semanticServices/",
             "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
             "http://cambridgesemantics.com/ontologies/Graphmarts#GraphmartRequest",  # noqa
             "http://openanzo.org/semanticServices/"),
        Quad("http://openanzo.org/semanticServices/",
             "http://cambridgesemantics.com/ontologies/Graphmarts#graphmart",
             graphmart,
             "http://openanzo.org/semanticServices/")
    })

    binary_service_uri = "http://openanzo.org/semanticServices/binaryStoreService#getServerConfig"  # noqa
    binary_service_empty_request = QuadStore()

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            DOMAIN, PORT, username=USERNAME, password=PASSWORD)

    def test_simple_semantic_service_endpoint_call(self) -> None:
        result = self.anzo_client.execute_semantic_service(
            self.reload_graphmart_service_uri,
            self.reload_graphmart_request
        )
        named_graph_quads = result.filter(
            graph='http://openanzo.org/semanticServices/'
        )
        self.assertNotEqual(named_graph_quads.quads, set())

    def test_simple_service_call_with_empty_request(self) -> None:
        self.anzo_client.execute_semantic_service(
            self.binary_service_uri,
            self.binary_service_empty_request
        )

    def test_bad_semantic_service_uri(self) -> None:
        bad_service_uri = self.reload_graphmart_service_uri = "this_is_bad"

        self.assertRaises(
            RuntimeError, self.anzo_client.execute_semantic_service,
            bad_service_uri, self.reload_graphmart_request
        )

    def test_empty_semantic_service_uri(self) -> None:
        empty_service_uri = ""

        self.assertRaises(
            RuntimeError, self.anzo_client.execute_semantic_service,
            empty_service_uri, self.reload_graphmart_request
        )

    # TODO:
    def test_unsuccessful_semantic_service_call(self) -> None:
        # (where everything used is legit) -> just the service call _fails_
        # e.g., reloading the gmart fails.
        pass
