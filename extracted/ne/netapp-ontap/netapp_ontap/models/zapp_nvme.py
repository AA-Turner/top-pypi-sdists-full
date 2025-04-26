r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvme", "ZappNvmeSchema"]
__pdoc__ = {
    "ZappNvmeSchema.resource": False,
    "ZappNvmeSchema.opts": False,
    "ZappNvme": False,
}


class ZappNvmeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvme object"""

    components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_components.ZappNvmeComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="components", allow_none=True)
    r""" The components field of the zapp_nvme. """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The name of the host OS running the application.

Valid choices:

* aix
* linux
* vmware
* windows """

    rpo = marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_rpo.ZappNvmeRpoSchema", unknown=EXCLUDE, data_key="rpo", allow_none=True)
    r""" The rpo field of the zapp_nvme. """

    @property
    def resource(self):
        return ZappNvme

    gettable_fields = [
        "components",
        "os_type",
        "rpo",
    ]
    """components,os_type,rpo,"""

    patchable_fields = [
        "components",
        "rpo",
    ]
    """components,rpo,"""

    postable_fields = [
        "components",
        "os_type",
        "rpo",
    ]
    """components,os_type,rpo,"""


class ZappNvme(Resource):

    _schema = ZappNvmeSchema
