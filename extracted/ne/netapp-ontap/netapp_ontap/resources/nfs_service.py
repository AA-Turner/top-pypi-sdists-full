r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

### Retrieving an NFS configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NfsService.get_collection()))

```

### Retrieving the mount permissions for a specified volume for a given IP address.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            NfsService.get_collection(
                fields="*",
                return_timeout=15,
                **{
                    "protocol_access_rules.volume": "testvol12",
                    "protocol_access_rules.client_ip": "1.2.3.4",
                    "protocol_access_rules.auth_type": "sys",
                    "svm.uuid": "525928e9-9f84-11eb-a89f-005056bb70a8",
                }
            )
        )
    )

```

### Creating an NFS configuration for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NfsService()
    resource.svm = {"uuid": "1cd8a442-86d1-11e0-ae1c-123478563412"}
    resource.protocol = {"v4_id_domain": "nfs-nsr-w01.rtp.netapp.com"}
    resource.vstorage_enabled = True
    resource.post(hydrate=True)
    print(resource)

```

### Updating an  NFS configuration for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NfsService(**{"svm.uuid": "4a415601-548c-11e8-a21d-0050568bcbc9"})
    resource.protocol = {"v4_id_domain": "nfs-nsr-w01.rtp.netapp.com"}
    resource.vstorage_enabled = False
    resource.patch()

```

### Deleting an NFS configuration for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NfsService(**{"svm.uuid": "4a415601-548c-11e8-a21d-0050568bcbc9"})
    resource.delete()

```

## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes."""

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


__all__ = ["NfsService", "NfsServiceSchema"]
__pdoc__ = {
    "NfsServiceSchema.resource": False,
    "NfsServiceSchema.opts": False,
}


class NfsServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nfs_service."""

    access_cache_config = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_access_cache_config.NfsServiceAccessCacheConfigSchema", data_key="access_cache_config", unknown=EXCLUDE, allow_none=True)
    r""" The access_cache_config field of the nfs_service."""

    auth_sys_extended_groups_enabled = marshmallow_fields.Boolean(
        data_key="auth_sys_extended_groups_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not extended groups support over AUTH_SYS is enabled."""

    credential_cache = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_credential_cache.NfsServiceCredentialCacheSchema", data_key="credential_cache", unknown=EXCLUDE, allow_none=True)
    r""" The credential_cache field of the nfs_service."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies if the NFS service is administratively enabled."""

    exports = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_exports.NfsServiceExportsSchema", data_key="exports", unknown=EXCLUDE, allow_none=True)
    r""" The exports field of the nfs_service."""

    extended_groups_limit = Size(
        data_key="extended_groups_limit",
        validate=integer_validation(minimum=32, maximum=1024),
        allow_none=True,
    )
    r""" Specifies the maximum auxiliary groups supported over AUTH_SYS and RPCSEC_GSS.

Example: 32"""

    file_session_io_grouping_count = Size(
        data_key="file_session_io_grouping_count",
        validate=integer_validation(minimum=1000, maximum=120000),
        allow_none=True,
    )
    r""" Number of I/O operations on a file to be grouped and considered as one session for event generation applications, such as FPolicy.

Example: 5000"""

    file_session_io_grouping_duration = Size(
        data_key="file_session_io_grouping_duration",
        validate=integer_validation(minimum=60, maximum=3600),
        allow_none=True,
    )
    r""" The duration for which I/O operations on a file will be grouped and considered as one session for event generation applications, such as FPolicy.

Example: 120"""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_svm_nfs_metric.PerformanceSvmNfsMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Historical performance numbers, such as IOPS latency and throughput, for SVM-NFS protocol."""

    protocol = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol.NfsServiceProtocolSchema", data_key="protocol", unknown=EXCLUDE, allow_none=True)
    r""" The protocol field of the nfs_service."""

    protocol_access_rules = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol_access_rules.NfsServiceProtocolAccessRulesSchema", data_key="protocol_access_rules", unknown=EXCLUDE, allow_none=True)
    r""" The protocol_access_rules field of the nfs_service."""

    qtree = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_qtree.NfsServiceQtreeSchema", data_key="qtree", unknown=EXCLUDE, allow_none=True)
    r""" The qtree field of the nfs_service."""

    root = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_root.NfsServiceRootSchema", data_key="root", unknown=EXCLUDE, allow_none=True)
    r""" The root field of the nfs_service."""

    rquota_enabled = marshmallow_fields.Boolean(
        data_key="rquota_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not the remote quota feature is enabled."""

    security = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_security.NfsServiceSecuritySchema", data_key="security", unknown=EXCLUDE, allow_none=True)
    r""" The security field of the nfs_service."""

    showmount_enabled = marshmallow_fields.Boolean(
        data_key="showmount_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not the showmount feature is enabled."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['online', 'offline']),
        allow_none=True,
    )
    r""" Specifies the state of the NFS service on the SVM. The following values are supported:

          * online - NFS server is ready to accept client requests.
          * offline - NFS server is not ready to accept client requests.


Valid choices:

* online
* offline"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_svm_nfs_statistics.PerformanceSvmNfsStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" Realtime performance numbers, such as IOPS latency and throughput, for SVM-NFS protocol."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nfs_service."""

    transport = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_transport.NfsServiceTransportSchema", data_key="transport", unknown=EXCLUDE, allow_none=True)
    r""" The transport field of the nfs_service."""

    vstorage_enabled = marshmallow_fields.Boolean(
        data_key="vstorage_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not the VMware vstorage feature is enabled."""

    windows = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_windows.NfsServiceWindowsSchema", data_key="windows", unknown=EXCLUDE, allow_none=True)
    r""" The windows field of the nfs_service."""

    @property
    def resource(self):
        return NfsService

    gettable_fields = [
        "links",
        "access_cache_config",
        "auth_sys_extended_groups_enabled",
        "credential_cache",
        "enabled",
        "exports",
        "extended_groups_limit",
        "file_session_io_grouping_count",
        "file_session_io_grouping_duration",
        "metric",
        "protocol",
        "protocol_access_rules",
        "qtree",
        "root",
        "rquota_enabled",
        "security",
        "showmount_enabled",
        "state",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "transport",
        "vstorage_enabled",
        "windows",
    ]
    """links,access_cache_config,auth_sys_extended_groups_enabled,credential_cache,enabled,exports,extended_groups_limit,file_session_io_grouping_count,file_session_io_grouping_duration,metric,protocol,protocol_access_rules,qtree,root,rquota_enabled,security,showmount_enabled,state,statistics,svm.links,svm.name,svm.uuid,transport,vstorage_enabled,windows,"""

    patchable_fields = [
        "access_cache_config",
        "auth_sys_extended_groups_enabled",
        "credential_cache",
        "enabled",
        "exports",
        "extended_groups_limit",
        "file_session_io_grouping_count",
        "file_session_io_grouping_duration",
        "protocol",
        "qtree",
        "root",
        "rquota_enabled",
        "security",
        "showmount_enabled",
        "svm.name",
        "svm.uuid",
        "transport",
        "vstorage_enabled",
        "windows",
    ]
    """access_cache_config,auth_sys_extended_groups_enabled,credential_cache,enabled,exports,extended_groups_limit,file_session_io_grouping_count,file_session_io_grouping_duration,protocol,qtree,root,rquota_enabled,security,showmount_enabled,svm.name,svm.uuid,transport,vstorage_enabled,windows,"""

    postable_fields = [
        "access_cache_config",
        "auth_sys_extended_groups_enabled",
        "credential_cache",
        "enabled",
        "exports",
        "extended_groups_limit",
        "file_session_io_grouping_count",
        "file_session_io_grouping_duration",
        "protocol",
        "qtree",
        "root",
        "rquota_enabled",
        "security",
        "showmount_enabled",
        "svm.name",
        "svm.uuid",
        "transport",
        "vstorage_enabled",
        "windows",
    ]
    """access_cache_config,auth_sys_extended_groups_enabled,credential_cache,enabled,exports,extended_groups_limit,file_session_io_grouping_count,file_session_io_grouping_duration,protocol,qtree,root,rquota_enabled,security,showmount_enabled,svm.name,svm.uuid,transport,vstorage_enabled,windows,"""

class NfsService(Resource):
    """Allows interaction with NfsService objects on the host"""

    _schema = NfsServiceSchema
    _path = "/api/protocols/nfs/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the NFS configuration of SVMs.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Advanced properties
* `security.rpcsec_context_idle`
* `security.ntfs_unix_security`
* `security.chown_mode`
* `security.nt_acl_display_permission`
* `protocol.v3_features.ejukebox_enabled`
* `protocol.v3_features.connection_drop`
* `protocol.v3_features.fsid_change`
* `protocol.v3_features.mount_daemon_port`
* `protocol.v3_features.network_lock_manager_port`
* `protocol.v3_features.network_status_monitor_port`
* `protocol.v3_features.rquota_daemon_port`
* `protocol.v3_features.hide_snapshot_enabled`
* `protocol.v41_features.implementation_domain`
* `protocol.v41_features.implementation_name`
* `protocol.v40_features.acl_max_aces`
* `windows.map_unknown_uid_to_default_user`
* `exports.netgroup_trust_any_nsswitch_no_match`
* `credential_cache.negative_ttl`
* `transport.tcp_max_transfer_size`
* `root.*`
* `protocol.v41_features.trunking_enabled`
* `protocol.v42_features.seclabel_enabled`
* `protocol.v42_features.sparsefile_ops_enabled`
* `protocol.v42_features.xattrs_enabled`
* `protocol.v40_features.referrals_enabled`
* `protocol.v41_features.referrals_enabled`
* `protocol.v4_lease_seconds`
* `protocol.v4_session_slots`
* `protocol.v4_session_slot_reply_cache_size`
* `protocol.v4_fsid_change`
### Diagnostic properties
* `credential_cache.transient_error_ttl`
* `access_cache_config.ttl_failure`
### Related ONTAP commands
* `vserver nfs show`
* `vserver nfs status`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
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
        """Returns a count of all NfsService resources that match the provided query"""
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
        """Returns a list of RawResources that represent NfsService resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NfsService"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the NFS configuration of an SVM.
### Related ONTAP commands
* `vserver nfs modify`
* `vserver nfs on`
* `vserver nfs off`
* `vserver nfs start`
* `vserver nfs stop`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["NfsService"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NfsService"], NetAppResponse]:
        r"""Creates an NFS configuration for an SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM for which to create the NFS configuration.
### Default property values
If not specified in POST, the following default property values are assigned:
* `enabled` - _true_
* `state` - online
* `transport.udp_enabled` - _true_
* `transport.tcp_enabled` - _true_
* `transport.rdma_enabled` - _true_
* `protocol.v3_enabled` - _true_
* `protocol.v3_64bit_identifiers_enabled` - _false_
* `protocol.v4_id_domain` - defaultv4iddomain.com
* `protocol.v4_64bit_identifiers_enabled` - _true_
* `protocol.v4_enabled` - _false_
* `protocol.v41_enabled` - _false_
* `protocol.v40_features.acl_enabled` - _false_
* `protocol.v40_features.read_delegation_enabled` - _false_
* `protocol.v40_features.write_delegation_enabled` - _false_
* `protocol.v41_features.acl_enabled` - _false_
* `protocol.v41_features.read_delegation_enabled` - _false_
* `protocol.v41_features.write_delegation_enabled` - _false_
* `protocol.v41_features.pnfs_enabled` - _false_
* `vstorage_enabled` - _false_
* `rquota_enabled` - _false_
* `showmount_enabled` - _true_
* `auth_sys_extended_groups_enabled` - _false_
* `extended_groups_limit` - _32_
* `qtree.export_enabled` - _false_
* `qtree.validate_export` - _true_
* `access_cache_config.ttl_positive` - _60_
* `access_cache_config.ttl_negative` - _30_
* `access_cache_config.ttl_failure` - _1_
* `access_cache_config.harvest_timeout` - _3600_
* `access_cache_config.isDnsTTLEnabled` - _false_
* `file_session_io_grouping_count` - _5000_
* `file_session_io_grouping_duration` - _120_
* `security.nt_acl_display_permission` - _false_
* `exports.netgroup_trust_any_nsswitch_no_match` - _false_
* `exports.name_service_lookup_protocol` - _udp_
* `security.permitted_encryption_types` - [aes-256,aes-128,des3,des]
* `security.rpcsec_context_idle` - _0_
* `security.chown_mode` - _use_export_policy_
* `security.ntfs_unix_security` - _use_export_policy_
* `windows.v3_ms_dos_client_enabled` - _false_
* `windows.default_user` - ""
* `windows.map_unknown_uid_to_default_user` - _true_
* `credential_cache.positive_ttl` - _86400000_
* `credential_cache.negative_ttl` - _7200000_
* `credential_cache.transient_error_ttl` - _30000_
* `protocol.v40_features.acl_preserve` - _true_
* `protocol.v41_features.implementation_domain` - 'netapp.com'
* `protocol.v40_features.acl_max_aces` - _400_
* `protocol.v3_features.ejukebox_enabled` - _true_
* `protocol.v3_features.connection_drop` - _true_
* `protocol.v3_features.fsid_change` - _true_
* `protocol.v3_features.mount_daemon_port` - _635_
* `protocol.v3_features.network_lock_manager_port` - _4045_
* `protocol.v3_features.network_status_monitor_port` - _4046_
* `protocol.v3_features.rquota_daemon_port` - _4046_
* `protocol.v3_features.mount_root_only` - _true_
* `transport.tcp_max_transfer_size` - _65536_
* `root.ignore_nt_acl` - _false_
* `root.skip_write_permission_check` - _false_
* `protocol.v40_features.referrals_enabled` - _false_
* `protocol.v41_features.referrals_enabled` - _false_
* `protocol.v4_fsid_change` - _true_
* `protocol.v4_lease_seconds` - 30
* `protocol.v4_grace_seconds` - 45
* `protocol.v4_session_slots` - 180
* `protocol.v4_session_slot_reply_cache_size` - 640
### Related ONTAP commands
* `vserver nfs create`
* `export-policy access-cache config show`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
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
        records: Iterable["NfsService"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the NFS configuration of an SVM.
### Related ONTAP commands
* `vserver nfs delete`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the NFS configuration of SVMs.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Advanced properties
* `security.rpcsec_context_idle`
* `security.ntfs_unix_security`
* `security.chown_mode`
* `security.nt_acl_display_permission`
* `protocol.v3_features.ejukebox_enabled`
* `protocol.v3_features.connection_drop`
* `protocol.v3_features.fsid_change`
* `protocol.v3_features.mount_daemon_port`
* `protocol.v3_features.network_lock_manager_port`
* `protocol.v3_features.network_status_monitor_port`
* `protocol.v3_features.rquota_daemon_port`
* `protocol.v3_features.hide_snapshot_enabled`
* `protocol.v41_features.implementation_domain`
* `protocol.v41_features.implementation_name`
* `protocol.v40_features.acl_max_aces`
* `windows.map_unknown_uid_to_default_user`
* `exports.netgroup_trust_any_nsswitch_no_match`
* `credential_cache.negative_ttl`
* `transport.tcp_max_transfer_size`
* `root.*`
* `protocol.v41_features.trunking_enabled`
* `protocol.v42_features.seclabel_enabled`
* `protocol.v42_features.sparsefile_ops_enabled`
* `protocol.v42_features.xattrs_enabled`
* `protocol.v40_features.referrals_enabled`
* `protocol.v41_features.referrals_enabled`
* `protocol.v4_lease_seconds`
* `protocol.v4_session_slots`
* `protocol.v4_session_slot_reply_cache_size`
* `protocol.v4_fsid_change`
### Diagnostic properties
* `credential_cache.transient_error_ttl`
* `access_cache_config.ttl_failure`
### Related ONTAP commands
* `vserver nfs show`
* `vserver nfs status`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the NFS configuration of an SVM.
### Related ONTAP commands
* `vserver nfs show`
* `vserver nfs status`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
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
        r"""Creates an NFS configuration for an SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM for which to create the NFS configuration.
### Default property values
If not specified in POST, the following default property values are assigned:
* `enabled` - _true_
* `state` - online
* `transport.udp_enabled` - _true_
* `transport.tcp_enabled` - _true_
* `transport.rdma_enabled` - _true_
* `protocol.v3_enabled` - _true_
* `protocol.v3_64bit_identifiers_enabled` - _false_
* `protocol.v4_id_domain` - defaultv4iddomain.com
* `protocol.v4_64bit_identifiers_enabled` - _true_
* `protocol.v4_enabled` - _false_
* `protocol.v41_enabled` - _false_
* `protocol.v40_features.acl_enabled` - _false_
* `protocol.v40_features.read_delegation_enabled` - _false_
* `protocol.v40_features.write_delegation_enabled` - _false_
* `protocol.v41_features.acl_enabled` - _false_
* `protocol.v41_features.read_delegation_enabled` - _false_
* `protocol.v41_features.write_delegation_enabled` - _false_
* `protocol.v41_features.pnfs_enabled` - _false_
* `vstorage_enabled` - _false_
* `rquota_enabled` - _false_
* `showmount_enabled` - _true_
* `auth_sys_extended_groups_enabled` - _false_
* `extended_groups_limit` - _32_
* `qtree.export_enabled` - _false_
* `qtree.validate_export` - _true_
* `access_cache_config.ttl_positive` - _60_
* `access_cache_config.ttl_negative` - _30_
* `access_cache_config.ttl_failure` - _1_
* `access_cache_config.harvest_timeout` - _3600_
* `access_cache_config.isDnsTTLEnabled` - _false_
* `file_session_io_grouping_count` - _5000_
* `file_session_io_grouping_duration` - _120_
* `security.nt_acl_display_permission` - _false_
* `exports.netgroup_trust_any_nsswitch_no_match` - _false_
* `exports.name_service_lookup_protocol` - _udp_
* `security.permitted_encryption_types` - [aes-256,aes-128,des3,des]
* `security.rpcsec_context_idle` - _0_
* `security.chown_mode` - _use_export_policy_
* `security.ntfs_unix_security` - _use_export_policy_
* `windows.v3_ms_dos_client_enabled` - _false_
* `windows.default_user` - ""
* `windows.map_unknown_uid_to_default_user` - _true_
* `credential_cache.positive_ttl` - _86400000_
* `credential_cache.negative_ttl` - _7200000_
* `credential_cache.transient_error_ttl` - _30000_
* `protocol.v40_features.acl_preserve` - _true_
* `protocol.v41_features.implementation_domain` - 'netapp.com'
* `protocol.v40_features.acl_max_aces` - _400_
* `protocol.v3_features.ejukebox_enabled` - _true_
* `protocol.v3_features.connection_drop` - _true_
* `protocol.v3_features.fsid_change` - _true_
* `protocol.v3_features.mount_daemon_port` - _635_
* `protocol.v3_features.network_lock_manager_port` - _4045_
* `protocol.v3_features.network_status_monitor_port` - _4046_
* `protocol.v3_features.rquota_daemon_port` - _4046_
* `protocol.v3_features.mount_root_only` - _true_
* `transport.tcp_max_transfer_size` - _65536_
* `root.ignore_nt_acl` - _false_
* `root.skip_write_permission_check` - _false_
* `protocol.v40_features.referrals_enabled` - _false_
* `protocol.v41_features.referrals_enabled` - _false_
* `protocol.v4_fsid_change` - _true_
* `protocol.v4_lease_seconds` - 30
* `protocol.v4_grace_seconds` - 45
* `protocol.v4_session_slots` - 180
* `protocol.v4_session_slot_reply_cache_size` - 640
### Related ONTAP commands
* `vserver nfs create`
* `export-policy access-cache config show`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
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
        r"""Updates the NFS configuration of an SVM.
### Related ONTAP commands
* `vserver nfs modify`
* `vserver nfs on`
* `vserver nfs off`
* `vserver nfs start`
* `vserver nfs stop`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
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
        r"""Deletes the NFS configuration of an SVM.
### Related ONTAP commands
* `vserver nfs delete`
### Learn more
* [`DOC /protocols/nfs/services`](#docs-NAS-protocols_nfs_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


