r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CapacityPoolResponseRecords", "CapacityPoolResponseRecordsSchema"]
__pdoc__ = {
    "CapacityPoolResponseRecordsSchema.resource": False,
    "CapacityPoolResponseRecordsSchema.opts": False,
    "CapacityPoolResponseRecords": False,
}


class CapacityPoolResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CapacityPoolResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the capacity_pool_response_records. """

    license_manager = marshmallow_fields.Nested("netapp_ontap.resources.license_manager.LicenseManagerSchema", unknown=EXCLUDE, data_key="license_manager", allow_none=True)
    r""" The license_manager field of the capacity_pool_response_records. """

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.capacity_pool_nodes.CapacityPoolNodesSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" Nodes in the cluster associated with this capacity pool. """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Serial number of the capacity pool license.

Example: 390000100 """

    @property
    def resource(self):
        return CapacityPoolResponseRecords

    gettable_fields = [
        "links",
        "license_manager.links",
        "license_manager.uuid",
        "nodes",
        "serial_number",
    ]
    """links,license_manager.links,license_manager.uuid,nodes,serial_number,"""

    patchable_fields = [
        "license_manager.links",
        "license_manager.uuid",
        "nodes",
        "serial_number",
    ]
    """license_manager.links,license_manager.uuid,nodes,serial_number,"""

    postable_fields = [
        "license_manager.links",
        "license_manager.uuid",
        "nodes",
        "serial_number",
    ]
    """license_manager.links,license_manager.uuid,nodes,serial_number,"""


class CapacityPoolResponseRecords(Resource):

    _schema = CapacityPoolResponseRecordsSchema
