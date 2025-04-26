r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeComponentsSubsystemHostsDhHmacChap", "ZappNvmeComponentsSubsystemHostsDhHmacChapSchema"]
__pdoc__ = {
    "ZappNvmeComponentsSubsystemHostsDhHmacChapSchema.resource": False,
    "ZappNvmeComponentsSubsystemHostsDhHmacChapSchema.opts": False,
    "ZappNvmeComponentsSubsystemHostsDhHmacChap": False,
}


class ZappNvmeComponentsSubsystemHostsDhHmacChapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeComponentsSubsystemHostsDhHmacChap object"""

    controller_secret_key = marshmallow_fields.Str(data_key="controller_secret_key", allow_none=True)
    r""" Authentication Controller Secret. """

    group_size = marshmallow_fields.Str(data_key="group_size", allow_none=True)
    r""" Authentication Diffie-Hellman Group.

Valid choices:

* 2048_bit
* 3072_bit
* 4096_bit
* 6144_bit
* 8192_bit
* none """

    hash_function = marshmallow_fields.Str(data_key="hash_function", allow_none=True)
    r""" Authentication Hash Function.

Valid choices:

* sha_256
* sha_512 """

    host_secret_key = marshmallow_fields.Str(data_key="host_secret_key", allow_none=True)
    r""" Authentication Host Secret. """

    @property
    def resource(self):
        return ZappNvmeComponentsSubsystemHostsDhHmacChap

    gettable_fields = [
        "group_size",
        "hash_function",
    ]
    """group_size,hash_function,"""

    patchable_fields = [
        "controller_secret_key",
        "group_size",
        "hash_function",
        "host_secret_key",
    ]
    """controller_secret_key,group_size,hash_function,host_secret_key,"""

    postable_fields = [
        "controller_secret_key",
        "group_size",
        "hash_function",
        "host_secret_key",
    ]
    """controller_secret_key,group_size,hash_function,host_secret_key,"""


class ZappNvmeComponentsSubsystemHostsDhHmacChap(Resource):

    _schema = ZappNvmeComponentsSubsystemHostsDhHmacChapSchema
