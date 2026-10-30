"""``sqlutils`` on an AWS Notebook local kernel: connection-less DuckDB over the chain secret,
Athena connections on the native executor, and the project's catalogs attached to DuckDB."""

import re
import threading
import unittest
from typing import Dict, List, Optional, Set
from unittest.mock import Mock, call, patch

from botocore.exceptions import CredentialRetrievalError
from pandas import DataFrame

from sagemaker_studio import ClientConfig, sqlutils
from sagemaker_studio._test.unit.local_app_fixture import (
    FakeApp,
    LocalKernelTestCase,
    athena_record,
    lakehouse_record,
    s3_record,
)
from sagemaker_studio.connections import ConnectionService
from sagemaker_studio.exceptions import (
    AccessDeniedError,
    CatalogUnavailableError,
    CredentialsExpiredError,
    CredentialsUnavailableError,
    UnsupportedInModeError,
)
from sagemaker_studio.local_kernel import current_context
from sagemaker_studio.sql_engine.duckdb_engine import catalogs as duckdb_catalogs
from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine
from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
from sagemaker_studio.utils import duckdbutils

#: The id the fake app gives its built-in ``default.s3`` connection (``s3://``, every bucket),
#: whose credentials the kernel server serves as the container credentials. The SDK knows nothing
#: of it: an S3 connection is listed and ignored, never attached or run on.
DEFAULT_S3_CONNECTION_ID = "default_s3"
#: What the kernel server answers botocore's container provider while the app is signed out.
SIGNED_OUT_REASON = "Sign in to AWS in the AWS Notebook app"
_SECRET_HEAD = re.compile(
    r'CREATE (?:OR REPLACE )?SECRET\s*("(?:[^"]|"")*"|\S*?)\s*\((.*)\)\s*;?\s*$',
    re.IGNORECASE | re.DOTALL,
)
_ATTACH_HEAD = re.compile(
    r'ATTACH (?:IF NOT EXISTS )?\'[^\']*\' AS "((?:[^"]|"")*)"(?:\s*\(TYPE (\w+))?', re.IGNORECASE
)
_DETACH_HEAD = re.compile(r'DETACH DATABASE (?:IF EXISTS )?"((?:[^"]|"")*)"', re.IGNORECASE)
_DROP_SECRET_HEAD = re.compile(r"DROP SECRET (?:IF EXISTS )?(\S+?);?$", re.IGNORECASE)


class _Rows:
    """What ``sql()`` answers, read as DuckDB 2.0 allows it: ``fetchall()`` only, no ``fetchone()``."""

    def __init__(self, rows):
        self.rows = list(rows)

    def fetchall(self):
        return list(self.rows)


class RecordingDuck:
    """
    Stands in for the duckdb module: records statements, answers a one-row frame, and keeps what
    DuckDB would keep of the statements that matter here: the secrets (name, type, scopes), the
    attached databases (alias, type), which extensions are loaded and the ``search_path``, so
    ``duckdb_secrets()``, ``duckdb_databases()``, ``duckdb_extensions()`` and
    ``current_setting('search_path')`` answer what the statements built.
    """

    def __init__(self, fail_with: Exception = None, fail_on_df: bool = False):
        self.statements: List[str] = []
        self.fail_with = fail_with
        self.fail_on_df = fail_on_df  # raise when the relation is materialised, not when built
        self.fail_drop_with: Exception = None  # raise on DROP SECRET (dropping is best effort)
        self.fail_secret_with: Dict[str, Exception] = {}  # raise on CREATE SECRET, by name part
        #: Whether the AWS credential chain resolves: False models a signed-out app (the kernel
        #: server serves no container credentials), so every credential_chain secret is refused.
        self.chain_resolves = True
        self.fail_attach_with: Dict[str, Exception] = (
            {}
        )  # by attach type (athena, iceberg) or alias
        self.fail_detach_with: Optional[Exception] = None
        self.fail_search_path_with: Optional[Exception] = None  # raise on SET search_path
        self.fail_nth_search_path: Optional[int] = (
            None  # ... on that SET only (1-based); every one when None
        )
        self._search_path_sets = 0
        self.secrets: Dict[str, tuple] = {}  # name -> (type, scopes)
        self.databases: Dict[str, str] = {}  # alias -> type
        self.extensions: Set[str] = set()  # loaded extensions
        self.search_path = ""  # DuckDB's: empty by default
        self.search_paths: List[str] = []  # every value SET put there, in order

    def sql(self, statement: str):
        self.statements.append(statement)
        upper = statement.upper()
        if self.fail_drop_with is not None and statement.startswith("DROP SECRET"):
            raise self.fail_drop_with
        if "CURRENT_SETTING('SEARCH_PATH')" in upper:
            return _Rows([(self.search_path,)])
        if upper.startswith("SET SEARCH_PATH"):
            self._search_path_sets += 1
            if self.fail_search_path_with is not None and self.fail_nth_search_path in (
                None,
                self._search_path_sets,
            ):
                raise self.fail_search_path_with
            value = re.search(
                r"SET search_path = '((?:[^']|'')*)'", statement, re.IGNORECASE
            ).group(1)
            self.search_path = value.replace("''", "'")
            self.search_paths.append(self.search_path)
            return None
        if "DUCKDB_SECRETS()" in upper:
            if "STARTS_WITH(NAME, '" in upper:
                prefix = re.search(r"starts_with\(name, '([^']*)'", statement, re.IGNORECASE).group(
                    1
                )
                return _Rows((n,) for n in self.secrets if n.startswith(prefix))
            return _Rows((name, list(scopes)) for name, (_kind, scopes) in self.secrets.items())
        if "DUCKDB_DATABASES()" in upper:
            return _Rows(self.databases.items())
        if "DUCKDB_EXTENSIONS()" in upper:
            return _Rows([(1 if "athena" in self.extensions else 0,)])
        if upper.startswith("CREATE") and "SECRET" in upper:
            if not self.chain_resolves and "credential_chain" in statement:
                raise RuntimeError(
                    "Invalid Input Error: Failed to resolve AWS credentials: no credentials available"
                )
            for part, failure in self.fail_secret_with.items():
                if part in statement:
                    raise failure
            self._create_secret(statement)
            return None
        if upper.startswith("DROP SECRET"):
            match = _DROP_SECRET_HEAD.match(statement.strip())
            self.secrets.pop(match.group(1).strip('"').lower(), None)
            return None
        if upper.startswith("ATTACH"):
            match = _ATTACH_HEAD.match(statement)
            alias, kind = match.group(1).replace('""', '"'), (match.group(2) or "duckdb").lower()
            failure = self.fail_attach_with.get(kind) or self.fail_attach_with.get(alias)
            if failure is not None:
                raise failure
            self.databases.setdefault(alias, kind)
            return None
        if upper.startswith("DETACH"):
            if self.fail_detach_with is not None:
                raise self.fail_detach_with
            self.databases.pop(_DETACH_HEAD.match(statement).group(1).replace('""', '"'), None)
            return None
        if self.fail_with is not None and "select" in statement.lower() and not self.fail_on_df:
            raise self.fail_with
        if upper.startswith(("CREATE", "DROP", "SET")):
            return None
        if self.fail_with is not None and self.fail_on_df:
            return Mock(df=Mock(side_effect=self.fail_with))
        return Mock(df=lambda: DataFrame({"one": [1]}))

    def _create_secret(self, statement: str) -> None:
        match = _SECRET_HEAD.match(statement.strip())
        name, body = (match.group(1) or "").strip('"').lower(), match.group(2)
        kind = re.search(r"TYPE\s+(\w+)", body, re.IGNORECASE).group(1).lower()
        scope = re.search(r"SCOPE\s+'([^']*)'", body, re.IGNORECASE)
        scopes = (
            [scope.group(1)] if scope else (["s3://", "s3n://", "s3a://"] if kind == "s3" else [""])
        )
        self.secrets[name or f"__default_{kind}"] = (kind, scopes)

    def vend(self, table_id: str) -> None:
        """What the iceberg extension does when Glue vends credentials for a table it loads."""
        self.secrets[duckdb_catalogs.VENDED_SECRET_PREFIX + table_id] = (
            "s3",
            [f"s3://tables/{table_id}/"],
        )

    def created(self, name_part: str) -> List[str]:
        return [
            s
            for s in self.statements
            if s.startswith("CREATE OR REPLACE SECRET") and name_part in s
        ]

    def dropped(self, name_part: str) -> bool:
        return any(
            s.startswith("DROP SECRET IF EXISTS") and name_part in s for s in self.statements
        )

    def attached(self, alias_part: str = "") -> List[str]:
        return [s for s in self.statements if s.startswith("ATTACH") and alias_part in s]

    def detached(self, alias_part: str = "") -> List[str]:
        return [s for s in self.statements if s.startswith("DETACH") and alias_part in s]


class LocalSqlFixture(LocalKernelTestCase):
    """
    A local kernel against the fake app, signed in. The AWS credential chain (DuckDB's for its
    secrets, botocore's for the SDK's own look at it) resolves while the app is signed in and not
    when it is signed out, as the kernel server's container credentials would: the DuckDB stand-in
    is kept in step by :meth:`sign_out` / :meth:`sign_in`, botocore's stand-in reads the app.
    """

    def setUp(self):
        super().setUp()
        self.app.add(s3_record())
        self.app.add(
            s3_record(
                connection_id=DEFAULT_S3_CONNECTION_ID,
                name="default.s3",
                uri="s3://",
                account=None,
                region=None,
            )
        )
        self.app.add(lakehouse_record())
        self.app.add(athena_record())
        self._saved_engine = _save_engine_state()
        self._saved_catalog_state = duckdb_catalogs._state
        duckdb_catalogs._state = (
            duckdb_catalogs.LocalCatalogs()
        )  # no catalog records from another test
        self.duck = RecordingDuck()
        _fresh_engine(self.duck)
        # botocore in the kernel: its chain finds the kernel server's container credentials, which
        # are the app's signed-in session, so it answers what the fake app would have the server say.
        self._boto3 = patch.object(duckdb_catalogs, "boto3")
        self.boto3 = self._boto3.start()
        self.chain = self.boto3.Session.return_value.get_credentials
        self.chain.side_effect = self._resolve_chain

    def tearDown(self):
        self._boto3.stop()
        duckdb_catalogs._state = self._saved_catalog_state
        _restore_engine_state(self._saved_engine)
        super().tearDown()

    def _resolve_chain(self):
        if self.app.credentials is None:
            # The container provider's error, quoting the kernel server's 403 and its envelope.
            raise CredentialRetrievalError(
                provider="container-role",
                error_msg="Received non 200 response 403 from container metadata: "
                '{"error": {"code": "NoCredentials", "message": "' + SIGNED_OUT_REASON + '"}}',
            )
        return Mock(name="credentials")

    def sign_out(self):
        self.app.sign_out()
        self.duck.chain_resolves = False

    def sign_in(self, key: str = "AKIA_TEST", minutes=60):
        self.app.sign_in(key, minutes=minutes)
        self.duck.chain_resolves = True


AMBIENT_SECRET = (
    duckdb_engine._AMBIENT_S3_SECRET_NAME
)  # __default_s3: the engine's credential-chain secret

#: The engine's module globals a test replaces: saved before, put back after, all of them.
_ENGINE_STATE = (
    "_duckdb",
    "_ambient_s3_secret",
    "_ambient_s3_secret_unavailable",
    "_default_aws_credentials_disabled",
)


def _save_engine_state() -> Dict[str, object]:
    return {name: getattr(duckdb_engine, name) for name in _ENGINE_STATE}


def _restore_engine_state(saved: Dict[str, object]) -> None:
    for name, value in saved.items():
        setattr(duckdb_engine, name, value)


def _fresh_engine(duck) -> None:
    """Make ``duck`` the engine, as a new one is: no secret yet, nothing failed, the fallback on."""
    duckdb_engine._duckdb = duck
    duckdb_engine._ambient_s3_secret = False
    duckdb_engine._ambient_s3_secret_unavailable = False
    duckdb_engine._default_aws_credentials_disabled = False


def _pause_statements(duck: RecordingDuck, prefix: str):
    """
    Make the stand-in's first statement starting with ``prefix`` wait, on whichever thread runs
    it, until released: a reset, a round or a cell parked half done. Returns the ``inside`` event
    (set once that statement is reached) and the ``release`` event to let it finish.
    """
    original, inside, release = duck.sql, threading.Event(), threading.Event()

    def paused(statement):
        if statement.startswith(prefix) and not inside.is_set():
            inside.set()
            release.wait(5)
        return original(statement)

    duck.sql = paused
    return inside, release


def _in_thread(target):
    """Run ``target()`` on a thread; returns the thread and the dict its result or error lands in."""
    outcome: dict = {}

    def run():
        try:
            outcome["result"] = target()
        except Exception as e:  # noqa: BLE001 - the test reports it
            outcome["error"] = e

    thread = threading.Thread(target=run)
    thread.start()
    return thread, outcome


class DuckDbS3ReadsTest(LocalSqlFixture):
    """A cell with no connection on the local kernel: its ``s3://`` reads and the chain secret."""

    def test_a_local_statement_reading_no_s3_resolves_nothing_and_the_first_s3_read_makes_the_secret_once(
        self,
    ):
        # The fixture's engine is set up and holds no secret yet (a sign-out dropped it, say): a
        # statement reading no S3 has nothing to resolve the chain for, so the SDK does not.
        frame = sqlutils.sql("select 1 as one")
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual([s for s in self.duck.statements if "credential_chain" in s], [])
        self.assertFalse(duckdb_engine._ambient_s3_secret)
        # The first read of s3:// makes the engine's one credential-chain secret, from the chain
        # (the kernel server's container credentials), not from a connections.get call.
        sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        self.assertEqual(
            [s for s in self.duck.statements if "credential_chain" in s],
            [duckdb_engine._AMBIENT_S3_SECRET_STATEMENT],
        )
        self.assertEqual(self.duck.secrets[AMBIENT_SECRET], ("s3", ["s3://", "s3n://", "s3a://"]))
        self.assertEqual(self.app.calls, [])
        sqlutils.sql("select 2 as two")
        sqlutils.sql("select * from 's3://b/raw/returns.parquet'")
        self.assertEqual(
            len([s for s in self.duck.statements if "credential_chain" in s]), 1
        )  # once

    def test_s3_without_a_connection_reads_with_the_chain_secret_and_asks_the_app_for_nothing(self):
        frame = sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual(self.app.get_calls(), [])  # nothing is fetched from the app
        self.assertEqual(self.duck.created("aws_notebook_s3"), [])  # no per-statement secret
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)  # what signs the read, and it stays
        self.assertFalse(self.duck.dropped(AMBIENT_SECRET))
        sqlutils.sql("select 1 from 's3://elsewhere/data.parquet'")
        self.assertEqual(self.app.get_calls(), [])
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 1)

    def test_the_chain_secret_refreshes_itself_and_carries_no_region_or_scope(self):
        sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        [statement] = [s for s in self.duck.statements if "credential_chain" in s]
        self.assertEqual(
            statement, "CREATE SECRET (TYPE s3, PROVIDER credential_chain, REFRESH auto);"
        )
        self.assertNotIn("REGION", statement)
        self.assertNotIn("SCOPE", statement)
        self.assertNotIn("KEY_ID", statement)

    def test_a_profile_switch_reaches_s3_reads_through_the_frontends_attach_call(self):
        sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        self.sign_in("OTHER_PROFILE")  # the app now vends another identity

        # The chain secret caches what it resolved: the frontend's call on the switch re-creates it.
        def ambient():
            return [
                s for s in self.duck.statements if s == duckdb_engine._AMBIENT_S3_SECRET_STATEMENT
            ]

        self.assertEqual(len(ambient()), 1)
        with patch.object(duckdb_catalogs, "_list_s3_tables_catalogs", return_value=[]):
            sqlutils.attach_local_catalogs()
        self.assertTrue(self.duck.dropped(AMBIENT_SECRET))
        self.assertEqual(len(ambient()), 2)
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)
        sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        self.assertEqual(self.app.get_calls(DEFAULT_S3_CONNECTION_ID), [])

    def test_a_statement_without_s3_never_needs_credentials(self):
        self.sign_out()
        frame = sqlutils.sql("select * from range(3)")  # signed out: the engine still answers
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual(self.app.calls, [])
        self.assertEqual(self.duck.created("aws_notebook_s3"), [])
        self.assertNotIn(AMBIENT_SECRET, self.duck.secrets)

    def test_s3_without_a_connection_signed_out_is_the_typed_refusal_before_it_runs(self):
        self.sign_out()
        with self.assertRaises(CredentialsUnavailableError) as raised:
            sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        message = str(raised.exception)
        self.assertIn("Reading S3 from DuckDB has no AWS credentials", message)
        self.assertIn("Sign in to AWS", message)
        self.assertIn("Failed to resolve AWS credentials", message)  # DuckDB's reason, kept
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])
        self.assertNotIn(AMBIENT_SECRET, self.duck.secrets)
        # Signing in makes the next read resolve the chain again, with no call through the SDK.
        self.sign_in("BACK")
        self.assertIsNotNone(sqlutils.sql("select * from 's3://b/raw/orders.parquet'"))
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)
        self.assertEqual(self.app.get_calls(), [])

    def test_a_signed_out_start_tries_the_chain_only_for_a_statement_that_reads_s3(self):
        self.sign_out()
        sqlutils.sql("select 1 as one")  # nothing to resolve for: not tried
        sqlutils.sql("select 2 as two")
        self.assertEqual([s for s in self.duck.statements if "credential_chain" in s], [])
        self.assertFalse(duckdb_engine._ambient_s3_secret_unavailable)
        with self.assertRaises(CredentialsUnavailableError):
            sqlutils.sql("select * from 's3://b/x.parquet'")  # a read needs it: tried, and refused
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 1)
        self.assertTrue(duckdb_engine._ambient_s3_secret_unavailable)
        with self.assertRaises(CredentialsUnavailableError):
            sqlutils.sql(
                "select * from 's3://b/y.parquet'"
            )  # tried again: the user may have signed in
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 2)

    def test_sql_stream_without_a_connection_reads_s3_with_the_chain_secret(self):
        results = list(sqlutils.sql_stream("select 1 from 's3://b/raw/a.parquet'"))
        self.assertEqual(results[0].status, ExecutionStatus.SUCCESS.value)
        self.assertEqual(self.duck.created("aws_notebook_s3"), [])
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["connection_type"], "DUCKDB")

    def test_an_s3_connection_is_not_a_duckdb_source_in_this_mode_either(self):
        # As on SageMaker Unified Studio compute: an S3 connection has no SQL engine. Resolving a
        # connection by id is one connections.get, as for any connection; then the route refuses,
        # and nothing runs on DuckDB or is made for the statement.
        with self.assertRaisesRegex(RuntimeError, "SQL is not supported for connection type S3"):
            sqlutils.sql("select * from 's3://b/raw/orders.parquet'", connection_id="s3raw")
        self.assertEqual(len(self.app.get_calls("s3raw")), 1)
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])
        self.assertEqual(self.duck.created("aws_notebook_s3"), [])  # nothing per statement, ever

    def test_a_403_inside_duckdb_is_an_access_denial_naming_the_location(self):
        self.duck.fail_with = RuntimeError("HTTP Error: HTTP GET error on ... (HTTP 403)")
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        message = str(raised.exception)
        self.assertIn("Reading s3://b/raw/a.parquet was denied", message)
        # The chain secret is the signed-in identity's; the SDK knows no account for it.
        self.assertIn("denied to the identity the app is signed in with", message)
        self.assertIn("Switch to a profile", message)
        self.assertNotIn("expired", message)
        self.assertEqual(
            (raised.exception.location, raised.exception.account), ("s3://b/raw/a.parquet", None)
        )
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)  # a refusal does not cost the secret

    def test_an_expired_token_inside_duckdb_is_typed_as_expiry(self):
        self.duck.fail_with = RuntimeError("HTTP Error: ... <Code>ExpiredToken</Code> (HTTP 400)")
        with self.assertRaises(CredentialsExpiredError):
            sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        self.assertIn(
            AMBIENT_SECRET, self.duck.secrets
        )  # DuckDB refreshes it; the SDK drops nothing

    def test_a_refusal_raised_when_the_relation_is_materialised_is_classified_too(self):
        # DuckDB reads S3 lazily: the request can run at .df(), after .sql() returned a relation.
        self.duck.fail_with = RuntimeError("HTTP Error: HTTP GET error on ... (HTTP 403)")
        self.duck.fail_on_df = True
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        self.assertIn("Reading s3://b/raw/a.parquet was denied", str(raised.exception))

    def test_a_refusal_without_a_location_in_the_statement_still_says_what_happened(self):
        self.duck.fail_with = RuntimeError("HTTP Error: ... AccessDenied ... (HTTP 403)")
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select * from parquet_scan(getvariable('path'))")  # no s3:// in the text
        self.assertIn("This read was denied", str(raised.exception))
        self.assertEqual(raised.exception.location, "")

    def test_other_duckdb_errors_pass_through(self):
        self.duck.fail_with = RuntimeError("Parser Error: syntax error at or near")
        with self.assertRaises(RuntimeError) as raised:
            sqlutils.sql("select from")
        self.assertNotIsInstance(raised.exception, (CredentialsExpiredError, AccessDeniedError))

    def test_sql_stream_without_a_connection_runs_duckdb(self):
        results = list(sqlutils.sql_stream("select 1 as one"))
        self.assertEqual(results[0].status, ExecutionStatus.SUCCESS.value)
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["connection_type"], "DUCKDB")

    def test_lookups_by_name_are_refused(self):
        with self.assertRaises(UnsupportedInModeError):
            sqlutils.sql("select 1", connection_name="raw")

    def test_no_cell_records_the_signed_in_state_since_none_asks_the_app_for_credentials(self):
        sqlutils.sql("select 1 from 's3://b/raw/a.parquet'")
        self.assertIsNone(current_context().signed_in)  # only attach_local_catalogs() looks
        self.chain.assert_not_called()


class SecretLifecycleTest(LocalSqlFixture):
    """The credential-chain secret around local statements: what a reset or a failed drop costs."""

    def test_a_kernel_reset_drops_the_chain_secret_and_the_next_s3_read_resolves_it_again(self):
        # A kernel configured or reset after DuckDB was first used (tests, embedders, a mode
        # switch) must not keep a secret resolved under the previous configuration. The engine is
        # not set up again for it (set-up is once per kernel): the first statement that needs the
        # secret makes it, from the chain of now.
        sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        self.assertTrue(duckdb_engine._ambient_s3_secret)
        from sagemaker_studio.local_kernel import reset_local_kernel

        reset_local_kernel()
        self.assertFalse(duckdb_engine._ambient_s3_secret)
        self.assertTrue(self.duck.dropped(AMBIENT_SECRET))
        self.assertNotIn(AMBIENT_SECRET, self.duck.secrets)
        frame = sqlutils.sql("select 1 as one")  # reads no S3: nothing to resolve the chain for
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertFalse(duckdb_engine._ambient_s3_secret)
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 1)
        sqlutils.sql("select * from 's3://b/raw/returns.parquet'")
        self.assertTrue(duckdb_engine._ambient_s3_secret)  # resolved again, from the chain of now
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 2)

    def test_a_failing_drop_of_the_chain_secret_is_logged_and_the_statement_still_runs(self):
        sqlutils.sql("select * from 's3://b/raw/orders.parquet'")  # the secret exists
        self.duck.fail_drop_with = RuntimeError("engine gone")
        with self.assertLogs(
            "sagemaker_studio.sql_engine.duckdb_engine.engine", level="WARNING"
        ) as logs:
            sqlutils.detach_local_catalogs()
        self.assertFalse(duckdb_engine._ambient_s3_secret)  # forgotten even though DuckDB kept it
        self.assertIn("Could not drop DuckDB secret __default_s3", "\n".join(logs.output))
        self.duck.fail_drop_with = None
        frame = sqlutils.sql("select 1 as one")
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])

    def _pause_the_drop(self):
        """The engine's DROP of the chain secret waits until released: a reset parked half done."""
        return _pause_statements(self.duck, f"DROP SECRET IF EXISTS {AMBIENT_SECRET}")

    def _order(self, *heads):
        return [
            next(i for i, s in enumerate(self.duck.statements) if s.startswith(h)) for h in heads
        ]

    def test_a_statement_reading_s3_waits_for_a_reset_in_another_thread_and_runs_on_the_new_secret(
        self,
    ):
        # The frontend's attach_local_catalogs() on a profile switch drops and re-creates the chain
        # secret; a cell reading s3:// at that moment must not slip between the two (no secret, or a
        # CREATE racing the reset's) nor leave the flags saying what the other thread undid.
        sqlutils.sql(
            "select * from 's3://b/raw/orders.parquet'"
        )  # the secret exists, for the reset to drop
        self.duck.statements.clear()
        inside, release = self._pause_the_drop()
        reset, _ = _in_thread(lambda: duckdb_engine._reset_ambient_s3_secret(self.duck))
        self.assertTrue(inside.wait(5))
        reader, outcome = _in_thread(
            lambda: sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        )
        reader.join(0.3)
        self.assertTrue(reader.is_alive())  # waiting on the reset, not running beside it
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])
        release.set()
        reset.join(5)
        reader.join(5)
        self.assertFalse(reader.is_alive())
        self.assertNotIn("error", outcome)
        self.assertEqual(outcome["result"].to_dict("records"), [{"one": 1}])
        dropped, created, read_at = self._order("DROP SECRET IF EXISTS", "CREATE SECRET", "select")
        self.assertLess(dropped, created)
        self.assertLess(created, read_at)  # the read ran after the whole reset, on the new secret
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 1)
        self.assertTrue(duckdb_engine._ambient_s3_secret)
        self.assertIn(AMBIENT_SECRET, self.duck.secrets)

    def test_a_statement_waiting_on_a_signed_out_reset_is_refused_after_it_with_the_flags_intact(
        self,
    ):
        sqlutils.sql(
            "select * from 's3://b/raw/orders.parquet'"
        )  # the secret exists, for the reset to drop
        self.sign_out()
        self.duck.statements.clear()
        inside, release = self._pause_the_drop()
        reset, _ = _in_thread(lambda: duckdb_engine._reset_ambient_s3_secret(self.duck))
        self.assertTrue(inside.wait(5))
        reader, outcome = _in_thread(
            lambda: sqlutils.sql("select * from 's3://b/raw/orders.parquet'")
        )
        reader.join(0.3)
        self.assertTrue(reader.is_alive())
        release.set()
        reset.join(5)
        reader.join(5)
        self.assertIsInstance(outcome.get("error"), CredentialsUnavailableError)
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])
        # The reset's attempt, then the read's own retry: two, in that order, and the flags are the
        # read's own verdict, not what the reset left half-written.
        self.assertEqual(len([s for s in self.duck.statements if "credential_chain" in s]), 2)
        self.assertTrue(duckdb_engine._ambient_s3_secret_unavailable)
        self.assertFalse(duckdb_engine._ambient_s3_secret)


class EngineSecretEdgeTest(unittest.TestCase):
    """The credential-chain secret when DuckDB doesn't cooperate."""

    def setUp(self):
        self._saved_engine = _save_engine_state()
        duckdb_engine._ambient_s3_secret = False
        duckdb_engine._ambient_s3_secret_unavailable = False
        duckdb_engine._default_aws_credentials_disabled = False

    def tearDown(self):
        _restore_engine_state(self._saved_engine)

    def test_a_credential_chain_secret_that_cant_be_created_later_is_logged_not_retried(self):
        # The engine is already set up and its secret dropped (a reset); outside a local kernel the
        # next statement reading s3:// re-creates it. Without the aws extension that fails: logged,
        # the read runs and gets DuckDB's own error, and the secret is not tried again each time.
        duck = Mock()

        def refuse_secrets(statement):
            if "SECRET" in statement:
                raise RuntimeError("aws extension unavailable")
            return Mock(df=lambda: "df")

        duck.sql.side_effect = refuse_secrets
        duckdb_engine._duckdb = duck
        with patch.object(duckdb_engine.local_kernel, "is_local_kernel", return_value=False):
            with self.assertLogs(duckdb_engine.logger.name, level="WARNING") as logs:
                self.assertEqual(
                    duckdb_engine._run_local_duckdb(duck, "select * from 's3://b/k.parquet'"),
                    "df",
                )
            self.assertIn("Could not create the DuckDB S3 secret", "\n".join(logs.output))
            self.assertTrue(duckdb_engine._ambient_s3_secret_unavailable)
            duck.sql.reset_mock()
            duckdb_engine._run_local_duckdb(duck, "select * from 's3://b/k.parquet'")
        self.assertEqual(
            [c.args[0] for c in duck.sql.call_args_list], ["select * from 's3://b/k.parquet'"]
        )

    def test_the_engine_is_set_up_once_and_a_later_call_runs_nothing(self):
        # After set-up, _ensure_duckdb() is a lookup: no statement, whatever the secret's state.
        duck = Mock()
        duckdb_engine._duckdb = duck
        duckdb_engine._ambient_s3_secret = False  # dropped by a reset or sign-out
        for _ in range(3):
            self.assertIs(duckdb_engine._ensure_duckdb(), duck)
        duck.sql.assert_not_called()
        self.assertFalse(duckdb_engine._ambient_s3_secret)


class AthenaOverCatalogTest(LocalSqlFixture):
    def _capture_engine(self):
        executor = Mock()
        executor.get_supported_connection_types.return_value = ["ATHENA", "REDSHIFT"]
        executor.create_engine.return_value = Mock(name="engine")
        return executor

    def test_a_lakehouse_catalog_connection_builds_an_athena_engine(self):
        connection = sqlutils._resolve_connection("lakehouse1", None)
        executor = self._capture_engine()
        with patch.object(sqlutils, "_ensure_sql_executor", return_value=executor):
            engine = sqlutils._get_engine_from_connection(connection, connection_id="lakehouse1")

        self.assertIs(engine, executor.create_engine.return_value)
        engine_type, config = executor.create_engine.call_args.args
        self.assertEqual(engine_type, "ATHENA")
        self.assertEqual(config["work_group"], "primary")
        self.assertNotIn("catalog_name", config)

    def test_an_athena_connection_passes_its_catalog(self):
        connection = sqlutils._resolve_connection("wh", None)
        executor = self._capture_engine()
        with patch.object(sqlutils, "_ensure_sql_executor", return_value=executor):
            engine = sqlutils._get_engine_from_connection(connection, connection_id="wh")

        self.assertIs(engine, executor.create_engine.return_value)
        engine_type, config = executor.create_engine.call_args.args
        self.assertEqual(engine_type, "ATHENA")
        self.assertEqual(
            (config["work_group"], config["catalog_name"]),
            ("primary", "AwsDataCatalog"),
        )

    def test_each_cell_builds_a_native_executor_with_fresh_connection_credentials(self):
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        access_keys = []

        def create_native(connection, **_kwargs):
            access_keys.append(connection.connection_creds.access_key_id)
            executor = Mock()
            executor.execute.return_value = SingleStatementResult(result=DataFrame({"one": [1]}))
            return executor

        with patch(
            "sagemaker_studio.utils.athena_v4.athena_executor", side_effect=create_native
        ) as create_executor:
            sqlutils.sql("select 1", connection_id="lakehouse1")
            self.app.sign_in("OTHER_PROFILE", minutes=60)
            sqlutils.sql("select 2", connection_id="lakehouse1")
            list(sqlutils.sql_stream("select 3", connection_id="lakehouse1"))

        self.assertEqual(create_executor.call_count, 3)
        self.assertEqual(access_keys, ["AKIA_TEST", "OTHER_PROFILE", "OTHER_PROFILE"])
        self.assertEqual(sqlutils._connection_cache.list_keys(), [])

    def test_a_query_level_catalog_wins_over_the_connection(self):
        connection = sqlutils._resolve_connection("wh", None)
        executor = self._capture_engine()
        with patch.object(sqlutils, "_ensure_sql_executor", return_value=executor):
            engine = sqlutils._get_engine_from_connection(
                connection,
                connection_id="wh",
                catalog_name="other",
                schema_name="db",
            )

        self.assertIs(engine, executor.create_engine.return_value)
        _engine_type, config = executor.create_engine.call_args.args
        self.assertEqual((config["catalog_name"], config["schema_name"]), ("other", "db"))

    def test_a_lakehouse_connection_without_a_workgroup_is_not_sql_able(self):
        self.app.add(lakehouse_record(connection_id="nowg", workgroup=None, with_scope=False))
        executor = self._capture_engine()
        with patch.object(sqlutils, "_ensure_sql_executor", return_value=executor):
            connection = sqlutils._resolve_connection("nowg", None)
            with self.assertRaises(RuntimeError) as raised:
                sqlutils._get_engine_from_connection(connection, connection_id="nowg")
        self.assertIn("LAKEHOUSE", str(raised.exception))

    def test_the_engine_type_is_the_connections_sql_engine_type(self):
        # One rule, on Connection; sqlutils only reads it. A connection-like object without the
        # attribute (the mocks of the pre-existing tests) runs on its type.
        self.assertEqual(
            sqlutils._engine_type_of(sqlutils._resolve_connection("lakehouse1", None)), "ATHENA"
        )
        self.assertEqual(
            sqlutils._engine_type_of(sqlutils._resolve_connection("s3raw", None)), "S3"
        )
        self.assertEqual(sqlutils._engine_type_of(Mock(type="REDSHIFT")), "REDSHIFT")

    def test_async_materialization_is_skipped_and_there_is_no_project_s3_root(self):
        self.assertFalse(
            sqlutils._stream_with_async_materialization(
                "select 1", "df", connection_id="lakehouse1"
            )
        )
        self.assertIsNone(sqlutils._ensure_project_s3_root())
        self.assertEqual(self.app.calls, [])


LAKEHOUSE_CHAIN_SECRET = (
    "sagemaker_studio_catalogs_us_east_2"  # the fixture's lakehouse is in us-east-2
)
#: What a Glue ATTACH ends with on this DuckDB: ``STAGE_CREATE_TABLES false`` on 2.x, nothing on 1.x.
GLUE_UNSTAGED = ", STAGE_CREATE_TABLES false" if duckdb_catalogs._has_unstaged_creates() else ""
GLUE_ATTACH = (
    "ATTACH IF NOT EXISTS '111122223333' AS \"catalog_AwsDataCatalog\" (TYPE ICEBERG, "
    "ENDPOINT 'glue.us-east-2.amazonaws.com/iceberg', AUTHORIZATION_TYPE 'sigv4', "
    f"SECRET '{LAKEHOUSE_CHAIN_SECRET}'{GLUE_UNSTAGED});"
)


class CatalogsFixture(LocalSqlFixture):
    """
    The local-kernel fixture with the project's catalogs attached, as the kernel does at start:
    ``attach_local_catalogs()`` has run against the fixture's one lakehouse connection. Each test
    starts observing after that: the statements and app calls of the start are cleared. Tests
    about Athena connections add their own and load the ``athena`` extension on the stand-in.
    """

    def setUp(self):
        super().setUp()
        # The base fixture's Athena connection ('warehouse') serves the connection-cell tests
        # (AthenaOverCatalogTest); here it would only show up as "not attached" (no athena
        # extension on the stand-in).
        self.app.records.pop("wh", None)
        # Glue is never called from a test: the S3 Tables listing answers what the test sets.
        self._glue = patch.object(duckdb_catalogs, "_list_s3_tables_catalogs", return_value=[])
        self.s3_tables = self._glue.start()
        self.kernel_start()

    def kernel_start(self):
        """What the kernel does at start, then forget the statements and calls it took."""
        self.started_with = sqlutils.attach_local_catalogs()
        self.duck.statements.clear()
        self.app.calls.clear()

    def tearDown(self):
        self._glue.stop()
        super().tearDown()

    def _ddl(self):
        return [
            s for s in self.duck.statements if s.startswith(("ATTACH", "DETACH", "CREATE", "DROP"))
        ]


class AttachLocalCatalogsTest(CatalogsFixture):
    """``attach_local_catalogs()``: what one call puts on DuckDB, from the project's listing."""

    def kernel_start(self):
        pass  # each test runs the attach itself, to see its statements

    def test_every_lakehouse_catalog_is_attached_signing_with_the_shared_chain_secret(self):
        attached = sqlutils.attach_local_catalogs()
        self.assertEqual(self.app.list_calls(), [{}])
        # One credential_chain secret for the region, refreshed by DuckDB, scoped off every s3:// read.
        [secret] = self.duck.created(LAKEHOUSE_CHAIN_SECRET)
        self.assertEqual(
            secret,
            f"CREATE OR REPLACE SECRET {LAKEHOUSE_CHAIN_SECRET} (TYPE s3, PROVIDER credential_chain, "
            "REFRESH auto, REGION 'us-east-2', SCOPE 'sagemaker-studio-catalogs://');",
        )
        self.assertNotIn("KEY_ID", secret)  # no credentials pass through the SDK
        self.assertEqual(self.duck.attached(), [GLUE_ATTACH])
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})
        self.assertEqual(
            self.duck.secrets[LAKEHOUSE_CHAIN_SECRET], ("s3", ["sagemaker-studio-catalogs://"])
        )
        self.assertEqual(
            attached,
            [
                {
                    "alias": "catalog_AwsDataCatalog",
                    "connection_id": "lakehouse1",
                    "connection_name": "catalog",
                    "catalog": "AwsDataCatalog",
                    "route": "glue",
                    "secret": LAKEHOUSE_CHAIN_SECRET,
                    "attached": True,
                    "error": None,
                }
            ],
        )
        self.assertEqual(sqlutils.list_attached_catalogs(), attached)
        [recorded] = duckdb_catalogs._state.secrets()
        self.assertEqual(
            (recorded.name, recorded.region, recorded.role_arn, recorded.connection_id),
            (LAKEHOUSE_CHAIN_SECRET, "us-east-2", None, None),
        )
        # No connection's credentials are fetched: the listing carries none, the secrets resolve the
        # chain, and the Glue call listing the S3 Tables catalogs signs with the chain too.
        self.assertEqual(self.app.get_calls(), [])
        self.assertEqual(len(self.app.list_calls()), 1)
        self.s3_tables.assert_called_once_with(
            "111122223333", "us-east-2", None
        )  # the connection's account

    def test_s3_tables_catalogs_are_attached_each_on_its_own_under_the_data_explorer_names(self):
        self.s3_tables.return_value = ["orders", "returns"]
        attached = sqlutils.attach_local_catalogs()
        self.assertEqual(
            [c["alias"] for c in attached],
            ["catalog_AwsDataCatalog", "catalog_orders", "catalog_returns"],
        )
        self.assertIn(
            "ATTACH IF NOT EXISTS '111122223333:s3tablescatalog/orders' AS \"catalog_orders\" (TYPE ICEBERG, ",
            " ".join(self.duck.attached("catalog_orders")),
        )
        self.assertEqual(
            len(self.duck.created(LAKEHOUSE_CHAIN_SECRET)), 1
        )  # one secret, three catalogs

    def test_connections_in_two_regions_get_a_shared_secret_each(self):
        self.app.add(
            lakehouse_record(
                connection_id="west", name="west.catalog", workgroup=None, region="us-west-2"
            )
        )
        self.app.add(
            lakehouse_record(
                connection_id="west2", name="west2.catalog", workgroup=None, region="us-west-2"
            )
        )
        sqlutils.attach_local_catalogs()
        self.assertEqual(len(self.duck.created(LAKEHOUSE_CHAIN_SECRET)), 1)
        [west] = self.duck.created("sagemaker_studio_catalogs_us_west_2")
        self.assertIn("REGION 'us-west-2'", west)
        self.assertTrue(
            all(
                "SECRET 'sagemaker_studio_catalogs_us_west_2'" in s
                for s in self.duck.attached("west")
            )
        )
        self.assertEqual(
            set(self.duck.secrets),
            {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET, "sagemaker_studio_catalogs_us_west_2"},
        )

    def test_the_default_catalog_connections_catalogs_keep_their_names(self):
        self.app.add(
            lakehouse_record(
                connection_id="default_catalog", name="default.catalog", workgroup=None
            )
        )
        attached = sqlutils.attach_local_catalogs()
        self.assertEqual(
            [c["alias"] for c in attached], ["AwsDataCatalog", "catalog_AwsDataCatalog"]
        )

    def test_a_connection_naming_an_access_role_gets_a_secret_assuming_it(self):
        role = "arn:aws:iam::444455556666:role/lake-reader"
        self.app.add(
            lakehouse_record(
                connection_id="shared_lh", name="shared.catalog", workgroup=None, access_role=role
            )
        )
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        [secret] = self.duck.created("sagemaker_studio_catalogs_role_shared_lh")
        self.assertEqual(
            secret,
            "CREATE OR REPLACE SECRET sagemaker_studio_catalogs_role_shared_lh (TYPE s3, PROVIDER credential_chain, "
            f"CHAIN 'sts', ASSUME_ROLE_ARN '{role}', REFRESH auto, REGION 'us-east-2', "
            "SCOPE 'sagemaker-studio-catalogs://');",
        )
        self.assertEqual(
            attached["shared_AwsDataCatalog"]["secret"], "sagemaker_studio_catalogs_role_shared_lh"
        )
        self.assertIn(
            "SECRET 'sagemaker_studio_catalogs_role_shared_lh'",
            self.duck.attached("shared_AwsDataCatalog")[0],
        )
        self.assertEqual(
            attached["catalog_AwsDataCatalog"]["secret"], LAKEHOUSE_CHAIN_SECRET
        )  # the others share
        [recorded] = [s for s in duckdb_catalogs._state.secrets() if s.role_arn]
        self.assertEqual((recorded.role_arn, recorded.connection_id), (role, "shared_lh"))
        # Its S3 Tables catalogs are listed as that role too, assumed from the chain, not fetched.
        self.assertIn(call("111122223333", "us-east-2", role), self.s3_tables.call_args_list)
        self.assertEqual(self.app.get_calls(), [])

    def test_an_athena_connection_is_attached_as_its_workgroup_with_the_regions_shared_secret(self):
        self.app.add(
            athena_record(
                connection_id="sales_sql",
                name="sales.sql",
                workgroup="wg-sales",
                region="us-west-2",
            )
        )
        self.duck.extensions.add("athena")
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertEqual(
            attached["sales"],
            {
                "alias": "sales",
                "connection_id": "sales_sql",
                "connection_name": "sales.sql",
                "catalog": "AwsDataCatalog",
                "route": "athena",
                "secret": "sagemaker_studio_catalogs_us_west_2",
                "attached": True,
                "error": None,
            },
        )
        self.assertEqual(
            self.duck.attached("sales"),
            [
                "ATTACH IF NOT EXISTS 'athena://us-west-2/wg-sales' AS \"sales\" "
                "(TYPE athena, SECRET 'sagemaker_studio_catalogs_us_west_2');"
            ],
        )
        self.assertFalse(
            any("TYPE aws" in s for s in self.duck.statements)
        )  # the s3 chain secret serves Athena too
        self.assertEqual(
            self.app.get_calls("sales_sql"), []
        )  # nothing of the connection is fetched
        self.assertEqual(
            self.duck.databases, {"catalog_AwsDataCatalog": "iceberg", "sales": "athena"}
        )

    def test_a_lakehouse_catalog_goes_through_glue_even_with_its_paired_athena_connection_listed(
        self,
    ):
        self.app.add(
            lakehouse_record(
                connection_id="sales_lh", name="sales.catalog", workgroup=None, region="us-west-2"
            )
        )
        self.app.add(
            athena_record(
                connection_id="sales_sql",
                name="sales.sql",
                workgroup="wg-sales",
                region="us-west-2",
            )
        )
        self.s3_tables.return_value = ["orders"]
        self.duck.extensions.add("athena")
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        # The pair is two entries: each Glue catalog of the lakehouse connection on its own, and
        # the Athena connection as its workgroup. Nothing of the lakehouse connection goes through Athena.
        self.assertEqual(
            {alias: (c["route"], c["connection_id"]) for alias, c in attached.items()},
            {
                "catalog_AwsDataCatalog": ("glue", "lakehouse1"),
                "catalog_orders": ("glue", "lakehouse1"),
                "sales_AwsDataCatalog": ("glue", "sales_lh"),
                "sales_orders": ("glue", "sales_lh"),
                "sales": ("athena", "sales_sql"),
            },
        )
        self.assertTrue(all("TYPE ICEBERG" in s for s in self.duck.attached("sales_")))
        self.assertEqual(len(self.duck.attached("'athena://")), 1)
        self.assertEqual(
            set(self.duck.secrets),
            {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET, "sagemaker_studio_catalogs_us_west_2"},
        )

    def test_an_athena_connection_naming_an_access_role_or_another_catalog_or_no_workgroup(self):
        role = "arn:aws:iam::111122223333:role/x"
        self.app.add(athena_record(connection_id="role_sql", name="role.sql", access_role=role))
        self.app.add(
            athena_record(
                connection_id="hive", name="hive.sql", workgroup="wg", catalog="hive_catalog"
            )
        )
        self.app.add(
            athena_record(connection_id="plain", name="plain", workgroup=None, region="eu-west-1")
        )
        self.duck.extensions.add("athena")
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertEqual(attached["role"]["secret"], "sagemaker_studio_catalogs_role_role_sql")
        self.assertIn(
            f"ASSUME_ROLE_ARN '{role}'",
            self.duck.created("sagemaker_studio_catalogs_role_role_sql")[0],
        )
        self.assertTrue(
            self.duck.attached("hive")[0].endswith(
                "(TYPE athena, SECRET 'sagemaker_studio_catalogs_us_west_2', CATALOG 'hive_catalog');"
            )
        )
        self.assertEqual(attached["hive"]["catalog"], "hive_catalog")
        self.assertEqual(
            self.duck.attached("plain"),
            [
                "ATTACH IF NOT EXISTS 'athena://eu-west-1' AS \"plain\" (TYPE athena, SECRET 'sagemaker_studio_catalogs_eu_west_1');"
            ],
        )

    def test_without_the_athena_extension_an_athena_connection_is_reported_not_attached(self):
        self.app.add(athena_record(connection_id="sales_sql", name="sales.sql"))
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertTrue(
            any("athena DuckDB extension is not loaded" in line for line in logs.output)
        )
        sales = attached["sales"]
        self.assertEqual(
            (sales["attached"], sales["route"], sales["connection_id"], sales["secret"]),
            (False, "athena", "sales_sql", None),
        )
        self.assertIn("athena DuckDB extension is not loaded", sales["error"])
        self.assertIn("attach_local_catalogs()", sales["error"])
        self.assertEqual(self.duck.attached("'athena://"), [])
        self.assertNotIn(
            "sagemaker_studio_catalogs_us_west_2", self.duck.secrets
        )  # no secret for nothing
        self.assertTrue(
            attached["catalog_AwsDataCatalog"]["attached"]
        )  # the lakehouse connection is unaffected
        # The next call with the extension loaded attaches it; the record is replaced.
        self.duck.extensions.add("athena")
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertEqual((attached["sales"]["attached"], attached["sales"]["error"]), (True, None))

    def test_a_connection_naming_no_aws_location_is_reported_not_attached_like_any_failure(self):
        nowhere = lakehouse_record(connection_id="lh_nowhere", name="nowhere.catalog")
        nowhere["physicalEndpoints"] = []
        self.app.add(nowhere)
        sales = athena_record(connection_id="sales_sql", name="sales.sql")
        sales["physicalEndpoints"] = []
        self.app.add(sales)
        self.duck.extensions.add("athena")
        with self.assertLogs(duckdb_catalogs.logger.name, level="INFO") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        # Neither vanishes from the listing: each has its entry, with the reason.
        nowhere_entry, sales_entry = attached["nowhere_AwsDataCatalog"], attached["sales"]
        self.assertEqual(
            (
                nowhere_entry["attached"],
                nowhere_entry["route"],
                nowhere_entry["connection_id"],
                nowhere_entry["secret"],
            ),
            (False, "glue", "lh_nowhere", None),
        )
        self.assertIn("names no AWS account or region", nowhere_entry["error"])
        self.assertEqual(
            (
                sales_entry["attached"],
                sales_entry["route"],
                sales_entry["connection_id"],
                sales_entry["secret"],
            ),
            (False, "athena", "sales_sql", None),
        )
        self.assertIn("names no AWS region", sales_entry["error"])
        self.assertEqual(
            sum("not attached: the connection names no AWS" in line for line in logs.output), 2
        )
        self.assertEqual(
            (self.duck.attached("nowhere"), self.duck.attached("'athena://")), ([], [])
        )
        # The located connection is unaffected.
        self.assertTrue(attached["catalog_AwsDataCatalog"]["attached"])

    def test_signed_out_nothing_is_attached_and_no_secret_is_made(self):
        self.sign_out()
        self.assertEqual(sqlutils.attach_local_catalogs(), [])
        self.assertEqual(self.app.get_calls(), [])
        self.assertEqual((self.duck.attached(), self.duck.secrets), ([], {}))

    def test_the_call_records_what_the_chain_resolves_as_the_signed_in_state(self):
        self.assertIsNone(current_context().signed_in)  # nothing has looked yet
        sqlutils.attach_local_catalogs()
        context = current_context()
        self.assertEqual((context.signed_in, context.signed_in_detail), (True, ""))
        self.assertEqual(self.chain.call_count, 1)  # one look at the chain per call ...
        self.assertEqual(self.app.get_calls(), [])  # ... and still no connection's credentials
        self.sign_out()
        sqlutils.attach_local_catalogs()
        context = current_context()
        # The reason is the app's own, out of the envelope the kernel server answered botocore with.
        self.assertEqual((context.signed_in, context.signed_in_detail), (False, SIGNED_OUT_REASON))
        self.assertEqual(self.chain.call_count, 2)
        self.assertEqual(self.app.get_calls(), [])

    def test_a_chain_that_cannot_be_looked_at_is_recorded_not_raised(self):
        self.chain.side_effect = RuntimeError("botocore is broken today")
        attached = sqlutils.attach_local_catalogs()  # the attach goes ahead regardless
        self.assertEqual([c["alias"] for c in attached], ["catalog_AwsDataCatalog"])
        context = current_context()
        self.assertEqual(
            (context.signed_in, context.signed_in_detail), (False, "botocore is broken today")
        )

    def test_a_secret_duckdb_cannot_create_is_reported_on_the_connection_and_does_not_stop_the_others(
        self,
    ):
        # credential_chain resolves credentials at CREATE SECRET: with none to resolve, DuckDB refuses.
        self.app.add(
            lakehouse_record(
                connection_id="west", name="west.catalog", workgroup=None, region="us-west-2"
            )
        )
        self.app.add(
            athena_record(
                connection_id="west_sql", name="west.sql", workgroup="wg-west", region="us-west-2"
            )
        )
        self.duck.extensions.add("athena")
        self.duck.fail_secret_with["sagemaker_studio_catalogs_us_west_2"] = RuntimeError(
            "Invalid Input Error: Failed to resolve AWS credentials"
        )
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        west = attached["west_AwsDataCatalog"]
        self.assertEqual(
            (west["attached"], west["connection_id"], west["secret"]), (False, "west", None)
        )
        self.assertIn("Failed to resolve AWS credentials", west["error"])
        self.assertEqual(self.duck.attached("west"), [])
        # The Athena connection of the region wants the same secret: reported the same way, and
        # the secret is asked of DuckDB again for it, not remembered as made.
        west_sql = attached["west"]
        self.assertEqual(
            (
                west_sql["attached"],
                west_sql["route"],
                west_sql["connection_id"],
                west_sql["secret"],
            ),
            (False, "athena", "west_sql", None),
        )
        self.assertIn("Failed to resolve AWS credentials", west_sql["error"])
        self.assertEqual(self.duck.attached("'athena://"), [])
        self.assertEqual(len(self.duck.created("sagemaker_studio_catalogs_us_west_2")), 2)
        self.assertTrue(attached["catalog_AwsDataCatalog"]["attached"])
        self.assertEqual(set(self.duck.secrets), {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET})

    def test_a_failing_s3_tables_listing_still_attaches_the_aws_data_catalog(self):
        self.s3_tables.side_effect = RuntimeError("AccessDeniedException: glue:GetCatalogs")
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            attached = sqlutils.attach_local_catalogs()
        self.assertEqual([c["alias"] for c in attached], ["catalog_AwsDataCatalog"])
        self.assertTrue(any("S3 Tables" in line for line in logs.output))

    def test_an_attach_that_fails_is_reported_and_does_not_stop_the_others(self):
        self.app.add(
            lakehouse_record(connection_id="broken", name="broken.catalog", workgroup=None)
        )
        self.duck.fail_attach_with["broken_AwsDataCatalog"] = RuntimeError(
            "HTTP 403 from glue.us-east-2.amazonaws.com"
        )
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        broken = attached["broken_AwsDataCatalog"]
        self.assertEqual((broken["attached"], broken["secret"]), (False, LAKEHOUSE_CHAIN_SECRET))
        self.assertIn("glue: HTTP 403", broken["error"])
        self.assertTrue(attached["catalog_AwsDataCatalog"]["attached"])
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})

    def test_two_connections_wanting_one_alias_first_come_first_served(self):
        self.app.add(
            athena_record(connection_id="clash", name="catalog_AwsDataCatalog.sql")
        )  # alias catalog_AwsDataCatalog
        self.duck.extensions.add("athena")
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertTrue(
            any(
                "already attaches a database as 'catalog_AwsDataCatalog'" in line
                for line in logs.output
            )
        )
        self.assertEqual(attached["catalog_AwsDataCatalog"]["connection_id"], "lakehouse1")
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})

    def test_a_holder_whose_attach_failed_keeps_its_alias_so_it_means_one_connection(self):
        # alias catalog_AwsDataCatalog, the fixture's lakehouse catalog's
        self.app.add(athena_record(connection_id="clash", name="catalog_AwsDataCatalog.sql"))
        self.duck.extensions.add("athena")
        self.duck.fail_attach_with["catalog_AwsDataCatalog"] = RuntimeError("HTTP 403 from glue")
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        # The lakehouse connection is first in line and holds the alias although its ATTACH failed:
        # the Athena connection is not attached, and the warning says why, not that a database is
        # already attached under the alias.
        holder = attached["catalog_AwsDataCatalog"]
        self.assertEqual((holder["connection_id"], holder["attached"]), ("lakehouse1", False))
        self.assertIn("glue: HTTP 403", holder["error"])
        self.assertEqual(self.duck.attached("'athena://"), [])
        self.assertEqual(self.duck.databases, {})
        warning = next(line for line in logs.output if "catalog_AwsDataCatalog.sql" in line)
        self.assertIn("is connection 'catalog''s, whose attach failed (glue: HTTP 403", warning)
        self.assertNotIn("already attaches", warning)
        # Once the failure clears, the alias is the same connection's catalog, not another's.
        self.duck.fail_attach_with.clear()
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        holder = attached["catalog_AwsDataCatalog"]
        self.assertEqual((holder["connection_id"], holder["attached"]), ("lakehouse1", True))
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})

    def test_a_refused_listing_is_raised_and_leaves_what_was_attached(self):
        sqlutils.attach_local_catalogs()
        self.app.raw_list_response = (
            500,
            b'{"error": {"code": "InternalFailure", "message": "x"}}',
            "application/json",
        )
        self.duck.statements.clear()
        with self.assertRaises(RuntimeError) as raised:
            sqlutils.attach_local_catalogs()
        # ConnectionService's translation, as for every listing through it: the app's reason kept.
        self.assertIs(type(raised.exception), RuntimeError)
        self.assertIn("InternalFailure", str(raised.exception))
        self.assertEqual(self._ddl(), [])  # nothing detached or dropped on a listing that failed
        self.assertEqual(
            [c["alias"] for c in sqlutils.list_attached_catalogs()], ["catalog_AwsDataCatalog"]
        )

    def test_a_refused_listing_is_also_a_warning_since_the_frontends_call_shows_the_user_nothing(
        self,
    ):
        self.app.raw_list_response = (
            500,
            b'{"error": {"code": "InternalFailure", "message": "x"}}',
            "application/json",
        )
        with self.assertLogs(sqlutils.logger.name, level="WARNING") as logs, self.assertRaises(
            RuntimeError
        ):
            sqlutils.attach_local_catalogs()
        [line] = logs.output
        self.assertIn(
            "Could not list the project's connections; the attached catalogs are unchanged", line
        )
        self.assertIn("InternalFailure", line)

    def test_a_round_logs_what_it_listed_and_what_it_attached(self):
        # Enough to follow a round in the kernel's log at INFO: the listing's counts at the start,
        # every attach, and one line with the outcome and how long it took.
        self.app.add(athena_record(connection_id="wg", name="warehouse.sql", workgroup="wg"))
        self.duck.extensions.add("athena")
        self.duck.fail_attach_with["athena"] = RuntimeError("HTTP 403")
        with self.assertLogs(duckdb_catalogs.logger.name, level="INFO") as logs:
            sqlutils.attach_local_catalogs()
        lines = "\n".join(logs.output)
        self.assertIn(
            "Attaching the project's catalogs to DuckDB: 4 connection(s) listed, 1 lakehouse and 1 Athena",
            lines,
        )
        self.assertIn(
            "Attached 'AwsDataCatalog' of connection 'catalog' as 'catalog_AwsDataCatalog' through glue",
            lines,
        )
        self.assertIn("Catalog round done in ", lines)
        self.assertIn("1 database(s) attached, 1 not (warehouse)", lines)
        # A failed ATTACH is a WARNING naming the connection, not a notice.
        self.assertTrue(
            any(
                line.startswith("WARNING")
                and "Could not attach 'AwsDataCatalog' of connection 'warehouse.sql' as 'warehouse' through athena: HTTP 403"
                in line
                for line in logs.output
            )
        )
        # A connection that is not attached is a WARNING too.
        self.duck.fail_attach_with.clear()
        self.app.records["wg"]["physicalEndpoints"] = []
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            sqlutils.attach_local_catalogs()
        self.assertTrue(
            any(
                "'warehouse.sql' not attached: the connection names no AWS region" in line
                for line in logs.output
            )
        )

    def test_a_cross_account_connections_table_buckets_are_listed_under_its_own_account(self):
        # Glue GetCatalogs lists the caller's account unless told otherwise; a connection in another
        # account is listed under that account (ParentCatalogId), signed as its catalogs are.
        self.app.add(
            lakehouse_record(
                connection_id="other",
                name="other.catalog",
                workgroup=None,
                account="999988887777",
                region="eu-west-1",
            )
        )
        self.s3_tables.side_effect = lambda account, region, role=None: (
            ["shared_bucket"] if account == "999988887777" else []
        )
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertIn(call("999988887777", "eu-west-1", None), self.s3_tables.call_args_list)
        self.assertIn(call("111122223333", "us-east-2", None), self.s3_tables.call_args_list)
        self.assertEqual(attached["other_shared_bucket"]["catalog"], "shared_bucket")
        self.assertIn(
            "ATTACH IF NOT EXISTS '999988887777:s3tablescatalog/shared_bucket' AS \"other_shared_bucket\"",
            "\n".join(self.duck.attached()),
        )

    def test_a_failure_does_not_take_the_record_of_the_connection_holding_the_alias(self):
        # An Athena connection wanting the fixture's lakehouse catalog's alias, and not attachable
        # (no region): its failure goes to the log, since the alias's record is the holder's.
        clash = athena_record(connection_id="clash", name="catalog_AwsDataCatalog.sql")
        clash["physicalEndpoints"] = []
        self.app.add(clash)
        self.duck.extensions.add("athena")
        with self.assertLogs(duckdb_catalogs.logger.name, level="INFO") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        holder = attached["catalog_AwsDataCatalog"]
        self.assertEqual(
            (holder["connection_id"], holder["attached"], holder["error"]),
            ("lakehouse1", True, None),
        )
        self.assertNotIn("clash", [c["connection_id"] for c in attached.values()])
        self.assertTrue(
            any(
                "'catalog_AwsDataCatalog.sql' not attached: the connection names no AWS region"
                in line
                for line in logs.output
            )
        )


class EveryChangeStartsOverTest(CatalogsFixture):
    """The frontend calls ``attach_local_catalogs()`` on every change: each call starts over."""

    def test_calling_again_detaches_drops_and_attaches_afresh(self):
        sqlutils.attach_local_catalogs()
        heads = [s.split(" ")[0] for s in self._ddl()]
        # The engine's chain secret first (dropped, resolved again), then the catalogs.
        self.assertEqual(heads, ["DROP", "CREATE", "DETACH", "DROP", "CREATE", "ATTACH"])
        self.assertEqual(self._ddl()[0], f"DROP SECRET IF EXISTS {AMBIENT_SECRET};")
        self.assertEqual(self._ddl()[1], duckdb_engine._AMBIENT_S3_SECRET_STATEMENT)
        self.assertEqual(
            self.duck.detached(), ['DETACH DATABASE IF EXISTS "catalog_AwsDataCatalog";']
        )
        self.assertTrue(self.duck.dropped(LAKEHOUSE_CHAIN_SECRET))
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})
        self.assertEqual(set(self.duck.secrets), {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET})

    def test_a_profile_switch_leaves_nothing_of_the_previous_profile(self):
        self.duck.vend("t-0001")  # the iceberg extension loaded a table of profile A's
        self.app.records.clear()  # the app signs in to another profile and lists its connections
        self.app.add(
            s3_record(
                connection_id=DEFAULT_S3_CONNECTION_ID,
                name="default.s3",
                uri="s3://",
                account=None,
                region=None,
            )
        )
        self.app.add(
            lakehouse_record(
                connection_id="default_catalog",
                name="default.catalog",
                workgroup=None,
                account="222222222222",
                region="eu-west-1",
            )
        )
        self.app.sign_in("PROFILE_B", minutes=60)
        attached = sqlutils.attach_local_catalogs()
        self.assertEqual(
            self.duck.detached(), ['DETACH DATABASE IF EXISTS "catalog_AwsDataCatalog";']
        )
        self.assertTrue(self.duck.dropped(LAKEHOUSE_CHAIN_SECRET))
        self.assertTrue(self.duck.dropped("__internal_ic_t-0001"))
        self.assertEqual(
            self.duck.attached(),
            [
                "ATTACH IF NOT EXISTS '222222222222' AS \"AwsDataCatalog\" (TYPE ICEBERG, "
                "ENDPOINT 'glue.eu-west-1.amazonaws.com/iceberg', AUTHORIZATION_TYPE 'sigv4', "
                f"SECRET 'sagemaker_studio_catalogs_eu_west_1'{GLUE_UNSTAGED});"
            ],
        )
        # DuckDB holds profile B's catalog and secret, and nothing of profile A's.
        self.assertEqual(self.duck.databases, {"AwsDataCatalog": "iceberg"})
        self.assertEqual(
            set(self.duck.secrets), {AMBIENT_SECRET, "sagemaker_studio_catalogs_eu_west_1"}
        )
        self.assertEqual([c["alias"] for c in attached], ["AwsDataCatalog"])

    def test_a_sign_out_clears_everything_and_a_sign_in_attaches_again(self):
        self.assertTrue(current_context().signed_in)  # the kernel start's look at the chain
        self.sign_out()
        self.assertEqual(sqlutils.attach_local_catalogs(), [])
        # Nothing of the previous identity: no catalog, no catalog secret, and no chain secret
        # either (dropped, and the chain has nothing to resolve while signed out).
        self.assertEqual((self.duck.databases, self.duck.secrets), ({}, {}))
        self.assertEqual(sqlutils.list_attached_catalogs(), [])
        self.assertEqual(
            (current_context().signed_in, current_context().signed_in_detail),
            (False, SIGNED_OUT_REASON),
        )
        with self.assertRaises(CredentialsUnavailableError):
            sqlutils.sql("select 1 from 's3://b/x.parquet'")
        self.sign_in("BACK")
        sqlutils.attach_local_catalogs()
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})
        self.assertEqual(set(self.duck.secrets), {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET})
        self.assertEqual(
            (current_context().signed_in, current_context().signed_in_detail), (True, "")
        )
        self.assertIsNotNone(sqlutils.sql("select 1 from 's3://b/x.parquet'"))

    def test_detach_local_catalogs_clears_everything_at_once(self):
        self.duck.vend("t-0002")
        with self.assertLogs(level="INFO") as logs:
            sqlutils.detach_local_catalogs()
        self.assertEqual((self.duck.databases, self.duck.secrets), ({}, {}))  # the chain secret too
        # The sign-out and what it took, in the log.
        self.assertTrue(
            any("Detaching the project's catalogs from DuckDB" in line for line in logs.output)
        )
        self.assertTrue(
            any(
                "Detached 1 of 1 database(s) and dropped 2 secret(s)" in line
                for line in logs.output
            )
        )
        self.assertEqual(sqlutils.list_attached_catalogs(), [])
        self.assertTrue(duckdb_catalogs._state.empty())
        self.assertFalse(duckdb_engine._ambient_s3_secret)
        # Still signed in (the frontend called this early, or for its own reasons): the next read
        # resolves the chain again rather than failing.
        self.assertIsNotNone(sqlutils.sql("select 1 from 's3://b/x.parquet'"))
        self.assertEqual(set(self.duck.secrets), {AMBIENT_SECRET})

    def test_a_users_own_database_and_secrets_are_left_alone(self):
        self.duck.sql("ATTACH 'mine.duckdb' AS \"mine\";")
        self.duck.sql(
            "CREATE SECRET mine (TYPE s3, KEY_ID 'k', SECRET 's', SCOPE 's3://my-bucket/');"
        )
        sqlutils.attach_local_catalogs()
        self.assertEqual(
            self.duck.detached(), ['DETACH DATABASE IF EXISTS "catalog_AwsDataCatalog";']
        )
        self.assertIn("mine", self.duck.databases)
        self.assertIn("mine", self.duck.secrets)
        self.assertFalse(self.duck.dropped("mine"))

    def test_a_removed_connection_is_gone_after_the_next_call(self):
        self.app.add(
            lakehouse_record(
                connection_id="sales_lh", name="sales.catalog", workgroup=None, region="us-west-2"
            )
        )
        sqlutils.attach_local_catalogs()
        self.assertIn("sales_AwsDataCatalog", self.duck.databases)
        del self.app.records[
            "sales_lh"
        ]  # the user removes the connection; the frontend calls again
        sqlutils.attach_local_catalogs()
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})
        self.assertEqual(
            set(self.duck.secrets), {AMBIENT_SECRET, LAKEHOUSE_CHAIN_SECRET}
        )  # us-west-2's shared secret went with it
        self.assertEqual(
            [c["alias"] for c in sqlutils.list_attached_catalogs()], ["catalog_AwsDataCatalog"]
        )

    def test_a_database_duckdb_will_not_detach_stays_on_record_and_nothing_is_attached_over_it(
        self,
    ):
        self.app.records["lakehouse1"] = lakehouse_record(
            account="999999999999", workgroup=None
        )  # same alias, new target
        self.duck.fail_detach_with = RuntimeError("database is in use")
        with self.assertLogs(duckdb_catalogs.logger.name, level="WARNING") as logs:
            attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertIn("catalog_AwsDataCatalog", self.duck.databases)  # the previous one is there
        self.assertEqual(self.duck.attached(), [])  # not attached over it
        self.assertTrue(self.duck.dropped(LAKEHOUSE_CHAIN_SECRET))  # its secret went all the same
        kept = attached["catalog_AwsDataCatalog"]
        self.assertTrue(kept["attached"])
        self.assertIn("still the previous database", kept["error"])
        self.assertIn("attach_local_catalogs() tries again", kept["error"])
        self.assertTrue(any("still the previous database" in line for line in logs.output))
        # The refused DETACH is a WARNING, and the round's summary names what stayed.
        self.assertTrue(
            any(
                line.startswith("WARNING")
                and "Could not detach 'catalog_AwsDataCatalog': database is in use" in line
                for line in logs.output
            )
        )
        with self.assertLogs(duckdb_catalogs.logger.name, level="INFO") as logs:
            sqlutils.attach_local_catalogs()
        self.assertTrue(
            any(
                "Detached 0 of 1 database(s) and dropped 1 secret(s); still attached: catalog_AwsDataCatalog"
                in line
                for line in logs.output
            )
        )
        # The next call tries again; once DuckDB lets go, the new target is attached and the mark is gone.
        self.duck.fail_detach_with = None
        attached = {c["alias"]: c for c in sqlutils.attach_local_catalogs()}
        self.assertEqual(
            (
                attached["catalog_AwsDataCatalog"]["attached"],
                attached["catalog_AwsDataCatalog"]["error"],
            ),
            (True, None),
        )
        self.assertIn("ATTACH IF NOT EXISTS '999999999999'", self.duck.attached()[-1])

    def test_no_cell_lists_or_refreshes_anything(self):
        sqlutils.sql("select 1 as one")
        list(sqlutils.sql_stream("select 1 as one; select 2 as two"))
        sqlutils.sql("select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1")
        self.assertEqual(self.app.list_calls(), [])
        self.assertEqual(self.app.get_calls(), [])
        self.assertEqual(self._ddl(), [])
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})
        self.assertIn(LAKEHOUSE_CHAIN_SECRET, self.duck.secrets)

    def test_a_kernel_reset_with_catalogs_attached_clears_them(self):
        from sagemaker_studio.local_kernel import reset_local_kernel

        reset_local_kernel()
        self.assertEqual(self.duck.databases, {})
        self.assertNotIn(LAKEHOUSE_CHAIN_SECRET, self.duck.secrets)
        self.assertEqual(sqlutils.list_attached_catalogs(), [])

    def test_a_kernel_reset_whose_catalog_reset_fails_still_forgets_the_project(self):
        from sagemaker_studio.local_kernel import reset_local_kernel

        self.assertIsNotNone(
            sqlutils._project
        )  # built when the fixture's round listed the connections
        with patch.object(
            duckdb_catalogs._state, "reset", side_effect=RuntimeError("DuckDB is gone")
        ):
            with self.assertLogs(duckdbutils.logger.name, level="WARNING") as logs:
                reset_local_kernel()  # best effort, like every drop: nothing raised
        self.assertIsNone(sqlutils._project)
        self.assertTrue(
            any(
                "Could not detach the attached catalogs on the kernel reset" in line
                for line in logs.output
            )
        )

    def test_a_sign_out_before_any_engine_has_nothing_to_detach(self):
        duckdb_engine._duckdb = None  # no cell or round has set the engine up
        with patch.object(duckdb_engine, "_ensure_duckdb") as ensure, self.assertLogs(
            duckdbutils.logger.name, level="INFO"
        ) as logs:
            sqlutils.detach_local_catalogs()
        ensure.assert_not_called()  # nothing is set up only to be cleared
        self.assertEqual(self.duck.statements, [])
        self.assertTrue(
            any("No DuckDB engine yet; nothing to detach" in line for line in logs.output)
        )

    def test_every_code_path_asks_for_the_engine_once(self):
        # A cell (sql, or a sql_stream of several statements), with or without a catalog on its
        # search_path, and a catalog round: each asks duckdb_engine._ensure_duckdb() exactly once,
        # at the start, and everything further down runs on what it returned.
        with patch.object(
            duckdb_engine, "_ensure_duckdb", wraps=duckdb_engine._ensure_duckdb
        ) as ensure:
            sqlutils.sql("select 1 as one")
            self.assertEqual(ensure.call_count, 1)
            sqlutils.sql(
                "select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
            )
            self.assertEqual(ensure.call_count, 2)
            results = list(
                sqlutils.sql_stream(
                    "select 1; select 2; select 3", catalog_name="catalog_AwsDataCatalog"
                )
            )
            self.assertEqual([r.status for r in results], ["success"] * 3)
            self.assertEqual(ensure.call_count, 3)
            sqlutils.attach_local_catalogs()
            self.assertEqual(ensure.call_count, 4)
            sqlutils.detach_local_catalogs()  # works on the engine it has, or none: asks for nothing
            self.assertEqual(ensure.call_count, 4)


class RoundsAndCellsTakeTurnsTest(CatalogsFixture):
    """A catalog round and a cell on two threads: one runs after the other, never beside it."""

    def _first(self, head: str) -> int:
        return next(i for i, s in enumerate(self.duck.statements) if s.startswith(head))

    def test_a_cell_arriving_during_a_round_waits_for_it_and_runs_on_what_the_round_attached(self):
        # The frontend's attach_local_catalogs() on a profile switch is half way, parked inside its
        # ATTACH, when a cell naming the catalog arrives on another thread: its search_path push and
        # its statement run after the round, on the catalog attached again, not between the
        # round's DETACH and its ATTACH.
        inside, release = _pause_statements(self.duck, "ATTACH")
        round_thread, round_outcome = _in_thread(sqlutils.attach_local_catalogs)
        self.assertTrue(inside.wait(5))
        cell, outcome = _in_thread(
            lambda: sqlutils.sql(
                "select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
            )
        )
        cell.join(0.3)
        self.assertTrue(cell.is_alive())  # waiting for the round, not running beside it
        self.assertEqual(
            [s for s in self.duck.statements if s.startswith(("SET search_path", "select"))], []
        )
        release.set()
        round_thread.join(5)
        cell.join(5)
        self.assertNotIn("error", round_outcome)
        self.assertNotIn("error", outcome)
        self.assertEqual(outcome["result"].to_dict("records"), [{"one": 1}])
        last_attach = max(i for i, s in enumerate(self.duck.statements) if s.startswith("ATTACH"))
        self.assertLess(last_attach, self._first("SET search_path"))
        self.assertLess(self._first("SET search_path"), self._first("select"))
        self.assertEqual(self.duck.databases, {"catalog_AwsDataCatalog": "iceberg"})

    def test_a_round_arriving_during_a_cell_waits_for_its_statement_and_starts_over_after_it(self):
        # The cell is inside its statement when the frontend's call arrives: the round lists (no
        # lock needed for that) and then waits; nothing is detached or dropped under the running
        # statement.
        inside, release = _pause_statements(self.duck, "select")
        cell, outcome = _in_thread(lambda: sqlutils.sql("select 1 as one"))
        self.assertTrue(inside.wait(5))
        round_thread, round_outcome = _in_thread(sqlutils.attach_local_catalogs)
        round_thread.join(0.3)
        self.assertTrue(round_thread.is_alive())
        self.assertEqual(self._ddl(), [])
        release.set()
        cell.join(5)
        round_thread.join(5)
        self.assertNotIn("error", outcome)
        self.assertNotIn("error", round_outcome)
        self.assertLess(self._first("select"), self._first("DETACH"))
        self.assertEqual(len(round_outcome["result"]), 1)

    def test_a_sign_out_arriving_during_a_cell_waits_for_its_statement_too(self):
        inside, release = _pause_statements(self.duck, "select")
        cell, outcome = _in_thread(lambda: sqlutils.sql("select 1 as one"))
        self.assertTrue(inside.wait(5))
        detach, detach_outcome = _in_thread(sqlutils.detach_local_catalogs)
        detach.join(0.3)
        self.assertTrue(detach.is_alive())
        self.assertEqual(self._ddl(), [])
        release.set()
        cell.join(5)
        detach.join(5)
        self.assertNotIn("error", outcome)
        self.assertNotIn("error", detach_outcome)
        self.assertLess(self._first("select"), self._first("DETACH"))
        self.assertEqual(self.duck.databases, {})
        self.assertNotIn(AMBIENT_SECRET, self.duck.secrets)


class DuckDbSearchPathTest(CatalogsFixture):
    """A DuckDB query's ``catalog_name``/``schema_name`` go first on DuckDB's ``search_path`` while it runs."""

    def _sets(self):
        return [s for s in self.duck.statements if s.startswith("SET search_path")]

    def test_the_catalog_and_schema_go_first_and_the_previous_search_path_comes_back(self):
        self.duck.search_path = "mine.s"  # what the user had
        frame = sqlutils.sql(
            "select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
        )
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual(self.duck.search_paths, ["catalog_AwsDataCatalog.db1,mine.s", "mine.s"])
        self.assertEqual(self.duck.search_path, "mine.s")
        # Read, set, run, put back: in that order, around the statement alone.
        heads = [
            s.split(" ")[0]
            for s in self.duck.statements
            if "search_path" in s or s.startswith("select 1")
        ]
        self.assertEqual(heads, ["SELECT", "SET", "select", "SET"])

    def test_a_catalog_alone_is_the_entry_and_names_are_quoted_as_duckdb_reads_them(self):
        self.duck.databases["my data_AwsDataCatalog"] = "iceberg"
        sqlutils.sql("select 1 as one", catalog_name="my data_AwsDataCatalog")
        sqlutils.sql("select 1 as one", catalog_name="my data_AwsDataCatalog", schema_name="1st")
        sqlutils.sql("select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="it's")
        self.assertEqual(
            [p for p in self.duck.search_paths if p],
            [
                '"my data_AwsDataCatalog"',
                '"my data_AwsDataCatalog"."1st"',
                'catalog_AwsDataCatalog."it\'s"',
            ],
        )
        self.assertEqual(
            self.duck.search_path, ""
        )  # nothing left over, and no trailing comma was ever set

    def test_the_previous_search_path_comes_back_when_the_query_fails(self):
        self.duck.fail_with = RuntimeError("Binder Error: no such table")
        with self.assertRaises(RuntimeError):
            sqlutils.sql(
                "select * from t", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
            )
        self.assertEqual(self.duck.search_paths, ["catalog_AwsDataCatalog.db1", ""])

    def test_a_restore_duckdb_refuses_never_replaces_the_cells_own_error(self):
        self.duck.search_path = "mine.s"
        self.duck.fail_with = RuntimeError(
            "Binder Error: no such table"
        )  # the error the user needs to see
        self.duck.fail_search_path_with = RuntimeError(
            'Catalog Error: SET search_path: No catalog + schema named "mine" found.'
        )
        self.duck.fail_nth_search_path = 2  # the push succeeds, the restore does not
        with self.assertLogs("sagemaker_studio.utils.duckdbutils", level="WARNING") as logs:
            with self.assertRaises(RuntimeError) as raised:
                sqlutils.sql(
                    "select * from t", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
                )
        self.assertIn("no such table", str(raised.exception))  # the cell's, not the restore's
        self.assertTrue(
            any(
                "Could not put DuckDB's search_path back to 'mine.s'" in line
                for line in logs.output
            )
        )
        self.assertEqual(
            self.duck.search_paths, ["catalog_AwsDataCatalog.db1,mine.s"]
        )  # left where the cell put it

    def test_a_restore_duckdb_refuses_after_a_successful_cell_keeps_the_frame_and_warns(self):
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: SET search_path")
        self.duck.fail_nth_search_path = 2
        with self.assertLogs("sagemaker_studio.utils.duckdbutils", level="WARNING") as logs:
            frame = sqlutils.sql(
                "select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1"
            )
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertTrue(any("search_path" in line for line in logs.output))
        # The next cell runs as usual, from where the failed restore left the search_path (which
        # is what the warning said): it pushes on top of it and puts that back.
        self.duck.fail_search_path_with = None
        sqlutils.sql("select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="db1")
        self.assertEqual(
            self.duck.search_paths[-2:],
            ["catalog_AwsDataCatalog.db1,catalog_AwsDataCatalog.db1", "catalog_AwsDataCatalog.db1"],
        )

    def test_a_streams_results_are_all_delivered_when_its_restore_fails(self):
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: SET search_path")
        self.duck.fail_nth_search_path = 2
        with self.assertLogs("sagemaker_studio.utils.duckdbutils", level="WARNING"):
            results = list(
                sqlutils.sql_stream(
                    "select 1 as one; select 2 as two",
                    catalog_name="catalog_AwsDataCatalog",
                    schema_name="db1",
                )
            )
        self.assertEqual([r.status for r in results], ["success", "success"])

    def test_a_stream_sets_it_once_for_all_its_statements_and_puts_it_back_when_exhausted(self):
        stream = sqlutils.sql_stream(
            "select 1 as one; select 2 as two",
            catalog_name="catalog_AwsDataCatalog",
            schema_name="db1",
        )
        self.assertEqual(self._sets(), [])  # nothing until the first result is asked for
        results = list(stream)
        self.assertEqual([r.status for r in results], [ExecutionStatus.SUCCESS.value] * 2)
        self.assertEqual(self.duck.search_paths, ["catalog_AwsDataCatalog.db1", ""])
        # The splitter re-spells the statements; both ran between the one SET and the one put-back.
        statements = [
            s
            for s in self.duck.statements
            if s.startswith("SET")
            or (
                s.lower().startswith("select ")
                and "duckdb_" not in s
                and "current_setting" not in s
            )
        ]
        self.assertEqual(statements[0].split(" ")[0], "SET")
        self.assertEqual(statements[-1], "SET search_path = '';")
        self.assertEqual(
            [s.lower() for s in statements[1:-1]], ["select 1 as one", "select 2 as two"]
        )

    def test_a_stream_closed_early_puts_the_search_path_back(self):
        stream = sqlutils.sql_stream(
            "select 1 as one; select 2 as two", catalog_name="catalog_AwsDataCatalog"
        )
        next(stream)
        self.assertEqual(self.duck.search_path, "catalog_AwsDataCatalog")
        stream.close()
        self.assertEqual(self.duck.search_path, "")

    def test_a_catalog_duckdb_does_not_have_is_a_typed_error_before_the_query_runs(self):
        self.duck.fail_search_path_with = RuntimeError(
            'Catalog Error: SET search_path: No catalog + schema named "nosuch" found.'
        )
        with self.assertRaises(CatalogUnavailableError) as raised:
            sqlutils.sql("select 1 as one", catalog_name="nosuch")
        self.assertIsInstance(raised.exception, LookupError)
        self.assertIn(
            "Catalog 'nosuch' is not available on the kernel's DuckDB: it is not attached",
            str(raised.exception),
        )
        self.assertIn("No catalog + schema named", str(raised.exception))
        self.assertIn("sqlutils.list_attached_catalogs()", str(raised.exception))
        self.assertEqual((raised.exception.catalog, raised.exception.schema), ("nosuch", None))
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])
        self.assertEqual(self.duck.search_paths, [])  # nothing to put back: nothing was set

    def test_a_catalog_whose_attach_failed_reports_the_attachs_reason(self):
        self.app.add(
            lakehouse_record(connection_id="broken", name="broken.catalog", workgroup=None)
        )
        self.duck.fail_attach_with["broken_AwsDataCatalog"] = RuntimeError("HTTP 403 from glue")
        sqlutils.attach_local_catalogs()
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: No catalog + schema named")
        with self.assertRaises(CatalogUnavailableError) as raised:
            sqlutils.sql("select 1 as one", catalog_name="broken_AwsDataCatalog", schema_name="db1")
        message = str(raised.exception)
        self.assertIn("Catalog 'broken_AwsDataCatalog', schema 'db1', is not available", message)
        self.assertIn("HTTP 403 from glue", message)
        self.assertIn("sqlutils.attach_local_catalogs()", message)

    def test_an_attached_catalog_without_the_schema_says_so(self):
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: No catalog + schema named")
        with self.assertRaises(CatalogUnavailableError) as raised:
            sqlutils.sql(
                "select 1 as one", catalog_name="catalog_AwsDataCatalog", schema_name="nosuch"
            )
        self.assertIn("the catalog has no schema 'nosuch'", str(raised.exception))
        with self.assertRaises(CatalogUnavailableError) as raised:
            sqlutils.sql("select 1 as one", catalog_name="catalog_AwsDataCatalog")
        self.assertIn("the catalog has no default schema", str(raised.exception))
        self.assertIn("Pass schema_name=", str(raised.exception))

    def test_a_stream_raises_the_typed_error_when_the_first_result_is_asked_for(self):
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: No catalog + schema named")
        stream = sqlutils.sql_stream("select 1 as one", catalog_name="nosuch")
        with self.assertRaises(CatalogUnavailableError):
            next(stream)
        self.assertEqual([s for s in self.duck.statements if s.startswith("select")], [])

    def test_a_streams_metadata_is_reset_when_it_is_made_not_when_it_is_first_read(self):
        # As for every other engine: sql_stream() clears the previous cell's metadata before it
        # returns, so a consumer never reads a stale entry between the call and the first next(),
        # nor after a cell that was refused before any statement ran.
        list(sqlutils.sql_stream("select 1 as one"))
        self.assertEqual(
            sqlutils._last_sql_execution_metadata[0]["statement"].lower(), "select 1 as one"
        )
        stream = sqlutils.sql_stream("select 2 as two", catalog_name="catalog_AwsDataCatalog")
        self.assertEqual(sqlutils._last_sql_execution_metadata, [])  # reset at the call
        self.assertEqual(self.duck.search_paths, [])  # the cell is not entered yet
        results = list(stream)
        self.assertEqual([r.status for r in results], ["success"])
        self.assertEqual(
            [
                (e["statement"].lower(), e["connection_type"])
                for e in sqlutils._last_sql_execution_metadata
            ],
            [("select 2 as two", "DUCKDB")],
        )
        self.duck.fail_search_path_with = RuntimeError("Catalog Error: No catalog + schema named")
        stream = sqlutils.sql_stream("select 3 as three", catalog_name="nosuch")
        self.assertEqual(sqlutils._last_sql_execution_metadata, [])
        with self.assertRaises(CatalogUnavailableError):
            next(stream)
        self.assertEqual(sqlutils._last_sql_execution_metadata, [])  # nothing of the previous cell

    def test_only_the_callers_catalog_counts_not_one_parsed_out_of_the_query(self):
        # The Athena execution context parsed out of a three-part name is not a DuckDB search_path.
        sqlutils.sql("select * from sales.db.t")
        list(sqlutils.sql_stream("select * from sales.db.t"))
        self.assertEqual(self._sets(), [])
        self.assertFalse(any("current_setting" in s for s in self.duck.statements))

    def test_a_cell_with_no_catalog_touches_the_search_path_not_at_all(self):
        sqlutils.sql("select 1 as one", schema_name="db1")  # a schema alone names no catalog
        self.assertEqual(self._sets(), [])

    def test_a_cell_with_an_athena_connection_never_reaches_duckdb(self):
        # A cell naming an Athena connection runs on the native Athena executor, whatever engine
        # its workgroup runs; DuckDB and the attached catalogs are for cells with no connection.
        self.app.add(athena_record(connection_id="wh", name="warehouse"))
        with patch(
            "sagemaker_studio.utils.athena_v4.athena_executor"
        ) as create_executor, patch.object(duckdbutils, "_duckdb_cell") as cell:
            create_executor.return_value.execute.return_value = Mock(result=DataFrame({"one": [1]}))
            sqlutils.sql(
                "select 1 as one", connection_id="wh", catalog_name="catalog_AwsDataCatalog"
            )
        create_executor.assert_called_once()
        cell.assert_not_called()
        self.assertEqual(self._sets(), [])


class RefusalNamesTheSignerTest(CatalogsFixture):
    """A 403 inside a query on an attached catalog names who signed: the role, when the catalog has one."""

    ROLE = "arn:aws:iam::444455556666:role/lake-reader"

    def setUp(self):
        super().setUp()
        self.app.add(
            lakehouse_record(
                connection_id="shared_lh",
                name="shared.catalog",
                workgroup=None,
                access_role=self.ROLE,
            )
        )
        sqlutils.attach_local_catalogs()
        self.duck.statements.clear()
        self.duck.fail_with = RuntimeError(
            "HTTP Error: HTTP GET error on 'https://glue.us-east-2.amazonaws.com/iceberg/v1/...' (HTTP 403)"
        )

    def test_a_cell_in_a_role_attached_catalog_names_the_role_and_its_connection(self):
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select 1 from t", catalog_name="shared_AwsDataCatalog", schema_name="db")
        message = str(raised.exception)
        self.assertIn(
            "Reading catalog 'shared_AwsDataCatalog' was denied to the role " + self.ROLE, message
        )
        self.assertIn("which the AWS Notebook app assumes for connection 'shared.catalog'", message)
        self.assertIn("Give the role access to it, or change the connection's access role", message)
        self.assertNotIn("Switch to a profile", message)
        self.assertEqual(
            (raised.exception.role, raised.exception.connections), (self.ROLE, ["shared.catalog"])
        )
        self.assertEqual(self.duck.search_paths[-1], "")  # the cell's search_path is still put back

    def test_a_statement_qualifying_the_role_attached_catalog_names_the_role_without_a_catalog_name(
        self,
    ):
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql('select * from "shared_AwsDataCatalog".db.t')
        self.assertEqual(raised.exception.role, self.ROLE)
        self.assertEqual(raised.exception.location, "catalog 'shared_AwsDataCatalog'")

    def test_a_catalog_signing_as_the_signed_in_identity_keeps_the_generic_message(self):
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select 1 from t", catalog_name="catalog_AwsDataCatalog", schema_name="db")
        self.assertIn("denied to the identity the app is signed in with", str(raised.exception))
        self.assertIsNone(raised.exception.role)

    def test_a_mix_of_signers_or_an_s3_path_of_the_statements_own_names_no_role(self):
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql(
                "select * from shared_AwsDataCatalog.a.t join catalog_AwsDataCatalog.b.u using (k)"
            )
        self.assertIsNone(
            raised.exception.role
        )  # two identities: the refused one cannot be told apart
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql(
                "select * from 's3://b/x.parquet'",
                catalog_name="shared_AwsDataCatalog",
                schema_name="db",
            )
        self.assertIsNone(raised.exception.role)  # the s3:// read is the signed-in identity's
        self.assertEqual(raised.exception.location, "s3://b/x.parquet")

    def test_a_search_path_duckdb_will_not_read_back_leaves_the_cells_catalog_out_of_the_message(
        self,
    ):
        # The cell's own read of the search_path (to put it back after) goes through; the
        # classifier's, for the message only, is refused: the error is still the typed one, with
        # what the statement itself names, and the cell's search_path is still put back.
        original, reads = self.duck.sql, []

        def sql(statement):
            if "current_setting('search_path')" in statement:
                reads.append(statement)
                if len(reads) == 2:
                    raise RuntimeError("no settings today")
            return original(statement)

        self.duck.sql = sql
        with self.assertRaises(AccessDeniedError) as raised:
            sqlutils.sql("select 1 from t", catalog_name="shared_AwsDataCatalog", schema_name="db")
        self.assertEqual(len(reads), 2)
        self.assertIsNone(raised.exception.role)  # the catalog on the search_path is not known
        self.assertIn("denied to the identity the app is signed in with", str(raised.exception))
        self.assertEqual(self.duck.search_paths[-1], "")


class RemoteUnchangedTest(unittest.TestCase):
    """Outside a local kernel the DuckDB path is what it always was."""

    def setUp(self):
        from sagemaker_studio.local_kernel import reset_local_kernel

        reset_local_kernel()
        self._saved_engine = _save_engine_state()
        self._saved_state = duckdb_catalogs._state
        duckdb_catalogs._state = duckdb_catalogs.LocalCatalogs()
        self.duck = RecordingDuck()
        _fresh_engine(self.duck)

    def tearDown(self):
        from sagemaker_studio.local_kernel import reset_local_kernel

        reset_local_kernel()
        duckdb_catalogs._state = self._saved_state
        _restore_engine_state(self._saved_engine)

    def _credential_chain_creates(self):
        return [s for s in self.duck.statements if "credential_chain" in s]

    def test_the_project_catalogs_attach_on_smus_compute_too_from_the_datazone_listing(self):
        """
        Not gated on the kernel: with a DataZone-backed project, ``attach_local_catalogs()`` lists
        the project's connections through its provider and attaches them the same way, the
        ``credential_chain`` secret resolving the space's own credentials.
        """
        import os

        provider = Mock()
        provider.list_connections.return_value = [
            lakehouse_record(
                connection_id="dz-lh",
                name="project.default_lakehouse",
                workgroup=None,
                region="us-west-2",
            ),
            athena_record(
                connection_id="dz-ath",
                name="project.athena",
                workgroup="wg-proj",
                region="us-west-2",
            ),
        ]
        project = Mock()
        project._connection_service = ConnectionService(
            project_id="proj",
            domain_id="dom",
            datazone_api=None,
            glue_api=Mock(),
            secrets_manager_api=Mock(),
            kms_api=Mock(),
            project_config=ClientConfig(),
            provider=provider,  # a DataZone-backed project's, here answering the listing directly
        )
        self.duck.extensions.add("athena")
        with patch.dict(os.environ, {}, clear=True), patch.object(
            sqlutils, "_ensure_project", return_value=project
        ), patch.object(
            duckdb_catalogs, "_list_s3_tables_catalogs", return_value=["tb"]
        ) as listing, patch.object(
            duckdb_catalogs, "boto3"
        ) as boto3:
            attached = sqlutils.attach_local_catalogs()
            frame = sqlutils.sql("select 1 as one", catalog_name="AwsDataCatalog", schema_name="db")
        listing.assert_called_once_with(
            "111122223333", "us-west-2", None
        )  # the connection's account and region, the space's chain
        # No local kernel to tell: the chain is not looked at, and the context is the remote one.
        boto3.Session.return_value.get_credentials.assert_not_called()
        self.assertIsNone(current_context().signed_in)
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual(
            {c["alias"]: (c["route"], c["secret"]) for c in attached},
            {
                "AwsDataCatalog": ("glue", "sagemaker_studio_catalogs_us_west_2"),
                "tb": ("glue", "sagemaker_studio_catalogs_us_west_2"),
                "project.athena": ("athena", "sagemaker_studio_catalogs_us_west_2"),
            },
        )
        provider.list_connections.assert_called_once_with()
        project.connection.assert_not_called()  # no connection's credentials: the listing signs with the chain
        self.assertEqual(self.duck.search_paths, ["AwsDataCatalog.db", ""])
        # The engine's own ambient secret and the catalogs' secret are different things.
        self.assertEqual(len(self.duck.created("sagemaker_studio_catalogs_us_west_2")), 1)
        self.assertIn("__default_s3", self.duck.secrets)

    def test_without_a_project_nothing_is_attached_and_the_cell_still_runs(self):
        import os

        with patch.dict(os.environ, {}, clear=True), patch.object(
            sqlutils, "_ensure_project", return_value=False
        ):
            with self.assertLogs("sagemaker_studio.utils.sqlutils", level="WARNING") as logs:
                self.assertEqual(sqlutils.attach_local_catalogs(), [])
            frame = sqlutils.sql("select 1 as one")
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertTrue(any("No project" in line for line in logs.output))
        self.assertEqual(
            [s for s in self.duck.statements if s.startswith(("ATTACH", "DETACH"))], []
        )

    def test_s3_statement_runs_without_any_check(self):
        import os

        with patch.dict(os.environ, {}, clear=True):
            frame = sqlutils.sql("select * from 's3://b/x.parquet'")
            sqlutils.sql("select 1")
        self.assertEqual(frame.to_dict("records"), [{"one": 1}])
        self.assertEqual(
            self.duck.created("aws_notebook_s3"), []
        )  # nothing per statement, here either
        # The credential-chain secret is created once, with REFRESH auto.
        self.assertEqual(
            self._credential_chain_creates(), [duckdb_engine._AMBIENT_S3_SECRET_STATEMENT]
        )
        self.assertIn("REFRESH auto", self._credential_chain_creates()[0])

    def test_the_credential_chain_secret_follows_a_mode_switch(self):
        """
        The engine is created once per process. A kernel configured after DuckDB was first used
        remotely must not keep the secret resolved under the remote chain: the switch drops it, and
        the local kernel resolves its own (the kernel server's container credentials) at its next
        ``s3://`` read; back to remote, the same again. No statement runs on the other mode's
        credentials, and a statement reading no S3 resolves nothing.
        """
        import os

        from sagemaker_studio.local_kernel import configure_local_kernel, reset_local_kernel

        app = FakeApp()
        try:
            with patch.dict(os.environ, {}, clear=True):
                sqlutils.sql(
                    "select * from 's3://b/x.parquet'"
                )  # remote first: the secret is created
                self.assertEqual(len(self._credential_chain_creates()), 1)
                self.assertTrue(duckdb_engine._ambient_s3_secret)

                configure_local_kernel(app.url, app.token)  # now a local kernel
                self.assertFalse(duckdb_engine._ambient_s3_secret)
                self.assertTrue(self.duck.dropped("__default_s3"))  # the remote chain's secret goes
                sqlutils.sql("select 1 as one")  # reads no S3: nothing resolved
                self.assertEqual(len(self._credential_chain_creates()), 1)
                sqlutils.sql("select * from 's3://b/y.parquet'")  # the local chain's secret
                self.assertEqual(len(self._credential_chain_creates()), 2)
                self.assertTrue(duckdb_engine._ambient_s3_secret)

                reset_local_kernel()  # back to remote: dropped, and the next s3:// read re-creates it
                self.assertFalse(duckdb_engine._ambient_s3_secret)
                sqlutils.sql("select 2")
                self.assertEqual(len(self._credential_chain_creates()), 2)
                sqlutils.sql("select * from 's3://b/z.parquet'")
                self.assertEqual(len(self._credential_chain_creates()), 3)
                self.assertTrue(duckdb_engine._ambient_s3_secret)
        finally:
            app.close()


if __name__ == "__main__":
    unittest.main()
