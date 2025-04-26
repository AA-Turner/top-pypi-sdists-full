r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsDestinationConnectivity", "EmsDestinationConnectivitySchema"]
__pdoc__ = {
    "EmsDestinationConnectivitySchema.resource": False,
    "EmsDestinationConnectivitySchema.opts": False,
    "EmsDestinationConnectivity": False,
}


class EmsDestinationConnectivitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsDestinationConnectivity object"""

    errors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_connectivity_error.EmsConnectivityErrorSchema", unknown=EXCLUDE, allow_none=True), data_key="errors", allow_none=True)
    r""" A list of errors encountered during connectivity checks. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Current connectivity state.

Valid choices:

* success
* fail
* not_supported """

    @property
    def resource(self):
        return EmsDestinationConnectivity

    gettable_fields = [
        "errors",
        "state",
    ]
    """errors,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsDestinationConnectivity(Resource):

    _schema = EmsDestinationConnectivitySchema
