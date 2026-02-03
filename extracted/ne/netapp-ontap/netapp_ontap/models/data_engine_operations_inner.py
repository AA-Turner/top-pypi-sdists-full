r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineOperationsInner", "DataEngineOperationsInnerSchema"]
__pdoc__ = {
    "DataEngineOperationsInnerSchema.resource": False,
    "DataEngineOperationsInnerSchema.opts": False,
    "DataEngineOperationsInner": False,
}

class DataEngineOperationsInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineOperationsInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the operation, service, or pod.

Example: content_processing """

    used_percent = Size(data_key="used_percent", allow_none=True)
    r""" The consumption percentage of the operation, service, or pod.

Example: 25 """

    @property
    def resource(self):
        return DataEngineOperationsInner

    gettable_fields = [
        "name",
        "used_percent",
    ]
    """name,used_percent,"""

    patchable_fields = [
        "name",
        "used_percent",
    ]
    """name,used_percent,"""

    postable_fields = [
        "name",
        "used_percent",
    ]
    """name,used_percent,"""


class DataEngineOperationsInner(Resource):

    _schema = DataEngineOperationsInnerSchema
