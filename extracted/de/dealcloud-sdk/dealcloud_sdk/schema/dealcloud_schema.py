from typing import Optional, Union

from requests.exceptions import HTTPError

from dealcloud_sdk import DealCloudBase
from dealcloud_sdk.models.schema import Field, Object, ObjectWithFields, Schema, User
from dealcloud_sdk.utils.request_retry import request_with_retry


class DealCloudSchema(DealCloudBase):
    """
    Schema Endpoint Methods
    """

    def get_users(self, active_only: bool = False) -> list[User]:
        """
        Gets all users or all active users from DealCloud

        Args:
            active_only (bool): if True will only return active users

        Returns:
            (list[User]): list of DealCloud users
        """
        url = f"{self._schema_url}/users?activeOnly={active_only}"
        response = request_with_retry("GET", url, self._get_access_token)
        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError(
                f"Could not fetch DealCloud users, response: {response.text}"
            )
        users = list([User(**obj) for obj in response.json()])

        return users

    def get_currencies(self) -> list[str]:
        """
        Get all currency codes enabled for a DealCloud site

        Returns:
            (list[str]): all currency codes enabled for the site
        """
        url = f"{self._schema_url}/currencies"
        response = request_with_retry("GET", url, self._get_access_token)
        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError(
                f"Could not fetch DealCloud currencies, response: {response.text}"
            )
        return response.json()

    def get_objects(self) -> list[Object]:
        """
        Get all objects configured in DealCloud

        Returns:
            (list[Object]): all objects
        """

        url = f"{self._schema_url}/entryTypes"
        response = request_with_retry("GET", url, self._get_access_token)
        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError(
                f"Could not fetch DealCloud objects, response: {response.text}"
            )
        objects = list([Object(**obj) for obj in response.json()])

        return objects

    def get_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
        field_id: Optional[int] = None,
    ) -> list[Field]:
        """
        Get fields configured in DealCloud

        Note:
            Both arguments cannot be defined, either object_id or field_id must be defined

        Args:
            object_id (Union[int, str]): If populated will filter the response to only fields from that object.
                Can either be the object ID, or object API name.
            field_id (int): If defined, will pull specific field metadata by ID

        Returns:
            list[Field]: list of DealCloud fields
        """

        if object_id and field_id:
            raise AttributeError(
                "cannot define both object_id and field_id, use only one"
            )
        if object_id:
            url = f"{self._schema_url}/entryTypes/{object_id}/fields"
        elif field_id:
            url = f"{self._schema_url}/fields/{field_id}"
        else:
            url = f"{self._schema_url}/allfields"

        response = request_with_retry("GET", url, self._get_access_token)
        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError(
                f"Could not fetch DealCloud fields, response: {response.text}"
            )
        if isinstance(response.json(), list):
            return list([Field.from_api(field) for field in response.json()])
        else:
            return [Field.from_api(response.json())]

    def get_schema(self, key_type: str = "api") -> Schema:
        """
        Returns a full DealCloud schema

        Args:
            key_type (str): define which schema field should be used in keys for the schema object must be one of:
                "api" (default): use api names as keys
                "display": use display names
                "id": use object/field ids

        Returns:
            Schema: the full dealcloud schema
        """
        objects = self.get_objects()
        fields = self.get_fields()

        schema = {}
        for o in objects:

            object_fields = list(filter(lambda x: x.entryListId == o.id, fields))

            if key_type == "api":
                filtered_object_fields = dict({f.apiName: f for f in object_fields})
                schema[o.apiName] = ObjectWithFields(
                    object=o, fields=filtered_object_fields
                )

            elif key_type == "display":
                filtered_object_fields = dict({f.name: f for f in object_fields})
                schema[o.name] = ObjectWithFields(
                    object=o, fields=filtered_object_fields
                )

            elif key_type == "id":
                filtered_object_fields = dict({str(f.id): f for f in object_fields})
                schema[str(o.id)] = ObjectWithFields(
                    object=o, fields=filtered_object_fields
                )

            else:
                raise AttributeError('key_type must be one of "api", "display", "id".')

        return Schema(objects=schema)
