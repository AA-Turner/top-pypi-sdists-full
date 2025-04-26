r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceStatus", "NvmeNamespaceStatusSchema"]
__pdoc__ = {
    "NvmeNamespaceStatusSchema.resource": False,
    "NvmeNamespaceStatusSchema.opts": False,
    "NvmeNamespaceStatus": False,
}


class NvmeNamespaceStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceStatus object"""

    container_state = marshmallow_fields.Str(data_key="container_state", allow_none=True)
    r""" The state of the volume and aggregate that contain the NVMe namespace. Namespaces are only available when their containers are available.


Valid choices:

* online
* aggregate_offline
* volume_offline """

    mapped = marshmallow_fields.Boolean(data_key="mapped", allow_none=True)
    r""" Reports if the NVMe namespace is mapped to an NVMe subsystem.<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more. """

    read_only = marshmallow_fields.Boolean(data_key="read_only", allow_none=True)
    r""" Reports if the NVMe namespace allows only read access. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the NVMe namespace. Normal states for a namespace are _online_ and _offline_. Other states indicate errors.


Valid choices:

* nvfail
* offline
* online
* space_error """

    @property
    def resource(self):
        return NvmeNamespaceStatus

    gettable_fields = [
        "container_state",
        "mapped",
        "read_only",
        "state",
    ]
    """container_state,mapped,read_only,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeNamespaceStatus(Resource):

    _schema = NvmeNamespaceStatusSchema
