from unittest import TestCase
from unittest.mock import Mock
from uuid import UUID, uuid4

from box import Box

from pycarlo.features.exceptions import MultipleResourcesFoundException, ResourceNotFoundException
from pycarlo.features.user import UserService
from pycarlo.features.user.queries import GET_USER_WAREHOUSES


class UserServiceTests(TestCase):
    single_resource_response = Box(
        {
            "get_user": {
                "account": {
                    "warehouses": [
                        {"uuid": str(uuid4()), "name": "Snowflake", "connection_type": "snowflake"}
                    ]
                }
            }
        }
    )

    multiple_resource_response = Box(
        {
            "get_user": {
                "account": {
                    "warehouses": [
                        {"uuid": str(uuid4()), "name": "Data Lake", "connection_type": "data-lake"},
                        {"uuid": str(uuid4()), "name": "Snowflake", "connection_type": "snowflake"},
                    ]
                }
            }
        }
    )

    def test_get_default_resource(self):
        # given
        mock_client = Mock(return_value=self.single_resource_response)
        service = UserService(mc_client=mock_client)
        warehouse = self.single_resource_response.get_user.account.warehouses[0]

        # when
        resource = service.get_resource()

        # then
        mock_client.assert_called_once_with(
            query=GET_USER_WAREHOUSES,
            additional_headers={
                "x-mcd-telemetry-reason": "service",
                "x-mcd-telemetry-service": "user_service",
            },
        )
        self.assertEqual(UUID(warehouse.uuid), resource.id)
        self.assertEqual(warehouse.name, resource.name)
        self.assertEqual(warehouse.connection_type, resource.type)

    def test_get_default_resource_with_multiple_resources(self):
        # given
        mock_client = Mock(return_value=self.multiple_resource_response)
        service = UserService(mc_client=mock_client)

        # when
        with self.assertRaises(MultipleResourcesFoundException) as context:
            service.get_resource()

        # then
        mock_client.assert_called_once_with(
            query=GET_USER_WAREHOUSES,
            additional_headers={
                "x-mcd-telemetry-reason": "service",
                "x-mcd-telemetry-service": "user_service",
            },
        )
        self.assertEqual(
            "Multiple resources found, please specify a resource id", str(context.exception)
        )

    def test_get_resource_with_invalid_id(self):
        # given
        mock_client = Mock(return_value=self.multiple_resource_response)
        service = UserService(mc_client=mock_client)
        resource_id = uuid4()

        # when
        with self.assertRaises(ResourceNotFoundException) as context:
            service.get_resource(resource_id)

        # then
        mock_client.assert_called_once_with(
            query=GET_USER_WAREHOUSES,
            additional_headers={
                "x-mcd-telemetry-reason": "service",
                "x-mcd-telemetry-service": "user_service",
            },
        )
        self.assertEqual(f"Resource not found with id={resource_id}", str(context.exception))

    def test_get_resource_with_valid_id(self):
        # given
        mock_client = Mock(return_value=self.multiple_resource_response)
        service = UserService(mc_client=mock_client)
        warehouse = self.multiple_resource_response.get_user.account.warehouses[0]

        # when
        resource = service.get_resource(warehouse.uuid)

        # then
        mock_client.assert_called_once_with(
            query=GET_USER_WAREHOUSES,
            additional_headers={
                "x-mcd-telemetry-reason": "service",
                "x-mcd-telemetry-service": "user_service",
            },
        )
        self.assertEqual(UUID(warehouse.uuid), resource.id)
        self.assertEqual(warehouse.name, resource.name)
        self.assertEqual(warehouse.connection_type, resource.type)
