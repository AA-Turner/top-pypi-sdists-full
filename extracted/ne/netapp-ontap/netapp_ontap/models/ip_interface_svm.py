r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpInterfaceSvm", "IpInterfaceSvmSchema"]
__pdoc__ = {
    "IpInterfaceSvmSchema.resource": False,
    "IpInterfaceSvmSchema.opts": False,
    "IpInterfaceSvm": False,
}


class IpInterfaceSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpInterfaceSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ip_interface_svm. """

    ip = marshmallow_fields.Nested("netapp_ontap.models.ip_interface_svm_ip.IpInterfaceSvmIpSchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" IP information """

    location = marshmallow_fields.Nested("netapp_ontap.models.ip_interface_svm_location.IpInterfaceSvmLocationSchema", unknown=EXCLUDE, data_key="location", allow_none=True)
    r""" Home_node is optional. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the interface (optional).

Example: lif1 """

    service_policy = marshmallow_fields.Str(data_key="service_policy", allow_none=True)
    r""" The service_policy field of the ip_interface_svm. """

    services = marshmallow_fields.List(marshmallow_fields.Str, data_key="services", allow_none=True)
    r""" The services associated with the interface. """

    subnet = marshmallow_fields.Nested("netapp_ontap.resources.ip_subnet.IpSubnetSchema", unknown=EXCLUDE, data_key="subnet", allow_none=True)
    r""" Allocates an interface address from a subnet. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IpInterfaceSvm

    gettable_fields = [
        "links",
        "ip",
        "name",
        "service_policy",
        "services",
        "subnet.links",
        "subnet.name",
        "subnet.uuid",
        "uuid",
    ]
    """links,ip,name,service_policy,services,subnet.links,subnet.name,subnet.uuid,uuid,"""

    patchable_fields = [
        "ip",
        "service_policy",
        "subnet.name",
        "subnet.uuid",
    ]
    """ip,service_policy,subnet.name,subnet.uuid,"""

    postable_fields = [
        "ip",
        "location",
        "name",
        "service_policy",
        "subnet.name",
        "subnet.uuid",
    ]
    """ip,location,name,service_policy,subnet.name,subnet.uuid,"""


class IpInterfaceSvm(Resource):

    _schema = IpInterfaceSvmSchema
