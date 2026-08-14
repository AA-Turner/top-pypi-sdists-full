"""Tests for MongoDB connection wrapper."""

import unittest
from unittest.mock import Mock, patch

from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.glue_connection_wrapper_inputs import (
    GlueConnectionWrapperInputs,
)
from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper import (
    MongoDBConnectionWrapper,
)


class TestMongoDBConnectionWrapper(unittest.TestCase):
    """Test cases for MongoDBConnectionWrapper."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_connection = {
            "Name": "test-mongodb-connection",
            "ConnectionType": "MONGODB",
            "ConnectionProperties": {
                "JDBC_CONNECTION_URL": "mongodb://localhost:27017/testdb",
                "USERNAME": "testuser",
                "PASSWORD": "testpass",
            },
        }

        self.wrapper_inputs = GlueConnectionWrapperInputs(
            connection=self.mock_connection,
            additional_options={},
            kms_client=Mock(),
            secrets_manager_client=Mock(),
        )

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_basic(self, mock_update_url):
        """Test basic MongoDB connection resolution."""
        # Mock JDBC conf
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://localhost:27017/testdb",
            "username": "testuser",
            "password": "testpass",
            "driver": "com.mongodb.spark.sql.DefaultSource",
        }

        # Mock URL update helper
        mock_update_url.return_value = {
            "fullUrl": "mongodb://localhost:27017/testdb",
            "username": "testuser",
            "password": "testpass",
            "driver": "com.mongodb.spark.sql.DefaultSource",
        }

        wrapper = MongoDBConnectionWrapper(self.wrapper_inputs)
        additional_options = {"option1": "value1"}
        wrapper._additional_options = additional_options

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            result = wrapper.get_resolved_connection()

        # Verify URL helper was called with correct parameters
        mock_update_url.assert_called_once()
        call_args = mock_update_url.call_args[0]
        self.assertEqual(call_args[0], "mongodb")  # connection_type
        self.assertEqual(call_args[1], "mongodb://localhost:27017/testdb")  # full_url
        self.assertEqual(call_args[3], additional_options)  # additional_options

        # Verify credentials are removed from SparkProperties
        spark_properties = result["SparkProperties"]
        self.assertNotIn("username", spark_properties)
        self.assertNotIn("password", spark_properties)

        # Verify other properties are preserved
        self.assertEqual(spark_properties["fullUrl"], "mongodb://localhost:27017/testdb")
        self.assertEqual(spark_properties["driver"], "com.mongodb.spark.sql.DefaultSource")

    def test_get_resolved_connection_custom_cert_error(self):
        """Test that custom cert options raise ValueError."""
        # Mock JDBC conf with custom cert
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "customJDBCCert": "/path/to/cert",
            "fullUrl": "mongodb://localhost:27017/testdb",
        }

        wrapper = MongoDBConnectionWrapper(self.wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            with self.assertRaises(ValueError) as context:
                wrapper.get_resolved_connection()

        self.assertEqual(
            str(context.exception), "Custom cert is not supported for spark dataframe."
        )

    def test_get_resolved_connection_custom_cert_string_error(self):
        """Test that custom cert string options raise ValueError."""
        # Mock JDBC conf with custom cert string
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "customJDBCCertString": "cert-content",
            "fullUrl": "mongodb://localhost:27017/testdb",
        }

        wrapper = MongoDBConnectionWrapper(self.wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            with self.assertRaises(ValueError) as context:
                wrapper.get_resolved_connection()

        self.assertEqual(
            str(context.exception), "Custom cert is not supported for spark dataframe."
        )

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_removes_ssl_options(self, mock_update_url):
        """Test that SSL-related options are removed."""
        # Mock JDBC conf with SSL options
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://localhost:27017/testdb",
            "skipCustomJDBCCertValidation": "true",
            "username": "testuser",
        }

        # Mock URL update helper to return enforceSSL
        mock_update_url.return_value = {
            "fullUrl": "mongodb://localhost:27017/testdb",
            "enforceSSL": "true",
            "username": "testuser",
        }

        wrapper = MongoDBConnectionWrapper(self.wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            result = wrapper.get_resolved_connection()

        spark_properties = result["SparkProperties"]

        # Verify SSL options are removed
        self.assertNotIn("skipCustomJDBCCertValidation", spark_properties)
        self.assertNotIn("enforceSSL", spark_properties)
        self.assertNotIn("username", spark_properties)  # Also removed by combine_options

    def test_mongodb_wrapper_creation_with_valid_options(self):
        """Test MongoDB wrapper creation with valid additional options."""
        valid_options = {"retryWrites": "true", "ssl.domain_match": "false"}

        wrapper_inputs = GlueConnectionWrapperInputs(
            connection=self.mock_connection,
            additional_options=valid_options,
            kms_client=Mock(),
            secrets_manager_client=Mock(),
        )

        # Should create successfully
        wrapper = MongoDBConnectionWrapper(wrapper_inputs)
        self.assertIsInstance(wrapper, MongoDBConnectionWrapper)

    def test_mongodb_wrapper_creation_with_malicious_options_fails(self):
        """Test MongoDB wrapper creation fails with malicious additional options."""
        malicious_options = {"retryWrites": "false&host=attacker.com&port=1337"}

        # Should raise ValueError during inputs creation due to validation
        with self.assertRaises(ValueError) as context:
            GlueConnectionWrapperInputs(
                connection=self.mock_connection,
                additional_options=malicious_options,
                kms_client=Mock(),
                secrets_manager_client=Mock(),
            )

        self.assertIn("Invalid value", str(context.exception))

    # ==========================================================================
    # IAM authentication marker tests
    #
    # MongoDBConnectionWrapper should set authenticationType=IAM on the options
    # map when the Glue Connection has IAM authentication. The downstream
    # consumer (GlueSparkConnector-MongoDB's DefaultSource) keys off this marker
    # to resolve credentials via the SDK default provider chain and rewrite the
    # URI to use MONGODB-AWS.
    # ==========================================================================

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_iam_auth_adds_marker(self, mock_update_url):
        """Test that IAM auth connection sets authenticationType=IAM marker."""
        iam_connection = {
            "Name": "docdb-iam-connection",
            "ConnectionType": "DOCUMENTDB",
            "AuthenticationConfiguration": {
                "AuthenticationType": "IAM",
            },
            "ConnectionProperties": {
                "CONNECTION_URL": "mongodb://docdb-host.cluster.eu-north-1.docdb.amazonaws.com:27017",
            },
        }

        wrapper_inputs = GlueConnectionWrapperInputs(
            connection=iam_connection,
            additional_options={},
            kms_client=Mock(),
            secrets_manager_client=Mock(),
        )

        # Mock JDBC conf (IAM connections have no user/password)
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://docdb-host.cluster.eu-north-1.docdb.amazonaws.com:27017",
            "vendor": "mongodb",
        }

        # Capture what gets passed to update_url_in_props
        mock_update_url.return_value = {
            "connection.uri": "mongodb://docdb-host.cluster.eu-north-1.docdb.amazonaws.com:27017",
            "fullUrl": "mongodb://docdb-host.cluster.eu-north-1.docdb.amazonaws.com:27017",
            "vendor": "mongodb",
            "authenticationType": "IAM",
        }

        wrapper = MongoDBConnectionWrapper(wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            result = wrapper.get_resolved_connection()

        # Verify authenticationType=IAM was passed to update_url_in_props
        call_args = mock_update_url.call_args[0]
        connection_options_arg = call_args[2]  # third positional arg
        self.assertEqual(connection_options_arg.get("authenticationType"), "IAM")

        # Verify marker appears in final SparkProperties
        spark_properties = result["SparkProperties"]
        self.assertEqual(spark_properties.get("authenticationType"), "IAM")

        # Verify no user/password leaked for IAM connections
        self.assertNotIn("username", spark_properties)
        self.assertNotIn("password", spark_properties)

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_iam_auth_case_insensitive(self, mock_update_url):
        """Test IAM auth detection is case-insensitive."""
        iam_connection = {
            "Name": "docdb-iam-connection",
            "ConnectionType": "DOCUMENTDB",
            "AuthenticationConfiguration": {
                "AuthenticationType": "iam",  # lowercase
            },
            "ConnectionProperties": {
                "CONNECTION_URL": "mongodb://docdb-host:27017",
            },
        }

        wrapper_inputs = GlueConnectionWrapperInputs(
            connection=iam_connection,
            additional_options={},
            kms_client=Mock(),
            secrets_manager_client=Mock(),
        )

        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://docdb-host:27017",
            "vendor": "mongodb",
        }

        mock_update_url.return_value = {
            "connection.uri": "mongodb://docdb-host:27017",
            "fullUrl": "mongodb://docdb-host:27017",
            "vendor": "mongodb",
            "authenticationType": "IAM",
        }

        wrapper = MongoDBConnectionWrapper(wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            wrapper.get_resolved_connection()

        # Verify authenticationType=IAM was passed to update_url_in_props even with lowercase 'iam'
        call_args = mock_update_url.call_args[0]
        connection_options_arg = call_args[2]
        self.assertEqual(connection_options_arg.get("authenticationType"), "IAM")

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_basic_auth_no_iam_marker(self, mock_update_url):
        """Test that BASIC auth connection does not add authenticationType marker."""
        basic_connection = {
            "Name": "mongo-basic-connection",
            "ConnectionType": "MONGODB",
            "AuthenticationConfiguration": {
                "AuthenticationType": "BASIC",
                "SecretArn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:test",
            },
            "ConnectionProperties": {
                "CONNECTION_URL": "mongodb://host:27017",
            },
        }

        wrapper_inputs = GlueConnectionWrapperInputs(
            connection=basic_connection,
            additional_options={},
            kms_client=Mock(),
            secrets_manager_client=Mock(),
        )

        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://host:27017",
            "vendor": "mongodb",
            "user": "testuser",
            "password": "testpass",
        }

        mock_update_url.return_value = {
            "connection.uri": "mongodb://testuser:testpass@host:27017",
            "fullUrl": "mongodb://host:27017",
            "vendor": "mongodb",
            "username": "testuser",
            "password": "testpass",
        }

        wrapper = MongoDBConnectionWrapper(wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            wrapper.get_resolved_connection()

        # Verify authenticationType was NOT passed to update_url_in_props
        call_args = mock_update_url.call_args[0]
        connection_options_arg = call_args[2]
        self.assertNotIn("authenticationType", connection_options_arg)

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.mongodb_wrapper.JDBCUrlUpdateHelper.update_url_in_props"
    )
    def test_get_resolved_connection_no_auth_config_no_iam_marker(self, mock_update_url):
        """Test that connection without AuthenticationConfiguration does not add marker."""
        mock_jdbc_conf = Mock()
        mock_jdbc_conf.as_map.return_value = {
            "fullUrl": "mongodb://localhost:27017/testdb",
            "username": "testuser",
            "password": "testpass",
        }

        mock_update_url.return_value = {
            "connection.uri": "mongodb://testuser:testpass@localhost:27017/testdb",
            "fullUrl": "mongodb://localhost:27017/testdb",
            "username": "testuser",
            "password": "testpass",
        }

        wrapper = MongoDBConnectionWrapper(self.wrapper_inputs)

        with patch.object(wrapper, "get_jdbc_conf", return_value=mock_jdbc_conf):
            wrapper.get_resolved_connection()

        # Verify authenticationType was NOT passed to update_url_in_props
        call_args = mock_update_url.call_args[0]
        connection_options_arg = call_args[2]
        self.assertNotIn("authenticationType", connection_options_arg)


if __name__ == "__main__":
    unittest.main()
