r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["JobLink", "JobLinkSchema"]
__pdoc__ = {
    "JobLinkSchema.resource": False,
    "JobLinkSchema.opts": False,
    "JobLink": False,
}


class JobLinkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the JobLink object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the job_link. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID of the asynchronous job that is triggered by a POST, PATCH, or DELETE operation. """

    @property
    def resource(self):
        return JobLink

    gettable_fields = [
        "links",
        "uuid",
    ]
    """links,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class JobLink(Resource):

    _schema = JobLinkSchema
