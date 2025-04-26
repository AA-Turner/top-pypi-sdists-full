r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEvents", "FpolicyEventsSchema"]
__pdoc__ = {
    "FpolicyEventsSchema.resource": False,
    "FpolicyEventsSchema.opts": False,
    "FpolicyEvents": False,
}


class FpolicyEventsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEvents object"""

    file_operations = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_event_file_operations.FpolicyEventFileOperationsSchema", unknown=EXCLUDE, data_key="file_operations", allow_none=True)
    r""" Specifies the file operations for the FPolicy event. You must specify a valid protocol in the protocol parameter.
The event will check the operations specified from all client requests using the protocol. """

    filters = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_event_filters.FpolicyEventFiltersSchema", unknown=EXCLUDE, data_key="filters", allow_none=True)
    r""" Specifies the list of filters for a given file operation for the specified protocol.
When you specify the filters, you must specify the valid protocols and a valid file operations. """

    monitor_fileop_failure = marshmallow_fields.Boolean(data_key="monitor_fileop_failure", allow_none=True)
    r""" Specifies whether failed file operations monitoring is required. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the FPolicy event.

Example: event_cifs """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" Protocol for which event is created. If you specify protocol, then you
must also specify a valid value for the file operation parameters.
  The value of this parameter must be one of the following:

    * cifs  - for the CIFS protocol.
    * nfsv3 - for the NFSv3 protocol.
    * nfsv4 - for the NFSv4 protocol.


Valid choices:

* cifs
* nfsv3
* nfsv4 """

    volume_monitoring = marshmallow_fields.Boolean(data_key="volume_monitoring", allow_none=True)
    r""" Specifies whether volume operation monitoring is required. """

    @property
    def resource(self):
        return FpolicyEvents

    gettable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "name",
        "protocol",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,name,protocol,volume_monitoring,"""

    patchable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "protocol",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,protocol,volume_monitoring,"""

    postable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "name",
        "protocol",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,name,protocol,volume_monitoring,"""


class FpolicyEvents(Resource):

    _schema = FpolicyEventsSchema
