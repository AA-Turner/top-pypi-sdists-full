r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Managing SVMs
<br/>Cluster administrators can manage any SVM bound to the cluster. In addition, SVMs can also be managed by their SVM administrators. The SVM administrator manages the SVM resources, such as volumes, protocols and services, depending on the capabilities assigned by the cluster administrator. SVM administrators cannot create, modify, or delete SVMs. The cluster administrator manages SVM create, modify, or delete operations.<br/>
<br/>While configuring CIFS, you must also configure IP interfaces and DNS. No other protocol configuration is allowed when configuring NVMe. NFS, FCP, CIFS, iSCSI, and S3 protocols can be configured together.<br/>
SVM administrators might have all or some of the following administration capabilities:
1. Data access protocol configuration
   Configures data access protocols, such as NFS, CIFS, iSCSI, S3, and Fibre Channel (FC) protocols (Fibre Channel over Ethernet included).
2. Services configuration
   Configures services such as LDAP, NIS, and DNS.
3. Monitoring SVM
   Monitors jobs, network connections, network interfaces, and SVM health.
4. Updating the TLS certificate for this SVM."""

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


__all__ = ["Svm", "SvmSchema"]
__pdoc__ = {
    "SvmSchema.resource": False,
    "SvmSchema.opts": False,
}


class SvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Svm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the svm."""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_aggregates.SvmAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" List of allowed aggregates for SVM volumes. An administrator is allowed to create volumes on these aggregates."""

    aggregates_delegated = marshmallow_fields.Boolean(
        data_key="aggregates_delegated",
        allow_none=True,
    )
    r""" This property is true when the administrator has delegated the aggregates for the SVM volumes."""

    anti_ransomware = marshmallow_fields.Nested("netapp_ontap.models.arw_vserver.ArwVserverSchema", data_key="anti_ransomware", unknown=EXCLUDE, allow_none=True)
    r""" Anti-ransomware related information for the SVM."""

    anti_ransomware_auto_switch_duration_without_new_file_extension = Size(
        data_key="anti_ransomware_auto_switch_duration_without_new_file_extension",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that no new file-extensions are observed in the volume in recent time. This parameter optionally specifies the recent time duration (in days) to be considered during which no new file-extension should be observed in a given volume to automatically switch the anti-ransomware state from ‘learning” to “enabled”."""

    anti_ransomware_auto_switch_from_learning_to_enabled = marshmallow_fields.Boolean(
        data_key="anti_ransomware_auto_switch_from_learning_to_enabled",
        allow_none=True,
    )
    r""" This property specifies whether anti-ransomware state of the volumes in this SVM are automatically switched by the system from “learning” (dry-run) to “enabled” (active) state after sufficient learning."""

    anti_ransomware_auto_switch_minimum_file_count = Size(
        data_key="anti_ransomware_auto_switch_minimum_file_count",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should have a minimum file count in “learning” state. This parameter optionally specifies the minimum number of newly created files in “learning” state in a given volume to automatically switch the anti-ransomware state from “learning” to “enabled”."""

    anti_ransomware_auto_switch_minimum_file_extension = Size(
        data_key="anti_ransomware_auto_switch_minimum_file_extension",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should have minimum number of file extensions in “learning” state. This parameter optionally specifies the minimum number of new file extensions in “learning” state in a given volume to automatically switch the anti-ransomware state from “learning” to “enabled”."""

    anti_ransomware_auto_switch_minimum_incoming_data = marshmallow_fields.Str(
        data_key="anti_ransomware_auto_switch_minimum_incoming_data",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should have sufficient data ingested to do the learning. This parameter optionally specifies the minimum amount of data (in GB) to be written to a given volume during the learning period to automatically switch the anti-ransomware state from “learning” to “enabled”. The amount of data considered as ingested also includes the data that is deleted or overwritten after ingestion."""

    anti_ransomware_auto_switch_minimum_learning_period = Size(
        data_key="anti_ransomware_auto_switch_minimum_learning_period",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should be in “learning” state for sufficient time period. This parameter optionally specifies the minimum number of days a given volume should be in “learning” state to automatically switch the anti-ransomware state from “learning” to “enabled”."""

    anti_ransomware_default_volume_state = marshmallow_fields.Str(
        data_key="anti_ransomware_default_volume_state",
        validate=enum_validation(['disabled', 'dry_run']),
        allow_none=True,
    )
    r""" Specifies the default Anti-ransomware state of the volumes in the SVM. Default "anti_ransomware_default_volume_state" property is disabled for POST operation. If this value is "disabled", Anti-ransomware protection is disabled by default on the new volumes that are created in the SVM. If this value is "dry_run", Anti-ransomware protection is in learning mode by default on the new volumes that are created in the SVM.  When the Anti-ransomware license is not present, this property is ignored and volumes will be created with the "disabled" state.

Valid choices:

* disabled
* dry_run"""

    anti_ransomware_incoming_write_threshold = marshmallow_fields.Str(
        data_key="anti_ransomware_incoming_write_threshold",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should have sufficient data ingested to do the learning. This parameter optionally specifies the minimum amount of data (in GB) to be written to a given volume during the learning period to automatically switch the anti-ransomware state from “learning” to “enabled”. The amount of data considered as ingested also includes the data that is deleted or overwritten after ingestion. This field is no longer supported."""

    anti_ransomware_incoming_write_threshold_percent = marshmallow_fields.Str(
        data_key="anti_ransomware_incoming_write_threshold_percent",
        allow_none=True,
    )
    r""" One of the many conditions to be satisfied to automatically switch the anti-ransomware state of the volumes in this SVM from “learning” (dry-run) to “enabled” is that the volume should have sufficient data ingested to do the learning. This parameter optionally specifies the minimum amount of data (in percentage) to be written to a given volume during the learning period to automatically switch the anti-ransomware state from “learning” to “enabled”. The amount of data considered as ingested also includes the data that is deleted or overwritten after ingestion."""

    auto_enable_activity_tracking = marshmallow_fields.Boolean(
        data_key="auto_enable_activity_tracking",
        allow_none=True,
    )
    r""" Specifies whether volume activity tracking is automatically enabled on volumes that are created in the SVM."""

    auto_enable_analytics = marshmallow_fields.Boolean(
        data_key="auto_enable_analytics",
        allow_none=True,
    )
    r""" Specifies whether file system analytics is automatically enabled on volumes that are created in the SVM."""

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the svm."""

    cifs = marshmallow_fields.Nested("netapp_ontap.models.svm_cifs_service.SvmCifsServiceSchema", data_key="cifs", unknown=EXCLUDE, allow_none=True)
    r""" The cifs field of the svm."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=255),
        allow_none=True,
    )
    r""" Comment"""

    dns = marshmallow_fields.Nested("netapp_ontap.models.svm_dns.SvmDnsSchema", data_key="dns", unknown=EXCLUDE, allow_none=True)
    r""" The dns field of the svm."""

    fc_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fc_interface_svm.FcInterfaceSvmSchema", unknown=EXCLUDE, allow_none=True), data_key="fc_interfaces", allow_none=True)
    r""" FC Interface for the SVM"""

    fcp = marshmallow_fields.Nested("netapp_ontap.models.svm_fcp.SvmFcpSchema", data_key="fcp", unknown=EXCLUDE, allow_none=True)
    r""" ### Platform Specifics

* **Unified ONTAP**: Available for GET, POST and PATCH.
* **ASA r2**: Available for GET. All SVMs are provisioned with the FCP service configured."""

    ip_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_interface_svm.IpInterfaceSvmSchema", unknown=EXCLUDE, allow_none=True), data_key="ip_interfaces", allow_none=True)
    r""" IP interfaces for the SVM"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the svm."""

    is_space_enforcement_logical = marshmallow_fields.Boolean(
        data_key="is_space_enforcement_logical",
        allow_none=True,
    )
    r""" Indicates whether logical space enforcement for the SVM is enabled."""

    is_space_reporting_logical = marshmallow_fields.Boolean(
        data_key="is_space_reporting_logical",
        allow_none=True,
    )
    r""" Indicates whether logical space reporting for the SVM is enabled."""

    iscsi = marshmallow_fields.Nested("netapp_ontap.models.svm_iscsi.SvmIscsiSchema", data_key="iscsi", unknown=EXCLUDE, allow_none=True)
    r""" ### Platform Specifics

* **Unified ONTAP**: Available for GET, POST and PATCH.
* **ASA r2**: Available for GET. All SVMs are provisioned with the iSCSI service configured."""

    language = marshmallow_fields.Str(
        data_key="language",
        validate=enum_validation(['c', 'da', 'de', 'en', 'en_us', 'es', 'fi', 'fr', 'he', 'it', 'ja', 'ja_jp.pck', 'ko', 'no', 'nl', 'pt', 'sv', 'zh', 'zh.gbk', 'zh_tw', 'zh_tw.big5', 'c.utf_8', 'ar', 'ar.utf_8', 'cs', 'cs.utf_8', 'da.utf_8', 'de.utf_8', 'en.utf_8', 'en_us.utf_8', 'es.utf_8', 'fi.utf_8', 'fr.utf_8', 'he.utf_8', 'hr', 'hr.utf_8', 'hu', 'hu.utf_8', 'it.utf_8', 'ja.utf_8', 'ja_v1', 'ja_v1.utf_8', 'ja_jp.pck.utf_8', 'ja_jp.932', 'ja_jp.932.utf_8', 'ja_jp.pck_v2', 'ja_jp.pck_v2.utf_8', 'ko.utf_8', 'no.utf_8', 'nl.utf_8', 'pl', 'pl.utf_8', 'pt.utf_8', 'ro', 'ro.utf_8', 'ru', 'ru.utf_8', 'sk', 'sk.utf_8', 'sl', 'sl.utf_8', 'sv.utf_8', 'tr', 'tr.utf_8', 'zh.utf_8', 'zh.gbk.utf_8', 'zh_tw.utf_8', 'zh_tw.big5.utf_8', 'utf8mb4']),
        allow_none=True,
    )
    r""" Default volume language code. UTF-8 encoded languages are valid in POST or PATCH. Non UTF-8 language encodings are for backward compatibility and are not valid input for POST and PATCH requests.

Valid choices:

* c
* da
* de
* en
* en_us
* es
* fi
* fr
* he
* it
* ja
* ja_jp.pck
* ko
* no
* nl
* pt
* sv
* zh
* zh.gbk
* zh_tw
* zh_tw.big5
* c.utf_8
* ar
* ar.utf_8
* cs
* cs.utf_8
* da.utf_8
* de.utf_8
* en.utf_8
* en_us.utf_8
* es.utf_8
* fi.utf_8
* fr.utf_8
* he.utf_8
* hr
* hr.utf_8
* hu
* hu.utf_8
* it.utf_8
* ja.utf_8
* ja_v1
* ja_v1.utf_8
* ja_jp.pck.utf_8
* ja_jp.932
* ja_jp.932.utf_8
* ja_jp.pck_v2
* ja_jp.pck_v2.utf_8
* ko.utf_8
* no.utf_8
* nl.utf_8
* pl
* pl.utf_8
* pt.utf_8
* ro
* ro.utf_8
* ru
* ru.utf_8
* sk
* sk.utf_8
* sl
* sl.utf_8
* sv.utf_8
* tr
* tr.utf_8
* zh.utf_8
* zh.gbk.utf_8
* zh_tw.utf_8
* zh_tw.big5.utf_8
* utf8mb4"""

    ldap = marshmallow_fields.Nested("netapp_ontap.models.svm_ldap.SvmLdapSchema", data_key="ldap", unknown=EXCLUDE, allow_none=True)
    r""" The ldap field of the svm."""

    max_volumes = marshmallow_fields.Str(
        data_key="max_volumes",
        allow_none=True,
    )
    r""" This property is used by cluster administrator to specify the limit on maximum number of volumes allowed in the SVM. The value can be either the string "unlimited" or a number."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the SVM.


Example: svm1"""

    ndmp = marshmallow_fields.Nested("netapp_ontap.models.svm_ndmp.SvmNdmpSchema", data_key="ndmp", unknown=EXCLUDE, allow_none=True)
    r""" The ndmp field of the svm."""

    nfs = marshmallow_fields.Nested("netapp_ontap.models.svm_nfs.SvmNfsSchema", data_key="nfs", unknown=EXCLUDE, allow_none=True)
    r""" The nfs field of the svm."""

    nis = marshmallow_fields.Nested("netapp_ontap.models.svm_nis.SvmNisSchema", data_key="nis", unknown=EXCLUDE, allow_none=True)
    r""" The nis field of the svm."""

    nsswitch = marshmallow_fields.Nested("netapp_ontap.models.svm_nsswitch.SvmNsswitchSchema", data_key="nsswitch", unknown=EXCLUDE, allow_none=True)
    r""" Name service switch configuration"""

    number_of_volumes_in_recovery_queue = Size(
        data_key="number_of_volumes_in_recovery_queue",
        allow_none=True,
    )
    r""" Number of volumes in the recovery queue."""

    nvme = marshmallow_fields.Nested("netapp_ontap.models.svm_nvme.SvmNvmeSchema", data_key="nvme", unknown=EXCLUDE, allow_none=True)
    r""" ### Platform Specifics

* **Unified ONTAP**: Available for GET, POST and PATCH.
* **ASA r2**: Available for GET. All SVMs are provisioned with the NVMe service configured."""

    qos_adaptive_policy_group_template = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_adaptive_policy_group_template", unknown=EXCLUDE, allow_none=True)
    r""" The qos_adaptive_policy_group_template field of the svm."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The qos_policy field of the svm."""

    qos_policy_group_template = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_policy_group_template", unknown=EXCLUDE, allow_none=True)
    r""" The qos_policy_group_template field of the svm."""

    routes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.network_route_for_svm.NetworkRouteForSvmSchema", unknown=EXCLUDE, allow_none=True), data_key="routes", allow_none=True)
    r""" Optional array of routes for the SVM"""

    s3 = marshmallow_fields.Nested("netapp_ontap.models.svm_s3_service.SvmS3ServiceSchema", data_key="s3", unknown=EXCLUDE, allow_none=True)
    r""" The s3 field of the svm."""

    snapmirror = marshmallow_fields.Nested("netapp_ontap.models.svm_snapmirror.SvmSnapmirrorSchema", data_key="snapmirror", unknown=EXCLUDE, allow_none=True)
    r""" Specifies attributes for SVM DR protection."""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" The snapshot_policy field of the svm."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['starting', 'running', 'stopping', 'stopped', 'deleting', 'initializing']),
        allow_none=True,
    )
    r""" SVM State

Valid choices:

* starting
* running
* stopping
* stopped
* deleting
* initializing"""

    storage = marshmallow_fields.Nested("netapp_ontap.models.svm_storage.SvmStorageSchema", data_key="storage", unknown=EXCLUDE, allow_none=True)
    r""" The storage field of the svm."""

    subtype = marshmallow_fields.Str(
        data_key="subtype",
        validate=enum_validation(['default', 'dp_destination', 'sync_source', 'sync_destination']),
        allow_none=True,
    )
    r""" SVM subtype. The SVM subtype sync_destination is created automatically when an SVM of subtype sync_source is created on the source MetroCluster cluster. A POST request with sync_destination as SVM subtype is invalid.

Valid choices:

* default
* dp_destination
* sync_source
* sync_destination"""

    total_volume_size_in_recovery_queue = Size(
        data_key="total_volume_size_in_recovery_queue",
        allow_none=True,
    )
    r""" Sum of the sizes of the volumes in the recovery queue."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the SVM.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7"""

    @property
    def resource(self):
        return Svm

    gettable_fields = [
        "links",
        "aggregates",
        "aggregates_delegated",
        "anti_ransomware",
        "anti_ransomware_auto_switch_duration_without_new_file_extension",
        "anti_ransomware_auto_switch_from_learning_to_enabled",
        "anti_ransomware_auto_switch_minimum_file_count",
        "anti_ransomware_auto_switch_minimum_file_extension",
        "anti_ransomware_auto_switch_minimum_incoming_data",
        "anti_ransomware_auto_switch_minimum_learning_period",
        "anti_ransomware_default_volume_state",
        "anti_ransomware_incoming_write_threshold",
        "anti_ransomware_incoming_write_threshold_percent",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "cifs.links",
        "cifs.ad_domain",
        "cifs.allowed",
        "cifs.auth_style",
        "cifs.domain_workgroup",
        "cifs.enabled",
        "cifs.name",
        "cifs.workgroup",
        "comment",
        "dns",
        "fc_interfaces",
        "fcp",
        "ip_interfaces",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "is_space_enforcement_logical",
        "is_space_reporting_logical",
        "iscsi",
        "language",
        "ldap.ad_domain",
        "ldap.base_dn",
        "ldap.bind_dn",
        "ldap.enabled",
        "ldap.restrict_discovery_to_site",
        "ldap.servers",
        "max_volumes",
        "name",
        "ndmp",
        "nfs",
        "nis",
        "nsswitch",
        "number_of_volumes_in_recovery_queue",
        "nvme",
        "qos_adaptive_policy_group_template.links",
        "qos_adaptive_policy_group_template.max_throughput_iops",
        "qos_adaptive_policy_group_template.max_throughput_mbps",
        "qos_adaptive_policy_group_template.min_throughput_iops",
        "qos_adaptive_policy_group_template.min_throughput_mbps",
        "qos_adaptive_policy_group_template.name",
        "qos_adaptive_policy_group_template.uuid",
        "qos_policy.links",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "qos_policy_group_template.links",
        "qos_policy_group_template.max_throughput_iops",
        "qos_policy_group_template.max_throughput_mbps",
        "qos_policy_group_template.min_throughput_iops",
        "qos_policy_group_template.min_throughput_mbps",
        "qos_policy_group_template.name",
        "qos_policy_group_template.uuid",
        "s3.links",
        "s3.allowed",
        "s3.certificate",
        "s3.default_unix_user",
        "s3.default_win_user",
        "s3.enabled",
        "s3.is_http_enabled",
        "s3.is_https_enabled",
        "s3.name",
        "s3.port",
        "s3.secure_port",
        "snapmirror",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "state",
        "storage",
        "subtype",
        "total_volume_size_in_recovery_queue",
        "uuid",
    ]
    """links,aggregates,aggregates_delegated,anti_ransomware,anti_ransomware_auto_switch_duration_without_new_file_extension,anti_ransomware_auto_switch_from_learning_to_enabled,anti_ransomware_auto_switch_minimum_file_count,anti_ransomware_auto_switch_minimum_file_extension,anti_ransomware_auto_switch_minimum_incoming_data,anti_ransomware_auto_switch_minimum_learning_period,anti_ransomware_default_volume_state,anti_ransomware_incoming_write_threshold,anti_ransomware_incoming_write_threshold_percent,auto_enable_activity_tracking,auto_enable_analytics,certificate.links,certificate.name,certificate.uuid,cifs.links,cifs.ad_domain,cifs.allowed,cifs.auth_style,cifs.domain_workgroup,cifs.enabled,cifs.name,cifs.workgroup,comment,dns,fc_interfaces,fcp,ip_interfaces,ipspace.links,ipspace.name,ipspace.uuid,is_space_enforcement_logical,is_space_reporting_logical,iscsi,language,ldap.ad_domain,ldap.base_dn,ldap.bind_dn,ldap.enabled,ldap.restrict_discovery_to_site,ldap.servers,max_volumes,name,ndmp,nfs,nis,nsswitch,number_of_volumes_in_recovery_queue,nvme,qos_adaptive_policy_group_template.links,qos_adaptive_policy_group_template.max_throughput_iops,qos_adaptive_policy_group_template.max_throughput_mbps,qos_adaptive_policy_group_template.min_throughput_iops,qos_adaptive_policy_group_template.min_throughput_mbps,qos_adaptive_policy_group_template.name,qos_adaptive_policy_group_template.uuid,qos_policy.links,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,qos_policy_group_template.links,qos_policy_group_template.max_throughput_iops,qos_policy_group_template.max_throughput_mbps,qos_policy_group_template.min_throughput_iops,qos_policy_group_template.min_throughput_mbps,qos_policy_group_template.name,qos_policy_group_template.uuid,s3.links,s3.allowed,s3.certificate,s3.default_unix_user,s3.default_win_user,s3.enabled,s3.is_http_enabled,s3.is_https_enabled,s3.name,s3.port,s3.secure_port,snapmirror,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,state,storage,subtype,total_volume_size_in_recovery_queue,uuid,"""

    patchable_fields = [
        "aggregates",
        "anti_ransomware",
        "anti_ransomware_auto_switch_duration_without_new_file_extension",
        "anti_ransomware_auto_switch_from_learning_to_enabled",
        "anti_ransomware_auto_switch_minimum_file_count",
        "anti_ransomware_auto_switch_minimum_file_extension",
        "anti_ransomware_auto_switch_minimum_incoming_data",
        "anti_ransomware_auto_switch_minimum_learning_period",
        "anti_ransomware_default_volume_state",
        "anti_ransomware_incoming_write_threshold",
        "anti_ransomware_incoming_write_threshold_percent",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "certificate.name",
        "certificate.uuid",
        "cifs.allowed",
        "cifs.workgroup",
        "comment",
        "fcp",
        "ip_interfaces",
        "is_space_enforcement_logical",
        "is_space_reporting_logical",
        "iscsi",
        "language",
        "max_volumes",
        "name",
        "ndmp",
        "nfs",
        "nsswitch",
        "nvme",
        "qos_adaptive_policy_group_template.max_throughput_iops",
        "qos_adaptive_policy_group_template.max_throughput_mbps",
        "qos_adaptive_policy_group_template.min_throughput_iops",
        "qos_adaptive_policy_group_template.min_throughput_mbps",
        "qos_adaptive_policy_group_template.name",
        "qos_adaptive_policy_group_template.uuid",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "qos_policy_group_template.max_throughput_iops",
        "qos_policy_group_template.max_throughput_mbps",
        "qos_policy_group_template.min_throughput_iops",
        "qos_policy_group_template.min_throughput_mbps",
        "qos_policy_group_template.name",
        "qos_policy_group_template.uuid",
        "snapmirror",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "state",
        "storage",
    ]
    """aggregates,anti_ransomware,anti_ransomware_auto_switch_duration_without_new_file_extension,anti_ransomware_auto_switch_from_learning_to_enabled,anti_ransomware_auto_switch_minimum_file_count,anti_ransomware_auto_switch_minimum_file_extension,anti_ransomware_auto_switch_minimum_incoming_data,anti_ransomware_auto_switch_minimum_learning_period,anti_ransomware_default_volume_state,anti_ransomware_incoming_write_threshold,anti_ransomware_incoming_write_threshold_percent,auto_enable_activity_tracking,auto_enable_analytics,certificate.name,certificate.uuid,cifs.allowed,cifs.workgroup,comment,fcp,ip_interfaces,is_space_enforcement_logical,is_space_reporting_logical,iscsi,language,max_volumes,name,ndmp,nfs,nsswitch,nvme,qos_adaptive_policy_group_template.max_throughput_iops,qos_adaptive_policy_group_template.max_throughput_mbps,qos_adaptive_policy_group_template.min_throughput_iops,qos_adaptive_policy_group_template.min_throughput_mbps,qos_adaptive_policy_group_template.name,qos_adaptive_policy_group_template.uuid,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,qos_policy_group_template.max_throughput_iops,qos_policy_group_template.max_throughput_mbps,qos_policy_group_template.min_throughput_iops,qos_policy_group_template.min_throughput_mbps,qos_policy_group_template.name,qos_policy_group_template.uuid,snapmirror,snapshot_policy.name,snapshot_policy.uuid,state,storage,"""

    postable_fields = [
        "aggregates",
        "anti_ransomware",
        "anti_ransomware_auto_switch_duration_without_new_file_extension",
        "anti_ransomware_auto_switch_from_learning_to_enabled",
        "anti_ransomware_auto_switch_minimum_file_count",
        "anti_ransomware_auto_switch_minimum_file_extension",
        "anti_ransomware_auto_switch_minimum_incoming_data",
        "anti_ransomware_auto_switch_minimum_learning_period",
        "anti_ransomware_default_volume_state",
        "anti_ransomware_incoming_write_threshold",
        "anti_ransomware_incoming_write_threshold_percent",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "cifs.ad_domain",
        "cifs.allowed",
        "cifs.enabled",
        "cifs.name",
        "cifs.workgroup",
        "comment",
        "dns",
        "fc_interfaces",
        "fcp",
        "ip_interfaces",
        "ipspace.name",
        "ipspace.uuid",
        "is_space_enforcement_logical",
        "is_space_reporting_logical",
        "iscsi",
        "language",
        "ldap.ad_domain",
        "ldap.base_dn",
        "ldap.bind_dn",
        "ldap.enabled",
        "ldap.restrict_discovery_to_site",
        "ldap.servers",
        "max_volumes",
        "name",
        "ndmp",
        "nfs",
        "nis",
        "nsswitch",
        "nvme",
        "qos_adaptive_policy_group_template.max_throughput_iops",
        "qos_adaptive_policy_group_template.max_throughput_mbps",
        "qos_adaptive_policy_group_template.min_throughput_iops",
        "qos_adaptive_policy_group_template.min_throughput_mbps",
        "qos_adaptive_policy_group_template.name",
        "qos_adaptive_policy_group_template.uuid",
        "qos_policy_group_template.max_throughput_iops",
        "qos_policy_group_template.max_throughput_mbps",
        "qos_policy_group_template.min_throughput_iops",
        "qos_policy_group_template.min_throughput_mbps",
        "qos_policy_group_template.name",
        "qos_policy_group_template.uuid",
        "routes",
        "s3.allowed",
        "s3.certificate",
        "s3.default_unix_user",
        "s3.default_win_user",
        "s3.enabled",
        "s3.is_http_enabled",
        "s3.is_https_enabled",
        "s3.name",
        "s3.port",
        "s3.secure_port",
        "snapmirror",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage",
        "subtype",
    ]
    """aggregates,anti_ransomware,anti_ransomware_auto_switch_duration_without_new_file_extension,anti_ransomware_auto_switch_from_learning_to_enabled,anti_ransomware_auto_switch_minimum_file_count,anti_ransomware_auto_switch_minimum_file_extension,anti_ransomware_auto_switch_minimum_incoming_data,anti_ransomware_auto_switch_minimum_learning_period,anti_ransomware_default_volume_state,anti_ransomware_incoming_write_threshold,anti_ransomware_incoming_write_threshold_percent,auto_enable_activity_tracking,auto_enable_analytics,cifs.ad_domain,cifs.allowed,cifs.enabled,cifs.name,cifs.workgroup,comment,dns,fc_interfaces,fcp,ip_interfaces,ipspace.name,ipspace.uuid,is_space_enforcement_logical,is_space_reporting_logical,iscsi,language,ldap.ad_domain,ldap.base_dn,ldap.bind_dn,ldap.enabled,ldap.restrict_discovery_to_site,ldap.servers,max_volumes,name,ndmp,nfs,nis,nsswitch,nvme,qos_adaptive_policy_group_template.max_throughput_iops,qos_adaptive_policy_group_template.max_throughput_mbps,qos_adaptive_policy_group_template.min_throughput_iops,qos_adaptive_policy_group_template.min_throughput_mbps,qos_adaptive_policy_group_template.name,qos_adaptive_policy_group_template.uuid,qos_policy_group_template.max_throughput_iops,qos_policy_group_template.max_throughput_mbps,qos_policy_group_template.min_throughput_iops,qos_policy_group_template.min_throughput_mbps,qos_policy_group_template.name,qos_policy_group_template.uuid,routes,s3.allowed,s3.certificate,s3.default_unix_user,s3.default_win_user,s3.enabled,s3.is_http_enabled,s3.is_https_enabled,s3.name,s3.port,s3.secure_port,snapmirror,snapshot_policy.name,snapshot_policy.uuid,storage,subtype,"""

class Svm(Resource):
    """Allows interaction with Svm objects on the host"""

    _schema = SvmSchema
    _path = "/api/svm/svms"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of SVMs and individual SVM properties. This includes protocol configurations such as CIFS, NFS and S3, export policies, name service configurations, and network services.
### Important notes
* The SVM object includes a large set of fields and can be expensive to retrieve. Use this API to list the collection of SVMs, and to retrieve only the full details of individual SVMs as needed.
* It is not recommended to create or delete more than five SVMs in parallel.
* REST APIs only expose a data SVM as an SVM.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `snapmirror.*`
### Related ONTAP commands
* `vserver show`
### Examples
1. Retrieves a list of SVMs in the cluster sorted by name
    <br/>
    ```
    GET "/api/svm/svms?order_by=name"
    ```
    <br/>
2. Retrieves a list of SVMs in the cluster that have the NFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?nfs.enabled=true"
    ```
    <br/>
3. Retrieves a list of SVMs in the cluster that have the CIFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?cifs.enabled=true"
    ```
    <br/>
4. Retrieves a list of SVMs in the cluster that have the S3 protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?s3.enabled=true"
    ```
    <br/>
5 Retrieves a list of SVMs in the cluster that have the FCP protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?fcp.allowed=true"
    ```
    <br/>
6. Retrieves a list of SVMs in the cluster that have the CIFS protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?cifs.allowed=true"
    ```
    <br/>
7. Retrieves a list of SVMs in the cluster where the NDMP protocol is specified as allowed
    <br/>
    ```
    GET "/api/svm/svms?ndmp.allowed=true"
    ```
    <br/>
8.  Retrieves a list of SVMs in the cluster that have the s3 protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?s3.allowed=true"
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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
        """Returns a count of all Svm resources that match the provided query"""
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
        """Returns a list of RawResources that represent Svm resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Svm"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates one or more of the following properties of an individual SVM: SVM name, SVM default volume language code, SVM comment, and SVM state.
### Related ONTAP commands
* `vserver modify`
* `vserver rename`
* `vserver start`
* `vserver stop`
* `security ssl modify`
* `vserver add-protocols`
* `vserver remove-protocols`
### Examples
1.  Stops an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"stopped", "comment":"This SVM is stopped."}'
    ```
    <br/>
2.  Starts an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"running", "comment":"This SVM is running."}'
    ```
    <br/>
3.  Updates the "language" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"language":"en.UTF-8"}'
    ```
    <br/>
4.  Updates the "name" field for an SVM or renames the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"name":"svm_new"}'
    ```
    <br/>
5.  Updates the aggregates for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"aggregates":["{"name":aggr1"},{"name":"aggr2"},{"name":"aggr3"}]}'
    ```
    <br/>
6.  Updates the snapshot policy for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"snapshot_policy":{"name":"custom1"}}'
    ```
    <br/>
7.  Updates the TLS certificate for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"certificate":{"uuid":"1cd8a442-86d1-11e0-ae1c-123478563412"}}'
    ```
    <br/>
8.  Updates the QoS policy for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_policy_group":{"name":"qpolicy1"}}'
    ```
    <br/>
9.  Allows NFS protocol which was previously disallowed for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"nfs":{"allowed":"true"}}'
    ```
    <br/>
10. Updates the max volume limit for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"max_volumes":"200"}'
    ```
    <br/>
11. Updates whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"auto_enable_analytics":"true"}'
    ```
    <br/>
12. Updates whether volume activity tracking is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"auto_enable_activity_tracking":"true"}'
    ```
    <br/>
13. Updates the QoS adaptive policy group template for the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_adaptive_policy_group_template":{"name":"aqpolicy1"}}'
    ```
    <br/>
14. Updates the maximum storage permitted on a single SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"storage":{"limit":"40GB"}}'
    ```
    <br/>
15. Updates the percentage of storage capacity at which an alert message is sent.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"storage":{"limit":"400MB", "limit_threshold_alert":"98"}}'
    ```
    <br/>
16. Updates the QoS policy group template for the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_policy_group_template":{"name":"policy1"}}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Svm"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Svm"], NetAppResponse]:
        r"""Creates and provisions an SVM. If no IPspace is provided, then the SVM is created on the `Default` IPspace.
* The number of parallel SVMs that can be created must not be greater than five.
* If a sixth SVM POST request is issued, the following error message is generated: "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again."
### Required properties
* `name` - Name of the SVM to be created.
### Recommended optional properties
* `ipspace.name` or `ipspace.uuid` - IPspace of the SVM
* `is_space_reporting_logical` - Logical Space Reporting parameter of the SVM
* `is_space_enforcement_logical` - Logical Space Enforcement parameter of the SVM
* `ip_interfaces` - If provided, the following fields are required:
* `ip_interfaces.name` - Name of the interface
* `ip_interfaces.ip.address` - IP address
* `ip_interfaces.ip.netmask` - Netmask length or IP address
* `ip_interfaces.location.broadcast_domain.uuid` or `ip_interfaces.location.broadcast_domain.name` - Broadcast domain name or UUID belonging to the same IPspace of the SVM.
* `ip_interfaces.location.home_port.name` - Home port name
* `ip_interfaces.location.home_port.uuid` - Home port uuid
* `subnet.uuid` or `subnet.name` - Either name or UUID of the subnet to create.
* `routes` - If provided, the following field is required:
  * `routes.gateway` - Gateway IP address
* `cifs` - If provided, interfaces, routes and DNS must be provided. The following fields are also required:
  * `cifs.name` - Name of the CIFS server to be created for the SVM.
  * `cifs.ad_domain.fqdn` - Fully qualified domain name
  * `cifs.ad_domain.user` - Administrator username
  * `cifs.ad_domain.password` - User password
* `ldap` - If provided, the following fields are required:
  * `ldap.servers` or `ldap.ad_domain` - LDAP server list or Active Directory domain
  * `ldap.bind_dn` - Bind DN
  * `ldap.base_dn` - Base DN
* `nis` - If provided, the following fields are required:
  * `nis.servers` - NIS servers
  * `nis.domain` - NIS domain
* `dns` - If provided, the following fields are required:
  * `dns.servers` - Name servers
  * `dns.domains` - Domains
* `fc_interfaces` - If provided, the following fields are required:
  * `fc_interfaces.name` - Fibre Channel interface name
  * `fc_interfaces.data_protocol` - Fibre Channel interface data protocol
  * `fc_interfaces.location.port.uuid` or `fc_interfaces.location.port.name` and `fc_interfaces.location.port.node.name` - Either port UUID or port name and node name together must be provided.
* `s3` - If provided, the following field should also be specified:
  * `s3.name` - Name of the S3 server. If `s3.name' is not specified while `s3.enabled` is set to 'true', the S3 server will be created with the default name '<svm.name>_S3Server'.
  * `s3.port` - S3 server listener port.
  * `s3.secure_port` - S3 server listener port for HTTPS.
  * `s3.is_http_enabled` - S3 server connections over HTTP.
  * `s3.is_https_enabled` - S3 server connections over HTTPS.
  * `s3.certificate.name` - S3 server certificate name. This is required if the S3 server runs over HTTPS.
  * `s3.certificate.uuid` - S3 server certificate UUID. This is required if the S3 server runs over HTTPS.
* `auto_enable_analytics` - Auto-enable file system analytics on new volumes created in the SVM.
* `auto_enable_activity_tracking` - Auto-enable volume activity-tracking on new volumes created in the SVM.
* `storage.limit` - Maximum storage permitted on a single SVM.
* `storage.limit_threshold_alert` - At what percentage of storage capacity, alert message needs to be sent.
### Default property values
If not specified in POST, the following default property values are assigned:
* `language` - _C.UTF-8_
* `ipspace.name` - _Default_
* `snapshot_policy.name` - _Default_
* `subtype` - _Default_ ( _sync-source_ if MetroCluster configuration )
* `anti_ransomware_default_volume_state` - _disabled_
* `qos_adaptive_policy_group_template` - _extreme_ ( if running ONTAP X and neither qos_policy_group_template nor qos_adaptive_policy_group_template are provided)
### Related ONTAP commands
* `vserver create`
* `vserver add-aggregates`
* `network interface create`
* `network route create`
* `vserver services name-service dns create`
* `vserver nfs create`
* `vserver services name-service ldap client create`
* `vserver cifs create`
* `vserver services name-service nis-domain create`
* `vserver iscsi create`
* `vserver nvme create`
* `vserver fcp create`
* `vserver services name-service ns-switch create`
* `vserver object-store-server create`
* `vserver add-protocols`
* `vserver remove-protocols`
### Examples
1. Creates an SVM with default "snapshot_policy"
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}}'
    ```
    <br/>
2. Creates an SVM and configures NFS, ISCSI and FCP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nfs":{"enabled":"true"}, "fcp":{"enabled":"true"}, "iscsi":{"enabled":"true"}}'
    ```
    <br/>
3. Creates an SVM and configures NVMe
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nvme":{"enabled":"true"}}'
    ```
    <br/>
4. Creates an SVM and configures LDAP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "ldap":{"servers":["10.140.101.1","10.140.101.2"], "ad_domain":"abc.com", "base_dn":"dc=netapp,dc=com", "bind_dn":"dc=netapp,dc=com"}}'
    ```
    <br/>
5. Creates an SVM and configures NIS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "nis":{"enabled":"true", "domain":"def.com","servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
6. Creates an SVM and configures DNS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "dns":{"domains":["abc.com","def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
7. Creates an SVM and configures a LIF
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
8. Creates an SVM and configures a LIF with IPV6 address
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif2", "ip":{"address":"fd22:8b1e:b255:202:2a0:98ff:fe01:7d5b", "netmask":"24"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
9. Creates an SVM and configures CIFS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "cifs":{"name":"CIFDOC", "ad_domain":{"fqdn":"abc.def.com", "organizational_unit":"CN=Computers", "user":"cif_admin", "password":"abc123"}}, "ip_interfaces":[{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}],"routes": [{"destination": {"address": "0.0.0.0", "netmask": "0"}, "gateway": "10.10.10.7"}], "dns":{"domains":["abc.def.com", "def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
10. Creates an SVM with an S3 server enabled and configured
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"svm5", "s3":{"name":"s3-server-1", "enabled":true, "allowed":true, "is_http_enabled": true, "is_https_enabled":false}}'
    ```
    <br/>
11. Creates an SVM and disallows NVMe service for the SVM
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nvme":{"allowed":"false"}}'
    ```
    <br/>
12. Creates an SVM, allows and configures the NFS service for the SVM
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nfs":{"allowed":"true", "enabled":true}}'
    ```
    <br/>
13. Create an SVM and set the max volume limit for the SVM
    <br/>
    ```
    POST "/api/svm/svms/" '{"name":"testVs", "max_volumes":"200"}'
    ```
    <br/>
14. Creates an SVM and disallows the NDMP service for the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ndmp":{"allowed":"false"}}'
    ```
    <br/>
15. Creates an SVM and specifies whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_analytics":true}}'
    ```
    <br/>
16. Creates an SVM and specifies whether volume_activity_tracking is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_activity_tracking":true}}'
    ```
    <br/>
17. Creates an SVM and specifies whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_analytics":true}}'
    ```
    <br/>
18. Creates an SVM and specifies the maximum storage limit for a single SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "storage": {"limit":"4GB"}}'
    ```
    <br/>
19. Creates an SVM and specifies at what percentage of storage capacity an alert message is sent. Default value is 90.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "storage": {"limit":"20GB", "limit_threshold_alert":"95"}}'
    ```
    <br/>
20. Creates an SVM and specifies the QoS policy group template to be assigned to the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "qos_policy_group_template":{"name":"performance-fixed"}}'
    ```
    <br/>
21. Creates an SVM and specifies the QoS adaptive policy group template to be assigned to the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "qos_adaptive_policy_group_template":{"name":"performance"}}'
    ```
    <br/>
22. On ASA r2 platforms, _fcp_, _iscsi_, and _nvme_ services are enabled and allowed by default, and are not necessary in the POST request.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs"}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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
        records: Iterable["Svm"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an SVM. As a prerequisite, SVM objects must be deleted first. SnapMirror relationships must be deleted and data volumes must be offline and deleted.
* The number of parallel SVMs that can be created must not be greater than five.
* If a sixth SVM POST request is issued, the following error message is generated: "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again."
### Related ONTAP commands
* `vserver delete`
### Example
Deleting an individual SVM in the cluster.
  <br/>
  ```
  DELETE "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
  ```
  <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of SVMs and individual SVM properties. This includes protocol configurations such as CIFS, NFS and S3, export policies, name service configurations, and network services.
### Important notes
* The SVM object includes a large set of fields and can be expensive to retrieve. Use this API to list the collection of SVMs, and to retrieve only the full details of individual SVMs as needed.
* It is not recommended to create or delete more than five SVMs in parallel.
* REST APIs only expose a data SVM as an SVM.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `snapmirror.*`
### Related ONTAP commands
* `vserver show`
### Examples
1. Retrieves a list of SVMs in the cluster sorted by name
    <br/>
    ```
    GET "/api/svm/svms?order_by=name"
    ```
    <br/>
2. Retrieves a list of SVMs in the cluster that have the NFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?nfs.enabled=true"
    ```
    <br/>
3. Retrieves a list of SVMs in the cluster that have the CIFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?cifs.enabled=true"
    ```
    <br/>
4. Retrieves a list of SVMs in the cluster that have the S3 protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?s3.enabled=true"
    ```
    <br/>
5 Retrieves a list of SVMs in the cluster that have the FCP protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?fcp.allowed=true"
    ```
    <br/>
6. Retrieves a list of SVMs in the cluster that have the CIFS protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?cifs.allowed=true"
    ```
    <br/>
7. Retrieves a list of SVMs in the cluster where the NDMP protocol is specified as allowed
    <br/>
    ```
    GET "/api/svm/svms?ndmp.allowed=true"
    ```
    <br/>
8.  Retrieves a list of SVMs in the cluster that have the s3 protocol allowed
    <br/>
    ```
    GET "/api/svm/svms?s3.allowed=true"
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the properties for an individual SVM. This includes protocol configurations such as CIFS and NFS, export policies, name service configurations, and network services.
### Important notes
* The SVM object includes a large set of fields and can be expensive to retrieve.
* REST APIs only expose a data SVM as an SVM.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `snapmirror.*`
### Example
    Retrieving an individual SVM in the cluster
    <br/>
    ```
    GET "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
    ```
    <br/>

### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)"""
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
        r"""Creates and provisions an SVM. If no IPspace is provided, then the SVM is created on the `Default` IPspace.
* The number of parallel SVMs that can be created must not be greater than five.
* If a sixth SVM POST request is issued, the following error message is generated: "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again."
### Required properties
* `name` - Name of the SVM to be created.
### Recommended optional properties
* `ipspace.name` or `ipspace.uuid` - IPspace of the SVM
* `is_space_reporting_logical` - Logical Space Reporting parameter of the SVM
* `is_space_enforcement_logical` - Logical Space Enforcement parameter of the SVM
* `ip_interfaces` - If provided, the following fields are required:
* `ip_interfaces.name` - Name of the interface
* `ip_interfaces.ip.address` - IP address
* `ip_interfaces.ip.netmask` - Netmask length or IP address
* `ip_interfaces.location.broadcast_domain.uuid` or `ip_interfaces.location.broadcast_domain.name` - Broadcast domain name or UUID belonging to the same IPspace of the SVM.
* `ip_interfaces.location.home_port.name` - Home port name
* `ip_interfaces.location.home_port.uuid` - Home port uuid
* `subnet.uuid` or `subnet.name` - Either name or UUID of the subnet to create.
* `routes` - If provided, the following field is required:
  * `routes.gateway` - Gateway IP address
* `cifs` - If provided, interfaces, routes and DNS must be provided. The following fields are also required:
  * `cifs.name` - Name of the CIFS server to be created for the SVM.
  * `cifs.ad_domain.fqdn` - Fully qualified domain name
  * `cifs.ad_domain.user` - Administrator username
  * `cifs.ad_domain.password` - User password
* `ldap` - If provided, the following fields are required:
  * `ldap.servers` or `ldap.ad_domain` - LDAP server list or Active Directory domain
  * `ldap.bind_dn` - Bind DN
  * `ldap.base_dn` - Base DN
* `nis` - If provided, the following fields are required:
  * `nis.servers` - NIS servers
  * `nis.domain` - NIS domain
* `dns` - If provided, the following fields are required:
  * `dns.servers` - Name servers
  * `dns.domains` - Domains
* `fc_interfaces` - If provided, the following fields are required:
  * `fc_interfaces.name` - Fibre Channel interface name
  * `fc_interfaces.data_protocol` - Fibre Channel interface data protocol
  * `fc_interfaces.location.port.uuid` or `fc_interfaces.location.port.name` and `fc_interfaces.location.port.node.name` - Either port UUID or port name and node name together must be provided.
* `s3` - If provided, the following field should also be specified:
  * `s3.name` - Name of the S3 server. If `s3.name' is not specified while `s3.enabled` is set to 'true', the S3 server will be created with the default name '<svm.name>_S3Server'.
  * `s3.port` - S3 server listener port.
  * `s3.secure_port` - S3 server listener port for HTTPS.
  * `s3.is_http_enabled` - S3 server connections over HTTP.
  * `s3.is_https_enabled` - S3 server connections over HTTPS.
  * `s3.certificate.name` - S3 server certificate name. This is required if the S3 server runs over HTTPS.
  * `s3.certificate.uuid` - S3 server certificate UUID. This is required if the S3 server runs over HTTPS.
* `auto_enable_analytics` - Auto-enable file system analytics on new volumes created in the SVM.
* `auto_enable_activity_tracking` - Auto-enable volume activity-tracking on new volumes created in the SVM.
* `storage.limit` - Maximum storage permitted on a single SVM.
* `storage.limit_threshold_alert` - At what percentage of storage capacity, alert message needs to be sent.
### Default property values
If not specified in POST, the following default property values are assigned:
* `language` - _C.UTF-8_
* `ipspace.name` - _Default_
* `snapshot_policy.name` - _Default_
* `subtype` - _Default_ ( _sync-source_ if MetroCluster configuration )
* `anti_ransomware_default_volume_state` - _disabled_
* `qos_adaptive_policy_group_template` - _extreme_ ( if running ONTAP X and neither qos_policy_group_template nor qos_adaptive_policy_group_template are provided)
### Related ONTAP commands
* `vserver create`
* `vserver add-aggregates`
* `network interface create`
* `network route create`
* `vserver services name-service dns create`
* `vserver nfs create`
* `vserver services name-service ldap client create`
* `vserver cifs create`
* `vserver services name-service nis-domain create`
* `vserver iscsi create`
* `vserver nvme create`
* `vserver fcp create`
* `vserver services name-service ns-switch create`
* `vserver object-store-server create`
* `vserver add-protocols`
* `vserver remove-protocols`
### Examples
1. Creates an SVM with default "snapshot_policy"
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}}'
    ```
    <br/>
2. Creates an SVM and configures NFS, ISCSI and FCP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nfs":{"enabled":"true"}, "fcp":{"enabled":"true"}, "iscsi":{"enabled":"true"}}'
    ```
    <br/>
3. Creates an SVM and configures NVMe
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nvme":{"enabled":"true"}}'
    ```
    <br/>
4. Creates an SVM and configures LDAP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "ldap":{"servers":["10.140.101.1","10.140.101.2"], "ad_domain":"abc.com", "base_dn":"dc=netapp,dc=com", "bind_dn":"dc=netapp,dc=com"}}'
    ```
    <br/>
5. Creates an SVM and configures NIS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "nis":{"enabled":"true", "domain":"def.com","servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
6. Creates an SVM and configures DNS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "dns":{"domains":["abc.com","def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
7. Creates an SVM and configures a LIF
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
8. Creates an SVM and configures a LIF with IPV6 address
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif2", "ip":{"address":"fd22:8b1e:b255:202:2a0:98ff:fe01:7d5b", "netmask":"24"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
9. Creates an SVM and configures CIFS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "cifs":{"name":"CIFDOC", "ad_domain":{"fqdn":"abc.def.com", "organizational_unit":"CN=Computers", "user":"cif_admin", "password":"abc123"}}, "ip_interfaces":[{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}],"routes": [{"destination": {"address": "0.0.0.0", "netmask": "0"}, "gateway": "10.10.10.7"}], "dns":{"domains":["abc.def.com", "def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
10. Creates an SVM with an S3 server enabled and configured
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"svm5", "s3":{"name":"s3-server-1", "enabled":true, "allowed":true, "is_http_enabled": true, "is_https_enabled":false}}'
    ```
    <br/>
11. Creates an SVM and disallows NVMe service for the SVM
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nvme":{"allowed":"false"}}'
    ```
    <br/>
12. Creates an SVM, allows and configures the NFS service for the SVM
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nfs":{"allowed":"true", "enabled":true}}'
    ```
    <br/>
13. Create an SVM and set the max volume limit for the SVM
    <br/>
    ```
    POST "/api/svm/svms/" '{"name":"testVs", "max_volumes":"200"}'
    ```
    <br/>
14. Creates an SVM and disallows the NDMP service for the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ndmp":{"allowed":"false"}}'
    ```
    <br/>
15. Creates an SVM and specifies whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_analytics":true}}'
    ```
    <br/>
16. Creates an SVM and specifies whether volume_activity_tracking is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_activity_tracking":true}}'
    ```
    <br/>
17. Creates an SVM and specifies whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "auto_enable_analytics":true}}'
    ```
    <br/>
18. Creates an SVM and specifies the maximum storage limit for a single SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "storage": {"limit":"4GB"}}'
    ```
    <br/>
19. Creates an SVM and specifies at what percentage of storage capacity an alert message is sent. Default value is 90.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "storage": {"limit":"20GB", "limit_threshold_alert":"95"}}'
    ```
    <br/>
20. Creates an SVM and specifies the QoS policy group template to be assigned to the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "qos_policy_group_template":{"name":"performance-fixed"}}'
    ```
    <br/>
21. Creates an SVM and specifies the QoS adaptive policy group template to be assigned to the SVM.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "qos_adaptive_policy_group_template":{"name":"performance"}}'
    ```
    <br/>
22. On ASA r2 platforms, _fcp_, _iscsi_, and _nvme_ services are enabled and allowed by default, and are not necessary in the POST request.
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs"}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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
        r"""Updates one or more of the following properties of an individual SVM: SVM name, SVM default volume language code, SVM comment, and SVM state.
### Related ONTAP commands
* `vserver modify`
* `vserver rename`
* `vserver start`
* `vserver stop`
* `security ssl modify`
* `vserver add-protocols`
* `vserver remove-protocols`
### Examples
1.  Stops an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"stopped", "comment":"This SVM is stopped."}'
    ```
    <br/>
2.  Starts an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"running", "comment":"This SVM is running."}'
    ```
    <br/>
3.  Updates the "language" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"language":"en.UTF-8"}'
    ```
    <br/>
4.  Updates the "name" field for an SVM or renames the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"name":"svm_new"}'
    ```
    <br/>
5.  Updates the aggregates for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"aggregates":["{"name":aggr1"},{"name":"aggr2"},{"name":"aggr3"}]}'
    ```
    <br/>
6.  Updates the snapshot policy for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"snapshot_policy":{"name":"custom1"}}'
    ```
    <br/>
7.  Updates the TLS certificate for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"certificate":{"uuid":"1cd8a442-86d1-11e0-ae1c-123478563412"}}'
    ```
    <br/>
8.  Updates the QoS policy for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_policy_group":{"name":"qpolicy1"}}'
    ```
    <br/>
9.  Allows NFS protocol which was previously disallowed for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"nfs":{"allowed":"true"}}'
    ```
    <br/>
10. Updates the max volume limit for the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"max_volumes":"200"}'
    ```
    <br/>
11. Updates whether file system analytics is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"auto_enable_analytics":"true"}'
    ```
    <br/>
12. Updates whether volume activity tracking is enabled on all newly created volumes in the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"auto_enable_activity_tracking":"true"}'
    ```
    <br/>
13. Updates the QoS adaptive policy group template for the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_adaptive_policy_group_template":{"name":"aqpolicy1"}}'
    ```
    <br/>
14. Updates the maximum storage permitted on a single SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"storage":{"limit":"40GB"}}'
    ```
    <br/>
15. Updates the percentage of storage capacity at which an alert message is sent.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"storage":{"limit":"400MB", "limit_threshold_alert":"98"}}'
    ```
    <br/>
16. Updates the QoS policy group template for the SVM.
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"qos_policy_group_template":{"name":"policy1"}}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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
        r"""Deletes an SVM. As a prerequisite, SVM objects must be deleted first. SnapMirror relationships must be deleted and data volumes must be offline and deleted.
* The number of parallel SVMs that can be created must not be greater than five.
* If a sixth SVM POST request is issued, the following error message is generated: "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again."
### Related ONTAP commands
* `vserver delete`
### Example
Deleting an individual SVM in the cluster.
  <br/>
  ```
  DELETE "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
  ```
  <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


