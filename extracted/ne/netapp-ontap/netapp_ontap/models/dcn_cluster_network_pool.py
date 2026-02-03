r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnClusterNetworkPool", "DcnClusterNetworkPoolSchema"]
__pdoc__ = {
    "DcnClusterNetworkPoolSchema.resource": False,
    "DcnClusterNetworkPoolSchema.opts": False,
    "DcnClusterNetworkPool": False,
}

class DcnClusterNetworkPoolSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnClusterNetworkPool object"""

    ip_ranges = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.ip_address_range", "IpAddressRangeSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="ip_ranges",
                allow_none=True
                )
    r""" IP address range """

    subnet = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.ip_info", "IpInfoSchema"),
                unknown=EXCLUDE,
                data_key="subnet",
                allow_none=True
            )
    r""" IP information """

    @property
    def resource(self):
        return DcnClusterNetworkPool

    gettable_fields = [
        "ip_ranges",
        "subnet",
    ]
    """ip_ranges,subnet,"""

    patchable_fields = [
        "ip_ranges",
        "subnet",
    ]
    """ip_ranges,subnet,"""

    postable_fields = [
        "ip_ranges",
        "subnet",
    ]
    """ip_ranges,subnet,"""


class DcnClusterNetworkPool(Resource):

    _schema = DcnClusterNetworkPoolSchema
