r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsMessageResponseRecords", "EmsMessageResponseRecordsSchema"]
__pdoc__ = {
    "EmsMessageResponseRecordsSchema.resource": False,
    "EmsMessageResponseRecordsSchema.opts": False,
    "EmsMessageResponseRecords": False,
}


class EmsMessageResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsMessageResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_message_response_records. """

    corrective_action = marshmallow_fields.Str(data_key="corrective_action", allow_none=True)
    r""" Corrective action """

    deprecated = marshmallow_fields.Boolean(data_key="deprecated", allow_none=True)
    r""" Is deprecated?

Example: true """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" Description of the event. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the event.

Example: callhome.spares.low """

    severity = marshmallow_fields.Str(data_key="severity", allow_none=True)
    r""" Severity

Valid choices:

* emergency
* alert
* error
* notice
* informational
* debug """

    snmp_trap_type = marshmallow_fields.Str(data_key="snmp_trap_type", allow_none=True)
    r""" SNMP trap type

Valid choices:

* standard
* built_in
* severity_based """

    @property
    def resource(self):
        return EmsMessageResponseRecords

    gettable_fields = [
        "links",
        "corrective_action",
        "deprecated",
        "description",
        "name",
        "severity",
        "snmp_trap_type",
    ]
    """links,corrective_action,deprecated,description,name,severity,snmp_trap_type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsMessageResponseRecords(Resource):

    _schema = EmsMessageResponseRecordsSchema
