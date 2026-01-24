# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest

from pyanzo import AnzoClient
from pyanzo.graphmart_manager import GraphmartManager

from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
    ANZOGRAPH_DS
)


class TestGraphmartManager(unittest.TestCase):
    # Paramterized values for the tests. This value is overwritten by the
    # values in the decorator

    graphmart = GRAPHMART
    anzograph_ds = ANZOGRAPH_DS

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

    layer_one_uri = "http://cambridgesemantics.com/Layer/dd29f470d8d44dad8e6cf9ce3b6322fd"  # noqa
    layer_two_uri = "http://cambridgesemantics.com/Layer/d2bb3f418d7942d8a85fdedad608ccb3"  # noqa

    load_step = "http://cambridgesemantics.com/LoadDataStep/1347736407234bdc84f7b04991c70541"  # noqa
    query_step = "http://cambridgesemantics.com/QueryStep/390e0618d5d04dd5ac57cbf26947f397"  # noqa

    @classmethod
    def setUpClass(cls) -> None:
        ac = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )
        gm = GraphmartManager(ac, cls.graphmart)

        # Make sure the graphmart is started in the right state
        gm.enable_layers()
        gm.activate()
        gm.reload()

    @classmethod
    def tearDownClass(cls) -> None:
        ac = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )
        gm = GraphmartManager(ac, cls.graphmart)

        # Make sure the graphmart is left in the right state
        gm.enable_layers()
        gm.reload()
        gm.activate()

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )

        self.graphmart_manager = GraphmartManager(
            self.anzo_client, self.graphmart
        )

    def test_query(self) -> None:
        result = self.graphmart_manager.query(
            query_string=self.select_query
        )

        self.assertEqual(
            result.as_table_results().as_list(), self.select_query_results
        )

    def test_enable_disable_layers(self) -> None:
        # First, disenable the first layer, and confirm things look good
        self.graphmart_manager.disable_layers([self.layer_one_uri])
        self.graphmart_manager.reload()
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

        self.assertFalse(
            self.graphmart_manager.are_layers_online([self.layer_one_uri])
        )

        self.assertTrue(
            self.graphmart_manager.are_layers_online([self.layer_two_uri])
        )

        result = self.graphmart_manager.query(self.select_query)
        self.assertEqual(
            result.as_table_results().as_list(),
            self.select_query_results_second_layer
        )

        # Second, re-enable, and confirm things look good
        self.graphmart_manager.enable_layers([self.layer_one_uri])
        self.graphmart_manager.reload()
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

        self.assertTrue(
            self.graphmart_manager.are_layers_online([self.layer_one_uri])
        )

        self.assertTrue(
            self.graphmart_manager.are_layers_online([self.layer_two_uri])
        )
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

        result = self.graphmart_manager.query(self.select_query)
        self.assertEqual(
            result.as_table_results().as_list(), self.select_query_results
        )

    def test_enable_disable_steps(self) -> None:
        load_steps = [self.load_step]
        query_steps = [self.query_step]

        self.graphmart_manager.enable_steps(query_steps)
        self.graphmart_manager.refresh()
        self.assertTrue(self.graphmart_manager.are_steps_online(query_steps))
        self.assertTrue(self.graphmart_manager.are_steps_online(load_steps))

        self.graphmart_manager.disable_steps(query_steps)
        self.graphmart_manager.refresh()
        self.assertFalse(self.graphmart_manager.are_steps_online(query_steps))
        self.assertTrue(self.graphmart_manager.are_steps_online(load_steps))

        self.graphmart_manager.enable_steps(query_steps)
        self.graphmart_manager.refresh()
        self.assertTrue(self.graphmart_manager.are_steps_online(query_steps))
        self.assertTrue(self.graphmart_manager.are_steps_online(load_steps))

    def test_reload(self) -> None:
        self.graphmart_manager.reload()

    def test_refresh(self) -> None:
        self.graphmart_manager.reload()

    def test_are_layers_online_with_args(self) -> None:
        self.assertTrue(self.graphmart_manager.are_layers_online(
            [self.layer_one_uri, self.layer_two_uri]
        ))

    def test_are_layers_online_without_args(self) -> None:
        self.assertTrue(self.graphmart_manager.are_layers_online())

    def test_get_layers(self) -> None:
        self.assertEqual(
            sorted(self.graphmart_manager.get_layers()),
            sorted([self.layer_one_uri, self.layer_two_uri])
        )

    def test_are_steps_online_with_args(self) -> None:
        self.assertTrue(self.graphmart_manager.are_steps_online(
            [self.load_step, self.query_step]
        ))

    def test_are_steps_online_without_args(self) -> None:
        self.assertTrue(self.graphmart_manager.are_steps_online())

    def test_get_steps(self) -> None:
        self.assertEqual(
            sorted(self.graphmart_manager.get_steps()),
            sorted([self.load_step, self.query_step])
        )

    def test_is_online(self) -> None:
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

    def test_deactivate_and_activate_without_azg_uri(self) -> None:
        self.assertTrue(self.graphmart_manager.are_layers_online())
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

        self.graphmart_manager.deactivate()

        self.assertFalse(self.graphmart_manager.is_graphmart_online())
        self.assertFalse(self.graphmart_manager.are_layers_online())

        self.graphmart_manager.activate()

        self.assertTrue(self.graphmart_manager.are_layers_online())
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

    def test_deactivate_and_activate_with_azg_uri(self) -> None:
        self.assertTrue(self.graphmart_manager.are_layers_online())
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

        self.graphmart_manager.deactivate()

        self.assertFalse(self.graphmart_manager.is_graphmart_online())
        self.assertFalse(self.graphmart_manager.are_layers_online())

        self.graphmart_manager.activate(self.anzograph_ds)

        self.assertTrue(self.graphmart_manager.are_layers_online())
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

    def test_activating_twice(self) -> None:
        self.graphmart_manager.activate()
        self.graphmart_manager.activate()
        self.assertTrue(self.graphmart_manager.is_graphmart_online())

    def test_deactivating_twice(self) -> None:
        self.graphmart_manager.deactivate()
        self.graphmart_manager.deactivate()
        self.assertFalse(self.graphmart_manager.is_graphmart_online())

        # put graphmart back in its normal state
        self.graphmart_manager.activate()
        self.assertTrue(self.graphmart_manager.is_graphmart_online())
