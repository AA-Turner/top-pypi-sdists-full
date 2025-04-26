r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CollectionLinks", "CollectionLinksSchema"]
__pdoc__ = {
    "CollectionLinksSchema.resource": False,
    "CollectionLinksSchema.opts": False,
    "CollectionLinks": False,
}


class CollectionLinksSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CollectionLinks object"""

    next = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="next", allow_none=True)
    r""" The next field of the collection_links. """

    self_ = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="self", allow_none=True)
    r""" The self_ field of the collection_links. """

    @property
    def resource(self):
        return CollectionLinks

    gettable_fields = [
        "next",
        "self_",
    ]
    """next,self_,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class CollectionLinks(Resource):

    _schema = CollectionLinksSchema
