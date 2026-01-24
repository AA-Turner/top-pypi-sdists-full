from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

from box import Box
from click.testing import CliRunner
from pycarlo.core import Client

from montecarlodata.common.user import UserService
from montecarlodata.management.commands import (
    delete_asset_collection_preferences,
    get_asset_collection_preferences,
    set_asset_collection_preferences,
)
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_RESOURCE_UUID = str(uuid4())
_SAMPLE_RESOURCE_NAME = "test-tableau-server"


class ManagementCommandsTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        # Mock the all_resource_identifiers to return our test resource
        self._user_service_mock.all_resource_identifiers = {
            _SAMPLE_RESOURCE_NAME: _SAMPLE_RESOURCE_UUID,
            _SAMPLE_RESOURCE_UUID: _SAMPLE_RESOURCE_NAME,
        }
        self._mc_client_mock = Mock(spec=Client)

    @patch("montecarlodata.management.commands.create_mc_client")
    @patch("montecarlodata.management.service.UserService")
    def test_get_asset_collection_preferences(self, mock_user_service_class, mock_create_client):
        # Setup mocks
        mock_user_service_class.return_value = self._user_service_mock
        mock_create_client.return_value = self._mc_client_mock

        # Mock the GraphQL response
        self._mc_client_mock.return_value = Box(
            {
                "get_asset_collection_preferences": Box(
                    {"edges": [], "page_info": Box({"has_next_page": False})}
                )
            }
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            get_asset_collection_preferences,
            obj={"config": ctx},
        )

        self.assertEqual(result.exit_code, 0)

        # Verify the GraphQL client was called
        self._mc_client_mock.assert_called_once()

        # Get the actual call arguments - the query object is the first positional arg
        call_args = self._mc_client_mock.call_args
        query_obj = call_args[0][0]  # First positional argument is the query object

        # Convert the query to string and compare the entire GraphQL query
        expected_query = """query {
  getAssetCollectionPreferences(first: 100) {
    edges {
      node {
        assetType
        defaultEffect
        rules {
          effect
        }
        resource {
          uuid
          name
        }
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}"""
        self.assertEqual(str(query_obj), expected_query)

    @patch("montecarlodata.management.commands.create_mc_client")
    @patch("montecarlodata.management.service.UserService")
    def test_set_asset_collection_preferences(self, mock_user_service_class, mock_create_client):
        # Setup mocks
        mock_user_service_class.return_value = self._user_service_mock
        mock_create_client.return_value = self._mc_client_mock

        # Mock the GraphQL mutation response
        self._mc_client_mock.return_value = Box(
            {"set_asset_collection_preferences": Box({"success": True})}
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            set_asset_collection_preferences,
            obj={"config": ctx},
            args=[
                "--resource-name",
                _SAMPLE_RESOURCE_NAME,
                "--asset-type",
                "workbook",
                "--default-effect",
                "BLOCK",
            ],
        )

        self.assertEqual(result.exit_code, 0)

        # Verify the GraphQL client was called with a mutation
        self._mc_client_mock.assert_called_once()

        # Get the actual call arguments - the mutation object is the first positional arg
        call_args = self._mc_client_mock.call_args
        mutation_obj = call_args[0][0]  # First positional argument is the mutation object

        # Convert the mutation to string and compare the entire GraphQL query
        expected_mutation = f"""mutation {{
  setAssetCollectionPreferences(resourceId: "{_SAMPLE_RESOURCE_UUID}", assetType: "workbook", defaultEffect: block) {{
    success
  }}
}}"""
        self.assertEqual(str(mutation_obj), expected_mutation)

    @patch("montecarlodata.management.commands.create_mc_client")
    @patch("montecarlodata.management.service.UserService")
    def test_set_asset_collection_preferences_without_default_effect(
        self, mock_user_service_class, mock_create_client
    ):
        # Setup mocks
        mock_user_service_class.return_value = self._user_service_mock
        mock_create_client.return_value = self._mc_client_mock

        # Mock the GraphQL mutation response
        self._mc_client_mock.return_value = Box(
            {"set_asset_collection_preferences": Box({"success": True})}
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            set_asset_collection_preferences,
            obj={"config": ctx},
            args=[
                "--resource-name",
                _SAMPLE_RESOURCE_NAME,
                "--asset-type",
                "workbook",
            ],
        )

        self.assertEqual(result.exit_code, 0)

        # Verify the GraphQL client was called
        self._mc_client_mock.assert_called_once()

        # Get the actual call arguments
        call_args = self._mc_client_mock.call_args
        mutation_obj = call_args[0][0]

        # Convert the mutation to string and compare the entire GraphQL query
        expected_mutation = f"""mutation {{
  setAssetCollectionPreferences(resourceId: "{_SAMPLE_RESOURCE_UUID}", assetType: "workbook") {{
    success
  }}
}}"""
        self.assertEqual(str(mutation_obj), expected_mutation)

    @patch("montecarlodata.management.commands.create_mc_client")
    @patch("montecarlodata.management.service.UserService")
    def test_delete_asset_collection_preferences(self, mock_user_service_class, mock_create_client):
        # Setup mocks
        mock_user_service_class.return_value = self._user_service_mock
        mock_create_client.return_value = self._mc_client_mock

        # Mock the GraphQL mutation response
        self._mc_client_mock.return_value = Box(
            {"delete_asset_collection_preferences": Box({"success": True})}
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            delete_asset_collection_preferences,
            obj={"config": ctx},
            args=[
                "--resource-name",
                _SAMPLE_RESOURCE_NAME,
                "--asset-type",
                "workbook",
            ],
        )

        self.assertEqual(result.exit_code, 0)

        # Verify the GraphQL client was called
        self._mc_client_mock.assert_called_once()

        # Get the actual call arguments
        call_args = self._mc_client_mock.call_args
        mutation_obj = call_args[0][0]

        # Convert the mutation to string and compare the entire GraphQL query
        expected_mutation = f"""mutation {{
  deleteAssetCollectionPreferences(resourceId: "{_SAMPLE_RESOURCE_UUID}", assetType: "workbook") {{
    success
  }}
}}"""
        self.assertEqual(str(mutation_obj), expected_mutation)

    @patch("montecarlodata.management.commands.create_mc_client")
    @patch("montecarlodata.management.service.UserService")
    def test_set_asset_collection_preferences_with_rules(
        self, mock_user_service_class, mock_create_client
    ):
        # Setup mocks
        mock_user_service_class.return_value = self._user_service_mock
        mock_create_client.return_value = self._mc_client_mock

        # Mock the GraphQL mutation response
        self._mc_client_mock.return_value = Box(
            {"set_asset_collection_preferences": Box({"success": True})}
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()

        # Test with rules JSON
        rules_json = '[{"conditions": [{"attribute_name": "name", "value": "test_*", "comparison_type": "prefix"}], "effect": "block"}]'

        result = runner.invoke(
            set_asset_collection_preferences,
            obj={"config": ctx},
            args=[
                "--resource-name",
                _SAMPLE_RESOURCE_NAME,
                "--asset-type",
                "workbook",
                "--default-effect",
                "ALLOW",
                "--rules-json",
                rules_json,
            ],
        )

        self.assertEqual(result.exit_code, 0)

        # Verify the GraphQL client was called
        self._mc_client_mock.assert_called_once()

        # Get the actual call arguments
        call_args = self._mc_client_mock.call_args
        mutation_obj = call_args[0][0]

        # Convert the mutation to string and compare the entire GraphQL query
        expected_mutation = f"""mutation {{
  setAssetCollectionPreferences(
      resourceId: "{_SAMPLE_RESOURCE_UUID}"
      assetType: "workbook"
      defaultEffect: allow
      rules: [{{conditions: [{{attributeName: "name", value: "test_*", comparisonType: prefix}}], effect: block}}]
    ) {{
    success
  }}
}}"""
        self.assertEqual(str(mutation_obj), expected_mutation)

    def test_help_text_includes_resource_type_asset_type_mapping(self):
        """Test that help text includes documentation of supported resource types."""
        runner = CliRunner()

        command = set_asset_collection_preferences

        result = runner.invoke(command, ["--help"])
        self.assertEqual(result.exit_code, 0)

        # Verify the help text includes the resource type documentation
        expected_text = """Supported asset types and attributes:

  tableau

    - project: name

    - workbook: name, luid
"""
        self.assertIn(expected_text, result.output)
