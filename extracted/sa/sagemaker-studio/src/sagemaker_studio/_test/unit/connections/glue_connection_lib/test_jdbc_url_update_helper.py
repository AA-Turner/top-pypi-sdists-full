"""
Unit tests for JdbcUrlUpdateHelper
"""

import unittest
import unittest.mock
from typing import Dict

from sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper import (
    JDBCUrlUpdateHelper,
)


class TestJdbcUrlUpdateHelper(unittest.TestCase):
    """Test cases for JdbcUrlUpdateHelper class."""

    def test_unsupported_vendor_fallback(self):
        """Test unsupported vendor returns original props unchanged."""
        url = "jdbc:postgresql://localhost:5432/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper.update_url_in_props(
            "postgresql", url, props, additional_options
        )

        # Should return original props unchanged
        self.assertEqual(result, props)
        self.assertEqual(result["user"], "testuser")
        self.assertEqual(result["password"], "testpass")
        # Should not have url or fullUrl added
        self.assertNotIn("url", result)
        self.assertNotIn("fullUrl", result)

    def test_mysql_url_update(self):
        """Test MySQL URL gets performance and SSL parameters added."""
        url = "jdbc:mysql://localhost:3306/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper.update_url_in_props("mysql", url, props, additional_options)

        # Check that performance parameters were added
        self.assertIn("useCursorFetch=true", result["url"])
        self.assertIn("zeroDateTimeBehavior=convertToNull", result["url"])
        self.assertEqual(result["fullUrl"], result["url"])
        self.assertEqual(result["user"], "testuser")
        self.assertEqual(result["password"], "testpass")

    def test_mysql_url_with_existing_params(self):
        """Test MySQL URL with existing query parameters."""
        url = "jdbc:mysql://localhost:3306/testdb?autoReconnect=true"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper.update_url_in_props("mysql", url, props, additional_options)

        # Check that new parameters were added with & separator
        self.assertIn("autoReconnect=true", result["url"])
        self.assertIn("&useCursorFetch=true", result["url"])
        self.assertIn("&zeroDateTimeBehavior=convertToNull", result["url"])

    def test_mysql_url_with_ssl_properties(self):
        """Test MySQL URL with SSL properties in props get added to URL."""
        url = "jdbc:mysql://localhost:3306/testdb"
        # Mock SSL properties that would be returned by JdbcConnectionProperties
        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcConnectionProperties.get_driver_connection_properties"
        ) as mock_props:
            mock_ssl_props = unittest.mock.Mock()
            mock_ssl_props.get_ssl_with_dn_match_properties.return_value.keys.return_value = {
                "useSSL",
                "verifyServerCertificate",
            }
            mock_props.return_value = mock_ssl_props

            props = {
                "user": "testuser",
                "password": "testpass",
                "useSSL": "true",
                "verifyServerCertificate": "true",
                "nonSSLProp": "value",  # This should not be added to URL
            }
            additional_options: Dict[str, str] = {}

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "mysql", url, props, additional_options
            )

            # Check that SSL properties were added to URL
            self.assertIn("useSSL=true", result["url"])
            self.assertIn("verifyServerCertificate=true", result["url"])
            # Non-SSL property should not be in URL
            self.assertNotIn("nonSSLProp=value", result["url"])

    def test_mysql_case_insensitive(self):
        """Test MySQL vendor name is case insensitive."""
        url = "jdbc:mysql://localhost:3306/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper.update_url_in_props("MYSQL", url, props, additional_options)

        self.assertIn("useCursorFetch=true", result["url"])
        self.assertIn("zeroDateTimeBehavior=convertToNull", result["url"])

    def test_add_url_params_empty(self):
        """Test _add_url_params with empty params dict."""
        url = "jdbc:mysql://localhost:3306/testdb"
        result = JDBCUrlUpdateHelper._add_url_params(url, {})
        self.assertEqual(result, url)

    def test_add_url_params_multiple(self):
        """Test _add_url_params with multiple parameters."""
        url = "jdbc:mysql://localhost:3306/testdb"
        params = {"param1": "value1", "param2": "value2"}
        result = JDBCUrlUpdateHelper._add_url_params(url, params)

        self.assertIn("param1=value1", result)
        self.assertIn("param2=value2", result)
        self.assertIn("?", result)  # First param uses ?
        self.assertIn("&", result)  # Second param uses &

    def test_create_result_with_url(self):
        """Test _create_result_with_url helper method."""
        props = {"user": "testuser", "password": "testpass"}
        url = "jdbc:mysql://localhost:3306/testdb"

        result = JDBCUrlUpdateHelper._create_result_with_url(props, url)

        self.assertEqual(result["url"], url)
        self.assertEqual(result["fullUrl"], url)
        self.assertEqual(result["user"], "testuser")
        self.assertEqual(result["password"], "testpass")

    def test_mysql_no_ssl_properties(self):
        """Test MySQL with no SSL properties in props - only performance params added."""
        url = "jdbc:mysql://localhost:3306/testdb"
        # Mock empty SSL properties
        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcConnectionProperties.get_driver_connection_properties"
        ) as mock_props:
            mock_ssl_props = unittest.mock.Mock()
            mock_ssl_props.get_ssl_with_dn_match_properties.return_value.keys.return_value = {
                "useSSL",
                "verifyServerCertificate",
            }
            mock_props.return_value = mock_ssl_props

            props = {"user": "testuser", "password": "testpass"}  # No SSL properties
            additional_options: Dict[str, str] = {}

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "mysql", url, props, additional_options
            )

            # Should have performance params but no SSL params
            self.assertIn("useCursorFetch=true", result["url"])
            self.assertIn("zeroDateTimeBehavior=convertToNull", result["url"])
            # Should not have any SSL properties
            self.assertNotIn("useSSL", result["url"])
            self.assertNotIn("verifyServerCertificate", result["url"])


class TestOracleUrlUpdateHelper(unittest.TestCase):
    """Test cases for Oracle JDBC URL update functionality."""

    def test_oracle_url_without_ssl(self):
        """Test Oracle URL without SSL properties."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin:@//localhost:1521/xe"
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "oracle", url, props, additional_options
            )

            # Should call get_connection_url with SSL disabled
            mock_jdbc_url.get_connection_url.assert_called_with(
                use_ssl=False, use_domain_match=False
            )
            self.assertEqual(result["url"], "jdbc:oracle:thin:@//localhost:1521/xe")
            self.assertEqual(result["fullUrl"], "jdbc:oracle:thin:@//localhost:1521/xe")

    def test_oracle_url_with_ssl_truststore(self):
        """Test Oracle URL with SSL truststore property."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {
            "user": "testuser",
            "password": "testpass",
            "javax.net.ssl.trustStore": "/path/to/truststore",
        }
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))"
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "oracle", url, props, additional_options
            )

            # Should call get_connection_url with SSL enabled
            mock_jdbc_url.get_connection_url.assert_called_with(use_ssl=True, use_domain_match=True)
            self.assertIn("tcps", result["url"])

    def test_oracle_url_with_enforce_ssl(self):
        """Test Oracle URL with enforceSSL property."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {"user": "testuser", "password": "testpass", "enforceSSL": "true"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))"
            mock_from_url.return_value = mock_jdbc_url

            JDBCUrlUpdateHelper.update_url_in_props("oracle", url, props, additional_options)

            # Should call get_connection_url with SSL enabled
            mock_jdbc_url.get_connection_url.assert_called_with(use_ssl=True, use_domain_match=True)

    def test_oracle_url_enforce_ssl_case_insensitive(self):
        """Test Oracle URL with enforceSSL property is case insensitive."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {"user": "testuser", "password": "testpass", "enforceSSL": "TRUE"}  # Uppercase
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))"
            mock_from_url.return_value = mock_jdbc_url

            JDBCUrlUpdateHelper.update_url_in_props("oracle", url, props, additional_options)

            # Should still enable SSL
            mock_jdbc_url.get_connection_url.assert_called_with(use_ssl=True, use_domain_match=True)

    def test_oracle_url_format_correction(self):
        """Test Oracle URL format correction from thin://@  to thin:@//."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            # Return URL that needs format correction
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin://@localhost:1521/xe"
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "oracle", url, props, additional_options
            )

            # Should correct the format
            self.assertEqual(result["url"], "jdbc:oracle:thin:@//localhost:1521/xe")

    def test_oracle_case_insensitive(self):
        """Test Oracle vendor name is case insensitive."""
        url = "jdbc:oracle:thin://@localhost:1521/xe"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = "jdbc:oracle:thin:@//localhost:1521/xe"
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "ORACLE", url, props, additional_options
            )

            # Should still work with uppercase vendor name
            self.assertEqual(result["url"], "jdbc:oracle:thin:@//localhost:1521/xe")


class TestSqlServerUrlUpdateHelper(unittest.TestCase):
    """Test cases for SQL Server JDBC URL update functionality."""

    def test_sqlserver_url_already_formatted(self):
        """Test SQL Server URL that's already in SQL Server format."""
        url = "jdbc:sqlserver://localhost:1433;database=testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database=testdb"
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "sqlserver", url, props, additional_options
            )

            # Should call get_connection_url with SSL disabled by default
            mock_jdbc_url.get_connection_url.assert_called_with(
                use_ssl=False, use_domain_match=False
            )
            self.assertEqual(result["url"], "jdbc:sqlserver://localhost:1433;database=testdb")

    def test_sqlserver_url_conversion_from_mysql_format(self):
        """Test SQL Server URL conversion from MySQL-like format."""
        url = "jdbc:sqlserver://localhost:1433/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database={testdb}"
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "sqlserver", url, props, additional_options
            )

            # Should convert to SQL Server format with curly braces
            self.assertEqual(result["url"], "jdbc:sqlserver://localhost:1433;database={testdb}")

    def test_sqlserver_url_with_wildcard_database(self):
        """Test SQL Server URL with wildcard database (%)."""
        url = "jdbc:sqlserver://localhost:1433/%"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database="
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "sqlserver", url, props, additional_options
            )

            # Should convert wildcard to empty database parameter
            self.assertEqual(result["url"], "jdbc:sqlserver://localhost:1433;database=")

    def test_sqlserver_url_with_encrypt_ssl(self):
        """Test SQL Server URL with encrypt=true for SSL."""
        url = "jdbc:sqlserver://localhost:1433/testdb"
        props = {"user": "testuser", "password": "testpass", "encrypt": "true"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database={testdb};hostNameInCertificate=localhost"
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "sqlserver", url, props, additional_options
            )

            # Should call get_connection_url with SSL enabled
            mock_jdbc_url.get_connection_url.assert_called_with(use_ssl=True, use_domain_match=True)
            # Should have hostNameInCertificate in the URL
            self.assertIn("hostNameInCertificate=localhost", result["url"])

    def test_sqlserver_url_encrypt_case_insensitive(self):
        """Test SQL Server URL with encrypt=TRUE (uppercase)."""
        url = "jdbc:sqlserver://localhost:1433/testdb"
        props = {"user": "testuser", "password": "testpass", "encrypt": "TRUE"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database={testdb};hostNameInCertificate=localhost"
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "sqlserver", url, props, additional_options
            )

            # Should still enable SSL with uppercase value
            mock_jdbc_url.get_connection_url.assert_called_with(use_ssl=True, use_domain_match=True)
            # Should have hostNameInCertificate in the URL
            self.assertIn("hostNameInCertificate=localhost", result["url"])

    def test_sqlserver_invalid_url_format_insufficient_parts(self):
        """Test SQL Server URL with insufficient parts raises ValueError."""
        url = "jdbc:sqlserver://localhost"  # Missing port and database
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with self.assertRaises(ValueError) as context:
            JDBCUrlUpdateHelper.update_url_in_props("sqlserver", url, props, additional_options)

        self.assertIn("Invalid SQL Server URL format", str(context.exception))

    def test_sqlserver_invalid_url_format_no_database(self):
        """Test SQL Server URL without database part raises ValueError."""
        url = "jdbc:sqlserver://localhost:1433"  # Missing database
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with self.assertRaises(ValueError) as context:
            JDBCUrlUpdateHelper.update_url_in_props("sqlserver", url, props, additional_options)

        self.assertIn("Invalid SQL Server URL format", str(context.exception))

    def test_sqlserver_case_insensitive(self):
        """Test SQL Server vendor name is case insensitive."""
        url = "jdbc:sqlserver://localhost:1433;database=testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        with unittest.mock.patch(
            "sagemaker_studio.connections.glue_connection_lib.connections.utils.jdbc_url_update_helper.JdbcUrl.from_url"
        ) as mock_from_url:
            mock_jdbc_url = unittest.mock.Mock()
            mock_jdbc_url.get_connection_url.return_value = (
                "jdbc:sqlserver://localhost:1433;database=testdb"
            )
            mock_from_url.return_value = mock_jdbc_url

            result = JDBCUrlUpdateHelper.update_url_in_props(
                "SQLSERVER", url, props, additional_options
            )

            # Should still work with uppercase vendor name
            self.assertEqual(result["url"], "jdbc:sqlserver://localhost:1433;database=testdb")

    def test_update_props_redshift_basic_no_ssl_no_iam(self):
        """Test basic Redshift URL without SSL or IAM - should return unchanged."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        self.assertEqual(result["url"], url)
        self.assertEqual(result["fullUrl"], url)
        self.assertEqual(result["user"], "testuser")
        self.assertEqual(result["password"], "testpass")

    def test_update_props_redshift_with_ssl_enabled(self):
        """Test Redshift URL with SSL enabled - should add SSL parameters."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev"
        props = {"user": "testuser", "password": "testpass", "ssl": "true"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?ssl=true&sslmode=verify-ca"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_ssl_with_existing_query_params(self):
        """Test Redshift URL with SSL when URL already has query parameters - should use & separator."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev?existingParam=value"
        props = {"user": "testuser", "password": "testpass", "ssl": "true"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "&ssl=true&sslmode=verify-ca"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_ssl_with_verify_full(self):
        """Test Redshift URL with SSL and sslmode=verify-full - should use ssl_with_dn_match_properties."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev"
        props = {
            "user": "testuser",
            "password": "testpass",
            "ssl": "true",
            "sslmode": "verify-full",
        }
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?ssl=true&sslmode=verify-full&sslrootcert="
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_with_enforce_ssl(self):
        """Test Redshift URL with enforceSSL=true - should take precedence over ssl property."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev"
        props = {"user": "testuser", "password": "testpass", "enforceSSL": "true"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?ssl=true&sslmode=verify-ca"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_iam_with_dbuser(self):
        """Test Redshift IAM URL with DbUser - should add DbUser parameter."""
        url = "jdbc:redshift:iam://cluster:region/dev"
        props: Dict[str, str] = {}
        additional_options = {"DbUser": "testuser"}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?DbUser=testuser"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_iam_without_dbuser_flag(self):
        """Test Redshift IAM URL without DbUser flag in additional_options - should not add DbUser."""
        url = "jdbc:redshift:iam://cluster:region/dev"
        props: Dict[str, str] = {}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        self.assertEqual(result["url"], url)
        self.assertEqual(result["fullUrl"], url)

    def test_update_props_redshift_iam_with_ssl_and_dbuser(self):
        """Test Redshift IAM URL with both SSL and DbUser - should add both parameters."""
        url = "jdbc:redshift:iam://cluster:region/dev"
        props = {"ssl": "true"}
        additional_options = {"DbUser": "testuser"}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?ssl=true&sslmode=verify-ca&DbUser=testuser"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_ssl_case_insensitive(self):
        """Test Redshift URL with SSL=TRUE (uppercase) - should work due to .lower() call."""
        url = "jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev"
        props = {"user": "testuser", "password": "testpass", "ssl": "TRUE"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?ssl=true&sslmode=verify-ca"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_url_mongodb_basic(self):
        """Test basic MongoDB URL without modifications."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        self.assertEqual(
            result["connection.uri"], "mongodb://testuser:testpass@localhost:27017/testdb"
        )
        self.assertEqual(result["username"], "testuser")
        self.assertEqual(result["password"], "testpass")

    def test_update_url_mongodb_with_ssl(self):
        """Test MongoDB URL with SSL enabled."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "testuser", "password": "testpass", "enforceSSL": "true"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        expected_url = "mongodb://testuser:testpass@localhost:27017/testdb/?ssl=true"
        self.assertEqual(result["connection.uri"], expected_url)
        self.assertNotIn("ssl", result)

    def test_update_url_mongodb_with_ssl_domain_mismatch(self):
        """Test MongoDB URL with SSL and domain mismatch allowed."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "testuser", "password": "testpass", "enforceSSL": "true"}
        additional_options = {"ssl.domain_match": "false"}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        expected_url = "mongodb://testuser:testpass@localhost:27017/testdb/?ssl=true&sslInvalidHostNameAllowed=true"
        self.assertEqual(result["connection.uri"], expected_url)

    def test_update_url_mongodb_with_retry_writes(self):
        """Test MongoDB URL with retryWrites parameter."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options = {"retryWrites": "false"}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        expected_url = "mongodb://testuser:testpass@localhost:27017/testdb/?retryWrites=false"
        self.assertEqual(result["connection.uri"], expected_url)

    def test_update_url_mongodb_no_credentials(self):
        """Test MongoDB URL without username/password."""
        url = "mongodb://localhost:27017/testdb"
        props: Dict[str, str] = {}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        self.assertEqual(result["connection.uri"], url)

    def test_validate_mongo_uri_disable_update_valid(self):
        """Test MongoDB URI validation with disableUpdateUri enabled."""
        valid_url = "mongodb://localhost:27017/testdb"
        result = JDBCUrlUpdateHelper._validate_mongo_uri("true", valid_url)
        self.assertTrue(result)

    def test_validate_mongo_uri_disable_update_invalid(self):
        """Test MongoDB URI validation with disableUpdateUri and invalid URL."""
        invalid_url = "invalid://localhost:27017/testdb"

        with self.assertRaises(RuntimeError):
            JDBCUrlUpdateHelper._validate_mongo_uri("true", invalid_url)

    def test_update_url_mongodb_disable_update_uri(self):
        """Test MongoDB URL with disableUpdateUri enabled."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "testuser", "password": "testpass"}
        additional_options = {"disableUpdateUri": "true"}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        self.assertEqual(result["username"], "testuser")
        self.assertEqual(result["password"], "testpass")
        self.assertNotIn("connection.uri", result)

    def test_update_url_mongodb_special_characters_encoding(self):
        """Test MongoDB URL with special characters in credentials."""
        url = "mongodb://localhost:27017/testdb"
        props = {"user": "test@user", "password": "pass:word"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_url_mongodb(url, props, additional_options)

        expected_url = "mongodb://test%40user:pass%3Aword@localhost:27017/testdb"
        self.assertEqual(result["connection.uri"], expected_url)

    def test_validate_mongo_uri_invalid(self):
        """Test MongoDB URI validation with invalid URLs."""
        invalid_url = "invalid://localhost:27017/testdb"

        with self.assertRaises(RuntimeError):
            JDBCUrlUpdateHelper._validate_mongo_uri("false", invalid_url)

    def test_mongodb_special_characters_encoding(self):
        """Test that urllib.parse.quote correctly encodes MongoDB special characters."""
        from urllib.parse import quote

        # Test each MongoDB special character individually
        test_cases = [
            ("%", "%25"),  # percent must be encoded first
            (":", "%3A"),  # colon
            ("/", "%2F"),  # forward slash
            ("?", "%3F"),  # question mark
            ("#", "%23"),  # hash
            ("[", "%5B"),  # left bracket
            ("]", "%5D"),  # right bracket
            ("@", "%40"),  # at sign
        ]

        for input_char, expected in test_cases:
            result = quote(input_char, safe="")
            self.assertEqual(result, expected, f"Failed to encode '{input_char}' correctly")

        # Test realistic username/password combinations
        realistic_cases = [
            ("user@domain.com", "user%40domain.com"),
            ("pass:word/123", "pass%3Aword%2F123"),
            ("user[admin]", "user%5Badmin%5D"),
            ("password?query#fragment", "password%3Fquery%23fragment"),
            ("user%encoded", "user%25encoded"),
        ]

        for input_str, expected in realistic_cases:
            result = quote(input_str, safe="")
            self.assertEqual(result, expected, f"Failed to encode '{input_str}' correctly")

    def test_update_props_redshift_converts_to_iam_url_with_iam_role(self):
        """Test Redshift URL conversion to IAM format when aws_iam_role is present."""
        url = "jdbc:redshift://test-cluster:5439/test"
        props = {"user": "testuser", "password": "testpass"}
        additional_options = {"aws_iam_role": "arn:aws:iam::123456789012:role/test-role"}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = "jdbc:redshift:iam://test-cluster:5439/test"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)
        self.assertEqual(result["aws_iam_role"], "arn:aws:iam::123456789012:role/test-role")

    def test_update_props_redshift_converts_to_iam_url_with_iam_auth_type(self):
        """Test Redshift URL conversion to IAM format when authenticationType is IAM."""
        url = "jdbc:redshift://test-cluster:5439/test"
        props = {"authenticationType": "IAM"}
        additional_options: Dict[str, str] = {}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = "jdbc:redshift:iam://test-cluster:5439/test"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)

    def test_update_props_redshift_does_not_convert_existing_iam_url(self):
        """Test that existing IAM URL is not double-converted."""
        url = "jdbc:redshift:iam://test-cluster:5439/test"
        props = {"authenticationType": "IAM"}
        additional_options = {"aws_iam_role": "arn:aws:iam::123456789012:role/test-role"}

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        # Should remain as IAM URL, not become jdbc:redshift:iam:iam://
        self.assertEqual(result["url"], url)
        self.assertEqual(result["fullUrl"], url)
        self.assertEqual(result["aws_iam_role"], "arn:aws:iam::123456789012:role/test-role")

    def test_update_props_redshift_iam_with_dbuser_and_iam_role(self):
        """Test Redshift IAM URL with both DbUser and aws_iam_role."""
        url = "jdbc:redshift:iam://test-cluster:5439/test"
        props: Dict[str, str] = {}
        additional_options = {
            "DbUser": "iam_user",
            "aws_iam_role": "arn:aws:iam::123456789012:role/test-role",
        }

        result = JDBCUrlUpdateHelper._update_props_redshift(url, props, additional_options)

        expected_url = url + "?DbUser=iam_user"
        self.assertEqual(result["url"], expected_url)
        self.assertEqual(result["fullUrl"], expected_url)
        self.assertEqual(result["aws_iam_role"], "arn:aws:iam::123456789012:role/test-role")


# ==========================================================================
# MongoDB / DocumentDB — authenticationType marker propagation
#
# MongoDBConnectionWrapper sets `authenticationType=IAM` on the props map when
# the Glue Connection has IAM auth. The downstream consumer
# (GlueSparkConnector-MongoDB's DefaultSource) keys off this marker. Lock in
# that _update_url_mongodb passes the marker through untranslated for both
# mongodb and documentdb connection types.
# ==========================================================================


class TestMongoDBAuthenticationTypeMarker(unittest.TestCase):
    """Test authenticationType marker propagation through update_url_in_props."""

    def test_update_url_in_props_mongodb_propagates_authentication_type_iam(self):
        """Test updateUrlInProps for MongoDB propagates authenticationType=IAM marker."""
        url = "mongodb://host:27017"
        props = {
            "url": url,
            "fullUrl": url,
            "authenticationType": "IAM",
            # enforceSSL=false must NOT disable TLS for IAM auth -- see the
            # TestMongoDBIamTlsEnforcement cases below.
            "enforceSSL": "false",
        }

        result = JDBCUrlUpdateHelper.update_url_in_props("mongodb", url, props, {})

        self.assertEqual(
            result.get("authenticationType"),
            "IAM",
            f"authenticationType marker was not propagated. Got: {result}",
        )
        self.assertIn("ssl=true", result["connection.uri"])

    def test_update_url_in_props_documentdb_propagates_authentication_type_iam(self):
        """Test updateUrlInProps for DocumentDB propagates authenticationType=IAM marker."""
        url = "mongodb://docdbhost:27017"
        props = {
            "url": url,
            "fullUrl": url,
            "authenticationType": "IAM",
            "enforceSSL": "true",
        }

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", url, props, {})

        self.assertEqual(
            result.get("authenticationType"),
            "IAM",
            f"authenticationType marker was not propagated. Got: {result}",
        )
        self.assertIn("ssl=true", result["connection.uri"])

    def test_update_url_in_props_mongodb_no_authentication_type_when_absent(self):
        """Test updateUrlInProps for MongoDB does not add authenticationType when absent."""
        url = "mongodb://host:27017"
        props = {"url": url, "fullUrl": url, "enforceSSL": "false"}

        result = JDBCUrlUpdateHelper.update_url_in_props("mongodb", url, props, {})

        self.assertNotIn("authenticationType", result)
        self.assertNotIn("ssl=true", result["connection.uri"])


# ==========================================================================
# MongoDB / DocumentDB -- TLS enforcement.
#
# The MONGODB-AWS SASL exchange carries the access key id, the session token,
# and a signed GetCallerIdentity payload, so TLS is mandatory for IAM auth.
# `enforceSSL` arrives verbatim from customer-supplied ConnectionProperties
# via CreateConnection/UpdateConnection, so it cannot be relied on: the
# console form that sets ENFORCE_SSL=true for DocumentDB IAM is not an
# enforcement point. These cases lock in that the URI is never IAM-marked
# without TLS, that the enforceSSL comparison is case-insensitive, and that
# the disableUpdateUri path fails closed instead of dropping TLS silently.
# ==========================================================================


class TestMongoDBIamTlsEnforcement(unittest.TestCase):
    """Test TLS enforcement for MongoDB/DocumentDB IAM authentication."""

    URL = "mongodb://docdbhost:27017"

    def test_iam_auth_forces_ssl_when_enforce_ssl_false(self):
        """IAM auth appends ssl=true even when enforceSSL is explicitly false."""
        props = {"url": self.URL, "fullUrl": self.URL, "authenticationType": "IAM"}
        props["enforceSSL"] = "false"

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", self.URL, props, {})

        self.assertEqual(result["connection.uri"], f"{self.URL}/?ssl=true")

    def test_iam_auth_forces_ssl_when_enforce_ssl_absent(self):
        """IAM auth appends ssl=true when enforceSSL is not supplied at all."""
        props = {"url": self.URL, "fullUrl": self.URL, "authenticationType": "IAM"}

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", self.URL, props, {})

        self.assertEqual(result["connection.uri"], f"{self.URL}/?ssl=true")

    def test_iam_auth_case_insensitive_marker(self):
        """IAM detection tolerates the marker's casing."""
        props = {"url": self.URL, "fullUrl": self.URL, "authenticationType": "iam"}

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", self.URL, props, {})

        self.assertIn("ssl=true", result["connection.uri"])

    def test_iam_auth_does_not_duplicate_ssl_already_in_url(self):
        """No duplicate ssl=true when the URL already declares TLS."""
        url = f"{self.URL}/?ssl=true"
        props = {"url": url, "fullUrl": url, "authenticationType": "IAM"}

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", url, props, {})

        self.assertEqual(result["connection.uri"].count("ssl=true"), 1)

    def test_iam_auth_accepts_tls_true_in_url(self):
        """`tls=true` in the URL satisfies the requirement -- it is the driver's synonym."""
        url = f"{self.URL}/?tls=true"
        props = {"url": url, "fullUrl": url, "authenticationType": "IAM"}

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", url, props, {})

        self.assertEqual(result["connection.uri"], url)
        self.assertNotIn("ssl=true", result["connection.uri"])

    def test_iam_auth_ignores_ssl_domain_match_false(self):
        """`ssl.domain_match=false` does not disable hostname verification under IAM."""
        props = {"url": self.URL, "fullUrl": self.URL, "authenticationType": "IAM"}
        additional_options = {"ssl.domain_match": "false"}

        result = JDBCUrlUpdateHelper.update_url_in_props(
            "documentdb", self.URL, props, additional_options
        )

        self.assertIn("ssl=true", result["connection.uri"])
        self.assertNotIn("sslInvalidHostNameAllowed", result["connection.uri"])

    def test_basic_auth_still_honors_ssl_domain_match_false(self):
        """Non-IAM connections keep the existing ssl.domain_match behavior."""
        props = {"url": self.URL, "fullUrl": self.URL, "enforceSSL": "true"}
        additional_options = {"ssl.domain_match": "false"}

        result = JDBCUrlUpdateHelper.update_url_in_props(
            "documentdb", self.URL, props, additional_options
        )

        self.assertIn("sslInvalidHostNameAllowed=true", result["connection.uri"])

    def test_enforce_ssl_comparison_is_case_insensitive(self):
        """enforceSSL="TRUE" enables TLS -- casing must not fail open."""
        for value in ("TRUE", "True", "tRuE"):
            with self.subTest(enforce_ssl=value):
                props = {"url": self.URL, "fullUrl": self.URL, "enforceSSL": value}

                result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", self.URL, props, {})

                self.assertIn("ssl=true", result["connection.uri"])

    def test_enforce_ssl_false_without_iam_leaves_url_untouched(self):
        """TLS is not forced for non-IAM connections that did not ask for it."""
        props = {"url": self.URL, "fullUrl": self.URL, "enforceSSL": "false"}

        result = JDBCUrlUpdateHelper.update_url_in_props("documentdb", self.URL, props, {})

        self.assertEqual(result["connection.uri"], self.URL)

    def test_disable_update_uri_rejects_iam_without_tls_in_url(self):
        """disableUpdateUri + IAM without TLS in the URL fails closed."""
        props = {"url": self.URL, "fullUrl": self.URL, "authenticationType": "IAM"}
        additional_options = {"disableUpdateUri": "true"}

        with self.assertRaises(ValueError) as context:
            JDBCUrlUpdateHelper.update_url_in_props(
                "documentdb", self.URL, props, additional_options
            )

        self.assertIn("TLS is required", str(context.exception))
        # Same rationale as validateMongoUri: the URL may carry credentials.
        self.assertNotIn(self.URL, str(context.exception))

    def test_disable_update_uri_rejects_enforce_ssl_without_tls_in_url(self):
        """disableUpdateUri + enforceSSL=true without TLS in the URL fails closed."""
        props = {"url": self.URL, "fullUrl": self.URL, "enforceSSL": "true"}
        additional_options = {"disableUpdateUri": "true"}

        with self.assertRaises(ValueError):
            JDBCUrlUpdateHelper.update_url_in_props(
                "documentdb", self.URL, props, additional_options
            )

    def test_disable_update_uri_accepts_tls_declared_in_url(self):
        """disableUpdateUri + IAM is fine when the URL already declares TLS."""
        url = f"{self.URL}/?ssl=true"
        props = {"url": url, "fullUrl": url, "authenticationType": "IAM"}
        additional_options = {"disableUpdateUri": "true"}

        result = JDBCUrlUpdateHelper.update_url_in_props(
            "documentdb", url, props, additional_options
        )

        self.assertEqual(result["connection.uri"], url)
        self.assertEqual(result["authenticationType"], "IAM")
        # The translated key is not honored by the downstream connector, which
        # reads connection settings only from connection.uri -- do not ship it.
        self.assertNotIn("ssl", result)

    def test_disable_update_uri_without_tls_requirement_unchanged(self):
        """disableUpdateUri with no TLS requirement keeps the existing behavior."""
        props = {"url": self.URL, "fullUrl": self.URL, "enforceSSL": "false"}
        additional_options = {"disableUpdateUri": "true"}

        result = JDBCUrlUpdateHelper.update_url_in_props(
            "documentdb", self.URL, props, additional_options
        )

        self.assertEqual(result["connection.uri"], self.URL)
        self.assertNotIn("ssl", result)


# ==========================================================================
# MongoDB / DocumentDB -- validateMongoUri must not embed the URL in the
# exception message.
#
# Customer-supplied Mongo URLs may carry `user:pass@` userinfo. When
# validation fails, the exception propagates through Spark's error path
# and lands in driver / executor stdout, event logs, and Py4JJavaError
# messages. Formatting the URL into the message leaks those credentials.
# Mirrors GlueSparkConnector-MongoDB commit 3541f5e.
# ==========================================================================


class TestMongoDBUriValidationUrlScrub(unittest.TestCase):
    """Test that validateMongoUri does not leak URLs in exception messages."""

    def test_validate_mongo_uri_regex_path_exception_does_not_carry_raw_url(self):
        """validateMongoUri (regex path) -- invalid URL: exception does not carry the raw URL."""
        bad_url = "postgres://user:secret@host:5432/db"
        props = {"url": bad_url, "fullUrl": bad_url}

        with self.assertRaises(RuntimeError) as ctx:
            JDBCUrlUpdateHelper.update_url_in_props("mongodb", bad_url, props, {})

        msg = str(ctx.exception)
        self.assertNotIn(bad_url, msg, f"Raw URL leaked into exception message: {msg}")
        self.assertNotIn("user:secret", msg, f"Credentials leaked into exception message: {msg}")
        # Message stays actionable
        self.assertIn("Mongo/DocumentDB", msg, f"Vendor context lost: {msg}")
        self.assertIn("Developer Guide", msg, f"Actionable pointer lost: {msg}")

    def test_validate_mongo_uri_regex_path_exception_message_shape(self):
        """validateMongoUri (regex path) -- exception message keeps its shape when URL is stripped."""
        bad_url = "notmongo://host/db"
        props = {"url": bad_url, "fullUrl": bad_url}

        with self.assertRaises(RuntimeError) as ctx:
            JDBCUrlUpdateHelper.update_url_in_props("mongodb", bad_url, props, {})

        # Snapshot: the exact message text callers may pattern-match on.
        expected = (
            "Mongo/DocumentDB connection URL is not supported. Check the Developer "
            "Guide for the list of supported data stores/URL formatting."
        )
        self.assertEqual(
            str(ctx.exception),
            expected,
            f"Unexpected exception message: {ctx.exception}",
        )

    def test_validate_mongo_uri_disable_update_uri_path_exception_does_not_carry_raw_url(self):
        """validateMongoUri (disableUpdateUri path) -- invalid URL: exception does not carry the raw URL."""
        bad_url = "postgres://user:secret@host:5432/db"
        props = {"url": bad_url, "fullUrl": bad_url}
        additional_options = {"disableUpdateUri": "true"}

        with self.assertRaises(RuntimeError) as ctx:
            JDBCUrlUpdateHelper.update_url_in_props("mongodb", bad_url, props, additional_options)

        msg = str(ctx.exception)
        self.assertNotIn(bad_url, msg, f"Raw URL leaked into exception message: {msg}")
        self.assertNotIn("user:secret", msg, f"Credentials leaked into exception message: {msg}")
        # Message stays actionable
        self.assertIn("mongodb://", msg, f"Valid prefixes not mentioned: {msg}")
        self.assertIn("mongodb+srv://", msg, f"Valid prefixes not mentioned: {msg}")

    def test_validate_mongo_uri_documentdb_path_uses_url_scrubbed_messages(self):
        """validateMongoUri -- DocumentDB path uses the same URL-scrubbed messages."""
        bad_url = "postgres://user:secret@host:5432/db"
        props = {"url": bad_url, "fullUrl": bad_url}

        with self.assertRaises(RuntimeError) as ctx:
            JDBCUrlUpdateHelper.update_url_in_props("documentdb", bad_url, props, {})

        msg = str(ctx.exception)
        self.assertNotIn(bad_url, msg, f"Raw URL leaked (documentdb): {msg}")
        self.assertNotIn("user:secret", msg, f"Credentials leaked (documentdb): {msg}")

    def test_validate_mongo_uri_valid_url_round_trips_without_throwing(self):
        """validateMongoUri -- valid mongodb URL round-trips without throwing."""
        url = "mongodb://host:27017/db"
        props = {"url": url, "fullUrl": url}

        result = JDBCUrlUpdateHelper.update_url_in_props("mongodb", url, props, {})

        self.assertIn(
            "connection.uri", result, f"connection.uri missing after happy path: {result}"
        )


if __name__ == "__main__":
    unittest.main()
