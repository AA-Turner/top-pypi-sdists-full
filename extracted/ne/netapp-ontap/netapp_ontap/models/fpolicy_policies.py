r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyPolicies", "FpolicyPoliciesSchema"]
__pdoc__ = {
    "FpolicyPoliciesSchema.resource": False,
    "FpolicyPoliciesSchema.opts": False,
    "FpolicyPolicies": False,
}


class FpolicyPoliciesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyPolicies object"""

    allow_privileged_access = marshmallow_fields.Boolean(data_key="allow_privileged_access", allow_none=True)
    r""" Specifies whether privileged access is required for FPolicy servers.
Privileged access is used when the FPolicy server requires direct
access to the cluster nodes. When this parameter is set to true,
FPolicy servers can access files on the cluster using a separate
data channel with privileged access. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies if the policy is enabled on the SVM or not. If no value is
mentioned for this field but priority is set, then this policy will be enabled. """

    engine = marshmallow_fields.Nested("netapp_ontap.resources.fpolicy_engine.FpolicyEngineSchema", unknown=EXCLUDE, data_key="engine", allow_none=True)
    r""" The engine field of the fpolicy_policies. """

    events = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.fpolicy_event.FpolicyEventSchema", unknown=EXCLUDE, allow_none=True), data_key="events", allow_none=True)
    r""" The events field of the fpolicy_policies.

Example: ["event_cifs","event_open"] """

    mandatory = marshmallow_fields.Boolean(data_key="mandatory", allow_none=True)
    r""" Specifies what action to take on a file access event in a case when all primary and secondary servers are down or no response is received from the FPolicy servers within a given timeout period. When this parameter is set to true, file access events will be denied under these circumstances. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the policy.

Example: fp_policy_1 """

    passthrough_read = marshmallow_fields.Boolean(data_key="passthrough_read", allow_none=True)
    r""" Specifies whether passthrough-read should be allowed for FPolicy servers
registered for the policy. Passthrough-read is a way to read data for
offline files without restoring the files to primary storage. Offline
files are files that have been moved to secondary storage. """

    persistent_store = marshmallow_fields.Str(data_key="persistent_store", allow_none=True)
    r""" Specifies the persistent storage name. This can then be used
to enable persistent mode for FPolicy events.


Example: ps1 """

    priority = Size(data_key="priority", allow_none=True)
    r""" Specifies the priority that is assigned to this policy.

Example: 1 """

    privileged_user = marshmallow_fields.Str(data_key="privileged_user", allow_none=True)
    r""" Specifies the privileged user name for accessing files on the cluster
using a separate data channel with privileged access. The input for
this field should be in "domain\username" format.


Example: mydomain\testuser """

    scope = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_policies_scope.FpolicyPoliciesScopeSchema", unknown=EXCLUDE, data_key="scope", allow_none=True)
    r""" The scope field of the fpolicy_policies. """

    @property
    def resource(self):
        return FpolicyPolicies

    gettable_fields = [
        "allow_privileged_access",
        "enabled",
        "engine.links",
        "engine.name",
        "events",
        "mandatory",
        "name",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
    ]
    """allow_privileged_access,enabled,engine.links,engine.name,events,mandatory,name,passthrough_read,persistent_store,priority,privileged_user,scope,"""

    patchable_fields = [
        "allow_privileged_access",
        "enabled",
        "engine.name",
        "events",
        "mandatory",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
    ]
    """allow_privileged_access,enabled,engine.name,events,mandatory,passthrough_read,persistent_store,priority,privileged_user,scope,"""

    postable_fields = [
        "engine.name",
        "events",
        "mandatory",
        "name",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
    ]
    """engine.name,events,mandatory,name,passthrough_read,persistent_store,priority,privileged_user,scope,"""


class FpolicyPolicies(Resource):

    _schema = FpolicyPoliciesSchema
