r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateSimulate", "AggregateSimulateSchema"]
__pdoc__ = {
    "AggregateSimulateSchema.resource": False,
    "AggregateSimulateSchema.opts": False,
    "AggregateSimulate": False,
}


class AggregateSimulateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateSimulate object"""

    job = marshmallow_fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", unknown=EXCLUDE, data_key="job", allow_none=True)
    r""" The job field of the aggregate_simulate. """

    num_records = Size(data_key="num_records", allow_none=True)
    r""" Number of records

Example: 1 """

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" The records field of the aggregate_simulate. """

    warnings = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.aggregate_warning.AggregateWarningSchema", unknown=EXCLUDE, allow_none=True), data_key="warnings", allow_none=True)
    r""" List of validation warnings and remediation advice for the aggregate simulate behavior. """

    @property
    def resource(self):
        return AggregateSimulate

    gettable_fields = [
        "job",
        "num_records",
        "records",
        "warnings",
    ]
    """job,num_records,records,warnings,"""

    patchable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""

    postable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""


class AggregateSimulate(Resource):

    _schema = AggregateSimulateSchema
