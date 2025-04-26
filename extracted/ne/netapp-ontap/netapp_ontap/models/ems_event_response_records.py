r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventResponseRecords", "EmsEventResponseRecordsSchema"]
__pdoc__ = {
    "EmsEventResponseRecordsSchema.resource": False,
    "EmsEventResponseRecordsSchema.opts": False,
    "EmsEventResponseRecords": False,
}


class EmsEventResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.ems_event_links.EmsEventLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_event_response_records. """

    index = Size(data_key="index", allow_none=True)
    r""" Index of the event. Returned by default.

Example: 1 """

    log_message = marshmallow_fields.Str(data_key="log_message", allow_none=True)
    r""" A formatted text string populated with parameter details. Returned by default. """

    message = marshmallow_fields.Nested("netapp_ontap.models.ems_event_message1.EmsEventMessage1Schema", unknown=EXCLUDE, data_key="message", allow_none=True)
    r""" The message field of the ems_event_response_records. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the ems_event_response_records. """

    parameters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_event_parameters.EmsEventParametersSchema", unknown=EXCLUDE, allow_none=True), data_key="parameters", allow_none=True)
    r""" A list of parameters provided with the EMS event. """

    source = marshmallow_fields.Str(data_key="source", allow_none=True)
    r""" Source """

    time = ImpreciseDateTime(data_key="time", allow_none=True)
    r""" Timestamp of the event. Returned by default. """

    @property
    def resource(self):
        return EmsEventResponseRecords

    gettable_fields = [
        "links",
        "index",
        "log_message",
        "message",
        "node.links",
        "node.name",
        "node.uuid",
        "parameters",
        "source",
        "time",
    ]
    """links,index,log_message,message,node.links,node.name,node.uuid,parameters,source,time,"""

    patchable_fields = [
        "log_message",
    ]
    """log_message,"""

    postable_fields = [
    ]
    """"""


class EmsEventResponseRecords(Resource):

    _schema = EmsEventResponseRecordsSchema
