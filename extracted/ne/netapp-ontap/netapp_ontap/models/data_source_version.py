r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataSourceVersion", "DataSourceVersionSchema"]
__pdoc__ = {
    "DataSourceVersionSchema.resource": False,
    "DataSourceVersionSchema.opts": False,
    "DataSourceVersion": False,
}

class DataSourceVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataSourceVersion object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the data_source_version. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the data source.


Example: vol1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the data source.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_source_version_version", "DataSourceVersionVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a data source. Defaults to the current version. """

    @property
    def resource(self):
        return DataSourceVersion

    gettable_fields = [
        "links",
        "name",
        "uuid",
        "version",
    ]
    """links,name,uuid,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataSourceVersion(Resource):

    _schema = DataSourceVersionSchema
