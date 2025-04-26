r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IkpKmsKey", "IkpKmsKeySchema"]
__pdoc__ = {
    "IkpKmsKeySchema.resource": False,
    "IkpKmsKeySchema.opts": False,
    "IkpKmsKey": False,
}


class IkpKmsKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IkpKmsKey object"""

    key_id = marshmallow_fields.Str(data_key="key_id", allow_none=True)
    r""" Key identifier of the IKP KMS key encryption key.

Example: 12345678-1234-1234-1234-123456789101 """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the ikp_kms_key. """

    @property
    def resource(self):
        return IkpKmsKey

    gettable_fields = [
        "key_id",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """key_id,scope,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "svm.name",
        "svm.uuid",
    ]
    """svm.name,svm.uuid,"""

    postable_fields = [
        "key_id",
        "svm.name",
        "svm.uuid",
    ]
    """key_id,svm.name,svm.uuid,"""


class IkpKmsKey(Resource):

    _schema = IkpKmsKeySchema
