# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

from pyanzo.quad_store import QuadStore, Quad
import unittest
import datetime
import urllib.parse

from pyanzo import AnzoClient
from pyanzo.lds_manager import LDSManager, DNG_PRED
from pyanzo import uris
from pyanzo.uris import SYSTEM_DATASOURCE_URI

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestLDSManager(unittest.TestCase):
    """
    Test class for LDS manager. On class initialization, an LDS is created
    with a timestampped title and the "quads_to_add" are added to the LDS.
    The class's lds_mgr manages this LDS. All tests should assume that they
    get the managed LDS in this same state, since tearDown() reverts the LDS
    back to this starting state.
    """
    
    # Paramterized values for the tests. This value is overwritten by the
    # values in the decorator

    ng_1_uri = "http://csi.test.com/"
    ng_2_uri = "http://csi.test.com/graph2"
    ng_3_uri = "http://csi.test.com/graph3"

    # Quads to add to LDS
    quads_to_add = QuadStore({
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate3",
             "7",
             ng_2_uri,
             obj_type="literal",
             obj_data_type="http://www.w3.org/2001/XMLSchema#integer"),
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate2",
             "http://csi.test.com/object2",
             ng_1_uri)
    })

    # different quads to add after clearing LDS
    new_quads_to_add = QuadStore({
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate3",
             "8",
             ng_3_uri,
             obj_type="literal",
             obj_data_type="http://www.w3.org/2001/XMLSchema#integer"),
        Quad("http://csi.test.com/subject2",
             "http://csi.test.com/predicate2",
             "http://csi.test.com/object2",
             ng_1_uri)
    })

    @classmethod
    def setUpClass(cls) -> None:
        cls.az_client = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )

        now = datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")
        cls.lds_title = "test LDS %s" % now
        cls.lds_mgr = LDSManager.create_lds(anzo_client=cls.az_client,
                                            title=cls.lds_title,
                                            statements=cls.quads_to_add,
                                            ontologies=["urn://ont"])
        cls.lds_uri = cls.lds_mgr.lds_uri

    @classmethod
    def tearDownClass(cls):
        # remove dataset created for test
        cls.lds_mgr.delete_lds()

    def tearDown(self) -> None:
        # reset back to "normal" state for further tests
        self.lds_mgr.overwrite_lds(self.quads_to_add)

    def test_created(self):
        # dataset was created in set up
        # test that the right artifacts are there

        qs = self.assert_lds_exists()

        # lds should have two NGs
        self.assertEqual(len(qs.filter(predicate=DNG_PRED)), 2)
        onto_pred = uris.NAMESPACE["cs-ld"] + "ontology"
        # lds should have one onto
        self.assertEqual(len(qs.filter(predicate=onto_pred)), 1)
        # lds should have correct title
        title = qs.filter(predicate=uris.NAMESPACE["dc"] + "title",
                          statement_object=self.lds_title)
        self.quadstore_not_empty(title)

        # actual graphs should exist and not be empty
        self.quadstore_not_empty(self.az_client.get(self.ng_1_uri))
        self.quadstore_not_empty(self.az_client.get(self.ng_2_uri))

    def test_clear_add(self):
        self.lds_mgr.clear_lds()
        qs = self.assert_lds_exists()

        # lds should have 0 NGs
        self.assertEqual(len(qs.filter(predicate=DNG_PRED)), 0)

        # actual graphs should not exist/be empty
        self.graph_empty(self.ng_1_uri)
        self.graph_empty(self.ng_2_uri)

        # add data back
        self.lds_mgr.add_to_lds(self.quads_to_add)

        # actual graphs should now exist and not be empty
        self.quadstore_not_empty(self.az_client.get(self.ng_1_uri))
        self.quadstore_not_empty(self.az_client.get(self.ng_2_uri))

    def test_overwrite(self):
        self.lds_mgr.overwrite_lds(self.new_quads_to_add)

        qs = self.assert_lds_exists()

        # lds should have two NGs
        self.assertEqual(len(qs.filter(predicate=DNG_PRED)), 2)

        # ng 1 and 3 should exist and be not empty
        self.quadstore_not_empty(self.az_client.get(self.ng_1_uri))
        self.quadstore_not_empty(self.az_client.get(self.ng_3_uri))

        # ng2 should not exist/be empty
        self.graph_empty(self.ng_2_uri)

    def assert_lds_exists(self) -> QuadStore:
        # first look at cat entry graph
        qs = self.az_client.get(cat_entry_graph(self.lds_uri))
        self.quadstore_not_empty(qs)
        online = qs.filter(predicate=uris.NAMESPACE["cs-ld"] + "online",
                           statement_object="true")
        self.quadstore_not_empty(online)
        title = qs.filter(predicate=uris.NAMESPACE["dc"] + "title",
                          statement_object=self.lds_title)
        self.quadstore_not_empty(title)

        # then look at lds graph itself
        qs = self.az_client.get(self.lds_uri)
        self.quadstore_not_empty(qs)
        return qs

    def quadstore_not_empty(self, quad_store: QuadStore):
        self.assertGreater(len(quad_store), 0)

    def graph_empty(self, graph_uri: str):
        self.assertRaises(RuntimeError, self.az_client.get, graph_uri)


def cat_entry_graph(lds_uri: str,
                    datasource_uri: str = SYSTEM_DATASOURCE_URI) -> str:
    """Utility method to construct the catalog entry URI
    for the given LDS and datasource URIs.

    Args:
        lds_uri: URI of the LDS
        datasource_uri: (optional) URI of the datasource.
            Defaults to the system datasource.

    Returns:
        The catalog entry URI.
    """
    encoded = urllib.parse.quote("[%s]@[%s]" %
                                 (lds_uri, datasource_uri), safe="")
    return "http://openanzo.org/catEntry(%s)" % encoded
