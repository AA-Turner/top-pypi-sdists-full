r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MongoDbOnSanNewIgroupsIgroups", "MongoDbOnSanNewIgroupsIgroupsSchema"]
__pdoc__ = {
    "MongoDbOnSanNewIgroupsIgroupsSchema.resource": False,
    "MongoDbOnSanNewIgroupsIgroupsSchema.opts": False,
    "MongoDbOnSanNewIgroupsIgroups": False,
}


class MongoDbOnSanNewIgroupsIgroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MongoDbOnSanNewIgroupsIgroups object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of an igroup to nest within a parent igroup. Mutually exclusive with initiators and initiator_objects. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID of an igroup to nest within a parent igroup Usage: &lt;UUID&gt; """

    @property
    def resource(self):
        return MongoDbOnSanNewIgroupsIgroups

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class MongoDbOnSanNewIgroupsIgroups(Resource):

    _schema = MongoDbOnSanNewIgroupsIgroupsSchema
