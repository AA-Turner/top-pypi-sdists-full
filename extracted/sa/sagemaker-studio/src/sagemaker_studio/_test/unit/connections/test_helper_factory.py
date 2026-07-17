import unittest

from sagemaker_studio.connections.helper_factory import HelperFactory
from sagemaker_studio.connections.sql_helper.athena_sql_helper import AthenaSqlHelper
from sagemaker_studio.connections.sql_helper.big_query_sql_helper import BigQuerySqlHelper
from sagemaker_studio.connections.sql_helper.ddb_sql_helper import DDBSQLHelper
from sagemaker_studio.connections.sql_helper.mssql_sql_helper import MSSQLHelper
from sagemaker_studio.connections.sql_helper.mysql_sql_helper import MySQLHelper
from sagemaker_studio.connections.sql_helper.opensearch_sql_helper import OpenSearchSQLHelper
from sagemaker_studio.connections.sql_helper.oracle_sql_helper import OracleSQLHelper
from sagemaker_studio.connections.sql_helper.postgresql_helper import PostgreSQLHelper
from sagemaker_studio.connections.sql_helper.redshift_sql_helper import RedshiftSqlHelper
from sagemaker_studio.connections.sql_helper.snowflake_sql_helper import SnowflakeSqlHelper
from sagemaker_studio.connections.sql_helper.teradata_sql_helper import TeraDataSQLHelper
from sagemaker_studio.connections.sql_helper.vertica_sql_helper import VerticaSQLHelper
from sagemaker_studio.connections.sql_helper.workday_data_connect_sql_helper import (
    WorkdayDataConnectSqlHelper,
)


class TestHelperFactory(unittest.TestCase):
    """Tests for HelperFactory.get_sql_helper covering all connection type mappings."""

    def test_athena_returns_athena_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("ATHENA"), AthenaSqlHelper)

    def test_redshift_returns_redshift_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("REDSHIFT"), RedshiftSqlHelper)

    def test_mysql_returns_mysql_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("MYSQL"), MySQLHelper)

    def test_snowflake_returns_snowflake_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("SNOWFLAKE"), SnowflakeSqlHelper)

    def test_bigquery_returns_bigquery_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("BIGQUERY"), BigQuerySqlHelper)

    def test_dynamodb_returns_ddb_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("DYNAMODB"), DDBSQLHelper)

    def test_sqlserver_returns_mssql_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("SQLSERVER"), MSSQLHelper)

    def test_postgresql_returns_postgresql_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("POSTGRESQL"), PostgreSQLHelper)

    def test_opensearch_returns_opensearch_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("OPENSEARCH"), OpenSearchSQLHelper)

    def test_oracle_returns_oracle_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("ORACLE"), OracleSQLHelper)

    def test_teradata_returns_teradata_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("TERADATA"), TeraDataSQLHelper)

    def test_vertica_returns_vertica_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("VERTICA"), VerticaSQLHelper)

    def test_workdayldq_returns_workday_helper(self):
        self.assertIs(HelperFactory.get_sql_helper("WORKDAYLDQ"), WorkdayDataConnectSqlHelper)

    def test_unsupported_type_returns_none(self):
        self.assertIsNone(HelperFactory.get_sql_helper("UNSUPPORTED_TYPE"))

    def test_empty_string_returns_none(self):
        self.assertIsNone(HelperFactory.get_sql_helper(""))
