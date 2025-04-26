r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventMessage1", "EmsEventMessage1Schema"]
__pdoc__ = {
    "EmsEventMessage1Schema.resource": False,
    "EmsEventMessage1Schema.opts": False,
    "EmsEventMessage1": False,
}


class EmsEventMessage1Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventMessage1 object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_event_message1. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Message name of the event. Returned by default.

Example: callhome.spares.low """

    severity = marshmallow_fields.Str(data_key="severity", allow_none=True)
    r""" Severity of the event. Returned by default.

Valid choices:

* emergency
* alert
* error
* notice
* informational
* debug """

    @property
    def resource(self):
        return EmsEventMessage1

    gettable_fields = [
        "links",
        "name",
        "severity",
    ]
    """links,name,severity,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsEventMessage1(Resource):

    _schema = EmsEventMessage1Schema
