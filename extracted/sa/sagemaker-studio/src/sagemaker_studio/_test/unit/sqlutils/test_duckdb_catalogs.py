"""The contract behind the attached catalogs: naming rules, statements, what DuckDB holds, the engine."""

import threading
import unittest
from unittest.mock import Mock, patch

from sagemaker_studio._test.unit.local_app_fixture import athena_record, lakehouse_record
from sagemaker_studio.sql_engine.duckdb_engine import catalogs
from sagemaker_studio.sql_engine.duckdb_engine.catalogs import (
    SECRET_SCOPE,
    AttachedCatalog,
    CatalogSecret,
    LocalCatalogs,
    athena_alias,
    athena_attach_statement,
    catalog_alias,
    catalogs_named,
    chain_secret_name,
    create_chain_secret_statement,
    create_role_secret_statement,
    detach_statement,
    drop_secret_statement,
    glue_attach_statement,
    glue_catalog_id,
    is_default_lakehouse,
    present_secrets,
    role_secret_name,
    search_path_catalog,
    search_path_entry,
    search_path_identifier,
    sql_identifier,
    sql_literal,
)


class NamingRulesTest(unittest.TestCase):
    """The Data Explorer's rules, which the frontend applies too: the two copies must agree."""

    def test_the_default_connections_catalogs_keep_their_names_and_others_are_prefixed(self):
        self.assertTrue(is_default_lakehouse("default.catalog"))
        self.assertTrue(is_default_lakehouse("project.default_lakehouse"))
        self.assertFalse(is_default_lakehouse("sales.catalog"))
        self.assertFalse(is_default_lakehouse(""))
        self.assertEqual(catalog_alias("default.catalog", "AwsDataCatalog"), "AwsDataCatalog")
        self.assertEqual(catalog_alias("project.default_lakehouse", "orders"), "orders")
        self.assertEqual(catalog_alias("sales.catalog", "AwsDataCatalog"), "sales_AwsDataCatalog")
        self.assertEqual(catalog_alias("sales.catalog", "orders"), "sales_orders")
        self.assertEqual(catalog_alias("my data", "orders"), "my data_orders")  # a space stays

    def test_an_athena_connection_is_attached_under_its_name_without_the_sql_suffix(self):
        self.assertEqual(
            athena_alias("sales.sql"), "sales"
        )  # the Athena half of a Glue connection pair
        self.assertEqual(athena_alias("warehouse"), "warehouse")  # any other name as it is
        self.assertEqual(athena_alias("project.athena"), "project.athena")
        self.assertEqual(
            athena_alias("sql.reports.sql"), "sql.reports"
        )  # only a trailing .sql goes
        self.assertEqual(athena_alias(""), "")

    def test_glue_catalog_ids(self):
        self.assertEqual(glue_catalog_id("111122223333"), "111122223333")
        self.assertEqual(
            glue_catalog_id("111122223333", "orders"), "111122223333:s3tablescatalog/orders"
        )

    def test_secret_names_are_per_region_or_per_role_connection_and_duckdb_safe(self):
        self.assertEqual(chain_secret_name("us-west-2"), "sagemaker_studio_catalogs_us_west_2")
        self.assertEqual(
            role_secret_name("Conn-1.a"), "sagemaker_studio_catalogs_role_conn_1_a"
        )  # lower case, as DuckDB keeps names
        self.assertNotEqual(chain_secret_name("us-west-2"), role_secret_name("us-west-2"))


class StatementsTest(unittest.TestCase):
    def test_quoting(self):
        self.assertEqual(sql_literal("it's"), "'it''s'")
        self.assertEqual(sql_identifier('a"b c'), '"a""b c"')

    def test_search_path_entries_are_quoted_only_when_duckdb_needs_it(self):
        self.assertEqual(search_path_identifier("plain_1"), "plain_1")
        self.assertEqual(search_path_identifier("my data"), '"my data"')
        self.assertEqual(search_path_identifier("1st"), '"1st"')
        self.assertEqual(
            search_path_identifier("a.b"), '"a.b"'
        )  # a dot would read as catalog.schema
        self.assertEqual(search_path_entry("sales_AwsDataCatalog"), "sales_AwsDataCatalog")
        self.assertEqual(
            search_path_entry("sales_AwsDataCatalog", "orders"), "sales_AwsDataCatalog.orders"
        )
        self.assertEqual(search_path_entry("my data_orders", "1st"), '"my data_orders"."1st"')
        self.assertEqual(search_path_entry('x"y', "s"), '"x""y".s')

    def test_the_chain_secret_resolves_and_refreshes_itself_and_carries_no_credentials(self):
        statement = create_chain_secret_statement(
            "sagemaker_studio_catalogs_us_west_2", "us-west-2"
        )
        self.assertEqual(
            statement,
            "CREATE OR REPLACE SECRET sagemaker_studio_catalogs_us_west_2 (TYPE s3, PROVIDER credential_chain, "
            "REFRESH auto, REGION 'us-west-2', SCOPE 'sagemaker-studio-catalogs://')",
        )
        for never in ("KEY_ID", "SECRET '", "SESSION_TOKEN", "CHAIN"):
            self.assertNotIn(never, statement)

    def test_the_role_secret_assumes_the_role_from_the_same_chain(self):
        self.assertEqual(
            create_role_secret_statement(
                "sagemaker_studio_catalogs_role_c1", "arn:aws:iam::1:role/it's", "eu-west-1"
            ),
            "CREATE OR REPLACE SECRET sagemaker_studio_catalogs_role_c1 (TYPE s3, PROVIDER credential_chain, "
            "CHAIN 'sts', ASSUME_ROLE_ARN 'arn:aws:iam::1:role/it''s', REFRESH auto, REGION 'eu-west-1', "
            "SCOPE 'sagemaker-studio-catalogs://')",
        )

    def test_the_glue_attach_names_the_catalog_the_endpoint_and_the_secret(self):
        self.assertEqual(
            glue_attach_statement(
                "sales_orders",
                "111122223333",
                "us-east-2",
                "sagemaker_studio_catalogs_us_east_2",
                "orders",
            ),
            "ATTACH IF NOT EXISTS '111122223333:s3tablescatalog/orders' AS \"sales_orders\" (TYPE ICEBERG, "
            "ENDPOINT 'glue.us-east-2.amazonaws.com/iceberg', AUTHORIZATION_TYPE 'sigv4', "
            "SECRET 'sagemaker_studio_catalogs_us_east_2')",
        )
        self.assertTrue(
            glue_attach_statement("AwsDataCatalog", "111122223333", "us-east-2", "n").startswith(
                "ATTACH IF NOT EXISTS '111122223333' AS \"AwsDataCatalog\" (TYPE ICEBERG, "
            )
        )

    def test_the_glue_attach_can_create_tables_unstaged_as_the_endpoint_needs(self):
        statement = glue_attach_statement(
            "AwsDataCatalog", "111122223333", "us-east-2", "n", unstaged_creates=True
        )
        self.assertTrue(
            statement.endswith("AUTHORIZATION_TYPE 'sigv4', SECRET 'n', STAGE_CREATE_TABLES false)")
        )

    def test_only_duckdb_2_attaches_with_unstaged_creates_as_1x_refuses_the_option(self):
        versions = [
            ("2.0.0", True),
            ("2.1.3", True),
            ("1.4.3", False),
            ("1.5.1", False),
            ("dev", False),
        ]
        for version, expected in versions:
            with patch("duckdb.__version__", version):
                self.assertEqual(catalogs._has_unstaged_creates(), expected, version)

    def test_the_athena_attach_is_the_workgroup_in_its_region_signing_with_the_given_secret(self):
        self.assertEqual(
            athena_attach_statement(
                "sales", "us-east-2", "wg1", "sagemaker_studio_catalogs_us_east_2"
            ),
            "ATTACH IF NOT EXISTS 'athena://us-east-2/wg1' AS \"sales\" (TYPE athena, SECRET 'sagemaker_studio_catalogs_us_east_2')",
        )
        # No workgroup: the path names the region alone, which is the extension's default workgroup.
        self.assertEqual(
            athena_attach_statement("my wh", "us-east-2", None, "n"),
            "ATTACH IF NOT EXISTS 'athena://us-east-2' AS \"my wh\" (TYPE athena, SECRET 'n')",
        )
        # The data catalog is an option only when it is not the extension's default.
        self.assertEqual(
            athena_attach_statement("sales", "us-east-2", "wg1", "n", "AwsDataCatalog"),
            "ATTACH IF NOT EXISTS 'athena://us-east-2/wg1' AS \"sales\" (TYPE athena, SECRET 'n')",
        )
        self.assertEqual(
            athena_attach_statement("sales", "us-east-2", "wg1", "n", "other_catalog"),
            "ATTACH IF NOT EXISTS 'athena://us-east-2/wg1' AS \"sales\" (TYPE athena, SECRET 'n', CATALOG 'other_catalog')",
        )

    def test_removing_a_database(self):
        self.assertEqual(detach_statement('x"y'), 'DETACH DATABASE IF EXISTS "x""y"')
        self.assertEqual(
            drop_secret_statement("sagemaker_studio_catalogs_c1"),
            'DROP SECRET IF EXISTS "sagemaker_studio_catalogs_c1"',
        )


class TargetsTest(unittest.TestCase):
    """What a listing's record becomes: the alias, the route, the secret and the statement."""

    def test_an_athena_record_is_its_workgroup_in_its_region_under_its_alias(self):
        record = athena_record(
            connection_id="sales_sql", name="sales.sql", workgroup="wg-sales", region="us-west-2"
        )
        target = catalogs._athena_target(record, "us-west-2", "sagemaker_studio_catalogs_us_west_2")
        self.assertEqual(
            (
                target.alias,
                target.connection_id,
                target.connection_name,
                target.catalog,
                target.route,
                target.secret,
            ),
            (
                "sales",
                "sales_sql",
                "sales.sql",
                "AwsDataCatalog",
                "athena",
                "sagemaker_studio_catalogs_us_west_2",
            ),
        )
        self.assertEqual(
            target.statement,
            "ATTACH IF NOT EXISTS 'athena://us-west-2/wg-sales' AS \"sales\" (TYPE athena, SECRET 'sagemaker_studio_catalogs_us_west_2')",
        )

    def test_an_athena_record_naming_another_data_catalog_passes_it(self):
        record = athena_record(
            connection_id="x", name="x.sql", workgroup="wg", catalog="hive_catalog"
        )
        target = catalogs._athena_target(record, "us-west-2", "n")
        self.assertEqual(target.catalog, "hive_catalog")
        self.assertTrue(
            target.statement.endswith("(TYPE athena, SECRET 'n', CATALOG 'hive_catalog')")
        )
        record["catalog"] = None  # none named: the extension's default
        self.assertEqual(
            catalogs._athena_target(record, "us-west-2", "n").catalog, "AwsDataCatalog"
        )

    @patch.object(catalogs, "_has_unstaged_creates", return_value=False)
    def test_a_lakehouse_catalog_goes_through_glue_with_the_given_secret(self, _):
        target = catalogs._glue_target(
            "sales_lh", "sales.catalog", "orders", "111122223333", "us-east-2", "n"
        )
        self.assertEqual(
            (target.alias, target.catalog, target.route, target.secret),
            ("sales_orders", "orders", "glue", "n"),
        )
        self.assertEqual(
            target.statement,
            "ATTACH IF NOT EXISTS '111122223333:s3tablescatalog/orders' AS \"sales_orders\" (TYPE ICEBERG, "
            "ENDPOINT 'glue.us-east-2.amazonaws.com/iceberg', AUTHORIZATION_TYPE 'sigv4', SECRET 'n')",
        )
        self.assertEqual(
            catalogs._glue_target("d", "default.catalog", "AwsDataCatalog", "1", "r", "n").alias,
            "AwsDataCatalog",
        )

    @patch.object(catalogs, "_has_unstaged_creates", return_value=True)
    def test_a_lakehouse_catalog_on_duckdb_2_attaches_with_unstaged_creates(self, _):
        target = catalogs._glue_target(
            "sales_lh", "sales.catalog", "AwsDataCatalog", "111122223333", "us-east-2", "n"
        )
        self.assertTrue(target.statement.endswith(", STAGE_CREATE_TABLES false)"))

    def test_a_records_location_carries_the_access_role_when_it_names_one(self):
        self.assertEqual(
            catalogs._record_location(lakehouse_record(access_role="arn:aws:iam::1:role/x")),
            ("111122223333", "us-east-2", "arn:aws:iam::1:role/x"),
        )
        self.assertEqual(
            catalogs._record_location(lakehouse_record()), ("111122223333", "us-east-2", None)
        )
        self.assertEqual(catalogs._record_location({"name": "bare"}), (None, None, None))


class RecordsTest(unittest.TestCase):
    def test_describe(self):
        secret = CatalogSecret("n", "us-west-2", "arn:aws:iam::1:role/x", "c1")
        self.assertEqual(
            secret.describe(),
            {
                "name": "n",
                "region": "us-west-2",
                "role_arn": "arn:aws:iam::1:role/x",
                "connection_id": "c1",
                "created_at": None,
            },
        )
        catalog = AttachedCatalog(
            "sales", "c1", "sales.sql", "AwsDataCatalog", "athena", "n", attached=False, error="x"
        )
        self.assertEqual(
            catalog.describe(),
            {
                "alias": "sales",
                "connection_id": "c1",
                "connection_name": "sales.sql",
                "catalog": "AwsDataCatalog",
                "route": "athena",
                "secret": "n",
                "attached": False,
                "error": "x",
            },
        )


class _Rows:
    """What ``sql()`` answers, read as DuckDB 2.0 allows it: ``fetchall()`` only, no ``fetchone()``."""

    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows


def _duck(answers):
    """A DuckDB stand-in answering ``duckdb_secrets()`` / ``duckdb_extensions()`` queries from a mapping of substrings."""
    duck = Mock()

    def sql(statement):
        for part, rows in answers.items():
            if part in statement:
                return _Rows(rows)
        return None

    duck.sql.side_effect = sql
    return duck


class WhatDuckDbHoldsTest(unittest.TestCase):
    def test_present_secrets_are_the_sdks_by_scope_whatever_their_name(self):
        duck = _duck(
            {
                "duckdb_secrets()": [
                    ("sagemaker_studio_catalogs_us_west_2", [SECRET_SCOPE]),
                    ("by_another_process", [SECRET_SCOPE]),  # any name, the scope says
                    ("sagemaker_studio_catalogs_role_c1", [SECRET_SCOPE]),
                    ("my_bucket_keys", ["s3://", "s3n://", "s3a://"]),  # a user's own, not ours
                    (
                        "__default_s3",
                        ["s3://", "s3n://", "s3a://"],
                    ),  # the engine's own credential-chain secret
                    ("__internal_ic_t1", ["s3://tables/t1/"]),  # vended by the iceberg extension
                    ("odd", "sagemaker-studio-catalogs://"),  # a scope as one string, not a list
                ]
            }
        )
        self.assertEqual(
            present_secrets(duck),
            [
                "sagemaker_studio_catalogs_us_west_2",
                "by_another_process",
                "sagemaker_studio_catalogs_role_c1",
                "odd",
            ],
        )
        self.assertEqual(
            catalogs.vended_secret_names(_duck({"starts_with(name": [("__internal_ic_t1",)]})),
            ["__internal_ic_t1"],
        )

    def test_an_engine_that_cannot_answer_is_none_not_empty(self):
        duck = Mock()
        duck.sql.side_effect = RuntimeError("no such function")
        self.assertIsNone(present_secrets(duck))
        self.assertEqual(catalogs.vended_secret_names(duck), [])
        self.assertFalse(catalogs._athena_extension_loaded(duck))

    def test_the_athena_extension_is_looked_up_as_loaded(self):
        duck = Mock()
        duck.sql.return_value.fetchall.return_value = [(1,)]
        self.assertTrue(catalogs._athena_extension_loaded(duck))
        duck.sql.return_value.fetchall.return_value = [(0,)]
        self.assertFalse(catalogs._athena_extension_loaded(duck))
        duck.sql.return_value.fetchall.return_value = []
        self.assertFalse(catalogs._athena_extension_loaded(duck))
        # Read as DuckDB 2.0 allows it: fetchall() on sql()'s relation, never fetchone().
        self.assertFalse(duck.sql.return_value.fetchone.called)

    def test_dropping_secrets_is_best_effort(self):
        duck = Mock()
        duck.sql.side_effect = [None, RuntimeError("busy"), None]
        self.assertEqual(catalogs.drop_secrets(duck, ["a", "b", "c"]), ["a", "c"])
        self.assertEqual(
            [c.args[0] for c in duck.sql.call_args_list],
            [
                'DROP SECRET IF EXISTS "a";',
                'DROP SECRET IF EXISTS "b";',
                'DROP SECRET IF EXISTS "c";',
            ],
        )


class S3TablesListingTest(unittest.TestCase):
    """The one AWS call this module makes signs like the catalogs it attaches: chain, or role from it."""

    PAGES = [
        {
            "CatalogList": [
                {"Name": "s3tablescatalog", "ParentCatalogNames": []},
                {"Name": "orders", "ParentCatalogNames": ["s3tablescatalog"]},
                {"Name": "nested", "ParentCatalogNames": ["other", "s3tablescatalog"]},
            ],
            "NextToken": "page-2",
        },
        {
            "CatalogList": [
                {"Name": "returns", "ParentCatalogNames": ["s3tablescatalog"]},
                {"ParentCatalogNames": ["s3tablescatalog"]},
                # What the public API answers for a federated table bucket: the parent only in the id.
                {"Name": "sales", "CatalogId": "123456789012:s3tablescatalog/sales"},
                {"Name": "s3tablescatalog", "CatalogId": "123456789012:s3tablescatalog"},
                {"Name": "plain", "CatalogId": "123456789012"},
            ]
        },
    ]

    def setUp(self):
        patcher = patch.object(catalogs, "boto3")
        self.boto3 = patcher.start()
        self.addCleanup(
            patcher.stop
        )  # this one only: patch.stopall would stop other modules' import-time patches
        self.session = self.boto3.Session.return_value
        self.glue = Mock()
        self.glue.get_catalogs.side_effect = list(self.PAGES)

    def test_pages_through_get_catalogs_and_keeps_the_s3_tables_children(self):
        self.session.client.return_value = self.glue
        self.assertEqual(
            catalogs._list_s3_tables_catalogs("123456789012", "us-east-2"),
            ["orders", "returns", "sales"],
        )
        first, second = self.glue.get_catalogs.call_args_list
        # Under the connection's account (not the caller's, which differs cross-account); every
        # bucket, with databases or not.
        self.assertEqual(first.kwargs, {"ParentCatalogId": "123456789012", "Recursive": True})
        self.assertEqual(
            second.kwargs,
            {"ParentCatalogId": "123456789012", "Recursive": True, "NextToken": "page-2"},
        )

    def test_without_a_role_the_client_is_the_default_chains_in_the_connections_region(self):
        self.session.client.return_value = self.glue
        catalogs._list_s3_tables_catalogs("123456789012", "us-east-2", None)
        self.boto3.Session.assert_called_once_with(region_name="us-east-2")
        self.session.client.assert_called_once_with("glue")  # no keys handed over: the chain's
        self.boto3.client.assert_not_called()  # and no STS

    def test_with_a_role_it_is_assumed_from_the_chain_as_a_sts_chain_secret_does(self):
        sts = Mock()
        sts.assume_role.return_value = {
            "Credentials": {
                "AccessKeyId": "ASIAROLE",
                "SecretAccessKey": "s",
                "SessionToken": "t",
                "Expiration": "...",
            }
        }
        self.session.client.side_effect = lambda service, **_: {"sts": sts}[service]
        self.boto3.client.return_value = self.glue
        role = "arn:aws:iam::111122223333:role/catalog-access"
        self.assertEqual(
            catalogs._list_s3_tables_catalogs("111122223333", "eu-west-1", role),
            ["orders", "returns", "sales"],
        )
        self.boto3.Session.assert_called_once_with(region_name="eu-west-1")
        sts.assume_role.assert_called_once_with(
            RoleArn=role, RoleSessionName="sagemaker-studio-duckdb-catalogs"
        )
        self.boto3.client.assert_called_once_with(
            "glue",
            region_name="eu-west-1",
            aws_access_key_id="ASIAROLE",
            aws_secret_access_key="s",
            aws_session_token="t",
        )

    def test_a_chain_with_nothing_to_resolve_fails_in_the_callers_hands(self):
        from botocore.exceptions import NoCredentialsError

        self.session.client.return_value = self.glue
        self.glue.get_catalogs.side_effect = (
            NoCredentialsError()
        )  # botocore resolves at the first call
        with self.assertRaises(NoCredentialsError):
            catalogs._list_s3_tables_catalogs("123456789012", "us-east-2")


class WhoSignedTest(unittest.TestCase):
    """Attributing a refused read: the catalog a cell ran in, the names a statement qualifies, their secret's role."""

    ROLE = "arn:aws:iam::444455556666:role/lake-reader"

    def test_the_first_search_path_entry_is_read_back_as_a_name(self):
        self.assertEqual(search_path_catalog("AwsDataCatalog.db,"), "AwsDataCatalog")
        self.assertEqual(search_path_catalog("sales"), "sales")
        self.assertEqual(search_path_catalog(" sales , other.x"), "sales")
        self.assertEqual(
            search_path_catalog(search_path_entry("my data_orders", "sales")), "my data_orders"
        )
        self.assertEqual(
            search_path_catalog(search_path_entry('a"b')), 'a"b'
        )  # a doubled quote inside
        self.assertEqual(search_path_catalog('"never closed'), "never closed")  # read to the end
        self.assertIsNone(search_path_catalog(""))
        self.assertIsNone(search_path_catalog("   "))

    def test_catalogs_named_are_the_cells_catalog_and_every_alias_the_statement_qualifies(self):
        aliases = ["AwsDataCatalog", "shared_AwsDataCatalog", "sales", "my data_orders"]
        self.assertEqual(
            catalogs_named("select 1 from t", "shared_AwsDataCatalog.db", aliases),
            ["shared_AwsDataCatalog"],
        )
        self.assertEqual(catalogs_named("select * from sales.db.t", "", aliases), ["sales"])
        self.assertEqual(
            catalogs_named('select * from "my data_orders".db.t', "", aliases), ["my data_orders"]
        )
        self.assertEqual(
            catalogs_named('select * from "SALES" . db.t', "", aliases), ["sales"]
        )  # case-insensitive, spaces
        self.assertEqual(
            catalogs_named(
                "select * from awsdatacatalog.x.t join sales.db.u using (k)",
                "shared_AwsDataCatalog",
                aliases,
            ),
            ["AwsDataCatalog", "shared_AwsDataCatalog", "sales"],
        )
        # 'sales' here is a schema of AwsDataCatalog, not the Athena alias; a bare word is not a qualifier.
        self.assertEqual(
            catalogs_named("select * from AwsDataCatalog.sales.t", "", aliases), ["AwsDataCatalog"]
        )
        self.assertEqual(catalogs_named("select sales from t", "", aliases), [])
        self.assertEqual(catalogs_named("select 1", "", aliases), [])

    def _state(self):
        state = LocalCatalogs()
        state._secrets = {
            "sagemaker_studio_catalogs_us_west_2": CatalogSecret(
                "sagemaker_studio_catalogs_us_west_2", "us-west-2"
            ),
            "sagemaker_studio_catalogs_role_shared": CatalogSecret(
                "sagemaker_studio_catalogs_role_shared", "us-east-2", self.ROLE, "shared"
            ),
        }
        state._attached = {
            "AwsDataCatalog": AttachedCatalog(
                "AwsDataCatalog",
                "lh",
                "default.catalog",
                "AwsDataCatalog",
                "glue",
                "sagemaker_studio_catalogs_us_west_2",
            ),
            "shared_AwsDataCatalog": AttachedCatalog(
                "shared_AwsDataCatalog",
                "shared",
                "shared.catalog",
                "AwsDataCatalog",
                "glue",
                "sagemaker_studio_catalogs_role_shared",
            ),
            "shared_orders": AttachedCatalog(
                "shared_orders",
                "shared",
                "shared.catalog",
                "orders",
                "glue",
                "sagemaker_studio_catalogs_role_shared",
            ),
            "broken": AttachedCatalog(
                "broken",
                "b",
                "broken.catalog",
                "AwsDataCatalog",
                "glue",
                None,
                attached=False,
                error="no",
            ),
        }
        return state

    def test_the_role_is_named_when_every_catalog_the_statement_ran_against_signs_as_it(self):
        state = self._state()
        signer = state.role_signing("select 1 from t", "shared_AwsDataCatalog.db")
        self.assertEqual(
            (signer.role_arn, signer.aliases, signer.connections),
            (self.ROLE, ["shared_AwsDataCatalog"], ["shared.catalog"]),
        )
        both = state.role_signing(
            "select * from shared_AwsDataCatalog.a.t join shared_orders.b.u using (k)", ""
        )
        self.assertEqual(both.aliases, ["shared_AwsDataCatalog", "shared_orders"])
        self.assertEqual(both.connections, ["shared.catalog"])  # one connection, named once

    def test_no_role_is_named_for_the_kernels_own_identity_or_a_mix_or_no_catalog(self):
        state = self._state()
        self.assertIsNone(
            state.role_signing("select 1 from t", "AwsDataCatalog.db")
        )  # the shared chain secret
        self.assertIsNone(
            state.role_signing(
                "select * from AwsDataCatalog.a.t join shared_orders.b.u using (k)", ""
            )
        )
        self.assertIsNone(state.role_signing("select 1 from t", ""))
        self.assertIsNone(
            state.role_signing("select 1 from broken.db.t", "")
        )  # never attached: not a signer


class LocksTest(unittest.TestCase):
    """A round's network calls keep no reader waiting; two rounds never interleave."""

    def _blocking_duck(self, gate, entered):
        """A stand-in whose CREATE SECRET blocks on ``gate`` (the chain resolving over the network)."""
        duck = Mock()

        def sql(statement):
            if statement.startswith("CREATE OR REPLACE SECRET"):
                entered.set()
                gate.wait(timeout=10)
            if "duckdb_extensions()" in statement:
                return _Rows([(0,)])
            if "duckdb_secrets()" in statement or "duckdb_databases()" in statement:
                return _Rows([])
            return None

        duck.sql.side_effect = sql
        return duck

    def test_readers_are_answered_while_a_round_waits_on_the_network(self):
        gate, entered = threading.Event(), threading.Event()
        duck = self._blocking_duck(gate, entered)
        state = LocalCatalogs()
        state._attached["old"] = AttachedCatalog(
            "old", "c0", "old.catalog", "AwsDataCatalog", "glue", "s0", attached=False, error="x"
        )
        records = [lakehouse_record(connection_id="lh", name="default.catalog", workgroup=None)]
        with patch.object(catalogs, "_list_s3_tables_catalogs", return_value=[]):
            round_thread = threading.Thread(target=state.attach_all, args=(duck, records))
            round_thread.start()
            self.assertTrue(entered.wait(timeout=5), "the round never reached its CREATE SECRET")
            # The round is inside its network call: a cell classifying its error, and a listing, get
            # an answer now, from the records as they stand (the reset of the round has run).
            answered = []
            reader = threading.Thread(
                target=lambda: answered.extend(
                    [state.role_signing("select 1", "AwsDataCatalog"), state.attached()]
                )
            )
            reader.start()
            reader.join(timeout=2)
            self.assertFalse(reader.is_alive(), "a reader waited on the round's network call")
            self.assertEqual(answered, [None, []])
            gate.set()
            round_thread.join(timeout=5)
        self.assertFalse(round_thread.is_alive())
        self.assertEqual([c.alias for c in state.attached()], ["AwsDataCatalog"])

    def test_a_second_round_waits_for_the_first(self):
        gate, entered = threading.Event(), threading.Event()
        duck = self._blocking_duck(gate, entered)
        state = LocalCatalogs()
        records = [lakehouse_record(connection_id="lh", name="default.catalog", workgroup=None)]
        with patch.object(catalogs, "_list_s3_tables_catalogs", return_value=[]):
            first = threading.Thread(target=state.attach_all, args=(duck, records))
            first.start()
            self.assertTrue(entered.wait(timeout=5))
            statements_before = duck.sql.call_count
            second = threading.Thread(target=state.reset, args=(duck,))
            second.start()
            second.join(timeout=0.5)
            self.assertTrue(second.is_alive(), "the second round ran while the first was in flight")
            self.assertEqual(
                duck.sql.call_count, statements_before
            )  # not one statement of its own yet
            gate.set()
            first.join(timeout=5)
            second.join(timeout=5)
        self.assertFalse(first.is_alive() or second.is_alive())
        self.assertEqual(
            state.attached(), []
        )  # the second round, a reset, ran after the first attached


class ChainCredentialsTest(unittest.TestCase):
    """``chain_credentials()``: one look at botocore's chain, answered as (found, reason)."""

    ENVELOPE = (
        '{"error": {"code": "NoCredentials", "message": "Sign in to AWS in the AWS Notebook app"}}'
    )

    def setUp(self):
        patcher = patch.object(catalogs, "boto3")
        self.boto3 = patcher.start()
        self.addCleanup(patcher.stop)
        self.resolve = self.boto3.Session.return_value.get_credentials

    def test_credentials_found_is_true_with_no_reason(self):
        self.resolve.return_value = Mock(name="credentials")
        self.assertEqual(catalogs.chain_credentials(), (True, ""))
        self.boto3.Session.assert_called_once_with()  # the default chain, no region, no profile
        self.resolve.assert_called_once_with()

    def test_a_chain_resolving_nothing_is_false_and_says_so(self):
        self.resolve.return_value = None
        self.assertEqual(
            catalogs.chain_credentials(),
            (False, "The AWS credential chain resolves no credentials"),
        )

    def test_the_kernel_servers_refusal_is_the_apps_own_reason(self):
        from botocore.exceptions import CredentialRetrievalError

        # The container provider quotes the kernel server's answer; its envelope carries the app's reason.
        self.resolve.side_effect = CredentialRetrievalError(
            provider="container-role",
            error_msg="Received non 200 response 403 from container metadata: " + self.ENVELOPE,
        )
        self.assertEqual(
            catalogs.chain_credentials(), (False, "Sign in to AWS in the AWS Notebook app")
        )

    def test_any_other_failure_is_its_first_line_and_never_raised(self):
        self.resolve.side_effect = RuntimeError(
            "Received non 200 response 502 from container metadata: upstream\nmore"
        )
        self.assertEqual(
            catalogs.chain_credentials(),
            (False, "Received non 200 response 502 from container metadata: upstream"),
        )
        self.resolve.side_effect = RuntimeError(
            '{"error": "not an envelope"} trailing'
        )  # a brace, no reason in it
        self.assertEqual(
            catalogs.chain_credentials(), (False, '{"error": "not an envelope"} trailing')
        )
        self.resolve.side_effect = RuntimeError("")
        self.assertEqual(catalogs.chain_credentials(), (False, "RuntimeError"))


class WithAnEngineThatCannotAnswerTest(unittest.TestCase):
    """DuckDB's introspection failing must not stop a reset from dropping what the SDK knows it made."""

    def test_reset_detaches_and_drops_what_the_sdk_knows_of(self):
        state = LocalCatalogs()
        state._attached["sales_AwsDataCatalog"] = AttachedCatalog(
            "sales_AwsDataCatalog",
            "c1",
            "sales.catalog",
            "AwsDataCatalog",
            "glue",
            "sagemaker_studio_catalogs_us_east_2",
        )
        state._attached["never"] = AttachedCatalog(
            "never",
            "c2",
            "never.catalog",
            "AwsDataCatalog",
            "glue",
            None,
            attached=False,
            error="x",
        )
        state._secrets["sagemaker_studio_catalogs_us_east_2"] = CatalogSecret(
            "sagemaker_studio_catalogs_us_east_2", "us-east-2"
        )
        duck = Mock()

        def sql(statement):
            if "duckdb_" in statement:
                raise RuntimeError("no introspection here")
            return None

        duck.sql.side_effect = sql
        self.assertEqual(state.reset(duck), {})
        statements = [c.args[0] for c in duck.sql.call_args_list if "duckdb_" not in c.args[0]]
        # The never-attached record is forgotten without a DETACH.
        self.assertEqual(
            statements,
            [
                'DETACH DATABASE IF EXISTS "sales_AwsDataCatalog";',
                'DROP SECRET IF EXISTS "sagemaker_studio_catalogs_us_east_2";',
            ],
        )
        self.assertEqual((state.attached(), state.secrets()), ([], []))
        self.assertTrue(state.empty())


class EnsureSecretTest(unittest.TestCase):
    """One shared secret per region; one secret per connection that names an access role."""

    def test_the_shared_secret_is_made_once_per_region(self):
        state, duck = LocalCatalogs(), Mock()
        first = state._ensure_secret(duck, "c1", "us-west-2", None)
        second = state._ensure_secret(duck, "c2", "us-west-2", None)
        third = state._ensure_secret(duck, "c3", "eu-west-1", None)
        self.assertIs(first, second)
        self.assertEqual(
            (first.name, third.name),
            ("sagemaker_studio_catalogs_us_west_2", "sagemaker_studio_catalogs_eu_west_1"),
        )
        self.assertEqual(duck.sql.call_count, 2)
        self.assertIsNone(first.connection_id)  # nobody's own: shared

    def test_a_role_secret_is_the_connections_own_and_re_created_each_time(self):
        state, duck = LocalCatalogs(), Mock()
        role = "arn:aws:iam::1:role/x"
        first = state._ensure_secret(duck, "c1", "us-west-2", role)
        state._ensure_secret(duck, "c1", "us-west-2", role)
        self.assertEqual(
            (first.name, first.role_arn, first.connection_id),
            ("sagemaker_studio_catalogs_role_c1", role, "c1"),
        )
        self.assertEqual(
            duck.sql.call_count, 2
        )  # CREATE OR REPLACE both times: the role may have changed
        self.assertEqual(len(state.secrets()), 1)

    def test_a_refused_secret_is_not_recorded(self):
        state, duck = LocalCatalogs(), Mock()
        duck.sql.side_effect = RuntimeError("Failed to resolve AWS credentials")
        with self.assertRaises(RuntimeError):
            state._ensure_secret(duck, "c1", "us-west-2", None)
        self.assertEqual(state.secrets(), [])


class OneRowTest(unittest.TestCase):
    """``_one_row``, the one way the SDK reads a row: ``sql(...).fetchall()`` and the first row,
    which DuckDB 1.x (these tests) and 2.0 (the app, where a relation has no ``fetchone()``) both
    allow, leaving nothing on the connection."""

    def test_the_first_row_or_none_through_fetchall_on_a_real_connection(self):
        import duckdb

        from sagemaker_studio.sql_engine.duckdb_engine import _one_row

        con = duckdb.connect()
        try:
            self.assertEqual(
                _one_row(con, "SELECT current_database(), current_schema()"), ("memory", "main")
            )
            self.assertEqual(_one_row(con, "SELECT current_setting('search_path')"), ("",))
            self.assertIsNone(_one_row(con, "SELECT 1 WHERE false"))
            self.assertEqual(_one_row(con, "SELECT 1 UNION ALL SELECT 2 ORDER BY 1"), (1,))
            self.assertEqual(
                con.sql("SELECT 3").fetchall(), [(3,)]
            )  # nothing left over blocks the next statement
        finally:
            con.close()

    def test_every_reader_of_a_row_goes_through_it(self):
        # The three places the SDK reads a row (the cell's search_path push and the classifier's
        # read of it, the athena extension check) call sql(...).fetchall(), never fetchone(): a
        # stand-in offering only fetchall(), as a DuckDB 2.0 relation does, answers them all.
        from types import SimpleNamespace

        from sagemaker_studio.sql_engine.duckdb_engine import engine
        from sagemaker_studio.utils import duckdbutils

        class Duck:
            def __init__(self):
                self.statements = []

            def sql(self, statement):
                self.statements.append(statement)
                upper = statement.upper()
                if "CURRENT_SETTING('SEARCH_PATH')" in upper:
                    return _Rows([("x.y",)])
                if "DUCKDB_EXTENSIONS()" in upper:
                    return _Rows([(1,)])
                return SimpleNamespace(df=lambda: "df")  # a statement's own result

        duck = Duck()
        self.assertEqual(duckdbutils._push_search_path(duck, "cat", "db"), "x.y")
        self.assertEqual(engine._current_search_path(duck), "x.y")
        self.assertTrue(catalogs._athena_extension_loaded(duck))
        self.assertEqual(
            engine._run_local_duckdb(duck, "SELECT 1"), "df"
        )  # a statement's own result


if __name__ == "__main__":
    unittest.main()
