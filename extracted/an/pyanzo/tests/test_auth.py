# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
from pyanzo import AnzoClient, AnzoRequestBuilder
import requests

from .test_common import (
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
    GRAPHMART,
)

AUTH = "AUTH_TOKEN"


class TestAuthenticationClient(unittest.TestCase):
    # A simple select query used for testing core functionality in the tests
    select_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    select_query_results = [
        ["Boston"],
        ["Cambridge"],
        ["Medford"],
        ["Somerville"],
        ["Watertown"],
    ]

    def test_client_with_auth(self) -> None:
        url = f"https://{DOMAIN}:{PORT}/anzo_authenticate?client_name=AnzoFormClient"  # noqa

        session = requests.Session()
        data = {
            "anzo_username": USERNAME,
            "anzo_password": PASSWORD,
        }

        session.post(url, verify=False, data=data)
        half_of_token = session.cookies.get_dict()['BAYEUX_BROWSER']
        auth_token = f"BAYEUX_BROWSER={half_of_token}"

        anzo_client = AnzoClient(DOMAIN, PORT, auth_token=auth_token)

        res = anzo_client.query_graphmart(GRAPHMART, self.select_query)
        print(res.as_table_results().as_list())
        self.assertEqual(
            res.as_table_results().as_list(), self.select_query_results
        )

    def test_client_no_auth(self) -> None:
        self.assertRaises(ValueError, AnzoClient, DOMAIN, PORT)

    def test_client_username_no_password(self) -> None:
        self.assertRaises(ValueError,
                          AnzoClient,
                          DOMAIN,
                          PORT,
                          username=USERNAME)

    def test_client_password_no_username(self) -> None:
        self.assertRaises(ValueError,
                          AnzoClient,
                          DOMAIN,
                          PORT,
                          password=PASSWORD)

    def test_client_username_password_and_auth_token(self) -> None:
        self.assertRaises(ValueError,
                          AnzoClient,
                          DOMAIN,
                          PORT,
                          username=USERNAME,
                          password=PASSWORD,
                          auth_token=AUTH)


class TestAuthenticationErrorsRequestBuilder(unittest.TestCase):

    arb = AnzoRequestBuilder()

    def test_overloaded_builder(self) -> None:
        self.assertRaises(ValueError,
                          self.arb.with_auth,
                          USERNAME,
                          PASSWORD,
                          AUTH)

    def test_builder_username_no_password(self) -> None:
        self.assertRaises(ValueError, self.arb.with_auth, USERNAME, "", "")

    def test_builder_password_no_username(self) -> None:
        self.assertRaises(ValueError, self.arb.with_auth, "", PASSWORD, "")

    def test_builder_no_auth(self) -> None:
        self.assertRaises(ValueError, self.arb.with_auth, "", "", "")
