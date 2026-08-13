r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterHa", "ClusterHaSchema"]
__pdoc__ = {
    "ClusterHaSchema.resource": False,
    "ClusterHaSchema.opts": False,
    "ClusterHa": False,
}

class ClusterHaSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterHa object"""

    failover_protection_level = marshmallow_fields.Str(data_key="failover_protection_level", allow_none=True)
    r""" Specifies the number of concurrent node failures the cluster can tolerate with no disruptions.

Valid choices:

* nplusone
* nplustwo """

    @property
    def resource(self):
        return ClusterHa

    gettable_fields = [
        "failover_protection_level",
    ]
    """failover_protection_level,"""

    patchable_fields = [
        "failover_protection_level",
    ]
    """failover_protection_level,"""

    postable_fields = [
        "failover_protection_level",
    ]
    """failover_protection_level,"""


class ClusterHa(Resource):

    _schema = ClusterHaSchema
