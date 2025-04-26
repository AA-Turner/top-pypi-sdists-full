r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagnosticsConfigreplication", "MetroclusterDiagnosticsConfigreplicationSchema"]
__pdoc__ = {
    "MetroclusterDiagnosticsConfigreplicationSchema.resource": False,
    "MetroclusterDiagnosticsConfigreplicationSchema.opts": False,
    "MetroclusterDiagnosticsConfigreplication": False,
}


class MetroclusterDiagnosticsConfigreplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagnosticsConfigreplication object"""

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Status of diagnostic operation for this component.

Valid choices:

* ok
* warning
* not_run
* not_applicable """

    summary = marshmallow_fields.Nested("netapp_ontap.models.error_arguments.ErrorArgumentsSchema", unknown=EXCLUDE, data_key="summary", allow_none=True)
    r""" The summary field of the metrocluster_diagnostics_configreplication. """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" Time of the most recent diagnostic operation for this component

Example: 2016-03-14T22:35:16.000+0000 """

    @property
    def resource(self):
        return MetroclusterDiagnosticsConfigreplication

    gettable_fields = [
        "state",
        "summary",
        "timestamp",
    ]
    """state,summary,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class MetroclusterDiagnosticsConfigreplication(Resource):

    _schema = MetroclusterDiagnosticsConfigreplicationSchema
