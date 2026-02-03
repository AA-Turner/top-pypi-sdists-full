r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataSourceSpace", "DataSourceSpaceSchema"]
__pdoc__ = {
    "DataSourceSpaceSchema.resource": False,
    "DataSourceSpaceSchema.opts": False,
    "DataSourceSpace": False,
}

class DataSourceSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataSourceSpace object"""

    available = Size(data_key="available", allow_none=True)
    r""" The available space of a data source, in bytes. """

    total = Size(data_key="total", allow_none=True)
    r""" The total space of a data source, in bytes. """

    used = Size(data_key="used", allow_none=True)
    r""" The used space of a data source, in bytes. """

    @property
    def resource(self):
        return DataSourceSpace

    gettable_fields = [
        "available",
        "total",
        "used",
    ]
    """available,total,used,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataSourceSpace(Resource):

    _schema = DataSourceSpaceSchema
