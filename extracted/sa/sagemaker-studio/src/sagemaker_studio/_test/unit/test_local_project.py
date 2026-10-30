"""``Project()`` on an AWS Notebook local kernel: connections by id through the app, no DataZone."""

import unittest
from datetime import timezone

from sagemaker_studio import ClientConfig, Project
from sagemaker_studio._test.unit.local_app_fixture import (
    LocalKernelTestCase,
    athena_record,
    credentials,
    lakehouse_record,
    s3_record,
)
from sagemaker_studio.connections.connection import Connection
from sagemaker_studio.exceptions import CredentialsUnavailableError, UnsupportedInModeError
from sagemaker_studio.local_kernel import RuntimeMode
from sagemaker_studio.sagemaker_studio_api import _LocalKernelClientStandIn


class LocalProjectTest(LocalKernelTestCase):
    def setUp(self):
        super().setUp()
        self.app.add(s3_record())
        self.app.add(lakehouse_record())
        self.app.add(athena_record())

    def test_project_stands_for_the_workspace_and_builds_no_aws_client(self):
        project = Project()
        self.assertEqual(
            (project.domain_id, project.id, project.name), ("dzd-local", "local", "local")
        )
        self.assertEqual(project.project_status, "LOCAL")
        api = project._sagemaker_studio_api
        for client in (api.datazone_api, api.glue_api, api.secrets_manager_api, api.kms_api):
            self.assertIsInstance(client, _LocalKernelClientStandIn)
        with self.assertRaises(UnsupportedInModeError):
            api.datazone_api.list_connections(domainIdentifier="x")
        self.assertIsNone(api.execution_client)
        self.assertEqual(self.app.calls, [])  # building the Project asks the app nothing

    def test_project_arguments_are_refused(self):
        for kwargs in ({"name": "p"}, {"id": "p"}, {"domain_id": "d"}):
            with self.assertRaises(UnsupportedInModeError):
                Project(**kwargs)

    def test_the_api_exposes_the_runtime_context(self):
        context = Project()._sagemaker_studio_api.context
        self.assertIs(context.mode, RuntimeMode.LOCAL)
        self.assertEqual(context.app_url, self.app.url)

    def test_the_client_stand_ins_look_like_plain_objects_to_introspection(self):
        import copy

        stand_in = Project()._sagemaker_studio_api.datazone_api
        self.assertEqual(
            repr(stand_in), f"<_LocalKernelClientStandIn datazone {stand_in.meta.region_name}>"
        )
        with self.assertRaises(AttributeError):  # dunder/private probes are not refusals
            stand_in._private
        self.assertIsInstance(copy.copy(stand_in), _LocalKernelClientStandIn)
        with self.assertRaises(UnsupportedInModeError) as raised:
            stand_in.list_connections
        self.assertIn("datazone client (list_connections)", str(raised.exception))

    def test_an_app_failure_resolving_a_connection_is_a_runtime_error(self):
        # Lookups by id translate nothing: the provider's access error (a RuntimeError carrying
        # the app's code) reaches the caller, as DataZone's ClientError does on a remote kernel.
        self.app.raw_responses["s3raw"] = (
            500,
            b'{"error": {"code": "InternalFailure", "message": "Internal error"}}',
            "application/json",
        )
        with self.assertRaises(RuntimeError) as raised:
            Project().connection(id="s3raw")
        self.assertIn("InternalFailure", str(raised.exception))

    def test_connection_by_id_comes_from_the_app_with_credentials(self):
        connection = Project().connection(id="s3raw")
        self.assertIsInstance(connection, Connection)
        self.assertEqual((connection.id, connection.name, connection.type), ("s3raw", "raw", "S3"))
        self.assertEqual(connection.data.s3_uri, "s3://b/raw/")
        self.assertEqual(connection.domain_id, "dzd-local")
        self.assertEqual(connection.physical_endpoints[0].aws_region, "us-west-2")
        creds = connection.connection_creds
        self.assertEqual(
            (creds.access_key_id, creds.session_token), ("AKIA_TEST", "AKIA_TEST-token")
        )
        self.assertEqual(creds.expiration.tzinfo, timezone.utc)  # the app's ``Z`` suffix parsed
        self.assertEqual(len(self.app.get_calls("s3raw", with_secret=True)), 1)

    def test_lakehouse_catalog_connection_runs_sql_on_athena(self):
        connection = Project().connection(id="lakehouse1")
        self.assertEqual(connection.type, "LAKEHOUSE")
        self.assertEqual(connection.athena_workgroup, "primary")
        self.assertEqual(connection.sql_engine_type, "ATHENA")
        self.assertEqual(
            connection.iam_role, "arn:aws:iam::111122223333:role/datazone_usr_role_example"
        )
        # The scope fields the record carried are kept, not replaced by the stand-ins.
        self.assertEqual(connection.project_id, "exampleproject")

    def test_athena_connection_keeps_its_type(self):
        connection = Project().connection(id="wh")
        self.assertEqual((connection.type, connection.sql_engine_type), ("ATHENA", "ATHENA"))
        self.assertEqual(connection.athena_workgroup, "primary")
        self.assertEqual(connection.data.catalog, "AwsDataCatalog")

    def test_lookups_by_name_are_refused_without_a_request(self):
        project = Project()
        with self.assertRaises(UnsupportedInModeError):
            project.connection("raw")
        self.assertEqual(self.app.calls, [])

    def test_connections_are_listed_through_the_app_without_credentials(self):
        connections = Project().connections
        self.assertEqual(sorted(c.name for c in connections), ["catalog", "raw", "warehouse"])
        self.assertTrue(all(isinstance(c, Connection) for c in connections))
        self.assertEqual(self.app.list_calls(), [{}])
        # The listing carries no credentials. A LAKEHOUSE connection builds its Glue client when
        # it is constructed, which fetches its credentials through the app once; the S3 and
        # Athena connections fetch nothing until something needs theirs.
        self.assertEqual(self.app.get_calls(), [{"identifier": "lakehouse1", "withSecret": True}])
        lakehouse = next(c for c in connections if c.name == "catalog")
        self.assertEqual(lakehouse.connection_creds.access_key_id, "AKIA_TEST")
        self.assertEqual(len(self.app.get_calls()), 1)  # the ones it holds are fresh
        self.assertEqual(lakehouse.sql_engine_type, "ATHENA")
        warehouse = next(c for c in connections if c.name == "warehouse")
        self.assertEqual(warehouse.connection_creds.access_key_id, "AKIA_TEST")
        self.assertEqual(len(self.app.get_calls("wh", with_secret=True)), 1)

    def test_signed_out_the_listing_is_empty(self):
        self.app.sign_out()
        self.assertEqual(Project().connections, [])

    def test_unknown_id_is_a_lookup_error(self):
        with self.assertRaises(LookupError):
            Project().connection(id="nosuchid")

    def test_signed_out_is_the_typed_refusal(self):
        self.app.sign_out()
        with self.assertRaises(CredentialsUnavailableError) as raised:
            Project().connection(id="s3raw")
        self.assertIn("Sign in to AWS", str(raised.exception))

    def test_create_client_signs_with_credentials_refreshed_from_the_app(self):
        from botocore.credentials import RefreshableCredentials

        connection = Project().connection(id="s3raw")
        client = connection.create_client("s3")
        self.assertEqual(client.meta.region_name, "us-west-2")
        signer_credentials = client._request_signer._credentials
        self.assertIsInstance(signer_credentials, RefreshableCredentials)
        frozen = signer_credentials.get_frozen_credentials()
        self.assertEqual(
            (frozen.access_key, frozen.secret_key, frozen.token),
            ("AKIA_TEST", "AKIA_TEST-secret", "AKIA_TEST-token"),
        )
        # Fresh for an hour: the record's own credentials were used, nothing was re-fetched.
        self.assertEqual(len(self.app.get_calls("s3raw", with_secret=True)), 1)

    def test_credentials_about_to_expire_are_fetched_again_before_use(self):
        self.app.sign_in("SHORT", minutes=2)  # inside the refresh window
        connection = Project().connection(id="s3raw")
        self.assertEqual(connection._connection_creds.access_key_id, "SHORT")
        self.app.sign_in("ROTATED", minutes=60)
        self.assertEqual(connection.connection_creds.access_key_id, "ROTATED")
        self.assertEqual(len(self.app.get_calls("s3raw", with_secret=True)), 2)
        self.assertEqual(connection.connection_creds.access_key_id, "ROTATED")
        self.assertEqual(
            len(self.app.get_calls("s3raw", with_secret=True)), 2
        )  # fresh: no third call

    def test_a_client_follows_a_rotation_at_expiry_and_a_sign_out(self):
        self.app.sign_in("SHORT", minutes=2)
        connection = Project().connection(id="s3raw")
        client = connection.create_client("s3")
        self.app.sign_in("ROTATED", minutes=60)
        frozen = client._request_signer._credentials.get_frozen_credentials()
        self.assertEqual(frozen.access_key, "ROTATED")
        # Signed out with short credentials: the next refresh raises the typed error.
        self.app.sign_in("SHORT2", minutes=2)
        connection._connection_creds = None
        connection.connection_creds  # SHORT2 now held, about to expire
        self.app.sign_out()
        with self.assertRaises(CredentialsUnavailableError):
            connection.connection_creds

    def test_members_only_datazone_answers_are_refused(self):
        project = Project()
        for call in (
            lambda: project.iam_role,
            lambda: project.user_id,
            lambda: project.kms_key_arn,
            lambda: project.mlflow_tracking_server_arn,
            lambda: project.shared_files,
            lambda: project.s3.root,
        ):
            with self.assertRaises(UnsupportedInModeError):
                call()

    def test_an_injected_provider_takes_precedence(self):
        class Memory:
            name = "memory"
            domain_id = "dzd-mem"
            project_id = "mem"
            refreshes_credentials = False

            def get_connection_by_id(self, connection_id):
                return {
                    **s3_record(connection_id=connection_id),
                    "connectionCredentials": credentials("MEM"),
                }

        project = Project(config=ClientConfig(connection_provider=Memory()))
        self.assertEqual((project.domain_id, project.id), ("dzd-mem", "mem"))
        self.assertEqual(project.connection(id="anything").connection_creds.access_key_id, "MEM")
        self.assertEqual(self.app.calls, [])

    def test_the_app_is_asked_each_time_a_connection_is_resolved(self):
        project = Project()
        project.connection(id="s3raw")
        project.connection(id="s3raw")
        self.assertEqual(len(self.app.get_calls("s3raw")), 2)


class SignedOutProjectTest(LocalKernelTestCase):
    signed_in = False

    def test_metadata_without_credentials_still_resolves(self):
        self.app.add(s3_record())
        provider = self.kernel.connection_provider()
        record = provider.get_connection_by_id("s3raw", with_secret=False)
        self.assertEqual(record["name"], "raw")
        with self.assertRaises(CredentialsUnavailableError):
            Project().connection(id="s3raw")
        self.assertIs(self.kernel.context().signed_in, False)


if __name__ == "__main__":
    unittest.main()
