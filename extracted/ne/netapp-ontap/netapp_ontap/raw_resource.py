"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This module defines the RawResource class. This class is meant to store
resource information as a dictionary without schema validation to make
fetching resources using fast_get_collection() possible. The class
supports promoting a raw resource to proper resource using promote().
"""

from typing import (
    Union,
)

from netapp_ontap.error import NetAppRestError
from netapp_ontap.host_connection import HostConnection

__all__ = ["RawResource"]
__pdoc__ = {
    "RawResource.get": False,
    "RawResource.post": False,
    "RawResource.patch": False,
    "RawResource.delete": False,
}


class RawResource:
    """An Abstract class which is the base of resources that haven't had their schema validated."""

    def __init__(
        self,
        raw_data_dict: dict,
        resource_type,
        *args,
    ) -> None:
        """Initialize a RawResource Object

        Args:
            raw_data_dict (dict): the data the resource contains as returned from the host
            resource_type (class): the class that this resource belongs to
        """
        self.resource_data: dict = raw_data_dict
        self.resource_type = resource_type
        self.parent_keys = args
        self.connection: Union[None, HostConnection] = None

    def __getattr__(self, attr):
        if attr in self.resource_data:
            return self.resource_data[attr]
        # pylint: disable=protected-access
        schema = self.resource_type._schema_instance
        # If the field is in the schema, return a different error message
        if attr in schema.fields:
            raise AttributeError(
                f"The {attr} field has not been set on this instance. If the field has"
                " changed or been set by the server since this object was retrieved,"
                " you can call get() on the promoted resource."
            )
        raise AttributeError

    def promote(self):
        """Turn a raw resource into one that supports all applicable RESTful operations."""
        resource = self.resource_type.from_dict(self.resource_data, self.parent_keys)
        if self.connection is not None:
            resource.set_connection(self.connection)
        return resource

    def set_connection(self, connection: HostConnection):
        """Set the connection attribute of the RawResource

        Args:
            connection (HostConnection): HostConnection object the resource belongs to
        """
        self.connection = connection

    def get(self, *args, **kwargs):
        """Catch the call to this and throw an error saying that
        the resource needs to be promoted before this method can be called"""
        raise NetAppRestError(
            f"get() is not a supported operation for RawResource and can only be called on"
            " the promoted version of this resource. Use promote()"
            f" to get a {self.resource_type.__name__} object."
        )

    def patch(self, *args, **kwargs):
        """Catch the call to this and throw an error saying that
        the resource needs to be promoted before this method can be called"""
        raise NetAppRestError(
            f"patch() is not a supported operation for RawResource and can only be called on"
            " the promoted version of this resource. Use promote()"
            f" to get a {self.resource_type.__name__} object."
        )

    def delete(self, *args, **kwargs):
        """Catch the call to this and throw an error saying that
        the resource needs to be promoted before this method can be called"""
        raise NetAppRestError(
            f"delete() is not a supported operation for RawResource and can only be called on"
            " the promoted version of this resource. Use promote()"
            f" to get a {self.resource_type.__name__} object."
        )

    def post(self, *args, **kwargs):
        """Catch the call to this and throw an error saying that
        the resource needs to be promoted before this method can be called"""
        raise NetAppRestError(
            f"post() is not a supported operation for RawResource and can only be called on"
            " the promoted version of this resource. Use promote()"
            f" to get a {self.resource_type.__name__} object."
        )
