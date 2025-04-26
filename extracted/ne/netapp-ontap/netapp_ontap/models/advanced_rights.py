r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AdvancedRights", "AdvancedRightsSchema"]
__pdoc__ = {
    "AdvancedRightsSchema.resource": False,
    "AdvancedRightsSchema.opts": False,
    "AdvancedRights": False,
}


class AdvancedRightsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AdvancedRights object"""

    append_data = marshmallow_fields.Boolean(data_key="append_data", allow_none=True)
    r""" Append DAta """

    delete = marshmallow_fields.Boolean(data_key="delete", allow_none=True)
    r""" Delete """

    delete_child = marshmallow_fields.Boolean(data_key="delete_child", allow_none=True)
    r""" Delete Child """

    execute_file = marshmallow_fields.Boolean(data_key="execute_file", allow_none=True)
    r""" Execute File """

    full_control = marshmallow_fields.Boolean(data_key="full_control", allow_none=True)
    r""" Full Control """

    read_attr = marshmallow_fields.Boolean(data_key="read_attr", allow_none=True)
    r""" Read Attributes """

    read_data = marshmallow_fields.Boolean(data_key="read_data", allow_none=True)
    r""" Read Data """

    read_ea = marshmallow_fields.Boolean(data_key="read_ea", allow_none=True)
    r""" Read Extended Attributes """

    read_perm = marshmallow_fields.Boolean(data_key="read_perm", allow_none=True)
    r""" Read Permissions """

    synchronize = marshmallow_fields.Boolean(data_key="synchronize", allow_none=True)
    r""" Synchronize """

    write_attr = marshmallow_fields.Boolean(data_key="write_attr", allow_none=True)
    r""" Write Attributes """

    write_data = marshmallow_fields.Boolean(data_key="write_data", allow_none=True)
    r""" Write Data """

    write_ea = marshmallow_fields.Boolean(data_key="write_ea", allow_none=True)
    r""" Write Extended Attributes """

    write_owner = marshmallow_fields.Boolean(data_key="write_owner", allow_none=True)
    r""" Write Owner """

    write_perm = marshmallow_fields.Boolean(data_key="write_perm", allow_none=True)
    r""" Write Permission """

    @property
    def resource(self):
        return AdvancedRights

    gettable_fields = [
        "append_data",
        "delete",
        "delete_child",
        "execute_file",
        "full_control",
        "read_attr",
        "read_data",
        "read_ea",
        "read_perm",
        "synchronize",
        "write_attr",
        "write_data",
        "write_ea",
        "write_owner",
        "write_perm",
    ]
    """append_data,delete,delete_child,execute_file,full_control,read_attr,read_data,read_ea,read_perm,synchronize,write_attr,write_data,write_ea,write_owner,write_perm,"""

    patchable_fields = [
        "append_data",
        "delete",
        "delete_child",
        "execute_file",
        "full_control",
        "read_attr",
        "read_data",
        "read_ea",
        "read_perm",
        "write_attr",
        "write_data",
        "write_ea",
        "write_owner",
        "write_perm",
    ]
    """append_data,delete,delete_child,execute_file,full_control,read_attr,read_data,read_ea,read_perm,write_attr,write_data,write_ea,write_owner,write_perm,"""

    postable_fields = [
        "append_data",
        "delete",
        "delete_child",
        "execute_file",
        "full_control",
        "read_attr",
        "read_data",
        "read_ea",
        "read_perm",
        "write_attr",
        "write_data",
        "write_ea",
        "write_owner",
        "write_perm",
    ]
    """append_data,delete,delete_child,execute_file,full_control,read_attr,read_data,read_ea,read_perm,write_attr,write_data,write_ea,write_owner,write_perm,"""


class AdvancedRights(Resource):

    _schema = AdvancedRightsSchema
