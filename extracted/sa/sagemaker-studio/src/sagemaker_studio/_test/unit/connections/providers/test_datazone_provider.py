"""The DataZone connection provider: the service's inline DataZone calls, behind the provider seam."""

import unittest
from unittest.mock import Mock

from botocore.exceptions import ClientError

from sagemaker_studio.connections.providers import (
    ConnectionAccessError,
    ConnectionNotFoundError,
    ConnectionProvider,
)
from sagemaker_studio.connections.providers.datazone import DataZoneConnectionProvider


def _client_error(code, operation, message="denied"):
    return ClientError(
        error_response={
            "Error": {"Code": code, "Message": message},
            "ResponseMetadata": {"RequestId": "req-1"},
        },
        operation_name=operation,
    )


class DataZoneConnectionProviderTest(unittest.TestCase):
    def setUp(self):
        self.datazone = Mock()
        self.provider = DataZoneConnectionProvider(self.datazone, "dzd-1", "proj-1")

    def test_it_is_a_connection_provider_that_keeps_vended_credentials(self):
        self.assertIsInstance(self.provider, ConnectionProvider)
        self.assertEqual(
            (self.provider.name, self.provider.domain_id, self.provider.project_id),
            ("datazone", "dzd-1", "proj-1"),
        )
        self.assertIs(self.provider.refreshes_credentials, False)
        self.assertEqual(
            repr(self.provider), "DataZoneConnectionProvider(domain='dzd-1', project='proj-1')"
        )

    def test_by_id_is_get_connection_with_secret(self):
        self.datazone.get_connection.return_value = {"connectionId": "c1", "name": "raw"}
        self.assertEqual(self.provider.get_connection_by_id("c1")["name"], "raw")
        self.datazone.get_connection.assert_called_once_with(
            domainIdentifier="dzd-1", identifier="c1", withSecret=True
        )

    def test_by_id_can_leave_the_secret_out(self):
        self.datazone.get_connection.return_value = {"connectionId": "c1"}
        self.provider.get_connection_by_id("c1", with_secret=False)
        self.datazone.get_connection.assert_called_once_with(
            domainIdentifier="dzd-1", identifier="c1", withSecret=False
        )

    def test_by_id_re_raises_datazones_client_error_with_code_and_message(self):
        self.datazone.get_connection.side_effect = _client_error(
            "ResourceNotFoundException", "GetConnection", "no such connection"
        )
        with self.assertRaises(ClientError) as cm:
            self.provider.get_connection_by_id("missing")
        self.assertEqual(
            cm.exception.response["Error"],
            {"Code": "ResourceNotFoundException", "Message": "no such connection"},
        )
        self.assertEqual(cm.exception.operation_name, "GetConnection")
        self.assertIsInstance(cm.exception.__cause__, ClientError)

    def test_by_name_lists_by_name_then_fetches_the_first_match_with_secret(self):
        self.datazone.list_connections.return_value = {
            "items": [{"connectionId": "c1", "name": "raw"}, {"connectionId": "c2", "name": "raw"}]
        }
        self.datazone.get_connection.return_value = {"connectionId": "c1", "name": "raw"}
        self.assertEqual(self.provider.get_connection_by_name("raw")["connectionId"], "c1")
        self.datazone.list_connections.assert_called_once_with(
            domainIdentifier="dzd-1", projectIdentifier="proj-1", name="raw"
        )
        self.datazone.get_connection.assert_called_once_with(
            domainIdentifier="dzd-1", identifier="c1", withSecret=True
        )

    def test_by_name_with_no_match_is_not_found(self):
        self.datazone.list_connections.return_value = {"items": []}
        with self.assertRaises(ConnectionNotFoundError) as cm:
            self.provider.get_connection_by_name("nope")
        self.assertEqual(str(cm.exception), "No connection found with name 'nope'")
        self.datazone.get_connection.assert_not_called()

    def test_by_name_refused_fetch_is_an_access_error_naming_the_connection(self):
        self.datazone.list_connections.return_value = {"items": [{"connectionId": "c1"}]}
        self.datazone.get_connection.side_effect = _client_error(
            "AccessDeniedException", "GetConnection"
        )
        with self.assertRaises(ConnectionAccessError) as cm:
            self.provider.get_connection_by_name("raw")
        self.assertIn("Unable to access connection 'raw', ", str(cm.exception))
        self.assertIn("AccessDeniedException", str(cm.exception))

    def test_a_failing_listing_propagates_as_the_client_error_it_is(self):
        self.datazone.list_connections.side_effect = _client_error(
            "ResourceNotFoundException", "ListConnections"
        )
        with self.assertRaises(ClientError):
            self.provider.get_connection_by_name("raw")
        with self.assertRaises(ClientError):
            self.provider.get_connection_by_type("ATHENA")

    def test_by_type_takes_the_first_listed_connection(self):
        self.datazone.list_connections.return_value = {
            "items": [
                {"connectionId": "c1", "name": "a", "type": "ATHENA"},
                {"connectionId": "c2", "name": "default.athena.spark", "type": "ATHENA"},
            ]
        }
        self.datazone.get_connection.return_value = {"connectionId": "c1"}
        self.provider.get_connection_by_type("ATHENA")
        self.datazone.list_connections.assert_called_once_with(
            domainIdentifier="dzd-1", projectIdentifier="proj-1", type="ATHENA"
        )
        self.datazone.get_connection.assert_called_once_with(
            domainIdentifier="dzd-1", identifier="c1", withSecret=True
        )

    def test_spark_connect_prefers_the_default_named_athena_connection(self):
        self.datazone.list_connections.return_value = {
            "items": [
                {"connectionId": "emr", "name": "emr-s.spark", "props": {"sparkEmrProperties": {}}},
                {"connectionId": "ath", "name": "other.spark", "props": {"athenaProperties": {}}},
                {
                    "connectionId": "dflt",
                    "name": "serverless.spark",
                    "props": {"athenaProperties": {}},
                },
            ]
        }
        self.datazone.get_connection.return_value = {"connectionId": "dflt"}
        self.provider.get_connection_by_type("SPARK_CONNECT")
        self.assertEqual(self.datazone.get_connection.call_args.kwargs["identifier"], "dflt")

    def test_spark_connect_without_an_athena_connection_takes_the_first(self):
        self.datazone.list_connections.return_value = {
            "items": [
                {"connectionId": "emr", "props": {"sparkEmrProperties": {}}},
                {"connectionId": "glue", "props": {"sparkGlueProperties": {}}},
            ]
        }
        self.datazone.get_connection.return_value = {"connectionId": "emr"}
        self.provider.get_connection_by_type("SPARK_CONNECT")
        self.assertEqual(self.datazone.get_connection.call_args.kwargs["identifier"], "emr")

    def test_by_type_with_no_match_is_not_found(self):
        self.datazone.list_connections.return_value = {"items": []}
        with self.assertRaises(ConnectionNotFoundError) as cm:
            self.provider.get_connection_by_type("REDSHIFT")
        self.assertEqual(str(cm.exception), "No connection found with type 'REDSHIFT'")

    def test_by_type_refused_fetch_is_an_access_error_naming_the_id(self):
        self.datazone.list_connections.return_value = {"items": [{"connectionId": "c1"}]}
        self.datazone.get_connection.side_effect = _client_error(
            "AccessDeniedException", "GetConnection"
        )
        with self.assertRaises(ConnectionAccessError) as cm:
            self.provider.get_connection_by_type("ATHENA")
        self.assertIn("Unable to access connection 'c1', ", str(cm.exception))

    def test_listing_follows_the_pagination_token_and_returns_summaries(self):
        self.datazone.list_connections.side_effect = [
            {"items": [{"connectionId": "c1"}], "nextToken": "t1"},
            {"items": [{"connectionId": "c2"}, {"connectionId": "c3"}], "nextToken": None},
        ]
        records = self.provider.list_connections()
        self.assertEqual([r["connectionId"] for r in records], ["c1", "c2", "c3"])
        first, second = self.datazone.list_connections.call_args_list
        self.assertEqual(first.kwargs, {"domainIdentifier": "dzd-1", "projectIdentifier": "proj-1"})
        self.assertEqual(second.kwargs["nextToken"], "t1")
        self.datazone.get_connection.assert_not_called()

    def test_a_failing_listing_is_an_access_error_naming_the_scope(self):
        self.datazone.list_connections.side_effect = _client_error(
            "AccessDeniedException", "ListConnections"
        )
        with self.assertRaises(ConnectionAccessError) as cm:
            self.provider.list_connections()
        self.assertIn(
            "Encountered an error while listing connections for project: proj-1 in domain: dzd-1, ",
            str(cm.exception),
        )


if __name__ == "__main__":
    unittest.main()
