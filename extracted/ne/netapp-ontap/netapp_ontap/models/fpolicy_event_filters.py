r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEventFilters", "FpolicyEventFiltersSchema"]
__pdoc__ = {
    "FpolicyEventFiltersSchema.resource": False,
    "FpolicyEventFiltersSchema.opts": False,
    "FpolicyEventFilters": False,
}


class FpolicyEventFiltersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEventFilters object"""

    close_with_modification = marshmallow_fields.Boolean(data_key="close_with_modification", allow_none=True)
    r""" Filter the client request for close with modification. """

    close_with_read = marshmallow_fields.Boolean(data_key="close_with_read", allow_none=True)
    r""" Filter the client request for close with read. """

    close_without_modification = marshmallow_fields.Boolean(data_key="close_without_modification", allow_none=True)
    r""" Filter the client request for close without modification. """

    exclude_directory = marshmallow_fields.Boolean(data_key="exclude_directory", allow_none=True)
    r""" Filter the client requests for directory operations. When this filter is specified directory operations are not monitored. """

    first_read = marshmallow_fields.Boolean(data_key="first_read", allow_none=True)
    r""" Filter the client requests for the first-read. """

    first_write = marshmallow_fields.Boolean(data_key="first_write", allow_none=True)
    r""" Filter the client requests for the first-write. """

    monitor_ads = marshmallow_fields.Boolean(data_key="monitor_ads", allow_none=True)
    r""" Filter the client request for alternate data stream. """

    offline_bit = marshmallow_fields.Boolean(data_key="offline_bit", allow_none=True)
    r""" Filter the client request for offline bit set. FPolicy server receives notification only when offline files are accessed. """

    open_with_delete_intent = marshmallow_fields.Boolean(data_key="open_with_delete_intent", allow_none=True)
    r""" Filter the client request for open with delete intent. """

    open_with_write_intent = marshmallow_fields.Boolean(data_key="open_with_write_intent", allow_none=True)
    r""" Filter the client request for open with write intent. """

    setattr_with_access_time_change = marshmallow_fields.Boolean(data_key="setattr_with_access_time_change", allow_none=True)
    r""" Filter the client setattr requests for changing the access time of a file or directory. """

    setattr_with_allocation_size_change = marshmallow_fields.Boolean(data_key="setattr_with_allocation_size_change", allow_none=True)
    r""" Filter the client setattr requests for changing the allocation size of a file. """

    setattr_with_creation_time_change = marshmallow_fields.Boolean(data_key="setattr_with_creation_time_change", allow_none=True)
    r""" Filter the client setattr requests for changing the creation time of a file or directory. """

    setattr_with_dacl_change = marshmallow_fields.Boolean(data_key="setattr_with_dacl_change", allow_none=True)
    r""" Filter the client setattr requests for changing dacl on a file or directory. """

    setattr_with_group_change = marshmallow_fields.Boolean(data_key="setattr_with_group_change", allow_none=True)
    r""" Filter the client setattr requests for changing group of a file or directory. """

    setattr_with_mode_change = marshmallow_fields.Boolean(data_key="setattr_with_mode_change", allow_none=True)
    r""" Filter the client setattr requests for changing the mode bits on a file or directory. """

    setattr_with_modify_time_change = marshmallow_fields.Boolean(data_key="setattr_with_modify_time_change", allow_none=True)
    r""" Filter the client setattr requests for changing the modification time of a file or directory. """

    setattr_with_owner_change = marshmallow_fields.Boolean(data_key="setattr_with_owner_change", allow_none=True)
    r""" Filter the client setattr requests for changing owner of a file or directory. """

    setattr_with_sacl_change = marshmallow_fields.Boolean(data_key="setattr_with_sacl_change", allow_none=True)
    r""" Filter the client setattr requests for changing sacl on a file or directory. """

    setattr_with_size_change = marshmallow_fields.Boolean(data_key="setattr_with_size_change", allow_none=True)
    r""" Filter the client setattr requests for changing the size of a file. """

    write_with_size_change = marshmallow_fields.Boolean(data_key="write_with_size_change", allow_none=True)
    r""" Filter the client request for write with size change. """

    @property
    def resource(self):
        return FpolicyEventFilters

    gettable_fields = [
        "close_with_modification",
        "close_with_read",
        "close_without_modification",
        "exclude_directory",
        "first_read",
        "first_write",
        "monitor_ads",
        "offline_bit",
        "open_with_delete_intent",
        "open_with_write_intent",
        "setattr_with_access_time_change",
        "setattr_with_allocation_size_change",
        "setattr_with_creation_time_change",
        "setattr_with_dacl_change",
        "setattr_with_group_change",
        "setattr_with_mode_change",
        "setattr_with_modify_time_change",
        "setattr_with_owner_change",
        "setattr_with_sacl_change",
        "setattr_with_size_change",
        "write_with_size_change",
    ]
    """close_with_modification,close_with_read,close_without_modification,exclude_directory,first_read,first_write,monitor_ads,offline_bit,open_with_delete_intent,open_with_write_intent,setattr_with_access_time_change,setattr_with_allocation_size_change,setattr_with_creation_time_change,setattr_with_dacl_change,setattr_with_group_change,setattr_with_mode_change,setattr_with_modify_time_change,setattr_with_owner_change,setattr_with_sacl_change,setattr_with_size_change,write_with_size_change,"""

    patchable_fields = [
        "close_with_modification",
        "close_with_read",
        "close_without_modification",
        "exclude_directory",
        "first_read",
        "first_write",
        "monitor_ads",
        "offline_bit",
        "open_with_delete_intent",
        "open_with_write_intent",
        "setattr_with_access_time_change",
        "setattr_with_allocation_size_change",
        "setattr_with_creation_time_change",
        "setattr_with_dacl_change",
        "setattr_with_group_change",
        "setattr_with_mode_change",
        "setattr_with_modify_time_change",
        "setattr_with_owner_change",
        "setattr_with_sacl_change",
        "setattr_with_size_change",
        "write_with_size_change",
    ]
    """close_with_modification,close_with_read,close_without_modification,exclude_directory,first_read,first_write,monitor_ads,offline_bit,open_with_delete_intent,open_with_write_intent,setattr_with_access_time_change,setattr_with_allocation_size_change,setattr_with_creation_time_change,setattr_with_dacl_change,setattr_with_group_change,setattr_with_mode_change,setattr_with_modify_time_change,setattr_with_owner_change,setattr_with_sacl_change,setattr_with_size_change,write_with_size_change,"""

    postable_fields = [
        "close_with_modification",
        "close_with_read",
        "close_without_modification",
        "exclude_directory",
        "first_read",
        "first_write",
        "monitor_ads",
        "offline_bit",
        "open_with_delete_intent",
        "open_with_write_intent",
        "setattr_with_access_time_change",
        "setattr_with_allocation_size_change",
        "setattr_with_creation_time_change",
        "setattr_with_dacl_change",
        "setattr_with_group_change",
        "setattr_with_mode_change",
        "setattr_with_modify_time_change",
        "setattr_with_owner_change",
        "setattr_with_sacl_change",
        "setattr_with_size_change",
        "write_with_size_change",
    ]
    """close_with_modification,close_with_read,close_without_modification,exclude_directory,first_read,first_write,monitor_ads,offline_bit,open_with_delete_intent,open_with_write_intent,setattr_with_access_time_change,setattr_with_allocation_size_change,setattr_with_creation_time_change,setattr_with_dacl_change,setattr_with_group_change,setattr_with_mode_change,setattr_with_modify_time_change,setattr_with_owner_change,setattr_with_sacl_change,setattr_with_size_change,write_with_size_change,"""


class FpolicyEventFilters(Resource):

    _schema = FpolicyEventFiltersSchema
