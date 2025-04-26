r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Managing SnapMirror policies
This API is used to manage SnapMirror policies of type "async" and "sync". When applied to a SnapMirror relationship, the SnapMirror policy controls the behavior of the relationship and specifies the configuration attributes for that relationship.<br>The policy type "async" can be associated with a SnapMirror relationship that has either a FlexVol volume, FlexGroup volume, or SVM as the endpoint.<br>The policy type "sync" can be associated with a SnapMirror relationship that has a FlexVol volume or a consistency group as the endpoint. The policy type "sync" can have a "sync_type" of either "sync", "strict_sync", "automated_failover" or "automated_failover_duplex". If the "sync_type" is "sync", a write success is returned to the client after writing the data to the primary endpoint and before writing the data to the secondary endpoint. If the "sync_type" is "strict_sync", a write success is returned to the client after writing the data to both primary and secondary endpoints.<br>A "sync_type" of "automated_failover" can be associated with a SnapMirror relationship that has a consistency group as the endpoint and provides asymmetric active active access to the two storage copies.</br>A "sync_type" of "automated_failover_duplex" can be associated with a SnapMirror relationship that has a consistency group as the endpoint and provides symmetric active active access to the two storage copies.<br>
Mapping of SnapMirror policies from CLI to REST
|        CLI               |            REST                   |
|--------------------------|-----------------------------------|
|mirror-vault              | async                             |
|async-mirror w/           | async w/                          |
| all_source_snapshots     |  copy_all_source_snapshots        |
|async-mirror w/o          | async w/                          |
| all_source_snapshots     |  copy_latest_source_snapshot      |
|vault                     | async w/                          |
|                          |  create_snapshot_on_source        |
|--------------------------|-----------------------------------|
|                          |       |  sync_type                |
|                          |       |---------------------------|
|sync-mirror               | sync  | sync                      |
|strict-sync-mirror        | sync  | strict_sync               |
|automated-failover        | sync  | automated_failover        |
|automated-failover-duplex | sync  | automated_failover_duplex |
|                          |                                   |"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SnapmirrorPolicy", "SnapmirrorPolicySchema"]
__pdoc__ = {
    "SnapmirrorPolicySchema.resource": False,
    "SnapmirrorPolicySchema.opts": False,
}


class SnapmirrorPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapmirror_policy."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment associated with the policy."""

    copy_all_source_snapshots = marshmallow_fields.Boolean(
        data_key="copy_all_source_snapshots",
        allow_none=True,
    )
    r""" Specifies that all the source snapshots (including the one created by SnapMirror before the transfer begins) should be copied to the destination on a transfer. "Retention" properties cannot be specified along with this property. This is applicable only to async policies. Property can only be set to 'true'.

Example: true"""

    copy_latest_source_snapshot = marshmallow_fields.Boolean(
        data_key="copy_latest_source_snapshot",
        allow_none=True,
    )
    r""" Specifies that the latest source snapshot (created by SnapMirror before the transfer begins) should be copied to the destination on a transfer. "Retention" properties cannot be specified along with this property. This is applicable only to async policies. Property can only be set to 'true'.

Example: true"""

    create_snapshot_on_source = marshmallow_fields.Boolean(
        data_key="create_snapshot_on_source",
        allow_none=True,
    )
    r""" Specifies whether a new snapshot should be created on the source at the beginning of an update or resync operation. This is applicable only to async policies. Property can only be set to 'false'.

Example: false"""

    identity_preservation = marshmallow_fields.Str(
        data_key="identity_preservation",
        validate=enum_validation(['full', 'exclude_network_config', 'exclude_network_and_protocol_config']),
        allow_none=True,
    )
    r""" Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with "async" policy type.

Valid choices:

* full
* exclude_network_config
* exclude_network_and_protocol_config"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the policy.

Example: Asynchronous"""

    network_compression_enabled = marshmallow_fields.Boolean(
        data_key="network_compression_enabled",
        allow_none=True,
    )
    r""" Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type "async"."""

    retention = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snapmirror_policy_rule.SnapmirrorPolicyRuleSchema", unknown=EXCLUDE, allow_none=True), data_key="retention", allow_none=True)
    r""" Rules for snapshot retention."""

    rpo = Size(
        data_key="rpo",
        allow_none=True,
    )
    r""" Specifies the duration of time for which a change to be propagated to a mirror should be delayed, in seconds. This is an intentional propagation delay between mirrors and is configurable down to zero, which means an immediate propagation. This is supported for policies of type 'continuous'."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for policies owned by an SVM, otherwise set to "cluster".

Valid choices:

* svm
* cluster"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snapmirror_policy."""

    sync_common_snapshot_schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="sync_common_snapshot_schedule", unknown=EXCLUDE, allow_none=True)
    r""" The sync_common_snapshot_schedule field of the snapmirror_policy."""

    sync_type = marshmallow_fields.Str(
        data_key="sync_type",
        validate=enum_validation(['sync', 'strict_sync', 'automated_failover', 'automated_failover_duplex']),
        allow_none=True,
    )
    r""" The sync_type field of the snapmirror_policy.

Valid choices:

* sync
* strict_sync
* automated_failover
* automated_failover_duplex"""

    throttle = Size(
        data_key="throttle",
        allow_none=True,
    )
    r""" Throttle in KB/s. Default to unlimited."""

    transfer_schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="transfer_schedule", unknown=EXCLUDE, allow_none=True)
    r""" The transfer_schedule field of the snapmirror_policy."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['async', 'sync', 'continuous']),
        allow_none=True,
    )
    r""" The type field of the snapmirror_policy.

Valid choices:

* async
* sync
* continuous"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the SnapMirror policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SnapmirrorPolicy

    gettable_fields = [
        "links",
        "comment",
        "copy_all_source_snapshots",
        "copy_latest_source_snapshot",
        "create_snapshot_on_source",
        "identity_preservation",
        "name",
        "network_compression_enabled",
        "retention",
        "rpo",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "sync_common_snapshot_schedule.links",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "sync_type",
        "throttle",
        "transfer_schedule.links",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
        "type",
        "uuid",
    ]
    """links,comment,copy_all_source_snapshots,copy_latest_source_snapshot,create_snapshot_on_source,identity_preservation,name,network_compression_enabled,retention,rpo,scope,svm.links,svm.name,svm.uuid,sync_common_snapshot_schedule.links,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,sync_type,throttle,transfer_schedule.links,transfer_schedule.name,transfer_schedule.uuid,type,uuid,"""

    patchable_fields = [
        "comment",
        "identity_preservation",
        "network_compression_enabled",
        "retention",
        "rpo",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "throttle",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
    ]
    """comment,identity_preservation,network_compression_enabled,retention,rpo,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,throttle,transfer_schedule.name,transfer_schedule.uuid,"""

    postable_fields = [
        "comment",
        "copy_all_source_snapshots",
        "copy_latest_source_snapshot",
        "create_snapshot_on_source",
        "identity_preservation",
        "name",
        "network_compression_enabled",
        "retention",
        "rpo",
        "svm.name",
        "svm.uuid",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "sync_type",
        "throttle",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
        "type",
    ]
    """comment,copy_all_source_snapshots,copy_latest_source_snapshot,create_snapshot_on_source,identity_preservation,name,network_compression_enabled,retention,rpo,svm.name,svm.uuid,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,sync_type,throttle,transfer_schedule.name,transfer_schedule.uuid,type,"""

class SnapmirrorPolicy(Resource):
    r""" SnapMirror policy information. SnapMirror policy can either be of type "async", "sync" or "continuous".<br>The policy type "async" can be associated with a SnapMirror relationship that has either a FlexVol volume, FlexGroup volume or SVM as the endpoint.<br>The policy type "sync" along with "sync_type" as "sync" or "strict_sync" can be associated with a SnapMirror relationship that has a FlexVol volume as the endpoint. The policy type "sync" can have a "sync_type" of either "sync", "strict_sync", "automated_failover" or "automated_failover_duplex". If the "sync_type" is "sync", a write success is returned to the client after writing the data to the source endpoint and before writing the data to the destination endpoint. If the "sync_type" is "strict_sync", a write success is returned to the client after writing the data to both source and destination endpoints.<br>If the "sync_type" is "automated_failover", the policy can be associated with a SnapMirror active sync relationship that has a consistency group as the endpoint and provides asymmetric active active access to the two storage copies. If the "sync_type" is "automated_failover_duplex", the policy can be associated with a SnapMirror active sync relationship that has a consistency group as the endpoint and provides symmetric active active access to the two storage copies. Use the "sync" policy with "sync_type" as "automated_failover" or "automated_failover_duplex" to establish SnapMirror active sync relationships for business continuity use cases. SnapMirror relationships with policy types as "sync" and "sync_type" as "automated_failover" or "automated_failover_duplex" can be monitored by the Mediator, if configured. If the source Consistency Group endpoint is not reachable, the Mediator might trigger a failover to the destination consistency group endpoint.<br>A policy type of "continuous" can be associated with SnapMirror relationships that have either ONTAP S3 buckets or non-ONTAP object stores as endpoints. This type of policy is used for FabricLink owned targets. """

    _schema = SnapmirrorPolicySchema
    _path = "/api/snapmirror/policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves SnapMirror policies of type "async" and "sync".
### Related ONTAP commands
* `snapmirror policy show`
### Example
The following example shows how to retrieve a collection of SnapMirror policies.
<br/>
```
GET "/api/snapmirror/policies"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SnapmirrorPolicy resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent SnapmirrorPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnapmirrorPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SnapMirror policy.
### Important notes
* The properties "retention.label" and "retention.count" are mandatory if "retention" is provided in the input. The provided "retention.label" is the final list and it replaces the existing values.
* The value of the "identity_preservation" property cannot be changed if the SnapMirror relationships associated with the policy have different identity_preservation configurations.
* If the SnapMirror policy "identity_preservation" value matches the "identity_preservation" value of the associated SnapMirror relationships, then the "identity_preservation" value can be changed from a higher "identity_preservation" threshold value to a lower "identity_preservation" threshold value but not vice-versa. For example, the threshold value of the "identity_preservation" property can be changed from "full" to "exclude_network_config", but cannot be increased from "exclude_network_and_protocol_config" to "exclude_network_config" to "full". The threshold value of the "identity_preservation" cannot be changed to "exclude_network_and_protocol_config" for IDP SVMDR.<br/>
* The policy properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" cannot be modified.
* No "retention" properties can be modified if the "copy_all_source_snapshots" or "copy_latest_source_snapshot" property is present in the policy.
* Replacing or deleting all retention rules of a policy that has the "create_snapshot_on_source" property set to false in a single API call is not supported.
* Modifying the property "retention.label" for all retention rules of a policy that has the "create_snapshot_on_source" property set to false in a single API call is not supported.
* To remove a transfer_schedule on a SnapMirror policy set the "transfer_schedule" to null (no-quotes) during SnapMirror policy PATCH.

### Related ONTAP commands
* `snapmirror policy modify`
### Example
  Updating the "retention" property to add rules to a policy without any rules.
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "newlabel", "count": 2}, {"label": "weekly", "count": 2, "creation_schedule": {"name": "weekly"}}, {"label": "daily", "count": 14}]}'
   ```
   <br/>
  Updating the "retention" property to add rules to a policy with existing rules {"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 5}]
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 5}, {"label": "newlabel", "count": 3}, {"label": "weekly", "count": 1}]}'
   ```
   <br/>
  Updating the "retention" property to remove a rule (oldLabel1) and add new rule to a policy with existing rules {"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 3}]
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel2", "count": 3}, {"label": "newlabel", "count": 2}]}'
   ```
   <br/>
  Updating "transfer_schedule", "throttle", and "identity_preservation" properties
   <br/>
   ```
   PATCH "/api/snapmirror/policies/8aef950b-3bef-11e9-80ac-0050568ea591" '{"transfer_schedule.name" : "weekly", "throttle" : "100", "identity_preservation":"exclude_network_and_protocol_config"}'
   ```
   <br/>
   Removing the SnapMirror transfer_schedule for a SnapMirror policy. Transfer_schedule can be specified as UUID or name or both with the value set to null (no-quotes).
   <br/>
   ```
   PATCH "/api/snapmirror/policies/98bb2608-fc60-11e8-aa13-005056a707ff/" '{"transfer_schedule":{"uuid":null, "name":null}}'
   ```
   <br/>
  
  Updating the "retention" property to have retention.preserve and retention.warn for existing rule.
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel1", "count": 3, "preserve": true, "warn": 2}]}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnapmirrorPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnapmirrorPolicy"], NetAppResponse]:
        r"""Creates a SnapMirror policy. The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.</br>
It takes the following values:
- `full` - indicates that the source SVM configuration is replicated to the destination SVM endpoint.
- `exclude_network_config` - indicates that the source SVM configuration other than network configuration is replicated to the destination SVM endpoint.
- `exclude_network_and_protocol_config` - indicates that the source SVM configuration is not replicated to the destination SVM endpoint.<br/>
### Important notes
- The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.
- The properties "identity_preservation" and "transfer_schedule" are not applicable for "sync" type policies.
- The properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" are mutually exclusive.
- The properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" are not applicable for "sync" type policies.
- No "retention" properties can be specified if "copy_all_source_snapshots" or 'copy_latest_source_snapshot' is specified.
- The properties "retention.creation_schedule" and "retention.prefix" are not applicable for "sync" type policies.
- The property "retention.creation_schedule" is not applicable for "async" policies with "create_snapshot_on_source" set to "false".
- The property "sync_common_snapshot_schedule" is not applicable for an "async" type policy.
- The property "retention.count" specifies the maximum number of snapshots that are retained on the SnapMirror destination volume.
- When the property "retention.label" is specified, the snapshots that have a SnapMirror label matching this property is transferred to the SnapMirror destination.
- When the property "retention.creation_schedule" is specified, snapshots are directly created on the SnapMirror destination. The snapshots created have the same content as the latest snapshot already present on the SnapMirror destination.
- The property "transfer_schedule" cannot be set to null (no-quotes) during SnapMirror policy POST.
- The properties "retention.label" and "retention.count" must be specified for "async" policies with "create_snapshot_on_source" set to "false".
- The property "retention.warn" is not supported for a policy when the "retention.preserve" property is false.
- The property "retention.warn" value must be less than the property "retention.count" value for a rule in a policy.
  
### Required properties
* `name` - Name of the new SnapMirror policy.
### Recommended optional properties
* `svm.name` or `svm.uuid` - Name or UUID of the SVM that owns the SnapMirror policy.
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - _async_
* `sync_type` - _sync_ (when `type` is _sync_)
* `network_compression_enabled` - _false_
* `throttle` - _0_
* `identity_preservation` - `_exclude_network_and_protocol_config_`

### Related ONTAP commands
* `snapmirror policy create`
### Examples
  Creating a SnapMirror policy of type "sync"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "sync"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" with two sets of retention values, one with a creation_schedule
   <br/>
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "2", "creation_schedule": {"name": "weekly"}}, {"label":"daily", "count":"7"}]}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async"
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which replicates all snapshots
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async", "copy_all_source_snapshots": "true"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which replicates latest snapshot
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy2", "svm":{"name" : "vs1"}, "type": "async", "copy_latest_source_snapshot": "true"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which does not create snapshots on source
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async", "create_snapshot_on_source": "false", "retention": [{"label": "daily", "count": 7}]}'
   ```
   <br/>
  Creating a SnapMirror policy of type "sync" with sync_type as "automated_failover"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "automated_failover" }'
   ```
   <br/>
  Creating a SnapMirror policy of type "sync" with sync_type as "automated_failover_duplex"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy_afd", "svm.name": "VS0", "type": "sync", "sync_type": "automated_failover_duplex" }'
   ```
   <br/>
  
  
  
  Creating a SnapMirror policy of type "async" with two sets of retention values and retention periods
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "2", "period": "P7D"}, {"label":"daily", "count":"7", "period": "PT3H"}]}'
   ```
   <br/>
   Creating a SnapMirror policy of type "async" with retention value as "infinite"
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "5", "period": "infinite"}]}'
   ```
   <br/>
   Creating a SnapMirror policy of type "async" with properties retention preserve as true and retention warn as 3.
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "5", "preserve": true, "warn": 3}]}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SnapmirrorPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a SnapMirror policy.
### Related ONTAP commands
* `snapmirror policy delete`
### Example
<br/>
```
DELETE "/api/snapmirror/policies/510c15d4-f9e6-11e8-bdb5-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves SnapMirror policies of type "async" and "sync".
### Related ONTAP commands
* `snapmirror policy show`
### Example
The following example shows how to retrieve a collection of SnapMirror policies.
<br/>
```
GET "/api/snapmirror/policies"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific SnapMirror policy.
### Example
<br/>
```
GET "/api/snapmirror/policies/567aaac0-f863-11e8-a666-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a SnapMirror policy. The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.</br>
It takes the following values:
- `full` - indicates that the source SVM configuration is replicated to the destination SVM endpoint.
- `exclude_network_config` - indicates that the source SVM configuration other than network configuration is replicated to the destination SVM endpoint.
- `exclude_network_and_protocol_config` - indicates that the source SVM configuration is not replicated to the destination SVM endpoint.<br/>
### Important notes
- The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.
- The properties "identity_preservation" and "transfer_schedule" are not applicable for "sync" type policies.
- The properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" are mutually exclusive.
- The properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" are not applicable for "sync" type policies.
- No "retention" properties can be specified if "copy_all_source_snapshots" or 'copy_latest_source_snapshot' is specified.
- The properties "retention.creation_schedule" and "retention.prefix" are not applicable for "sync" type policies.
- The property "retention.creation_schedule" is not applicable for "async" policies with "create_snapshot_on_source" set to "false".
- The property "sync_common_snapshot_schedule" is not applicable for an "async" type policy.
- The property "retention.count" specifies the maximum number of snapshots that are retained on the SnapMirror destination volume.
- When the property "retention.label" is specified, the snapshots that have a SnapMirror label matching this property is transferred to the SnapMirror destination.
- When the property "retention.creation_schedule" is specified, snapshots are directly created on the SnapMirror destination. The snapshots created have the same content as the latest snapshot already present on the SnapMirror destination.
- The property "transfer_schedule" cannot be set to null (no-quotes) during SnapMirror policy POST.
- The properties "retention.label" and "retention.count" must be specified for "async" policies with "create_snapshot_on_source" set to "false".
- The property "retention.warn" is not supported for a policy when the "retention.preserve" property is false.
- The property "retention.warn" value must be less than the property "retention.count" value for a rule in a policy.
  
### Required properties
* `name` - Name of the new SnapMirror policy.
### Recommended optional properties
* `svm.name` or `svm.uuid` - Name or UUID of the SVM that owns the SnapMirror policy.
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - _async_
* `sync_type` - _sync_ (when `type` is _sync_)
* `network_compression_enabled` - _false_
* `throttle` - _0_
* `identity_preservation` - `_exclude_network_and_protocol_config_`

### Related ONTAP commands
* `snapmirror policy create`
### Examples
  Creating a SnapMirror policy of type "sync"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "sync"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" with two sets of retention values, one with a creation_schedule
   <br/>
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "2", "creation_schedule": {"name": "weekly"}}, {"label":"daily", "count":"7"}]}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async"
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which replicates all snapshots
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async", "copy_all_source_snapshots": "true"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which replicates latest snapshot
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy2", "svm":{"name" : "vs1"}, "type": "async", "copy_latest_source_snapshot": "true"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" which does not create snapshots on source
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async", "create_snapshot_on_source": "false", "retention": [{"label": "daily", "count": 7}]}'
   ```
   <br/>
  Creating a SnapMirror policy of type "sync" with sync_type as "automated_failover"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "automated_failover" }'
   ```
   <br/>
  Creating a SnapMirror policy of type "sync" with sync_type as "automated_failover_duplex"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy_afd", "svm.name": "VS0", "type": "sync", "sync_type": "automated_failover_duplex" }'
   ```
   <br/>
  
  
  
  Creating a SnapMirror policy of type "async" with two sets of retention values and retention periods
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "2", "period": "P7D"}, {"label":"daily", "count":"7", "period": "PT3H"}]}'
   ```
   <br/>
   Creating a SnapMirror policy of type "async" with retention value as "infinite"
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "5", "period": "infinite"}]}'
   ```
   <br/>
   Creating a SnapMirror policy of type "async" with properties retention preserve as true and retention warn as 3.
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": [{"label": "weekly", "count": "5", "preserve": true, "warn": 3}]}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SnapMirror policy.
### Important notes
* The properties "retention.label" and "retention.count" are mandatory if "retention" is provided in the input. The provided "retention.label" is the final list and it replaces the existing values.
* The value of the "identity_preservation" property cannot be changed if the SnapMirror relationships associated with the policy have different identity_preservation configurations.
* If the SnapMirror policy "identity_preservation" value matches the "identity_preservation" value of the associated SnapMirror relationships, then the "identity_preservation" value can be changed from a higher "identity_preservation" threshold value to a lower "identity_preservation" threshold value but not vice-versa. For example, the threshold value of the "identity_preservation" property can be changed from "full" to "exclude_network_config", but cannot be increased from "exclude_network_and_protocol_config" to "exclude_network_config" to "full". The threshold value of the "identity_preservation" cannot be changed to "exclude_network_and_protocol_config" for IDP SVMDR.<br/>
* The policy properties "copy_all_source_snapshots", "copy_latest_source_snapshot", and "create_snapshot_on_source" cannot be modified.
* No "retention" properties can be modified if the "copy_all_source_snapshots" or "copy_latest_source_snapshot" property is present in the policy.
* Replacing or deleting all retention rules of a policy that has the "create_snapshot_on_source" property set to false in a single API call is not supported.
* Modifying the property "retention.label" for all retention rules of a policy that has the "create_snapshot_on_source" property set to false in a single API call is not supported.
* To remove a transfer_schedule on a SnapMirror policy set the "transfer_schedule" to null (no-quotes) during SnapMirror policy PATCH.

### Related ONTAP commands
* `snapmirror policy modify`
### Example
  Updating the "retention" property to add rules to a policy without any rules.
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "newlabel", "count": 2}, {"label": "weekly", "count": 2, "creation_schedule": {"name": "weekly"}}, {"label": "daily", "count": 14}]}'
   ```
   <br/>
  Updating the "retention" property to add rules to a policy with existing rules {"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 5}]
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 5}, {"label": "newlabel", "count": 3}, {"label": "weekly", "count": 1}]}'
   ```
   <br/>
  Updating the "retention" property to remove a rule (oldLabel1) and add new rule to a policy with existing rules {"retention": [{"label": "oldLabel1", "count": 2}, {"label": "oldLabel2", "count": 3}]
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel2", "count": 3}, {"label": "newlabel", "count": 2}]}'
   ```
   <br/>
  Updating "transfer_schedule", "throttle", and "identity_preservation" properties
   <br/>
   ```
   PATCH "/api/snapmirror/policies/8aef950b-3bef-11e9-80ac-0050568ea591" '{"transfer_schedule.name" : "weekly", "throttle" : "100", "identity_preservation":"exclude_network_and_protocol_config"}'
   ```
   <br/>
   Removing the SnapMirror transfer_schedule for a SnapMirror policy. Transfer_schedule can be specified as UUID or name or both with the value set to null (no-quotes).
   <br/>
   ```
   PATCH "/api/snapmirror/policies/98bb2608-fc60-11e8-aa13-005056a707ff/" '{"transfer_schedule":{"uuid":null, "name":null}}'
   ```
   <br/>
  
  Updating the "retention" property to have retention.preserve and retention.warn for existing rule.
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention": [{"label": "oldLabel1", "count": 3, "preserve": true, "warn": 2}]}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a SnapMirror policy.
### Related ONTAP commands
* `snapmirror policy delete`
### Example
<br/>
```
DELETE "/api/snapmirror/policies/510c15d4-f9e6-11e8-bdb5-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


