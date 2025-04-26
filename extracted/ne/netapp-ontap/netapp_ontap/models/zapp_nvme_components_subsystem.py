r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeComponentsSubsystem", "ZappNvmeComponentsSubsystemSchema"]
__pdoc__ = {
    "ZappNvmeComponentsSubsystemSchema.resource": False,
    "ZappNvmeComponentsSubsystemSchema.opts": False,
    "ZappNvmeComponentsSubsystem": False,
}


class ZappNvmeComponentsSubsystemSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeComponentsSubsystem object"""

    hosts = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_components_subsystem_hosts.ZappNvmeComponentsSubsystemHostsSchema", unknown=EXCLUDE, allow_none=True), data_key="hosts", allow_none=True)
    r""" The hosts field of the zapp_nvme_components_subsystem. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the subsystem accessing the component. If neither the name nor the UUID is provided, the name defaults to &lt;application-name&gt;_&lt;component-name&gt;, whether that subsystem already exists or not. """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The name of the host OS accessing the component. The default value is the host OS that is running the application.

Valid choices:

* aix
* linux
* vmware
* windows """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID of an existing subsystem to be granted access to the component. """

    @property
    def resource(self):
        return ZappNvmeComponentsSubsystem

    gettable_fields = [
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """hosts,name,os_type,uuid,"""

    patchable_fields = [
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """hosts,name,os_type,uuid,"""

    postable_fields = [
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """hosts,name,os_type,uuid,"""


class ZappNvmeComponentsSubsystem(Resource):

    _schema = ZappNvmeComponentsSubsystemSchema
