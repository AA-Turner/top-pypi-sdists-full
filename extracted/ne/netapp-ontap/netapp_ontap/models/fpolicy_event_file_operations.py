r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEventFileOperations", "FpolicyEventFileOperationsSchema"]
__pdoc__ = {
    "FpolicyEventFileOperationsSchema.resource": False,
    "FpolicyEventFileOperationsSchema.opts": False,
    "FpolicyEventFileOperations": False,
}


class FpolicyEventFileOperationsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEventFileOperations object"""

    access = marshmallow_fields.Boolean(data_key="access", allow_none=True)
    r""" Access operations """

    close = marshmallow_fields.Boolean(data_key="close", allow_none=True)
    r""" File close operations """

    create = marshmallow_fields.Boolean(data_key="create", allow_none=True)
    r""" File create operations """

    create_dir = marshmallow_fields.Boolean(data_key="create_dir", allow_none=True)
    r""" Directory create operations """

    delete = marshmallow_fields.Boolean(data_key="delete", allow_none=True)
    r""" File delete operations """

    delete_dir = marshmallow_fields.Boolean(data_key="delete_dir", allow_none=True)
    r""" Directory delete operations """

    getattr = marshmallow_fields.Boolean(data_key="getattr", allow_none=True)
    r""" Get attribute operations """

    link = marshmallow_fields.Boolean(data_key="link", allow_none=True)
    r""" Link operations """

    lookup = marshmallow_fields.Boolean(data_key="lookup", allow_none=True)
    r""" Lookup operations """

    open = marshmallow_fields.Boolean(data_key="open", allow_none=True)
    r""" File open operations """

    read = marshmallow_fields.Boolean(data_key="read", allow_none=True)
    r""" File read operations """

    rename = marshmallow_fields.Boolean(data_key="rename", allow_none=True)
    r""" File rename operations """

    rename_dir = marshmallow_fields.Boolean(data_key="rename_dir", allow_none=True)
    r""" Directory rename operations """

    setattr = marshmallow_fields.Boolean(data_key="setattr", allow_none=True)
    r""" Set attribute operations """

    symlink = marshmallow_fields.Boolean(data_key="symlink", allow_none=True)
    r""" Symbolic link operations """

    write = marshmallow_fields.Boolean(data_key="write", allow_none=True)
    r""" File write operations """

    @property
    def resource(self):
        return FpolicyEventFileOperations

    gettable_fields = [
        "access",
        "close",
        "create",
        "create_dir",
        "delete",
        "delete_dir",
        "getattr",
        "link",
        "lookup",
        "open",
        "read",
        "rename",
        "rename_dir",
        "setattr",
        "symlink",
        "write",
    ]
    """access,close,create,create_dir,delete,delete_dir,getattr,link,lookup,open,read,rename,rename_dir,setattr,symlink,write,"""

    patchable_fields = [
        "access",
        "close",
        "create",
        "create_dir",
        "delete",
        "delete_dir",
        "getattr",
        "link",
        "lookup",
        "open",
        "read",
        "rename",
        "rename_dir",
        "setattr",
        "symlink",
        "write",
    ]
    """access,close,create,create_dir,delete,delete_dir,getattr,link,lookup,open,read,rename,rename_dir,setattr,symlink,write,"""

    postable_fields = [
        "access",
        "close",
        "create",
        "create_dir",
        "delete",
        "delete_dir",
        "getattr",
        "link",
        "lookup",
        "open",
        "read",
        "rename",
        "rename_dir",
        "setattr",
        "symlink",
        "write",
    ]
    """access,close,create,create_dir,delete,delete_dir,getattr,link,lookup,open,read,rename,rename_dir,setattr,symlink,write,"""


class FpolicyEventFileOperations(Resource):

    _schema = FpolicyEventFileOperationsSchema
