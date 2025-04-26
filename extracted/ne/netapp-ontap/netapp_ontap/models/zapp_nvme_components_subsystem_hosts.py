r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeComponentsSubsystemHosts", "ZappNvmeComponentsSubsystemHostsSchema"]
__pdoc__ = {
    "ZappNvmeComponentsSubsystemHostsSchema.resource": False,
    "ZappNvmeComponentsSubsystemHostsSchema.opts": False,
    "ZappNvmeComponentsSubsystemHosts": False,
}


class ZappNvmeComponentsSubsystemHostsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeComponentsSubsystemHosts object"""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_components_subsystem_hosts_dh_hmac_chap.ZappNvmeComponentsSubsystemHostsDhHmacChapSchema", unknown=EXCLUDE, data_key="dh_hmac_chap", allow_none=True)
    r""" The dh_hmac_chap field of the zapp_nvme_components_subsystem_hosts. """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The host NQN. """

    priority = marshmallow_fields.Str(data_key="priority", allow_none=True)
    r""" Host Priority.

Valid choices:

* high
* regular """

    @property
    def resource(self):
        return ZappNvmeComponentsSubsystemHosts

    gettable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
    ]
    """dh_hmac_chap,nqn,priority,"""

    patchable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
    ]
    """dh_hmac_chap,nqn,priority,"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
    ]
    """dh_hmac_chap,nqn,priority,"""


class ZappNvmeComponentsSubsystemHosts(Resource):

    _schema = ZappNvmeComponentsSubsystemHostsSchema
