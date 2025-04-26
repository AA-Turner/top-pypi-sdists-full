r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsDestinationResponseRecords", "EmsDestinationResponseRecordsSchema"]
__pdoc__ = {
    "EmsDestinationResponseRecordsSchema.resource": False,
    "EmsDestinationResponseRecordsSchema.opts": False,
    "EmsDestinationResponseRecords": False,
}


class EmsDestinationResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsDestinationResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_destination_response_records. """

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", unknown=EXCLUDE, data_key="access_control_role", allow_none=True)
    r""" The access_control_role field of the ems_destination_response_records. """

    certificate = marshmallow_fields.Nested("netapp_ontap.models.ems_certificate.EmsCertificateSchema", unknown=EXCLUDE, data_key="certificate", allow_none=True)
    r""" Specifies the client-side certificate used by the ONTAP system when mutual authentication is required. This object is only applicable for __rest_api__ type destinations. Both the `ca` and `serial_number` fields must be specified when configuring a certificate in a PATCH or POST request. The `name` field is read-only and cannot be used to configure a client-side certificate. """

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.ems_destination_response_records_connectivity.EmsDestinationResponseRecordsConnectivitySchema", unknown=EXCLUDE, data_key="connectivity", allow_none=True)
    r""" The connectivity field of the ems_destination_response_records. """

    destination = marshmallow_fields.Str(data_key="destination", allow_none=True)
    r""" Event destination

Example: administrator@mycompany.com """

    filters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_destination_filters.EmsDestinationFiltersSchema", unknown=EXCLUDE, allow_none=True), data_key="filters", allow_none=True)
    r""" The filters field of the ems_destination_response_records. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Destination name.  Valid in POST.

Example: Admin_Email """

    syslog = marshmallow_fields.Nested("netapp_ontap.models.ems_syslog.EmsSyslogSchema", unknown=EXCLUDE, data_key="syslog", allow_none=True)
    r""" The syslog field of the ems_destination_response_records. """

    system_defined = marshmallow_fields.Boolean(data_key="system_defined", allow_none=True)
    r""" Flag indicating system-defined destinations.

Example: true """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Type of destination. Valid in POST.

Valid choices:

* snmp
* email
* syslog
* rest_api """

    @property
    def resource(self):
        return EmsDestinationResponseRecords

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "certificate",
        "connectivity",
        "destination",
        "filters.links",
        "filters.name",
        "name",
        "syslog",
        "system_defined",
        "type",
    ]
    """links,access_control_role.links,access_control_role.name,certificate,connectivity,destination,filters.links,filters.name,name,syslog,system_defined,type,"""

    patchable_fields = [
        "certificate",
        "connectivity",
        "destination",
        "filters.name",
        "syslog",
    ]
    """certificate,connectivity,destination,filters.name,syslog,"""

    postable_fields = [
        "certificate",
        "connectivity",
        "destination",
        "filters.name",
        "name",
        "syslog",
        "type",
    ]
    """certificate,connectivity,destination,filters.name,name,syslog,type,"""


class EmsDestinationResponseRecords(Resource):

    _schema = EmsDestinationResponseRecordsSchema
