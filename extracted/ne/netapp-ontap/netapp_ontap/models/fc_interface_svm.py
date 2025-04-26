r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcInterfaceSvm", "FcInterfaceSvmSchema"]
__pdoc__ = {
    "FcInterfaceSvmSchema.resource": False,
    "FcInterfaceSvmSchema.opts": False,
    "FcInterfaceSvm": False,
}


class FcInterfaceSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcInterfaceSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the fc_interface_svm. """

    data_protocol = marshmallow_fields.Str(data_key="data_protocol", allow_none=True)
    r""" The data protocol for which the Fibre Channel interface is configured.

Valid choices:

* fcp
* fc_nvme """

    location = marshmallow_fields.Nested("netapp_ontap.models.fc_interface_svm_location.FcInterfaceSvmLocationSchema", unknown=EXCLUDE, data_key="location", allow_none=True)
    r""" The location of the Fibre Channel interface is defined by the location of its port. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the Fibre Channel interface.

Example: lif1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the Fibre Channel interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return FcInterfaceSvm

    gettable_fields = [
        "links",
        "data_protocol",
        "name",
        "uuid",
    ]
    """links,data_protocol,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "data_protocol",
        "location",
        "name",
    ]
    """data_protocol,location,name,"""


class FcInterfaceSvm(Resource):

    _schema = FcInterfaceSvmSchema
