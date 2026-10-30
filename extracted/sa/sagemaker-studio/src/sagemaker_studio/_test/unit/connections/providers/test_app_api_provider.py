"""The connection provider over the AWS Notebook app's API."""

import unittest

from sagemaker_studio._test.unit.local_app_fixture import (
    LocalKernelTestCase,
    athena_record,
    lakehouse_record,
    s3_record,
)
from sagemaker_studio.connections.providers import ConnectionAccessError, ConnectionNotFoundError
from sagemaker_studio.connections.providers.app_api import (
    LOCAL_DOMAIN_ID,
    LOCAL_SCOPE_ID,
    AppApiConnectionProvider,
    athena_workgroup,
    aws_location,
    normalize_record,
)
from sagemaker_studio.exceptions import CredentialsUnavailableError, UnsupportedInModeError
from sagemaker_studio.local_kernel import current_context


class RecordHelpersTest(unittest.TestCase):
    def test_normalize_fills_the_scope_fields_the_app_omits(self):
        record = normalize_record(s3_record())
        self.assertEqual(record["domainId"], LOCAL_DOMAIN_ID)
        self.assertEqual(record["projectId"], LOCAL_SCOPE_ID)
        self.assertEqual(record["environmentId"], LOCAL_SCOPE_ID)
        self.assertEqual(record["domainUnitId"], LOCAL_SCOPE_ID)
        self.assertEqual(record["scope"], "PROJECT")
        self.assertEqual(record["store"], "machine")  # local fields pass through

    def test_normalize_keeps_scope_fields_the_record_carries(self):
        record = normalize_record(lakehouse_record())
        self.assertEqual(record["domainId"], "dzd-exampledomain")
        self.assertEqual(record["projectId"], "exampleproject")
        self.assertEqual(
            record["environmentUserRole"],
            "arn:aws:iam::111122223333:role/datazone_usr_role_example",
        )

    def test_normalize_does_not_touch_the_input(self):
        original = s3_record()
        normalize_record(original)
        self.assertNotIn("domainId", original)

    def test_athena_workgroup_from_props_configurations_or_connected_workgroup(self):
        self.assertEqual(athena_workgroup(athena_record(workgroup="wg1")), "wg1")
        self.assertEqual(athena_workgroup(lakehouse_record(workgroup="primary")), "primary")
        self.assertEqual(
            athena_workgroup(
                {
                    "type": "LAKEHOUSE",
                    "configurations": [
                        {"classification": "spark-defaults", "properties": {"x": "y"}},
                        {"classification": "Athena", "properties": {"workgroupName": "mixed-case"}},
                    ],
                }
            ),
            "mixed-case",
        )
        self.assertEqual(athena_workgroup({"type": "LAKEHOUSE", "connectedWorkgroup": "cw"}), "cw")
        self.assertIsNone(athena_workgroup(lakehouse_record(workgroup=None)))
        self.assertIsNone(athena_workgroup(s3_record()))
        self.assertIsNone(athena_workgroup({"configurations": "not a list", "props": "nope"}))
        # Entries that are not mappings, or athena entries naming no workgroup, are skipped.
        self.assertEqual(
            athena_workgroup(
                {
                    "configurations": [
                        "junk",
                        None,
                        {"classification": "athena"},
                        {"classification": "athena", "properties": "nope"},
                        {"classification": "athena", "properties": {"workgroupName": ""}},
                        {"classification": "athena", "properties": {"workgroupName": "after-junk"}},
                    ]
                }
            ),
            "after-junk",
        )
        self.assertIsNone(
            athena_workgroup({"configurations": ["junk", {"classification": "athena"}]})
        )

    def test_aws_location(self):
        self.assertEqual(
            aws_location(s3_record(account="111122223333", region="us-west-2")),
            {"account": "111122223333", "region": "us-west-2"},
        )
        self.assertEqual(
            aws_location(s3_record(account=None, region=None)), {"account": None, "region": None}
        )
        self.assertEqual(aws_location({}), {"account": None, "region": None})
        self.assertEqual(
            aws_location({"physicalEndpoints": [{"awsLocation": "not a mapping"}]}),
            {"account": None, "region": None},
        )


class ProviderTest(LocalKernelTestCase):
    def setUp(self):
        super().setUp()
        self.provider = AppApiConnectionProvider(self.kernel)
        self.app.add(s3_record())
        self.app.add(lakehouse_record())

    def test_identity(self):
        self.assertEqual(self.provider.name, "aws-notebook-app")
        self.assertEqual(
            (self.provider.domain_id, self.provider.project_id), (LOCAL_DOMAIN_ID, LOCAL_SCOPE_ID)
        )
        self.assertIs(self.provider.refreshes_credentials, True)
        self.assertNotIn(self.app.token, repr(self.provider))

    def test_get_by_id_returns_the_normalized_record_with_credentials(self):
        record = self.provider.get_connection_by_id("s3raw")
        self.assertEqual(record["name"], "raw")
        self.assertEqual(record["domainId"], LOCAL_DOMAIN_ID)
        self.assertEqual(record["connectionCredentials"]["accessKeyId"], "AKIA_TEST")
        self.assertEqual(self.app.get_calls("s3raw", with_secret=True)[0]["identifier"], "s3raw")
        self.assertTrue(current_context().signed_in)

    def test_get_by_id_without_secret(self):
        record = self.provider.get_connection_by_id("s3raw", with_secret=False)
        self.assertNotIn("connectionCredentials", record)
        self.assertIsNone(current_context().signed_in)  # nothing observed about credentials

    def test_signed_out_is_the_typed_refusal_with_the_apps_reason(self):
        self.app.sign_out()
        with self.assertRaises(CredentialsUnavailableError) as raised:
            self.provider.get_connection_by_id("s3raw")
        self.assertIn("Connection 's3raw'", str(raised.exception))
        self.assertIn("Sign in to AWS", str(raised.exception))
        self.assertIn("use this connection's data", str(raised.exception))
        self.assertIs(current_context().signed_in, False)
        self.assertIn("Sign in", current_context().signed_in_detail)

    def test_a_200_without_credentials_when_asked_for_them_is_a_refusal(self):
        import json

        row = dict(s3_record(connection_id="nocreds"))
        self.app.raw_responses["nocreds"] = (200, json.dumps(row).encode(), "application/json")
        with self.assertRaises(CredentialsUnavailableError):
            self.provider.get_connection_by_id("nocreds")

    def test_unknown_id_and_bad_id_are_not_found(self):
        with self.assertRaises(ConnectionNotFoundError) as raised:
            self.provider.get_connection_by_id("nosuchid")
        self.assertIn("No connection with id nosuchid", str(raised.exception))
        self.app.raw_responses["bad.id"] = (
            400,
            b'{"error": {"code": "ValidationException", "message": "must be a connection id"}}',
            "application/json",
        )
        with self.assertRaises(ConnectionNotFoundError):
            self.provider.get_connection_by_id("bad.id")

    def test_other_refusals_are_access_errors(self):
        self.app.raw_responses["boom"] = (
            500,
            b'{"error": {"code": "InternalFailure", "message": "Internal error"}}',
            "application/json",
        )
        with self.assertRaises(ConnectionAccessError) as raised:
            self.provider.get_connection_by_id("boom")
        self.assertIn("InternalFailure", str(raised.exception))

    def test_lookups_by_name_or_type_are_id_only_refusals(self):
        for call in (
            lambda: self.provider.get_connection_by_name("raw"),
            lambda: self.provider.get_connection_by_type("S3"),
        ):
            with self.assertRaises(UnsupportedInModeError) as raised:
                call()
            self.assertIn("connection_id=", str(raised.exception))
        self.assertEqual(self.app.calls, [])  # no request was made

    def test_listing_returns_the_normalized_records_without_credentials(self):
        records = self.provider.list_connections()
        self.assertEqual(sorted(r["connectionId"] for r in records), ["lakehouse1", "s3raw"])
        by_id = {r["connectionId"]: r for r in records}
        self.assertEqual(by_id["s3raw"]["domainId"], LOCAL_DOMAIN_ID)  # normalized like a get
        self.assertEqual(by_id["lakehouse1"]["domainId"], "dzd-exampledomain")
        self.assertTrue(all("connectionCredentials" not in r for r in records))
        self.assertEqual(self.app.list_calls(), [{}])
        self.assertIsNone(current_context().signed_in)  # nothing observed about credentials

    def test_listing_one_type_sends_the_type_filter(self):
        records = self.provider.list_connections("LAKEHOUSE")
        self.assertEqual([r["connectionId"] for r in records], ["lakehouse1"])
        self.assertEqual(self.app.list_calls(), [{"type": "LAKEHOUSE"}])

    def test_signed_out_lists_nothing_rather_than_failing(self):
        self.app.sign_out()
        self.assertEqual(self.provider.list_connections(), [])

    def test_a_refused_listing_is_an_access_error(self):
        self.app.raw_list_response = (
            500,
            b'{"error": {"code": "InternalFailure", "message": "Internal error"}}',
            "application/json",
        )
        with self.assertRaises(ConnectionAccessError) as raised:
            self.provider.list_connections()
        self.assertIn("InternalFailure", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
