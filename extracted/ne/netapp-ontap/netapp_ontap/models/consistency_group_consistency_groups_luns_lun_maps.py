r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsLunsLunMaps", "ConsistencyGroupConsistencyGroupsLunsLunMapsSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsLunsLunMapsSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsLunsLunMapsSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsLunsLunMaps": False,
}


class ConsistencyGroupConsistencyGroupsLunsLunMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsLunsLunMaps object"""

    igroup = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_igroup.ConsistencyGroupIgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" An initiator group (igroup) is a collection of Fibre Channel (FC) world wide port names (WWPNs), and/or iSCSI Qualified Names (IQNs), and/or iSCSI EUIs (Extended Unique Identifiers) that identify host endpoints.<br/>
Initiator groups are used to control which hosts can access specific LUNs. To grant access to a LUN from one or more hosts, create an initiator group containing the host initiator names, then create a LUN map that associates the initiator group with the LUN.<br/>
An initiator group may contain either initiators or other initiator groups, but not both simultaneously. When a parent initiator group is mapped, it inherits all of the initiators of any initiator groups nested below it. If any nested initiator group is modified to contain different initiators, the parent initiator groups inherit the change. A parent can have many nested initiator groups and an initiator group can be nested under multiple parents. Initiators can only be added or removed from the initiator group that directly contains them. The maximum supported depth of nesting is three layers.<br/>
Best practice when using nested initiator groups is to match host hierarchies. A single initiator group should correspond to a single host. If a LUN needs to be mapped to multiple hosts, the initiator groups representing those hosts should be aggregated into a parent initiator group and the LUN should be mapped to that initiator group. For multi-ported hosts, initiators have a comment property where the port corresponding to the initiator can be documented.<br/>
An initiator can appear in multiple initiator groups. An initiator group can be mapped to multiple LUNs. A specific initiator can be mapped to a specific LUN only once. With the introduction of nestable initiator groups, best practice is to use the hierarchy such that an initiator is only a direct member of a single initiator group, and that initiator group can then be referenced by other initiator groups.<br/>
All initiators or nested initiator groups in an initiator group must be from the same operating system. The initiator group's operating system is specified when the initiator group is created.<br/>
When an initiator group is created, the `protocol` property is used to restrict member initiators to Fibre Channel (_fcp_), iSCSI (_iscsi_), or both (_mixed_). Initiator groups within a nested hierarchy may not have conflicting protocols.<br/>
Zero or more initiators or nested initiator groups can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. Initiator groups containing other initiator groups report the aggregated list of initiators from all nested initiator groups, but modifications of the initiator list must be performed on the initiator group that directly contains the initiators. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details.<br/> """

    logical_unit_number = Size(data_key="logical_unit_number", allow_none=True)
    r""" The logical unit number assigned to the LUN when mapped to the specified initiator group. The number is used to identify the LUN to initiators in the initiator group when communicating through the Fibre Channel Protocol or iSCSI. Optional in POST; if no value is provided, ONTAP assigns the lowest available value. This property is not supported when the _provisioning_options.count_ property is 2 or more. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsLunsLunMaps

    gettable_fields = [
        "igroup",
        "logical_unit_number",
    ]
    """igroup,logical_unit_number,"""

    patchable_fields = [
        "igroup",
    ]
    """igroup,"""

    postable_fields = [
        "igroup",
        "logical_unit_number",
    ]
    """igroup,logical_unit_number,"""


class ConsistencyGroupConsistencyGroupsLunsLunMaps(Resource):

    _schema = ConsistencyGroupConsistencyGroupsLunsLunMapsSchema
