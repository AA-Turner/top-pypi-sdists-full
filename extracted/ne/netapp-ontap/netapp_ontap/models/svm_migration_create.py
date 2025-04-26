r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationCreate", "SvmMigrationCreateSchema"]
__pdoc__ = {
    "SvmMigrationCreateSchema.resource": False,
    "SvmMigrationCreateSchema.opts": False,
    "SvmMigrationCreate": False,
}


class SvmMigrationCreateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationCreate object"""

    job = marshmallow_fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", unknown=EXCLUDE, data_key="job", allow_none=True)
    r""" The job field of the svm_migration_create. """

    num_records = Size(data_key="num_records", allow_none=True)
    r""" Number of records

Example: 1 """

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.svm_migration.SvmMigrationSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" Provides information on SVM migration, default and user specified configurations, the state of the migration, and volume transfer metrics. """

    @property
    def resource(self):
        return SvmMigrationCreate

    gettable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""

    patchable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""

    postable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""


class SvmMigrationCreate(Resource):

    _schema = SvmMigrationCreateSchema
