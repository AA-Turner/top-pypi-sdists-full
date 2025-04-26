r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NasApplicationComponentsQos", "NasApplicationComponentsQosSchema"]
__pdoc__ = {
    "NasApplicationComponentsQosSchema.resource": False,
    "NasApplicationComponentsQosSchema.opts": False,
    "NasApplicationComponentsQos": False,
}


class NasApplicationComponentsQosSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NasApplicationComponentsQos object"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.nas_application_components_qos_policy.NasApplicationComponentsQosPolicySchema", unknown=EXCLUDE, data_key="policy", allow_none=True)
    r""" The policy field of the nas_application_components_qos. """

    @property
    def resource(self):
        return NasApplicationComponentsQos

    gettable_fields = [
        "policy",
    ]
    """policy,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "policy",
    ]
    """policy,"""


class NasApplicationComponentsQos(Resource):

    _schema = NasApplicationComponentsQosSchema
