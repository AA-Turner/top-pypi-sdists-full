r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockLogArchive", "SnaplockLogArchiveSchema"]
__pdoc__ = {
    "SnaplockLogArchiveSchema.resource": False,
    "SnaplockLogArchiveSchema.opts": False,
    "SnaplockLogArchive": False,
}


class SnaplockLogArchiveSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLogArchive object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snaplock_log_archive. """

    archive = marshmallow_fields.Boolean(data_key="archive", allow_none=True)
    r""" Archive the specified SnapLock log file for the given base_name, and create a new log file. If base_name is not mentioned, archive all log files. """

    base_name = marshmallow_fields.Str(data_key="base_name", allow_none=True)
    r""" Base name of log archive

Valid choices:

* legal_hold
* privileged_delete
* system """

    @property
    def resource(self):
        return SnaplockLogArchive

    gettable_fields = [
        "links",
    ]
    """links,"""

    patchable_fields = [
        "archive",
        "base_name",
    ]
    """archive,base_name,"""

    postable_fields = [
    ]
    """"""


class SnaplockLogArchive(Resource):

    _schema = SnaplockLogArchiveSchema
