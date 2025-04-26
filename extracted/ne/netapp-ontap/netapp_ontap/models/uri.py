r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Uri", "UriSchema"]
__pdoc__ = {
    "UriSchema.resource": False,
    "UriSchema.opts": False,
    "Uri": False,
}


class UriSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Uri object"""

    fragment = marshmallow_fields.Str(data_key="fragment", allow_none=True)
    r""" The fragment field of the uri.

Example: top """

    host = marshmallow_fields.Str(data_key="host", allow_none=True)
    r""" The host field of the uri.

Example: 10.1.1.1 """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" The path field of the uri.

Example: /api/cluster """

    port = Size(data_key="port", allow_none=True)
    r""" The port field of the uri.

Example: 433 """

    query = marshmallow_fields.Str(data_key="query", allow_none=True)
    r""" The query field of the uri.

Example: key1=value1 """

    scheme = marshmallow_fields.Str(data_key="scheme", allow_none=True)
    r""" The scheme field of the uri.

Example: https """

    userinfo = marshmallow_fields.Str(data_key="userinfo", allow_none=True)
    r""" The userinfo field of the uri.

Example: john.doe """

    @property
    def resource(self):
        return Uri

    gettable_fields = [
        "fragment",
        "host",
        "path",
        "port",
        "query",
        "scheme",
        "userinfo",
    ]
    """fragment,host,path,port,query,scheme,userinfo,"""

    patchable_fields = [
        "fragment",
        "host",
        "path",
        "port",
        "query",
        "scheme",
        "userinfo",
    ]
    """fragment,host,path,port,query,scheme,userinfo,"""

    postable_fields = [
        "fragment",
        "host",
        "path",
        "port",
        "query",
        "scheme",
        "userinfo",
    ]
    """fragment,host,path,port,query,scheme,userinfo,"""


class Uri(Resource):

    _schema = UriSchema
