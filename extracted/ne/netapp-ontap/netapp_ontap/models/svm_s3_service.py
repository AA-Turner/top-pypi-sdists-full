r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmS3Service", "SvmS3ServiceSchema"]
__pdoc__ = {
    "SvmS3ServiceSchema.resource": False,
    "SvmS3ServiceSchema.opts": False,
    "SvmS3Service": False,
}


class SvmS3ServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmS3Service object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_s3_service. """

    allowed = marshmallow_fields.Boolean(data_key="allowed", allow_none=True)
    r""" If this is set to true, an SVM administrator can manage the S3 service. If it is false, only the cluster administrator can manage the service. """

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", unknown=EXCLUDE, data_key="certificate", allow_none=True)
    r""" The certificate field of the svm_s3_service. """

    default_unix_user = marshmallow_fields.Str(data_key="default_unix_user", allow_none=True)
    r""" Specifies the default UNIX user for NAS Access. """

    default_win_user = marshmallow_fields.Str(data_key="default_win_user", allow_none=True)
    r""" Specifies the default Windows user for NAS Access. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether or not to enable S3. Setting this value to true creates a service if one is not yet created. """

    is_http_enabled = marshmallow_fields.Boolean(data_key="is_http_enabled", allow_none=True)
    r""" Specifies whether HTTP is enabled on the S3 server. By default, HTTP is disabled on the S3 server. """

    is_https_enabled = marshmallow_fields.Boolean(data_key="is_https_enabled", allow_none=True)
    r""" Specifies whether HTTPS is enabled on the S3 server. By default, HTTPS is enabled on the S3 server. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the S3 server. A server name length can range from 1 to 253 characters and can only contain the following combination of characters 0-9, A-Z, a-z, ".", and "-".

Example: s3-server-1 """

    port = Size(data_key="port", allow_none=True)
    r""" Specifies the HTTP listener port for the S3 server. By default, HTTP is enabled on port 80. """

    secure_port = Size(data_key="secure_port", allow_none=True)
    r""" Specifies the HTTPS listener port for the S3 server. By default, HTTPS is enabled on port 443. """

    @property
    def resource(self):
        return SvmS3Service

    gettable_fields = [
        "links",
        "allowed",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "name",
        "port",
        "secure_port",
    ]
    """links,allowed,certificate.links,certificate.name,certificate.uuid,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,name,port,secure_port,"""

    patchable_fields = [
        "allowed",
        "certificate.name",
        "certificate.uuid",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "name",
        "port",
        "secure_port",
    ]
    """allowed,certificate.name,certificate.uuid,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,name,port,secure_port,"""

    postable_fields = [
        "allowed",
        "certificate.name",
        "certificate.uuid",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "name",
        "port",
        "secure_port",
    ]
    """allowed,certificate.name,certificate.uuid,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,name,port,secure_port,"""


class SvmS3Service(Resource):

    _schema = SvmS3ServiceSchema
