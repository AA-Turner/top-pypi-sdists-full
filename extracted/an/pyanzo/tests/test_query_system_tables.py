# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest

from pyanzo import (
    AnzoClient,
)

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
    GRAPHMART
)


class TestAnzoClientQuerySystemTables(unittest.TestCase):

    query_string = f"""
        PREFIX gm: <http://cambridgesemantics.com/ontologies/GraphmartStatus#>

        SELECT distinct * WHERE {{
            ?graphmart a gm:GraphmartStatus ;
                gm:totalStatements ?statements ;
            .
            FILTER(?graphmart = <{GRAPHMART}>)
        }}
        LIMIT 10
    """  # noqa


    construct_query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX system: <http://openanzo.org/ontologies/2008/07/System#>

        CONSTRUCT {
            <urn://one> dc:title ?type
        } WHERE {
           ?s a ?type .
           #FILTER(?type = system:QueryExecution)
        }
        LIMIT 10
    """  # noqa

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    def test_select(self) -> None:
        result = self.anzo_client.query_system_tables(
            query_string=self.query_string
        )

        result_table = result.as_table_results().as_list()

        self.assertEqual(len(result_table), 1)

        only_result = result_table[0]

        self.assertEqual(only_result[0], GRAPHMART)
        self.assertTrue(0 < int(only_result[1]))

    @unittest.skip("Requires Anzo improvement to pass")
    def test_construct(self) -> None:
        result = self.anzo_client.query_system_tables(
            query_string=self.construct_query
        )

        qs = result.as_quad_store()
        self.assertTrue(len(qs) == 10)
