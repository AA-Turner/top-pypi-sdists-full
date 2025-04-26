r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3ServicePostResponseRecords", "S3ServicePostResponseRecordsSchema"]
__pdoc__ = {
    "S3ServicePostResponseRecordsSchema.resource": False,
    "S3ServicePostResponseRecordsSchema.opts": False,
    "S3ServicePostResponseRecords": False,
}


class S3ServicePostResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3ServicePostResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_service_post_response_records. """

    job = marshmallow_fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", unknown=EXCLUDE, data_key="job", allow_none=True)
    r""" The job field of the s3_service_post_response_records. """

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_service_user_post_response.S3ServiceUserPostSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" The users field of the s3_service_post_response_records. """

    warning = marshmallow_fields.Nested("netapp_ontap.models.s3_server_warning.S3ServerWarningSchema", unknown=EXCLUDE, data_key="warning", allow_none=True)
    r""" The warning field of the s3_service_post_response_records. """

    @property
    def resource(self):
        return S3ServicePostResponseRecords

    gettable_fields = [
        "links",
        "job",
        "users",
        "warning",
    ]
    """links,job,users,warning,"""

    patchable_fields = [
        "job",
        "users",
    ]
    """job,users,"""

    postable_fields = [
        "job",
        "users",
    ]
    """job,users,"""


class S3ServicePostResponseRecords(Resource):

    _schema = S3ServicePostResponseRecordsSchema
