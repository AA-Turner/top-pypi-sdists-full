r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupNamespace", "ConsistencyGroupNamespaceSchema"]
__pdoc__ = {
    "ConsistencyGroupNamespaceSchema.resource": False,
    "ConsistencyGroupNamespaceSchema.opts": False,
    "ConsistencyGroupNamespace": False,
}


class ConsistencyGroupNamespaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupNamespace object"""

    auto_delete = marshmallow_fields.Boolean(data_key="auto_delete", allow_none=True)
    r""" * **Unified ONTAP**:
This property marks the NVMe namespace for auto deletion when the volume containing the namespace runs out of space. This is most commonly set on namespace clones.<br/>
When set to _true_, the NVMe namespace becomes eligible for automatic deletion when the volume runs out of space. Auto deletion only occurs when the volume containing the namespace is also configured for auto deletion and free space in the volume decreases below a particular threshold.<br/>
This property is optional in POST and PATCH. The default value for a new NVMe namespace is _false_.<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.

* **ASA r2**:
This property is not supported. It cannot be set in POST or PATCH and will not be returned by GET. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A configurable comment available for use by the administrator. Valid in POST and PATCH. """

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" The time the NVMe namespace was created.

Example: 2018-06-04T19:00:00.000+0000 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" The enabled state of the NVMe namespace. Certain error conditions cause the namespace to become disabled. If the namespace is disabled, check the `status.state` property to determine what error disabled the namespace. An NVMe namespace is enabled automatically when it is created. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the NVMe namespace.
### Platform Specifics

* **Unified ONTAP**:
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
Renaming an NVMe namespace is not supported. Valid in POST.

* **ASA r2**:
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
Renaming an NVMe namespace is supported. Valid in POST and PATCH.


Example: /vol/volume1/qtree1/namespace1 """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The operating system type of the NVMe namespace.<br/>
Required in POST when creating an NVMe namespace that is not a clone of another. Disallowed in POST when creating a namespace clone.


Valid choices:

* aix
* linux
* vmware
* windows """

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_vdisk_provisioning_options.ConsistencyGroupVdiskProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options", allow_none=True)
    r""" Options that are applied to the operation. """

    space = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_namespace_space.ConsistencyGroupNamespaceSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The storage space related properties of the NVMe namespace. """

    status = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_namespace_status.ConsistencyGroupNamespaceStatusSchema", unknown=EXCLUDE, data_key="status", allow_none=True)
    r""" Status information about the NVMe namespace. """

    subsystem_map = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_namespace_subsystem_map.ConsistencyGroupNamespaceSubsystemMapSchema", unknown=EXCLUDE, data_key="subsystem_map", allow_none=True)
    r""" The NVMe subsystem with which the NVMe namespace is associated. A namespace can be mapped to zero (0) or one (1) subsystems.<br/>
There is an added computational cost to retrieving property values for `subsystem_map`.
They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the NVMe namespace.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupNamespace

    gettable_fields = [
        "auto_delete",
        "comment",
        "create_time",
        "enabled",
        "name",
        "os_type",
        "space",
        "status",
        "subsystem_map",
        "uuid",
    ]
    """auto_delete,comment,create_time,enabled,name,os_type,space,status,subsystem_map,uuid,"""

    patchable_fields = [
        "auto_delete",
        "comment",
        "name",
        "provisioning_options",
        "space",
        "subsystem_map",
    ]
    """auto_delete,comment,name,provisioning_options,space,subsystem_map,"""

    postable_fields = [
        "auto_delete",
        "comment",
        "name",
        "os_type",
        "provisioning_options",
        "space",
        "subsystem_map",
    ]
    """auto_delete,comment,name,os_type,provisioning_options,space,subsystem_map,"""


class ConsistencyGroupNamespace(Resource):

    _schema = ConsistencyGroupNamespaceSchema
